#!/usr/bin/env python3
"""Seeded CDF discovery, complete exact pricing, and gated fine certification.

The existing native solver optimizes legal transport profiles and discovers
physical Monster responses. This driver supplies genuinely different seeded
starts, preserves resumable state, and records the distinction between the
floating master, exact finite bank, and transferred unrestricted game bound.
Nothing here asserts security of the same interpolated Princess law.
"""
from __future__ import annotations

import argparse
from fractions import Fraction
import gzip
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import platform
import random
import signal
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
NATIVE = ROOT / 'packages/interval_clock_grid/normalized_native'
sys.path.insert(0, str(NATIVE))

BASELINE = max(Fraction(3050023091, 2147483648),
               Fraction(json.loads((ROOT/'packages/interval_clock_grid/lower_n256_field.json').read_text())['global_lower']))


def read_json(path):
    data = Path(path).read_bytes()
    return json.loads(gzip.decompress(data) if data[:2] == b'\x1f\x8b' else data)


def write_json(path, value):
    path = Path(path)
    temporary = path.with_suffix(path.suffix + '.tmp')
    temporary.write_text(json.dumps(value, separators=(',', ':')) + '\n')
    temporary.replace(path)


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def random_path(n, rng):
    """A correlated physical walk with an enforced time-two center deadline."""
    radius, cutoff = 2*n, 4*n
    start = 2*rng.randrange(n+1)
    x, centered, moves = start, start == 0, []
    direction = rng.choice((-1, 1))
    persistence = rng.uniform(.55, .98)
    for t in range(cutoff):
        if abs(x) == radius:
            break
        if rng.random() > persistence:
            direction = -direction
        choices = []
        for step in (-1, 1):
            y = x + step
            if abs(y) > radius:
                continue
            if not centered and abs(y) > cutoff-t-1:
                continue
            if not centered and abs(y) == radius and t+1+radius > cutoff:
                continue
            choices.append(step)
        if not choices:
            raise AssertionError('center deadline construction failed')
        step = direction if direction in choices else choices[0]
        moves.append(step)
        x += step
        centered = centered or x == 0
    first = x if abs(x) == radius else rng.choice((-radius, radius))
    for target in (first, -first):
        step = 1 if target > x else -1
        moves.extend([step]*abs(target-x))
        x = target
    from cached_path_pricing import normalize_path
    return normalize_path(n, {'start_grid': start, 'moves': moves})


def full_seed(path):
    """Decode compact saved fields before the old solver's interpolation API."""
    data = read_json(path)
    if 'radial_nodes' in data:
        return data
    from verify_native_field import load_table
    data, table, _ = load_table(Path(path))
    n = data['n']
    data = dict(data)
    data['radial_nodes'] = [[j, k, str(table[j*(2*n+1)+k])]
                            for j in range(12*n+1)
                            for k in range(1, 2*n+1) if (j+k)%2 == 0]
    return data


def make_starts(args, directory):
    import numpy as np
    from solve_normalized import Master
    from cached_path_pricing import normalize_path

    rng = random.Random(args.seed)
    coarse_n = args.profile_grid or args.n
    model = Master(coarse_n, directory/'initial.work', args.denominator, True)
    # These are legal waiting-then-outward populations; convex mixing gives
    # distinct continuous initial laws. Integer order repair is still applied.
    components = [(rng.uniform(.2, 1.), rng.uniform(0., 1.8),
                   rng.uniform(.45, 2.5), rng.random()+.1) for _ in range(4)]
    mass = sum(c[3] for c in components)
    generated = np.asarray([
        sum(weight * min(1., max(0., k/(2*coarse_n)-max(0., j/(2*coarse_n)-wait))/width)**power
            for width, wait, power, weight in components)/mass
        for j, k in model.nodes])
    if args.profile_seed:
        known = model.interpolate_seed(full_seed(args.profile_seed))
        # The randomized family changes a seed, not the legal feasible set.
        fraction = args.perturbation if args.family == 'randomized' else 0.
        generated = (1-fraction)*known + fraction*generated
    table = model.repair(generated)
    initial = {'scope': 'Feasible starting profile only; no security claimed.',
               'n': coarse_n, 'field_denominator': str(model.D),
               'normalized_profile': True,
               'radial_nodes': [[j, k, str(int(table[j, k]))]
                                for j in range(model.H+1)
                                for k in range(1, model.R+1) if (j+k)%2 == 0]}
    write_json(directory/'initial_field.json', initial)

    fine = Master(args.n, directory/'initial_bank.work', args.denominator, True)
    fine_table = fine.repair(fine.interpolate_seed(initial))
    paths = [random_path(args.n, rng) for _ in range(args.random_paths)]
    if args.monster_seed:
        source = read_json(args.monster_seed)
        source_paths = source.get('paths')
        if source_paths is None:
            source_paths = [c['plan'] for c in source['columns']]
        if args.n % source['n']:
            raise ValueError('Monster seed mesh must divide discovery mesh')
        paths.extend(normalize_path(args.n, p, source_n=source['n']) for p in source_paths)
    unique = {(p['start_grid'], tuple(p['moves'])): p for p in paths}
    plans = [fine.calendar(p, fine_table)[0] for p in unique.values()]
    write_json(directory/'initial_bank.json', {'n': args.n, 'paths': plans,
               'scope': 'Physical response seeds; no bound or mixture weight claimed.',
               'random_seed': args.seed, 'generated_paths': args.random_paths})
    return {'random_components': components, 'unique_initial_physical_paths': len(plans)}


