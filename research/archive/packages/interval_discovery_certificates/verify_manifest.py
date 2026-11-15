#!/usr/bin/env python3
"""Verify retained CI upper bytes, physical clocks, exact flow/cut and arithmetic.

The Python reconstruction is separate from the existing Node verifier.  Both
check the same finite all-Princess certificate; neither replays or assumes the
floating discovery optimization.  Concurrent lower fractions are arithmetic
inputs here, not lower proofs re-established by this script.
"""
from collections import defaultdict
from fractions import Fraction
from pathlib import Path
import argparse
import gzip
import hashlib
import json
import subprocess

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]


def sha(data):
    return hashlib.sha256(data).hexdigest()


def independent_upper(c):
    n=c['n'];R=2*n;C=4*n;W=int(c['weight_denominator'])
    assert isinstance(n,int) and n>0 and W>0
    assert c['pair_law']=='fair_reflection' and c['center_deadline']==2
    assert c['completion_horizon']==8 and c['physical_step']==f'1/{2*n}'
    probability=0;mass=0;pressure=defaultdict(int);prefix_checks=0;physical=set()
    for p in c['paths']:
        weight=int(p['weight_numerator']);assert weight>0;probability+=weight
        start=p['start_grid'];assert isinstance(start,int) and start%2==0 and abs(start)<=R
        positions=[start]
        for step in p['moves']:
            assert step in (-1,1)
            positions.append(positions[-1]+step);assert abs(positions[-1])<=R
        assert len(p['moves'])<=16*n
        left,right,center=positions.index(-R),positions.index(R),positions.index(0)
        assert center<=C
        physical.add((start,tuple(p['moves'])))
        for name,sign,end in [('minus_charges',1,left),('plus_charges',-1,right)]:
            charges=defaultdict(int)
            for j,amount in p[name]:
                assert isinstance(j,int) and isinstance(amount,int) and 0<=j<end and amount>0
                charges[j]+=amount
                pressure[j,sign*positions[j]]+=weight*amount
                mass+=weight*amount
            total=0
            for j in range(end):
                total+=charges[j];assert total>=j+1;prefix_checks+=1
            assert total==end
    assert probability==W
    nodes=[(j,k) for j in range(C+1) for k in range(1,R+1) if (j+k)%2==0]
    ids={point:i for i,point in enumerate(nodes)};coeff=[0]*len(nodes)
    for (j,k),value in pressure.items():
        if k==0:continue
        sign=1 if k>0 else -1;k=abs(k)
        if j>C:k-=j-C;j=C
        if k>0:coeff[ids[j,k]]+=sign*value
    positive=sum(v for v in coeff if v>0);source=len(nodes);sink=source+1
    arcs=[];hard=positive+1
    for i,value in enumerate(coeff):
        if value>0:arcs.append((source,i,value))
        elif value<0:arcs.append((i,sink,-value))
    for i,(j,k) in enumerate(nodes):
        if k<R:
            for step in (-1,1):
                if 0<=j+step<=C:arcs.append((i,ids[j+step,k+1],hard))
    for j in range(0,C,2):arcs.append((ids[j+2,R],ids[j,R],hard))
    balance=[0]*(sink+1);seen=set()
    for index,value in c['closure_flow']:
        value=int(value)
        assert isinstance(index,int) and 0<=index<len(arcs) and index not in seen
        seen.add(index);u,v,capacity=arcs[index];assert 0<value<=capacity
        balance[u]-=value;balance[v]+=value
    flow=-balance[source]
    assert flow>=0 and balance[sink]==flow and all(v==0 for v in balance[:source])
    cut_side=set(c['closure_source_side'])
    assert len(cut_side)==len(c['closure_source_side']) and source in cut_side and sink not in cut_side
    assert all(isinstance(i,int) and 0<=i<=sink for i in cut_side)
    cut=sum(capacity for u,v,capacity in arcs if u in cut_side and v not in cut_side)
    assert cut==flow
    upper=Fraction(mass+positive-flow,4*n*W)
    assert upper==Fraction(c['global_upper'])
    return {'status':'PASS','n':n,'physical_calendar_plans':len(c['paths']),
            'distinct_physical_pairs':len(physical),'checked_active_clock_prefixes':prefix_checks,
            'closure_nodes':sink+1,'closure_arcs':len(arcs),'positive_flow_entries':len(c['closure_flow']),
            'exact_flow':str(flow),'exact_cut':str(cut),'global_upper':str(upper),
            'endpoint_baseline':str(Fraction(mass,4*n*W)),
            'closure_excess':str(Fraction(positive-flow,4*n*W))}


def verify(path):
    manifest=json.loads(path.read_text());folder=path.parent
    for name,expected in manifest['files_sha256'].items():
        assert sha((folder/name).read_bytes())==expected, f'file hash mismatch: {name}'
    packed=(folder/manifest['certificate']).read_bytes();raw=gzip.decompress(packed)
    assert sha(packed)==manifest['certificate_gzip_sha256']
    assert sha(raw)==manifest['uncompressed_certificate_sha256'] and len(raw)==manifest['uncompressed_bytes']
    assert int.from_bytes(packed[4:8],'little')==manifest['gzip_mtime']==0
    certificate=json.loads(raw);python=independent_upper(certificate)
    command=['node',str(ROOT/'packages/interval_clock_grid/qout_primal_certificate.cjs'),str(folder/manifest['certificate'])]
    node=json.loads(subprocess.run(command,check=True,text=True,capture_output=True).stdout)
    saved=json.loads((folder/manifest['replay']).read_text())
    assert node==saved==manifest['exact_result']
    for key,value in python.items():
        if key in node:assert value==node[key], f'Python/Node mismatch: {key}'
    comparison=manifest['comparison'];upper=Fraction(node['global_upper'])
    lower=Fraction(comparison['concurrent_game_value_lower'])
    explicit=Fraction(comparison['concurrent_explicit_princess_security'])
    assert explicit<=lower<=upper
    assert Fraction(comparison['game_value_gap'])==upper-lower
    assert Fraction(comparison['explicit_strategy_gap'])==upper-explicit
    assert Fraction(comparison['upper_improvement'])==Fraction(comparison['previous_upper'])-upper
    return {'status':'PASS','scope':'Independent Python integer reconstruction plus existing Node replay, source-byte hashes and exact interval arithmetic. Concurrent lower certificates are not replayed.',
            'certificate_sha256':sha(packed),'uncompressed_certificate_sha256':sha(raw),
            'global_upper':str(upper),'concurrent_lower':str(lower),'gap':str(upper-lower),
            'python_replay':python,'node_replay':node}


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('manifest',type=Path,nargs='?',default=HERE/'monster_mutations_n128_manifest.json')
    args=parser.parse_args()
    print(json.dumps(verify(args.manifest.resolve()),indent=2))
