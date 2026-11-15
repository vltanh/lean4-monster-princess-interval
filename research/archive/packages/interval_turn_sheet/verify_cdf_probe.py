#!/usr/bin/env python3
"""Check the floating attack probe against independent exact capture engines.

This is a regression check for numerical discovery, not a rational
certificate for a candidate field.  References are exact continuous-rank
integration and direct Fraction intersections of the atomic paths.
"""
from fractions import Fraction as Q
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'interval_continuous_rank'))
from continuous_rank import RankLaw
from probe_cdf_field import Field
from probe_ordered_capture import Polygon, solve
from verify_center_memory import first_capture


NODES = [(0, 0), (1, -1), (2, 0), (3, 1), (1, 1)]
TRIANGLES = [(0, 1, 2), (0, 2, 4), (2, 3, 4)]
OUTWARD = [0, 1, 0, 0, 0]
CENTER = [(Q(0), Q(0)), (Q(1), Q(0)), (Q(2), Q(1)), (Q(8), Q(1))]
ENDPOINT = [(Q(0), Q(1)), (Q(8), Q(1))]


def exact_route(route):
    result = []
    for time, position in route:
        pair = tuple(Q(float(x)).limit_denominator(2**40) for x in (time, position))
        assert max(abs(float(x)-y) for x, y in zip(pair, (time, position))) < 1e-12
        result.append(pair)
    return result


def routes():
    for z in [Q(-1), Q(-3, 4), Q(-1, 4), Q(0), Q(1, 4), Q(3, 4), Q(1)]:
        yield [(Q(0), z), (1-z, Q(1)), (3-z, Q(-1))]
        for s in [max(abs(z), Q(7, 8)), Q(1)]:
            if s >= 2-z:
                continue
            yield [(Q(0), z), ((s-z)/2, (s+z)/2), (s+1, Q(-1)), (s+3, Q(1))]
            for t in [s, max(s, Q(15, 16)), s+Q(1, 2)]:
                yield [(Q(0), z), ((s-z)/2, (s+z)/2),
                       ((s+t)/2, (s-t)/2), (t+1, Q(1)), (t+3, Q(-1))]
    yield [(Q(0), Q(1, 4)), (Q(1, 2), Q(0)), (Q(5, 4), Q(0)),
           (Q(9, 4), Q(1)), (Q(17, 4), Q(-1))]
    yield [(Q(0), Q(0)), (Q(1), Q(1, 2)), (Q(2), Q(-1, 2)),
           (Q(5, 2), Q(-1)), (Q(9, 2), Q(1))]
    for sign in [-1, 1]:
        yield [(Q(0), Q(sign)), (Q(2), Q(sign)), (Q(4), Q(-sign))]
    # A positive interior turn very close to an endpoint must not capture
    # the endpoint atom.  In particular, open-cell interpolation must not
    # silently mix an endpoint trace with an interior trace.
    delta = Q(1, 2**34)
    yield [(Q(0), Q(0)), (1-delta, 1-delta),
           (3-2*delta, Q(-1)), (5-2*delta, Q(1))]


def main():
    uniform = RankLaw([0, 1], [0, 1], [0, 1], [0, -1], exact=True)
    counts = 0
    maximum_error = 0.
    mixtures = [
        (Q(0), None, OUTWARD),
        (Q(1), CENTER, [1]*5),
        (Q(1), ENDPOINT, [0]*5),
        (Q(1, 4), CENTER, [Q(1, 4)+Q(3, 4)*r for r in OUTWARD]),
        (Q(1, 4), ENDPOINT, [Q(3, 4)*r for r in OUTWARD]),
    ]
    for atomic_weight, atom, values in mixtures:
        field = Field(dict(nodes=NODES, triangles=TRIANGLES, values=list(map(float, values))))
        assert field.cone_violation < 1e-12
        for route in routes():
            prediction = field.payoff(route)
            completed = exact_route(prediction['route'])
            expected = (1-atomic_weight)*uniform.payoff(completed).value
            if atomic_weight:
                expected += atomic_weight*sum(first_capture(atom, completed, sign)
                                              for sign in [-1, 1])/2
            error = abs(prediction['value']-float(expected))
            assert error < 2e-9, (atomic_weight, atom, route, prediction, expected, error)
            maximum_error = max(maximum_error, error)
            counts += 1
        for q in [Q(1, 8), Q(3, 8), Q(7, 8)]:
            path = field.quantile(float(q))
            assert all(abs(y-x) <= b-a+1e-8
                       for a, b, x, y in zip(path.t, path.t[1:], path.x, path.x[1:]))
    # A whole continuum has a different response from any finite quantile
    # sample.  Check the analytic endpoint-sweep cost directly.
    field = Field(dict(nodes=NODES, triangles=TRIANGLES, values=OUTWARD))
    assert abs(field.payoff([(0, 1), (2, -1)])['value']-Q(9, 8)) < 1e-12
    # Independent simple finite laws check search and explicit route recovery.
    pairs = [([Polygon([0, 4], [-1, -1]), Polygon([0, 4], [1, 1])], 1.),
             ([Polygon([0, 4], [-1, -1]), Polygon([0, 4], [0, 0]),
               Polygon([0, 4], [1, 1])], 1.)]
    for paths, expected in pairs:
        result = solve(paths, node_limit=10000, seconds=5.)
        assert result['stats']['complete']
        assert abs(result['value']-expected) < 1e-12
    print(f'PASS: {counts} entire-field comparisons with independent exact capture costs')
    print(f'Maximum floating comparison error: {maximum_error:.3g}')
    print('PASS: continuum sweep 9/8, boundary/center atoms, near-endpoint turn, quantile paths')
    print('PASS: complete finite capture-order searches on two analytic fixtures')
    print('Scope: numerical discovery implementation; no candidate or unrestricted value certificate')


if __name__ == '__main__':
    main()
