#!/usr/bin/env python3
"""Exact affine-in-field forms for geometric quadratic response cells.

The forms use only the geometry of the supplied continuous affine CDF.
No rank cutoff is solved from the current field. Positive-part integrals
are lifted by a freely quantified cutoff before forming the coefficients.
This is a response-family component, not an all-monster certificate.
"""
from bisect import bisect_right
from dataclasses import dataclass
from fractions import Fraction as Q
from functools import lru_cache
from audit_m1 import ExactField, cross, subtract

@dataclass(frozen=True)
class Form:
    constant: Q = Q(0)
    terms: tuple = ()
    def __add__(self, other):
        if not isinstance(other, Form):
            other = Form(Q(other))
        terms = dict(self.terms)
        for i, value in other.terms:
            terms[i] = terms.get(i, Q(0)) + value
        return Form(self.constant+other.constant,
                    tuple(sorted((i,value) for i,value in terms.items() if value)))
    __radd__ = __add__
    def __neg__(self):
        return self * -1
    def __sub__(self, other):
        return self + (-other if isinstance(other, Form) else -Q(other))
    def __rsub__(self, other):
        return -self + other
    def __mul__(self, scalar):
        scalar = Q(scalar)
        return Form(self.constant*scalar,
                    tuple((i,v*scalar) for i,v in self.terms if v*scalar))
    __rmul__ = __mul__
    def __truediv__(self, scalar):
        return self * (1/Q(scalar))
    def value(self, values):
        return self.constant + sum(w*values[i] for i,w in self.terms)
    def payload(self):
        return dict(constant=str(self.constant),terms=[[i,str(w)] for i,w in self.terms])

