#!/usr/bin/env python3
"""Optimize physical/calendar mixtures with exact Qout cut separation.

The small LP has one probability per admitted calendar and one row per
observed Qout cut. Its objective is NOT a global lower bound. Each proposed
rational physical mixture is checked against every Princess by an exact
integer closure oracle. The LP dual mixes the admitted cuts into a feasible
field for discovering additional physical paths and causal calendars.
"""
from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
import json
import os
from pathlib import Path
import platform
import random
import shutil
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
for folder in ("interval_clock_grid/normalized_native","interval_discovery","interval_monster_boundary","interval_sparse_upper"):
    sys.path.insert(0,str(ROOT/"packages"/folder))
import numpy as np
import scipy
from scipy.optimize import linprog
from scipy.sparse import coo_matrix,csr_matrix,hstack,vstack,eye
from solve_normalized import Master
from cached_path_pricing import CachedPathPricing
from monster_search import digest, lift_plan, mutate_routes, read_json, restore_rng, write_json
from master import SparseMaster, projected_order, plan_column
# The same-named search module in the boundary package is loaded explicitly.
import importlib.util
_spec = importlib.util.spec_from_file_location("boundary_discovery",ROOT/"packages/interval_monster_boundary/search.py")
_boundary = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_boundary)
boundary_routes,seed_values,endpoint_diagnostic = _boundary.boundary_routes,_boundary.seed_values,_boundary.endpoint_diagnostic

HERE = Path(__file__).resolve().parent
_retention_spec=importlib.util.spec_from_file_location("mixture_princess_retention",HERE/"princess_retention.py")
_retention=importlib.util.module_from_spec(_retention_spec);_retention_spec.loader.exec_module(_retention)
CompleteBankArchive=_retention.CompleteBankArchive
_physical_spec=importlib.util.spec_from_file_location("mixture_physical_screen",HERE/"physical_screen.py")
_physical=importlib.util.module_from_spec(_physical_spec);_physical_spec.loader.exec_module(_physical)


def rationalize(weights, denominator=10**12):
    positive = np.maximum(0.,np.asarray(weights,dtype=float))
    total = float(positive.sum())
    if not np.isfinite(total) or total <= 0:
        raise ValueError("invalid probability vector")
    scaled = positive/total*denominator
    result = [int(x) for x in scaled]
    remainder = denominator-sum(result)
    if not 0 <= remainder <= len(result):
        raise ValueError("rounding remainder")
    order = sorted(range(len(result)),key=lambda i:(-(scaled[i]-result[i]),i))
    for i in order[:remainder]:
        result[i] += 1
    return result


class ClosureServer:
    def __init__(self):
        self.process = subprocess.Popen(["node","--stack-size=16384",str(HERE/"closure_server.cjs")],
            stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,bufsize=1)

    def ask(self, request):
        self.process.stdin.write(json.dumps(request,separators=(",", ":"))+"\n")
        self.process.stdin.flush()
        line = self.process.stdout.readline()
        if not line:
            raise RuntimeError("closure server stopped: "+self.process.stderr.read())
        result = json.loads(line)
        if result.get("status") == "ERROR":
            raise RuntimeError(result["error"])
        return result

    def close(self):
        if self.process.poll() is None:
            self.ask({"command":"stop"})
            self.process.stdin.close()
            self.process.wait(timeout=10)


def make_closure_server(directory,native=False):
    if native:
        sys.path.insert(0,str(ROOT/"packages/interval_integer_flow"))
        from native_closure import NativeClosureServer
        return NativeClosureServer(directory)
    return ClosureServer()


