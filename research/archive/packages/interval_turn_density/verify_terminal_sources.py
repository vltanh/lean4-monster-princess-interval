#!/usr/bin/env python3
"""Exact endpoint-normalized terminal identities with a separate low field.

Direct first intersections are compared with the Q/Omega source formulas.
These fixtures establish identities, not existence of a matched tail or
an unrestricted lower guarantee.  Parameters avoid incoming-atom rows;
the intended continuous-field application has no such trace ambiguity.
"""
from collections import Counter
from fractions import Fraction as Q

from verify_positive_cdf_sheet import Law, wave, direct_cost


def fixture(scale):
    low=[wave(Q(1,5),Q(4,5),Q(4,5),1+Q(1,10000),Q(9,10)),
         wave(Q(1,2),Q(19,20),Q(1,2),1+Q(1,5000),Q(3,5)),
         wave(Q(4,5),1-Q(1,10**12),-Q(2,5),Q(1),-Q(2,5))]
    weighted=[(Q(3,10),p) for p in low]
    tails=[]
    for d in [Q(1,10),Q(1,20),Q(1,40)]:
        x=d*d/16;h=scale*x*x/16;weight=Q(1,30)
        tails.append((weight,x,d,h))
        weighted.append((weight,wave(1-x,1-h,-1+d,Q(1),-1+d)))
    return Law(weighted),Law([(Q(1,3),p) for p in low]),Q(9,10),tails


def main():
    counts=Counter()
    for scale in [Q(1,2),Q(1),Q(3,2)]:
        law,low,q0,tails=fixture(scale)
        n0=q0*low.integrate(Q(1),Q(-1),Q(1),horizontal=True,strict=True)
        endpoint=direct_cost(law,Q(1),Q(1))
        moment=sum((w*d for w,x,d,h in tails),Q(0))
        assert 4*endpoint==4+n0+moment
        counts['endpoint moment']+=1
        epsilons={Q(k,1003) for k in range(1,90)}
        epsilons.update(Q(1,1600)*Q(k,37) for k in range(1,37))
        for e in sorted(epsilons):
            z=1-e
            r=sum((w for w,x,d,h in tails if x<e),Q(0))
            E=sum((w for w,x,d,h in tails if d<e),Q(0))
            P=sum((w*(d+h) for w,x,d,h in tails if x<e),Q(0))
            delayed=sum((w*h for w,x,d,h in tails if d<e),Q(0))
            Qpost=(q0*e+q0*low.integrate(1+e,-1+e,Q(1),horizontal=True,strict=True)-n0)
            omega=(n0-q0*e-q0*low.integrate(1-e,-1+e,1-e,horizontal=True,strict=True))
            cf=direct_cost(law,2-z,z);cg=direct_cost(law,Q(1),z)
            cell=direct_cost(law,2+z,-z)
            assert 4*(cf-endpoint)==3*e+Qpost+e*E+delayed-P
            assert 4*(cf-cg)==e*(3-r)+Qpost-(8-2*e)*E
            J=sum((w*(d-x) for w,x,d,h in tails if h<e),Q(0))
            S=sum((w*max(Q(0),e-x) for w,x,d,h in tails),Q(0))
            assert 4*(cell-endpoint)==(8-2*e)*r+S-3*e-omega-J
            counts['positive M1 endpoint difference']+=1
            counts['positive M1/M2 difference']+=1
            counts['negative M1 endpoint difference']+=1
            if Qpost:counts['nonzero post source']+=1
            if omega:counts['nonzero prefix source']+=1
        # Also probe the much smaller incoming scale before every tail
        # rank has completed its incoming leg.
        hs=sorted(h for w,x,d,h in tails)
        for e in [hs[0]/2,(hs[0]+hs[1])/2,(hs[1]+hs[2])/2,2*hs[2]]:
            z=1-e;r=sum((w for w,x,d,h in tails if x<e),Q(0))
            omega=n0-q0*e-q0*low.integrate(z,-z,z,horizontal=True,strict=True)
            J=sum((w*(d-x) for w,x,d,h in tails if h<e),Q(0))
            S=sum((w*max(Q(0),e-x) for w,x,d,h in tails),Q(0))
            cell=direct_cost(law,2+z,-z)
            assert 4*(cell-endpoint)==(8-2*e)*r+S-3*e-omega-J
            counts['negative M1 incoming-scale truncation']+=1
    print('PASS:',sum(counts.values()),'exact terminal-source checks')
    for label,n in counts.items():print(' ',label+':',n)
    print('Scope: capture/source identities; no exact history or global equilibrium claim')


if __name__=='__main__':main()
