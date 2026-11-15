#!/usr/bin/env python3
"""Analytic fixtures and an independent segment-intersection sanity check."""

from fractions import Fraction as F
from continuous_rank import RankLaw, FiveLegLaw


def direct_capture(law, q, sign, monster):
    """Intersect explicit polygonal paths; no CDF or rank-record algorithm."""
    values = law.parameters(q)
    end = monster[-1][0]
    lines = [(1, values[0]), (0, 0), (0, 1)]
    for incoming, outgoing in zip(values[1::2], values[2::2]):
        lines.extend(((-1, incoming), (1, -outgoing)))
    cuts = {0.0, end}
    for i, (slope, constant) in enumerate(lines):
        for oslope, oconstant in lines[:i]:
            if slope != oslope:
                time = (oconstant-constant)/(slope-oslope)
                if 0 < time < end:
                    cuts.add(time)
    times = sorted(cuts)
    princess = [(t, sign*law.position(t, q)) for t in times]
    for (t0, x0), (t1, x1) in zip(monster, monster[1:]):
        mv = (x1-x0)/(t1-t0)
        mb = x0-mv*t0
        for (s0, y0), (s1, y1) in zip(princess, princess[1:]):
            lo, hi = max(t0, s0), min(t1, s1)
            if hi < lo:
                continue
            pv = (y1-y0)/(s1-s0)
            pb = y0-pv*s0
            d0 = (mv-pv)*lo+mb-pb
            d1 = (mv-pv)*hi+mb-pb
            if abs(d0) < 1e-10:
                return lo
            if abs(d1) < 1e-10:
                return hi
            if d0*d1 <= 0:
                return (pb-mb)/(mv-pv)
    raise AssertionError("Independent path intersection found a survivor")


