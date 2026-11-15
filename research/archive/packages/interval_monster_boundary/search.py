#!/usr/bin/env python3
"""Joint physical support and calendar discovery across the endpoint layer.

All optimization is floating discovery.  A candidate is an unrestricted upper
only after the existing exact physical Qout certificate maker and verifier pass.
The boundary kernel is used to propose routes, never as an all-Princess oracle.
"""
from __future__ import annotations

import argparse
from fractions import Fraction
import gzip
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
NATIVE = ROOT / "packages/interval_clock_grid/normalized_native"
sys.path.insert(0, str(NATIVE))
sys.path.insert(0, str(ROOT / "packages/interval_discovery"))
import numpy as np
import scipy
from cached_path_pricing import CachedPathPricing, normalize_path
from monster_search import digest, lift_plan, mutate_routes, read_json, restore_rng, route_hash, write_json
from persistent_highs import PersistentMaster, SolveError
from solve_normalized import Master
from verify_native_field import load_table


def seed_values(master: Master, path: Path):
    """Read either exact source encoding without materializing a JSON node list."""
    seed, table, _ = load_table(path)
    sn, sd = seed["n"], int(seed["field_denominator"])
    if sn % master.n == 0:
        ratio = sn//master.n
        return np.asarray([table[(j*ratio)*(2*sn+1)+k*ratio]/sd for j,k in master.nodes])
    def coordinate(z):
        cell = int(np.floor(z))
        alpha = z-cell
        if alpha < 1e-12:
            alpha = 0.
        elif alpha > 1-1e-12:
            cell,alpha = cell+1,0.
        plus = cell % (2*sn) < sn
        return cell,alpha,plus,alpha if plus else 1-alpha
    def node(j,k):
        if k == 0 or j >= 6*sn:
            return 0.
        return (1 if k>0 else -1)*table[j*(2*sn+1)+abs(k)]/sd
    answer = []
    for j,k in master.nodes:
        u,w = coordinate(sn*(j+k)/(2*master.n)),coordinate(sn*(j-k)/(2*master.n))
        cuts = sorted(set((0.,1.,u[3],w[3])))
        result = 0.
        for left,right in zip(cuts,cuts[1:]):
            z = (left+right)/2
            def rounded(c):
                cell,alpha,plus,_ = c
                return cell+int(alpha>0 and (z<alpha if plus else z>1-alpha))
            U,W = rounded(u),rounded(w)
            result += (right-left)*node(U+W,U-W)
        answer.append(result)
    return np.asarray(answer)


def inward_boundary_route(n: int, a: int, z: int, front: int = 0) -> dict:
    """I_(a/n,z/n) with an independently shifted final front U=1+front/n.

    The first turn is on W=-1+z/n.  Integer parameters satisfy
    0 <= a <= z < n and -a <= front <= z.  The latter inequalities keep
    the middle outward leg nonnegative and within the physical interval.
    The last inward leg crosses the center by time two.  Actual endpoint
    contacts and the time-two suffix are normalized by the shared validator.
    """
    if not (n >= 1 and 0 <= a <= z < n and -a <= front <= z):
        raise ValueError("invalid boundary route parameters")
    moves = [-1] * (z-a) + [1] * (a+front)
    moves += [-1] * (4*n+front-z) + [1] * (4*n)
    return normalize_path(n, {"start_grid": 2*n-2*a, "moves": moves})


def deficit_nodes(n: int, points: int) -> list[int]:
    """Fine near zero, then a global mesh; every gap scale is crossed."""
    values = {0, n-1}
    values.update(range(1, min(n, 17)))
    values.update(round(k*n/max(1, points)) for k in range(points+1))
    value = 1
    while value < n:
        values.update((value, value-1, value+1))
        value *= 2
    return sorted(a for a in values if 0 <= a < n)


