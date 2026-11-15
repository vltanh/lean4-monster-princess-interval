#!/usr/bin/env python3
"""Reproduce the negative earlier-front probe without response search.

Gamma_(237/128) changes the retained field, but all nine saved route costs
and one near-minimizing native path cost are unchanged. The aligned-front
theorem gives only an inherited lower; the physical path gives an upper on
this field's n256 bank minimum. No new exact minimum is asserted.

For the saved dyadic route, the chronological survival is nonincreasing.
Its left Riemann sum C_N therefore satisfies 0 <= C_N - T <= 1/(2N),
since initial survival is at most one. Every compatible exact full-width
refinement has bank minimum <= C_N, so its standard transferred lower is
<= T. This ceiling concerns this fixed geometry and transfer, not the game
value or the security of a separately extracted narrow Princess law.

The default command checks the fixture. --write-field PATH optionally
generates the compact field; no full refined table or pricing oracle is run.
"""
from __future__ import annotations

import argparse
import base64
from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path
import sys
import time
import zlib

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT/'packages/interval_clock_grid/normalized_native'),
                str(ROOT/'packages/interval_quantile_certificate')]
from verify_native_field import load_table
from cached_path_pricing import CachedPathPricing, normalize_path
from score_continuous_attack import Field, supporting_plane
from test_refinement_ceiling import grid_samples, left_records, integer_clock_price

HERE = Path(__file__).resolve().parent
sha = lambda raw: hashlib.sha256(raw).hexdigest()


