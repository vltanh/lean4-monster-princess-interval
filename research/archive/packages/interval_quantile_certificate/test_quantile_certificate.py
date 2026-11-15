#!/usr/bin/env python3
"""Independent exact small-law tests for the optional center-balance prune."""
from bisect import bisect_left,bisect_right
from fractions import Fraction as Q
import json
import os
from pathlib import Path
import random
import subprocess
import tempfile

from extract_quantiles import Field, extract, ROOT
from score_continuous_attack import supporting_plane


class Target:
    def __init__(self,path,weight):
        self.path=path;self.weight=weight
        self.t=[p[0] for p in path];self.x=[p[1] for p in path]
        self.v=[(b[1]-a[1])/(b[0]-a[0]) for a,b in zip(path,path[1:])]
        self.lines={d:[t-d*x for t,x in path] for d in (-1,1)}
    def at(self,t):
        k=bisect_right(self.t,t)-1
        return self.x[k] if k+1==len(self.t) else self.x[k]+self.v[k]*(t-self.t[k])
    def hit(self,t,x,d):
        q=t-d*x;z=self.lines[d];k=bisect_left(z,q)
        if k==len(z):return self.t[-1]+q-z[-1]
        if k==0:return t
        return self.t[k-1]+(q-z[k-1])/(1-d*self.v[k-1])


def exhaustive(targets):
    """Full next-capture tree: no Pareto, pursuit, or balance pruning."""
    full=(1<<len(targets))-1
    best=None;visited=0
    def walk(t,x,mask,cost):
        nonlocal best,visited
        visited+=1
        for i,p in enumerate(targets):
            if not(mask>>i&1) and p.at(t)==x:
                mask|=1<<i;cost+=p.weight*t
        if mask==full:
            best=cost if best is None else min(best,cost)
            return
        for d in (-1,1):
            hits=[p.hit(t,x,d) for i,p in enumerate(targets)
                  if not(mask>>i&1) and d*(p.at(t)-x)>0]
            if hits:
                at=min(hits);assert at>t
                walk(at,x+d*(at-t),mask,cost)
    for x in sorted({p.x[0] for p in targets if p.x[0]>=0}):
        walk(Q(0),x,0,Q(0))
    return best,visited


def capture(route,target):
    """Separate chronological segment intersection, without pursuit inverse."""
    def at(path,t):
        for (a,x),(b,y) in zip(path,path[1:]):
            if a<=t<=b:return x+(y-x)*(t-a)/(b-a)
        return path[-1][1]
    times=sorted({t for t,x in route+target.path})
    old=None
    for t in times:
        difference=at(route,t)-at(target.path,t)
        if difference==0:return t
        if old and old[1]*difference<0:
            return old[0]+(t-old[0])*old[1]/(old[1]-difference)
        old=t,difference
    raise AssertionError('uncaptured target')


def signed(radial,weights):
    total=2*sum(weights)
    return [Target([(t,-x) for t,x in p],Q(w,total))
            for p,w in reversed(list(zip(radial,weights)))] + \
           [Target(p,Q(w,total)) for p,w in zip(radial,weights)]


def text_input(targets):
    rows=[f'{len(targets)} 3']
    for p in targets:
        rows.append(' '.join([str(p.weight),str(len(p.path))]+[str(x) for pt in p.path for x in pt]))
    return '\n'.join(rows)+'\n'


