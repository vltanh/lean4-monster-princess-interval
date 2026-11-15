"""Exact counterexample to one rationalized monster candidate; not a game bound."""
from pathlib import Path
from fractions import Fraction
import json
from exact_response import capture

def verify(file=None):
    file=Path(file) if file else Path(__file__).resolve().parent/'rejected_dual.json'
    d=json.loads(file.read_text());S=d['scale'];weights=d['pair_weights'];p=d['princess']
    assert S>0 and weights and min(weights)>0 and sum(weights)==10**9
    assert len(weights)==len(d['monsters'])
    full=[q for m in d['monsters'] for q in (m,[[t,-x]for t,x in m])]
    for q in full+[p]:
        assert q and q[0][0]==0
        assert all(t>=0 and abs(x)<=S for t,x in q)
        assert all(b>a and abs(y-x)<=b-a for (a,x),(b,y)in zip(q,q[1:]))
    times=[capture(m,p)for m in full]
    assert times==[Fraction(t)for t in d['captured_times']]
    ww=[a for a in weights for _ in (0,1)]
    value=sum(a*t for a,t in zip(ww,times))/(sum(ww)*S)
    assert value==Fraction(d['payoff']) and value>Fraction(8,5)
    print('PASS: explicit princess defeats the rationalized monster candidate at payoff',value)
    return value
if __name__=='__main__':verify()
