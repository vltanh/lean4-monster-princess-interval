#!/usr/bin/env python3
"""Continuous ordered-rank capture payoffs, without sampling princess paths.

The positive princess at uniform rank q follows

    min(1, max(min(a(q)+t, u(q)-t), t-C(q), 0)),

where a,u increase strictly and C decreases strictly, and all three are
piecewise affine on the supplied quantile partition. The reflected law has
equal mass. An optional total mass endpoint_mass is split between the two
stationary endpoints. Rational inputs in exact mode give a Fraction payoff.

The engine integrates the running left/right CDF records along a polygonal
monster. It never calls the finite-hider capture-order oracle.
"""

from bisect import bisect_right
from dataclasses import dataclass
from fractions import Fraction


def _number(value, exact):
    if exact:
        if isinstance(value, float):
            raise TypeError("Use integers, strings, or Fractions in exact mode.")
        return Fraction(value)
    return float(value)


@dataclass(frozen=True)
class Payoff:
    value: object
    survival: object
    cutoff: object
    affine_cells: int


class PiecewiseCDF:
    """Continuous affine interpolation, constant outside its knot range."""

    def __init__(self, x, y):
        self.x = tuple(x)
        self.y = tuple(y)
        assert len(x) == len(y) >= 2
        assert all(a < b for a, b in zip(x, x[1:]))

    def affine_at(self, x):
        zero = self.x[0] * 0
        if x <= self.x[0]:
            return zero, self.y[0]
        if x >= self.x[-1]:
            return zero, self.y[-1]
        i = bisect_right(self.x, x) - 1
        slope = (self.y[i+1] - self.y[i]) / (self.x[i+1] - self.x[i])
        return slope, self.y[i] - slope * self.x[i]

    def __call__(self, x):
        slope, intercept = self.affine_at(x)
        return slope * x + intercept


