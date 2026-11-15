#!/usr/bin/env python3
"""Exact finite minimization of a rational quadratic on a bounded polytope.

This small reference implementation enumerates stationary points on every
possible face, including singular stationary affine spaces. It does NOT
replace interior minima by vertex tests. Exponential enumeration is intended
for transparent small certificates, not large-scale numerical discovery.
"""
from __future__ import annotations
from fractions import Fraction as Q
from itertools import combinations
from dataclasses import dataclass
from typing import Sequence


def dot(a,b): return sum((x*y for x,y in zip(a,b)),Q(0))

def affine_solve(A,b,n):
    """Return (particular, nullspace columns) or None for inconsistency."""
    rows=[[Q(x) for x in row]+[Q(v)] for row,v in zip(A,b)]
    pivots=[]; r=0
    for col in range(n):
        pivot=next((j for j in range(r,len(rows)) if rows[j][col]),None)
        if pivot is None: continue
        rows[r],rows[pivot]=rows[pivot],rows[r]
        v=rows[r][col]; rows[r]=[x/v for x in rows[r]]
        for j in range(len(rows)):
            if j!=r and rows[j][col]:
                v=rows[j][col]; rows[j]=[x-v*y for x,y in zip(rows[j],rows[r])]
        pivots.append(col);r+=1
    if any(not any(row[:n]) and row[n] for row in rows): return None
    p=[Q(0)]*n
    for i,col in enumerate(pivots): p[col]=rows[i][n]
    null=[]
    for free in range(n):
        if free in pivots: continue
        v=[Q(0)]*n;v[free]=Q(1)
        for i,col in enumerate(pivots):v[col]=-rows[i][free]
        null.append(v)
    return p,null


def feasible(A,b,x): return all(dot(row,x)<=v for row,v in zip(A,b))

def vertices(A,b,n):
    """Enumerate vertices. The supplied polytope must be bounded."""
    if n==0:
        return [()] if all(Q(v)>=0 for v in b) else []
    out=set()
    for active in combinations(range(len(A)),n):
        answer=affine_solve([A[i] for i in active],[b[i] for i in active],n)
        if answer is None or answer[1]:continue
        p=tuple(answer[0])
        if feasible(A,b,p):out.add(p)
    return sorted(out)

@dataclass(frozen=True)
class Quadratic:
    """q(x)=constant+linear.x+x^T matrix x, with symmetric matrix."""
    constant: Q
    linear: tuple
    matrix: tuple

    @classmethod
    def make(cls,constant,linear,matrix=None):
        n=len(linear)
        if matrix is None: matrix=[[0]*n for _ in range(n)]
        assert len(matrix)==n and all(len(row)==n for row in matrix)
        assert all(matrix[i][j]==matrix[j][i] for i in range(n) for j in range(n))
        return cls(Q(constant),tuple(map(Q,linear)),tuple(tuple(map(Q,row)) for row in matrix))
    @property
    def dim(self):return len(self.linear)
    def value(self,x):return self.constant+dot(self.linear,x)+sum((x[i]*dot(row,x) for i,row in enumerate(self.matrix)),Q(0))
    def gradient(self,x):return [g+2*dot(row,x) for g,row in zip(self.linear,self.matrix)]
    def subtract(self,other):
        assert self.dim==other.dim
        return Quadratic.make(self.constant-other.constant,
            [a-b for a,b in zip(self.linear,other.linear)],
            [[a-b for a,b in zip(ra,rb)] for ra,rb in zip(self.matrix,other.matrix)])
    def pullback(self,p,columns):
        k=len(columns); gp=self.gradient(p)
        return Quadratic.make(self.value(p),[dot(c,gp) for c in columns],
            [[sum((columns[i][r]*dot(self.matrix[r],columns[j]) for r in range(self.dim)),Q(0))
              for j in range(k)] for i in range(k)])


