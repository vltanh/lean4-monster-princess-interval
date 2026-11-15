"""A concrete signed-small-start M3 attachment to the two-late-sheet law.

Geometry is intentionally fixed on the existing density coordinates:
signed M3 starts [0,1/8], first turns (1/4,1), second turn V=1.
Negative early M2 starts [1/8,1/2], turn floor15/16, retain their old
line marginal but subtract BOTH full M3 beta prices from their edge.
The remaining late geometry is supplied by discover_separated.

That full negative-M3 subtraction is conservative for initial a<1/8.
The local derivative above the negative early edge is
 -J_P,a - integral_(z>a)mN(z,U), which is nonpositive. For a>=1/8
both terms vanish, giving an actual equality corridor. The ordered
first-crossing prefix is therefore still globally maximizing.

Logarithmic M3 features are analytic. The cross-price start integrals
and any smooth low-initial prefix are evaluated to floating precision;
the discovery output is not a certified game bound.
"""
import numpy as np
from numba import njit
from numpy.polynomial.legendre import leggauss

from separated_oracle import (affine_integral, beta, bin_at,
                              features_affine, phi_integral, value_at)
from positive_sheet_oracle import positive_sheet_features
from m3_early_oracle import (m3_early_features, m3_early_threshold,
                             m3_early_price_row)


M3_LEFT, M3_RIGHT, M3_TURN = 0., .125, .25
GAUSS_NODES, GAUSS_WEIGHTS = leggauss(12)


@njit
def positive_late_profile(knots):
    v = np.ones(len(knots)-1)
    for j in range(len(v)):
        if knots[j] >= .5-1e-12 and knots[j+1] <= .625+1e-12:
            v[j] = 17./16.
    return v


@njit
def full_m3_beta_row(s, knots):
    return (m3_early_price_row(-1., s, knots, M3_LEFT, M3_RIGHT,
                              M3_TURN, 1, False)
            +m3_early_price_row(2., s, knots, M3_LEFT, M3_RIGHT,
                               M3_TURN, -1, True))


@njit
def beta_integral_row(lo, hi, knots, denominator):
    """Integral of both full beta rows, optionally divided by denominator-z."""
    row = np.zeros(1+4*(len(knots)-1))
    if hi <= lo:
        return row
    for j in range(len(knots)-1):
        left, right = max(lo, knots[j]), min(hi, knots[j+1])
        if right <= left:
            continue
        middle, half = (left+right)/2., (right-left)/2.
        for q in range(len(GAUSS_NODES)):
            z = middle+half*GAUSS_NODES[q]
            factor = half*GAUSS_WEIGHTS[q]
            if denominator > 0.:
                factor /= denominator-z
            row += factor*full_m3_beta_row(z, knots)
    return row


@njit
def negative_edge_correction(parameters, segments, count, knots, left, right, s0):
    a, u, c, y = parameters
    row = -max(0., u-s0)*beta_integral_row(left, min(right, c), knots, 0.)
    row += (1.-s0)**2*beta_integral_row(max(left, c), right, knots, s0+6.)
    reflected = (affine_integral(s0, 1., -4., 1.)
                 +phi_integral(s0, 1., parameters, segments, count))
    row -= reflected*beta_integral_row(left, min(right, a), knots, s0+6.)
    return row/4.


@njit
def attached_features(parameters, segments, count, knots, negative_profile,
                      left, right, s0, edge_trace=True):
    if not edge_trace:
        raise ValueError('The M3 attachment uses the corrected nonzero early edge')
    row = features_affine(parameters, segments, count, knots, negative_profile,
                          left, right, s0, True)
    row += positive_sheet_features(parameters, knots, positive_late_profile(knots))
    row += m3_early_features(parameters, segments, count, knots,
                            M3_LEFT, M3_RIGHT, M3_TURN, 1)
    row += m3_early_features(parameters, segments, count, knots,
                            M3_LEFT, M3_RIGHT, M3_TURN, -1)
    row += negative_edge_correction(parameters, segments, count, knots, left, right, s0)
    return row


@njit
def alpha(a, U, knots, p, k):
    U = min(U, 1.-1e-12)
    return value_at(U, knots, k)+m3_early_threshold(
        a, U, knots, p, k, M3_LEFT, M3_RIGHT, M3_TURN, 1, False)


