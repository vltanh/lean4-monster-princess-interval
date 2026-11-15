"""Early M3 sheets with second turn V=1: exact scalar feature primitives.

A generator of coefficient C(z), lower turn r, and signed initial position
sigma*z has density

    C(z)*(4+sigma*z-r)/(4+sigma*z-s)**2,  r<s<1.

For step k, the flat-corridor density is the lower-edge generator with
C=k(r)-p(z) (positive starts) or k(r)-k(z)-other_beta(z) (negative starts),
plus one generator of size Delta k for each later jump. The row functions
below are linear in the same (w0,f,g,k,ell) variables as separated_oracle.
They replace the corresponding U=1 M2 line, without changing its total
start marginal. These are implementation identities, not a fitted law.

The time-one beta inverse is bounded by 2 in the upper envelope. Equality
is approached by the usual legal epsilon paths with final y<1. The exact
pure-path verifier retains beta(1), including the center-wait equality face.
"""
from math import log1p

import numpy as np
from numba import njit

from separated_oracle import bin_at, value_at


@njit
def cumulative(r, lo, hi, t, sign):
    """Integral over starts and turns r<s<t of a unit generator."""
    if hi <= lo or t <= r:
        return 0.
    t = min(t, 1.)
    left = 4. + sign*lo - t
    right = 4. + sign*hi - t
    return (t-r)*sign*np.log1p((right-left)/left)


@njit
def cumulative_primitive(r, lo, hi, t, sign):
    """Integral_r^t cumulative(q)dq, with a stable convergent log series."""
    if hi <= lo or t <= r:
        return 0.
    t = min(t, 1.)
    width = t-r
    left = 4. + sign*lo-r
    right = 4. + sign*hi-r
    result = .5*np.log1p((right-left)/left)
    pl = width/left
    pr = width/right
    tl, tr = pl, pr
    # Here width/left and width/right are at most 1/3 for legal starts.
    # Sixty terms leave far less than double-precision rounding error.
    for n in range(1, 61):
        result -= (tr-tl)/(n*(n+2.))
        tl *= pl
        tr *= pr
    return sign*width*width*result


@njit
def generator_threshold(r, lo, hi, s, sign):
    """Integral over starts of the instantaneous unit-generator density."""
    if hi <= lo or s <= r or s >= 1.:
        return 0.
    left = 4. + sign*lo-s
    right = 4. + sign*hi-s
    return sign*(np.log1p((right-left)/left)
                 +(s-r)*(1./left-1./right))


@njit
def inverse_area(r, lo, hi, parameters, segments, count, sign):
    """Integral over the entire prefix of cumulative(phi(V))."""
    a, u, c, y = parameters
    total = max(0., a+min(c, 0.))*cumulative(r, lo, hi, u, sign)
    for i in range(count):
        left, right, slope, intercept = segments[i]
        if slope == 0.:
            total += (right-left)*cumulative(r, lo, hi, intercept, sign)
        else:
            total += (cumulative_primitive(r, lo, hi, slope*right+intercept, sign)
                      -cumulative_primitive(r, lo, hi, slope*left+intercept, sign))/slope
    return total


@njit
def reflected(r, lo, hi, parameters, segments, count, sign):
    """The second-turn capture correction, integrated over a generator."""
    a, u, c, y = parameters
    result = 4.*cumulative(r, lo, hi, 1., sign)
    for i in range(count):
        left, right, slope, intercept = segments[i]
        left = max(left, r)
        right = min(right, 1.)
        if right <= left:
            continue
        b, d = 1.+slope, intercept-8.
        result += ((b*right+d)*cumulative(r, lo, hi, right, sign)
                   -(b*left+d)*cumulative(r, lo, hi, left, sign)
                   -b*(cumulative_primitive(r, lo, hi, right, sign)
                       -cumulative_primitive(r, lo, hi, left, sign)))
    return result


