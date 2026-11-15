#!/usr/bin/env python3
"""Exact rational fixtures for a no-regularity running-record envelope lemma.

The universal lemma and CDF integral interchange are proved analytically in
research/12-global-closure/GLOBAL_CDF_VARIATIONAL_STATIONARITY.md.
"""
from fractions import Fraction as Q
from itertools import product

fvals = (Q(0), Q(1,3), Q(2,3))
gvals = (Q(-1), Q(-1,3), Q(0), Q(1,3), Q(1))
lam = Q(1,100)
tested=0
ties=0
for f in product(fvals, repeat=3):
    for g in product(gvals, repeat=3):
        af = min(f)
        bf = max(f)
        df = min(g[i] for i in range(3) if f[i]==af)
        dg = max(g[i] for i in range(3) if f[i]==bf)
        derivative_inf = (min(f[i]+lam*g[i] for i in range(3))-af)/lam
        derivative_sup = (max(f[i]+lam*g[i] for i in range(3))-bf)/lam
        assert derivative_inf == df, (f,g,df,derivative_inf)
        assert derivative_sup == dg, (f,g,dg,derivative_sup)
        tested+=1
        if f.count(af)>1 or f.count(bf)>1:
            ties+=1
assert tested==3375
print(f'finite record envelope: {tested} exact min/max fixtures; {ties} have active ties')

# Genuine non-attainment: f_j=1/j and g_j=-1 for odd j, +1 for even j.
# inf_j f_j=0 not attained; for every lambda>0,
# -lambda <= inf_j(f_j+lambda*g_j) <= -lambda+lambda^2
# by taking an odd j with j>=lambda^-2. Hence the derivative is -1.
for n in (4,8,16,32,64,128):
    a = Q(1,n)
    j = n*n+1  # odd, so g_j=-1 and 1/j < 1/n^2
    assert j%2==1 and Q(1,j) <= a*a
    lower = -a
    upper = -a + Q(1,j)
    assert lower <= upper <= -a+a*a
    quotient_lower = lower/a
    quotient_upper = upper/a
    assert quotient_lower==-1 and quotient_upper <= -1+a
    print(f'nonattained inf, lambda=1/{n}: derivative quotient in [{quotient_lower},{quotient_upper}]')
print('Exact derivative fixtures passed; infinite-dimensional theorem remains a hand proof')
