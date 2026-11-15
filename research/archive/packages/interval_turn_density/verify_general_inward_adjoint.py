#!/usr/bin/env python3
"""Exact first variations for an arbitrary initial-inward density.

The fixtures use nonnegative bivariate polynomial densities on the full
physical triangle or its negative-turn half.  Their four-score is checked
against direct physical segment capture, integrated over an independent
rational polygon partition.  The a/c variations are then checked by exact
polynomial differentiation, including initial and terminal connector terms.

This verifies identities.  It does not construct a matched equilibrium.
"""
from __future__ import annotations

from collections import Counter
from fractions import Fraction as Q
from functools import lru_cache
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/"interval_turn_sheet"))
from verify_uniform_inward import arrangements, direct_four, twice_area


def multiply(p, q):
    out = [Q(0)]*(len(p)+len(q)-1)
    for i, x in enumerate(p):
        for j, y in enumerate(q):
            out[i+j] += x*y
    return out


@lru_cache(None)
def integration_weights(n):
    """Interpolatory quadrature at n strictly interior rational nodes."""
    nodes = tuple(Q(j+1, n+1) for j in range(n))
    weights = []
    for j, x in enumerate(nodes):
        polynomial, denominator = [Q(1)], Q(1)
        for k, y in enumerate(nodes):
            if j != k:
                polynomial = multiply(polynomial, [-y, Q(1)])
                denominator *= x-y
        weights.append(sum((v/Q(k+1) for k, v in enumerate(polynomial)), Q(0))/denominator)
    return nodes, tuple(weights)


def integrate(fn, left, right, degree=8):
    if right <= left:
        return Q(0)
    nodes, weights = integration_weights(degree+1)
    return (right-left)*sum((w*fn(left+(right-left)*t)
                             for t, w in zip(nodes, weights)), Q(0))


@lru_cache(None)
def differentiation_weights(n):
    """Derivative at zero of the polynomial through nodes 0,...,n-1."""
    weights = []
    for j in range(n):
        polynomial, denominator = [Q(1)], Q(1)
        for k in range(n):
            if j != k:
                polynomial = multiply(polynomial, [Q(-k), Q(1)])
                denominator *= j-k
        weights.append(polynomial[1]/denominator)
    return tuple(weights)


def derivative(fn, point, step, degree=8):
    return sum((w*fn(point+j*step) for j, w in
                enumerate(differentiation_weights(degree+1))), Q(0))/step


class PolynomialInward:
    """A nonnegative polynomial i(a,v), restricted to -a<v<top(a)."""

    def __init__(self, terms, negative_only=False):
        self.terms = dict(terms)
        self.negative_only = negative_only
        self.degree = max(sum(ij) for ij in self.terms)
        self.mass = integrate(self.row_mass, Q(0), Q(1), self.degree+2)

    def density(self, a, v):
        return sum((coefficient*a**i*v**j
                    for (i, j), coefficient in self.terms.items()), Q(0))

    def top(self, a):
        return Q(0) if self.negative_only else a

    def row_mass(self, a):
        return integrate(lambda v: self.density(a, v), -a, self.top(a), self.degree)

    def row_tail(self, a, v):
        return integrate(lambda s: self.density(a, s), v, self.top(a), self.degree)

    def column(self, b, v):
        assert -b <= v < 0
        return integrate(lambda a: self.density(a, v), -v, b, self.degree)

    def integrand(self, b, c, v, u):
        return (self.column(b, v)*(v+u-8)
                - integrate(lambda a: self.row_tail(a, v)
                            +(1+c-a-v)*self.density(a, v),
                            b, u, self.degree+1))

    def gradient(self, b, c, v, u):
        return (self.column(b, v)-self.row_tail(u, v)
                -(1+c-u-v)*self.density(u, v))

    def feature(self, b, c, graph):
        below = integrate(self.row_mass, Q(0), b, self.degree+2)
        constant = (4*self.mass+(1+c)*(self.mass-below)+8*below
                    +integrate(lambda a: (a-1)*self.row_tail(a, c),
                               b, Q(1), self.degree+2))
        return constant+graph_integral(graph, lambda v, u: self.integrand(b, c, v, u),
                                       self.degree+3)


def graph_integral(graph, function, degree=8):
    total = Q(0)
    for (vl, ul), (vr, ur) in zip(graph, graph[1:]):
        if vl < vr:
            slope = (ur-ul)/(vr-vl)
            total += integrate(lambda v: function(v, ul+slope*(v-vl)),
                               vl, vr, degree)
    return total


def make_graph(b, c, breaks, slopes, intercepts):
    """Clamp a fixed monotone affine function below by the changing b."""
    cuts = {-b, c}
    cuts.update(v for v in breaks if -b < v < c)
    for slope, intercept in zip(slopes, intercepts):
        if slope:
            root = (b-intercept)/slope
            if -b < root < c:
                cuts.add(root)
    cuts = sorted(cuts)

    def value(v, side=0):
        index = sum(v > knot or (v == knot and side > 0) for knot in breaks)
        return max(b, slopes[index]*v+intercepts[index])

    graph = [(-b, b)]
    for left, right in zip(cuts, cuts[1:]):
        for point in [(left, value(left, 1)), (right, value(right, -1))]:
            if point != graph[-1]:
                graph.append(point)
    for (vl, ul), (vr, ur) in zip(graph, graph[1:]):
        assert vl <= vr and b <= ul <= ur < 1 and ul >= vl
    return graph


