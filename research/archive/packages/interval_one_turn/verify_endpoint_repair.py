#!/usr/bin/env python3
"""Exact physical kernels and saved-law endpoint-repair obstruction.

The arbitrary-measure theorem is proved in ONE_TURN_ENDPOINT_REPAIR_OBSTRUCTION.md.
This standard-library replay checks its physical kernels and all input fractions.
"""
from __future__ import annotations

from fractions import Fraction as Q
import gzip
import hashlib
import json
from pathlib import Path

from verify_domain import Path as PhysicalPath, direct_first_hit


HERE = Path(__file__).resolve().parent
BENCHMARK = Q(291849329389899, 204800000000000)


def princess(e):
    assert 0 < e < 1
    return PhysicalPath.make(((0, 1-e), (e, 1), (6, 1)))


def pair_payoff(m, e):
    p = princess(e)
    return (direct_first_hit(m, p) + direct_first_hit(m, p.reflected())) / 2


def opposite_first(a, h):
    assert 0 < a <= 1 and 0 <= h < a
    d = a - 2*h
    return PhysicalPath.make(((0, 1-a), (h, 1-a+h),
                              (2-d, -1), (4-d, 1), (6, 1)))


def same_first(a, z):
    assert 0 < a <= 1 and a <= z < 4-a
    return PhysicalPath.make(((0, 1-a), ((z-a)/2, 1-(a+z)/2),
                              (z, 1), (z+2, -1), (6, -1)))


def kernel_a(a, d, e):
    if e < a:
        return 3-d
    if e == a:
        return 1-d/2
    return 1+e/4-3*d/4


def kernel_b(a, z, e):
    if e < a:
        return 1+z
    if e == a:
        return 1+z/2
    if e <= z:
        return 1+z/2+(e-a)/4
    return 1+3*z/4+e/4


def check_kernels():
    count_a = count_b = 0
    for i in range(1, 9):
        a = Q(i, 8)
        es = {Q(k, 16) for k in range(1, 16)}
        if a < 1:
            es.add(a)
        for j in range(4):
            h = a * Q(j, 4)
            d = a - 2*h
            m = opposite_first(a, h)
            for e in es:
                assert pair_payoff(m, e) == kernel_a(a, d, e)
                count_a += 1
        for j in range(8):
            z = a + (4-2*a) * Q(j, 8)
            m = same_first(a, z)
            tied_es = es | ({z} if z < 1 else set())
            for e in tied_es:
                actual = pair_payoff(m, e)
                assert actual == kernel_b(a, z, e)
                assert actual >= 1+e/4
                count_b += 1
    outside_checks = 0
    for delta in (Q(1, 128), Q(1, 4), Q(1, 2)):
        for a in (delta+(1-delta)/4, delta+(1-delta)/2, Q(1)):
            for j in range(4):
                h = a*Q(j, 4)
                d = a-2*h
                m = opposite_first(a, h)
                for e in (delta/3, 2*delta/3):
                    value = pair_payoff(m, e)
                    assert value == 3-d
                    assert value >= 1+a > 1+delta > 1+e/4
                    outside_checks += 1
            for j in range(4):
                z = a+(4-2*a)*Q(j, 4)
                m = same_first(a, z)
                for e in (delta/3, 2*delta/3):
                    value = pair_payoff(m, e)
                    assert value == 1+z
                    assert value >= 1+a > 1+delta > 1+e/4
                    outside_checks += 1
    return count_a, count_b, outside_checks


