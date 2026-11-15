#!/usr/bin/env python3
"""Exact finite-support response tools. Arithmetic uses Fraction throughout.
The structural proofs and scope are in REDUCTION.md.
"""
from fractions import Fraction as Q
from itertools import combinations
from math import inf


def normalize(path):
    out=[]
    for t,x in path:
        t,x=Q(t),Q(x)
        if out and t==out[-1][0]:
            assert x==out[-1][1], 'conflicting vertices'
        else:
            assert not out or t>out[-1][0]
            out.append((t,x))
    assert out and out[0][0]==0
    return out


def position(path,t):
    t=Q(t)
    for (a,x),(b,y) in zip(path,path[1:]):
        if a<=t<=b:return x+(y-x)*(t-a)/(b-a)
    assert t>=path[-1][0]
    return path[-1][1]


def admissible(path):
    p=normalize(path)
    return all(-1<=x<=1 for _,x in p) and all(abs(y-x)<=b-a for (a,x),(b,y) in zip(p,p[1:]))


def simplify(path):
    out=[]
    for t,x in normalize(path):
        out.append((t,x))
        while len(out)>=3:
            (a,x),(b,y),(c,z)=out[-3:]
            if (y-x)*(c-b)==(z-y)*(b-a):out.pop(-2)
            else:break
    return out


def first_meeting(p,q):
    ts=sorted({t for t,_ in p}|{t for t,_ in q})
    for a,b in zip(ts,ts[1:]):
        da=position(p,a)-position(q,a)
        db=position(p,b)-position(q,b)
        if da==0:return a
        if da*db<=0:return a+(b-a)*abs(da)/(abs(da)+abs(db))
    if position(p,ts[-1])==position(q,ts[-1]):return ts[-1]
    return None


def ray_hit(path,t,x,direction):
    """First meeting of an unreflected unit-speed ray and a hider ahead.
    Returns None if the hider is strictly behind the ray's starting point.
    Hider inputs have constant tails after their last listed vertex.
    """
    t,x=Q(t),Q(x);d=Q(direction)
    y=position(path,t)
    if y==x:return t
    if (y-x)*d<0:return None
    wall=t+(Q(1)-x if d==1 else x+1)
    knots=sorted({t,wall}|{s for s,_ in path if t<s<wall})
    for a,b in zip(knots,knots[1:]):
        da=position(path,a)-(x+d*(a-t))
        db=position(path,b)-(x+d*(b-t))
        if da==0:return a
        if da*db<=0:return a+(b-a)*abs(da)/(abs(da)+abs(db))
    assert position(path,wall)==x+d*(wall-t)
    return wall


def monster_best_response(hiders,weights):
    """Exhaust all next-capture direction cases with exact arithmetic.

    No numerical optimizer, pruning tolerance, or assumed turn bound is used.
    The theorem supplies the bound: each segment captures a new hider.
    """
    hs=[normalize(p) for p in hiders];ws=list(map(Q,weights));n=len(hs)
    assert n==len(ws) and n>0 and all(w>=0 for w in ws) and sum(ws)==1
    assert all(admissible(p) for p in hs)
    full=(1<<n)-1;states=0;leaves=0;best=None;bestpath=None;bestcaptures=None
    def walk(mask,t,x,captures,path):
        nonlocal states,leaves,best,bestpath,bestcaptures
        states+=1
        for j,h in enumerate(hs):
            if not(mask>>j&1) and position(h,t)==x:
                mask|=1<<j;captures[j]=t
        if mask==full:
            leaves+=1;value=sum(w*s for w,s in zip(ws,captures))
            if best is None or value<best:
                best=value;bestpath=path.copy();bestcaptures=captures.copy()
            return
        for d in (-1,1):
            hits=[ray_hit(h,t,x,d) for j,h in enumerate(hs) if not(mask>>j&1)]
            hits=[s for s in hits if s is not None]
            if not hits:continue
            s=min(hits);assert s>t
            y=x+d*(s-t)
            walk(mask,s,y,captures.copy(),path+[(s,y)])
    starts=sorted({h[0][1] for h in hs})
    for x in starts:walk(0,Q(0),x,[None]*n,[(Q(0),x)])
    assert best is not None
    checked=[first_meeting(bestpath,h) for h in hs]
    assert checked==bestcaptures
    return {'value':best,'path':simplify(bestpath),'captures':bestcaptures,
            'states':states,'leaves':leaves,'initial_positions':len(starts),
            'universal_leaf_bound':n*2**(n-1)}
