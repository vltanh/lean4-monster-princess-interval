#!/usr/bin/env python3
"""Exact full-signed-CDF unit-leg actions for a global verification potential.

The law supplies exact CDF line cells.  The left leg uses the strict CDF
trace; the right leg uses the closed trace.  Initial, center, incoming,
and endpoint capture atoms are consequently retained.
"""


class SignedLegActions:
    def __init__(self, law):
        self.law = law
        self.zero, self.one = law.zero, law.one

    def leg(self, t, x, e, lower, upper, velocity):
        if velocity not in (-1, 1):
            raise ValueError('The canonical leg velocity is -1 or +1')
        y = x+velocity*(e-t)
        assert t <= e and -1 <= y <= 1
        strict, closed = self.law.cdf_sides(e, y)
        if velocity == 1:
            newlower, newupper = lower, max(upper, closed)
            captured = newupper-upper
        else:
            newlower, newupper = min(lower, strict), upper
            captured = lower-newlower
        area = self.zero
        for lo, hi, radial, region in self.law._radial_cells(
                t, e, velocity, x-velocity*t):
            left, right = self.law._cdf_lines(radial, region)
            if velocity == 1:
                slope, constant = right[0], right[1]-upper
            else:
                slope, constant = -left[0], lower-left[1]
            cuts = [lo, hi]
            if slope:
                root = -constant/slope
                if lo < root < hi:
                    cuts.insert(1, root)
            for start, end in zip(cuts, cuts[1:]):
                if slope*(start+end)/2+constant > 0:
                    area += slope*(end*end-start*start)/2+constant*(end-start)
        return e*captured-area, y, newlower, newupper

    @staticmethod
    def endpoint_tail(t, x, lower, upper):
        """Exact only once the law has been absorbed at the endpoints."""
        left_first = lower*(t+x+1)+(1-upper)*(t+x+3)
        right_first = (1-upper)*(t+1-x)+lower*(t+3-x)
        return min(left_first, right_first)


def capture_records(law, vertices):
    """Exact strict lower / closed upper CDF extrema along an arbitrary prefix."""
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
            for time in [lo, hi]:
                position = velocity*time+intercept
                if time == start:
                    position = xstart
                elif time == end:
                    position = xend
                left, right = law.cdf_sides(time, position)
                lower, upper = min(lower, left), max(upper, right)
        left, right = law.cdf_sides(end, xend)
        lower, upper = min(lower, left), max(upper, right)
    return lower, upper


def append_endpoint_tail(route, t, x, lower, upper):
    left_first = lower*(t+x+1)+(1-upper)*(t+x+3)
    right_first = (1-upper)*(t+1-x)+lower*(t+3-x)
    if left_first <= right_first:
        route.extend([(t+x+1, -1), (t+x+3, 1)])
    else:
        route.extend([(t+1-x, 1), (t+3-x, -1)])
