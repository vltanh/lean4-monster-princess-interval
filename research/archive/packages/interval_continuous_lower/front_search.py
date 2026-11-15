#!/usr/bin/env python3
"""Incoming-front variant with a source-bound inherited bank lower floor."""
from pathlib import Path
import sys
import numpy as np

import search
from front_model import install,project

ROOT=search.ROOT
_load_table=search.load_table


def load_front_table(path):
    data,raw,sha=_load_table(path)
    n=data['n'];shape=(12*n+1,2*n+1)
    table=np.frombuffer(raw,dtype=np.uint64).reshape(shape)
    if not np.array_equal(project(n,table),table):
        raise ValueError('front search requires an exact incoming-front seed')
    if 'pricing' in data:return data,raw,sha
    if data.get('incoming_front')!='2' or 'certified_bank_lower_units' not in data:
        return data,raw,sha
    source=ROOT/'packages/interval_clock_grid/lower_n256_field.json'
    replay_path=ROOT/'packages/interval_clock_grid/lower_n256_native_replay.json'
    old,oldraw,oldsha=_load_table(source)
    replay=search.read_json(replay_path)
    if data['proof_source']['field_sha256']!=oldsha or replay['input_sha256']!=oldsha:
        raise ValueError('incoming-front source binding failed')
    if replay['verifier_source_sha256']!=search.digest(search.NATIVE/'price_normalized.cpp'):
        raise ValueError('source verifier binding failed')
    D=int(data['field_denominator'])
    if old['n']!=n or int(old['field_denominator'])!=D:raise ValueError('front/source grids differ')
    oldtable=np.frombuffer(oldraw,dtype=np.uint64).reshape(shape)
    if not np.array_equal(project(n,oldtable),table):raise ValueError('field is not the exact incoming-front projection')
    units=int(replay['pricing']['minimum_units'])
    if units!=int(old['minimum_units']) or units!=int(data['certified_bank_lower_units']):
        raise ValueError('inherited bank lower mismatch')
    data=dict(data,pricing={'status':'PASS','certifies_lower':True,'minimum_units':str(units),
        'minimum_is_exact':False,'paths':[],
        'engine':'exact incoming-front projection of an independently certified source lower',
        'engine_source_sha256':replay['verifier_source_sha256'],
        'source_field_sha256':oldsha,'projection_field_sha256':sha,
        'source_replay_sha256':search.digest(replay_path),
        'projection_theorem':'research/12-global-closure/GLOBAL_INCOMING_FRONT_COMPLETION.md',
        'scope':'Every physical bank path minimum weakly increases. This is a lower bound, not a computed new minimum.'})
    return data,raw,sha


if __name__=='__main__':
    search.EventLP=install()
    search.FRONT_TWO=True
    search.load_table=load_front_table
    original_pack=search.pack_field
    search.pack_field=lambda master,table:dict(original_pack(master,table),incoming_front='2')
    if not any(a=='--seed-field' or a.startswith('--seed-field=') for a in sys.argv):
        sys.argv+=['--seed-field',str(ROOT/'packages/interval_global_closure/lower_n256_front2_field.json')]
    search.main()
