#!/usr/bin/env python3
"""Exact fixed-route ceilings on standard refined-bank lower certificates.

Only the two saved attack routes are sampled. No refined field table or
complete response search is constructed, and no new game bound is asserted.
"""
from __future__ import annotations

import argparse
from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path

from extract_quantiles import Field, ROOT, read
from score_continuous_attack import supporting_plane


HERE = Path(__file__).resolve().parent
CASES = (
    {
        'name': 'retained_fullwidth',
        'source': 'packages/interval_clock_grid/lower_n256_field.json',
        'sha256': '81483589b60c14d823d2bb467015a321d77cf555076fe8d69a36d63cd829d7d5',
        'fixture': 'current_fullwidth_attack.json',
        'replay': 'current_fullwidth_attack_replay.json',
        'cost': '36421298289/25600000000',
        'route': [('0', '31/32'), ('63/32', '-1'), ('127/32', '1')],
    },
    {
        'name': 'retained_front2_fullwidth',
        'source': 'packages/interval_global_closure/lower_n256_front2_field.json',
        'sha256': 'a8e1d84d67e66e08d6d1eeb02f18c6e5121108cb4368ededd9db2e792a97189e',
        'fixture': 'projected_fullwidth_attack.json',
        'replay': 'projected_fullwidth_attack_replay.json',
        'cost': '14570592687/10240000000',
        'route': [('0', '7/8'), ('123/128', '-11/128'),
                  ('131/64', '1'), ('259/64', '-1')],
    },
)


def grid_samples(field, route, n):
    """Evaluate the original exact CDF only along a grid-compatible route."""
    assert n > 0 and n % field.n == 0
    assert route[0][0] == 0
    for t, x in route:
        assert abs(x) <= 1
        # The normalized physical bank uses parity j+k even, not every
        # point of the Cartesian half-step grid.
        assert (n*(t+x)).denominator == (n*(t-x)).denominator == 1
    samples = []
    for (ta, xa), (tb, xb) in zip(route, route[1:]):
        assert tb > ta and abs(xb-xa) == tb-ta
        count = (tb-ta)*2*n
        assert count.denominator == 1
        direction = 1 if xb > xa else -1
        for i in range(int(count)):
            t, x = ta+Q(i, 2*n), xa+direction*Q(i, 2*n)
            samples.append((t, x, field.cdf(t, x)))
    t, x = route[-1]
    samples.append((t, x, field.cdf(t, x)))
    assert samples[-1][0]*2*n == len(samples)-1
    # Transport makes each signed CDF trace monotone on a unit-speed edge.
    # It is therefore enough to retain the node extrema in each clock.
    for (ta, xa, fa), (tb, xb, fb) in zip(samples, samples[1:]):
        assert tb-ta == abs(xb-xa) == Q(1, 2*n)
        fm = field.cdf((ta+tb)/2, (xa+xb)/2)
        if xb > xa:
            assert fa <= fm <= fb
        else:
            assert fa >= fm >= fb
    return samples


