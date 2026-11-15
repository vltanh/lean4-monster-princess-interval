#!/usr/bin/env python3
"""Check an all-calendar obstruction and its continuous quadrature diagnostic.

No LP or maximum-flow solver is trusted here.  A feasible integer Qout field
and all retained physical paths determine every number by prefix minima.
"""
from fractions import Fraction as Q
import argparse
import gzip
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def load(field_path=None, marginals_path=None):
    field_path = field_path or HERE / "blocking_field_n128.json.gz"
    marginals_path = marginals_path or HERE / "seed_plain_marginals.json"
    raw = field_path.read_bytes()
    data = json.loads(gzip.decompress(raw))
    n, D = int(data["n"]), int(data["field_denominator"])
    nodes = [(j, k) for j in range(4*n+1) for k in range(1, 2*n+1)
             if (j+k) % 2 == 0]
    values = data["field_values"]
    assert len(values) == len(nodes)
    assert all(type(v) is int and 0 <= v <= D for v in values)
    table = dict(zip(nodes, values))
    for (j, k), a in table.items():
        if k < 2*n:
            for s in (-1, 1):
                if 0 <= j+s <= 4*n:
                    assert a <= table[j+s, k+1]
    for j in range(0, 4*n, 2):
        assert table[j+2, 2*n] <= table[j, 2*n]
    compact = json.loads(marginals_path.read_text())
    assert compact["n"] == n
    if "physical_pairs" not in compact:
        pairs = []
        for plan in compact["routes"]:
            runs = []
            for direction in plan["moves"]:
                if runs and runs[-1][0] == direction:
                    runs[-1][1] += 1
                else:
                    runs.append([direction, 1])
            pairs.append({"start_grid": plan["start_grid"], "runs": runs,
                          "weight_numerator": plan["weight_numerator"]})
        compact = dict(compact, physical_pairs=pairs)
    return data, table, compact


def route_scores(n, D, table, plan, scale):
    """Return nodal sum and outward-rounded continuous integral numerators.

    In these units each time step has duration one and each survival record
    lies in [0,2D]. Divide the result by 4*n*D (and by scale for intervals).
    A full-width common-threshold field is affine on every lattice edge.
    """
    positions = [int(plan["start_grid"])]
    for direction, count in plan["runs"]:
        assert direction in (-1, 1) and type(count) is int and count > 0
        for _ in range(count):
            positions.append(positions[-1] + direction)
    assert all(abs(k) <= 2*n for k in positions)
    assert positions.index(0) <= 4*n
    assert max(positions.index(-2*n), positions.index(2*n)) <= 12*n

    def radial(j, k):
        if j > 4*n:
            k -= j - 4*n
            j = 4*n
        return 0 if k <= 0 else table[j, k]

    nodal = lower = upper = crossings = 0
    for sign, endpoint in ((1, -2*n), (-1, 2*n)):
        # An actual start at its own endpoint gives an empty clock, including
        # endpoint atoms. The one-sided trace is used only before first arrival.
        end = positions.index(endpoint)
        record = 2*D + 1
        for j in range(end):
            x, y = positions[j:j+2]
            a = D + (1 if sign*x >= 0 else -1)*radial(j, abs(x))
            b = D + (1 if sign*y >= 0 else -1)*radial(j+1, abs(y))
            record = min(record, a)
            nodal += record
            if b >= record:
                numerator, denominator = record, 1
            else:
                # Integral of min(record, a+(b-a)t), 0 <= t <= 1.
                numerator = 2*record*(a-b) - (record-b)**2
                denominator = 2*(a-b)
                crossings += a > record
            lower += numerator*scale // denominator
            upper += (numerator*scale + denominator-1) // denominator
            record = min(record, b)
    return nodal, lower, upper, crossings


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--result-directory", type=Path,
                        help="Check a new search's blocking.field/report.json and physical_marginals.json.")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if args.result_directory:
        folder = args.result_directory
        expected = json.loads((folder / "blocking.report.json").read_text())
        field_path, law_path = folder / "blocking.field.json.gz", folder / "physical_marginals.json"
        assert hashlib.sha256(field_path.read_bytes()).hexdigest() == expected["field_sha256"]
        assert hashlib.sha256(law_path.read_bytes()).hexdigest() == expected["physical_marginals_sha256"]
        data, table, law = load(field_path, law_path)
    else:
        expected = json.loads((HERE / "blocking_field_report.json").read_text())
        data, table, law = load()
        assert hashlib.sha256((HERE / "blocking_field_n128.json.gz").read_bytes()).hexdigest() == expected["blocking_field_sha256"]
        assert hashlib.sha256((HERE / "seed_manifest.json").read_bytes()).hexdigest() == expected["seed_manifest_sha256"]
        seed = json.loads((HERE / "seed_manifest.json").read_text())
        assert hashlib.sha256((HERE / "seed_plain_marginals.json").read_bytes()).hexdigest() == seed["files_sha256"]["seed_plain_marginals.json"]
    n, D = data["n"], int(data["field_denominator"])
    scale, W = int(expected.get("interval_rounding_scale", 10**6)), int(law["weight_denominator"])
    assert sum(int(p["weight_numerator"]) for p in law["physical_pairs"]) == W
    nodal = lower = upper = crossings = 0
    for plan in law["physical_pairs"]:
        mass = int(plan["weight_numerator"])
        assert mass > 0
        a, b, c, d = route_scores(n, D, table, plan, scale)
        nodal += mass*a
        lower += mass*b
        upper += mass*c
        crossings += d
    family = Q(nodal, 4*n*D*W)
    lo, hi = Q(lower, 4*n*D*W*scale), Q(upper, 4*n*D*W*scale)
    assert str(family) == expected["all_calendar_family_floor"]
    if "actual_continuous_payoff_lower" in expected:
        assert str(lo) == expected["actual_continuous_payoff_lower"]
        assert str(hi) == expected["actual_continuous_payoff_upper"]
        assert crossings == expected["strict_interior_running_minimum_crossings"]
    target = Q(expected["global_target_upper"])
    assert family >= target
    report = {
        "status": "PASS", "n": n, "physical_pairs": len(law["physical_pairs"]),
        "all_calendar_family_floor": str(family),
        "actual_continuous_payoff_interval": [str(lo), str(hi)],
        "continuous_interval_width": str(hi-lo),
        "nodal_minus_continuous_lower": str(family-hi),
        "global_target_upper": str(target),
        "actual_fixed_law_obstructed_by_this_field": lo >= target,
        "scope": "This grid's nodal-clock certificate family is blocked for this fixed law. The continuous interval separately quantifies the actual response of this field. No game-value lower is asserted.",
    }
    if args.output:
        args.output.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
