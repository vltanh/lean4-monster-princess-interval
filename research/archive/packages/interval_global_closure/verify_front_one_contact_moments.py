#!/usr/bin/env python3
"""Exact physical replay of the front-one S/P and J/I moment algebra.

The radial Princess is uniform initially, stays at radius r until time
1-r, then moves outward at speed one and sticks at the endpoint.  A
stationary endpoint pair may carry extra probability.  Actual first
contacts are integrated independently of the moment formulas.

This checks the conditional theorem's physical identities.  It does not
test the non-Puiseux proof by reproducing its coefficient recurrence and
does not claim that these fixture laws have the hypothesized contacts.
"""
from fractions import Fraction as Q
from itertools import combinations
from pathlib import Path
import argparse
import json

from verify_bulk_contact_equations import clip


def uniform_physical_score(path):
    answer = Q(0)
    branch_count = 0
    for sign in (-1, 1):
        branches = []
        # Position ar*r+bt*t+c, with guards a*r+b*t<=k.
        pieces = [
            (Q(sign), Q(0), Q(0), [(0,-1,0), (1,1,1)]),
            (Q(2*sign), Q(sign), Q(-sign), [(-1,-1,-1), (2,1,2)]),
            (Q(0), Q(0), Q(sign), [(-2,-1,-2)]),
        ]
        for (start, x), (end, y) in zip(path, path[1:]):
            if start == end:
                assert x == y
                continue
            v = (y-x)/(end-start)
            offset = x-v*start
            assert abs(v) <= 1
            for ar, bt, c, guards in pieces:
                if v == bt:
                    assert ar != 0  # one zero-mass initial radius only
                    continue
                slope, intercept = ar/(v-bt), (c-offset)/(v-bt)
                rows = [(-slope, intercept-start), (slope, end-intercept)]
                rows += [(Q(a)+Q(b)*slope, Q(k)-Q(b)*intercept)
                         for a,b,k in guards]
                domain = clip(rows)
                if domain is not None:
                    branches.append((*domain, slope, intercept))
        cuts = {Q(0), Q(1)}
        for lo, hi, _, _ in branches:
            cuts.update((lo, hi))
        for p, q in combinations(branches, 2):
            lo, hi = max(p[0], q[0]), min(p[1], q[1])
            difference = p[2]-q[2]
            if difference:
                r = (q[3]-p[3])/difference
                if lo < r < hi:
                    cuts.add(r)
        cuts = sorted(cuts)
        for lo, hi in zip(cuts, cuts[1:]):
            r = (lo+hi)/2
            eligible = [p for p in branches if p[0] <= r <= p[1]]
            assert eligible, (path, sign, lo, hi)
            branch = min(eligible, key=lambda p:p[2]*r+p[3])
            answer += (branch[2]*(hi*hi-lo*lo)/2+branch[3]*(hi-lo))/2
        branch_count += len(branches)
    return answer, branch_count


def endpoint_score(path):
    total = Q(0)
    for endpoint in (Q(-1), Q(1)):
        hits = []
        for (a,x),(b,y) in zip(path,path[1:]):
            if x == endpoint:
                hits.append(a)
            if a < b and x != y:
                t = a+(endpoint-x)*(b-a)/(y-x)
                if a <= t <= b:
                    hits.append(t)
        assert hits
        total += min(hits)/2
    return total


def cdf(t, x, endpoint_mass):
    if x > 1:
        return Q(1)
    if x < -1:
        return Q(0)
    radial = max(Q(0), min(abs(x), (abs(x)+1-t)/2))
    uniform = Q(1,2)+(radial/2 if x > 0 else -radial/2 if x < 0 else 0)
    return endpoint_mass/2+(1-endpoint_mass)*uniform


def integral(p, start, end, v, offset, cap=None):
    if start == end:
        return Q(0)
    cuts = {start,end}
    # These are all branch/arena crossings of the explicit physical CDF.
    for slope, intercept in ((v,offset),(v,offset-1),(v,offset+1),
                             (1+v,offset-1),(1-v,-offset-1)):
        if slope:
            at = -intercept/slope
            if start < at < end:
                cuts.add(at)
    result = Q(0)
    cuts = sorted(cuts)
    for lo, hi in zip(cuts, cuts[1:]):
        a,b = (3*lo+hi)/4,(lo+3*hi)/4
        fa,fb = cdf(a,v*a+offset,p),cdf(b,v*b+offset,p)
        slope = (fb-fa)/(b-a)
        intercept = fa-slope*a
        assert cdf((lo+hi)/2,v*(lo+hi)/2+offset,p) == slope*(lo+hi)/2+intercept
        sub = {lo,hi}
        if cap is not None and slope:
            at = (cap-intercept)/slope
            if lo < at < hi:
                sub.add(at)
        sub = sorted(sub)
        for a,b in zip(sub,sub[1:]):
            if cap is not None and slope*(a+b)/2+intercept >= cap:
                result += cap*(b-a)
            else:
                result += slope*(b*b-a*a)/2+intercept*(b-a)
    return result


def max_integral(p, start, end, v, offset, floor):
    return (integral(p,start,end,v,offset)+floor*(end-start)
            -integral(p,start,end,v,offset,floor))


def moment(p,b,cap):
    return integral(p,Q(0),b+1,Q(-1),b,cap)


