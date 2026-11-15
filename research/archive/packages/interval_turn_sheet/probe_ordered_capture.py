#!/usr/bin/env python3
"""Find attacking monster routes against supplied ordered polygonal hiders.

This is a floating-point discovery tool, not an exact response certificate.
It enumerates capture orders, retaining a time/cost Pareto frontier. A node
or wall-time cap may stop enumeration; the returned route remains a legal
response and is independently evaluated by segment intersections.

Input: {"times": [...], "positions": [[...], ...], "weights": [...]}.
Each position row is one hider, in increasing spatial order. Optional
"reflect": true prepends the reversed reflected paths with equal weights.
The final positions are held fixed. No princess-rank sampling is performed
by this module: the input is a finite law, possibly extracted elsewhere
from a continuous field. Its minimum is not a continuous-law guarantee.
"""
from __future__ import annotations

import argparse
from bisect import bisect_left, bisect_right
import json
import math
from pathlib import Path
import sys
import time


class Polygon:
    def __init__(self, times, positions, weight=1.):
        self.t = tuple(map(float, times))
        self.x = tuple(map(float, positions))
        self.weight = float(weight)
        if not self.t or self.t[0] != 0 or len(self.t) != len(self.x):
            raise ValueError('Invalid polygon dimensions or initial time')
        self.slopes = []
        for i in range(len(self.t)-1):
            dt = self.t[i+1]-self.t[i]
            if dt <= 0:
                raise ValueError('Times must strictly increase')
            v = (self.x[i+1]-self.x[i])/dt
            if abs(v) > 1+2e-9:
                raise ValueError('Hider speed exceeds one')
            self.slopes.append(max(-1., min(1., v)))
        if any(abs(x) > 1+1e-9 for x in self.x) or self.weight <= 0:
            raise ValueError('Invalid position or weight')
        self.seq = {}
        for d in (-1,1):
            sequence=[]
            for t,x in zip(self.t,self.x):
                z=t-d*x
                if sequence and abs(z-sequence[-1])<1e-10:z=sequence[-1]
                if sequence and z<sequence[-1]:
                    raise ValueError('Characteristic decreases')
                sequence.append(z)
            self.seq[d]=tuple(sequence)

    def at(self, t):
        i = min(len(self.t)-1, max(0,bisect_right(self.t,t)-1))
        return self.x[i] if i == len(self.t)-1 else self.x[i]+self.slopes[i]*(t-self.t[i])

    def inverse(self, z, d):
        seq = self.seq[d]
        i = bisect_left(seq,z)
        if i == 0:
            return 0.
        if i == len(seq):
            return self.t[-1]+z-seq[-1]
        den = 1-d*self.slopes[i-1]
        if den <= 1e-14:
            # A zero characteristic interval is hit at its first endpoint.
            return self.t[i-1]
        return self.t[i-1]+(z-seq[i-1])/den

    def hit(self,t,x,d):
        return max(t,self.inverse(t-d*x,d))


class InversePrefix:
    """Piecewise-affine weighted inverse sums for a rigorous-form lower bound.

    Arithmetic here is floating point; it accelerates discovery only.
    The inverse is evaluated at its first-touch value at every breakpoint.
    """
    def __init__(self, paths, d):
        self.z = sorted(set(z for p in paths for z in p.seq[d]))
        self.values, self.slopes, self.intercepts = [], [], []
        for z in self.z:
            values=[0.]; slopes=[0.]; intercepts=[0.]
            for p in paths:
                tm=p.inverse(z,d); seq=p.seq[d]; i=bisect_right(seq,z)
                if i == 0:
                    a=b=0.
                elif i == len(seq):
                    a=1.; b=p.t[-1]-seq[-1]
                else:
                    den=1-d*p.slopes[i-1]
                    if den <= 1e-14:
                        raise ValueError('Non-increasing characteristic in prefix')
                    a=1/den; b=p.t[i-1]-a*seq[i-1]
                values.append(values[-1]+p.weight*tm)
                slopes.append(slopes[-1]+p.weight*a)
                intercepts.append(intercepts[-1]+p.weight*b)
            self.values.append(values); self.slopes.append(slopes); self.intercepts.append(intercepts)

    def value(self,z,left,right):
        if left == right:
            return 0.
        i=bisect_left(self.z,z)
        if i < len(self.z) and self.z[i] == z:
            row=self.values[i]
            return row[right]-row[left]
        if i == 0:
            return 0.
        a,b=self.slopes[i-1],self.intercepts[i-1]
        return (a[right]-a[left])*z+b[right]-b[left]


def direct_capture(route,path):
    """Independent first segment intersection; no characteristic inverses."""
    def monster_at(t):
        i=bisect_right([v[0] for v in route],t)-1
        if i < 0:return route[0][1]
        if i+1 == len(route):return route[-1][1]
        a,x=route[i]; b,y=route[i+1]
        return x+(y-x)*(t-a)/(b-a)
    times=sorted(set([v[0] for v in route]+list(path.t)))
    previous=None
    for t in times:
        delta=monster_at(t)-path.at(t)
        if abs(delta) <= 2e-10:
            return t
        if previous is not None:
            a,b=previous
            if b*delta < 0:
                return a+(t-a)*abs(b)/(abs(b)+abs(delta))
        previous=t,delta
    return math.inf


