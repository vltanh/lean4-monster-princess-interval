#!/usr/bin/env python3
"""Trust-box interior-point discovery with complete normalized-bank acceptance.

This optimizes the Princess field, not a finite Princess path mixture. Cached
physical routes separate newly exposed causal calendars; they never certify
a lower. Only the existing complete integer oracle can update best.dual.json.
The 1/(2n) transfer is still subtracted without modification.
"""
from __future__ import annotations

import argparse
from fractions import Fraction
import base64
import gzip
import hashlib
import json
from pathlib import Path
import platform
import sys
import time
import zlib

import numpy as np
from scipy.sparse import coo_matrix
from scipy.optimize import OptimizeResult

ROOT = Path(__file__).resolve().parents[2]
NATIVE = ROOT/'packages/interval_clock_grid/normalized_native'
sys.path[:0] = [str(NATIVE), str(ROOT/'packages/interval_discovery')]
from solve_normalized import Master
from interpolated_master import InterpolatedMaster
from cached_path_pricing import CachedPathPricing, normalize_path
from persistent_highs import PersistentMaster, SolveError, _check
from princess_search import full_seed, read_json
from verify_native_field import load_table


def write_json(path, data):
    path = Path(path)
    raw = (json.dumps(data, separators=(',', ':'))+'\n').encode()
    if path.suffix == '.gz':
        raw = gzip.compress(raw, compresslevel=6, mtime=0)
    temp = path.with_suffix(path.suffix+'.tmp')
    temp.write_bytes(raw)
    temp.replace(path)


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def save_priced_trial(path, master, table, answer):
    """Compact exact bytes and witnesses, including failed serious steps."""
    if master.D >= 2**32:
        raise ValueError('compact trial encoding requires denominator below 2**32')
    before_two = np.asarray([table[j,k] for j in range(master.C+1)
                            for k in range(1,master.R+1) if (j+k)%2 == 0], dtype='<u4').tobytes()
    den = 4*master.n*master.D
    units = int(answer['minimum_units'])
    write_json(path, {
        'format':'qout-clock-grid-field-u32-zlib-v1', 'n':master.n,
        'field_denominator':str(master.D), 'normalized_profile':True,
        'encoding':{'count':(master.C+1)*master.n,
                    'integer_type':'uint32 little-endian','compression':'zlib',
                    'uncompressed_sha256':hashlib.sha256(before_two).hexdigest()},
        'pre_two_values_base64':base64.b64encode(zlib.compress(before_two,9)).decode(),
        'scope':'Completely priced discovery trial; may be weaker than retained best. The same-CDF continuum security is not claimed.',
        'minimum_units':str(units), 'objective_denominator':str(den),
        'normalized_bank_dual_value':str(Fraction(units,den)),
        'global_lower':str(Fraction(units-2*master.D,den)),
        'pricing':answer,
        'native_source_sha256':sha256(NATIVE/'price_normalized.cpp')})


