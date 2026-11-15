#!/usr/bin/env python3
"""Exact local checks for DISCRETE_AFFINE_CELL_TWO_RUNS.md.

No pricing prune is enabled by this script. Direct node sums independently
check the ceiling-integral identities and fractional old-record boundaries.
Full small word banks check domination for every concave monotone future
through a convex-mixture certificate of area and both exit extents.
"""
from fractions import Fraction as Q
from itertools import combinations, product
import json


def direct(word,alpha,beta,a,b):
    value=Q(0);lower=a;upper=b;low_area=high_area=Q(0)
    for direction in word:
        lower=max(lower,-value);upper=max(upper,value)
        low_area+=lower;high_area+=upper
        value+=alpha if direction else -beta
    lower=max(lower,-value);upper=max(upper,value)
    return low_area+high_area,lower,upper,low_area,high_area


def ceiling_integral(start,end,step):
    assert Q(0)<=start<=end and step>0
    def primitive(z):
        k=z//step
        return step*Q(k*(k+1),2)+(z-step*k)*(k+1)
    return primitive(end)-primitive(start)


def lower_formula(m,n,alpha,beta,a,p):
    N=m+n;C=beta*n;X=alpha*p;q=C-a
    if X>=q:return N*a
    return N*a+N*(C-a-X)-ceiling_integral(a+X,C,beta)-X*(q-X)/alpha


def upper_formula(m,n,alpha,beta,b,p,down_area):
    N=m+n;C=beta*n;X=alpha*p;f=alpha*m-C
    if X<=b:return down_area
    delta=N*(X-b)-ceiling_integral(b,X,alpha)
    cutoff=min(X,f)
    if cutoff>b:
        delta-=m*(cutoff-b)-ceiling_integral(C+b,C+cutoff,alpha)
    return down_area+delta


def dominating_mixture(up,down,word):
    """Return a rational weight with all three averaged quantities >= word."""
    lo,hi=Q(0),Q(1)
    for u,d,target in zip(up[:3],down[:3],word[:3]):
        if u==d:
            assert d>=target,(up,down,word)
        elif u>d:lo=max(lo,Q(target-d,u-d))
        else:hi=min(hi,Q(target-d,u-d))
    assert lo<=hi,(up,down,word,lo,hi)
    theta=(lo+hi)/2
    assert all(theta*u+(1-theta)*d>=w for u,d,w in zip(up[:3],down[:3],word[:3]))
    return theta


def main():
    slopes=((Q(1),Q(1)),(Q(1),Q(2)),(Q(3,2),Q(2,3)),(Q(5,3),Q(4,3)))
    caps=((Q(0),Q(0)),(Q(1,3),Q(1,7)),(Q(3,2),Q(1,2)),
          (Q(3),Q(5)),(Q(7,3),Q(8,3)))
    cases=[(m,n,al,be,a,b) for m,n in product(range(1,5),repeat=2)
           for al,be in slopes for a,b in caps]
    # The next lattice point crosses q=C-a: this is the boundary jump
    # needed in the proof, rather than an old-record equality on the grid.
    cases += [(5,3,Q(3,2),Q(4,3),Q(6,7),Q(1,9)),
              (5,3,Q(3,2),Q(4,3),Q(8,7),Q(17,9))]
    identities=second_differences=words=tail_checks=explicit_mixtures=0
    for m,n,al,be,a,b in cases:
        up=direct([1]*m+[0]*n,al,be,a,b)
        down=direct([0]*n+[1]*m,al,be,a,b)
        values=[]
        for p in range(m+1):
            v=direct([1]*p+[0]*n+[1]*(m-p),al,be,a,b)
            assert v[3]==lower_formula(m,n,al,be,a,p)
            assert v[4]==upper_formula(m,n,al,be,b,p,down[4])
            values.append(v);identities+=2
            q=be*n-a
            P=min(m,-(-q//al)) if q>0 else 0
            theta=Q(p,P) if p<P else Q(1)
            assert all(theta*u+(1-theta)*d>=w
                       for u,d,w in zip(up[:3],down[:3],v[:3]))
            explicit_mixtures+=1
        for p in range(1,m):
            if al*p<be*n-a:
                assert values[p+1][3]-2*values[p][3]+values[p-1][3]>=2*al
                assert values[p+1][4]-2*values[p][4]+values[p-1][4]>=-al
                assert values[p+1][0]-2*values[p][0]+values[p-1][0]>=al
                second_differences+=1
        futures=(lambda B,H:-2*B-3*H,
                 lambda B,H:min(5-B-4*H,-2*B-H),
                 lambda B,H:-max(B,Q(2,3))-2*max(H,Q(5,7)))
        for locations in combinations(range(m+n),m):
            mask=set(locations)
            v=direct([int(i in mask) for i in range(m+n)],al,be,a,b)
            theta=dominating_mixture(up,down,v);words+=1
            for g in futures:
                old=-v[0]+g(v[1],v[2])
                corner=min(-x[0]+g(x[1],x[2]) for x in (up,down))
                assert corner<=old
                # Explicitly check the Jensen step for these non-linear
                # futures in addition to the universal mixture certificate.
                average=tuple(theta*u+(1-theta)*d for u,d in zip(up[:3],down[:3]))
                assert theta*g(up[1],up[2])+(1-theta)*g(down[1],down[2])<=g(average[1],average[2])
                tail_checks+=1
    print(json.dumps({'status':'PASS','parameter_cases':len(cases),
                      'independent_ceiling_area_identities':identities,
                      'strict_discrete_convexity_checks':second_differences,
                      'explicit_three_run_mixture_certificates':explicit_mixtures,
                      'full_bank_word_mixture_certificates':words,
                      'concave_continuation_comparisons':tail_checks,
                      'scope':'Local affine-cell identities and exact full-word regressions; no new game bound or enabled pricing prune.'},indent=2))


if __name__=='__main__':main()
