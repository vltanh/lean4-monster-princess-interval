#!/usr/bin/env python3
"""Compare structural center pricing with uncompressed complete responses."""
from pathlib import Path
import hashlib
import json
import random
import subprocess
import sys
import tempfile

CODE=Path(__file__).resolve().parents[1]  # research/code
NATIVE=CODE/'interval_clock_grid/normalized_native'
sys.path.insert(0,str(NATIVE))
from test_price_normalized import (binary_input, fraction_reference, independent_record_dp,
                                   legal_nodes, order_profile, replay_route, validate_profile)
from verify_native_field import load_table


def main():
    rng=random.Random(2026111402)
    cases=[];fraction_paths=0;routes=0;front_cases=[];nonfront_rejections=0
    with tempfile.TemporaryDirectory(prefix='center-pricing-') as folder:
        folder=Path(folder)
        old=folder/'old';new=folder/'center'
        for source,target in [(NATIVE/'price_normalized.cpp',old),(Path(__file__).with_name('price_center.cpp'),new)]:
            subprocess.run(['g++','-O3','-std=c++17','-Wall','-Wextra',str(source),'-o',str(target)],check=True)
        fields=[]
        for n in (1,2,3,4,6):
            R,C,H=2*n,4*n,12*n
            nodes=[(j,k) for j,k in legal_nodes(n) if k and j<=C]
            for trial in range(18):
                D=(17,101,1000000000000)[trial%3]
                seeds=[(j,k,rng.randrange(D+1)) for j,k in rng.sample(nodes,min(3+trial,len(nodes)))]
                field=order_profile(n,D,seeds)
                for j in range(C-2,-1,-2):field[j][R]=max(field[j][R],field[j+2][R])
                for j in range(C+1,H+1):
                    for k in range(j%2,R+1,2):
                        foot=k-j+C;field[j][k]=0 if foot<=0 else field[C][foot]
                fields.append((f'random_n{n}_{trial}',n,D,field))
        data,table,_=load_table(CODE/'interval_clock_grid/normalized_princess_n6_fixture.json')
        n=data['n'];R=2*n
        fields.append(('optimized_n6',n,int(data['field_denominator']),
                       [list(table[j*(R+1):(j+1)*(R+1)]) for j in range(12*n+1)]))
        for name,n,D,field in fields:
            path=folder/'input.bin';binary_input(path,n,D,field)
            reference=json.loads(subprocess.check_output([str(old),str(path),'0'],text=True))
            expected=int(reference['minimum_units'])
            if n<=2:
                independent=fraction_reference(n,D,field)
                assert independent['minimum_units']==expected
                fraction_paths+=independent['normalized_paths']
            elif name.endswith('_0') or name=='optimized_n6':
                independent=independent_record_dp(n,D,field)
                assert independent['minimum_units']==expected
            stats=[]
            for policy in (0,1,2,3):
                keep=9 if policy==2 else 0
                answer=json.loads(subprocess.check_output([str(new),str(path),str(keep),str(policy)],text=True))
                assert int(answer['minimum_units'])==expected,(name,policy,expected,answer['minimum_units'])
                for route in answer['paths']:
                    replay_route(n,D,field,route);routes+=1
                stats.append({key:answer[key] for key in ['center_policy','retained_states','generated_transitions',
                              'center_phase_pruned_moves','heavier_side_pruned_moves','peak_balance_pruned_moves']})
            cases.append({'name':name,'n':n,'minimum_units':str(expected),'policies':stats})
            R,C,H=2*n,4*n,12*n
            projected=[row.copy() for row in field]
            for j in range(H+1):
                for k in range(j%2,R+1,2):
                    if j+k>C:
                        distance=(j+k-C)//2;foot=k-distance
                        projected[j][k]=0 if foot<=0 else field[j-distance][foot]
            if projected!=field:
                rejected=subprocess.run([str(new),str(path),'0','4'],capture_output=True,text=True)
                assert rejected.returncode!=0 and 'incoming-front-two identities' in rejected.stderr
                nonfront_rejections+=1
            binary_input(path,n,D,projected)
            original=json.loads(subprocess.check_output([str(old),str(path),'0'],text=True))
            front=json.loads(subprocess.check_output([str(new),str(path),'0','4'],text=True))
            assert int(original['minimum_units'])>=expected
            assert front['minimum_units']==original['minimum_units'],(name,original,front)
            if n<=2:
                independent=fraction_reference(n,D,projected)
                assert independent['minimum_units']==int(front['minimum_units'])
                fraction_paths+=independent['normalized_paths']
            front_cases.append({'name':name,'minimum_units':front['minimum_units'],
                                'original_minimum_units':str(expected)})
        # Non-Qout fields must not silently enter the stronger proof class.
        invalid=order_profile(2,101,[(13,1,77)])
        binary_input(folder/'invalid.bin',2,101,invalid)
        rejected=subprocess.run([str(new),str(folder/'invalid.bin'),'0','2'],capture_output=True,text=True)
        assert rejected.returncode!=0 and 'outward-after-two' in rejected.stderr
    assert nonfront_rejections>0
    report={'status':'PASS','scope':'Exact center compression against unchanged full native oracle and independent Fraction/record references',
            'fields':len(cases),'policy_comparisons':4*len(cases),'fraction_paths':fraction_paths,
            'independent_route_replays':routes,'non_qout_rejection':True,
            'front_projection_comparisons':len(front_cases),
            'nonfront_field_rejections':nonfront_rejections,
            'new_source_sha256':hashlib.sha256(Path(__file__).with_name('price_center.cpp').read_bytes()).hexdigest(),
            'cases':cases,'front_cases':front_cases}
    if len(sys.argv)>1:Path(sys.argv[1]).write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ('cases','front_cases')},indent=2))


if __name__=='__main__':main()
