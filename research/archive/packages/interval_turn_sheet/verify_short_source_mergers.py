"""Exact arithmetic audit of short-source merger identities and margins.
Analytic argument is in LOW_SURPLUS_ALL_HINGES_EXCLUSION.md.
"""
from fractions import Fraction as F
from random import Random
from collections import Counter
import json

def pos(z): return max(F(0),z)

def E(k,ell,h,y):
    d=k-ell; A=k/F(8)-ell/F(2); n=len(h)
    ans=A*sum(x*x for x in h)-ell/F(2)*sum(h[i]*h[i+1] for i in range(n-1))
    ans-=F(3)*ell*h[-1]/F(2)+y*h[0]/F(2)+y*y/(F(8)*k)
    ans-=pos(y-d*h[0])**2/(F(8)*k)
    ans-=sum(pos(ell*h[i-1]-d*h[i])**2/(F(8)*k) for i in range(1,n-1))
    if n>1: ans-=pos(ell*h[-2]-d*h[-1])/F(2)
    return ans

def C(k,ell,H,h,y):
    """Independent rank-moment recurrence, MAX retained at nonproductive returns.
    Normalization uses b=15/16, Z(t)=d(t-7/8), and terminal true jump.
    This is exact on the declared synthetic affine cell, not a substitute
    for checking the exterior saved field on every altered rank band.
    """
    d=k-ell; b=F(15,16)
    def z(t): return d*(t-F(7,8))
    def T(t,n,last):return t*n+(pos(n-z(t)) if last else pos(n-z(t))**2/(F(4)*k))
    assert sum(h)==H
    t=b-H;n=z(t)+y;cost=F(0)
    for j,p in enumerate(h):
        new=max(n,z(t)+k*p);e=t+p;last=j==len(h)-1
        cost+=(T(t,new,False)-T(t,n,False)+T(e,new,last)-T(e,n,last))/F(2)
        t=e;n=new
    return cost+(b+F(2))*(F(1)-n)

def prefix_bound(k,ell,p,q,g):
    d=k-ell; P=ell*p
    f=lambda v:pos(v-d*q)**2-v*v
    return -k*p*q/F(2)-g*q-ell*ell*p*q/(F(2)*k)+(f(P)-f(g))/(F(4)*k)

def hand_prefix_difference(k,ell,p,q,g):
    """Independent derivation from four affine first-inverse moments;
    T_t(q) = tq + (q-Z(t))_+^2/(4k). Term from added ranks uses
    an AFFINE LOWER BOUND on their future capture times.
    """
    d=k-ell; t=F(0); e=p+q
    n=d*p+g; N1=k*p; N2=d*p+k*q; Nh=k*(p+q)
    T=lambda s,x:s*x+pos(x-d*s)**2/(F(4)*k)
    return T(0,Nh)-T(0,N1)+T(e,N1)-T(e,n)-(T(p,N2)-T(p,n))-(T(e,Nh)-T(e,N2))

k=F(655898601421,62500000000);ell=F(820954217,12500000000)
d=k-ell;r=ell/k;B=k/F(4)-ell/F(2);cy=(k+ell)/(F(4)*k)
assert 0<r<F(1,8)
rng=Random(11260043)
counts=Counter();examples=[]
for rr in [r,F(1,100),F(1,20),F(1,9)]:
    K=k if rr==r else F(1)
    L=K*rr
    D=K-L
    for i in range(1440):
        p=F(rng.randrange(1,200),40000)
        q=max(F(rng.randrange(1,100),40000),L*p/K)
        if p+q>F(1,16):fac=F(1,16)/(p+q);p*=fac;q*=fac
        g=L*p*F(rng.randrange(0,101),100)
        f1=prefix_bound(K,L,p,q,g)
        f2=hand_prefix_difference(K,L,p,q,g)
        assert f1==f2,(f1,f2)
        assert f1<=-K*p*q/F(2)
        counts['exact_prefix_factorizations']+=1
# Terminal source penultimate: exact formal energy + quantitative margins.
for rr in [r,F(1,100),F(1,20),F(1,9)]:
    K=k if rr==r else F(1);L=K*rr;D=K-L
    for m in range(2,11):
        for t in range(90):
            hs=[F(rng.randrange(1,200),100000) for _ in range(m)]
            for j in range(1,m):hs[j]=max(hs[j], L*hs[j-1]/K)
            if m==2:
                p=hs[0];hs[1]=max(hs[1],L*p/K)
                y=(D+L*F(rng.randrange(1,100),100))*p
            else:
                a=hs[-3];p=L*a/(K-L*F(rng.randrange(1,100),100));hs[-2]=p
                hs[-1]=max(hs[-1],L*p/K)
                y=K*hs[0]*F(rng.randrange(1,100),100)
            H=sum(hs)
            if H>F(1,16):hs=[x*F(1,16)/H for x in hs]
            assert all(K*hs[j]>=L*hs[j-1] for j in range(1,m))
            y=(D+L*F(1,2))*hs[0] if m==2 else K*hs[0]*F(1,2)
            source=y if m==2 else L*hs[-3]
            assert D*hs[-2]<source<=K*hs[-2]
            hh=hs[:-2]+[hs[-2]+hs[-1]]
            diff=E(K,L,hh,y)-E(K,L,hs,y)
            assert diff<=(-L*hs[0] if m==2 else -K*hs[-2]*hs[-1]/F(4)-F(31,32)*L*hs[-2]),(m,diff)
            counts['exact_terminal_pair_mergers']+=1
# General interior or first short sources, against the SAME later physical
# renewal suffix, allowing merged later returns to become nonproductive.
for m in range(3,11):
    for j in range(m-2):
        for t in range(180):
            hs=[F(rng.randrange(1,200),100000) for _ in range(m)]
            for s in range(1,m):hs[s]=max(hs[s],ell*hs[s-1]/k*F(rng.randrange(101,125),100))
            if j>0:
                hs[j]=ell*hs[j-1]/(k-ell*F(rng.randrange(1,100),100))
                for s in range(j+1,m):hs[s]=max(hs[s],ell*hs[s-1]/k)
            H=sum(hs)
            if H>F(1,16):hs=[v*F(1,16)/H for v in hs];H=F(1,16)
            y=(d+ell*F(rng.randrange(1,100),100))*hs[0] if j==0 else k*hs[0]*F(rng.randrange(1,100),100)
            src=y if j==0 else ell*hs[j-1]
            assert d*hs[j]<src<=k*hs[j]
            hh=hs[:j]+[hs[j]+hs[j+1]]+hs[j+2:]
            # exact physical comparison, including nonproductive later actions
            old=C(k,ell,H,hs,y);new=C(k,ell,H,hh,y)
            assert new-old <=-k*hs[j]*hs[j+1]/F(4),(m,j,new-old)
            counts['exact_full_suffix_comparisons']+=1
            if any(k*hh[s]<ell*hh[s-1] for s in range(1,len(hh))):
                counts['postmerge_nonproductive_suffixes']+=1
                if len(examples)<4:examples.append({'m':m,'index':j+1,'decrease':str(old-new)})
print(json.dumps({'status':'PASS','counts':counts,'postmerge_nonproductive_examples':examples,
                   'scope':'fraction identities and independent synthetic-affine physical suffix checks; geometry/exterior proof is analytic'},indent=2))
