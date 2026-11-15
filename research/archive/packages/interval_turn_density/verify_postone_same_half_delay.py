#!/usr/bin/env python3
"""Exact delay bound for same-half detours after a U=1 outward turn."""
from collections import Counter
from fractions import Fraction as Q

from verify_positive_cdf_sheet import finite_fixtures
from verify_curved_terminal_sources import inward_cost
from verify_repeated_same_half import cost,repeated_route
from verify_endpoint_inward_comparison import inverse


def main():
    counts=Counter()
    for law in finite_fixtures():
        outgoing_atom=any(inverse(p,'V',Q(1))<2 for _,p in law.paths)
        for a in [Q(1,5),Q(3,5),Q(9,10),Q(1)]:
            for v1 in [-a,-a/2]:
                A=sum((w for w,p in law.paths if p.value(Q(0))<=a),Q(0))
                m1=1-max(A,law.radial(Q(1),v1))
                baseline=inward_cost(law,a,v1)
                for v2 in [v1/2,Q(0),Q(1,2),Q(9,10)]:
                    for fraction in [Q(1,10),Q(1,2),Q(9,10)]:
                        s2=1+(1+v2)*fraction
                        route=repeated_route(a,v1,Q(1),v2,s2)
                        delta=2*(cost(law,route)-baseline)
                        assert delta>=s2-1-4*m1,(a,v1,v2,s2,delta,m1)
                        counts['one added same-half detour']+=1
                        if outgoing_atom:counts['outgoing-time-one atom witnesses']+=1

                        v3=(1+v2)/2
                        s3=s2+(2+v3-s2)/3
                        route=route[:-2]+[((s2+v3)/2,(s2-v3)/2),
                                         ((s3+v3)/2,(s3-v3)/2),
                                         (s3+1,Q(-1)),(s3+3,Q(1))]
                        delta=2*(cost(law,route)-baseline)
                        assert delta>=s3-1-4*m1,(a,v1,v2,s2,v3,s3,delta,m1)
                        counts['two added same-half detours']+=1
    print('PASS:',sum(counts.values()),'exact post-one same-half delay checks')
    for name,n in counts.items():print(' ',name+':',n)
    print('No beta(1)=2 assumption; early center/outgoing atoms are retained')


if __name__=='__main__':main()
