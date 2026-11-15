"""Whole-law features for arbitrary positive-prefix equality contours.

The original canonical early-M2 shortcut uses phi(z)=u whenever phi(z)
exceeds its early turn floor on the start band. A noncanonical equality
contour need not obey that shortcut. This module adds the exact missing
local term; the underlying first-capture law itself does not change.
"""
import numpy as np
from numba import njit

from m3_attached_oracle import (attached_features, full_m3_beta_row,
                                GAUSS_NODES, GAUSS_WEIGHTS)
from m3_early_oracle import local_positive_part
from separated_oracle import bin_at


@njit
def general_face_features(parameters, segments, count, knots, profile,
                           left, right, s0):
    row = attached_features(parameters, segments, count, knots, profile, left, right, s0)
    a, u, c, y = parameters
    n = len(knots)-1
    ks = bin_at(s0, knots)
    for j in range(n):
        lo, hi = max(left, knots[j]), min(right, c, knots[j+1])
        if hi <= lo:
            continue
        change = (local_positive_part(s0, lo, hi, segments, count)
                  -(hi-lo)*max(0., u-s0))/4.
        row[1+2*n+ks] += change
        row[1+2*n+j] -= change
    for j in range(1, n):
        r = knots[j]
        if r <= s0+1e-13:
            continue
        hi = min(right, c)
        change = (local_positive_part(r, left, hi, segments, count)
                  -max(0., hi-left)*max(0., u-r))/4.
        row[1+2*n+j] += change
        row[1+2*n+j-1] -= change
    # The subtracted full-M3 beta source is a varying start coefficient.
    for i in range(count):
        sl, sr, slope, intercept = segments[i]
        for j in range(n):
            lo, hi = max(sl, left, knots[j]), min(sr, right, c, knots[j+1])
            if hi <= lo:
                continue
            cuts = np.array([lo, hi, lo])
            nc = 2
            if slope > 0.:
                crossing = (s0-intercept)/slope
                if lo < crossing < hi:
                    cuts[2] = crossing
                    nc = 3
            cuts = np.sort(cuts[:nc])
            for zlo, zhi in zip(cuts[:-1], cuts[1:]):
                middle, half = (zlo+zhi)/2., (zhi-zlo)/2.
                for g in range(len(GAUSS_NODES)):
                    z = middle+half*GAUSS_NODES[g]
                    difference = max(0., slope*z+intercept-s0)-max(0., u-s0)
                    row -= (half*GAUSS_WEIGHTS[g]*difference/4.)*full_m3_beta_row(z, knots)
    return row


def verify():
    import json
    from pathlib import Path
    from verify_separated import actual_princess
    from verify_m3_attached import full_direct
    data = json.loads(Path(__file__).with_name('m3_attached_settled.json').read_text())
    knots = np.asarray(data['knots'])
    weights = np.r_[data['endpoint_mass'], *(data['densities'][name] for name in ('f', 'g', 'k', 'ell'))]
    profile = np.asarray(data['affine_profile'])
    left, right, s0 = data['left'], data['right'], data['turn']
    cases = [(np.array([.95, .95, .4, .8]), np.array([[0., .4, .1, .95]])),
             (np.array([.05, .2, .2, .8]), np.array([[0., .2, .5, .2]]))]
    for parameters, segments in cases:
        expected = general_face_features(parameters, segments, len(segments), knots,
                                           profile, left, right, s0)@weights
        values = []
        for epsilon in (2e-5, 1e-5):
            princess, uv = actual_princess(parameters, segments, epsilon)
            values.append(direct_density_capture(princess, uv, weights, knots, profile, left, right, s0))
        error = abs(2*values[1]-values[0]-expected)
        assert error < 3e-7, (parameters, expected, values, error)
        print('GENERAL_PREFIX_CAPTURE', parameters.tolist(), 'error', error)
    parameters, segments = cases[0]
    constant = np.array([[0., .4, 0., .95]])
    change = general_face_features(parameters, segments, 1, knots, profile, left, right, s0)-general_face_features(
        parameters, constant, 1, knots, profile, left, right, s0)
    assert np.max(abs(change)) < 2e-14
    print('UNIVERSAL_CORRIDOR_FEATURE_CHANGE', np.max(abs(change)))


