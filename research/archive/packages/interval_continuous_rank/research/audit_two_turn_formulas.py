#!/usr/bin/env python3
"""Exact audit independent of the rank-record payoff implementation.

Each first capture is the earliest valid affine segment intersection.
The uniform-rank integral is split at all candidate-validity and ordering
boundaries. No radial CDF or running-record routine computes this payoff.
"""

from fractions import Fraction as F
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from continuous_rank import FiveLegLaw


def add(a, b):
    return a[0]+b[0], a[1]+b[1]


def sub(a, b):
    return a[0]-b[0], a[1]-b[1]


def mul(k, a):
    return k*a[0], k*a[1]


def at(a, q):
    return a[0]*q+a[1]


def constrain_nonnegative(interval, line):
    lo, hi = interval
    slope, constant = line
    if slope > 0:
        lo = max(lo, -constant/slope)
    elif slope < 0:
        hi = min(hi, -constant/slope)
    elif constant < 0:
        return None
    return (lo, hi) if lo < hi else None


def independent_integral(knots, rows, route, sign):
    """Integrate first capture exactly for a law with separated valleys."""
    total = F(0)
    end = route[-1][0]
    for i, (ql, qh) in enumerate(zip(knots, knots[1:])):
        params = []
        for row in rows:
            slope = (row[i+1]-row[i])/(qh-ql)
            params.append((slope, row[i]-slope*ql))
        a, u, c, w, d = params
        times = [(F(0), F(0)), mul(F(1, 2), sub(u, a)),
                 mul(F(1, 2), add(u, c)), mul(F(1, 2), add(w, c)),
                 mul(F(1, 2), add(w, d)), add((F(0), F(1)), d),
                 (F(0), end)]
        slopes = [1, -1, 1, -1, 1, 0]
        intercepts = [a, u, mul(-1, c), w, mul(-1, d), (F(0), F(1))]
        candidates = []
        for (t0, x0), (t1, x1) in zip(route, route[1:]):
            if t0 == t1:
                continue
            mv = (x1-x0)/(t1-t0)
            mb = x0-mv*t0
            for j, (pv, pb) in enumerate(zip(slopes, intercepts)):
                pv, pb = sign*pv, mul(sign, pb)
                denominator = mv-pv
                if not denominator:
                    # Strict parameter slopes make any coincidence a single
                    # rank, hence irrelevant to this Lebesgue integral.
                    assert pb[0] != 0 or pb[1] != mb
                    continue
                meeting = mul(1/denominator, sub(pb, (F(0), mb)))
                interval = (ql, qh)
                constraints = [sub(meeting, (F(0), t0)),
                               sub((F(0), t1), meeting),
                               sub(meeting, times[j]), sub(times[j+1], meeting)]
                for condition in constraints:
                    interval = constrain_nonnegative(interval, condition)
                    if interval is None:
                        break
                if interval is not None:
                    candidates.append((meeting, interval))
        cuts = {ql, qh}
        for _, interval in candidates:
            cuts.update(interval)
        for j, (left, _) in enumerate(candidates):
            for right, _ in candidates[:j]:
                difference = sub(left, right)
                if difference[0]:
                    crossing = -difference[1]/difference[0]
                    if ql < crossing < qh:
                        cuts.add(crossing)
        ordered = sorted(cuts)
        for lo, hi in zip(ordered, ordered[1:]):
            middle = (lo+hi)/2
            valid = [line for line, (vl, vh) in candidates if vl <= middle <= vh]
            assert valid, (i, sign, lo, hi)
            first = min(valid, key=lambda line: at(line, middle))
            total += first[0]*(hi*hi-lo*lo)/2+first[1]*(hi-lo)
    return total


def rank_integral(knots, values, low, high):
    total = F(0)
    for i in range(len(knots)-1):
        left, right = max(low, knots[i]), min(high, knots[i+1])
        if right <= left:
            continue
        slope = (values[i+1]-values[i])/(knots[i+1]-knots[i])
        value = lambda q: values[i]+slope*(q-knots[i])
        total += (right-left)*(value(left)+value(right))/2
    return total