class ContractedMaster(Master):
    """Keep the seed's exact tight cone components equal during discovery.

    This is an explicitly restricted CDF family, not an optimality theorem.
    It includes the exact seed and substantially reduces finer-grid models.
    Every lifted candidate is independently repaired and completely priced.
    """
    def __init__(self, base, seed_values):
        self.base = base
        for name in ('n', 'R', 'C', 'H', 'D', 'directory', 'normalized_profile',
                     'profile_horizon', 'binary', 'executable'):
            setattr(self, name, getattr(base, name))
        self.profile_grid = getattr(base, 'profile_grid', base.n)
        self.coarse_denominator = getattr(base, 'coarse', base).D
        seed = base.profile_values(base.repair(seed_values))
        integers = np.rint(seed*self.coarse_denominator).astype(np.int64)
        parent = list(range(base.K))
        def find(i):
            while parent[i] != i:
                parent[i] = parent[parent[i]]
                i = parent[i]
            return i
        for u,v in base.order:
            if integers[u] == integers[v]:
                u,v = find(u),find(v)
                if u != v:
                    parent[u] = v
        roots = [find(i) for i in range(base.K)]
        unique = sorted(set(roots), key=lambda i: (int(integers[i]), i))
        indices = {root: j for j,root in enumerate(unique)}
        self.labels = np.asarray([indices[root] for root in roots], dtype=np.int32)
        self.representatives = np.asarray(unique, dtype=np.int32)
        self.K = len(unique)
        self.nodes = [base.nodes[i] for i in unique]
        self.order = sorted({(int(self.labels[u]), int(self.labels[v]))
                             for u,v in base.order if self.labels[u] != self.labels[v]})
        # All surviving edges have strictly increasing original seed values,
        # so this component numbering is an exact topological order.
        if any(u >= v for u,v in self.order):
            raise AssertionError('tight-component contraction is not acyclic')
        self.predecessors = [[] for _ in range(self.K)]
        for u,v in self.order:
            self.predecessors[v].append(u)
        row = np.repeat(np.arange(len(self.order)), 2)
        col = np.asarray(self.order, dtype=int).reshape(-1)
        val = np.tile([1., -1.], len(self.order))
        self.order_matrix = coo_matrix((val, (row, col)),
                                      shape=(len(self.order), self.K+1)).tocsr()
        self.columns, self.seen = [], set()

    def repair(self, values):
        D = self.coarse_denominator
        rounded = [min(D, max(0, int(np.floor(float(x)*D)))) for x in values]
        for v in range(self.K):
            for u in self.predecessors[v]:
                rounded[v] = max(rounded[v], rounded[u])
        # A positive sub-unit guard preserves these exact integer values
        # through the inherited floating-to-integer input conversion.
        expanded = np.minimum(1., (np.asarray(rounded, dtype=float)[self.labels]+.25)/D)
        return self.base.repair(expanded)

    def profile_values(self, table):
        values = self.base.profile_values(table)
        selected = values[self.representatives]
        if np.max(np.abs(values-selected[self.labels])) > 1e-12:
            raise AssertionError('field left the frozen component family')
        return selected

    def interpolate_seed(self, seed):
        return self.base.interpolate_seed(seed)[self.representatives]

    def _aggregate(self, coeff):
        result = {}
        for i,a in coeff.items():
            j = int(self.labels[int(i)])
            result[j] = result.get(j, 0)+a
        return {j:a for j,a in result.items() if a}

    def calendar(self, path, table, latest=False):
        plan,mass,coeff = self.base.calendar(path, table, latest)
        return plan,mass,self._aggregate(coeff)

    def add_plan(self, plan):
        if isinstance(self.base, InterpolatedMaster):
            mass,coeff = self.base._coefficients(plan)
        else:
            # Derive the old coefficients without changing the base bank.
            old = len(self.base.columns)
            self.base.add_plan(plan)
            if len(self.base.columns) == old:
                return False
            mass,coeff = self.base.columns[-1]['mass'],self.base.columns[-1]['coeff']
        coeff = self._aggregate(coeff)
        key = mass,tuple(sorted(coeff.items()))
        if key in self.seen:
            return False
        self.seen.add(key)
        self.columns.append({'plan':plan,'mass':mass,'coeff':coeff})
        return True


class InteriorMaster(PersistentMaster):
    """A smaller stabilizer: bounds on existing variables, no L1 auxiliaries.

    Initial IPM with crossover supplies a basis for sparse warm simplex
    updates. Every LP number is exploratory even after an optimal solve.
    """
    def __init__(self, master, seconds=120., crossover=True,
                 component_prox=False, level_fraction=.5):
        super().__init__(master, seconds)
        self.component_prox = component_prox
        self.level_fraction = level_fraction
        h = self.main.highs
        _check(h.setOptionValue('solver', 'ipm'), 'select discovery IPM')
        _check(h.setOptionValue('run_crossover', 'on' if crossover else 'off'),
               'select crossover')
        _check(h.setOptionValue('ipm_optimality_tolerance', 1e-9), 'set IPM accuracy')

    def solve_box(self, anchor, radius, lower=None):
        self._sync_main()
        anchor = np.asarray(anchor, dtype=float)
        indices = np.arange(self.K, dtype=np.int32)
        _check(self.main.highs.changeColsBounds(
            self.K, indices, np.maximum(0., anchor-radius),
            np.minimum(1., anchor+radius)), 'update trust box')
        result = self.main.solve()
        if self.main.highs.getBasis().valid:
            _check(self.main.highs.setOptionValue('solver', 'simplex'),
                   'reuse the IPM crossover basis for sparse new rows')
        weights = -result.ineqlin.marginals[self.order_rows:]
        self.last_stats = self.main.last_stats.copy()
        trial = result.x[:-1].copy()
        self.trial_level = float(-result.fun)
        if self.component_prox and lower is not None and -result.fun > lower+1e-9:
            level = lower+self.level_fraction*(-result.fun-lower)
            if self.prox is None:
                self._make_prox(anchor, level)
                _check(self.prox.highs.setOptionValue('solver', 'ipm'), 'initialize level IPM')
                _check(self.prox.highs.setOptionValue('run_crossover', 'on'), 'level crossover')
            else:
                fixed = np.r_[self.K,np.arange(2*self.K+1,3*self.K+1)]
                self.prox.fix_columns(fixed,np.r_[level,anchor])
            _check(self.prox.highs.changeColsBounds(
                self.K,indices,np.maximum(0.,anchor-radius),np.minimum(1.,anchor+radius)),
                'level trust box')
            self._sync_prox()
            try:
                prox = self.prox.solve()
            except SolveError as error:
                self.last_stats['level_prox_failure'] = str(error)
            else:
                trial = prox.x[:self.K].copy()
                self.trial_level = float(level)
                self.last_stats['level_prox'] = dict(self.prox.last_stats,
                    target_level=float(level),l1_component_displacement=float(np.abs(trial-anchor).sum()))
                if self.prox.highs.getBasis().valid:
                    _check(self.prox.highs.setOptionValue('solver', 'simplex'), 'warm level basis')
        return result, weights, trial


