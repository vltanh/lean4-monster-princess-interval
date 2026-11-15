#!/usr/bin/env python3
"""Re-evaluate a stored full field without rounding or repairing its values."""
import argparse
import json
from collections import defaultdict
from pathlib import Path

import numpy as np
from joint_cdf_field import (FieldMesh,RouteFunctional,route_pool,two_interior_pool,
                             wait_two_triangle_pool,initial_inward_pool)


def evaluate(path,extra_paths=()):
    p=json.loads(Path(path).read_text());m=FieldMesh(p['base']);values=np.asarray(p['values'])
    assert np.max(np.abs(m.nodes-np.asarray(p['nodes'])))<1e-12
    options=p.get('options',{});pool=route_pool(m)
    if options.get('include_m3'):pool.extend(two_interior_pool(m))
    if options.get('include_wait_pool'):pool.extend(wait_two_triangle_pool(m,options['constant_early_cone']))
    if options.get('include_inward_pool'):pool.extend(initial_inward_pool(m))
    for item in p.get('route_pool',{}).get('extra_routes',[]):
        pool.append(RouteFunctional(m,item['route'],item['label']))
    family={};worst=[]
    for functional in pool:
        cost=functional.value_gradient(values)[0]
        kind=functional.label['kind']
        family[kind]=min(family.get(kind,float('inf')),cost)
        worst.append(dict(cost=cost,label=functional.label))
    worst.sort(key=lambda row:row['cost'])
    extras=[]
    for name in extra_paths:
        q=json.loads(Path(name).read_text());r=q.get('field_response',q)
        cost=RouteFunctional(m,r['route'],{}).value_gradient(values)[0]
        extras.append(dict(source=Path(name).name,cost=cost,route=r['route']))
    return dict(scope='Floating evaluation of every declared fixed-route cost on the entire stored field; no unrestricted guarantee',
                input=Path(path).name,route_count=len(pool),minimum_route_cost=worst[0]['cost'],
                family_minimum=family,worst_routes=worst[:20],additional_routes=extras,
                values_were_repaired=False)


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('field')
    parser.add_argument('--extra-routes',nargs='*',default=[]);parser.add_argument('--output')
    args=parser.parse_args();result=evaluate(args.field,args.extra_routes)
    text=json.dumps(result,indent=2)+'\n'
    if args.output:Path(args.output).write_text(text)
    print(text,end='')
