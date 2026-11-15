#!/usr/bin/env python3
"""Exact contacts and a/c/field variations for endpoint-second inward rows.

The reference is physical first segment capture over independently
partitioned rational polygons.  This is an identity audit, not a game
value calculation or a claimed matching law.
"""
from collections import Counter
from fractions import Fraction as Q

from verify_general_inward_adjoint import (
    PolynomialInward, derivative, graph_integral, integrate,
    make_graph, missed_mass, path_from_graph,
)
from verify_center_memory import first_capture
from verify_free_second_inward import split_polygons
from verify_uniform_inward import inverse, paths, twice_area


def monster(z, v):
    assert 0 < z <= 1 and -z <= v < z
    raw = [(Q(0), z), ((z+v)/2, (z-v)/2),
           (1+v, Q(1)), (3+v, Q(-1))]
    clean = []
    for point in raw:
        if not clean or point != clean[-1]:
            clean.append(point)
    return clean


def direct_four(path, z, v):
    route = monster(z, v)
    captures = [first_capture(path, route, sign) for sign in (1, -1)]
    assert None not in captures
    return 2*sum(captures, Q(0))


def inverse_four(path, z, v):
    a = path[0][1]
    if a <= z:
        alpha = inverse(path, z, True)
        positive = alpha if 2*alpha-z <= v else inverse(path, 2+v, True)
    else:
        positive = inverse(path, v, False)
    return 2*(positive+inverse(path, 2+v, False))


class EndpointInward(PolynomialInward):
    def column(self, a, v):
        return integrate(lambda z: self.density(z, v), abs(v), a, self.degree)

    def integrand(self, a, c, v, u):
        return ((u-v-2)*self.column(a, v)
                -integrate(lambda z: self.row_tail(z, v)
                           +(2+c-z)*self.density(z, v),
                           a, u, self.degree+1))

    def gradient(self, a, c, v, u):
        return (self.column(a, v)-self.row_tail(u, v)
                -(2+c-u)*self.density(u, v))

    def feature(self, a, c, graph):
        reflected = integrate(lambda z: integrate(
            lambda v: (6+2*v)*self.density(z, v),
            -z, z, self.degree+1), Q(0), Q(1), self.degree+2)
        below = integrate(lambda z: integrate(
            lambda v: (2+2*v)*self.density(z, v),
            -z, z, self.degree+1), Q(0), a, self.degree+2)
        above = integrate(lambda z: integrate(
            lambda v: (2+v+c)*self.density(z, v),
            -z, c, self.degree+1)+(z+c)*self.row_tail(z, c),
            a, Q(1), self.degree+2)
        return reflected+below+above+graph_integral(
            graph, lambda v, u: self.integrand(a, c, v, u), self.degree+3)

    def a_variation(self, a, c, graph):
        u0 = graph[1][1] if graph[1][0] == -a else a
        return (graph_integral(graph, lambda v, u: (v+u)*self.density(a, v),
                               self.degree+1)
                +integrate(lambda v: (2+2*v)*self.density(a, v),
                           c, a, self.degree+1)
                +self.integrand(a, c, -a, u0))

    def c_variation(self, a, c, graph):
        u = graph[-1][1]
        positive_mass = (integrate(self.row_mass, u, Q(1), self.degree+2)
                         +missed_mass(self, a, u, graph))
        positive_edge = integrate(lambda z: (2+c-z)*self.density(z, c),
                                  u, Q(1), self.degree+1)
        negative_edge = -(2+c-u)*self.column(a, c)
        return positive_mass+positive_edge+negative_edge, (positive_mass, positive_edge, negative_edge)


