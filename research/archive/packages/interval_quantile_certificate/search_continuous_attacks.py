#!/usr/bin/env python3
"""Discover new physical attacks; optionally replay exact supporting planes.

Floating Powell searches are exploratory. Only the separate Fraction
scoring of a snapped rational route supplies an exact fixed-field attack.
No finite attack family certifies a Princess lower bound.
"""
from __future__ import annotations

import argparse
from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path
import time

import numpy as np
from scipy.optimize import minimize

from extract_quantiles import Field,coarse_field,read
from score_continuous_attack import supporting_plane


class FastField:
    def __init__(self,field):
        assert field.epsilon==Q(1,2)
        self.n=field.n;self.R=field.R;self.C=field.C
        self.table=np.zeros((self.C+1,self.R+1),dtype=np.float64)
        for (j,k),v in field.pre.items():self.table[j,k]=v/field.den

    def node(self,u,w):
        j=u+w;k=u-w
        foot=np.abs(k)-np.maximum(0,j-self.C)
        # A nonzero exact interpolation weight never uses an out-of-arena
        # node. Clipping here only absorbs floating endpoint roundoff.
        value=self.table[np.clip(j,0,self.C),np.clip(foot,0,self.R)]
        value=np.where(foot>0,value,0.0)
        return (1.0+np.sign(k)*value)*0.5

    def cdf(self,t,x):
        u=self.n*(np.asarray(t)+np.asarray(x));w=self.n*(np.asarray(t)-np.asarray(x))
        iu=np.floor(u).astype(np.int64);iw=np.floor(w).astype(np.int64)
        a=u-iu;b=w-iw
        same=((iu%(2*self.n)<self.n)==(iw%(2*self.n)<self.n))
        p00=np.where(same,1-np.maximum(a,b),np.maximum(0,1-a-b))
        p10=np.where(same,np.maximum(a-b,0),np.minimum(a,1-b))
        p01=np.where(same,np.maximum(b-a,0),np.minimum(b,1-a))
        p11=np.where(same,np.minimum(a,b),np.maximum(a+b-1,0))
        return p00*self.node(iu,iw)+p10*self.node(iu+1,iw)+p01*self.node(iu,iw+1)+p11*self.node(iu+1,iw+1)

    def leg(self,ta,xa,tb,xb,left,right):
        d=1 if xb>xa else -1
        fixed=ta-d*xa;za=ta+d*xa;zb=tb+d*xb
        frac=(self.n*fixed)%1
        k=np.arange(int(np.floor(self.n*za))-1,int(np.ceil(self.n*zb))+2,dtype=np.float64)
        cuts=np.unique(np.concatenate((k,k+frac,k+1-frac))/self.n)
        cuts=cuts[(cuts>za+1e-13)&(cuts<zb-1e-13)]
        cuts=np.concatenate(([za],cuts,[zb]))
        values=self.cdf((fixed+cuts)*0.5,d*(cuts-fixed)*0.5)
        left=min(left,float(values[0]));right=min(right,1-float(values[0]))
        cap=right if d>0 else left
        falling=np.minimum.accumulate(1-values if d>0 else values)
        a,b=falling[:-1],falling[1:];dt=np.diff(cuts)*0.5
        gap=np.maximum(a-b,1e-300)
        with np.errstate(over='ignore',invalid='ignore'):
            area=np.where(cap<=b,cap,np.where(cap>=a,(a+b)*0.5,
                          cap-(cap-b)**2/(2*gap)))
        amount=float(np.sum(dt*area))+(tb-ta)*(left if d>0 else right)
        if d>0:right=min(right,float(falling[-1]))
        else:left=min(left,float(falling[-1]))
        if abs(xb+1)<1e-12:left=0.0
        if abs(xb-1)<1e-12:right=0.0
        return amount,left,right

    def cost(self,route):
        left=0.0 if route[0][1]==-1 else 1.0
        right=0.0 if route[0][1]==1 else 1.0
        cost=0.0
        for (ta,xa),(tb,xb) in zip(route,route[1:]):
            if tb-ta<=1e-13:continue
            amount,left,right=self.leg(ta,xa,tb,xb,left,right);cost+=amount
        return cost


