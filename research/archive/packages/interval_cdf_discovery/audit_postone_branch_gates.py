#!/usr/bin/env python3
"""Exact whole-cell gate certificate for the post-U1 same-half reduction.

The output is a branch-geometry certificate, not a lower game-value
certificate: it asserts no free-I or M1 cost inequalities.
"""
import argparse
from fractions import Fraction as Q
import json
from pathlib import Path

from audit_m1 import ExactField


def pack(value):
    return dict(exact=str(value), value=float(value))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('field', type=Path)
    parser.add_argument('--initial-domain', default='1/128')
    parser.add_argument('--outgoing-cut', default='1/2')
    parser.add_argument('--outgoing-slope', default='9/20')
    parser.add_argument('--endpoint-ratio', default='19/20')
    parser.add_argument('--rank-ratio', default='19/10')
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    field = ExactField(json.loads(args.field.read_text()))
    Y, Yout = Q(args.initial_domain), Q(args.outgoing_cut)
    C, kappa, gamma = Q(args.outgoing_slope), Q(args.endpoint_ratio), Q(args.rank_ratio)
    assert 0 < Y <= Yout <= 2 and C > 0 and kappa > 0 and gamma > 0
    assert gamma > 4*C and kappa*gamma >= 1
    # The physical endpoint edge is U=1+y,V=-1+y.  Its intersections
    # with either coordinate grid give every affine breakpoint.
    ys = sorted({Q(0), Q(2), Yout}
                | {1+v for v in field.grid[1] if -1 <= v <= 1}
                | {u-1 for u in field.grid[0] if 1 <= u <= 3})
    post_vertices = []
    first_min = endpoint_min = None
    for y in ys:
        e = 1-field.radial(Q(1), -1+y)
        eend = 1-field.radial(1+y, -1+y)
        row = dict(y=pack(y), e=pack(e), eend=pack(eend),
                   endpoint_slack=pack(eend-kappa*e))
        if y <= Yout:
            row['outgoing_slack'] = pack(C*y-e)
            if first_min is None or C*y-e < first_min[0]:
                first_min = (C*y-e,y)
        if endpoint_min is None or eend-kappa*e < endpoint_min[0]:
            endpoint_min = (eend-kappa*e,y)
        post_vertices.append(row)

    certificates = []
    rank_min = ratio_min = None
    probe_count = 0
    for number, (points, coefficient, orientation) in enumerate(field.triangles):
        xy = [(1-u,1+v) for u,v in points]
        if not all(0 <= x <= y <= Y for x,y in xy):
            continue
        # On each original triangle, D, r(x), and e(y) are all affine.
        # Splitting once at r=e makes D-gamma*min(r,e) affine as well.
        vertices = []
        for x,y in xy:
            vertices.append((x,y,1-field.radial(1-x,-1+y),
                             1-field.initial_value(1-x),
                             1-field.radial(Q(1),-1+y)))
        probes = vertices.copy()
        for a,b in zip(vertices,vertices[1:]+vertices[:1]):
            ga,gb = a[3]-a[4], b[3]-b[4]
            if ga*gb < 0:
                t = ga/(ga-gb)
                probes.append(tuple(aa+t*(bb-aa) for aa,bb in zip(a,b)))
        witnesses = []
        for x,y,d,r,e in probes:
            m = min(r,e)
            slack = d-gamma*m
            probe_count += 1
            witnesses.append(dict(x=pack(x),y=pack(y),d=pack(d),m=pack(m),slack=pack(slack)))
            if rank_min is None or slack < rank_min[0]:
                rank_min = (slack,x,y,number)
            if m and (ratio_min is None or d/m < ratio_min[0]):
                ratio_min = (d/m,x,y,number)
        certificates.append(dict(triangle=number,witnesses=witnesses))

    maximum_d = 1-field.initial_value(1-Y)
    outgoing_d = 1-field.radial(Q(1),-1+Yout)
    capacity = outgoing_d-maximum_d
    passed = (first_min[0] >= 0 and endpoint_min[0] >= 0
              and rank_min[0] >= 0 and capacity > 0)
    output = dict(
        scope='Exact continuous-cell sufficient geometry for arbitrary-speed same-half '
              'continuations after a terminal initial-inward prefix reaches U=1. '
              'No free-I/M1 cost inequality or all-monster game bound is asserted.',
        source_field=str(args.field.resolve()), passed=passed,
        theorem='research/10-turn-density/POSTONE_SAME_HALF_GATE.md',
        domain=dict(x='1-a',y='1+v',inequalities=f'0<=x<=y<={Y}'),
        constants=dict(C=pack(C),kappa=pack(kappa),gamma=pack(gamma),
                       gamma_minus_four_C=pack(gamma-4*C),
                       kappa_gamma_minus_one=pack(kappa*gamma-1)),
        outgoing_cut=pack(Yout), maximum_initial_domain_deficit=pack(maximum_d),
        e_at_outgoing_cut=pack(outgoing_d), capacity_slack=pack(capacity),
        exact_transport_triangles=len(field.triangles),
        post_affine_cells=len(post_vertices)-1,
        prefix_triangles=len(certificates), prefix_affine_vertex_checks=probe_count,
        outgoing_minimum=dict(slack=pack(first_min[0]),y=pack(first_min[1])),
        endpoint_minimum=dict(slack=pack(endpoint_min[0]),y=pack(endpoint_min[1])),
        rank_minimum=dict(slack=pack(rank_min[0]),x=pack(rank_min[1]),
                          y=pack(rank_min[2]),triangle=rank_min[3]),
        rank_ratio_minimum=dict(ratio=pack(ratio_min[0]),x=pack(ratio_min[1]),
                                y=pack(ratio_min[2]),triangle=ratio_min[3]),
        post_vertices=post_vertices, prefix_cell_certificates=certificates)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(output,indent=2)+'\n')
    print('PASS' if passed else 'FAIL', 'whole-cell post-one branch gates')
    for key in ['exact_transport_triangles','post_affine_cells','prefix_triangles',
                'prefix_affine_vertex_checks','capacity_slack','rank_ratio_minimum']:
        print(key,output[key])
    print('Saved',args.output)
    if not passed:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
