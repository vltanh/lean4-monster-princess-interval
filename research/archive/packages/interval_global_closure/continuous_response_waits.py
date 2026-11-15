#!/usr/bin/env python3
"""Replace center waits by closed unit excursions for a symmetric upper law.

The transformed reflected pair has no larger unrestricted princess-response
supremum. This is not pointwise domination against princess paths which can
touch zero. Original waits must remain in the lower-law response bank.
"""
from __future__ import annotations
import argparse
from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path


def rational(value):return value if isinstance(value,Q)else Q(str(value))


def unitize_center_waits(route,direction=1):
    """Return exact vertices, preserving all original timestamps and legs.

    Transform a representative of a reflected pair once, then reflect that
    result. Equivalently, transform the reflected input with -direction.
    Only unit legs and waits at zero are accepted; another stationary or
    slow leg is rejected rather than silently modified.
    """
    route=[tuple(map(rational,p))for p in route]
    assert route and route[0][0]==0 and direction in (-1,1)
    assert all(abs(x)<=1 for t,x in route)
    output=[route[0]]
    for(t,x),(end,y)in zip(route,route[1:]):
        assert end>=t
        if end==t:
            assert x==y;continue
        if abs(y-x)==end-t:
            output.append((end,y));continue
        assert x==y==0,('Unsupported non-unit, non-center-wait segment',(t,x),(end,y))
        current=t
        while current<end:
            duration=min(Q(2),end-current)
            output.append((current+duration/2,Q(direction)*duration/2))
            output.append((current+duration,Q(0)))
            current+=duration
    assert output[-1][0]==route[-1][0]
    assert all(s>t and abs(y-x)==s-t for(t,x),(s,y)in zip(output,output[1:]))
    return output


def convert_report(data,source_hash=None):
    """Convert every attack in a physical-DP report, keeping provenance."""
    if isinstance(data,dict)and'attacks'in data:attacks=data['attacks']
    elif isinstance(data,list):attacks=[{'route':r}for r in data]
    else:raise ValueError('Expected a physical-DP report with attacks[] or a list of routes')
    output=[];seen=set()
    for i,attack in enumerate(attacks):
        original=[tuple(map(rational,p))for p in attack['route']]
        transformed=unitize_center_waits(original)
        key=tuple(transformed)
        if key in seen:continue
        seen.add(key)
        output.append(dict(route=[[str(t),str(x)]for t,x in transformed],
                           source_attack=i,source_sha256=source_hash,
                           center_waits_replaced=sum(t<s and x==y==0 for(t,x),(s,y)in zip(original,original[1:])),
                           original_route=[[str(t),str(x)]for t,x in original],
                           original_lower_attack_payoff=attack.get('payoff')))
    return dict(scope='Unit-only reflected-pair columns with no worse global upper supremum than the original center-wait pairs; original lower-law attack costs do not transfer.',
                source_sha256=source_hash,attacks=output)


def main():
    parser=argparse.ArgumentParser();parser.add_argument('report');parser.add_argument('--output',required=True)
    args=parser.parse_args();raw=Path(args.report).read_bytes()
    result=convert_report(json.loads(raw),hashlib.sha256(raw).hexdigest())
    Path(args.output).write_text(json.dumps(result,indent=2)+'\n')
    print(len(result['attacks']),'unit-only pair columns;',sum(a['center_waits_replaced']for a in result['attacks']),'center waits replaced')


if __name__=='__main__':main()
