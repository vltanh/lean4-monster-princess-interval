#!/usr/bin/env python3
"""Sparse numerical master with exact integer normalized-bank dual pricing.

The LP is discovery only. Each saved lower is obtained by pricing a repaired
integer isotone profile exhaustively, then subtracting the proved grid error.
It is a bound on the game value, not a security claim for an extracted CDF.
"""
from __future__ import annotations
import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import struct
import subprocess
import time

import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix, csr_matrix, hstack, vstack

HERE = Path(__file__).resolve().parent


class Master:
    def __init__(self, n: int, directory: Path, denominator: int = 10**9,
                 normalized_profile: bool = True):
        self.n, self.R, self.C, self.H = n, 2*n, 4*n, 12*n
        self.directory, self.D = directory, denominator
        self.directory.mkdir(parents=True, exist_ok=True)
        self.normalized_profile = normalized_profile
        self.profile_horizon = self.C if normalized_profile else self.H
        self.nodes = [(j,k) for j in range(self.profile_horizon+1)
                      for k in range(1,self.R+1) if (j+k)%2 == 0]
        self.index = {p:i for i,p in enumerate(self.nodes)}
        self.K = len(self.nodes)
        self.order = [(i,self.index[j+s,k+1]) for i,(j,k) in enumerate(self.nodes)
                      for s in (-1,1) if k < self.R and 0 <= j+s <= self.profile_horizon]
        if normalized_profile:
            # First-endpoint stopping makes the strict positive endpoint trace
            # nonincreasing. Outward2 extends every later interior node from t=2.
            self.order += [(self.index[j+2,self.R],self.index[j,self.R])
                           for j in range(0,self.C,2)]
        row = np.repeat(np.arange(len(self.order)),2)
        col = np.asarray(self.order,dtype=int).reshape(-1)
        val = np.tile([1.,-1.],len(self.order))
        self.order_matrix = coo_matrix((val,(row,col)),shape=(len(self.order),self.K+1)).tocsr()
        self.columns, self.seen = [], set()
        self.binary = self.directory/'pricing.input.bin'
        self.executable = HERE/'price_normalized'
        source = HERE/'price_normalized.cpp'
        if not self.executable.exists() or self.executable.stat().st_mtime < source.stat().st_mtime:
            subprocess.run(['g++','-O3','-std=c++17',str(source),'-o',str(self.executable)],check=True)

    def variable(self,j,k):
        if self.normalized_profile and j>self.C:
            k-=j-self.C;j=self.C
            if k<=0:
                return None
        return self.index[j,k]

    def repair(self, values):
        """Floor bounded values, then take exact finite order closure."""
        table = np.zeros((self.H+1,self.R+1),dtype=np.uint64)
        rounded=np.asarray([min(self.D,max(0,int(np.floor(float(v)*self.D))))
                            for v in values],dtype=np.uint64)
        # The order graph is acyclic: cone arcs increase radius; endpoint
        # stopping arcs stay at maximum radius and decrease time.
        for k in range(1,self.R+1):
            for j in range(k%2,self.profile_horizon+1,2):
                a=self.index[j,k]
                if k>1:
                    for s in (-1,1):
                        if 0<=j+s<=self.profile_horizon:
                            rounded[a]=max(rounded[a],rounded[self.index[j+s,k-1]])
        if self.normalized_profile:
            for j in range(self.C-2,-1,-2):
                rounded[self.index[j,self.R]]=max(rounded[self.index[j,self.R]],
                                                 rounded[self.index[j+2,self.R]])
        for j in range(self.H+1):
            for k in range(1,self.R+1):
                if (j+k)%2==0:
                    a=self.variable(j,k)
                    if a is not None:
                        table[j,k]=rounded[a]
        return table

    def price(self, values, keep=48):
        table = self.repair(values)
        self.binary.write_bytes(struct.pack('<IIQ',1,self.n,self.D)+table.astype('<u8').tobytes())
        done = subprocess.run([str(self.executable),str(self.binary),str(keep)],
                              check=True,text=True,stdout=subprocess.PIPE)
        answer = json.loads(done.stdout)
        return answer,table

    def profile_values(self,table):
        return np.asarray([int(table[j,k])/self.D for j,k in self.nodes])

    def calendar(self, path, table, latest=False):
        positions = [path['start_grid']]
        for step in path['moves']:
            assert step in (-1,1)
            positions.append(positions[-1]+step)
        assert all(abs(k)<=self.R for k in positions)
        assert 0 in positions[:self.C+1]
        assert -self.R in positions and self.R in positions
        result = {'start_grid':positions[0],'moves':path['moves']}
        coeff = {}; mass = 0
        for name,sign,endpoint in [('minus_charges',1,-self.R),('plus_charges',-1,self.R)]:
            end = positions.index(endpoint); counts = {}; minimum = 2*self.D+1; when = None
            for j in range(end):
                k = sign*positions[j]
                q = self.D + (1 if k>=0 else -1)*int(table[j,abs(k)])
                if q<minimum or latest and q==minimum:
                    minimum,when = q,j
                counts[when] = counts.get(when,0)+1
            result[name] = list(map(list,sorted(counts.items())))
            mass += end
            for j,a in counts.items():
                k = sign*positions[j]
                if k:
                    i = self.variable(j,abs(k))
                    if i is not None:
                        coeff[i] = coeff.get(i,0)+(a if k>0 else -a)
        return result,mass,{k:v for k,v in coeff.items() if v}

    def add(self, path, table):
        added=0
        for latest in (False,True):
            plan,mass,coeff = self.calendar(path,table,latest)
            key = mass,tuple(sorted(coeff.items()))
            if key not in self.seen:
                self.seen.add(key)
                self.columns.append({'plan':plan,'mass':mass,'coeff':coeff})
                added+=1
        return added

    def add_plan(self,plan):
        positions=[plan['start_grid']]
        for step in plan['moves']:
            positions.append(positions[-1]+step)
        mass=0;coeff={}
        for name,sign in [('minus_charges',1),('plus_charges',-1)]:
            for j,a in plan[name]:
                mass+=a;k=sign*positions[j]
                if k:
                    i=self.variable(j,abs(k))
                    if i is not None:
                        coeff[i]=coeff.get(i,0)+(a if k>0 else -a)
        coeff={k:v for k,v in coeff.items() if v}
        key=mass,tuple(sorted(coeff.items()))
        if key in self.seen:
            return False
        self.seen.add(key);self.columns.append({'plan':plan,'mass':mass,'coeff':coeff})
        return True

    def interpolate_seed(self,seed):
        """Numerical common-threshold interpolation; integer pricing certifies it."""
        coarse=seed['n'];den=int(seed['field_denominator'])
        values={(j,k):int(a)/den for j,k,a in seed['radial_nodes']}
        def node(j,k):
            if k==0:
                return 0.
            if j>=6*coarse:
                return 0.
            return (1 if k>0 else -1)*values[j,abs(k)]
        def coordinate(z):
            cell=int(np.floor(z));alpha=z-cell
            if alpha<1e-12:
                alpha=0.
            elif alpha>1-1e-12:
                cell+=1;alpha=0.
            plus=cell%(2*coarse)<coarse
            return cell,alpha,plus,alpha if plus else 1-alpha
        answer=[]
        for j,k in self.nodes:
            u=coordinate(coarse*(j+k)/(2*self.n))
            w=coordinate(coarse*(j-k)/(2*self.n))
            cuts=sorted(set([0.,1.,u[3],w[3]]));v=0.
            for left,right in zip(cuts,cuts[1:]):
                if right-left<1e-14:
                    continue
                z=(left+right)/2
                def rnd(c):
                    cell,a,plus,_=c
                    return cell+int(a>0 and (z<a if plus else z>1-a))
                U,W=rnd(u),rnd(w)
                v+=(right-left)*node(U+W,U-W)
            answer.append(v)
        return np.asarray(answer)

    def solve_lp(self,anchor=None,level_lower=None):
        rr=[];cc=[];vv=[];rhs=[];scale=4*self.n
        for row,column in enumerate(self.columns):
            rr.append(row);cc.append(self.K);vv.append(1.)
            for i,a in column['coeff'].items():
                rr.append(row);cc.append(i);vv.append(-a/scale)
            rhs.append(column['mass']/scale)
        cuts = coo_matrix((vv,(rr,cc)),shape=(len(self.columns),self.K+1)).tocsr()
        matrix = vstack([self.order_matrix,cuts],format='csr')
        b = np.r_[np.zeros(len(self.order)),rhs]
        objective=np.zeros(self.K+1);objective[-1]=-1
        result=linprog(objective,A_ub=matrix,b_ub=b,
                       bounds=[(0.,1.)]*self.K+[(0.,2.)],method='highs-ds',
                       options={'time_limit':120.,'primal_feasibility_tolerance':1e-9,
                                'dual_feasibility_tolerance':1e-9})
        if not result.success:
            raise RuntimeError(result.message)
        weights=-result.ineqlin.marginals[len(self.order):]
        trial=result.x[:-1]
        if anchor is not None and level_lower is not None and -result.fun>level_lower+1e-9:
            level=level_lower+.5*(-result.fun-level_lower)
            matrix_g=matrix[:,:self.K]
            rhs=b-matrix[:,self.K].toarray().ravel()*level
            eye=coo_matrix((np.ones(self.K),(np.arange(self.K),np.arange(self.K))),
                          shape=(self.K,self.K)).tocsr()
            prox_matrix=vstack([hstack([matrix_g,csr_matrix((matrix_g.shape[0],self.K))]),
                                hstack([eye,-eye]),hstack([-eye,-eye])],format='csr')
            prox=linprog(np.r_[np.zeros(self.K),np.ones(self.K)],A_ub=prox_matrix,
                         b_ub=np.r_[rhs,anchor,-anchor],
                         bounds=[(0.,1.)]*self.K+[(0.,None)]*self.K,method='highs-ds',
                         options={'time_limit':120.,'primal_feasibility_tolerance':1e-9,
                                  'dual_feasibility_tolerance':1e-9})
            if prox.success:
                trial=prox.x[:self.K]
        return result,weights,trial

    def save(self, output, table, answer, lp, weights, history):
        if answer.get('status')!='PASS' or answer.get('certifies_lower') is False:
            raise ValueError('only complete exact pricing can certify a saved dual')
        units=int(answer['minimum_units']);den=4*self.n*self.D
        lower=Fraction(units-2*self.D,den)
        certificate={'scope':'Exact integer feasible dual on the normalized physical grid bank. The global game-value lower subtracts 1/(2n); no claim of Princess security for this nodal profile.',
                     'n':self.n,'field_denominator':str(self.D),
                     'normalized_profile':self.normalized_profile,
                     'radial_nodes':[[j,k,str(int(table[j,k]))] for j in range(self.H+1)
                                     for k in range(1,self.R+1) if (j+k)%2==0],
                     'minimum_units':str(units),'objective_denominator':str(den),
                     'normalized_bank_dual_value':str(Fraction(units,den)),
                     'global_lower':str(lower),'global_lower_decimal':float(lower),
                     'pricing':answer,'native_source_sha256':hashlib.sha256((HERE/'price_normalized.cpp').read_bytes()).hexdigest()}
        dual_path=output.with_suffix('.dual.json');dual_tmp=dual_path.with_suffix('.json.tmp')
        dual_tmp.write_text(json.dumps(certificate,indent=2 if self.n<=16 else None,
                                       separators=None if self.n<=16 else (',',':'))+'\n')
        dual_tmp.replace(dual_path)
        checkpoint={'scope':'Floating sparse-master discovery; upper and weights require separate exact replay.',
                    'n':self.n,'profile_grid':getattr(self,'profile_grid',self.n),
                    'normalized_profile':self.normalized_profile,
                    'profile':lp.x[:-1].tolist(),'upper':float(-lp.fun),
                    'columns':self.columns,'weights':weights.tolist(),'history':history}
        # Integer keys are restored explicitly on restart.
        checkpoint_path=output.with_suffix('.checkpoint.json')
        checkpoint_tmp=checkpoint_path.with_suffix('.json.tmp')
        checkpoint_tmp.write_text(json.dumps(checkpoint,separators=(',',':'))+'\n')
        checkpoint_tmp.replace(checkpoint_path)


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('n',type=int)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--iterations',type=int,default=200)
    parser.add_argument('--denominator',type=int,default=10**9)
    parser.add_argument('--profile-grid',type=int,
                        help='optimize a coarser full-width interpolated field on the fine physical grid')
    parser.add_argument('--restart',action='store_true')
    parser.add_argument('--unrestricted-profile',action='store_true')
    parser.add_argument('--seed',type=Path)
    parser.add_argument('--profile-seed',type=Path)
    parser.add_argument('--plain',action='store_true')
    parser.add_argument('--fresh-lp',action='store_true',
                        help='rebuild SciPy LPs instead of retaining HiGHS bases')
    parser.add_argument('--no-cached-separation',action='store_true',
                        help='run the complete oracle at every LP iteration')
    parser.add_argument('--pricing-paths',type=int,default=48,
                        help='number of physical witnesses requested from complete pricing')
    parser.add_argument('--tolerance',type=float,default=2e-8)
    args=parser.parse_args();began=time.monotonic()
    if args.pricing_paths<1:
        raise ValueError('discovery requires at least one full-oracle witness')
    directory=args.output.parent/(args.output.stem+'.work')
    if args.profile_grid and args.profile_grid!=args.n:
        if args.unrestricted_profile:
            raise ValueError('interpolated profiles require outward normalization')
        from interpolated_master import InterpolatedMaster
        master=InterpolatedMaster(args.n,args.profile_grid,directory,args.denominator)
    else:
        master=Master(args.n,directory,args.denominator,not args.unrestricted_profile)
    history=[]
    best_value=-1.;best_answer=best_table=anchor=None
    old=args.output.with_suffix('.checkpoint.json')
    if args.restart and old.exists():
        saved=json.loads(old.read_text());assert saved['n']==args.n
        assert saved.get('normalized_profile',False)==master.normalized_profile
        assert saved.get('profile_grid',args.n)==getattr(master,'profile_grid',args.n)
        for column in saved['columns']:
            column['coeff']={int(k):v for k,v in column['coeff'].items()}
            master.columns.append(column);master.seen.add((column['mass'],tuple(sorted(column['coeff'].items()))))
        history=saved['history']
        dual_file=args.output.with_suffix('.dual.json')
        if dual_file.exists():
            dual=json.loads(dual_file.read_text())
            assert dual['n']==args.n and int(dual['field_denominator'])==master.D
            lookup={(j,k):int(a) for j,k,a in dual['radial_nodes']}
            best_table=np.zeros((master.H+1,master.R+1),dtype=np.uint64)
            for (j,k),a in lookup.items():best_table[j,k]=a
            anchor=master.profile_values(best_table)
            best_table=master.repair(anchor)
            # Reusing saved feasible values is safe only if quantization did
            # not alter the exact integer field. Otherwise reprice it.
            if all(int(best_table[j,k])==a for (j,k),a in lookup.items()):
                best_answer=dual['pricing']
            else:
                best_answer,best_table=master.price(anchor,keep=0)
            best_value=int(best_answer['minimum_units'])/(4*args.n*master.D)
    else:
        table=master.repair(np.zeros(master.K))
        master.add({'start_grid':master.R,'moves':[-1]*(2*master.R)},table)
        master.add({'start_grid':0,'moves':[1]*args.n+[-1]*(3*args.n)+[1]*(4*args.n)},table)
    seed=None
    if args.seed:
        seed=json.loads(args.seed.read_text());coarse=seed['n'];ratio=args.n//coarse
        assert ratio>=1 and ratio*coarse==args.n
        plans=seed.get('paths')
        if plans is None:
            plans=[column['plan'] for column,w in zip(seed['columns'],seed['weights']) if w>1e-10]
        for plan in plans:
            scaled={'start_grid':plan['start_grid']*ratio,
                    'moves':[step for step in plan['moves'] for _ in range(ratio)],
                    'minus_charges':[[j*ratio,a*ratio] for j,a in plan['minus_charges']],
                    'plus_charges':[[j*ratio,a*ratio] for j,a in plan['plus_charges']]}
            master.add_plan(scaled)
    if args.profile_seed:
        trial=master.interpolate_seed(json.loads(args.profile_seed.read_text()))
        # The seed only needs a complete value certificate. Keep no ancestor
        # histories: cached seed routes supply the first separation witnesses.
        best_answer,best_table=master.price(trial,keep=0)
        best_value=int(best_answer['minimum_units'])/(4*args.n*master.D)
        anchor=master.profile_values(best_table)
        for path in best_answer['paths']:
            master.add(path,best_table)
        print(json.dumps({'event':'profile_seed','bank_dual':best_value,
                          'global_lower':best_value-1/(2*args.n)}),flush=True)
    cache=None
    if not args.no_cached_separation:
        from cached_path_pricing import CachedPathPricing
        cache=CachedPathPricing(master.n,master.D)
        cache.update_columns(master.columns)
        if seed is not None:
            cache.add_many(seed.get('paths',[c['plan'] for c in seed.get('columns',[])]),
                           source_n=seed['n'])
    backend=master
    if not args.fresh_lp:
        try:
            from persistent_highs import PersistentMaster
            backend=PersistentMaster(master)
        except ImportError:
            print(json.dumps({'event':'lp_backend','method':'fresh SciPy fallback'}),flush=True)
    force_main=False
    for iteration in range(args.iterations):
        use_prox=not args.plain and not force_main and anchor is not None
        force_main=False
        previous_best=best_value
        lp,weights,trial=backend.solve_lp(anchor if use_prox else None,
                                        None if best_value<0 else best_value)
        if cache is not None and best_answer is not None:
            cache.update_columns(master.columns)
            table=master.repair(trial)
            level=best_value+.5*(-lp.fun-best_value) if use_prox else -lp.fun
            cached=cache.price(table,keep=args.pricing_paths,level=level)
            additions=[];addition_keys=set()
            for path in cached['violating_paths']:
                for latest in (False,True):
                    plan,mass,coeff=master.calendar(path,table,latest)
                    key=mass,tuple(sorted(coeff.items()))
                    if key not in master.seen and key not in addition_keys:
                        addition_keys.add(key)
                        additions.append((key,{'plan':plan,'mass':mass,'coeff':coeff}))
            if additions:
                # A known response only bounds the dual minimum from above.
                # Preserve the previous fully certified field and its value.
                report={'iteration':len(history),'n':args.n,'variables':master.K,
                        'columns':len(master.columns),
                        'restricted_master_upper':float(-lp.fun),
                        'pricing_scope':'cached physical witnesses only',
                        'cached_path_upper':int(cached['cached_minimum_units'])/(4*args.n*master.D),
                        'cached_paths':len(cache),'new_calendars':len(additions),
                        'best_exact_dual':best_value,'global_lower':best_value-1/(2*args.n),
                        'gap':float(-lp.fun)-best_value,'seconds':time.monotonic()-began}
                if hasattr(backend,'last_stats'):
                    report['lp_stats']=backend.last_stats
                history.append(report)
                master.save(args.output,best_table,best_answer,lp,weights,history)
                print(json.dumps(report),flush=True)
                for key,column in additions:
                    master.seen.add(key);master.columns.append(column)
                continue
        answer,table=master.price(trial,keep=args.pricing_paths)
        if cache is not None:
            cache.add_many(answer['paths'])
        priced=int(answer['minimum_units'])/(4*args.n*master.D)
        if priced>best_value:
            best_value,best_answer,best_table=priced,answer,table
            anchor=master.profile_values(table)
        report={'iteration':len(history),'n':args.n,'variables':master.K,
                'columns':len(master.columns),'restricted_master_upper':float(-lp.fun),
                'pricing_scope':'complete exact normalized bank',
                'exact_normalized_dual':priced,'best_exact_dual':best_value,
                'global_lower':best_value-1/(2*args.n),
                'gap':float(-lp.fun)-best_value,'record_states':answer['retained_states'],
                'max_layer':answer['maximum_layer'],'seconds':time.monotonic()-began}
        if hasattr(backend,'last_stats'):
            report['lp_stats']=backend.last_stats
        history.append(report)
        master.save(args.output,best_table,best_answer,lp,weights,history)
        print(json.dumps(report),flush=True)
        if report['gap']<=args.tolerance:
            break
        added=sum(master.add(path,table) for path in answer['paths'])
        if not added:
            # A globally feasible bundle-level point need not expose a new
            # calendar: it can still strictly improve the exact lower. Raise
            # the next level, or use the main optimizer to leave a flat prox.
            if best_value>previous_best+5e-12:
                continue
            if use_prox:
                force_main=True
                continue
            raise RuntimeError('pricing stalled; no new exact calendar column')


if __name__=='__main__':
    main()
