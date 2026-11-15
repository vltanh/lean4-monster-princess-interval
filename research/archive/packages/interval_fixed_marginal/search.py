#!/usr/bin/env python3
"""Optimize causal calendars while preserving a rational physical law exactly."""
from __future__ import annotations

import argparse
from collections import defaultdict
from fractions import Fraction
import gzip
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import time

ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location("mixture_cut",ROOT/"packages/interval_mixture_cut/search.py")
C=importlib.util.module_from_spec(spec);sys.modules["mixture_cut"]=C;spec.loader.exec_module(C)
import numpy as np
import scipy
from scipy.optimize import linprog
from scipy.sparse import coo_matrix,csr_matrix,hstack,vstack,eye


def route_key(plan):return int(plan["start_grid"]),tuple(map(int,plan["moves"]))


def physical_marginals(law):
    masses=defaultdict(int)
    for p in law["paths"]:masses[route_key(p)]+=int(p["weight_numerator"])
    return dict(masses)


class FixedMaster(C.Master):
    """Do not merge equal clock planes belonging to different physical groups."""
    def __init__(self,law,directory):
        super().__init__(law["n"],directory)
        self.W=int(law["weight_denominator"])
        masses=physical_marginals(law)
        self.routes=[{"start_grid":key[0],"moves":list(key[1])} for key in masses]
        self.group_index={route_key(p):i for i,p in enumerate(self.routes)}
        self.group_numerators=list(masses.values())
        self.column_index={}

    def plan_data(self,plan):
        group=self.group_index[route_key(plan)]
        mass,points=C.plan_column(self.n,plan)
        coeff={self.index[point]:value for point,value in points.items()}
        return group,mass,coeff

    def add_plan(self,plan):
        group,mass,coeff=self.plan_data(plan)
        key=group,mass,tuple(sorted(coeff.items()))
        if key in self.column_index:return False
        self.column_index[key]=len(self.columns)
        self.columns.append({"plan":plan,"mass":mass,"coeff":coeff,"group":group})
        return True

    def add(self,path,table):
        added=0
        for latest in (False,True):
            plan,_,_=self.calendar(path,table,latest)
            added+=int(self.add_plan(plan))
        return added

    def weights_for(self,law):
        if law["n"]!=self.n or int(law["weight_denominator"])!=self.W or physical_marginals(law)!={route_key(p):q for p,q in zip(self.routes,self.group_numerators)}:
            raise ValueError("physical marginals changed")
        weights=np.zeros(len(self.columns))
        for p in law["paths"]:
            g,mass,coeff=self.plan_data(p)
            i=self.column_index[g,mass,tuple(sorted(coeff.items()))]
            weights[i]+=int(p["weight_numerator"])/self.W
        return weights

    def rationalize(self,weights):
        """Largest remainders separately inside each exact physical group."""
        weights=np.maximum(0.,np.asarray(weights,dtype=float))
        entries=defaultdict(list)
        for i,c in enumerate(self.columns):entries[c["group"]].append(i)
        result=[0]*len(self.columns)
        for group,indices in entries.items():
            total=float(weights[indices].sum());amount=self.group_numerators[group]
            if total<=0:
                result[indices[0]]=amount
                continue
            scaled=[float(weights[i])/total*amount for i in indices]
            rounded=[int(v) for v in scaled]
            remainder=amount-sum(rounded)
            if not 0<=remainder<=len(indices):raise ValueError("group rounding remainder")
            order=sorted(range(len(indices)),key=lambda j:(-(scaled[j]-rounded[j]),indices[j]))
            for j in order[:remainder]:rounded[j]+=1
            for i,value in zip(indices,rounded):result[i]=value
        if sum(result)!=self.W:raise AssertionError("probability normalization")
        for group,indices in entries.items():
            if sum(result[i] for i in indices)!=self.group_numerators[group]:raise AssertionError("physical mass changed")
        return result