def left_records(samples, n, denominator=None):
    """Chronological survival after the sample, with actual endpoint resets.

    If denominator is supplied, floor the radial g value at each queried
    node. This is exactly the route restriction of pure nodal flooring;
    no full refined table is needed.
    """
    records = [Q(1), Q(1)]
    history = []
    for _, x, f in samples:
        if denominator is not None:
            radial = abs(2*f-1)
            scaled = radial*denominator
            g = Q(scaled.numerator//scaled.denominator, denominator)
            f = (1+(1 if x > 0 else -1 if x < 0 else 0)*g)/2
        records[0] = Q(0) if x == -1 else min(records[0], f)
        records[1] = Q(0) if x == 1 else min(records[1], 1-f)
        history.append(tuple(records))
    assert history[-1] == (0, 0)
    assert all(a[0] >= b[0] and a[1] >= b[1]
               for a, b in zip(history, history[1:]))
    return sum((sum(r) for r in history[:-1]), Q(0))/(2*n), history


def integer_clock_price(samples, n, denominator):
    """Independent integer normalization: doubled CDF prices D +/- g."""
    left = right = 2*denominator
    units = 0
    for index, (_, x, f) in enumerate(samples):
        radial = abs(2*f-1)*denominator
        assert radial.denominator == 1
        signed = (1 if x > 0 else -1 if x < 0 else 0)*int(radial)
        left = 0 if x == -1 else min(left, denominator+signed)
        right = 0 if x == 1 else min(right, denominator-signed)
        if index+1 < len(samples):
            units += left+right
    assert left == right == 0
    return units, Q(units, 4*n*denominator)


def verify():
    rows = []
    sources = []
    counts = {'source_fields': 0, 'exact_continuous_replays': 0,
              'refinement_cases': 0, 'sampled_route_nodes': 0,
              'edge_monotonicity_checks': 0, 'floored_cases': 0,
              'floor_record_error_checks': 0}
    for case in CASES:
        data, raw = read(ROOT/case['source'])
        source_hash = hashlib.sha256(raw).hexdigest()
        assert source_hash == case['sha256']
        fixture_raw = (HERE/case['fixture']).read_bytes()
        fixture = json.loads(fixture_raw)
        assert fixture['source_sha256'] == source_hash
        assert fixture['interpolation_epsilon'] == '1/2'
        if 'source_field' in fixture:
            assert fixture['source_field'] == case['source']
        route = [tuple(map(Q, p)) for p in fixture['route']]
        assert route == [tuple(map(Q, p)) for p in case['route']]
        expected = Q(case['cost'])
        old_replay = json.loads((HERE/case['replay']).read_bytes())
        assert old_replay['status'] == 'PASS'
        assert old_replay['source_sha256'] == source_hash
        assert Q(old_replay['value']) == expected
        assert old_replay['interpolation_epsilon'] == '1/2'
        assert [tuple(map(Q, p)) for p in old_replay['route']] == route

        field = Field(data, Q(1, 2))
        assert field.n == 256
        # This invokes both the exact supporting-plane integrator and its
        # independent chronological affine-record replay. It does not rely
        # solely on the saved numerical value or replay metadata.
        continuous = supporting_plane(field, route)
        assert Q(continuous['value']) == expected
        counts['source_fields'] += 1
        counts['exact_continuous_replays'] += 2
        sources.append({
            'name': case['name'], 'source_file': case['source'],
            'source_sha256': source_hash, 'fixture_file': case['fixture'],
            'fixture_sha256': hashlib.sha256(fixture_raw).hexdigest(),
            'exact_attack_cost': str(expected),
            'attack_horizon': str(route[-1][0]),
            'affine_intervals_checked': continuous['affine_intervals_checked'],
            'independent_affine_intervals_checked': continuous['independent_affine_intervals_checked'],
        })
        for n in (256, 512, 1024):
            samples = grid_samples(field, route, n)
            price, history = left_records(samples, n)
            exact_denominator = field.den*(n//field.n)
            units, integer_price = integer_clock_price(samples, n, exact_denominator)
            assert price == integer_price
            h = Q(1, 2*n)
            initial_survival = sum(history[0])
            assert 0 <= price-expected <= h*initial_survival <= h
            # Since the complete-bank minimum is at most this one-path
            # price, its usual c_n-h certificate cannot exceed expected.
            assert price-h <= expected
            floored = []
            for denominator in (17, 10**9):
                floor_price, floor_history = left_records(samples, n, denominator)
                for exact, rounded in zip(history, floor_history):
                    assert all(abs(a-b) < Q(1, 2*denominator)
                               for a, b in zip(exact, rounded))
                    counts['floor_record_error_checks'] += 2
                allowance = route[-1][0]/denominator
                assert abs(floor_price-price) <= allowance
                assert floor_price-h <= expected+allowance
                floored.append({'denominator': denominator,
                                'left_sum': str(floor_price),
                                'certificate_ceiling_allowance': str(allowance)})
                counts['floored_cases'] += 1
            rows.append({
                'name': case['name'], 'n': n, 'h': str(h),
                'initial_survival': str(initial_survival),
                'left_sum': str(price), 'exact_attack_cost': str(expected),
                'riemann_excess': str(price-expected),
                'riemann_excess_bound': str(h*initial_survival),
                'exact_probability_denominator': str(exact_denominator),
                'normalized_clock_units': str(units),
                'normalization_denominator': str(4*n*exact_denominator),
                'floored_checks': floored,
            })
            counts['refinement_cases'] += 1
            counts['sampled_route_nodes'] += len(samples)
            counts['edge_monotonicity_checks'] += len(samples)-1
    return {
        'status': 'PASS',
        'scope': 'Fixed-field ceilings on the standard c_n-1/(2n) certificate only; not a new game bound and not a security upper for a separately extracted narrow law.',
        'full_refined_tables_built': 0,
        'complete_response_oracle_run': False,
        'interpolation_epsilon': '1/2',
        'test_source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'counts': counts, 'sources': sources, 'refinements': rows,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    report = verify()
    text = json.dumps(report, indent=2)+'\n'
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(text)
    print(text, end='')


if __name__ == '__main__':
    main()
