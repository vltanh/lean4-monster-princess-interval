#!/usr/bin/env python3
"""Fixed-support structural search with the global separated-sheet oracle.

This is floating discovery, never an exact bound or lower certificate.
Run with the repository's experiment dependency directory on PYTHONPATH.
"""

import argparse
import json
import time
from pathlib import Path

import numpy as np
from scipy.optimize import differential_evolution,linprog,minimize

from separated_oracle import (baseline_prefix,bin_at,features,freeze_response,
    optimal_features,parameters_to_unit,residual_row,unit_to_parameters,
    validate_structure,features_affine,freeze_response_affine,
    optimal_features_affine,residual_row_affine)


def constraints(knots,profile,left,right,s0,cap_level,affine_profile=None,
                negative_start_bound=None,edge_trace=False):
    n=len(knots)-1; N=1+4*n
    widths=np.diff(knots)
    if negative_start_bound is None:negative_start_bound=right
    inequalities=[]; equalities=[]
    def vec():return np.zeros(N)
    for groups in [(0,),(0,1),(2,)]:
        for j in range(n-1):
            r=vec()
            for group in groups:
                r[1+group*n+j]=1
                r[1+group*n+j+1]=-1
            inequalities.append(r)
    for j in range(n-1):
        if not edge_trace and knots[j]>=left-1e-12 and knots[j+2]<=s0+1e-12:
            r=vec();r[1+2*n+j]=1;r[1+2*n+j+1]=-1
            equalities.append(r)
    # No negative-M2 starts in the early turn band, including its gap.
    for j in range(n):
        if knots[j]>=negative_start_bound-1e-12:
            r=vec();r[1+2*n+j]=1;r[1+3*n+j]=-1
            equalities.append(r)
        if affine_profile is None:
            inequalities.append(-residual_row(knots[j+1],j,knots,profile,left,right,s0,edge_trace))
            vmax=profile[j]
        else:
            inequalities.append(-residual_row_affine(knots[j+1],j,knots,affine_profile,left,right,s0,edge_trace))
            vmax=affine_profile[j,0]+affine_profile[j,1]*knots[j+1]
        if vmax>1:
            r=vec();r[1+3*n+j]=1
            r[1+bin_at(2-vmax,knots)]-=1
            inequalities.append(r)

    def gamma(z,j):
        r=vec();v=profile[j] if affine_profile is None else affine_profile[j,0]+affine_profile[j,1]*z
        for k in range(n):
            r[1+k]=max(0,min(knots[k+1],2-v)-knots[k])
        r[1+3*n+j]=-(z+2-v)
        return r
    for j in range(n-1):
        z=knots[j+1]
        inequalities.append(gamma(z,j+1)-gamma(z,j))
    if cap_level is not None:
        r=vec();r[0]=1
        for j in range(n):
            r[1+j]=widths[j];r[1+n+j]=widths[j]
            if knots[j]>=cap_level-1e-12:
                r[1+3*n+j]+=widths[j]
        r[1+3*n+bin_at(cap_level,knots)]-=2
        inequalities.append(r)
    normalization=vec();normalization[0]=1
    for group in [0,1,2]:
        normalization[1+group*n:1+(group+1)*n]=widths
    equalities.insert(0,normalization)
    return np.array(inequalities),np.array(equalities)


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--left',type=float,default=1/8)
    parser.add_argument('--right',type=float,default=7/8)
    parser.add_argument('--turn',type=float,default=15/16)
    parser.add_argument('--late-left',type=float,default=None)
    parser.add_argument('--late-right',type=float,default=None)
    parser.add_argument('--edge-trace',action='store_true',
                        help='Permit monotone nonflat k using the nonzero lower-edge early sheet.')
    parser.add_argument('--offset',type=float,default=1/32)
    parser.add_argument('--slope',type=float,default=None,
                        help='Use genuine v(z)=1+offset+slope*(z-left) on start band.')
    parser.add_argument('--cap',action='store_true')
    parser.add_argument('--cap-level',type=float,default=None)
    parser.add_argument('--rounds',type=int,default=7)
    parser.add_argument('--output',default='separated_discovery.json')
    args=parser.parse_args()
    started=time.time()
    knot_list=[0,1/8,1/4,3/8,1/2,5/8,3/4,7/8,15/16,31/32,63/64,1.]
    if args.cap_level is not None:knot_list.append(args.cap_level)
    knots=np.array(sorted(set(knot_list)))
    n=len(knots)-1;N=1+4*n
    left,right,s0=args.left,args.right,args.turn
    late_left=left if args.late_left is None else args.late_left
    late_right=right if args.late_right is None else args.late_right
    negative_start_bound=max(right,late_right)
    assert 0<=late_left<late_right<=s0
    profile=np.ones(n)
    affine_profile=None if args.slope is None else np.c_[np.ones(n),np.zeros(n)]
    for j in range(n):
        if knots[j]>=late_left-1e-12 and knots[j+1]<=late_right+1e-12:
            profile[j]=1+args.offset
            if affine_profile is not None:
                affine_profile[j]=[1+args.offset-args.slope*late_left,args.slope]
    validate_structure(knots,profile,left,right,s0)
    if affine_profile is not None:
        assert args.slope>=0
        assert 0<=args.offset and 1+args.offset+args.slope*(late_right-late_left)<=2
    cap_level=args.cap_level if args.cap_level is not None else (negative_start_bound if args.cap else None)
    structural,equalities=constraints(knots,profile,left,right,s0,cap_level,affine_profile,
                                      negative_start_bound,args.edge_trace)
    feature_fn=features if affine_profile is None else features_affine
    optimal_fn=optimal_features if affine_profile is None else optimal_features_affine
    freeze_fn=freeze_response if affine_profile is None else freeze_response_affine
    active_profile=profile if affine_profile is None else affine_profile
    signed=sorted(set(knots.tolist()+(-knots).tolist()))
    shapes=[];matrix=[];frozen=[]
    for a in knots:
        for u in sorted(set([a,1.])):
            for c in signed:
                if c < -a:continue
                for y in sorted(set([c,0.,right,negative_start_bound,1.])):
                    if y<c:continue
                    p=np.array([a,u,c,y])
                    seg,count=baseline_prefix(p,knots)
                    shapes.append(p)
                    matrix.append(feature_fn(p,seg,count,knots,active_profile,left,right,s0,args.edge_trace))
                    frozen.append(seg[:count].tolist())
    shapes=np.array(shapes);matrix=np.array(matrix)
    selected=sorted(set(np.linspace(0,len(shapes)-1,120,dtype=int)))
    logs=[]
    print('SEPARATED',dict(left=left,right=right,turn=s0,offset=args.offset,
                           late_left=late_left,late_right=late_right,
                           edge_trace=args.edge_trace,
                           slope=args.slope,cap_level=cap_level,initial_rows=len(shapes)),flush=True)
    for outer in range(args.rounds):
        for iteration in range(70):
            response_rows=np.c_[matrix[selected],-np.ones(len(selected))]
            rows=np.vstack((response_rows,np.c_[structural,np.zeros(len(structural))]))
            eq=np.c_[equalities,np.zeros(len(equalities))]
            rhs=np.zeros(len(eq));rhs[0]=1
            sol=linprog(np.r_[np.zeros(N),1.],A_ub=rows,b_ub=np.zeros(len(rows)),
                        A_eq=eq,b_eq=rhs,bounds=[(0,None)]*N+[(None,None)],
                        method='highs',options={'primal_feasibility_tolerance':1e-9,
                                               'dual_feasibility_tolerance':1e-9})
            if not sol.success:
                print('LP_FAILURE',sol.message,flush=True);return
            solved_selected=np.asarray(selected,dtype=int).copy()
            weights=sol.x[:-1]
            scores=matrix@weights
            gap=float(scores.max()-sol.fun)
            if gap<1e-8:break
            candidates=np.where(scores>sol.fun+max(1e-8,gap/10))[0]
            selected=sorted(set(selected)|set(candidates[np.argsort(scores[candidates])[-100:]]))
        def objective(r):
            p=unit_to_parameters(r)
            return -float(optimal_fn(p,knots,active_profile,weights,left,right,s0,args.edge_trace)@weights)
        de=differential_evolution(objective,[(0,1)]*4,maxiter=100,popsize=12,
                                  seed=81224+outer,tol=2e-8,polish=True)
        candidate_results=[(-float(de.fun),unit_to_parameters(de.x))]
        # Check all currently active scalar parameters with their newly
        # optimized prefixes; these may differ from the frozen LP paths.
        top=np.argsort(scores)[-36:]
        for index in top:
            start=parameters_to_unit(shapes[index])
            local=minimize(objective,start,method='SLSQP',bounds=[(0,1)]*4,
                           options={'maxiter':110,'ftol':2e-11})
            candidate_results.append((-float(local.fun),unit_to_parameters(local.x)))
        best,p=max(candidate_results,key=lambda item:item[0])
        structural_dual=float(abs(sol.ineqlin.marginals[len(solved_selected):]).sum())
        final_structural_duals=sol.ineqlin.marginals[len(solved_selected):].tolist()
        final_equality_duals=sol.eqlin.marginals[1:].tolist()
        log=dict(round=outer,objective=float(sol.fun),response=best,
                 parameters=p.tolist(),rows=len(selected),
                 structural_dual_mass=structural_dual,seconds=time.time()-started)
        log['structural_equality_dual_mass']=float(abs(sol.eqlin.marginals[1:]).sum())
        logs.append(log);print('ROUND',log,flush=True)
        added=[]
        for value,p in candidate_results:
            if value>sol.fun+2e-8:
                row,seg=freeze_fn(p,knots,active_profile,weights,left,right,s0,args.edge_trace)
                added.append((p,row,seg.tolist()))
        if not added:break
        old_count=len(shapes)
        shapes=np.vstack((shapes,np.array([p for p,row,seg in added])))
        matrix=np.vstack((matrix,np.array([row for p,row,seg in added])))
        frozen.extend([seg for p,row,seg in added])
        selected.extend(range(old_count,len(shapes)))
    scores=matrix@weights
    active=np.where(scores>sol.fun-2e-6)[0]
    output=dict(scope='Floating structural discovery with analytic separated-sheet response reduction; not an exact bound or lower strategy.',
                knots=knots.tolist(),profile=profile.tolist(),left=left,right=right,
                late_left=late_left,late_right=late_right,
                negative_start_bound=negative_start_bound,
                edge_trace=args.edge_trace,
                affine_profile=None if affine_profile is None else affine_profile.tolist(),
                turn=s0,cap_level=cap_level,endpoint_mass=float(weights[0]),
                densities={name:weights[1+j*n:1+(j+1)*n].tolist()
                           for j,name in enumerate(['f','g','k','ell'])},
                objective=float(sol.fun),response=best,log=logs,
                active_shape_samples=shapes[active].tolist(),
                active_prefix_samples=[frozen[j] for j in active],
                response_dual_support=[dict(parameters=shapes[j].tolist(),
                    prefix=frozen[j],weight=float(-dual))
                    for j,dual in zip(solved_selected,
                                      sol.ineqlin.marginals[:len(solved_selected)])
                    if dual < -1e-10],
                response_dual_mass=float(-sol.ineqlin.marginals[:len(solved_selected)].sum()),
                normalization_dual=float(sol.eqlin.marginals[0]),
                structural_duals=final_structural_duals,
                structural_equality_duals=final_equality_duals,
                stopping_rule=f'Fixed bins/profile, at most {args.rounds} scalar separation rounds.')
    dest=Path(__file__).with_name(args.output)
    dest.write_text(json.dumps(output,indent=2))
    print('ENDPOINT',weights[0],flush=True)
    for j,name in enumerate(['f','g','k','ell']):
        print(name,weights[1+j*n:1+(j+1)*n].tolist(),flush=True)
    print('OUTPUT',str(dest),flush=True)


if __name__=='__main__':main()
