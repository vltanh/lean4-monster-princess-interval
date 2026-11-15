#!/usr/bin/env python3
"""Exact independent segment-capture checks of the curved outgoing layer."""
from fractions import Fraction as Q

def from_uv(nodes):
    p=[((u+v)/2,(u-v)/2)for u,v in nodes]
    assert p[0][0]==0 and all(0<=x<=1 for t,x in p)
    assert all(t<s and abs(x-y)<=s-t for(t,x),(s,y)in zip(p,p[1:]))
    return p+[(Q(6),p[-1][1])]

def ordinary(a,u,c):
    nodes=[(a,-a)]
    middle=[(u,u),(c,c)]if c>u else [(u,c)]
    for pair in [(u,-a)]+middle+[(2+c,c)]:
        if pair!=nodes[-1]:nodes.append(pair)
    return from_uv(nodes)

def value(p,t):
    for(t0,x0),(t1,x1)in zip(p,p[1:]):
        if t<=t1:return x0+(x1-x0)*(t-t0)/(t1-t0)
    return p[-1][1]

def capture(p,m,sign):
    ts=sorted(set([t for t,x in p]+[t for t,x in m]))
    for l,r in zip(ts,ts[1:]):
        a=sign*value(p,l)-value(m,l);b=sign*value(p,r)-value(m,r)
        if a==0:return l
        if a*b<=0:return l+(r-l)*a/(a-b)
    raise AssertionError('No capture')

def inverse(p,z,sign):
    for(t,x),(s,y)in zip(p,p[1:]):
        a=t+sign*x;b=s+sign*y
        if z<=a:return t
        if z<=b:return t+(s-t)*(z-a)/(b-a)
    raise AssertionError('Missing first inverse')

def cost4(p,kind,z):
    if kind=='ell':m=[(Q(0),-z),(1+z,Q(1)),(3+z,Q(-1)),(Q(6),Q(-1))]
    elif kind=='f':m=[(Q(0),z),(1-z,Q(1)),(3-z,Q(-1)),(Q(6),Q(-1))]
    else:m=[(Q(0),z),((1-z)/2,(1+z)/2),(Q(2),Q(-1)),(Q(4),Q(1)),(Q(6),Q(1))]
    return 2*(capture(p,m,1)+capture(p,m,-1))

def omega(p,c,z):
    first=max(Q(0),c-(2*inverse(p,z,1)-z))
    return first+(z+2-(2*inverse(p,z,-1)-z)if z<=c else 0)

def main():
    lows=[
      (from_uv([(Q(1,5),Q(-1,5)),(Q(1,5),Q(1,5)),(Q(13,20),Q(7,20)),
       (Q(9,10),Q(7,10)),(Q(19,20),Q(17,20)),(Q(57,20),Q(17,20))]),Q(17,20)),
      (from_uv([(Q(3,10),Q(-3,10)),(Q(3,5),Q(-3,10)),(Q(3,5),Q(1,4)),
       (Q(17,20),Q(11,20)),(Q(97,100),Q(9,10)),(Q(29,10),Q(9,10))]),Q(9,10)),
      (ordinary(Q(1,4),Q(2,5),Q(4,5)),Q(4,5))]
    highs=[(Q(3,5),Q(17,20),Q(-1,5)),(Q(9,10),Q(97,100),Q(-13,20)),
           (Q(49,50),Q(199,200),Q(-9,10))]
    probes=sorted(set([Q(k,101)for k in range(51,101)]+[Q(3,5),Q(4,5),Q(17,20),
        Q(9,10),Q(19,20),Q(97,100),Q(199,200)]))
    count=0
    for p,c in lows:
        for z in probes:
            assert cost4(p,'ell',z)==3*z+2+c-omega(p,c,z)
            assert cost4(p,'f',z)==8-3*z+c
            assert cost4(p,'g',z)==5+c
            count+=3
    weights=[Q(1,12),Q(1,8),Q(1,6),Q(1,5),Q(1,4),Q(7,40)]
    assert sum(weights)==1
    paths=[p for p,c in lows]+[ordinary(a,u,c)for a,u,c in highs]
    cutoffs=[c for p,c in lows]+[c for a,u,c in highs]
    initials=[p[0][1]for p in paths]
    v4=5+sum(w*c for w,c in zip(weights,cutoffs))
    for z in probes:
        v=1-z
        r=sum(w for w,a in zip(weights,initials)if a>z)
        primitive=sum(w*max(Q(0),a-z)for w,a in zip(weights,initials))
        H=(8-2*v)*r+primitive-3*v
        incoming=sum(w*(a+c)for w,(a,u,c)in zip(weights[3:],highs)if u>=z)
        correction=sum(w*omega(p,c,z)for w,(p,c)in zip(weights[:3],lows))
        actual=sum(w*cost4(p,'ell',z)for w,p in zip(weights,paths))
        assert actual-v4==H-incoming-correction,(z,actual-v4,H-incoming-correction)
        count+=1
    print(f'PASS: {count} exact curved-prefix and mixed-law capture identities')
    print('PASS: first-touch U plateaus and exact V cutoffs included')
    print('Scope: outgoing-layer identity, not a matched equilibrium')

if __name__=='__main__':main()
