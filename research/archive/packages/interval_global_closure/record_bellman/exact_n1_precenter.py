#!/usr/bin/env python3
"""Exact continuous response to the supplied n=1 full-width Princess field.

This fixed-field certificate includes free initial positions, every
precenter cell, and the previously certified complete center envelope.
It is not the value of the unrestricted two-player game. Every arithmetic
decision uses Fraction/integer arithmetic; elapsed times are diagnostic.
"""
from fractions import Fraction as Q
from pathlib import Path
from itertools import product
import argparse,gzip,hashlib,json,sys,time

from exact_center_renewal_envelope import (Quad,Envelope,affine_quad,product_quad,zero_quad,
    constraints_compose,canonical,read_bytes,write_json,encode,history_digest,compact_layer)
from eliminate_quadratic_interval import eliminate_last_variable
from build_endpoint_tail_charts import Field


def add(*forms):
    return tuple(sum(x,Q(0)) for x in zip(*forms))
def scale(a,k):
    return tuple(k*x for x in a)
def unit(d,j):
    return tuple(Q(int(i==j+1)) for i in range(d+1))
def const(d,a):
    return (Q(a),)+(Q(0),)*d
def inequality(form):
    """form<=0 as an inequality row."""
    return form[1:],-form[0]
def coord(edge,z):
    return tuple(add(const(len(z)-1,b),scale(z,a)) for b,a in edge["map"])
def field(f,U,W):
    return add(const(len(U)-1,f[0]),scale(U,f[1]),scale(W,f[2]))
def embed_rows(rows,d):
    return [(tuple(a)+(Q(0),)*(d-3),b) for a,b in rows]


EDGES={
 "center":{"map":((0,1),(0,1)),"range":(0,2)},
 "endpoint":{"map":((0,1),(-2,1)),"range":(1,2)},
 "deadline":{"map":((2,0),(0,1)),"range":(0,2)},
 "flat_entry":{"map":((0,1),(1,0)),"range":(1,2)},
 "time_one":{"map":((0,1),(2,-1)),"range":(1,2)},
 "d_left":{"map":((1,0),(0,1)),"range":(0,1)},
 "d_bottom":{"map":((0,1),(0,0)),"range":(1,2)},
 "b_bottom":{"map":((0,1),(0,0)),"range":(0,1)},
 "c_left":{"map":((1,0),(0,1)),"range":(-1,0)},
 "initial":{"map":((0,1),(0,-1)),"range":(0,1)},
}
FIELDS={
 "A":(Q(1,2),Q(7,16),Q(-1,16)),
 "B":(Q(1,2),Q(7,16),Q(-7,16)),
 "C":(Q(7,8),Q(1,16),Q(-1,16)),
 "D":(Q(7,8),Q(1,16),Q(-7,16)),
 "E":(Q(1),Q(0),Q(-1,2)),
 "F":(Q(1,2),Q(0),Q(0)),
}
CELL_VERTICES={
 "A":((0,0),(1,-1),(1,0)),
 "B":((0,0),(1,0),(1,1)),
 "C":((1,-1),(1,0),(2,0)),
 "D":((1,0),(1,1),(2,0)),
 "E":((1,1),(2,0),(2,1)),
 "F":((1,1),(2,1),(2,2)),
}
CELL_ROWS={
 "A":((1,0,1),(0,1,0),(-1,-1,0)),
 "B":((1,0,1),(0,-1,0),(-1,1,0)),
 "C":((-1,0,-1),(0,1,0),(1,-1,2)),
 "D":((-1,0,-1),(0,-1,0),(1,1,2)),
 "E":((1,0,2),(0,1,1),(-1,-1,-2)),
 "F":((1,0,2),(0,-1,-1),(-1,1,0)),
}


def cell_constraints(f,U,W):
    name=next(k for k,v in FIELDS.items() if v==f)
    return [inequality(add(scale(U,a),scale(W,b),const(len(U)-1,-c))) for a,b,c in CELL_ROWS[name]]


