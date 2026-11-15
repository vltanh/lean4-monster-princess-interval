#!/usr/bin/env python3
"""Exact physical audit of a first-turn graph with diffuse second turns.

The reference integrates actual segment first captures over independent
rational polygons in (curve parameter, second turn).  It does not use
the proposed derivative or an inverse-capture formula for its scores.
"""
from collections import Counter
from fractions import Fraction as Q

from verify_double_corner_inward import initial, incoming, outgoing, ordinary
from verify_free_second_inward import direct_four, split_polygons
from verify_general_inward_adjoint import derivative, integrate
from verify_uniform_inward import twice_area


def physical_integral(path, left, right, density, degree):
    polygon = [(left, incoming(left)), (right, incoming(right)),
               (right, Q(1)), (left, Q(1))]
    lines = set()

    def add(fn):
        zero = fn(Q(0), Q(0))
        line = (fn(Q(1), Q(0))-zero, fn(Q(0), Q(1))-zero, zero)
        if line[0] or line[1]:
            lines.add(line)

    vertices = [lambda b, s: (Q(0), incoming(b)),
                lambda b, s: ((incoming(b)-initial(b))/2,
                              (incoming(b)+initial(b))/2),
                lambda b, s: ((s-initial(b))/2, (s+initial(b))/2),
                lambda b, s: (1+s, Q(-1)),
                lambda b, s: (3+s, Q(1))]
    for point in vertices:
        for tp, xp in path:
            add(lambda b, s, point=point, tp=tp: point(b, s)[0]-tp)
        for (tl, xl), (tr, xr) in zip(path, path[1:]):
            velocity = (xr-xl)/(tr-tl)
            intercept = xl-velocity*tl
            for sign in (Q(-1), Q(1)):
                add(lambda b, s, point=point, velocity=velocity,
                    intercept=intercept, sign=sign:
                    sign*point(b, s)[1]-velocity*point(b, s)[0]-intercept)
    for i, velocity in enumerate((Q(-1), Q(1), Q(-1), Q(1))):
        point = vertices[i]
        for tp, xp in path:
            for sign in (Q(-1), Q(1)):
                add(lambda b, s, point=point, velocity=velocity,
                    tp=tp, xp=xp, sign=sign:
                    sign*(point(b, s)[1]+velocity*(tp-point(b, s)[0]))-xp)

    total, cells = Q(0), 0
    for cell in split_polygons([polygon], lines):
        for j in range(1, len(cell)-1):
            tri = [cell[0], cell[j], cell[j+1]]
            jacobian = twice_area(tri)
            if not jacobian:
                continue
            origin, first, last = tri

            def outer(r):
                def inner(t):
                    b, s = (origin[k]+r*(first[k]-origin[k])
                            +t*(last[k]-origin[k]) for k in (0, 1))
                    return density(b, s)*direct_four(path, incoming(b), -initial(b), s)
                return integrate(inner, Q(0), 1-r, degree+1)

            total += jacobian*integrate(outer, Q(0), Q(1), degree+2)
            cells += 1
    return total, cells


def main():
    counts = Counter()
    left, right, step = Q(1, 8), Q(7, 8), Q(1, 100000)
    densities = [(lambda b, s: Q(1), 0),
                 (lambda b, s: 1+b+s, 1),
                 (lambda b, s: 1+b*b+s*s, 2)]
    for q in (Q(1, 3), Q(2, 3)):
        a, u, c = initial(q), incoming(q), outgoing(q)
        for density, degree in densities:
            cache = {}

            def score(level):
                if level not in cache:
                    path = ordinary(a, level, c)
                    cache[level] = physical_integral(path, left, right, density, degree)
                return cache[level][0]

            jump = (derivative(score, u, step, degree+4)
                    -derivative(score, u, -step, degree+4))
            expected = integrate(lambda s: (s-u+c+a)*density(q, s),
                                 u, Q(1), degree+1)/Q(57, 100)
            assert jump == expected > 0, (q, degree, jump, expected)
            counts["exact incoming-level derivative jumps"] += 1
            assert score(u-step)+score(u+step) > 2*score(u)
            counts["finite incoming-level midpoint gains"] += 1
            counts["complete physical two-dimensional integrals"] += len(cache)
            counts["independent physical capture triangles"] += sum(
                cells for _, cells in cache.values())
    print("PASS:", sum(counts.values()), "diffuse-second first-corner checks")
    for label, count in counts.items():
        print(" ", label+":", count)
    print("Scope: first-corner complementarity obstruction, not an equilibrium construction")


if __name__ == "__main__":
    main()
