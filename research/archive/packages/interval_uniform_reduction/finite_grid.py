"""Finite path game used in the uniform approximation theorem.
The verifier uses only integer arithmetic and fractions. Discovery imports SciPy.
"""
from __future__ import annotations
from fractions import Fraction as F
from itertools import product
import json,sys

def paths(K:int,N:int,monster:bool=False):
    out=[]
    if monster:
        def walk(p):
            if len(p)==2*N+1:out.append(p);return
            for d in(-1,1):
                x=p[-1]+d
                if 0<=x<=2*K:walk(p+[x])
        for j in range(K+1):walk([2*j])
    else:
        def walk(p):
            if len(p)==N+1:
                q=[]
                for a,b in zip(p,p[1:]):q.extend([2*a,a+b])
                out.append(q+[2*p[-1]]);return
            for d in(-1,0,1):
                x=p[-1]+d
                if 0<=x<=K:walk(p+[x])
        for j in range(K+1):walk([j])
    return out

def payoff(h,m):
    for i,(a,b)in enumerate(zip(h,m)):
        if a==b:return i
        if i and (h[i-1]-m[i-1])*(a-b)<0:raise AssertionError('Unexpected off-lattice crossing')
    return len(h)-1

def discover(K=4,N=4):
    import numpy as np
    from scipy.optimize import linprog
    hs=paths(K,N);ms=paths(K,N,True);A=np.array([[payoff(h,m)for m in ms]for h in hs],float)
    s=linprog(np.r_[np.zeros(len(ms)),1],A_ub=np.c_[A,-np.ones(len(hs))],b_ub=np.zeros(len(hs)),A_eq=[np.r_[np.ones(len(ms)),0]],b_eq=[1],bounds=[(0,None)]*len(ms)+[(None,None)],method='highs')
    assert s.success
    wi=[i for i,w in enumerate(s.x[:-1])if w>1e-8];qi=[i for i,w in enumerate(-s.ineqlin.marginals)if w>1e-8]
    for den in(10**3,10**6,10**9):
        w=[F(float(s.x[i])).limit_denominator(den)for i in wi];q=[F(float(-s.ineqlin.marginals[i])).limit_denominator(den)for i in qi];c=F(float(s.x[-1])).limit_denominator(den)
        if sum(w)!=1 or sum(q)!=1:continue
        if all(sum(a*int(A[i,j])for a,j in zip(w,wi))<=c for i in range(len(hs))) and all(sum(a*int(A[i,j])for a,i in zip(q,qi))>=c for j in range(len(ms))):break
    else:raise RuntimeError('Rational reconstruction did not certify')
    d=dict(K=K,N=N,hider_count=len(hs),monster_count=len(ms),value_time=str(c/F(K)),value_ticks=str(c),hiders=[dict(path=hs[i],weight=str(a))for i,a in zip(qi,q)],monsters=[dict(path=ms[i],weight=str(a))for i,a in zip(wi,w)])
    json.dump(d,open('grid_case.json','w'),indent=2);return d

def verify(file='grid_case.json'):
    d=json.load(open(file));K,N=d['K'],d['N'];hs=paths(K,N);ms=paths(K,N,True);c=F(d['value_ticks'])
    assert len(hs)==d['hider_count'] and len(ms)==d['monster_count']
    q=[F(a['weight'])for a in d['hiders']];w=[F(a['weight'])for a in d['monsters']]
    assert sum(q)==sum(w)==1 and min(q+w)>0
    assert all(a['path']in hs for a in d['hiders']) and all(a['path']in ms for a in d['monsters'])
    upper=max(sum(b*payoff(h,a['path'])for a,b in zip(d['monsters'],w))for h in hs)
    lower=min(sum(b*payoff(a['path'],m)for a,b in zip(d['hiders'],q))for m in ms)
    assert upper==lower==c and F(d['value_time'])==c/K
    print('PASS: exhaustive finite-grid saddle certificate:',c/K,'hiders',len(hs),'monsters',len(ms))
    return d
if __name__=='__main__':
    if '--discover'in sys.argv:print(discover())
    verify()