class FixedCutBank(C.CutBank):
    def equality(self,extra_columns):
        M=len(self.master.columns)
        rows=[c["group"] for c in self.master.columns]
        matrix=coo_matrix((np.ones(M),(rows,np.arange(M))),shape=(len(self.master.routes),M+extra_columns)).tocsr()
        return matrix,np.asarray(self.master.group_numerators,dtype=float)/self.master.W

    def bounds(self):
        return [(0.,self.master.group_numerators[c["group"]]/self.master.W) for c in self.master.columns]

    def solve(self,seconds):
        self.sync_columns();M=len(self.master.columns);costs=self.response_matrix()
        equality,values=self.equality(1)
        answer=linprog(np.r_[np.zeros(M),1.],A_ub=np.c_[costs,-np.ones(costs.shape[0])],b_ub=np.zeros(costs.shape[0]),
            A_eq=equality,b_eq=values,bounds=self.bounds()+[(0.,2.)],method="highs-ds",
            options={"time_limit":seconds,"primal_feasibility_tolerance":1e-9,"dual_feasibility_tolerance":1e-9})
        if not answer.success:raise RuntimeError(answer.message)
        return answer

    def stabilized_weights(self,best,level,seconds):
        M=len(self.master.columns);best=np.r_[best,np.zeros(M-len(best))]
        costs=csr_matrix(self.response_matrix());identity=eye(M,format="csr")
        matrix=vstack((hstack((costs,csr_matrix((costs.shape[0],M)))),hstack((identity,-identity)),hstack((-identity,-identity))),format="csr")
        equality,values=self.equality(M)
        answer=linprog(np.r_[np.zeros(M),np.ones(M)],A_ub=matrix,
            b_ub=np.r_[np.full(costs.shape[0],level),best,-best],A_eq=equality,b_eq=values,
            bounds=self.bounds()+[(0.,1.)]*M,method="highs-ds",
            options={"time_limit":seconds,"primal_feasibility_tolerance":1e-9,"dual_feasibility_tolerance":1e-9})
        answer.response_rows=costs.shape[0]
        return answer


def price_all_calendars(master,cuts,table):
    """Exact family floor and strictly improving calendars for every route.

    Prefix minima minimize all causal nodal clocks of each fixed route.
    Pricing only strict improvements avoids thousands of irrelevant tied
    calendar planes while the exact floor still covers all calendars.
    """
    cuts.sync_columns()
    values=np.asarray([int(table[j,k]) for j,k in master.nodes],dtype=np.int64)
    costs=cuts.mass*master.D+cuts.matrix@values
    old=np.full(len(master.routes),np.iinfo(np.int64).max,dtype=np.int64)
    np.minimum.at(old,np.asarray([c["group"] for c in master.columns]),costs)
    numerator=added=0
    for group,route in enumerate(master.routes):
        plan,mass,coeff=master.calendar(route,table)
        cost=mass*master.D+sum(v*int(values[i]) for i,v in coeff.items())
        if cost>int(old[group]):raise AssertionError("prefix minimum exceeds an admitted causal calendar")
        numerator+=master.group_numerators[group]*cost
        if cost<int(old[group]):
            added+=int(master.add_plan(plan))
            latest,_,_=master.calendar(route,table,True)
            added+=int(master.add_plan(latest))
    return Fraction(numerator,4*master.n*master.D*master.W),added


