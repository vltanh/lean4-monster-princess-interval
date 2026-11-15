#!/usr/bin/env python3
"""Exact singular double-corner contacts and independent physical variations.

The monster law is a one-dimensional curve, not an area density.  Every
integral below partitions its parameter using physical segment events
and evaluates actual first-capture times.  All arithmetic is rational.
The checks audit an obstruction; they do not construct an equilibrium.
"""
from collections import Counter
from fractions import Fraction as Q

from verify_general_inward_adjoint import derivative, integrate, path_from_graph
from verify_free_second_inward import direct_four, monster


def initial(q):
    return Q(2, 5)+Q(3, 5)*q


def incoming(q):
    return Q(43, 100)+Q(57, 100)*q


def outgoing(q):
    return -Q(1, 3)-Q(2, 3)*q


def sigma(b):
    return Q(1, 20)+Q(19, 20)*b


def later_rank(b):
    return Q(1, 10)+Q(9, 10)*b


def second(b):
    return incoming(later_rank(b))


def ordinary(a, u, c):
    assert Q(0) < a < u < 1 and -a < c < 0
    return path_from_graph(a, c, [(-a, a), (-a, u), (c, u)])


def curve(b):
    return incoming(b), -initial(b), second(b)


def kernel(q, b):
    a, u, c = initial(q), incoming(q), outgoing(q)
    start, _, s = curve(b)
    if q < b:
        return 2+3*s+c
    if q <= sigma(b):
        return 2+2*s+start-a
    if q <= later_rank(b):
        return 2+2*s+u-initial(b)
    return 8+4*s


def affine_root(fn, left, right):
    f0, f1 = fn(Q(0)), fn(Q(1))
    if f0 == f1:
        return None
    root = -f0/(f1-f0)
    return root if left < root < right else None


def curve_integral(path, left, right, density, degree):
    """Use all segment-endpoint and line-intersection order events.

    Both route vertices and their +/-1 line intercepts are affine in b.
    Thus between the resulting exact cuts the first-capture time is
    affine.  Neither the rank kernel nor its cutoff formulas is used.
    """
    cuts = {left, right}

    def add(fn):
        root = affine_root(fn, left, right)
        if root is not None:
            cuts.add(root)

    route0, route1 = monster(*curve(Q(0))), monster(*curve(Q(1, 2)))
    # At b=1 the first two legs degenerate, so construct the affine
    # vertices from values at 0 and 1/2 without deleting any endpoint.
    assert len(route0) == len(route1) == 5
    route_vertices = []
    for p0, ph in zip(route0, route1):
        route_vertices.append(lambda b, p0=p0, ph=ph:
                              tuple(p0[k]+2*b*(ph[k]-p0[k]) for k in (0, 1)))
    for point in route_vertices:
        for tp, xp in path:
            add(lambda b, point=point, tp=tp: point(b)[0]-tp)
        for (tl, xl), (tr, xr) in zip(path, path[1:]):
            velocity = (xr-xl)/(tr-tl)
            intercept = xl-velocity*tl
            for sign in (Q(-1), Q(1)):
                add(lambda b, point=point, velocity=velocity,
                    intercept=intercept, sign=sign:
                    sign*point(b)[1]-velocity*point(b)[0]-intercept)
    for i, velocity in enumerate((Q(-1), Q(1), Q(-1), Q(1))):
        point = route_vertices[i]
        for tp, xp in path:
            for sign in (Q(-1), Q(1)):
                add(lambda b, point=point, velocity=velocity,
                    tp=tp, xp=xp, sign=sign:
                    sign*(point(b)[1]+velocity*(tp-point(b)[0]))-xp)

    total, cells = Q(0), 0
    ordered = sorted(cuts)
    for left, right in zip(ordered, ordered[1:]):
        def capture(b):
            return direct_four(path, *curve(b))
        first = capture((3*left+right)/4)
        middle = capture((left+right)/2)
        last = capture((left+3*right)/4)
        assert first+last == 2*middle
        total += integrate(lambda b: density(b)*capture(b), left, right, degree+1)
        cells += 1
    return total, cells


def main():
    counts = Counter()
    for b in (Q(1, 8), Q(1, 4), Q(1, 2), Q(3, 4), Q(7, 8)):
        assert b < sigma(b) < later_rank(b) < 1
        assert initial(sigma(b)) == incoming(b)
        assert outgoing(later_rank(b)) == -initial(b)
        levels = sorted({Q(0), b, sigma(b), later_rank(b), Q(1)})
        for q in sorted(set(levels[1:-1]) | {
                (lo+hi)/2 for lo, hi in zip(levels, levels[1:])}):
            path = ordinary(initial(q), incoming(q), outgoing(q))
            assert direct_four(path, *curve(b)) == kernel(q, b)
            counts["closed rank-kernel contacts"] += 1

    left, right, step = Q(1, 8), Q(7, 8), Q(1, 100000)
    densities = [(lambda b: Q(1), 0), (lambda b: 1+b, 1),
                 (lambda b: 1+2*b*b, 2)]
    for q in (Q(1, 4), Q(1, 2), Q(3, 4)):
        a, u, c = initial(q), incoming(q), outgoing(q)
        bstar = (q-Q(1, 10))/Q(9, 10)
        assert left < bstar < q < right
        assert incoming(bstar) < a
        assert second(bstar) == u and initial(bstar) == -c
        first_gap = second(q)-u+c+a
        second_gap = 6+u-c
        assert first_gap > 0 and second_gap > 0
        for density, degree in densities:
            caches = {"c": {}, "u": {}}

            def score(axis, value):
                cache = caches[axis]
                if value not in cache:
                    path = ordinary(a, value if axis == "u" else u,
                                    value if axis == "c" else c)
                    cache[value] = curve_integral(path, left, right, density, degree)
                return cache[value][0]

            for axis, point, expected in (
                    ("c", c, second_gap*density(bstar)/Q(3, 5)),
                    ("u", u, first_gap*density(q)/Q(57, 100)
                     +second_gap*density(bstar)/Q(513, 1000))):
                evaluate = lambda value: score(axis, value)
                jump = (derivative(evaluate, point, step, degree+3)
                        -derivative(evaluate, point, -step, degree+3))
                assert jump == expected > 0, (axis, q, jump, expected)
                counts["exact "+axis+" derivative jumps"] += 1
                midpoint = evaluate(point-step)+evaluate(point+step)-2*evaluate(point)
                assert midpoint > 0
                counts["finite "+axis+" midpoint gains"] += 1
            counts["complete physical curve integrals"] += sum(len(ca) for ca in caches.values())
            counts["independent affine capture cells"] += sum(
                cells for ca in caches.values() for _, cells in ca.values())
    print("PASS:", sum(counts.values()), "singular double-corner checks")
    for label, count in counts.items():
        print(" ", label+":", count)
    print("Scope: exact singular-curve contacts and upper-response obstruction; no equilibrium")


if __name__ == "__main__":
    main()
