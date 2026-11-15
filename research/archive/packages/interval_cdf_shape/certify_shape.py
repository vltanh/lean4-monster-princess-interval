#!/usr/bin/env python3
"""Independent coarse replay and bounded fine pricing for shape experiments."""
import argparse
from fractions import Fraction
import json
import os
from pathlib import Path
import sys

from shape_search import ROOT,NATIVE,CURRENT_GAME_LOWER,read_json,write_json,digest
from princess_search import run_logged
from verify_native_field import load_table


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('directory',type=Path)
    parser.add_argument('--refine',type=int,default=256)
    parser.add_argument('--refine-seconds',type=int,default=240)
    args=parser.parse_args();directory=args.directory.resolve()
    manifest=read_json(directory/'manifest.json')
    assert manifest['status']=='PASS' and manifest['exact_security_floor_verified']
    candidate=directory/'candidate.dual.json'
    assert digest(candidate)==manifest['artifacts_sha256']['candidate.dual.json']
    command=['node','--max-old-space-size=8192',str(ROOT/'packages/interval_clock_grid/normalized_record_pricing.cjs'),str(candidate),'--target-bound']
    run_logged(command,directory,'independent_bigint',180)
    replay=read_json(directory/'independent_bigint.log')
    assert replay['status']=='PASS' and replay['qout_verified'] is True
    assert replay['input_sha256']==digest(candidate)
    assert Fraction(replay['normalized_bank_lower'])>=Fraction(manifest['requested_bank_floor'])
    result={'status':'PASS','search_result':manifest['search_result'],
            'scope':'Exact security verification of shape discovery; no claim of a globally minimal variation or sufficient equilibrium class.',
            'current_game_lower':str(CURRENT_GAME_LOWER),
            'coarse_independent_game_lower':replay['global_lower'],
            'coarse_input_sha256':digest(candidate),
            'before':manifest['before'],'after':manifest['after'],
            'new_shape_accepted':manifest['shape_improved'],
            'same_cdf_continuum_security_claimed':False}
    if manifest['shape_improved'] and args.refine>manifest['options']['n']:
        refined=directory/'refined.dual.json'
        command=[sys.executable,str(NATIVE/'refine_dual.py'),str(candidate),str(args.refine),
                 '--output',str(refined),'--denominator','1000000000','--paths','0']
        status=run_logged(command,directory,'refinement',args.refine_seconds,candidate)
        result['refinement_status']=status
        if status=='PASS':
            data,table,field_hash=load_table(refined)
            assert data['source_seed_sha256']==digest(candidate)
            n,D=data['n'],int(data['field_denominator']);R,H=2*n,12*n
            checks=0
            for j in range(H+1):
                for k in range(j%2,R,2):
                    value=table[j*(R+1)+k]
                    for step in (-1,1):
                        if 0<=j+step<=H:
                            assert value<=table[(j+step)*(R+1)+k+1]
                            checks+=1
            priced=data['pricing']
            assert priced['status']=='PASS'
            assert int(priced['minimum_units'])==int(data['minimum_units'])
            lower=Fraction(int(data['minimum_units'])-2*D,4*n*D)
            assert lower==Fraction(data['global_lower'])
            result.update({'fine_native_game_lower':str(lower),'fine_input_sha256':field_hash,
                           'fine_independent_cone_checks':checks,
                           'fine_certificate_scope':'Complete integer native search and independent exact field decoding/inequality check; no independent high-resolution BigInt search in this short workflow.',
                           'requires_independent_high_resolution_replay':lower>CURRENT_GAME_LOWER})
    for p in directory.glob('*.work/pricing.input.bin'):p.unlink()
    result['artifacts_sha256']={str(p.relative_to(directory)):digest(p) for p in directory.rglob('*')
                                if p.is_file() and p.name!='verification.json'}
    write_json(directory/'verification.json',result)
    text=(f"## {directory.name}\n\nResult: **{result['search_result']}**. "
          f"The coarse candidate passed independent BigInt pricing.\n\n"
          f"Discrete temporal variation: {manifest['before']['temporal_total_variation']} → "
          f"{manifest['after']['temporal_total_variation']}. "
          f"Nodal temporal direction changes: {manifest['before']['temporal_direction_reversals']} → "
          f"{manifest['after']['temporal_direction_reversals']}.\n\n"
          f"Current unrestricted game lower remains {CURRENT_GAME_LOWER}; "
          "this experiment does not automatically promote a new global bound or prove optimality of the variation objective.\n")
    if os.environ.get('GITHUB_STEP_SUMMARY'):
        with open(os.environ['GITHUB_STEP_SUMMARY'],'a') as stream:stream.write(text)
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