@njit
def target(a, V, knots, p, k, left, right, s0, edge_correction):
    result = value_at(V, knots, k)+beta(a, V, knots, k, left, right, s0, True)
    if V > s0:
        result -= edge_correction
    result += m3_early_threshold(-1., V, knots, p, k,
                                 M3_LEFT, M3_RIGHT, M3_TURN, 1, False)
    result += m3_early_threshold(a, V, knots, p, k,
                                 M3_LEFT, M3_RIGHT, M3_TURN, -1, True)
    return result


@njit
def prefix_value(a, u, V, knots, p, k, left, right, s0, edge_correction):
    goal = target(a, V, knots, p, k, left, right, s0, edge_correction)
    lower = max(u, V)
    if alpha(a, lower+1e-12, knots, p, k) >= goal-1e-13:
        return lower
    for j in range(len(k)):
        lo, hi = max(lower, knots[j]), knots[j+1]
        if hi <= lo:
            continue
        if alpha(a, lo+1e-12, knots, p, k) >= goal-1e-13:
            return lo
        if alpha(a, hi-1e-12, knots, p, k) < goal-1e-13:
            continue
        for _ in range(42):
            mid = (lo+hi)/2.
            if alpha(a, mid, knots, p, k) >= goal:
                hi = mid
            else:
                lo = mid
        return hi
    return 1.


@njit
def attached_prefix(parameters, knots, variables, left, right, s0,
                    tolerance=2e-7):
    a, u, c, y = parameters
    n = len(knots)-1
    k = variables[1+2*n:1+3*n]
    p = variables[1:1+n]+variables[1+n:1+2*n]
    result = np.zeros((4096, 4))
    count = 0
    if c <= 0.:
        return result, count
    correction = beta_integral_row(left, min(right, a), knots, s0+6.) @ variables
    basecuts = np.zeros(len(knots)+6)
    nb = 0
    for value in (0., c, u, M3_TURN, s0):
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
        low_target = target(a, blo+eps, knots, p, k, left, right, s0, correction)
        high_target = target(a, bhi-eps, knots, p, k, left, right, s0, correction)
        cuts = np.zeros(2*len(knots)+8)
        nc = 2
        cuts[0], cuts[1] = blo, bhi
        for ui in range(len(knots)+1):
            U = u if ui == len(knots) else knots[ui]
            if U < u-1e-12 or U > 1.:
                continue
            for side in (-1., 1.):
                level = alpha(a, U+side*1e-10, knots, p, k)
                if low_target+1e-12 < level < high_target-1e-12:
                    lo, hi = blo, bhi
                    for _ in range(40):
                        mid = (lo+hi)/2.
                        if target(a, mid, knots, p, k, left, right, s0, correction) >= level:
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
                l, h, depth = stack[ns]
                delta = min(1e-11, (h-l)*1e-5)
                vl = max(l, prefix_value(a, u, l+delta, knots, p, k, left, right, s0, correction))
                vh = max(h, prefix_value(a, u, h-delta, knots, p, k, left, right, s0, correction))
                vm = prefix_value(a, u, (l+h)/2., knots, p, k, left, right, s0, correction)
                vq1 = prefix_value(a, u, (3*l+h)/4., knots, p, k, left, right, s0, correction)
                vq3 = prefix_value(a, u, (l+3*h)/4., knots, p, k, left, right, s0, correction)
                error = max(abs(vm-(vl+vh)/2.),
                            abs(vq1-(3*vl+vh)/4.), abs(vq3-(vl+3*vh)/4.))
                if error > tolerance and depth < 14. and h-l > 2e-10:
                    mid = (l+h)/2.
                    stack[ns] = np.array([mid, h, depth+1.])
                    stack[ns+1] = np.array([l, mid, depth+1.])
                    ns += 2
                    continue
                if count >= len(result):
                    raise ValueError('Too many curved-prefix segments')
                slope = max(0., (vh-vl)/(h-l))
                result[count] = np.array([l, h, slope, vl-slope*l])
                count += 1
    return result, count


@njit
def optimal_features_attached(parameters, knots, negative_profile, variables,
                              left, right, s0, edge_trace=True):
    segments, count = attached_prefix(parameters, knots, variables, left, right, s0)
    return attached_features(parameters, segments, count, knots, negative_profile,
                              left, right, s0, edge_trace)


def freeze_response_attached(parameters, knots, negative_profile, variables,
                             left, right, s0, edge_trace=True):
    segments, count = attached_prefix(parameters, knots, variables, left, right, s0)
    return (attached_features(parameters, segments, count, knots, negative_profile,
                               left, right, s0, edge_trace), segments[:count].copy())