class RankLaw:
    def __init__(self, q, a, u, c, endpoint_mass=0, *, exact=True):
        self.exact = exact
        self.q, self.a, self.u, self.c = (
            tuple(_number(v, exact) for v in values) for values in (q, a, u, c)
        )
        self.endpoint_mass = _number(endpoint_mass, exact)
        self.zero, self.one = _number(0, exact), _number(1, exact)
        self.tol = self.zero if exact else 1e-12
        assert len(self.q) == len(self.a) == len(self.u) == len(self.c) >= 2
        assert self.q[0] == 0 and self.q[-1] == 1
        for values in (self.q, self.a, self.u):
            assert all(x < y for x, y in zip(values, values[1:]))
        assert all(x > y for x, y in zip(self.c, self.c[1:]))
        assert all(0 <= a <= 1 and u >= a and -a <= c <= 1
                   for a, u, c in zip(self.a, self.u, self.c))
        assert 0 <= self.endpoint_mass <= 1
        self.A = PiecewiseCDF(self.a, self.q)
        self.B = PiecewiseCDF(self.u, self.q)
        self.D = PiecewiseCDF(self.c[::-1], self.q[::-1])

    def radial(self, t, r):
        """CDF at 0<=r<1; at r=1, its limit from the interior."""
        return min(max(self.A(r-t), self.B(t+r)), self.D(t-r))

    def cdf_sides(self, t, x):
        """Return Pr(p(t)<x), Pr(p(t)<=x), including center/endpoint atoms."""
        half = self.one / 2
        radius = abs(x)
        mass = (1-self.endpoint_mass) * self.radial(t, radius) / 2
        if x == 0:
            return half-mass, half+mass
        if x == 1:
            return half+mass, self.one
        if x == -1:
            return self.zero, half-mass
        if x > 0:
            return half+mass, half+mass
        return half-mass, half-mass

    def parameters(self, q):
        """Rank interpolation, used only by independent checks and plotting."""
        i = min(max(bisect_right(self.q, q)-1, 0), len(self.q)-2)
        w = (q-self.q[i])/(self.q[i+1]-self.q[i])
        return tuple(values[i] + w*(values[i+1]-values[i])
                     for values in (self.a, self.u, self.c))

    def position(self, t, q):
        a, u, c = self.parameters(q)
        return min(self.one, max(min(a+t, u-t), t-c, self.zero))

    def _components(self, r_velocity, r_intercept):
        return ((self.A, (r_velocity-1, r_intercept)),
                (self.B, (r_velocity+1, r_intercept)),
                (self.D, (1-r_velocity, -r_intercept)))

    def _selected_radial(self, lines, time):
        value = lambda j: lines[j][0]*time+lines[j][1]
        first = max((0, 1), key=value)
        return min((first, 2), key=value)

    def _radial_cells(self, start, end, velocity, intercept):
        """Yield (time0,time1,radial-affine,region) on one monster leg."""
        cuts = {start, end}
        if velocity:
            crossing = -intercept / velocity
            if start < crossing < end:
                cuts.add(crossing)
        signcuts = sorted(cuts)
        for left, right in zip(signcuts, signcuts[1:]):
            middle = (left+right)/2
            xmiddle = velocity*middle+intercept
            sign = 1 if xmiddle > 0 else (-1 if xmiddle < 0 else 0)
            if velocity == 0 and intercept in (-1, 0, 1):
                region = int(intercept) * 2  # -2,+2 endpoints, 0 center
            else:
                region = sign
            r_velocity, r_intercept = sign*velocity, sign*intercept
            components = self._components(r_velocity, r_intercept)
            affinecuts = {left, right}
            for dist, (slope, constant) in components:
                if slope:
                    for knot in dist.x:
                        crossing = (knot-constant)/slope
                        if left < crossing < right:
                            affinecuts.add(crossing)
            affinecuts = sorted(affinecuts)
            for low, high in zip(affinecuts, affinecuts[1:]):
                mid = (low+high)/2
                lines = []
                for dist, (slope, constant) in components:
                    dslope, dconstant = dist.affine_at(slope*mid+constant)
                    lines.append((dslope*slope, dslope*constant+dconstant))
                clampcuts = {low, high}
                for i in range(len(lines)):
                    for j in range(i):
                        denominator = lines[i][0]-lines[j][0]
                        if denominator:
                            crossing = (lines[j][1]-lines[i][1])/denominator
                            if low < crossing < high:
                                clampcuts.add(crossing)
                clampcuts = sorted(clampcuts)
                for lo, hi in zip(clampcuts, clampcuts[1:]):
                    md = (lo+hi)/2
                    selected = self._selected_radial(lines, md)
                    yield lo, hi, lines[selected], region

    def _cdf_lines(self, radial, region):
        slope, constant = radial
        scale, half = (1-self.endpoint_mass)/2, self.one/2
        positive = scale*slope, half+scale*constant
        negative = -scale*slope, half-scale*constant
        if region == 0:
            return negative, positive
        if region == 2:
            return positive, (self.zero, self.one)
        if region == -2:
            return (self.zero, self.zero), negative
        if region == 1:
            return positive, positive
        return negative, negative

    def payoff(self, vertices, *, require_complete=True):
        """Exact expected min(capture time, last time), plus survival mass.

        With require_complete=True, surviving mass is rejected, so value is
        the full expected capture time. Arbitrary fixed rational leg speeds
        in [-1,1] are permitted; the response theorem uses only -1,0,+1.
        """
        points = []
        for time, position in vertices:
            point = _number(time, self.exact), _number(position, self.exact)
            assert -1 <= point[1] <= 1
            if points and point[0] == points[-1][0]:
                assert point[1] == points[-1][1]
                continue
            points.append(point)
        assert len(points) >= 1 and points[0][0] == 0
        lower, upper = self.cdf_sides(*points[0])
        total, cells = self.zero, 0
        for (start, xstart), (end, xend) in zip(points, points[1:]):
            assert end > start
            assert abs(xend-xstart) <= end-start+self.tol
            velocity = (xend-xstart)/(end-start)
            intercept = xstart-velocity*start
            for low, high, radial, region in self._radial_cells(
                    start, end, velocity, intercept):
                if high <= low:
                    continue
                xlow = velocity*low+intercept
                # Monster vertices must retain their exact 0/endpoint value.
                if low == start:
                    xlow = xstart
                elif low == end:
                    xlow = xend
                if velocity and low == -intercept/velocity:
                    xlow = self.zero
                left, right = self.cdf_sides(low, xlow)
                lower, upper = min(lower, left), max(upper, right)
                lline, rline = self._cdf_lines(radial, region)
                lower = min(lower, lline[0]*low+lline[1])
                upper = max(upper, rline[0]*low+rline[1])
                recordcuts = {low, high}
                for line, record in ((lline, lower), (rline, upper)):
                    if line[0]:
                        crossing = (record-line[1])/line[0]
                        if low < crossing < high:
                            recordcuts.add(crossing)
                recordcuts = sorted(recordcuts)
                for lo, hi in zip(recordcuts, recordcuts[1:]):
                    md = (lo+hi)/2
                    lactive = lline if lline[0]*md+lline[1] < lower else (self.zero, lower)
                    ractive = rline if rline[0]*md+rline[1] > upper else (self.zero, upper)
                    slope = lactive[0]-ractive[0]
                    constant = 1+lactive[1]-ractive[1]
                    total += slope*(hi*hi-lo*lo)/2+constant*(hi-lo)
                    cells += 1
                lower = min(lower, lline[0]*high+lline[1])
                upper = max(upper, rline[0]*high+rline[1])
            left, right = self.cdf_sides(end, xend)
            lower, upper = min(lower, left), max(upper, right)
        survival = 1-upper+lower
        if require_complete and abs(survival) > self.tol:
            raise ValueError(f"Monster unfinished: surviving mass {survival}")
        return Payoff(total, survival, points[-1][0], cells)


