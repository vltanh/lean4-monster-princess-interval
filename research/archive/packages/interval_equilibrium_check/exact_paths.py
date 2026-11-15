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


def tail_cone(path,deadline,H,direction):
    """Retain path through deadline, then continue with slope direction."""
    d=Q(deadline);H=Q(H)
    out=[(t,x) for t,x in path if t<d]
    x=position(path,d)
    out.append((d,x))
    if d<H:out.append((H,x+direction*(H-d)))
    return normalize(out)


def envelope_knots(curves,H):
    ts=sorted({Q(0),Q(H)}|{t for p in curves for t,_ in p if t<=H})
    cuts=set(ts)
    for a,b in zip(ts,ts[1:]):
        va=[position(p,a) for p in curves]
        vb=[position(p,b) for p in curves]
        for i,j in combinations(range(len(curves)),2):
            d=va[i]-va[j];e=vb[i]-vb[j]
            if d*e<0:cuts.add(a+(b-a)*abs(d)/(abs(d)+abs(e)))
    return cuts


def princess_witness(monsters,targets,initial,delta,H):
    """Construct a 1-Lipschitz witness to feasible capture deadlines.

    It stays in the given open initial chamber. For every i,
    T(monsters[i],p)>max(targets[i]-delta,0), except that the
    weaker T>=target-delta is used by callers when target=0.
    """
    monsters=[normalize(p) for p in monsters]
    targets=list(map(Q,targets));initial=Q(initial);delta=Q(delta);H=Q(H)
    assert delta>0 and len(monsters)==len(targets)
    assert all(admissible(p) for p in monsters)
    assert all(p[0][1]!=initial for p in monsters)
    below=[p[0][1]<initial for p in monsters]
    lows=[[(Q(0),Q(-1)),(H,Q(-1))]]
    ups=[[(Q(0),Q(1)),(H,Q(1))]]
    for m,r,b in zip(monsters,targets,below):
        assert 0<=r<=H
        curve=tail_cone(m,max(Q(0),r-delta),H,-1 if b else 1)
        (lows if b else ups).append(curve)
    ts=sorted(envelope_knots(lows,H)|envelope_knots(ups,H))
    L0=max(position(q,Q(0)) for q in lows)
    U0=min(position(q,Q(0)) for q in ups)
    blend=(initial-L0)/(U0-L0)
    assert 0<blend<1
    p=[];gaps=[]
    for t in ts:
        L=max(position(q,t) for q in lows)
        U=min(position(q,t) for q in ups)
        assert L<U,('empty corridor',t,L,U)
        p.append((t,(1-blend)*L+blend*U));gaps.append(U-L)
    p=simplify(p)
    assert admissible(p) and p[0][1]==initial
    for m,b in zip(monsters,below):assert (m[0][1]<p[0][1])==b
    captures=[first_meeting(m,p) for m in monsters]
    assert all(t is not None and t>=r-delta for t,r in zip(captures,targets))
    return p,captures,min(gaps)


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