FAMILIES=('outward','inward','two_turn','two_turn_t2','precenter_loop')


class SearchDeadline(Exception):
    """Internal signal retaining the best point reached by a bounded search."""


def positions(family,parameters):
    a=parameters[0]
    if family=='outward':
        b=a+(1-a)*parameters[1]
        return [a,b,-1,1]
    if family=='inward':return [a,-parameters[1],1,-1]
    if family=='two_turn_t2':
        b=a+(1-a)*parameters[1]/2
        c=(1+a)/2-b
        return [a,b,-c,1,-1]
    if family=='two_turn':
        b=a+(1-a)*parameters[1]
        c=min(1,(3-2*b+a)/2)*parameters[2]
        return [a,b,-c,1,-1]
    if family=='precenter_loop':
        b=a*parameters[1]
        c=b+(min(1,1-a/2+b)-b)*parameters[2]
        return [a,b,c,-1,1]
    raise ValueError(family)


def route_from_positions(xs):
    out=[(0*xs[0],xs[0])]
    endpoints={xs[0]} & {-1,1}
    for x in xs[1:]:
        dt=abs(x-out[-1][1])
        if not dt:continue
        out.append((out[-1][0]+dt,x))
        while len(out)>=3:
            a,b,c=out[-3:]
            if (b[1]-a[1])*(c[0]-b[0]) != (c[1]-b[1])*(b[0]-a[0]):break
            del out[-2]
        if x in (-1,1):endpoints.add(x)
        if len(endpoints)==2:break
    return out


def snap_route(family,parameters,denominator):
    # Snap normalized bounded parameters, then build all times from exact
    # distances. This preserves legality and every defining inequality.
    q=[Q(max(0,min(denominator,int(round(float(x)*denominator)))),denominator)
       for x in parameters]
    return route_from_positions(positions(family,q))


