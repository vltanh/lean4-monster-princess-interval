#!/usr/bin/env python3
"""Exact endpoint-I score and first-crossing derivative for two waves."""
from collections import Counter
from fractions import Fraction as Q

from verify_endpoint_inward_adjoint import EndpointInward, physical_integral
from verify_general_inward_adjoint import derivative, integrate, path_from_graph
from verify_terminal_inward_c import split_integral
from verify_uniform_inward import inverse


def two_wave(a, u1, c, u2, y):
    assert a < u1 < 1 < u2 < 2+c and -a < c < y < 0
    graph = [(-a, a), (-a, u1), (c, u1), (c, u2), (y, u2)]
    return [((u+v)/2, (u-v)/2) for v, u in graph]+[
        (1+y, Q(1)), (Q(8), Q(1))]


def missed_after(density, a, u1, c, u2):
    # The first inverse below U=1 is -a up to u1 and c above it.
    threshold = u2-2
    cuts = {a, u1, Q(1), -threshold}
    def row(z):
        psi = -a if z <= u1 else c
        return integrate(lambda v: density.density(z, v),
                         max(-z, threshold), psi, density.degree)
    return split_integral(row, a, Q(1), cuts, density.degree+2)


def correction(density, a, u1, c, u2, y):
    alpha = missed_after(density, a, u1, c, u2)
    beta = integrate(lambda v: (2+v-u2)*density.column(a, v),
                     c, y, density.degree+2)
    return (y-c)*alpha-beta


def main():
    counts = Counter()
    a, u1, c, y = Q(7, 10), Q(17, 20), Q(-2, 5), Q(-1, 10)
    step = Q(1, 10000)
    polynomials = [{(0, 0): Q(1)},
                   {(0, 0): Q(1), (1, 0): Q(1), (0, 2): Q(1)}]
    for terms in polynomials:
        density = EndpointInward(terms)
        for u2 in (Q(11, 10), Q(27, 20), Q(3, 2)):
            graph = [(-a, a), (-a, u1), (c, u1)]
            baseline = density.feature(a, c, graph)
            expected = baseline+correction(density, a, u1, c, u2, y)
            actual, cells = physical_integral(two_wave(a, u1, c, u2, y), density)
            assert actual == expected, (terms, u2, actual, expected)
            counts["complete physical two-wave integrals"] += 1
            counts["independent physical capture triangles"] += cells

            _, pieces = density.c_variation(a, c, graph)
            q_pre = pieces[0]
            alpha = missed_after(density, a, u1, c, u2)
            edge = integrate(lambda z: (2+y-z)*density.density(z, c),
                              u1, Q(1), density.degree+1)
            target = q_pre-alpha+edge-(u2-u1)*density.column(a, c)
            assert q_pre-alpha >= 0
            for direction in (step, -step):
                def vary(first):
                    first_graph = [(-a, a), (-a, u1), (first, u1)]
                    return (density.feature(a, first, first_graph)
                            +correction(density, a, u1, first, u2, y))
                computed = derivative(vary, c, direction, density.degree+5)
                assert computed == target
                counts["exact first-crossing derivatives"] += 1

            # The physical diagonal can make the alpha source INCREASE;
            # its curvature must not be assigned the old Chebyshev sign.
            def score(level):
                return baseline+correction(density, a, u1, c, level, y)
            second = derivative(lambda level: derivative(
                score, level, step, density.degree+5), u2, step, density.degree+4)
            def alpha_source(level):
                v = level-2
                lower = -v if v < -a else u1
                return integrate(lambda z: density.density(z, v),
                                 lower, Q(1), density.degree)
            source_derivative = derivative(alpha_source, u2, step, density.degree+2)
            assert second == -(y-c)*source_derivative
            if u2 < 2-a:
                assert second < 0
                counts["strictly concave interior-turn fixtures"] += 1
            counts["exact source-curvature identities"] += 1
    print("PASS:", sum(counts.values()), "endpoint-I two-wave checks")
    for label, count in counts.items():
        print(" ", label+":", count)
    print("Scope: exact two-wave features and prices, not a global response theorem")


if __name__ == "__main__":
    main()