def minimum(q,A,b):
    """Exact (value,witness,diagnostics); None means the bounded set is empty.

    Each nonempty polytope face is represented by a linearly independent
    subset of at most n active constraints. At a relative-interior minimum,
    the restricted gradient vanishes. A singular stationary affine space
    has constant objective; its feasible intersection is checked exactly.
    """
    n=q.dim; best=None; face_count=0; stationary_count=0
    for count in range(n+1):
      for active in combinations(range(len(A)),count):
        face_count+=1
        face=affine_solve([A[i] for i in active],[b[i] for i in active],n)
        if face is None:continue
        p,cols=face
        if len(cols)!=n-count:continue
        restricted=q.pullback(p,cols)
        stationarity=affine_solve([[2*v for v in row] for row in restricted.matrix],
                                  [-v for v in restricted.linear],len(cols))
        if stationarity is None:continue
        yp,ycols=stationarity
        xp=[p[i]+sum((col[i]*t for col,t in zip(cols,yp)),Q(0)) for i in range(n)]
        xcols=[[sum((cols[j][i]*yc[j] for j in range(len(cols))),Q(0))
                 for i in range(n)] for yc in ycols]
        AA=[[dot(row,col) for col in xcols] for row in A]
        bb=[v-dot(row,xp) for row,v in zip(A,b)]
        vv=vertices(AA,bb,len(xcols))
        if not vv:continue
        stationary_count+=1
        param=vv[0]
        x=tuple(xp[i]+sum((col[i]*t for col,t in zip(xcols,param)),Q(0)) for i in range(n))
        assert feasible(A,b,x)
        value=q.value(x)
        for param2 in vv[1:]:
            x2=[xp[i]+sum((col[i]*t for col,t in zip(xcols,param2)),Q(0)) for i in range(n)]
            assert q.value(x2)==value
        if best is None or value<best[0]:best=(value,x)
    if best is None:return None
    return best[0],best[1],dict(face_subsets=face_count,feasible_stationary_faces=stationary_count)


def box(bounds):
    n=len(bounds);A=[];b=[]
    for i,(lo,hi) in enumerate(bounds):
        row=[Q(0)]*n;row[i]=1;A.append(row);b.append(Q(hi))
        row=[Q(0)]*n;row[i]=-1;A.append(row);b.append(-Q(lo))
    return A,b


def self_test():
    checks=0
    fixtures=[
      (Quadratic.make(Q(1,9),[-Q(2,3)],[[1]]),box([(0,1)]),Q(0)),
      (Quadratic.make(Q(1,100),[0,0],[[1,-1],[-1,1]]),box([(0,1),(0,1)]),Q(1,100)),
      (Quadratic.make(0,[0,0],[[-1,0],[0,-1]]),box([(0,1),(0,1)]),Q(-2)),
      (Quadratic.make(Q(1,4),[-1,-1],[[2,0],[0,2]]),([[-1,0],[0,-1],[1,1]],[0,0,1]),Q(0)),
    ]
    for q,(A,b),expected in fixtures:
        answer=minimum(q,A,b);assert answer is not None and answer[0]==expected
        checks+=1
    q=Quadratic.make(Q(1,9)-Q(1,100),[-Q(2,3)],[[1]])
    A,b=box([(0,1)])
    assert all(q.value(v)>0 for v in vertices(A,b,1))
    assert minimum(q,A,b)[0]==-Q(1,100); checks+=1
    q=Quadratic.make(0,[0,0],[[1,0],[0,1]])
    A,b=box([(0,1),(0,1)]);A += [[1,1],[-1,-1]];b += [1,-1]
    assert minimum(q,A,b)[0]==Q(1,2);checks+=1
    assert minimum(q,[[1,0],[-1,0],[0,1],[0,-1]],[0,-1,1,0]) is None;checks+=1
    return checks

if __name__=='__main__':print('PASS',self_test(),'exact quadratic minimization fixtures')
