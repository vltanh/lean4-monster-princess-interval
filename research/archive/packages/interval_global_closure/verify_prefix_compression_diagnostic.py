#!/usr/bin/env python3
"""Replay exact fixed-field prefix comparisons with the chronological oracle.

The interpolation parameter is dimensionless: this fixture uses full width
1/2, not the saved explicit Princess strategy's narrow width 1/512.
No best-response, global bound, or equilibrium claim is made.
"""
from fractions import Fraction as Q
import argparse
import hashlib
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "record_bellman"))
from build_endpoint_tail_charts import Field
from replay_center_renewal_paths import integrate_path


def position(path, t):
    for (a, x), (b, y) in zip(path, path[1:]):
        if a <= t <= b:
            return x + (y-x)*(t-a)/(b-a)
    raise AssertionError("query outside the route")


def suffix(path, t):
    return [(t, position(path, t))] + [(s, x) for s, x in path if s > t]


def decode(path):
    return [(Q(t), Q(x)) for t, x in path]


def initial_records(field, path):
    t, x = path[0]
    f = field.cdf(t, x)
    return (Q(0) if x == -1 else f,
            Q(0) if x == 1 else 1-f)


def prefix_records(field, path, t):
    # Along a legal unit-speed leg the signed CDF is monotone, so extrema
    # and the two running records are determined by the segment endpoints.
    vertices = [(s, x) for s, x in path if s < t] + [(t, position(path, t))]
    left, right = initial_records(field, path)
    for s, x in vertices:
        f = field.cdf(s, x)
        left = Q(0) if x == -1 else min(left, f)
        right = Q(0) if x == 1 else min(right, 1-f)
    return left, right


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    data = json.loads((HERE / "early_return_prefix_deletion.json").read_text())
    field_bytes = (HERE / "lower_n256_front2_field.json").read_bytes()
    field_hash = hashlib.sha256(field_bytes).hexdigest()
    assert field_hash == data["field_sha256"]
    assert data["epsilon"] == "1/2"
    field = Field(json.loads(field_bytes), Q(data["epsilon"]))
    counts = {"source_routes": 0, "prefix_deletions": 0,
              "front_preserving_compressions": 0, "affine_intervals": 0}
    for row in data["rows"]:
        path = decode(row["route"])
        old, checks = integrate_path(field, path, *initial_records(field, path))
        assert old == Q(row["old_cost"])
        counts["source_routes"] += 1
        counts["affine_intervals"] += checks
        for item in row["prefix_deletions"] + row.get("small_prefix_derivatives", []):
            removed = Q(item["removed_prefix"])
            shifted = [(t-removed, x) for t, x in suffix(path, removed)]
            new, checks = integrate_path(field, shifted, *initial_records(field, shifted))
            assert new == Q(item["new_cost"])
            assert new-old == Q(item["difference"]) > 0
            if "difference_over_tau" in item:
                assert (new-old)/removed == Q(item["difference_over_tau"])
            assert checks == item["affine_checks"]
            counts["prefix_deletions"] += 1
            counts["affine_intervals"] += checks
        for item in row.get("front_preserving_two_triangle_compression", []):
            new_path = decode(item["new_route"])
            new, checks = integrate_path(field, new_path, *initial_records(field, new_path))
            assert new == Q(item["new_cost"])
            assert new-old == Q(item["cost_change"])
            t = Q(3, 8)
            old_records = prefix_records(field, path, t)
            new_records = prefix_records(field, new_path, t)
            assert old_records == tuple(map(Q, item["old_center_records"]))
            assert new_records == tuple(map(Q, item["new_center_records"]))
            assert sum(new_records)-sum(old_records) == Q(item["new_total_records_minus_old"])
            old_tail, old_checks = integrate_path(field, suffix(path, t), *old_records)
            new_tail, new_checks = integrate_path(field, suffix(new_path, t), *new_records)
            assert (new-new_tail)-(old-old_tail) == Q(item["prefix_cost_change"])
            counts["front_preserving_compressions"] += 1
            counts["affine_intervals"] += checks+old_checks+new_checks
    report = {"status": "PASS", "field_sha256": field_hash,
              "dimensionless_interpolation_epsilon": "1/2", "checks": counts,
              "scope": "Exact fixed-field chronological prefix comparisons; distinct from the saved narrow Princess law and not a game-value certificate."}
    text = json.dumps(report, indent=2)+"\n"
    args.report.write_text(text)
    print(text, end="")


if __name__ == "__main__":
    main()
