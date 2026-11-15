#!/usr/bin/env python3
"""Vectorized separation of every native-grid initial-inward route.

This is a whole fixed family scan, not a continuous-family certificate.
It evaluates the existing exact CDF formula without allocating a dense
gradient for each of the roughly54,000 routes. Global physical DP remains
the broader opposing-player separator.
"""
from __future__ import annotations
import argparse
from fractions import Fraction as Q
import json
from pathlib import Path
import time
import numpy as np

from continuum_field import ExtendedFieldMesh,ExtendedExactField
from joint_cdf_field import InitialInwardFunctional,initial_inward_route,RouteFunctional


def hinge_integrals(left,right,width):
    """Integral of the positive part of affine endpoint values."""
    positive_left=np.maximum(0.,left);positive_right=np.maximum(0.,right)
    both=(left>=0)&(right>=0)
    total=np.where(both,(positive_left+positive_right)*width/2,0.)
    crossing=(left<0)&(right>0)
    total+=np.divide(positive_right**2*width,2*(right-left),
                     out=np.zeros_like(total),where=crossing)
    crossing=(left>0)&(right<0)
    total+=np.divide(positive_left**2*width,2*(left-right),
                     out=np.zeros_like(total),where=crossing)
    return total


class InwardScanner:
    def __init__(self,data):
        self.mesh=ExtendedFieldMesh(data['base'],data.get('domain_max_v',1))
        assert np.array_equal(self.mesh.nodes,np.asarray(data['nodes']))
        self.values=np.asarray(data['values'],float)
        self.starts=self.mesh.base[self.mesh.base>0]
        self.u=self.mesh.ugrid;self.v=self.mesh.vgrid
        self.au=np.array([int(np.argmin(abs(self.u-a)))for a in self.starts])
        self.r=np.full((len(self.u),len(self.v)),np.nan)
        for key,index in self.mesh.index.items():self.r[key]=self.values[index]
        self.records=np.asarray([(i,j,k)for i,a in enumerate(self.starts)
            for j,v in enumerate(self.v)if -a-1e-12<=v<a-1e-12
            for k,s in enumerate(self.u)if a-1e-12<=s<=v+2+1e-12],dtype=int)

    def evaluate(self):
        m=self.mesh;u,v=self.u,self.v;starts=self.starts
        initial=np.array([self.r[au,int(np.argmin(abs(v+a)))]for a,au in zip(starts,self.au)])
        nbar=np.zeros((len(starts),len(v)))
        for i,(a,au)in enumerate(zip(starts,self.au)):
            js=np.flatnonzero((v>=-a-1e-12)&(v<=a+1e-12))
            y=self.r[au,js]
            nbar[i,js[1:]]=np.cumsum(np.diff(v[js])*(y[:-1]+y[1:])/2)
        # H2(a,v,s)=int_(|v|)^s (R(U,v)-A(a))_+ dU. The part
        # below U=a is zero by the characteristic order constraints.
        h2=np.zeros((len(starts),len(v),len(u)))
        for j,fixed in enumerate(v):
            if fixed>=starts.max()-1e-12:continue
            ks=np.flatnonzero((u>=abs(fixed)-1e-12)&(u<=fixed+2+1e-12))
            y=self.r[ks,j]
            left=y[None,:-1]-initial[:,None];right=y[None,1:]-initial[:,None]
            pieces=hinge_integrals(left,right,np.diff(u[ks])[None,:])
            h2[:,j,ks[1:]]=np.cumsum(pieces,axis=1)
        outgoing=np.zeros(len(u))
        for k,s in enumerate(u):
            if s>=m.vmax-1e-12:continue
            j=int(np.argmin(abs(v-s)));assert abs(v[j]-s)<1e-12
            ks=np.flatnonzero((u>=s-1e-12)&(u<=s+2+1e-12));y=self.r[ks,j]
            outgoing[k]=np.sum(np.diff(u[ks])*(y[:-1]+y[1:])/2)
        ia,jv,ks=self.records.T;a=starts[ia];first=v[jv];second=u[ks]
        low=self.r[self.au[ia],jv];high=self.r[ks,jv].copy()
        high[abs(second-first-2)<1e-12]=1.
        value=(nbar[ia,jv]+(2*second-a-first)*low-(2*second+6)*initial[ia]
               -outgoing[ks]+4*second+8
               -(second+6-first)*np.maximum(0.,high-initial[ia])-h2[ia,jv,ks])
        # H1(s,B)=int_(max(-s,s-2))^s (B-R(s,V))_+ dV. The
        # omitted part below first V is zero since R(s,V)>=R(a,first).
        for k,s in enumerate(u):
            selected=np.flatnonzero(ks==k)
            if not len(selected):continue
            js=np.flatnonzero((v>=max(-s,s-2)-1e-12)&(v<=min(s,m.vmax)+1e-12))
            coordinates=v[js];y=self.r[k,js]
            if s>m.vmax:
                coordinates=np.r_[coordinates,s];y=np.r_[y,0.]
            left=low[selected,None]-y[None,:-1];right=low[selected,None]-y[None,1:]
            value[selected]-=hinge_integrals(left,right,np.diff(coordinates)[None,:]).sum(axis=1)
        assert np.all(np.isfinite(value))
        return value/4

    def route(self,index):
        i,j,k=self.records[index]
        return initial_inward_route(float(self.starts[i]),float(self.v[j]),float(self.u[k]))

    def label(self,index):
        i,j,k=self.records[index]
        return dict(kind='initial_inward',start=float(self.starts[i]),
                    first_v=float(self.v[j]),second_u=float(self.u[k]))


def main():
    p=argparse.ArgumentParser();p.add_argument('field');p.add_argument('--count',type=int,default=16)
    p.add_argument('--output');p.add_argument('--verify',action='store_true');args=p.parse_args()
    started=time.monotonic();data=json.loads(Path(args.field).read_text());scanner=InwardScanner(data)
    costs=scanner.evaluate();order=np.argsort(costs)[:args.count];attacks=[]
    exact=ExtendedExactField(data)if args.verify else None
    for index in order:
        label=scanner.label(index);route=scanner.route(index)
        item=dict(decimal=float(costs[index]),label=label,route=route)
        if exact is not None:
            # Native coordinates are rational; reconstruct times from the
            # three characteristic parameters to avoid independent rounding.
            a=Q(str(label['start'])).limit_denominator(2**22)
            v=Q(str(label['first_v'])).limit_denominator(2**22)
            s=Q(str(label['second_u'])).limit_denominator(2**22)
            rational=[(Q(0),a),((a+v)/2,(a-v)/2),((s+v)/2,(s-v)/2),(s+1,Q(-1)),(s+3,Q(1))]
            payoff=exact.unit_route_payoff(rational)
            assert abs(float(payoff)-costs[index])<2e-10,(payoff,costs[index],label)
            item.update(payoff=str(payoff),route=[[str(t),str(x)]for t,x in rational])
        attacks.append(item)
    result=dict(scope='Complete native-grid initial-inward family only; numerical separation, not an unrestricted lower certificate.',
                routes=len(costs),input=Path(args.field).name,minimum=float(costs.min()),
                attacks=attacks,seconds=time.monotonic()-started)
    if args.output:Path(args.output).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(result,attacks=attacks[:1]),indent=2))


if __name__=='__main__':main()
