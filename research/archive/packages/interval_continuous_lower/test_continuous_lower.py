#!/usr/bin/env python3
"""Test distinct objective/floor semantics and exact cross-field attack planes."""
from fractions import Fraction as Q
from pathlib import Path
import json
import tempfile

import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix,vstack

from search import Master,pack_field,Field,supporting_plane,add_calendar,price_table
from event_lp import EventLP


def run():
    lp_checks=plane_checks=0
    with tempfile.TemporaryDirectory() as folder:
        for n in (1,2):
            master=Master(n,Path(folder)/str(n),10**8)
            seed=master.repair(np.array([min(1,(j+k)/(2*n)) for j,k in master.nodes]))
            native=price_table(master,seed,16)
            c=Q(int(native['minimum_units']),4*n*master.D);floor=c-Q(1,10000)
            for path in native['paths']:add_calendar(master,path,seed)
            model=EventLP(master,floor,30.)
            routes=[((Q(0),Q(1)),(Q(2),Q(-1))),
                    ((Q(0),Q(0)),(Q(1),Q(1)),(Q(3),Q(-1))),
                    ((Q(0),Q(1,3)),(Q(1,3),Q(2,3)),(Q(2),Q(-1)),(Q(4),Q(1)))]
            field=Field(pack_field(master,seed),Q(1,2))
            planes=[supporting_plane(field,r) for r in routes]
            for p in planes:model.add_plane(p)
            screen=min(Q(p['value']) for p in planes)
            anchor=master.profile_values(seed)
            for iteration in range(3):
                candidate,upper,level,stats=model.solve(seed,screen,.05)
                # Independent FULL-node LP. Bank rows constrain a fixed floor;
                # only continuous planes contain the objective z.
                rr=[];cc=[];vv=[];rhs=[]
                for column in master.columns:
                    row=len(rhs);rhs.append(float(Q(column['mass'],4*n)-floor))
                    for i,a in column['coeff'].items():
                        rr.append(row);cc.append(i);vv.append(-a/(4*n))
                for plane in model.attacks:
                    row=len(rhs);rhs.append(float(plane['constant']))
                    rr.append(row);cc.append(master.K);vv.append(1.)
                    for point,a in plane['coeff'].items():
                        rr.append(row);cc.append(master.index[point]);vv.append(-float(a))
                cuts=coo_matrix((vv,(rr,cc)),shape=(len(rhs),master.K+1)).tocsr()
                full=linprog(np.r_[np.zeros(master.K),-1.],A_ub=vstack([master.order_matrix,cuts]),
                    b_ub=np.r_[np.zeros(len(master.order)),rhs],
                    bounds=list(zip(np.maximum(0,anchor-.05),np.minimum(1,anchor+.05)))+[(0,3)],method='highs-ds')
                assert full.success and abs(-full.fun-upper)<2e-7
                lp_checks+=1
                newfield=Field(pack_field(master,candidate),Q(1,2))
                for route,old in zip(routes,planes):
                    exact=supporting_plane(newfield,route)
                    support=Q(old['constant'])+sum(Q(a)*Q(int(candidate[j,k]),master.D) for j,k,a in old['coefficients'])
                    assert Q(exact['value'])<=support
                    model.add_plane(exact);plane_checks+=1
                response=price_table(master,candidate,16)
                for p in response['paths']:add_calendar(master,p,candidate)
    return {'status':'PASS','independent_full_vs_sparse_two_objective_lps':lp_checks,
            'exact_cross_field_support_plane_inequalities':plane_checks,
            'native_complete_responses_executed':8,'continuous_screen_claimed_as_lower':False}


if __name__=='__main__':print(json.dumps(run(),indent=2))