def validate_sources(fieldfile,centerfile,centercharts,tailfile):
    """Bind this six-cell construction to its actual field and continuations.

The chart/envelope regeneration commands remain separate, independent
steps: these hashes bind their checked outputs, rather than replacing
their mathematical or computational validation.
"""
    paths={"field":fieldfile,"center_envelope":centerfile,
           "center_charts":centercharts,"endpoint_charts":tailfile}
    raw={name:read_bytes(path) for name,path in paths.items()}
    data={name:json.loads(value) for name,value in raw.items()}
    hashes={name:hashlib.sha256(value).hexdigest() for name,value in raw.items()}
    f=Field(data["field"],Q(1,2))
    assert f.n==1
    assert {(j,k):Q(v,f.den) for (j,k),v in f.pre.items()}=={
        (0,2):Q(1),(1,1):Q(7,8),(2,2):Q(1),(3,1):Q(0),(4,2):Q(1)}
    center=data["center_envelope"]
    assert center["format"]=="exact-center-renewal-envelope-v1"
    assert center["n"]==1 and Q(center["epsilon"])==Q(1,2) and center["depth"]==5
    assert center["source_sha256"]==hashes["center_charts"]
    for name,fmt in (("center_charts","center-excursion-charts-v1"),
                     ("endpoint_charts","endpoint-tail-charts-v1")):
        d=data[name]
        assert d["format"]==fmt and d["n"]==1 and Q(d["epsilon"])==Q(1,2)
        assert d["source_sha256"]==hashes["field"]
    checks=0
    for name,vertices in CELL_VERTICES.items():
        # The common-threshold geometry makes each displayed triangle
        # affine; these exact samples independently bind its coefficients.
        samples=set(tuple(map(Q,v)) for v in vertices)
        samples.add(tuple(sum(Q(v[j]) for v in vertices)/3 for j in range(2)))
        for i,v in enumerate(vertices):
            w=vertices[(i+1)%3]
            samples.add(tuple(Q(v[j]+w[j],2) for j in range(2)))
        c,u,w=FIELDS[name]
        for U,W in samples:
            assert f.cdf((U+W)/2,(U-W)/2)==c+u*U+w*W,(name,U,W)
            assert all(a*U+b*W<=v for a,b,v in CELL_ROWS[name])
            checks+=1
    return {"decompressed_sha256":hashes,"six_cell_field_checks":checks}


def admissible(edge,f):
    z,L,R=unit(3,0),unit(3,1),unit(3,2)
    U,W=coord(edge,z);F=field(f,U,W);lo,hi=map(Q,edge["range"])
    return [inequality(add(const(3,lo),scale(z,-1))),inequality(add(z,const(3,-hi))),
            inequality(add(const(3,Q(1,2)),scale(L,-1))),inequality(add(L,scale(F,-1))),
            inequality(scale(R,-1)),inequality(add(R,F,const(3,-1)))]


def seed_center(certificate):
    data=json.loads(read_bytes(certificate));env=Envelope()
    for p in data["envelopes"][-1]["active_pieces"]:
        q=p["objective"]
        objective=Quad(Q(q["c"]),tuple(map(Q,q["linear"])),tuple(tuple(map(Q,r)) for r in q["hessian"]))
        rows=[(tuple(map(Q,a)),Q(b)) for a,b in p["inequalities"]]
        rows+=admissible(EDGES["center"],(Q(1,2),0,0))
        env.add(objective,rows,{"kind":"center","center_uid":p["uid"]})
    return env


def seed_endpoint(tailfile):
    data=json.loads(read_bytes(tailfile));env=Envelope()
    # Parameters(z=U,L,R), endpoint time=z-1.
    t=(-Q(1),Q(1),Q(0),Q(0));L=unit(3,1)
    for j,ch in enumerate(data["charts"]):
        c=list(map(Q,ch["coefficients"]))
        q=Quad(c[0],(c[1],c[2]),((c[3],c[4]/2),(c[4]/2,c[5])))
        rows=[((Q(a),Q(b)),Q(v)) for a,b,v in ch["inequalities"]]
        rows=constraints_compose(rows,(t,L))+admissible(EDGES["endpoint"],(Q(1),0,0))
        env.add(q.compose((t,L)),rows,{"kind":"first_endpoint","tail_chart":j})
    return env


