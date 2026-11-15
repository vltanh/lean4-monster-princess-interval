#!/usr/bin/env python3
"""Construct and audit a complete-CDF terminal incoming-band warp.

The warp repairs negative M1 on a continuous terminal interval while leaving
the specified high negative-V endpoint/f/I1 data unchanged. It is a local
family repair, not an all-monster or equilibrium certificate.
"""
import argparse
from bisect import bisect_right
from fractions import Fraction as Q
import json
import math
from pathlib import Path
import sys

from audit_m1 import ExactField

PACKAGE=Path(__file__).resolve().parent


def quadratic(f,lo,hi):
    f0,fm,f1=f(lo),f((lo+hi)/2),f(hi)
    a=2*(f1-2*fm+f0)
    b,c=f1-f0-a,f0
    assert f((3*lo+hi)/4)==a/16+b/4+c
    return a,b,c


def poly(coeff,t):
    a,b,c=coeff
    return (a*t+b)*t+c


def maximum(coeff):
    a,b,c=coeff
    candidates=[(Q(0),c),(Q(1),a+b+c)]
    if a<0 and 0 < -b/(2*a) < 1:
        t=-b/(2*a)
        candidates.append((t,poly(coeff,t)))
    return max(candidates,key=lambda p:p[1])


def pack(x):
    return dict(exact=str(x),value=float(x))


class Warp:
    def __init__(self,payload):
        self.payload=payload
        self.start=float(Q(payload['repair_start']))
        self.repair_end=float(Q(payload.get('repair_end','1')))
        self.bridge=float(Q(payload['bridge_start']))
        self.pieces=[]
        for row in payload['pieces']:
            self.pieces.append((float(Q(row['lo'])),float(Q(row['hi'])),
                                [float(Q(x))for x in row['B']],
                                [float(Q(x))for x in row['G']],float(Q(row['prefix_G']))))
        self.ends=[piece[1]for piece in self.pieces]
        self.bends=[poly(piece[2],1.)for piece in self.pieces]
        self.at_start=self._envelope(self.start)
        self.at_end=self._envelope(self.repair_end)

    def _B_inverse(self,target,lower):
        k=min(len(self.pieces)-1,bisect_right(self.bends,target))
        lo,hi,bc,_,_=self.pieces[k]
        if target<=bc[2]:return max(lower,lo)
        a,b,c=bc;c-=target
        if abs(a)<1e-18:
            t=-c/b if b else 0.
        else:
            disc=max(0.,b*b-4*a*c)
            roots=[(-b-math.sqrt(disc))/(2*a),(-b+math.sqrt(disc))/(2*a)]
            good=[r for r in roots if -1e-8<=r<=1+1e-8]
            if not good:raise ValueError(('No inverse',target,k,roots))
            t=min(good)
        return max(lower,min(1.,lo+(hi-lo)*max(0.,min(1.,t))))

    def _envelope(self,u):
        k=min(len(self.pieces)-1,bisect_right(self.ends,u))
        lo,hi,bc,gc,previous=self.pieces[k]
        t=max(0.,min(1.,(u-lo)/(hi-lo)))
        candidates=[previous,poly(gc,0.),poly(gc,t)]
        a,b,_=gc
        if a<0 and 0 < -b/(2*a) < t:
            candidates.append(poly(gc,-b/(2*a)))
        target=max(poly(bc,t),*candidates)
        return self._B_inverse(target,u)

    def __call__(self,u):
        if u<=self.bridge or u>=1:return u
        if u<self.start:
            return self.bridge+(u-self.bridge)*(self.at_start-self.bridge)/(self.start-self.bridge)
        if u>self.repair_end:
            return max(u,self.at_end)
        return self._envelope(u)


