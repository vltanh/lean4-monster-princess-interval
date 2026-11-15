#!/usr/bin/env python3
"""Exact continuous-start endpoint-sweep audit for a triangular CDF field.

This closes every starting position in the M1 family for the supplied
field, including stationary points between mesh coordinates. It is not an
all-monster certificate. The field must have no initial center/endpoint
atom and no outgoing V=1 atom, as in the discovery representation.
"""
import argparse
from bisect import bisect_left, bisect_right
from fractions import Fraction as Q
from functools import lru_cache
import json
from pathlib import Path

from audit_snapshot import coordinate


def cross(a, b):
    return a[0]*b[1]-a[1]*b[0]


def subtract(a, b):
    return a[0]-b[0], a[1]-b[1]


class ExactField:
    def __init__(self, data):
        self.nodes = [tuple(map(coordinate, point)) for point in data['nodes']]
        self.values = [Q(str(value)) for value in data.get('rational_values', data['values'])]
        self.grid = [sorted(set(point[axis] for point in self.nodes)) for axis in [0, 1]]
        self.triangles = []
        self.cells = {}
        self.strips = [{}, {}]
        self.initial = sorted((u, value) for (u, v), value in zip(self.nodes, self.values) if u == -v)
        self.initial_knots = [u for u, value in self.initial]
        assert self.initial[0] == (0, 0) and self.initial[-1] == (1, 1)
        assert all(0 <= value <= 1 for value in self.values)
        assert all(value == 0 for (u, v), value in zip(self.nodes, self.values) if v == 1)
        for indices in data['triangles']:
            points = [self.nodes[i] for i in indices]
            p, q, r = points
            e, f = subtract(q, p), subtract(r, p)
            determinant = cross(e, f)
            x, y, z = [self.values[i] for i in indices]
            ru = ((y-x)*f[1]-(z-x)*e[1])/determinant
            rv = (e[0]*(z-x)-f[0]*(y-x))/determinant
            assert ru >= 0 and rv <= 0
            coefficient = ru, rv, x-ru*p[0]-rv*p[1]
            number = len(self.triangles)
            self.triangles.append((points, coefficient, determinant > 0))
            ranges = []
            for axis in [0, 1]:
                left = bisect_left(self.grid[axis], min(p[axis] for p in points))
                right = bisect_left(self.grid[axis], max(p[axis] for p in points))
                ranges.append(range(left, right))
                for i in ranges[-1]:
                    self.strips[axis].setdefault(i, []).append(number)
            for i in ranges[0]:
                for j in ranges[1]:
                    self.cells.setdefault((i, j), []).append(number)

    def initial_value(self, z):
        i = max(0, min(len(self.initial)-2, bisect_right(self.initial_knots, z)-1))
        a, x = self.initial[i]; b, y = self.initial[i+1]
        return x+(z-a)*(y-x)/(b-a)

    def radial(self, u, v):
        if v > 1:
            return Q(0)
        cell = [max(0, min(len(self.grid[k])-2,
                           bisect_right(self.grid[k], p)-1)) for k, p in enumerate((u, v))]
        possible = set()
        for i in [cell[0], cell[0]-1]:
            for j in [cell[1], cell[1]-1]:
                possible.update(self.cells.get((i, j), []))
        point = u, v
        for number in sorted(possible):
            points, coefficient, positive = self.triangles[number]
            turns = [cross(subtract(b, a), subtract(point, a))
                     for a, b in zip(points, points[1:]+points[:1])]
            if (all(turn >= 0 for turn in turns) if positive else all(turn <= 0 for turn in turns)):
                a, b, c = coefficient
                return a*u+b*v+c
        raise ValueError(('No exact triangle', u, v))

    def integral(self, fixed, left, right, axis, threshold=None):
        """Integrate R, or (threshold-R)_+, along one characteristic row."""
        if right <= left:
            return Q(0)
        if (axis == 1 and fixed >= 1) or (axis == 0 and left >= 1):
            return max(Q(0), threshold)*(right-left) if threshold is not None else Q(0)
        if axis == 0 and right > 1:
            return (self.integral(fixed, left, Q(1), axis, threshold)
                    + (max(Q(0), threshold)*(right-1) if threshold is not None else 0))
        i = max(0, min(len(self.grid[axis])-2, bisect_right(self.grid[axis], fixed)-1))
        possible = set(self.strips[axis].get(i, [])) | set(self.strips[axis].get(i-1, []))
        cuts = {left, right}
        other = 1-axis
        for number in possible:
            points = self.triangles[number][0]
            for a, b in zip(points, points[1:]+points[:1]):
                if a[axis] == b[axis]:
                    if a[axis] == fixed:
                        cuts.update(x[other] for x in [a, b] if left < x[other] < right)
                elif min(a[axis], b[axis]) <= fixed <= max(a[axis], b[axis]):
                    value = a[other]+(fixed-a[axis])*(b[other]-a[other])/(b[axis]-a[axis])
                    if left < value < right:
                        cuts.add(value)
        total = Q(0)
        cuts = sorted(cuts)
        for a, b in zip(cuts, cuts[1:]):
            def value(x):
                return self.radial(fixed, x) if axis == 0 else self.radial(x, fixed)
            fa, fb = value(a), value(b)
            if threshold is not None:
                fa, fb = threshold-fa, threshold-fb
                if fa <= 0 and fb <= 0:
                    continue
                if fa*fb < 0:
                    width = (b-a)*(fa/(fa-fb) if fa > 0 else fb/(fb-fa))
                    total += width*max(fa, fb)/2
                    continue
            total += (b-a)*(fa+fb)/2
        return total

    def cdf_sides(self, time, position):
        r = self.radial(time+abs(position), time-abs(position))
        if position == 0:
            return (1-r)/2, (1+r)/2
        if position == 1:
            return (1+r)/2, Q(1)
        if position == -1:
            return Q(0), (1-r)/2
        value = (1+r)/2 if position > 0 else (1-r)/2
        return value, value

    def unit_route_payoff(self, route):
        """Independent exact first-moment actions, including contact atoms."""
        route = [tuple(map(Q, point)) for point in route]
        assert route[0][0] == 0
        lower, upper = self.cdf_sides(*route[0])
        cost = Q(0)
        for (start, x), (end, y) in zip(route, route[1:]):
            if end == start:
                assert x == y
                continue
            velocity = (y-x)/(end-start)
            assert abs(velocity) == 1 and max(abs(x), abs(y)) <= 1
            cuts = [start, end]
            if x*y < 0:
                cuts.insert(1, start-velocity*x)
            area = Q(0)
            for a, b in zip(cuts, cuts[1:]):
                xa, xb = x+velocity*(a-start), x+velocity*(b-start)
                sign = 1 if xa+xb > 0 else -1
                ua, va = a+abs(xa), a-abs(xa)
                ub, vb = b+abs(xb), b-abs(xb)
                record = upper if velocity == 1 else lower
                if velocity*sign == 1:
                    threshold = 2*record-1 if sign == 1 else 1-2*record
                    # (R-threshold)_+ = R-threshold+(threshold-R)_+.
                    area += (self.integral(va, ua, ub, 1)-threshold*(ub-ua)
                             + self.integral(va, ua, ub, 1, threshold))/4
                else:
                    threshold = 1-2*record if sign == -1 else 2*record-1
                    area += self.integral(ua, va, vb, 0, threshold)/4
            strict, closed = self.cdf_sides(end, y)
            if velocity == 1:
                updated = max(upper, closed)
                cost += end*(updated-upper)-area
                upper = updated
            else:
                updated = min(lower, strict)
                cost += end*(lower-updated)-area
                lower = updated
        assert lower == 0 and upper == 1, ('Incomplete route', lower, upper)
        return cost

    @lru_cache(maxsize=None)
    def negative_m1(self, z):
        a = self.initial_value(z)
        n = self.integral(z, -z, z, 0)
        h = self.integral(z, z, z+2, 1)
        return (n+4*z+8-2*(z+3)*a-h)/4

    @lru_cache(maxsize=None)
    def positive_m1(self, z):
        a = self.initial_value(z)
        column = self.integral(-z, z, 2-z, 1)
        return (8-4*z+(3-z)*a-column
                -self.integral(2-z, -z, Q(1), 0, a))/4

    def breakpoints(self, positive):
        knots = {Q(0), Q(1)} | set(self.initial_knots)
        knots.update(x for row in self.grid for x in row if 0 <= x <= 1)
        if not positive:
            return sorted(knots)
        knots.update(2-x for x in self.grid[0] if 1 <= x <= 2)
        for points, coefficient, _ in self.triangles:
            if min(p[0] for p in points) < 1 or max(p[0] for p in points) > 2:
                continue
            # The discovery mesh already includes 2 minus every initial
            # knot. Thus A(2-U)-R(U,V) is affine on this entire triangle.
            ulo, uhi = min(p[0] for p in points), max(p[0] for p in points)
            assert not any(ulo < 2-x < uhi for x in self.initial_knots)
            ru, rv, c = coefficient
            gaps = [self.initial_value(2-u)-ru*u-rv*v-c for u, v in points]
            for a, b, fa, fb in zip(points, points[1:]+points[:1], gaps, gaps[1:]+gaps[:1]):
                if fa*fb < 0:
                    u = a[0]-fa*(b[0]-a[0])/(fb-fa)
                    knots.add(2-u)
        return sorted(knots)


