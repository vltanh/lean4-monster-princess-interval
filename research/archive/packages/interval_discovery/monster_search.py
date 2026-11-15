#!/usr/bin/env python3
"""Discover new physical Monster laws; accept uppers only by exact Qout replay.

The floating sparse master and mutation reservoir are search devices.  Every
retained upper is rebuilt as a rational physical law and passed through the
existing all-Princess verifier.  Full native response calls also produce exact
finite-bank duals, whose game-value transfer is kept separate from the upper.
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
import numpy as np
import scipy
from solve_normalized import Master
from cached_path_pricing import CachedPathPricing, normalize_path


def read_json(path):
    raw = Path(path).read_bytes()
    return json.loads(gzip.decompress(raw) if raw[:2] == b"\x1f\x8b" else raw)


def write_json(path, value):
    path = Path(path)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(json.dumps(value, separators=(",", ":")) + "\n")
    temporary.replace(path)


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def route_key(route):
    return route["start_grid"], tuple(route["moves"])


def route_hash(route):
    return hashlib.sha256(json.dumps(route_key(route), separators=(",", ":")).encode()).hexdigest()


def lift_plan(plan, ratio):
    return {"start_grid": plan["start_grid"] * ratio,
            "moves": [step for step in plan["moves"] for _ in range(ratio)],
            "minus_charges": [[j * ratio, a * ratio] for j, a in plan["minus_charges"]],
            "plus_charges": [[j * ratio, a * ratio] for j, a in plan["plus_charges"]]}


def complete_prefix(n, start, moves, first):
    """Truncate at the first endpoint/time 2 and attach physical endpoint tours."""
    R, C = 2 * n, 4 * n
    if start % 2 or abs(start) > R:
        raise ValueError("invalid initial lattice point")
    x, prefix = start, []
    for step in moves[:C]:
        if abs(x) == R:
            first = x
            break
        x += step
        if abs(x) > R:
            raise ValueError("prefix exits arena")
        prefix.append(step)
    if abs(x) == R:
        first = x
    for target in (first, -first):
        step = 1 if target > x else -1
        prefix.extend([step] * abs(target - x))
        x = target
    return normalize_path(n, {"start_grid": start, "moves": prefix})


def mutate_routes(n, routes, rng, count):
    """Produce legal new turn times, starts and short excursions.

    Rejected proposals are simply absent from discovery.  Neither rejection
    nor this finite reservoir is used as a completeness or lower-bound claim.
    """
    R, C, produced = 2 * n, 4 * n, []
    for _ in range(count * 4):
        if len(produced) >= count:
            break
        source = rng.choice(routes)
        start, moves = source["start_grid"], list(source["moves"][:C])
        choice = rng.randrange(4)
        if choice == 0:
            start += rng.choice((-4, -2, 2, 4))
        elif choice == 1:
            turns = [j for j in range(len(moves) - 1) if moves[j] != moves[j + 1]]
            if not turns:
                continue
            j = rng.choice(turns)
            moves[j], moves[j + 1] = moves[j + 1], moves[j]
        elif choice == 2:
            if not moves:
                continue
            j = rng.randrange(len(moves))
            direction = rng.choice((-1, 1))
            length = rng.choice((1, 2, 4, max(1, n // 16)))
            moves[j:j] = [direction] * length + [-direction] * length
        else:
            # Persistently directed random exploration; force the center
            # when its deadline becomes tight, then finish with endpoint tours.
            start = 2 * rng.randrange(n + 1)
            x, moves, centered = start, [], start == 0
            direction = rng.choice((-1, 1))
            for j in range(C):
                if abs(x) == R:
                    break
                if not centered and C - j <= abs(x):
                    direction = -1 if x > 0 else 1
                elif rng.random() < 2.5 / max(1, n):
                    direction = -direction
                moves.append(direction)
                x += direction
                centered = centered or x == 0
        try:
            produced.append(complete_prefix(n, start, moves, rng.choice((-R, R))))
        except ValueError:
            continue
    return produced


def restore_rng(value):
    return tuple(restore_rng(x) if isinstance(x, list) else x for x in value)


def law_structure(certificate, initial_hashes):
    W, n = int(certificate["weight_denominator"]), certificate["n"]
    groups, start_mass, prefix_turn_mass = {}, {}, {}
    for plan in certificate["paths"]:
        key = route_hash(plan)
        positions = [plan["start_grid"]]
        for step in plan["moves"]:
            positions.append(positions[-1]+step)
        endpoint_time = min(positions.index(-2*n), positions.index(2*n))
        prefix_cutoff = min(endpoint_time, 4*n)
        turns = [j for j in range(1,len(plan["moves"])) if plan["moves"][j-1] != plan["moves"][j]]
        prefix_turns = sum(j < prefix_cutoff for j in turns)
        start = str(Fraction(plan["start_grid"], 2*n))
        weight = int(plan["weight_numerator"])
        start_mass[start] = start_mass.get(start, 0)+weight
        prefix_turn_mass[prefix_turns] = prefix_turn_mass.get(prefix_turns, 0)+weight
        item = groups.setdefault(key, {"path_sha256": key, "start": str(Fraction(plan["start_grid"], 2*n)),
                                      "turns": len(turns), "turns_before_first_endpoint_or_time_two": prefix_turns,
                                      "turn_events": [[str(Fraction(j,2*n)), str(Fraction(positions[j],2*n))] for j in turns],
                                      "first_endpoint_time": str(Fraction(endpoint_time, 2*n)),
                                      "weight_numerator": 0, "new_physical_path": key not in initial_hashes})
        item["weight_numerator"] += weight
    paths = sorted(groups.values(), key=lambda x: (-x["weight_numerator"], x["path_sha256"]))
    return {"distinct_physical_pairs": len(paths),
            "new_physical_pairs": sum(p["new_physical_path"] for p in paths),
            "new_physical_probability": str(Fraction(sum(p["weight_numerator"] for p in paths if p["new_physical_path"]), W)),
            "weight_denominator": str(W),
            "starting_position_probabilities": {k: str(Fraction(v,W)) for k,v in sorted(start_mass.items(),key=lambda z:Fraction(z[0]))},
            "prefix_turn_probabilities": {str(k): str(Fraction(v,W)) for k,v in sorted(prefix_turn_mass.items())},
            "physical_support": paths}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--n", type=int, default=128)
    ap.add_argument("--iterations", type=int, default=40)
    ap.add_argument("--seconds", type=float, default=1800)
    ap.add_argument("--lp-seconds", type=float, default=600)
    ap.add_argument("--seed", type=int, default=271828)
    ap.add_argument("--family", choices=("priced", "mutations"), default="mutations")
    ap.add_argument("--mutation-count", type=int, default=128)
    ap.add_argument("--pricing-paths", type=int, default=64)
    ap.add_argument("--full-every", type=int, default=8)
    ap.add_argument("--denominator", type=int, default=10**9)
    ap.add_argument("--initial-law", type=Path, default=ROOT / "packages/interval_clock_grid/upper_n64_physical.json.gz")
    ap.add_argument("--profile-seed", type=Path)
    ap.add_argument("--resume", type=Path)
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()
    if min(args.n, args.iterations, args.pricing_paths, args.full_every, args.denominator) < 1 or args.mutation_count < 0 or min(args.seconds,args.lp_seconds) <= 0:
        ap.error("positive search limits required")
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    started, rng = time.monotonic(), random.Random(args.seed)
    history, best_upper, best_dual = [], None, None
    best_answer = best_table = anchor = None
    seed_law = read_json(args.initial_law)
    if args.n % seed_law["n"]:
        ap.error("target grid must be an integer refinement of initial-law grid")
    master = Master(args.n, output / "work", args.denominator)
    seed_plans = [lift_plan(p, args.n // seed_law["n"]) for p in seed_law["paths"]]
    initial_hashes = {route_hash(p) for p in seed_plans}
    for p in seed_plans:
        master.add_plan(p)
    cache = CachedPathPricing(args.n, master.D)
    cache.update_columns(master.columns)
    if args.resume:
        saved = read_json(args.resume)
        if saved["n"] != args.n or saved.get("family") != args.family or saved.get("seed") != args.seed or saved.get("initial_law_sha256") != digest(args.initial_law):
            raise ValueError("resume settings or initial-law hash mismatch")
        for column in saved["columns"]:
            master.add_plan(column["plan"])
        history = saved.get("history", [])
        rng.setstate(restore_rng(saved["rng_state"]))
        cache.add_many(saved.get("reservoir_paths", []))
        # Saved floating objectives are never inherited as certificates.
    try:
        from persistent_highs import PersistentMaster
        backend = PersistentMaster(master, time_limit=min(args.lp_seconds, args.seconds))
        backend_name = "persistent HiGHS simplex"
    except ImportError:
        backend, backend_name = master, "fresh SciPy HiGHS simplex"
    source_files = [Path(__file__), NATIVE/"solve_normalized.py", NATIVE/"price_normalized.cpp",
                    NATIVE/"cached_path_pricing.py", ROOT/"packages/interval_clock_grid/qout_primal_certificate.cjs",
                    ROOT/"packages/interval_clock_grid/exact_certificate.cjs"]
    if (NATIVE/"persistent_highs.py").exists():
        source_files.append(NATIVE/"persistent_highs.py")
    metadata = {"scope": "Discovery estimates are separate from exact all-Princess physical upper certificates.",
                "arguments": {k: str(v) if isinstance(v, Path) else v for k, v in vars(args).items()},
                "seed": args.seed, "family": args.family,
                "initial_law_sha256": digest(args.initial_law), "lp_backend": backend_name,
                "python": platform.python_version(), "numpy": np.__version__, "scipy": scipy.__version__,
                "compiler": subprocess.run(["g++", "--version"], check=True, capture_output=True, text=True).stdout.splitlines()[0],
                "node": subprocess.run(["node", "--version"], check=True, capture_output=True, text=True).stdout.strip(),
                "source_sha256": {str(p.relative_to(ROOT)): digest(p) for p in source_files},
                "github_sha": os.environ.get("GITHUB_SHA"), "github_run_id": os.environ.get("GITHUB_RUN_ID"),
                "github_run_attempt": os.environ.get("GITHUB_RUN_ATTEMPT"), "baseline_global_upper": seed_law.get("global_upper", seed_law.get("exact_value"))}
    write_json(output/"metadata.json", metadata)
    log = (output/"solver.jsonl").open("a", buffering=1)
    def emit(report):
        report["elapsed_seconds"] = time.monotonic()-started
        line = json.dumps(report, separators=(",", ":"))
        print(line, flush=True)
        log.write(line+"\n")
    def checkpoint(lp, weights):
        return {"scope": "Floating physical mixture proposal. Requires rationalization and exact Qout replay.",
                "n": args.n, "profile_grid": args.n, "normalized_profile": True,
                "seed": args.seed, "family": args.family, "initial_law_sha256": digest(args.initial_law),
                "rng_state": rng.getstate(), "columns": master.columns,
                "weights": list(map(float, weights)) + [0.]*(len(master.columns)-len(weights)),
                "profile": lp.x[:-1].tolist(), "upper": float(-lp.fun), "history": history,
                "reservoir_paths": [{"start_grid": r.start, "moves": [2*s-1 for s in r.moves]} for r in cache._routes]}
    def certify(checkpoint_path, iteration):
        nonlocal best_upper
        prefix = output / "candidate"
        maker = ["node", "--stack-size=16384", str(ROOT/"packages/interval_clock_grid/qout_primal_certificate.cjs"),
                 "--make", str(checkpoint_path), str(prefix)]
        done = subprocess.run(maker, check=True, text=True, capture_output=True)
        (output/"certificate-maker.log").write_text(done.stdout+done.stderr)
        cert_path = output/"candidate.physical.json"
        replay = subprocess.run(["node", "--stack-size=16384", str(ROOT/"packages/interval_clock_grid/qout_primal_certificate.cjs"), str(cert_path)],
                                check=True, text=True, capture_output=True)
        exact = json.loads(replay.stdout)
        if exact["status"] != "PASS":
            raise ValueError("exact replay did not pass")
        (output/"candidate.fresh-replay.json").write_text(replay.stdout)
        value = Fraction(exact["global_upper"])
        improved = best_upper is None or value < best_upper
        if improved:
            best_upper = value
            for source, dest in [(cert_path, output/"best.physical.json"),
                                 (output/"candidate.replay.json", output/"best.replay.json"),
                                 (checkpoint_path, output/"best.checkpoint.json")]:
                shutil.copyfile(source, dest)
            write_json(output/"structure.json", law_structure(read_json(cert_path), initial_hashes))
        emit({"event": "exact_upper", "iteration": iteration, "global_upper": str(value),
              "global_upper_decimal": float(value), "improved_run_best": improved,
              "improves_baseline": metadata["baseline_global_upper"] is not None and value < Fraction(metadata["baseline_global_upper"]),
              "certificate_sha256": digest(cert_path), "status": "PASS"})
        return exact

    emit({"event": "start", "n": args.n, "family": args.family, "seed": args.seed,
          "seed_physical_pairs": len(initial_hashes), "seed_calendars": len(master.columns), "lp_backend": backend_name})
    resumed_best = None
    if args.resume:
        previous_best = args.resume.resolve().parent/"best.physical.json"
        if previous_best.exists():
            resumed_best = output/"resume-best.input.json"
            shutil.copyfile(previous_best, resumed_best)
    # Preserve the old physical strategy before optimizing.  On a refined
    # grid its clocks are revalidated and its closure is solved exactly again.
    seed_checkpoint = output/"seed.checkpoint.json"
    write_json(seed_checkpoint, {"n": args.n, "columns": [{"plan": p} for p in seed_plans],
                                 "weights": [int(p["weight_numerator"])/int(seed_law["weight_denominator"]) for p in seed_law["paths"]]})
    certify(seed_checkpoint, "seed_law")
    if resumed_best is not None:
        if resumed_best.exists():
            previous = read_json(resumed_best)
            if previous["n"] != args.n:
                raise ValueError("resumed best law has wrong grid")
            replay = subprocess.run(["node", "--stack-size=16384", str(ROOT/"packages/interval_clock_grid/qout_primal_certificate.cjs"), str(resumed_best)],
                                    check=True, text=True, capture_output=True)
            verified = json.loads(replay.stdout)
            if verified["status"] != "PASS":
                raise ValueError("resumed exact upper replay failed")
            value = Fraction(verified["global_upper"])
            if value < best_upper:
                best_upper = value
                if resumed_best != output/"best.physical.json":
                    shutil.copyfile(resumed_best, output/"best.physical.json")
                (output/"best.replay.json").write_text(replay.stdout)
                write_json(output/"structure.json", law_structure(previous, initial_hashes))
            emit({"event": "resumed_best_exact_replay", "global_upper": str(value), "source_sha256": digest(resumed_best)})
    if args.profile_seed:
        from verify_native_field import load_table
        seed, table, _ = load_table(args.profile_seed)
        sn, sd = seed["n"], int(seed["field_denominator"])
        seed["radial_nodes"] = [[j,k,str(table[j*(2*sn+1)+k])] for j in range(12*sn+1) for k in range(1,2*sn+1) if (j+k)%2 == 0]
        trial = master.interpolate_seed(seed)
        best_answer, best_table = master.price(trial, keep=args.pricing_paths)
        best_dual = Fraction(int(best_answer["minimum_units"]), 4*args.n*master.D)
        anchor = master.profile_values(best_table)
        for path in best_answer["paths"]:
            master.add(path, best_table)
        cache.add_many(best_answer["paths"])
        emit({"event": "profile_seed_exact_price", "bank_dual": str(best_dual), "global_value_lower": str(best_dual-Fraction(1,2*args.n))})

    # This pre-solve checkpoint contains no claimed LP objective.  It still
    # resumes every physical column and random generator state if the first
    # enlarged LP exhausts its budget.
    write_json(output/"checkpoint.json", {
        "scope": "Resumable discovery geometry before the next LP solve; weights are placeholders and certify nothing.",
        "n": args.n, "profile_grid": args.n, "normalized_profile": True,
        "seed": args.seed, "family": args.family, "initial_law_sha256": digest(args.initial_law),
        "rng_state": rng.getstate(), "columns": master.columns, "weights": [0.]*len(master.columns),
        "profile": [], "upper": None, "history": history,
        "reservoir_paths": [{"start_grid": r.start, "moves": [2*s-1 for s in r.moves]} for r in cache._routes]})
    reason, loops, last_certified_upper = "iteration_limit", 0, None
    try:
        for iteration in range(args.iterations):
            if time.monotonic()-started >= args.seconds:
                reason = "wall_time_limit"
                break
            lp_start = time.monotonic()
            lp, weights, trial = backend.solve_lp(anchor, None if best_dual is None else float(best_dual))
            lp_seconds = time.monotonic()-lp_start
            cp = output/"checkpoint.json"
            write_json(cp, checkpoint(lp, weights))
            # Accept every proposed mixture independently, including a worse
            # one: the log never promotes the floating master objective.
            exact = certify(cp, len(history))
            last_certified_upper = exact["global_upper"]
            cache.update_columns(master.columns)
            if args.family == "mutations":
                active = [c["plan"] for c,w in zip(master.columns, weights) if w > 1e-10] or seed_plans
                proposals = mutate_routes(args.n, active, rng, args.mutation_count)
                new_mutations = cache.add_many(proposals)
            else:
                new_mutations = 0
            table = master.repair(trial)
            level = float(-lp.fun) if best_dual is None else float(best_dual) + .5*(float(-lp.fun)-float(best_dual))
            cached = cache.price(table, keep=args.pricing_paths, level=level)
            before = len(master.columns)
            for path in cached["violating_paths"]:
                master.add(path, table)
            additions = len(master.columns)-before
            full = args.family == "priced" or iteration % args.full_every == 0 or not additions
            report = {"event": "iteration", "iteration": len(history), "n": args.n,
                      "floating_master_upper": float(-lp.fun), "exact_physical_upper": exact["global_upper"],
                      "columns": before, "cached_paths": len(cache), "new_mutation_paths": new_mutations,
                      "new_cached_calendars": additions, "lp_seconds": lp_seconds,
                      "pricing_scope": "complete exact bank" if full else "cached counterexamples only"}
            if full:
                answer, table = master.price(trial, keep=args.pricing_paths)
                value = Fraction(int(answer["minimum_units"]), 4*args.n*master.D)
                report.update(exact_bank_dual=str(value), exact_global_value_lower=str(value-Fraction(1,2*args.n)),
                              retained_states=answer["retained_states"])
                if best_dual is None or value > best_dual:
                    best_dual, best_answer, best_table = value, answer, table
                    anchor = master.profile_values(table)
                    # save() enforces complete exact pricing; never call it
                    # with cached reservoir minima.
                    master.save(output/"best_dual", table, answer, lp,
                                np.r_[weights, np.zeros(len(master.columns)-len(weights))], history+[report])
                cache.add_many(answer["paths"])
                before_full = len(master.columns)
                for path in answer["paths"]:
                    master.add(path, table)
                report["new_full_calendars"] = len(master.columns)-before_full
            if hasattr(backend, "last_stats"):
                report["lp_stats"] = backend.last_stats
            if best_answer is not None and not (output/"best_dual.dual.json").exists():
                master.save(output/"best_dual", best_table, best_answer, lp,
                            np.r_[weights, np.zeros(len(master.columns)-len(weights))], history+[report])
            history.append(report)
            emit(report)
            write_json(cp, checkpoint(lp, weights))
            loops += 1
            if best_dual is not None and float(best_upper-best_dual) <= 2e-8:
                reason = "finite_bank_gap_closed"
                break
        summary = {"status": "BUDGET_STOPPED" if reason == "wall_time_limit" else "COMPLETED", "stop_reason": reason,
                   "scope": "Exact physical upper is unrestricted. Exact lower uses finite-bank game-value transfer, not same-CDF security. No exact unrestricted equilibrium is claimed.",
                   "iterations_this_run": loops, "iterations_total": len(history),
                   "best_certified_global_upper": str(best_upper) if best_upper is not None else None,
                   "last_certified_global_upper": last_certified_upper,
                   "baseline_global_upper": metadata["baseline_global_upper"],
                   "best_certified_global_value_lower": str(best_dual-Fraction(1,2*args.n)) if best_dual is not None else None,
                   "best_upper_improves_baseline": best_upper is not None and metadata["baseline_global_upper"] is not None and best_upper < Fraction(metadata["baseline_global_upper"]),
                   "elapsed_seconds": time.monotonic()-started}
        write_json(output/"summary.json", summary)
        emit({"event": "complete", **summary})
    except Exception as error:
        if "time limit" in str(error).lower() or "time_limit" in str(error).lower():
            summary = {"status": "BUDGET_STOPPED", "stop_reason": "lp_time_limit", "error": str(error),
                       "scope": "Only previously replayed physical upper certificates are retained. The unfinished LP provides no objective or bound.",
                       "iterations_this_run": loops, "iterations_total": len(history),
                       "best_certified_global_upper": str(best_upper) if best_upper is not None else None,
                       "baseline_global_upper": metadata["baseline_global_upper"],
                       "best_certified_global_value_lower": str(best_dual-Fraction(1,2*args.n)) if best_dual is not None else None,
                       "elapsed_seconds": time.monotonic()-started}
            write_json(output/"summary.json", summary)
            emit({"event": "budget_stop", **summary})
        else:
            write_json(output/"failure.json", {"status": "FAILED", "error": repr(error), "completed_iterations": loops,
                                              "best_certified_global_upper": str(best_upper) if best_upper is not None else None})
            raise
    finally:
        log.close()
        files = {str(p.relative_to(output)): digest(p) for p in output.rglob("*") if p.is_file() and "work" not in p.relative_to(output).parts and p.name != "manifest.json"}
        finished = read_json(output/"summary.json") if (output/"summary.json").exists() else {"status": "FAILED"}
        write_json(output/"manifest.json", {"sha256": files, "source_metadata": "metadata.json",
                                            "status": finished["status"], "options": metadata["arguments"],
                                            "best_certified_global_upper": str(best_upper) if best_upper is not None else None,
                                            "best_upper": str(best_upper) if best_upper is not None else None,
                                            "best_certified_global_value_lower": str(best_dual-Fraction(1,2*args.n)) if best_dual is not None else None})


if __name__ == "__main__":
    main()
