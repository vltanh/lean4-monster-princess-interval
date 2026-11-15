#!/usr/bin/env python3
"""Fixed-bin discovery of an indifference sheet of negative M2 turns.

This is numerical geometry discovery, not an exact game certificate.
The chosen turn-front profile is fixed in each solve. Density bins are
not refined. The upper response formula includes all four scalar
parameters; monotonicity constraints are sufficient, not necessary.
"""

import argparse
import json
from pathlib import Path
import sys
import time

import numpy as np
from numba import njit
from scipy.optimize import differential_evolution, linprog, minimize

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'packages/interval_signed_densities'))
from discover import features, parameters_from_unit, pure_integrand, unit_from_parameters


@njit
def ratio_integral(lo, hi, intercept, slope, pole):
    return -slope*(hi-lo)+(intercept+slope*pole)*np.log((pole-lo)/(pole-hi))


@njit
def sheet_features(parameters, knots, turns, coefficients):
    a,u,c,y = parameters
    n = len(knots)-1
    widths = knots[1:]-knots[:-1]
    result = features(parameters,knots)
    for kind in range(4):
        for j in range(n):
            result[1+kind*n+j] *= widths[j]
    breaks = np.sort(np.array([a,u,c,y,-a,-c,-y]))
    for j in range(n):
        lo,hi = knots[j],knots[j+1]
        cuts = [lo]
        for cut in breaks:
            if lo < cut < hi:
                cuts.append(cut)
        cuts.append(hi)
        for component in range(turns.shape[1]):
            b = turns[j,component]
            if b <= 1:
                continue
            delta = b-1
            integral = 0.0
            for low,high in zip(cuts[:-1],cuts[1:]):
                if high-low < 1e-13:
                    continue
                z = (low+high)/2
                z1,z2 = (2*low+high)/3,(low+2*high)/3
                val1 = pure_integrand(2,z1,a,u,c,y)
                val2 = pure_integrand(2,z2,a,u,c,y)
                slope = delta*(val2-val1)/(z2-z1)
                intercept = delta*val1-slope*z1
                intercept += delta*delta/4*((z<a)+(z>max(0.,y)))
                if max(0.,c) < z < max(0.,y):
                    intercept -= 7*delta/4
                    slope += delta/4
                integral += ratio_integral(low,high,intercept,slope,b+6)
            result += integral*coefficients[j,component]
    return result


@njit
def feature_matrix(shapes,knots,turns,coefficients):
    out = np.empty((len(shapes),1+4*(len(knots)-1)))
    for i in range(len(shapes)):
        out[i] = sheet_features(shapes[i],knots,turns,coefficients)
    return out


def setup(knots,profile):
    n = len(knots)-1
    count = 1+4*n
    turns = np.ones((n,n+1))
    coefficients = np.zeros((n,n+1,count))
    mass = np.r_[1.,np.tile(np.diff(knots),4)]
    constraints = []
    # Nonnegative variables are endpoint mass and f,g,h0,ell bin densities.
    for groups in [(0,),(0,1)]:
        for j in range(n-1):
            row = np.zeros(count)
            for group in groups:
                row[1+group*n+j] = 1
                row[1+group*n+j+1] = -1
            constraints.append(row)
    for j,v in enumerate(profile):
        if v <= 1:
            continue
        index = min(n-1,np.searchsorted(knots,2-v,side='right')-1)
        turns[j,0] = v
        coefficients[j,0,1+index] = 1
        coefficients[j,0,1+3*n+j] = -1
        constraints.append(-coefficients[j,0])
        component = 1
        for i in range(1,n):
            b = 2-knots[i]
            if 1 < b < v-1e-12:
                turns[j,component] = b
                coefficients[j,component,1+i] = 1
                coefficients[j,component,1+i-1] = -1
                component += 1
        for b,coef in zip(turns[j],coefficients[j]):
            if b>1:
                mass += (b-1)*np.log((b+6-knots[j])/(b+6-knots[j+1]))*coef

    def k_row(j,z):
        row = np.zeros(count)
        row[1+2*n+j] = 1
        row[1+3*n+j] = 1
        for b,coef in zip(turns[j],coefficients[j]):
            if b>1:
                row += (b-1)/(b+6-z)*coef
        return row

    def gamma_row(j,z):
        v = profile[j]
        row = np.zeros(count)
        for i in range(n):
            row[1+i] = max(0.,min(knots[i+1],2-v)-knots[i])
        row[1+3*n+j] = -(z+2-v)
        return row

    for j in range(n-1):
        z = knots[j+1]
        constraints.append(k_row(j,z)-k_row(j+1,z))
        constraints.append(gamma_row(j+1,z)-gamma_row(j,z))
    return turns,coefficients,mass,np.array(constraints)