def run_logged(command, directory, name, timeout, checkpoint=None):
    """Keep both solver JSON and diagnostic text; a timeout preserves checkpoints."""
    started = time.monotonic()
    with (directory/(name+'.log')).open('w') as log:
        process = subprocess.Popen(command, stdout=log, stderr=subprocess.STDOUT,
                                   start_new_session=True,
                                   cwd=ROOT, env={**os.environ, 'PYTHONUNBUFFERED': '1'})
        try:
            code = process.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            os.killpg(process.pid, signal.SIGTERM)
            try:
                process.wait(timeout=15)
            except subprocess.TimeoutExpired:
                os.killpg(process.pid, signal.SIGKILL)
                process.wait()
            if checkpoint is not None and checkpoint.exists():
                print(json.dumps({'event':name, 'status':'BUDGET_STOPPED',
                                  'saved_exact_checkpoint':str(checkpoint),
                                  'seconds':time.monotonic()-started}), flush=True)
                return 'BUDGET_STOPPED'
            raise RuntimeError(f'{name} exceeded {timeout}s; saved checkpoints retained')
    print(json.dumps({'event': name, 'exit_code': code,
                      'seconds': time.monotonic()-started}), flush=True)
    if code:
        tail = (directory/(name+'.log')).read_text()[-5000:]
        # HiGHS can exhaust one genuine per-solve budget after a cold restart,
        # even when the cumulative-clock bug has been fixed. Preserve only an
        # already completed exact field; the unfinished LP supplies no bound.
        if checkpoint is not None and checkpoint.exists() and 'HiGHS status: Time limit reached' in tail:
            saved = read_json(checkpoint)
            if saved.get('pricing', {}).get('status') == 'PASS':
                print(json.dumps({'event':name, 'status':'BUDGET_STOPPED',
                                  'reason':'per_solve_lp_time_limit',
                                  'saved_exact_checkpoint':str(checkpoint),
                                  'unfinished_lp_objective_used':False}), flush=True)
                return 'BUDGET_STOPPED'
        raise RuntimeError(f'{name} failed with exit {code}: {tail}')
    return 'PASS'


def field_summary(path):
    data = read_json(path)
    lower = Fraction(data['global_lower'])
    return {'file': Path(path).name, 'sha256': digest(path), 'n': data['n'],
            'exact_bank_dual': data['normalized_bank_dual_value'],
            'transfer_penalty': str(Fraction(1, 2*data['n'])),
            'certified_game_value_lower': str(lower),
            'certified_game_value_lower_decimal': float(lower),
            'improves_retained_game_lower': lower > BASELINE,
            'same_cdf_continuum_security_claimed': False,
            'pricing_status': data['pricing'].get('status')}


