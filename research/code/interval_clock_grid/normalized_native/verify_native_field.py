#!/usr/bin/env python3
"""Regenerate a complete integer input and replay its normalized-bank lower.

Uses only Python's standard library and a C++17 compiler. Supports the full
radial-node JSON and the exact compact pre-two Qout encoding independently of
the JavaScript decoder. The C++ validates all cone inequalities itself.
"""
import argparse
import array
import base64
from fractions import Fraction
import gzip
import hashlib
import json
from pathlib import Path
import struct
import subprocess
import sys
import tempfile
import time
import zlib


def load_table(path):
    content=path.read_bytes()
    raw=gzip.decompress(content) if path.suffix=='.gz' else content
    data=json.loads(raw);n=data['n'];D=int(data['field_denominator'])
    assert isinstance(n,int) and 1<=n<=10000 and D>0
    R,C,H=2*n,4*n,12*n
    table=array.array('Q',[0])*((H+1)*(R+1))
    if data.get('format')=='qout-clock-grid-field-u32-zlib-v1':
        assert data['normalized_profile'] is True
        count=(C+1)*n;encoding=data['encoding']
        assert encoding['count']==count and encoding['integer_type']=='uint32 little-endian'
        assert encoding['compression']=='zlib'
        packed=zlib.decompress(base64.b64decode(data['pre_two_values_base64'],validate=True))
        assert len(packed)==4*count and hashlib.sha256(packed).hexdigest()==encoding['uncompressed_sha256']
        values=array.array('I');values.frombytes(packed)
        if sys.byteorder!='little':values.byteswap()
        for j in range(H+1):
            for k in range(1,R+1):
                if (j+k)%2==0:
                    time=min(j,C);foot=k-max(0,j-C)
                    table[j*(R+1)+k]=0 if foot<=0 else values[time*n+(foot-1)//2]
    else:
        seen=bytearray(len(table))
        for j,k,a in data['radial_nodes']:
            assert isinstance(j,int) and isinstance(k,int) and 0<=j<=H and 1<=k<=R and (j+k)%2==0
            index=j*(R+1)+k;assert not seen[index]
            seen[index]=1;table[index]=int(a)
        assert sum(seen)==(H+1)*n
    assert all(a<=D for a in table)
    if data.get('normalized_profile'):
        for j in range(0,C,2):
            assert table[(j+2)*(R+1)+R]<=table[j*(R+1)+R]
        for j in range(C,H+1):
            for k in range(j%2,R+1,2):
                foot=k-j+C
                assert table[j*(R+1)+k]==(0 if foot<=0 else table[C*(R+1)+foot])
    return data,table,hashlib.sha256(content).hexdigest()


def verify(path,output=None):
    started=time.monotonic();data,table,input_hash=load_table(path)
    n,D=data['n'],int(data['field_denominator'])
    source=Path(__file__).with_name('price_normalized.cpp')
    with tempfile.TemporaryDirectory(prefix='normalized_exact_') as folder:
        root=Path(folder);binary=root/'input.bin';executable=root/'price_normalized'
        if sys.byteorder!='little':table.byteswap()
        binary.write_bytes(struct.pack('<IIQ',1,n,D)+table.tobytes())
        subprocess.run(['g++','-O3','-std=c++17',str(source),'-o',str(executable)],check=True)
        result=subprocess.run([str(executable),str(binary),'0'],check=True,text=True,stdout=subprocess.PIPE)
        replay=json.loads(result.stdout)
    units=int(replay['minimum_units']);scale=4*n*D
    assert units==int(data['minimum_units'])
    assert scale==int(data['objective_denominator'])==int(replay['objective_denominator'])
    assert Fraction(units,scale)==Fraction(data['normalized_bank_dual_value'])
    lower=Fraction(units-2*D,scale)
    assert lower==Fraction(data['global_lower'])
    answer={'status':'PASS','scope':'exact normalized-bank dual; unrestricted game-value lower uses the proved atomization, bank normalization and quantitative transfer',
            'n':n,'exact_bank_dual':str(Fraction(units,scale)),'global_value_lower':str(lower),
            'global_value_lower_decimal':float(lower),'input_sha256':input_hash,
            'verifier_source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
            'pricing':replay,'seconds':time.monotonic()-started}
    if output:output.write_text(json.dumps(answer,indent=2)+'\n')
    return answer


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('field',type=Path)
    parser.add_argument('--output',type=Path);args=parser.parse_args()
    print(json.dumps(verify(args.field,args.output),indent=2))