def project(table, n, front):
    front = Q(front)
    assert 1 <= front <= 2 and (n*front).denominator == 1
    J = int(2*n*front)
    result = table.copy()
    for j in range(12*n+1):
        for k in range(j % 2, 2*n+1, 2):
            if j-k >= J:
                result[j, k] = 0
            elif j+k > J:
                result[j, k] = table[(J+j-k)//2, (J-j+k)//2]
    return result


def verify(write_field=None):
    began = time.monotonic()
    fixture = json.loads((HERE/'earlier_front_probe.json').read_bytes())
    n, front = fixture['n'], Q(fixture['front'])
    source, source_raw, source_hash = load_table(ROOT/fixture['source']['file'])
    old_front, front_raw, front_hash = load_table(ROOT/fixture['front_two_source']['file'])
    assert source_hash == fixture['source']['sha256']
    assert front_hash == fixture['front_two_source']['sha256']
    replay_raw = (ROOT/fixture['source']['replay_file']).read_bytes()
    assert sha(replay_raw) == fixture['source']['replay_sha256']
    replay = json.loads(replay_raw)
    assert replay['input_sha256'] == source_hash and replay['pricing']['status'] == 'PASS'
    assert replay['pricing']['minimum_units'] == source['minimum_units']
    assert n == source['n'] == old_front['n'] == 256
    D = int(source['field_denominator'])
    assert D == int(old_front['field_denominator']) == 800000000
    shape = (12*n+1, 2*n+1)
    old = np.frombuffer(source_raw, dtype=np.uint64).reshape(shape)
    old2 = np.frombuffer(front_raw, dtype=np.uint64).reshape(shape)
    new = project(old, n, front)
    assert int(2*n*front) == fixture['physical_front_tick'] == 948
    assert np.array_equal(project(old, n, 2), old2)
    assert np.array_equal(new, project(old2, n, front))
    assert np.array_equal(new, project(new, n, front))
    assert np.array_equal(new, project(new, n, 2))
    assert np.all(new <= old2)
    assert int(np.count_nonzero(new != old)) == fixture['projection']['changed_valid_nodes_from_source']
    assert int(np.count_nonzero(new != old2)) == fixture['projection']['changed_valid_nodes_from_front_two']
    assert np.all(new[:, 0] == 0) and np.max(new) <= D
    cone_checks = 0
    for j in range(12*n+1):
        for k in range(j % 2, 2*n+1, 2):
            if k < 2*n:
                for step in (-1, 1):
                    if 0 <= j+step <= 12*n:
                        assert new[j, k] <= new[j+step, k+1]
                        cone_checks += 1
            if j > 4*n:
                assert new[j, k] == (new[4*n, k-(j-4*n)] if k > j-4*n else 0)
    for j in range(0, 4*n, 2):
        assert new[j+2, 2*n] <= new[j, 2*n]
    bound = Q(int(source['minimum_units']), 4*n*D)
    assert bound == Q(fixture['projection']['inherited_bank_lower']) <= (front+1)/2
    assert (front+1)/2 == Q(fixture['projection']['late_center_floor'])
    pre = np.array([new[j, k] for j in range(4*n+1)
                    for k in range(1, 2*n+1) if (j+k) % 2 == 0], dtype='<u4').tobytes()
    assert sha(pre) == fixture['projection']['pre_two_sha256']
    field = {
        'format': 'qout-clock-grid-field-u32-zlib-v1', 'n': n,
        'field_denominator': str(D), 'normalized_profile': True,
        'encoding': {'count': (4*n+1)*n, 'integer_type': 'uint32 little-endian',
                     'compression': 'zlib', 'uncompressed_sha256': sha(pre)},
        'pre_two_values_base64': base64.b64encode(zlib.compress(pre, 9)).decode(),
        'incoming_front': str(front), 'certified_bank_lower_units': source['minimum_units'],
        'normalized_bank_lower': str(bound), 'minimum_is_exact': False,
        'source_input_sha256': source_hash, 'source_front2_sha256': front_hash,
        'projection_theorem': 'research/12-global-closure/DISCRETE_CENTER_BALANCE_PRICING.md section 7',
        'scope': 'Exact earlier-front projection with inherited source-bound complete bank lower, not a newly computed minimum. Full-width continuous attack scores are upper screens only.'}
    field_bytes = (json.dumps(field, separators=(',', ':'))+'\n').encode()
    # Zlib output can differ by runtime. The exact decoded nodal hash above
    # is the portable identity; this records the originally observed bytes.
    if write_field is not None:
        write_field = Path(write_field)
        write_field.parent.mkdir(parents=True, exist_ok=True)
        write_field.write_bytes(field_bytes)

    witness = fixture['cached_path']
    moves = []
    for step, count in witness['moves_rle']:
        assert step in (-1, 1) and isinstance(count, int) and count > 0
        moves += [step]*count
    path = {'start_grid': witness['start_grid'], 'moves': moves}
    assert normalize_path(n, path) == path
    cache = CachedPathPricing(n, D)
    cache.add(path)
    for table in (old, old2, new):
        result = cache.price(table, keep=1)
        assert result['cached_minimum_units'] == witness['units']
        assert result['objective_denominator'] == witness['objective_denominator']
    upper = Q(int(witness['units']), 4*n*D)
    assert upper == Q(witness['cost'])
    assert upper-bound == Q(fixture['maximum_n256_bank_improvement'])

    fields = (Field(old_front, Q(1, 2)), Field(field, Q(1, 2)))
    routes = []
    for row in fixture['routes']:
        costs = []
        for f, key in zip(fields, ('front_two_cost', 'earlier_front_cost')):
            answer = supporting_plane(f, row['route'])
            assert Q(answer['value']) == Q(row[key])
            assert answer['affine_intervals_checked'] == row['affine_intervals_checked']
            costs.append(answer['value'])
        assert costs[0] == costs[1]
        routes.append({'name': row['name'], 'front_two_cost': costs[0],
                       'earlier_front_cost': costs[1]})
    ceiling = fixture['standard_exact_refinement_ceiling']
    route = [tuple(map(Q, p)) for p in fixture['routes'][ceiling['route_index']]['route']]
    cost = Q(ceiling['value'])
    assert cost == Q(routes[ceiling['route_index']]['earlier_front_cost'])
    refinements = []
    for N in ceiling['sampled_grids']:
        samples = grid_samples(fields[1], route, N)
        price, records = left_records(samples, N)
        units, integer_price = integer_clock_price(samples, N, D*(N//n))
        assert price == integer_price
        h = Q(1, 2*N)
        assert 0 <= price-cost <= h*sum(records[0]) <= h
        assert price-h <= cost
        refinements.append({'n': N, 'one_path_left_sum': str(price),
                            'standard_bank_certificate_ceiling': str(price-h),
                            'continuous_attack_cost': str(cost)})
    return {
        'status': 'PASS', 'scope': fixture['scope'],
        'complete_response_oracle_run': False, 'new_exact_bank_minimum_asserted': False,
        'full_refined_tables_built': 0, 'source_sha256': source_hash,
        'source_front_two_sha256': front_hash, 'front': str(front),
        'generated_field_sha256': sha(field_bytes),
        'original_probe_field_sha256': fixture['projection']['field_sha256'],
        'exact_projected_nodes_sha256': sha(pre),
        'changed_nodes_from_front_two': fixture['projection']['changed_valid_nodes_from_front_two'],
        'checked_transport_inequalities': cone_checks,
        'inherited_bank_lower': str(bound), 'one_path_bank_upper': str(upper),
        'maximum_n256_bank_improvement': str(upper-bound),
        'unchanged_routes': routes, 'standard_exact_refinement_ceiling': str(cost),
        'refinement_checks': refinements, 'elapsed_seconds': time.monotonic()-began}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write-field', type=Path)
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    report = json.dumps(verify(args.write_field), indent=2)+'\n'
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(report)
    print(report, end='')
