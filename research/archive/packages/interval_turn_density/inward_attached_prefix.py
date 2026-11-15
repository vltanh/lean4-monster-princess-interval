"""Ordered positive inverse for an added nondecreasing inward density h.

For fixed (a,u,c), the derivative of the total prefix score is
 target_old(a,V)+j_a(V)-alpha_old(a,U)-(1+c-2V)h(U).
It is nonincreasing in U and nondecreasing in V on U>=max(a,V), using
nondecreasing k,h and the signed-M3 edge conditions.  The smallest crossing
is therefore ordered.  This module approximates that curve by affine pieces;
the frozen feature integrals themselves are evaluated analytically.
"""
import numpy as np
from numba import njit

from m3_attached_oracle import alpha, target, beta_integral_row, M3_TURN
from separated_oracle import value_at
from uniform_inward_prefix import primitive


@njit
def inward_alpha(a, c, V, U, knots, p, k, h):
    U = min(U, 1.-1e-12)
    return alpha(a, U, knots, p, k)+(1.+c-2.*V)*value_at(U, knots, h)


@njit
def inward_target(a, V, knots, p, k, h, left, right, s0, correction):
    j = max(0., primitive(a, knots, h)-primitive(abs(V), knots, h))
    return target(a, V, knots, p, k, left, right, s0, correction)+j


@njit
def derivative(a, c, V, U, knots, p, k, h, left, right, s0, correction):
    return (inward_target(a, V, knots, p, k, h, left, right, s0, correction)
            -inward_alpha(a, c, V, U, knots, p, k, h))


@njit
def inward_prefix_value(a, u, c, V, knots, p, k, h, left, right, s0, correction):
    lower = max(u, V)
    if derivative(a, c, V, lower+1e-12, knots, p, k, h,
                  left, right, s0, correction) <= 1e-13:
        return lower
    for j in range(len(k)):
        lo, hi = max(lower, knots[j]), knots[j+1]
        if hi <= lo:
            continue
        if derivative(a, c, V, lo+1e-12, knots, p, k, h,
                      left, right, s0, correction) <= 1e-13:
            return lo
        if derivative(a, c, V, hi-1e-12, knots, p, k, h,
                      left, right, s0, correction) > 1e-13:
            continue
        for _ in range(42):
            mid = (lo+hi)/2.
            if derivative(a, c, V, mid, knots, p, k, h,
                          left, right, s0, correction) <= 0.:
                hi = mid
            else:
                lo = mid
        return hi
    return 1.


@njit
def inward_prefix(parameters, knots, variables, h, left, right, s0,
                   tolerance=2e-7):
    a, u, c, y = parameters
    n = len(knots)-1
    k = variables[1+2*n:1+3*n]
    p = variables[1:1+n]+variables[1+n:1+2*n]
    result = np.zeros((4096, 4))
    count = 0
    if c <= 0.:
        return result, count
    correction = beta_integral_row(left, min(right, a), knots, s0+6.)@variables
    basecuts = np.zeros(len(knots)+7)
    nb = 0
    for value in (0., c, u, a, M3_TURN, s0):
        if 0. <= value <= c:
            basecuts[nb] = value
            nb += 1
    for value in knots:
        if 0. < value < c:
            basecuts[nb] = value
            nb += 1
    basecuts = np.sort(basecuts[:nb])
    for bi in range(nb-1):
        blo, bhi = basecuts[bi], basecuts[bi+1]
        if bhi <= blo+1e-13:
            continue
        eps = min(1e-10, (bhi-blo)*1e-5)
        cuts = np.zeros(2*len(knots)+8)
        nc = 2
        cuts[0], cuts[1] = blo, bhi
        for ui in range(len(knots)+1):
            U = u if ui == len(knots) else knots[ui]
            if U < u-1e-12 or U < bhi-1e-12 or U > 1.:
                continue
            for side in (-1., 1.):
                level = U+side*1e-10
                dl = derivative(a, c, blo+eps, level, knots, p, k, h,
                                left, right, s0, correction)
                dr = derivative(a, c, bhi-eps, level, knots, p, k, h,
                                left, right, s0, correction)
                if dl < -1e-12 and dr > 1e-12:
                    lo, hi = blo, bhi
                    for _ in range(40):
                        mid = (lo+hi)/2.
                        if derivative(a, c, mid, level, knots, p, k, h,
                                      left, right, s0, correction) >= 0.:
                            hi = mid
                        else:
                            lo = mid
                    cuts[nc] = (lo+hi)/2.
                    nc += 1
        cuts = np.sort(cuts[:nc])
        for ci in range(nc-1):
            lo, hi = cuts[ci], cuts[ci+1]
            if hi <= lo+1e-12:
                continue
            stack = np.zeros((2048, 3))
            stack[0] = np.array([lo, hi, 0.])
            ns = 1
            while ns:
                ns -= 1
                l, r, depth = stack[ns]
                delta = min(1e-11, (r-l)*1e-5)
                vl = max(l, inward_prefix_value(a, u, c, l+delta, knots, p, k, h,
                                               left, right, s0, correction))
                vr = max(r, inward_prefix_value(a, u, c, r-delta, knots, p, k, h,
                                               left, right, s0, correction))
                vm = inward_prefix_value(a, u, c, (l+r)/2., knots, p, k, h,
                                          left, right, s0, correction)
                vq1 = inward_prefix_value(a, u, c, (3*l+r)/4., knots, p, k, h,
                                           left, right, s0, correction)
                vq3 = inward_prefix_value(a, u, c, (l+3*r)/4., knots, p, k, h,
                                           left, right, s0, correction)
                error = max(abs(vm-(vl+vr)/2.), abs(vq1-(3*vl+vr)/4.),
                            abs(vq3-(vl+3*vr)/4.))
                if error > tolerance and depth < 14. and r-l > 2e-10:
                    mid = (l+r)/2.
                    stack[ns] = np.array([mid, r, depth+1.])
                    stack[ns+1] = np.array([l, mid, depth+1.])
                    ns += 2
                    continue
                if count >= len(result):
                    raise ValueError('Too many inward prefix segments')
                slope = max(0., (vr-vl)/(r-l))
                result[count] = np.array([l, r, slope, vl-slope*l])
                count += 1
    return result, count
