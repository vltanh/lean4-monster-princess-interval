#!/usr/bin/env python3
"""Exact algebra for continuous records and their conservative secant LP.

Uses only the standard library and the existing exact field/integration
modules. This tests specified physical routes, not response completeness.
"""
from __future__ import annotations

import argparse
from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path

from extract_quantiles import Field
from score_continuous_attack import leg_intervals, supporting_plane


def cone_area(duration, q0, q1, record, decreasing):
    """Exact maximal hypograph charge, in probability-times-time units."""
    assert duration > 0 and 0 <= record <= q0 <= 1 and 0 <= q1 <= 1
    if not decreasing:
        assert q1 >= q0
        return duration*record, Q(0), Q(0)
    assert q0 >= q1
    d = q0-q1
    u = max(Q(0), record-q1)
    if d == 0:
        assert u == 0
        return duration*record, Q(0), Q(0)
    v = u*u/d
    assert 0 <= u <= d and d*v == u*u
    return duration*(record-v/2), u, v


def secant_perspective(u, d, count):
    assert count > 0 and 0 <= u <= d
    return max(Q(2*j+1, count)*u-Q(j*(j+1), count*count)*d
               for j in range(count))


def scalar_checks(counts):
    for q0 in (Q(i, 12) for i in range(13)):
        for q1 in (Q(i, 12) for i in range(13)):
            for z in range(9):
                record, duration = q0*Q(z, 8), Q(7, 11)
                decreasing = q1 <= q0
                value, u, v = cone_area(duration, q0, q1, record, decreasing)
                # Independent integration after splitting at the cap crossing.
                cuts = [Q(0), duration]
                if q0 != q1:
                    crossing = duration*(record-q0)/(q1-q0)
                    if 0 < crossing < duration:
                        cuts.insert(1, crossing)
                direct = sum((b-a)*(min(record, q0+(q1-q0)*a/duration)
                                     +min(record, q0+(q1-q0)*b/duration))/2
                             for a, b in zip(cuts, cuts[1:]))
                assert value == direct
                counts['scalar_cases'] += 1
                if q0 == q1:
                    counts['zero_slope_cases'] += 1
                    for K in (1, 2, 4, 8, 16):
                        assert secant_perspective(0, 0, K) == 0
                if q0 > q1:
                    d = q0-q1
                    # Any larger cone slack can only lower the charge.
                    for extra in (Q(0), Q(1, 17)):
                        vv = v+extra
                        assert d*vv >= u*u
                        assert duration*(record-vv/2) <= direct
                    for K in (1, 2, 4, 8, 16):
                        upper = secant_perspective(u, d, K)
                        assert 0 <= upper-v <= d/(4*K*K)
                        inner = duration*(record-upper/2)
                        assert 0 <= direct-inner <= duration*d/(8*K*K)
                        counts['exact_secant_cases'] += 1


def legal_test_fields(n):
    # Uniform initial radial laws wait until T=0,1,2 and then move outward.
    # The last two cases include genuine initial endpoint atoms, including
    # the completely flat interior field of the stationary endpoint pair.
    for weights, endpoint_weight in (((1, 0, 0), 0), ((0, 1, 0), 0),
                                     ((0, 0, 1), 0), ((2, 3, 1), 2),
                                     ((0, 0, 0), 1)):
        denominator = 2*n*(sum(weights)+endpoint_weight)
        data = {'n': n, 'field_denominator': denominator,
                'radial_nodes': [
                    [j, k, sum(w*max(0, k-max(0, j-2*n*T))
                               for T, w in enumerate(weights))]
                    for j in range(4*n+1)
                    for k in range(1, 2*n+1) if (j+k)%2 == 0]}
        yield Field(data, Q(1, 2)), bool(endpoint_weight)


def physical_routes():
    routes = []
    for start in (Q(0), Q(1, 2), Q(1)):
        routes.append([(Q(0), start), (1+start, Q(-1)), (3+start, Q(1))])
        if start < 1:
            routes.append([(Q(0), start), (1-start, Q(1)), (3-start, Q(-1))])
        for height in (Q(1, 4), Q(3, 4)):
            routes.append([(Q(0), start), (start+height, -height),
                           (start+2*height+1, Q(1)),
                           (start+2*height+3, Q(-1))])
    # Both endpoint-start deactivations, including an endpoint atom.
    routes.extend([[(t, -x) for t, x in route]
                   for route in routes if route[0][1] == 1])
    # A genuine four-leg inward/outward/endpoint/endpoint route.
    routes.append([(Q(0), Q(3, 4)), (Q(1, 4), Q(1, 2)),
                   (Q(5, 8), Q(7, 8)), (Q(5, 2), Q(-1)),
                   (Q(9, 2), Q(1))])
    return routes


