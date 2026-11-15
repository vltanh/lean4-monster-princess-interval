#!/usr/bin/env python3
"""Exact independent checks of the coupled front derivatives and example."""

from fractions import Fraction as F
from audit_two_turn_formulas import independent_integral
from continuous_rank import FiveLegLaw


def interpolate(knots, row, q):
    for i in range(len(knots)-1):
        if knots[i] <= q <= knots[i+1]:
            return row[i]+(row[i+1]-row[i])*(q-knots[i])/(knots[i+1]-knots[i])
    raise AssertionError(q)


def main():
    knots = [F(0), F(7, 20), F(3, 4), F(1)]
    initial = [F(1, 10), F(3, 5), F(17, 20), F(99, 100)]
    incoming = [F(4, 5), F(19, 20), F(99, 100), F(1)]
    outgoing = [F(3, 5), F(11, 20), F(2, 5), F(1, 5)]
    late = [F(1001, 1000)+q/F(10**6) for q in knots]
    last = [F(9, 10), F(4, 5), F(3, 5), F(3, 10)]
    rows = [initial, incoming, outgoing, late, last]
    law = FiveLegLaw(knots, *rows)
    def payoff(s, z):
        route = [(F(0), -z), ((s+z)/2, (s-z)/2),
                 (s+1, F(-1)), (s+3, F(1))]
        return sum(independent_integral(knots, rows, route, sign)
                   for sign in (-1, 1))/2
    for z, quantile in [(F(21, 50), F(4, 5)),
                        (F(21, 25), F(3, 20)),
                        (F(7, 10), F(2, 5)),
                        (F(3, 4), F(11, 25))]:
        s = interpolate(knots, late, quantile)
        r, b, d, q = law.A(z), law.Is[0](z), law.Ds[0](z), law.Is[1](s)
        assert d < q < law.Ds[1](z)
        aprime = law.A.affine_at(z)[0]
        b1prime = law.Is[0].affine_at(z)[0]
        d1prime = law.Ds[0].affine_at(z)[0]
        b2prime = law.Is[1].affine_at(s)[0]
        correction = ((interpolate(knots, initial, b)+interpolate(knots, outgoing, b))*b1prime
                      +(interpolate(knots, late, d)-interpolate(knots, incoming, d))*(-d1prime))
        cs = (2*(2-r-q)-(6+s-z)*b2prime)/4
        cz = (-2*(s+1)*aprime+r+q+correction)/4
        mixed = (b2prime-2*aprime)/4
        hs, hz = F(1, 10**9), F(1, 10**5)
        # On a fixed affine-front chamber, the exact payoff is quadratic,
        # so these centered differences are exact identities, not estimates.
        assert (payoff(s+hs, z)-payoff(s-hs, z))/(2*hs) == cs
        assert (payoff(s, z+hz)-payoff(s, z-hz))/(2*hz) == cz
        assert ((payoff(s+hs, z+hz)-payoff(s+hs, z-hz)
                 -payoff(s-hs, z+hz)+payoff(s-hs, z-hz))/(4*hs*hz)) == mixed
    print("PASS: exact Cs, Cz, and mixed derivatives in four front chambers,")
    print("including both moving-front terms, the separation gap, and A+B2>1.")

    k0, d, center = F(13467, 250), F(11033, 12250), F(27, 20)
    tail_slope = F(1217, 4900)
    assert 2-k0/(F(6, 5)+F(11, 2))**2 == F(4, 5)
    assert 2-k0/(F(3, 2)+F(11, 2))**2 == d
    assert d+tail_slope*(F(19, 10)-F(3, 2)) == 1
    assert F(1, 2)-(F(19, 10)+F(11, 2))*tail_slope/4 == F(3971, 98000)
    assert F(1, 10)-F(5, 4) == -F(23, 20)
    for gamma in [F(0), F(1)]:
        k = k0-F(9, 400)*gamma
        assert k-gamma*F(137, 20)*F(3, 20) > 0
        for s in [F(6, 5), F(5, 4), center, F(7, 5), F(3, 2)]:
            w, difference = s+F(11, 2), s-center
            b = 2-(k+gamma*difference*difference)/(w*w)
            density = 2*(k-gamma*F(137, 20)*difference)/(w*w*w)
            derivative = (2-b)/2-w*density/4
            assert derivative == gamma*difference/(2*w)
    print("PASS: exact joins, density signs, tail derivative, and turn identities")
    print("for the flat and strict finite-last-wave counterexamples.")


if __name__ == '__main__':
    main()
