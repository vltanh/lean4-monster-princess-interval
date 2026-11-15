#!/usr/bin/env python3
"""Fraction replay of the curved initial-phase RLR exchange.

This is a local transport/record calculation, not an equilibrium or global
phase-existence certificate.  Running records are integrated directly on
the actual three unit-axis legs.  The fixtures include a strict non-rank-one
quadratic field, as well as bilinear and curved rank-one boundary cases.
"""
from dataclasses import dataclass
from fractions import Fraction as Q
from itertools import combinations
from math import isqrt
from pathlib import Path
import argparse
import json


def polynomial_value(poly, x):
    a, b, c = poly
    return (a*x+b)*x+c


def polynomial_integral(poly, a, b):
    c2, c1, c0 = poly
    return c2*(b**3-a**3)/3+c1*(b*b-a*a)/2+c0*(b-a)


def rational_sqrt(x):
    assert x >= 0
    a, b = isqrt(x.numerator), isqrt(x.denominator)
    assert a*a == x.numerator and b*b == x.denominator, x
    return Q(a, b)


def crossing(poly, cap, lo, hi):
    """Unique crossing of a monotone polynomial in these exact fixtures."""
    a, b, c = poly
    if not a:
        root = (cap-c)/b
    else:
        disc = rational_sqrt(b*b-4*a*(c-cap))
        roots = [(-b-disc)/(2*a), (-b+disc)/(2*a)]
        inside = [x for x in roots if lo <= x <= hi]
        assert len(inside) == 1, (poly, cap, lo, hi, roots)
        root = inside[0]
    assert lo <= root <= hi
    assert polynomial_value(poly, root) == cap
    return root


def clipped_integral(poly, lo, hi, cap, operation):
    assert operation in ('min', 'max')
    if lo == hi:
        return Q(0)
    flo, fhi = polynomial_value(poly, lo), polynomial_value(poly, hi)
    cuts = [lo, hi]
    if min(flo, fhi) < cap < max(flo, fhi):
        cuts.insert(1, crossing(poly, cap, lo, hi))
    result = Q(0)
    for a, b in zip(cuts, cuts[1:]):
        value = polynomial_value(poly, (a+b)/2)
        use_cap = value >= cap if operation == 'min' else value <= cap
        result += cap*(b-a) if use_cap else polynomial_integral(poly, a, b)
    return result


@dataclass(frozen=True)
class Patch:
    name: str
    p: Q
    q: Q
    r: Q
    s: Q
    k: Q
    scale: Q

    @property
    def constant(self):
        # F(1,1)=1/2; all rectangles stay in the positive open arena.
        return Q(1, 2)-self.scale*(self.p+self.q/2+self.r+self.s/2-self.k)

    def field(self, u, w):
        return (self.constant+self.scale*(self.p*u+self.q*u*u/2
                +self.r*u*w+self.s*u*u*w/2-self.k*w))

    def fu(self, u, w):
        return self.scale*(self.p+self.q*u+self.r*w+self.s*u*w)

    def horizontal(self, w):
        return (self.scale*(self.q+self.s*w)/2,
                self.scale*(self.p+self.r*w),
                self.constant-self.scale*self.k*w)

    def vertical(self, u):
        return (Q(0), self.scale*(self.r*u+self.s*u*u/2-self.k),
                self.constant+self.scale*(self.p*u+self.q*u*u/2))

    def verify_shape(self, u0, u1, w0, w1):
        assert min(self.p, self.q, self.r, self.s) >= 0
        assert self.p*self.s <= self.q*self.r
        assert self.fu(u0, w0) > 0
        assert self.k > self.r*u1+self.s*u1*u1/2
        assert 0 < self.field(u0, w1) <= self.field(u1, w0) < 1
        assert u0 >= w1 and u1-w0 < 2
        # The global logarithmic mixed derivative has numerator
        # p*s-q*r. The other three signs follow from these coefficients.


