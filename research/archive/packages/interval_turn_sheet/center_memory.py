#!/usr/bin/env python3
"""A concrete endpoint-sweep value after a center-memory barrier.

The mathematical condition is max(r_plus,r_minus) >= Y_tail(t), where
Y_tail is an upper bound for every radial rank that can be caught in the
interior after departing the center at t.  Under that condition the best
continuation is the direct sweep toward the less-captured sign.

For a continuous triangular CDF field, boundary_barrier checks the
reachable-state sufficient condition H(t) >= Y_tail(t) in exact decimal
rational arithmetic.  It does not certify the field's transport cone,
the costs before the barrier, or a game value.
"""
from fractions import Fraction


def rational(value):
    return value if isinstance(value, Fraction) else Fraction(str(value))


def _boundary_values(data, which):
    points = {}
    for pair, value in zip(data['nodes'], data['values']):
        u, v = map(rational, pair)
        if (which == 'center' and u == v
                or which == 'endpoint' and u-v == 2):
            value = rational(value)
            if v in points and points[v] != value:
                raise ValueError('Conflicting boundary values')
            points[v] = value
    return sorted(points.items())


def _value_at(points, coordinate):
    for (a, x), (b, y) in zip(points, points[1:]):
        if a <= coordinate <= b:
            return x+(coordinate-a)*(y-x)/(b-a)
    if points and coordinate == points[0][0]:
        return points[0][1]
    raise ValueError('Boundary does not cover the requested coordinate')


def _boundary_max(points, left, right):
    values = [_value_at(points, left), _value_at(points, right)]
    values.extend(value for coordinate, value in points
                  if left <= coordinate <= right)
    return max(values)


def boundary_barrier(data, time):
    """Exact nodal audit for a continuous affine field on the full domain.

    Saved endpoint boundary values must be fixed-V interior limits of the
    radial CDF, rather than the closed value one at actual endpoint contact.
    The maximum is over *all* future endpoint-interior traces.  This allows
    paths that hit an endpoint, leave it, and are finally absorbed by two.
    """
    time = rational(time)
    if not 0 <= time <= 1:
        raise ValueError('The boundary audit uses a time in [0,1]')
    memory = _boundary_max(_boundary_values(data, 'center'), Fraction(0), time)
    future = _boundary_max(_boundary_values(data, 'endpoint'), time, Fraction(1))
    return {'time': time, 'center_memory': memory,
            'future_interior_front': future, 'gap': memory-future,
            'passes': memory >= future}


def sweep_value(actions, time, positive, negative, future_interior_front):
    """The attained continuation value on a certified memory region."""
    if max(positive, negative) < future_interior_front:
        raise ValueError('The interior frontier exceeds both captured prefixes')
    sign = 1 if positive <= negative else -1
    return actions.sweep(time, positive, negative, sign)


if __name__ == '__main__':
    import argparse
    import json
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('field')
    parser.add_argument('--time', default='15/16')
    args = parser.parse_args()
    with open(args.field) as source:
        result = boundary_barrier(json.load(source), Fraction(args.time))
    print(json.dumps({key: str(value) if isinstance(value, Fraction) else value
                      for key, value in result.items()}, indent=2))
    print('Scope: boundary criterion only; admissibility and earlier response costs remain separate.')
