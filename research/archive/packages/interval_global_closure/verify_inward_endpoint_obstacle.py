#!/usr/bin/env python3
"""Exact physical replay of the inward-valley / positive-endpoint row.

The chronological first-contact oracle is independent of the new moment
formula.  Endpoint atoms are mixed explicitly into a uniform radial law,
so the initial-endpoint trace jump and actual endpoint deactivation are
tested rather than inferred from a continuous initial distribution.
"""
from fractions import Fraction as Q
from pathlib import Path
import argparse
import json

from verify_bulk_contact_equations import cdf, integral, physical_score


def route(a, z):
    d = (z-a)/2
    return [(Q(0), 1-a), (d, 1-(a+z)/2),
            (z, Q(1)), (z+2, Q(-1))]


def endpoint_score(path):
    answer = Q(0)
    for endpoint in (Q(-1), Q(1)):
        hits = []
        for (s, x), (t, y) in zip(path, path[1:]):
            if x == endpoint:
                hits.append(s)
            if t > s and x != y:
                hit = s+(endpoint-x)*(t-s)/(y-x)
                if s <= hit <= t:
                    hits.append(hit)
        assert hits, (endpoint, path)
        answer += min(hits)/2
    return answer


def mixed_cdf(t, x, T, p):
    if x > 1:
        return Q(1)
    if x < -1:
        return Q(0)
    # At either endpoint this is its interior trace, as required by all
    # positive-duration integrals and by the limiting initial record.
    return p/2+(1-p)*cdf(t, x, T)


def mixed_integral(T, p, start, end, v, offset, cap=None):
    """Integrate the mixed field on a line, with an optional upper cap."""
    cuts = {start, end}
    if v:
        for endpoint in (Q(-1), Q(1)):
            hit = (endpoint-offset)/v
            if start < hit < end:
                cuts.add(hit)
    cuts = sorted(cuts)
    answer = Q(0)
    for a, b in zip(cuts, cuts[1:]):
        x = v*(a+b)/2+offset
        if x > 1 or x < -1 or p == 1:
            value = Q(1) if x > 1 else Q(0) if x < -1 else Q(1, 2)
            answer += (value if cap is None else min(value, cap))*(b-a)
        else:
            transformed = None if cap is None else (cap-p/2)/(1-p)
            answer += p*(b-a)/2+(1-p)*integral(
                T, a, b, v, offset, transformed)
    return answer


def max_integral(T, p, start, end, v, offset, floor):
    return (mixed_integral(T, p, start, end, v, offset)
            +floor*(end-start)
            -mixed_integral(T, p, start, end, v, offset, floor))


def moments(a, z, T, p, actual_initial_endpoint=False):
    d = (z-a)/2
    f = mixed_cdf(Q(0), 1-a, T, p)
    if actual_initial_endpoint and a == 0:
        f = Q(1)
    l = mixed_cdf(d, 1-(a+z)/2, T, p)
    row = mixed_integral(T, p, Q(0), d, Q(-1), 1-a)
    column = max_integral(T, p, d, z/2, Q(1), 1-z, f)
    outer = max_integral(T, p, z/2, z, Q(1), 1-z, f)
    moment = mixed_integral(T, p, Q(0), z+2, Q(-1), 1+z, l)
    return z+moment+row-column-outer-d*(f+l)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('output', type=Path)
    args = ap.parse_args()
    counts = {'physical_rows': 0, 'initial_endpoint_trace_jumps': 0,
              'endpoint_first_boundary': 0, 'lower_obstacle_chords': 0}
    branches = 0
    for T in (Q(0), Q(1), Q(2)):
        for p in (Q(0), Q(1, 3), Q(1)):
            for z in (Q(1, 4), Q(1, 2), Q(3, 4)):
                for a in (Q(0), z/2, z):
                    path = route(a, z)
                    value, n = physical_score(path, T)
                    branches += n
                    actual = (1-p)*value+p*endpoint_score(path)
                    formula = moments(a, z, T, p, True)
                    assert actual == formula, (T, p, a, z, actual, formula)
                    counts['physical_rows'] += 1
                    if a == 0:
                        trace = moments(a, z, T, p)
                        phi0 = mixed_cdf(Q(0), Q(1), T, p)
                        assert trace-actual == z*(1-phi0)
                        counts['initial_endpoint_trace_jumps'] += 1
                    if a == z:
                        direct = [(Q(0), 1-z), (z, Q(1)), (z+2, Q(-1))]
                        value, _ = physical_score(direct, T)
                        direct_value = (1-p)*value+p*endpoint_score(direct)
                        assert direct_value == actual
                        counts['endpoint_first_boundary'] += 1
                    # This is an independent chord check of the full
                    # H_{1+z} moment, including its exterior contribution.
                    for lo, hi in ((Q(0), Q(1, 4)),
                                   (Q(1, 4), Q(3, 4)),
                                   (Q(3, 4), Q(1))):
                        hlo = mixed_integral(T, p, Q(0), z+2,
                                             Q(-1), 1+z, lo)
                        hhi = mixed_integral(T, p, Q(0), z+2,
                                             Q(-1), 1+z, hi)
                        d = (z-a)/2
                        assert hhi-hlo-d*(hi-lo) >= (z+a)*(hi-lo)/2
                        counts['lower_obstacle_chords'] += 1
    report = {
        'status': 'PASS',
        'scope': 'Exact inward-valley/endpoint cost and trace identities; no family sufficiency or equilibrium claim.',
        'princess_family': 'Uniform initial radius, stationary until T in {0,1,2}, then outward/sticky, mixed with stationary endpoint-pair mass p in {0,1/3,1}.',
        'counts': counts,
        'physical_affine_contact_branches': branches,
    }
    text = json.dumps(report, indent=2)+'\n'
    args.output.write_text(text)
    print(text, end='')


if __name__ == '__main__':
    main()