def physical_records(patch, path, low, high):
    """Direct chronological unit-axis record integration; no RLR formula."""
    cost = Q(0)
    for (u0, w0), (u1, w1) in zip(path, path[1:]):
        assert u1 >= u0 and w1 >= w0
        assert u0 == u1 or w0 == w1
        start = patch.field(u0, w0)
        assert low <= start <= high, (low, start, high, path)
        if w0 == w1:
            width = u1-u0
            upper = clipped_integral(patch.horizontal(w0), u0, u1, high, 'max')
            cost += ((low+1)*width-upper)/2
            high = max(high, patch.field(u1, w1))
        else:
            width = w1-w0
            lower = clipped_integral(patch.vertical(u0), w0, w1, low, 'min')
            cost += (lower+(1-high)*width)/2
            low = min(low, patch.field(u1, w1))
    return cost, low, 1-high


def suffix(index, low, right):
    if index == 0:
        return Q(0)
    if index == 1:
        return 2*min(low, Q(11, 20))+3*min(right, Q(3, 8))
    return min(3*low+right, low+3*right)


def peak_derivative(patch, u, low, high, u0, u1, w0, w1):
    """The theorem's derivative of twice-prefix cost in s=F(u,W0)."""
    f, g = patch.field(u, w0), patch.field(u, w1)
    assert f >= high and g <= low
    wp = w1 if g == low else crossing(patch.vertical(u), low, w0, w1)
    bottom = patch.fu(u, w0)
    ratio = patch.fu(u, w1)/bottom
    cprime = patch.scale*((patch.p+patch.q*u)*(w1-wp)
             +(patch.r+patch.s*u)*(w1*w1-wp*wp)/2)/bottom
    fend = patch.field(u1, w1)
    v = u1 if fend <= f else crossing(patch.horizontal(w1), f, u, u1)
    return ((low-g)/bottom+cprime+(u1-u)*(ratio-1)
            +u1-(w1-w0)-v)


