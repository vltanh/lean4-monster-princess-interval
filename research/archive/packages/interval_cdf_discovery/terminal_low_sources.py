#!/usr/bin/env python3
"""Extract exact low-rank source functions for a terminal-tail replacement.

The retained low sublaw has radial CDF min(R,q0), q0=A(1-xT).
The source functions are exact piecewise quadratics of the characteristic
offset.  This is boundary data for a conditional tail problem, not a
solution of that problem.
"""
import argparse,json
from fractions import Fraction as Q
from pathlib import Path

from audit_m1 import ExactField,cross,subtract


def extract(data,cutoff,low_mass=None):
    f=ExactField(data);xT=Q(cutoff);initial_cut=f.initial_value(1-xT)
    q0=initial_cut if low_mass is None else Q(low_mass)
    assert 0<q0<1
    assert q0<=initial_cut, 'Retained low initial support must end by 1-xT.'
    future=[value for (u,v),value in zip(f.nodes,f.values) if u-v==2 and v>=1-xT]
    assert future and max(future)==0, 'The terminal formulas require a low outgoing gap.'
    base=f.integral(Q(1),Q(-1),Q(1),0,q0)
    nlow=2*q0-base
    def post(x):return base-f.integral(1+x,-1+x,Q(1),0,q0)
    def prefix(h):return q0*h+f.integral(1-h,-1+h,1-h,0,q0)-base

    # A clipped affine triangle is still a polygon.  Every change in its
    # horizontal slice occurs at a mesh vertex or at an edge/q0 crossing.
    cuts=set(f.grid[0])
    for points,coefficient,_ in f.triangles:
        ru,rv,c=coefficient
        for a,b in zip(points,points[1:]+points[:1]):
            ra=ru*a[0]+rv*a[1]+c-q0;rb=ru*b[0]+rv*b[1]+c-q0
            if ra*rb<0:cuts.add(a[0]-ra*(b[0]-a[0])/(rb-ra))

    def pieces(fun,knots):
        result=[]
        for lo,hi in zip(knots,knots[1:]):
            f0,fm,f1=fun(lo),fun((lo+hi)/2),fun(hi)
            a=2*(f1-2*fm+f0);b=f1-f0-a;c=f0
            for p in [Q(1,4),Q(3,4)]:assert fun(lo+p*(hi-lo))==a*p*p+b*p+c
            result.append(dict(lo=str(lo),hi=str(hi),quadratic=str(a),linear=str(b),constant=str(c)))
        return result

    post_knots=sorted({Q(0),xT}|{u-1 for u in cuts if 1<u<1+xT})
    prefix_knots=sorted({Q(0),xT}|{1-u for u in cuts if 1-xT<u<1})
    post_pieces=pieces(post,post_knots);prefix_pieces=pieces(prefix,prefix_knots)

    def leading(row):
        lo,hi=Q(row['lo']),Q(row['hi']);assert lo==0
        return Q(row['linear'])/hi,Q(row['quadratic'])/(hi*hi)
    q1,q2=leading(post_pieces[0]);o1,o2=leading(prefix_pieces[0])
    post_is_one_quadratic=all(post(x)==q1*x+q2*x*x for x in post_knots)
    for row in post_pieces:
        lo,hi=Q(row['lo']),Q(row['hi'])
        post_is_one_quadratic &= post((lo+hi)/2)==q1*(lo+hi)/2+q2*((lo+hi)/2)**2

    row=sorted((v,r) for (u,v),r in zip(f.nodes,f.values) if u==1)
    for (v0,r0),(v1,r1) in zip(row,row[1:]):
        if r0>=q0>=r1 and r0>r1:
            cT=v0+(r0-q0)*(v1-v0)/(r0-r1);break
    else:raise AssertionError('Missing outgoing cutoff')
    # Select the incoming-side triangle at that row crossing.  Its affine
    # q0 contour gives the exact single-corner order gate d_new=d_old-k*h.
    probe_h=min(prefix_knots[1],xT)/100
    point=(1-probe_h,cT)
    gate=None
    for points,coef,positive in f.triangles:
        if not min(u for u,v in points)<=point[0]<=max(u for u,v in points):continue
        if not min(v for u,v in points)<=point[1]<=max(v for u,v in points):continue
        ru,rv,c=coef
        turns=[cross(subtract(b,a),subtract(point,a)) for a,b in zip(points,points[1:]+points[:1])]
        contains=(all(value>=0 for value in turns) if positive else all(value<=0 for value in turns))
        if rv<0 and contains:
            gate=-ru/rv;break
    assert gate is not None
    nall=f.integral(Q(1),Q(-1),Q(1),0)
    return dict(scope='Exact source and attachment data for a conditional high-rank ordinary tail; no tail solution or unrestricted payoff certificate.',
                xT=str(xT),q0=str(q0),rT=str(1-q0),initial_mass_gap=str(initial_cut-q0),
                dT_old=str(1+cT),outgoing_gap=True,
                Q_linear=str(q1),Q_quadratic=str(q2),Q_one_quadratic=bool(post_is_one_quadratic),
                Q_pieces=post_pieces,Omega_linear=str(o1),Omega_quadratic=str(o2),
                Omega_local_limit=prefix_pieces[0]['hi'],Omega_pieces=prefix_pieces,
                order_gate_kappa=str(gate),order_gate_probe_h=str(probe_h),
                old_tail_endpoint_moment=str(nall-nlow),low_endpoint_four_cost=str(nlow+4*q0),
                exact_quadratic_checks=2*(len(post_pieces)+len(prefix_pieces)))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('field');p.add_argument('--cutoff',default='1/262144');p.add_argument('--low-mass');p.add_argument('--output',required=True);a=p.parse_args()
    result=extract(json.loads(Path(a.field).read_text()),Q(a.cutoff),a.low_mass);result['source']=Path(a.field).name
    Path(a.output).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if not k.endswith('_pieces')},indent=2))