class CutBank:
    def __init__(self, master):
        self.master = master
        self.packed,self.seen = [],set()
        self.base_profiles,self.base_seen = [],set()
        self.matrix = None
        self.costs = np.empty((0,0),dtype=np.int64)
        self.columns = -1

    def sync_columns(self):
        master = self.master
        if self.columns == len(master.columns):
            return
        rr,cc,vv = [],[],[]
        for row,c in enumerate(master.columns):
            for i,v in c["coeff"].items():
                rr.append(row);cc.append(i);vv.append(v)
        self.matrix = coo_matrix((np.asarray(vv,dtype=np.int64),(rr,cc)),
            shape=(len(master.columns),master.K),dtype=np.int64).tocsr()
        self.mass = np.asarray([c["mass"] for c in master.columns],dtype=np.int64)
        self.costs = np.asarray([self.row(self.unpack(p)) for p in self.packed],dtype=np.int64)
        if not len(self.packed):
            self.costs = np.empty((0,len(master.columns)),dtype=np.int64)
        self.base_costs=np.asarray([(self.mass+self.matrix@p)/(4*master.n) for p in self.base_profiles])
        if not self.base_profiles:self.base_costs=np.empty((0,len(master.columns)))
        self.columns = len(master.columns)

    def unpack(self, packed):
        return np.unpackbits(packed,count=self.master.K)

    def row(self, field):
        return self.mass+self.matrix@field.astype(np.int64)

    def add(self, field):
        field = np.asarray(field,dtype=np.uint8)
        if field.shape != (self.master.K,) or np.any(field>1):
            raise ValueError("cut must be a binary full profile")
        packed = np.packbits(field)
        key = hashlib.sha256(packed.tobytes()).hexdigest()
        if key in self.seen:
            return False
        self.seen.add(key);self.packed.append(packed)
        self.costs = np.vstack((self.costs,self.row(field)))
        return True

    def add_base(self, field):
        """Retain a supplied feasible nonbinary field without quantile sampling loss."""
        field=np.asarray(field,dtype=float)
        if field.shape!=(self.master.K,) or np.any(field<0) or np.any(field>1):
            raise ValueError("invalid supplied Qout field")
        if any(field[a]>field[b]+1e-12 for a,b in self.master.order):
            raise ValueError("supplied field violates Qout order")
        key=hashlib.sha256(field.tobytes()).hexdigest()
        if key in self.base_seen:return False
        self.base_seen.add(key);self.base_profiles.append(field.copy())
        self.base_costs=np.vstack((self.base_costs,(self.mass+self.matrix@field)/(4*self.master.n)))
        return True

    def response_matrix(self):
        return np.vstack((self.base_costs,self.costs.astype(float)/(4*self.master.n)))

    def solve(self, seconds):
        self.sync_columns()
        M = len(self.master.columns)
        costs=self.response_matrix()
        matrix = np.c_[costs,-np.ones(costs.shape[0])]
        result = linprog(np.r_[np.zeros(M),1.],A_ub=matrix,b_ub=np.zeros(costs.shape[0]),
            A_eq=np.asarray([np.r_[np.ones(M),0.]]),b_eq=[1.],
            bounds=[(0.,1.)]*M+[(0.,2.)],method="highs-ds",
            options={"time_limit":seconds,"primal_feasibility_tolerance":1e-9,"dual_feasibility_tolerance":1e-9})
        if not result.success:
            raise RuntimeError(result.message)
        return result

    def dual_field(self, result):
        weights = np.maximum(0.,-np.asarray(result.ineqlin.marginals))
        if weights.sum() <= 0:
            raise ValueError("empty cut dual")
        weights /= weights.sum()
        field = np.zeros(self.master.K)
        for w,p in zip(weights,self.base_profiles):
            if w>0:field+=w*p
        for w,p in zip(weights[len(self.base_profiles):],self.packed):
            if w > 0:
                field += w*self.unpack(p)
        return field

    def stabilized_weights(self, best, level, seconds):
        """Nearest retained physical mixture in a promising cut-model level."""
        M=len(self.master.columns)
        best=np.r_[best,np.zeros(M-len(best))]
        costs=csr_matrix(self.response_matrix())
        identity=eye(M,format="csr")
        matrix=vstack((hstack((costs,csr_matrix((costs.shape[0],M)))),
                       hstack((identity,-identity)),hstack((-identity,-identity))),format="csr")
        answer=linprog(np.r_[np.zeros(M),np.ones(M)],A_ub=matrix,
            b_ub=np.r_[np.full(costs.shape[0],level),best,-best],
            A_eq=csr_matrix(np.asarray([np.r_[np.ones(M),np.zeros(M)]])),b_eq=[1.],
            bounds=[(0.,1.)]*(2*M),method="highs-ds",
            options={"time_limit":seconds,"primal_feasibility_tolerance":1e-9,"dual_feasibility_tolerance":1e-9})
        return answer


