#!/usr/bin/env python3
"""Exact check of a counterexample to the FIXED-INFINITESIMAL response family.
This is not a lower-bound certificate for the full minimax game.
"""
from fractions import Fraction as Q
from verify import path, first_meeting

p=[(Q(0),Q(3,4)),(Q(3,16),Q(3,4)),(Q(11,16),Q(1,4)),(Q(23,16),Q(1)),(Q(4),Q(1))]
for (t,x),(u,y) in zip(p,p[1:]):
    assert t<u and abs(y-x)<=u-t
    assert -1<=x<=1 and -1<=y<=1
families=[(-1,Q(3,7)),(Q(-1,2),Q(4,7))]
expected=Q(0)
for x,w in families:
    captures=[first_meeting(path(1,x,s),p) for s in [1,-1]]
    expected+=w*sum(captures)/2
    print(f'M1 start {x}, reflected pair: capture times {captures}; family mass {w}')
assert expected==Q(901,448)
restricted_limit=Q(13,7)
assert expected>restricted_limit
print('Unrestricted response payoff:',expected,float(expected))
print('Fixed-infinitesimal-family supremum:',restricted_limit,float(restricted_limit))
print('Strict improvement:',expected-restricted_limit)
