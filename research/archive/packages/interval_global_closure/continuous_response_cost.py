#!/usr/bin/env python3
"""Exact capture moments for unit legs and waits at the center."""
from fractions import Fraction as Q


def hinge_area(q,g0,g1,duration):
    """Integral of (q-g)_+ for an affine g, using exact rationals."""
    a,b=q-g0,q-g1
    if a<=0 and b<=0:return Q(0)
    if a>=0 and b>=0:return duration*(a+b)/2
    return duration*(max(a,b)**2)/(2*abs(b-a))


def route_payoff(field,route):
    """Exact full payoff; a stationary segment is permitted only at x=0.

    Unit-only routes retain the independently implemented existing scorer.
    The mixed scorer uses the same proven unit-leg action and exact center
    boundary integrals, retaining strict/closed records at every contact.
    """
    route=[tuple(map(Q,p))for p in route]
    assert route and route[0][0]==0
    if all(b>a and abs(y-x)==b-a for(a,x),(b,y)in zip(route,route[1:])):
        return field.unit_route_payoff(route)
    lower,upper=field.cdf_sides(*route[0]);cost=Q(0)
    center=sorted({u for u,v in field.nodes if u==v})
    for(start,x),(end,y)in zip(route,route[1:]):
        assert end>start and max(abs(x),abs(y))<=1
        velocity=(y-x)/(end-start)
        if velocity==0:
            assert x==y==0,'Only center waits are supported'
            cuts=[start]+[t for t in center if start<t<end]+[end]
            for a,b in zip(cuts,cuts[1:]):
                g0=(1-field.radial(a,a))/2;g1=(1-field.radial(b,b))/2
                assert lower<=g0 and 1-upper<=g0
                aa,bb=min(lower,g1),min(1-upper,g1)
                area=hinge_area(lower,g0,g1,b-a)+hinge_area(1-upper,g0,g1,b-a)
                cost+=b*((lower-aa)+(1-upper-bb))-area
                lower,upper=aa,1-bb
            continue
        assert abs(velocity)==1
        cuts=[start,end]
        if x*y<0:cuts.insert(1,start-velocity*x)
        area=Q(0)
        for a,b in zip(cuts,cuts[1:]):
            xa,xb=x+velocity*(a-start),x+velocity*(b-start)
            sign=1 if xa+xb>0 else-1
            ua,va=a+abs(xa),a-abs(xa);ub,vb=b+abs(xb),b-abs(xb)
            record=upper if velocity==1 else lower
            if velocity*sign==1:
                threshold=2*record-1 if sign==1 else 1-2*record
                area+=(field.integral(va,ua,ub,1)-threshold*(ub-ua)
                       +field.integral(va,ua,ub,1,threshold))/4
            else:
                threshold=1-2*record if sign==-1 else 2*record-1
                area+=field.integral(ua,va,vb,0,threshold)/4
        strict,closed=field.cdf_sides(end,y)
        if velocity==1:
            updated=max(upper,closed);cost+=end*(updated-upper)-area;upper=updated
        else:
            updated=min(lower,strict);cost+=end*(lower-updated)-area;lower=updated
    assert lower==0 and upper==1,('Incomplete route',lower,upper)
    return cost
