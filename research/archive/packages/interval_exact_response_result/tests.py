#!/usr/bin/env python3
"""Small-instance regression and exact capture-vector checks."""
from fractions import Fraction as Q
from pathlib import Path
import json
from verify import verify
from reference_unpruned import monster_best_response, first_meeting, admissible
ROOT=Path(__file__).resolve().parent
D=json.loads((ROOT/'princess_strategy.json').read_text())
R=json.loads((ROOT/'attaining_monster.json').read_text())
hs=[[(Q(t),Q(x)) for t,x in p] for p in D['paths']]
ws=list(map(Q,D['weights']))
m=[(Q(t),Q(x)) for t,x in R['path']]
assert admissible(m) and all(admissible(p) for p in hs)
assert len(hs)==60 and len(ws)==60 and sum(ws)==1
caps=[first_meeting(m,p) for p in hs]
assert [str(t) for t in caps]==R['captures']
assert sum(w*t for w,t in zip(ws,caps))==Q('56305800187/40000000000')
print('All 60 capture times and the attaining payoff checked with Fraction arithmetic.')
for c in json.loads((ROOT/'regression_cases.json').read_text()):
    d=c['data'];p=[[(Q(t),Q(x)) for t,x in z] for z in d['paths']];w=list(map(Q,d['weights']))
    a=verify(d);b=monster_best_response(p,w)
    assert Q(a['value'])==b['value']==Q(c['exact_value'])
print('All 40 regression instances agree with unpruned exact enumeration.')

D=json.loads((ROOT/'rejected_monster_candidate.json').read_text())
ms=[[(Q(t),Q(x)) for t,x in p] for p in D['monsters']]
ws=list(map(Q,D['weights']))
p=[(Q(t),Q(x)) for t,x in D['princess']]
assert admissible(p) and all(admissible(m) for m in ms) and sum(ws)==1
caps=[first_meeting(m,p) for m in ms]
assert [str(t) for t in caps]==D['captures']
assert sum(w*t for w,t in zip(ws,caps))==Q(D['payoff'])>Q(3,2)
print('The rejected monster candidate is defeated by the exact supplied princess path.')
