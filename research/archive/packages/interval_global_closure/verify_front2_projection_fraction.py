#!/usr/bin/env python3
"""Independent standard-library replay of the frozen incoming-front projection.

No JavaScript modules, pricing caches, or floating arithmetic are imported.
The large certificate is checked by decoding its exact integer field, not by
rerunning a large optimization. Small-grid physical paths are exhausted.
"""
from __future__ import annotations

import argparse
import base64
from collections import Counter
from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path
import struct
import zlib


SOURCE_FIELD_SHA = "81483589b60c14d823d2bb467015a321d77cf555076fe8d69a36d63cd829d7d5"
SOURCE_STRATEGY_SHA = "d1432172efe4aca9c67394ae7c12fd5b553302e5c9e067d930cc343cb0db4086"
FORMAT = "qout-clock-grid-field-u32-zlib-v1"


def sha(data):
    return hashlib.sha256(data).hexdigest()


def read(path):
    data = Path(path).read_bytes()
    return json.loads(data), sha(data)


class Profile:
    def __init__(self, n, denominator, values):
        self.n, self.D = n, denominator
        self.R, self.C, self.N = 2*n, 4*n, 16*n
        self.values = tuple(values)
        assert len(self.values) == (self.C+1)*n
        assert all(type(v) is int and 0 <= v <= denominator for v in self.values)

    @classmethod
    def decode(cls, data):
        assert data["format"] == FORMAT and data["normalized_profile"] is True
        n, D = data["n"], int(data["field_denominator"])
        assert type(n) is int and n > 0 and 0 < D <= 2**32-1
        enc = data["encoding"]
        count = (4*n+1)*n
        assert enc["count"] == count
        assert enc["integer_type"] == "uint32 little-endian"
        assert enc["compression"] == "zlib"
        compressed = base64.b64decode(data["pre_two_values_base64"], validate=True)
        assert base64.b64encode(compressed).decode() == data["pre_two_values_base64"]
        raw = zlib.decompress(compressed)
        assert len(raw) == 4*count and sha(raw) == enc["uncompressed_sha256"]
        return cls(n, D, struct.unpack("<"+str(count)+"I", raw)), raw

    def node(self, j, k):
        assert type(j) is int and type(k) is int
        assert 0 <= j <= self.N and 0 <= k <= self.R and (j+k)%2 == 0
        if k == 0:
            return 0
        if j > self.C:
            k -= j-self.C
            j = self.C
        if k <= 0:
            return 0
        return self.values[j*self.n+(k-1)//2]

    def projected_node(self, j, k):
        """Original nodal g evaluated at U capped at2, with the center zero extension."""
        if j+k <= self.C:
            return self.node(j, k)
        if j-k >= self.C:
            return 0
        return self.node((self.C+j-k)//2, (self.C-j+k)//2)

    def project(self):
        return Profile(self.n, self.D, [self.projected_node(j,k)
            for j in range(self.C+1) for k in range(1,self.R+1) if (j+k)%2 == 0])

    def validate_all_nodes(self):
        counts = Counter()
        for j in range(self.N+1):
            for k in range(j%2, self.R+1, 2):
                a = self.node(j,k)
                assert 0 <= a <= self.D
                counts["range"] += 1
                if k < self.R:
                    for jj in (j-1,j+1):
                        if 0 <= jj <= self.N:
                            assert a <= self.node(jj,k+1), (j,k,jj)
                            counts["transport"] += 1
        for j in range(0,self.N-1,2):
            assert self.node(j+2,self.R) <= self.node(j,self.R)
            counts["sticky_endpoint"] += 1
        return dict(counts)


def interpolation(p, epsilon, U, W):
    """Exact expected radial node value under the one-threshold map."""
    assert U >= W and 0 <= U-W <= 2 and U+W >= 0
    low, high = Q(1,2)-epsilon, Q(1,2)+epsilon
    descriptors, cuts = [], {low,high}
    for coord in (U,W):
        scaled = coord*p.n
        cell = scaled.numerator//scaled.denominator
        alpha = scaled-cell
        positive = cell%(2*p.n) < p.n
        threshold = alpha if positive else 1-alpha
        descriptors.append((cell,alpha,positive))
        if alpha and low < threshold < high:
            cuts.add(threshold)
    total = Q(0)
    cuts = sorted(cuts)
    for a,b in zip(cuts,cuts[1:]):
        z = (a+b)/2
        indices=[]
        for cell,alpha,positive in descriptors:
            up = bool(alpha and (z<alpha if positive else z>1-alpha))
            indices.append(cell+up)
        u,w=indices
        assert u>=w
        total += (b-a)*p.node(u+w,u-w)
    return total/((high-low)*p.D)


def normalized_paths(n):
    """Every unit-grid prefix until its first endpoint or time2, then a tour.

    Starts are every initial grid point. Only prefixes centered by2 are
    admitted, including an exact time2 center visit. No record dominance or
    pricing/pruning is used in this exhaustive generator.
    """
    R,C=2*n,4*n
    def walk(start, target):
        direction=1 if target>start else -1
        return list(range(start+direction,target+direction,direction))
    def finish(vertices):
        x=vertices[-1]
        if abs(x)==R:
            yield tuple(vertices+walk(x,-x))
        else:
            for end in (-R,R):
                yield tuple(vertices+walk(x,end)+walk(end,-end))
    def recurse(vertices, centered):
        x,j=vertices[-1],len(vertices)-1
        if abs(x)==R:
            # The fastest opposite sweep reaches center by2 whenever this
            # earlier prefix can do so; test this condition literally.
            if centered or j+R <= C:
                yield from finish(vertices)
            return
        if j==C:
            if centered:
                yield from finish(vertices)
            return
        for d in (-1,1):
            y=x+d
            if -R<=y<=R:
                yield from recurse(vertices+[y],centered or y==0)
    for start in range(-R,R+1,2):
        yield from recurse([start],start==0)


def record_trace(profile, path):
    records=[2*profile.D,2*profile.D]
    alive=[True,True]
    result=[]
    for j,x in enumerate(path):
        if x==-profile.R:
            alive[0]=False
        if x==profile.R:
            alive[1]=False
        g=profile.node(j,abs(x))
        signed=g if x>=0 else -g
        for i,price in enumerate((profile.D+signed,profile.D-signed)):
            records[i]=min(records[i],price) if alive[i] else 0
        result.append(tuple(records))
    assert not any(alive)
    # A left-node calendar costs one current record per alive scoring tick.
    return result, sum(sum(r) for r in result[:-1])


def exhaustive_record_checks():
    report=[]
    for n in (1,2):
        for wait,endpoint_half in ((1,False),(2,False),(2,True)):
            D=(4 if endpoint_half else 2)*n
            values=[max(0,k-max(0,j-2*n*wait))
                for j in range(4*n+1) for k in range(1,2*n+1) if (j+k)%2==0]
            p=Profile(n,D,values); q=p.project()
            p.validate_all_nodes(); q.validate_all_nodes()
            counts=Counter(); old_min=new_min=None
            for path in normalized_paths(n):
                old,co=record_trace(p,path); new,cn=record_trace(q,path)
                centered=False
                for j,(x,ro,rn) in enumerate(zip(path,old,new)):
                    centered |= x==0
                    assert rn[0]>=ro[0] and rn[1]>=ro[1]
                    counts["record_states"]+=1
                    if p.node(j,abs(x))!=q.node(j,abs(x)):
                        assert centered and j+abs(x)>4*n
                        counts["changed_postcenter_nodes"]+=1
                    if rn!=ro:
                        counts["strict_record_states"]+=1
                assert cn>=co
                counts["paths"]+=1
                counts["strictly_improved_prices"]+=cn>co
                old_min=co if old_min is None else min(old_min,co)
                new_min=cn if new_min is None else min(new_min,cn)
            report.append({"n":n,"stationary_until":wait,"endpoint_atom":endpoint_half,
                "checks":dict(counts),"old_minimum":str(Q(old_min,4*n*D)),
                "projected_minimum":str(Q(new_min,4*n*D))})
    assert sum(r["checks"].get("strict_record_states",0) for r in report)>0
    return report


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--checkout",type=Path,required=True)
    ap.add_argument("--report",type=Path)
    args=ap.parse_args()
    bank=args.checkout/"packages/interval_clock_grid"
    front=args.checkout/"packages/interval_global_closure"
    old,old_hash=read(bank/"lower_n256_field.json")
    old_s,old_s_hash=read(bank/"lower_n256_princess.json")
    new,new_hash=read(front/"lower_n256_front2_field.json")
    new_s,new_s_hash=read(front/"lower_n256_front2_princess.json")
    assert old_hash==SOURCE_FIELD_SHA and old_s_hash==SOURCE_STRATEGY_SHA
    p,praw=Profile.decode(old); q,qraw=Profile.decode(new)
    sp,spraw=Profile.decode(old_s["nodal_profile"])
    sq,sqraw=Profile.decode(new_s["nodal_profile"])
    assert p.n==q.n==sp.n==sq.n==256
    assert p.D==q.D==sp.D==sq.D==800000000
    assert praw==spraw and qraw==sqraw
    assert q.values==p.project().values
    assert old_s["source_input_sha256"]==old_hash
    assert new_s["source_input_sha256"]==new_hash
    assert new["proof_source"]["field_sha256"]==old_hash
    assert new["proof_source"]["strategy_sha256"]==old_s_hash
    assert new["incoming_front"]=="2"
    for s in (old_s,new_s):
        assert s["format"]=="normalized-qout-princess-p1-v1"
        assert s["n"]==p.n and int(s["cdf_denominator"])==p.D
        assert s["outward_time"]==2 and s["absorption_time"]==3
        units=int(s["verified_lower_units"])
        denom=int(s["objective_denominator"])
        assert denom==4*p.n*p.D
        c=Q(units,denom); eps=Q(s["interpolation_epsilon"])
        assert 0<eps<=Q(1,2)
        loss=(1+eps)/(2*p.n)
        assert Q(s["finite_dual_lower"])==c
        assert Q(s["exact_transfer_loss"])==loss
        assert Q(s["guaranteed_security"])==c-loss
    for key in ("verified_lower_units","objective_denominator","finite_dual_lower",
                "interpolation_epsilon","exact_transfer_loss","guaranteed_security",
                "cell_orientation","quantile_rule"):
        assert old_s[key]==new_s[key]
    units=int(new["certified_bank_lower_units"])
    denominator=4*p.n*p.D
    assert units==int(old["minimum_units"])==int(old_s["verified_lower_units"])
    assert int(new["objective_denominator"])==denominator
    assert Q(new["normalized_bank_lower"])==Q(units,denominator)
    assert Q(new["global_value_lower"])==Q(old["global_lower"])==Q(units,denominator)-Q(1,2*p.n)
    counts=Counter()
    maximum=total=0
    for j in range(p.N+1):
        for k in range(j%2,p.R+1,2):
            before,after=p.node(j,k),q.node(j,k)
            assert after==p.projected_node(j,k)<=before
            counts["all_horizon_projection_identities"]+=1
            if j+k<=p.C:
                assert before==after
                counts["unchanged_incoming_nodes"]+=1
            if j<=p.C and k:
                counts["stored_nodes"]+=1
                counts["stored_beyond_front"]+=j+k>p.C
                counts["stored_changed_nodes"]+=after!=before
                maximum=max(maximum,before-after)
                total+=before-after
    assert counts["stored_changed_nodes"]==892
    for k in range(0,p.R+1,2):
        assert p.node(0,k)==q.node(0,k)
        counts["initial_distribution"]+=1
    # Check the exact interpolation identity at rational center, front,
    # boundary, narrow-threshold and ordinary interior queries.
    for eps in (Q(1,2),Q(1,512)):
        for W in (Q(0),Q(1,7),Q(1,2),Q(1),Q(3,2),Q(511,256),Q(2),Q(15,7)):
            for gap in (Q(0),Q(1,513),Q(1,3),Q(1),Q(3,2),Q(2)):
                U=W+gap
                if U<2:
                    expected=interpolation(p,eps,U,W)
                elif W>=2:
                    expected=Q(0)
                else:
                    expected=interpolation(p,eps,Q(2),W)
                assert interpolation(q,eps,U,W)==expected
                counts["rational_interpolation_identities"]+=1
    report={"status":"PASS","scope":"Independent exact nodal/hash/guarantee replay and exhaustive small normalized-bank record checks; no new n256 optimization or exact-minimum claim.",
        "source_field_sha256":old_hash,"source_strategy_sha256":old_s_hash,
        "projected_field_sha256":new_hash,"projected_strategy_sha256":new_s_hash,
        "source_raw_sha256":sha(praw),"projected_raw_sha256":sha(qraw),
        "large_projection_checks":dict(counts),"maximum_nodal_decrease_units":maximum,
        "total_nodal_decrease_units":str(total),
        "source_legality":p.validate_all_nodes(),"projected_legality":q.validate_all_nodes(),
        "global_value_lower":new["global_value_lower"],
        "explicit_princess_security":new_s["guaranteed_security"],
        "small_exhaustive_fixtures":exhaustive_record_checks()}
    text=json.dumps(report,indent=2)+"\n"
    if args.report:
        args.report.write_text(text)
    print(text,end="")


if __name__=="__main__":
    main()
