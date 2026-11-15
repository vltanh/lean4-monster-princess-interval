#!/usr/bin/env python3
"""Targeted exact regressions for global incoming-front completion.

The proof covers arbitrary paths. These Fraction fixtures exercise
initial/center/endpoint co-location, front lingering, ordering, and the
two distinct one-sided CDF traces.
"""
import argparse
from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path

from verify_boundary_layer_kernel import clean,contact,value


def complete(path,C):
    C=Q(C)
    assert C>=1
    hit=None
    for (t,x),(s,y) in zip(path,path[1:]):
        if t+x>=C:
            hit=t
            break
        if s+y>=C:
            hit=t+(s-t)*(C-t-x)/(s+y-t-x)
            break
    assert hit is not None and C-1<=hit<=C
    radius=value(path,hit)
    assert hit+radius==C
    result=[point for point in path if point[0]<hit]+[(hit,radius)]
    endpoint=hit+1-radius
    result += [(endpoint,Q(1)),(Q(8),Q(1))]
    return clean(result),hit


def reflected(path):
    return [(t,-x) for t,x in path]


def ordered(a,b):
    return all(value(a,t)<=value(b,t) for t in sorted({t for t,_ in a+b}))


def profiles():
    rows=[
        [(0,0),(8,0)],
        [(0,1),(8,1)],
        [(0,Q(1,4)),(8,Q(1,4))],
        [(0,Q(1,2)),(8,Q(1,2))],
        [(0,Q(3,4)),(8,Q(3,4))],
        [(0,0),(1,1),(8,1)],
        [(0,1),(1,0),(2,0),(3,1),(8,1)],
        [(0,Q(3,4)),(Q(1,2),Q(1,4)),(Q(5,4),1),(8,1)],
        # Positive mass can linger on U=2 after its first hit.
        [(0,Q(1,4)),(Q(1,2),Q(3,4)),(Q(5,4),Q(3,4)),(2,0),(3,1),(8,1)],
        # A slow front approach distinguishes the inner and double traces.
        [(0,Q(1,2)),(Q(3,2),Q(1,2)),(2,1),(8,1)],
    ]
    return [clean(row) for row in rows]


def monsters():
    raw=[
        [(0,1),(2,-1),(4,1)],
        [(0,0),(1,1),(3,-1)],
        [(0,0),(Q(1,2),0),(Q(3,2),1),(Q(7,2),-1)],
        [(0,Q(3,4)),(Q(3,4),0),(Q(7,4),1),(Q(15,4),-1)],
        [(0,Q(3,4)),(Q(1,2),Q(3,4)),(Q(5,4),0),(Q(9,4),-1),(Q(17,4),1)],
        [(0,1),(1,1),(3,-1),(5,1)],
        [(0,1),(2,1),(4,-1),(6,1)],
        [(0,Q(1,2)),(Q(1,2),1),(2,1),(4,-1),(6,1)],
        [(0,Q(1,4)),(Q(1,2),Q(-1,4)),(Q(7,4),1),(Q(15,4),-1)],
        [(0,Q(3,4)),(Q(1,4),1),(Q(5,4),0),(Q(7,4),Q(1,2)),(Q(13,4),-1),(Q(21,4),1)],
    ]
    for C in (Q(1),Q(3,2),Q(2)):
        for delay in (Q(0),Q(1,4)):
            wait=C+delay-Q(1,2)
            raw.append([(0,Q(1,2)),(wait,Q(1,2)),(C+delay+1,-1),(C+delay+3,1)])
    result=[]
    for row in raw:
        path=clean(row)
        result += [path,reflected(path)]
    return result


def cdf(path,U,W):
    return int(value(path,(U+W)/2)<=(U-W)/2)


def verify():
    ps,ms=profiles(),monsters()
    early=late=ordering=0
    for C in (Q(1),Q(3,2),Q(2)):
        completed=[complete(p,C) for p in ps]
        for i,p in enumerate(ps):
            new,T=completed[i]
            assert value(new,C+1)==1
            for m in ms:
                tau=contact(m,[(Q(0),Q(0))])
                if tau<=C:
                    assert contact(m,new)>=contact(m,p)
                    assert contact(m,reflected(new))>=contact(m,reflected(p))
                    early += 1
                else:
                    x=value(m,C)
                    assert x!=0
                    opposite=reflected(new) if x>0 else new
                    capture=contact(m,opposite)
                    assert capture>=C+1+abs(x)
                    pair=(contact(m,new)+contact(m,reflected(new)))/2
                    assert pair>(C+1)/2
                    late += 1
            for j,q in enumerate(ps):
                if ordered(p,q):
                    assert completed[j][1]<=T
                    assert ordered(new,completed[j][0])
                    ordering += 1

    # Raw boundary data are unsafe for an atom lingering on the front.
    linger=ps[8]
    changed,T=complete(linger,Q(2))
    assert T==Q(5,4) and 2*T-2==Q(1,2)
    assert cdf(linger,Q(2),Q(1))==1
    assert cdf(changed,Q(9,4),Q(1))==0

    # At a slow first hit, the incoming U trace alone misses the atom;
    # the left-continuous W representative restores it.
    slow=ps[9]
    changed,T=complete(slow,Q(2))
    assert T==Q(3,2) and 2*T-2==1
    trace_checks=0
    for denominator in (16,32,64,128):
        e=Q(1,denominator)
        assert cdf(slow,2-e,1)==0
        assert cdf(slow,2-e*e,1-e)==1
        assert cdf(changed,Q(9,4),1)==1
        trace_checks += 1

    # For every pure atom fixture, direct completed-path queries agree
    # with the departure distribution at legal interior points.
    distribution_checks=0
    for C in (Q(1),Q(3,2),Q(2)):
        for old in ps:
            changed,T=complete(old,C)
            B=2*T-C
            for i in range(17):
                U=C+Q(i,8)
                for j in range(17):
                    radius=Q(j,16)
                    if radius>=1:
                        continue
                    W=U-2*radius
                    if U+W<0:
                        continue
                    assert cdf(changed,U,W)==int(B>=W)
                    distribution_checks += 1
    return {
        'status':'PASS',
        'scope':'Exact targeted physical regressions; the universal security and regularity statements are proved in GLOBAL_INCOMING_FRONT_COMPLETION.md.',
        'radial_paths':len(ps),'Monster_paths':len(ms),
        'early_center_signed_pair_checks':early,
        'late_center_endpoint_floor_checks':late,
        'ordered_completion_checks':ordering,
        'atomic_departure_distribution_checks':distribution_checks,
        'double_trace_closure_checks':trace_checks,
        'lingering_front_raw_trace_counterexample':{
            'C':'2','first_hit':'5/4','departure_W':'1/2',
            'old_G_at_front_2_1':'1','new_G_at_9_4_1':'0'},
        'slow_approach_trace_counterexample':{
            'C':'2','first_hit':'3/2','departure_W':'1',
            'incoming_U_trace_at_W_1':'0','correct_left_W_representative':'1'},
        'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--report',type=Path,required=True)
    args=p.parse_args()
    result=verify()
    args.report.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
