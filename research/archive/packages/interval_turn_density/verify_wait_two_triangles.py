#!/usr/bin/env python3
"""Exact wait/triangle capture identities, independent of the mesh optimizer.

Finite ordered radial fixtures validate the general prefix-moment formula.
The constant-density-cone formula follows by P_wait=s*q/2 and B>=q.
No matching strategy or unrestricted guarantee is asserted.
"""
from collections import Counter
from fractions import Fraction as Q

from verify_positive_cdf_sheet import (Law, finite_fixtures, first_capture,
                                      wave, ONE, ZERO)


def vertices(s,t,e,first):
    return [(ZERO,ZERO),(s,ZERO),((s+t)/2,(s-t)/2),(t,ZERO),
            ((t+e)/2,(e-t)/2),(e,ZERO),(e+1,Q(first)),(e+3,Q(-first))]


def first_zero(path):
    for t0,t1,m,b in path.segments:
        if path.value(t0)==0:return t0
        if m and t0<=-b/m<=t1:return -b/m
    return None


def prefix_moments(law,s):
    rank,moment=ZERO,ZERO
    for weight,path in law.paths:
        hit=first_zero(path)
        if hit is not None and hit<=s:
            rank+=weight;moment+=weight*hit
    return rank,moment


def formula(law,s,t,e,first):
    q,prefix=prefix_moments(law,s)
    b,d=law.radial(t,s),law.radial(e,t)
    x,y=max(ZERO,b-q),max(ZERO,d-q)
    j1=law.integrate(s,s,t,horizontal=False,transform=lambda r:max(ZERO,r-q))
    j2=law.integrate(t,t,e,horizontal=False,transform=lambda r:max(ZERO,r-q))
    negative,positive=q+x,q+y
    if first==-1:
        tail=2*(e+1)*(1-negative)+2*(e+3)*(1-positive)
        center_scale=2
    else:
        tail=2*(e+3)*(1-negative)+2*(e+1)*(1-positive)
        center_scale=6
    center_gain=max(ZERO,law.radial(e,e)-negative)
    return (4*prefix+(s+t)*x+(t+e)*y-j1-j2+tail-center_scale*center_gain)


def direct(law,s,t,e,first):
    route=vertices(s,t,e,first)
    return sum((weight*(first_capture(path,route,1)+first_capture(path,route,-1))/2
                for weight,path in law.paths),ZERO)


def main():
    counts=Counter()
    fixtures=finite_fixtures()+[Law([(ONE,wave(Q(1,4),ONE,ONE,ONE,ONE))])]
    for law in fixtures:
        for s in [ZERO,Q(1,8),Q(1,4),Q(1,2)]:
            for t in sorted({s,(s+1)/2,Q(3,4),ONE}):
                if t<s:continue
                for e in [ONE,Q(9,8),Q(3,2)]:
                    for first in [-1,1]:
                        expected=4*direct(law,s,t,e,first)
                        assert formula(law,s,t,e,first)==expected,(s,t,e,first)
                        counts['direct wait/triangle identities']+=1
                        q,_=prefix_moments(law,s)
                        if law.radial(e,e)>max(q,law.radial(t,s)):
                            counts['time-one center correction witnesses']+=1
    # Pure rational elimination of the general formula on an exact linear
    # cone, with no time-one center atom.  This includes both final orders.
    for s in [ZERO,Q(1,4),Q(1,2)]:
        q=Q(3,10)*s
        for t in [Q(1,2),Q(3,4),ONE]:
            if t<s:continue
            for e in [ONE,Q(9,8)]:
                for b in [q,(1+q)/2,ONE]:
                    for d in [ZERO,q,(1+q)/2,ONE]:
                        x,y=b-q,max(ZERO,d-q)
                        for first in [-1,1]:
                            alpha=2*e+(2 if first==-1 else 6)-s-t
                            beta=e+(6 if first==-1 else 2)-t
                            gamma=2*e+(6 if first==-1 else 2)
                            tail=(2*(e+1)*(1-b)+2*(e+3)*(1-q-y) if first==-1
                                  else 2*(e+3)*(1-b)+2*(e+1)*(1-q-y))
                            expanded=2*s*q+(s+t)*x+(t+e)*y+(t-s)*q+tail
                            simplified=4*e+8-alpha*b-gamma*q-beta*y
                            assert expanded==simplified
                            counts['constant-cone coefficient identities']+=1
    print(f'PASS: {sum(counts.values())} exact wait/two-triangle checks')
    for key,value in counts.items():print(f'  {key}: {value}')
    print('Scope: exact identities; no matching law or unrestricted value claim')


if __name__=='__main__':main()
