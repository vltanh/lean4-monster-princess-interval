#!/usr/bin/env python3
"""Canonicalize a CDF at a fixed security floor using exact response separation.

Only the shape objective is floating point. An accepted profile must pass the
complete integer normalized-bank oracle at the requested rational security
floor. Its unrestricted game-value certificate still subtracts 1/(2n).
No claim of exact optimality of the discrete variation objective is made.
"""
from __future__ import annotations
import argparse
from fractions import Fraction
import gzip
import hashlib
import json
import os
from pathlib import Path
import sys
import time

import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix, csr_matrix, hstack, vstack, eye

ROOT = Path(__file__).resolve().parents[2]
NATIVE = ROOT/'packages/interval_clock_grid/normalized_native'
sys.path.insert(0, str(NATIVE))
sys.path.insert(0, str(ROOT/'packages/interval_discovery'))
from solve_normalized import Master
from interpolated_master import InterpolatedMaster
from cached_path_pricing import CachedPathPricing, normalize_path
from princess_search import read_json, write_json, digest, full_seed

CURRENT_GAME_LOWER = Fraction(582291421641,409600000000)


def add_checkpoint(master, path, table=None):
    data = read_json(path)
    if master.n % data['n']:
        raise ValueError('response checkpoint grid must divide the current bank')
    ratio = master.n//data['n']
    plans = data.get('paths')
    if plans is None:
        plans = [c['plan'] for c in data['columns']]
    count = 0
    for p in plans:
        if 'minus_charges' not in p or 'plus_charges' not in p:
            if table is None:raise ValueError('a physical-only seed needs a current profile')
            physical = normalize_path(master.n,p,source_n=data['n'])
            count += master.add(physical,table)
            continue
        scaled = {'start_grid':p['start_grid']*ratio,
                  'moves':[s for s in p['moves'] for _ in range(ratio)],
                  'minus_charges':[[j*ratio,a*ratio] for j,a in p['minus_charges']],
                  'plus_charges':[[j*ratio,a*ratio] for j,a in p['plus_charges']]}
        # Validate physical geometry separately from the supplied causal clocks.
        normalize_path(master.n, scaled)
        count += int(master.add_plan(scaled))
    return count


def difference_matrix(coarse, order=1):
    rr, cc, vv = [], [], []
    count = 0
    for k in range(1,coarse.R+1):
        times = range(k%2,coarse.C+1,2)
        indices = [coarse.index[j,k] for j in times]
        for i in range(len(indices)-order):
            coefficients = [-1,1] if order == 1 else [1,-2,1]
            for index, coefficient in zip(indices[i:i+order+1],coefficients):
                rr.append(count);cc.append(index);vv.append(coefficient)
            count += 1
    return coo_matrix((vv,(rr,cc)),shape=(count,coarse.K)).tocsr()


def initial_integer_bounds(master, table):
    """Propagate fixed initial values through the finite order graph exactly."""
    coarse = getattr(master,'coarse',master)
    ratio = master.n//coarse.n
    factor = master.D//coarse.D
    lower = np.zeros(coarse.K,dtype=np.int64)
    upper = np.full(coarse.K,coarse.D,dtype=np.int64)
    adjacency = [[] for _ in range(coarse.K)]
    indegree = [0]*coarse.K
    for a,b in coarse.order:
        adjacency[a].append(b);indegree[b] += 1
    anchors = {}
    for i,(j,k) in enumerate(coarse.nodes):
        if j == 0:
            value,remainder = divmod(int(table[j*ratio,k*ratio]),factor)
            if remainder:raise AssertionError('coarse anchor does not have its integer scale')
            lower[i] = upper[i] = value
            anchors[i] = value
    queue = [i for i,a in enumerate(indegree) if a == 0]
    for a in queue:
        for b in adjacency[a]:
            lower[b] = max(lower[b],lower[a]);indegree[b] -= 1
            if indegree[b] == 0:queue.append(b)
    if len(queue) != coarse.K:raise AssertionError('profile order should be acyclic')
    for a in reversed(queue):
        for b in adjacency[a]:upper[a] = min(upper[a],upper[b])
    if np.any(lower > upper):raise AssertionError('the feasible seed should give compatible anchors')
    return lower,upper,anchors


