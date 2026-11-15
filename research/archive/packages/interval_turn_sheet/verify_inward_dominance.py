#!/usr/bin/env python3
"""Exact rank-based removal of unproductive inward/outward blocks.

Complete continuum costs are compared with bounds from capture classes;
individual polygon intersections independently test pointwise dominance.
No optimal support or game value is assumed.
"""
from collections import Counter
from fractions import Fraction as Q

from verify_general_center import SlowWaveRankLaw
from verify_initial_inward_start import princess


def clean(route):
    out = []
    for point in route:
        if out and point[0] == out[-1][0]:
            assert point[1] == out[-1][1]
        else:
            out.append(point)
    return out


def inward(a, v, s=Q(1)):
    return clean([(Q(0), a), ((a+v)/2, (a-v)/2),
                  ((s+v)/2, (s-v)/2), (s+1, Q(-1)),
                  (s+3, Q(1))])


def left(a):
    return [(Q(0), a), (a+1, Q(-1)), (a+3, Q(1))]


def negative_three(z, s, t):
    return clean([(Q(0), -z), ((s+z)/2, (s-z)/2),
                  ((s+t)/2, (s-t)/2), (t+1, Q(1)),
                  (t+3, Q(-1))])


def capture(p, monster, sign):
    best = None
    for (pa, xa), (pb, xb) in zip(p, p[1:]):
        pv = sign*(xb-xa)/(pb-pa)
        pi = sign*xa-pv*pa
        for (ma, ya), (mb, yb) in zip(monster, monster[1:]):
            lo, hi = max(pa, ma), min(pb, mb)
            if lo > hi:
                continue
            mv = (yb-ya)/(mb-ma)
            mi = ya-mv*ma
            slope, offset = pv-mv, pi-mi
            if slope == 0:
                point = lo if offset == 0 else None
            else:
                root = -offset/slope
                point = root if lo <= root <= hi else None
            if point is not None:
                best = point if best is None else min(best, point)
    assert best is not None
    return best


def pointwise(law, better, worse, counts, label):
    for q in [Q(k, 11) for k in range(12)]:
        path = princess(law, q)
        for sign in [-1, 1]:
            assert capture(path, better, sign) <= capture(path, worse, sign)
            counts[label] += 1


def main():
    counts = Counter()
    for speed in [Q(1, 3), Q(2, 3), Q(1)]:
        law = SlowWaveRankLaw([0, Q(2, 5), 1],
            [Q(1, 20), Q(2, 5), Q(9, 10)],
            [Q(1, 4), Q(3, 5), Q(19, 20)],
            [Q(4, 5), Q(1, 5), -Q(4, 5)], [speed, Q(1), Q(1)])
        for a in [Q(k, 13) for k in range(1, 13)]:
            A = law.A(a)
            cell = law.payoff(left(a)).value
            for fraction in [Q(k, 8) for k in range(8)]:
                v = -a+2*a*fraction
                B = law.radial((1+v)/2, (1-v)/2)
                old = inward(a, v)
                cost = law.payoff(old).value
                delta = max(Q(0), B-A)
                lower = ((1-a)*(2-A)-(4-(a+v)/2)*delta)/2
                assert cost-cell >= lower
                counts['quantitative active-rank strip'] += 1
                if B <= A:
                    assert cost > cell
                    counts['strict inactive-rank cost'] += 1
                    pointwise(law, left(a), old, counts, 'inactive-rank pointwise captures')
                # The continuous incoming family completes strictly before
                # U=1. Choose a second turn inside its final CDF plateau.
                uB = law.parameters(B)[1]
                s = (1+max(a, uB))/2
                Bs = law.radial((s+v)/2, (s-v)/2)
                if Bs == B:
                    shorter = inward(a, v, s)
                    new_cost = law.payoff(shorter).value
                    gap = (1-s)*(2-max(A, B))/2
                    assert cost-new_cost >= gap > 0
                    counts['strict earlier second-turn attack'] += 1
                    pointwise(law, shorter, old, counts, 'earlier-turn pointwise captures')
        for z in [Q(3, 4), Q(7, 8), Q(15, 16)]:
            A = law.A(z)
            direct = [(t, -x) for t, x in left(z)]
            for s in [z, (z+1)/2, Q(1)]:
                for t in [s, (s+1)/2, Q(1)]:
                    D = law.radial((s+t)/2, (t-s)/2)
                    if D > A:
                        continue
                    old = negative_three(z, s, t)
                    assert law.payoff(old).value >= law.payoff(direct).value
                    counts['negative M3 empty-return block'] += 1
                    pointwise(law, direct, old, counts, 'negative-M3 pointwise captures')
    print('PASS:', sum(counts.values()), 'exact inward dominance checks')
    for label, n in counts.items():
        print(' ', label+':', n)
    print('Scope: specified capture classes and legal finite attacks; no equilibrium claim')


if __name__ == '__main__':
    main()
