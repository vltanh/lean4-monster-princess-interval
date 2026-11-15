#!/usr/bin/env python3
"""Compare compressed path hypographs with full clock histories and full LPs."""
from fractions import Fraction as Q
from pathlib import Path
import json
import tempfile

import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix,hstack,vstack,csr_matrix

from search import Master,pack_field,Field,supporting_plane,add_calendar,price_table,CachedPathPricing
from record_lp import RecordLP,path_records
from front_model import project,canonical


def full_model(master,paths,planes,seed,floor,radius,front):
    K=master.K;rr=[];cc=[];vv=[];rhs=[];nextcol=K+1
    def row(terms,b):
        i=len(rhs);rhs.append(float(b))
        for c,v in terms:rr.append(i);cc.append(c);vv.append(float(v))
    for path in paths:
        pos=[path['start_grid']]
        for step in path['moves']:pos.append(pos[-1]+step)
        charged=[]
        for sign,end in ((1,-master.R),(-1,master.R)):
            previous=None
            # Independent dense history: every charged node gets its own
            # variable, including all post-two ticks, with no omissions.
            for j in range(pos.index(end)):
                record=nextcol;nextcol+=1;charged.append(record)
                if previous is not None:row([(record,1),(previous,-1)],0)
                x=sign*pos[j];terms=[(record,1)]
                variable=master.variable(j,abs(x)) if x else None
                if variable is not None:terms.append((variable,-(1 if x>0 else -1)))
                row(terms,1);previous=record
        row([(record,-Q(1,4*master.n)) for record in charged],-floor)
    for plane in planes:
        row([(K,1)]+[(master.index[j,k],-Q(a)) for j,k,a in plane['coefficients']],Q(plane['constant']))
    er=[];ec=[];ev=[];equations=0
    if front:
        for i,point in enumerate(master.nodes):
            target=canonical(master.n,point)
            if target==point:continue
            er.append(equations);ec.append(i);ev.append(1.)
            if target is not None:er.append(equations);ec.append(master.index[target]);ev.append(-1.)
            equations+=1
    order=hstack([master.order_matrix,csr_matrix((len(master.order),nextcol-K-1))])
    cuts=coo_matrix((vv,(rr,cc)),shape=(len(rhs),nextcol))
    equality=coo_matrix((ev,(er,ec)),shape=(equations,nextcol)) if equations else None
    anchor=master.profile_values(seed)
    result=linprog(np.r_[np.zeros(K),-1.,np.zeros(nextcol-K-1)],A_ub=vstack([order,cuts]),
        b_ub=np.r_[np.zeros(len(master.order)),rhs],A_eq=equality,b_eq=np.zeros(equations) if equations else None,
        bounds=list(zip(np.maximum(0,anchor-radius),np.minimum(1,anchor+radius)))+[(0,3)]+[(0,2)]*(nextcol-K-1),method='highs-ds')
    assert result.success,result.message
    return -result.fun


def main():
    rng=np.random.default_rng(2026111409);fixed=0;full=0;omitted=0
    with tempfile.TemporaryDirectory() as temporary:
        for n in (1,2,3):
            master=Master(n,Path(temporary)/str(n),100003)
            for front in (False,True):
                master.columns=[];master.seen=set();master.bank_model='records';master.physical_seen=set()
                seed=master.repair(rng.random(master.K))
                if front:seed=project(n,seed)
                native=price_table(master,seed,12)
                paths=native['paths']+[
                    {'start_grid':master.R,'moves':[-1]*(2*master.R)},
                    {'start_grid':0,'moves':[1,-1]*(2*n)+[1]*master.R+[-1]*(2*master.R)}]
                if n>1:
                    paths.append({'start_grid':2,'moves':[1,-1]*(2*n-1)+[-1,-1]+[1]*master.R+[-1]*(2*master.R)})
                for path in paths:
                    normalized,records=path_records(n,path,front)
                    cached=CachedPathPricing(n,master.D);cached.add(normalized)
                    expected=int(cached.price(seed,keep=1)['cached_minimum_units'])
                    actual=[];rr=[];cc=[];vv=[];rhs=[]
                    for i,r in enumerate(records):
                        cap=master.D+(r['coefficient']*int(seed[r['point']]) if r['point'] is not None else 0)
                        value=cap if r['previous'] is None else min(cap,actual[r['previous']]);actual.append(value)
                        if r['previous'] is not None:
                            row=len(rhs);rhs.append(0.)
                            rr.extend((row,row));cc.extend((i,r['previous']));vv.extend((1.,-1.))
                    assert sum(r['weight']*value for r,value in zip(records,actual))==expected
                    caps=[(0,(master.D+(r['coefficient']*int(seed[r['point']]) if r['point'] is not None else 0))/master.D) for r in records]
                    lp=linprog([-r['weight']/(4*n) for r in records],A_ub=coo_matrix((vv,(rr,cc)),shape=(len(rhs),len(records))),
                        b_ub=rhs,bounds=caps,method='highs-ds')
                    assert lp.success and abs(-lp.fun-float(Q(expected,4*n*master.D)))<1e-9
                    fixed+=1;omitted+=sum(r['weight'] for r in records)-len(records)
                    add_calendar(master,normalized,seed)
                floor=Q(int(native['minimum_units']),4*n*master.D)-Q(1,10000)
                model=RecordLP(master,floor,30.,front=front)
                routes=[((Q(0),Q(1)),(Q(2),Q(-1))),((Q(0),Q(0)),(Q(1),Q(1)),(Q(3),Q(-1)))]
                planes=[supporting_plane(Field(pack_field(master,seed),Q(1,2)),route) for route in routes]
                for plane in planes:model.add_plane(plane)
                screen=min(Q(p['value']) for p in planes)
                for iteration in range(2):
                    candidate,upper,_,_=model.solve(seed,screen,.05)
                    expected=full_model(master,model.paths,planes,seed,floor,.05,front)
                    assert abs(upper-expected)<2e-7,(n,front,upper,expected)
                    if front:assert np.array_equal(project(n,candidate),candidate)
                    cache=CachedPathPricing(n,master.D);cache.add_many(model.paths)
                    # Only a tiny integer-rounding allowance in this test;
                    # production accepts a floor only by its exact oracle.
                    assert Q(int(cache.price(candidate,1)['cached_minimum_units']),4*n*master.D)>=floor-Q(1,master.D)
                    full+=1
                    fresh=price_table(master,candidate,12)
                    for path in fresh['paths']:add_calendar(master,path,candidate)
                    for route in routes:
                        plane=supporting_plane(Field(pack_field(master,candidate),Q(1,2)),route)
                        planes.append(plane);model.add_plane(plane)
    print(json.dumps({'status':'PASS','fixed_field_exact_cached_cost_and_aux_lp_comparisons':fixed,
        'independent_full_tick_full_node_vs_compressed_sparse_lps':full,
        'charged_tick_copies_omitted':omitted,'finite_path_bank_claimed_complete':False},indent=2))


if __name__=='__main__':main()
