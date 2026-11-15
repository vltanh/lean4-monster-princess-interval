#!/usr/bin/env python3
"""Exact source-free comparison of a terminal free-second I route to Cell(s).

This is a conditional terminal-field identity, with the retained low ranks
below the first turn and no outgoing rows near U=1.  It does not identify
the active second-turn surface or establish a matching law.
"""
from collections import Counter
from fractions import Fraction as Q

from verify_positive_cdf_sheet import Law, direct_cost
from verify_curved_terminal_sources import CurvedWholePrefix, fixture, inward_cost


def four_difference(tail, tails, x, y, z):
    rt = sum(weight for weight, _ in tails)
    dmax = max(g.d for _, g in tails)
    rx = sum((weight for weight, g in tails if g.x < x), Q(0))
    rz = sum((weight for weight, g in tails if g.x < z), Q(0))
    a, v, s = 1-x, -1+y, 1-z
    D0 = rt*(1-tail.radial(a, v, strict=True))
    m = min(rx, rt*(1-tail.radial(s, v)))
    column = tail.integrate(v, a, s, horizontal=False,
                           transform=lambda R: min(rx, rt*(1-R)))
    row_x = rt*(y-x)-rt*tail.integrate(a, -a, v,
                                      horizontal=True, strict=True)
    row_z = rt*(y-z)-rt*tail.integrate(s, -s, v,
                                      horizontal=True, strict=True)
    hinge = tail.integrate(s, v, -1+dmax, horizontal=True, strict=True,
                           transform=lambda R: max(Q(0), D0-rt*(1-R)))
    return ((y-x)*rx-(8-2*z)*rz+column+(8-y-z)*m-row_x
            -(x-z)*D0+row_z-hinge)


def main():
    shape = [(Q(0), Q(0)), (Q(1, 2), Q(1, 4)), (Q(1), Q(1))]
    fixtures = [fixture(Q(1), shape, Q(4)),
                fixture(Q(10000), shape, Q(4))]
    _, low, q0, _ = fixtures[0]
    for bend in [Q(1, 4), Q(1, 3), Q(1, 2), Q(2, 3)]:
        tails = [(Q(1, 30), CurvedWholePrefix(d*d/16, d, bend))
                 for d in [Q(1, 10), Q(1, 20), Q(1, 40)]]
        law = Law([(q0*w, path) for w, path in low.paths]
                  +[(w, g.path) for w, g in tails])
        fixtures.append((law, low, q0, tails))
    counts = Counter()
    for law, low, q0, tails in fixtures:
        rt = 1-q0
        tail = Law([(w/rt, g.path) for w, g in tails])
        for x in [Q(1, 10000), Q(1, 3000), Q(1, 200), Q(1, 50)]:
            a = 1-x
            for y in sorted({x, 2*x, Q(3, 100), Q(3, 50), Q(2, 25)}):
                if y < x:
                    continue
                v = -1+y
                assert law.radial(a, v, strict=True) >= q0
                for fraction in [Q(0), Q(1, 7), Q(1, 2), Q(6, 7), Q(1)]:
                    z = fraction*x
                    s = 1-z
                    expected = four_difference(tail, tails, x, y, z)
                    actual = 4*(inward_cost(law, a, v, s)
                                -direct_cost(law, 2+s, -s))
                    assert actual == expected, (x, y, z, actual, expected)
                    counts['source-free CI minus Cell(s)'] += 1
                    if z == x:
                        assert actual == 0
                        counts['zero outward-leg cancellation'] += 1
    print('PASS:', sum(counts.values()), 'exact source-free free-inward checks')
    for label, n in counts.items():
        print(' ', label+':', n)
    print('Scope: terminal response identity; no active support or global value claim')


if __name__ == '__main__':
    main()