class WarpedField:
    """Evaluate the complete unmeshed sum of disjoint warped rank bands.

    ``radial`` uses light coordinates (U,V), not time/radius. The algebraic
    warp is defined by the exact rational payload; this evaluator uses
    doubles only for response discovery and independent quadrature.
    """
    def __init__(self,manifest):
        self.manifest_path=Path(manifest).resolve()
        self.manifest=json.loads(self.manifest_path.read_text())
        folder=self.manifest_path.parent
        self.base_path=(folder/self.manifest['base_field']).resolve()
        self.base_data=json.loads(self.base_path.read_text())
        sys.path.insert(0,str(PACKAGE.parent/'interval_turn_sheet'))
        from probe_cdf_field import Field
        self.base=Field(self.base_data)
        self.bands=[]
        for name in self.manifest['bands']:
            payload=json.loads((folder/name).read_text())
            assert payload['status'].startswith('exact terminal inverse range')
            self.bands.append((float(Q(payload['qlo'])),float(Q(payload['qhi'])),Warp(payload)))
        assert all(self.bands[i][1]<=self.bands[i+1][0]for i in range(len(self.bands)-1))
        self.breakpoints=sorted({u for lo,hi,warp in self.bands
                                 for u in [warp.bridge,warp.start,warp.repair_end,warp.at_end,
                                           *[p[0]for p in warp.pieces],*[p[1]for p in warp.pieces]]})

    def base_radial(self,u,v):
        return self.base.radial((u+v)/2,(u-v)/2)

    def radial(self,u,v):
        original=self.base_radial(u,v)
        result=original
        initial=self.base_radial(u,-u) if u<1 else 1.
        for lo,hi,warp in self.bands:
            shifted=warp(u)
            if shifted==u:continue
            # A bridge can lie below the band's initial saturation
            # threshold. Retain the original initial distribution there.
            replacement=min(initial,self.base_radial(shifted,v))
            result+=min(max(replacement-lo,0.),hi-lo)-min(max(original-lo,0.),hi-lo)
        return min(1.,max(0.,result))

    def psi(self,index,u):
        return self.bands[index][2](u)

    def traces(self,time,position):
        radial=self.radial(time+abs(position),time-abs(position))
        if position==0:return (1-radial)/2,(1+radial)/2
        if position==1:return (1+radial)/2,1.
        if position==-1:return 0.,(1-radial)/2
        value=(1+radial)/2 if position>0 else (1-radial)/2
        return value,value


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--field',type=Path,default=PACKAGE/'snapshots/endpoint_joint_i1_field.json')
    parser.add_argument('--qlo',default='1/2')
    parser.add_argument('--qhi',default='17/20')
    parser.add_argument('--repair-start',default='127/128')
    parser.add_argument('--repair-end',default='1')
    parser.add_argument('--bridge-start',default='63/64')
    parser.add_argument('--output',type=Path,default=PACKAGE/'snapshots/endpoint_band_warp.json')
    args=parser.parse_args()
    data=json.loads(args.field.read_text())
    field=ExactField(data)
    qlo,qhi=Q(args.qlo),Q(args.qhi)
    start,bridge,end=Q(args.repair_start),Q(args.bridge_start),Q(args.repair_end)
    mass=qhi-qlo
    assert 0<qlo<qhi<1 and 0<=bridge<start<end<=1
    initial_gate=field.initial_value(start)-qhi
    outgoing_gate=qlo-field.radial(Q(1),start)
    assert initial_gate>0 and outgoing_gate>0
    value=field.positive_m1(Q(1))
    def B(u):
        return mass*(1+u)+field.integral(u,-u,u,0,qlo)-field.integral(u,-u,u,0,qhi)
    def G(u):
        return B(u)+4*(value-field.negative_m1(u))
    knots={start,end,Q(1)}
    knots.update(k for row in field.grid for k in row if start<k<1)
    for points,coefficient,_ in field.triangles:
        ru,rv,c=coefficient
        if max(p[0]for p in points)<start or min(p[0]for p in points)>1:continue
        vals=[ru*u+rv*v+c for u,v in points]
        for threshold in [qlo,qhi]:
            for pa,pb,fa,fb in zip(points,points[1:]+points[:1],vals,vals[1:]+vals[:1]):
                if (fa-threshold)*(fb-threshold)<0:
                    u=pa[0]+(threshold-fa)*(pb[0]-pa[0])/(fb-fa)
                    if start<u<1:knots.add(u)
    knots=sorted(knots)
    b1=B(Q(1))
    prefix=G(start)
    pieces=[]
    range_min=(None,None)
    worst_base=(start,field.negative_m1(start)-value)
    for lo,hi in zip(knots,knots[1:]):
        bc,gc=quadratic(B,lo,hi),quadratic(G,lo,hi)
        assert min(bc[1],2*bc[0]+bc[1])>=0
        t,gmax=maximum(gc)
        margin=b1-gmax
        if hi<=end and (range_min[0] is None or margin<range_min[1]):range_min=(lo+(hi-lo)*t,margin)
        cc=quadratic(lambda u:field.negative_m1(u)-value,lo,hi)
        t,minus=maximum(tuple(-c for c in cc))
        if hi<=end and -minus<worst_base[1]:worst_base=(lo+(hi-lo)*t,-minus)
        pieces.append(dict(lo=str(lo),hi=str(hi),B=list(map(str,bc)),G=list(map(str,gc)),
                           prefix_G=str(prefix),maximum_G=pack(gmax),range_margin=pack(margin)))
        prefix=max(prefix,gmax)
    payload=dict(scope='Complete ordered-CDF terminal middle-rank warp; terminal negative-M1 repair only, other monster families still require audit.',
                 base_field=args.field.name,qlo=str(qlo),qhi=str(qhi),repair_start=str(start),repair_end=str(end),bridge_start=str(bridge),
                 endpoint_value=pack(value),initial_gate=pack(initial_gate),outgoing_gate=pack(outgoing_gate),
                 B_at_one=pack(b1),pieces=pieces,range_gate_min=dict(U=str(range_min[0]),margin=pack(range_min[1])),
                 worst_base_ell=dict(U=str(worst_base[0]),slack=pack(worst_base[1])),
                 formula='Rnew=min(Rbase,qlo)+max(Rbase-qhi,0)+clamp(min(A_base(U),Rbase(psi(U),V))-qlo,0,qhi-qlo); A_base(U)=1 after U1.',
                 terminal_warp='psi(U)=max(U,B^{-1}(max(B(U),sup_{start<=t<=U}G(t))))',
                 bridge='Linear from identity at bridge_start to psi(repair_start).',
                 continuation='For U>repair_end use max(U,psi(repair_end)).')
    if range_min[1]<0:
        payload['status']='failed inverse range gate'
    else:
        payload['status']='exact terminal inverse range and transport gates pass; external response audit open'
        warp=Warp(payload)
        payload['warp_examples']=[dict(U=float(u),psi=warp(float(u)),shift=warp(float(u))-float(u))for u in
                                  [start,(start+end)/2,Q(worst_base[0]),end,Q(1)]]
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(payload,indent=2)+'\n')
    print(json.dumps({k:v for k,v in payload.items()if k!='pieces'},indent=2))
    print('Exact quadratic pieces',len(pieces))


if __name__=='__main__':main()
