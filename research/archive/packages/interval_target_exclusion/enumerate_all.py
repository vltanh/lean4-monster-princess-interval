#!/usr/bin/env python3
"""Exact enumeration of ALL minimizing capture-order paths for this input.

No scientific Python, solver, native compiler, or floating point is required.
The exhaustive capture-order reduction is explained in the accompanying proof.
Only strict exact lower-bound pruning is used. No dominance pruning is used.
"""
from __future__ import annotations
from bisect import bisect_right, bisect_left
from fractions import Fraction
from math import lcm
from pathlib import Path
import argparse, json, time

class PathData:
    def __init__(self, vertices, mass: int, scale: int):
        self.t=[int(Fraction(t)*scale) for t,x in vertices]
        self.x=[int(Fraction(x)*scale) for t,x in vertices]
        self.mass=mass
        assert self.t[0]==0
        self.slope=[]
        for i in range(len(self.t)-1):
            dt=self.t[i+1]-self.t[i];dx=self.x[i+1]-self.x[i]
            assert dt>0 and dx in (-dt,0,dt)
            self.slope.append(dx//dt)
        self.slope.append(0)
        self.minus=[t-x for t,x in zip(self.t,self.x)]
        self.plus=[t+x for t,x in zip(self.t,self.x)]
    def pos(self,t:int)->int:
        k=bisect_right(self.t,t)-1
        return self.x[k]+self.slope[k]*(t-self.t[k])
    def intercept(self,t:int,x:int,d:int)->int:
        """First encounter of ray x+d(s-t) with this known path."""
        q=t-d*x; seq=self.minus if d==1 else self.plus
        k=bisect_left(seq,q)
        if k==len(seq):
            h=self.t[-1]+q-seq[-1]
        elif k==0:
            h=self.t[0]
        else:
            slope=1-d*self.slope[k-1]
            assert slope>0
            delta=q-seq[k-1]
            assert delta%slope==0, 'Increase the integer time scale.'
            h=self.t[k-1]+delta//slope
        assert h>=t
        return h

def verify(data:dict)->dict:
    den=lcm(*(Fraction(z).denominator for p in data['paths'] for v in p for z in v))
    scale=2*den
    weightden=lcm(*(Fraction(w).denominator for w in data['weights']))
    ps=[PathData(v,int(Fraction(w)*weightden),scale) for v,w in zip(data['paths'],data['weights'])]
    n=len(ps);full=(1<<n)-1
    assert sum(p.mass for p in ps)==weightden
    assert all(p.mass>0 and all(-scale<=x<=scale for x in p.x) for p in ps)
    nodes=leaves=lb_prunes=dominance_prunes=0
    best=None;bestpath=None;memo={};minpaths=[]
    def walk(mask:int,t:int,x:int,cost:int,anchor:int,route:list):
        nonlocal nodes,leaves,lb_prunes,dominance_prunes,best,bestpath,minpaths
        nodes+=1
        for j,p in enumerate(ps):
            if not (mask>>j)&1 and p.pos(t)==x:
                mask|=1<<j;cost+=p.mass*t;anchor=j
        if mask==full:
            leaves+=1
            if best is None or cost<best:best=cost;bestpath=route[:];minpaths=[route[:]]
            elif cost==best:minpaths.append(route[:])
            return
        lb=cost;nexts=[None,None]
        for j,p in enumerate(ps):
            if not (mask>>j)&1:
                y=p.pos(t);d=1 if y>x else -1
                h=p.intercept(t,x,d);lb+=p.mass*h
                k=(d+1)//2
                if nexts[k] is None or h<nexts[k][0]:nexts[k]=(h,j,d)
        if best is not None and lb>best:
            lb_prunes+=1;return
        for h,j,d in sorted(z for z in nexts if z is not None):
            y=x+d*(h-t)
            assert h>t and -scale<=y<=scale
            walk(mask,h,y,cost,j,route+[(h,y)])
    starts=sorted({p.x[0] for p in ps})
    start=time.perf_counter()
    for x in starts:walk(0,0,x,0,0,[(0,x)])
    value=Fraction(best,scale*weightden)
    return dict(value=str(value),nodes=nodes,leaves=leaves,lower_bound_prunes=lb_prunes,
                dominance_prunes=dominance_prunes,states=len(memo),initial_positions=len(starts),
                integer_time_scale=scale,weight_denominator=weightden,
                path=[[str(Fraction(t,scale)),str(Fraction(x,scale))] for t,x in bestpath],
                seconds=time.perf_counter()-start, minimizers=[[[str(Fraction(t,scale)),str(Fraction(x,scale))]for t,x in p]for p in minpaths])

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input',type=Path)
    parser.add_argument('--expect',default=None)
    args=parser.parse_args()
    result=verify(json.loads(args.input.read_text()))
    if args.expect is not None:assert Fraction(result['value'])==Fraction(args.expect)
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
