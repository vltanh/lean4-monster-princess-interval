#!/usr/bin/env python3
"""Independent exact CDF checks for pure-integer common-threshold refinement.

The reference evaluates Field.cdf by Fraction threshold averaging. It does
not use the four-vector interpolation formula being tested. Endpoint CDF
queries use the field's prescribed interior trace convention.
"""
from fractions import Fraction as Q
from pathlib import Path
import base64
import gzip
import hashlib
import json
import random
import struct
import subprocess
import sys
import tempfile
import zlib

import numpy as np

ROOT=Path(__file__).resolve().parents[2]
NATIVE=ROOT/'packages/interval_clock_grid/normalized_native'
sys.path[:0]=[str(NATIVE),str(ROOT/'packages/interval_quantile_certificate')]
from test_price_normalized import legal_nodes,order_profile,binary_input,fraction_reference
from extract_quantiles import Field
from refine import interpolate


def compact(n,D,table):
    values=[int(table[j][k]) for j in range(4*n+1)
            for k in range(1,2*n+1) if (j+k)%2==0]
    raw=struct.pack('<'+'I'*len(values),*values)
    return {'format':'qout-clock-grid-field-u32-zlib-v1','n':n,
        'field_denominator':str(D),'normalized_profile':True,
        'encoding':{'count':len(values),'integer_type':'uint32 little-endian',
                    'compression':'zlib','uncompressed_sha256':hashlib.sha256(raw).hexdigest()},
        'pre_two_values_base64':base64.b64encode(zlib.compress(raw)).decode()}


def outward_sticky(n,field):
    R,C,H=2*n,4*n,12*n
    for j in range(C-2,-1,-2):field[j][R]=max(field[j][R],field[j+2][R])
    for j in range(C+1,H+1):
        for k in range(j%2,R+1,2):
            foot=k-j+C
            field[j][k]=0 if foot<=0 else field[C][foot]
    return field


def check_local_order(n,D,table):
    R,C,H=2*n,4*n,12*n
    for j,k in legal_nodes(n):
        value=int(table[j][k])
        assert 0<=value<=D and (k or value==0)
        if k<R:
            for dt in (-1,1):
                if 0<=j+dt<=H:assert value<=int(table[j+dt][k+1])
    for j in range(0,C,2):assert int(table[j+2][R])<=int(table[j][R])
    for j in range(C,H+1):
        for k in range(j%2,R+1,2):
            foot=k-j+C
            assert int(table[j][k])==(0 if foot<=0 else int(table[C][foot]))


