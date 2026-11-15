#!/usr/bin/env python3
"""Run real tiny hybrid searches and resume their immutable trial checkpoints."""
from pathlib import Path
import json
import subprocess
import sys
import tempfile

import numpy as np

import search
from front_model import project


def run():
    counts = dict(searches=0, resumes=0, retained_trials=0, replayed_cached_costs=0)
    with tempfile.TemporaryDirectory() as temporary:
        folder = Path(temporary)
        master = search.Master(2, folder/'seed-work', 10**8)
        for front in (False, True):
            seed = master.repair([min(1., k/4+max(0, 4-j)/32) for j,k in master.nodes])
            if front:
                seed = project(master.n, seed)
            answer = search.price_table(master, seed, 4)
            source = folder/f'seed-{front}.json'
            search.write(source, search.add_certificate(master, search.pack_field(master, seed), answer))
            bank = folder/f'bank-{front}.json'
            search.write(bank, dict(n=master.n, paths=answer['paths']))
            output = folder/f'run-{front}'
            command = [sys.executable, '-B', str(Path(__file__).with_name('front_search.py' if front else 'search.py')),
                       '--n', '2', '--seed-field', str(source), '--response-bank', str(bank),
                       '--oracle', 'classic', '--bank-model', 'hybrid', '--continuous-secants', '4',
                       '--promotion-after', '2', '--initial-routes', '4', '--initial-attacks', '0',
                       '--keep', '4', '--cached-keep', '4', '--attack-seconds', '0',
                       '--lp-seconds', '10', '--seconds', '30', '--iterations', '2',
                       '--radius', '.005', '--bank-slack', '1/1000', '--output', str(output)]
            subprocess.run(command, check=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            counts['searches'] += 1
            state = search.read_json(output/'state.json.gz')
            assert len(state['history']) == 2 and state['bank_model'] == 'hybrid'
            references = [r['trial_field'] for r in state['history']]
            old = {(output/r['path']): (output/r['path']).read_bytes() for r in references}
            subprocess.run(command+['--resume'], check=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            counts['resumes'] += 1
            for path, raw in old.items():
                assert path.read_bytes() == raw
            state = search.read_json(output/'state.json.gz')
            assert len(state['history']) == 4
            assert len(state['hybrid_model']['continuous_routes']) >= 2
            manifest = search.read_json(output/'manifest.json')
            assert not manifest['continuous_screen_is_lower_bound']
            assert not manifest['same_fullwidth_cdf_security_claimed']
            cache = search.CachedPathPricing(master.n, master.D)
            cache.add_many(search.read_json(bank)['paths'])
            cache.add({'start_grid': master.R, 'moves': [-1]*(2*master.R)})
            for row in state['history']:
                assert row['lp_secant_model_is_upper_bound'] is False
                assert 'lp_continuous_screen_upper' not in row
                assert 'continuous_restricted_upper' not in row['lp']
                ref = row['trial_field']
                data = search.check_trial_binding(output, ref)
                assert 'pricing' not in data and 'global_lower' not in data
                _, raw, _ = search.load_table(output/ref['path'])
                trial = np.frombuffer(raw, dtype=np.uint64).reshape(seed.shape)
                # This replay is an independent upper screen on each trial,
                # not an assignment of its source's lower certificate.
                cached = cache.price(trial, keep=1)
                assert search.Q(int(cached['cached_minimum_units']), 4*master.n*master.D) == search.Q(row['cached_bank_upper'])
                certified = output/f"trial_{row['iteration']:04d}.certified.json.gz"
                if certified.exists():
                    cache.add_many(search.read_json(certified)['pricing']['paths'])
                counts['retained_trials'] += 1
                counts['replayed_cached_costs'] += 1
            # A changed inner model must never silently resume old records.
            changed = list(command)+['--resume', '--continuous-secants', '5']
            rejected = subprocess.run(changed, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            assert rejected.returncode and 'hybrid checkpoint model parameters changed' in rejected.stderr
    return dict(status='PASS', counts=counts, all_monster_security_claimed=False)


if __name__ == '__main__':
    print(json.dumps(run(), indent=2))