def direct_density_capture(princess, uv, weights, knots, profile, left, right, s0):
    """Independent actual-density integration with curve/turn intersections split."""
    from verify_separated import integrate, m1, m2, pair
    from verify_m3_attached import m3
    from m3_attached_oracle import M3_LEFT, M3_RIGHT, M3_TURN, positive_late_profile
    from m3_early_oracle import m3_early_mass_row
    from positive_sheet_oracle import positive_line_residual
    from separated_oracle import residual_row_affine, value_at
    n = len(knots)-1
    f, g, k, ell = (weights[1+i*n:1+(i+1)*n] for i in range(4))
    plus = positive_late_profile(knots)
    zcuts = list(knots)+[princess[0, 1]]
    scuts = list(knots)+[2-z for z in knots]
    for U, V in uv:
        zcuts.extend((U, V, -V, 2-U)); scuts.extend((U, V))
    for (U0, V0), (U1, V1) in zip(uv[:-1], uv[1:]):
        if U1 > U0:
            for U in scuts.copy():
                if U0 < U < U1:
                    V = V0+(V1-V0)*(U-U0)/(U1-U0)
                    zcuts.extend((V, -V))

    def phi(v):
        for (U0, V0), (U1, V1) in zip(uv[:-1], uv[1:]):
            if V0 <= v <= V1 and V1 > V0:
                return U0+(U1-U0)*(v-V0)/(V1-V0)
        return uv[0][0] if v < uv[0][1] else v+2

    def at_z(z):
        j = bin_at(z, knots)
        cuts = scuts+[phi(z), phi(-z)]
        oldp, oldn = pair(m2(-z, 1.), princess), pair(m2(z, 1.), princess)
        h0 = residual_row_affine(z, j, knots, profile, left, right, s0, True)@weights
        price = full_m3_beta_row(z, knots)@weights
        if left < z < right:
            h0 += price*(1-s0)/(s0+6-z)
        h0 -= m3_early_mass_row(z, j, knots, M3_LEFT, M3_RIGHT, M3_TURN, -1)@weights
        g0 = positive_line_residual(z, j, knots, plus)@weights
        g0 -= m3_early_mass_row(z, j, knots, M3_LEFT, M3_RIGHT, M3_TURN, 1)@weights
        value = f[j]*pair(m1(z), princess)+ell[j]*pair(m1(-z), princess)+g0*oldp+h0*oldn
        if left < z < right:
            edge = value_at(s0, knots, k)-k[j]-price
            value += edge/(s0+6-z)*integrate(lambda s: pair(m2(z, s), princess), s0, 1., cuts)
            for h in range(1, n):
                r = knots[h]
                if r > s0+1e-13:
                    value += (k[h]-k[h-1])/(r+6-z)*integrate(lambda s: pair(m2(z, s), princess), r, 1., cuts)
        for sign in (1, -1):
            if M3_LEFT < z < M3_RIGHT:
                source = f[j]+g[j] if sign > 0 else k[j]
                edge = value_at(M3_TURN, knots, k)-source
                def generator(r):
                    return integrate(lambda s: (4+sign*z-r)/(4+sign*z-s)**2
                                     *pair(m3(sign*z, s), princess), r, 1., cuts)
                value += edge*generator(M3_TURN)
                for h in range(1, n):
                    r = knots[h]
                    if r > M3_TURN+1e-13:
                        value += (k[h]-k[h-1])*generator(r)
        v = profile[j, 0]+profile[j, 1]*z
        if v > 1.:
            value += (value_at(2-v, knots, f)-ell[j])/(v+6-z)*integrate(
                lambda s: pair(m2(z, s), princess), 1., v, cuts)
            for h in range(1, n):
                r = 2-knots[h]
                if 1. < r < v:
                    value += (f[h]-f[h-1])/(r+6-z)*integrate(lambda s: pair(m2(z, s), princess), 1., r, cuts)
        v = plus[j]
        if v > 1.:
            value += (value_at(2-v, knots, f)-f[j])/(v+6+z)*integrate(
                lambda s: pair(m2(-z, s), princess), 1., v, cuts)
            for h in range(1, n):
                r = 2-knots[h]
                if 1. < r < v:
                    value += (f[h]-f[h-1])/(r+6+z)*integrate(lambda s: pair(m2(-z, s), princess), 1., r, cuts)
        return value

    return weights[0]*pair(m1(-1.), princess)+integrate(at_z, 0., 1., zcuts, order=12)


if __name__ == '__main__':
    verify()
