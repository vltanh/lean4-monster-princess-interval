#!/usr/bin/env python3
"""Exact algebra checks for SIGNED_M1_FUNCTIONAL.md; not a saddle test."""
from fractions import Fraction as Q
import importlib.util
from pathlib import Path


# Reuse only the rational arithmetic primitives, not the previous formulas.
source = Path(__file__).resolve().parents[1] / 'interval_candidate_densities' / 'verify.py'
spec = importlib.util.spec_from_file_location('rational_dual', source)
arithmetic = importlib.util.module_from_spec(spec)
spec.loader.exec_module(arithmetic)
Dual, poly, integral = arithmetic.Dual, arithmetic.poly, arithmetic.integral


def evaluate(values, fs, gs, hs, ls):
    a0, u0, c0, y0 = values
    a, u, c, y = [Dual(v, tuple(int(i == j) for j in range(4)))
                   for i, v in enumerate(values)]
    zero, one, w0 = Dual(0), Dual(1), Q(1, 7)
    cumulatives = [lambda z, coeffs=cs: integral(coeffs, zero, z)
                   for cs in (fs, gs, hs, ls)]
    F, G, H, L = cumulatives
    fb, gb = lambda z: F(one)-F(z), lambda z: G(one)-G(z)
    K0 = lambda z: H(z)+L(z)
    kb = lambda z: K0(one)-K0(z)
    f, g, h, ell = [lambda z, coeffs=cs: poly(coeffs, z)
                    for cs in (fs, gs, hs, ls)]
    k = lambda z: h(z)+ell(z)
    negc = -c if c0 < 0 else zero
    q = c if c0 > u0 else u
    r = c if c0 < u0 else u

    # Assemble 4J directly from capture-time integrals for each family.
    j4 = w0*(5+c)
    j4 += integral(fs, zero, negc, 8, -4)
    j4 += integral(fs, negc, a, u+6, -3)
    j4 += integral(fs, a, one, 8+c, -3)
    j4 += 12*G(negc)+integral(gs, negc, a, u+4, -1)+(5+c)*gb(a)
    j4 += 4*H(a)+integral(hs, a, u, -a, 1)
    j4 += integral(hs, q, one, c, 1)
    j4 += integral(ls, zero, a, 6, 2)+integral(ls, a, u, -a, 1)
    j4 += integral(ls, q, one, c, 1)
    if c0 >= u0:
        j4 += 2*integral(hs, u, c, 0, 1)
        j4 += 2*integral(ls, u, c, 0, 1)
    if c0 < 0:
        j4 += 8*H(one)+2*integral(ls, zero, one, 1, 1)
    else:
        j4 += integral(hs, zero, r, u, 1)+8*(H(one)-H(c))
        j4 += integral(ls, zero, r, u, 1)+2*integral(ls, c, one, 1, 1)
        if c0 >= u0:
            j4 += 2*integral(hs, u, c, 0, 1)
            j4 += 2*integral(ls, u, c, 0, 1)

    negy = -y if y0 < 0 else zero
    posc = c if c0 > 0 else zero
    posy = y if y0 > 0 else zero
    k4 = (j4+(y-c)*fb(a)-integral(fs, negy, negc, 1, -1)
          -integral(ls, posc, posy, 1, 1))

    ea = ((u-2-y)*f(a)+(u-1-a-c)*g(a)+4*h(a)
          +(6+2*a)*ell(a)-K0(u)+K0(a))
    if c0 < 0:
        eu = F(a)-F(-c)+G(a)-G(-c)-(a+c)*k(u)
        ec = w0+gb(a)+kb(u)-(1-u)*f(-c)-(8-c-u)*g(-c)
    else:
        eu = F(a)+G(a)+K0(r)-(a+r)*k(u)
        ec = w0+gb(a)+kb(q)-(8-c-q)*h(c)-(1-q)*ell(c)
    ey = fb(a)-(1+y)*(f(-y) if y0 < 0 else ell(y))
    assert k4.gradient == tuple(v.value for v in (ea, eu, ec, ey)), values

    # The endpoint-start y=c condition is tangential, not partial in c.
    if a0 == u0 == 1 and y0 == c0:
        if c0 > 0:
            endpoint = w0-(7-c)*h(c)-(1+c)*ell(c)
        else:
            endpoint = w0-(1+c)*f(-c)-(7-c)*g(-c)
        assert k4.gradient[2]+k4.gradient[3] == endpoint.value

    # Check the diagonal central branch tangent in a and u.
    if u0 == a0 and c0 == y0 == 1:
        diagonal = ((a-3)*f(a)-2*g(a)+(4-2*a)*h(a)
                    +6*ell(a)+F(a)+G(a)+K0(a))
        assert k4.gradient[0]+k4.gradient[1] == diagonal.value

    return k4.value


def main():
    densities = [
        ((1,), (2,), (3,), (4,)),
        ((1, 0, 1), (2, -1), (1, 2, 0, 1), (0, 3, 2)),
        ((0, 1, 2), (1, 3, 1), (2, 0, 1), (2, -1, 1)),
    ]
    interior = [
        (2, 6, 1, 3), (2, 6, 3, 5), (2, 6, 7, 8),
        (5, 7, 2, 8), (5, 7, 6, 8), (5, 7, -4, -2),
        (5, 7, -4, 2), (5, 7, -1, 8), (6, 7, -5, -1),
    ]
    count = 0
    for den in (8, 9, 11):
        for values in interior:
            for coeffs in densities:
                evaluate(tuple(Q(v, den) for v in values), *coeffs)
                count += 1
    boundary_count = 0
    for coeffs in densities:
        for c in (Q(-2, 3), Q(-1, 5), Q(1, 5), Q(2, 3)):
            evaluate((Q(1), Q(1), c, c), *coeffs)
            boundary_count += 1
        for a in (Q(1, 5), Q(1, 2), Q(4, 5)):
            evaluate((a, a, Q(1), Q(1)), *coeffs)
            boundary_count += 1
    print(f'PASS: {count} exact signed-M1 derivative cases across all smooth branches')
    print(f'PASS: {boundary_count} exact endpoint and central-diagonal tangent checks')
    print('Scope: conditional integral identities; no equilibrium or new value bound')


if __name__ == '__main__':
    main()