def minimize_quadratics(field, positive):
    function = field.positive_m1 if positive else field.negative_m1
    knots = field.breakpoints(positive)
    best = None
    for left, right in zip(knots, knots[1:]):
        f0, fm, f1 = function(left), function((left+right)/2), function(right)
        a = 2*(f1-2*fm+f0)
        b, c = f1-f0-a, f0
        # An extra exact value detects a missing arrangement breakpoint.
        assert function((3*left+right)/4) == a/16+b/4+c
        candidates = [(left, f0), (right, f1)]
        if a > 0 and 0 < -b/(2*a) < 1:
            y = -b/(2*a)
            z = left+(right-left)*y
            value = c-b*b/(4*a)
            assert function(z) == value
            candidates.append((z, value))
        for z, value in candidates:
            if best is None or value < best[1]:
                best = z, value
    z, value = best
    return dict(sign='positive' if positive else 'negative', cells=len(knots)-1,
                start=str(z if positive else -z), value=str(value), decimal=float(value))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('field', type=Path)
    parser.add_argument('--negative-only', action='store_true')
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    field = ExactField(json.loads(args.field.read_text()))
    result = dict(scope='Exact minimum over all signed M1 starting positions for this rational field only.',
                  input=str(args.field), families=[minimize_quadratics(field, False)])
    if not args.negative_only:
        result['families'].append(minimize_quadratics(field, True))
    if args.output:
        args.output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
