#!/usr/bin/env python3
"""Exact chronological fixtures for the continuum E/S/P_b payoff formulas.

The physical oracle intersects actual Princess and Monster segments and
integrates over a complete start-coordinate arrangement. No potential
values, HJB constraints, optimizer output, or residual-repair code is used.
All calculations use only the Python standard library and Fraction arithmetic.
"""
from __future__ import annotations

import argparse
from fractions import Fraction as Q
import json
from pathlib import Path
from random import Random

if __package__:
    from .verify_continuum_functional import complete, functional, physical_integral
    from .verify_domain import Path as PhysicalPath, direct_first_hit
    from .verify_finite_princess import general_attacks
else:
    from verify_continuum_functional import complete, functional, physical_integral
    from verify_domain import Path as PhysicalPath, direct_first_hit
    from verify_finite_princess import general_attacks


def endpoint_family_integral(path, lo, hi):
    """Integrate physical S(a) captures over a uniform density bin."""
    lines, _ = general_attacks([path])
    cuts = {lo, hi}
    # The S family is the physical endpoint-first face b=2-a.
    for A, B, C in lines:
        if A != B:
            a = Q(C-2*B, A-B)
            if lo < a < hi:
                cuts.add(a)
    total = Q(0)
    cuts = sorted(cuts)
    for left, right in zip(cuts, cuts[1:]):
        a = (left+right)/2
        route = PhysicalPath.make([(0, a), (1-a, 1), (3-a, -1), (6, -1)])
        total += (right-left)*(direct_first_hit(route, path)
                              + direct_first_hit(route, path.reflected()))/2
    return total/(hi-lo)


def endpoint_family_formula(path, lo, hi):
    """Independently integrate G_S and its time-two terminal term."""
    def cdf(z):
        return max(Q(0), min(Q(1), (z-lo)/(hi-lo)))

    r, s = path.nodes[0][1], path.at(2)
    cuts = {Q(0), Q(2)}
    for (t0, x0), (t1, x1) in zip(path.nodes, path.nodes[1:]):
        if t0 >= 2:
            break
        t1 = min(t1, Q(2))
        x1 = path.at(t1)
        cuts.update((t0, t1))
        for sign in (-1, 1):
            a, b = t0+sign*x0, t1+sign*x1
            assert a < b
            for level in (-lo, -hi, 2-lo, 2-hi, 2-r):
                if a < level < b:
                    cuts.add(t0+(t1-t0)*(level-a)/(b-a))
    total = Q(0)
    cuts = sorted(cuts)
    for left, right in zip(cuts, cuts[1:]):
        t = (left+right)/2
        p = path.at(t)
        U, W = t+p, t-p
        running = (cdf(-U)+cdf(-W)+max(Q(0), cdf(2-U)-cdf(r))
                   + cdf(2-W)-cdf(-r))
        total += (right-left)*running
    a, b = max(-r, lo), min(s, hi)
    if b > a:
        total += ((b-b*b/2)-(a-a*a/2))/(hi-lo)
    return total/2


def run():
    seed = 170319
    rng = Random(seed)
    paths = [complete([(0, r), (2, r)])
             for r in (Q(1, 8), Q(1, 2), Q(7, 8), Q(15, 16))]
    for _ in range(30):
        radius = Q(rng.randrange(1, 16), 16)
        nodes = [(Q(0), radius)]
        for j in range(1, 5):
            options = [radius+Q(k, 16) for k in range(-5, 6)
                       if 0 < radius+Q(k, 16) < 1]
            radius = rng.choice(options)
            nodes.append((Q(j, 2), radius))
        paths.append(complete(nodes))

    P = S = E = above = equal = late = 0
    for index, path in enumerate(paths):
        for b in (Q(1, 4), Q(1, 2), Q(7, 8), Q(31, 32), Q(1),
                  Q(17, 16), Q(7, 4)):
            lo, hi = -min(b, Q(1)), min(b, 2-b, Q(1))
            k = index % 5
            interval = (lo+(hi-lo)*Q(k, 8), lo+(hi-lo)*Q(k+3, 8))
            actual = physical_integral(path, b, interval)
            expected = functional(path, b, interval)
            assert actual == expected, (path.nodes, b, interval, actual, expected)
            P += 1
            above += path.nodes[0][1] > b
            equal += path.nodes[0][1] == b
            late += 2-path.at(2) < b

        for lo, hi in ((Q(-1), Q(1)), (Q(-7, 8), Q(-1, 8)),
                       (Q(-1, 4), Q(3, 4)), (Q(1, 8), Q(15, 16))):
            actual = endpoint_family_integral(path, lo, hi)
            expected = endpoint_family_formula(path, lo, hi)
            assert actual == expected, (path.nodes, lo, hi, actual, expected)
            S += 1

        endpoint = PhysicalPath.make([(0, -1), (2, 1), (6, 1)])
        actual = (direct_first_hit(endpoint, path)
                  + direct_first_hit(endpoint, path.reflected()))/2
        expected = Q(0)
        for sign in (-1, 1):
            for (t0, x0), (t1, x1) in zip(path.nodes, path.nodes[1:]):
                a, b = t0+sign*x0, t1+sign*x1
                if a <= 1 <= b:
                    expected += (t0+(t1-t0)*(1-a)/(b-a))/2
                    break
        assert actual == expected, (path.nodes, actual, expected)
        E += 1

    return {
        'status': 'PASS',
        'scope': 'exact chronological E/S/P_b payoff-formula fixtures; independent of the potential checker',
        'arithmetic': 'Fraction throughout',
        'deterministic_seed': seed,
        'radial_princess_paths': len(paths),
        'P_density_bin_fixtures': P,
        'S_density_bin_fixtures': S,
        'endpoint_fixtures': E,
        'initial_radius_above_turn_level': above,
        'initial_radius_equal_turn_level': equal,
        'late_W_terminal_fixtures': late,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, help='write the deterministic replay JSON')
    args = parser.parse_args()
    report = run()
    rendered = json.dumps(report, indent=2)+'\n'
    if args.output:
        args.output.write_text(rendered)
    print(rendered, end='', flush=True)


if __name__ == '__main__':
    main()