def route_for(x, v, s):
    return [(F(0), x), ((x+v)/2, (x-v)/2),
            ((s+v)/2, (s-v)/2), (s+1, F(-1)), (s+3, F(1))]


def main():
    knots = [F(0), F(7, 20), F(3, 4), F(1)]
    initial = [F(1, 10), F(3, 5), F(17, 20), F(99, 100)]
    incoming = [F(4, 5), F(19, 20), F(99, 100), F(1)]
    outgoing = [F(3, 5), F(11, 20), F(2, 5), F(1, 5)]
    late = [F(1001, 1000)+q/F(10**6) for q in knots]
    last = [F(9, 10), F(4, 5), F(3, 5), F(3, 10)]
    rows = [initial, incoming, outgoing, late, last]
    law = FiveLegLaw(knots, *rows, F(1, 10))
    integral = lambda row, lo, hi: rank_integral(knots, row, lo, hi)
    checked, positive_first_return = 0, 0
    for x in [F(1, 5), F(1, 2), F(9, 10), F(99, 100)]:
        for v in [-x, -x/2, F(0), x/2, x]:
            s = late[-1]
            if s-v >= 2:
                continue
            r, b = law.A(x), law.Is[0](x)
            d1, d2 = law.Ds[0](v), law.Ds[1](v)
            low = max(law.A(-v), min(b, d1))
            middle, high1, high2 = max(low, b), max(r, d1), max(r, d2)
            four = (2*(s+1)+s*low+integral(last, 0, low)
                    +x*(r-low)+integral(outgoing, low, middle)
                    -integral(initial, middle, r)
                    +integral(incoming, r, high1)+integral(late, high1, high2)
                    +v*(high2-r)+2*(s+3)*(1-high2))
            route = route_for(x, v, s)
            independent = sum(independent_integral(knots, rows, route, sign)
                              for sign in (-1, 1))/2
            assert independent == four/4, (x, v, independent, four/4)
            expected = F(9, 10)*independent+F(1, 10)*(s+2)
            assert law.payoff(route).value == expected
            checked += 1
            positive_first_return += middle > low
    # Explicitly exercise the previously untested first-return interval.
    for v in [F(29, 50), F(4, 5)]:
        x, s = F(9, 10), late[-1]
        r, b, d1, d2 = law.A(x), law.Is[0](x), law.Ds[0](v), law.Ds[1](v)
        low = max(law.A(-v), min(b, d1))
        middle, high1, high2 = max(low, b), max(r, d1), max(r, d2)
        assert middle > low
        four = (2*(s+1)+s*low+integral(last, 0, low)
                +x*(r-low)+integral(outgoing, low, middle)
                -integral(initial, middle, r)+integral(incoming, r, high1)
                +integral(late, high1, high2)+v*(high2-r)+2*(s+3)*(1-high2))
        route = route_for(x, v, s)
        independent = sum(independent_integral(knots, rows, route, sign)
                          for sign in (-1, 1))/2
        assert independent == four/4
        checked += 1
        positive_first_return += 1
    first_checked = 0
    for x in [F(1, 5), F(1, 2), F(9, 10), F(99, 100)]:
        for v in [-x, -x/2, F(0), F(1, 10), F(1, 5)]:
            if v > x:
                continue
            s = F(1)
            r = law.A(x)
            low = max(law.A(-v), law.Is[0](x))
            four = (2*(s+1)+s*low+integral(outgoing, 0, low)
                    +x*(r-low)-integral(initial, low, r)
                    +integral(incoming, r, 1)+v*(1-r))
            route = route_for(x, v, s)
            independent = sum(independent_integral(knots, rows, route, sign)
                              for sign in (-1, 1))/2
            assert independent == four/4
            first_checked += 1
    print(f"PASS: {checked} exact last-wave comparisons, including "
          f"{positive_first_return} nonempty first-return intervals.")
    print(f"PASS: {first_checked} exact first-wave comparisons.")
    print("All independent payoffs integrate affine first-segment intersections; "
          "no CDF record routine is used.")


if __name__ == '__main__':
    main()
