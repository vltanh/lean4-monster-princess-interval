#!/usr/bin/env python3
"""Compare front-event optimization with independent full-node equalities."""
from fractions import Fraction as Q
from pathlib import Path
import json
import tempfile

import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix,vstack

from search import Master,pack_field,Field,supporting_plane,add_calendar,price_table
from front_model import install,canonical,coefficients,project


def run():
    FrontEventLP=install();checks=0;projection_checks=0
    rng=np.random.default_rng(1701)
    with tempfile.TemporaryDirectory() as directory:
        for n in (1,2,3):
            master=Master(n,Path(directory)/str(n),10**8)
            original=master.repair(rng.random(master.K))
            seed=project(n,original)
            assert np.array_equal(project(n,seed),seed)
            old=price_table(master,original,8);native=price_table(master,seed,8)
            assert int(native['minimum_units'])>=int(old['minimum_units'])
            projection_checks+=1
            c=Q(int(native['minimum_units']),4*n*master.D);floor=c-Q(1,10000)
            for path in native['paths']:add_calendar(master,path,seed)
            model=FrontEventLP(master,floor,30.)
            routes=[((Q(0),Q(1)),(Q(2),Q(-1))),
                    ((Q(0),Q(1,3)),(Q(1,3),Q(2,3)),(Q(2),Q(-1)),(Q(4),Q(1)))]
            field=Field(pack_field(master,seed),Q(1,2))
            planes=[supporting_plane(field,r) for r in routes]
            for plane in planes:model.add_plane(plane)
            screen=min(Q(p['value']) for p in planes)
            anchor=master.profile_values(seed)
            er=[];ec=[];ev=[];ecount=0
            for i,point in enumerate(master.nodes):
                target=canonical(n,point)
                if target==point:continue
                er.append(ecount);ec.append(i);ev.append(1.)
                if target is not None:
                    er.append(ecount);ec.append(master.index[target]);ev.append(-1.)
                ecount+=1
            equality=coo_matrix((ev,(er,ec)),shape=(ecount,master.K+1))
            for _ in range(2):
                candidate,upper,level,stats=model.solve(seed,screen,.05)
                assert np.array_equal(project(n,candidate),candidate)
                rr=[];cc=[];vv=[];rhs=[]
                for column in master.columns:
                    row=len(rhs);rhs.append(float(Q(column['mass'],4*n)-floor))
                    for i,a in column['coeff'].items():
                        rr.append(row);cc.append(i);vv.append(-a/(4*n))
                for plane in planes:
                    row=len(rhs);rhs.append(float(Q(plane['constant'])))
                    rr.append(row);cc.append(master.K);vv.append(1.)
                    before=Q(plane['constant']);after=before
                    for j,k,a in plane['coefficients']:
                        rr.append(row);cc.append(master.index[j,k]);vv.append(-float(Q(a)))
                        before+=Q(a)*Q(int(candidate[j,k]),master.D)
                    transformed=coefficients(n,{(j,k):Q(a) for j,k,a in plane['coefficients']})
                    after+=sum(a*Q(int(candidate[p]),master.D) for p,a in transformed.items())
                    assert before==after
                cuts=coo_matrix((vv,(rr,cc)),shape=(len(rhs),master.K+1))
                full=linprog(np.r_[np.zeros(master.K),-1.],
                    A_ub=vstack([master.order_matrix,cuts]),b_ub=np.r_[np.zeros(len(master.order)),rhs],
                    A_eq=equality,b_eq=np.zeros(ecount),
                    bounds=list(zip(np.maximum(0,anchor-.05),np.minimum(1,anchor+.05)))+[(0,3)],method='highs-ds')
                assert full.success and abs(-full.fun-upper)<2e-7
                response=price_table(master,candidate,8)
                for path in response['paths']:add_calendar(master,path,candidate)
                newfield=Field(pack_field(master,candidate),Q(1,2))
                for route in routes:
                    p=supporting_plane(newfield,route);planes.append(p);model.add_plane(p)
                checks+=1
    return {'status':'PASS','independent_full_front_equalities_vs_sparse_lps':checks,
            'exact_native_minimum_projection_comparisons':projection_checks,
            'inherited_minimum_claimed_exact':False}


if __name__=='__main__':print(json.dumps(run(),indent=2))
