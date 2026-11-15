#!/usr/bin/env python3
"""Independent Fraction and native-oracle checks of the cached separator."""
from __future__ import annotations

from fractions import Fraction
import hashlib
import json
from pathlib import Path
import random
import struct
import subprocess
import tempfile

import numpy as np

from cached_path_pricing import CachedPathPricing, normalize_path, UINT64_MAX
from test_price_normalized import order_profile, binary_input

HERE = Path(__file__).resolve().parent


def check(ok, message):
    if not ok:
        raise AssertionError(message)


def normalized_routes(n):
    radius, cutoff = 2 * n, 4 * n

    def completed(start, moves, x, first):
        result = list(moves)
        for target in (first, -first):
            direction = 1 if target > x else -1
            result += [direction] * abs(target - x)
            x = target
        positions = [start]
        for direction in result:
            positions.append(positions[-1] + direction)
        if 0 in positions[:cutoff + 1]:
            yield {"start_grid": start, "moves": result}

    def visit(start, moves, x):
        if abs(x) == radius:
            yield from completed(start, moves, x, x)
        elif len(moves) == cutoff:
            for first in (-radius, radius):
                yield from completed(start, moves, x, first)
        else:
            for direction in (-1, 1):
                yield from visit(start, moves + [direction], x + direction)

    for start in range(-radius, radius + 1, 2):
        yield from visit(start, [], start)


def fraction_cost(n, D, field, route):
    """Chronological capture-plane integration, with Python integer rationals."""
    radius, x = 2 * n, route["start_grid"]
    alive_left, alive_right = x != -radius, x != radius
    left = right = None
    answer = Fraction(0)
    dt = Fraction(1, 2 * n)
    centered = x == 0
    for j, step in enumerate(route["moves"]):
        value = int(field[j, abs(x)])
        p = Fraction(D + (value if x >= 0 else -value), 2 * D)
        if alive_left:
            left = p if left is None else min(left, p)
            answer += left * dt
        if alive_right:
            right = 1 - p if right is None else min(right, 1 - p)
            answer += right * dt
        x += step
        check(abs(x) <= radius, "route arena")
        centered |= x == 0 and j + 1 <= 4 * n
        alive_left &= x != -radius
        alive_right &= x != radius
    check(not alive_left and not alive_right and centered, "completed center-by-two route")
    units = answer * (4 * n * D)
    check(units.denominator == 1, "integer pricing scale")
    return units.numerator


