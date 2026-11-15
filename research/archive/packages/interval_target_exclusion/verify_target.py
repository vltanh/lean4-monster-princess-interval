#!/usr/bin/env python3
"""Re-enumerate every minimizing monster and verify strict target exclusion.
Python standard library only. No floating-point decision is used.
"""
from fractions import Fraction as Q
from pathlib import Path
import json
from enumerate_all import verify

def simplify(p):
    out=[]
    for t,x in p:
        out.append((Q(t),Q(x)))
        while len(out)>=3:
            (a,x),(b,y),(c,z)=out[-3:]
            if (y-x)*(c-b)==(z-y)*(b-a):out.pop(-2)
            else:break
    return tuple(out)

def main():
    root=Path(__file__).resolve().parent
    data=json.loads((root/'princess_strategy.json').read_text())
    result=verify(data)
    c=Q(56305800187,40000000000)
    assert Q(result['value'])==c
    expected=((Q(0),Q(-5,16)),(Q(131249,200000),Q(68749,200000)),
              (Q(199999,100000),Q(-1)),(Q(399999,100000),Q(1)))
    reflected=tuple((t,-x)for t,x in expected)
    got={simplify(p)for p in result['minimizers']}
    assert got=={expected,reflected}
    assert len(result['minimizers'])==2
    endpoint_payoffs=[]
    for p in got:
        endpoints=[]
        for wall in (Q(-1),Q(1)):
            hits=[t for t,x in p if x==wall]
            assert hits
            endpoints.append(min(hits))
        endpoint_payoffs.append(sum(endpoints)/2)
    b=Q(299999,100000)
    assert endpoint_payoffs==[b,b]
    assert result['integer_time_scale']==200000
    assert result['weight_denominator']==200000
    spacing=Q(1,result['integer_time_scale']*result['weight_denominator'])
    theta=Q(1,10**12)
    assert (1-theta)*spacing > theta*b
    c_theta=(1-theta)*c+theta*b
    assert c_theta>c
    report=dict(original_response=str(c),all_minimizers=2,
                endpoint_test=str(b),theta=str(theta),spacing=str(spacing),
                strict_perturbation_response=str(c_theta),nodes=result['nodes'],
                lower_bound_prunes=result['lower_bound_prunes'],
                dominance_prunes=result['dominance_prunes'],
                full_game_solved=False)
    print(json.dumps(report,indent=2))
    (root/'verified_result.json').write_text(json.dumps(report,indent=2)+'\n')

if __name__=='__main__':main()
