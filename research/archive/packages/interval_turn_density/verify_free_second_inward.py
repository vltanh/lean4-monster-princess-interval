#!/usr/bin/env python3
"""Exact free-second-I contacts and a moving-surface response obstruction.

All reported checks use Fraction arithmetic.  Surface integrals are taken
over an independent polygonal partition and evaluated by actual physical
segment intersection.  This is a structural audit, not an equilibrium fit.
"""
from collections import Counter
from fractions import Fraction as Q

from verify_general_inward_adjoint import integrate, derivative, path_from_graph
from verify_uniform_inward import clip, twice_area, inverse, paths
from verify_center_memory import first_capture


def monster(z, v, s):
    assert 0 < z <= s <= 1 and -z <= v < z
    raw = [(Q(0), z), ((z+v)/2, (z-v)/2),
           ((s+v)/2, (s-v)/2), (1+s, Q(-1)), (3+s, Q(1))]
    result = []
    for point in raw:
        if not result or point != result[-1]:
            result.append(point)
    return result


def direct_four(path, z, v, s):
    route = monster(z, v, s)
    captures = [first_capture(path, route, sign) for sign in (1, -1)]
    assert None not in captures
    return 2*sum(captures, Q(0))


def inverse_four(path, z, v, s):
    b = path[0][1]
    beta_s = inverse(path, s, False)
    if b <= z:
        alpha_z = inverse(path, z, True)
        positive = alpha_z if 2*alpha_z-z <= v else inverse(path, s, True)
    else:
        beta_v = inverse(path, v, False)
        positive = beta_v if 2*beta_v-v <= s else inverse(path, s+2, False)
    return 2*(positive+beta_s)


def split_polygons(polygons, lines):
    original = sum((twice_area(p) for p in polygons), Q(0))
    for line in sorted(lines):
        refined = []
        for polygon in polygons:
            values = [line[0]*z+line[1]*v+line[2] for z, v in polygon]
            if min(values) < 0 < max(values):
                for positive in (False, True):
                    cell = clip(polygon, line, positive)
                    if len(cell) >= 3 and twice_area(cell):
                        refined.append(cell)
            else:
                refined.append(polygon)
        polygons = refined
    assert sum((twice_area(p) for p in polygons), Q(0)) == original
    return polygons


def surface_integral(path, left, right, intercept, slope, density, degree):
    """S(v)=intercept+slope*v; support -v<z<S(v), left<v<right."""
    def second(v):
        return intercept+slope*v
    polygon = [(-left, left), (second(left), left),
               (second(right), right), (-right, right)]
    lines = {(Q(1), Q(0), -path[0][1])}
    for t, x in path:
        u, v = t+x, t-x
        lines.add((Q(1), Q(0), -u))
        lines.add((Q(0), Q(1), -v))
        lines.add((Q(0), slope, intercept-u))
    for (ta, xa), (tb, xb) in zip(path, path[1:]):
        velocity = (xb-xa)/(tb-ta)
        offset = xa-velocity*ta
        # Equality with the first inward turn.
        lines.add((1-velocity, -1-velocity, -2*offset))
        # Equality with the moving second turn.
        lines.add((Q(0), (1-velocity)*slope-1-velocity,
                   (1-velocity)*intercept-2*offset))
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
                    s = second(v)
                    return density(z, v)*direct_four(path, z, v, s)
                return integrate(inner, Q(0), 1-r, degree+1)

            total += jacobian*integrate(outer, Q(0), Q(1), degree+2)
            cells += 1
    return total, cells


def main():
    counts = Counter()
    for path in paths():
        b = path[0][1]
        starts = sorted({Q(1, 5), Q(1, 2), Q(4, 5), *([b] if 0 < b < 1 else [])})
        for z in starts:
            for turn_fraction in (Q(0), Q(1, 4), Q(1, 2), Q(3, 4)):
                v = -z+2*z*turn_fraction
                for second_fraction in (Q(0), Q(1, 3), Q(2, 3), Q(1)):
                    s = z+(1-z)*second_fraction
                    assert direct_four(path, z, v, s) == inverse_four(path, z, v, s)
                    counts["exact free-second first contacts"] += 1

    a, u, c0 = Q(3, 4), Q(9, 10), Q(-1, 2)
    left, right, slope = Q(-3, 5), Q(-2, 5), Q(-1, 8)
    intercept = u-slope*c0
    densities = [(lambda z, v: Q(1), 0),
                 (lambda z, v: 1+z+v*v, 2)]
    step = Q(1, 10000)
    for curved_initial in (False, True):
        def graph(c):
            if curved_initial:
                return [(-a, a), (Q(-7, 10), Q(4, 5)),
                        (Q(-13, 20), u), (c, u)]
            return [(-a, a), (-a, u), (c, u)]

        for density, degree in densities:
            cache = {}
            def score(c):
                if c not in cache:
                    path = path_from_graph(a, c, graph(c))
                    cache[c] = surface_integral(path, left, right, intercept,
                                               slope, density, degree)
                return cache[c][0]

            right_derivative = derivative(score, c0, step, degree+5)
            left_derivative = derivative(score, c0, -step, degree+5)
            column = integrate(lambda z: density(z, c0), -c0, a, degree)
            expected_jump = (u+6-c0)*column
            assert right_derivative-left_derivative == expected_jump > 0
            counts["exact upward derivative jumps"] += 1
            counts["physical surface integrals"] += len(cache)
            counts["independent surface capture cells"] += sum(c for _, c in cache.values())
            # The midpoint inequality is already a finite, physical
            # improving c variation for the surface component itself.
            assert score(c0-step)+score(c0+step) > 2*score(c0)
            counts["strict finite midpoint gaps"] += 1
    print("PASS:", sum(counts.values()), "free-second inward checks")
    for label, count in counts.items():
        print(" ", label+":", count)
    print("Scope: first contacts and a surface/cap incompatibility; no matched strategy")


if __name__ == "__main__":
    main()