def physical_integral(path, density):
    polygon = [(Q(0), Q(0)), (Q(1), Q(-1)), (Q(1), Q(1))]
    lines = set()

    def add(fn):
        zero = fn(Q(0), Q(0))
        line = (fn(Q(1), Q(0))-zero, fn(Q(0), Q(1))-zero, zero)
        if line[0] or line[1]:
            lines.add(line)

    vertices = [lambda z, v: (Q(0), z),
                lambda z, v: ((z+v)/2, (z-v)/2),
                lambda z, v: (1+v, Q(1)),
                lambda z, v: (3+v, Q(-1))]
    for point in vertices:
        for tp, xp in path:
            add(lambda z, v, point=point, tp=tp: point(z, v)[0]-tp)
        for (tl, xl), (tr, xr) in zip(path, path[1:]):
            velocity = (xr-xl)/(tr-tl)
            intercept = xl-velocity*tl
            for sign in (Q(-1), Q(1)):
                add(lambda z, v, point=point, velocity=velocity,
                    intercept=intercept, sign=sign:
                    sign*point(z, v)[1]-velocity*point(z, v)[0]-intercept)
    for j, velocity in enumerate((Q(-1), Q(1), Q(-1))):
        point = vertices[j]
        for tp, xp in path:
            for sign in (Q(-1), Q(1)):
                add(lambda z, v, point=point, velocity=velocity,
                    tp=tp, xp=xp, sign=sign:
                    sign*(point(z, v)[1]+velocity*(tp-point(z, v)[0]))-xp)

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
                    z, v = (origin[k]+r*(first[k]-origin[k])
                            +t*(last[k]-origin[k]) for k in (0, 1))
                    return density.density(z, v)*direct_four(path, z, v)
                return integrate(inner, Q(0), 1-r, density.degree+1)

            total += jacobian*integrate(outer, Q(0), Q(1), density.degree+2)
            cells += 1
    return total, cells


def main():
    counts = Counter()
    for path in paths():
        starts = {Q(1, 5), Q(1, 2), Q(4, 5)}
        if 0 < path[0][1] < 1:
            starts.add(path[0][1])
        for z in sorted(starts):
            for fraction in (Q(0), Q(1, 4), Q(1, 2), Q(3, 4)):
                v = -z+2*z*fraction
                assert direct_four(path, z, v) == inverse_four(path, z, v)
                counts["closed endpoint-I first contacts"] += 1

    polynomials = [{(0, 0): Q(1)},
                   {(0, 0): Q(1), (1, 0): Q(2), (0, 1): Q(1)},
                   {(0, 0): Q(1), (2, 0): Q(1), (0, 2): Q(1)}]
    fixtures = [
        (Q(3, 5), Q(-1, 5), [], [Q(1, 2)], [Q(9, 10)]),
        (Q(4, 5), Q(-2, 5), [Q(-3, 5)],
         [Q(1, 4), Q(1, 2)], [Q(1), Q(23, 20)]),
        (Q(1, 2), Q(-1, 4), [], [Q(1, 4)], [Q(7, 8)]),
    ]
    step = Q(1, 10000)
    for terms in polynomials:
        density = EndpointInward(terms)
        for a, c, breaks, slopes, intercepts in fixtures:
            graph = make_graph(a, c, breaks, slopes, intercepts)
            path = path_from_graph(a, c, graph)
            feature = density.feature(a, c, graph)
            actual, cells = physical_integral(path, density)
            assert feature == actual, (terms, graph, feature, actual)
            counts["complete physical endpoint-I integrals"] += 1
            counts["independent physical capture triangles"] += cells
            expected_a = density.a_variation(a, c, graph)
            expected_c, pieces = density.c_variation(a, c, graph)
            for direction in (step, -step):
                da = derivative(lambda start: density.feature(start, c,
                    make_graph(start, c, breaks, slopes, intercepts)), a, direction, density.degree+5)
                dc = derivative(lambda last: density.feature(a, last,
                    make_graph(a, last, breaks, slopes, intercepts)), c, direction, density.degree+5)
                assert da == expected_a, ("a", terms, graph, da, expected_a)
                assert dc == expected_c, ("c", terms, graph, dc, expected_c, pieces)
                counts["exact initial-coordinate derivatives"] += 1
                counts["exact final-characteristic derivatives"] += 1
            for v in (-a+(c+a)/3, -a+2*(c+a)/3):
                u = (a+Q(1))/2
                numerical = derivative(lambda level: density.integrand(a, c, v, level),
                                       u, step, density.degree+3)
                assert numerical == density.gradient(a, c, v, u)
                counts["exact local inverse Euler derivatives"] += 1
    print("PASS:", sum(counts.values()), "endpoint-inward adjoint checks")
    for label, count in counts.items():
        print(" ", label+":", count)
    print("Scope: exact endpoint-I contacts and adjoint identities, not a matched law")


if __name__ == "__main__":
    main()
