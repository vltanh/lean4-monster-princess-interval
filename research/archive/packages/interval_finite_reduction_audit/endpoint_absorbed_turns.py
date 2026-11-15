#!/usr/bin/env python3
"""Exact exhaustive response experiment for endpoint-absorbed shell laws.

Targets stay at x_i=delta*i/k until t=1 and then run to the endpoint of
that sign. Split the central mass equally between the two final signs.
A cheap pre-one sweep and the smallest positive mass force every optimal
response (also under any turn cap) to capture all targets before t=1.
Thus the enumeration is exact for the full continuous-time response
problem, not a grid approximation. See FINITE_REDUCTION_GATE.md.
"""
from __future__ import annotations
import argparse
from fractions import Fraction
import json
from pathlib import Path


def enumerate_case(k: int, base: int) -> dict:
    if k < 1 or base < 2:
        raise ValueError('k>=1 and base>=2 are required')
    xs = list(range(-k,k+1))
    weights = [base**(k-abs(i)) for i in xs]
    total = sum(weights)
    delta = Fraction(1,4*total)
    assert 2*delta < Fraction(1,total)
    assert 4*k*delta < 1
    records: dict[int,tuple[int,int,tuple[int,...]]] = {}
    leaves = 0
    def visit(left,right,cur,time,cost,direction,turns,order):
        nonlocal leaves
        if left == 0 and right == 2*k:
            leaves += 1
            prev=records.get(turns)
            if prev is None or cost<prev[0]: records[turns]=(cost,1,order)
            elif cost==prev[0]: records[turns]=(cost,prev[1]+1,prev[2])
            return
        for nxt in (left-1,right+1):
            if not 0 <= nxt <= 2*k: continue
            di=1 if nxt>cur else -1
            ti=time+abs(xs[nxt]-xs[cur])
            visit(min(left,nxt),max(right,nxt),nxt,ti,cost+weights[nxt]*ti,
                  di,turns+int(direction!=0 and direction!=di),order+(xs[nxt],))
    for start in range(2*k+1): visit(start,start,start,0,0,0,0,(xs[start],))
    assert leaves==4**k
    unrestricted=min(r[0] for r in records.values())
    analytic_cost=2*sum(base**(k-i)*i*(i+1) for i in range(1,k+1))
    if base==16*k*k+1: assert unrestricted==analytic_cost
    min_turns=min(t for t,r in records.items() if r[0]==unrestricted)
    by_cap=[]
    for cap in range(min(2*k,k+1)+1):
        cost=min(r[0] for t,r in records.items() if t<=cap)
        by_cap.append(dict(cap=cap,integer_cost=cost,
            mean_time=str(Fraction(cost,k*total)*delta),
            gap_to_unrestricted=str(Fraction(cost-unrestricted,k*total)*delta)))
    return dict(k=k,base=base,initial_sites=2*k+1,physical_paths=2*k+2,
                total_weight=total,spatial_scale=str(delta),canonical_orders=leaves,
                minimum_turns=min_turns,
                unrestricted_mean=str(Fraction(unrestricted,k*total)*delta),
                optimal_orders=sum(r[1] for r in records.values() if r[0]==unrestricted),
                example_order=list(next(r[2] for r in records.values() if r[0]==unrestricted)),
                cap_results=by_cap)


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--max-k',type=int,default=8)
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    rows=[]
    for k in range(1,args.max_k+1):
        row=enumerate_case(k,16*k*k+1)
        assert row['minimum_turns']==k
        assert row['optimal_orders']==2
        assert Fraction(row['cap_results'][k-1]['gap_to_unrestricted'])>0
        rows.append(row)
        print(f"k={k}: {row['canonical_orders']} orders, {k} turns required, "
              f"gap={row['cap_results'][k-1]['gap_to_unrestricted']}",flush=True)
    compact=enumerate_case(4,8)
    assert compact['minimum_turns']==4
    rows.append(compact)
    result=dict(scope='Specified-law exact response obstruction, NOT a game value or an equilibrium exclusion',
                all_path_basis='Stationary-prefix normalization plus strict late-capture separation',
                cases=rows,total_canonical_orders=sum(x['canonical_orders'] for x in rows))
    if args.output: args.output.write_text(json.dumps(result,indent=2)+'\n')
    print('PASS',result['total_canonical_orders'],'complete canonical orders')
if __name__=='__main__': main()