def save_family_field(master,table,path):
    data={"format":"normalized-qout-nodal-field-v1","n":master.n,"field_denominator":str(master.D),
          "node_order":"j=0..4n, k=1..2n, j+k even; j-major",
          "field_values":[int(table[j,k]) for j,k in master.nodes]}
    path.write_bytes(gzip.compress((json.dumps(data,separators=(",",":"))+"\n").encode(),mtime=0))


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--input",type=Path,default=HERE/"seed_plain_n128.sparse.json.gz")
    ap.add_argument("--profile-seed",type=Path,default=ROOT/"packages/interval_clock_grid/lower_n256_field.json")
    ap.add_argument("--n",type=int,help="Refine only the causal-clock grid; must be a multiple of the seed grid.")
    ap.add_argument("--iterations",type=int,default=120)
    ap.add_argument("--seconds",type=float,default=1200)
    ap.add_argument("--lp-seconds",type=float,default=120)
    ap.add_argument("--price-every",type=int,default=4)
    ap.add_argument("--pricing-rounds",type=int,default=2,help="Calendar pricing passes before each expensive closure query.")
    ap.add_argument("--native-flow",action="store_true",help="Use checked native flow discovery; the original BigInt certificate verifier remains mandatory.")
    ap.add_argument("--alternative-cuts",type=int,default=4)
    ap.add_argument("--level-fraction",type=float,default=.5)
    ap.add_argument("--seed",type=int,default=223606)
    ap.add_argument("--resume",type=Path)
    ap.add_argument("--target-upper",default="291849329389899/204800000000000")
    ap.add_argument("--output",type=Path,required=True)
    args=ap.parse_args()
    if min(args.iterations,args.price_every,args.pricing_rounds)<1 or min(args.seconds,args.lp_seconds)<=0 or not 0<args.level_fraction<=1 or not 0<=args.alternative_cuts<=64:ap.error("invalid budget")
    out=args.output.resolve();out.mkdir(parents=True,exist_ok=True)
    began=time.monotonic();log=(out/"solver.jsonl").open("a",buffering=1)
    options={k:str(v) if isinstance(v,Path) else v for k,v in vars(args).items()}
    def emit(report):
        report["elapsed_seconds"]=time.monotonic()-began
        line=json.dumps(report,separators=(",", ":"));print(line,flush=True);log.write(line+"\n")
    source_law=C.read_json(args.input)
    target_n=args.n or int(source_law["n"])
    if target_n<source_law["n"] or target_n%source_law["n"]:ap.error("--n must be a positive multiple of the seed grid")
    ratio=target_n//source_law["n"]
    law={"n":target_n,"weight_denominator":source_law["weight_denominator"],"global_upper":source_law["global_upper"],
        "paths":[dict(C.lift_plan(p,ratio),weight_numerator=p["weight_numerator"]) for p in source_law["paths"]]}
    master=FixedMaster(law,out/"work")
    for p in law["paths"]:master.add_plan(C.lift_plan(p,1))
    history=[];resume=None
    if args.resume:
        resume=C.read_json(args.resume)
        if resume["input_sha256"]!=C.digest(args.input) or resume["n"]!=target_n:raise ValueError("wrong fixed-law resume input or clock grid")
        for c in resume["columns"]:master.add_plan(c["plan"])
        history=resume.get("history",[])
    seed_table=master.repair(C.seed_values(master,args.profile_seed));seed_profile=master.profile_values(seed_table)
    for p in master.routes:master.add(p,seed_table)
    cuts=FixedCutBank(master);cuts.sync_columns();cuts.add_base(seed_profile)
    cuts.add(np.zeros(master.K,dtype=np.uint8));cuts.add(np.ones(master.K,dtype=np.uint8));cuts.add(C.source_cut(master,source_law))
    if resume:
        archive=args.resume.resolve().parent/resume["cut_archive"]
        if C.digest(archive)!=resume["cut_archive_sha256"]:raise ValueError("cut archive hash")
        with np.load(archive,allow_pickle=False) as values:
            for p in values["base_profiles"]:cuts.add_base(p)
            for p in values["packed"]:cuts.add(cuts.unpack(p))
    verifier=ROOT/"packages/interval_sparse_upper/sparse_certificate.cjs" if "qout_nodes" in source_law else ROOT/"packages/interval_clock_grid/qout_primal_certificate.cjs"
    replay=subprocess.run(["node","--stack-size=16384",str(verifier),str(args.input)],check=True,text=True,capture_output=True)
    C.write_json(out/"seed.replay.json",json.loads(replay.stdout));C.write_json(out/"seed.physical.json",source_law)
    best_upper=Fraction(law["global_upper"]);best_weights=master.weights_for(law);best_certificate="seed.physical.json"
    if resume:
        prior=args.resume.resolve().parent/"best.sparse.json"
        if prior.exists():
            old=C.read_json(prior);weights=master.weights_for(old)
            replay=subprocess.run(["node","--stack-size=16384",str(ROOT/"packages/interval_sparse_upper/sparse_certificate.cjs"),str(prior)],check=True,text=True,capture_output=True)
            if Fraction(old["global_upper"])<best_upper:
                best_upper=Fraction(old["global_upper"]);best_weights=weights;best_certificate="best.sparse.json"
                if prior!=out/"best.sparse.json":shutil.copyfile(prior,out/"best.sparse.json")
                C.write_json(out/"best.replay.json",json.loads(replay.stdout))
    diagnostic=C.endpoint_diagnostic(law);floor=Fraction(diagnostic["endpoint_loop_supremum_lower"])
    C.write_json(out/"physical_marginals.json",{"n":master.n,"weight_denominator":str(master.W),
        "routes":[dict(p,weight_numerator=str(w)) for p,w in zip(master.routes,master.group_numerators)],
        "endpoint_diagnostic":diagnostic})
    sources=[Path(__file__),ROOT/"packages/interval_mixture_cut/search.py",ROOT/"packages/interval_mixture_cut/closure_server.cjs",
             ROOT/"packages/interval_sparse_upper/master.py",ROOT/"packages/interval_sparse_upper/sparse_certificate.cjs",
             ROOT/"packages/interval_clock_grid/qout_primal_certificate.cjs",ROOT/"packages/interval_clock_grid/exact_certificate.cjs",
             ROOT/"packages/interval_clock_grid/normalized_native/solve_normalized.py",
             ROOT/"packages/interval_clock_grid/normalized_native/verify_native_field.py",
             ROOT/"packages/interval_discovery/monster_search.py",ROOT/"packages/interval_monster_boundary/search.py"]
    if args.native_flow:
        sources.extend(ROOT/"packages/interval_integer_flow"/name for name in ("maximum_flow.cpp","native_server.cjs","native_closure.py"))
    C.write_json(out/"metadata.json",{"options":options,"input_sha256":C.digest(args.input),"profile_seed_sha256":C.digest(args.profile_seed),
        "source_sha256":{str(p.relative_to(ROOT)):C.digest(p) for p in sources},"github_sha":os.getenv("GITHUB_SHA"),"github_run_id":os.getenv("GITHUB_RUN_ID"),
        "python_version":platform.python_version(),"numpy_version":np.__version__,"scipy_version":scipy.__version__,
        "node_version":subprocess.run(["node","--version"],check=True,text=True,capture_output=True).stdout.strip()})
    emit({"event":"initialized","n":master.n,"source_n":source_law["n"],"physical_pairs":len(master.routes),"calendars":len(master.columns),
        "fixed_law_loop_floor":str(floor),"seed_exact_upper":law["global_upper"],"global_target_upper":args.target_upper})
    if args.native_flow:
        sys.path.insert(0,str(ROOT/"packages/interval_integer_flow"))
        from native_closure import NativeClosureServer
        server=NativeClosureServer(out/"work")
        C.write_json(out/"native_optimizer.json",{"binary_sha256":C.digest(server.binary),
            "scope":"Untrusted integer-flow optimizer. Original BigInt physical, geometric-edge, flow and cut verification remains mandatory on every candidate."})
    else:server=C.ClosureServer()
    extension=None;loaded=-1;latest=best_weights
    status,reason="COMPLETED","iteration_limit"
    family_floor=None
    def save():
        archive=out/"cuts.npz";np.savez_compressed(archive,packed=np.asarray(cuts.packed,dtype=np.uint8),base_profiles=np.asarray(cuts.base_profiles))
        C.write_json(out/"checkpoint.json",{"scope":"Fixed physical marginals; exploratory calendar/cut optimization only.","n":master.n,
            "input_sha256":C.digest(args.input),"columns":master.columns,"weights":np.r_[latest,np.zeros(len(master.columns)-len(latest))].tolist(),
            "history":history,"options":options,"cut_archive":archive.name,"cut_archive_sha256":C.digest(archive),"best_certified_global_upper":str(best_upper)})
    def add_cuts(report,weights):
        added=0
        for side in [report["source_side"]]+report.get("alternative_source_sides",[]):
            bits=np.zeros(len(extension.nodes),dtype=np.uint8);bits[side]=1
            table=extension.extend_integer(bits);field=np.asarray([table[j,k] for j,k in master.nodes],dtype=np.uint8)
            units=sum(int(x)*w for x,w in zip(cuts.row(field),weights))
            if Fraction(units,4*master.n*master.W)!=Fraction(report["global_upper"]):raise AssertionError("cut extension changed objective")
            added+=int(cuts.add(field))
        return added
    save()
    try:
        for iteration in range(args.iterations):
            if time.monotonic()-began>=args.seconds:status,reason="BUDGET_STOPPED","wall_time_limit";break
            cuts.sync_columns()
            lp_start=time.monotonic();priced=0;pricing_passes=0
            for pricing_pass in range(args.pricing_rounds):
                lp=cuts.solve(args.lp_seconds)
                table=master.repair(cuts.dual_field(lp))
                family_floor,added_calendars=price_all_calendars(master,cuts,table)
                priced+=added_calendars;pricing_passes+=1
                if family_floor>=Fraction(args.target_upper):
                    save_family_field(master,table,out/"blocking.field.json.gz")
                    C.write_json(out/"blocking.report.json",{"n":master.n,"field_sha256":C.digest(out/"blocking.field.json.gz"),
                        "physical_marginals_sha256":C.digest(out/"physical_marginals.json"),"all_calendar_family_floor":str(family_floor),
                        "global_target_upper":args.target_upper,"scope":"This grid's entire causal-clock certificate family for the fixed physical law cannot improve the target. This is not an obstruction for the actual continuous physical law."})
                    reason="all_calendar_qout_family_floor_reaches_target"
                    emit({"event":"family_blocked","all_calendar_qout_family_floor":str(family_floor),"global_target_upper":args.target_upper})
                    break
                if not added_calendars:break
            if reason=="all_calendar_qout_family_floor_reaches_target":break
            if added_calendars:lp=cuts.solve(args.lp_seconds)
            latest=lp.x[:-1];lp_seconds=time.monotonic()-lp_start
            if loaded!=len(master.columns):
                extension,model=C.load_model(server,master,out/"oracle.model.json");loaded=len(master.columns);emit({"event":"closure_model",**model})
            stabilizer=None
            guide=max(float(floor),float(lp.fun))
            if args.level_fraction<1 and float(best_upper)-guide>2e-8:
                level=guide+args.level_fraction*(float(best_upper)-guide)
                stabilizer=cuts.stabilized_weights(best_weights,level,args.lp_seconds)
                if stabilizer.success:latest=stabilizer.x[:len(master.columns)]
            numerators=master.rationalize(latest)
            exact=server.ask({"weights":list(map(str,numerators)),"denominator":str(master.W),"prefix":str(out/"oracle.current"),
                "alternative_cuts":args.alternative_cuts,"seed":args.seed+len(history)})
            upper=Fraction(exact["global_upper"]);added=add_cuts(exact,numerators)
            report={"event":"iteration","iteration":len(history),"calendars":len(master.columns),"cuts":len(cuts.packed),
                "restricted_cut_lp_estimate":float(lp.fun),"fixed_law_actual_loop_floor":str(floor),"exact_unrestricted_upper":str(upper),
                "exact_upper_minus_fixed_law_floor":str(upper-floor),"new_cuts":added,"lp_seconds":lp_seconds,
                "closure_seconds":exact["seconds"],"physical_marginals_preserved_exactly":True,
                "all_calendar_qout_family_floor":str(family_floor),"calendar_pricing_passes":pricing_passes,
                "prequery_new_causal_calendars":priced}
            if stabilizer is not None:report["stabilizer"]={"success":bool(stabilizer.success),"level":level,"l1_calendar_change":float(stabilizer.fun) if stabilizer.success else None}
            if upper<floor:raise AssertionError("upper below independently proved physical loop payoff")
            if upper<best_upper:
                candidate=C.read_json(out/"oracle.current.sparse.json")
                if physical_marginals(candidate)!=physical_marginals(law):raise AssertionError("certificate physical law changed")
                best_upper=upper;best_weights=np.asarray(numerators,dtype=float)/master.W;best_certificate="best.sparse.json"
                for suffix in (".sparse.json",".replay.json"):shutil.copyfile(out/("oracle.current"+suffix),out/("best"+suffix))
                report["new_best_certified_upper"]=str(upper);report["improves_global_target"]=upper<Fraction(args.target_upper)
            if (iteration+1)%args.price_every==0 or not added:
                fields=[]
                if stabilizer is not None and stabilizer.success:
                    marginals=stabilizer.ineqlin.marginals[:stabilizer.response_rows]
                    if np.maximum(0.,-marginals).sum()>1e-12:
                        proxy=type("Result",(),{"ineqlin":type("Marginals",(),{"marginals":marginals})()})()
                        fields.append(cuts.dual_field(proxy))
                before=len(master.columns)
                for field in fields:
                    table=master.repair(field)
                    price_all_calendars(master,cuts,table)
                report["all_physical_routes_priced"]=len(master.routes);report["pricing_fields"]=len(fields)
                report["new_causal_calendars"]=len(master.columns)-before
            history.append(report);emit(report);save()
    except RuntimeError as error:
        if "time limit" not in str(error).lower() and "time_limit" not in str(error).lower():status,reason="FAILED","runtime_failure";raise
        status,reason="BUDGET_STOPPED","small_lp_time_limit";emit({"event":"budget_stop","error":str(error)})
    except Exception:status,reason="FAILED","unexpected_failure";raise
    finally:
        server.close();save()
        summary={"status":status,"stop_reason":reason,"n":master.n,"source_n":source_law["n"],"iterations_total":len(history),"physical_pairs":len(master.routes),
            "best_certified_global_upper":str(best_upper),"seed_exact_upper":law["global_upper"],"fixed_law_loop_floor":str(floor),
            "best_upper_minus_fixed_law_floor":str(best_upper-floor),"global_target_upper":args.target_upper,
            "all_calendar_qout_family_floor":str(family_floor) if family_floor is not None else None,
            "improves_global_target":best_upper<Fraction(args.target_upper),"best_certificate":best_certificate,
            "scope":"Exact physical upper; all physical probabilities remain unchanged. Loop floor is only for this fixed law, not a game lower.",
            "elapsed_seconds":time.monotonic()-began}
        C.write_json(out/"summary.json",summary);emit({"event":"complete",**summary});log.close()
        files={str(p.relative_to(out)):C.digest(p) for p in out.rglob("*") if p.is_file() and "work" not in p.relative_to(out).parts and p.name!="manifest.json"}
        C.write_json(out/"manifest.json",{**summary,"options":options,"files_sha256":files})


if __name__=="__main__":main()
