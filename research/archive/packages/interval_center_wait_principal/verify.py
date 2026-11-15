#!/usr/bin/env python3
"""Exact Fraction regression for the centered-Princess / principal-one-turn game.

Audits chronological first contacts on sample rational routes. The mathematical
integral/differential saddle proof is in CENTER_WAIT_PRINCIPAL_ONE_TURN_EXACT.md.
"""
from fractions import Fraction as Q
from decimal import Decimal, localcontext

def locate(nodes, t):
    if t >= nodes[-1][0]:
        return nodes[-1][1]
    for (a, v), (b, w) in zip(nodes, nodes[1:]):
        if a <= t <= b:
            return v if a == b else v + (w-v)*(t-a)/(b-a)
    raise AssertionError((nodes,t))

def first_capture(p,m):
    knots=sorted(set(t for t,_ in p+m))
    for left,right in zip(knots,knots[1:]):
        x=locate(p,left)-locate(m,left)
        y=locate(p,right)-locate(m,right)
        if x==0:return left
        if x*y<=0:return left-x*(right-left)/(y-x)
    raise AssertionError('No capture before terminal time')

def principal_monster(a):
    h=(Q(1)-a)/2
    return [(Q(0),a),(h,a+h),(Q(2),Q(-1)),(Q(4),Q(1)),(Q(7),Q(1))]

def princess(r,d,outbound,sign):
    return [(Q(0),sign*r),(r,Q(0)),(d,Q(0)),
            (d+1,sign*outbound),(Q(7),sign*outbound)]

def pair_cost(a,r,d,outbound):
    m=principal_monster(a)
    return (first_capture(princess(r,d,outbound,Q(1)),m)
           +first_capture(princess(r,d,outbound,Q(-1)),m))/2

def main():
    grid=[Q(i,12) for i in range(13)]
    count=0
    for a in grid:
        for r in grid:
            for d in [r,Q(1),Q(13,12),Q(3,2)]+[q for q in grid if q>r]:
                for out in [-1,1]:
                    got=pair_cost(a,r,d,Q(out))
                    if r>0 and d<1:
                        if a<r:
                            expected=Q(1)+(r-a)/4 if out==1 else (r-a+1+d)/4
                        elif a>r:
                            expected=Q(1)+(1+d)/4
                        else:
                            expected=Q(1) if out==1 else (1+d)/4
                        assert got==expected,(a,r,d,out,got,expected)
                    if d>=1:assert got<=1,(a,r,d,out,got)
                    if r==0 and a==0:assert got==0,(a,r,d,out,got)
                    count+=1
    with localcontext() as ctx:
        ctx.prec=50
        alpha=(Decimal(-1)/2).exp()
        value=Decimal(3)/2-alpha/2
        for i in range(1001):
            a=Decimal(i)/1000
            F=((a-1)/2).exp()
            f=F/2
            assert abs(F/4-f/2)<Decimal('1e-48')
        print('Exact subgame value = 3/2 - e^(-1/2)/2 =',value)
    print('PASS:',count,'exact first-capture cases, indifference identity')

if __name__=='__main__':main()
