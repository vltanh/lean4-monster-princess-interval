#!/usr/bin/env python3
"""Exact physical capture checks for the added uniform-inward feature.

The two-dimensional density integral is independently partitioned into
rational polygons in (a,v).  Every cost value comes from direct polygonal
path intersections, not from the inverse-graph feature or its alpha/beta
formula.  Interior quadrature avoids substituting a limiting payoff for
first touch on a capture discontinuity.
"""
from fractions import Fraction as Q
import numpy as np

from uniform_inward import UniformInward, graph_from_path
from uniform_inward_features import uniform_inward_feature_row
from verify_center_memory import first_capture


def monster(a, v):
    vertices = [(Q(0),a), ((a+v)/2,(a-v)/2),
                ((1+v)/2,(1-v)/2), (Q(2),Q(-1)), (Q(4),Q(1))]
    result = []
    for point in vertices:
        if not result or point != result[-1]:
            result.append(point)
    return result


def direct_four(path, a, v):
    route = monster(a,v)
    positive, negative = (first_capture(path,route,sign) for sign in (1,-1))
    assert positive is not None and negative is not None
    return 2*(positive+negative)


def inverse(path, level, plus):
    """First closed inverse, used only for the separate pointwise identity."""
    start = path[0][1] if plus else -path[0][1]
    if level <= start:
        return Q(0)
    for (s,x),(t,y) in zip(path,path[1:]):
        left = s+x if plus else s-x
        right = t+y if plus else t-y
        if left <= level <= right:
            if left == level:
                return s
            return s+(t-s)*(level-left)/(right-left)
    raise ValueError("Inverse beyond supplied horizon")


def pointwise_four(path, a, v):
    b = path[0][1]
    alpha_a, alpha_1 = inverse(path,a,True), inverse(path,Q(1),True)
    beta_v, beta_1, beta_3 = (inverse(path,x,False) for x in (v,Q(1),Q(3)))
    if b <= a:
        positive = alpha_a if 2*alpha_a-a <= v else alpha_1
    else:
        positive = beta_v if 2*beta_v-v <= 1 else beta_3
    return 2*(positive+beta_1)


def clip(polygon, line, positive):
    aa, vv, cc = line
    def side(point):
        value = aa*point[0]+vv*point[1]+cc
        return value if positive else -value
    result = []
    for p,q in zip(polygon,polygon[1:]+polygon[:1]):
        fp,fq = side(p),side(q)
        if fp >= 0:
            result.append(p)
        if fp*fq < 0:
            fraction = fp/(fp-fq)
            result.append((p[0]+fraction*(q[0]-p[0]),p[1]+fraction*(q[1]-p[1])))
    clean = []
    for p in result:
        if not clean or p != clean[-1]:
            clean.append(p)
    if len(clean)>1 and clean[0]==clean[-1]:
        clean.pop()
    return clean


def twice_area(poly):
    return abs(sum((p[0]*q[1]-p[1]*q[0] for p,q in zip(poly,poly[1:]+poly[:1])),Q(0)))


def arrangements(path, left, right, top=None):
    b,c,_ = graph_from_path(path)
    lines = {(Q(1),Q(0),-b), (Q(0),Q(1),-c)}
    for time,radius in path:
        u,v = time+radius,time-radius
        if 0 < u < 1:
            lines.add((Q(1),Q(0),-u))
        if -1 < v < 1:
            lines.add((Q(0),Q(1),-v))
    for (s,x),(t,y) in zip(path,path[1:]):
        if s >= 1:
            continue
        velocity = (y-x)/(t-s)
        intercept = x-velocity*s
        # Equality at the first monster turn, whose coordinates are
        # ((a+v)/2,(a-v)/2).  Inactive segment lines merely overpartition.
        lines.add((1-velocity,-1-velocity,-2*intercept))
    polygon = ([(left,-left),(right,-right),(right,right),(left,left)] if top is None else
               [(left,-left),(right,-right),(right,top),(left,top)])
    polygon = [p for i,p in enumerate(polygon) if i==0 or p!=polygon[i-1]]
    original_area = twice_area(polygon)
    polygons = [polygon]
    for line in sorted(lines):
        next_polygons = []
        for polygon in polygons:
            values = [line[0]*a+line[1]*v+line[2] for a,v in polygon]
            if min(values)<0<max(values):
                for positive in (False,True):
                    piece = clip(polygon,line,positive)
                    if len(piece)>=3 and twice_area(piece)>0:
                        next_polygons.append(piece)
            else:
                next_polygons.append(polygon)
        polygons = next_polygons
    assert sum((twice_area(poly) for poly in polygons),Q(0)) == original_area
    return polygons


