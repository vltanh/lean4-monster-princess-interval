#!/usr/bin/env python3
"""Whole-domain continuum CDF meshes with a declared absorption horizon.

vmax=1 reproduces the existing time-two class. vmax=2 allows center mass
after time one and endpoint absorption as late as time three. These are
candidate classes, not a proved equilibrium reduction. ExactField supports
arbitrary unit-leg monster costs; its old M1 breakpoint audit is deliberately
disabled because the larger domain requires additional response cells.
"""
from __future__ import annotations
from bisect import bisect_left,bisect_right
from fractions import Fraction as Q
import json
from pathlib import Path
import sys
import numpy as np

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'packages/interval_cdf_discovery'))
from joint_cdf_field import FieldMesh,Form
from audit_m1 import ExactField,cross,subtract
from audit_snapshot import coordinate


class ExtendedFieldMesh(FieldMesh):
    def __init__(self,base=None,vmax=2):
        assert int(vmax)==vmax and vmax>=1
        self.vmax=float(vmax)
        if base is None:
            base=sorted(set(np.linspace(0,1,17))|{.45,.525,.55,.575}
                        |{1-2.**(-k) for k in range(5,19)})
        self.base=np.asarray(base,float)
        # Reflect alternate unit strips. The grids must meet both physical
        # diagonal faces U=V and U-V=2 at vertices; simply translating the
        # nonuniform base into every strip leaves uncovered boundary cells.
        self.vgrid=np.unique(np.concatenate([-self.base]+
                            [j+(self.base if j%2==0 else 1-self.base)
                             for j in range(int(vmax))]))
        self.ugrid=np.unique(np.r_[np.abs(self.vgrid),2+self.vgrid])
        self.nodes=[];self.index={}
        for i,u in enumerate(self.ugrid):
            for j,v in enumerate(self.vgrid):
                if u+1e-12>=abs(v) and u-v<=2+1e-12 and v<=self.vmax:
                    self.index[i,j]=len(self.nodes);self.nodes.append((u,v))
        self.nodes=np.asarray(self.nodes)
        self.triangles=[];self.cells={}
        for i in range(len(self.ugrid)-1):
            for j in range(len(self.vgrid)-1):
                corners=[(i,j),(i+1,j),(i+1,j+1),(i,j+1)]
                inside=[p for p in corners if p in self.index]
                if len(inside)<3:continue
                triangles=([tuple(self.index[corners[k]] for k in ids) for ids in ((0,1,2),(0,2,3))]
                           if len(inside)==4 else [tuple(self.index[p] for p in inside)])
                self.cells[i,j]=triangles;self.triangles.extend(triangles)
        self.triangles=np.asarray(self.triangles,dtype=int)
        self.inverses={tuple(tri):np.linalg.inv(np.c_[self.nodes[tri],np.ones(3)].T)
                       for tri in self.triangles}
        self.transport=[]
        for (i,j),left in self.index.items():
            if (i+1,j) in self.index:self.transport.append((left,self.index[i+1,j],'U'))
            if (i,j+1) in self.index:self.transport.append((self.index[i,j+1],left,'-V'))
        self.bounds=[(0.,1.) for p in self.nodes]
        for i,(u,v) in enumerate(self.nodes):
            if abs(v-self.vmax)<1e-12 or abs(u)+abs(v)<1e-12:self.bounds[i]=(0.,0.)
            if abs(u-1)+abs(v+1)<1e-12:self.bounds[i]=(1.,1.)

    def weights(self,u,v):
        if v>=self.vmax-1e-13:return ()
        if u<abs(v)-2e-10 or u-v>2+2e-10:raise ValueError(('outside field',u,v))
        ii=max(0,min(len(self.ugrid)-2,np.searchsorted(self.ugrid,u,side='right')-1))
        jj=max(0,min(len(self.vgrid)-2,np.searchsorted(self.vgrid,v,side='right')-1))
        for i,j in ((ii,jj),(ii-1,jj),(ii,jj-1),(ii-1,jj-1)):
            for triangle in self.cells.get((i,j),[]):
                weights=self.inverses[triangle]@np.array([u,v,1.])
                if weights.min()>=-1e-8:
                    weights[abs(weights)<1e-10]=0;weights=np.maximum(weights,0);weights/=weights.sum()
                    return tuple((index,float(w)) for index,w in zip(triangle,weights) if w)
        raise ValueError(('missing cell',u,v))

    def radial_form(self,t,r):
        return Form(0.,()) if t-r>=self.vmax-1e-13 else Form(0.,self.weights(t+r,t-r))

    def route_cells(self,route):
        result=[]
        for (t0,x0),(t1,x1) in zip(route,route[1:]):
            if t1<=t0+1e-14:continue
            speed=(x1-x0)/(t1-t0);assert abs(speed)<=1+1e-8
            intercept=x0-speed*t0;cuts=[t0,t1]
            if abs(speed)>1e-14:
                crossing=-intercept/speed
                if t0<crossing<t1:cuts.append(crossing)
            pieces=sorted(cuts)
            for left,right in zip(pieces,pieces[1:]):
                mid=(left+right)/2;sign=1 if speed*mid+intercept>=0 else -1
                us,ui=1+sign*speed,sign*intercept
                vs,vi=1-sign*speed,-sign*intercept
                boundaries=[left,right]
                for grid,slope,constant in ((self.ugrid,us,ui),(self.vgrid,vs,vi)):
                    if abs(slope)>1e-14:
                        times=(grid-constant)/slope
                        boundaries.extend(times[(times>left+1e-12)&(times<right-1e-12)])
                boundaries=sorted(set(boundaries));detailed=list(boundaries)
                for lo,hi in zip(boundaries,boundaries[1:]):
                    middle=(lo+hi)/2;u,v=us*middle+ui,vs*middle+vi
                    if v>=self.vmax or u-v>2+1e-9:continue
                    i=max(0,min(len(self.ugrid)-2,np.searchsorted(self.ugrid,u,side='right')-1))
                    j=max(0,min(len(self.vgrid)-2,np.searchsorted(self.vgrid,v,side='right')-1))
                    if len(self.cells.get((i,j),[]))!=2:continue
                    du,dv=self.ugrid[i+1]-self.ugrid[i],self.vgrid[j+1]-self.vgrid[j]
                    slope=us/du-vs/dv;constant=(ui-self.ugrid[i])/du-(vi-self.vgrid[j])/dv
                    if abs(slope)>1e-14:
                        crossing=-constant/slope
                        if lo+1e-12<crossing<hi-1e-12:detailed.append(crossing)
                detailed=sorted(set(detailed))
                for lo,hi in zip(detailed,detailed[1:]):
                    midx=speed*(lo+hi)/2+intercept
                    kind=('center' if abs(midx)<1e-12 else 'right_endpoint' if abs(midx-1)<1e-12
                          else 'left_endpoint' if abs(midx+1)<1e-12 else 'positive' if midx>0 else 'negative')
                    xl,xr=speed*lo+intercept,speed*hi+intercept
                    result.append((hi-lo,self.sides(lo,xl),self.sides(lo,xl,kind),self.sides(hi,xr,kind)))
        return result

    def save(self,path,values,compact=False,**extra):
        payload=dict(scope='Complete extended triangular radial CDF; candidate only, no game certificate.',
                     nodes=self.nodes.tolist(),triangles=self.triangles.tolist(),values=list(map(float,values)),
                     terminal_time=self.vmax+1,domain_max_v=self.vmax,ugrid=self.ugrid.tolist(),
                     vgrid=self.vgrid.tolist(),base=self.base.tolist(),
                     trace='continuous interior; closed endpoint=1, strict center=0')
        payload.update(extra);Path(path).write_text(json.dumps(payload,indent=None if compact else 2)+'\n')

    def import_values(self,data):
        old=ExtendedFieldMesh(data['base'],data.get('domain_max_v',1))
        assert np.max(np.abs(old.nodes-np.asarray(data['nodes'])))<1e-12
        values=np.asarray(data['values'],float)
        imported=np.array([0. if v>=old.vmax-1e-13 else sum(values[i]*w for i,w in old.weights(u,v))
                           for u,v in self.nodes])
        return self.repair_values(imported)[0]