def solve(knots,profile,rounds=3):
    start=time.time()
    turns,coefficients,mass,monotone=setup(knots,profile)
    n=len(knots)-1
    signed=sorted(set(knots.tolist()+(-knots).tolist()))
    shapes=np.array([[a,u,c,y] for a in knots for u in knots if u>=a
                     for c in signed if c>=-a for y in signed if y>=c])
    matrix=feature_matrix(shapes,knots,turns,coefficients)
    selected=sorted(set(np.linspace(0,len(shapes)-1,100,dtype=int)))
    log=[]
    for outer in range(rounds):
        for iteration in range(80):
            constraints=np.vstack((np.c_[matrix[selected],-np.ones(len(selected))],
                                    np.c_[monotone,np.zeros(len(monotone))]))
            count=len(mass)
            sol=linprog(np.r_[np.zeros(count),1.],A_ub=constraints,
                        b_ub=np.zeros(len(constraints)),
                        A_eq=[np.r_[mass,0.]],b_eq=[1.],
                        bounds=[(0,None)]*count+[(None,None)],method='highs',
                        options={'primal_feasibility_tolerance':1e-9,
                                 'dual_feasibility_tolerance':1e-9})
            if not sol.success:
                raise RuntimeError(sol.message)
            weights=sol.x[:-1]
            payoffs=matrix@weights
            violation=payoffs.max()-sol.fun
            if violation<1e-8:
                break
            new=np.where(payoffs>sol.fun+max(1e-8,violation/8))[0]
            selected=sorted(set(selected)|set(new[np.argsort(payoffs[new])[-100:]]))

        def objective(r):
            return -float(sheet_features(parameters_from_unit(r),knots,turns,coefficients)@weights)
        de=differential_evolution(objective,[(0,1)]*4,maxiter=130,popsize=16,
                                  seed=61111+outer,polish=True,tol=1e-9)
        candidates=[(-float(de.fun),parameters_from_unit(de.x))]
        for index in np.argsort(payoffs)[-20:]:
            local=minimize(objective,unit_from_parameters(shapes[index]),
                           method='SLSQP',bounds=[(0,1)]*4,
                           options={'maxiter':130,'ftol':1e-12})
            candidates.append((-float(local.fun),parameters_from_unit(local.x)))
        best,shape=max(candidates,key=lambda x:x[0])
        row=dict(round=outer,objective=float(sol.fun),response=best,
                 parameters=shape.tolist(),rows=len(selected),seconds=time.time()-start,
                 constraint_dual_mass=float(np.abs(sol.ineqlin.marginals[len(selected):]).sum()))
        log.append(row)
        print('ROUND',row,flush=True)
        added=np.array([p for value,p in candidates if value>sol.fun+1e-8])
        if not len(added):
            break
        old_count=len(shapes)
        shapes=np.vstack((shapes,added))
        matrix=np.vstack((matrix,feature_matrix(added,knots,turns,coefficients)))
        selected+=list(range(old_count,len(shapes)))
    names=('f','g','h0','ell')
    near=np.where(matrix@weights>sol.fun-1e-6)[0]
    result=dict(scope='Floating structural discovery only; no exact bound or saddle claim.',
                knots=knots.tolist(),profile=profile.tolist(),endpoint_mass=float(weights[0]),
                densities={name:weights[1+i*n:1+(i+1)*n].tolist() for i,name in enumerate(names)},
                objective=float(sol.fun),response=best,log=log,
                active_shape_samples=shapes[near].tolist(),
                constraint_duals=sol.ineqlin.marginals[len(selected):].tolist(),
                stopping_rule='Fixed bins, fixed turn profile, bounded scalar separation rounds.')
    print('ENDPOINT',weights[0],flush=True)
    for name,density in result['densities'].items():
        print(name,density,flush=True)
    return result


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--delta',type=float,default=1/32)
    parser.add_argument('--lower',type=float,default=1/8)
    parser.add_argument('--upper',type=float,default=7/8)
    parser.add_argument('--rise',type=float,default=0.)
    parser.add_argument('--rounds',type=int,default=4)
    parser.add_argument('--output',default='discovery.json')
    args=parser.parse_args()
    knots=np.array([0,1/8,1/4,3/8,1/2,5/8,3/4,7/8,15/16,31/32,63/64,1.])
    centers=(knots[1:]+knots[:-1])/2
    profile=np.where((centers>=args.lower)&(centers<=args.upper),
                     1+args.delta*np.exp(args.rise*(centers-args.upper)),1.)
    result=solve(knots,profile,args.rounds)
    Path(__file__).with_name(args.output).write_text(json.dumps(result,indent=2)+'\n')


if __name__=='__main__':
    main()
