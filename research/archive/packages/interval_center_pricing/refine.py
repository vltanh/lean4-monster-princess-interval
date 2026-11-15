#!/usr/bin/env python3
"""Exactly interpolate a supplied field and completely price its finer bank.

No LP is assembled and no floating interpolation is used. When the refined
denominator fits uint32, the full-width common-threshold field is preserved
exactly. Otherwise the legal nodal values are explicitly floored. Neither
case assigns the transferred game lower to the same continuous CDF.
"""
import argparse
import base64
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import struct
import subprocess
import sys
import time
import zlib

import numpy as np

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'packages/interval_clock_grid/normalized_native'))
from verify_native_field import load_table


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def interpolate(source,n,denominator=None):
    data,flat,_=load_table(source)
    old,D0=data['n'],int(data['field_denominator'])
    if n<old or n%old:raise ValueError('target must be an integer refinement')
    factor=n//old;exact_denominator=factor*D0
    D=(exact_denominator if exact_denominator<2**32 else 10**9) if denominator is None else denominator
    if not 0<D<2**32:raise ValueError('uint32 field denominator required')
    original=np.asarray(flat,dtype=np.uint64).reshape(12*old+1,2*old+1)
    R,C,H=2*n,4*n,12*n
    table=np.zeros((H+1,R+1),dtype=np.uint64)
    for j in range(C+1):
        k=np.arange(2 if j%2==0 else 1,R+1,2,dtype=np.int64)
        iu,a=np.divmod((j+k)//2,factor);iw,b=np.divmod((j-k)//2,factor)
        same=(iu%(2*old)<old)==(iw%(2*old)<old)
        weights=[np.where(same,factor-np.maximum(a,b),np.maximum(factor-a-b,0)),
                 np.where(same,np.maximum(a-b,0),np.minimum(a,factor-b)),
                 np.where(same,np.maximum(b-a,0),np.minimum(b,factor-a)),
                 np.where(same,np.minimum(a,b),np.maximum(a+b-factor,0))]
        total=np.zeros(n,dtype=np.int64)
        for weight,(du,dw) in zip(weights,((0,0),(1,0),(0,1),(1,1))):
            tj=iu+du+iw+dw;rk=iu+du-iw-dw;active=weight>0
            assert np.all((tj[active]>=0)&(tj[active]<=12*old)&(abs(rk[active])<=2*old))
            node=original[tj[active],abs(rk[active])].astype(np.int64)*np.sign(rk[active])
            total[active]+=weight[active]*node
        assert np.all((total>=0)&(total<=exact_denominator))
        if D==exact_denominator:values=total
        elif exact_denominator*D<=np.iinfo(np.int64).max:
            values=total*D//exact_denominator
        else:
            values=np.fromiter((int(x)*D//exact_denominator for x in total),dtype=np.uint64,count=n)
        table[j,k]=values
    for j in range(C+1,H+1):
        k=np.arange(1 if j%2 else 2,R+1,2,dtype=np.int64);foot=k-j+C
        active=foot>0;table[j,k[active]]=table[C,foot[active]]
    return data,D,table,D==exact_denominator


def refine(source,n,output,policy=3,denominator=None,classic=False):
    started=time.monotonic();output.mkdir(parents=True,exist_ok=True)
    work=output/'work';work.mkdir(exist_ok=True)
    source_data,D,table,exact=interpolate(source,n,denominator)
    pre=np.concatenate([table[j,2 if j%2==0 else 1::2] for j in range(4*n+1)])
    packed=pre.astype('<u4').tobytes()
    certificate={'format':'qout-clock-grid-field-u32-zlib-v1','n':n,
        'field_denominator':str(D),'normalized_profile':True,
        'encoding':{'domain':'pre-two radial parity nodes in increasing time then radius',
          'integer_type':'uint32 little-endian','compression':'zlib','count':(4*n+1)*n,
          'uncompressed_sha256':hashlib.sha256(packed).hexdigest()},
        'pre_two_values_base64':base64.b64encode(zlib.compress(packed,9)).decode(),
        'source_seed_sha256':sha(source),'exact_fullwidth_refinement':exact,
        'scope':'Complete normalized-bank minimum with the existing 1/(2n) game-value transfer. No same-CDF security claim.'}
    prepared=output/'prepared.field.json'
    prepared.write_text(json.dumps(certificate,separators=(',',':'))+'\n')
    _,decoded,_=load_table(prepared)
    assert np.array_equal(np.asarray(decoded,dtype=np.uint64).reshape(table.shape),table)
    binary=work/'pricing.input.bin'
    binary.write_bytes(struct.pack('<IIQ',1,n,D)+table.astype('<u8').tobytes())
    source_cpp=Path(__file__).with_name('price_center.cpp');executable=work/'price_center'
    subprocess.run(['g++','-O3','-std=c++17',str(source_cpp),'-o',str(executable)],check=True)
    answer=json.loads(subprocess.check_output([str(executable),str(binary),'0',str(policy)],text=True))
    units=int(answer['minimum_units']);scale=4*n*D
    bank=Fraction(units,scale);lower=bank-Fraction(1,2*n)
    certificate.update(minimum_units=str(units),objective_denominator=str(scale),
        normalized_bank_dual_value=str(bank),global_lower=str(lower),global_lower_decimal=float(lower),
        native_source_sha256=sha(source_cpp),center_policy=policy)
    target=output/'field.json';target.write_text(json.dumps(certificate,separators=(',',':'))+'\n')
    report={'status':'PASS','scope':certificate['scope'],'n':n,'exact_bank_dual':str(bank),
        'global_value_lower':str(lower),'global_value_lower_decimal':float(lower),
        'input_sha256':sha(target),'verifier_source_sha256':sha(source_cpp),'pricing':answer,
        'seconds':time.monotonic()-started,'independent_original_replay':False,
        'independent_bigint_replay':False}
    if classic:
        reference=ROOT/'packages/interval_clock_grid/normalized_native/price_normalized.cpp'
        other=work/'price_normalized'
        subprocess.run(['g++','-O3','-std=c++17',str(reference),'-o',str(other)],check=True)
        original=json.loads(subprocess.check_output([str(other),str(binary),'0'],text=True))
        assert original['minimum_units']==answer['minimum_units']
        report['independent_original_replay']=True
        (output/'original.replay.json').write_text(json.dumps({'input_sha256':sha(target),
          'verifier_source_sha256':sha(reference),'pricing':original},indent=2)+'\n')
    (output/'center.replay.json').write_text(json.dumps(report,indent=2)+'\n')
    manifest={'status':'COMPLETE_EXACT_CENTER_PRICING','source_n':source_data['n'],'target_n':n,
        'global_value_lower':str(lower),'source_seed_sha256':sha(source),
        'exact_fullwidth_refinement':exact,'center_policy':policy,
        'independent_original_replay':classic,'independent_bigint_replay':False,
        'same_cdf_security_claimed':False,'elapsed_seconds':time.monotonic()-started,
        'files_sha256':{p.name:sha(p) for p in output.iterdir() if p.is_file() and p.name!='manifest.json'}}
    (output/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    return manifest


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--source',type=Path,required=True);p.add_argument('--n',type=int,required=True)
    p.add_argument('--output',type=Path,required=True);p.add_argument('--denominator',type=int)
    p.add_argument('--policy',type=int,choices=(0,1,2,3,4),default=3)
    p.add_argument('--classic',action='store_true')
    a=p.parse_args()
    print(json.dumps(refine(a.source,a.n,a.output,a.policy,a.denominator,a.classic),indent=2),flush=True)
