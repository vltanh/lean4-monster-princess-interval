#!/usr/bin/env python3
"""Independent physical replay of the exact n1 precenter edge envelopes."""
from fractions import Fraction as Q
from pathlib import Path
from itertools import combinations
import argparse,gzip,hashlib,json

from build_endpoint_tail_charts import Field
from replay_center_renewal_paths import (parse_certificate, reconstruct as center_route,
                                         objective, eligible, minimum, one_record)


def read(path):
    raw=Path(path).read_bytes()
    return gzip.decompress(raw) if raw[:2]==b"\x1f\x8b" else raw


def point(edge,z):
    if edge=="center":U,W=z,z
    elif edge=="endpoint":U,W=z,z-2
    elif edge=="deadline":U,W=Q(2),z
    elif edge=="flat_entry":U,W=z,Q(1)
    elif edge=="time_one":U,W=z,2-z
    elif edge=="d_left":U,W=Q(1),z
    elif edge=="d_bottom":U,W=z,Q(0)
    elif edge=="b_bottom":U,W=z,Q(0)
    elif edge=="c_left":U,W=Q(1),z
    elif edge=="initial":U,W=z,-z
    else:raise ValueError(edge)
    return (U+W)/2,(U-W)/2


def clean(path):
    out=[]
    for p in path:
        if not out or p!=out[-1]:out.append(p)
    return out