def explicit_initial_guard(patch, alpha, a, z, e):
    """Evaluate the new L-coordinate formula separately from record evolution.

    Translate the patch by (U,W)->(U+1,W+1), so L(a,z)=F(2-a,z).
    All guards below start strictly inside the physical arena.
    """
    assert 0 < a < 1 and 0 <= alpha <= a <= z <= e <= 1
    assert alpha == 0 or e == 1
    f = patch.field(2-a,a)
    l = patch.field(2-a,z)
    k = max(f,patch.field(2-alpha,z))
    row = polynomial_integral(patch.vertical(2-a),a,z)
    c2,c1,c0 = patch.horizontal(z)
    # Substitute U=2-b into the horizontal polynomial.
    column_poly = (c2,-4*c2-c1,4*c2+2*c1+c0)
    column = clipped_integral(column_poly,alpha,a,f,'max')
    tail = clipped_integral(patch.vertical(2-alpha),z,e,l,'min')
    twice = (e-alpha+row-(z-a)*f+(a-alpha)*l-column+tail-(e-z)*k)
    return twice/2,min(l,patch.field(2-alpha,e)),1-k


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('output', type=Path)
    args = ap.parse_args()
    fixtures = [
        (Patch('bilinear_active_final_record', Q(1), Q(0), Q(1), Q(0),
               Q(3), Q(1, 50)), Q(5, 4), Q(3, 2)),
        (Patch('curved_rank_one', Q(0), Q(2), Q(0), Q(2),
               Q(16), Q(1, 100)), Q(5, 4), Q(7, 4)),
        (Patch('curved_strict_log_submodular', Q(1), Q(1), Q(1), Q(1, 2),
               Q(10), Q(1, 50)), Q(5, 4), Q(7, 4)),
    ]
    counts = {'global_polynomial_shape_checks': 0, 'direct_RLR_integrals': 0,
              'bilinear_closed_formula': 0, 'peak_derivative_monotonicity': 0,
              'exact_concavity_chords_with_suffix': 0,
              'unproductive_boundary_domination': 0,
              'endpoint_minimum_comparisons': 0,
              'explicit_initial_LRL_guards': 0,
              'guard_peak_below_initial_record': 0,
              'guard_peak_above_initial_record': 0}
    summaries = []
    u0, u1, w0, w1 = Q(1), Q(2), Q(1, 2), Q(1)
    for patch, left, right in fixtures:
        patch.verify_shape(u0, u1, w0, w1)
        counts['global_polynomial_shape_checks'] += 1
        low, high = patch.field(right, w1), patch.field(left, w0)
        assert low <= patch.field(u0, w0) <= high
        turns = [left+(right-left)*Q(i, 8) for i in range(9)]
        records, derivatives = [], []
        for u in turns:
            path = [(u0, w0), (u, w0), (u, w1), (u1, w1)]
            result = physical_records(patch, path, low, high)
            records.append(result)
            derivatives.append(peak_derivative(patch, u, low, high,
                                                u0, u1, w0, w1))
            counts['direct_RLR_integrals'] += 1
            if not patch.q and not patch.s:
                f, g = patch.field(u, w0), patch.field(u, w1)
                p, q = patch.fu(u, w0), patch.fu(u, w1)
                d, fend = w1-w0, patch.field(u1, w1)
                formula = ((u-u0)*(low-high)-(f-high)**2/(2*p)
                    +d*low-d*(low-g)**2/(2*(f-g))-d*f
                    +(u1-u)*(g-f)-max(fend-f, Q(0))**2/(2*q))
                assert formula == 2*result[0]-(u1-u0+w1-w0)
                counts['bilinear_closed_formula'] += 1
        for a, b in zip(derivatives, derivatives[1:]):
            assert a >= b
            counts['peak_derivative_monotonicity'] += 1
        for future in range(3):
            values = [cost+suffix(future, l, r) for cost, l, r in records]
            peaks = [patch.field(u, w0) for u in turns]
            for i, j, k in combinations(range(len(turns)), 3):
                theta = (peaks[j]-peaks[i])/(peaks[k]-peaks[i])
                assert values[j] >= (1-theta)*values[i]+theta*values[k]
                counts['exact_concavity_chords_with_suffix'] += 1
            lr = physical_records(patch, [(u0,w0),(u0,w1),(u1,w1)], low, high)
            rl = physical_records(patch, [(u0,w0),(u1,w0),(u1,w1)], low, high)
            assert lr[0]+suffix(future,lr[1],lr[2]) <= values[0]
            assert rl[0]+suffix(future,rl[1],rl[2]) <= values[-1]
            counts['unproductive_boundary_domination'] += 2
            for value in values:
                assert min(values[0], values[-1]) <= value
                counts['endpoint_minimum_comparisons'] += 1
        summaries.append({'name': patch.name,
                          'log_mixed_numerator': str(patch.p*patch.s-patch.q*patch.r),
                          'productive_turn_interval': [str(left),str(right)],
                          'entry_survivor_records': [str(low),str(1-high)]})
    guard_patch = fixtures[0][0]
    for alpha,a,z,e in (
        (Q(1,4),Q(1,2),Q(3,4),Q(1)),
        (Q(0),Q(1,2),Q(3,4),Q(7,8)),
        (Q(1,4),Q(1,2),Q(1),Q(1)),
        (Q(1,4),Q(1,2),Q(1,2),Q(1)),
        (Q(1,2),Q(1,2),Q(3,4),Q(1)),
        (Q(0),Q(1,2),Q(3,4),Q(3,4)),
    ):
        f = guard_patch.field(2-a,a)
        path = [(2-a,a),(2-a,z),(2-alpha,z),(2-alpha,e)]
        actual = physical_records(guard_patch,path,f,f)
        formula = explicit_initial_guard(guard_patch,alpha,a,z,e)
        assert actual == formula,(alpha,a,z,e,actual,formula)
        counts['explicit_initial_LRL_guards'] += 1
        peak = guard_patch.field(2-alpha,z)
        if peak < f:
            counts['guard_peak_below_initial_record'] += 1
        if peak > f:
            counts['guard_peak_above_initial_record'] += 1
    report = {'status':'PASS',
        'scope':'Exact local curvature/record-exchange checks; no equilibrium, global phase-existence, or unrestricted game-value claim.',
        'counts':counts,'fixtures':summaries}
    text = json.dumps(report, indent=2)+'\n'
    args.output.write_text(text)
    print(text,end='')


if __name__ == '__main__':
    main()
