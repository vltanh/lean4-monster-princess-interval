#!/usr/bin/env python3
"""Independent Fraction checks of physical-cost <= every vertex-clock plane.

This does not import the native lattice edge formula, dominance pruning, or
the normalized pricing oracle.  It enumerates small physical banks, integrates
continuous affine record envelopes directly, and compares them with every
integer causal clock on short histories and representative valid clocks on
longer ones.  The universal bridge is proved in PHYSICAL_LATTICE_PRINCESS_EXTRACTION.md.
"""
from __future__ import annotations

import argparse
from fractions import Fraction as Q
from functools import lru_cache
import json
from pathlib import Path
import random


def profiles(n):
    """Small exact Qout fixtures, independent of the optimization code."""
    R, C = 2 * n, 4 * n
    for seed in range(5):
        rng = random.Random(7129 + 100 * n + seed)
        D = 12
        g = {(j, 0): 0 for j in range(0, C + 1, 2)}
        for k in range(1, R + 1):
            for j in range(k % 2, C + 1, 2):
                value = rng.randrange(D + 1) if seed else 0
                for s in (-1, 1):
                    value = max(value, g.get((j + s, k - 1), 0))
                g[j, k] = value
        for j in range(C - 2, -1, -2):
            g[j, R] = max(g[j, R], g[j + 2, R])

        def node(j, k):
            if j > C:
                k -= j - C
                j = C
            return 0 if k <= 0 else g[j, k]

        table = [[Q(D + (1 if k >= 0 else -1) * node(j, abs(k)), 2 * D)
                  if (j + k) % 2 == 0 else None
                  for k in range(-R, R + 1)] for j in range(12 * n + 1)]
        # Verify speed-cone orders on the entire lattice, including tails.
        for j in range(12 * n):
            for k in range(-R, R + 1):
                if (j + k) % 2:
                    continue
                if k > -R:
                    assert table[j + 1][k - 1 + R] <= table[j][k + R]
                if k < R:
                    assert table[j][k + R] <= table[j + 1][k + 1 + R]
        yield table


def banks(n):
    """All normalized lattice routes, with both reflected orientations."""
    R, C = 2 * n, 4 * n

    def sweep(path, target):
        q = path[-1]
        step = 1 if target > q else -1
        return path + list(range(q + step, target + step, step))

    def visit(path, centered):
        k, j = path[-1], len(path) - 1
        if abs(k) == R:
            answer = sweep(path, -k)
            if 0 in answer[:C + 1]:
                yield answer
            return
        if j == C:
            if centered:
                for first in (-R, R):
                    yield sweep(sweep(path, first), -first)
            return
        for step in (-1, 1):
            next_k = k + step
            next_centered = centered or next_k == 0
            if not next_centered and j + 1 + abs(next_k) > C:
                continue
            yield from visit(path + [next_k], next_centered)

    for start in range(-R, R + 1, 2):
        yield from visit([start], start == 0)


def record_integral(left, right, record, duration):
    """Direct Fraction integral of min(record, affine interpolant)."""
    record = min(record, left)
    cuts = [Q(0), duration]
    if left != right:
        crossing = duration * (record - left) / (right - left)
        if 0 < crossing < duration:
            cuts.append(crossing)
    cuts.sort()
    result = Q(0)
    for a, b in zip(cuts, cuts[1:]):
        at_a = left + (right - left) * a / duration
        at_b = left + (right - left) * b / duration
        result += (b - a) * (min(record, at_a) + min(record, at_b)) / 2
    return result, min(record, right), len(cuts) == 3


def physical_clock_cost(table, path, n, endpoint):
    R, h = 2 * n, Q(1, 2 * n)
    end = path.index(endpoint)
    sign = 1 if endpoint == -R else -1
    if end == 0:
        return Q(0), [], 0
    # The trace at one's own endpoint is never a charged event.  At the other
    # endpoint the interior trace is exactly the relevant strict CDF.
    values = [table[j][sign * k + R] for j, k in enumerate(path[:end + 1])]
    record = values[0]
    cost = Q(0)
    crossings = 0
    for left, right in zip(values, values[1:]):
        piece, record, crossed = record_integral(left, right, record, h)
        cost += piece
        crossings += crossed
    return cost, values[:-1], crossings


@lru_cache(maxsize=None)
def all_integer_calendars(length):
    """All mass vectors with sum length and prefix mass >= elapsed steps."""
    answers = []

    def recurse(prefix, used):
        j = len(prefix)
        if j == length:
            if used == length:
                answers.append(tuple(prefix))
            return
        lower = max(0, j + 1 - used)
        for mass in range(lower, length - used + 1):
            recurse(prefix + [mass], used + mass)

    recurse([], 0)
    return tuple(answers)


def clocks(values):
    count = len(values)
    if count <= 6:
        return all_integer_calendars(count), True
    earliest = (count,) + (0,) * (count - 1)
    latest = (1,) * count
    greedy = []
    for latest_tie in (False, True):
        allocation = [0] * count
        best = None
        chosen = None
        for j, value in enumerate(values):
            if best is None or value < best or latest_tie and value == best:
                best, chosen = value, j
            allocation[chosen] += 1
        greedy.append(tuple(allocation))
    return tuple(set([earliest, latest] + greedy)), False


def run():
    totals = {'fields': 0, 'physical_paths': 0, 'clock_planes': 0,
              'exhaustive_short_clocks': 0, 'partial_record_crossings': 0,
              'endpoint_start_paths': 0, 'strict_domination_examples': 0}
    for n in (1, 2):
        paths = list(banks(n))
        for table in profiles(n):
            totals['fields'] += 1
            for path in paths:
                totals['physical_paths'] += 1
                totals['endpoint_start_paths'] += abs(path[0]) == 2 * n
                physical = Q(0)
                vertex_minimum = Q(0)
                for endpoint in (-2 * n, 2 * n):
                    cost, values, crossings = physical_clock_cost(table, path, n, endpoint)
                    totals['partial_record_crossings'] += crossings
                    physical += cost
                    if not values:
                        continue
                    best = values[0]
                    running = []
                    for value in values:
                        best = min(best, value)
                        running.append(best)
                    discrete = sum(running, Q(0)) / (2 * n)
                    assert cost <= discrete
                    vertex_minimum += discrete
                    allocations, exhaustive = clocks(values)
                    for allocation in allocations:
                        assert len(allocation) == len(values)
                        assert sum(allocation) == len(values)
                        assert all(sum(allocation[:j + 1]) >= j + 1 for j in range(len(values)))
                        plane = sum((a * v for a, v in zip(allocation, values)), Q(0)) / (2 * n)
                        assert plane >= discrete >= cost
                        totals['clock_planes'] += 1
                        totals['exhaustive_short_clocks'] += exhaustive
                assert physical <= vertex_minimum
                totals['strict_domination_examples'] += physical < vertex_minimum
    assert totals['partial_record_crossings'] > 0
    assert totals['endpoint_start_paths'] > 0
    assert totals['strict_domination_examples'] > 0
    B = 1536
    c = Q(9154263577, 6442450944)
    assert c - (1 + Q(1, B)) / B == Q(27450199627, 19327352832)
    assert Q(27450199627, 19327352832) > Q(726775425061, 512000000000)
    return {'status': 'PASS', 'scope': ('Independent small-bank Fraction physical/clock '
            'domination regressions and exact new-strategy arithmetic; not a replay '
            'of the B=1536 exhaustive search or a mechanical proof of continuum transfer.'),
            **totals, 'guaranteed_security': '27450199627/19327352832'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    report = run()
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))