@njit
def local_positive_part(r, lo, hi, segments, count):
    """Integral over a positive prefix start band of (phi(z)-r)_+."""
    total = 0.
    for i in range(count):
        left, right, slope, intercept = segments[i]
        left, right = max(left, lo), min(right, hi)
        if right <= left:
            continue
        if slope == 0.:
            total += (right-left)*max(0., intercept-r)
        else:
            left = max(left, (r-intercept)/slope)
            if right > left:
                total += (intercept-r)*(right-left)+slope*(right*right-left*left)/2.
    return total


@njit
def component(r, lo, hi, parameters, segments, count, sign):
    """Four times the payoff change for one unit-C generator."""
    if hi <= lo:
        return 0.
    a, u, c, y = parameters
    if sign > 0:
        cutoff = max(0., -c)
        result = max(0., u-r)*max(0., min(hi, a)-max(lo, cutoff))
        result -= 4.*cumulative(r, lo, min(hi, min(a, cutoff)), 1., sign)
        alpha_lo = max(lo, a)
        result -= cumulative_primitive(r, alpha_lo, hi, 1., sign)
        result -= inverse_area(r, alpha_lo, hi, parameters, segments, count, sign)
        result += reflected(r, lo, hi, parameters, segments, count, sign)
    else:
        result = local_positive_part(r, lo, min(hi, c), segments, count)
        result -= 4.*cumulative(r, max(lo, c), hi, 1., sign)
        result += reflected(r, lo, min(hi, a), parameters, segments, count, sign)
    return result


@njit
def m3_early_features(parameters, segments, count, knots, left, right, s0,
                      sign=1):
    """Flat-corridor rows before any other-sheet beta edge subtraction."""
    n = len(knots)-1
    row = np.zeros(1+4*n)
    ks = bin_at(s0, knots)
    for j in range(n):
        lo, hi = max(left, knots[j]), min(right, knots[j+1])
        if hi <= lo:
            continue
        factor = component(s0, lo, hi, parameters, segments, count, sign)/4.
        row[1+2*n+ks] += factor
        if sign > 0:
            row[1+j] -= factor
            row[1+n+j] -= factor
        else:
            row[1+2*n+j] -= factor
    for j in range(1, n):
        r = knots[j]
        if r <= s0+1e-13:
            continue
        factor = component(r, left, right, parameters, segments, count, sign)/4.
        row[1+2*n+j] += factor
        row[1+2*n+j-1] -= factor
    return row


@njit
def m3_early_mass_row(z, j, knots, left, right, s0, sign=1):
    n = len(knots)-1
    row = np.zeros(1+4*n)
    if not left <= z <= right:
        return row
    ks = bin_at(s0, knots)
    factor = (1.-s0)/(3.+sign*z)
    row[1+2*n+ks] += factor
    if sign > 0:
        row[1+j] -= factor
        row[1+n+j] -= factor
    else:
        row[1+2*n+j] -= factor
    for i in range(1, n):
        r = knots[i]
        if r > s0+1e-13:
            factor = (1.-r)/(3.+sign*z)
            row[1+2*n+i] += factor
            row[1+2*n+i-1] -= factor
    return row


@njit
def m3_early_threshold(a, s, knots, pvals, kvals, left, right, s0,
                       sign=1, below=False):
    """Start integral of m3 density; above a is alpha, below a is betaN."""
    lower, upper = left, right
    if below:
        upper = min(a, right)
    else:
        lower = max(a, left)
    if upper <= lower or s <= s0 or s >= 1.:
        return 0.
    edge = value_at(s0, knots, kvals)
    total = 0.
    for j in range(len(kvals)):
        lo, hi = max(lower, knots[j]), min(upper, knots[j+1])
        source = pvals[j] if sign > 0 else kvals[j]
        total += (edge-source)*generator_threshold(s0, lo, hi, s, sign)
    for j in range(1, len(kvals)):
        r = knots[j]
        if s0+1e-13 < r < s-1e-13:
            total += (kvals[j]-kvals[j-1])*generator_threshold(r, lower, upper, s, sign)
    return total