def structure(path, checkpoint):
    data = read_json(path)
    n, den = data['n'], int(data['field_denominator'])
    field = {(j, k): int(a) for j, k, a in data['radial_nodes']}
    # g(t,r)=2*F(t,r)-1 for r>=0. Values at r=1 are strict
    # traces; the remaining probability is the endpoint atom.
    traces = {str(Fraction(j, 2*n)): [[str(Fraction(k, 2*n)), str(Fraction(field[j,k], den))]
                for k in range(2, 2*n+1, 2)] for j in (0, 2*n, 4*n)}
    edges = [(field[j,k], field[j+s,k+1]) for j in range(4*n+1)
             for k in range(1, 2*n) if (j+k)%2 == 0
             for s in (-1, 1) if 0 <= j+s <= 4*n]
    ans = {'scope': 'Exact candidate geometry; no equilibrium claim.',
           'radial_signed_cdf_at_t_0_1_2': traces,
           'transport_equalities': sum(a == b for a,b in edges),
           'transport_edges': len(edges),
           'endpoint_atom_each_at_t_0_1_2': [str(Fraction(den-field[j,2*n],2*den))
                                            for j in (0,2*n,4*n)]}
    if checkpoint.exists():
        saved = read_json(checkpoint)
        bank_n = saved['n']
        active = [(c,w) for c,w in zip(saved['columns'], saved['weights']) if w > 1e-9]
        ans.update({'floating_master_objective': saved['upper'],
                    'floating_active_calendars': len(active),
                    'floating_support_scope': 'Unverified LP dual weights, not a global upper.',
                    'floating_start_mass': {str(Fraction(s,2*bank_n)):sum(w for c,w in active if c['plan']['start_grid']==s)
                        for s in sorted({c['plan']['start_grid'] for c,w in active})}})
    return ans


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--n', type=int, required=True)
    parser.add_argument('--profile-grid', type=int)
    parser.add_argument('--family', choices=('proximal', 'plain', 'randomized'), default='proximal')
    parser.add_argument('--seed', type=int, default=20261114)
    parser.add_argument('--iterations', type=int, default=120)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--profile-seed', type=Path)
    parser.add_argument('--monster-seed', type=Path)
    parser.add_argument('--random-paths', type=int, default=48)
    parser.add_argument('--perturbation', type=float, default=.015)
    parser.add_argument('--denominator', type=int, default=10**9)
    parser.add_argument('--pricing-paths', type=int, default=48)
    parser.add_argument('--refine', type=int)
    parser.add_argument('--refine-threshold', type=str, default=str(BASELINE))
    parser.add_argument('--independent-replay', action='store_true')
    parser.add_argument('--resume', action='store_true')
    parser.add_argument('--timeout', type=int, default=2400)
    parser.add_argument('--seconds', type=int, help='Discovery budget; preserve the last complete exact checkpoint.')
    parser.add_argument('--refine-seconds', type=int, default=1800)
    args = parser.parse_args()
    if args.n < 1 or args.iterations < 1 or args.random_paths < 0 or not 0 <= args.perturbation <= 1:
        parser.error('invalid search dimensions')
    if args.profile_grid and (args.profile_grid < 1 or args.n % args.profile_grid):
        parser.error('profile grid must divide n')
    if args.refine and args.refine <= args.n:
        parser.error('refinement must be finer than discovery')
    args.output = args.output.resolve()
    for name in ('profile_seed', 'monster_seed'):
        if getattr(args, name):
            setattr(args, name, getattr(args, name).resolve())
    directory = args.output
    directory.mkdir(parents=True, exist_ok=True)
    options = {k: str(v) if isinstance(v, Path) else v for k,v in vars(args).items()}
    manifest = {'status': 'RUNNING', 'scope': 'Seeded discovery with separate exact pricing.',
                'options': options, 'random_seed': args.seed,
                'github_run_id': os.environ.get('GITHUB_RUN_ID'),
                'github_sha': os.environ.get('GITHUB_SHA'),
                'python': sys.version, 'platform': platform.platform(),
                'dependencies': {name: importlib.metadata.version(name) for name in ('numpy','scipy')},
                'baseline_game_lower': str(BASELINE),
                'source_sha256': {str(p.relative_to(ROOT)): digest(p)
                    for p in [Path(__file__),
                              NATIVE/'persistent_highs.py', NATIVE/'solve_normalized.py',
                              NATIVE/'price_normalized.cpp', NATIVE/'interpolated_master.py',
                              NATIVE/'cached_path_pricing.py', NATIVE/'refine_dual.py']},
                'input_sha256': {name: digest(getattr(args,name))
                    for name in ('profile_seed','monster_seed') if getattr(args,name)}}
    old = directory/'manifest.json'
    retained = directory/'best.dual.json.gz'
    retained_value = None
    if args.resume and old.exists():
        previous = read_json(old)
        for key in ('n','profile_grid','family','seed','denominator'):
            if previous['options'][key] != options[key]:
                raise ValueError(f'resume changed {key}')
        manifest['resumed_manifest_sha256'] = digest(old)
        if previous.get('best_exact'):
            previous_best = directory/previous['best_exact']['file']
            if digest(previous_best) != previous['best_exact']['sha256']:
                raise ValueError('retained exact certificate hash changed')
            previous_data = read_json(previous_best)
            retained_value = Fraction(previous_data['global_lower'])
            if previous_best != retained:
                retained.write_bytes(gzip.compress(json.dumps(previous_data,separators=(',',':')).encode()+b'\n',mtime=0))
            manifest['retained_previous_lower'] = str(retained_value)
    started = time.monotonic()
    write_json(old, manifest)
    try:
        if not args.resume or not (directory/'initial_field.json').exists():
            manifest['starting_geometry'] = make_starts(args, directory)
        prefix = directory/'candidate'
        command = [sys.executable, str(NATIVE/'solve_normalized.py'), str(args.n),
                   '--output', str(prefix), '--iterations', str(args.iterations),
                   '--denominator', str(args.denominator), '--pricing-paths', str(args.pricing_paths)]
        if args.profile_grid:
            command += ['--profile-grid', str(args.profile_grid)]
        if args.family == 'plain':
            command += ['--plain']
        if args.resume and prefix.with_suffix('.checkpoint.json').exists():
            command += ['--restart']
        else:
            command += ['--profile-seed', str(directory/'initial_field.json'),
                        '--seed', str(directory/'initial_bank.json')]
        manifest['commands'] = [command]
        write_json(old, manifest)
        discovery_status = run_logged(command, directory, 'discovery', args.seconds or args.timeout,
                                      prefix.with_suffix('.dual.json'))
        manifest['optimization_status'] = discovery_status
        candidate = prefix.with_suffix('.dual.json')
        manifest['coarse_exact'] = field_summary(candidate)
        best = candidate
        if args.refine:
            data = read_json(candidate)
            optimistic = Fraction(data['normalized_bank_dual_value']) - Fraction(1,2*args.refine)
            gate = Fraction(args.refine_threshold)
            manifest['refinement_gate'] = {'threshold':str(gate), 'optimistic_screen':str(optimistic),
                                          'scope':'Heuristic allocation screen; no new bound.',
                                          'selected':optimistic > gate}
            if optimistic > gate:
                refined = directory/'refined.dual.json'
                command = [sys.executable, str(NATIVE/'refine_dual.py'), str(candidate), str(args.refine),
                           '--output', str(refined), '--denominator', str(args.denominator), '--paths', '0']
                manifest['commands'].append(command)
                write_json(old, manifest)
                refinement_status = run_logged(command, directory, 'refinement', args.refine_seconds,
                                               candidate)
                manifest['refinement_status'] = refinement_status
                if refinement_status == 'PASS':
                    manifest['refined_exact'] = field_summary(refined)
                    if Fraction(read_json(refined)['global_lower']) > Fraction(data['global_lower']):
                        best = refined
        if retained_value is not None and retained_value > Fraction(read_json(best)['global_lower']):
            best = retained
        if best != retained:
            retained.write_bytes(gzip.compress(best.read_bytes(),mtime=0))
            best = retained
        if args.independent_replay:
            command = ['node', '--max-old-space-size=8192',
                       str(ROOT/'packages/interval_clock_grid/normalized_record_pricing.cjs'),
                       str(best), '--target-bound']
            manifest['commands'].append(command)
            run_logged(command, directory, 'independent_bigint_replay', args.timeout)
            manifest['independent_bigint_replay'] = 'PASS'
        manifest['best_exact'] = field_summary(best)
        write_json(directory/'structure.json', structure(best, prefix.with_suffix('.checkpoint.json')))
        manifest['status'] = ('BUDGET_STOPPED' if 'BUDGET_STOPPED' in
                              (manifest.get('optimization_status'), manifest.get('refinement_status'))
                              else 'PASS')
    except Exception as exc:
        manifest['status'] = 'FAILED'
        manifest['error'] = str(exc)
        raise
    finally:
        manifest['seconds'] = time.monotonic()-started
        # Inputs are deterministic from the exact JSON. Keep certificates and
        # restart state, not potentially hundreds of MB of disposable tables.
        for p in directory.glob('*.work/pricing.input.bin'):
            p.unlink()
        manifest['artifacts_sha256'] = {p.name:digest(p) for p in sorted(directory.iterdir())
                                        if p.is_file() and p.name != 'manifest.json'}
        write_json(old, manifest)
        print(json.dumps({'status':manifest['status'], 'manifest':str(old),
                          'best_exact':manifest.get('best_exact'),
                          'seconds':manifest['seconds']}), flush=True)


if __name__ == '__main__':
    main()
