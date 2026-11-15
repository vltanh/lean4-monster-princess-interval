#!/usr/bin/env python3
"""Sparse global concave-cut master for a complete legal CDF field.

All configured routes are rescored after every LP solve. Only the most
violated global supporting cuts are added in a batch; no route is removed
from separation. New continuum_dp_attacks.json routes can be added while
the solve runs. Floating optimization is discovery, not a game certificate.
"""
from __future__ import annotations
import argparse
from collections import defaultdict
from fractions import Fraction
import gzip
import json
from pathlib import Path
import sys
import time
import subprocess
import tempfile
from types import SimpleNamespace
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix,vstack,hstack,csr_matrix

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
sys.path.insert(0,str(ROOT/'packages/interval_cdf_discovery'))
from joint_cdf_field import (RouteFunctional,TemplateFunctional,InitialInwardFunctional,TwoInteriorFunctional,
                             route_pool,two_interior_pool,m1,m2)
from continuum_synthesis import prepare_routes
from continuum_field import ExtendedFieldMesh
from continuum_inward_scan import InwardScanner
from continuum_hotstart import FieldMaster


def sparse(rows,n):
    ii=[];jj=[];vv=[]
    for i,row in enumerate(rows):
        for j,v in row.items():
            if abs(v)>1e-14:ii.append(i);jj.append(j);vv.append(v)
    return coo_matrix((vv,(ii,jj)),shape=(len(rows),n)).tocsr()


def full_native_m2_pool(mesh):
    """Every signed native start and legal signed first-U turn.

    Negative-half first turns use the generic record integral. Endpoint
    and zero-duration limits are the corresponding complete M1 sweeps.
    This is the entire declared native grid, not every continuous M2.
    """
    starts=np.unique(np.r_[mesh.base,-mesh.base])
    turns=np.unique(np.r_[mesh.ugrid,-mesh.ugrid])
    result=[]
    for x in starts:
        for s in turns:
            if s<x-1e-12 or s>2-x+1e-12:continue
            label=dict(kind='M2_full_native',start=float(x),turn=float(s))
            if abs(s-x)<1e-12:
                result.append(RouteFunctional(mesh,[(0.,float(x)),(1+float(x),-1.),(3+float(x),1.)],label))
            elif abs(s-(2-x))<1e-12:
                result.append(TemplateFunctional(mesh,m1(float(x)),dict(kind='M1',start=float(x))))
            elif s+x>=-1e-12:
                result.append(TemplateFunctional(mesh,m2(float(x),float(s)),label))
            else:
                result.append(RouteFunctional(mesh,m2(float(x),float(s)),label))
    return result


