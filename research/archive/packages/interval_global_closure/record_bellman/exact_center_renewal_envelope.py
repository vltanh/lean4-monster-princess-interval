#!/usr/bin/env python3
"""Exact finite-depth center-renewal envelopes.

All geometry, objective composition, eligibility pruning and domination
checks use Fraction/integer arithmetic. This file is an operational
research fixture, not by itself a global game lower certificate.

The generic one-coordinate minimizer is supplied separately under
record_bellman. A retained candidate means a realizable formal
return-triangle/tour cost; a depth bound or a proved Bellman fixed point
is needed before its minimum can be called the exact center value.
"""
from __future__ import annotations
from dataclasses import dataclass
from fractions import Fraction as Q
from functools import lru_cache
from itertools import combinations
from pathlib import Path
import argparse
import gzip
import hashlib
import json
import math
import sys
import time

HERE = Path(__file__).resolve().parent
CORE = HERE if (HERE/"eliminate_quadratic_interval.py").exists() else HERE.parent/"finite-reduction-checkout/packages/interval_global_closure/record_bellman"
sys.path.insert(0, str(CORE))


def dot(a,b):
    return sum((x*y for x,y in zip(a,b)),Q(0))


def read_bytes(path):
    raw=Path(path).read_bytes()
    return gzip.decompress(raw) if raw[:2]==b"\x1f\x8b" else raw


def write_json(path,value):
    raw=(json.dumps(value,default=encode,indent=2)+"\n").encode()
    Path(path).write_bytes(gzip.compress(raw,mtime=0) if str(path).endswith(".gz") else raw)


@dataclass(frozen=True)
class Quad:
    c: Q
    linear: tuple
    hessian: tuple

    @property
    def dimension(self):
        return len(self.linear)

    def value(self,p):
        return self.c+dot(self.linear,p)+sum((p[i]*self.hessian[i][j]*p[j] for i in range(len(p)) for j in range(len(p))),Q(0))

    def polar(self,p,q):
        return self.c+dot(self.linear,tuple((x+y)/2 for x,y in zip(p,q)))+sum((p[i]*self.hessian[i][j]*q[j] for i in range(len(p)) for j in range(len(p))),Q(0))

    def subtract(self,other):
        return Quad(self.c-other.c,tuple(a-b for a,b in zip(self.linear,other.linear)),tuple(tuple(a-b for a,b in zip(x,y)) for x,y in zip(self.hessian,other.hessian)))

    def add(self,other):
        return Quad(self.c+other.c,tuple(a+b for a,b in zip(self.linear,other.linear)),tuple(tuple(a+b for a,b in zip(x,y)) for x,y in zip(self.hessian,other.hessian)))

    def compose(self,maps):
        """old variables = b+B*new variables, maps=(b,*B) per old variable."""
        old=self.dimension;new=len(maps[0])-1
        b=tuple(a[0] for a in maps)
        B=tuple(a[1:] for a in maps)
        Hb=tuple(dot(row,b) for row in self.hessian)
        c=self.c+dot(self.linear,b)+dot(b,Hb)
        linear=tuple(sum((B[i][j]*(self.linear[i]+2*Hb[i]) for i in range(old)),Q(0)) for j in range(new))
        H=tuple(tuple(sum((B[i][j]*self.hessian[i][k]*B[k][l] for i in range(old) for k in range(old)),Q(0)) for l in range(new)) for j in range(new))
        return Quad(c,linear,H)


def zero_quad(d):
    return Quad(Q(0),(Q(0),)*d,tuple((Q(0),)*d for _ in range(d)))


def affine_quad(a):
    d=len(a)-1
    return Quad(Q(a[0]),tuple(map(Q,a[1:])),tuple((Q(0),)*d for _ in range(d)))


def product_quad(a,b):
    d=len(a)-1
    return Quad(a[0]*b[0],tuple(a[0]*b[j+1]+b[0]*a[j+1] for j in range(d)),
                tuple(tuple((a[i+1]*b[j+1]+b[i+1]*a[j+1])/2 for j in range(d)) for i in range(d)))


def q_from_chart(q):
    """Chart basis1,t,h,r,t²,th,tr,h²,hr,r²."""
    q=tuple(map(Q,q))
    return Quad(q[0],q[1:4],((q[4],q[5]/2,q[6]/2),(q[5]/2,q[7],q[8]/2),(q[6]/2,q[8]/2,q[9])))


