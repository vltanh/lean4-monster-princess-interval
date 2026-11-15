#!/usr/bin/env python3
"""Exact start and boundary derivatives for the initial-inward response.

The reference payoff integrates the signed running capture records of the
complete route.  The compared expression uses local radial derivatives,
one characteristic-row integral, and an independent first inverse of an
individual princess path.  This is an identity audit, not an equilibrium.
"""
from collections import Counter
from fractions import Fraction as Q

from verify_general_center import SlowWaveRankLaw
from verify_initial_inward_cdf import route


def radial_derivatives(law, u, v):
    t, x = (u+v)/2, (u-v)/2
    speeds = law.outward_speed, law.inward_speed, law.final_speed
    coordinates = x-speeds[0]*t, x+speeds[1]*t, t-x/speeds[2]
    cdfs = law.A, law.B, law.D
    values = [cdf(z) for cdf, z in zip(cdfs, coordinates)]
    selected = max((0, 1), key=lambda j: values[j])
    selected = min((selected, 2), key=lambda j: values[j])
    density = cdfs[selected].affine_at(coordinates[selected])[0]
    du = ((1-speeds[0])/2, (1+speeds[1])/2,
          (1-1/speeds[2])/2)[selected]
    dv = (-(1+speeds[0])/2, (-1+speeds[1])/2,
          (1+1/speeds[2])/2)[selected]
    return density*du, density*dv


def integrated_ru(law, a, v):
    total = Q(0)
    for left, right, _, _ in law._radial_cells(Q(0), (a+v)/2, Q(-1), a):
        middle = (left+right)/2
        du, _ = radial_derivatives(law, a, 2*middle-a)
        total += 2*(right-left)*du
    return total


def princess(law, q):
    a, u, c = law.parameters(q)
    s = law.outward_speed
    turn = (u-a)/(1+s)
    valley = min(u, (u+c)/2)
    points = [(Q(0), a), (turn, a+s*turn),
              (valley, max(Q(0), u-valley))]
    if u < c:
        points.append((c, Q(0)))
    points.extend([(1+c, Q(1)), (Q(5), Q(1))])
    clean = []
    for point in points:
        if clean and point[0] == clean[-1][0]:
            assert point[1] == clean[-1][1]
        else:
            clean.append(point)
    return clean


def first_beta(law, q, v):
    points = princess(law, q)
    for (s, x), (t, y) in zip(points, points[1:]):
        left, right = s-x, t-y
        if v <= left:
            return s
        if v <= right:
            return s+(t-s)*(v-left)/(right-left)
    raise AssertionError(('missing first inverse', q, v))


def four(law, a, v):
    return 4*law.payoff(route(a, v)).value


def derivative(law, a, v, direction, step):
    da, dv = direction
    return (four(law, a+step*da, v+step*dv)
            -four(law, a-step*da, v-step*dv))/(2*step)


def start_formula(law, a, v):
    initial = law.A(a)
    at_turn = law.radial((a+v)/2, (a-v)/2)
    outgoing = law.radial((1+v)/2, (1-v)/2)
    assert outgoing > initial
    rho = law.A.affine_at(a)[0]
    c1 = law.parameters(at_turn)[2]
    ru, _ = radial_derivatives(law, a, v)
    return (initial-at_turn+integrated_ru(law, a, v)
            +(1+c1-a-v)*ru-2*first_beta(law, initial, v)*rho)


def main():
    counts = Counter()
    fixtures = [
        ([0, 1], [Q(1, 10), Q(4, 5)],
         [Q(1, 5), Q(9, 10)], [Q(9, 10), -Q(3, 5)]),
        ([0, Q(2, 5), 1], [Q(1, 20), Q(2, 5), Q(9, 10)],
         [Q(1, 4), Q(3, 5), Q(19, 20)],
         [Q(4, 5), Q(1, 5), -Q(4, 5)]),
    ]
    step = Q(1, 1000000)
    for speed in [Q(1, 4), Q(1, 2), Q(3, 4), Q(1)]:
        for q, a0, u, c in fixtures:
            law = SlowWaveRankLaw(q, a0, u, c, [speed, Q(1), Q(1)])
            for a in (Q(k, 23) for k in range(3, 20)):
                if not a0[0] < a < a0[-1]:
                    continue
                initial = law.A(a)
                for fraction in [Q(k, 7) for k in range(1, 7)]:
                    v = -a+2*a*fraction
                    at_turn = law.radial((a+v)/2, (a-v)/2)
                    outgoing = law.radial((1+v)/2, (1-v)/2)
                    if outgoing > initial:
                        direct = derivative(law, a, v, (Q(1), Q(0)), step)
                        refined = derivative(law, a, v, (Q(1), Q(0)), step/2)
                        # A stable quadratic-cell stencil is exact.  Skip
                        # a breakpoint rather than assign it a smooth trace.
                        if direct != refined:
                            counts['nonsmooth start faces skipped'] += 1
                            continue
                        predicted = start_formula(law, a, v)
                        assert direct == predicted, (speed, a, v, direct, predicted)
                        counts['interior start derivative'] += 1
                    elif outgoing < initial:
                        _, rv = radial_derivatives(law, a, v)
                        c1 = law.parameters(at_turn)[2]
                        predicted = (1+c1-a-v)*rv
                        direct = derivative(law, a, v, (Q(0), Q(1)), step)
                        refined = derivative(law, a, v, (Q(0), Q(1)), step/2)
                        if direct != refined:
                            counts['nonsmooth turn faces skipped'] += 1
                            continue
                        assert direct == predicted
                        counts['turn derivative beyond B=A'] += 1
                        if rv < 0:
                            assert direct < 0
                            counts['strict descending turn beyond B=A'] += 1
                if speed < 1:
                    def diagonal(s):
                        dv = (-3*four(law, a, -a)+4*four(law, a, -a+s)
                              -four(law, a, -a+2*s))/(2*s)
                        dg = (four(law, a+s, -a-s)
                              -four(law, a-s, -a+s))/(2*s)
                        return dv+dg
                    actual = diagonal(step)
                    assert diagonal(step/2) == actual
                    rho = law.A.affine_at(a)[0]
                    d = 1+law.parameters(initial)[2]
                    predicted = d*rho*(1-speed)/2
                    assert actual == predicted > 0
                    counts['immediately slower initial tangent'] += 1
    checked = sum(n for label, n in counts.items() if 'skipped' not in label)
    print('PASS:', checked, 'exact initial-inward derivative checks')
    for label, n in counts.items():
        print(' ', label+':', n)
    print('Scope: smooth cells and one-sided diagonal traces; no matching-law claim')


if __name__ == '__main__':
    main()
