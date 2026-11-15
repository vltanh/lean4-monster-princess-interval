#!/usr/bin/env python3
"""Independent integer replay of an all-Princess canonical one-turn upper.

No LP, numerical tolerance, source graph generator or JavaScript verifier is
used. The input is the sparse Qout certificate format. The mathematical
normalizations and causal-clock upper theorem are referenced in the accompanying
manuscript; this program checks every finite hypothesis of that theorem.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from fractions import Fraction as Q
import gzip
import hashlib
import json
from pathlib import Path

BENCHMARK = Q(291849329389899, 204800000000000)


def integer(x):
    assert isinstance(x, int) and not isinstance(x, bool), "integer required"
    return x


def verify(c, *, require_counterexample=False):
    n = integer(c['n'])
    W = int(c['weight_denominator'])
    assert n > 0 and W > 0
    R, C = 2 * n, 4 * n
    assert c['pair_law'] == 'fair_reflection'
    assert c['center_deadline'] == 2 and c['completion_horizon'] == 8
    assert c['physical_step'] == f'1/{R}'
    probability = mass = prefix_checks = 0
    pressure = defaultdict(int)
    counts, class_mass = Counter(), Counter()
    geometries = set()
    latest_end = 0
    for plan in c['paths']:
        w = int(plan['weight_numerator'])
        assert w > 0
        probability += w
        start = integer(plan['start_grid'])
        assert start % 2 == 0 and abs(start) <= R
        moves = tuple(integer(x) for x in plan['moves'])
        assert moves and len(moves) <= 16 * n
        positions = [start]
        for move in moves:
            assert move in (-1, 1)
            positions.append(positions[-1] + move)
            assert abs(positions[-1]) <= R
        assert -R in positions and R in positions and 0 in positions
        left, right = positions.index(-R), positions.index(R)
        assert positions.index(0) <= C
        first, last = min(left, right), max(left, right)
        assert last == len(moves), "stop the certificate path at both endpoints"
        turns = sum(moves[j] != moves[j-1] for j in range(1, first))
        assert turns <= 1, "outside the canonical one-turn class"
        direction = -1 if positions[first] == R else 1
        assert last - first == 2 * R, "post-endpoint tour must be direct"
        assert all(move == direction for move in moves[first:last])
        kind = ('endpoint_start' if first == 0 else
                'one_interior_reversal' if turns else 'endpoint_first')
        counts[kind] += 1
        class_mass[kind] += w
        geometries.add(min((start, moves), (-start, tuple(-d for d in moves))))
        latest_end = max(latest_end, last)
        for name, end, sign in (('minus_charges', left, 1),
                                ('plus_charges', right, -1)):
            charges = [0] * end
            for row in plan[name]:
                assert len(row) == 2
                j, amount = map(integer, row)
                assert 0 <= j < end and amount > 0
                charges[j] += amount
            total = 0
            for j, amount in enumerate(charges):
                total += amount
                assert total >= j + 1, "noncausal selected clock"
                prefix_checks += 1
                if not amount:
                    continue
                selected = w * amount
                mass += selected
                x = sign * positions[j]
                if x == 0:
                    continue
                k = abs(x) - max(0, j - C)
                if k > 0:
                    pressure[min(j, C), k] += selected * (1 if x > 0 else -1)
            assert total == end, "active selected mass must equal lifetime"
    assert probability == W
    nodes = []
    index = {}
    for i, row in enumerate(c['qout_nodes']):
        assert len(row) == 2
        j, k = map(integer, row)
        assert 0 <= j <= C and 1 <= k <= R and (j+k) % 2 == 0
        assert (j, k) not in index
        nodes.append((j, k))
        index[j, k] = i
    coefficients = [0] * len(nodes)
    for point, value in pressure.items():
        if value:
            assert point in index, "charged event missing from certificate"
            coefficients[index[point]] += value
    positive = sum(max(0, v) for v in coefficients)
    source, sink = len(nodes), len(nodes) + 1
    infinity = positive + 1
    arcs = []
    for i, value in enumerate(coefficients):
        if value > 0:
            arcs.append((source, i, value))
        elif value < 0:
            arcs.append((i, sink, -value))
    seen = set()
    for row in c['qout_order']:
        assert len(row) == 2
        a, b = map(integer, row)
        assert 0 <= a < len(nodes) and 0 <= b < len(nodes) and a != b
        assert (a, b) not in seen
        seen.add((a, b))
        j, k = nodes[a]
        t, r = nodes[b]
        cone = r - k >= abs(t - j)
        stopped_endpoint = r == R and t <= min(C, j + R - k)
        assert cone or stopped_endpoint, "unproved Qout inequality"
        arcs.append((a, b, infinity))
    balance = [0] * (sink + 1)
    used = set()
    for row in c['closure_flow']:
        assert len(row) == 2
        i = integer(row[0])
        amount = int(row[1])
        assert 0 <= i < len(arcs) and i not in used
        used.add(i)
        a, b, capacity = arcs[i]
        assert 0 < amount <= capacity
        balance[a] -= amount
        balance[b] += amount
    flow = -balance[source]
    assert flow >= 0 and balance[sink] == flow
    assert all(v == 0 for v in balance[:source]), "flow conservation"
    side = set(map(integer, c['closure_source_side']))
    assert len(side) == len(c['closure_source_side'])
    assert source in side and sink not in side
    assert all(0 <= i <= sink for i in side)
    cut = sum(cap for a, b, cap in arcs if a in side and b not in side)
    assert flow == cut, "integer flow/cut gap"
    upper = Q(mass + positive - flow, 4 * n * W)
    assert upper == Q(c['global_upper']), "reported upper differs from replay"
    if require_counterexample:
        assert upper <= BENCHMARK, "one-turn necessity target not disproved"
    return {
        'status': 'PASS',
        'scope': 'all-Princess upper for a physical law in canonical B1',
        'arithmetic': 'Python integers and fractions.Fraction only',
        'n': n,
        'physical_calendar_plans': len(c['paths']),
        'distinct_reflected_path_pairs': len(geometries),
        'class_counts': dict(sorted(counts.items())),
        'class_probability': {k: str(Q(v, W)) for k, v in sorted(class_mass.items())},
        'maximum_completion_time': str(Q(latest_end, R)),
        'causal_prefix_checks': prefix_checks,
        'closure_nodes': sink + 1,
        'closure_arcs': len(arcs),
        'exact_flow': str(flow),
        'exact_cut': str(cut),
        'global_upper': str(upper),
        'global_upper_decimal': float(upper),
        'endpoint_baseline': str(Q(mass, 4 * n * W)),
        'closure_excess': str(Q(positive - flow, 4 * n * W)),
        'benchmark': str(BENCHMARK),
        'benchmark_minus_upper': str(BENCHMARK - upper),
        'one_turn_separation_target_disproved': upper <= BENCHMARK,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('certificate', type=Path)
    parser.add_argument('--require-counterexample', action='store_true')
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    raw = args.certificate.read_bytes()
    data = gzip.decompress(raw) if raw[:2] == b'\x1f\x8b' else raw
    report = verify(json.loads(data), require_counterexample=args.require_counterexample)
    report['input_sha256'] = hashlib.sha256(raw).hexdigest()
    report['uncompressed_sha256'] = hashlib.sha256(data).hexdigest()
    text = json.dumps(report, indent=2, sort_keys=True) + '\n'
    if args.output:
        args.output.write_text(text)
    print(text, end='')


if __name__ == '__main__':
    main()
