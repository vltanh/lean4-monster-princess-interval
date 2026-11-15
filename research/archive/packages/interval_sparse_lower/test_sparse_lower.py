#!/usr/bin/env python3
"""Independent order reachability, closest-extension, and sparse LP tests."""
from pathlib import Path
import json
import sys
import tempfile

import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix,vstack

from clamp import clamp_extend,validate_pre_two
from backend import ClampedSparseMaster,projected_order

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'packages/interval_clock_grid/normalized_native'))
from solve_normalized import Master


def closure(count,edges):
    reach=np.eye(count,dtype=bool)
    for a,b in edges:reach[a,b]=True
    for k in range(count):reach|=reach[:,k,None]&reach[k,None,:]
    return reach


def run():
    rng=np.random.default_rng(94173)
    order_checks=clamp_checks=lp_checks=0
    with tempfile.TemporaryDirectory() as temp:
        for n in (1,2,3):
            master=Master(n,Path(temp)/str(n),1000000)
            reach=closure(master.K,master.order)
            for attempt in range(80):
                selected=np.sort(rng.choice(master.K,min(master.K,2+attempt%10),replace=False))
                nodes=[master.nodes[i] for i in selected]
                restricted=closure(len(nodes),projected_order(n,nodes))
                assert np.array_equal(restricted,reach[np.ix_(selected,selected)])
                order_checks+=1
                seed=master.repair(rng.random(master.K))
                anchors=master.repair(rng.random(master.K))
                values=np.array([int(anchors[j,k])/master.D for j,k in nodes])
                table,stats=clamp_extend(n,master.D,nodes,values,seed)
                validate_pre_two(table[:4*n+1],n,master.D)
                # Independent all-node interval envelopes using the full
                # transitive relation, not either optimized sweep.
                actual=np.array([int(table[j,k]) for j,k in master.nodes])
                chosen=np.array([actual[i] for i in selected])
                old=np.array([int(seed[j,k]) for j,k in master.nodes])
                for i in range(master.K):
                    low=max([0]+[int(v) for a,v in zip(selected,chosen) if reach[a,i]])
                    high=min([master.D]+[int(v) for a,v in zip(selected,chosen) if reach[i,a]])
                    assert actual[i]==max(low,min(int(old[i]),high))
                clamp_checks+=1
            table=master.repair(np.array([min(1,(j+k)/(2*n)) for j,k in master.nodes]))
            paths=[{'start_grid':2*n,'moves':[-1]*(4*n)},
                   {'start_grid':0,'moves':[1]*n+[-1]*(3*n)+[1]*(4*n)}]
            for path in paths:master.add(path,table)
            backend=ClampedSparseMaster(master,30.,component_prox=True)
            anchor=master.profile_values(table)
            best,_=master.price(anchor,keep=0)
            lower=int(best['minimum_units'])/(4*n*master.D)
            for iteration in range(4):
                result,weights,trial=backend.solve_box(anchor,.1,lower)
                # Independent full-grid trust-box LP, without projected order.
                rr=[];cc=[];vv=[];rhs=[]
                for row,column in enumerate(master.columns):
                    rr.append(row);cc.append(master.K);vv.append(1.)
                    for i,v in column['coeff'].items():
                        rr.append(row);cc.append(i);vv.append(-v/(4*n))
                    rhs.append(column['mass']/(4*n))
                cuts=coo_matrix((vv,(rr,cc)),shape=(len(rhs),master.K+1)).tocsr()
                cold=linprog(np.r_[np.zeros(master.K),-1.],
                    A_ub=vstack([master.order_matrix,cuts]),
                    b_ub=np.r_[np.zeros(len(master.order)),rhs],
                    bounds=list(zip(np.maximum(0,anchor-.1),np.minimum(1,anchor+.1)))+[(0,2)],method='highs-ds')
                assert cold.success and abs(cold.fun-result.fun)<2e-7
                complete,priced=master.price(trial,keep=12)
                # Clamping at selected trust bounds controls the whole field.
                new=master.profile_values(priced)
                assert np.max(np.abs(new-anchor))<=.1+4/master.D
                for path in complete['paths']:master.add(path,priced)
                lp_checks+=1
    return {'status':'PASS','exact_reachability_comparisons':order_checks,
            'independent_integer_clamp_checks':clamp_checks,'dynamic_sparse_full_lp_comparisons':lp_checks,
            'new_game_value_claimed':False}


if __name__=='__main__':print(json.dumps(run(),indent=2))