def principal(a):
    h = (1-a)/2
    return [(Q(0),a),(h,(1+a)/2),(Q(2),Q(-1)),(Q(4),Q(1))]


def endpoint(a):
    return [(Q(0),a),(1-a,Q(1)),(3-a,Q(-1))]


def inward(a,z, endpoint_first=False):
    d = (z-a)/2
    prefix = [(Q(0),1-a),(d,1-(a+z)/2)]
    if endpoint_first:
        return prefix+[(z,Q(1)),(z+2,Q(-1))]
    return prefix+[(z/2,1-z/2),(Q(2),Q(-1)),(Q(4),Q(1))]


def inward_moments(p,a,z):
    d = (z-a)/2
    f = cdf(Q(0),1-a,p)
    l = cdf(d,1-(a+z)/2,p)
    k = cdf(z/2,1-z/2,p)
    row = integral(p,Q(0),d,Q(-1),1-a)
    column = max_integral(p,d,z/2,Q(1),1-z,f)
    outer = max_integral(p,z/2,z,Q(1),1-z,f)
    ci = 4+moment(p,Q(1),l)+row-column-d*(f+l)-(4-z/2)*max(f,k)
    cj = z+moment(p,1+z,l)+row-column-outer-d*(f+l)
    return ci,cj,(f,l,k,outer)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('output',type=Path)
    args = ap.parse_args()
    counts = {'physical_P_and_S':0,'positive_SP_identity':0,
              'negative_SP_identity':0,'center_start_identity':0,
              'front_column_extension':0,'front_moment_difference':0,
              'physical_I_and_J':0,'JI_difference_and_nonnegative_remainder':0,
              'J_outer_moment_and_column':0,'endpoint_trace_jumps':0,
              'actual_endpoint_sweep':0}
    branches = 0
    for p in (Q(0),Q(1,3),Q(1)):
        def physical(path):
            nonlocal branches
            value,n = uniform_physical_score(path)
            branches += n
            return (1-p)*value+p*endpoint_score(path)
        sweep = physical([(Q(0),Q(1)),(Q(2),Q(-1))])
        assert sweep == moment(p,Q(1),Q(1))
        counts['actual_endpoint_sweep'] += 1
        sp = {}
        for i in range(-7,8):
            a = Q(i,8)
            f,k = cdf(Q(0),a,p),cdf((1-a)/2,(1+a)/2,p)
            cp,cs = physical(principal(a)),physical(endpoint(a))
            ip = integral(p,Q(0),(1-a)/2,Q(1),a)
            ie = integral(p,Q(0),1-a,Q(1),a)
            assert cp == 4-ip-(7+a)*k/2+moment(p,Q(1),f)
            assert cs == 1-a-ie+moment(p,2-a,f)
            counts['physical_P_and_S'] += 2
            if a >= 0:
                expected = -4+Q(5,4)*(1-a)+(3+a)*k+(1-a)*f/2
                assert ie-ip == (1-a)*k/2
                assert moment(p,2-a,f)-moment(p,Q(1),f) == (1-a)*f/2+(1-a)/4
                counts['front_column_extension'] += 1
                counts['front_moment_difference'] += 1
                counts['positive_SP_identity' if a else 'center_start_identity'] += 1
            else:
                expected = -(3+a)+(3+a)*k+(1-a)*f
                assert moment(p,Q(1),f) == 2*f
                assert moment(p,2-a,f) == (3-a)*f
                counts['negative_SP_identity'] += 1
            assert cs-cp == expected,(p,a,cs,cp,expected)
            sp[a] = cs-cp
        for z in (Q(1,4),Q(1,2),Q(3,4)):
            for a in (Q(0),z/2,z):
                ci,cj = physical(inward(a,z)),physical(inward(a,z,True))
                mi,mj,(f,l,k,outer) = inward_moments(p,a,z)
                if a == 0:
                    atom = 1-cdf(Q(0),Q(1),p)
                    assert ci == sweep
                    assert mi-ci == 4*atom
                    assert mj-cj == z*atom
                    counts['endpoint_trace_jumps'] += 2
                    continue
                assert ci == mi and cj == mj
                counts['physical_I_and_J'] += 2
                assert moment(p,1+z,l)-moment(p,Q(1),l) == z*l/2+z/4
                assert outer == z*max(f,k)/2
                counts['J_outer_moment_and_column'] += 2
                direct = -4+5*z/4+z*l/2+(4-z)*max(f,k)
                remainder = z*(l-cdf(Q(0),1-z,p))/2+(4-z)*(max(f,k)-k)
                assert cj-ci == direct
                assert cj-ci == sp[1-z]+remainder
                assert remainder >= 0
                counts['JI_difference_and_nonnegative_remainder'] += 1
    report = {'status':'PASS',
        'scope':'Exact physical front-one moment identities and endpoint jumps; the asymptotic nonalgebraicity theorem remains analytic, and no fixture contact or game-value claim is made.',
        'princess_family':'Uniform initial radius r, stationary until1−r then outward/sticky; mixed with stationary endpoint-pair mass p in {0,1/3,1}.',
        'counts':counts,'physical_affine_contact_branches':branches}
    text=json.dumps(report,indent=2)+'\n'
    args.output.write_text(text)
    print(text,end='')


if __name__ == '__main__':
    main()
