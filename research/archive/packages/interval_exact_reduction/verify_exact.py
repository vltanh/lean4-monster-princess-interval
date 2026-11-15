#!/usr/bin/env python3
"""Verify seven EXACT finite-support response suprema.
Run python verify_exact.py. Standard library only; no optimizer is invoked.
"""
import sys,json,gzip
from pathlib import Path
from fractions import Fraction as Q
from exact_oracles import princess_witness,monster_best_response,admissible
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'prior_certificate'))
from verify import build,path,H

def main(rebuild=False):
    prior=ROOT/'prior_certificate'
    spec=json.loads((prior/'strategy.json').read_text())
    with gzip.open(prior/'flows.json.gz','rt') as f:flows=json.load(f)
    cases=json.loads((ROOT/'old_strategy_best_responses.json').read_text())
    saved=None if rebuild else json.loads((ROOT/'witnesses.json').read_text())
    if saved is not None:assert len(saved)==len(cases)
    monsters=[];weights=[]
    for item in spec['families']:
        for s in [1,-1]:
            monsters.append(path(item['kind'],Q(item['start']),s))
            weights.append(Q(item['weight_numerator'],2*spec['weight_denominator']))
    assert len(monsters)==32 and sum(weights)==1 and all(w>=0 for w in weights) and all(admissible(m) for m in monsters)
    boundaries=sorted({Q(0),Q(1)}|{abs(m[0][1]) for m in monsters})
    assert len(cases)==len(flows)==len(boundaries)-1==7
    assert [list(map(Q,c['chamber'])) for c in cases]==[list(x) for x in zip(boundaries,boundaries[1:])]
    assert [r['chamber_index'] for r in flows]==list(range(7))
    allwitnesses=[]
    for case_number,(case,rec) in enumerate(zip(cases,flows)):
        a,b=map(Q,case['chamber']);initial=(a+b)/2;r=list(map(Q,case['targets']))
        edges,source,sink,scale,times=build(spec,initial)
        assert len(r)==len(monsters) and all(x in times for x in r)
        bal=[0]*(sink+1);seen=set()
        for u,v,amt in rec['arcs']:
            assert (u,v) not in seen and isinstance(amt,int) and 0<amt<=edges.get((u,v),0)
            seen.add((u,v));bal[u]+=amt;bal[v]-=amt
        F=bal[source];assert bal[sink]==-F
        bal[source]=bal[sink]=0;assert not any(bal)
        below=[m[0][1]<initial for m in monsters]
        from exact_oracles import first_meeting
        for i,m in enumerate(monsters):
            wall=Q(1) if below[i] else Q(-1)
            d=first_meeting(m,[(Q(0),wall),(H,wall)])
            assert 0<=r[i]<=d
            for j,q in enumerate(monsters):
                if below[i] and not below[j]:
                    meet=first_meeting(m,q)
                    if meet is not None:assert min(r[i],r[j])<=meet
        value=sum(w*t for w,t in zip(weights,r))
        assert value==H-Q(F,scale)==Q(case['value'])
        # These are finite rational witnesses, in addition to the all-delta theorem.
        tests=[]
        for test_number,delta in enumerate([Q(1,1000),Q(1,10000),Q(1,1000000)]):
            if rebuild:
                p,caps,gap=princess_witness(monsters,r,initial,delta,H)
            else:
                record=saved[case_number]
                assert record['chamber']==case['chamber'] and Q(record['value'])==value
                assert len(record['tests'])==3
                test=record['tests'][test_number]
                assert Q(test['delta'])==delta
                p=[(Q(t),Q(x)) for t,x in test['vertices']]
                assert admissible(p) and a<p[0][1]<b and p[-1][0]==H
                caps=[first_meeting(m,p) for m in monsters]
                assert caps==list(map(Q,test['capture_times']))
                assert all(t>=rr-delta for t,rr in zip(caps,r))
                gap=Q(test['gap'])  # Diagnostic only; not needed for the certificate.
            score=sum(w*t for w,t in zip(weights,caps))
            assert value-delta<=score<=value
            if not rebuild:assert score==Q(test['payoff'])
            tests.append({'delta':str(delta),'payoff':str(score),'gap':str(gap),
                          'vertices':[[str(t),str(x)] for t,x in p],
                          'capture_times':list(map(str,caps))})
        print(f'CLOSED ({a},{b}): exact response supremum {value}; 3 rational witnesses verified')
        allwitnesses.append({'chamber':case['chamber'],'value':str(value),'tests':tests})
    if rebuild:(ROOT/'witnesses.json').write_text(json.dumps(allwitnesses,indent=2))
    h=[[(Q(0),Q(3,4)),(Q(3,16),Q(3,4)),(Q(11,16),Q(1,4)),(Q(23,16),Q(1))],
       [(Q(0),Q(-3,4)),(Q(3,16),Q(-3,4)),(Q(11,16),Q(-1,4)),(Q(23,16),Q(-1))],
       [(Q(0),Q(1))],[(Q(0),Q(-1))]]
    result=monster_best_response(h,[Q(1,4)]*4)
    print('CLOSED four-hider response test:',result)
    encoded={k:str(v) if isinstance(v,Q) else v for k,v in result.items()}
    encoded['path']=[[str(t),str(x)] for t,x in result['path']]
    encoded['captures']=list(map(str,result['captures']))
    (ROOT/'monster_response_test.json').write_text(json.dumps(encoded,indent=2))
    print('PASS: exact response reductions checked; no claim of a full-game saddle point.')

if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--rebuild-witnesses',action='store_true',help='Reconstruct all 21 envelope witnesses instead of checking the saved paths.')
    args=parser.parse_args()
    main(rebuild=args.rebuild_witnesses)