class ExtendedExactField(ExactField):
    def __init__(self,data):
        self.vmax=coordinate(data.get('domain_max_v',1.))
        self.terminal_time=self.vmax+1
        self.nodes=[tuple(map(coordinate,p)) for p in data['nodes']]
        self.values=[Q(str(v)) for v in data.get('rational_values',data['values'])]
        self.grid=[sorted(set(p[k] for p in self.nodes)) for k in (0,1)]
        self.triangles=[];self.cells={};self.strips=[{},{}]
        self.initial=sorted((u,v) for (u,w),v in zip(self.nodes,self.values) if u==-w)
        self.initial_knots=[u for u,v in self.initial]
        assert self.initial[0]==(0,0) and self.initial[-1]==(1,1)
        assert all(0<=v<=1 for v in self.values)
        assert all(value==0 for (u,v),value in zip(self.nodes,self.values) if v==self.vmax)
        for indices in data['triangles']:
            points=[self.nodes[i] for i in indices];p,q,r=points
            e,f=subtract(q,p),subtract(r,p);det=cross(e,f)
            x,y,z=[self.values[i] for i in indices]
            ru=((y-x)*f[1]-(z-x)*e[1])/det;rv=(e[0]*(z-x)-f[0]*(y-x))/det
            assert ru>=0 and rv<=0,('transport',indices,ru,rv)
            number=len(self.triangles);self.triangles.append((points,(ru,rv,x-ru*p[0]-rv*p[1]),det>0))
            ranges=[]
            for axis in (0,1):
                left=bisect_left(self.grid[axis],min(p[axis] for p in points))
                right=bisect_left(self.grid[axis],max(p[axis] for p in points));ranges.append(range(left,right))
                for i in ranges[-1]:self.strips[axis].setdefault(i,[]).append(number)
            for i in ranges[0]:
                for j in ranges[1]:self.cells.setdefault((i,j),[]).append(number)

    def radial(self,u,v):
        if v>self.vmax:return Q(0)
        cell=[max(0,min(len(self.grid[k])-2,bisect_right(self.grid[k],p)-1)) for k,p in enumerate((u,v))]
        possible=set()
        for i in (cell[0],cell[0]-1):
            for j in (cell[1],cell[1]-1):possible.update(self.cells.get((i,j),[]))
        point=u,v
        for number in sorted(possible):
            points,coefficient,positive=self.triangles[number]
            turns=[cross(subtract(b,a),subtract(point,a)) for a,b in zip(points,points[1:]+points[:1])]
            if all(t>=0 for t in turns) if positive else all(t<=0 for t in turns):
                a,b,c=coefficient;return a*u+b*v+c
        raise ValueError(('No exact triangle',u,v))

    def integral(self,fixed,left,right,axis,threshold=None):
        if right<=left:return Q(0)
        if (axis==1 and fixed>=self.vmax) or (axis==0 and left>=self.vmax):
            return max(Q(0),threshold)*(right-left) if threshold is not None else Q(0)
        if axis==0 and right>self.vmax:
            return self.integral(fixed,left,self.vmax,axis,threshold)+(max(Q(0),threshold)*(right-self.vmax) if threshold is not None else 0)
        i=max(0,min(len(self.grid[axis])-2,bisect_right(self.grid[axis],fixed)-1))
        possible=set(self.strips[axis].get(i,[]))|set(self.strips[axis].get(i-1,[]))
        cuts={left,right};other=1-axis
        for number in possible:
            points=self.triangles[number][0]
            for a,b in zip(points,points[1:]+points[:1]):
                if a[axis]==b[axis]:
                    if a[axis]==fixed:cuts.update(x[other] for x in (a,b) if left<x[other]<right)
                elif min(a[axis],b[axis])<=fixed<=max(a[axis],b[axis]):
                    value=a[other]+(fixed-a[axis])*(b[other]-a[other])/(b[axis]-a[axis])
                    if left<value<right:cuts.add(value)
        total=Q(0);cuts=sorted(cuts)
        for a,b in zip(cuts,cuts[1:]):
            fa=self.radial(fixed,a) if axis==0 else self.radial(a,fixed)
            fb=self.radial(fixed,b) if axis==0 else self.radial(b,fixed)
            if threshold is not None:
                fa,fb=threshold-fa,threshold-fb
                if fa<=0 and fb<=0:continue
                if fa*fb<0:
                    width=(b-a)*(fa/(fa-fb) if fa>0 else fb/(fb-fa));total+=width*max(fa,fb)/2;continue
            total+=(b-a)*(fa+fb)/2
        return total

    def positive_m1(self,z):
        return self.unit_route_payoff([(Q(0),z),(1-z,Q(1)),(3-z,Q(-1))])

    def negative_m1(self,z):
        return self.unit_route_payoff([(Q(0),-z),(1+z,Q(1)),(3+z,Q(-1))])

    def breakpoints(self,positive):
        raise NotImplementedError('The extended time domain needs a new complete M1 response arrangement')