def seed_deadline():
    env=Envelope();z,L,R=unit(3,0),unit(3,1),unit(3,2)
    base=affine_quad((Q(1,2),0,0,3)) # exact center(t2,L=.5,R)
    duration=scale(add(const(3,1),scale(z,-1)),Q(1,2))
    gap=add(L,const(3,-Q(1,2)))
    q=base.add(product_quad(add(L,R),duration)).add(product_quad(gap,scale(gap,-Q(1,2))))
    q=q.add(product_quad(add(const(3,Q(1,2)),R),const(3,Q(1,2))))
    rows=admissible(EDGES["deadline"],FIELDS["E"])+[((1,0,0),Q(1))]
    env.add(q,rows,{"kind":"deadline_low"})
    duration=scale(add(const(3,2),scale(z,-1)),Q(1,2))
    q=base.add(product_quad(add(L,R),duration))
    rows=admissible(EDGES["deadline"],FIELDS["F"])+[((-1,0,0),Q(-1))]
    env.add(q,rows,{"kind":"deadline_high"})
    return env


def leg_branches(f,U0,W0,U1,W1,L,R,objective,rows,word):
    d=len(U0)-1
    if W0==W1:
        direction=1;duration=scale(add(U1,scale(U0,-1)),Q(1,2));rate=2*f[1]
    elif U0==U1:
        direction=-1;duration=scale(add(W1,scale(W0,-1)),Q(1,2));rate=-2*f[2]
    else:
        raise ValueError("not a unit-axis leg")
    assert rate>=0
    Fend=field(f,U1,W1)
    cost=objective.add(product_quad(add(L,R),duration))
    rows=rows+[inequality(scale(duration,-1)),
               inequality(add(W1,scale(U1,-1))), # do not pass the center
               inequality(add(U1,scale(W1,-1),const(d,-2)))]
    rows+=cell_constraints(f,U1,W1)
    if not rate:
        return [(L,R,cost,rows,word+[{"direction":direction,"capture":False}])]
    record=L if direction<0 else R
    threshold=Fend if direction<0 else add(const(d,1),scale(Fend,-1))
    gap=add(record,scale(threshold,-1))
    out=[(L,R,cost,rows+[inequality(gap)],word+[{"direction":direction,"capture":False}])]
    dropped=cost.add(product_quad(gap,scale(gap,-1/(2*rate))))
    out.append((threshold if direction<0 else L,threshold if direction>0 else R,
                dropped,rows+[inequality(scale(gap,-1))],word+[{"direction":direction,"capture":True}]))
    return out


def axis_transition(entry_name,exit_name,future,f):
    entry,exit=EDGES[entry_name],EDGES[exit_name]
    z,L0,R0,w=(unit(4,j) for j in range(4))
    Us,Ws=coord(entry,z);Ue,We=coord(exit,w)
    base_rows=embed_rows(admissible(entry,f),4)
    base_rows+=cell_constraints(f,Us,Ws)
    base_rows += [inequality(add(Us,scale(Ue,-1))),inequality(add(Ws,scale(We,-1)))]
    outgoing=[]
    for order in ("UW","WU"):
        points=[(Us,Ws),(Ue,Ws) if order=="UW" else (Us,We),(Ue,We)]
        branches=[(L0,R0,zero_quad(4),base_rows,[])]
        for (U0,W0),(U1,W1) in zip(points,points[1:]):
            new=[]
            for L,R,q,rows,word in branches:
                new+=leg_branches(f,U0,W0,U1,W1,L,R,q,rows,word)
            branches=new
        for L,R,q,rows,word in branches:
            for child in future.active:
                maps=(w,L,R)
                objective=q.add(child.objective.compose(maps))
                feasible=rows+constraints_compose(child.rows,maps)
                for candidate in eliminate_last_variable(feasible,objective.c,objective.linear,objective.hessian,interval=exit["range"]):
                    c=candidate.objective
                    outgoing.append((Quad(c.constant,c.linear,c.hessian),candidate.inequalities,
                         {"kind":"axis_cell","entry":entry_name,"exit":exit_name,"order":order,
                          "capture_pattern":word,"child_uid":child.uid,
                          "exit_constant":str(candidate.h_constant),"exit_linear":list(map(str,candidate.h_linear)),
                          "origins":list(candidate.origins)}))
    return outgoing


def build_axis(name,f,exits,known):
    env=Envelope();generated=0;start=time.monotonic()
    for target in exits:
        for q,rows,pro in axis_transition(name,target,known[target],f):
            env.add(q,rows,pro);generated+=1
    print(json.dumps({"edge":name,"retained":len(env.active),"nonempty":len(env.registry),
                      "empty":env.empty,"generated":generated,"seconds":time.monotonic()-start}),flush=True)
    return env


