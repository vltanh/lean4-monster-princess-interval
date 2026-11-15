"""Continuous-tail positive-prefix oracle on a fixed analytic join."""
import numpy as np
from numba import njit
from m3_attached_oracle import (alpha,target,beta_integral_row,M3_TURN)
from singular_tail_basis import (density,m3_price,negative_early_price)

@njit
def alpha_tail(a,U,knots,p,k,amplitude):
    if U >= 1. and amplitude > 0.:
        return np.inf
    U=min(U,1.-1e-15)
    return (alpha(a,U,knots,p,k)
        +amplitude*(density(U,1./6.,.5)+m3_price(a,U,1,False)))

@njit
def target_tail(a,V,knots,p,k,left,right,s0,correction,amplitude):
    return (target(a,V,knots,p,k,left,right,s0,correction)
        +amplitude*(density(V,1./6.,.5)+negative_early_price(a,V,left,right)
                    +m3_price(-1.,V,1,False)+m3_price(a,V,-1,True)))

@njit
def tail_prefix_value(a, u, V, knots, p, k, left, right, s0, edge_correction, amplitude):
    goal = target_tail(a, V, knots, p, k, left, right, s0, edge_correction, amplitude)
    lower = max(u, V)
    if alpha_tail(a, np.nextafter(lower, 1.), knots, p, k, amplitude) >= goal-1e-13:
        return lower
    for j in range(len(k)):
        lo, hi = max(lower, knots[j]), knots[j+1]
        if hi <= lo:
            continue
        if alpha_tail(a, np.nextafter(lo, 1.), knots, p, k, amplitude) >= goal-1e-13:
            return lo
        # The step helper snaps within 1e-13 to the right-hand bin.  A
        # nextafter probe would therefore read the wrong trace here.
        endpoint = hi if hi == 1. else hi-1e-12
        if alpha_tail(a, endpoint, knots, p, k, amplitude) < goal-1e-13:
            continue
        for _ in range(42):
            mid = (lo+hi)/2.
            if alpha_tail(a, mid, knots, p, k, amplitude) >= goal:
                hi = mid
            else:
                lo = mid
        return hi
    return 1.


@njit
def tail_prefix(parameters, knots, variables, left, right, s0, amplitude,
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
        low_target = target_tail(a, blo+eps, knots, p, k, left, right, s0, correction, amplitude)
        high_target = target_tail(a, bhi-eps, knots, p, k, left, right, s0, correction, amplitude)
        cuts = np.zeros(2*len(knots)+8)
        nc = 2
        cuts[0], cuts[1] = blo, bhi
        for ui in range(len(knots)+1):
            U = u if ui == len(knots) else knots[ui]
            if U < u-1e-12 or U > 1.:
                continue
            for side in (-1., 1.):
                level = alpha_tail(a, U+side*1e-10, knots, p, k, amplitude)
                if low_target+1e-12 < level < high_target-1e-12:
                    lo, hi = blo, bhi
                    for _ in range(40):
                        mid = (lo+hi)/2.
                        if target_tail(a, mid, knots, p, k, left, right, s0, correction, amplitude) >= level:
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
                vl = max(l, tail_prefix_value(a, u, l+delta, knots, p, k, left, right, s0, correction, amplitude))
                vh = max(h, tail_prefix_value(a, u, h-delta, knots, p, k, left, right, s0, correction, amplitude))
                vm = tail_prefix_value(a, u, (l+h)/2., knots, p, k, left, right, s0, correction, amplitude)
                vq1 = tail_prefix_value(a, u, (3*l+h)/4., knots, p, k, left, right, s0, correction, amplitude)
                vq3 = tail_prefix_value(a, u, (l+3*h)/4., knots, p, k, left, right, s0, correction, amplitude)
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
