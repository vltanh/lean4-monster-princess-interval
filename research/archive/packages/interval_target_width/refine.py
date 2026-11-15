#!/usr/bin/env python3
"""Refine a legal CDF candidate and completely price its new integer bank.

The compact output is decoded independently after construction.  A fresh
native search supplies its finite-bank value.  The same-CDF continuum
security is never inferred; the existing 1/(2n) value transfer is explicit.
"""
from __future__ import annotations
import argparse
import base64
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import sys
import time
import zlib

import numpy as np

ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT/'packages/interval_clock_grid/normalized_native'),
              str(ROOT/'packages/interval_discovery')]
from solve_normalized import Master
from princess_search import full_seed
from verify_native_field import load_table


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def refine(source,n,output,denominator=10**9):
    started=time.monotonic()
    output.mkdir(parents=True,exist_ok=True)
    seed=full_seed(source)
    if n<seed['n'] or n%seed['n']:
        raise ValueError('target must be an integer refinement of source')
    master=Master(n,output/'work',denominator,True)
    values=master.interpolate_seed(seed)
    answer,table=master.price(values,keep=0)
    units=int(answer['minimum_units']);scale=4*n*denominator
    bank=Fraction(units,scale);lower=bank-Fraction(1,2*n)
    pre=np.concatenate([table[j,2 if j%2==0 else 1::2] for j in range(4*n+1)])
    if denominator>=2**32 or np.max(pre)>denominator:
        raise ValueError('compact integer range')
    raw=pre.astype('<u4').tobytes()
    native=ROOT/'packages/interval_clock_grid/normalized_native/price_normalized.cpp'
    certificate={
        'format':'qout-clock-grid-field-u32-zlib-v1','n':n,
        'field_denominator':str(denominator),'normalized_profile':True,
        'encoding':{'domain':'pre-two radial parity nodes in increasing time then radius',
                    'integer_type':'uint32 little-endian','compression':'zlib',
                    'count':(4*n+1)*n,'uncompressed_sha256':hashlib.sha256(raw).hexdigest()},
        'pre_two_values_base64':base64.b64encode(zlib.compress(raw,9)).decode(),
        'scope':'Complete exact normalized-bank pricing with unchanged 1/(2n) unrestricted value transfer; not a same-CDF security claim.',
        'minimum_units':str(units),'objective_denominator':str(scale),
        'normalized_bank_dual_value':str(bank),'global_lower':str(lower),
        'global_lower_decimal':float(lower),'source_seed_sha256':digest(source),
        'native_source_sha256':digest(native)}
    path=output/'field.json'
    path.write_text(json.dumps(certificate,separators=(',',':'))+'\n')
    _,decoded,input_hash=load_table(path)
    if not np.array_equal(np.asarray(decoded,dtype=np.uint64).reshape(table.shape),table):
        raise AssertionError('independent compact decoder changed priced input')
    report={'status':'PASS','scope':certificate['scope'],'n':n,
            'exact_bank_dual':str(bank),'global_value_lower':str(lower),
            'global_value_lower_decimal':float(lower),'input_sha256':input_hash,
            'verifier_source_sha256':digest(native),'pricing':answer,
            'seconds':time.monotonic()-started,'independent_bigint_replay':False}
    (output/'native.replay.json').write_text(json.dumps(report,indent=2)+'\n')
    baseline=Fraction(json.loads((ROOT/'packages/interval_clock_grid/lower_n256_field.json').read_text())['global_lower'])
    manifest={'status':'COMPLETE_NATIVE_PRICING','global_value_lower':str(lower),
              'baseline_lower':str(baseline),'native_candidate_improves_baseline':lower>baseline,
              'independent_bigint_replay':False,'same_cdf_security_claimed':False,
              'source_seed_sha256':digest(source),'source_n':seed['n'],'target_n':n,
              'elapsed_seconds':time.monotonic()-started,
              'files_sha256':{p.name:digest(p) for p in output.iterdir() if p.is_file()}}
    (output/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    return manifest


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source',type=Path,default=ROOT/'packages/interval_clock_grid/lower_n256_field.json')
    parser.add_argument('--n',type=int,default=512)
    parser.add_argument('--denominator',type=int,default=10**9)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    print(json.dumps(refine(args.source,args.n,args.output,args.denominator),indent=2),flush=True)