def possible_box(rows,bounds):
    """Sound exact interval propagation; False only proves infeasibility."""
    bounds=[list(map(Q,p)) for p in bounds]
    for _ in range(6):
        changed=False
        for a,b in rows:
            terms=[x*(bounds[j][0] if x>=0 else bounds[j][1]) for j,x in enumerate(a)]
            low=sum(terms,Q(0))
            if low>b:return False
            for j,x in enumerate(a):
                if not x:continue
                limit=(b-low+terms[j])/x
                if x>0 and limit<bounds[j][1]:
                    bounds[j][1]=limit;changed=True
                elif x<0 and limit>bounds[j][0]:
                    bounds[j][0]=limit;changed=True
                if bounds[j][0]>bounds[j][1]:return False
        if not changed:break
    return True


def boundary_transition(entry_name,exit_name,future):
    """All four alternating unit legs plus a final stationary hold."""
    f=FIELDS["C"];entry=EDGES[entry_name];exit=EDGES[exit_name]
    d=7;z,L0,R0,w,d1,d2,d3=(unit(d,j) for j in range(d))
    Us,Ws=coord(entry,z);Ue,We=coord(exit,w)
    ts=scale(add(Us,Ws),Q(1,2));xs=scale(add(Us,scale(Ws,-1)),Q(1,2))
    te=scale(add(Ue,We),Q(1,2));xe=scale(add(Ue,scale(We,-1)),Q(1,2))
    dx=add(xe,scale(xs,-1));T=add(te,scale(ts,-1))
    for sign in (1,-1):
        d4=add(d1,scale(d2,-1),d3,scale(dx,-sign))
        durations=[d1,d2,d3,d4]
        hold=add(T,*(scale(v,-1) for v in durations))
        rows=embed_rows(admissible(entry,f),d)+[inequality(scale(v,-1)) for v in durations+[hold]]
        rows+=cell_constraints(f,Us,Ws)+cell_constraints(f,Ue,We)
        points=[(Us,Ws)];tt,xx=ts,xs
        for j,duration in enumerate(durations):
            tt=add(tt,duration);xx=add(xx,scale(duration,sign*((-1)**j)))
            points.append((add(tt,xx),add(tt,scale(xx,-1))))
        assert xx==xe
        assert add(tt,hold)==te
        branches=[(L0,R0,zero_quad(d),rows,[])]
        for (U0,W0),(U1,W1) in zip(points,points[1:]):
            new=[]
            for L,R,q,ie,word in branches:
                new+=leg_branches(f,U0,W0,U1,W1,L,R,q,ie,word)
            branches=new
        for L,R,q,ie,word in branches:
            q=q.add(product_quad(add(L,R),hold))
            for child in future.active:
                maps=(w,L,R)
                objective=q.add(child.objective.compose(maps))
                rows=canonical(ie+constraints_compose(child.rows,maps))
                if rows is None:continue
                choices=[(objective,rows,[])]
                for variable in (6,5,4,3):
                    next_choices={}
                    interval=exit["range"] if variable==3 else (0,1)
                    bounds=[entry["range"],(Q(1,2),1),(0,Q(1,2)),exit["range"]]+[(0,1)]*(variable-3)
                    for oldq,oldrows,steps in choices:
                        if not possible_box(oldrows,bounds):continue
                        for item in eliminate_last_variable(oldrows,oldq.c,oldq.linear,oldq.hessian,interval=interval):
                            cq=item.objective
                            qnew=Quad(cq.constant,cq.linear,cq.hessian)
                            newrows=canonical(item.inequalities)
                            if newrows is None or not possible_box(newrows,bounds[:-1]):continue
                            key=(qnew,newrows)
                            if key not in next_choices:
                                next_choices[key]=(qnew,newrows,steps+[{"variable":variable,"constant":str(item.h_constant),
                                    "linear":list(map(str,item.h_linear)),"origins":list(item.origins)}])
                    choices=list(next_choices.values())
                    if not choices:break
                for finalq,finalrows,steps in choices:
                    yield finalq,finalrows,{"kind":"boundary_four_legs","entry":entry_name,"exit":exit_name,
                         "initial_direction":sign,"capture_pattern":word,"child_uid":child.uid,
                         "elimination_steps":steps}


