#!/usr/bin/env python3
"""Exact physical attack and its supporting plane for full-width Qout fields.

The retained clocks are causal continuous clocks. Nodal coefficients are
their EXACT integral in the specified full-width P1 basis, not a claim that
trapezoidal endpoint atoms form causal clocks for arbitrary Princess laws.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path
import sys

from extract_quantiles import Field, coarse_field, read, ROOT
sys.path.insert(0,str(ROOT/'packages/interval_global_closure/record_bellman'))
from replay_center_renewal_paths import integrate_path


def basis(field,t,x):
    coords=(field.n*(t+x),field.n*(t-x))
    index=[z.numerator//z.denominator for z in coords]
    frac=[z-i for z,i in zip(coords,index)]
    cuts={Q(0),Q(1)}
    for i,z in zip(index,frac):
        cuts.add(z if field.orientation(i) else 1-z)
    cuts=sorted(cuts)
    answer=defaultdict(Q)
    for a,b in zip(cuts,cuts[1:]):
        z=(a+b)/2
        u,w=[i+int(f>(z if field.orientation(i) else 1-z))
             for i,f in zip(index,frac)]
        j,k=u+w,u-w
        if k:
            # Qout eliminates all post-two variables by their exact footpoint.
            ksign=1 if k>0 else -1
            k=abs(k)
            if j>field.C:
                k-=j-field.C;j=field.C
            if k>0:answer[j,k]+=ksign*(b-a)/2
    return dict(answer)


def leg_intervals(field,ta,xa,tb,xb):
    assert tb>ta and abs(xb-xa)==tb-ta and max(abs(xa),abs(xb))<=1
    sign=1 if xb>xa else -1
    fixed=ta-sign*xa
    za,zb=ta+sign*xa,tb+sign*xb
    frac=field.n*fixed;frac-=frac.numerator//frac.denominator
    lo=(field.n*za).numerator//(field.n*za).denominator-1
    hi=(field.n*zb).numerator//(field.n*zb).denominator+2
    cuts={za,zb}
    for k in range(lo,hi+1):
        for f in (Q(0),frac,1-frac,Q(1)):
            z=(k+f)/field.n
            if za<z<zb:cuts.add(z)
    for z in (fixed,4-fixed):
        if za<z<zb:cuts.add(z)
    cuts=sorted(cuts)
    for a,b in zip(cuts,cuts[1:]):
        yield ((fixed+a)/2,sign*(a-fixed)/2),((fixed+b)/2,sign*(b-fixed)/2)


def supporting_plane(field,route):
    route=[tuple(map(Q,p)) for p in route]
    assert route and route[0][0]==0 and abs(route[0][1])<=1
    assert any(x==-1 for t,x in route) and any(x==1 for t,x in route)
    coefficients=defaultdict(Q)
    constant=Q(0)
    masses=[Q(0),Q(0)]
    atoms=[defaultdict(Q),defaultdict(Q)]
    continuous=[[],[]]
    records=[Q(1),Q(1)]
    locations=[route[0],route[0]]
    stopped=[route[0][1]==-1,route[0][1]==1]
    intervals=0

    def add_point(side,point,mass):
        nonlocal constant
        if not mass:return
        constant+=mass/2
        factor=1 if side==0 else -1
        for key,value in basis(field,*point).items():
            coefficients[key]+=factor*mass*value
        masses[side]+=mass

    for first,last in zip(route,route[1:]):
        for a,b in leg_intervals(field,*first,*last):
            ta,xa=a;tb,xb=b;duration=tb-ta
            fa,fb=field.cdf(*a),field.cdf(*b)
            assert field.cdf((ta+tb)/2,(xa+xb)/2)==(fa+fb)/2
            for side in (0,1):
                if stopped[side]:continue
                ga,gb=(fa,fb) if side==0 else (1-fa,1-fb)
                if ga<records[side]:
                    records[side]=ga;locations[side]=a
                old=records[side]
                if gb>=old:
                    atoms[side][locations[side]]+=duration
                    add_point(side,locations[side],duration)
                    continue
                assert ga>=old>gb
                fraction=(ga-old)/(ga-gb)
                split=(ta+duration*fraction,xa+(xb-xa)*fraction)
                held=duration*fraction
                if held:
                    atoms[side][locations[side]]+=held
                    add_point(side,locations[side],held)
                moving=duration-held
                add_point(side,split,moving/2)
                add_point(side,b,moving/2)
                continuous[side].append((split,b))
                records[side]=gb;locations[side]=b
            intervals+=1
        if last[1]==-1:stopped[0]=True
        if last[1]==1:stopped[1]=True
    assert all(stopped)
    value=constant+sum(c*Q(field.gnum(j,k),field.den)
                       for (j,k),c in coefficients.items())
    start=route[0][1]
    independent,checks=integrate_path(field,route,Q(0) if start==-1 else Q(1),
                                     Q(0) if start==1 else Q(1))
    assert value==independent
    endpoint_times=[next(t for t,x in route if x==end) for end in (-1,1)]
    assert masses==endpoint_times
    clocks=[]
    for side in (0,1):
        merged=[]
        for a,b in continuous[side]:
            if merged and merged[-1][1]==a and \
                    (merged[-1][1][1]-merged[-1][0][1])*(b[0]-a[0]) == \
                    (b[1]-a[1])*(merged[-1][1][0]-merged[-1][0][0]):
                merged[-1]=(merged[-1][0],b)
            else:merged.append((a,b))
        clocks.append({
            'endpoint':-1 if side==0 else 1,
            'total_mass':str(masses[side]),
            'atoms':[[str(t),str(x),str(w)] for (t,x),w in sorted(atoms[side].items()) if w],
            'current_time_intervals':[[list(map(str,a)),list(map(str,b))] for a,b in merged],
        })
    return {'value':str(value),'decimal':float(value),'constant':str(constant),
            'coefficients':[[j,k,str(c)] for (j,k),c in sorted(coefficients.items()) if c],
            'continuous_causal_clocks':clocks,'affine_intervals_checked':intervals,
            'independent_affine_intervals_checked':checks}


def score(source,witness,output=None,coarse=None):
    data,raw=read(source)
    field0=Field(data,Q(1,2))
    if coarse is None:coarse=data.get('discovery_profile_grid',field0.n)
    field,count=coarse_field(field0,int(coarse))
    route=json.loads(witness.read_bytes())
    if isinstance(route,dict):
        if 'source_sha256' in route:
            assert route['source_sha256']==hashlib.sha256(raw).hexdigest()
        route=route.get('route',route.get('physical_route'))
    answer=supporting_plane(field,route)
    answer.update({
        'status':'PASS','scope':'One exact physical attack; an upper on this full-width fixed CDF security, not a global game upper. The supporting plane is valid for all full-width profiles on the specified contour grid.',
        'source_sha256':hashlib.sha256(raw).hexdigest(),
        'source_n':field0.n,'contour_n':field.n,
        'refinement_identity_node_checks':count,'interpolation_epsilon':'1/2',
        'route':route,
    })
    if output:output.write_text(json.dumps(answer,indent=2)+'\n')
    return answer


if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('source',type=Path)
    ap.add_argument('route',type=Path)
    ap.add_argument('--output',type=Path)
    ap.add_argument('--coarse',type=int)
    args=ap.parse_args()
    result=score(args.source,args.route,args.output,args.coarse)
    result.pop('coefficients');result.pop('continuous_causal_clocks')
    print(json.dumps(result,indent=2))