def main():
    executable, source = HERE / "price_normalized", HERE / "price_normalized.cpp"
    if not executable.exists() or executable.stat().st_mtime < source.stat().st_mtime:
        subprocess.run(["g++", "-O3", "-std=c++17", str(source), "-o", str(executable)], check=True)
    stats = {"profiles": 0, "fraction_route_checks": 0, "native_minimum_comparisons": 0,
             "native_witness_checks": 0, "normalization_checks": 0, "incremental_cache_checks": 0,
             "level_checks": 0, "malformed_rejections": 0, "maximum_exact_units_bits": 0}
    cases = []
    rng = random.Random(718262144)
    with tempfile.TemporaryDirectory(prefix="cached_path_test_") as tmp:
        for n in (1, 2):
            routes = list(normalized_routes(n))
            cache = CachedPathPricing(n, 10**9, chunk_size=7)
            columns = [{"plan": p} for p in routes]
            cache.update_columns(columns[:5])
            cache.update_columns(columns)
            check(cache.update_columns(columns) == 0, "unchanged append-only cache")
            expected_unique = {tuple([p["start_grid"]] + p["moves"]) for p in
                               (normalize_path(n, p) for p in routes)}
            check(len(cache) == len(expected_unique), "canonical physical deduplication")
            stats["incremental_cache_checks"] += 2
            check(cache.add_many(routes) == 0, "duplicate native routes")
            for case in range(4):
                D = 10**9
                seeds = [] if case == 0 else [(rng.randrange(12*n+1), rng.randrange(1,2*n+1), rng.randrange(D+1))
                                              for _ in range(3+case)]
                field = np.asarray(order_profile(n, D, seeds), dtype=np.uint64)
                answer = cache.price(field, keep=len(cache), level="3/2", tolerance="1e-7")
                check(answer["certifies_lower"] is False and answer["bound_direction"] == "upper", "scope guard")
                costs = []
                for route in answer["paths"]:
                    value = fraction_cost(n, D, field, route)
                    check(value == int(route["units"]), "vector cost != Fraction chronological cost")
                    costs.append(value)
                    stats["fraction_route_checks"] += 1
                check(costs == sorted(costs), "sorted witness costs")
                check(min(costs) == int(answer["cached_minimum_units"]), "cached minimum")
                for route in answer["paths"]:
                    should = Fraction(int(route["units"]), 4*n*D) < Fraction(3,2)-Fraction(1,10**7)
                    check((route in answer["violating_paths"]) == should, "exact level classification")
                    stats["level_checks"] += 1
                target = Path(tmp) / f"field{n}_{case}.bin"
                binary_input(target, n, D, field.tolist())
                native = json.loads(subprocess.check_output([str(executable), str(target), "12"], text=True))
                check(native["minimum_units"] == answer["cached_minimum_units"], "exhaustive cached bank != native minimum")
                stats["native_minimum_comparisons"] += 1
                for route in native["paths"]:
                    check(fraction_cost(n, D, field, route) == int(route["units"]), "native witness exact replay")
                    check(cache.add(route) is False, "native route absent from exhaustive cache")
                    stats["native_witness_checks"] += 1
                # Same cache against a changed field must recompute every record.
                check(cache.price(field, keep=0)["cached_minimum_units"] == answer["cached_minimum_units"], "value-only cached mode")
                stats["profiles"] += 1
                cases.append({"n": n, "case": case, "cached_paths": len(cache),
                              "minimum_units": answer["cached_minimum_units"]})
        # Full-bank paths with obsolete wandering suffixes normalize exactly.
        examples = [
            (2, {"start_grid": -4, "moves": [1]*4 + [-1,1]*3 + [1]*4},
             {"start_grid": 4, "moves": [-1]*8}),
            (1, {"start_grid": 0, "moves": [1,-1,1,-1,1,-1,1,1,-1,-1,-1,-1]},
             {"start_grid": 0, "moves": [1,-1,1,-1,1,1,-1,-1,-1,-1]}),
        ]
        for n, raw, expected in examples:
            check(normalize_path(n, raw) == expected, "known physical normalization")
            check(normalize_path(n, expected) == expected, "idempotent normalization")
            stats["normalization_checks"] += 2
        coarse = {"start_grid": -2, "moves": [1]*4}
        check(normalize_path(2, coarse, source_n=1) == {"start_grid": 4, "moves": [-1]*8}, "integer path refinement")
        stats["normalization_checks"] += 1
        # Chunk cache growth through both a full-block boundary and a new tail.
        grow = CachedPathPricing(2, 100, chunk_size=3, canonical_reflection=False)
        routes = list(normalized_routes(2))
        zero = np.zeros((25,5), dtype=np.uint64)
        for size in (1,2,3,4,6,7,10):
            grow.add_many(routes[:size])
            answer = grow.price(zero, keep=len(grow))
            for route in answer["paths"]:
                check(int(route["units"]) == fraction_cost(2,100,zero,route), "incremental vector batch")
            stats["incremental_cache_checks"] += 1
        # Values well beyond 2**53 and almost maximal conservative uint64 scale.
        D = UINT64_MAX // 48
        big = CachedPathPricing(1, D, chunk_size=3)
        big.add_many(normalized_routes(1))
        field = np.zeros((13,3), dtype=np.uint64)
        for route in big.price(field, keep=len(big))["paths"]:
            check(int(route["units"]) == fraction_cost(1,D,field,route), "large uint64 exact price")
            stats["maximum_exact_units_bits"] = max(stats["maximum_exact_units_bits"], int(route["units"]).bit_length())
            stats["fraction_route_checks"] += 1

        def reject(fn):
            try:
                fn()
            except (ValueError, OverflowError):
                stats["malformed_rejections"] += 1
            else:
                raise AssertionError("malformed input accepted")

        reject(lambda: CachedPathPricing(1, D+1))
        reject(lambda: CachedPathPricing(0, 1))
        reject(lambda: normalize_path(2, {"start_grid": 4, "moves": [-1,1]*3+[-1]*8}))
        reject(lambda: normalize_path(1, {"start_grid": 1, "moves": [-1,-1,-1,1,1,1,1]}))
        reject(lambda: normalize_path(1, {"start_grid": 0, "moves": [0,1,1,-1,-1,-1,-1]}))
        reject(lambda: normalize_path(1, {"start_grid": 0, "moves": [1,1,1,-1,-1,-1,-1,-1]}))
        reject(lambda: normalize_path(1, {"start_grid": 0, "moves": [1,-1]}))
        reject(lambda: normalize_path(2, coarse, source_n=3))
        reject(lambda: grow.price(zero.astype(float)))
        negative = zero.astype(np.int64); negative[0,2] = -1
        reject(lambda: grow.price(negative))
        excessive = zero.copy(); excessive[0,2] = 101
        reject(lambda: grow.price(excessive))
        center = zero.copy(); center[0,0] = 1
        reject(lambda: grow.price(center))
        reject(lambda: grow.price(zero[:-1]))
        reject(lambda: grow.price(zero, keep=-1))
        reject(lambda: grow.price(zero, level=1, tolerance=-1))
    return {"status": "PASS", "scope": "Cached-route separation only; exact upper witnesses for the dual minimum, never a lower certificate.",
            "stats": stats, "cases": cases,
            "source_sha256": hashlib.sha256((HERE/"cached_path_pricing.py").read_bytes()).hexdigest(),
            "native_source_sha256": hashlib.sha256(source.read_bytes()).hexdigest()}


if __name__ == "__main__":
    print(json.dumps(main(), indent=2))