def constraints_compose(rows,maps):
    out=[]
    for a,b in rows:
        out.append((tuple(sum((a[i]*maps[i][j+1] for i in range(len(a))),Q(0)) for j in range(len(maps[0])-1)),
                    b-sum((a[i]*maps[i][0] for i in range(len(a))),Q(0))))
    return out


def canonical(rows):
    """Primitive integer normals and tightest rational parallel bound."""
    normals={}
    for a,b in rows:
        a=tuple(map(Q,a));b=Q(b)
        if not any(a):
            if b<0:return None
            continue
        den=math.lcm(*(z.denominator for z in a))
        ints=tuple(int(z*den) for z in a)
        g=math.gcd(*(abs(z) for z in ints))
        normal=tuple(z//g for z in ints)
        bound=b*den/g
        if normal not in normals or bound<normals[normal]:
            normals[normal]=bound
    return tuple(sorted(normals.items()))


def det3(a,b,c):
    return a[0]*(b[1]*c[2]-b[2]*c[1])-a[1]*(b[0]*c[2]-b[2]*c[0])+a[2]*(b[0]*c[1]-b[1]*c[0])


@lru_cache(maxsize=100000)
def poly_vertices(rows):
    """Exact vertices of a known bounded3D polytope; includes lower dimensions."""
    integers=[(tuple(int(x*b.denominator) for x in a),b.numerator) for a,b in rows]
    found=set()
    for selected in combinations(integers,3):
        A=[z[0] for z in selected];b=[z[1] for z in selected]
        denominator=det3(*A)
        if not denominator:continue
        nums=[]
        for col in range(3):
            C=[list(row) for row in A]
            for i in range(3):C[i][col]=b[i]
            nums.append(det3(*C))
        if denominator<0:denominator=-denominator;nums=[-z for z in nums]
        if all(sum(a[i]*nums[i] for i in range(3))<=b*denominator for a,b in integers):
            found.add(tuple(Q(z,denominator) for z in nums))
    return tuple(sorted(found))


def eligibility(rows):
    rows=canonical(rows)
    if rows is None:return None
    vertices=poly_vertices(rows)
    if not vertices:return None
    # A compact polytope is the intersection of its active supporting
    # inequalities; removing constraints strict on every vertex is exact.
    active=tuple((a,b) for a,b in rows if any(dot(a,p)==b for p in vertices))
    return active,vertices


@dataclass
class Piece:
    uid: int
    objective: Quad
    rows: tuple
    vertices: tuple
    provenance: dict


class Envelope:
    def __init__(self,exact_min_fallback=False):
        self.registry=[]
        self.active=[]
        self.proofs=[]
        self.empty=0
        self.exact_min_fallback=exact_min_fallback
        self.counts={"domain_tests":0,"polar_tests":0,"exact_min_tests":0,"dominated":0}

    def dominates(self,better,worse):
        self.counts["domain_tests"]+=1
        if any(dot(a,p)>b for a,b in better.rows for p in worse.vertices):return False
        diff=worse.objective.subtract(better.objective)
        if any(diff.value(p)<0 for p in worse.vertices):return False
        self.counts["polar_tests"]+=1
        if all(diff.polar(p,q)>=0 for i,p in enumerate(worse.vertices) for q in worse.vertices[i:]):
            return "quadratic_polar"
        if self.exact_min_fallback:
            from exact_quadratic_polytope import minimize_quadratic
            self.counts["exact_min_tests"]+=1
            result=minimize_quadratic(worse.rows,diff.c,diff.linear,diff.hessian)
            assert result is not None
            if result.value>=0:return "exact_quadratic_minimum"
        return False

    def add(self,objective,rows,provenance):
        domain=eligibility(rows)
        if domain is None:
            self.empty+=1
            return None
        rows,vertices=domain
        piece=Piece(len(self.registry),objective,rows,vertices,provenance)
        self.registry.append(piece)
        for old in self.active:
            method=self.dominates(old,piece)
            if method:
                self.proofs.append({"removed":piece.uid,"dominator":old.uid,"method":method})
                self.counts["dominated"]+=1
                return piece
        keep=[]
        for old in self.active:
            method=self.dominates(piece,old)
            if method:
                self.proofs.append({"removed":old.uid,"dominator":piece.uid,"method":method})
                self.counts["dominated"]+=1
            else:
                keep.append(old)
        self.active=keep+[piece]
        return piece

    def value(self,state):
        eligible=[p for p in self.active if all(dot(a,state)<=b for a,b in p.rows)]
        assert eligible,("uncovered state",state)
        value,piece=min((p.objective.value(state),p.uid) for p in eligible)
        return value,piece


def box3(tmax=Q(3)):
    return [((-1,0,0),0),((1,0,0),tmax),((0,-1,0),0),((0,1,0),Q(1,2)),((0,0,-1),0),((0,0,1),Q(1,2))]


def load_charts(path):
    data=json.loads(read_bytes(path))
    assert data["format"]=="center-excursion-charts-v1"
    out=[]
    for i,ch in enumerate(data["charts"]):
        out.append({"id":i,"rows":tuple((tuple(map(Q,row[:3])),Q(row[3])) for row in ch["inequalities"]),
                    "objective":q_from_chart(ch["coefficients"]),"update":tuple(map(Q,ch["record_update"]))})
    return data,out


def direct_envelope(charts,exact_min=False):
    envelope=Envelope(exact_min)
    # Center variables(t,L,R), chart variables(t,h,r).
    for sign in (1,-1):
        rec=2 if sign>0 else 1
        maps=[(Q(0),Q(1),Q(0),Q(0)),(Q(1),Q(0),Q(0),Q(0)),
              tuple([Q(0)]+[Q(int(j==rec)) for j in range(3)])]
        extra=affine_quad((0,0,3,0) if sign>0 else (0,0,0,3))
        for ch in charts:
            objective=ch["objective"].compose(maps).add(extra)
            rows=constraints_compose(ch["rows"],maps)+box3(2)
            envelope.add(objective,rows,{"kind":"direct_tour","sign":sign,"chart":ch["id"]})
    for sign in (1,-1):
        objective=affine_quad((0,0,3,1) if sign>0 else (0,0,1,3))
        envelope.add(objective,box3()+[((-1,0,0),-2)],{"kind":"late_tour","sign":sign})
    return envelope


def compose_renewal(chart,child,sign):
    """Return q and inequalities in(t,L,R,h)."""
    t=(Q(0),Q(1),Q(0),Q(0),Q(0))
    L=(Q(0),Q(0),Q(1),Q(0),Q(0))
    R=(Q(0),Q(0),Q(0),Q(1),Q(0))
    h=(Q(0),Q(0),Q(0),Q(0),Q(1))
    changing=R if sign>0 else L
    fixed=L if sign>0 else R
    chart_maps=(t,h,changing)
    u=chart["update"]
    update=tuple(u[0]*int(j==0)+u[1]*t[j]+u[2]*h[j]+u[3]*changing[j] for j in range(5))
    future_time=(Q(0),Q(1),Q(0),Q(0),Q(2))
    future=(future_time,fixed,update) if sign>0 else (future_time,update,fixed)
    objective=chart["objective"].compose(chart_maps)
    objective=objective.add(product_quad(tuple(2*z for z in h),fixed))
    objective=objective.add(product_quad(h,update))
    objective=objective.add(child.objective.compose(future))
    rows=constraints_compose(chart["rows"],chart_maps)+constraints_compose(child.rows,future)
    rows+= [((-1,0,0,0),0),((1,0,0,0),2),((0,0,0,-1),0),((0,0,0,1),1),((1,0,0,1),2)]
    return objective,canonical(rows)


def renewal_envelope(charts,previous,base,depth,exact_min=False):
    from eliminate_quadratic_interval import eliminate_last_variable
    out=Envelope(exact_min)
    for piece in base.active:
        out.add(piece.objective,piece.rows,dict(piece.provenance))
    eliminated=0
    total=2*len(charts)*len(previous.active)
    for k,(sign,chart,child) in enumerate((s,ch,p) for s in (1,-1) for ch in charts for p in previous.active):
        objective,rows=compose_renewal(chart,child,sign)
        if rows is None:continue
        candidates=eliminate_last_variable(rows,objective.c,objective.linear,objective.hessian)
        eliminated+=len(candidates)
        for item in candidates:
            q=item.objective
            out.add(Quad(q.constant,q.linear,q.hessian),list(item.inequalities)+box3(2),
                    {"kind":"return_triangle","sign":sign,"chart":chart["id"],
                     "child_depth":depth-1,"child_uid":child.uid,
                     "h_constant":str(item.h_constant),"h_linear":list(map(str,item.h_linear)),
                     "origins":list(item.origins)})
        if (k+1)%100==0:
            print(json.dumps({"phase":"renewal","depth":depth,"branches":k+1,"total_branches":total,
                              "eliminated_candidates":eliminated,"active":len(out.active),
                              "nonempty":len(out.registry),"empty":out.empty}),flush=True)
    return out


def encode(z):
    if isinstance(z,Q):return str(z)
    if isinstance(z,Quad):return {"c":str(z.c),"linear":list(map(str,z.linear)),"hessian":[list(map(str,row)) for row in z.hessian]}
    if isinstance(z,Piece):return {"uid":z.uid,"objective":encode(z.objective),"inequalities":[[list(a),str(b)] for a,b in z.rows],"vertices":[list(map(str,p)) for p in z.vertices],"provenance":z.provenance}
    raise TypeError(type(z))


def report(envelope,depth,start):
    states=[(Q(t,4),Q(L,8),Q(R,8)) for t in range(9) for L in range(5) for R in range(5)]
    values=[{"state":list(map(str,p)),"value":str(envelope.value(p)[0])} for p in states]
    center=envelope.value((Q(0),Q(1,2),Q(1,2)))
    return {"depth":depth,"active":len(envelope.active),"nonempty_generated":len(envelope.registry),"empty_candidates":envelope.empty,
            "pruning_counts":envelope.counts,"elapsed_seconds":time.monotonic()-start,
            "initial_center":{"value":str(center[0]),"piece":center[1]},"sample_values":values}


def history_digest(registry,proofs):
    encoded=json.dumps({"all_generated_pieces":registry,"domination_replay":proofs},
                       default=encode,sort_keys=True,separators=(",",":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def compact_layer(envelope):
    return {"active_pieces":envelope.active,
            "generated_candidates_and_pruning_sha256":history_digest(envelope.registry,envelope.proofs),
            "nonempty_generated":len(envelope.registry),"empty_candidates":envelope.empty,
            "domination_count":len(envelope.proofs)}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("charts")
    parser.add_argument("output")
    parser.add_argument("--depth",type=int,default=0)
    parser.add_argument("--exact-min-prune",action="store_true")
    parser.add_argument("--verify",action="store_true",help="Regenerate every layer and compare the existing output certificate; do not rewrite it.")
    parser.add_argument("--history-output",help="Optionally save all generated candidates and exact pruning evidence, with gzip when the suffix is .gz.")
    args=parser.parse_args()
    metadata,charts=load_charts(args.charts)
    start=time.monotonic()
    envelope=direct_envelope(charts,args.exact_min_prune)
    envelopes=[envelope];base=envelope
    reports=[report(envelope,0,start)]
    print(json.dumps({k:v for k,v in reports[-1].items() if k!="sample_values"}),flush=True)
    for depth in range(1,args.depth+1):
        envelope=renewal_envelope(charts,envelope,base,depth,args.exact_min_prune)
        envelopes.append(envelope);reports.append(report(envelope,depth,start))
        print(json.dumps({k:v for k,v in reports[-1].items() if k!="sample_values"}),flush=True)
    result={"format":"exact-center-renewal-envelope-v1",
            "scope":"Exact finite-depth formal center-continuation envelope; no global-game lower claim.",
            "source_sha256":hashlib.sha256(read_bytes(args.charts)).hexdigest(),
            "n":metadata["n"],"epsilon":metadata["epsilon"],"depth":args.depth,
            "reports":reports,"envelopes":[compact_layer(e) for e in envelopes]}
    if args.verify:
        expected=json.loads(read_bytes(args.output))
        actual=json.loads(json.dumps(result,default=encode))
        for key in ("format","source_sha256","n","epsilon","depth","envelopes"):
            assert actual[key]==expected[key],("regeneration mismatch",key)
        assert len(actual["reports"])==len(expected["reports"])
        for a,b in zip(actual["reports"],expected["reports"]):
            a.pop("elapsed_seconds",None);b.pop("elapsed_seconds",None)
            assert a==b,"exact layer report mismatch"
        print(json.dumps({"status":"PASS","check":"complete exact regeneration","layers":len(envelopes),
                          "final_pieces":len(envelope.active),"initial_center":str(envelope.value((Q(0),Q(1,2),Q(1,2)))[0])}),flush=True)
    else:
        write_json(args.output,result)
    if args.history_output:
        write_json(args.history_output,{"envelopes":[{"active_uids":[p.uid for p in e.active],
                         "all_generated_pieces":e.registry,"domination_replay":e.proofs} for e in envelopes]})

if __name__=="__main__":
    main()
