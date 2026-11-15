#!/usr/bin/env python3
"""Exact certificate verification using only Python's standard library.

Certifies the fixed 32-path support minimax problem, and certifies that this
support cannot be optimal for the unrestricted game. DOES NOT solve that game.
No numerical optimizer, networkx, or floating-point comparisons are used.
"""
from fractions import Fraction as Q
from math import lcm
from pathlib import Path
import gzip,json,subprocess,sys
from network import build,path,first_meeting,H
from exact_paths import normalize,admissible,position
ROOT=Path(__file__).resolve().parent

def load_spec(filename):
    spec=json.load(open(ROOT/filename));den=spec['weight_denominator']
    assert isinstance(den,int) and den>0
    assert all(isinstance(x['weight_numerator'],int) and x['weight_numerator']>0 for x in spec['families'])
    assert sum(x['weight_numerator'] for x in spec['families'])==den
    ms=[];ws=[]
    for x in spec['families']:
        assert -1<=Q(x['start'])<1
        ms.extend([path(x['kind'],x['start'],1),path(x['kind'],x['start'],-1)])
        ws.extend([Q(x['weight_numerator'],2*den)]*2)
    assert all(admissible(m) for m in ms)
    return spec,ms,ws

def feasible(ms,r,initial):
    assert all(m[0][1]!=initial for m in ms)
    below=[m[0][1]<initial for m in ms]
    for i,m in enumerate(ms):
        d=first_meeting(m,[(Q(0),Q(1 if below[i] else -1)),(H,Q(1 if below[i] else -1))])
        assert d is not None and 0<=r[i]<=d
    for i in range(len(ms)):
        if not below[i]:continue
        for j in range(len(ms)):
            if below[j]:continue
            t=first_meeting(ms[i],ms[j])
            if t is not None:assert min(r[i],r[j])<=t

def verify_flows(spec,ms,ws,filename,expected=None):
    with gzip.open(ROOT/filename,'rt') as f:records=json.load(f)
    positions=sorted(set([Q(0),Q(1)]+[abs(Q(x['start'])) for x in spec['families']]))
    assert len(records)==len(positions)-1
    bounds=[]
    for k,(record,a,b) in enumerate(zip(records,positions,positions[1:])):
        initial=(a+b)/2
        assert record['chamber_index']==k and Q(record['initial'])==initial
        caps,s,t,scale,ts=build(spec,initial);bal=[0]*(t+1);used=set()
        for u,v,f in record['arcs']:
            assert all(isinstance(x,int) for x in (u,v,f))
            assert (u,v) not in used;used.add((u,v))
            assert 0<f<=caps.get((u,v),0)
            bal[u]+=f;bal[v]-=f
        F=bal[s];assert F>=0 and bal[t]==-F
        bal[s]=bal[t]=0;assert not any(bal)
        assert F==record['value'] and scale==record['scale']
        upper=H-Q(F,scale);bounds.append(upper)
        if expected is not None:assert upper==expected
        if 'deadlines' in record:
            r=list(map(Q,record['deadlines']));feasible(ms,r,initial)
            assert sum(w*z for w,z in zip(ws,r))==upper
    return max(bounds),len(records)

def main():
    D=json.load(open(ROOT/'certificate.json'));v=Q(D['value'])
    spec,ms,ws=load_spec('strategy.json')
    assert len(ms)==32
    assert ws==[Q(w)/2 for w in D['weights'] for _ in range(2)]
    for m,p in zip(ms,D['paths']):
        p=normalize(p)
        for t in set(t for t,x in m+p):assert position(m,t)==position(p,t)
    q=list(map(Q,D['duals']));assert all(z>0 for z in q) and sum(q)==1
    rs=[list(map(Q,r)) for r in D['deadlines']]
    assert len(q)==len(rs)==len(D['initials'])==16
    A=[]
    for r,initial in zip(rs,D['initials']):
        assert len(r)==32;feasible(ms,r,Q(initial))
        A.append([(r[2*j]+r[2*j+1])/2 for j in range(16)])
    assert A==[[Q(x) for x in row] for row in D['matrix']]
    for j in range(16):assert sum(q[i]*A[i][j] for i in range(16))==v
    for row in A:assert sum(row[j]*Q(D['weights'][j]) for j in range(16))==v
    upper,n=verify_flows(spec,ms,ws,'flows.json.gz',v)
    print('PASS: exact primal and dual equalities; all seven starting chambers.')
    print('Fixed-support minimax value:',v)
    spec2,ms2,ws2=load_spec('exclusion_strategy.json')
    upper2,n2=verify_flows(spec2,ms2,ws2,'exclusion_flows.json.gz')
    E=json.load(open(ROOT/'support_exclusion.json'))
    assert upper2==Q(E['upper']) and Q(E['restricted_value'])==v
    assert v-upper2==Q(E['strict_gap'])>0
    print('PASS: a different monster mixture has a strictly smaller unrestricted upper guarantee.')
    print('Therefore none of the reweightings of the original 32 paths is globally optimal.')
    subprocess.run([sys.executable,str(ROOT/'check_symbolic.py'),'--check'],check=True)
    print('PASS: displayed approaching dual family is defeated by the explicit omitted monster.')
    print('SCOPE: this is NOT an exact solution of the unrestricted game.')

if __name__=='__main__':main()