def solve(args):
    started=time.monotonic()
    restored=None
    if args.resume_checkpoint:
        with gzip.open(args.resume_checkpoint,'rt')as file:restored=json.load(file)
        assert args.vmax==restored['vmax'],('checkpoint domain',args.vmax,restored['vmax'])
        data=dict(base=restored['base'],domain_max_v=restored['vmax'])
    else:data=json.loads(Path(args.resume).read_text())
    mesh=ExtendedFieldMesh(data['base'],vmax=args.vmax);n=len(mesh.nodes)
    if restored:
        implementations={c.__name__:c for c in (RouteFunctional,TemplateFunctional,InitialInwardFunctional,TwoInteriorFunctional)}
        raw_pool=[implementations[row['implementation']](mesh,row['route'],row['label'])for row in restored['pool']]
    else:raw_pool=route_pool(mesh)+full_native_m2_pool(mesh)+two_interior_pool(mesh)
    pool=[]
    seen=set()
    def key(route):
        points=tuple((round(t,11),round(x,11)) for t,x in route)
        return min(points,tuple((t,-x) for t,x in points))
    for f in raw_pool:
        k=key(f.route)
        if restored or k not in seen:pool.append(f);seen.add(k)
    def add_file(path):
        if not path.exists():return 0
        payload=json.loads(path.read_text());found=[]
        def walk(obj):
            if isinstance(obj,dict):
                if 'route' in obj:found.append(obj['route'])
                for value in obj.values():walk(value)
            elif isinstance(obj,list):
                for value in obj:walk(value)
        walk(payload);added=0
        for j,route in enumerate(found):
            try:route=[tuple(float(Fraction(v)) if isinstance(v,str) else float(v) for v in p) for p in route]
            except (TypeError,ValueError):continue
            if not route or any(len(p)!=2 for p in route):continue
            walls=set();complete=[]
            for point in route:
                complete.append(point)
                if abs(abs(point[1])-1)<1e-12:walls.add(1 if point[1]>0 else -1)
                if len(walls)==2:break
            route=complete
            k=key(route)
            if k in seen:continue
            try:functional=RouteFunctional(mesh,route,dict(kind='global_attack',source=path.name,index=j))
            except (AssertionError,ValueError):continue
            pool.append(functional);seen.add(k);added+=1
        return added
    bank=Path(args.attack_bank)if args.attack_bank else prepare_routes([HERE/'continuum_bank_routes.json']+
                        sorted(HERE.glob('continuous_response_*.json'))+
                        sorted(HERE.glob('*_node_dp_*.json'))+
                        sorted(HERE.glob('*_inward_*.json')),
                        output=HERE/f'{args.tag}_attack_routes.json')
    add_file(bank)
    values=np.asarray(restored['values'])if restored else mesh.import_values(data)
    structural=sparse([{lo:1.,hi:-1.} for lo,hi,axis in mesh.transport],n+1)
    cuts=[];rhs=[];cut_routes=[]
    best=-np.inf;history=[];answer=None;best_values=values.copy();best_report=None
    objective=np.r_[np.zeros(n),-1.]
    bounds=mesh.bounds+[(0.,args.ceiling)]
    hot=None if args.cold_lp else FieldMaster(objective,bounds,structural,args.lp_seconds)
    checkpoint_path=Path(args.checkpoint)if args.checkpoint else HERE/f'{args.tag}_model.json.gz'
    def checkpoint(pending):
        if hot:hot.append(sparse(cuts,n+1),rhs)
        payload=dict(scope='Numerical model checkpoint: all previous physical constraints, cost cuts, route metadata and simplex basis.',
            base=mesh.base.tolist(),vmax=mesh.vmax,values=values.tolist(),best_values=best_values.tolist(),
            best=best if np.isfinite(best)else None,best_report=best_report,history=history,
            master_upper=args.ceiling if answer is None else float(answer.x[-1]),pending_solve=pending,
            cuts=[list(row.items())for row in cuts],rhs=rhs,cut_routes=cut_routes,
            pool=[dict(implementation=type(f).__name__,route=f.route,label=f.label)for f in pool],
            basis=hot.basis()if hot else None)
        payload['replayed_from']=args.replay_run
        temporary=checkpoint_path.with_name(checkpoint_path.name+'.tmp')
        with gzip.open(temporary,'wt',compresslevel=3)as file:json.dump(payload,file,separators=(',',':'))
        temporary.replace(checkpoint_path)
    def primary():
        cut_matrix=sparse(cuts,n+1)
        if hot:return hot.primary(cut_matrix,rhs)
        matrix=vstack([structural,cut_matrix],format='csr')
        return linprog(objective,A_ub=matrix,b_ub=np.r_[np.zeros(structural.shape[0]),rhs],
            bounds=bounds,method=args.method,options=dict(primal_feasibility_tolerance=1e-9,
            dual_feasibility_tolerance=1e-9,time_limit=args.lp_seconds))
    if restored:
        cuts=[{int(i):float(v)for i,v in row}for row in restored['cuts']]
        rhs=list(restored['rhs']);cut_routes=list(restored['cut_routes'])
        best=-np.inf if restored['best']is None else restored['best']
        best_values=np.asarray(restored['best_values']);best_report=restored['best_report'];history=restored['history']
        answer=SimpleNamespace(x=np.r_[values,restored['master_upper']])
        if hot:
            hot.append(sparse(cuts,n+1),rhs);hot.restore_basis(restored['basis'])
        print(json.dumps(dict(event='restored_model',routes=len(pool),cuts=len(cuts),
                             basis_restored=bool(restored['basis']and restored['basis']['valid']))),flush=True)
        if restored['pending_solve']:
            trial=primary()
            if not trial.success:
                checkpoint(True)
                print(json.dumps(dict(event='restored_lp_failure',message=trial.message)),flush=True)
                return history
            answer=trial;values=answer.x[:n];checkpoint(False)
    if args.replay_run:
        # Earlier cold runs did not expose their solver basis. Reconstruct
        # their tangent cuts from frozen complete fields. Including every
        # currently violated route, rather than only the old batch, retains
        # the old cuts and may add further valid supporting inequalities.
        old_tag=args.replay_run
        old_data=json.loads((HERE/f'{old_tag}_field.json').read_text())
        add_file(HERE/f'{old_tag}_attack_routes.json')
        for path in [HERE/'continuum_dp_attacks.json',HERE/'continuum_m1_attacks.json',HERE/'continuum_known_new_attacks.json']:
            add_file(path)
        for entry in old_data['history']:
            number=entry['iteration'];path=HERE/f'{old_tag}_iter_{number:02d}.json'
            if not path.exists():raise ValueError(('Missing replay field',path))
            previous=json.loads(path.read_text());assert np.array_equal(np.asarray(previous['nodes']),mesh.nodes)
            point=np.asarray(previous['values'])
            replayed_worst=RouteFunctional(mesh,entry['worst_path']).value_gradient(point)[0]
            assert abs(replayed_worst-entry['minimum_route_cost'])<1e-8,('replay payoff',number,replayed_worst,entry['minimum_route_cost'])
            inward_path=HERE/f'{old_tag}_inward_{number:02d}.json'
            if inward_path.exists():
                for row in json.loads(inward_path.read_text())['attacks']:
                    # Retain the specialized supergradient even when a
                    # generic representation of the same route is present.
                    pool.append(InitialInwardFunctional(mesh,row['route'],row['label']));seen.add(key(row['route']))
            add_file(HERE/f'{old_tag}_node_dp_{number:02d}.json')
            added=0
            for j,f in enumerate(pool):
                value,g=f.value_gradient(point)
                if number and value>entry['master_upper']+1e-8:continue
                indices=np.flatnonzero(abs(g)>1e-14)
                row={int(i):-float(g[i])for i in indices};row[n]=1.
                cuts.append(row);rhs.append(float(value-g[indices]@point[indices]));cut_routes.append(j);added+=1
            print(json.dumps(dict(event='replayed_global_cuts',source=old_tag,iteration=number,added=added,total=len(cuts))),flush=True)
        checkpoint(True);trial=primary()
        if not trial.success:
            checkpoint(True)
            print(json.dumps(dict(event='replayed_lp_failure',message=trial.message)),flush=True)
            return history
        answer=trial;values=answer.x[:n];checkpoint(False)
        print(json.dumps(dict(event='replayed_primary_solved',master=float(answer.x[-1]),cuts=len(cuts))),flush=True)
    print(json.dumps(dict(event='setup',nodes=n,triangles=len(mesh.triangles),routes=len(pool),
                         batch=args.batch,method=args.method if args.cold_lp else 'persistent IPM then simplex',
                         terminal_time=mesh.vmax+1)),flush=True)
    first_iteration=max((row['iteration']for row in history),default=-1)+1
    last_iteration=first_iteration+args.iterations
    for iteration in range(first_iteration,last_iteration+1):
        previous_routes=len(pool)
        added_routes=0
        for path in [HERE/'continuum_dp_attacks.json',HERE/'continuum_m1_attacks.json',
                     HERE/'continuum_known_new_attacks.json']:
            added_routes+=add_file(path)
        values,repair=mesh.repair_values(values)
        inward=None
        if args.inward_batch:
            scanner=InwardScanner(dict(base=mesh.base.tolist(),nodes=mesh.nodes.tolist(),
                                       values=values.tolist(),domain_max_v=mesh.vmax))
            inward_costs=scanner.evaluate();indices=np.argsort(inward_costs)[:args.inward_batch]
            inward_rows=[]
            for index in indices:
                route=scanner.route(index);label=scanner.label(index);k=key(route)
                inward_rows.append(dict(route=route,label=label,decimal=float(inward_costs[index])))
                if k in seen:continue
                pool.append(InitialInwardFunctional(mesh,route,label));seen.add(k);added_routes+=1
            inward=dict(scope='All native-grid initial-inward routes; numerical complete-family scan.',
                         routes=len(inward_costs),minimum=float(inward_costs.min()),attacks=inward_rows)
            (HERE/f'{args.tag}_inward_{iteration:02d}.json').write_text(json.dumps(inward,indent=2)+'\n')
        separator=None
        if args.dp_bins:
            # Every iterate receives a fresh unrestricted-shape physical
            # grid search. Its record discretization is a discovery
            # device; each returned physical path is then scored against
            # the complete continuum field, including all contact atoms.
            snapshot=HERE/f'{args.tag}_iter_{iteration:02d}.json'
            mesh.save(snapshot,values,compact=True,scope='Frozen legal CDF iterate for global physical-grid separation; no unrestricted lower guarantee.')
            output=HERE/f'{args.tag}_node_dp_{iteration:02d}.json'
            work=Path(tempfile.gettempdir())/f'princess-monster-{args.tag}-node-dp'
            subprocess.run([sys.executable,str(HERE/'continuous_response_grid.py'),str(snapshot),
                            '--bins',str(args.dp_bins),'--route-count',str(args.dp_routes),
                            '--all-prefixes','--work',str(work),'--output',str(output)],check=True,
                           stdout=subprocess.DEVNULL)
            separator=json.loads(output.read_text())
            added_routes+=add_file(output)
            print(json.dumps(dict(event='global_physical_separator',iteration=iteration,
                                 rank_bins=args.dp_bins,minimum=separator['best_attack']['decimal'],
                                 attacks=len(separator['attacks']),report=output.name)),flush=True)
        if added_routes and np.isfinite(best):
            # Compare incumbents against the same growing route bank.
            best=min(best,min(f.value_gradient(best_values)[0] for f in pool[previous_routes:]))
        evaluations=[]
        for f in pool:
            value,g=f.value_gradient(values)
            indices=np.flatnonzero(abs(g)>1e-14)
            evaluations.append((value,indices,g[indices]))
        costs=np.array([e[0] for e in evaluations]);worst=int(costs.argmin())
        upper=args.ceiling if answer is None else float(answer.x[-1])
        gap=upper-costs.min()
        report=dict(iteration=iteration,master_upper=upper,minimum_route_cost=float(costs[worst]),
                    global_cut_gap=float(gap),worst_route=pool[worst].label,
                    worst_path=pool[worst].route,cuts=len(cuts),routes=len(pool),
                    new_routes=added_routes,rounding_repair=repair,seconds=time.monotonic()-started,
                    complete_native_inward=(dict(routes=inward['routes'],minimum=inward['minimum'])
                                             if inward is not None else None),
                    global_physical_separator=(dict(rank_bins=args.dp_bins,
                        minimum_route_cost=separator['best_attack']['decimal'],
                        attacks=len(separator['attacks'])) if separator is not None else None))
        history.append(report);print(json.dumps(report),flush=True)
        opts=dict(positive_v=False,negative_v=False,center_peak=None,terminal_barrier=None,
                  constant_early_cone=None,all_fixed_routes_rescored=True,batch=args.batch)
        meta=dict(options=opts,report=report,history=history,
                  attack_bank_snapshot=bank.name,
                  scope='Complete legal fixed-mesh continuum CDF; numerical finite-bank maximin, '
                        'not an unrestricted lower certificate.')
        mesh.save(HERE/f'{args.tag}_field.json',values,compact=True,**meta)
        if costs[worst]>best or best_report is None:
            best=float(costs[worst]);best_values=values.copy()
            best_report=dict(report)
        checked_best=dict(best_report,minimum_route_cost=best,verified_routes=len(pool),
                          latest_separation_iteration=iteration)
        mesh.save(HERE/f'{args.tag}_best_field.json',best_values,compact=True,
                  **dict(meta,report=checked_best))
        if (answer is not None and gap<=args.tolerance) or iteration==last_iteration:
            checkpoint(False);break
        order=np.argsort(costs)
        selected=([int(j) for j in order] if not cuts and args.initial_all else
                  [int(j) for j in order if upper-costs[j]>max(args.tolerance/4,1e-8)][:args.batch])
        if not selected:break
        for j in selected:
            value,indices,g=evaluations[j]
            row={int(i):-float(x) for i,x in zip(indices,g)};row[n]=1.
            cuts.append(row);rhs.append(float(value-g@values[indices]));cut_routes.append(j)
        checkpoint(True);trial=primary()
        if not trial.success:
            checkpoint(True)
            print(json.dumps(dict(event='lp_failure',message=trial.message,iteration=iteration,
                                 checkpoint=str(checkpoint_path))),flush=True)
            break
        answer=trial;values=answer.x[:n];checkpoint(False)
        weights=np.zeros(len(pool))
        for j,w in zip(cut_routes,-answer.ineqlin.marginals[structural.shape[0]:]):weights[j]+=w
        total_weight=float(weights.sum())
        assert -1e-7<=total_weight<=1+1e-7
        families=defaultdict(float)
        for f,w in zip(pool,weights):families[f.label.get('kind','unknown')]+=float(w)
        payload=dict(scope='Normalized cost-cut dual monster candidate; global princess response '
                     'must be checked independently before claiming an upper guarantee.',
                     iteration=iteration,master_value=float(answer.x[-1]),weight_sum=total_weight,
                     imposed_ceiling=args.ceiling,normalization_required=abs(total_weight-1)>1e-7,
                     symmetry='Each listed route denotes its fair mixture with spatial reflection.',
                     family_mass=dict(families),routes=[dict(weight=float(w),label=f.label,route=f.route)
                     for f,w in zip(pool,weights) if w>1e-12],seconds=time.monotonic()-started)
        (HERE/f'{args.tag}_duals.json').write_text(json.dumps(payload,indent=2)+'\n')
        print(json.dumps(dict(event='dual_candidate',iteration=iteration,value=payload['master_value'],
                             support=len(payload['routes']),families=dict(families))),flush=True)
        if args.proximal:
            # The whole field remains free. This secondary LP chooses the
            # nearest point on the almost-optimal master face, preventing
            # arbitrary LP vertex oscillations in weakly constrained cells.
            matrix=vstack([structural,sparse(cuts,n+1)],format='csr')
            extended=hstack([matrix,csr_matrix((matrix.shape[0],n))],format='csr')
            deviations=[];deviation_rhs=[]
            for i in range(n):
                deviations.extend(({i:1.,n+1+i:-1.},{i:-1.,n+1+i:-1.}))
                deviation_rhs.extend((best_values[i],-best_values[i]))
            extended=vstack([extended,sparse(deviations,2*n+1)],format='csr')
            prox_bounds=list(bounds)+[(0.,None)]*n
            prox_bounds[n]=(max(0.,float(answer.x[-1])-args.tolerance/4),float(answer.x[-1]))
            prox=linprog(np.r_[np.zeros(n+1),np.ones(n)/n],A_ub=extended,
                         b_ub=np.r_[np.zeros(structural.shape[0]),rhs,deviation_rhs],
                         bounds=prox_bounds,method=args.method,options=dict(primal_feasibility_tolerance=1e-9,
                         dual_feasibility_tolerance=1e-9,time_limit=args.lp_seconds))
            if prox.success:
                values=prox.x[:n]
                print(json.dumps(dict(event='proximal_choice',iteration=iteration,
                                     mean_nodal_change=float(prox.fun))),flush=True)
            else:print(json.dumps(dict(event='proximal_failure',message=prox.message)),flush=True)
    return history


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--resume',default=str(ROOT/'packages/interval_cdf_discovery/snapshots/initial_inward_repaired.json'))
    p.add_argument('--resume-checkpoint',help='Restore every prior cut, physical route, and saved simplex basis.')
    p.add_argument('--checkpoint',help='Numerical model checkpoint path; defaults to TAG_model.json.gz.')
    p.add_argument('--replay-run',help='Preserve cold-run cuts by replaying its frozen fields and attack snapshots.')
    p.add_argument('--attack-bank',help='Use a specified frozen additional-route bank; default gathers all current attacks.')
    p.add_argument('--cold-lp',action='store_true',help='Use cold scipy.linprog calls instead of persistent HiGHS.')
    p.add_argument('--iterations',type=int,default=24)
    p.add_argument('--vmax',type=int,default=2,
                   help='Whole characteristic-domain maximum V; absorption time is Vmax+1.')
    p.add_argument('--dp-bins',type=int,default=64,
                   help='Run physical native-node DP with this many record bins on every iterate; zero disables it.')
    p.add_argument('--dp-routes',type=int,default=8)
    p.add_argument('--inward-batch',type=int,default=512,
                   help='Scan the entire native initial-inward family and add this many worst routes; zero disables it.')
    p.add_argument('--batch',type=int,default=512)
    p.add_argument('--initial-all',action='store_true',
                   help='Seed one supporting cut for every configured route before batched separation.')
    p.add_argument('--tolerance',type=float,default=2e-7)
    p.add_argument('--method',choices=['highs','highs-ds','highs-ipm'],default='highs-ipm')
    p.add_argument('--lp-seconds',type=float,default=300.)
    p.add_argument('--ceiling',type=float,default=2.)
    p.add_argument('--proximal',action='store_true')
    p.add_argument('--tag',default='continuum_global')
    solve(p.parse_args())


if __name__=='__main__':main()