def anchored_trial(master, values, anchor_bounds):
    if anchor_bounds is None:return values
    coarse = getattr(master,'coarse',master)
    lower,upper,_ = anchor_bounds
    rounded = np.floor(np.clip(values,0,1)*coarse.D).astype(np.int64)
    rounded = np.maximum(lower,np.minimum(upper,rounded))
    # The quarter-unit interior avoids floating division producing N-1 when
    # the existing integer sampler applies floor again. It is construction
    # only; the table and all security comparisons remain exact integers.
    return (rounded.astype(np.float64)+.25)/coarse.D


def shape_metrics(master, table):
    coarse = getattr(master,'coarse',master)
    ratio = master.n//coarse.n
    values = [int(table[j*ratio,k*ratio]) for j,k in coarse.nodes]
    variation = curvature = reversals = 0
    for k in range(1,coarse.R+1):
        row = [values[coarse.index[j,k]] for j in range(k%2,coarse.C+1,2)]
        delta = [b-a for a,b in zip(row,row[1:])]
        variation += sum(abs(a) for a in delta)
        curvature += sum(abs(b-a) for a,b in zip(delta,delta[1:]))
        signs = [1 if a>0 else -1 for a in delta if a]
        reversals += sum(a != b for a,b in zip(signs,signs[1:]))
    parents = list(range(coarse.K))
    def find(i):
        while parents[i] != i:
            parents[i] = parents[parents[i]]
            i = parents[i]
        return i
    tight = 0
    for a,b in coarse.order:
        if values[a] == values[b]:
            tight += 1
            a,b = find(a),find(b)
            if a != b:parents[a] = b
    counts = {}
    for i in range(coarse.K):
        root = find(i);counts[root] = counts.get(root,0)+1
    # Discrete exact functionals; the factor 1/(2m) is radial mesh width.
    scale = master.D*2*coarse.n
    return {'scope':'Exact nodal shape statistics; not a phase classification.',
            'profile_grid':coarse.n,
            'temporal_total_variation':str(Fraction(variation,scale)),
            'temporal_total_variation_decimal':variation/scale,
            'temporal_curvature':str(Fraction(curvature,scale)),
            'temporal_curvature_decimal':curvature/scale,
            'temporal_direction_reversals':reversals,
            'tight_order_edges':tight,'order_edges':len(coarse.order),
            'tight_equality_components':len(counts),
            'largest_equality_components':sorted(counts.values(),reverse=True)[:20]}


def save_field(path,master,table,answer,seed_hash):
    if answer.get('status') != 'PASS' or answer.get('certifies_lower') is False:
        raise ValueError('a complete exact pricing result is required')
    units,den = int(answer['minimum_units']),4*master.n*master.D
    lower = Fraction(units-2*master.D,den)
    data = {'scope':'Complete exact normalized-bank pricing of a shape-regularized legal profile; unrestricted game-value lower uses the established 1/(2n) transfer. No same-CDF continuum security claimed.',
            'n':master.n,'field_denominator':str(master.D),'normalized_profile':True,
            'radial_nodes':[[j,k,str(int(table[j,k]))] for j in range(master.H+1)
                            for k in range(1,master.R+1) if (j+k)%2 == 0],
            'minimum_units':str(units),'objective_denominator':str(den),
            'normalized_bank_dual_value':str(Fraction(units,den)),
            'global_lower':str(lower),'global_lower_decimal':float(lower),
            'pricing':answer,'seed_sha256':seed_hash,
            'native_source_sha256':digest(NATIVE/'price_normalized.cpp')}
    if Path(path).suffix == '.gz':
        Path(path).write_bytes(gzip.compress(json.dumps(data,separators=(',',':')).encode()+b'\n',mtime=0))
    else:
        write_json(path,data)


def contact_summary(n, plans, scope):
    histogram = {'center':0,'endpoint':0,'incoming_t_plus_r_1':0,
                 'outgoing_t_minus_r_1':0,'other':0}
    lines = {'t_plus_r':{},'t_minus_r':{}}
    for plan in plans:
        positions = [plan['start_grid']]
        for move in plan['moves']:positions.append(positions[-1]+move)
        for name in ('minus_charges','plus_charges'):
            for j,a in plan[name]:
                r = abs(positions[j]);t = j
                key = ('center' if r == 0 else 'endpoint' if r == 2*n
                       else 'incoming_t_plus_r_1' if t+r == 2*n
                       else 'outgoing_t_minus_r_1' if t-r == 2*n else 'other')
                histogram[key] += 1
                for name,value in [('t_plus_r',t+r),('t_minus_r',t-r)]:
                    label = str(Fraction(value,2*n))
                    lines[name][label] = lines[name].get(label,0)+1
    return {'scope':scope,
            'active_calendars':len(plans),'charge_location_counts':histogram,
            'most_frequent_contact_lines':{name:sorted(row.items(),key=lambda x:-x[1])[:20]
                                           for name,row in lines.items()}}