def main():
    folder=Path(__file__).resolve().parent
    cases=[];rng=random.Random(20261114)
    for count in (2,3,4):
        for factors in ((1,1,1,1,1),(1,Q(3,4),Q(1,2),Q(3,4),1),
                        (1,Q(1,2),Q(3,4),Q(1,2),Q(3,4))):
            radial=[]
            for i in range(count):
                a=Q(i+1,count+1)
                route=[(Q(j,2),a*f) for j,f in enumerate(factors)]
                route.append((3-route[-1][1],Q(1)))
                radial.append(route)
            cases.append(signed(radial,[rng.randrange(1,8) for _ in radial]))
    cases.append(signed([[(Q(0),Q(1))]],[1]))
    data=json.loads((ROOT/'packages/interval_clock_grid/grid_n1_princess.json').read_text())
    field=Field(data)
    for k in (2,3,4):
        ranks,paths,stats=extract(field,k,True)
        assert stats['independent_midpoint_cdf_checks']>0
        cases.append(signed(paths,[1]*k))
    nodes=routes=0
    with tempfile.TemporaryDirectory(prefix='quantile_balance_test_') as td:
        td=Path(td);exe=td/'response';inp=td/'law.txt'
        subprocess.run(['g++','-O2','-std=c++17',str(folder/'center_balanced_response.cpp'),
                        '-lgmpxx','-lgmp','-o',str(exe)],check=True)
        for index,targets in enumerate(cases):
            expected,number=exhaustive(targets);nodes+=number
            inp.write_text(text_input(targets))
            values=[]
            for enabled in ('0','1'):
                env={**os.environ,'QUANTILE_CENTER_BALANCE':enabled}
                result=subprocess.run([str(exe),str(inp),'1000000'],env=env,
                                      capture_output=True,text=True,check=True)
                d=json.loads(result.stdout)
                assert d['complete'] and Q(d['value'])==expected,(index,enabled,d,expected)
                route=[tuple(map(Q,p)) for p in d['route']]
                assert sum(p.weight*capture(route,p) for p in targets)==expected
                values.append(d['value']);routes+=1
            assert values[0]==values[1]
        # The new prune must reject hypotheses it cannot certify.
        bad=[[(Q(0),Q(0)),(Q(2),Q(0)),(Q(3),Q(1))]], \
            [[(Q(0),Q(1,2)),(Q(5,2),Q(1,2)),(Q(3),Q(1))]], \
            [[(Q(0),Q(1,2)),(Q(1,2),Q(1)),(Q(3,4),Q(3,4)),(Q(1),Q(1))]]
        for radial in bad:
            inp.write_text(text_input(signed(radial,[1])))
            result=subprocess.run([str(exe),str(inp),'100'],
                env={**os.environ,'QUANTILE_CENTER_BALANCE':'1'},capture_output=True,text=True)
            assert result.returncode!=0

    # A concrete causal-clock plane is tight at its source field and an
    # upper plane at other legal fields on exactly the same P1 mesh.
    route=[(Q(0),Q(3,4)),(Q(1,8),Q(7,8)),(Q(2),Q(-1)),(Q(4),Q(1))]
    # The third time must preserve unit speed from the peak.
    route[2]=(Q(2),Q(-1));assert route[2][0]-route[1][0]==route[1][1]+1
    plane=supporting_plane(field,route)
    plane_checks=0
    for f in (Q(0),Q(1,3),Q(2,3),Q(1)):
        other={'n':1,'field_denominator':24,'radial_nodes':[]}
        for (j,k),v in field.pre.items():
            # Convex mix with the stationary uniform law through time2.
            value=f*Q(v,field.den)+(1-f)*Q(k,2)
            assert (24*value).denominator==1
            other['radial_nodes'].append([j,k,int(24*value)])
        g=Field(other)
        actual=supporting_plane(g,route)
        upper=Q(plane['constant'])+sum(Q(c)*Q(g.gnum(j,k),g.den)
                                     for j,k,c in plane['coefficients'])
        assert Q(actual['value'])<=upper
        plane_checks+=1
    print(json.dumps({'status':'PASS','exact_laws':len(cases),
                      'unpruned_fraction_states':nodes,'independent_route_replays':routes,
                      'hypothesis_rejections':len(bad),'supporting_plane_checks':plane_checks,
                      'scope':'Exact finite-law center-balance regression; not a new game bound.'},indent=2))


if __name__=='__main__':main()
