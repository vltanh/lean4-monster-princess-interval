"""Ordered negative-prefix blocks for the analytic signed-M3 tail column.

No density bins or optimization coefficients are added. A continuous tail
interval enters adjacent-violator pooling through its exact integrated
mean. Its coefficient decreases in V, so the cumulative pooling inequality
holds inside that interval as well as across the finite step intervals.

The fixed tail feature uses the same analytic moments and numerical
quadrature precision as singular_tail_basis. It is discovery arithmetic,
not a certified scalar supremum.
"""
import numpy as np
from numba import njit

from m3_attached_oracle import M3_LEFT, M3_RIGHT, M3_TURN
from separated_oracle import value_at
from singular_tail_basis import (tail_feature, density, moment, kbar, kcum,
    m3_cumulative, CUTOFF)


@njit
def tail_mass(lo, hi):
    return moment(1.-lo, 2./3., 0, 1.)-moment(1.-hi, 2./3., 0, 1.)


@njit
def negative_tail_change(parameters, negative, count):
    a, u, c, y = parameters
    total = 0.
    for i in range(count):
        vl, vr, slope, level = negative[i]
        if slope != 0.:
            raise ValueError('Negative tail inverses must be constant blocks')
        width = vr-vl
        total += (level-u)*tail_mass(-vr, -vl)
        total += width*(kbar(level)-kbar(u))
        overlap = max(0., min(M3_RIGHT, -vl)-max(M3_LEFT, -vr))
        total += overlap*(kcum(level)-kcum(u))
        total -= width*(m3_cumulative(level, max(a, M3_LEFT), M3_RIGHT, 1)
                        -m3_cumulative(u, max(a, M3_LEFT), M3_RIGHT, 1))
    return total/4.


@njit
def general_tail_feature(parameters, packed, count, knots, profile, left, right):
    split = 0
    while split < count and packed[split, 0] < 0.:
        split += 1
    value = tail_feature(parameters, packed[split:count], count-split, knots, profile, left, right)
    if split:
        value += negative_tail_change(parameters, packed[:split], split)
    return value


@njit
def total_k(U, knots, k, amplitude):
    if U >= 1. and amplitude > 0.:
        return np.inf
    return value_at(U, knots, k)+amplitude*density(U, 1./6., .5)


@njit
def first_k_crossing(target, lower, upper, knots, k, amplitude):
    if total_k(lower, knots, k, amplitude) >= target:
        return lower
    if total_k(upper, knots, k, amplitude) < target:
        return upper
    for j in range(len(k)):
        lo, hi = max(lower, knots[j]), min(upper, knots[j+1])
        if hi < lo:
            continue
        if total_k(lo, knots, k, amplitude) >= target:
            return lo
        if hi > CUTOFF and total_k(hi, knots, k, amplitude) >= target:
            for _ in range(58):
                mid = (lo+hi)/2.
                if total_k(mid, knots, k, amplitude) >= target:
                    hi = mid
                else:
                    lo = mid
            return hi
    return upper


@njit
def ordinary_tail_blocks(lo, hi, lower, upper, knots, p, k, amplitude):
    result = np.zeros((2*len(knots)+4, 4))
    if hi <= lo:
        return result, 0
    cuts = np.empty(len(knots)+2)
    nc = 2
    cuts[0], cuts[1] = lo, hi
    for z in knots:
        if lo < -z < hi:
            cuts[nc] = -z
            nc += 1
    cuts = np.sort(cuts[:nc])
    stack = np.zeros((len(cuts), 4))
    ns = 0
    for j in range(len(cuts)-1):
        l, r = cuts[j], cuts[j+1]
        if r <= l:
            continue
        weight = r-l
        coefficient_mass = weight*value_at(-(l+r)/2., knots, p)+amplitude*tail_mass(-r, -l)
        stack[ns] = np.array([l, r, weight, coefficient_mass])
        ns += 1
        while ns > 1 and stack[ns-2, 3]*stack[ns-1, 2] > stack[ns-1, 3]*stack[ns-2, 2]:
            stack[ns-2, 1] = stack[ns-1, 1]
            stack[ns-2, 2] += stack[ns-1, 2]
            stack[ns-2, 3] += stack[ns-1, 3]
            ns -= 1
    count = 0
    for j in range(ns):
        target = stack[j, 3]/stack[j, 2]
        chosen = first_k_crossing(target, lower, upper, knots, k, amplitude)
        if count and abs(result[count-1, 3]-chosen) < 1e-13:
            result[count-1, 1] = stack[j, 1]
        else:
            result[count] = np.array([stack[j, 0], stack[j, 1], 0., chosen])
            count += 1
    return result, count


@njit
def negative_tail_cases(parameters, knots, base_variables, amplitude):
    a, u, c, y = parameters
    n = len(knots)-1
    p = base_variables[1:1+n]+base_variables[1+n:1+2*n]
    k = base_variables[1+2*n:1+3*n]
    lo, hi = -a, min(c, 0.)
    first = np.zeros((2*len(knots)+4, 4))
    second = np.zeros_like(first)
    if hi <= lo:
        return first, 0, second, -1
    if hi <= -M3_RIGHT:
        first, nf = ordinary_tail_blocks(lo, hi, a, u, knots, p, k, amplitude)
        return first, nf, second, -1
    nf = -1
    if a <= M3_TURN:
        first, nf = ordinary_tail_blocks(lo, hi, a, min(u, M3_TURN), knots, p, k, amplitude)
    ns = -1
    if a >= M3_RIGHT and u >= M3_TURN:
        second, ns = ordinary_tail_blocks(lo, min(hi, -M3_RIGHT), a, u, knots, p, k, amplitude)
        start = max(lo, -M3_RIGHT)
        if hi > start:
            level = max(a, M3_TURN)
            if ns:
                level = max(level, second[ns-1, 3])
            if ns and abs(second[ns-1, 3]-level) < 1e-13:
                second[ns-1, 1] = hi
            else:
                second[ns] = np.array([start, hi, 0., level])
                ns += 1
    return first, nf, second, ns