def search(source,output,*,families=FAMILIES,starts=6,seed=1701,seconds=120,
           denominator=1000000,exact_top=1,coarse=None,max_evaluations=1200):
    begun=time.monotonic();data,raw=read(source)
    original=Field(data,Q(1,2))
    if coarse is None:coarse=data.get('discovery_profile_grid',original.n)
    field,checked=coarse_field(original,int(coarse));fast=FastField(field)
    rng=np.random.default_rng(seed);results=[];evaluations=0
    # Cheap independent evaluation check before trusting exploratory scores.
    for t,x in ((Q(0),Q(3,4)),(Q(1,2),Q(1,3)),(Q(5,4),Q(-2,3)),(Q(2),Q(1,7))):
        assert abs(float(field.cdf(t,x))-float(fast.cdf(float(t),float(x))))<2e-12
    exploration_begun=time.monotonic()
    for family_index,family in enumerate(families):
        # Reserve a share for every independent family. An objective-level
        # deadline prevents one nonsmooth Powell search consuming the run.
        deadline=exploration_begun+seconds*(family_index+1)/len(families)
        dim=3 if family in ('two_turn','precenter_loop') else 2
        initial=[np.full(dim,0.5),np.zeros(dim),np.ones(dim)]
        if family=='outward':initial.insert(0,np.array([0.748407,(0.868166-0.748407)/(1-0.748407)]))
        if family=='two_turn_t2':initial.insert(0,np.array([1/32,13/31]))
        initial += [rng.random(dim) for _ in range(max(0,starts-len(initial)))]
        best=None;calls=0
        for x0 in initial[:starts]:
            if time.monotonic()>=deadline:break
            cache={}
            def objective(x):
                nonlocal evaluations,calls,best
                if time.monotonic()>=deadline:raise SearchDeadline
                key=tuple(np.round(x,14))
                if key not in cache:
                    value=fast.cost(route_from_positions(positions(family,x)))
                    cache[key]=value;evaluations+=1;calls+=1
                    if best is None or value<best[0]:best=(value,list(map(float,x)))
                return cache[key]
            try:
                objective(x0)
                minimize(objective,x0,method='Powell',bounds=[(0,1)]*dim,
                         options={'maxfev':max_evaluations,'xtol':1e-9,'ftol':1e-10})
            except SearchDeadline:
                break
        if best is None:continue
        route=snap_route(family,best[1],denominator)
        item={'family':family,'floating_cost':best[0],
              'floating_cost_of_snapped_route':fast.cost([(float(t),float(x)) for t,x in route]),
              'parameters':best[1],'route':[[str(t),str(x)] for t,x in route],
              'floating_evaluations':calls}
        results.append(item)
    results.sort(key=lambda x:x['floating_cost_of_snapped_route'])
    exact=[]
    for index,item in enumerate(results[:exact_top]):
        route=[tuple(map(Q,p)) for p in item['route']]
        plane=supporting_plane(field,route)
        plane.update({'source_sha256':hashlib.sha256(raw).hexdigest(),'contour_n':field.n,
                      'source_n':original.n,'interpolation_epsilon':'1/2',
                      'family':item['family'],'route':item['route'],
                      'scope':'Exact fixed-field physical attack and supporting plane for the stated full-width P1 profile class. No unrestricted Princess lower is asserted.'})
        filename=output.parent/(output.name+f'.plane{index}.json')
        filename.parent.mkdir(parents=True,exist_ok=True)
        filename.write_text(json.dumps(plane,indent=2)+'\n')
        exact.append({'file':filename.name,'value':plane['value'],'decimal':plane['decimal'],
                      'family':item['family'],'sha256':hashlib.sha256(filename.read_bytes()).hexdigest()})
    report={'status':'EXPLORATION_COMPLETED','source_sha256':hashlib.sha256(raw).hexdigest(),
            'source_n':original.n,'contour_n':field.n,'refinement_identity_node_checks':checked,
            'seed':seed,'requested_families':list(families),'starts_per_family':starts,
            'rational_parameter_denominator':denominator,'floating_evaluations':evaluations,
            'floating_discoveries':results,'exact_attacks':exact,
            'seconds':time.monotonic()-begun,
            'scope':'Finite-family floating attack discovery with separately identified exact rational replays; no lower certificate.'}
    output.parent.mkdir(parents=True,exist_ok=True)
    output.with_suffix('.search.json').write_text(json.dumps(report,indent=2)+'\n')
    return report


if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('source',type=Path);ap.add_argument('--output',type=Path,required=True)
    ap.add_argument('--families',default=','.join(FAMILIES));ap.add_argument('--starts',type=int,default=6)
    ap.add_argument('--seed',type=int,default=1701);ap.add_argument('--seconds',type=float,default=120)
    ap.add_argument('--denominator',type=int,default=1000000)
    ap.add_argument('--exact-top',type=int,default=1);ap.add_argument('--coarse',type=int)
    ap.add_argument('--max-evaluations',type=int,default=1200)
    args=ap.parse_args();families=tuple(args.families.split(','))
    if not families or any(f not in FAMILIES for f in families):ap.error('unknown/empty family')
    if min(args.starts,args.denominator,args.max_evaluations)<1 or args.exact_top<0 or args.seconds<=0:ap.error('invalid positive budget')
    result=search(args.source,args.output,families=families,starts=args.starts,seed=args.seed,
                  seconds=args.seconds,denominator=args.denominator,exact_top=args.exact_top,
                  coarse=args.coarse,max_evaluations=args.max_evaluations)
    print(json.dumps({k:v for k,v in result.items() if k!='floating_discoveries'},indent=2))