def physical_integral(path, density):
    total, triangles = Q(0), 0
    for left,right,height in zip(density.knots,density.knots[1:],density.heights):
        if height == 0:
            continue
        for polygon in arrangements(path,left,right):
            for i in range(1,len(polygon)-1):
                vertices = [polygon[0],polygon[i],polygon[i+1]]
                area = twice_area(vertices)/2
                if area == 0:
                    continue
                centroid = tuple(sum((p[k] for p in vertices),Q(0))/3 for k in (0,1))
                middle = direct_four(path,*centroid)
                # These are strictly interior to the triangle/capture cell.
                checks = []
                for distinguished in range(3):
                    point = tuple(sum((vertices[j][k]*(Q(2,3) if j==distinguished else Q(1,6))
                                       for j in range(3)),Q(0)) for k in (0,1))
                    checks.append(direct_four(path,*point))
                assert sum(checks,Q(0))/3 == middle, (path,vertices,checks,middle)
                total += height*area*middle
                triangles += 1
    return total,triangles


def ceiling_gap(path, density, b, c):
    """Exact loss of the three explicitly stated upper relaxations."""
    alpha_1 = inverse(path,Q(1),True)
    beta_1, beta_3 = (inverse(path,level,False) for level in (Q(1),Q(3)))
    cuts = {Q(0),Q(1),b,abs(c),*density.knots}
    cuts.update(t+p for t,p in path if 0<t+p<1)
    cuts = sorted(x for x in cuts if 0<=x<=1)
    lower_missed, higher_missed = Q(0),Q(0)
    for left,right in zip(cuts,cuts[1:]):
        a = (left+right)/2
        weight = (right-left)*density.density(a)
        if a>b:
            lower_missed += weight*2*inverse(path,a,True)
        else:
            higher_missed += weight*max(Q(0),a-max(-a,c))
    return (2*density.mass*(2-beta_1)
            +2*((1+c)/2-alpha_1)*lower_missed
            +2*(4-beta_3)*higher_missed)


def paths():
    raw = [
        [(0,Q(1,4)),(Q(1,4),Q(1,2)),(Q(1,2),Q(1,4)),(Q(5,4),1),(8,1)],
        [(0,Q(3,4)),(Q(1,8),Q(7,8)),(Q(3,4),Q(1,4)),(Q(3,2),1),(8,1)],
        [(0,Q(1,4)),(Q(3,8),Q(5,8)),(Q(5,8),Q(3,8)),(Q(5,4),1),(8,1)],
        [(0,Q(1,2)),(Q(1,2),Q(1,2)),(1,Q(1,4)),(Q(7,4),1),(8,1)],
        [(0,0),(1,0),(2,1),(8,1)],
        [(0,1),(1,0),(2,1),(8,1)],
        [(0,Q(1,3)),(8,Q(1,3))],
        [(0,Q(1,5)),(Q(2,5),Q(2,5)),(Q(4,5),Q(1,5)),
         (Q(7,5),Q(4,5)),(Q(8,5),1),(8,1)],
    ]
    return [[tuple(map(Q,p)) for p in path] for path in raw]


def main():
    densities = [UniformInward([Q(0),Q(1,3),Q(2,3),Q(1)], [Q(1),Q(2),Q(3)]),
                 UniformInward([Q(0),Q(1,2),Q(1)], [Q(2),Q(1)])]
    counts = dict(pointwise=0, physical_density=0, affine_cells=0, exact_relaxation_identity=0,
                  fast_feature=0, exact_attainment=0, strict_relaxation=0)
    for path in paths():
        for a in sorted({Q(1,8),Q(1,3),Q(1,2),Q(3,4),Q(1),path[0][1]}):
            if a <= 0:
                continue
            for fraction in (Q(0),Q(1,4),Q(1,2),Q(3,4)):
                v = -a+2*a*fraction
                assert pointwise_four(path,a,v) == direct_four(path,a,v), (path,a,v)
                counts['pointwise'] += 1
        b,c,graph = graph_from_path(path)
        segments = []
        for (vl,ul),(vr,ur) in zip(graph,graph[1:]):
            if vl < vr:
                slope=(ur-ul)/(vr-vl)
                segments.append([float(vl),float(vr),float(slope),float(ul-slope*vl)])
        segments=np.array(segments,dtype=float).reshape((-1,4))
        for density in densities:
            actual,cells = physical_integral(path,density)
            feature = density.graph_four_score(b,c,graph)
            assert actual <= feature, (path,actual,feature)
            assert feature-actual == ceiling_gap(path,density,b,c), (path,actual,feature)
            counts['exact_relaxation_identity'] += 1
            counts['physical_density'] += 1
            counts['affine_cells'] += cells
            counts['exact_attainment' if actual==feature else 'strict_relaxation'] += 1
            row=uniform_inward_feature_row(np.array(density.knots,dtype=float),float(b),float(c),segments)
            result=float(row@np.array(density.heights,dtype=float))
            assert abs(result-float(feature)) < 2e-12, (result,feature)
            counts['fast_feature'] += 1
    assert counts['exact_attainment'] and counts['strict_relaxation']
    print(f'PASS: {sum(counts.values())} uniform-inward checks')
    for name,count in counts.items():
        print(f'  {name}: {count}')
    print('PASS: physical two-dimensional law integration by exact polygonal intersections')
    print('PASS: U=1 plateaus, initial equality, zero first legs, and strict ceiling losses')
    print('Scope: additional unnormalized monster feature; no matching game value')


if __name__=='__main__':
    main()