def plans_from(data):
    if 'columns' in data:
        return [column.get('plan', column) for column in data['columns']]
    return data.get('paths', data.get('plans', []))


def load_physical_paths(master, table, paths, directory):
    """Seed with all supplied paths, recomputing calendars at the new field."""
    cache = CachedPathPricing(master.n, master.D)
    sources = []
    for path in paths:
        data = read_json(path)
        if master.n % data['n']:
            raise ValueError(f'bank {path} at n={data["n"]} does not divide {master.n}')
        count = cache.add_many(plans_from(data), source_n=data['n'])
        sources.append({'file': str(path), 'sha256': sha256(path),
                        'n': data['n'], 'new_physical_paths': count})
    # Safe endpoint/center routes make even an empty route bank well posed.
    cache.add({'start_grid': master.R, 'moves': [-1]*(2*master.R)})
    cache.add({'start_grid': 0, 'moves': [1]*master.R+[-1]*(2*master.R)})
    for batch in cache.price(table, keep=len(cache))['paths']:
        master.add(batch, table)
    write_json(directory/'sources.json', sources)
    return cache


def save_state(args, master, best, history, radius, status, started):
    bank_value = Fraction(int(best['answer']['minimum_units']), 4*master.n*master.D)
    lower = bank_value-Fraction(1, 2*master.n)
    state = {'scope': 'Discovery state; only best.dual.json has complete integer pricing.',
             'n': master.n, 'profile_grid': args.profile_grid,
             'denominator': args.denominator, 'trust_radius': radius,
             'contract_tight_cones': args.contract_tight_cones,
             'seed_field': str(args.seed_field), 'seed_field_sha256': sha256(args.seed_field),
             'columns': master.columns, 'history': history,
             'best_exact_bank_value': str(bank_value), 'global_lower': str(lower)}
    write_json(args.output/'state.json.gz', state)
    write_json(args.output/'manifest.json', {
        'status': status, 'method': 'IPM trust-box exact-separated Princess field search',
        'n': master.n, 'profile_grid': args.profile_grid, 'profile_variables': master.K,
        'original_profile_variables': getattr(master, 'base', master).K,
        'frozen_tight_cone_components': args.contract_tight_cones,
        'transport_order_rows': len(master.order), 'calendar_rows': len(master.columns),
        'best_exact_bank_value': str(bank_value),
        'transfer_penalty': str(Fraction(1, 2*master.n)),
        'certified_unrestricted_game_lower': str(lower),
        'certified_unrestricted_game_lower_decimal': float(lower),
        'same_cdf_security_claimed': False,
        'restricted_master_is_global_upper': False,
        'elapsed_seconds': time.monotonic()-started,
        'python_version': platform.python_version(), 'numpy_version': np.__version__,
        'arguments': {k: str(v) if isinstance(v, Path) else
                      [str(p) for p in v] if isinstance(v, list) else v
                      for k,v in vars(args).items()},
        'files': {p.name: {'sha256': sha256(p), 'bytes': p.stat().st_size}
                  for p in args.output.iterdir() if p.is_file() and
                  p.name not in ('manifest.json', 'search.log')}})


