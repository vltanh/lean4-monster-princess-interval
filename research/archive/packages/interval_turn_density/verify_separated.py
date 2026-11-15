#!/usr/bin/env python3
"""Independent segment-capture check of the separated analytic features.

Numerical quadrature is used only as an independent implementation check.
The response oracle itself integrates every feature analytically.
"""

import sys
from pathlib import Path

import numpy as np
from numpy.polynomial.legendre import leggauss

from separated_oracle import (baseline_prefix,bin_at,features,positive_prefix,
                              residual_row,unit_to_parameters,value_at,
                              features_affine,residual_row_affine)


def capture(monster,princess):
    i=j=0
    while i<len(monster)-1 and j<len(princess)-1:
        mt,mx=monster[i];nt,nx=monster[i+1]
        pt,px=princess[j];qt,qx=princess[j+1]
        lo=max(mt,pt);hi=min(nt,qt)
        if hi>=lo-1e-12:
            mv=(nx-mx)/(nt-mt);pv=(qx-px)/(qt-pt)
            d0=mx+mv*(lo-mt)-px-pv*(lo-pt)
            rate=mv-pv
            if abs(d0)<2e-11:return lo
            if abs(rate)>1e-13:
                t=lo-d0/rate
                if lo-1e-11<=t<=hi+1e-11:return max(lo,t)
        if nt<=qt+1e-12:i+=1
        if qt<=nt+1e-12:j+=1
    raise AssertionError('No capture')


def m1(x):return np.array([[0.,x],[1-x,1.],[3-x,-1.],[6.,-1.]])


def m2(z,s):
    return np.array([[0.,-z],[(s+z)/2,(s-z)/2],
                     [s+1,-1.],[s+3,1.],[6.,1.]])


def pair(path,p):
    reflected=path.copy();reflected[:,1]*=-1
    return (capture(path,p)+capture(reflected,p))/2


def actual_princess(parameters,segments,epsilon):
    a,u,c,y=parameters
    points=[(a,-a)]
    def append(U,V):
        if U<points[-1][0]-1e-10 or V<points[-1][1]-1e-10:
            raise AssertionError((points[-1],(U,V)))
        if abs(U-points[-1][0])+abs(V-points[-1][1])>1e-12:
            points.append((U,V))
    up=min(u,1-epsilon)
    append(up,-a)
    append(up,min(c,0))
    for lo,hi,slope,intercept in segments:
        ulo=min(slope*lo+intercept,1-epsilon)
        uhi=min(slope*hi+intercept,1-epsilon)
        append(ulo,lo);append(uhi,hi)
    append(1-epsilon,c)
    append(1+epsilon,c)
    append(1+epsilon,y)
    append(y+2,y)
    times=np.array([[(U+V)/2,(U-V)/2] for U,V in points])
    times=np.vstack((times,[6.,1.]))
    return times,points


def integrate(function,lo,hi,cuts,order=10):
    if hi<=lo:return 0.
    nodes,weights=leggauss(order)
    grid=sorted(set([lo,hi]+[float(x) for x in cuts if lo<x<hi]))
    result=0.
    for l,r in zip(grid,grid[1:]):
        mid=(l+r)/2;half=(r-l)/2
        result+=half*sum(w*function(mid+half*x) for x,w in zip(nodes,weights))
    return result


def direct_expectation(p,uv,weights,knots,profile,left,right,s0,affine_profile=None,
                       edge_trace=False):
    n=len(knots)-1
    f=weights[1:1+n];g=weights[1+n:1+2*n]
    k=weights[1+2*n:1+3*n];ell=weights[1+3*n:]
    zcuts=list(knots)+[p[0,1]]
    for U,V in uv:zcuts.extend([U,V,-V,2-U])
    if affine_profile is not None:
        for v0,v1 in affine_profile:
            if abs(v1)>1e-14:
                zcuts.extend([(2-x-v0)/v1 for x in knots])
                zcuts.extend([(U-v0)/v1 for U,V in uv])
    scuts=[V for U,V in uv]+[U for U,V in uv]+list(knots)
    result=weights[0]*pair(m1(-1),p)
    for j in range(n):
        lo,hi=knots[j:j+2]
        result+=f[j]*integrate(lambda x:pair(m1(x),p),lo,hi,zcuts)
        result+=g[j]*integrate(lambda x:pair(m2(-x,1.),p),lo,hi,zcuts)
        result+=ell[j]*integrate(lambda z:pair(m1(-z),p),lo,hi,zcuts)
        def line(z):
            if affine_profile is None:
                residual=float(residual_row(z,j,knots,profile,left,right,s0,edge_trace)@weights)
            else:
                residual=float(residual_row_affine(z,j,knots,affine_profile,left,right,s0,edge_trace)@weights)
            assert residual>=-1e-10
            return residual*pair(m2(z,1.),p)
        result+=integrate(line,lo,hi,zcuts)
    # Direct integration of the actual early and late monster paths.
    if edge_trace:
        ks=value_at(s0,knots,k)
        for j in range(n):
            lo=max(left,knots[j]);hi=min(right,knots[j+1])
            if hi<=lo:continue
            coefficient=ks-k[j]
            def trace_z(z):
                return coefficient/(s0+6-z)*integrate(lambda s:pair(m2(z,s),p),s0,1.,scuts)
            result+=integrate(trace_z,lo,hi,zcuts)
    for j in range(1,n):
        r=knots[j];jump=k[j]-k[j-1]
        active=r>s0 if edge_trace else r>=s0
        if not active or abs(jump)<1e-14:continue
        def early_z(z):
            return jump/(r+6-z)*integrate(lambda s:pair(m2(z,s),p),r,1.,scuts)
        result+=integrate(early_z,left,right,zcuts)
    for j in range(n):
        lo,hi=knots[j:j+2]
        if affine_profile is None:v0,v1=profile[j],0.
        else:v0,v1=affine_profile[j]
        if v0+v1*(lo+hi)/2<=1:continue
        def late_base(z):
            v=v0+v1*z
            pcoef=value_at(2-v,knots,f)-ell[j]
            return pcoef/(v+6-z)*integrate(lambda s:pair(m2(z,s),p),1.,v,scuts)
        result+=integrate(late_base,lo,hi,zcuts)
        for h in range(1,n):
            r=2-knots[h];jump=f[h]-f[h-1]
            if abs(jump)<1e-14:continue
            def late_jump(z):
                if r>=v0+v1*z:return 0.
                return jump/(r+6-z)*integrate(lambda s:pair(m2(z,s),p),1.,r,scuts)
            result+=integrate(late_jump,lo,hi,zcuts)
    return result


