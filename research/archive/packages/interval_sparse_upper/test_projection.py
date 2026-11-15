#!/usr/bin/env python3
"""Independent checks of the projected Qout order and integer extension."""
from collections import deque
from pathlib import Path
import json
import random
import sys

import numpy as np

from master import SparseMaster, projected_order, read_json, solve_existing_master

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT/'packages/interval_clock_grid/normalized_native'))
from solve_normalized import Master


def main():
    rng = random.Random(20261114)
    pairs, fields, lps = 0, 0, []
    for n in range(1, 9):
        all_nodes = [(j, k) for j in range(4*n+1) for k in range(1, 2*n+1) if (j+k) % 2 == 0]
        for repetition in range(12):
            nodes = [p for p in all_nodes if rng.random() < .08+.075*repetition]
            edges = projected_order(n, nodes)
            adj = [[] for _ in nodes]
            for a, b in edges:
                adj[a].append(b)
            for a, (j, k) in enumerate(nodes):
                reached = {a}; queue = deque([a])
                while queue:
                    for b in adj[queue.popleft()]:
                        if b not in reached:
                            reached.add(b); queue.append(b)
                for b, (s, r) in enumerate(nodes):
                    expected = r-k >= abs(s-j) or (r == 2*n and s <= min(4*n, j+2*n-k))
                    assert (b in reached) == expected, (n, nodes[a], nodes[b], expected)
                    pairs += 1
            # Random feasible sparse fields are generated from arbitrary full
            # values by the independently implemented dense Qout repair.
            dense = Master(n, Path('/tmp/sparse_projection_test'), 1009)
            full = dense.repair(rng.random() for _ in dense.nodes)
            sparse = SparseMaster(n, 1009); sparse.nodes = nodes
            values = [int(full[j, k])/1009 for j, k in nodes]
            extended = sparse.extend_integer(values)
            for i, (j, k) in enumerate(dense.nodes):
                for step in (-1, 1):
                    if k < 2*n and 0 <= j+step <= 4*n:
                        assert extended[j, k] <= extended[j+step, k+1]
            for j in range(0, 4*n, 2):
                assert extended[j+2, 2*n] <= extended[j, 2*n]
            for j in range(4*n+1, 12*n+1):
                for k in range(1, 2*n+1):
                    if (j+k) % 2 == 0:
                        foot = k-j+4*n
                        assert extended[j, k] == (extended[4*n, foot] if foot > 0 else 0)
            fields += 1
    for n in (1, 2, 3, 4, 6):
        certificate = read_json(ROOT/f'packages/interval_clock_grid/grid_n{n}_certificate.json')
        sparse = SparseMaster(n)
        dense = Master(n, Path('/tmp/sparse_projection_lp'))
        for plan in certificate['paths']:
            sparse.add_plan(plan); dense.add_plan(plan)
        result, _ = sparse.solve(60)
        ordinary, _, _ = dense.solve_lp()
        assert abs(result.fun-ordinary.fun) < 1e-8
        lps.append({'n': n, 'sparse_variables': len(sparse.nodes), 'full_variables': dense.K,
                    'restricted_master_upper': -result.fun})
    warm = Master(4, Path('/tmp/sparse_projection_warm'))
    seed = read_json(ROOT/'packages/interval_clock_grid/grid_n4_certificate.json')
    for stop in (2, 5, len(seed['paths'])):
        for plan in seed['paths'][:stop]:
            warm.add_plan(plan)
        persistent, weights, profile = solve_existing_master(warm, seconds=60)
        independent, _, _ = solve_existing_master(warm, seconds=60, method='highs-ds')
        assert abs(persistent.fun-independent.fun) < 1e-8
        assert len(weights) == len(warm.columns) and abs(weights.sum()-1) < 1e-8
        assert len(profile) == warm.K
    print(json.dumps({'status': 'PASS', 'ordered_event_pairs': pairs,
                      'integer_extension_fields': fields, 'dense_sparse_lp_comparisons': lps,
                      'persistent_node_and_calendar_updates': 3,
                      'scope': 'Projection regressions; no new game bound'}, indent=2))


if __name__ == '__main__':
    main()
