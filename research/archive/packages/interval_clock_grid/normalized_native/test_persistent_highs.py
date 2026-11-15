#!/usr/bin/env python3
"""Compare the persistent floating HiGHS master with the original SciPy solver."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import tempfile
import time

import numpy as np
from scipy.sparse import csr_matrix

from solve_normalized import Master
from persistent_highs import PersistentMaster, PersistentLP, highs


def require(ok, why):
    if not ok:
        raise AssertionError(why)


def append_saved(master, columns):
    for raw in columns:
        column = dict(raw)
        column["coeff"] = {int(k): v for k, v in raw["coeff"].items()}
        master.columns.append(column)
        master.seen.add((column["mass"], tuple(sorted(column["coeff"].items()))))


def feasibility(master, x, level):
    worst = max(float(np.max(-x)), float(np.max(x - 1.)), 0.)
    if master.order:
        worst = max(worst, max(float(x[a] - x[b]) for a, b in master.order))
    for column in master.columns:
        plane = (column["mass"] + sum(value * x[i] for i, value in column["coeff"].items())) / (4 * master.n)
        worst = max(worst, float(level - plane))
    return worst


def compare(master, persistent, anchor, lower):
    began = time.monotonic()
    pr, pw, px = persistent.solve_lp(anchor, lower)
    persistent_seconds = time.monotonic() - began
    began = time.monotonic()
    br, bw, bx = master.solve_lp(anchor, lower)
    scipy_seconds = time.monotonic() - began
    require(abs(pr.fun - br.fun) <= 2e-8, "master objective differs")
    require(abs(pw.sum() - 1.) < 2e-7 and pw.min() > -2e-8, "master dual weights")
    require(feasibility(master, pr.x[:-1], -pr.fun) <= 2e-7, "persistent master feasibility")
    row = {
        "cuts": len(master.columns), "upper": float(-pr.fun),
        "scipy_upper": float(-br.fun), "persistent_seconds": persistent_seconds,
        "scipy_seconds": scipy_seconds, "persistent": persistent.last_stats,
    }
    if anchor is not None and lower is not None and -pr.fun > lower + 1e-9:
        level = lower + .5 * (-pr.fun - lower)
        pl1, bl1 = float(np.abs(px-anchor).sum()), float(np.abs(bx-anchor).sum())
        require(abs(pl1-bl1) <= 2e-6 * max(1., pl1, bl1), "L1 prox optimum differs")
        require(feasibility(master, px, level) <= 2e-7, "persistent prox feasibility")
        row.update({"level": level, "persistent_l1": pl1, "scipy_l1": bl1})
    return row, px


def fallback_control():
    """Exercise the native IPM/crossover branch using an explicit status proxy."""
    lp = PersistentLP([1., 1.], csr_matrix([[-1., -1.], [-2., -1.]]),
                      [-1., -1.4], [0., 0.], [1., 1.])
    lp.highs.setOptionValue("presolve", "off")

    class UnknownOnce:
        def __init__(self, native):
            self.native, self.first = native, True

        def __getattr__(self, name):
            return getattr(self.native, name)

        def getModelStatus(self):
            if self.first:
                self.first = False
                return highs.HighsModelStatus.kUnknown
            return self.native.getModelStatus()

    lp.highs = UnknownOnce(lp.highs)
    result = lp.solve()
    require(abs(result.fun - 1.) < 1e-8 and lp.highs.getBasis().valid,
            "fallback optimum and crossover basis")
    require("fallback" in lp.last_stats and lp.last_stats["ipm_iterations"] > 0,
            "native IPM fallback branch was exercised")
    first = lp.last_stats.copy()
    lp.add_rows(csr_matrix([[-1., 0.]]), [-.75])
    result = lp.solve()
    require(abs(result.fun - 1.) < 1e-8 and "fallback" not in lp.last_stats,
            "post-fallback warm simplex")
    return {"scope": "Explicitly injected Unknown status; both subsequent native solves are real.",
            "fallback": first, "warm_update": lp.last_stats}


def cumulative_timer_control():
    """Reproduce the real native cumulative deadline, then recover warm."""
    lp=PersistentLP([1.,1.],csr_matrix([[-1.,-1.]]),[-1.],
                    [0.,0.],[1.,1.],time_limit=1.)
    lp.highs.setOptionValue('presolve','off')
    lp.solve();previous=float(lp.highs.getRunTime())
    require(previous>0,'native run clock did not advance')
    lp.highs.setOptionValue('time_limit',previous/2)
    lp.add_rows(csr_matrix([[-1.,0.]]),[-.25])
    lp.highs.run()
    expired=lp.highs.getModelStatus()
    require(expired==highs.HighsModelStatus.kTimeLimit,
            'expected the elapsed native cumulative deadline to stop the real solve')
    result=lp.solve()
    require(abs(result.fun-1.)<1e-8 and lp.highs.getBasis().valid,
            'refreshed deadline did not recover the real warm solve')
    return {'scope':'Real native cumulative timer rejection and warm recovery; no injected status or sleep.',
            'expired_status':lp.highs.modelStatusToString(expired),
            'runtime_before_expired_attempt':previous,'recovered':lp.last_stats}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--checkpoint", type=Path)
    parser.add_argument("--output", type=Path,
                        default=Path(__file__).with_name("persistent_highs_replay.json"))
    args = parser.parse_args()
    report = {"scope": "Floating solver equivalence and warm-basis performance; no exact game certificate.",
              "small_runs": [], "checkpoint_benchmark": []}
    report["forced_fallback_control"] = fallback_control()
    report["cumulative_timer_control"] = cumulative_timer_control()
    with tempfile.TemporaryDirectory(prefix="persistent-highs-regression-") as tmp:
        root = Path(tmp)
        for n in (2, 4):
            master = Master(n, root / ("n" + str(n)))
            table = master.repair(np.zeros(master.K))
            master.add({"start_grid": master.R, "moves": [-1]*(2*master.R)}, table)
            master.add({"start_grid": 0,
                        "moves": [1]*n+[-1]*(3*n)+[1]*(4*n)}, table)
            persistent = PersistentMaster(master)
            best, anchor = None, None
            rows = []
            for iteration in range(18):
                row, x = compare(master, persistent, anchor, best)
                answer, table = master.price(x, keep=16)
                value = int(answer["minimum_units"])/(4*n*master.D)
                if best is None or value > best:
                    best = value
                    anchor = np.asarray([int(table[j,k])/master.D for j,k in master.nodes])
                row.update({"iteration": iteration, "priced": value})
                rows.append(row)
                added = sum(master.add(path, table) for path in answer["paths"])
                if not added:
                    break
            # With no new rows/bounds, both retained bases should solve directly.
            repeated, _ = compare(master, persistent, anchor, best)
            rows.append(dict(repeated, repeat_without_new_cuts=True))
            report["small_runs"].append({"n": n, "iterations": rows})
        if args.checkpoint:
            frozen = None
            for attempt in range(10):
                raw = args.checkpoint.read_bytes()
                try:
                    frozen = json.loads(raw)
                    break
                except json.JSONDecodeError:
                    time.sleep(.05)
            require(frozen is not None, "could not obtain complete checkpoint snapshot")
            report["checkpoint_sha256"] = hashlib.sha256(raw).hexdigest()
            n, columns = frozen["n"], frozen["columns"]
            master = Master(n, root / "checkpoint", normalized_profile=frozen.get("normalized_profile", False))
            total = len(columns)
            batch = min(64, max(1, total//6))
            stops = sorted(set((max(1, total-2*batch), max(1, total-batch), total)))
            append_saved(master, columns[:stops[0]])
            persistent = PersistentMaster(master)
            anchor = np.asarray(frozen["profile"], dtype=float)
            last = frozen["history"][-1]
            lower = last['best_exact_dual'] if 'best_exact_dual' in last else last['exact_normalized_dual']
            dual_path = args.checkpoint.with_name(args.checkpoint.name.replace(".checkpoint.json", ".dual.json"))
            if dual_path.exists():
                dual = json.loads(dual_path.read_text())
                values = {(j,k): int(value) / int(dual["field_denominator"])
                          for j,k,value in dual["radial_nodes"]}
                anchor = np.asarray([values[j,k] for j,k in master.nodes])
                lower = int(dual["minimum_units"]) / int(dual["objective_denominator"])
            previous = stops[0]
            for index, stop in enumerate(stops):
                if stop > previous:
                    append_saved(master, columns[previous:stop])
                row, _ = compare(master, persistent, anchor, lower)
                row.update({"stage": index, "n": n, "variables": master.K})
                report["checkpoint_benchmark"].append(row)
                previous = stop
            # Exercise a new anchor and level with no matrix reconstruction.
            shifted_anchor = np.clip(anchor + 1e-4*np.sin(np.arange(master.K)), 0., 1.)
            row, _ = compare(master, persistent, shifted_anchor, lower-1e-4)
            row.update({"stage": "changed_anchor_and_level", "n": n, "variables": master.K})
            report["checkpoint_benchmark"].append(row)
        report["status"] = "passed"
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": "passed", "small_comparisons": sum(
        len(x["iterations"]) for x in report["small_runs"]),
        "checkpoint_comparisons": len(report["checkpoint_benchmark"])}))
    for row in report["checkpoint_benchmark"]:
        print(json.dumps({key: row[key] for key in (
            "stage", "n", "cuts", "persistent_seconds", "scipy_seconds")}))
        print(json.dumps(row["persistent"], sort_keys=True))


if __name__ == "__main__":
    main()

