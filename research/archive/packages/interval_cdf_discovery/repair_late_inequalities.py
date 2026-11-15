#!/usr/bin/env python3
"""Exact rational mixture with the uniform-outward CDF R0=max(0,-V).

R0 has at least two units of slack in both optional late inequalities.
The mixture preserves transport, a constant positive cone, and the future
center-memory rank barrier.  It is a separate law, not an equilibrium
claim.  Rational values are stored explicitly; floats serve probe readers.
"""
import argparse
import json
from fractions import Fraction as Q
from pathlib import Path

from audit_snapshot import audit,coordinate


def repair(source,destination,theta=Q(1,10**6)):
    if not 0<theta<1:raise ValueError('Mixture weight must lie in (0,1)')
    p=json.loads(Path(source).read_text())
    old=[Q(value) for value in p['rational_values']] if 'rational_values' in p else [Q(str(v)) for v in p['values']]
    new=[(1-theta)*r+theta*max(Q(0),-coordinate(v)) for r,(u,v) in zip(old,p['nodes'])]
    p['values']=[float(value) for value in new]
    p['rational_values']=[str(value) for value in new]
    p['source_report']=p.pop('report',None)
    p.pop('history',None)
    p['repair']=dict(kind='exact uniform-outward CDF mixture',theta=str(theta),source=Path(source).name,
                     maximum_nodal_change=str(max(abs(a-b) for a,b in zip(new,old))),
                     note='Capture costs must be re-evaluated. No unrestricted guarantee is inferred.')
    p['provenance']='Separate rationally repaired law; exact local inequalities do not establish a matching equilibrium.'
    if 'known_attack' in p:
        p['source_known_attack']=p.pop('known_attack')
    if 'constant_early_density' in p:
        p['constant_early_density']*=float(1-theta)
    Path(destination).write_text(json.dumps(p,separators=(',',':'))+'\n')
    result=audit(destination)
    assert all(Q(item['minimum_slack'])>=0 for item in result['optional_late_inequalities'].values())
    return result


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('source');parser.add_argument('destination')
    parser.add_argument('--theta',default='1/1000000')
    parser.add_argument('--audit-output')
    args=parser.parse_args()
    result=repair(args.source,args.destination,Q(args.theta))
    text=json.dumps(result,indent=2)+'\n'
    if args.audit_output:Path(args.audit_output).write_text(text)
    print(text,end='')