def main():
    outward = RankLaw([0, 1], [0, 1], [0, 1], [0, -1])
    assert outward.payoff([(0, 1), (2, -1)]).value == F(9, 8)
    assert outward.payoff([(0, 0), (1, 1), (3, -1)]).value == 2
    assert outward.payoff([(0, 0), (1, 0), (2, 1), (4, -1)]).value == 3
    mixture = RankLaw([0, 1], [0, 1], [0, 1], [0, -1], F(1, 3))
    assert mixture.payoff([(0, 1), (2, -1)]).value == F(13, 12)
    central = RankLaw([0, 1], [0, 1], [0, 1], [1, 0])
    short = central.payoff([(0, 0), (F(1, 2), 0)], require_complete=False)
    assert short.value == F(3, 8) and short.survival == F(1, 2)
    assert central.payoff([(0, 0), (F(1, 2), 0),
                           (F(3, 2), 1), (F(7, 2), -1)]).value == F(11, 8)
    arrivals = RankLaw([0, 1], [0, F(1, 2)], [0, F(1, 2)], [1, F(1, 2)])
    assert arrivals.payoff([(0, 0), (F(1, 2), 0)]).value == F(1, 4)
    print("PASS: seven exact analytic fixtures, including all three atom locations.")

    # A two-parameter word with positive-length coincident central waits.
    for s, h in [(F(1, 10), F(1, 20)), (F(1, 8), F(1, 10))]:
        e = s+2*h
        route = [(0, 0), (s, 0), (s+h, h), (e, 0), (e+1, -1), (e+3, 1)]
        assert central.payoff(route).value == F(13, 8)-s/2-h+h*h/2
    # The generic polynomial extension differs from the actual equality face.
    for z in [F(1, 100), F(1, 50), F(3, 100), F(1, 25)]:
        route = [(0, z), (F(1, 2), z), (F(3, 2)-z, 1), (F(7, 2)-z, -1)]
        assert central.payoff(route).value == F(35, 16)-5*z/8+z*z/8
    assert F(35, 16)-F(11, 8) == F(13, 16)
    print("PASS: fixed-word quadratics and a positive-mass equality-face jump.")

    data = ([0, F(2, 5), 1], [F(1, 5), F(2, 5), F(9, 10)],
            [F(2, 5), F(3, 5), F(11, 10)], [F(4, 5), F(1, 2), F(-1, 2)])
    exact = RankLaw(*data)
    law = RankLaw(*data, exact=False)
    routes = [
        [(0, 1), (2, -1)],
        [(0, F(2, 3)), (F(5, 3), -1), (F(11, 3), 1)],
        [(0, F(3, 4)), (F(1, 4), F(1, 2)), (F(3, 4), 1), (F(11, 4), -1)],
        [(0, F(1, 2)), (F(1, 2), 0), (F(3, 4), F(1, 4)), (1, 0),
         (F(5, 4), 0), (F(9, 4), -1), (F(17, 4), 1)],
        [(0, 0), (F(1, 3), 0), (F(1, 2), F(-1, 6)), (F(2, 3), 0),
         (F(5, 3), 1), (F(11, 3), -1)],
        [(0, -1), (F(1, 5), -1), (F(11, 5), 1)],
    ]
    samples = 257
    for route in routes:
        rational = exact.payoff(route)
        floating = law.payoff(route)
        assert abs(float(rational.value)-floating.value) < 2e-12
        monster = [(float(t), float(x)) for t, x in route]
        sampled = sum(direct_capture(law, (i+.5)/samples, sign, monster)
                      for i in range(samples) for sign in (-1, 1))/(2*samples)
        # Monotone quantile discrepancy bounds both CDF records uniformly.
        assert abs(sampled-floating.value) <= float(route[-1][0])/samples
    print("PASS: six exact/float comparisons and independent polygonal capture checks.")

    # Equal successive characteristics must reproduce the three-leg law.
    duplicate = FiveLegLaw([0, 1], [0, 1], [0, 1], [1, 0], [0, 1], [1, 0])
    for route in routes:
        assert duplicate.payoff(route).value == central.payoff(route).value
    # Two distinct center-arrival waves. Waiting at zero first captures ranks
    # q<=2/5 at u1=1/10+7q/10, then 2/5<q<=4/7 at u2=3/5+q/2.
    five_data = ([0, 1], [F(1, 20), F(3, 5)],
                 [F(1, 10), F(4, 5)], [F(1, 2), F(1, 5)],
                 [F(3, 5), F(11, 10)], [1, F(4, 5)])
    five_exact = FiveLegLaw(*five_data)
    five_float = FiveLegLaw(*five_data, exact=False)
    q1, q2 = F(2, 5), F(4, 7)
    analytic = q1/10+F(7, 20)*q1*q1 + F(3, 5)*(q2-q1)+(q2*q2-q1*q1)/4+1-q2
    waiting = five_exact.payoff([(0, 0), (1, 0)], require_complete=False)
    assert waiting.value == analytic and waiting.survival == 1-q2
    for route in routes:
        rational = five_exact.payoff(route)
        floating = five_float.payoff(route)
        assert abs(float(rational.value)-floating.value) < 2e-12
        monster = [(float(t), float(x)) for t, x in route]
        sampled = sum(direct_capture(five_float, (i+.5)/samples, sign, monster)
                      for i in range(samples) for sign in (-1, 1))/(2*samples)
        assert abs(sampled-floating.value) <= float(route[-1][0])/samples
    print("PASS: five-leg degeneration, two central waves, and six independent path checks.")

    # Independent first-wave two-turn formula, including both lower-front cases.
    quantiles = [F(0), F(7, 20), F(3, 4), F(1)]
    initial = [F(1, 10), F(3, 5), F(17, 20), F(99, 100)]
    incoming = [F(4, 5), F(19, 20), F(99, 100), F(1)]
    outgoing = [F(3, 5), F(11, 20), F(2, 5), F(1, 5)]
    late = [F(1001, 1000)+q/F(10**6) for q in quantiles]
    last = [F(9, 10), F(4, 5), F(3, 5), F(3, 10)]
    front_law = FiveLegLaw(quantiles, initial, incoming, outgoing, late, last, F(1, 10))
    def rank_integral(values, low, high):
        total = F(0)
        for i in range(len(quantiles)-1):
            left, right = max(low, quantiles[i]), min(high, quantiles[i+1])
            if right <= left:
                continue
            slope = (values[i+1]-values[i])/(quantiles[i+1]-quantiles[i])
            f = lambda z: values[i]+slope*(z-quantiles[i])
            total += (right-left)*(f(left)+f(right))/2
        return total
    x, s = F(9, 10), F(1)
    for v in [F(0), F(1, 10), F(-1, 2)]:
        upper = front_law.A(x)
        lower = max(front_law.A(-v), front_law.Is[0](x))
        four_j = (2*(s+1)+s*lower+rank_integral(outgoing, 0, lower)
                  +x*(upper-lower)-rank_integral(initial, lower, upper)
                  +rank_integral(incoming, upper, 1)+v*(1-upper))
        expected = F(9, 10)*four_j/4+F(1, 10)*(s+2)
        route = [(0, x), ((x+v)/2, (x-v)/2),
                 ((s+v)/2, (s-v)/2), (s+1, -1), (s+3, 1)]
        assert front_law.payoff(route).value == expected
    print("PASS: exact first-wave two-turn formula on both missed-front branches.")

    s = late[-1]
    for v in [F(0), F(1, 4), F(1, 2), F(-1, 2)]:
        r = front_law.A(x)
        b, d1, d2 = front_law.Is[0](x), front_law.Ds[0](v), front_law.Ds[1](v)
        lower = max(front_law.A(-v), min(b, d1))
        middle, high1, high2 = max(lower, b), max(r, d1), max(r, d2)
        four_j = (2*(s+1)+s*lower+rank_integral(last, 0, lower)
                  +x*(r-lower)+rank_integral(outgoing, lower, middle)
                  -rank_integral(initial, middle, r)
                  +rank_integral(incoming, r, high1)+rank_integral(late, high1, high2)
                  +v*(high2-r)+2*(s+3)*(1-high2))
        expected = F(9, 10)*four_j/4+F(1, 10)*(s+2)
        route = [(0, x), ((x+v)/2, (x-v)/2),
                 ((s+v)/2, (s-v)/2), (s+1, -1), (s+3, 1)]
        assert front_law.payoff(route).value == expected
    print("PASS: exact last-wave two-turn formula across four capture regimes.")


if __name__ == "__main__":
    main()