class MultiLegRankLaw(RankLaw):
    """Ordered 2k+1-leg law with no early endpoint peaks at interior ranks.

    incoming[j] is A_(j+1)(q); outgoing[j] is C_(j+1)(q).
    Each incoming function increases strictly, each outgoing decreases
    strictly, and they are ordered across leg indices. The checked peak
    inequalities exclude early endpoint absorption for every q<1; the
    top rank itself has zero measure. The final C is at most one.
    """

    def __init__(self, q, a, incoming, outgoing, endpoint_mass=0, *, exact=True):
        assert len(incoming) == len(outgoing) >= 1
        super().__init__(q, a, incoming[0], outgoing[0], endpoint_mass, exact=exact)
        self.incoming = tuple(tuple(_number(v, exact) for v in values)
                              for values in incoming)
        self.outgoing = tuple(tuple(_number(v, exact) for v in values)
                              for values in outgoing)
        self.legs = len(self.incoming)
        for values in self.incoming:
            assert len(values) == len(self.q)
            assert all(x < y for x, y in zip(values, values[1:]))
        for values in self.outgoing:
            assert len(values) == len(self.q)
            assert all(x > y for x, y in zip(values, values[1:]))
            assert all(v <= 1 for v in values)
        assert all(a+u <= 2 for a, u in zip(self.a, self.incoming[0]))
        for j in range(1, self.legs):
            assert all(old <= new for old, new in zip(self.incoming[j-1], self.incoming[j]))
            assert all(old <= new for old, new in zip(self.outgoing[j-1], self.outgoing[j]))
            assert all(u-c <= 2 for u, c in zip(self.incoming[j], self.outgoing[j-1]))
        self.Is = tuple(PiecewiseCDF(values, self.q) for values in self.incoming)
        self.Ds = tuple(PiecewiseCDF(values[::-1], self.q[::-1]) for values in self.outgoing)

    def radial(self, t, r):
        result = self.A(r-t)
        for inc, dec in zip(self.Is, self.Ds):
            result = max(result, min(inc(t+r), dec(t-r)))
        return result

    def parameters(self, q):
        i = min(max(bisect_right(self.q, q)-1, 0), len(self.q)-2)
        w = (q-self.q[i])/(self.q[i+1]-self.q[i])
        rows = [self.a]
        for incoming, outgoing in zip(self.incoming, self.outgoing):
            rows.extend((incoming, outgoing))
        return tuple(values[i]+w*(values[i+1]-values[i]) for values in rows)

    def position(self, t, q):
        values = self.parameters(q)
        value = values[0]+t
        for incoming, outgoing in zip(values[1::2], values[2::2]):
            value = max(min(value, incoming-t), t-outgoing)
        return min(self.one, max(value, self.zero))

    def _components(self, r_velocity, r_intercept):
        components = [(self.A, (r_velocity-1, r_intercept))]
        for inc, dec in zip(self.Is, self.Ds):
            components.extend(((inc, (r_velocity+1, r_intercept)),
                               (dec, (1-r_velocity, -r_intercept))))
        return tuple(components)

    def _selected_radial(self, lines, time):
        value = lambda j: lines[j][0]*time+lines[j][1]
        candidates = [0]
        for j in range(self.legs):
            candidates.append(min((2*j+1, 2*j+2), key=value))
        return max(candidates, key=value)


class FiveLegLaw(MultiLegRankLaw):
    def __init__(self, q, a, u1, c1, u2, c2, endpoint_mass=0, *, exact=True):
        super().__init__(q, a, (u1, u2), (c1, c2), endpoint_mass, exact=exact)

