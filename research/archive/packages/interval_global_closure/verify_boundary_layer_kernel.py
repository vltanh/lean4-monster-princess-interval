#!/usr/bin/env python3
"""Exact physical replay of the two-parameter endpoint-layer kernel.

Uses only chronological affine intersections and Python's standard library.
An optional n64 physical certificate is inspected for the boundary-gap
diagnostic. This script does not replay that certificate's max-flow witness.
"""
from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction as Q
import gzip
import hashlib
import json
from pathlib import Path


def clean(points):
    out = []
    for t, x in points:
        t, x = Q(t), Q(x)
        if out and t == out[-1][0]:
            assert x == out[-1][1], (out[-1], (t, x))
            continue
        if out:
            assert t > out[-1][0]
            assert abs(x - out[-1][1]) <= t - out[-1][0]
        assert -1 <= x <= 1
        out.append((t, x))
    assert out[0][0] == 0
    return out


def value(path, t):
    for (s, x), (u, y) in zip(path, path[1:]):
        if s <= t <= u:
            return x + (y - x) * (t - s) / (u - s)
    assert t >= path[-1][0]
    return path[-1][1]


def contact(a, b):
    """First contact, with both paths held at their final position afterward."""
    times = sorted({t for t, _ in a} | {t for t, _ in b})
    for idx, t in enumerate(times):
        if value(a, t) == value(b, t):
            return t
        # A linear difference has at most one zero in each open interval.
        if idx + 1 == len(times):
            break
        u = times[idx + 1]
        d0, d1 = value(a, t) - value(b, t), value(a, u) - value(b, u)
        if d0 * d1 < 0:
            return t + (u - t) * d0 / (d0 - d1)
    raise AssertionError("uncaught target in finite replay")


def princess(epsilon, h):
    assert 0 <= epsilon <= h < 1
    turn = (h - epsilon) / 2
    return clean([(0, 1 - epsilon), (turn, 1 - epsilon - turn),
                  (h, 1), (4, 1)])


def monster(a, z):
    """Start 1-a, inward first, turn outward, then descend on t+x=1."""
    assert 0 <= a <= z < 1
    return clean([(0, 1-a), ((z-a)/2, 1-(z+a)/2),
                  (z/2, 1-z/2), (2, -1), (4, 1)])


def pair_score(m, p):
    return (contact(m, p) + contact(m, [(t, -x) for t, x in p])) / 2


def kernel(a, z, epsilon, h):
    if epsilon == a:  # Actual initial co-location, not a one-sided trace.
        return Q(1), "initial_contact"
    if h == z:
        return 1 + (z - min(a, epsilon)) / 4, "turn_contact"
    if epsilon > a:
        if h < z:
            return 1 + (h-a)/4, "outside_short_loop"
        return 1 + h/4, "outside_long_loop"
    if h < z:
        return Q(3), "inside_short_loop"
    return 1 + (z-epsilon)/4, "inside_long_loop"


def check_kernel():
    # All four strict regions, both ties, immediate-outward Princesses,
    # and zero-length initial inward Monster legs occur on this grid.
    # Zero deficits test actual endpoint co-location, not a limiting germ.
    grid = [Q(i, 12) for i in range(12)]
    counts = Counter()
    sweep = clean([(0, 1), (2, -1), (4, 1)])
    sweep_count = 0
    for h in grid:
        for epsilon in grid:
            if epsilon > h:
                continue
            p = princess(epsilon, h)
            assert pair_score(sweep, p) == (1 if epsilon == 0 else 1 + h/4)
            sweep_count += 1
            for z in grid:
                for a in grid:
                    if a > z:
                        continue
                    m = monster(a, z)
                    expected, case = kernel(a, z, epsilon, h)
                    actual = pair_score(m, p)
                    assert actual == expected, (a, z, epsilon, h, actual, expected)
                    assert contact(m, [(t, -x) for t, x in p]) == 2
                    counts[case] += 1
    return {"cases": sum(counts.values()), "case_counts": dict(sorted(counts.items())),
            "fast_sweep_cases": sweep_count,
            "scope": "finite exact regression of the analytic contact formula, including ties"}