def solve(paths, *, node_limit=200000, seconds=45., symmetry=False):
    n=len(paths)
    if not paths:
        raise ValueError('Empty law')
    for a,b in zip(paths,paths[1:]):
        if any(a.at(t)>b.at(t)+2e-9 for t in sorted(set(a.t+b.t))):
            raise ValueError('Paths are not ordered')
    if symmetry:
        for a,b in zip(paths,paths[::-1]):
            if abs(a.weight-b.weight)>1e-10 or any(abs(a.at(t)+b.at(t))>1e-9 for t in set(a.t+b.t)):
                raise ValueError('Reflection symmetry was not supplied')
    sys.setrecursionlimit(max(2000,4*n+100))
    start=time.monotonic(); weight=sum(p.weight for p in paths)
    best=sum(p.weight*p.hit(0.,-1.,1) for p in paths)
    best_route=[[0.,-1.],[2.,1.]]
    memo={}; route=[]
    stats=dict(nodes=0,leaves=0,dominated=0,bounded=0,complete=True)
    prefix={d:InversePrefix(paths,d) for d in (-1,1)}
    class Cap(Exception):pass

    def walk(left,right,anchor,t,x,cost):
        nonlocal best,best_route
        stats['nodes']+=1
        if stats['nodes']>node_limit or (stats['nodes']%256==0 and time.monotonic()-start>seconds):
            raise Cap
        while left>0 and abs(paths[left-1].at(t)-x)<=1e-11:
            left-=1; cost+=paths[left].weight*t
        while right+1<n and abs(paths[right+1].at(t)-x)<=1e-11:
            right+=1; cost+=paths[right].weight*t
        if left==0 and right==n-1:
            stats['leaves']+=1
            if cost<best:
                best=cost; best_route=[list(z) for z in route]
            return
        key=left,right,anchor; records=memo.get(key,[])
        if any(a<=t-1e-11 and b<=cost-1e-11 for a,b in records):
            stats['dominated']+=1; return
        memo[key]=[(a,b)for a,b in records if not(t<a-1e-11 and cost<b-1e-11)]+[(t,cost)]
        lower=cost+prefix[-1].value(t+x,0,left)+prefix[1].value(t-x,right+1,n)
        if lower>best+1e-9*weight:
            stats['bounded']+=1; return
        choices=[]
        if left>0: choices.append((paths[left-1].hit(t,x,-1),left-1,-1))
        if right+1<n: choices.append((paths[right+1].hit(t,x,1),right+1,1))
        choices.sort()
        for nt,j,d in choices:
            nx=x+d*(nt-t)
            if abs(nx)>1+1e-8:
                raise ValueError('Computed route leaves interval')
            route.append((nt,nx))
            walk(min(left,j),max(right,j),j,nt,nx,cost+paths[j].weight*nt)
            route.pop()

    try:
        for i,p in enumerate(paths):
            if symmetry and p.x[0]<-1e-12:continue
            if i and abs(p.x[0]-paths[i-1].x[0])<1e-12:continue
            route[:]=[(0.,p.x[0])]
            walk(i,i,i,0.,p.x[0],0.)
    except Cap:
        stats['complete']=False
    actual=sum(p.weight*direct_capture(best_route,p)for p in paths)/weight
    if not math.isfinite(actual) or abs(actual-best/weight)>2e-8:
        raise ArithmeticError('Independent direct capture differs from search')
    simplified=[]
    for point in best_route:
        if simplified and abs(point[0]-simplified[-1][0])<1e-12:continue
        while len(simplified)>1:
            a,x=simplified[-2];b,y=simplified[-1];c,z=point
            if abs((y-x)*(c-b)-(z-y)*(b-a))>1e-10:break
            simplified.pop()
        simplified.append(point)
    return dict(scope='Floating discovery response to a finite ordered law; not an exact or continuous-law certificate.',
                value=actual,route=simplified,stats=stats,seconds=time.monotonic()-start,hiders=n)


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('input',type=Path)
    ap.add_argument('--output',type=Path)
    ap.add_argument('--nodes',type=int,default=200000)
    ap.add_argument('--seconds',type=float,default=45.)
    args=ap.parse_args(); data=json.loads(args.input.read_text())
    times=data['times']; xs=data['positions']; ws=data.get('weights',[1.]*len(xs))
    if data.get('reflect'):
        xs=[[-x for x in row]for row in xs[::-1]]+xs
        ws=list(ws[::-1])+list(ws)
    paths=[Polygon(times,row,w)for row,w in zip(xs,ws)]
    result=solve(paths,node_limit=args.nodes,seconds=args.seconds,symmetry=bool(data.get('reflect')))
    if args.output:args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
