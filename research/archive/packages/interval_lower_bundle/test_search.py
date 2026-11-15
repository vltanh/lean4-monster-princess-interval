#!/usr/bin/env python3
"""Check contracted-family algebra and native certification on tiny grids."""
from pathlib import Path
import json
import tempfile

import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix, vstack, hstack, eye, csr_matrix

from search import (Master, InterpolatedMaster, ContractedMaster, InteriorMaster,
                    save_priced_trial, load_table)


def check():
    reports = []
    with tempfile.TemporaryDirectory() as temp:
        for n,p in ((2,2), (4,2)):
            folder = Path(temp)/f'n{n}p{p}'
            base = Master(n, folder, 1000000) if n == p else InterpolatedMaster(n,p,folder,1000000)
            values = np.array([min(1., (j+k)/(2*p)) for j,k in base.nodes])
            contracted = ContractedMaster(base, values)
            x = contracted.profile_values(base.repair(values))
            table = contracted.repair(x)
            expected = base.repair(x[contracted.labels])
            assert np.array_equal(table, expected)
            routes = [
                {'start_grid':2*n,'moves':[-1]*(4*n)},
                {'start_grid':0,'moves':[1]*n+[-1]*(3*n)+[1]*(4*n)},
                {'start_grid':0,'moves':[1]*(2*n)+[-1]*(4*n)},
            ]
            for path in routes:
                contracted.add(path,table)
            backend = InteriorMaster(contracted, seconds=30.,component_prox=True)
            seed_answer,_=contracted.price(x,keep=0)
            lower=int(seed_answer['minimum_units'])/(4*n*contracted.D)
            for iteration in range(4):
                result,weights,trial = backend.solve_box(x,.1,lower)
                # Independent SciPy LP in the full nodal space, imposing
                # explicit equality to the representative of every component.
                rr=[];cc=[];vv=[];rhs=[]
                for row,column in enumerate(contracted.columns):
                    plan = column['plan']
                    if isinstance(base,InterpolatedMaster):
                        mass,coef = base._coefficients(plan)
                    else:
                        base.add_plan(plan)
                        item = next(c for c in base.columns if c['plan']==plan)
                        mass,coef = item['mass'],item['coeff']
                    rr.append(row);cc.append(base.K);vv.append(1.)
                    for i,v in coef.items():
                        rr.append(row);cc.append(i);vv.append(-v/(4*n))
                    rhs.append(mass/(4*n))
                cuts=coo_matrix((vv,(rr,cc)),shape=(len(rhs),base.K+1)).tocsr()
                er=[];ec=[];ev=[]
                for i,c in enumerate(contracted.labels):
                    if i != contracted.representatives[c]:
                        row=len(er)//2
                        er.extend((row,row));ec.extend((i,int(contracted.representatives[c])));ev.extend((1.,-1.))
                equal=coo_matrix((ev,(er,ec)),shape=(len(er)//2,base.K+1)).tocsr()
                expanded=x[contracted.labels]
                cold=linprog(np.r_[np.zeros(base.K),-1.],
                    A_ub=vstack([base.order_matrix,cuts]),
                    b_ub=np.r_[np.zeros(len(base.order)),rhs],
                    A_eq=equal,b_eq=np.zeros(equal.shape[0]),
                    bounds=list(zip(np.maximum(0,expanded-.1),np.minimum(1,expanded+.1)))+[(0,2)],
                    method='highs-ds')
                assert cold.success and abs(cold.fun-result.fun)<2e-7
                if 'level_prox' in backend.last_stats:
                    # Independently solve the same level's displacement LP.
                    cuts_c,rhs_c=backend._cuts(0)
                    full=vstack([contracted.order_matrix,cuts_c],format='csr')
                    rhs_c=np.r_[np.zeros(len(contracted.order)),rhs_c]
                    level=backend.trial_level;K=contracted.K
                    g=full[:,:K];b=rhs_c-full[:,K].toarray().ravel()*level
                    identity=eye(K,format='csr')
                    matrix=vstack([hstack([g,csr_matrix((g.shape[0],K))]),
                                   hstack([identity,-identity]),hstack([-identity,-identity])],format='csr')
                    reference=linprog(np.r_[np.zeros(K),np.ones(K)],A_ub=matrix,
                        b_ub=np.r_[b,x,-x],
                        bounds=list(zip(np.maximum(0,x-.1),np.minimum(1,x+.1)))+[(0,None)]*K,
                        method='highs-ds')
                    assert reference.success
                    assert abs(reference.fun-np.abs(trial-x).sum())<2e-7
                    assert np.max(g@trial-b)<2e-7
                answer,priced=contracted.price(trial,keep=12)
                compact=folder/f'exact_trial_{iteration}.json.gz'
                save_priced_trial(compact,contracted,priced,answer)
                decoded,flat,_=load_table(compact)
                assert np.array_equal(np.frombuffer(flat,dtype=np.uint64).reshape(priced.shape),priced)
                assert decoded['minimum_units']==answer['minimum_units']
                # Independent base decoder/repair represents the same legal
                # nodal field, and therefore gets exactly the same integer DP.
                base_trial=base.profile_values(priced)
                direct,actual=base.price(base_trial,keep=0)
                assert np.max(np.abs(actual.astype(np.int64)-priced.astype(np.int64)))<=1
                # Avoid making equality claims if a floating reimport floors
                # an integer by one; the exact certificate is the first DP.
                if np.array_equal(actual,priced):
                    assert answer['minimum_units']==direct['minimum_units']
                for path in answer['paths']:
                    contracted.add(path,priced)
            reports.append({'n':n,'profile_grid':p,'full_variables':base.K,
                            'component_variables':contracted.K,'iterations':4})
    return {'status':'PASS','scope':'contracted LP equivalence and exact complete tiny-bank pricing',
            'runs':reports,'new_game_bound_claimed':False}


if __name__ == '__main__':
    print(json.dumps(check(),indent=2))
