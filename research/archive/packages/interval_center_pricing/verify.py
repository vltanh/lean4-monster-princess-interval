#!/usr/bin/env python3
"""Replay an exact field using the proved center-phase restriction.

The unchanged native and BigInt engines remain independent reference
implementations. This executable certifies the same normalized bank and
uses exactly the existing 1/(2n) game-value transfer.
"""
import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import struct
import subprocess
import sys
import tempfile
import time

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'packages/interval_clock_grid/normalized_native'))
from verify_native_field import load_table


def verify(path,policy=3):
    started=time.monotonic()
    data,table,input_hash=load_table(path)
    source=Path(__file__).with_name('price_center.cpp')
    n,D=data['n'],int(data['field_denominator'])
    with tempfile.TemporaryDirectory(prefix='center-pricing-replay-') as name:
        folder=Path(name);binary=folder/'field.bin';executable=folder/'price_center'
        if sys.byteorder!='little':table.byteswap()
        binary.write_bytes(struct.pack('<IIQ',1,n,D)+table.tobytes())
        subprocess.run(['g++','-O3','-std=c++17','-Wall','-Wextra',str(source),'-o',str(executable)],check=True)
        answer=json.loads(subprocess.check_output([str(executable),str(binary),'0',str(policy)],text=True))
    units=int(answer['minimum_units']);scale=4*n*D
    if 'minimum_units' in data:
        assert units==int(data['minimum_units'])
    else:
        assert units>=int(data['certified_bank_lower_units'])
    assert scale==int(data['objective_denominator'])==int(answer['objective_denominator'])
    bank=Fraction(units,scale);lower=bank-Fraction(1,2*n)
    if 'normalized_bank_dual_value' in data:
        assert bank==Fraction(data['normalized_bank_dual_value'])
        assert lower==Fraction(data['global_lower'])
    else:
        assert bank>=Fraction(data['normalized_bank_lower'])
        assert lower>=Fraction(data['global_value_lower'])
    return {'status':'PASS','scope':'Complete normalized-bank minimum using the proved center-phase equivalence; the unchanged continuum transfer gives a game-value lower, not same-CDF security.',
            'n':n,'exact_bank_dual':str(bank),'global_value_lower':str(lower),
            'global_value_lower_decimal':float(lower),'input_sha256':input_hash,
            'verifier_source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
            'proof_dependency':'research/12-global-closure/DISCRETE_CENTER_BALANCE_PRICING.md',
            'pricing':answer,'seconds':time.monotonic()-started,
            'independent_reference_replayed_in_this_step':False}


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('field',type=Path)
    parser.add_argument('--policy',type=int,choices=(0,1,2,3,4),default=3)
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    result=json.dumps(verify(args.field,args.policy),indent=2)+'\n'
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(result)
    print(result,end='')
