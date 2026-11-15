#!/usr/bin/env python3
"""Exact continuous-start audit for M2 whose first turn is U=1.

This is a supplied-field response audit, not an unrestricted game
certificate. Reconstructed after the 2026-11-11 executor outage. An
independent V8 BigInt implementation reproduced every minimum and checked
238 physical first-capture identities on the frozen field during the
outage. The reconstructed Python source itself has not been rerun.
"""
import argparse
from fractions import Fraction as Q
from functools import lru_cache
import json
from pathlib import Path
from audit_m1 import ExactField

PACKAGE = Path(__file__).resolve().parent


@lru_cache(maxsize=None)
def positive(field, a):
    a = Q(a)
    A = field.initial_value(a)
    return (12+2*A-(7+a)*field.radial(Q(1), -a)
            -field.integral(-a, a, Q(1), 1)
            -field.integral(Q(1), -a, Q(1), 0, A))/4


@lru_cache(maxsize=None)
def negative(field, a):
    a = Q(a)
    A = field.initial_value(a)
    return (field.integral(a, -a, a, 0)+12-4*A
            -(7-a)*field.radial(Q(1), a)
            -field.integral(a, a, Q(1), 1))/4


def fixed_one_route(x):
    x = Q(x)
    return [(Q(0), x), ((1-x)/2, (1+x)/2),
            (Q(2), -Q(1)), (Q(4), Q(1))]


def early_m3_route(a, s):
    a, s = Q(a), Q(s)
    assert 0 <= a <= s <= 1
    return [(Q(0), -a), ((s+a)/2, (s-a)/2), ((s+1)/2, (s-1)/2),
            (Q(2), Q(1)), (Q(4), -Q(1))]


def negative_early_m3(field, a, s):
    a, s = Q(a), Q(s)
    assert 0 <= a <= s <= 1
    A = field.initial_value(a)
    N = field.integral(a, -a, a, 0)
    B = field.radial(s, a)
    D = field.radial(Q(1), s)
    I = field.integral(a, a, s, 1)
    # Keep the positive part: the center row can lie below A.
    G = (field.integral(s, s, Q(1), 1)-(1-s)*A
         +field.integral(s, s, Q(1), 1, A))
    return (N+12-8*A+(s+a-4)*B-(7-s)*max(Q(0), D-A)-I-G)/4


def breakpoints(field, is_positive):
    cuts = {Q(0), Q(1)} | set(field.initial_knots)
    cuts.update(x for row in field.grid for x in row if 0 <= x <= 1)
    if is_positive:
        levels = {field.radial(Q(1), v) for v in field.grid[1]}
        for (a, x), (b, y) in zip(field.initial, field.initial[1:]):
            if x == y:
                continue
            for r in levels:
                if x < r < y:
                    cuts.add(a+(r-x)*(b-a)/(y-x))
    return sorted(cuts)


def minimize(field, is_positive):
    function = positive if is_positive else negative
    cuts = breakpoints(field, is_positive)
    best = None
    captures = 0
    for left, right in zip(cuts, cuts[1:]):
        f0 = function(field, left)
        fm = function(field, (left+right)/2)
        f1 = function(field, right)
        qa = 2*(f1-2*fm+f0)
        qb = f1-f0-qa
        assert function(field, (3*left+right)/4) == f0+qb/4+qa/16
        candidates = [(left, f0), (right, f1)]
        if qa > 0 and 0 < -qb/(2*qa) < 1:
            y = -qb/(2*qa)
            point = left+(right-left)*y
            value = f0-qb*qb/(4*qa)
            assert function(field, point) == value
            candidates.append((point, value))
        for point, value in candidates:
            if best is None or value < best[1]:
                best = point, value
        for j in (1, 2):
            point = left+(right-left)*Q(j, 3)
            x = point if is_positive else -point
            assert field.unit_route_payoff(fixed_one_route(x)) == function(field, point)
            captures += 1
    a, value = best
    start = a if is_positive else -a
    assert field.unit_route_payoff(fixed_one_route(start)) == value
    reference = field.positive_m1(Q(1))
    return dict(sign='positive' if is_positive else 'negative',
                cells=len(cuts)-1, start=str(start), absolute_start=str(a),
                value=str(value), decimal=float(value),
                gap=str(value-reference), gap_decimal=float(value-reference),
                quadratic_checks=len(cuts)-1, capture_checks=captures)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--field', type=Path,
        default=PACKAGE/'snapshots/endpoint_joint_i1_field.json')
    parser.add_argument('--output', type=Path,
        default=PACKAGE/'snapshots/endpoint_joint_i1_fixed_one_audit.json')
    args = parser.parse_args()
    field = ExactField(json.loads(args.field.read_text()))
    families = [minimize(field, True), minimize(field, False)]
    source_checks = 0
    for a in (Q(1, 32), Q(3, 5), Q(3, 4)):
        for s in (max(a, Q(13, 16)), max(a, Q(273, 320)),
                  max(a, Q(7, 8)), Q(1)):
            assert negative_early_m3(field, a, s) == field.unit_route_payoff(early_m3_route(a, s))
            source_checks += 1
    a, s = Q(1, 32), Q(273, 320)
    cost = negative_early_m3(field, a, s)
    reference = field.positive_m1(Q(1))
    report = dict(
        scope='Exact continuous-start fixed-U=1 M2 audit and early-M3 witness; no unrestricted guarantee.',
        source=args.field.name, endpoint_reference=str(reference), families=families,
        m3_source_checks=source_checks,
        m3_witness=dict(a=str(a), s=str(s), cost=str(cost), decimal=float(cost),
                        gap=str(cost-reference)))
    args.output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