def main():
    rng=random.Random(2026111407)
    counts={'source_fields':0,'refinement_cases':0,'exact_refinements':0,
            'floored_refinements':0,'parity_node_cdf_comparisons':0,
            'negative_node_symmetry_checks':0,'nonnodal_cdf_comparisons':0,
            'large_product_floor_cases':0,'changed_rational_nodes':0,
            'original_native_center_comparisons':0,'independent_fraction_paths':0,
            'invalid_parameter_rejections':0}
    native_cases=[]
    with tempfile.TemporaryDirectory(prefix='exact-refinement-') as folder:
        folder=Path(folder);old=folder/'original';new=folder/'center'
        for cpp,exe in ((NATIVE/'price_normalized.cpp',old),
                        (Path(__file__).with_name('price_center.cpp'),new)):
            subprocess.run(['g++','-O3','-std=c++17',str(cpp),'-o',str(exe)],check=True)
        fields=[]
        for n in (1,2,3):
            nodes=[(j,k) for j,k in legal_nodes(n) if k and j<=4*n]
            for trial,D in enumerate((17,101,2**32-5,101)):
                seeds=[(j,k,rng.randrange(D+1)) for j,k in rng.sample(nodes,min(4+trial,len(nodes)))]
                fields.append((n,D,outward_sticky(n,order_profile(n,D,seeds)),f'random_{n}_{trial}'))
            for value,name in ((0,'zero'),(101,'saturated')):
                field=[[value if k and (j+k)%2==0 else 0 for k in range(2*n+1)] for j in range(12*n+1)]
                fields.append((n,101,outward_sticky(n,field),f'{name}_{n}'))
        for case,(n,D0,field,name) in enumerate(fields):
            data=compact(n,D0,field)
            # Exercise both established input formats and gzip decoding.
            if case%2:
                data={'n':n,'field_denominator':str(D0),'normalized_profile':True,
                      'radial_nodes':[[j,k,str(field[j][k])] for j,k in legal_nodes(n) if k]}
            source=folder/(name+('.json.gz' if case%3==0 else '.json'))
            raw=(json.dumps(data,separators=(',',':'))+'\n').encode()
            source.write_bytes(gzip.compress(raw,mtime=0) if source.suffix=='.gz' else raw)
            reference=Field(data,Q(1,2));counts['source_fields']+=1
            for factor in (1,2,3,4):
                target=n*factor
                for requested in (None,37,2**32-17):
                    _,D,table,exact=interpolate(source,target,requested)
                    counts['refinement_cases']+=1
                    counts['exact_refinements' if exact else 'floored_refinements']+=1
                    if D*factor*D0>np.iinfo(np.int64).max:counts['large_product_floor_cases']+=1
                    assert exact==(D==factor*D0)
                    if requested is not None:assert D==requested
                    check_local_order(target,D,table)
                    for j,k in legal_nodes(target):
                        value=2*reference.cdf(Q(j,2*target),Q(k,2*target))-1
                        expected=(value*D).numerator//(value*D).denominator
                        assert int(table[j][k])==expected,(name,factor,requested,j,k,value,int(table[j][k]))
                        error=value-Q(expected,D)
                        assert 0<=error<Q(1,D)
                        if error:counts['changed_rational_nodes']+=1
                        if exact:assert error==0
                        counts['parity_node_cdf_comparisons']+=1
                        if k:
                            assert reference.cdf(Q(j,2*target),Q(-k,2*target))==(1-value)/2
                            counts['negative_node_symmetry_checks']+=1
                    refined=Field(compact(target,D,table),Q(1,2))
                    for _ in range(7):
                        t=Q(rng.randrange(6*97+1),97)
                        x=Q(rng.randrange(-83,84),83)
                        before=reference.cdf(t,x);after=refined.cdf(t,x)
                        if exact:assert before==after,(name,factor,t,x,before,after)
                        else:assert abs(before-after)<Q(1,2*D)
                        counts['nonnodal_cdf_comparisons']+=1
                    # Selected independent complete original vs center prices;
                    # interpolation itself was checked on EVERY case above.
                    if factor==2 and case%6 in (0,2) and requested in (None,37):
                        binary=folder/'pricing.bin';binary_input(binary,target,D,table)
                        a=json.loads(subprocess.check_output([str(old),str(binary),'0'],text=True))
                        b=json.loads(subprocess.check_output([str(new),str(binary),'0','3'],text=True))
                        assert a['status']==b['status']=='PASS'
                        assert a['minimum_units']==b['minimum_units']
                        assert int(a['objective_denominator'])==4*target*D
                        if target<=2:
                            # Fraction must receive Python ints, never NumPy
                            # uint64 scalars whose arithmetic can wrap before
                            # Fraction's normalization sees the result.
                            independent=fraction_reference(target,D,table.tolist())
                            assert int(a['minimum_units'])==independent['minimum_units']
                            counts['independent_fraction_paths']+=independent['normalized_paths']
                        counts['original_native_center_comparisons']+=1
                        native_cases.append({'source':name,'n':target,'denominator':str(D),
                                             'exact_fullwidth_refinement':exact,'minimum_units':a['minimum_units']})
            for target,denominator in ((n-1,None),(n,0),(n,-1),(n,2**32)):
                try:interpolate(source,target,denominator)
                except ValueError:counts['invalid_parameter_rejections']+=1
                else:raise AssertionError('invalid refinement parameters accepted')
            if n>1:
                try:interpolate(source,n+1)
                except ValueError:counts['invalid_parameter_rejections']+=1
                else:raise AssertionError('noninteger refinement accepted')
    assert counts['changed_rational_nodes'] and counts['large_product_floor_cases']
    report={'status':'PASS','scope':'Integer refinement checked against independent exact common-threshold CDF averaging; no new game bound claimed.',
            'seed':2026111407,**counts,'native_cases':native_cases,
            'refinement_source_sha256':hashlib.sha256(Path(__file__).with_name('refine.py').read_bytes()).hexdigest()}
    if len(sys.argv)>1:Path(sys.argv[1]).write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='native_cases'},indent=2))


if __name__=='__main__':main()
