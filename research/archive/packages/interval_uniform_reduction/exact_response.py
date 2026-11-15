"""Exact response of an unrestricted monster to ordered, symmetric finite hiders.
Only Python's standard library is required. No floating-point pruning is used.
"""
from __future__ import annotations
from bisect import bisect_left, bisect_right
from fractions import Fraction
from dataclasses import dataclass
from collections import defaultdict
import argparse,json,time,sys

@dataclass
class Path:
    t:list[int]
    x:list[int]
    slope:list[int]
    seq:tuple[list[int],list[int]]
    weight:int
    def at(self,t:int)->int:
        k=bisect_right(self.t,t)-1
        return self.x[k] if k+1==len(self.t) else self.x[k]+self.slope[k]*(t-self.t[k])
    def hit(self,t:int,x:int,d:int)->int:
        q=t-d*x;seq=self.seq[(d+1)//2];k=bisect_left(seq,q)
        if k==len(seq):a=self.t[-1]+q-seq[-1]
        elif k==0:a=t
        else:
            den=1-d*self.slope[k-1];num=q-seq[k-1]
            if den<=0 or num%den:raise ValueError('Insufficient coordinate scale')
            a=self.t[k-1]+num//den
        if a<t:raise ValueError('Capture would be in the past')
        return a

def build_paths(raw:list[list[list[int]]],weights:list[int],scale:int)->list[Path]:
    if len(raw)!=len(weights) or not raw or scale<=0:raise ValueError('Invalid dimensions')
    ps=[]
    for p,w in zip(raw,weights):
        if not isinstance(w,int) or w<=0:raise ValueError('Weights must be positive integers')
        if not p or p[0][0]!=0:raise ValueError('Every path must start at time zero')
        ts=[];xs=[];sl=[]
        for t,x in p:
            if not isinstance(t,int) or not isinstance(x,int) or t<0 or abs(x)>scale:raise ValueError('Invalid vertex')
            ts.append(t);xs.append(x)
        for (a,x),(b,y) in zip(p,p[1:]):
            if b<=a or y-x not in (0,b-a,a-b):raise ValueError('Invalid speed or time order')
            sl.append((y-x)//(b-a))
        ps.append(Path(ts,xs,sl,([t+x for t,x in p],[t-x for t,x in p]),w))
    for a,b in zip(ps,ps[1:]):
        if any(a.at(t)>b.at(t) for t in a.t+b.t):raise ValueError('Hider paths cross')
    for a,b in zip(ps,ps[::-1]):
        if a.weight!=b.weight or any(a.at(t)!=-b.at(t) for t in a.t+b.t):raise ValueError('Reflection symmetry fails')
    return ps

class Prefix:
    """Exact weighted generalized-inverse sums; factor two clears slopes 1/2."""
    def __init__(self,ps:list[Path],d:int):
        self.q=sorted(set(z for p in ps for z in p.seq[(d+1)//2]));self.at=[];self.aa=[];self.bb=[]
        for z in self.q:
            ats=[0];aas=[0];bbs=[0]
            for p in ps:
                seq=p.seq[(d+1)//2];b=bisect_left(seq,z)
                if b==len(seq):tm2=2*(p.t[-1]+z-seq[-1])
                elif b==0:tm2=0
                else:
                    den=1-d*p.slope[b-1];assert den in (1,2)
                    tm2=2*p.t[b-1]+(2//den)*(z-seq[b-1])
                b=bisect_right(seq,z)
                if b==len(seq):a=2;c=2*(p.t[-1]-seq[-1])
                elif b==0:a=c=0
                else:
                    den=1-d*p.slope[b-1];assert den in (1,2)
                    a=2//den;c=2*p.t[b-1]-a*seq[b-1]
                ats.append(ats[-1]+p.weight*tm2);aas.append(aas[-1]+p.weight*a);bbs.append(bbs[-1]+p.weight*c)
            self.at.append(ats);self.aa.append(aas);self.bb.append(bbs)
    def eval(self,z:int,l:int,r:int)->int:
        if l==r:return 0
        k=bisect_left(self.q,z)
        if k<len(self.q) and self.q[k]==z:return self.at[k][r]-self.at[k][l]
        if not k:return 0
        k-=1;return (self.aa[k][r]-self.aa[k][l])*z+self.bb[k][r]-self.bb[k][l]

def solve(raw,weights,scale,*,cached=True,prune=True,node_limit=10**9):
    ps=build_paths(raw,weights,scale);n=len(ps);sys.setrecursionlimit(max(2000,n+100))
    best=sum(2*p.weight*p.hit(0,-scale,1) for p in ps);bestpath=[[0,-scale],[2*scale,scale]]
    route=[];memo=defaultdict(list);stats=dict(nodes=0,leaves=0,dominated=0,bounded=0)
    cache=[Prefix(ps,-1),Prefix(ps,1)] if cached and prune else None
    def walk(l,r,anchor,t,x,cost):
        nonlocal best,bestpath
        stats['nodes']+=1
        if stats['nodes']>node_limit:raise RuntimeError('Node limit reached; no completed certificate')
        while l>0 and ps[l-1].at(t)==x:l-=1;cost+=2*ps[l].weight*t
        while r+1<n and ps[r+1].at(t)==x:r+=1;cost+=2*ps[r].weight*t
        if l==0 and r==n-1:
            stats['leaves']+=1
            if cost<best:best=cost;bestpath=[list(z)for z in route]
            return
        if prune:
            key=(l,r,anchor);vv=memo[key]
            if any(a<=t and c<=cost for a,c in vv):stats['dominated']+=1;return
            memo[key]=[(a,c)for a,c in vv if not(t<=a and cost<=c)]+[(t,cost)]
            if cache:lb=cost+cache[0].eval(t+x,0,l)+cache[1].eval(t-x,r+1,n)
            else:lb=cost+sum(2*ps[j].weight*ps[j].hit(t,x,-1)for j in range(l))+sum(2*ps[j].weight*ps[j].hit(t,x,1)for j in range(r+1,n))
            if lb>=best:stats['bounded']+=1;return
        a=ps[l-1].hit(t,x,-1) if l>0 else None;b=ps[r+1].hit(t,x,1) if r+1<n else None
        choices=[]
        if a is not None:choices.append((a,l-1,-1))
        if b is not None:choices.append((b,r+1,1))
        choices.sort(key=lambda z:(z[0],-z[2]))
        for nt,j,d in choices:
            nx=x+d*(nt-t);route.append((nt,nx));walk(min(l,j),max(r,j),j,nt,nx,cost+2*ps[j].weight*nt);route.pop()
    for i,p in enumerate(ps):
        if p.x[0]<0 or i and p.x[0]==ps[i-1].x[0]:continue
        route[:]=[(0,p.x[0])];walk(i,i,i,0,p.x[0],0)
    return Fraction(best,2*sum(weights)*scale),bestpath,stats

def capture(m:list[list[int]],p:list[list[int]])->Fraction:
    """Separate Fraction-based segment-intersection check, not the search hit routine."""
    def at(q,t):
        for (a,x),(b,y)in zip(q,q[1:]):
            if a<=t<=b:return Fraction(x)+Fraction((y-x)*(t-a),b-a)
        return Fraction(q[-1][1])
    ts=sorted(set(t for t,x in m+p));old=None
    for t in ts:
        d=at(m,t)-at(p,t)
        if d==0:return Fraction(t)
        if old:
            a,e=old
            if d*e<0:return Fraction(a)+Fraction(t-a)*abs(e)/(abs(e)+abs(d))
        old=(t,d)
    raise ValueError('No capture of a listed hider')

def main():
    ap=argparse.ArgumentParser();ap.add_argument('file');ap.add_argument('--naive',action='store_true');args=ap.parse_args()
    d=json.load(open(args.file));hs=d['paths_h'];ws=d['weights_h'];S=d['S']
    raw=[[[t,-x]for t,x in p]for p in hs[::-1]]+hs;weights=ws[::-1]+ws
    start=time.time();v,m,stats=solve(raw,weights,S,cached=not args.naive)
    assert v==Fraction(d['value']),(v,d['value'])
    actual=sum(w*capture(m,p) for w,p in zip(weights,raw))/(sum(weights)*S)
    supplied=sum(w*capture(d['attaining_monster'],p)for w,p in zip(weights,raw))/(sum(weights)*S)
    assert actual==supplied==v
    print('PASS: exact unrestricted response =',v);print('Decimal (display only):',float(v));print('Search:',stats);print('Seconds:',time.time()-start)
if __name__=='__main__':main()
