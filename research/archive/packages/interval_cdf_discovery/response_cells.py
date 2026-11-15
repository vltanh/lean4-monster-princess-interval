#!/usr/bin/env python3
"""Finite exact geometry cells for M1/M2 and second-V=1 M3.

The construction is independent of CDF values.  Its equivalent BigInt V8
implementation was audited on all cells of the 34-interval repository
mesh during the executor outage.  This Python port still needs its first
execution before being called a tested Python implementation.
"""
from dataclasses import dataclass
from fractions import Fraction as Q
from itertools import permutations
from audit_snapshot import coordinate

@dataclass(frozen=True)
class Cell:
    family: str
    key: tuple
    vertices: tuple

def _base(data_or_base):
    values = data_or_base['base'] if isinstance(data_or_base,dict) else data_or_base
    return tuple(coordinate(value) for value in values)

def negative_m3_cells(data_or_base):
    """All 0<=a<=s<=b<=1; exactly n**3 tetrahedra."""
    grid=_base(data_or_base);n=len(grid)-1
    for ia in range(n):
        for is_ in range(ia,n):
            for ib in range(is_,n):
                for permutation in permutations(range(3)):
                    positions={axis:i for i,axis in enumerate(permutation)}
                    if ia==is_ and positions[0]>positions[1]:
                        continue
                    if is_==ib and positions[1]>positions[2]:
                        continue
                    bits=[0,0,0];cube=[tuple(bits)]
                    for axis in reversed(permutation):
                        bits=list(bits);bits[axis]=1;cube.append(tuple(bits))
                    bins=(ia,is_,ib)
                    vertices=tuple(tuple(grid[bins[k]+v[k]] for k in range(3)) for v in cube)
                    yield Cell('negative_m3',(ia,is_,ib,permutation),vertices)

def _fibers(grid,i):
    """U=s fibers, as endpoint pairs (loV,hiV) on a common s interval."""
    s0,s1=grid[i:i+2];rows=[];bin_index=0
    rows.append((bin_index,'negative',((-s0,-s0),(-s1,-s0)),'edge'))
    bin_index+=1
    cuts=tuple(-x for x in reversed(grid[:i+1]))+grid[1:i+1]
    for lo,hi in zip(cuts,cuts[1:]):
        side='negative' if hi<=0 else 'positive'
        rows.append((bin_index,side,((lo,lo),(lo,hi)),'lower'))
        rows.append((bin_index,side,((lo,hi),(hi,hi)),'upper'))
        bin_index+=1
    rows.append((bin_index,'positive',((s0,s0),(s0,s1)),'edge'))
    return tuple(rows)

def positive_m3_cells(data_or_base):
    """All 0<=a<=s<=1, -a<=c<=s; exactly 3*n**3 tetrahedra."""
    grid=_base(data_or_base);n=len(grid)-1
    for i in range(n):
        ss=grid[i:i+2];rows=_fibers(grid,i)
        for fi,f in enumerate(rows):
            if f[1]!='negative':
                continue
            for gi,g in enumerate(rows):
                if g[0]<f[0]:
                    continue
                tetrahedra=[]
                if fi==gi:
                    ends=f[2]
                    collapsed=0 if ends[0][0]==ends[0][1] else 1
                    base=1-collapsed
                    apex=(ss[collapsed],ends[collapsed][0],ends[collapsed][0])
                    lo,hi=ends[base]
                    tetrahedra=[(apex,(ss[base],lo,lo),(ss[base],lo,hi),(ss[base],hi,hi))]
                else:
                    if f[0]==g[0] and not all(f[2][e][1]<=g[2][e][0] for e in(0,1)):
                        continue
                    def endpoint(e):
                        a,b=f[2][e];c,d=g[2][e]
                        return tuple(dict.fromkeys(((ss[e],a,c),(ss[e],b,c),
                                                    (ss[e],b,d),(ss[e],a,d))))
                    left,right=endpoint(0),endpoint(1)
                    if len(left)+len(right)==4:
                        tetrahedra=[left+right]
                    elif len(left)==1 and len(right)==4:
                        tetrahedra=[(left[0],right[0],right[1],right[2]),
                                    (left[0],right[0],right[2],right[3])]
                    elif len(right)==1 and len(left)==4:
                        tetrahedra=[(right[0],left[0],left[1],left[2]),
                                    (right[0],left[0],left[2],left[3])]
                    else:
                        raise AssertionError(('unexpected fiber',left,right))
                for part,tetrahedron in enumerate(tetrahedra):
                    vertices=tuple((-v,s,c) for s,v,c in tetrahedron)
                    yield Cell('positive_m3',(i,fi,gi,part),vertices)

def positive_m1_cells(data):
    """Map each post-one triangle by (a,c)=(2-U,V)."""
    nodes=tuple(tuple(coordinate(x) for x in p) for p in data['nodes'])
    for number,indices in enumerate(data['triangles']):
        points=tuple(nodes[i] for i in indices)
        if all(1<=u<=2 for u,v in points):
            yield Cell('positive_m1',(number,),tuple((2-u,v) for u,v in points))

def positive_m2_cells(data_or_base):
    """Initial interval times U1-row interval, clipped by c>=-a."""
    grid=_base(data_or_base);n=len(grid)-1
    def rectangle(a,b,c,d):
        return (((a,c),(b,c),(b,d)),((a,c),(b,d),(a,d)))
    for j in range(n):
        a,b=grid[j:j+2]
        for k in range(j):
            for part,vertices in enumerate(rectangle(a,b,-grid[k+1],-grid[k])):
                yield Cell('positive_m2',(j,'negative',k,part),vertices)
        yield Cell('positive_m2',(j,'diagonal'),((a,-a),(b,-b),(b,-a)))
        for k in range(n):
            for part,vertices in enumerate(rectangle(a,b,grid[k],grid[k+1])):
                yield Cell('positive_m2',(j,'positive',k,part),vertices)

def negative_one_parameter_cells(data_or_base,family):
    assert family in('negative_m1','negative_m2')
    grid=_base(data_or_base)
    for i,(a,b) in enumerate(zip(grid,grid[1:])):
        yield Cell(family,(i,),((a,),(b,)))


def center_i_one_cells(data):
    """Fixed s=1 center-first I; n**2 positive pre-one triangles."""
    nodes=tuple(tuple(coordinate(x) for x in p) for p in data['nodes'])
    for number,indices in enumerate(data['triangles']):
        points=tuple(nodes[i] for i in indices)
        if all(0<=v<=u<=1 for u,v in points):
            yield Cell('center_i_one',(number,),tuple((v,u) for u,v in points))

def response_form(geometry,cell,point):
    if cell.family=='center_i_one':
        z,b=point
        return geometry.center_i_four(z,Q(1),b,Q(3),1)
    if cell.family=='negative_m3':
        # Branch0 is redundant provided every negative-M1 constraint is enforced.
        return geometry.negative_m3_four(*point,1)
    function=getattr(geometry,cell.family+'_four')
    return function(*point)
