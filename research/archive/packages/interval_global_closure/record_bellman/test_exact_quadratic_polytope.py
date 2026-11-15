#!/usr/bin/env python3
"""Independent exact references for the active-face quadratic guard checker."""
from fractions import Fraction as Q
from itertools import product
import hashlib
import json
from pathlib import Path
import random

from exact_quadratic_polytope import minimize_quadratic, UnboundedPolytope


def objective(c, linear, H, x):
    return c+sum(a*b for a, b in zip(linear, x))+sum(
        x[i]*H[i][j]*x[j] for i in range(len(x)) for j in range(len(x)))


def segment_minimum(f, start, end):
    """Reference uses three exact evaluations, without a KKT system."""
    mid=tuple((a+b)/2 for a,b in zip(start,end))
    c,y1,y2=f(start),f(mid),f(end)
    a=2*(y2-2*y1+c);b=y2-c-a
    candidates=[(c,start),(y2,end)]
    if a>0:
        t=-b/(2*a)
        if 0<t<1:
            x=tuple(u+t*(v-u) for u,v in zip(start,end))
            candidates.append((f(x),x))
    return min(candidates)


def rectangle_minimum(c, linear, H, bounds):
    """Reference: four independent 1D edge minima plus explicit 2D critical point."""
    (a,b),(u,v)=bounds
    corners=[(a,u),(b,u),(b,v),(a,v)]
    f=lambda x:objective(c,linear,H,x)
    candidates=[segment_minimum(f,corners[i],corners[(i+1)%4]) for i in range(4)]
    det=H[0][0]*H[1][1]-H[0][1]**2
    if det:
        x=(-H[1][1]*linear[0]+H[0][1]*linear[1])/(2*det)
        y=(H[0][1]*linear[0]-H[0][0]*linear[1])/(2*det)
        if a<=x<=b and u<=y<=v:candidates.append((f((x,y)),(x,y)))
    return min(candidates)


def box_constraints(bounds):
    d=len(bounds);rows=[]
    for i,(lo,hi) in enumerate(bounds):
        a=tuple(Q(int(i==j)) for j in range(d))
        rows.extend([(a,Q(hi)),(tuple(-v for v in a),Q(-lo))])
    return rows