def path_from_graph(b, c, graph):
    vertices = [((u+v)/2, (u-v)/2) for v, u in graph]
    vertices += [((1+c)/2, (1-c)/2), (1+c, Q(1)), (Q(8), Q(1))]
    clean = []
    for point in vertices:
        if not clean or point != clean[-1]:
            clean.append(point)
    assert clean[0] == (Q(0), b)
    return clean


def physical_integral(path, density):
    """Independent polygonal integration of actual first-capture times."""
    result, cells = Q(0), 0
    top = Q(0) if density.negative_only else None
    for polygon in arrangements(path, Q(0), Q(1), top=top):
        for j in range(1, len(polygon)-1):
            triangle = [polygon[0], polygon[j], polygon[j+1]]
            jacobian = twice_area(triangle)
            if not jacobian:
                continue
            origin, first, second = triangle

            def outer(s):
                def inner(t):
                    a, v = (origin[k]+s*(first[k]-origin[k])
                            +t*(second[k]-origin[k]) for k in (0, 1))
                    assert -a < v < density.top(a)
                    return density.density(a, v)*direct_four(path, a, v)
                return integrate(inner, Q(0), 1-s, density.degree+1)

            result += jacobian*integrate(outer, Q(0), Q(1), density.degree+2)
            cells += 1
    return result, cells


def missed_mass(density, b, u, graph):
    """Initial inward legs which miss, for starts b<a<u."""
    result = Q(0)
    for (vl, ul), (vr, ur) in zip(graph, graph[1:]):
        if ul < ur:
            def integrand(a):
                psi = vl+(vr-vl)*(a-ul)/(ur-ul)
                return integrate(lambda v: density.density(a, v), -a, psi, density.degree)
            result += integrate(integrand, ul, ur, density.degree+1)
    assert graph[0][1] == b and graph[-1][1] == u
    return result


def a_variation(density, b, c, graph):
    u0 = next(u for v, u in graph[1:] if v >= -b)
    if graph[1][0] > -b:
        u0 = b
    return (graph_integral(graph, lambda v, u: (u+v)*density.density(b, v), density.degree+1)
            +8*density.row_tail(b, c)+density.integrand(b, c, -b, u0))


def c_variation(density, b, c, graph):
    u = graph[-1][1]
    mass_above_u = integrate(density.row_mass, u, Q(1), density.degree+2)
    missed = missed_mass(density, b, u, graph)
    edge = integrate(lambda a: (1-a)*density.density(a, c), u, Q(1), density.degree+1)
    early_jump = (c+u-8)*density.column(b, c)
    return mass_above_u+missed+edge+early_jump, edge


def main():
    counts = Counter()
    polynomials = [
        {(0, 0): Q(1)},
        {(0, 0): Q(1), (1, 0): Q(2), (0, 1): Q(1)},
        {(0, 0): Q(1), (2, 0): Q(1), (1, 1): Q(2), (0, 2): Q(1)},
    ]
    # The first two curves have no initial outward connector.  The third
    # has one, so its a derivative needs the displayed boundary correction.
    fixtures = [
        (Q(3, 5), Q(-1, 5), [], [Q(1, 2)], [Q(9, 10)]),
        (Q(4, 5), Q(-2, 5), [Q(-3, 5)],
         [Q(1, 4), Q(1, 2)], [Q(1), Q(23, 20)]),
        (Q(1, 2), Q(-1, 4), [], [Q(1, 4)], [Q(7, 8)]),
    ]
    step = Q(1, 10000)
    for negative_only in (False, True):
        for terms in polynomials:
            density = PolynomialInward(terms, negative_only)
            for b, c, breaks, slopes, intercepts in fixtures:
                graph = make_graph(b, c, breaks, slopes, intercepts)
                path = path_from_graph(b, c, graph)
                feature = density.feature(b, c, graph)
                actual, cells = physical_integral(path, density)
                assert feature == actual, (negative_only, terms, graph, feature, actual)
                counts["physical two-dimensional density integrals"] += 1
                counts["independent capture cells"] += cells

                def vary_a(a):
                    return density.feature(a, c, make_graph(a, c, breaks, slopes, intercepts))

                expected_a = a_variation(density, b, c, graph)
                for direction in (step, -step):
                    computed = derivative(vary_a, b, direction, density.degree+5)
                    assert computed == expected_a, ("a", graph, computed, expected_a)
                    counts["exact initial-coordinate variations"] += 1

                def vary_c(last):
                    return density.feature(b, last, make_graph(b, last, breaks, slopes, intercepts))

                expected_c, edge = c_variation(density, b, c, graph)
                for direction in (step, -step):
                    computed = derivative(vary_c, c, direction, density.degree+5)
                    assert computed == expected_c, ("c", graph, computed, expected_c)
                    assert computed != expected_c-edge
                    counts["exact last-characteristic variations"] += 1
                    counts["nonzero terminal edge corrections"] += 1

                v = (-b+c)/2
                u = (b+1)/2
                computed = derivative(lambda value: density.integrand(b, c, v, value),
                                      u, step, density.degree+3)
                assert computed == density.gradient(b, c, v, u)
                counts["exact inverse-gradient identities"] += 1
    print("PASS:", sum(counts.values()), "general initial-inward adjoint checks")
    for label, count in counts.items():
        print(" ", label+":", count)
    print("Scope: exact response identities and their boundary terms; no matched law or value claim")


if __name__ == "__main__":
    main()