def read_saved_law():
    raw = (HERE / "one_turn_upper.json.gz").read_bytes()
    data = json.loads(gzip.decompress(raw))
    assert data["format"] == "one-turn-run-length-v1"
    assert data["pair_law"] == "fair_reflection"
    n, W = data["n"], int(data["weight_denominator"])
    assert n == 256 and W == 10**12
    R = 2*n
    total = endpoint_mass = endpoint_times = 0
    interior_starts = []
    catalog = []
    for row in data["paths"]:
        weight = int(row["weight_numerator"])
        assert weight > 0
        total += weight
        start = row["start_grid"]
        assert type(start) is int and start % 2 == 0 and abs(start) <= R
        moves = []
        knot_positions = [(0, start)]
        step, x = 0, start
        for sign, length in row["move_runs"]:
            assert type(sign) is int and sign in (-1, 1)
            assert type(length) is int and length > 0
            moves.extend([sign] * length)
            step += length
            x += sign * length
            assert abs(x) <= R
            knot_positions.append((step, x))
        positions = [start]
        for move in moves:
            positions.append(positions[-1] + move)
            assert abs(positions[-1]) <= R
        assert -R in positions and R in positions
        left, right = positions.index(-R), positions.index(R)
        first, last = min(left, right), max(left, right)
        assert last == len(moves)
        assert positions.index(0) <= 4*n
        assert sum(moves[j] != moves[j-1]
                   for j in range(1, first)) <= 1
        assert last-first == 2*R
        sign = 1 if positions[first] == -R else -1
        assert all(move == sign for move in moves[first:last])
        endpoint_times += weight * (left+right)
        if abs(start) == R:
            endpoint_mass += weight
        else:
            interior_starts.append(abs(start))
        knots = [(Q(t, R), Q(x, R)) for t, x in knot_positions]
        knots.append((Q(6), knots[-1][1]))
        catalog.append((Q(weight, W), PhysicalPath.make(knots)))
    assert total == W
    q = Q(endpoint_mass, W)
    delta = 1-Q(max(interior_starts), R)
    baseline = Q(endpoint_times, 2*R*W)
    return data, catalog, q, delta, baseline, hashlib.sha256(raw).hexdigest()


def main():
    count_a, count_b, outside_checks = check_kernels()
    data, catalog, q, delta, M, digest = read_saved_law()
    assert q == Q(158373491249, 250000000000)
    assert delta == Q(1, 128)
    assert M == Q(182280512903797, 128000000000000)
    old_law_checks = 0
    for e in (delta/8, delta/2, 7*delta/8):
        actual = sum((weight*pair_payoff(path, e)
                      for weight, path in catalog), Q(0))
        assert actual == M+q*e/4
        old_law_checks += len(catalog)
    floor = M+q*delta/4
    gain = 3*q*delta*delta/(4*(8-delta))
    barrier = floor-gain
    lam = 3*delta/(8-delta)
    assert lam*(2/delta-1) - (1-lam)*Q(3, 4) == 0
    assert barrier == M+q*delta*(2-delta)/(8-delta)
    assert floor == Q(91219443197523, 64000000000000)
    assert gain == Q(158373491249, 43648000000000000)
    assert barrier == Q(62211501887219437, 43648000000000000)
    assert barrier-BENCHMARK == Q(88908487977701, 349184000000000000)
    assert Q(data["global_upper"])-floor == Q(9803, 1024000000000000)
    assert barrier > BENCHMARK
    print(json.dumps({
        "status": "PASS",
        "scope": "arbitrary B1 replacement of endpoint component with old bulk fixed; not a W1 lower",
        "opposite_first_kernel_checks": count_a,
        "same_first_kernel_and_domination_checks": count_b,
        "outside_gap_and_center_start_checks": outside_checks,
        "saved_physical_plan_test_comparisons": old_law_checks,
        "saved_law_sha256": digest,
        "q": str(q),
        "delta": str(delta),
        "old_baseline": str(M),
        "old_endpoint_floor": str(floor),
        "maximum_permitted_floor_improvement": str(gain),
        "repair_family_response_lower": str(barrier),
        "repair_family_response_lower_decimal": float(barrier),
        "barrier_minus_benchmark": str(barrier-BENCHMARK),
        "saved_upper_minus_endpoint_floor": str(Q(data["global_upper"])-floor),
    }, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()