class GeometryForms:
    """The supplied field locates triangles; its values never enter the forms."""
    def __init__(self, data):
        self.geometry = ExactField(data)
        self.indices = [tuple(row) for row in data['triangles']]
        self.nodes = self.geometry.nodes

    @lru_cache(maxsize=None)
    def radial(self, u, v):
        u,v = Q(u),Q(v)
        if v>1:
            return Form()
        field = self.geometry
        cell = [max(0,min(len(field.grid[k])-2,
                         bisect_right(field.grid[k],p)-1))
                for k,p in enumerate((u,v))]
        possible=set()
        for i in [cell[0],cell[0]-1]:
            for j in [cell[1],cell[1]-1]:
                possible.update(field.cells.get((i,j),[]))
        point=u,v
        for number in sorted(possible):
            points,_,positive=field.triangles[number]
            turns=[cross(subtract(b,a),subtract(point,a))
                   for a,b in zip(points,points[1:]+points[:1])]
            inside=all(t>=0 for t in turns) if positive else all(t<=0 for t in turns)
            if inside:
                p,q,r=points
                determinant=cross(subtract(q,p),subtract(r,p))
                weights=[cross(subtract(q,point),subtract(r,point))/determinant,
                         cross(subtract(r,point),subtract(p,point))/determinant,
                         cross(subtract(p,point),subtract(q,point))/determinant]
                assert sum(weights)==1 and min(weights)>=0
                return Form(Q(0),tuple((i,w) for i,w in zip(self.indices[number],weights) if w))
        raise ValueError(('No exact geometric triangle',u,v))

    @lru_cache(maxsize=None)
    def integral(self, fixed, left, right, axis):
        """axis0 fixes U and integrates V; axis1 fixes V and integrates U."""
        fixed,left,right=Q(fixed),Q(left),Q(right)
        if right<=left:
            return Form()
        if (axis==1 and fixed>=1) or (axis==0 and left>=1):
            return Form()
        if axis==0 and right>1:
            return self.integral(fixed,left,Q(1),axis)
        field=self.geometry
        i=max(0,min(len(field.grid[axis])-2,
                    bisect_right(field.grid[axis],fixed)-1))
        possible=set(field.strips[axis].get(i,[]))|set(field.strips[axis].get(i-1,[]))
        cuts={left,right}
        other=1-axis
        for number in possible:
            points=field.triangles[number][0]
            for a,b in zip(points,points[1:]+points[:1]):
                if a[axis]==b[axis]:
                    if a[axis]==fixed:
                        cuts.update(x[other] for x in [a,b] if left<x[other]<right)
                elif min(a[axis],b[axis])<=fixed<=max(a[axis],b[axis]):
                    value=a[other]+(fixed-a[axis])*(b[other]-a[other])/(b[axis]-a[axis])
                    if left<value<right:
                        cuts.add(value)
        total=Form()
        cuts=sorted(cuts)
        for a,b in zip(cuts,cuts[1:]):
            fa=self.radial(fixed,a) if axis==0 else self.radial(a,fixed)
            fb=self.radial(fixed,b) if axis==0 else self.radial(b,fixed)
            total+=(b-a)*(fa+fb)/2
        return total

    def initial(self,a):
        return self.radial(a,-a)
    def endpoint_four(self):
        return 4+self.integral(Q(1),-Q(1),Q(1),0)

    def negative_m3_four(self,a,s,b,branch):
        """Actual early-M3 four-cost is min over b and branch."""
        a,s,b=Q(a),Q(s),Q(b)
        assert 0<=a<=s<=b<=1 and branch in(0,1)
        A=self.initial(a)
        N=self.integral(a,-a,a,0)
        B=self.radial(s,a)
        D=self.radial(Q(1),s)
        I=self.integral(a,a,s,1)
        return (N+12-8*A+(s+a-4)*B-I
                -branch*(7-s)*(D-A)
                -self.integral(s,b,Q(1),1)+(1-b)*A)



    def center_i_four(self,z,s,b,d,branch):
        """Lifted CENTER-first initial-inward family.

        The first inward leg ends at center at time z; the next outward
        turn has U=s. B is CLOSED, including B=1 at s=z+2. On general
        atomic laws the N row must use strict incoming traces, whereas
        the fixed-V beta rows are closed; GeometryForms represents the
        continuous interior field, where that distinction is automatic.
        Minimize over b in[z,s], d in[s,s+2], and both branches.
        If s>=1 and the outgoing V=1 atom is absent, d=s+2 is optimal.
        """
        z,s,b,d=map(Q,(z,s,b,d))
        assert 0<=z<=1 and z<=s<=z+2
        assert z<=b<=s and s<=d<=s+2 and branch in(0,1)
        A=self.initial(z)
        Z=self.radial(z,z)
        B=Form(Q(1)) if s==z+2 else self.radial(s,z)
        N=self.integral(z,-z,z,0)
        return (N+4*s+8+(2*z-s-d)*Z-(s+b+6)*A
                -branch*(s+6-z)*(B-A)
                -self.integral(z,b,s,1)
                -self.integral(s,d,s+2,1))

    def positive_i_four(self,z,v,s,b,c,branch):
        """Lifted initial-inward family; actual four-cost is min over b,c,j.

        z is initial positive position, v<z is the first inward turn,
        z<=s<=v+2 is the following outward turn. At s=v+2, B=1 is
        the CLOSED endpoint capture. The center-first-turn v=z needs
        a separate trace formula and is intentionally excluded.
        The exact row-cutoff domain tightens to c>=v by transport.
        Branch0 is redundant when all reflected negative-M1 constraints
        are imposed, but remains an argument for full-identity tests.
        This has five continuous parameters; a 6x6 PSD+N test is only
        sufficient, not an exact copositive representation.
        """
        z,v,s,b,c=map(Q,(z,v,s,b,c))
        assert 0<=z<=1 and -z<=v<z and z<=s<=v+2
        assert z<=b<=s and v<=c<=min(s,Q(1))
        assert branch in(0,1)
        A=self.initial(z)
        ell=self.radial(z,v)
        B=Form(Q(1)) if s==v+2 else self.radial(s,v)
        N=self.integral(z,-z,z,0)
        return (N+4*s+8+(s+c-z-v)*ell-(s+b+6)*A
                -branch*(s+6-v)*(B-A)
                -self.integral(z,v,z,0)
                +self.integral(s,c,s,0)
                -self.integral(v,b,s,1)
                -self.integral(s,s,s+2,1))

    def positive_m2_four(self,a,c):
        a,c=Q(a),Q(c)
        assert 0<=a<=1 and -a<=c<=1
        A=self.initial(a)
        return (12+(1+c)*A-(7+a)*self.radial(Q(1),-a)
                -self.integral(-a,a,Q(1),1)
                +self.integral(Q(1),c,Q(1),0))

    def positive_m1_four(self,a,c):
        a,c=Q(a),Q(c)
        assert 0<=a<=1 and -a<=c<=1
        A=self.initial(a)
        return (8-4*a+(2-a+c)*A
                -self.integral(-a,a,2-a,1)
                +self.integral(2-a,c,Q(1),0))

    def negative_m1_four(self,a):
        a=Q(a)
        assert 0<=a<=1
        return (self.integral(a,-a,a,0)+4*a+8
                -2*(a+3)*self.initial(a)
                -self.integral(a,a,a+2,1))

    def negative_m2_four(self,a):
        a=Q(a)
        assert 0<=a<=1
        return (self.integral(a,-a,a,0)+12-4*self.initial(a)
                -(7-a)*self.radial(Q(1),a)
                -self.integral(a,a,Q(1),1))

    def positive_m3_four(self,a,s,c):
        a,s,c=Q(a),Q(s),Q(c)
        assert 0<=a<=s<=1 and -a<=c<=s
        return (12+(s+c)*self.initial(a)
                -(4+a-s)*self.radial(s,-a)
                -(7-s)*self.radial(Q(1),s)
                -self.integral(-a,a,s,1)
                -self.integral(s,s,Q(1),1)
                +self.integral(s,c,s,0))

def matrix_forms(vertices,function):
    """Caller must prove its geometric cell is one quadratic piece."""
    vertices=[tuple(map(Q,v)) for v in vertices]
    values=[function(v) for v in vertices]
    result=[[Form() for _ in vertices] for _ in vertices]
    for i in range(len(vertices)):
        result[i][i]=values[i]
        for j in range(i):
            midpoint=tuple((x+y)/2 for x,y in zip(vertices[i],vertices[j]))
            result[i][j]=result[j][i]=2*function(midpoint)-(values[i]+values[j])/2
    return result

ATTACK_TETRAHEDRON=((Q(0),Q(13,16),Q(13,16)),
                   (Q(1,16),Q(7,8),Q(7,8)),
                   (Q(0),Q(7,8),Q(7,8)),
                   (Q(0),Q(13,16),Q(7,8)))
