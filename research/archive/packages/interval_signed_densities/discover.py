#!/usr/bin/env python3
"""Bounded continuous-density shape discovery, not a saddle certificate.

The fixed bins are integrated analytically in the monster start parameter.
Princess responses use the four-parameter limiting family. Three sufficient
monotonicity conditions are imposed; their LP dual is not a princess lower
strategy against individual unrestricted monsters.
"""

import json
import time
from pathlib import Path

import numpy as np
from numba import njit
from scipy.optimize import differential_evolution, linprog, minimize


@njit
def inverse_a(z, a, u, c):
    if z <= a:
        return 0.0
    if z <= u:
        return (z-a)/2
    if c >= u and z <= c:
        return z
    return (z+c)/2


@njit
def inverse_b(z, a, u, c, y):
    if z <= -a:
        return 0.0
    if z <= min(u, c):
        return (z+u)/2
    if c >= u and z <= c:
        return z
    if z <= y:
        return (z+1)/2
    return z+1


@njit
def pure_integrand(kind, x, a, u, c, y):
    if kind == 0:  # positive M1
        first = inverse_b(-x,a,u,c,y) if x < a else (2-x+y)/2
        return (first+3-x)/2
    if kind == 1:  # positive M2
        if x < -c:
            first = 4.0
        elif x < a:
            first = inverse_b(-x,a,u,c,y)
        else:
            first = (1+c)/2
        return (first+2)/2
    if kind == 2:  # negative M2, parameter -x
        first = 4.0 if x > c else inverse_b(x,a,u,c,y)
        second = inverse_a(x,a,u,c) if x > a else 2.0
        return (first+second)/2
    # negative M1, parameter -x
    second = inverse_a(x,a,u,c) if x > a else 3+x
    return (inverse_b(x,a,u,c,y)+second)/2


@njit
def features(parameters, knots):
    a,u,c,y = parameters
    n = len(knots)-1
    result = np.zeros(1+4*n)
    result[0] = (5+c)/4
    breaks = np.sort(np.array([a,u,c,y,-a,-c,-y]))
    for j in range(n):
        lo,hi = knots[j],knots[j+1]
        cuts = [lo]
        for cut in breaks:
            if lo < cut < hi:
                cuts.append(cut)
        cuts.append(hi)
        for low,high in zip(cuts[:-1],cuts[1:]):
            if high <= low:
                continue
            x = (low+high)/2
            for kind in range(4):
                result[1+kind*n+j] += (high-low)*pure_integrand(kind,x,a,u,c,y)/(hi-lo)
    return result


@njit
def feature_matrix(parameters, knots):
    result = np.empty((len(parameters),1+4*(len(knots)-1)))
    for i in range(len(parameters)):
        result[i] = features(parameters[i],knots)
    return result


def parameters_from_unit(r):
    a = r[0]
    u = a+(1-a)*r[1]
    c = -a+(1+a)*r[2]
    y = c+(1-c)*r[3]
    return np.array([a,u,c,y])


def unit_from_parameters(p):
    a,u,c,y = p
    return np.array([a, (u-a)/(1-a) if a < 1 else 0,
                     (c+a)/(1+a), (y-c)/(1-c) if c < 1 else 0])