def main():
    rng=random.Random(940271)
    counts={"one_dimensional":0,"independent_rectangles":0,
            "independent_rational_polygons":0,
            "known_high_dimensional":0,"lower_dimensional":0,
            "empty_domains":0,"unbounded_rejections":0,"malformed_rejections":0,
            "singular_stationary_fixtures":0}
    for _ in range(100):
        a,b=sorted(rng.sample(range(-7,8),2));lo,hi=Q(a,3),Q(b,3)
        H=[[Q(rng.randrange(-5,6),3)]];linear=[Q(rng.randrange(-8,9),5)];c=Q(rng.randrange(-4,5),7)
        f=lambda x:objective(c,linear,H,x)
        expected=segment_minimum(f,(lo,),(hi,))
        result=minimize_quadratic(box_constraints([(lo,hi)]),c,linear,H)
        assert result.value==expected[0] and f(result.point)==result.value
        counts['one_dimensional']+=1
    for index in range(160):
        bounds=[]
        for _ in range(2):
            a,b=sorted(rng.sample(range(-8,9),2));bounds.append((Q(a,4),Q(b,4)))
        a,b,c=(Q(rng.randrange(-6,7),5) for _ in range(3))
        H=[[a,b],[b,c]]
        if index%5==0:
            # Deliberately singular, including both flat and concave cases.
            a=Q(rng.randrange(-3,4));H=[[a,a],[a,a]]
        linear=[Q(rng.randrange(-9,10),7) for _ in range(2)];constant=Q(index%7,11)
        result=minimize_quadratic(box_constraints(bounds),constant,linear,H)
        expected=rectangle_minimum(constant,linear,H,bounds)
        assert result.value==expected[0]
        assert objective(constant,linear,H,result.point)==result.value
        counts['independent_rectangles']+=1
    for index in range(80):
        # A separate convex-hull/edge reference exercises oblique faces.
        points=sorted(set((Q(rng.randrange(-12,13),7),Q(rng.randrange(-12,13),7))
                          for _ in range(10)))
        def cross(a,b,c):return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
        lower=[];upper=[]
        for point in points:
            while len(lower)>1 and cross(lower[-2],lower[-1],point)<=0:lower.pop()
            lower.append(point)
        for point in reversed(points):
            while len(upper)>1 and cross(upper[-2],upper[-1],point)<=0:upper.pop()
            upper.append(point)
        hull=lower[:-1]+upper[:-1];assert len(hull)>=3
        rows=[]
        for i,a in enumerate(hull):
            b=hull[(i+1)%len(hull)];normal=(b[1]-a[1],a[0]-b[0])
            rows.append((normal,sum(u*v for u,v in zip(normal,a))))
        a,b,c=(Q(rng.randrange(-9,10),11) for _ in range(3));H=[[a,b],[b,c]]
        linear=[Q(rng.randrange(-11,12),13) for _ in range(2)]
        constant=Q(index,17);f=lambda x:objective(constant,linear,H,x)
        reference=[segment_minimum(f,hull[i],hull[(i+1)%len(hull)]) for i in range(len(hull))]
        det=a*c-b*b
        if det:
            point=((-c*linear[0]+b*linear[1])/(2*det),(b*linear[0]-a*linear[1])/(2*det))
            if all(sum(u*v for u,v in zip(row,point))<=rhs for row,rhs in rows):reference.append((f(point),point))
        result=minimize_quadratic(rows,constant,linear,H)
        assert result.value==min(reference)[0]
        counts['independent_rational_polygons']+=1
    for d in (2,3,4):
        bounds=[(Q(-1),Q(1))]*d;constraints=box_constraints(bounds)
        for rank in range(d+1):
            B=[[Q(rng.randrange(-3,4),5) for _ in range(d)] for _ in range(rank)]
            H=[[sum((row[i]*row[j] for row in B),Q(0)) for j in range(d)] for i in range(d)]
            p=tuple(Q(i+1,2*d+1) for i in range(d))
            linear=[-2*sum((H[i][j]*p[j] for j in range(d)),Q(0)) for i in range(d)]
            offset=Q(7,13);constant=offset+sum(p[i]*H[i][j]*p[j] for i in range(d) for j in range(d))
            result=minimize_quadratic(constraints,constant,linear,H)
            assert result.value==offset
            if rank<d:
                assert result.stats['singular_systems']>0
                counts['singular_stationary_fixtures']+=1
            counts['known_high_dimensional']+=1
        H=[[-Q(int(i==j)) for j in range(d)] for i in range(d)]
        result=minimize_quadratic(constraints,0,[0]*d,H)
        assert result.value==-d
        counts['known_high_dimensional']+=1

    # An interior stationary line, forced boundary stationarity, redundant
    # equalities, and a hidden zero-dimensional face given only by inequalities.
    result=minimize_quadratic(box_constraints([(0,1),(0,1)]),Q(1,4),[-1,-1],[[1,1],[1,1]])
    assert result.value==0 and sum(result.point)==Q(1,2)
    counts['singular_stationary_fixtures']+=1
    for d in (2,3,4):
        eq=[]
        for i in range(1,d):
            a=[Q(0)]*d;a[0]=-1;a[i]=1;eq.append((a,0))
        eq.append((tuple(2*v for v in eq[0][0]),0))
        bounds=[(Q(-2),Q(3))]*d
        H=[[Q(0)]*d for _ in range(d)];H[0][0]=Q(2)
        linear=[Q(0)]*d;linear[0]=Q(-1)
        result=minimize_quadratic(box_constraints(bounds),Q(3),linear,H,eq)
        assert result.value==Q(23,8) and result.point==(Q(1,4),)*d
        counts['lower_dimensional']+=1
        rows=[(tuple(-Q(int(i==j)) for j in range(d)),0) for i in range(d)]
        rows.append(([1]*d,0))
        result=minimize_quadratic(rows,5,[1]*d,[[-Q(int(i==j)) for j in range(d)] for i in range(d)])
        assert result.point==(Q(0),)*d and result.value==5
        counts['lower_dimensional']+=1
    assert minimize_quadratic([],7,[],[]) .value==7
    assert minimize_quadratic([([], -1)],0,[],[]) is None
    counts['lower_dimensional']+=1;counts['empty_domains']+=1

    empties=[([([1],0),([-1],-1)],[],[0],[[0]]),
             ([],[([1],0),([1],1)],[0],[[0]]),
             ([([1,0],0),([-1,0],-1)],[],[0,0],[[0,0],[0,0]])]
    for inequalities,equalities,linear,H in empties:
        assert minimize_quadratic(inequalities,0,linear,H,equalities) is None
        counts['empty_domains']+=1
    unbounded=[([],[],[0],[[1]]),([([-1],0)],[],[0],[[-1]]),
               ([],[([1,0],0)],[0,0],[[1,0],[0,1]]),
               ([([1,0],1),([-1,0],0)],[],[0,0],[[0,0],[0,0]])]
    for inequalities,equalities,linear,H in unbounded:
        try:minimize_quadratic(inequalities,0,linear,H,equalities)
        except UnboundedPolytope as e:
            assert any(e.direction)
            assert all(sum(Q(a)*x for a,x in zip(row,e.direction))<=0 for row,b in inequalities)
            assert all(sum(Q(a)*x for a,x in zip(row,e.direction))==0 for row,b in equalities)
        else:raise AssertionError('unbounded domain accepted')
        counts['unbounded_rejections']+=1
    bad=[(box_constraints([(0,1)]),0,[0.0],[[1]],[]),
         (box_constraints([(0,1),(0,1)]),0,[0,0],[[1,2],[0,1]],[]),
         ([([1,0],0)],0,[0],[[1]],[]),
         ([],0,[0]*5,[[0]*5 for _ in range(5)],[]),
         ([],False,[],[],[])]
    for args in bad:
        try:minimize_quadratic(*args)
        except (ValueError,TypeError):pass
        else:raise AssertionError('malformed input accepted')
        counts['malformed_rejections']+=1

    here=Path(__file__).resolve().parent
    report={'status':'PASS','scope':'Exact global quadratic minima on compact rational polytopes; independent one- and two-dimensional analytic references, manufactured higher-dimensional minima, singular and boundary cases, empty-domain handling, and rational unboundedness witnesses.',
            'counts':counts,'source_sha256':hashlib.sha256((here/'exact_quadratic_polytope.py').read_bytes()).hexdigest()}
    (here/'exact_quadratic_polytope_replay.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))


if __name__=='__main__':main()
