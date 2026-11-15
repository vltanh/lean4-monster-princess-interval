#!/usr/bin/env python3
"""One finite LP for a whole atomic support against every princess path.

The LP is the order-polytope extension of the lexicographic survival cut.
Its mathematical reduction is exact for the supplied monster support;
SciPy's solution and the exported diagnostics use floating arithmetic.
No unrestricted all-monster lower guarantee is inferred from the LP value.
"""
from __future__ import annotations
import argparse
from collections import Counter
from fractions import Fraction as Q
import json
from pathlib import Path
import sys
import time

import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'packages/interval_turn_density'))
from atom_survival_cut import SurvivalCut, light_route


def bank(n=4):
    """A specified fixed grid bank, with explicit turn-side restrictions.

    M1 and M2 use all legal grid parameters. M3 has its second turn in
    the nonnegative half; I has its initial inward turn there. This is
    not an exhaustive enumeration of grid paths or monster strategies.
    """
    result, seen = [], set()
    def add(kind, values):
        atom = dict(kind=kind, parameters=tuple(Q(v, n) for v in values))
        route = light_route(atom)
        reflected = light_route(atom, True)
        # Trim after first completion of both endpoints; subsequent legs
        # cannot affect a princess capture time. Deduplicate reflected pairs.
        def trim(r):
            walls = set()
            out = []
            for u, v in r:
                out.append((u, v))
                if u-v in (-2, 2):
                    walls.add(u-v)
                if len(walls) == 2:
                    break
            return tuple(out)
        key = min(trim(route), trim(reflected))
        if key not in seen:
            seen.add(key)
            result.append(atom)
    for x in range(-n, n+1):
        add('M1', (x,))
    for x in range(-n, n+1):
        for s in range(x, 2*n-x+1):
            add('M2', (x, s))
    for x in range(-n, n+1):
        for s in range(x, 2*n-x+1):
            for t in range(max(-x, s-2*n), s+1):
                add('M3', (x, s, t))
    for z in range(0, n+1):
        for v in range(-z, z+1):
            for s in range(z, v+2*n+1):
                add('I', (z, v, s))
    return result


class Minimax:
    def __init__(self, atoms):
        self.model = SurvivalCut(atoms, lexicographic=True)
        self.atoms = atoms
        model = self.model
        nlevels = len(model.levels)
        self.threshold_count = len(model.v) * (nlevels-1)
        self.node = lambda i, k: i*(nlevels-1)+k-1
        auxiliary = {}
        edges = set()
        self.rows = []
        self.constants = []
        for i in range(len(atoms)):
            row = {}
            constant = Q(0)
            for (positive, bits), coefficient in model.unit_rewards(i).items():
                coefficient /= 4
                if not bits:
                    constant += coefficient
                    continue
                if len(bits) == 1:
                    j = self.node(*bits[0])
                else:
                    key = positive, bits
                    if key not in auxiliary:
                        j = self.threshold_count + len(auxiliary)
                        auxiliary[key] = j
                        if positive:
                            edges.update((j, self.node(*bit)) for bit in bits)
                        else:
                            edges.update((self.node(*bit), j) for bit in bits)
                    j = auxiliary[key]
                if not positive:
                    constant += coefficient
                row[j] = row.get(j, Q(0)) + (coefficient if positive else -coefficient)
            self.rows.append({j:c for j,c in row.items() if c})
            self.constants.append(constant)
        self.variable_count = self.threshold_count + len(auxiliary)
        self.auxiliary = auxiliary
        for i in range(len(model.v)):
            edges.update((self.node(i,k), self.node(i,k-1)) for k in range(2,nlevels))
        for i in range(len(model.v)-1):
            edges.update((self.node(i,k), self.node(i+1,k)) for k in range(1,nlevels))
        self.edges = sorted(edges)
        self.bounds = [(0.,1.)] * self.variable_count
        for i,(lo,hi) in enumerate(model.bounds):
            for k in range(1,nlevels):
                if k <= lo:
                    self.bounds[self.node(i,k)] = (1.,1.)
                elif k > hi:
                    self.bounds[self.node(i,k)] = (0.,0.)

    def solve(self, time_limit=600., method='highs'):
        ri, ci, vv = [], [], []
        count = len(self.atoms)
        for i,row in enumerate(self.rows):
            ri.append(i); ci.append(self.variable_count); vv.append(1.)
            for j,c in row.items():
                ri.append(i); ci.append(j); vv.append(-float(c))
        for i,(u,v) in enumerate(self.edges, count):
            ri.extend((i,i)); ci.extend((u,v)); vv.extend((1.,-1.))
        matrix = coo_matrix((vv,(ri,ci)), shape=(count+len(self.edges),self.variable_count+1)).tocsr()
        rhs = np.r_[list(map(float,self.constants)),np.zeros(len(self.edges))]
        objective = np.r_[np.zeros(self.variable_count),-1.]
        answer = linprog(objective,A_ub=matrix,b_ub=rhs,bounds=self.bounds+[(None,None)],
                         method=method,options={'primal_feasibility_tolerance':1e-9,
                         'dual_feasibility_tolerance':1e-9,'time_limit':time_limit})
        if not answer.success:
            raise RuntimeError(answer.message)
        z, value = answer.x[:-1], answer.x[-1]
        weights = -answer.ineqlin.marginals[:count]
        payoff = np.array([float(c)+sum(float(a)*z[j] for j,a in row.items())
                           for c,row in zip(self.constants,self.rows)])
        assert min(payoff) >= value-1e-7
        assert abs(weights.sum()-1.) < 1e-7 and weights.min() >= -1e-7
        return value, z, weights, payoff, answer

    def decomposition(self, z, tolerance=2e-8):
        """A finite mixed query response for this fractional point.

        Only threshold coordinates are needed. Auxiliaries can be completed
        pointwise to the true conjunction values, increasing all payoffs.
        Clustering is solely a floating-output convenience, not a proof step.
        """
        probabilities = np.clip(z[:self.threshold_count],0,1)
        levels = [0.]
        for p in sorted(probabilities):
            if p-levels[-1] > tolerance:
                levels.append(float(p))
        if 1.-levels[-1] <= tolerance:
            levels[-1] = 1.
        else:
            levels.append(1.)
        result = []
        model = self.model
        for a,b in zip(levels,levels[1:]):
            if b-a <= tolerance:
                continue
            threshold = (a+b)/2
            labels = tuple(int(sum(probabilities[self.node(i,k)] >= threshold
                               for k in range(1,len(model.levels))))
                           for i in range(len(model.v)))
            assert all(lo <= labels[i] <= hi for i,(lo,hi) in enumerate(model.bounds))
            assert all(a <= b for a,b in zip(labels,labels[1:]))
            values = tuple(model.levels[k] for k in labels)
            result.append(dict(weight=b-a, labels=labels, values=values))
        assert abs(sum(item['weight'] for item in result)-1.) < 1e-7
        return result


