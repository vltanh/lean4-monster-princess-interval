#!/usr/bin/env python3
"""Extract exact rational level-set quantile paths from a full-width Qout CDF.

The output is a NEW finite legal Princess law. Its unrestricted security
must be certified by a complete response search (or its valid frontier
lower bound); no sampled-path test or mesh transfer is a lower certificate.
"""
from __future__ import annotations

import argparse
from bisect import bisect_left, bisect_right
from fractions import Fraction as Q
import gzip
import hashlib
import json
from math import gcd
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT/'packages/interval_global_closure/record_bellman'))
from build_endpoint_tail_charts import Field, unwrap_field_data


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def read(path):
    raw = path.read_bytes()
    return json.loads(gzip.decompress(raw) if raw[:2] == b'\x1f\x8b' else raw), raw


def coarse_field(source, n):
    """Reduce a redundant integer refinement only after checking EVERY node."""
    if n == source.n:
        return source, 0
    if n <= 0 or source.n % n:
        raise ValueError('coarse grid must divide the source grid')
    m = source.n//n
    data = {'n': n, 'field_denominator': source.den,
            'radial_nodes': [[j, k, source.gnum(m*j, m*k)]
                             for j in range(4*n+1)
                             for k in range(1, 2*n+1) if (j+k)%2 == 0]}
    field = Field(data, Q(1, 2))

    def signed_node(i, w):
        t, x = i+w, i-w
        value = field.gnum(t, abs(x))
        return field.den + (1 if x > 0 else -1 if x < 0 else 0)*value

    count = 0
    for (t, x), value in source.pre.items():
        iu, u = divmod((t+x)//2, m)
        iw, w = divmod((t-x)//2, m)
        if field.orientation(iu) == field.orientation(iw):
            weights = (m-max(u,w), max(u-w,0), max(w-u,0), min(u,w))
        else:
            weights = (max(m-u-w,0), min(u,m-w), min(w,m-u), max(u+w-m,0))
        total = sum(weight*signed_node(iu+du,iw+dw)
                    for weight,(du,dw) in zip(weights, ((0,0),(1,0),(0,1),(1,1)))
                    if weight)
        if total != m*(source.den+value):
            raise ValueError(f'coarsening changes node {(t,x)}')
        count += 1
    return field, count


def mesh_edges(field):
    """All edges of the exact full-width positive-half triangulation.

    Vertex coordinates are integer physical indices (j,k)/(2n), and values
    are radial CDF numerators. The four physical domain boundaries align
    with the common-threshold diagonal selected in their light squares.
    """
    n = field.n

    def legal(i, w):
        return 0 <= i+w <= 4*n and 0 <= i-w <= 2*n

    edges = set()

    def add(a, b):
        if legal(*a) and legal(*b):
            aa, bb = (a[0]+a[1], a[0]-a[1]), (b[0]+b[1], b[0]-b[1])
            edges.add(tuple(sorted((aa,bb))))

    for i in range(-1, 3*n+1):
        for w in range(-n-1, 2*n+1):
            add((i,w),(i+1,w))
            add((i,w),(i,w+1))
            if field.orientation(i) == field.orientation(w):
                add((i,w),(i+1,w+1))
            else:
                add((i+1,w),(i,w+1))
    return [(a,b,field.gnum(*a),field.gnum(*b)) for a,b in sorted(edges)]


def clean(points):
    out = []
    for t,x in sorted(set(points)):
        if out and t == out[-1][0]:
            if x != out[-1][1]:
                raise AssertionError('a selected rank has a nonunique contour')
            continue
        out.append((t,x))
        while len(out) >= 3:
            a,b,c = out[-3:]
            if (b[1]-a[1])*(c[0]-b[0]) != (c[1]-b[1])*(b[0]-a[0]):
                break
            del out[-2]
    return out


def extract(field, count, check_points=False):
    if type(count) is not int or count < 1:
        raise ValueError('positive integer radial rank count required')
    # This offset is coprime to the field denominator. No selected rank can
    # equal ANY nodal value, avoiding flat-level tie and contour branching.
    p = field.den+1
    assert gcd(p, field.den) == 1
    ranks = [Q((2*k+1)*p+1, 2*count*p) for k in range(count)]
    assert all((q*field.den).denominator != 1 for q in ranks)
    points = [[] for _ in ranks]
    edges = mesh_edges(field)
    hits = 0
    for (j0,k0),(j1,k1),v0,v1 in edges:
        if v0 == v1:
            continue
        lo,hi = sorted((Q(v0,field.den),Q(v1,field.den)))
        first,last = bisect_right(ranks,lo),bisect_left(ranks,hi)
        for index in range(first,last):
            z = (ranks[index]*field.den-v0)/(v1-v0)
            point = (Q(j0,2*field.n)+Q(j1-j0,2*field.n)*z,
                     Q(k0,2*field.n)+Q(k1-k0,2*field.n)*z)
            points[index].append(point)
            hits += 1
    paths = []
    tests = 0
    for rank,vertices in zip(ranks,points):
        if rank > Q(field.gnum(0,2*field.n), field.den):
            assert not vertices
            route = [(Q(0),Q(1))]
        else:
            route = clean(vertices)
            assert route and route[0][0] == 0
            t,x = route[-1]
            assert x == 1 or t == 2, (rank,t,x)
            if x < 1:
                route.append((t+1-x,Q(1)))
            assert route[-1][0] <= 3
            for (ta,xa),(tb,xb) in zip(route,route[1:]):
                assert tb > ta and abs(xb-xa) <= tb-ta
                if check_points and ta < 2 and xa < 1:
                    tm,xm = (ta+tb)/2,(xa+xb)/2
                    if tm < 2 and xm < 1:
                        assert 2*field.cdf(tm,xm)-1 == rank
                        tests += 1
        paths.append(route)
    return ranks,paths,{'mesh_edges':len(edges),'contour_edge_intersections':hits,
                        'independent_midpoint_cdf_checks':tests}


def save(source_path, count, prefix, coarse=None, check_points=False):
    started = time.monotonic()
    data, raw = read(source_path)
    source = Field(data, Q(1,2))
    source_data = unwrap_field_data(data)
    if coarse is None:
        coarse = data.get('discovery_profile_grid', source_data.get('discovery_profile_grid',source.n))
    field, refined_checks = coarse_field(source, int(coarse))
    ranks, radial, statistics = extract(field,count,check_points)
    weight = Q(1,2*count)
    signed = [(weight,[(t,-x) for t,x in path]) for path in reversed(radial)]
    signed += [(weight,path) for path in radial]
    merged = []
    for w,path in signed:
        if merged and merged[-1][1] == path:
            merged[-1] = (merged[-1][0]+w,path)
        else:
            merged.append((w,path))
    assert sum(w for w,_ in merged) == 1
    text = [f'{len(merged)} 3']
    for w,path in merged:
        text.append(' '.join([str(w),str(len(path))] + [str(v) for pt in path for v in pt]))
    payload = ('\n'.join(text)+'\n').encode()
    prefix.parent.mkdir(parents=True,exist_ok=True)
    path_file = prefix.with_suffix('.paths.txt')
    path_file.write_bytes(payload)
    meta = {
        'format':'exact-fullwidth-finite-quantiles-v1',
        'scope':'A new finite rational ordered symmetric Princess law; no security bound is asserted by extraction.',
        'source_file':str(source_path),'source_sha256':digest(raw),
        'source_n':source.n,'contour_n':field.n,'interpolation_epsilon':'1/2',
        'refinement_identity_node_checks':refined_checks,
        'radial_rank_count':count,'signed_distinct_paths':len(merged),
        'rank_formula':'((2*k+1)*(D+1)+1)/(2*K*(D+1)), 0<=k<K',
        'field_denominator':str(field.den),
        'radial_ranks':[str(q) for q in ranks],
        'maximum_path_vertices':max(len(path) for _,path in merged),
        'total_path_vertices':sum(len(path) for _,path in merged),
        'paths_file':path_file.name,'paths_sha256':digest(payload),
        'statistics':statistics,'extraction_seconds':time.monotonic()-started,
    }
    prefix.with_suffix('.extraction.json').write_text(json.dumps(meta,indent=2)+'\n')
    return meta


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('source',type=Path)
    ap.add_argument('--ranks',type=int,required=True)
    ap.add_argument('--output',type=Path,required=True)
    ap.add_argument('--coarse',type=int)
    ap.add_argument('--check-points',action='store_true')
    args = ap.parse_args()
    result = save(args.source,args.ranks,args.output,args.coarse,args.check_points)
    result.pop('radial_ranks')
    print(json.dumps(result,indent=2))