def run(args):
    began = time.monotonic()
    args.output.mkdir(parents=True, exist_ok=True)
    if args.n % args.profile_grid or args.profile_grid > args.n:
        raise ValueError('profile grid must divide the response grid')
    master = (Master(args.n, args.output/'work', args.denominator, True)
              if args.profile_grid == args.n else
              InterpolatedMaster(args.n, args.profile_grid,
                                 args.output/'work', args.denominator))
    seed = full_seed(args.seed_field)
    anchor = master.interpolate_seed(seed)
    if args.contract_tight_cones:
        master = ContractedMaster(master, anchor)
        anchor = master.interpolate_seed(seed)
    table = master.repair(anchor)
    anchor = master.profile_values(table)
    cache = load_physical_paths(master, table, args.response_bank, args.output)
    history = []
    radius = args.radius
    if args.resume and (args.output/'state.json.gz').exists():
        state = read_json(args.output/'state.json.gz')
        if state['n'] != args.n or state['profile_grid'] != args.profile_grid:
            raise ValueError('checkpoint has a different bank/profile resolution')
        for column in state['columns']:
            master.add_plan(column['plan'])
        if bool(state.get('contract_tight_cones',False)) != args.contract_tight_cones:
            raise ValueError('checkpoint has a different frozen-component family')
        previous, raw, _ = load_table(args.output/'best.dual.json')
        if previous['n'] != master.n or int(previous['field_denominator']) != master.D:
            raise ValueError('checkpoint probability or response denominator changed')
        # Do not round-trip a certified integer field through binary floats.
        table = np.frombuffer(raw,dtype=np.uint64).reshape((master.H+1,master.R+1)).copy()
        anchor = master.profile_values(table)
        best = {'answer': previous['pricing'], 'table': table.copy()}
        history, radius = state['history'], state['trust_radius']
        cache.update_columns(master.columns)
    else:
        # Complete baseline is necessary: a coarsened seed carries no inherited
        # bound, even if the input file has a stronger certificate at finer n.
        answer, table = master.price(anchor, keep=args.keep)
        best = {'answer': answer, 'table': table.copy()}
        anchor = master.profile_values(table)
        cache.add_many(answer['paths'])
        for path in answer['paths']:
            master.add(path, table)
        value = int(answer['minimum_units'])/(4*master.n*master.D)
        placeholder = OptimizeResult(x=np.r_[anchor, value], fun=-value)
        master.save(args.output/'best', table, answer, placeholder,
                    np.zeros(len(master.columns)), [])
        print(json.dumps({'event': 'complete_seed', 'n': master.n,
                          'profile_grid': args.profile_grid, 'bank_value': value,
                          'global_lower': value-1/(2*master.n),
                          'states': answer['retained_states'],
                          'seconds': time.monotonic()-began}), flush=True)
    backend = InteriorMaster(master,args.lp_seconds,args.crossover,
                             args.component_prox,args.level_fraction)
    save_state(args, master, best, history, radius, 'RUNNING', began)
    status = 'ITERATION_LIMIT'
    for iteration in range(args.iterations):
        if time.monotonic()-began >= args.seconds:
            status = 'BUDGET_STOPPED'
            break
        previous_value = int(best['answer']['minimum_units'])/(4*master.n*master.D)
        try:
            lp, weights, trial = backend.solve_box(anchor, radius, previous_value)
        except SolveError as error:
            if 'Time limit reached' not in str(error):
                raise
            status = 'LP_BUDGET_STOPPED'
            print(json.dumps({'event': status, 'error': str(error)}), flush=True)
            break
        trial_table = master.repair(trial)
        cache.update_columns(master.columns)
        cached = cache.price(trial_table, keep=args.cached_keep,
                             level=backend.trial_level,tolerance=str(args.cut_tolerance))
        additions = sum(master.add(path, trial_table) for path in cached['violating_paths'])
        report = {'iteration': len(history), 'radius': radius,
                  'restricted_box_master_value': float(-lp.fun),
                  'trial_target_level':backend.trial_level,
                  'columns': len(master.columns), 'cached_paths': len(cache),
                  'cached_path_upper': int(cached['cached_minimum_units'])/(4*master.n*master.D),
                  'new_calendars': additions, 'lp': backend.last_stats,
                  'seconds': time.monotonic()-began}
        if additions:
            report['pricing_scope'] = 'cached witnesses only; no new lower'
        else:
            priced, priced_table = master.price(trial, keep=args.keep)
            trial_dir = args.output/'priced_trials'
            trial_dir.mkdir(exist_ok=True)
            trial_path = trial_dir/f'trial_{len(history):05d}.json.gz'
            save_priced_trial(trial_path,master,priced_table,priced)
            cache.add_many(priced['paths'])
            value = int(priced['minimum_units'])/(4*master.n*master.D)
            report.update({'pricing_scope': 'complete exact normalized physical bank',
                           'exact_bank_value': value, 'record_states': priced['retained_states'],
                           'exact_trial_file':str(trial_path.relative_to(args.output)),
                           'exact_trial_sha256':sha256(trial_path),
                           'new_calendars': sum(master.add(p, priced_table)
                                                for p in priced['paths'])})
            if int(priced['minimum_units']) > int(best['answer']['minimum_units']):
                best = {'answer': priced, 'table': priced_table.copy()}
                anchor = master.profile_values(priced_table)
                padded_weights = np.pad(weights, (0, len(master.columns)-len(weights)))
                # Checkpoint profile must describe the actually certified
                # (possibly proximal and integer-repaired) field.
                saved_lp = OptimizeResult(x=np.r_[anchor,value],fun=lp.fun)
                master.save(args.output/'best',priced_table,priced,saved_lp,padded_weights,history+[report])
                report['accepted_new_complete_field'] = True
            elif value < previous_value-args.tolerance:
                radius = max(args.minimum_radius, radius/2)
                report['next_radius'] = radius
                report['radius_reason'] = 'complete oracle rejected the trial; keep exact anchor'
            gap = float(-lp.fun)-max(value, previous_value)
            if gap <= args.tolerance:
                if radius >= 1:
                    status = 'FULL_PROFILE_GAP_CLOSED'
                    history.append(report)
                    print(json.dumps(report), flush=True)
                    break
                radius = min(1., 2*radius)
                report['next_radius'] = radius
        report['seconds'] = time.monotonic()-began
        history.append(report)
        print(json.dumps(report), flush=True)
        if len(history) % args.checkpoint_every == 0 or report.get('accepted_new_complete_field'):
            save_state(args, master, best, history, radius, 'RUNNING', began)
    save_state(args, master, best, history, radius, status, began)
    return read_json(args.output/'manifest.json')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--n', type=int, default=128)
    parser.add_argument('--profile-grid', type=int, default=64)
    parser.add_argument('--seed-field', type=Path,
                        default=ROOT/'packages/interval_clock_grid/lower_n256_field.json')
    parser.add_argument('--response-bank', type=Path, action='append', default=[])
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--iterations', type=int, default=200)
    parser.add_argument('--seconds', type=float, default=1200.)
    parser.add_argument('--lp-seconds', type=float, default=90.)
    parser.add_argument('--radius', type=float, default=.025)
    parser.add_argument('--minimum-radius', type=float, default=.0001)
    parser.add_argument('--denominator', type=int, default=10**8)
    parser.add_argument('--keep', type=int, default=96)
    parser.add_argument('--cached-keep', type=int, default=384)
    parser.add_argument('--cut-tolerance', type=float, default=5e-8)
    parser.add_argument('--tolerance', type=float, default=2e-7)
    parser.add_argument('--checkpoint-every', type=int, default=5)
    parser.add_argument('--crossover', action=argparse.BooleanOptionalAction, default=True)
    parser.add_argument('--contract-tight-cones', action='store_true')
    parser.add_argument('--component-prox',action='store_true',
                        help='minimize L1 displacement at a bundle level inside the current trust box')
    parser.add_argument('--level-fraction',type=float,default=.5)
    parser.add_argument('--resume', action='store_true')
    args = parser.parse_args()
    if args.keep < 1 or args.keep > 1000 or args.cached_keep < 1:
        raise ValueError('invalid witness limits')
    if not 0 < args.minimum_radius <= args.radius <= 1 or args.checkpoint_every < 1:
        raise ValueError('invalid trust radius or checkpoint frequency')
    if not 0 < args.level_fraction < 1:
        raise ValueError('level fraction must lie strictly between zero and one')
    if not args.response_bank:
        args.response_bank = [Path(__file__).with_name('initial_paths_n128.json.gz')]
    print(json.dumps(run(args)), flush=True)


if __name__ == '__main__':
    main()
