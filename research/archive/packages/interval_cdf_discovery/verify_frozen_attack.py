#!/usr/bin/env python3
"""Exact same-half attack on the two frozen discovery fields.

The route is checked both by the initial-inward CDF formula and by
independent signed-CDF first-moment actions. This excludes the pooled
objective as a guarantee for these fields; it is not a game-value bound.
"""
from fractions import Fraction as Q
import json
from pathlib import Path

from audit_m1 import ExactField


def main():
    root = Path(__file__).resolve().parent / 'snapshots'
    a, v, s = Q(13, 16), Q(-3, 4), Q(1)
    route = [(Q(0), a), ((a+v)/2, (a-v)/2),
             ((s+v)/2, (s-v)/2), (s+1, Q(-1)), (s+3, Q(1))]
    results = []
    for name in ['constant_half_wait_candidate', 'constant_half_wait_repaired']:
        field = ExactField(json.loads((root / (name+'.json')).read_text()))
        A = field.initial_value(a)
        L = field.radial(a, v)
        M = max(A, field.radial(s, v))
        N = field.integral(a, -a, v, 0)
        F = field.integral(s, v, s, 0, L)
        I = (field.integral(v, a, s, 1)-A*(s-a)
             + field.integral(v, a, s, 1, A))
        H = field.integral(s, s, s+2, 1)
        formula = (4*s+8+N+(2*s-a-v)*L-(s+6-v)*M-(s+v)*A-F-I-H)/4
        independent = field.unit_route_payoff(route)
        assert formula == independent
        assert formula < Q(142147, 100000)
        for z in [Q(0), Q(1, 10), Q(11, 20), Q(9, 10), Q(63, 64), Q(1)]:
            for sign in [-1, 1]:
                x = sign*z
                actual = field.unit_route_payoff([(0, x), (1-x, 1), (3-x, -1)])
                predicted = field.positive_m1(z) if sign == 1 else field.negative_m1(z)
                assert actual == predicted
        results.append(dict(field=name+'.json', value=str(formula), decimal=float(formula)))
    result = dict(scope='Exact specified-field exclusions, not a bound on the unrestricted game.',
                  route=[[str(t), str(x)] for t, x in route],
                  strict_upper='142147/100000', fields=results,
                  independent_m1_checks=24)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
