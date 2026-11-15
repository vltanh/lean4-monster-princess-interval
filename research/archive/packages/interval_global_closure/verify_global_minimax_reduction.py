#!/usr/bin/env python3
"""Exact examples supporting global horizon/rank reduction and Monster coupling obstruction.

The minimax and infinite-population statements are analytic proofs, not
finitary assertions checked by this program.
"""
from fractions import Fraction as Q

ZERO = Q(0)
ONE = Q(1)

# Routes represented as (time, position) in rational arithmetic.
A = [(Q(0),Q(-1)), (Q(2),Q(0))]
B = [(Q(0),Q(1)), (Q(2),Q(0))]
L = [(Q(2),Q(0)), (Q(4),Q(-1)), (Q(6),Q(1))]
R = [(Q(2),Q(0)), (Q(4),Q(1)), (Q(6),Q(-1))]

def glue(prefix,suffix):
    assert prefix[-1] == suffix[0]
    return prefix + suffix[1:]

def interp(path,t):
    assert path[0][0] <= t <= path[-1][0]
    for (a,x),(b,y) in zip(path,path[1:]):
        if a <= t <= b:
            return x+(t-a)*(y-x)/(b-a)
    raise AssertionError('time not covered')

def first_hit(path,z):
    """Exact first hitting time of stationary Princess at z."""
    for (a,x),(b,y) in zip(path,path[1:]):
        if x == z:
            return a
        if x != y and min(x,y) <= z <= max(x,y):
            return a+(b-a)*(z-x)/(y-x)
    return None

def check_legality(path):
    assert all(-ONE <= x <= ONE for _,x in path)
    for (a,x),(b,y) in zip(path,path[1:]):
        assert b>a and abs(y-x) <= b-a
    assert -ONE in [x for _,x in path] and ONE in [x for _,x in path]

cross=[glue(A,R),glue(B,L)]
bounce=[glue(A,L),glue(B,R)]
for law in (cross,bounce):
    for path in law:check_legality(path)

# Exact equality of full time-marginal laws: on each affine phase the
# unlabelled coordinate pair is the same. Verify at every phase endpoint,
# then check a dense deterministic mesh (the endpoint proof is analytic).
for t in (Q(0),Q(1,2),Q(1),Q(3,2),Q(2),Q(5,2),Q(3),Q(7,2),Q(4),Q(9,2),Q(5),Q(11,2),Q(6)):
    assert sorted(interp(p,t) for p in cross) == sorted(interp(p,t) for p in bounce)

z = Q(-3,10)
assert [first_hit(p,z) for p in cross] == [Q(7,5),Q(13,5)]
assert [first_hit(p,z) for p in bounce] == [Q(7,5),Q(53,10)]
assert sum(first_hit(p,z) for p in cross)/2 == Q(2)
assert sum(first_hit(p,z) for p in bounce)/2 == Q(67,20)
print('Monster identical time marginals / distinct capture law: E_cross=2; E_bounce=67/20')

# All midpoint quantile samples yield a uniform error <= 1/N per two
# survivor tails (a left prefix and right suffix), including ties/atoms.
def midpoint_mass(N,a,b):
    assert ZERO <= a <= b <= ONE
    return Q(sum(1 for i in range(N) if Q(2*i+1,2*N)<a or Q(2*i+1,2*N)>b),N)
for N in (2,4,6,8,16,32,64):
    for ia in range(101):
        for ib in range(ia,101):
            a,b=Q(ia,100),Q(ib,100)
            truth=a+1-b
            empirical=midpoint_mass(N,a,b)
            assert abs(empirical-truth)<=Q(1,N), (N,a,b,truth,empirical)
print('Midpoint-quantile two-tail bound checked on 7 N values and 36,057 exact interval pairs')

# Exact endpoint-completion fixture: every prefix can be completed from H
# by nearest-endpoint then crossing, requiring no more than 3 time units.
def completed(prefix,H):
    x=interp(prefix,H)
    leg_prefix=[(t,v) for t,v in prefix if t<H]+[(H,x)]
    first = ONE if x>0 else -ONE
    end = -first
    t1 = H+abs(first-x)
    t2 = t1+Q(2)
    return leg_prefix+[(t1,first),(t2,end)]

raw=[(Q(0),Q(-1)),(Q(1),Q(-1)),(Q(3),Q(1)),(Q(6),Q(-1))]
H=Q(3,2)
new=completed(raw,H)
assert max(t for t,_ in new)<=H+3
for a in (Q(-1),Q(-4,5),Q(-3,10),Q(0),Q(1,10),Q(1,2),Q(1)):
    o=first_hit(raw,a)
    v=first_hit(new,a)
    assert o is not None and v is not None
    assert v<=o+(Q(3) if o>H else Q(0)), (a,o,v)
    assert v<=H+3
print('Horizon completion: exact capture inequality checked for 7 stationary targets')
print('All exact fixtures passed. Universal minimax/compactness proof is mathematical, not certified here.')