def main():
    # A separate previously checked scalar implementation is used only
    # for the zero-sheet regression, not for the direct segment check.
    sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'interval_signed_densities'))
    from discover import features as old_features
    knots=np.array([0,1/4,1/2,3/4,7/8,15/16,1.])
    n=len(knots)-1;left,right,s0=1/4,3/4,7/8
    rng=np.random.default_rng(41);zero_error=0.
    for _ in range(80):
        p=unit_to_parameters(rng.random(4));seg,count=baseline_prefix(p,knots)
        row=features(p,seg,count,knots,np.ones(n),left,right,1.)
        old=old_features(p,knots);width=np.diff(knots)
        converted=np.r_[old[0],old[1:1+n]*width,old[1+n:1+2*n]*width,
                        old[1+2*n:1+3*n]*width,
                        (old[1+3*n:]-old[1+2*n:1+3*n])*width]
        zero_error=max(zero_error,float(abs(row-converted).max()))
    assert zero_error<1e-12
    weights=np.r_[.5,[.1,.2,.3,.8,.8,.8],[.1]*n,
                  [.1,.2,.2,.2,.5,.5],[0,0,0,.2,.5,.5]]
    profile=np.array([1.,1.125,1.125,1.,1.,1.])
    cases=[np.array(p) for p in [(.2,.4,.8,.9),(.6,.95,.7,.9),
                                 (.92,.94,-.3,.7),(.4,.5,.95,.97)]]
    max_extrapolated_error=0.
    for params in cases:
        seg,count=positive_prefix(params,knots,weights[1+2*n:1+3*n],left,right,s0)
        expected=float(features(params,seg,count,knots,profile,left,right,s0)@weights)
        values=[]
        for eps in [2e-5,1e-5]:
            actual,uv=actual_princess(params,seg[:count],eps)
            values.append(direct_expectation(actual,uv,weights,knots,profile,left,right,s0))
        extrapolated=2*values[1]-values[0]
        error=abs(extrapolated-expected)
        max_extrapolated_error=max(max_extrapolated_error,error)
        print('CAPTURE_CASE',params.tolist(),'analytic',expected,
              'epsilon_values',values,'extrapolated_error',error,flush=True)
        assert error<3e-8,(params,expected,values,error)
    print('PASS: 80 zero-sheet regressions; max error',zero_error)
    print('PASS: 4 independent first-segment-capture epsilon limits; max error',
          max_extrapolated_error)
    affine=np.c_[np.ones(n),np.zeros(n)]
    for j in range(n):
        if knots[j]>=left and knots[j+1]<=right:
            affine[j]=[1.015625-.125*left,.125]
    params=cases[1]
    seg,count=positive_prefix(params,knots,weights[1+2*n:1+3*n],left,right,s0)
    expected=float(features_affine(params,seg,count,knots,affine,left,right,s0)@weights)
    values=[]
    for eps in [2e-5,1e-5]:
        actual,uv=actual_princess(params,seg[:count],eps)
        values.append(direct_expectation(actual,uv,weights,knots,profile,left,right,s0,affine))
    error=abs(2*values[1]-values[0]-expected)
    assert error<3e-8,(expected,values,error)
    print('PASS: genuinely affine-turn direct capture limit; error',error)
    edge_weights=weights.copy()
    edge_weights[1+2*n:1+3*n]=[.1,.2,.3,.35,.5,.6]
    edge_weights[1+3*n:]=[0,0,0,.35,.5,.6]
    seg,count=positive_prefix(params,knots,edge_weights[1+2*n:1+3*n],left,right,s0,True)
    expected=float(features_affine(params,seg,count,knots,affine,left,right,s0,True)@edge_weights)
    values=[]
    for eps in [2e-5,1e-5]:
        actual,uv=actual_princess(params,seg[:count],eps)
        values.append(direct_expectation(actual,uv,edge_weights,knots,profile,left,right,s0,affine,True))
    error=abs(2*values[1]-values[0]-expected)
    assert error<3e-8,(expected,values,error)
    print('PASS: nonflat-k lower-edge-sheet direct capture limit; error',error)
    print('Scope: implementation verification, not numerical equilibrium certification.')


if __name__=='__main__':main()