def decode_route(row, step):
    position = int(row["start_grid"])
    raw = [(Q(0), position * step)]
    last_move = None
    for j, d in enumerate(row["moves"]):
        assert d in (-1, 1)
        if last_move is not None and d != last_move:
            raw.append((j * step, position * step))
        position += d
        assert -1 <= position * step <= 1
        last_move = d
    raw.append((len(row["moves"]) * step, position * step))
    return clean(raw)


def endpoint_times(route):
    return (contact(route, [(Q(0), Q(-1))]),
            contact(route, [(Q(0), Q(1))]))


def inspect_certificate(path):
    raw = path.read_bytes()
    data = json.loads(gzip.decompress(raw) if path.suffix == ".gz" else raw)
    assert data["pair_law"] == "fair_reflection"
    step, denominator = Q(data["physical_step"]), int(data["weight_denominator"])
    n = int(data["n"])
    assert step == Q(1, 2*n)
    routes = []
    total, endpoint_weight, baseline = 0, 0, Q(0)
    max_interior = Q(0)
    for row in data["paths"]:
        weight = int(row["weight_numerator"])
        assert weight > 0
        total += weight
        route = decode_route(row, step)
        minus, plus = endpoint_times(route)
        center = contact(route, [(Q(0), Q(0))])
        assert center <= 2
        first = min(minus, plus)
        assert max(minus, plus) == first + 2
        # The post-first-endpoint tail must really be the direct sweep.
        sign = value(route, first)
        for t, x in route:
            if first <= t <= first+2:
                assert x == sign * (1-(t-first))
        baseline += Q(weight, denominator) * (minus + plus)/2
        start = abs(route[0][1])
        if start == 1:
            endpoint_weight += weight
            assert first == 0
        else:
            max_interior = max(max_interior, start)
        routes.append((weight, route, minus, plus, center))
    assert total == denominator
    q, delta = Q(endpoint_weight, denominator), 1-max_interior
    upper = Q(data["global_upper"])
    diagnostic = upper - baseline - q*delta/4
    replayed_scores = []
    for hfactor in (Q(1,4), Q(1,2), Q(3,4)):
        h = hfactor * delta
        for epsilon in (h/3, h):
            p = princess(epsilon, h)
            score = Q(0)
            for weight, route, minus, plus, _ in routes:
                actual = pair_score(route, p)
                if abs(route[0][1]) < 1:
                    assert actual == (minus+plus)/2
                else:
                    assert actual == 1+h/4
                score += Q(weight, denominator)*actual
            assert score == baseline + q*h/4
            replayed_scores.append({"epsilon": str(epsilon), "h": str(h), "score": str(score)})
    cutoff_checks = 0
    if n == 64:
        assert q == Q(630441926044, 10**12)
        assert delta == Q(1,64)
        assert baseline == Q(2276326166273, 1600000000000)
        assert diagnostic == Q(5567, 256000000000000)
        for a in [Q(i,128) for i in range(129)]:
            h = max((center for _, route, _, _, center in routes if abs(route[0][1]) > a), default=Q(0))
            if a < Q(9,16):
                expected = Q(23,16)
            elif a < Q(63,64):
                expected = 2-Q((64*a).__floor__()+1,64)
            elif a < 1:
                expected = Q(1)
            else:
                expected = Q(0)
            assert h == expected, (a,h,expected)
            cutoff_checks += 1
    return {"file_sha256": hashlib.sha256(raw).hexdigest(), "n": n,
            "calendar_plans": len(routes), "total_weight_numerator": str(total),
            "endpoint_weight": str(q), "interior_gap": str(delta),
            "stationary_endpoint_score": str(baseline),
            "stored_certified_upper": str(upper),
            "upper_minus_boundary_limit": str(diagnostic),
            "exact_loop_scores": replayed_scores, "cutoff_checks": cutoff_checks,
            "scope": "exact route legality, endpoint-tail, chronological loop-payoff and diagnostic replay; max-flow witness not replayed here"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--physical-certificate", type=Path)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    report = {"status": "PASS", "kernel": check_kernel()}
    if args.physical_certificate:
        report["physical_certificate"] = inspect_certificate(args.physical_certificate)
    report["script_sha256"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    text = json.dumps(report, indent=2)+"\n"
    if args.report:
        args.report.write_text(text)
    print(text, end="")


if __name__ == "__main__":
    main()
