#!/usr/bin/env python3
"""Global response-cut optimization of a supplied finite monster bank.

Every master contains every monster column. A master objective alone is not
an upper guarantee: the current normalized law is independently separated
by the unrestricted princess survival cut after each solve.
"""
from __future__ import annotations
import argparse
from fractions import Fraction as Q
import json
from pathlib import Path
import subprocess
import sys
import time

import numpy as np
from scipy.optimize import linprog
from scipy.sparse import csr_matrix, eye, hstack, vstack

from survival_minimax import ROOT, append_field_atoms, bank, encode_atom, light_route


def fixed_bank():
    atoms=bank(4)
    keys={(a['kind'],tuple(a['parameters'])) for a in atoms}
    archive=json.loads((ROOT/'packages/interval_refined_upper/strategy.json').read_text())
    for item in archive['families']:
        kind='M'+str(item['kind'])
        pars=(Q(item['start']),) if item['kind']==1 else (Q(item['start']),Q(1))
        if (kind,pars) not in keys:
            atoms.append(dict(kind=kind,parameters=pars));keys.add((kind,pars))
    support=append_field_atoms(atoms)
    assert len(atoms)==909
    weights=[0.]*len(atoms)
    lookup={(a['kind'],tuple(a['parameters'])):i for i,a in enumerate(atoms)}
    for item in archive['families']:
        kind='M'+str(item['kind'])
        pars=(Q(item['start']),) if item['kind']==1 else (Q(item['start']),Q(1))
        weights[lookup[kind,pars]]=item['weight_numerator']/archive['weight_denominator']
    return atoms,weights,support


def export_bank(atoms,weights,support,path):
    records=[]
    for atom in atoms:
        route=light_route(atom)
        cleaned=[];walls=set()
        for u,v in route:
            while len(cleaned)>1 and ((cleaned[-2][0]==cleaned[-1][0]==u)
                  or (cleaned[-2][1]==cleaned[-1][1]==v)):
                cleaned.pop()
            cleaned.append((u,v))
            if u-v in(-2,2):walls.add(u-v)
            if len(walls)==2:break
        records.append(dict(**encode_atom(atom),exact_light=[[str(u),str(v)] for u,v in cleaned],
                            event_light=[[str(u),str(v)] for u,v in route],
                            light=[[float(u),float(v)] for u,v in cleaned]))
    payload=dict(scope='The fixed909monster bank. A pure route denotes its fair reflected pair.',
        atoms=records,seed_weights=weights,field_support=support)
    Path(path).write_text(json.dumps(payload,indent=2)+'\n')
    physical=dict(scope=payload['scope'],count=len(atoms),
        routes=[dict(index=i,kind=atom['kind'],parameters=list(map(str,atom['parameters'])),
          route=[[str((u+v)/2),str((u-v)/2)] for u,v in light_route(atom)])
          for i,atom in enumerate(atoms)])
    (Path(__file__).parent/'continuum_bank_routes.json').write_text(json.dumps(physical,indent=2)+'\n')


