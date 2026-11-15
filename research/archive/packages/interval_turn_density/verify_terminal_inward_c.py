#!/usr/bin/env python3
"""Exact final-characteristic variations for free-second inward laws.

Fixed second-turn slices suffice to check the linear measure identity.
The payoff reference integrates physical first captures on independent
polygons.  Both unrestricted slices (including both edge terms) and
slices with an empty first-turn edge are included.
"""
from collections import Counter
from fractions import Fraction as Q

from verify_free_second_inward import surface_integral
from verify_general_inward_adjoint import derivative, integrate, path_from_graph
from verify_uniform_inward import inverse


def split_integral(fn, left, right, cuts, degree):
    points = sorted({left, right, *(z for z in cuts if left < z < right)})
    return sum((integrate(fn, lo, hi, degree) for lo, hi in zip(points, points[1:])), Q(0))


def expected(path, a, u, c, s, left, right, density, degree):
    if s < u:
        return Q(0), (Q(0),)*3
    assert s > u
    cuts = {-left, -right, -c, a, u, s}
    cuts.update(t+x for t, x in path)
    cuts.update(2*inverse(path, v, False)-v for v in (left, right))

    def row(z, upper=Q(2)):
        return integrate(lambda v: density(z, v), max(-z, left),
                         min(right, upper), degree)

    whole = split_integral(lambda z: row(z), u, s, cuts, degree+2)

    def missed(z):
        psi = 2*inverse(path, z, True)-z
        return row(z, psi)

    early = split_integral(missed, a, min(u, s), cuts, degree+2)
    positive_edge = negative_edge = Q(0)
    if left < c < right:
        positive_edge = integrate(lambda z: (s-z)*density(z, c),
                                  max(u, -c), s, degree+1)
        negative_edge = integrate(lambda z: (c+u-2*s-6)*density(z, c),
                                  -c, min(a, s), degree+1)
    return whole+early+positive_edge+negative_edge, (whole+early, positive_edge, negative_edge)


def main():
    counts = Counter()
    a, u, c, step = Q(7, 10), Q(17, 20), Q(-2, 5), Q(1, 10000)
    densities = [(lambda z, v: Q(1), 0),
                 (lambda z, v: 1+z+v*v, 2)]
    fixtures = [(Q(19, 20), -Q(19, 20), Q(0)),
                (Q(4, 5), -Q(4, 5), Q(0)),
                (Q(19, 20), -Q(3, 5), -Q(1, 2)),
                (Q(19, 20), -Q(17, 20), -Q(4, 5))]
    for curved in (0, 1, 2):
        def graph(last):
            if curved == 2:
                return [(-a, a), (-Q(13, 20), Q(3, 4)),
                        (last, Q(101, 100)+Q(2, 5)*last)]
            if curved == 1:
                return [(-a, a), (-Q(13, 20), Q(3, 4)),
                        (-Q(1, 2), u), (last, u)]
            return [(-a, a), (-a, u), (last, u)]

        for s, left, right in fixtures:
            for density, degree in densities:
                cache = {}

                def score(last):
                    if last not in cache:
                        path = path_from_graph(a, last, graph(last))
                        cache[last] = surface_integral(path, left, right, s,
                                                      Q(0), density, degree)
                    return cache[last][0]

                path = path_from_graph(a, c, graph(c))
                target, pieces = expected(path, a, u, c, s, left, right, density, degree)
                for direction in (step, -step):
                    actual = derivative(score, c, direction, degree+5)
                    assert actual == target, (curved, s, left, degree, actual, target, pieces)
                    counts["exact final-characteristic derivatives"] += 1
                if not (left < c < right):
                    assert pieces[1] == pieces[2] == 0
                    assert target >= 0
                    counts["nonnegative edge-free mass identities"] += 1
                counts["complete physical slice integrals"] += len(cache)
                counts["independent physical capture triangles"] += sum(
                    cells for _, cells in cache.values())
    print("PASS:", sum(counts.values()), "terminal inward c-variation checks")
    for label, count in counts.items():
        print(" ", label+":", count)
    print("Scope: the exact c-variation and its edge signs; support deletion uses the separate theorem")


if __name__ == "__main__":
    main()
