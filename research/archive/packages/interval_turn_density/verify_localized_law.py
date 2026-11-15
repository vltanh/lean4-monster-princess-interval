#!/usr/bin/env python3
"""Combined-law checks for the localized inward triangle and tied ramp."""
import json
from pathlib import Path

import numpy as np
from scipy.optimize import linprog

from localized_inward_law import LocalizedLaw
from localized_inward_oracle import freeze_response, frozen_features
from negative_prefix_oracle import optimal_features as old_optimal


def projected_seed(law, old, eta=.2):
    original = np.r_[old, eta]
    n = law.size
    rows = np.vstack((np.c_[law.inequalities, np.zeros((len(law.inequalities),n))],
        np.c_[np.eye(n),-np.eye(n)],np.c_[-np.eye(n),-np.eye(n)]))
    rhs = np.r_[np.zeros(len(law.inequalities)),original,-original]
    eq = np.c_[law.equalities,np.zeros((len(law.equalities),n))]
    erhs = np.zeros(len(eq));erhs[0]=1.
    bounds = list(law.bounds);bounds[-1]=(eta,eta)
    solution = linprog(np.r_[np.zeros(n),np.ones(n)],A_ub=rows,b_ub=rhs,
        A_eq=eq,b_eq=erhs,bounds=bounds+[(0.,None)]*n,method='highs')
    assert solution.success,solution.message
    return solution.x[:n]


def main():
    data=json.loads(Path(__file__).with_name('negative_prefix_discovery.json').read_text())
    law=LocalizedLaw(data['knots'],data['affine_profile'],data['left'],data['right'],
        data['turn'],data['negative_start_bound'])
    old=np.r_[data['endpoint_mass'],*(data['densities'][name] for name in ('f','g','k','ell'))]
    rng=np.random.default_rng(81049)
    errors=[]
    for _ in range(60):
        a=rng.uniform(0.,1.);u=rng.uniform(a,1.);c=rng.uniform(-a,1.);y=rng.uniform(c,1.)
        p=np.array([a,u,c,y]);variables=np.r_[old,0.]
        row,graph=freeze_response(p,law,variables)
        reference=old_optimal(p,law.knots,law.profile,old,law.left,law.right,law.turn)
        errors.append(abs(row@variables-reference@old))
    assert max(errors)<2e-10,max(errors)
    print('ZERO_LOCALIZED_FULL_ORACLE',len(errors),'max error',max(errors),flush=True)
    variables=projected_seed(law,old)
    assert abs(law.equalities[0]@variables-1.)<2e-12
    assert np.min(-law.inequalities@variables)>-2e-11
    print('FEASIBLE_LOCALIZED_LAW',law.summary(variables),flush=True)
    count,maximum=0,0.
    for _ in range(40):
        a=rng.uniform(0.,1.);u=rng.uniform(a,1.);c=rng.uniform(.05,1.);y=rng.uniform(c,1.)
        p=np.array([a,u,c,y]);row,graph=freeze_response(p,law,variables)
        negative=graph[graph[:,0]<0.]
        cuts=np.sort(np.r_[0.,law.knots[(law.knots>0.)&(law.knots<c)],c])
        for _ in range(24):
            levels=np.sort(rng.uniform(u,1.,len(cuts)-1))
            candidate=np.zeros((len(negative)+len(levels),4));candidate[:len(negative)]=negative
            for j,(lo,hi) in enumerate(zip(cuts[:-1],cuts[1:])):
                candidate[len(negative)+j]=np.array([lo,hi,0.,max(hi,levels[j])])
            competing=frozen_features(p,candidate,len(candidate),law.knots,law.profile,
                law.left,law.right,law.turn)
            gain=float((competing-row)@variables);maximum=max(maximum,gain)
            assert gain<2e-9,(p.tolist(),gain)
            count+=1
    print('POSITIVE_PREFIX_COMPETITORS',count,'greatest gain',maximum)
    print('PASS: zero-component equivalence, admissible normalized law, nonzero-ramp positive response')


if __name__=='__main__':main()
