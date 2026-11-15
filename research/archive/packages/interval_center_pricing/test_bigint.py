#!/usr/bin/env python3
"""Compare compact BigInt target replay with the original independent engines."""
from pathlib import Path
import json
import random
import subprocess
import sys
import tempfile

from test_refinement import ROOT,NATIVE,compact,outward_sticky
from test_price_normalized import legal_nodes,order_profile,binary_input,fraction_reference


def main():
    rng=random.Random(2026111408)
    counts={'fields':0,'compact_target_passes':0,'strict_overclaim_rejections':0,
            'old_bigint_comparisons':0,'original_cpp_comparisons':0,
            'independent_fraction_paths':0,'no_pruning_passes':0,'malformed_input_rejections':0}
    with tempfile.TemporaryDirectory(prefix='compact-bigint-') as folder:
        folder=Path(folder);native=folder/'old';tool=Path(__file__).with_name('verify_bigint.cjs')
        subprocess.run(['g++','-O3','-std=c++17',str(NATIVE/'price_normalized.cpp'),'-o',str(native)],check=True)
        for n in (1,2,3,4,6):
            nodes=[(j,k) for j,k in legal_nodes(n) if k and j<=4*n]
            for trial in range(6):
                D=(17,101,2**32-5)[trial%3]
                seeds=[(j,k,rng.randrange(D+1)) for j,k in rng.sample(nodes,min(4+trial,len(nodes)))]
                field=outward_sticky(n,order_profile(n,D,seeds))
                if trial%2:
                    projected=[row.copy() for row in field]
                    for j,k in legal_nodes(n):
                        if j+k>4*n:
                            d=(j+k-4*n)//2;foot=k-d
                            projected[j][k]=0 if foot<=0 else field[j-d][foot]
                    field=projected
                binary=folder/'input.bin';binary_input(binary,n,D,field)
                original=json.loads(subprocess.check_output([str(native),str(binary),'0'],text=True))
                minimum=original['minimum_units'];data=compact(n,D,field);data['minimum_units']=minimum
                source=folder/'input.json';source.write_text(json.dumps(data,separators=(',',':'))+'\n')
                answer=json.loads(subprocess.check_output(['node',str(tool),str(source)],text=True))
                assert answer['status']=='PASS' and answer['verified_lower_units']==minimum
                counts['fields']+=1;counts['compact_target_passes']+=1;counts['original_cpp_comparisons']+=1
                rejected=subprocess.run(['node',str(tool),str(source),'--target-units',str(int(minimum)+1)],capture_output=True,text=True)
                assert rejected.returncode!=0 and 'target lower fails' in rejected.stderr
                counts['strict_overclaim_rejections']+=1
                if not answer['incoming_front_verified']:
                    failure=subprocess.run(['node',str(tool),str(source),'--front'],capture_output=True,text=True)
                    assert failure.returncode!=0 and 'incoming-front-two identities required' in failure.stderr
                    counts['malformed_input_rejections']+=1
                if n<=3:
                    old=json.loads(subprocess.check_output(['node',str(ROOT/'packages/interval_clock_grid/normalized_record_pricing.cjs'),str(source),'--target-bound'],text=True))
                    assert old['verified_lower_units']==minimum and old['global_lower']==answer['global_lower']
                    counts['old_bigint_comparisons']+=1
                if n<=2:
                    independent=fraction_reference(n,D,field)
                    assert independent['minimum_units']==int(minimum)
                    counts['independent_fraction_paths']+=independent['normalized_paths']
                if n<=3 and trial%2==1:
                    no=json.loads(subprocess.check_output(['node',str(tool),str(source),'--no-pareto','--no-pursuit','--no-front'],text=True))
                    assert no['verified_lower_units']==minimum
                    counts['no_pruning_passes']+=1
                if n==1 and trial==0:
                    bad=dict(data,encoding=dict(data['encoding'],uncompressed_sha256='0'*64))
                    invalid=folder/'invalid.json';invalid.write_text(json.dumps(bad))
                    failure=subprocess.run(['node',str(tool),str(invalid)],capture_output=True,text=True)
                    assert failure.returncode!=0 and 'length or hash' in failure.stderr
                    counts['malformed_input_rejections']+=1
                    for kind in ('range','cone','sticky'):
                        broken=[[0]*(2*n+1) for _ in range(12*n+1)]
                        if kind=='range':broken[0][2*n]=D+1
                        elif kind=='cone':broken[1][1]=D
                        else:broken[2][2*n]=D
                        malformed=compact(n,D,broken);malformed['minimum_units']='0'
                        invalid.write_text(json.dumps(malformed))
                        failure=subprocess.run(['node',str(tool),str(invalid)],capture_output=True,text=True)
                        expected={'range':'nodal range','cone':'radial transport inequality','sticky':'sticky endpoint identity'}[kind]
                        assert failure.returncode!=0 and expected in failure.stderr,(kind,failure.stderr)
                        counts['malformed_input_rejections']+=1
    report={'status':'PASS','scope':'Exact target tests, including minimum+1 counterexample rejection; no new game bound claimed.',
            'seed':2026111408,**counts}
    if len(sys.argv)>1:Path(sys.argv[1]).write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))


if __name__=='__main__':main()