def main():
    start = time.time()
    knots = np.array([0,1/8,1/4,3/8,1/2,5/8,3/4,7/8,
                      15/16,31/32,63/64,1.0])
    n = len(knots)-1
    signed = sorted(set(knots.tolist()+(-knots).tolist()))
    shapes = []
    for a in knots:
        for u in knots:
            if u < a: continue
            for c in signed:
                if c < -a: continue
                for y in signed:
                    if y >= c: shapes.append([a,u,c,y])
    shapes = np.array(shapes)
    matrix = feature_matrix(shapes,knots)
    widths = np.diff(knots)
    monotone = []
    # f, f+g, h+ell are nondecreasing densities, not bin masses.
    for groups in [(0,),(0,1),(2,3)]:
        for j in range(n-1):
            row = np.zeros(matrix.shape[1]+1)
            for group in groups:
                row[1+group*n+j] = 1/widths[j]
                row[1+group*n+j+1] = -1/widths[j+1]
            monotone.append(row)
    monotone = np.array(monotone)
    selected = sorted(set(np.linspace(0,len(shapes)-1,120,dtype=int)))
    log = []
    extra_shapes = []
    print('FIXED_BINS',len(widths),'SHAPES',len(shapes),flush=True)
    for outer in range(5):
        for iteration in range(60):
            rows = np.c_[matrix[selected],-np.ones(len(selected))]
            constraints = np.vstack((rows,monotone))
            count = matrix.shape[1]
            sol = linprog(np.r_[np.zeros(count),1.], A_ub=constraints,
                          b_ub=np.zeros(len(constraints)),
                          A_eq=[np.r_[np.ones(count),0.]],b_eq=[1.],
                          bounds=[(0,None)]*count+[(None,None)],method='highs',
                          options={'primal_feasibility_tolerance':1e-9,
                                   'dual_feasibility_tolerance':1e-9})
            assert sol.success,sol.message
            weights = sol.x[:-1]
            payoffs = matrix@weights
            violation = payoffs.max()-sol.fun
            if violation < 1e-8: break
            new = np.where(payoffs > sol.fun+max(1e-8,violation/8))[0]
            selected = sorted(set(selected)|set(new[np.argsort(payoffs[new])[-80:]]))
        def objective(r):
            return -float(features(parameters_from_unit(r),knots)@weights)
        de = differential_evolution(objective,[(0,1)]*4,maxiter=100,popsize=12,
                                    seed=61111+outer,polish=True,tol=1e-8)
        candidates = [(float(-de.fun),parameters_from_unit(de.x))]
        for index in np.argsort(payoffs)[-12:]:
            local = minimize(objective,unit_from_parameters(shapes[index]),
                             method='SLSQP',bounds=[(0,1)]*4,
                             options={'maxiter':100,'ftol':1e-11})
            candidates.append((-float(local.fun),parameters_from_unit(local.x)))
        best,shape = max(candidates,key=lambda x:x[0])
        row = dict(round=outer,sampled_objective=float(sol.fun),
                   separated_response=best,parameters=shape.tolist(),
                   rows=len(selected),seconds=time.time()-start)
        log.append(row)
        print('ROUND',row,flush=True)
        extra_shapes.extend(p.tolist() for v,p in candidates if v > sol.fun+1e-8)
        added = np.array([p for v,p in candidates if v > sol.fun+1e-8])
        if not len(added): break
        old_count = len(shapes)
        shapes = np.vstack((shapes,added))
        matrix = np.vstack((matrix,feature_matrix(added,knots)))
        selected += list(range(old_count,len(shapes)))

    density = [weights[1+i*n:1+(i+1)*n]/widths for i in range(4)]
    near = np.where(matrix@weights > sol.fun-1e-6)[0]
    output = dict(scope='Discovery only: fixed continuous density bins and bounded numerical separation; not a lower strategy or exact upper certificate.',
                  knots=knots.tolist(),endpoint_mass=float(weights[0]),
                  densities={name:d.tolist() for name,d in zip(('f','g','h','ell'),density)},
                  sampled_objective=float(sol.fun),separated_response=best,
                  active_shape_samples=shapes[near].tolist(),log=log,
                  stopping_rule='At most five continuous-separation rounds; fixed bins throughout.')
    Path(__file__).with_name('discovery.json').write_text(json.dumps(output))
    print('ENDPOINT',weights[0],flush=True)
    for name,d in zip(('f','g','h','ell'),density):print(name,d.tolist(),flush=True)
    print('ACTIVE_SHAPE_COUNT',len(near),flush=True)


if __name__ == '__main__':
    main()
