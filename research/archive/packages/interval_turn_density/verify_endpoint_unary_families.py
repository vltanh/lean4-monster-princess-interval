#!/usr/bin/env python3
"""Independent physical checks of the complete paired-control unary family.

This verifies identities, positivity of mixed threshold differences, and
finite cut optima.  It is not a continuum response or game-value bound.
"""
from collections import Counter
from fractions import Fraction as Q
from itertools import product
import random

from endpoint_unary_families import ExtendedPairedEndpoint
from monotone_cut import maximize, chain_implications
from verify_endpoint_inward_adjoint import EndpointInward, physical_integral
from verify_general_inward_adjoint import physical_integral as fixed_integral
from verify_general_inward_adjoint import integrate
from verify_center_memory import first_capture
from verify_terminal_inward_c import split_integral


def route_m1(x):
    raw = [(Q(0), x), (1-x, Q(1)), (3-x, Q(-1))]
    return [p for i, p in enumerate(raw) if i == 0 or p != raw[i-1]]


def route_m2(x, s):
    raw = [(Q(0), x), ((s-x)/2, (s+x)/2),
           (s+1, Q(-1)), (s+3, Q(1))]
    return [p for i, p in enumerate(raw) if i == 0 or p != raw[i-1]]


def route_m3(x, s):
    assert abs(x) <= s < 1
    raw = [(Q(0), x), ((s-x)/2, (s+x)/2),
           ((s+1)/2, (s-1)/2), (Q(2), Q(1)), (Q(4), Q(-1))]
    return [p for i, p in enumerate(raw) if i == 0 or p != raw[i-1]]


def pair_four(path, route):
    times = [first_capture(path, route, sign) for sign in (1, -1)]
    assert None not in times
    return 2*sum(times, Q(0))


def physical(law, labels, path=None):
    path = law.path(labels) if path is None else path
    value, cells = physical_integral(path, law.density)
    for d in law.fixed_inward:
        extra, count = fixed_integral(path, d)
        value += extra
        cells += count
    for x, mass in law.m1_atoms:
        value += mass*pair_four(path, route_m1(x))
    for x, mass in law.fixed_m2_atoms:
        value += mass*pair_four(path, route_m2(x, Q(1)))
    for x, s, mass in law.late_m2_atoms:
        value += mass*pair_four(path, route_m2(x, s))
    for x, s, mass in law.early_m2_atoms:
        value += mass*pair_four(path, route_m2(x, s))
    for x, s, mass in law.early_m3_atoms:
        value += mass*pair_four(path, route_m3(x, s))
    # The physical start partition is obtained independently from the
    # actual path's characteristic vertices, not from feature labels.
    cuts = {Q(0), path[0][1], -path[0][1]}
    for t, p in path:
        u, v = t+p, t-p
        cuts.update((-u, -v, 2-u, 2-v))
    for left, right, coefficients in law.m1_polynomials:
        value += split_integral(
            lambda x: sum((c*x**k for k, c in enumerate(coefficients)), Q(0))
                      *pair_four(path, route_m1(x)),
            left, right, cuts, len(coefficients))
    for s, left, right, coefficients in law.m2_polynomials:
        value += split_integral(
            lambda x: sum((c*x**k for k, c in enumerate(coefficients)), Q(0))
                      *pair_four(path, route_m2(x, s)),
            left, right, cuts, len(coefficients))
    return value, cells


def regularized(law, labels, epsilon):
    """Joint pre-U1/post-U1 construction, not a capture-time formula."""
    path = law.path(labels)
    k = 1-epsilon
    split = next(j for j, (t, p) in enumerate(path) if t+p == 1)
    assert path[split][0]-path[split][1] == law.c
    result = [(k*t, k*p) for t, p in path[:split+1]]
    result.append(((1+epsilon+k*law.c)/2, (1+epsilon-k*law.c)/2))
    result.extend((epsilon+k*t, epsilon+k*p) for t, p in path[split+1:])
    clean = [p for j, p in enumerate(result) if j == 0 or p != result[j-1]]
    for (t, p), (s, q) in zip(clean, clean[1:]):
        assert s > t and abs(q-p) <= s-t and 0 <= p <= 1 and 0 <= q <= 1
    return clean


def interpolate(values, point):
    result = Q(0)
    for j, value in enumerate(values, 1):
        weight = Q(1)
        for k in range(1, len(values)+1):
            if k != j:
                weight *= Q(point-k, j-k)
        result += weight*value
    return result


