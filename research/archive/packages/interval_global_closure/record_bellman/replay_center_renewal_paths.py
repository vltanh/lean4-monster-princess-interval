#!/usr/bin/env python3
"""Independent chronological replay of exact center-envelope routes.

Reconstructs the minimizing physical path from saved affine-height
witnesses, then integrates its running records directly against the
threshold-averaged field. It does not use the quadratic integral charts
or the envelope objective to compute the physical cost.
"""
from fractions import Fraction as Q
from pathlib import Path
from itertools import product
import argparse
import gzip
import hashlib
import json

from build_endpoint_tail_charts import Field


def read_bytes(path):
    raw=Path(path).read_bytes()
    return gzip.decompress(raw) if raw[:2]==b"\x1f\x8b" else raw


def eligible(piece,state):
    return all(sum(Q(a)*x for a,x in zip(row,state))<=Q(b) for row,b in piece["inequalities"])


def objective(piece,state):
    q=piece["objective"]
    c=Q(q["c"]);l=list(map(Q,q["linear"]));H=[list(map(Q,row)) for row in q["hessian"]]
    return c+sum(a*x for a,x in zip(l,state))+sum(state[i]*H[i][j]*state[j] for i in range(3) for j in range(3))


def minimum(pieces,state):
    options=[(objective(p,state),p["uid"]) for p in pieces if eligible(p,state)]
    assert options,("empty eligibility fiber",state)
    return min(options)


def parse_certificate(data):
    return [{p["uid"]:p for p in layer["active_pieces"]} for layer in data["envelopes"]]


def reconstruct(layers,field,depth,uid,state):
    p=layers[depth][uid]
    assert eligible(p,state)
    t,L,R=state;pro=p["provenance"];sign=pro["sign"]
    if pro["kind"] in ("direct_tour","late_tour"):
        return [(t,Q(0)),(t+1,Q(sign)),(t+3,Q(-sign))]
    assert pro["kind"]=="return_triangle"
    h=Q(pro["h_constant"])+sum(Q(a)*x for a,x in zip(pro["h_linear"],state))
    assert 0<=h<=min(Q(1),2-t)
    # Deliberately derive the update from direct threshold averaging,
    # not from the saved integral-chart update coefficients.
    if sign>0:
        next_state=(t+2*h,L,min(R,1-field.cdf(t+h,h)))
    else:
        next_state=(t+2*h,min(L,field.cdf(t+h,-h)),R)
    child=reconstruct(layers,field,pro["child_depth"],pro["child_uid"],next_state)
    assert child[0]==(t+2*h,0)
    raw=[(t,Q(0)),(t+h,sign*h),(t+2*h,Q(0))]+child[1:]
    out=[]
    for point in raw:
        if not out or point!=out[-1]:
            out.append(point)
    return out


def one_record(record,a,b,duration):
    record=min(record,a)
    if b>=record:
        return duration*record,record
    assert a>=record>b
    if a==record:
        return duration*(a+b)/2,b
    fraction=(a-record)/(a-b)
    return duration*(record*fraction+(record+b)*(1-fraction)/2),b