def build_boundary(known):
    env=Envelope();start=time.monotonic();count=0
    for target in ("d_bottom","endpoint"):
        for q,rows,pro in boundary_transition("c_left",target,known[target]):
            env.add(q,rows,pro);count+=1
            if count%1000==0:
                print(json.dumps({"edge":"c_left","target":target,"generated":count,
                                  "retained":len(env.active),"seconds":time.monotonic()-start}),flush=True)
    print(json.dumps({"edge":"c_left","generated":count,"nonempty":len(env.registry),"empty":env.empty,
                      "retained":len(env.active),"seconds":time.monotonic()-start}),flush=True)
    return env


def initial_minimum(envelope):
    # Exact initial uniform radial CDF: L=(1+z)/2,R=(1-z)/2.
    maps=((Q(0),Q(1)),(Q(1,2),Q(1,2)),(Q(1,2),Q(-1,2)))
    best=None;count=0
    for p in envelope.active:
        q=p.objective.compose(maps);rows=constraints_compose(p.rows,maps)
        for c in eliminate_last_variable(rows,q.c,q.linear,q.hessian,interval=(0,1)):
            assert not c.objective.linear
            assert c.eligible(())
            value=c.objective.constant;z=c.h_constant
            count+=1
            if best is None or (value,z,p.uid)<best:best=(value,z,p.uid)
    assert best is not None
    return {"value":str(best[0]),"initial_position":str(best[1]),"initial_piece":best[2],
            "constant_candidates":count}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--center",required=True);p.add_argument("--tail",required=True);p.add_argument("--output",required=True)
    p.add_argument("--field",required=True);p.add_argument("--center-charts",required=True)
    p.add_argument("--complete",action="store_true",help="Include boundary cell C and free initial positions.")
    p.add_argument("--verify",action="store_true",help="Regenerate all exact candidates/pruning and compare the saved certificate.")
    p.add_argument("--history-output",help="Optional complete generated candidates/pruning evidence; .gz is supported.")
    a=p.parse_args()
    sources=validate_sources(a.field,a.center,a.center_charts,a.tail)
    known={"center":seed_center(a.center),"endpoint":seed_endpoint(a.tail),"deadline":seed_deadline()}
    print(json.dumps({"seed_counts":{k:len(v.active) for k,v in known.items()}}),flush=True)
    for name,f,exits in [
        ("flat_entry",FIELDS["F"],["center","deadline"]),
        ("time_one",FIELDS["E"],["flat_entry","deadline"]),
        ("d_left",FIELDS["D"],["time_one"]),
        ("d_bottom",FIELDS["D"],["time_one"]),
        ("b_bottom",FIELDS["B"],["center","d_left"]),
    ]:
        known[name]=build_axis(name,f,exits,known)
    final=None
    if a.complete:
        known["c_left"]=build_boundary(known)
        known["initial"]=build_axis("initial",FIELDS["A"],["c_left","b_bottom"],known)
        final=initial_minimum(known["initial"])
        print(json.dumps({"initial_minimum":final}),flush=True)
    result={"format":"exact-n1-fixed-field-response-v1",
            "scope":"Complete continuous response to this supplied n1 full-width field, including free initial positions; no unrestricted-game value claim." if a.complete else "Incomplete until physical-boundary C and initial A have exact transitions.",
            "complete":a.complete,"sources":sources,
            "initial_minimum":final,
            "edges":{k:compact_layer(v) for k,v in known.items()}}
    if a.verify:
        actual=json.loads(json.dumps(result,default=encode))
        expected=json.loads(read_bytes(a.output))
        assert actual==expected,"exact precenter regeneration mismatch"
        print(json.dumps({"status":"PASS","check":"complete exact precenter regeneration",
                          "initial_minimum":final,"edges":len(known)}),flush=True)
    else:
        write_json(a.output,result)
    if a.history_output:
        write_json(a.history_output,{"edges":{name:{"active_uids":[p.uid for p in env.active],
                          "all_generated_pieces":env.registry,"domination_replay":env.proofs}
                          for name,env in known.items()}})

if __name__=="__main__":main()