def load_model(server, master, path):
    nodes = sorted({master.nodes[i] for c in master.columns for i in c["coeff"]})
    order = projected_order(master.n,nodes)
    write_json(path,{"n":master.n,"columns":[{"plan":c["plan"]} for c in master.columns],
                     "qout_nodes":nodes,"qout_order":order})
    report = server.ask({"command":"load","path":str(path)})
    extension = SparseMaster(master.n,1)
    extension.nodes = nodes
    return extension,report


def source_cut(master, law):
    """Exactly lift the retained full-grid maximizing cut to the target grid."""
    sn = law["n"]
    ratio = master.n//sn
    if "qout_nodes" in law:
        nodes = [tuple(p) for p in law["qout_nodes"]]
    else:
        nodes = [(j,k) for j in range(4*sn+1) for k in range(1,2*sn+1) if (j+k)%2 == 0]
    side = set(law["closure_source_side"])
    extension = SparseMaster(master.n,1)
    extension.nodes = [(j*ratio,k*ratio) for j,k in nodes]
    table = extension.extend_integer([int(i in side) for i in range(len(nodes))])
    return np.asarray([table[j,k] for j,k in master.nodes],dtype=np.uint8)


def law_weights(master, law):
    """Represent an exactly retained law in the admitted calendar columns."""
    def key(mass,coeff):return mass,tuple(sorted(coeff.items()))
    lookup={key(c["mass"],{master.nodes[i]:v for i,v in c["coeff"].items()}):i for i,c in enumerate(master.columns)}
    result=np.zeros(len(master.columns))
    ratio=master.n//law["n"]
    for p in law["paths"]:
        mass,coeff=plan_column(master.n,lift_plan(p,ratio))
        result[lookup[key(mass,coeff)]]+=int(p["weight_numerator"])/int(law["weight_denominator"])
    if abs(result.sum()-1)>1e-9:raise ValueError("retained law is not represented")
    return result


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--n",type=int,default=256)
    ap.add_argument("--initial-law",type=Path,default=ROOT/"packages/interval_discovery_certificates/monster_mutations_n128.physical.json.gz")
    ap.add_argument("--profile-seed",type=Path,default=ROOT/"packages/interval_clock_grid/lower_n256_field.json")
    ap.add_argument("--resume",type=Path)
    ap.add_argument("--iterations",type=int,default=160)
    ap.add_argument("--seconds",type=float,default=3600)
    ap.add_argument("--lp-seconds",type=float,default=120)
    ap.add_argument("--seed",type=int,default=693147)
    ap.add_argument("--initial-cuts",type=int,default=24)
    ap.add_argument("--boundary-points",type=int,default=32)
    ap.add_argument("--pricing-paths",type=int,default=128)
    ap.add_argument("--price-every",type=int,default=8)
    ap.add_argument("--full-every",type=int,default=0,help="Complete native pricing every this many pricing rounds; 0 skips it")
    ap.add_argument("--mutation-count",type=int,default=128)
    ap.add_argument("--level-fraction",type=float,default=.5,
                    help="Mixture-level stabilization toward retained law; 1 uses the raw cut LP")
    ap.add_argument("--alternative-cuts",type=int,default=4,
                    help="Additional exactly maximizing residual-closed cuts per integer flow")
    ap.add_argument("--native-flow",action="store_true",
                    help="Checked native flow optimizer; original BigInt physical/edge/flow/cut replay remains mandatory")
    ap.add_argument("--loop-screen",action="store_true",
                    help="Separate all one-turn endpoint-loop clock fields cheaply; distinguish actual physical defeat from calendar-only rejection")
    ap.add_argument("--output",type=Path,required=True)
    args = ap.parse_args()
    if min(args.n,args.iterations,args.initial_cuts,args.boundary_points,args.pricing_paths,args.price_every)<1 or min(args.seconds,args.lp_seconds)<=0 or args.full_every<0 or args.mutation_count<0 or not 0<args.level_fraction<=1 or not 0<=args.alternative_cuts<=64:
        ap.error("invalid positive search limits")
    out = args.output.resolve();out.mkdir(parents=True,exist_ok=True)
    began = time.monotonic();rng = random.Random(args.seed)
    args_dict = {k:str(v) if isinstance(v,Path) else v for k,v in vars(args).items()}
    log = (out/"solver.jsonl").open("a",buffering=1)
    def emit(data):
        data["elapsed_seconds"] = time.monotonic()-began
        line = json.dumps(data,separators=(",", ":"));print(line,flush=True);log.write(line+"\n")
    law = read_json(args.initial_law)
    if args.n % law["n"]:
        ap.error("n must refine the initial physical law")
    master = Master(args.n,out/"work")
    for p in law["paths"]:
        master.add_plan(lift_plan(p,args.n//law["n"]))
    history = [];resume = None
    if args.resume:
        resume = read_json(args.resume)
        if resume["n"] != args.n:
            ap.error("cut resume requires the same target grid")
        for c in resume["columns"]:
            master.add_plan(c["plan"])
        history = resume.get("history",[])
        if resume.get("rng_state"):
            rng.setstate(restore_rng(resume["rng_state"]))
    cache = CachedPathPricing(args.n,master.D)
    cache.update_columns(master.columns)
    new_routes = cache.add_many(boundary_routes(args.n,args.boundary_points))
    seed_profile = seed_values(master,args.profile_seed)
    seed_table = master.repair(seed_profile)
    seed_profile = master.profile_values(seed_table)
    selected = cache.price(seed_table,keep=args.pricing_paths)
    before = len(master.columns)
    for route in selected["paths"]:
        master.add(route,seed_table)
    cuts = CutBank(master);cuts.sync_columns()
    cuts.add_base(seed_profile)
    cuts.add(np.zeros(master.K,dtype=np.uint8));cuts.add(np.ones(master.K,dtype=np.uint8))
    cuts.add(source_cut(master,law))
    for i in range(1,args.initial_cuts+1):
        cuts.add((seed_profile>=i/(args.initial_cuts+1)).astype(np.uint8))
    if resume is not None and resume.get("cut_archive"):
        archive = args.resume.resolve().parent/resume["cut_archive"]
        if digest(archive) != resume["cut_archive_sha256"]:
            raise ValueError("resume cut hash mismatch")
        with np.load(archive,allow_pickle=False) as saved:
            if "base_profiles" in saved:
                for field in saved["base_profiles"]:cuts.add_base(field)
            for packed in saved["packed"]:
                cuts.add(cuts.unpack(packed))
    emit({"event":"initialized","n":args.n,"calendars":len(master.columns),"cuts":len(cuts.packed),
          "new_boundary_routes":new_routes,"new_seed_calendars":len(master.columns)-before,
          "scope":"Restricted cut LP has no global lower-bound meaning; every reported physical upper is independently exact."})
    sources = [Path(__file__),HERE/"closure_server.cjs",ROOT/"packages/interval_sparse_upper/master.py",
               ROOT/"packages/interval_sparse_upper/sparse_certificate.cjs",ROOT/"packages/interval_monster_boundary/search.py",
               ROOT/"packages/interval_clock_grid/qout_primal_certificate.cjs",ROOT/"packages/interval_clock_grid/exact_certificate.cjs",
               ROOT/"packages/interval_clock_grid/normalized_native/solve_normalized.py",ROOT/"packages/interval_clock_grid/normalized_native/cached_path_pricing.py",
               HERE/"physical_screen.py",HERE/"princess_retention.py",
               ROOT/"packages/interval_clock_grid/normalized_native/price_normalized.cpp",
               ROOT/"packages/interval_clock_grid/normalized_native/verify_native_field.py"]
    if args.native_flow:
        sources.extend(ROOT/"packages/interval_integer_flow"/name for name in ("maximum_flow.cpp","native_server.cjs","native_closure.py"))
    write_json(out/"metadata.json",{"options":args_dict,"initial_law_sha256":digest(args.initial_law),
        "profile_seed_sha256":digest(args.profile_seed),"source_sha256":{str(p.relative_to(ROOT)):digest(p) for p in sources},
        "github_sha":os.getenv("GITHUB_SHA"),"github_run_id":os.getenv("GITHUB_RUN_ID"),
        "resume_sha256":digest(args.resume) if args.resume else None,"python_version":platform.python_version(),
        "numpy_version":np.__version__,"scipy_version":scipy.__version__,
        "node_version":subprocess.run(["node","--version"],check=True,capture_output=True,text=True).stdout.strip()})
    princess_archive=CompleteBankArchive(out,args.resume.resolve().parent if args.resume else None)
    write_json(out/"seed.physical.json",law)
    original_verifier = ROOT/"packages/interval_sparse_upper/sparse_certificate.cjs" if "qout_nodes" in law else ROOT/"packages/interval_clock_grid/qout_primal_certificate.cjs"
    verification = subprocess.run(["node","--stack-size=16384",str(original_verifier),str(out/"seed.physical.json")],check=True,capture_output=True,text=True)
    write_json(out/"seed.replay.json",json.loads(verification.stdout))
    target_seed={"n":args.n,"weight_denominator":law["weight_denominator"],
        "paths":[dict(lift_plan(p,args.n//law["n"]),weight_numerator=p["weight_numerator"]) for p in law["paths"]]}
    seed_diagnostic,seed_marginals=_physical.analyze_physical_law(target_seed)
    if seed_diagnostic["endpoint_loop_supported"]:
        seed_diagnostic["maximum_clock_only_improvement"]=str(Fraction(law["global_upper"])-Fraction(seed_diagnostic["endpoint_loop_supremum_lower"]))
    write_json(out/"seed.physical_diagnostic.json",seed_diagnostic)
    emit({"event":"seed_geometry_diagnostic",**seed_diagnostic})
    best_upper = Fraction(law["global_upper"]);best_certificate = "seed.physical.json"
    best_weights=law_weights(master,law)
    if resume is not None:
        prior = args.resume.resolve().parent/"best.sparse.json"
        if prior.exists():
            old_law = read_json(prior)
            verification = subprocess.run(["node","--stack-size=16384",str(ROOT/"packages/interval_sparse_upper/sparse_certificate.cjs"),str(prior)],check=True,capture_output=True,text=True)
            if Fraction(old_law["global_upper"]) < best_upper:
                best_upper = Fraction(old_law["global_upper"]);best_certificate="best.sparse.json"
                best_weights=law_weights(master,old_law)
                if prior != out/"best.sparse.json":shutil.copyfile(prior,out/"best.sparse.json")
                write_json(out/"best.replay.json",json.loads(verification.stdout))
    server = make_closure_server(out/"work",args.native_flow);extension = None;loaded_columns = -1
    if args.native_flow:
        write_json(out/"native_optimizer.json",{"binary_sha256":digest(server.binary),
            "scope":"Untrusted optimizer only. Original BigInt physical, calendar, geometric-edge, flow and cut replay remains mandatory."})
    status,reason = "COMPLETED","iteration_limit"
    latest_weights = np.zeros(len(master.columns))
    pricing_round = int(resume.get("pricing_round",sum("cached_minimum_only" in r for r in history))) if resume else 0
    loop_rejections = sum(r.get("candidate_rejected_before_closure",False) for r in history)
    clock_loop_rejections=sum(r.get("rejection_scope")=="calendar_mixture" for r in history)
    loop_rejections-=clock_loop_rejections
    loop_separator=_physical.EndpointLoopSeparator(master) if args.loop_screen else None
    def add_oracle_cuts(answer, numerators):
        added=0
        for side in [answer["source_side"]]+answer.get("alternative_source_sides",[]):
            cut=np.zeros(len(extension.nodes),dtype=np.uint8);cut[side]=1
            table=extension.extend_integer(cut)
            field=np.asarray([table[j,k] for j,k in master.nodes],dtype=np.uint8)
            row=cuts.row(field)
            # Each residual-closed cut is independently checked against the
            # exact objective after extending it to the full Qout field.
            witnessed=Fraction(sum(int(a)*q for a,q in zip(row,numerators)),4*args.n*10**12)
            if witnessed!=Fraction(answer["global_upper"]):
                raise AssertionError("projected maximizing cut changed under exact full-field extension")
            added+=int(cuts.add(field))
        return added
    def save_checkpoint():
        archive = out/"cuts.npz"
        np.savez_compressed(archive,packed=np.asarray(cuts.packed,dtype=np.uint8),base_profiles=np.asarray(cuts.base_profiles))
        write_json(out/"checkpoint.json",{"scope":"Cut/mixture discovery; restricted cut values are not game lower bounds.",
            "n":args.n,"columns":master.columns,"weights":np.r_[latest_weights,np.zeros(len(master.columns)-len(latest_weights))].tolist(),
            "history":history,"rng_state":rng.getstate(),"options":args_dict,
            "cut_archive":archive.name,"cut_archive_sha256":digest(archive),"best_certified_global_upper":str(best_upper),
            "pricing_round":pricing_round,"initial_law_sha256":digest(args.initial_law),
            "complete_princess_candidates":len(princess_archive.candidates),
            "best_complete_bank_pointer":"best_complete_bank.json" if princess_archive.candidates else None})
    def price_routes(lp,report):
        nonlocal pricing_round
        pricing_round+=1
        trial=cuts.dual_field(lp)
        priced_table=master.repair(trial)
        cache.update_columns(master.columns)
        active=[c["plan"] for c,w in zip(master.columns,latest_weights) if w>1e-9]
        if active and args.mutation_count:
            report["new_bulk_routes"]=cache.add_many(mutate_routes(args.n,active,rng,args.mutation_count))
        selected=cache.price(priced_table,keep=args.pricing_paths,level=float(lp.fun),tolerance="1e-8")
        before=len(master.columns)
        for route in selected["violating_paths"]:
            master.add(route,priced_table)
        report["new_cached_calendars"]=len(master.columns)-before
        report["pricing_field"]="dual mixture of admitted exact Qout cuts"
        report["cached_minimum_only"]=str(Fraction(int(selected["cached_minimum_units"]),4*args.n*master.D))
        if args.full_every and pricing_round%args.full_every==0:
            emit({"event":"complete_pricing_start","pricing_round":pricing_round,"n":args.n})
            answer,priced_table=master.price(trial,keep=args.pricing_paths)
            retained=princess_archive.retain(master,priced_table,answer,pricing_round,out/"metadata.json")
            cache.add_many(answer["paths"])
            before=len(master.columns)
            for route in answer["paths"]:master.add(route,priced_table)
            report["new_complete_calendars"]=len(master.columns)-before
            report["complete_exact_bank_minimum"]=str(Fraction(int(answer["minimum_units"]),4*args.n*master.D))
            report["complete_princess_candidate"]=retained
    save_checkpoint()
    try:
        for iteration in range(args.iterations):
            if time.monotonic()-began>=args.seconds:
                status,reason="BUDGET_STOPPED","wall_time_limit";break
            cuts.sync_columns()
            if loaded_columns != len(master.columns):
                extension,model_report = load_model(server,master,out/"oracle.model.json")
                loaded_columns = len(master.columns)
                emit({"event":"closure_model",**model_report})
                anchor_numerators=rationalize(np.r_[best_weights,np.zeros(len(master.columns)-len(best_weights))])
                anchor=server.ask({"weights":list(map(str,anchor_numerators)),"denominator":str(10**12),
                    "prefix":str(out/"oracle.anchor"),"alternative_cuts":args.alternative_cuts,"seed":args.seed+len(history)})
                anchor_added=add_oracle_cuts(anchor,anchor_numerators)
                emit({"event":"active_face_cuts","new_cuts":anchor_added,"exact_anchor_upper":anchor["global_upper"],"closure_seconds":anchor["seconds"]})
            lp_began=time.monotonic();lp=cuts.solve(args.lp_seconds);lp_seconds=time.monotonic()-lp_began
            latest_weights=lp.x[:-1]
            stabilizer=None
            if args.level_fraction<1 and float(best_upper)-lp.fun>2e-8:
                level=lp.fun+args.level_fraction*(float(best_upper)-lp.fun)
                stabilizer=cuts.stabilized_weights(best_weights,level,args.lp_seconds)
                if stabilizer.success:latest_weights=stabilizer.x[:len(master.columns)]
            numerator=rationalize(latest_weights)
            query={"weights":[str(q) for q in numerator],"denominator":str(10**12),"prefix":str(out/"oracle.current"),
                "alternative_cuts":args.alternative_cuts,"seed":args.seed+len(history)}
            proposal=_physical.candidate_law(master,numerator)
            physical_diagnostic,physical_marginals=_physical.analyze_physical_law(proposal)
            physical_change=_physical.marginal_change(physical_marginals,seed_marginals)
            loop_report=None
            if args.loop_screen:
                screened=_physical.loop_cut(master,physical_diagnostic,best_upper+Fraction(1,10**8))
                if screened is not None:
                    field,loop_report=screened
                    row=cuts.row(field)
                    cost=Fraction(sum(int(a)*q for a,q in zip(row,numerator)),4*args.n*10**12)
                    if cost<Fraction(loop_report["actual_physical_loop_payoff"]):
                        raise AssertionError("loop field clock plane is below the independently known physical payoff")
                    loop_report["exact_clock_plane_value"]=str(cost)
                    loop_report["new_feasible_field_cut"]=bool(cuts.add(field))
                    if loop_report["new_feasible_field_cut"]:
                        loop_rejections+=1
                        report={"event":"physical_loop_rejected","iteration":len(history),
                            "candidate_rejected_before_closure":True,"calendars":len(master.columns),"cuts":len(cuts.packed),
                            "rejection_scope":"physical_mixture",
                            "restricted_cut_lp_estimate":float(lp.fun),"lp_seconds":lp_seconds,
                            "physical_diagnostic":physical_diagnostic,"physical_change":physical_change,"loop_screen":loop_report}
                        write_json(out/"last_physical_rejection.json",{"scope":"Rejected rational proposal; no upper certificate is claimed.",
                            "model_sha256":digest(out/"oracle.model.json"),"weights":query["weights"],"denominator":query["denominator"],
                            "diagnostic":physical_diagnostic,"loop_witness":loop_report})
                        if (iteration+1)%args.price_every==0:price_routes(lp,report)
                        history.append(report);emit(report);save_checkpoint();continue
            rectangle_report=None
            if args.loop_screen:
                rectangle_report=loop_separator.maximize(cuts,numerator,10**12)
                if Fraction(rectangle_report["clock_plane_value"])>best_upper+Fraction(1,10**8):
                    field=_physical.rectangle_field(master,rectangle_report["a"],rectangle_report["b"])
                    row=cuts.row(field)
                    exact_row=Fraction(sum(int(a)*q for a,q in zip(row,numerator)),4*args.n*10**12)
                    if exact_row!=Fraction(rectangle_report["clock_plane_value"]):
                        raise AssertionError("endpoint rectangle suffix sum disagrees with the full clock plane")
                    if cuts.add(field):
                        actual=_physical.rectangle_loop_payoff(proposal,rectangle_report["a"],rectangle_report["b"])
                        if actual>exact_row:raise AssertionError("actual endpoint loop exceeds its clock majorant")
                        physical_rejection=actual>best_upper
                        if physical_rejection:loop_rejections+=1
                        else:clock_loop_rejections+=1
                        rectangle_report["actual_physical_loop_payoff"]=str(actual)
                        rectangle_report["actual_payoff_exceeds_incumbent"]=physical_rejection
                        report={"event":"endpoint_loop_cut_rejected","iteration":len(history),
                            "candidate_rejected_before_closure":True,"rejection_scope":"physical_mixture" if physical_rejection else "calendar_mixture",
                            "calendars":len(master.columns),"cuts":len(cuts.packed),"restricted_cut_lp_estimate":float(lp.fun),
                            "lp_seconds":lp_seconds,"physical_diagnostic":physical_diagnostic,"physical_change":physical_change,
                            "endpoint_loop_separation":rectangle_report}
                        write_json(out/"last_loop_cut_rejection.json",{"scope":"Rejected rational calendar proposal. The separately computed actual loop payoff determines whether its physical mixture is also defeated; no upper certificate is claimed.",
                            "model_sha256":digest(out/"oracle.model.json"),"weights":query["weights"],"denominator":query["denominator"],
                            "diagnostic":physical_diagnostic,"separation":rectangle_report})
                        if (iteration+1)%args.price_every==0:price_routes(lp,report)
                        history.append(report);emit(report);save_checkpoint();continue
            exact=server.ask(query)
            upper=Fraction(exact["global_upper"])
            new_cut=add_oracle_cuts(exact,numerator)
            report={"event":"iteration","iteration":len(history),"calendars":len(master.columns),
                "cuts":len(cuts.packed),"restricted_cut_lp_estimate":float(lp.fun),
                "exact_unrestricted_upper":str(upper),"separation_gap_estimate":float(upper)-float(lp.fun),
                "new_cuts":new_cut,"lp_seconds":lp_seconds,"closure_seconds":exact["seconds"],
                "closure_nodes":exact["closure_nodes"],"closure_arcs":exact["closure_arcs"],
                "physical_diagnostic":physical_diagnostic,"physical_change":physical_change}
            if loop_report is not None:report["loop_screen"]=loop_report
            if rectangle_report is not None:report["endpoint_loop_separation"]=rectangle_report
            if physical_diagnostic["endpoint_loop_supported"]:
                residual=upper-Fraction(physical_diagnostic["endpoint_loop_supremum_lower"])
                if residual<0:raise AssertionError("certified upper below actual endpoint-loop response")
                report["upper_minus_fixed_law_loop_floor"]=str(residual)
            if stabilizer is not None:
                report["mixture_stabilization"]={"success":bool(stabilizer.success),"level":level,
                    "l1_change":float(stabilizer.fun) if stabilizer.success else None}
            if upper<best_upper:
                best_upper=upper;best_certificate="best.sparse.json"
                best_weights=np.asarray(numerator,dtype=float)/10**12
                for suffix in (".sparse.json",".replay.json"):
                    shutil.copyfile(out/("oracle.current"+suffix),out/("best"+suffix))
                write_json(out/"best.weights.json",query)
                write_json(out/"best.endpoint_diagnostic.json",endpoint_diagnostic(read_json(out/"best.sparse.json")))
                write_json(out/"best.physical_diagnostic.json",{**physical_diagnostic,**physical_change})
                report["new_best_certified_upper"]=str(upper)
            if (iteration+1)%args.price_every==0 or float(upper)-float(lp.fun)<1e-7 or not new_cut:
                price_routes(lp,report)
            history.append(report);emit(report);save_checkpoint()
    except RuntimeError as error:
        if "time limit" not in str(error).lower() and "time_limit" not in str(error).lower():
            status,reason="FAILED","runtime_failure";raise
        status,reason="BUDGET_STOPPED","small_lp_time_limit";emit({"event":"budget_stop","error":str(error)})
    except Exception:
        status,reason="FAILED","unexpected_failure";raise
    finally:
        server.close();save_checkpoint()
        summary={"status":status,"stop_reason":reason,"iterations_total":len(history),
            "best_certified_global_upper":str(best_upper),"baseline_global_upper":law["global_upper"],
            "certified_improvement":str(Fraction(law["global_upper"])-best_upper),"best_certificate":best_certificate,
            "exact_physical_loop_rejections":loop_rejections,"exact_calendar_loop_rejections":clock_loop_rejections,
            "completed_candidate_certifications":sum("exact_unrestricted_upper" in r for r in history),"native_flow":args.native_flow,
            "retained_complete_princess_candidates":len(princess_archive.candidates),
            "best_complete_bank_pointer":"best_complete_bank.json" if princess_archive.candidates else None,
            "scope":"Only exact replayed physical uppers have unrestricted meaning. Restricted-cut LP values are not global lower bounds.",
            "elapsed_seconds":time.monotonic()-began}
        write_json(out/"summary.json",summary);emit({"event":"complete",**summary});log.close()
        files={str(p.relative_to(out)):digest(p) for p in out.rglob("*") if p.is_file() and "work" not in p.relative_to(out).parts and p.name!="manifest.json"}
        write_json(out/"manifest.json",{**summary,"options":args_dict,"files_sha256":files,"source_metadata":"metadata.json"})


if __name__=="__main__":main()