def active_contacts(master, lp, norder):
    # Multipliers for a variation objective do not form a Monster mixture.
    weights = -np.asarray(lp.ineqlin.marginals[norder:norder+len(master.columns)])
    plans = [c['plan'] for c,w in zip(master.columns,weights) if w > 1e-8]
    return contact_summary(master.n,plans,
        'Unweighted clock-charge locations in active floating shape constraints; regularizer dual multipliers are not a physical Monster law.')


def solve_shape(master, baseline, floor, objective, fixed_initial, seconds):
    coarse = getattr(master,'coarse',master)
    difference = difference_matrix(coarse,1 if objective == 'variation' else 2)
    ntv,K = difference.shape
    order = hstack([master.order_matrix[:,:K],csr_matrix((len(master.order),ntv))],format='csr')
    rr,cc,vv,rhs = [],[],[],[]
    scale = 4*master.n
    for row,column in enumerate(master.columns):
        for i,a in column['coeff'].items():rr.append(row);cc.append(i);vv.append(-a/scale)
        # A small numerical guard helps floor repair; acceptance uses the exact
        # rational floor and complete integer oracle regardless of this guard.
        rhs.append(column['mass']/scale-float(floor)-32/coarse.D)
    cuts = hstack([coo_matrix((vv,(rr,cc)),shape=(len(master.columns),K)).tocsr(),
                   csr_matrix((len(master.columns),ntv))],format='csr')
    absolute = vstack([hstack([difference,-eye(ntv,format='csr')]),
                       hstack([-difference,-eye(ntv,format='csr')])],format='csr')
    matrix = vstack([order,cuts,absolute],format='csr')
    bounds = [(0.,1.)]*K + [(0.,None)]*ntv
    if fixed_initial:
        for i,(j,k) in enumerate(coarse.nodes):
            if j == 0:bounds[i] = (baseline[i],baseline[i])
    cost = np.r_[np.zeros(K),np.ones(ntv)/(2*coarse.n)]
    result = linprog(cost,A_ub=matrix,
                     b_ub=np.r_[np.zeros(len(master.order)),rhs,np.zeros(2*ntv)],
                     bounds=bounds,method='highs-ds',
                     options={'time_limit':max(.1,min(120.,seconds)),
                              'primal_feasibility_tolerance':1e-9,
                              'dual_feasibility_tolerance':1e-9})
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--seed-field',type=Path,required=True)
    parser.add_argument('--response-checkpoint',type=Path)
    parser.add_argument('--n',type=int,required=True)
    parser.add_argument('--profile-grid',type=int,required=True)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--fixed-initial',action='store_true')
    parser.add_argument('--objective',choices=('variation','curvature'),default='variation')
    parser.add_argument('--loss',default='1/100000',help='Declared rational allowance below the exact seed bank value.')
    parser.add_argument('--floor',help='Override the seed-minus-loss security floor.')
    parser.add_argument('--iterations',type=int,default=120)
    parser.add_argument('--seconds',type=int,default=900)
    parser.add_argument('--denominator',type=int,default=10**9)
    parser.add_argument('--pricing-paths',type=int,default=64)
    parser.add_argument('--independent-replay',action='store_true')
    args = parser.parse_args()
    if args.n < 1 or not 1 <= args.profile_grid <= args.n or args.n % args.profile_grid:
        parser.error('profile grid must divide the bank grid')
    if Fraction(args.loss) < 0:parser.error('security loss must be nonnegative')
    directory = args.output.resolve();directory.mkdir(parents=True,exist_ok=True)
    began = time.monotonic()
    master = (Master(args.n,directory/'oracle.work',args.denominator,True)
              if args.n == args.profile_grid else
              InterpolatedMaster(args.n,args.profile_grid,directory/'oracle.work',args.denominator))
    seed = full_seed(args.seed_field)
    initial = master.interpolate_seed(seed)
    seed_answer,seed_table = master.price(initial,keep=args.pricing_paths)
    baseline = master.profile_values(seed_table)
    anchor_bounds = initial_integer_bounds(master,seed_table) if args.fixed_initial else None
    seed_value = Fraction(int(seed_answer['minimum_units']),4*master.n*master.D)
    floor = Fraction(args.floor) if args.floor else seed_value-Fraction(args.loss)
    if floor > seed_value:
        raise ValueError('requested floor exceeds the certified seed; feasibility is not established')
    seed_hash = digest(args.seed_field)
    save_field(directory/'seed.dual.json',master,seed_table,seed_answer,seed_hash)
    if args.response_checkpoint:add_checkpoint(master,args.response_checkpoint,seed_table)
    for path in seed_answer['paths']:master.add(path,seed_table)
    cache = CachedPathPricing(master.n,master.D)
    cache.update_columns(master.columns)
    before = shape_metrics(master,seed_table)
    manifest = {'status':'RUNNING','scope':'Discovery of lower-variation CDFs at a fixed exact finite-bank floor; floating shape optimality is not certified.',
                'options':{k:str(v) if isinstance(v,Path) else v for k,v in vars(args).items()},
                'seed_field_sha256':seed_hash,'seed_exact_bank_value':str(seed_value),
                'requested_bank_floor':str(floor),'declared_bank_allowance':str(seed_value-floor),
                'unrestricted_game_floor':str(floor-Fraction(1,2*master.n)),
                'current_certified_game_lower':str(CURRENT_GAME_LOWER),
                'same_cdf_continuum_security_claimed':False,
                'github_run_id':os.environ.get('GITHUB_RUN_ID'),'github_sha':os.environ.get('GITHUB_SHA'),
                'source_sha256':{str(p.relative_to(ROOT)):digest(p) for p in [Path(__file__),NATIVE/'price_normalized.cpp',NATIVE/'interpolated_master.py']},
                'before':before,'history':[]}
    if args.response_checkpoint:
        response_data = read_json(args.response_checkpoint)
        if 'weights' in response_data:
            plans = [c['plan'] for c,w in zip(response_data['columns'],response_data['weights']) if w > 1e-8]
            manifest['before_contact_lines'] = contact_summary(response_data['n'],plans,
                'Unweighted clock-charge locations in the floating seed master active constraints; different objectives make the multiplier magnitudes incomparable.')
    write_json(directory/'manifest.json',manifest)
    best_table,best_answer,best_metrics = seed_table,seed_answer,before
    accepted = 0
    last_lp = None
    try:
        for iteration in range(args.iterations):
            remaining = args.seconds-(time.monotonic()-began)
            if remaining <= 0:
                manifest['stop_reason'] = 'BUDGET_STOPPED';break
            lp = solve_shape(master,baseline,floor,args.objective,args.fixed_initial,remaining)
            if not lp.success:
                manifest['stop_reason'] = 'LP_STOPPED'
                manifest['lp_message'] = lp.message
                break
            last_lp = lp
            trial = anchored_trial(master,lp.x[:master.K],anchor_bounds)
            table = master.repair(trial)
            if anchor_bounds is not None:
                coarse = getattr(master,'coarse',master)
                ratio = master.n//coarse.n;factor = master.D//coarse.D
                for i,value in anchor_bounds[2].items():
                    j,k = coarse.nodes[i]
                    if int(table[j*ratio,k*ratio]) != value*factor:
                        raise AssertionError('integer repair changed a fixed initial value')
            cache.update_columns(master.columns)
            cached = cache.price(table,keep=args.pricing_paths,level=float(floor))
            added = sum(master.add(path,table) for path in cached['violating_paths'])
            item = {'iteration':iteration,'floating_shape_objective':float(lp.fun),
                    'columns':len(master.columns),'seconds':time.monotonic()-began,
                    'cache_paths':len(cache)}
            if added:
                item.update({'pricing_scope':'cached response separation only','new_calendars':added,
                             'cached_bank_upper':str(Fraction(int(cached['cached_minimum_units']),4*master.n*master.D))})
            else:
                answer,table = master.price(trial,keep=args.pricing_paths)
                value = Fraction(int(answer['minimum_units']),4*master.n*master.D)
                cache.add_many(answer['paths'])
                item.update({'pricing_scope':'complete exact native oracle','exact_bank_value':str(value),
                             'accepted_security_floor':value >= floor})
                if value >= floor:
                    metrics = shape_metrics(master,table);accepted += 1
                    key = 'temporal_total_variation' if args.objective == 'variation' else 'temporal_curvature'
                    if Fraction(metrics[key]) < Fraction(best_metrics[key]):
                        best_table,best_answer,best_metrics = table,answer,metrics
                    manifest['accepted_contact_lines'] = active_contacts(master,lp,len(master.order))
                    manifest['stop_reason'] = 'ACCEPTED_COMPLETE_ORACLE'
                    manifest['history'].append(item)
                    print(json.dumps(item),flush=True)
                    break
                rejected = directory/'rejected'
                rejected.mkdir(exist_ok=True)
                rejected_field = rejected/f'iteration_{iteration:04d}.dual.json.gz'
                concise = dict(answer)
                concise['paths'] = answer['paths'][:4]
                save_field(rejected_field,master,table,concise,seed_hash)
                item['rejected_field'] = str(rejected_field.relative_to(directory))
                item['rejected_field_sha256'] = digest(rejected_field)
                item['attack_scope'] = 'Physical paths with exact nodal running-record calendar costs; no same-CDF continuous-payoff assertion.'
                added = sum(master.add(path,table) for path in answer['paths'])
                item['new_calendars'] = added
                if not added:
                    manifest['stop_reason'] = 'NUMERICAL_SEPARATION_STALLED'
                    manifest['history'].append(item)
                    print(json.dumps(item),flush=True)
                    break
            manifest['history'].append(item)
            write_json(directory/'manifest.json',manifest)
            print(json.dumps(item),flush=True)
        else:
            manifest['stop_reason'] = 'ITERATION_LIMIT'
        save_field(directory/'candidate.dual.json',master,best_table,best_answer,seed_hash)
        manifest['accepted_new_profiles'] = accepted
        manifest['after'] = best_metrics
        metric_key = 'temporal_total_variation' if args.objective == 'variation' else 'temporal_curvature'
        manifest['shape_improved'] = Fraction(best_metrics[metric_key]) < Fraction(before[metric_key])
        manifest['search_result'] = 'NEW_ACCEPTED_SHAPE' if manifest['shape_improved'] else 'NO_NEW_ACCEPTED_SHAPE'
        value = Fraction(int(best_answer['minimum_units']),4*master.n*master.D)
        manifest['best_exact_bank_value'] = str(value)
        manifest['best_game_value_lower'] = str(value-Fraction(1,2*master.n))
        manifest['improves_current_game_lower'] = value-Fraction(1,2*master.n) > CURRENT_GAME_LOWER
        manifest['exact_security_floor_verified'] = value >= floor
        manifest['status'] = 'PASS'
        write_json(directory/'response.checkpoint.json',{
            'scope':'Physical calendar constraints for shape regularization; no Monster mixture weights.',
            'n':master.n,'profile_grid':args.profile_grid,'columns':master.columns,
            'seed_sha256':seed_hash,'requested_bank_floor':str(floor)})
        if args.independent_replay:
            import subprocess
            with (directory/'independent_bigint_replay.json').open('w') as output:
                subprocess.run(['node','--max-old-space-size=8192',
                    str(ROOT/'packages/interval_clock_grid/normalized_record_pricing.cjs'),
                    str(directory/'candidate.dual.json'),'--target-bound'],check=True,stdout=output)
            manifest['independent_bigint_replay'] = 'PASS'
    except Exception as exc:
        manifest['status'] = 'FAILED';manifest['error'] = str(exc)
        raise
    finally:
        for p in directory.glob('*.work/pricing.input.bin'):p.unlink()
        manifest['seconds'] = time.monotonic()-began
        manifest['artifacts_sha256'] = {str(p.relative_to(directory)):digest(p) for p in directory.rglob('*')
                                        if p.is_file() and p.name not in ('manifest.json','search.log')}
        write_json(directory/'manifest.json',manifest)
        print(json.dumps({k:manifest.get(k) for k in ['status','stop_reason','before','after',
                          'best_exact_bank_value','best_game_value_lower','seconds']}),flush=True)


if __name__ == '__main__':main()
