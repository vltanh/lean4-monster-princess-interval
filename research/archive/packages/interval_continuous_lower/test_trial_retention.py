#!/usr/bin/env python3
"""Exercise actual cache rejection and stale-checkpoint trial preservation.

The LP is replaced by prescribed legal bad fields so this tests the rejection
branch deterministically. One tiny n6 source response is priced; no numerical
optimization or large response search is performed.
"""
from contextlib import redirect_stdout
from fractions import Fraction as Q
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
import gzip
import hashlib
import io
import json
import tempfile

import numpy as np

import search


def verify():
    with tempfile.TemporaryDirectory(prefix='continuous_trial_retention_') as temporary:
        folder=Path(temporary)
        fixture=search.ROOT/'packages/interval_clock_grid/normalized_princess_n6_fixture.json'
        data,raw,_=search.load_table(fixture)
        n,D=data['n'],int(data['field_denominator'])
        master=search.Master(n,folder/'seed-work',D)
        seed=np.frombuffer(raw,dtype=np.uint64).reshape((master.H+1,master.R+1)).copy()
        response=search.price_table(master,seed,0)
        assert response['minimum_units']==data['minimum_units']
        seed_file=folder/'seed.json'
        search.write(seed_file,search.add_certificate(master,search.pack_field(master,seed),response))
        bank={'n':n,'paths':[
            {'start_grid':master.R,'moves':[-1]*(2*master.R)},
            {'start_grid':master.R-2,'moves':[1]*2+[-1]*(2*master.R)}]}
        bank_file=folder/'bank.json';search.write(bank_file,bank)
        args=SimpleNamespace(n=n,output=folder/'discovery',seed_field=seed_file,
            denominator=None,oracle='classic',bank_model='calendars',seed_replay=None,
            bank_slack='1/10000000',resume=False,response_bank=bank_file,
            initial_routes=1,keep=2,cached_keep=2,lp_seconds=1.,level_fraction=.5,
            attack=search.ROOT/'packages/interval_quantile_certificate/current_fullwidth_attack.json',
            initial_attacks=0,attack_seconds=0.,attack_starts=1,attack_evaluations=1,
            random_seed=20261114,new_attacks=1,iterations=1,seconds=30.,
            radius=.01,minimum_radius=.00005,maximum_radius=.05,
            screen_tolerance='1/1000000',attack_every=1)
        trials=[master.repair(np.zeros(master.K)),master.repair(np.full(master.K,.1))]
        chosen=[0]

        class PrescribedTrial(search.EventLP):
            def solve(self,incumbent,screen,radius):
                return trials[chosen[0]],float(screen)+.01,float(screen)+.005,{'prescribed_test_trial':True}

        initial_checkpoint={}
        save_state=search.save_state
        def observe_initial(*values,**kwargs):
            save_state(*values,**kwargs)
            if not initial_checkpoint:
                state=search.read_json(args.output/'state.json.gz')
                assert state['history']==[]
                for name in ('state.json.gz','incumbent.field.json'):
                    initial_checkpoint[name]=(args.output/name).read_bytes()

        def no_trial_pricing(*unused,**kwargs):
            raise AssertionError('a cached-rejected trial reached complete response pricing')

        def run_once():
            with patch.object(search,'EventLP',PrescribedTrial), \
                    patch.object(search,'save_state',observe_initial), \
                    patch.object(search,'price_table',no_trial_pricing), redirect_stdout(io.StringIO()):
                result=search.run(args)
            state=search.read_json(args.output/'state.json.gz')
            assert len(state['history'])==1
            row=state['history'][0]
            assert row['status']=='CACHED_BANK_FLOOR_REJECTED'
            assert row['iteration']==0 and row['new_bank_calendars']>=1
            reference=row['trial_field'];path=args.output/reference['path']
            trial=search.check_trial_binding(args.output,reference)
            assert not {'minimum_units','certified_bank_lower_units','pricing','global_lower'} & trial.keys()
            assert reference['field_json_sha256'] in path.name
            saved,table,_=search.load_table(path)
            restored=np.frombuffer(table,dtype=np.uint64).reshape(seed.shape)
            assert np.array_equal(restored,trials[chosen[0]])
            cache=search.CachedPathPricing(n,D);cache.add_many(bank['paths'])
            price=cache.price(restored,keep=2)
            assert Q(int(price['cached_minimum_units']),4*n*D)==Q(row['cached_bank_upper'])
            assert Q(row['cached_bank_upper'])<Q(row['bank_floor'])
            assert result['files'][reference['path']]['sha256']==reference['compressed_sha256']
            assert result['files'][reference['path']]['bytes']==reference['compressed_bytes']
            assert (args.output/'incumbent.field.json').read_bytes()==initial_checkpoint['incumbent.field.json']
            return reference,path.read_bytes()

        first,first_bytes=run_once()
        # Simulate a restart from the checkpoint preceding an interrupted
        # trial. Its old field already exists, but iteration zero is retried.
        for name,raw in initial_checkpoint.items():(args.output/name).write_bytes(raw)
        args.resume=True;chosen[0]=1
        second,second_bytes=run_once()
        assert first['path']!=second['path']
        assert first['raw_nodal_sha256']!=second['raw_nodal_sha256']
        assert (args.output/first['path']).read_bytes()==first_bytes
        assert len(list((args.output/'trials').glob('*.field.json.gz')))==2
        assert search.retain_trial_field(master,trials[1],args.output,0)==second
        assert (args.output/second['path']).read_bytes()==second_bytes
        assert not list((args.output/'trials').glob('*.tmp'))
        # Reusing an immutable name may not silently replace corrupt content.
        damaged=gzip.compress(b'{"different":true}\n',mtime=0)
        (args.output/first['path']).write_bytes(damaged)
        try:search.retain_trial_field(master,trials[0],args.output,0)
        except ValueError:pass
        else:raise AssertionError('different existing bytes were overwritten')
        assert (args.output/first['path']).read_bytes()==damaged
        try:search.check_trial_binding(args.output,first)
        except ValueError:pass
        else:raise AssertionError('corrupt compressed hash was accepted')
        return {'status':'PASS','actual_cached_rejected_trials_retained':2,
            'exact_cached_cost_replays':2,'stale_checkpoint_same_iteration_fields_preserved':2,
            'matching_trial_reused_without_overwrite':True,'corrupt_existing_trial_rejected':True,
            'incumbent_unchanged':True,'trial_complete_oracle_calls':0,
            'tiny_n6_seed_response_calls':1,'numerical_optimizations':0}


if __name__=='__main__':print(json.dumps(verify(),indent=2))
