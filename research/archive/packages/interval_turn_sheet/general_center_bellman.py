#!/usr/bin/env python3
"""Exact center actions for a general ordered radial endpoint-by-two law.

The implementation uses the piecewise-affine CDF line interface of
continuous_rank.  It supports its ordinary and multi-wave laws, and any
subclass implementing that same interface, including non-unit-speed waves.
The terminal-at-one rule additionally requires no positive mass whose
final endpoint absorption time is exactly two.
"""


class GeneralCenterActions:
    def __init__(self, law):
        self.law = law
        self.zero, self.one = law.zero, law.one
        self.scale = 1-law.endpoint_mass

    def radial(self, u, v):
        if u == v+2:
            return self.one  # actual endpoint contact, not the interior trace
        if u == v:
            return self.scale*self.law.radial(u, self.zero)
        return self.scale*self.law.radial((u+v)/2, (u-v)/2)

    def center(self, t):
        return self.scale*self.law.radial(t, self.zero)

    def row_integral(self, t, e, threshold):
        """Integral_t^e (R(U,t)-threshold)_+ dU."""
        if e <= t:
            return self.zero
        value = self.zero
        for lo, hi, (slope, constant), _ in self.law._radial_cells(
                t, (t+e)/2, self.one, -t):
            slope *= self.scale
            constant = self.scale*constant-threshold
            cuts = [lo, hi]
            if slope:
                root = -constant/slope
                if lo < root < hi:
                    cuts.insert(1, root)
            for left, right in zip(cuts, cuts[1:]):
                if slope*(left+right)/2+constant > 0:
                    value += slope*(right*right-left*left)+2*constant*(right-left)
        return value

    def outward(self, t, e, frontier):
        rho = self.radial(e, t)
        newly_caught = max(self.zero, rho-frontier)
        return ((t+e)*newly_caught-self.row_integral(t, e, frontier))/4

    def triangle(self, t, e, positive, negative, sign=1):
        """Immediate absolute capture contribution and both updated frontiers."""
        outward = positive if sign == 1 else negative
        opposite = negative if sign == 1 else positive
        rho, central = self.radial(e, t), self.center(e)
        value = self.outward(t, e, outward)+e*max(self.zero, central-opposite)/2
        outward = max(outward, rho)
        opposite = max(opposite, central)
        if sign == 1:
            return value, outward, opposite
        return value, opposite, outward

    def center_record_integral(self, t, e, frontier):
        """Return new frontier and integral of its increase during a center wait."""
        initial = frontier
        frontier = max(frontier, self.center(t))
        area = self.zero
        for lo, hi, (slope, constant), _ in self.law._radial_cells(
                t, e, self.zero, self.zero):
            slope *= self.scale
            constant *= self.scale
            frontier = max(frontier, slope*lo+constant)
            if slope > 0 and slope*hi+constant > frontier:
                crossing = max(lo, min(hi, (frontier-constant)/slope))
                area += (frontier-initial)*(crossing-lo)
                area += (slope*(hi*hi-crossing*crossing)/2
                         +(constant-initial)*(hi-crossing))
                frontier = slope*hi+constant
            else:
                area += (frontier-initial)*(hi-lo)
        frontier = max(frontier, self.center(e))
        return frontier, area

    def wait(self, t, e, positive, negative):
        plus, plus_area = self.center_record_integral(t, e, positive)
        minus, minus_area = self.center_record_integral(t, e, negative)
        value = (e*(plus-positive+minus-negative)-plus_area-minus_area)/2
        return value, plus, minus

    @staticmethod
    def endpoint(e, positive, negative):
        return (e+2)*(1-(positive+negative)/2)-abs(positive-negative)/2

    def sweep(self, t, positive, negative, sign=1):
        outward = positive if sign == 1 else negative
        opposite = negative if sign == 1 else positive
        return self.outward(t, t+2, outward)+(t+3)*(1-opposite)/2

    def terminal_triangle(self, t, e, positive, negative, sign=1):
        value, positive, negative = self.triangle(t, e, positive, negative, sign)
        return value+self.endpoint(e, positive, negative)


def record_frontiers(law, vertices):
    """Independent exact CDF extrema along a route ending at center."""
    points = []
    for time, position in vertices:
        if points and time == points[-1][0]:
            assert position == points[-1][1]
            continue
        points.append((time, position))
    lower, upper = law.cdf_sides(*points[0])
    for (start, xstart), (end, xend) in zip(points, points[1:]):
        velocity = (xend-xstart)/(end-start)
        intercept = xstart-velocity*start
        for lo, hi, radial, region in law._radial_cells(start, end, velocity, intercept):
            lline, rline = law._cdf_lines(radial, region)
            lower = min(lower, lline[0]*lo+lline[1], lline[0]*hi+lline[1])
            upper = max(upper, rline[0]*lo+rline[1], rline[0]*hi+rline[1])
            # Exact center and endpoint contacts can jump the closed trace.
            for time in [lo, hi]:
                position = velocity*time+intercept
                if time == start:
                    position = xstart
                elif time == end:
                    position = xend
                if position in (-1, 0, 1):
                    left, right = law.cdf_sides(time, position)
                    lower, upper = min(lower, left), max(upper, right)
        left, right = law.cdf_sides(end, xend)
        lower, upper = min(lower, left), max(upper, right)
    assert points[-1][1] == 0
    return 2*upper-1, 1-2*lower


def append_general_triangle(route, t, e, sign=1):
    if route[-1][0] < t:
        route.append((t, t*0))
    if e > t:
        route.extend([((t+e)/2, sign*(e-t)/2), (e, e*0)])


def append_endpoint_completion(route, e, positive, negative):
    first = 1 if positive <= negative else -1
    route.extend([(e+1, first), (e+3, -first)])
