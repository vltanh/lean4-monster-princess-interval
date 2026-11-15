#!/usr/bin/env python3
"""Independent attacking-route probe for a continuous triangular radial CDF.

Consumes nodes (U,V), triangles, and affine vertex values. Boundary values
are interior radial traces; closed endpoint capture and strict center
capture are handled separately. The input must already be an admissible
ordered law absorbed by time two. This numerical discovery tool checks
cone slopes but is not an interval-arithmetic certificate.

Quantile contour paths are extracted from triangle level sets. A floating
capture-order search proposes a monster route. Its payoff is then computed
against the *entire supplied affine field*, by direct running-CDF records
along that route, not by the sampled quantile mean. Thus the output may
expose a missing lower inequality without mistaking the quantile law's
minimum for the full field's value.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import time
import numpy as np

from probe_ordered_capture import Polygon, solve


def monotone_majorant(data,scale=10**12):
    """Repair a coordinate-grid field in integer nodal arithmetic.

    This is an explicitly reported modification of numerical discovery
    data. Route costs and optional structural inequalities must be checked
    again afterward. Only horizontal/vertical coordinate neighbors are
    used; the returned field is separately checked for triangle cone slopes.
    """
    nodes=data['nodes'];raw=np.asarray(data['values'],float)
    values=[max(0,min(scale,round(float(v)*scale)))for v in raw]
    by_u={};by_v={};predecessors=[[]for _ in nodes]
    for i,(u,v)in enumerate(nodes):
        by_u.setdefault(u,[]).append(i);by_v.setdefault(v,[]).append(i)
    for group in by_u.values():
        order=sorted(group,key=lambda i:-nodes[i][1])
        for a,b in zip(order,order[1:]):predecessors[b].append(a)
    for group in by_v.values():
        order=sorted(group,key=lambda i:nodes[i][0])
        for a,b in zip(order,order[1:]):predecessors[b].append(a)
    for i in sorted(range(len(nodes)),key=lambda i:nodes[i][0]-nodes[i][1]):
        values[i]=max([values[i]]+[values[j]for j in predecessors[i]])
    result=dict(data);result['values']=[v/scale for v in values]
    result['transport_repair']=dict(method='rounded integer coordinate-grid monotone majorant',scale=scale,
        max_nodal_change=float(np.max(abs(np.asarray(result['values'])-raw))))
    return result


class Field:
    def __init__(self,data):
        self.data=data
        self.nodes=np.asarray(data['nodes'],float)
        self.triangles=np.asarray(data['triangles'],int)
        self.values=np.asarray(data['values'],float)
        if self.nodes.shape[1]!=2 or len(self.values)!=len(self.nodes):
            raise ValueError('Field dimensions differ')
        verts=self.nodes[self.triangles]
        mat=np.concatenate((verts,np.ones((*verts.shape[:2],1))),axis=2)
        self.coeff=np.linalg.solve(mat,self.values[self.triangles][...,None])[...,0]
        self.inv=np.linalg.inv(mat.transpose(0,2,1))
        self.lo=verts.min(axis=1);self.hi=verts.max(axis=1)
        self.ugrid=np.unique(self.nodes[:,0]);self.vgrid=np.unique(self.nodes[:,1])
        self.locator={}
        for k,(lo,hi)in enumerate(zip(self.lo,self.hi)):
            ua,ub=np.searchsorted(self.ugrid,[lo[0],hi[0]])
            va,vb=np.searchsorted(self.vgrid,[lo[1],hi[1]])
            for i in range(ua,ub):
                for j in range(va,vb):self.locator.setdefault((i,j),[]).append(k)
        edges=set()
        for a,b,c in self.triangles:
            edges.update((tuple(sorted((int(a),int(b)))),tuple(sorted((int(b),int(c)))),tuple(sorted((int(c),int(a))))))
        self.edges=np.asarray(sorted(edges),int)
        self.edge_a=self.nodes[self.edges[:,0]]
        self.edge_d=self.nodes[self.edges[:,1]]-self.edge_a
        self.cone_violation=float(max(0.,-self.coeff[:,0].min(),self.coeff[:,1].max(),-self.values.min(),self.values.max()-1))

    def radial(self,t,r):
        if t>2 or t-r>1:
            return 0.
        u,v=t+r,t-r
        i=max(0,min(len(self.ugrid)-2,int(np.searchsorted(self.ugrid,u,side='right')-1)))
        j=max(0,min(len(self.vgrid)-2,int(np.searchsorted(self.vgrid,v,side='right')-1)))
        inds=np.asarray(list(dict.fromkeys(k for cell in [(i,j),(i-1,j),(i,j-1),(i-1,j-1)]
                                         for k in self.locator.get(cell,[]))),int)
        if not len(inds):
            raise ValueError(f'No field cell at {(t,r,u,v)}')
        bary=self.inv[inds]@np.array([u,v,1.])
        good=np.flatnonzero(np.all(bary>=-2e-8,axis=1))
        if not len(good):
            raise ValueError(f'Point outside field triangles {(t,r,u,v)}')
        i=inds[good[0]]
        return float(np.clip(self.coeff[i]@np.array([u,v,1.]),0,1))

    def traces(self,t,x,kind=None):
        if abs(x)>1+1e-8:raise ValueError('Monster leaves interval')
        if kind=='center' or (kind is None and abs(x)<=1e-12):
            radial=self.radial(t,0.) if t<=1 else 0.
            return (1-radial)/2,(1+radial)/2
        radial=self.radial(t,min(1.,abs(x)))
        if t>=2 and (kind in ('right_endpoint','left_endpoint') or
                     kind is None and abs(abs(x)-1.)<=1e-12):
            # The saved V=1 boundary is a fixed-characteristic interior
            # limit. At its actual time-two endpoint every such atom has
            # arrived, so the strict spatial endpoint trace is zero.
            radial=0.
        if kind=='right_endpoint' or (kind is None and abs(x-1.)<=1e-12):return (1+radial)/2,1.
        if kind=='left_endpoint' or (kind is None and abs(x+1.)<=1e-12):return 0.,(1-radial)/2
        if kind=='outgoing' or (kind is None and abs(t-abs(x)-1.)<=1e-12):
            # The endpoint-by-two cone permits an atom on the outgoing
            # characteristic V=1. Its strict radial trace is zero.
            return (.5,(1+radial)/2) if x>0 else ((1-radial)/2,.5)
        val=(1+radial)/2 if x>0 else (1-radial)/2
        return val,val

    def quantile(self,q):
        """Extract all affine contour segments, filling center/endpoint waits."""
        # Avoid an entire level edge; this perturbs only the discovery sample.
        if np.min(abs(self.values-q))<1e-11:q+=3.141592653589793e-10
        points=[]
        for edge in self.edges:
            ia,ib=map(int,edge);ra,rb=self.values[[ia,ib]]
            pa,pb=self.nodes[[ia,ib]]
            center=abs(pa[0]-pa[1])+abs(pb[0]-pb[1])<1e-10
            outgoing=abs(pa[1]-1)+abs(pb[1]-1)<1e-10
            endpoint=abs(pa[0]-pa[1]-2)+abs(pb[0]-pb[1]-2)<1e-10
            # Level sets can follow a boundary atom for a whole interval.
            for (u,v),value in ((pa,ra),(pb,rb)):
                if ((center or outgoing) and q<value) or (endpoint and q>value):
                    points.append(((u+v)/2,(u-v)/2))
            if (ra-q)*(rb-q)>=0:continue
            theta=(q-ra)/(rb-ra)
            u,v=self.nodes[ia]+theta*(self.nodes[ib]-self.nodes[ia])
            points.append(((u+v)/2,(u-v)/2))
        def initial():
            if self.radial(0.,0.)>=q:return 0.
            if self.radial(0.,1.)<q:return 1.
            lo,hi=0.,1.
            for _ in range(50):
                mid=(lo+hi)/2
                if self.radial(0.,mid)>=q:hi=mid
                else:lo=mid
            return (lo+hi)/2
        points.extend([(0.,initial()),(2.,1.)])
        points.sort(); vertices=[]
        for t,r in points:
            t=max(0.,min(2.,float(t)));r=max(0.,min(1.,float(r)))
            if vertices and abs(t-vertices[-1][0])<2e-9:
                if abs(r-vertices[-1][1])>2e-7:
                    raise ValueError('Ambiguous contour at one time')
                continue
            vertices.append((t,r))
        # Remove collinear interpolation vertices before capture-order search.
        simple=[]
        for point in vertices:
            while len(simple)>1:
                a,x=simple[-2];b,y=simple[-1];c,z=point
                if abs((y-x)*(c-b)-(z-y)*(b-a))>1e-12:break
                simple.pop()
            simple.append(point)
        return Polygon([t for t,x in simple],[x for t,x in simple])

    @staticmethod
    def cross(a,b):return a[...,0]*b[...,1]-a[...,1]*b[...,0]

    def line_knots(self,a,x,b,y):
        """All cell-edge crossings of a route leg staying on one side."""
        v=(y-x)/(b-a);sgn=1 if (x+y)>=0 else -1
        origin=np.array([a+sgn*x,a-sgn*x]);direction=np.array([1+sgn*v,1-sgn*v])
        den=self.cross(direction,self.edge_d)
        delta=self.edge_a-origin
        good=abs(den)>1e-12
        dt=np.zeros(len(den));frac=np.zeros(len(den))
        dt[good]=self.cross(delta[good],self.edge_d[good])/den[good]
        frac[good]=self.cross(delta[good],direction)/den[good]
        mask=good&(dt>1e-13)&(dt<b-a-1e-13)&(frac>=-1e-10)&(frac<=1+1e-10)
        knots=[a,b]+list(a+dt[mask])
        # Collinear edges need their endpoints as breakpoints too.
        col=(~good)&(abs(self.cross(delta,direction))<1e-10)
        for idx in np.flatnonzero(col):
            for point in (self.edge_a[idx],self.edge_a[idx]+self.edge_d[idx]):
                t=(point[0]+point[1])/2
                if a<t<b:knots.append(float(t))
        knots.sort(); out=[]
        for t in knots:
            if not out or t-out[-1]>1e-13:out.append(t)
        if out[-1]<b-1e-12:out.append(b)
        else:out[-1]=b
        return out

    @staticmethod
    def clip_integral(f0,f1,c,length,maximum):
        clip=max if maximum else min
        if (f0-c)*(f1-c)>=0 or abs(f1-f0)<1e-15:
            return length*(clip(c,f0)+clip(c,f1))/2
        fraction=(c-f0)/(f1-f0)
        return length*(fraction*(clip(c,f0)+c)+(1-fraction)*(c+clip(c,f1)))/2

    def payoff(self,route):
        """Entire-field first-capture expectation, with optimal endpoint tail."""
        route=[list(map(float,p)) for p in route]
        if not route or abs(route[0][0])>1e-12:raise ValueError('Route must start at zero')
        if len(route)==1:route.append([2.,route[0][1]])
        if route[-1][0]<2:
            # A finite sample may finish before the whole CDF is captured.
            # Continue its last unit direction, bouncing at endpoints.
            (a,x),(b,y)=route[-2:]
            direction=1. if y>=x else -1.
            while b<2-1e-12:
                if abs(y-direction)<1e-10:direction=-direction
                arrival=b+1-direction*y
                if arrival>=2:
                    route.append([2.,y+direction*(2-b)]);break
                route.append([arrival,direction]);b,y=route[-1]
        legs=[]
        for (a,x),(b,y) in zip(route,route[1:]):
            if b<=a+1e-12:continue
            if abs(y-x)>b-a+1e-8:raise ValueError('Monster speed exceeds one')
            if a>=2:break
            if b>2:y=x+(y-x)*(2-a)/(b-a);b=2.
            if x*y<0:
                middle=a+(b-a)*abs(x)/(abs(x)+abs(y))
                legs.extend([(a,x,middle,0.),(middle,0.,b,y)])
            else:legs.append((a,x,b,y))
        l,h=self.traces(0.,route[0][1]); integral=0.; xfinal=route[0][1]
        for a,x,b,y in legs:
            velocity=(y-x)/(b-a)
            if abs(x)+abs(y)<1e-13:kind='center'
            elif abs(x-1)+abs(y-1)<1e-13:kind='right_endpoint'
            elif abs(x+1)+abs(y+1)<1e-13:kind='left_endpoint'
            elif abs(a-abs(x)-1)+abs(b-abs(y)-1)<1e-13:kind='outgoing'
            else:kind='interior'
            knots=self.line_knots(a,x,b,y)
            for ta,tb in zip(knots,knots[1:]):
                xa=x+velocity*(ta-a);xb=x+velocity*(tb-a)
                fm,fp=self.traces(ta,xa);l=min(l,fm);h=max(h,fp)
                dt=tb-ta
                one=self.traces(ta+dt/3,xa+velocity*dt/3,kind)
                two=self.traces(ta+2*dt/3,xa+2*velocity*dt/3,kind)
                lm0,lm1=2*one[0]-two[0],2*two[0]-one[0]
                hp0,hp1=2*one[1]-two[1],2*two[1]-one[1]
                if min(lm0,lm1,hp0,hp1)<-1e-6 or max(lm0,lm1,hp0,hp1)>1+1e-6:
                    raise ArithmeticError('Non-affine CDF trace inside one route cell')
                lm0,lm1,hp0,hp1=(float(np.clip(v,0,1))for v in (lm0,lm1,hp0,hp1))
                l=min(l,lm0);h=max(h,hp0)
                lint=self.clip_integral(lm0,lm1,l,dt,False) if lm1<lm0 else l*dt
                hint=self.clip_integral(hp0,hp1,h,dt,True) if hp1>hp0 else h*dt
                integral+=dt+lint-hint
                l=min(l,lm0,lm1);h=max(h,hp0,hp1)
                fm,fp=self.traces(tb,xb);l=min(l,fm);h=max(h,fp)
            xfinal=y
        left=l*(1+xfinal)+(1-h)*(3+xfinal)
        right=(1-h)*(1-xfinal)+l*(3-xfinal)
        # Retain only the prefix to time two and append its actual endpoint tour.
        prefix=[[legs[0][0],legs[0][1]]] if legs else [[0.,xfinal],[2.,xfinal]]
        prefix.extend([[b,y] for a,x,b,y in legs])
        if left<=right:
            tail=left;prefix.extend([[3+xfinal,-1.],[5+xfinal,1.]])
        else:
            tail=right;prefix.extend([[3-xfinal,1.],[5-xfinal,-1.]])
        if not (0<=l<=h<=1) or integral+tail<-1e-9:
            raise ArithmeticError('Invalid captured records')
        clean=[]
        for item in prefix:
            if clean and abs(item[0]-clean[-1][0])<1e-10:continue
            clean.append(item)
        return dict(value=float(integral+tail),prefix_integral=float(integral),remaining_left=float(l),remaining_right=float(1-h),route=clean)


def polish_route(field,route,seconds=20.):
    """Heuristically move the start and switch times, retaining legal speeds.

    This corrects attacks that exploit only the finite sample's initial
    atoms. The reported result is always reevaluated on the whole field.
    """
    from scipy.optimize import minimize,LinearConstraint
    from scipy.linalg import null_space
    route=field.payoff(route)['route']
    if route[0][1]<0:route=[[t,-x]for t,x in route]
    points=[]
    for t,x in route:
        if t>2:break
        points.append([t,x])
    if points[-1][0]<2:
        for (a,x),(b,y)in zip(route,route[1:]):
            if a<2<b:
                points.append([2.,x+(y-x)*(2-a)/(b-a)]);break
    compact=[]
    for point in points:
        while len(compact)>1:
            a,x=compact[-2];b,y=compact[-1];c,z=point
            if abs((y-x)*(c-b)-(z-y)*(b-a))>1e-10:break
            compact.pop()
        compact.append(point)
    if len(compact)<2:return dict(response=field.payoff(route),status='no moving prefix')
    speeds=[(y-x)/(b-a)for(a,x),(b,y)in zip(compact,compact[1:])]
    if any(abs(abs(v)-1)>1e-7 for v in speeds):
        return dict(response=field.payoff(route),status='non-unit prefix retained')
    d=1. if speeds[0]>0 else -1.
    n=len(compact)-2
    initial=np.array([compact[0][1]]+[p[0]for p in compact[1:-1]])
    rows=[];lower=[];upper=[];endpoint_rows=[]
    # Ordered switching times.
    for j in range(1,n):
        row=np.zeros(n+1);row[j]=1;row[j+1]=-1
        rows.append(row);lower.append(-np.inf);upper.append(0.)
    # Every switch position and the position at time two are in [-1,1].
    for k in range(1,n+2):
        row=np.zeros(n+1);row[0]=1.
        for j in range(1,min(k,n+1)):
            row[j]=2*d*(-1)**(j-1)
        constant=0.
        if k<=n:row[k]=d*(-1)**(k-1)
        else:constant=2*d*(-1)**n
        rows.append(row);lower.append(-1-constant);upper.append(1-constant)
        if k<=n and abs(compact[k][1])>1-1e-8:endpoint_rows.append(row.copy())
    matrix=np.asarray(rows);lo=np.asarray(lower);hi=np.asarray(upper)
    # Keep existing endpoint turns on their equality face. Moving a turn
    # an arbitrarily small distance inside can miss an entire endpoint atom;
    # coordinatewise finite differences would then destroy its tangent.
    basis=null_space(np.asarray(endpoint_rows)) if endpoint_rows else np.eye(n+1)
    if basis.shape[1]==0:return dict(response=field.payoff(route),status='fixed endpoint face')
    constraints_matrix=np.concatenate((matrix,np.eye(n+1)))
    constraints_low=np.r_[lo,[0.]+[0.]*n]
    constraints_high=np.r_[hi,[1.]+[2.]*n]
    shifted_low=constraints_low-constraints_matrix@initial
    shifted_high=constraints_high-constraints_matrix@initial
    projected=constraints_matrix@basis
    active_rows=np.linalg.norm(projected,axis=1)>1e-10
    projected=projected[active_rows]
    shifted_low=shifted_low[active_rows];shifted_high=shifted_high[active_rows]
    best=field.payoff(route);calls=0;start=time.monotonic()
    class Cap(Exception):pass
    def make(v):
        times=np.maximum.accumulate(np.clip([0.]+list(v[1:])+[2.],0,2))
        x=float(np.clip(v[0],0,1));out=[[0.,x]]
        for i,(a,b)in enumerate(zip(times,times[1:])):
            x+=d*(-1)**i*(b-a)
            if b>a+1e-10:out.append([float(b),float(np.clip(x,-1,1))])
        return out
    def objective(z):
        nonlocal best,calls
        v=initial+basis@z
        calls+=1
        if time.monotonic()-start>seconds:raise Cap
        av=matrix@v
        violation=float(np.maximum(lo-av,0).sum()+np.maximum(av-hi,0).sum())
        if violation>1e-5:return 100+100*violation
        response=field.payoff(make(v))
        if response['value']<best['value']:best=response
        return response['value']
    try:
        result=minimize(objective,np.zeros(basis.shape[1]),method='SLSQP',
            constraints=[LinearConstraint(projected,shifted_low,shifted_high)],
            options=dict(maxiter=100,ftol=2e-11))
        status=str(result.message)
    except Cap:
        status='wall-time cap; best evaluated route retained'
    return dict(response=best,status=status,calls=calls,seconds=time.monotonic()-start)


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('input',type=Path)
    ap.add_argument('--quantiles',type=int,default=24)
    ap.add_argument('--nodes',type=int,default=100000)
    ap.add_argument('--seconds',type=float,default=45.)
    ap.add_argument('--polish-seconds',type=float,default=20.)
    ap.add_argument('--repair-transport',action='store_true')
    ap.add_argument('--output',type=Path)
    args=ap.parse_args();data=json.loads(args.input.read_text())
    if args.repair_transport:data=monotone_majorant(data)
    field=Field(data)
    if field.cone_violation>2e-7:raise ValueError(f'Input violates transport cone: {field.cone_violation}')
    positive=[field.quantile((i+.5)/args.quantiles)for i in range(args.quantiles)]
    paths=[Polygon(p.t,[-x for x in p.x])for p in positive[::-1]]+positive
    found=solve(paths,node_limit=args.nodes,seconds=args.seconds,symmetry=True)
    actual=field.payoff(found['route'])
    polished=polish_route(field,found['route'],seconds=args.polish_seconds) if args.polish_seconds>0 else None
    options=[actual,field.payoff([[0.,1.],[2.,-1.]])]
    if polished:options.append(polished['response'])
    best=min(options,key=lambda r:r['value'])
    output=dict(scope='Floating structural attack search. Whole-field route payoff is evaluated independently of the finite quantile law; no exact global minimum is claimed.',
                input=str(args.input),transport_repair=data.get('transport_repair'),cone_violation=field.cone_violation,finite_probe=found,
                raw_field_response=actual,polish=polished,field_response=best)
    if args.output:args.output.write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps(output,indent=2))


if __name__=='__main__':main()
