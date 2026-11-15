#!/usr/bin/env python3
"""Exact rational parameter enclosures for the all-count two-source Green theorem.

This is a parameter-certificate audit, not a substitute for the analytic
all-m minimization/constructive-limit proof in the accompanying note.
"""
from fractions import Fraction as Q

k = Q(655898601421, 62500000000)
ell = Q(820954217, 12500000000)
d = k - ell
r = ell / k
A = k / 8 - ell / 2
Tlo, Thi = Q(12839, 1000000), Q(321, 25000)
Hlo, Hhi = Q(1, 20), Q(1, 16)
c = Q(2, 5)
ymax = c * Hhi


def rat_of_th(x):
    return x / (2 * (1 + x)**2)

assert 0 < Tlo < Thi < Q(2, 3)
assert 0 < rat_of_th(Tlo) < r < rat_of_th(Thi) < Q(1, 8)
assert Hlo >= 6 * ell / (k - 2 * ell)
assert c < d
assert Thi * c < ell  # derivative of the switching quadratic strictly negative

# Rigorous upper/lower algebraic enclosures across whole rectangle.
delta_lower = Hlo - (Thi * (3 + ymax / ell)) / (1 - Thi)
rhs_upper = 12 * Thi**3 * ymax / (ell * (1 - Thi)**2)
assert delta_lower > 0
assert delta_lower**2 > rhs_upper
print('all-m count-independent square gap (rational) =', delta_lower**2 - rhs_upper)

# D = E_one - E_infinity = C(H) - H*y/2 + theta*y*y/(4ell).
def D(H, y, th):
    return (A * H**2 - Q(3, 2) * ell * H + Q(9, 4) * ell * th
            - H * y / 2 + th * y**2 / (4 * ell))

# D(H,0)>0 by theta LOWER enclosure, positivity of derivative wrt H.
assert 2 * A * Hlo - Q(3, 2) * ell > 0
assert D(Hlo, 0, Tlo) > 0

# D(H,c*H)<0 by theta UPPER enclosure, positive leading H^2 coefficient,
# convexity in H therefore maximum on closed interval is at its endpoints.
assert A - c/2 + Thi*c*c/(4*ell) > 0
for H in (Hlo,Hhi):
    assert D(H,c*H,Thi) < 0, (H, D(H,c*H,Thi))
    print(f'exact switching signs: H={H}, D(H,0)>0; D(H,2H/5)<0')

# Exact rational proof facts behind the constructive no-hinge sequence.
# For theta satisfying r=theta/(2(1+theta)^2),
# d*theta/ell = 2+3theta+2theta^2 > 1 and d/ell > 1.
assert d > ell
assert 2 + 3*Tlo + 2*Tlo*Tlo > 1
print('ALL EXACT PARAMETER CHECKS PASS; no turn-count cutoff')


# Independent exact rational physical-duration / energy fixtures for an
# affine model whose theta is rational and obeys the same Riccati identity.
theta0 = Q(1, 80)
k0 = Q(10)
ell0 = k0 * rat_of_th(theta0)
d0 = k0 - ell0
A0 = k0 / 8 - ell0 / 2
C00 = ell0 / (4 * theta0)
H0, y0 = Q(3, 50), Q(1, 100)
alpha0, gamma0 = theta0 * y0 / ell0, 3 * theta0
Einf0 = -C00 * (alpha0**2 + gamma0**2) - y0**2 / (8*k0)


def exact_approach(n):
    w = (H0 - (alpha0 + gamma0)*(1-theta0**n)/(1-theta0)) / n
    h = [alpha0*theta0**j + gamma0*theta0**(n-1-j) + w for j in range(n)]
    assert w > 0 and sum(h) == H0
    assert d0*h[0] >= y0
    assert all(d0*h[j] >= ell0*h[j-1] for j in range(1,n))
    E = (A0*sum(v*v for v in h)
         - ell0/2*sum(h[j]*h[j+1] for j in range(n-1))
         - 3*ell0/2*h[-1] - y0/2*h[0] - y0**2/(8*k0))
    assert E > Einf0
    return E - Einf0

previous = exact_approach(2)
for n in (4,8,16,32,64):
    difference = exact_approach(n)
    assert difference < previous, (n, difference, previous)
    previous = difference
print('Exact rational Green family: 6 physically productive test cases, decreasing gaps')