def integrate_path(field,path,L,R):
    total=Q(0);checks=0
    for (ta,xa),(tb,xb) in zip(path,path[1:]):
        assert tb>ta and abs(xb-xa)==tb-ta and max(abs(xa),abs(xb))<=1
        sign=1 if xb>xa else -1
        fixed=ta-sign*xa
        za,zb=ta+sign*xa,tb+sign*xb
        assert fixed==tb-sign*xb and zb>za
        frac=field.n*fixed
        frac-=frac.numerator//frac.denominator
        lo=(field.n*za).numerator//(field.n*za).denominator-1
        hi=(field.n*zb).numerator//(field.n*zb).denominator+2
        cuts={za,zb}
        for k in range(lo,hi+1):
            for f in (Q(0),field.a,field.b,frac,1-frac,Q(1)):
                z=(k+f)/field.n
                if za<z<zb:cuts.add(z)
        for z in (fixed,4-fixed):
            if za<z<zb:cuts.add(z)
        cuts=sorted(cuts)
        def value(z):
            return field.cdf((fixed+z)/2,sign*(z-fixed)/2)
        for a,b in zip(cuts,cuts[1:]):
            fa,fb=value(a),value(b)
            assert value((a+b)/2)==(fa+fb)/2,("missing affine cut",fixed,a,b)
            amount,L=one_record(L,fa,fb,(b-a)/2)
            total+=amount
            amount,R=one_record(R,1-fa,1-fb,(b-a)/2)
            total+=amount;checks+=1
        if xb==-1:L=Q(0)
        if xb==1:R=Q(0)
    assert L==R==0
    return total,checks


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("certificate")
    parser.add_argument("field")
    parser.add_argument("output")
    parser.add_argument("--raw-history",help="Optional uncompressed full generation history for raw/pruned sample comparisons.")
    args=parser.parse_args()
    raw=read_bytes(args.certificate)
    data=json.loads(raw);layers=parse_certificate(data)
    field=Field(json.loads(read_bytes(args.field)),Q(data["epsilon"]))
    assert field.n==data["n"]
    depth=data["depth"];pieces=list(layers[-1].values())
    states={(Q(t,4),Q(L,8),Q(R,8)) for t,L,R in product(range(9),range(5),range(5))}
    for p in pieces:
        vs=[tuple(map(Q,v)) for v in p["vertices"]]
        states.update(v for v in vs if v[0]<=2)
        center=tuple(sum(v[i] for v in vs)/len(vs) for i in range(3))
        if center[0]<=2:states.add(center)
    checked=intervals=0;max_legs=0;example=None
    for state in sorted(states):
        value,uid=minimum(pieces,state)
        path=reconstruct(layers,field,depth,uid,state)
        actual,count=integrate_path(field,path,state[1],state[2])
        assert actual==value,("physical/envelope mismatch",state,value,actual,path)
        assert path[-1][0]<=6
        assert len(path)-1<=8*field.n+4 if Q(data["epsilon"])==Q(1,2) else len(path)-1<=24*field.n+4
        checked+=1;intervals+=count;max_legs=max(max_legs,len(path)-1)
        if state==(0,Q(1,2),Q(1,2)):
            example={"state":list(map(str,state)),"value":str(value),
                     "physical_path":[list(map(str,p)) for p in path]}
    raw_checks=0
    if args.raw_history:
        histories=json.loads(read_bytes(args.raw_history))["envelopes"]
        sample=[(t,L,R) for t in (Q(0),Q(1,3),Q(1),Q(2))
                for L,R in ((Q(0),Q(0)),(Q(1,2),Q(0)),(Q(0),Q(1,2)),(Q(1,2),Q(1,2)),(Q(1,8),Q(3,8)))]
        for k,history in enumerate(histories):
            for state in sample:
                assert minimum(history["all_generated_pieces"],state)[0]==minimum(list(layers[k].values()),state)[0]
                raw_checks+=1
    report={"status":"PASS","scope":"Independent direct chronological integration of reconstructed exact-envelope minimizers; sampled raw/pruned regression. Finite-depth completeness is supplied by the normal-form proof and complete exact regeneration.",
            "certificate_sha256":hashlib.sha256(raw).hexdigest(),
            "certificate_sha256_scope":"decompressed JSON bytes",
            "depth":depth,"final_pieces":len(pieces),"physical_route_checks":checked,
            "affine_field_interval_checks":intervals,"raw_pruned_sample_checks":raw_checks,
            "maximum_checked_legs":max_legs,"initial_center_example":example}
    payload=(json.dumps(report,indent=2)+"\n").encode()
    Path(args.output).write_bytes(gzip.compress(payload,mtime=0) if str(args.output).endswith(".gz") else payload)
    print(json.dumps(report,indent=2))


if __name__=="__main__":
    main()
