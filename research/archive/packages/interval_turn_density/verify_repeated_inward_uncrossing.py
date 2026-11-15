#!/usr/bin/env python3
"""Exact conditional uncrossing of two chainable inward routes."""
from collections import Counter
from fractions import Fraction as Q

from verify_positive_cdf_sheet import finite_fixtures
from verify_curved_terminal_sources import inward_cost
from verify_repeated_same_half import cost, repeated_route


def main():
    counts=Counter()
    for law in finite_fixtures():
        for a in [Q(1,5),Q(2,5),Q(3,5),Q(4,5)]:
            for v1 in [-a,-a/2]:
                for s1 in [a+(1-a)*Q(1,5),a+(1-a)*Q(1,2)]:
                    for v2 in [v1*Q(3,4),v1*Q(1,4),Q(0)]:
                        As=sum((w for w,p in law.paths if p.value(Q(0))<=s1),Q(0))
                        Aa=sum((w for w,p in law.paths if p.value(Q(0))<=a),Q(0))
                        B1=law.radial(s1,v1)
                        for s2 in [s1+(1-s1)*Q(1,4),s1+(1-s1)*Q(3,4),Q(1),
                                   1+(1+v1)/3]:
                            B2=law.radial(s2,v2)
                            if B2<As:
                                continue
                            first=inward_cost(law,a,v1,s1)
                            second=inward_cost(law,s1,v2,s2)
                            loop=cost(law,repeated_route(a,v1,s1,v2,s2))
                            sweep=cost(law,[(Q(0),s1),(s1+1,Q(-1)),(s1+3,Q(1))])
                            gain=4*(first+second-loop-sweep)
                            lower=(6+2*s1-s2-v2)*(As-max(Aa,B1))
                            assert gain>=lower>=0,(a,v1,s1,v2,s2,gain,lower)
                            counts['conditional chain uncrossing']+=1
                            if s2>1:
                                counts['post-one second turns']+=1
                            if lower>0:
                                counts['strict initial-front gap witnesses']+=1
    print('PASS:',sum(counts.values()),'exact repeated-inward uncrossing checks')
    for name,n in counts.items(): print(' ',name+':',n)
    print('Scope: requires second outward frontier at least A(s1); s1<=1')


if __name__=='__main__':main()
