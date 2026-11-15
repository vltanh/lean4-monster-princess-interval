#!/usr/bin/env python3
"""Exact full-CDF costs for two interior monster turns, for either start sign.

The radial paths, CDF integrals, and direct first intersections are supplied
by the independent Fraction fixtures in verify_positive_cdf_sheet. No
continuum candidate or unrestricted lower bound is asserted here.
"""
from collections import Counter
from fractions import Fraction as Q

from verify_positive_cdf_sheet import (Law, Path, finite_fixtures, first_capture,
                                      direct_cost, four_cost)


def route(start, s, t):
    return [(Q(0), start), ((s-start)/2, (s+start)/2),
            ((s+t)/2, (s-t)/2), (t+1, Q(1)), (t+3, Q(-1))]


def direct(law, start, s, t):
    vertices = route(start, s, t)
    return direct_route(law, vertices)


def direct_route(law, vertices):
    return sum((weight*(first_capture(path, vertices, 1)
                        + first_capture(path, vertices, -1))/2
                for weight, path in law.paths), Q(0))


def g(law, v, lo, hi, threshold):
    return law.integrate(v, lo, hi, horizontal=False,
                         transform=lambda r: max(Q(0), r-threshold))


def positive(law, z, s, t):
    a = law.initial(z)  # strict: an a=z atom was caught at time zero
    b, d = law.radial(s, -z), law.radial(t, s)
    column = law.column(z, z, s)
    across = law.integrate(s, s, t, horizontal=False)
    return (4*t+8+2*s*a-(2*t+2+z-s)*b-(t+6-s)*d
            - column-law.f(s, z)-across-g(law, t, t, t+2, b))


def negative(law, z, s, t):
    a = sum((w for w, path in law.paths if path.value(Q(0)) <= z), Q(0))
    b, d = law.radial(s, z), law.radial(t, s)
    nbar = law.integrate(z, -z, z, horizontal=True, strict=True)
    column = law.integrate(z, z, s, horizontal=False)
    return (nbar+4*t+8-2*(t+3)*a+(s+z-2*t-2)*b
            -(t+6-s)*max(Q(0), d-a)-column
            -g(law, s, s, t, a)-g(law, t, t, t+2, b))


def positive_same_half(law, z, s, t):
    """Second interior turn remains positive: -z<=t<s, t<=1."""
    a = law.initial(z)
    b = law.radial(s, -z)
    d = law.radial(s, t, strict=True)
    low = min(a, d)
    incoming = law.integrate(s, -z, t, horizontal=True, strict=True,
                             transform=lambda r: max(Q(0), a-r))
    last_incoming = law.integrate(t+2, t, Q(1), horizontal=True, strict=True,
                                  transform=lambda r: min(low, r))
    return (4*t+8+(s+t)*a-(2*t+2+z-s)*b-law.column(z,z,s)-incoming
            -g(law,t,abs(t),t+2,b)+(2+t-s)*low+last_incoming)


def initial_inward_route(a, v, s):
    return [(Q(0), a), ((a+v)/2, (a-v)/2), ((s+v)/2, (s-v)/2),
            (s+1, Q(-1)), (s+3, Q(1))]


def initial_inward(law, a, v, s):
    initial = sum((w for w,path in law.paths if path.value(Q(0)) <= a),Q(0))
    low = law.radial(a,v,strict=True)
    high = max(initial,law.radial(s,v))
    n_part = law.integrate(a,-a,v,horizontal=True,strict=True)
    f_part = law.integrate(s,v,s,horizontal=True,strict=True,
                           transform=lambda r:max(Q(0),low-r))
    i_part = g(law,v,a,s,initial)
    return (4*s+8+n_part+(2*s-a-v)*low-(s+6-v)*high-(s+v)*initial
            -f_part-i_part-law.h(s))


def verify_same_half_families(law, counts):
    starts={Q(1,10),Q(1,4),Q(1,2),Q(3,4),Q(9,10)}
    starts.update(path.value(Q(0)) for _,path in law.paths if 0<path.value(Q(0))<1)
    for z in sorted(starts):
        for s in sorted({z,(z+1)/2,Q(1),Q(9,8),2-z}):
            if not z<=s<=2-z:continue
            lower=max(-z,s-2)
            upper=min(s,Q(1))
            turns={lower+(upper-lower)*fraction for fraction in [Q(0),Q(1,4),Q(1,2),Q(3,4),Q(1)]}
            for t in sorted(turns):
                if not t<s:continue
                prediction=positive_same_half(law,z,s,t)
                actual=4*direct(law,z,s,t)
                assert prediction==actual,('same half',z,s,t,prediction,actual)
                counts['positive second turn stays on same half']+=1
                if t<0:counts['same-half negative return characteristic']+=1
                if law.radial(s,t)!=law.radial(s,t,strict=True):
                    counts['same-half strict turn witnesses']+=1
        for fraction in [Q(0),Q(1,4),Q(1,2),Q(3,4)]:
            v=-z+2*z*fraction
            for ratio in [Q(0),Q(1,4),Q(1,2),Q(3,4),Q(1)]:
                s=z+(v+2-z)*ratio
                prediction=initial_inward(law,z,v,s)
                actual=4*direct_route(law,initial_inward_route(z,v,s))
                assert prediction==actual,('initial inward',z,v,s,prediction,actual)
                counts['initial inward then outward']+=1
                if v==-z:
                    assert prediction==four_cost(law,s,z)
                    counts['initial inward zero-leg collapse']+=1


def main():
    counts = Counter()
    for original in finite_fixtures():
        law = Law([(w, Path(list(path.knots)+[(Q(8), Q(1))]))
                   for w, path in original.paths])
        verify_same_half_families(law,counts)
        starts = [Q(1, 10), Q(1, 8), Q(3, 8), Q(2, 5),
                  Q(5, 8), Q(7, 10), Q(7, 8)]
        for z in starts:
            turns = sorted({z, (z+1)/2, Q(3, 4), Q(7, 8), Q(1),
                            Q(9, 8), Q(5, 4), 2-z})
            for s in turns:
                if s < z or s > 2-z:
                    continue
                later = {s+2*f for f in [Q(0), Q(1, 16), Q(1, 4), Q(1, 2), Q(1)]}
                later.update(t for t in [Q(7, 8), Q(15, 16), Q(1), Q(9, 8)]
                             if s <= t <= s+2)
                for t in sorted(later):
                    for sign, formula in [(1, positive), (-1, negative)]:
                        prediction = formula(law, z, s, t)
                        actual = 4*direct(law, sign*z, s, t)
                        assert prediction == actual, (sign, z, s, t, prediction, actual)
                        counts['positive' if sign == 1 else 'negative'] += 1
                        if t == s+2:
                            assert actual == 4*direct_cost(law, s, sign*z)
                            if sign == 1:
                                assert prediction == four_cost(law, s, z)
                            counts['second turn at endpoint'] += 1
                    if s == z or t == s:
                        counts['initial or center equality faces'] += 1
                    if any(path.value(Q(0)) == z for _, path in law.paths):
                        counts['initial atom starts'] += 1
    print(f'PASS: {sum(counts.values())} exact two-interior-turn CDF checks')
    for key, value in counts.items():
        print(f'  {key}: {value}')
    print('Scope: exact capture identities; no matching law or global value claim')


if __name__ == '__main__':
    main()
