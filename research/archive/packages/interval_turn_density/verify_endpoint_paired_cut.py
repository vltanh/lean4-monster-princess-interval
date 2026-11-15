#!/usr/bin/env python3
"""Physical endpoint-law features versus a globally solved finite cut.

The fixed control arrangement includes V>1 and uses reflected beta
prices explicitly.  It is not a continuum discretization certificate.
"""
from collections import Counter
from fractions import Fraction as Q
from itertools import product
import random

from endpoint_paired_controls import PairedEndpoint
from verify_endpoint_inward_adjoint import EndpointInward, physical_integral
from verify_center_memory import first_capture

from monotone_cut import maximize, chain_implications


def physical(law, labels):
    path = law.path(labels)
    value, cells = physical_integral(path, law.density)
    for parameter, mass in law.m1_atoms:
        route = [(Q(0), parameter), (1-parameter, Q(1)), (3-parameter, Q(-1))]
        route = [point for i, point in enumerate(route) if i == 0 or point != route[i-1]]
        captures = [first_capture(path, route, sign) for sign in (1, -1)]
        assert None not in captures
        value += 2*mass*sum(captures, Q(0))
    return value, cells


def main():
    counts = Counter()
    a, c = Q(1, 2), Q(-1, 4)
    pre_edges = [-a, Q(-3, 8), c]
    post_edges = [Q(1), Q(5, 4), Q(3, 2), Q(13, 8), Q(7, 4)]
    p_levels = [a, Q(13, 20), Q(4, 5), Q(19, 20)]
    z_levels = [c, Q(0), Q(1, 2), Q(1), Q(5, 4)]
    m1 = [(Q(-1), Q(1, 5)), (Q(1, 3), Q(1, 7)),
          (Q(-3, 4), Q(1, 6)), (Q(2, 3), Q(1, 8))]
    densities = [{(0, 0): Q(1)},
                 {(0, 0): Q(1), (1, 0): Q(1), (0, 2): Q(1)}]
    for terms in densities:
        law = PairedEndpoint(EndpointInward(terms), a, c, pre_edges, post_edges,
                             p_levels, z_levels, m1)
        tables = law.tables()
        unaries, pairs, bounds, constant = tables
        implications = (chain_implications(range(law.npre), len(p_levels), increasing=True)
                        +chain_implications(range(law.npre, law.npre+law.npost),
                                            len(z_levels), increasing=False))
        result = maximize(unaries, pairs, implications, bounds)
        feasible = []
        for labels in product(*(range(lo, hi+1) for lo, hi in bounds)):
            pre, post = labels[:law.npre], labels[law.npre:]
            if any(x > y for x, y in zip(pre, pre[1:])):
                continue
            if any(x < y for x, y in zip(post, post[1:])):
                continue
            feasible.append(labels)
        best = max(law.reward(labels, tables) for labels in feasible)
        assert result.score+constant == best
        assert law.reward(result.labels, tables) == best
        counts["exhaustively compared finite feasible paths"] += len(feasible)
        counts["global finite cut optima"] += 1

        anchor = (0,)*law.npre+(len(z_levels)-1,)*law.npost
        anchor_value, cells = physical(law, anchor)
        offset = anchor_value-law.reward(anchor, tables)
        counts["complete physical score checks"] += 1
        counts["independent physical capture triangles"] += cells
        chosen = {anchor, result.labels}
        chosen.add(next(labels for labels in feasible if labels[-1] == 0))
        chosen.update(random.Random(3817).sample(feasible, 10))
        for labels in sorted(chosen-{anchor}):
            actual, cells = physical(law, labels)
            expected = offset+law.reward(labels, tables)
            assert actual == expected, (terms, labels, actual, expected)
            counts["complete physical score checks"] += 1
            counts["independent physical capture triangles"] += cells
            if max(v for t, p in law.path(labels) if (v := t-p) <= law.L) > 1:
                counts["physical checks retaining V above one"] += 1
        total_mass = law.density.mass+sum((mass for _, mass in m1), Q(0))
        assert total_mass > 0
        normalized_score = (offset+best)/(4*total_mass)
        print("Finite-control optimum (normalized physical law):", normalized_score)
        print("  controls:", result.labels, "mass:", total_mass)
    print("PASS:", sum(counts.values()), "paired endpoint-cut checks")
    for label, count in counts.items():
        print(" ", label+":", count)
    print("Scope: exact physical features and global optimum of one fixed finite arrangement")
    print("No continuum error bound, game-value bound, or equilibrium is asserted")


if __name__ == "__main__":
    main()
