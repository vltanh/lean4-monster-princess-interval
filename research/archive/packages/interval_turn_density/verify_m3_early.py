#!/usr/bin/env python3
"""Exact first-inverse identities and flat-density algebra for early M3.

Direct intersections use independent finite path fixtures. The general
identity retains beta(1), so a center-wait atom is not silently replaced
by endpoint capture. This establishes formulas, not a matching strategy.
"""
from collections import Counter
from fractions import Fraction as Q

from verify_positive_cdf_sheet import finite_fixtures, first_capture
from verify_two_interior_cdf import route


def inverse(path, level, sign):
    if sign*path.value(Q(0)) >= level:
        return Q(0)
    for lo, hi, slope, intercept in path.segments:
        velocity = 1+sign*slope
        start = velocity*lo+sign*intercept
        end = velocity*hi+sign*intercept
        if start >= level:
            return lo
        if end >= level:
            assert velocity > 0
            return (level-sign*intercept)/velocity
    raise AssertionError(('inverse not found', level, sign))


def twice_cost(path, start, s):
    """The two reflected first-capture times, with all closed contacts."""
    a, z = path.value(Q(0)), abs(start)
    if a == 0 and z == 0:
        return Q(0)
    alpha = lambda u: inverse(path, u, 1)
    beta = lambda v: inverse(path, v, -1)
    phi = lambda v: 2*beta(v)-v
    second = beta(s) if phi(s) <= 1 else beta(3)
    if start >= 0:
        first = alpha(s) if a < z else (beta(-z) if phi(-z) <= s else beta(1))
        return first+second
    first = alpha(z) if a <= z else second
    return first+(beta(z) if phi(z) <= s else beta(1))


def ceiling_twice_cost(path, start, s):
    """The upper envelope using beta(1)<=2 and beta(3)<=4."""
    a, z = path.value(Q(0)), abs(start)
    if a == 0 and z == 0:
        return Q(0)
    alpha = lambda u: inverse(path, u, 1)
    beta = lambda v: inverse(path, v, -1)
    phi = lambda v: 2*beta(v)-v
    second = beta(s) if phi(s) <= 1 else Q(4)
    if start >= 0:
        first = alpha(s) if a < z else (beta(-z) if phi(-z) <= s else Q(2))
        return first+second
    first = alpha(z) if a <= z else second
    return first+(beta(z) if phi(z) <= s else Q(2))


def main():
    counts = Counter()
    paths = [path for law in finite_fixtures() for _, path in law.paths]
    for path in paths:
        starts = {Q(j, 16) for j in range(16)}
        a = path.value(Q(0))
        if a < 1:
            starts.add(a)
        for z in starts:
            turns = {z+(1-z)*Q(j, 8) for j in range(9)}
            for v in (z, -z):
                u = 2*inverse(path, v, -1)-v
                if z <= u <= 1:
                    turns.add(u)
            for s in turns:
                for sign in (1, -1):
                    start = sign*z
                    monster = route(start, s, Q(1))
                    actual = first_capture(path, monster, 1)+first_capture(path, monster, -1)
                    predicted = twice_cost(path, start, s)
                    assert predicted == actual, (start, s, a, predicted, actual)
                    counts['signed first-capture identities'] += 1
                    ceiling = ceiling_twice_cost(path, start, s)
                    assert actual <= ceiling
                    counts['endpoint ceiling inequalities'] += 1
                    if inverse(path, Q(1), -1) == 2:
                        assert actual == ceiling
                        counts['no time-one contact equalities'] += 1

    # Affine k: exact solution of W*m_s-2*m=k'. The edge coefficient
    # C=k(r)-base is arbitrary nonnegative; all checks use rational values.
    for sign in (1, -1):
        for z in (Q(0), Q(1, 8), Q(1, 4), Q(1, 2)):
            for r in (Q(5, 8), Q(3, 4), Q(7, 8)):
                if z >= r:
                    continue
                for edge in (Q(0), Q(1, 20), Q(1, 3)):
                    for slope in (Q(0), Q(1, 5), Q(1)):
                        wr = 4+sign*z-r
                        constant = wr*edge+slope*wr*wr/2
                        for j in range(1, 8):
                            u = r+(1-r)*Q(j, 8)
                            w = 4+sign*z-u
                            density = constant/(w*w)-slope/2
                            derivative = 2*constant/(w*w*w)
                            marginal = constant*(1/w-1/wr)-slope*(u-r)/2
                            assert w*derivative-2*density == slope
                            assert w*density-marginal == edge+slope*(u-r)
                            assert density >= 0 and derivative >= 0 and marginal >= 0
                            counts['flat-corridor density identities'] += 3

    print(f'PASS: {sum(counts.values())} exact early-M3 checks')
    for label, count in counts.items():
        print(f'  {label}: {count}')
    print('Scope: capture and adjoint identities; no equilibrium or global value claim')


if __name__ == '__main__':
    main()