def encode_atom(atom):
    return dict(kind=atom['kind'], parameters=list(map(str,atom['parameters'])))


def compact_payload(payload):
    """Keep proof/reconstruction inputs; drop regenerable debug vectors."""
    result=dict(payload)
    result['debug_vectors_omitted']=[key for key in
        ('order_variables','optimal_face','lp_payoffs') if key in result]
    for key in result['debug_vectors_omitted']:
        result.pop(key)
    return result


def append_field_atoms(atoms):
    """Use the existing field's named active routes, with legal rational data.

    Structural multipliers are discarded; all probabilities are solved anew.
    Center-wait and arbitrary external routes are omitted explicitly because
    they are outside the current named atom parser.
    """
    source=ROOT/'packages/interval_cdf_discovery/snapshots/initial_inward_duals.json'
    data=json.loads(source.read_text())
    keys={(a['kind'],tuple(a['parameters'])) for a in atoms}
    omitted=Counter()
    count=0
    rational=lambda x:Q(str(x)).limit_denominator(2**24)
    for row in data['routes']:
        label=row['label'];kind=label['kind']
        if kind=='M1':
            parameters=(rational(label['start']),)
        elif kind=='M2':
            parameters=tuple(rational(label[k]) for k in ('start','turn'))
        elif kind=='M3':
            parameters=tuple(rational(label[k]) for k in ('start','first_turn','second_turn'))
        elif kind=='initial_inward':
            kind='I'
            parameters=tuple(rational(label[k]) for k in ('start','first_v','second_u'))
        else:
            omitted[kind]+=1
            continue
        if (kind,parameters) not in keys:
            atom=dict(kind=kind,parameters=parameters)
            # Build and verify the exact unit legs before using the data.
            route=light_route(atom)
            assert route[0][0]+route[0][1]==0
            assert all(-2<=u-v<=2 for u,v in route)
            assert {-2,2}<={u-v for u,v in route}
            atoms.append(atom);keys.add((kind,parameters));count+=1
    return dict(source=str(source.relative_to(ROOT)),added=count,omitted=dict(omitted),
                note='Old cost/structural multipliers are not reused as probabilities.')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--grid',type=int,default=4)
    parser.add_argument('--output',default='global_minimax_grid4.json')
    parser.add_argument('--archived-upper',action='store_true',
                        help='Include all 67 pairs of the existing certified upper law.')
    parser.add_argument('--field-support',action='store_true',
                        help='Include named active routes from the existing initial-inward CDF fit.')
    parser.add_argument('--skip-cut',action='store_true')
    parser.add_argument('--time-limit',type=float,default=600.,
                        help='Wall-clock cap in seconds for the single floating LP solve.')
    parser.add_argument('--method',choices=('highs','highs-ds','highs-ipm'),default='highs')
    parser.add_argument('--full-output',action='store_true',
                        help='Retain regenerable order variables and residual-face debug vectors.')
    args = parser.parse_args()
    started = time.time()
    atoms = bank(args.grid)
    if args.archived_upper:
        archived=json.loads((ROOT/'packages/interval_refined_upper/strategy.json').read_text())
        keys={(a['kind'],tuple(a['parameters'])) for a in atoms}
        for item in archived['families']:
            kind='M'+str(item['kind'])
            parameters=(Q(item['start']),) if item['kind']==1 else (Q(item['start']),Q(1))
            if (kind,parameters) not in keys:
                atoms.append(dict(kind=kind,parameters=parameters))
                keys.add((kind,parameters))
    field_support=append_field_atoms(atoms) if args.field_support else None
    problem = Minimax(atoms)
    print('MODEL',dict(atoms=len(atoms),kinds=dict(Counter(a['kind'] for a in atoms)),
          queries=len(problem.model.v),labels=len(problem.model.levels),
          variables=problem.variable_count,implications=len(problem.edges)),flush=True)
    value,z,weights,payoff,answer = problem.solve(time_limit=args.time_limit,method=args.method)
    print('LP_SOLVED',dict(value=float(value),seconds=time.time()-started),flush=True)
    decomposition = problem.decomposition(z)
    physical_rows = np.array([list(map(float,problem.model.row(atoms,row['values'])))
                              for row in decomposition])
    physical_payoff = np.array([row['weight'] for row in decomposition]) @ physical_rows
    active = np.flatnonzero(weights > 1e-8)
    upper = None
    face = None
    if not args.skip_cut:
        # Use the same full geometry: zero weights remain legal, so the cut
        # independently checks the complete fractional LP's upper dual.
        cut = problem.model.solve(weights,tolerance=1e-10,retain_face=args.full_output)
        upper,face = float(cut.value),cut.face
        assert abs(upper-value) < 2e-6,(upper,value)
    out = dict(scope='Global princess minimax for this fixed finite monster bank; '
          'floating optimization, not an unrestricted all-monster lower certificate.',
          grid=args.grid,include_archived_upper=args.archived_upper,value=float(value),cut_upper=upper,
          field_support=field_support,
          method=args.method,lp_time_limit=args.time_limit,
          model_size=dict(atoms=len(atoms),queries=len(problem.model.v),
              labels=len(problem.model.levels),variables=problem.variable_count,
              implications=len(problem.edges)),
          atoms=[encode_atom(a) for a in atoms],weights=weights.tolist(),
          active_atoms=[dict(index=int(i),**encode_atom(atoms[i]),weight=float(weights[i]),
                       payoff=float(physical_payoff[i])) for i in active],
          query_v=list(map(str,problem.model.v)),
          event_labels=[[str(q),side] for q,side in problem.model.levels],
          princess_mixture=[dict(weight=row['weight'],labels=row['labels']) for row in decomposition],
          princess_payoffs=physical_payoff.tolist(),
          order_variables=z.tolist(),lp_payoffs=payoff.tolist(),
          dual_atom_marginals=answer.ineqlin.marginals[:len(atoms)].tolist(),
          optimal_face=face,seconds=time.time()-started,
          stopping_rule='One fixed support, one global finite minimax LP, then omitted-monster attacks; no mesh refinement.')
    if not args.full_output:
        out=compact_payload(out)
    path=Path(args.output)
    if not path.is_absolute():
        path=Path(__file__).parent/path
    path.write_text(json.dumps(out,indent=2)+'\n')
    print('RESULT',dict(value=value,cut_upper=upper,active_monster_pairs=len(active),
          princess_components=len(decomposition),minimum_bank_payoff=float(physical_payoff.min()),
          seconds=time.time()-started),flush=True)
    print('ACTIVE',out['active_atoms'],flush=True)
    print('OUTPUT',path,flush=True)


if __name__=='__main__':
    main()