def path_checks(counts):
    routes = physical_routes()
    K = 8
    for n in (1, 2, 3):
        for field, endpoint_atoms in legal_test_fields(n):
            counts['fields'] += 1
            counts['fields_with_initial_endpoint_atoms'] += endpoint_atoms
            for route in routes:
                records = [Q(1), Q(1)]
                smaller_records = [Q(1), Q(1)]
                stopped = [route[0][1] == -1, route[0][1] == 1]
                counts['initial_endpoint_deactivations'] += sum(stopped)
                total = smaller_total = inner_total = error_budget = Q(0)
                for first, last in zip(route, route[1:]):
                    direction = 1 if last[1] > first[1] else -1
                    for a, b in leg_intervals(field, *first, *last):
                        duration = b[0]-a[0]
                        assert 0 < duration <= Q(1, 2*n)
                        f0, f1 = field.cdf(*a), field.cdf(*b)
                        assert field.cdf((a[0]+b[0])/2, (a[1]+b[1])/2) == (f0+f1)/2
                        counts['affine_segments'] += 1
                        for side in (0, 1):
                            if stopped[side]:
                                continue
                            q0, q1 = (f0, f1) if side == 0 else (1-f0, 1-f1)
                            # Monotonicity is fixed by physical direction,
                            # not selected after inspecting the field values.
                            decreasing = (direction < 0) if side == 0 else (direction > 0)
                            records[side] = min(records[side], q0)
                            value, u, _ = cone_area(duration, q0, q1, records[side], decreasing)
                            total += value
                            if decreasing:
                                d = q0-q1
                                upper = secant_perspective(u, d, K)
                                inner_total += duration*(records[side]-upper/2)
                                error_budget += duration*d/(8*K*K)
                            else:
                                inner_total += value
                            # A feasible but deliberately smaller causal
                            # record history cannot overstate the route cost.
                            smaller_records[side] = Q(3, 4)*min(smaller_records[side], q0)
                            smaller, _, _ = cone_area(duration, q0, q1, smaller_records[side], decreasing)
                            smaller_total += smaller
                            assert smaller <= value
                            records[side] = min(records[side], q1)
                            smaller_records[side] = min(smaller_records[side], q1)
                            assert smaller_records[side] <= records[side]
                            counts['active_clock_segments'] += 1
                            counts['smaller_causal_record_checks'] += 1
                    # q1 above is the endpoint INTERIOR LIMIT. Actual capture
                    # deactivates the corresponding clock only after the leg.
                    if last[1] == -1 and not stopped[0]:
                        stopped[0] = True
                        counts['endpoint_resets'] += 1
                    if last[1] == 1 and not stopped[1]:
                        stopped[1] = True
                        counts['endpoint_resets'] += 1
                assert all(stopped) and smaller_total <= total
                assert 0 <= total-inner_total <= error_budget
                assert error_budget <= Q(len(route)-1, 16*n*K*K)
                replay = supporting_plane(field, route)
                assert total == Q(replay['value'])
                counts['physical_routes'] += 1
                counts['independent_continuous_integrations'] += 2


def verify():
    counts = {name: 0 for name in (
        'scalar_cases', 'zero_slope_cases', 'exact_secant_cases', 'fields',
        'fields_with_initial_endpoint_atoms', 'physical_routes', 'affine_segments',
        'active_clock_segments', 'smaller_causal_record_checks',
        'initial_endpoint_deactivations', 'endpoint_resets',
        'independent_continuous_integrations')}
    scalar_checks(counts)
    path_checks(counts)
    return {
        'status': 'PASS',
        'scope': 'Exact known-unit-speed-route hypograph algebra and conservative secant LP; no optimization run, all-Monster certificate, or new game bound.',
        'probability_normalized_clocks': True,
        'field_dependent_crossing_times_used': False,
        'counts': counts,
        'secant_counts_tested': [1, 2, 4, 8, 16],
        'four_leg_profile64_K16_error_bound': str(Q(4, 16*64*16**2)),
        'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
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
