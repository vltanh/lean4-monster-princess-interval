#!/usr/bin/env python3
"""Exact physical-cone and declared-selection audit for a saved affine CDF.

This audits the realized field, not an unrestricted monster guarantee.
The intended rational coordinate mesh is recovered within 1e-14 from its
JSON floats; values are read as exact decimal rationals.
"""
import argparse
import json
from fractions import Fraction as Q
from pathlib import Path


def coordinate(value):
    answer=Q(str(value)).limit_denominator(2**22)
    assert abs(float(answer)-value)<1e-14
    return answer


def audit(path):
    p=json.loads(Path(path).read_text())
    nodes=[tuple(map(coordinate,point)) for point in p['nodes']]
    values=[Q(value) for value in p['rational_values']] if 'rational_values' in p else [Q(str(value)) for value in p['values']]
    assert all(0<=value<=1 for value in values)
    index={point:i for i,point in enumerate(nodes)}
    assert values[index[Q(0),Q(0)]]==0
    assert values[index[Q(1),Q(-1)]]==1
    assert all(values[i]==0 for i,(u,v) in enumerate(nodes) if v==1)
    slopes=[]
    min_late={'positive_v':None,'negative_v':None}
    negative_late={'positive_v':0,'negative_v':0}
    for triangle in p['triangles']:
        i,j,k=triangle
        u0,v0=nodes[i];u1,v1=nodes[j];u2,v2=nodes[k]
        r0,r1,r2=values[i],values[j],values[k]
        du1,dv1,du2,dv2=u1-u0,v1-v0,u2-u0,v2-v0
        determinant=du1*dv2-du2*dv1
        ru=((r1-r0)*dv2-(r2-r0)*dv1)/determinant
        rv=(du1*(r2-r0)-du2*(r1-r0))/determinant
        assert ru>=0 and rv<=0,('transport violation',triangle,ru,rv)
        slopes.append((ru,-rv))
        if min(u0,u1,u2)<1:continue
        positive=min(v0,v1,v2)>=0
        negative=max(v0,v1,v2)<=0
        if not (positive or negative):continue
        key='positive_v' if positive else 'negative_v'
        for vertex in triangle:
            u,v=nodes[vertex]
            a=values[index[abs(v),-abs(v)]]
            slack=4-(6+u-v)*ru-2*values[vertex]-(2*a if positive else -a)
            if min_late[key] is None or slack<min_late[key]:min_late[key]=slack
            if slack<0:negative_late[key]+=1
    result=dict(scope='Exact realized-CDF legality and declared local conditions; no unrestricted payoff certificate',
                input=Path(path).name,nodes=len(nodes),triangles=len(slopes),
                transport_cone='PASS',minimum_R_U=str(min(s[0] for s in slopes)),
                minimum_minus_R_V=str(min(s[1] for s in slopes)),
                initial_center_atom=0,initial_endpoint_atom=0,outgoing_time_one_atom=0,
                optional_late_inequalities={key:dict(minimum_slack=str(value),
                                                   minimum_slack_float=float(value),
                                                   negative_vertex_rows=negative_late[key])
                                            for key,value in min_late.items() if value is not None})
    options=p.get('options',{})
    if options.get('constant_early_cone') is not None:
        tau=coordinate(options['constant_early_cone'])
        density=values[index[tau,Q(0)]]/tau
        count=0
        for i,(u,v) in enumerate(nodes):
            if 0<=v<=u<=tau:
                assert values[i]==density*u,('constant cone',u,v)
                count+=1
        result['constant_early_cone']=dict(cutoff=str(tau),density=str(density),
                                           density_float=float(density),checked_nodes=count,status='PASS')
    if options.get('terminal_barrier') is not None:
        tau=coordinate(options['terminal_barrier'])
        peak=values[index[tau,tau]]
        future=[values[i] for i,(u,v) in enumerate(nodes) if u-v==2 and v>=tau]
        assert future and max(future)<=peak
        past=[values[i] for i,(u,v) in enumerate(nodes) if u==v and u<=tau]
        result['future_rank_barrier']=dict(cutoff=str(tau),rank=str(peak),
                                           rank_float=float(peak),future_interior_envelope=str(max(future)),
                                           past_center_maximum=str(max(past)),
                                           checked_boundary_nodes=len(future),status='PASS')
    return result


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('field')
    parser.add_argument('--output')
    args=parser.parse_args()
    result=audit(args.field)
    text=json.dumps(result,indent=2)+'\n'
    if args.output:Path(args.output).write_text(text)
    print(text,end='')