def main():
    counts = Counter()
    fixtures = [
        (Q(1, 2), Q(-1, 4),
         [Q(-1, 2), Q(-3, 8), Q(-1, 4)],
         [Q(1), Q(5, 4), Q(3, 2), Q(13, 8), Q(7, 4)],
         [Q(1, 2), Q(13, 20), Q(4, 5), Q(19, 20)],
         [Q(-1, 4), Q(0), Q(1, 2), Q(1), Q(5, 4)]),
        (Q(1, 4), Q(3, 4),
         [Q(-1, 4), Q(0), Q(1, 2), Q(3, 4)],
         [Q(1), Q(5, 4), Q(7, 4), Q(2), Q(5, 2), Q(11, 4)],
         [Q(1, 4), Q(1, 2), Q(4, 5), Q(19, 20)],
         [Q(3, 4), Q(1), Q(5, 4), Q(2)])]
    for a, c, pe, se, pl, zl in fixtures:
        law = ExtendedPairedEndpoint(
            EndpointInward({(0, 0): Q(1, 5), (1, 0): Q(1, 7), (0, 2): Q(1, 9)}),
            a, c, pe, se, pl, zl,
            m1_atoms=[(Q(-1), Q(1, 5)), (a, Q(1, 11)), (-a, Q(1, 19))],
            fixed_m2_atoms=[(-c, Q(1, 59)), (a, Q(1, 61)), (-a, Q(1, 67))],
            early_m2_atoms=[(Q(1, 3), Q(3, 4), Q(1, 71)),
                            (Q(-1, 4), Q(1, 2), Q(1, 73)),
                            (Q(-1, 2), Q(13, 20), Q(1, 79)),
                            (a, Q(4, 5), Q(1, 83)),
                            (-a, Q(4, 5), Q(1, 89))],
            early_m3_atoms=[(Q(1, 8), Q(13, 20), Q(1, 97)),
                            (Q(-1, 4), Q(4, 5), Q(1, 101)),
                            (Q(-1, 2), Q(13, 20), Q(1, 103)),
                            (a, Q(4, 5), Q(1, 107)),
                            (-a, Q(4, 5), Q(1, 109))],
            fixed_inward=[EndpointInward({(0, 0): Q(1, 13), (1, 0): Q(1, 17)})],
            late_m2_atoms=[(Q(-3, 4), Q(5, 2), Q(1, 23)),
                           (Q(-1, 4), Q(7, 4), Q(1, 29)),
                           (Q(1, 4), Q(3, 2), Q(1, 31)),
                           (Q(3, 5), Q(5, 4), Q(1, 37)),
                           (Q(-1, 2), Q(5, 2), Q(1, 41)),
                           (Q(3, 4), Q(5, 4), Q(1, 43))],
            m1_polynomials=[(Q(-1), Q(0), (Q(1, 5), Q(1, 5))),
                            (Q(0), Q(1), (Q(0), Q(0), Q(3, 10)))],
            m2_polynomials=[(Q(1), Q(-1), Q(0), (Q(1, 100),)),
                            (Q(1), Q(0), Q(1), (Q(0), Q(1, 50))),
                            (Q(5, 4), Q(-1), Q(3, 4), (Q(1, 47), Q(1, 94))),
                            (Q(2), Q(-1), Q(0), (Q(1, 53),)),
                            (Q(13, 20), Q(-3, 5), Q(3, 5), (Q(1, 113),))])
        tables = law.tables()
        unaries, pairs, bounds, constant = tables
        # Exact physical fixtures have no U=1 plateau: first Z=c.
        c_label = law.w_levels.index(-c)
        physical_bounds = list(bounds)
        physical_bounds[law.npre] = (c_label, c_label)
        implications = (chain_implications(range(law.npre), len(pl), True)
                        +chain_implications(range(law.npre, law.npre+law.npost),
                                            len(zl), False))
        answer = maximize(unaries, pairs, implications, physical_bounds)
        feasible = []
        for labels in product(*(range(lo, hi+1) for lo, hi in physical_bounds)):
            pre, post = labels[:law.npre], labels[law.npre:]
            if any(x > y for x, y in zip(pre, pre[1:])):
                continue
            if any(x < y for x, y in zip(post, post[1:])):
                continue
            feasible.append(labels)
        best = max(law.reward(labels, tables) for labels in feasible)
        assert answer.score+constant == best
        counts["exhaustive finite feasible controls"] += len(feasible)
        counts["global finite cut optima"] += 1
        chosen = {answer.labels}
        chosen.update(random.Random(1267).sample(feasible, min(7, len(feasible))))
        for labels in sorted(chosen):
            actual, cells = physical(law, labels)
            expected = law.reward(labels, tables)
            assert actual == expected, (a, c, labels, actual, expected, actual-expected)
            counts["absolute full-law physical scores"] += 1
            counts["independent physical capture triangles"] += cells
            if c > a:
                counts["positive-c physical clipping checks"] += 1
        # A true U=1 incoming plateau has a different I1 early branch.
        # Move it to 1+epsilon and independently extrapolate its physical
        # polynomial scores.  Atomic beta(1) can improve the limit.
        prefix = tuple(lo for lo, hi in bounds[:law.npre])
        z = Q(1, 2) if c < 0 else Q(1)
        labels = prefix+(law.w_levels.index(-z),)*law.npost
        target = law.reward(labels, tables)
        values = []
        for j in range(1, 8):
            actual, cells = physical(law, labels, regularized(law, labels, Q(j, 100000)))
            values.append(actual)
            counts["joint-epsilon physical scores"] += 1
            counts["independent physical capture triangles"] += cells
        assert interpolate(values[:6], 7) == values[6]
        assert interpolate(values[:6], 0) >= target
        counts["exact joint-epsilon polynomial limits"] += 1
        assert law.total_mass > 0
    print("PASS:", sum(counts.values()), "extended paired-law checks")
    for label, count in counts.items():
        print(" ", label+":", count)
    print("Scope: actual density/atomic features and complete finite-control optimization")
    print("No continuum error bound, new game-value bound, or equilibrium is asserted")


if __name__ == "__main__":
    main()