@njit
def m3_early_price_row(a, s, knots, left, right, s0, sign=1, below=False):
    """Linear row for the threshold function, including the start cutoff."""
    n = len(knots)-1
    row = np.zeros(1+4*n)
    lower, upper = left, right
    if below:
        upper = min(a, right)
    else:
        lower = max(a, left)
    if upper <= lower or s <= s0 or s >= 1.:
        return row
    edge = bin_at(s0, knots)
    for j in range(n):
        lo, hi = max(lower, knots[j]), min(upper, knots[j+1])
        factor = generator_threshold(s0, lo, hi, s, sign)
        row[1+2*n+edge] += factor
        if sign > 0:
            row[1+j] -= factor
            row[1+n+j] -= factor
        else:
            row[1+2*n+j] -= factor
    for j in range(1, n):
        r = knots[j]
        if s0+1e-13 < r < s-1e-13:
            factor = generator_threshold(r, lower, upper, s, sign)
            row[1+2*n+j] += factor
            row[1+2*n+j-1] -= factor
    return row


def verify_capture_features():
    from separated_oracle import baseline_prefix
    from verify_separated import actual_princess, integrate, m2, pair
    knots = np.array([0., .125, .25, .5, .75, .875, .9375, 1.])
    n = len(knots)-1
    left, right, s0 = .0625, .5, .75
    f = np.array([0., .03, .05, .07, .1, .2, .4])
    g = np.full(n, .06)
    k = np.array([.02, .03, .05, .08, .12, .25, .55])
    variables = np.r_[.5, f, g, k, np.zeros(n)]
    cases = [(.07, .4, .8, .9), (.2, .6, .96, .98), (.6, .92, .7, .94),
             (.92, .96, -.3, .7), (.92, .97, -.7, -.5), (.97, .985, -.8, -.8)]
    errors = []

    def m3(start, s):
        return np.array([[0., start], [(s-start)/2., (s+start)/2.],
                         [(s+1.)/2., (s-1.)/2.], [2., 1.], [4., -1.], [6., -1.]])

    for sign in (1, -1):
        for case in cases:
            parameters = np.array(case)
            seg, count = baseline_prefix(parameters, knots)
            expected = m3_early_features(parameters, seg, count, knots,
                                         left, right, s0, sign) @ variables
            vals = []
            for eps in (2e-5, 1e-5):
                princess, uv = actual_princess(parameters, seg[:count], eps)
                zcuts = list(knots)+[parameters[0], -parameters[2], parameters[2]]
                scuts = list(knots)+[U for U, V in uv]+[V for U, V in uv]

                def at_z(z):
                    j = bin_at(z, knots)
                    old = pair(m2(-sign*z, 1.), princess)
                    base = f[j]+g[j] if sign > 0 else k[j]
                    edge = value_at(s0, knots, k)-base

                    def generator(r):
                        return integrate(lambda s: (4.+sign*z-r)/(4.+sign*z-s)**2
                                         *(pair(m3(sign*z, s), princess)-old),
                                         r, 1., scuts, order=12)

                    total = edge*generator(s0)
                    for h in range(1, n):
                        r = knots[h]
                        if r > s0+1e-13:
                            total += (k[h]-k[h-1])*generator(r)
                    return total

                vals.append(integrate(at_z, left, right, zcuts, order=12))
            error = abs(2*vals[1]-vals[0]-expected)
            errors.append(error)
            assert error < 3e-9, (sign, case, expected, vals, error)
            print('M3_EARLY_CAPTURE', sign, case, 'error', error)
    print('PASS: 12 independent signed M3 feature limits; maximum error', max(errors))


if __name__ == '__main__':
    verify_capture_features()
