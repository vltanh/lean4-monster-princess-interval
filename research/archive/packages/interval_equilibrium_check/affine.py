"""Exact affine arithmetic a+b*epsilon, ordered for epsilon -> 0+.
Each comparison records a positive radius on which its sign is valid.
This is a proof checker for a particular approaching family, not a solver.
"""
from fractions import Fraction as Q
from functools import total_ordering
RADIUS=Q(1)

@total_ordering
class A:
    __slots__=('a','b')
    def __init__(self,a=0,b=0):
        if isinstance(a,A):self.a,self.b=a.a,a.b;assert b==0
        else:self.a,self.b=Q(a),Q(b)
    def __add__(x,y):
        y=A(y);return A(x.a+y.a,x.b+y.b)
    __radd__=__add__
    def __neg__(x):return A(-x.a,-x.b)
    def __sub__(x,y):return x+-A(y)
    def __rsub__(x,y):return A(y)+-x
    def __mul__(x,c):c=Q(c);return A(x.a*c,x.b*c)
    __rmul__=__mul__
    def __truediv__(x,c):return x*(1/Q(c))
    def __eq__(x,y):y=A(y);return x.a==y.a and x.b==y.b
    def __lt__(x,y):
        global RADIUS
        d=x-A(y)
        if d.a*d.b<0:RADIUS=min(RADIUS,abs(d.a/d.b)/2)
        return d.a<0 or d.a==0 and d.b<0
    def __hash__(x):return hash((x.a,x.b))
    def __abs__(x):return -x if x<0 else x
    def data(x):return [str(x.a),str(x.b)]
    def __repr__(x):return f'({x.a})+({x.b})*eps'

def slope(a,x,b,y):
    dt=b-a;dx=y-x;assert dt>0
    v=dx.a/dt.a if dt.a else dx.b/dt.b
    assert dx==dt*v
    assert abs(v)<=1
    return v

def simplify(p):
    out=[]
    for t,x in p:
        t,x=A(t),A(x)
        if out and t==out[-1][0]:assert x==out[-1][1];continue
        assert not out or out[-1][0]<t
        out.append((t,x))
        while len(out)>=3:
            (a,x),(b,y),(c,z)=out[-3:]
            if slope(a,x,b,y)==slope(b,y,c,z):out.pop(-2)
            else:break
    return out

def pos(p,t):
    for (a,x),(b,y) in zip(p,p[1:]):
        if a<=t<=b:return x+(t-a)*slope(a,x,b,y)
    assert t>=p[-1][0];return p[-1][1]

def meeting(p,q):
    ts=sorted(set(t for t,x in p+q))
    for i,t in enumerate(ts):
        d=pos(p,t)-pos(q,t)
        if d==0:return t
        if i+1<len(ts):
            b=ts[i+1];e=pos(p,b)-pos(q,b)
            if (d<0)!=(e<0) or e==0:
                dt=b-t;dv=e-d
                v=dv.a/dt.a if dt.a else dv.b/dt.b
                assert dv==dt*v and v!=0
                ans=t-d/v;assert t<=ans<=b;return ans
    return None

def envelope_knots(curves,H):
    ts=sorted(set([A(0),H]+[t for p in curves for t,x in p]));cuts=set(ts)
    for a,b in zip(ts,ts[1:]):
        va=[pos(p,a) for p in curves];vb=[pos(p,b) for p in curves]
        for i in range(len(curves)):
            for j in range(i):
                d=va[i]-va[j];e=vb[i]-vb[j]
                if d!=0 and e!=0 and (d<0)!=(e<0):
                    dt=b-a;dv=e-d
                    v=dv.a/dt.a if dt.a else dv.b/dt.b
                    assert dv==dt*v and v!=0
                    cuts.add(a-d/v)
    return cuts

def witness(monsters,targets,initial,H=A(4)):
    eps=A(0,1);lows=[[(A(0),A(-1)),(H,A(-1))]];ups=[[(A(0),A(1)),(H,A(1))]]
    for m,r in zip(monsters,targets):
        e=max(A(0),A(r)-eps);d=-1 if m[0][1]<initial else 1
        p=[(t,x) for t,x in m if t<e]+[(e,pos(m,e))]
        if e<H:p.append((H,pos(m,e)+(H-e)*d))
        (lows if d<0 else ups).append(simplify(p))
    ts=sorted(envelope_knots(lows,H)|envelope_knots(ups,H))
    L0=max(pos(p,A(0)) for p in lows);U0=min(pos(p,A(0)) for p in ups)
    assert L0.b==U0.b==0
    lam=(Q(initial)-L0.a)/(U0.a-L0.a);assert 0<lam<1
    out=[]
    for t in ts:
        L=max(pos(p,t) for p in lows);U=min(pos(p,t) for p in ups);assert L<U
        out.append((t,L*(1-lam)+U*lam))
    p=simplify(out)
    assert all(-1<=x<=1 for t,x in p)
    for m,r in zip(monsters,targets):
        t=meeting(m,p);assert t is not None and t>=A(r)-eps
    return p
