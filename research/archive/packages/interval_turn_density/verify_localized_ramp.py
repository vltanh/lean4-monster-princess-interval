#!/usr/bin/env python3
"""Independent reconstruction of every old-law component induced by a ramp."""
import json
from pathlib import Path

import numpy as np
from numpy.polynomial.legendre import leggauss
from scipy.integrate import quad

from negative_prefix_oracle import general_features
from localized_ramp_basis import (D, general_ramp_feature, early_mass,
    negative_early_price, m3_price, KM)


def step_score(r, parameters, packed, knots, profile, left, right, s0):
    augmented = np.array(sorted(set(knots.tolist()+[r])))
    n = len(augmented)-1
    variables = np.zeros(1+4*n)
    mapped = np.zeros((n, 2))
    for j in range(n):
        middle = (augmented[j]+augmented[j+1])/2.
        old = min(len(knots)-2, max(0, int(np.searchsorted(knots, middle)-1)))
        mapped[j] = profile[old]
        if augmented[j] >= r-1e-13:
            variables[1+2*n+j] = variables[1+3*n+j] = 1.
    return float(general_features(parameters, packed, len(packed), augmented,
        mapped, left, right, s0, True)@variables)


def reference(parameters, packed, knots, profile, left, right, s0):
    a, u, c, y = parameters
    cuts = [D, 1., a, u, c, y, -c, -y, s0, *knots]
    for lo, hi, slope, intercept in packed:
        cuts.extend((lo, hi, -lo, -hi, slope*lo+intercept, slope*hi+intercept))
        # A generator crosses a local start-band boundary when r=phi(V).
        # These events need not be endpoints of the supplied affine piece.
        for V in np.r_[knots, -knots, a, -a, c, y]:
            if lo < V < hi:
                cuts.append(slope*V+intercept)
    cuts = sorted(set(x for x in cuts if D <= x <= 1.))
    nodes, weights = leggauss(16)
    total = 0.
    for lo, hi in zip(cuts[:-1], cuts[1:]):
        middle, half = (lo+hi)/2., (hi-lo)/2.
        for node, weight in zip(nodes, weights):
            total += half*weight*step_score(middle+half*node, parameters,
                packed, knots, profile, left, right, s0)
    return total


def main():
    data = json.loads(Path(__file__).with_name('negative_prefix_discovery.json').read_text())
    knots, profile = np.asarray(data['knots']), np.asarray(data['affine_profile'])
    left, right, s0 = data['left'], data['right'], data['turn']
    cases = [
        (np.array([.2, .5, .9, .95]), np.array([[-.2, 0., 0., .3], [0., .9, .1, .9]])),
        (np.array([.99, .9995, -.9, .625]), np.array([[-.99, -.95, 0., .994], [-.95, -.9, 0., .999]])),
        (np.array([.95, .99, .4, .8]), np.array([[-.95, -.4, 0., .96], [-.4, 0., 0., .98], [0., .4, 0., .99]])),
        (np.array([.999, 1., -.995, -.99]), np.array([[-.999, -.995, 0., .9999]])),
        (np.array([.05, .96, .8, .9]), np.array([[-.05, 0., 0., .2], [0., .8, .04, .96]])),
    ]
    errors = []
    for parameters, packed in cases:
        expected = reference(parameters, packed, knots, profile, left, right, s0)
        actual = general_ramp_feature(parameters, packed, len(packed), left, right, s0)
        error = abs(expected-actual); errors.append(error)
        assert error < 2e-11, (parameters, expected, actual, error)
        print('RAMP_COLUMN', parameters.tolist(), 'actual', actual, 'reference', expected,
              'error', error, flush=True)
    kernel_errors = []
    for z in (.125, .3, .5):
        h = lambda s: (s0-D)/(s0+6.-z)+np.log((s+6.-z)/(s0+6.-z))
        expected = quad(h, s0, 1., epsabs=1e-14)[0]
        kernel_errors.append(abs(early_mass(z, s0)-expected))
    for a in (.2, .4, .8):
        for U in (.9, .95, .98, 1.):
            expected = 0.
            if U > s0:
                expected = quad(lambda z: (s0-D)/(s0+6.-z)
                    +np.log((U+6.-z)/(s0+6.-z)), left, min(a, right), epsabs=1e-14)[0]
            kernel_errors.append(abs(negative_early_price(a,U,left,right,s0)-expected))
    for a in (0., .07, .2):
        for U in (.9, .97, 1.):
            for sign in (-1, 1):
                lo, hi = (0., min(a, .125)) if sign < 0 else (min(max(a, 0.), .125), .125)
                expected = quad(lambda z: (U-D)/(4.+sign*z-U)
                    +(U-D)**2/(2.*(4.+sign*z-U)**2), lo, hi, epsabs=1e-14)[0]
                kernel_errors.append(abs(m3_price(a,U,sign,sign<0)-expected))
    assert max(kernel_errors) < 2e-12, max(kernel_errors)
    assert abs(KM[0]-(1.-D)**2/2.) < 1e-16
    print('RAMP_KERNELS', len(kernel_errors), 'max error', max(kernel_errors))
    print('PASS: 5 full induced-column reconstructions, 33 independent kernel checks; max column error', max(errors))


if __name__ == '__main__':
    main()
