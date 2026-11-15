#!/usr/bin/env python3
"""Check the local-gap payoffs by independent direct capture integration.

Builds legal epsilon paths, integrates actual segment intersections over
the rational piecewise-constant monster densities, and takes their exact
quadratic one-sided payoff limit. No scalar functional is used to obtain
the reference capture integrals.
"""

from bisect import bisect_right
from fractions import Fraction as Q
import json
from pathlib import Path

from verify_local_gap import Law
from verify_trace_cap import ref


def princess(parameters, epsilon):
    a,u,c,y = parameters
    assert a <= u < 1 and y < 1 and epsilon < 1+y
    graph = [(a,-a),(u,-a),(u,min(u,c))]
    if c >= u:
        graph.append((c,c))
    graph.extend([(1,c),(1+epsilon,c),(1+epsilon,y),(2+y,y)])
    path = ref.clean([((U+V)/2,(U-V)/2) for U,V in graph]+[(Q(4),Q(1))])
    assert all(0 <= x <= 1 for t,x in path)
    assert all(abs(y-x) <= s-t for (t,x),(s,y) in zip(path,path[1:]))
    return path


def direct_integral(law, path):
    a = path[0][1]
    e = ref.inverse(path,1,1,strict=True)
    xcuts = {Q(0),a,-a,1-2*e}
    # These are all possible threshold and initial-branch changes for the
    # M1/M2 parameter. The reference times below use direct intersections.
    for t,p in path:
        for z in (t+p,t-p):
            xcuts.update((-z,2-z))
    value = Q(0)
    for name,family,sign in [('f',1,1),('g',2,1),('h',2,-1),('ell',1,-1)]:
        cuts = sorted(set(law.knots) | {sign*x for x in xcuts if 0 < sign*x < 1})

        def capture(z):
            monster = ref.monster_path(family,sign*z)
            return (ref.direct_capture(monster,path)
                    +ref.direct_capture([(t,-x) for t,x in monster],path))/2

        for lo,hi in zip(cuts,cuts[1:]):
            middle = (lo+hi)/2
            density = law.density[name][bisect_right(law.knots,middle)-1]
            if not density:
                continue
            first,second = capture((2*lo+hi)/3),capture((lo+2*hi)/3)
            midvalue = capture(middle)
            assert first+second == 2*midvalue
            value += density*(hi-lo)*midvalue
    sweep = ref.monster_path(1,Q(-1))
    value += law.w0*(ref.direct_capture(sweep,path)
                     +ref.direct_capture([(t,-x) for t,x in sweep],path))/2
    return value


def lagrange(samples, point):
    answer = Q(0)
    for i,(x,fx) in enumerate(samples):
        weight = Q(1)
        for j,(y,fy) in enumerate(samples):
            if i != j:
                weight *= (point-y)/(x-y)
        answer += weight*fx
    return answer


def main():
    data = json.loads(Path(__file__).with_name('local_gap_certificate.json').read_text())
    law = Law(data)
    cases = [tuple(map(Q,data['reference_tuple'])),
             (Q(63,64),Q(63,64),Q(-1,2),Q(329021,372832)),
             (Q(31,32),Q(31,32),Q(7,8),Q(15,16)),
             (Q(3,8),Q(5,8),Q(3,4),Q(7,8)),
             (Q(3,4),Q(7,8),Q(-1,2),Q(-1,4))]
    for parameters in cases:
        scales = [Q(1,4096*2**i) for i in range(4)]
        samples = [(epsilon,direct_integral(law,princess(parameters,epsilon)))
                   for epsilon in scales]
        # For these fixed parameters, all nonzero threshold distances
        # exceed the largest epsilon. On this interval the moving cuts
        # and capture times are affine in epsilon, hence their integral
        # is quadratic. The fourth exact value independently checks this.
        assert lagrange(samples[:3],scales[3]) == samples[3][1]
        assert lagrange(samples[:3],Q(0)) == law.payoff(*parameters), parameters
    print('PASS: 20 exact legal-path integrals for the rational signed-density law')
    print('PASS: five exact one-sided limits, including the reference and both bad-set maximizers')
    print('Scope: independent capture check of the exclusion functional; not a game-value certificate')


if __name__ == '__main__':
    main()
