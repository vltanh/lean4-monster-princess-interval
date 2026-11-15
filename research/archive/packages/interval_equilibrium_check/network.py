#!/usr/bin/env python3
"""Verify a universal Princess--Monster upper-bound certificate.
Only the Python standard library is required. No optimizer is used.
Run: python verify.py
The mathematical reduction is proved in PROOF.md.
"""
import gzip
import argparse
from fractions import Fraction as Q
from math import lcm
from pathlib import Path
import json

H=Q(4)

def path(kind,x,sign=1):
    x=Q(x)
    if kind==1:
        t=[Q(0),1-x,3-x,H]; y=[x,Q(1),Q(-1),Q(-1)]
    elif kind==2:
        u=(1-x)/2
        t=[Q(0),u,Q(2),H];y=[x,x+u,Q(-1),Q(1)]
    else:raise ValueError('Unknown monster family')
    # All starts used below are <1, so no zero-length initial segment.
    out=[]
    for a,b in zip(t,y):
        if out and a==out[-1][0]:out[-1]=(a,sign*b)
        else:out.append((a,sign*b))
    return out

def pos(p,t):
    for (a,x),(b,y) in zip(p,p[1:]):
        if a<=t<=b:return x+(y-x)*(t-a)/(b-a)
    raise ValueError((p,t))

def first_meeting(p,q):
    ts=sorted(set([t for t,_ in p]+[t for t,_ in q]))
    for a,b in zip(ts,ts[1:]):
        da=pos(p,a)-pos(q,a);db=pos(p,b)-pos(q,b)
        if da==0:return a
        if da*db<=0:return a+(b-a)*abs(da)/(abs(da)+abs(db))
    if pos(p,ts[-1])==pos(q,ts[-1]):return ts[-1]
    return None

def build(spec,initial):
    den=spec['weight_denominator']
    ms=[];wn=[]
    for item in spec['families']:
        k,x,w=item['kind'],Q(item['start']),item['weight_numerator']
        ms.extend([path(k,x,1),path(k,x,-1)]);wn.extend([w,w])
    N=len(ms);B={i for i,m in enumerate(ms) if m[0][1]<initial}
    A=set(range(N))-B
    events=[]
    for i in B:
        for j in A:
            t=first_meeting(ms[i],ms[j])
            if t is not None and t<H:events.append((i,j,t))
    deadlines={}
    for i in range(N):
        wall=Q(1) if i in B else Q(-1)
        deadlines[i]=first_meeting(ms[i],[(Q(0),wall),(H,wall)])
        assert deadlines[i] is not None
    ts=sorted(set([Q(0),H]+[e[2] for e in events]+list(deadlines.values())))
    K=len(ts)-1;idx={t:k for k,t in enumerate(ts)}
    scale=2*den*lcm(*[(b-a).denominator for a,b in zip(ts,ts[1:])])
    source=N*K;sink=source+1
    edges={}
    def add(u,v,c):
        assert c.denominator==1 if isinstance(c,Q) else True
        edges[(u,v)]=edges.get((u,v),0)+int(c)
    node=lambda i,k:i*K+k
    for i in range(N):
        for k,(a,b) in enumerate(zip(ts,ts[1:])):
            c=Q(wn[i],2*den)*(b-a)*scale
            if i in B:add(source,node(i,k),c)
            else:add(node(i,k),sink,c)
        for k in range(K-1):
            if i in B:add(node(i,k+1),node(i,k),H*scale)
            else:add(node(i,k),node(i,k+1),H*scale)
        d=deadlines[i]
        if d<H:
            if i in B:add(node(i,idx[d]),sink,H*scale)
            else:add(source,node(i,idx[d]),H*scale)
    for i,j,t in events:add(node(i,idx[t]),node(j,idx[t]),H*scale)
    return edges,source,sink,scale,ts