def boundary_routes(n: int, points: int, shifted: bool = True):
    nodes = deficit_nodes(n, points)
    for z in nodes:
        for a in nodes:
            if a > z:
                break
            fronts = {0}
            if shifted:
                # Change the two fronts independently; this is not one common
                # coordinate warp of all routes and does not fix probabilities.
                fronts.update((-a, -min(a, 1), min(z, 1),
                               -min(a, max(1, n//32)), min(z, max(1, n//32))))
            for front in sorted(fronts):
                yield inward_boundary_route(n, a, z, front)
    # Outward-first and inward-first direct endpoint tours throughout the arena.
    for a in range(n+1):
        start = 2*n-2*a
        for first in (-2*n, 2*n):
            direction = 1 if first == 2*n else -1
            moves = [direction] * abs(first-start) + [-direction] * (4*n)
            yield normalize_path(n, {"start_grid": start, "moves": moves})


def endpoint_diagnostic(law: dict) -> dict:
    """Exact fixed-law lower witness, never a game-value lower bound."""
    n, W = int(law["n"]), int(law["weight_denominator"])
    mass = Fraction(0)
    endpoint_mass = Fraction(0)
    baseline = Fraction(0)
    interior_starts = []
    for plan in law["paths"]:
        weight = Fraction(int(plan["weight_numerator"]), W)
        mass += weight
        positions = [int(plan["start_grid"])]
        for step in plan["moves"]:
            positions.append(positions[-1]+int(step))
        left, right = positions.index(-2*n), positions.index(2*n)
        baseline += weight * Fraction(left+right, 4*n)
        if abs(positions[0]) == 2*n:
            expected = -1 if positions[0] > 0 else 1
            if plan["moves"][:4*n] != [expected]*(4*n):
                raise ValueError("endpoint-loop witness requires direct endpoint-start sweeps")
            endpoint_mass += weight
        else:
            interior_starts.append(abs(positions[0]))
    if mass != 1:
        raise ValueError("physical probabilities do not sum to one")
    gap = 1-Fraction(max(interior_starts), 2*n) if interior_starts else Fraction(1)
    witness = baseline + endpoint_mass*gap/4
    answer = {"scope": "Lower witness for the worst response to this fixed physical law only.",
              "endpoint_sweep_mass": str(endpoint_mass), "endpoint_baseline": str(baseline),
              "initial_gap": str(gap), "endpoint_loop_supremum_lower": str(witness)}
    if law.get("global_upper") is not None:
        answer["certified_upper_minus_loop_witness"] = str(Fraction(law["global_upper"])-witness)
    return answer


def checkpoint(master, weights, profile, history, arguments, baseline_sha, rng_state=None):
    return {"scope": "Floating joint physical/calendar discovery; exact replay required for any upper.",
            "n": master.n, "profile_grid": master.n, "normalized_profile": True,
            "columns": master.columns, "weights": list(map(float, weights)),
            "profile": list(map(float, profile)), "history": history,
            "options": arguments, "initial_law_sha256": baseline_sha,
            "rng_state":rng_state}


def exact_certificate(source: Path, prefix: Path) -> dict:
    verifier = ROOT / "packages/interval_clock_grid/qout_primal_certificate.cjs"
    subprocess.run(["node", "--stack-size=16384", str(verifier), "--make", str(source), str(prefix)],
                   check=True, capture_output=True, text=True)
    path = prefix.with_suffix(".physical.json")
    replay = subprocess.run(["node", "--stack-size=16384", str(verifier), str(path)],
                            check=True, capture_output=True, text=True)
    report = json.loads(replay.stdout)
    write_json(prefix.with_suffix(".replay.json"), report)
    return report


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--n", type=int, default=256)
    ap.add_argument("--initial-law", type=Path, default=ROOT/"packages/interval_discovery_certificates/monster_mutations_n128.physical.json.gz")
    ap.add_argument("--profile-seed", type=Path, default=ROOT/"packages/interval_clock_grid/lower_n256_field.json")
    ap.add_argument("--resume", type=Path)
    ap.add_argument("--iterations", type=int, default=80)
    ap.add_argument("--seconds", type=float, default=3600)
    ap.add_argument("--lp-seconds", type=float, default=600)
    ap.add_argument("--sparse-master", action="store_true",
                    help="Project each LP onto its charged event nodes before solving")
    ap.add_argument("--seed", type=int, default=577215)
    ap.add_argument("--boundary-points", type=int, default=48)
    ap.add_argument("--pricing-paths", type=int, default=256)
    ap.add_argument("--full-every", type=int, default=4)
    ap.add_argument("--mutation-count", type=int, default=128)
    ap.add_argument("--certify-every", type=int, default=8)
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()
    if min(args.n,args.iterations,args.boundary_points,args.pricing_paths,args.full_every,args.certify_every) < 1 or min(args.seconds,args.lp_seconds) <= 0 or args.pricing_paths > 1000:
        ap.error("invalid positive budget")
    out = args.output.resolve()
    out.mkdir(parents=True, exist_ok=True)
    began = time.monotonic()
    rng = random.Random(args.seed)
    args_dict = {k: str(v) if isinstance(v,Path) else v for k,v in vars(args).items()}
    log = (out/"solver.jsonl").open("a", buffering=1)
    def emit(data):
        data["elapsed_seconds"] = time.monotonic()-began
        text = json.dumps(data, separators=(",", ":"))
        print(text, flush=True)
        log.write(text+"\n")
    law = read_json(args.initial_law)
    if args.n % law["n"]:
        ap.error("n must refine the initial physical law")
    master = Master(args.n, out/"work")
    for p in law["paths"]:
        master.add_plan(lift_plan(p, args.n//law["n"]))
    history = []
    resumed_law = None
    if args.resume:
        old = read_json(args.resume)
        if args.n % old["n"]:
            ap.error("n must refine the checkpoint grid")
        for c in old["columns"]:
            master.add_plan(lift_plan(c["plan"], args.n//old["n"]))
        if old.get("scope","").startswith("Floating joint") and old["n"] == args.n:
            history = old.get("history",[])
            if old.get("rng_state") is not None:
                rng.setstate(restore_rng(old["rng_state"]))
        previous_best = args.resume.resolve().parent/"best.physical.json"
        if previous_best.exists():
            resumed_law = read_json(previous_best)
    cache = CachedPathPricing(args.n, master.D)
    cache.update_columns(master.columns)
    source_hashes = {route_hash({"start_grid":r.start,"moves":[2*s-1 for s in r.moves]}) for r in cache._routes}
    structural_count = cache.add_many(boundary_routes(args.n,args.boundary_points))
    emit({"event":"support_initialized","n":args.n,"columns":len(master.columns),
          "distinct_physical_routes":len(cache),"new_boundary_routes":structural_count,
          "baseline":law["global_upper"],"baseline_endpoint_diagnostic":endpoint_diagnostic(law)})
    if args.profile_seed:
        seed_profile = seed_values(master,args.profile_seed)
        table = master.repair(seed_profile)
        selected = cache.price(table, keep=args.pricing_paths)
        before = len(master.columns)
        for p in selected["paths"]:
            master.add(p,table)
        emit({"event":"seed_separation","new_calendars":len(master.columns)-before,
              "cached_minimum":str(Fraction(int(selected["cached_minimum_units"]),4*args.n*master.D)),
              "scope":"Known-route costs only; no full-bank or unrestricted lower claim."})
    source_files = [Path(__file__), NATIVE/"solve_normalized.py", NATIVE/"persistent_highs.py",
                    NATIVE/"cached_path_pricing.py", NATIVE/"price_normalized.cpp", NATIVE/"verify_native_field.py",
                    ROOT/"packages/interval_discovery/monster_search.py",
                    ROOT/"packages/interval_clock_grid/qout_primal_certificate.cjs",
                    ROOT/"packages/interval_clock_grid/exact_certificate.cjs"]
    if args.sparse_master:
        source_files.append(ROOT/"packages/interval_sparse_upper/master.py")
    metadata = {"options":args_dict,"initial_law_sha256":digest(args.initial_law),
                "profile_seed_sha256":digest(args.profile_seed) if args.profile_seed else None,
                "source_sha256":{str(p.relative_to(ROOT)):digest(p) for p in source_files},
                "python":platform.python_version(),"numpy":np.__version__,"scipy":scipy.__version__,
                "github_sha":os.getenv("GITHUB_SHA"),"github_run_id":os.getenv("GITHUB_RUN_ID"),
                "scope":"Joint physical support, probability, and causal calendar search; no restricted-family result is a game lower bound."}
    write_json(out/"metadata.json",metadata)
    # Independently replay the seed so a budget stop always retains a certificate.
    seed_plain = out/"best.physical.json"
    best_source = min([law]+([resumed_law] if resumed_law is not None else []),
                      key=lambda d:Fraction(d["global_upper"]))
    write_json(seed_plain,best_source)
    replay = subprocess.run(["node","--stack-size=16384",str(ROOT/"packages/interval_clock_grid/qout_primal_certificate.cjs"),str(seed_plain)],
                            check=True,capture_output=True,text=True)
    write_json(out/"best.replay.json",json.loads(replay.stdout))
    best_upper = Fraction(best_source["global_upper"])
    best_bank = None
    # Retain the initialized support even if the very first cold solve times out.
    write_json(out/"checkpoint.json",checkpoint(master,np.zeros(len(master.columns)),
        seed_profile if args.profile_seed else [],history,args_dict,digest(args.initial_law),rng.getstate()))
    if args.sparse_master:
        sys.path.insert(0,str(ROOT/"packages/interval_sparse_upper"))
        from master import solve_existing_master
        backend = None
    else:
        backend = PersistentMaster(master,time_limit=args.lp_seconds)
    status, reason = "COMPLETED", "iteration_limit"
    last_lp = last_weights = None
    try:
        for iteration in range(args.iterations):
            if time.monotonic()-began >= args.seconds:
                status,reason = "BUDGET_STOPPED","wall_time_limit"
                break
            # Crucial distinction from lower-oriented proximal discovery:
            # separate the actual maximizing master field, without a level shift.
            emit({"event":"lp_start","iteration":len(history),"columns":len(master.columns),
                  "sparse_projection":args.sparse_master})
            if args.sparse_master:
                lp,weights,trial = solve_existing_master(master,seconds=args.lp_seconds)
                lp_stats = lp.sparse_stats
            else:
                lp,weights,trial = backend.solve_lp()
                lp_stats = backend.last_stats
            last_lp,last_weights = lp,weights
            floating_upper = float(-lp.fun)
            cp = checkpoint(master,weights,trial,history,args_dict,digest(args.initial_law),rng.getstate())
            write_json(out/"checkpoint.json",cp)
            report = {"event":"iteration","iteration":len(history),"floating_master_upper":floating_upper,
                      "columns":len(master.columns),"physical_reservoir":len(cache),
                      "separation_field":"actual master optimizer","lp_stats":lp_stats}
            if floating_upper < float(best_upper)-1e-8 and (iteration % args.certify_every == 0 or iteration == args.iterations-1):
                certified = exact_certificate(out/"checkpoint.json",out/"candidate")
                exact_upper = Fraction(certified["global_upper"])
                report["certified_upper"] = str(exact_upper)
                if exact_upper < best_upper:
                    best_upper = exact_upper
                    for suffix in (".physical.json",".replay.json"):
                        shutil.copyfile(out/("candidate"+suffix),out/("best"+suffix))
                    best_law = read_json(out/"best.physical.json")
                    write_json(out/"best.endpoint_diagnostic.json",endpoint_diagnostic(best_law))
                    write_json(out/"best.support.json",{
                        "distinct_physical_pairs":len({route_hash(p) for p in best_law["paths"]}),
                        "new_supported_routes":len({route_hash(p) for p in best_law["paths"]}-source_hashes),
                        "new_supported_probability":str(sum((Fraction(int(p["weight_numerator"]),int(best_law["weight_denominator"])) for p in best_law["paths"] if route_hash(p) not in source_hashes),Fraction(0)))})
            cache.update_columns(master.columns)
            active = [c["plan"] for c,w in zip(master.columns,weights) if w > 1e-9]
            if args.mutation_count and active:
                report["new_bulk_routes"] = cache.add_many(mutate_routes(args.n,active,rng,args.mutation_count))
            table = master.repair(trial)
            selected = cache.price(table,keep=args.pricing_paths,level=floating_upper,tolerance="1e-8")
            before = len(master.columns)
            for p in selected["violating_paths"]:
                master.add(p,table)
            added = len(master.columns)-before
            report["new_cached_calendars"] = added
            report["cached_minimum_only"] = str(Fraction(int(selected["cached_minimum_units"]),4*args.n*master.D))
            if iteration % args.full_every == 0 or not added:
                emit({"event":"complete_pricing_start","iteration":len(history),"n":args.n})
                answer,table = master.price(trial,keep=args.pricing_paths)
                value = Fraction(int(answer["minimum_units"]),4*args.n*master.D)
                report.update(complete_exact_bank_minimum=str(value),
                              complete_transfer_value_lower=str(value-Fraction(1,2*args.n)),
                              native_retained_states=answer["retained_states"])
                if best_bank is None or value > best_bank:
                    best_bank = value
                    master.save(out/"best_bank",table,answer,lp,
                                np.r_[weights,np.zeros(len(master.columns)-len(weights))],history+[report])
                cache.add_many(answer["paths"])
                before = len(master.columns)
                for p in answer["paths"]:
                    master.add(p,table)
                report["new_complete_calendars"] = len(master.columns)-before
                if floating_upper-float(value) < 1e-8:
                    reason = "finite_bank_separation_closed"
                    history.append(report)
                    emit(report)
                    break
            history.append(report)
            emit(report)
            cp = checkpoint(master,np.r_[weights,np.zeros(len(master.columns)-len(weights))],trial,history,args_dict,digest(args.initial_law),rng.getstate())
            write_json(out/"checkpoint.json",cp)
    except RuntimeError as error:
        if "time limit" not in str(error).lower() and "time_limit" not in str(error).lower():
            status,reason = "FAILED","solver_failure"
            raise
        status,reason = "BUDGET_STOPPED","per_solve_lp_time_limit"
        emit({"event":"budget_stop","reason":reason,"error":str(error)})
    except Exception as error:
        status,reason = "FAILED","unexpected_failure"
        emit({"event":"failure","error":repr(error)})
        raise
    finally:
        # A final fully solved mixture may improve between scheduled replays.
        if last_lp is not None and -last_lp.fun < float(best_upper)-1e-8:
            weights = np.r_[last_weights,np.zeros(len(master.columns)-len(last_weights))]
            write_json(out/"candidate.checkpoint.json",checkpoint(master,weights,last_lp.x[:-1],history,args_dict,digest(args.initial_law),rng.getstate()))
            certified = exact_certificate(out/"candidate.checkpoint.json",out/"candidate")
            if Fraction(certified["global_upper"]) < best_upper:
                best_upper = Fraction(certified["global_upper"])
                for suffix in (".physical.json",".replay.json"):
                    shutil.copyfile(out/("candidate"+suffix),out/("best"+suffix))
        best_law = read_json(out/"best.physical.json")
        write_json(out/"best.endpoint_diagnostic.json",endpoint_diagnostic(best_law))
        result = {"status":status,"stop_reason":reason,"iterations":len(history),
                  "best_certified_global_upper":str(best_upper),"baseline_global_upper":law["global_upper"],
                  "certified_upper_improvement":str(Fraction(law["global_upper"])-best_upper),
                  "best_complete_bank_minimum":str(best_bank) if best_bank is not None else None,
                  "scope":"Only exact replayed physical uppers are unrestricted certificates. Cached route minima are not lower bounds; no equilibrium claim.",
                  "elapsed_seconds":time.monotonic()-began}
        write_json(out/"summary.json",result)
        emit({"event":"complete",**result})
        log.close()
        hashes = {str(p.relative_to(out)):digest(p) for p in out.rglob("*") if p.is_file() and "work" not in p.relative_to(out).parts and p.name != "manifest.json"}
        write_json(out/"manifest.json",{**result,"best_upper":str(best_upper),"options":args_dict,"files_sha256":hashes,"source_metadata":"metadata.json"})


if __name__ == "__main__":
    main()