class Separator:
    def __init__(self, bank_path):
        command=['node','--stack-size=16384',str(Path(__file__).with_name('efficient_separator.cjs')),str(bank_path)]
        self.process=subprocess.Popen(command,stdin=subprocess.PIPE,stdout=subprocess.PIPE,
                                      stderr=sys.stderr,text=True,bufsize=1)
        self.ready=self.read()
        if 'error' in self.ready:
            raise RuntimeError(self.ready)
    def read(self):
        line=self.process.stdout.readline()
        if not line:
            raise RuntimeError('Separator process exited')
        answer=json.loads(line)
        if 'error' in answer:
            raise RuntimeError(answer['error'])
        return answer
    def call(self,**payload):
        self.process.stdin.write(json.dumps(payload)+'\n');self.process.stdin.flush()
        return self.read()
    def close(self):
        if self.process.poll() is None:
            self.process.stdin.close();self.process.wait(timeout=10)


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--rounds',type=int,default=200)
    parser.add_argument('--tolerance',type=float,default=2e-8)
    parser.add_argument('--face-samples',type=int,default=12)
    parser.add_argument('--output',default='efficient_master_result.json')
    parser.add_argument('--bank-input',help='Explicit physical union bank; default rebuilds the original 909 pairs.')
    parser.add_argument('--pool',default='efficient_master_pool.npz',help='Response pool for this exact bank geometry.')
    parser.add_argument('--export-only',action='store_true')
    parser.add_argument('--resume',help='Previous efficient result; retain its active master-response basis.')
    parser.add_argument('--line-search',type=int,default=3,
                        help='Additional globalcuts on the segment from the incumbent to the master law.')
    parser.add_argument('--prox-level',type=float,default=0.5,
                        help='L1-proximal bundle level between master lower and incumbent upper; negative disables.')
    parser.add_argument('--resume-pool',action='store_true',help='Reuse the saved full response pool for this same geometry.')
    parser.add_argument('--uncross-every',type=int,default=8,
                        help='Every N rounds add all common-quantile profiles of the complete master dual; zero disables.')
    parser.add_argument('--cold-master',action='store_true',help='Use stateless SciPy LP calls instead of retaining HiGHS bases.')
    parser.add_argument('--rational-oracle',action='store_true',help='Use the slower reference rational model for every discovery cut.')
    parser.add_argument('--coarea-steps',type=int,default=0,
                        help='Whole-bank quantile-completion/reoptimization steps before each costly global separation.')
    args=parser.parse_args()
    directory=Path(__file__).parent
    if args.bank_input:
        bank_path=directory/args.bank_input
        explicit=json.loads(bank_path.read_text())
        atoms=[dict(kind=a['kind'],parameters=tuple(map(Q,a['parameters']))) for a in explicit['atoms']]
        seed=explicit['seed_weights']
    else:
        atoms,seed,support=fixed_bank()
        bank_path=directory/'efficient_bank.json'
        export_bank(atoms,seed,support,bank_path)
    if args.export_only:
        print('EXPORTED',len(atoms),'monster pairs',flush=True);return
    started=time.time();separator=Separator(bank_path)
    print('SEPARATOR',{k:v for k,v in separator.ready.items() if k not in ('v','event_labels')},flush=True)
    initial=separator.call(operation='seed')
    rows=[];profiles=[];seen=set();seen_payoffs=set()
    def add(item):
        labels=item['labels']
        key=tuple(labels)
        if key in seen:return False
        seen.add(key)
        payoff_key=np.asarray(item['row'],dtype=np.float64).tobytes()
        if payoff_key in seen_payoffs:return False
        seen_payoffs.add(payoff_key);profiles.append(labels);rows.append(item['row']);return True
    for item in initial['responses']:add(item)
    resumed=json.loads((directory/args.resume).read_text()) if args.resume else None
    if resumed:
        assert resumed['query_v']==separator.ready['v']
        assert resumed['event_labels']==separator.ready['event_labels']
        extra=separator.call(operation='rows',profiles=[r['labels'] for r in resumed['princess_mixture']])
        for item in extra['responses']:add(item)
    pool_path=directory/args.pool
    if args.resume_pool and pool_path.exists():
        pool=np.load(pool_path)
        assert pool['rows'].shape[1]==len(atoms)
        assert pool['labels'].shape[1]==len(separator.ready['v'])
        if 'query_v' in pool:
            assert pool['query_v'].tolist()==separator.ready['v']
        for payoff,labels in zip(pool['rows'],pool['labels']):
            add(dict(row=payoff.tolist(),labels=labels.tolist()))
    print('SEEDS',len(rows),'seconds',time.time()-started,flush=True)
    best=dict(upper=float(initial.get('seed_value',Q(36563170811,25600000000))),
        weights=seed,iteration=-1,response_labels=initial.get('seed_labels'))
    if resumed and resumed.get('best',{}).get('upper',float('inf'))<best['upper']:
        best=resumed['best']
    history=[];closed=False
    hotstart=None
    if not args.cold_master:
        from efficient_hotstart import GlobalMasters
        hotstart=GlobalMasters(len(atoms))
    try:
        for iteration in range(args.rounds):
            matrix=np.asarray(rows,dtype=float)
            objective=np.r_[np.zeros(len(atoms)),1.]
            solution=hotstart.primary(matrix) if hotstart else linprog(objective,
                A_ub=np.c_[matrix,-np.ones(len(matrix))],b_ub=np.zeros(len(matrix)),
                A_eq=np.array([[1.]*len(atoms)+[0.]]),b_eq=[1.],
                bounds=[(0.,None)]*len(atoms)+[(None,None)],method='highs',
                options={'primal_feasibility_tolerance':1e-9,'dual_feasibility_tolerance':1e-9})
            if not solution.success:raise RuntimeError(solution.message)
            for inner in range(args.coarea_steps):
                q=np.maximum(-np.asarray(solution.ineqlin.marginals),0.);q/=q.sum()
                active=[j for j,p in enumerate(q) if p>1e-11]
                coarea=separator.call(operation='uncross',profiles=[profiles[j] for j in active],
                    weights=[float(q[j]) for j in active],retain=-1)
                introduced=sum(add(item) for item in coarea['responses'])
                if not introduced:break
                previous=float(solution.fun);matrix=np.asarray(rows,dtype=float)
                solution=hotstart.primary(matrix) if hotstart else linprog(objective,
                    A_ub=np.c_[matrix,-np.ones(len(matrix))],b_ub=np.zeros(len(matrix)),
                    A_eq=np.array([[1.]*len(atoms)+[0.]]),b_eq=[1.],
                    bounds=[(0.,None)]*len(atoms)+[(None,None)],method='highs',
                    options={'primal_feasibility_tolerance':1e-9,'dual_feasibility_tolerance':1e-9})
                if not solution.success:raise RuntimeError(solution.message)
                assert solution.fun>=previous-2e-7
                print('COAREA',dict(iteration=iteration,inner=inner,added=introduced,
                    master=float(solution.fun),improvement=float(solution.fun)-previous,
                    separator_seconds=coarea['seconds']),flush=True)
            weights=np.maximum(solution.x[:-1],0.);weights/=weights.sum()
            lower=float(solution.fun)
            if 0<=args.prox_level<1 and best['upper']-lower>args.tolerance:
                target=lower+args.prox_level*(best['upper']-lower)
                anchor=np.asarray(best['weights'])
                if hotstart:
                    prox=hotstart.prox(matrix,anchor,target)
                else:
                    identity=eye(len(atoms),format='csr')
                    zero=csr_matrix((len(matrix),len(atoms)))
                    prox_matrix=vstack((hstack((csr_matrix(matrix),zero)),
                        hstack((identity,-identity)),hstack((-identity,-identity))),format='csr')
                    prox=linprog(np.r_[np.zeros(len(atoms)),np.ones(len(atoms))],
                        A_ub=prox_matrix,b_ub=np.r_[np.full(len(matrix),target),anchor,-anchor],
                        A_eq=np.array([[1.]*len(atoms)+[0.]*len(atoms)]),b_eq=[1.],
                        bounds=[(0.,None)]*(2*len(atoms)),method='highs',
                        options={'primal_feasibility_tolerance':1e-9,'dual_feasibility_tolerance':1e-9})
                if not prox.success:raise RuntimeError('Proximal master: '+prox.message)
                weights=np.maximum(prox.x[:len(atoms)],0.);weights/=weights.sum()
            response=separator.call(operation='separate',weights=weights.tolist(),
                samples=args.face_samples,seed=9981+iteration,rational=args.rational_oracle)
            upper=float(response['value']);gap=upper-lower
            assert gap>=-2e-7,(lower,upper)
            entry=dict(iteration=iteration,master=lower,global_response=upper,gap=gap,
                rows=len(rows),positive_atoms=int((weights>1e-10).sum()),
                separator_seconds=response['seconds'],seconds=time.time()-started)
            history.append(entry);print('ROUND',json.dumps(entry),flush=True)
            if best is None or upper<best['upper']:
                best=dict(upper=upper,weights=weights.tolist(),iteration=iteration,
                    response_labels=response['responses'][0]['labels'])
            additional=[]
            # Convex stabilization changes no strategy class or oracle. Each
            # trial is a normalized actual monster law with a globalresponse.
            if upper>best['upper']+args.tolerance:
                anchor=np.asarray(best['weights'])
                direction=weights-anchor
                line_rows=np.vstack((matrix,np.asarray([item['row'] for item in response['responses']])))
                tested=[0.,1.]
                for step in range(args.line_search):
                    # Minimize the piecewise-affine response model on this
                    # segment, then globally separate that actual mixed law.
                    # A fixed midpoint can miss a narrow improving interval.
                    intercept=line_rows@anchor;slope=line_rows@direction
                    line=linprog([0.,1.],A_ub=np.c_[slope,-np.ones(len(line_rows))],
                        b_ub=-intercept,bounds=[(0.,1.),(None,None)],method='highs')
                    if not line.success:raise RuntimeError('Line master: '+line.message)
                    alpha=float(line.x[0])
                    if min(abs(alpha-a) for a in tested)<1e-10:break
                    tested.append(alpha)
                    trial=(1-alpha)*anchor+alpha*weights
                    probe=separator.call(operation='separate',weights=trial.tolist(),samples=0,seed=iteration,
                        rational=args.rational_oracle)
                    additional.extend(probe['responses'])
                    line_rows=np.vstack((line_rows,np.asarray([item['row'] for item in probe['responses']])))
                    if probe['value']<best['upper']:
                        best=dict(upper=float(probe['value']),weights=trial.tolist(),iteration=iteration,
                            response_labels=probe['responses'][0]['labels'])
            certified_gap=best['upper']-lower
            entry['best_upper']=best['upper'];entry['best_gap']=certified_gap
            dual=-np.asarray(solution.ineqlin.marginals)
            dual=np.maximum(dual,0.);dual/=dual.sum()
            payload=dict(scope='Floating global-cut optimization of the supplied finite monster bank. '
                'The princess response is unrestricted; the lower master covers only the bank. '
                'No unrestricted equilibrium or exact game-value claim.',
                complete=certified_gap<=args.tolerance,bank_size=len(atoms),
                master_value=lower,global_response=best['upper'],separation_gap=certified_gap,
                all_princess_oracle='Rationalgeometry lexicographic survival cut; floating capacities.',
                atoms=[encode_atom(a) for a in atoms],weights=best['weights'],
                current_master_weights=weights.tolist(),current_master_response=upper,
                best=best,query_v=separator.ready['v'],event_labels=separator.ready['event_labels'],
                princess_mixture=[dict(weight=float(p),labels=profiles[j]) for j,p in enumerate(dual) if p>1e-11],
                history=history,resume_source=args.resume,bank_source=bank_path.name,seconds=time.time()-started)
            output=directory/args.output
            output.write_text(json.dumps(payload,indent=2)+'\n')
            if iteration%25==0 or certified_gap<=args.tolerance:
                np.savez_compressed(pool_path,
                    rows=matrix,labels=np.asarray(profiles,dtype=np.int32),
                    query_v=np.asarray(separator.ready['v']))
            if certified_gap<=args.tolerance:
                closed=True;break
            added=sum(add(item) for item in response['responses']+additional)
            if args.uncross_every and iteration%args.uncross_every==0:
                active=[j for j,p in enumerate(dual) if p>1e-11]
                coarea=separator.call(operation='uncross',profiles=[profiles[j] for j in active],
                    weights=[float(dual[j]) for j in active],retain=-1)
                coarea_added=sum(add(item) for item in coarea['responses'])
                added+=coarea_added
                print('UNCR0SS',dict(components=coarea['components'],added=coarea_added,
                    minimum=coarea['minimum'],seconds=coarea['seconds']),flush=True)
            if not added:
                raise RuntimeError('Global separation gap persists but no new response profile was added')
        print('FINISHED',dict(support_game_closed=closed,best_upper=best['upper'],
                             seconds=time.time()-started,output=str(output)),flush=True)
    finally:
        separator.close()


if __name__=='__main__':
    main()