def integrate(field,path,L,R):
    """General rational constant-velocity legs; no integral-chart formulas."""
    cost=Q(0);intervals=0
    if path[0][1]==1:R=Q(0)
    if path[0][1]==-1:L=Q(0)
    for (ta,xa),(tb,xb) in zip(path,path[1:]):
        assert tb>ta and abs(xb-xa)<=tb-ta and max(abs(xa),abs(xb))<=1
        velocity=(xb-xa)/(tb-ta);duration=tb-ta
        U0,W0=ta+xa,ta-xa
        rates=(1+velocity,1-velocity);starts=(U0,W0)
        cuts={Q(0),duration}
        for start,rate in zip(starts,rates):
            if not rate:continue
            lo=(field.n*start).numerator//(field.n*start).denominator-1
            end=start+rate*duration
            hi=(field.n*end).numerator//(field.n*end).denominator+1
            for k in range(lo,hi+1):
                for offset in (Q(0),field.a,field.b,Q(1)):
                    s=((k+offset)/field.n-start)/rate
                    if 0<s<duration:cuts.add(s)
        if 0<2-ta<duration:cuts.add(2-ta)
        first=sorted(cuts)
        for a,b in zip(first,first[1:]):
            s=(a+b)/2
            coords=[field.n*(start+rate*s) for start,rate in zip(starts,rates)]
            iu,iw=[v.numerator//v.denominator for v in coords]
            if field.orientation(iu)==field.orientation(iw):
                rate=rates[0]-rates[1]
                if rate:
                    at=(Q(iu-iw,field.n)-(U0-W0))/rate
                    if a<at<b:cuts.add(at)
            else:
                at=(Q(iu+iw+1,field.n)-(U0+W0))/2
                if a<at<b:cuts.add(at)
        cuts=sorted(cuts)
        def value(s):return field.cdf(ta+s,xa+velocity*s)
        for a,b in zip(cuts,cuts[1:]):
            fa,fb=value(a),value(b)
            assert value((a+b)/2)==(fa+fb)/2,("missing raw-field cut",ta,xa,tb,xb,a,b)
            amount,L=one_record(L,fa,fb,b-a);cost+=amount
            amount,R=one_record(R,1-fa,1-fb,b-a);cost+=amount
            intervals+=1
        if xb==1:R=Q(0)
        if xb==-1:L=Q(0)
    return cost,L,R,intervals


def reconstruct(edges,centers,field,name,uid,state):
    p=edges[name][uid];assert eligible(p,state)
    z,L,R=state;pro=p["provenance"];start=point(name,z)
    kind=pro["kind"]
    if kind=="center":
        return center_route(centers,field,len(centers)-1,pro["center_uid"],state)
    if kind=="first_endpoint":
        return [start,(start[0]+2,Q(-1))]
    if kind.startswith("deadline_"):
        return clean([start,(Q(2),Q(0)),(Q(3),Q(-1)),(Q(5),Q(1))])
    if kind=="axis_cell":
        w=Q(pro["exit_constant"])+sum(Q(a)*x for a,x in zip(pro["exit_linear"],state))
        end=point(pro["exit"],w)
        Us,Ws=start[0]+start[1],start[0]-start[1]
        Ue,We=end[0]+end[1],end[0]-end[1]
        U,W=(Ue,Ws) if pro["order"]=="UW" else (Us,We)
        prefix=clean([start,((U+W)/2,(U-W)/2),end])
    elif kind=="boundary_four_legs":
        values=list(state)
        for step in reversed(pro["elimination_steps"]):
            assert len(values)==step["variable"]
            values.append(Q(step["constant"])+sum(Q(a)*x for a,x in zip(step["linear"],values)))
        w=values[3];end=point(pro["exit"],w)
        sign=pro["initial_direction"];d1,d2,d3=values[4:]
        d4=d1-d2+d3-sign*(end[1]-start[1])
        ds=(d1,d2,d3,d4)
        hold=end[0]-start[0]-sum(ds)
        assert min(*ds,hold)>=0
        prefix=[start];t,x=start
        for i,d in enumerate(ds):
            t+=d;x+=sign*((-1)**i)*d
            prefix.append((t,x))
        assert x==end[1]
        prefix=clean(prefix+[end])
    else:raise ValueError(kind)
    _,L1,R1,_=integrate(field,prefix,L,R)
    next_state=(w,L1,R1)
    child=reconstruct(edges,centers,field,pro["exit"],pro["child_uid"],next_state)
    assert child[0]==prefix[-1]
    return clean(prefix+child[1:])


def initial_candidates(pieces):
    """Independent interval clipping and one-variable quadratic minima."""
    answers=[];tests=set()
    def state(x):return (x,(1+x)/2,(1-x)/2)
    for p in pieces:
        lo,hi=Q(0),Q(1);empty=False
        for row,b in p["inequalities"]:
            a=list(map(Q,row));b=Q(b)
            slope=a[0]+a[1]/2-a[2]/2
            rhs=b-a[1]/2-a[2]/2
            if slope>0:hi=min(hi,rhs/slope)
            elif slope<0:lo=max(lo,rhs/slope)
            elif rhs<0:empty=True
        if empty or lo>hi:continue
        q0=objective(p,state(Q(0)));qm=objective(p,state(Q(1,2)));q1=objective(p,state(Q(1)))
        A=2*(q1-2*qm+q0);B=q1-q0-A
        points={lo,hi}
        if A>0 and lo<=-B/(2*A)<=hi:points.add(-B/(2*A))
        for x in points:
            answers.append((objective(p,state(x)),x,p["uid"]));tests.add(x)
    assert answers
    return min(answers),tests


def replay_initial_profile(pieces):
    """Prove the complete initial-position envelope is two explicit quadratics.

Every eligible saved candidate is compared on its full exact interval,
not merely at sampled starts. Conversely, one candidate has exactly each
displayed polynomial and covers its whole claimed interval.
"""
    profile=[(Q(0),Q(7,8),(Q(79,64),Q(1,32),Q(-15,448))),
             (Q(7,8),Q(1),(Q(37,64),Q(49,32),Q(-57,64)))]
    covered=[False,False];checks=0
    for p in pieces:
        lo,hi=Q(0),Q(1);empty=False
        for row,b in p["inequalities"]:
            a=list(map(Q,row));b=Q(b)
            slope=a[0]+a[1]/2-a[2]/2;rhs=b-a[1]/2-a[2]/2
            if slope>0:hi=min(hi,rhs/slope)
            elif slope<0:lo=max(lo,rhs/slope)
            elif rhs<0:empty=True
        if empty or lo>hi:continue
        state=lambda x:(x,(1+x)/2,(1-x)/2)
        c=objective(p,state(Q(0)));m=objective(p,state(Q(1,2)));v=objective(p,state(Q(1)))
        A=2*(v-2*m+c);B=v-c-A
        for j,(a,b,coefficients) in enumerate(profile):
            q0,q1,q2=coefficients
            if (c,B,A)==coefficients and lo<=a<=b<=hi:covered[j]=True
            left,right=max(lo,a),min(hi,b)
            if left>right:continue
            aa,bb,cc=A-q2,B-q1,c-q0
            tests={left,right}
            if aa>0 and left<=-bb/(2*aa)<=right:tests.add(-bb/(2*aa))
            assert min(aa*x*x+bb*x+cc for x in tests)>=0,("initial profile domination",p["uid"],j)
            checks+=1
    assert all(covered),"explicit initial profile lacks a feasible attaining candidate"
    return profile,checks


def main():
    a=argparse.ArgumentParser(description=__doc__)
    a.add_argument("precenter");a.add_argument("center");a.add_argument("field");a.add_argument("output")
    args=a.parse_args()
    pre=json.loads(read(args.precenter));center=json.loads(read(args.center))
    assert pre["format"]=="exact-n1-fixed-field-response-v1" and pre["complete"]
    assert pre["sources"]["decompressed_sha256"]["field"]==hashlib.sha256(read(args.field)).hexdigest()
    assert pre["sources"]["decompressed_sha256"]["center_envelope"]==hashlib.sha256(read(args.center)).hexdigest()
    assert center["n"]==1 and Q(center["epsilon"])==Q(1,2) and center["depth"]==5
    field=Field(json.loads(read(args.field)),Q(1,2))
    assert field.n==1
    assert {(j,k):Q(v,field.den) for (j,k),v in field.pre.items()}=={
        (0,2):Q(1),(1,1):Q(7,8),(2,2):Q(1),(3,1):Q(0),(4,2):Q(1)}
    edges={name:{p["uid"]:p for p in value["active_pieces"]} for name,value in pre["edges"].items()}
    centers=parse_certificate(center)
    best,tests=initial_candidates(list(edges["initial"].values()))
    profile,profile_checks=replay_initial_profile(list(edges["initial"].values()))
    assert best[0]==Q(pre["initial_minimum"]["value"])
    tests|={Q(i,64) for i in range(65)}
    initial_checks=intervals=0;maxlegs=0;witness=None
    for x in sorted(tests):
        state=(x,(1+x)/2,(1-x)/2)
        value,uid=minimum(list(edges["initial"].values()),state)
        path=reconstruct(edges,centers,field,"initial",uid,state)
        actual,L,R,count=integrate(field,path,state[1],state[2])
        assert actual==value and L==R==0,("initial route mismatch",x,value,actual,path)
        branch=profile[0] if x<=Q(7,8) else profile[1]
        a,b,(c,d,e)=branch
        assert value==c+d*x+e*x*x
        turning=(1-x)/2
        simple=clean([(Q(0),x),(turning,(1+x)/2),(Q(2),Q(-1)),(Q(4),Q(1))])
        simple_cost,SL,SR,simple_count=integrate(field,simple,state[1],state[2])
        assert simple_cost==value and SL==SR==0,"explicit three-leg response mismatch"
        assert path[-1][0]<=6
        initial_checks+=1;intervals+=count+simple_count;maxlegs=max(maxlegs,len(path)-1)
        if x==best[1]:
            witness={"value":str(value),"initial_position":str(x),
                     "path":[list(map(str,p)) for p in path]}
    edge_checks=0
    for name,items in edges.items():
        if name=="initial":continue
        states=set()
        for p in items.values():
            vs=[tuple(map(Q,v)) for v in p["vertices"]]
            states.update(vs)
            states.add(tuple(sum(v[i] for v in vs)/len(vs) for i in range(3)))
        for state in sorted(states):
            value,uid=minimum(list(items.values()),state)
            path=reconstruct(edges,centers,field,name,uid,state)
            actual,L,R,count=integrate(field,path,state[1],state[2])
            assert actual==value and L==R==0,("edge route mismatch",name,state,value,actual,path)
            edge_checks+=1;intervals+=count
    report={"status":"PASS","scope":"Independent raw-CDF chronological replay and exact initial-curve exhaustion of the saved precenter envelope; the source proof/regeneration supplies completeness over all legal responses.",
            "precenter_json_sha256":hashlib.sha256(read(args.precenter)).hexdigest(),
            "fixed_field_security":str(best[0]),"initial_curve_route_checks":initial_checks,
            "initial_profile_exact_interval_comparisons":profile_checks,
            "fixed_initial_position_value":[{"interval":[str(a),str(b)],"coefficients_1_x_x2":list(map(str,c))} for a,b,c in profile],
            "edge_route_checks":edge_checks,"affine_field_interval_checks":intervals,
            "maximum_initial_witness_legs":maxlegs,"attaining_response":witness}
    Path(args.output).write_text(json.dumps(report,indent=2)+"\n")
    print(json.dumps(report,indent=2))

if __name__=="__main__":main()
