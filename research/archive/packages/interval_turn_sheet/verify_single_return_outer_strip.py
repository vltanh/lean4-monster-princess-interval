#!/usr/bin/env python3
"""Exact four-corner certificate for the all-count terminal single-return strip.

All successful assertions use fractions, not approximate floating arithmetic.
The analytical proof deriving the inequalities is in
research/12-global-closure/LOW_SURPLUS_UNIFORM_SINGLE_RETURN.md.
"""
from fractions import Fraction as Q

k = Q(655898601421, 62500000000)
ell = Q(820954217, 12500000000)
d = k - ell
r = ell / k
A = k / 8 - ell / 2
theta_hi = Q(321, 25000)
H_1 = 6 * ell / (k - 2 * ell)
H_max = Q(1, 16)
c_lo = Q(2, 5)
c_hi = 3 * k / 8
margin = Q(1, 125000)

def g_upper(H, y):
    th = theta_hi
    return (A * H**2 - Q(3, 2) * ell * H + Q(9, 4) * ell * th
            + y * (Q(3, 2) * th**2 - H / 2)
            + th * y**2 / (4 * ell))

def quadratic_coefficient(c):
    return A - c / 2 + theta_hi * c**2 / (4 * ell)

def r_of_theta(theta):
    return theta / (2 * (1 + theta)**2)

assert 0 < r < Q(1, 8)
assert r_of_theta(theta_hi) > r  # strict theta < theta_hi by monotonicity
assert 0 < H_1 < H_max
assert 0 < c_lo < c_hi < d
for c in (c_lo, c_hi):
    assert quadratic_coefficient(c) > 0
    for H in (H_1, H_max):
        v = g_upper(H, c * H)
        assert v < -margin, (c, H, v)
        print(f"exact corner: c={c}, H={H}, value={v.numerator}/{v.denominator}, negative=true")
print("ALL 4 CORNERS STRICTLY BELOW -1/125000; required convexities and theta enclosure hold")
