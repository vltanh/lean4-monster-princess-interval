#!/usr/bin/env python3
"""Independent whole-law capture and prefix checks for the M3 attachment."""
import json
import sys
from pathlib import Path

import numpy as np

from m3_attached_oracle import (attached_features, attached_prefix,
    full_m3_beta_row, positive_late_profile, M3_LEFT, M3_RIGHT, M3_TURN)
from separated_oracle import bin_at, value_at
from verify_separated import actual_princess, direct_expectation, integrate, m2, pair


def m3(start, s):
    return np.array([[0., start], [(s-start)/2., (s+start)/2.],
                     [(s+1.)/2., (s-1.)/2.], [2., 1.], [4., -1.], [6., -1.]])


def full_direct(princess, uv, weights, knots, negative_profile, left, right, s0):
    n = len(knots)-1
    f, g, k = weights[1:1+n], weights[1+n:1+2*n], weights[1+2*n:1+3*n]
    positive_profile = positive_late_profile(knots)
    total = direct_expectation(princess, uv, weights, knots, np.ones(n), left, right, s0,
                                affine_profile=negative_profile, edge_trace=True)
    zcuts = list(knots)+[princess[0, 1]]
    for U, V in uv:
        zcuts.extend((U, V, -V, 2-U))
    scuts = list(knots)+[2-x for x in knots]+[U for U, V in uv]+[V for U, V in uv]
    for j in range(n):
        v = positive_profile[j]
        if v <= 1.:
            continue

        def plus_late(z):
            old = pair(m2(-z, 1.), princess)
            edge = (value_at(2-v, knots, f)-f[j])/(v+6+z)
            value = edge*integrate(lambda s: pair(m2(-z, s), princess)-old, 1., v, scuts)
            for h in range(1, n):
                r = 2-knots[h]
                if 1. < r < v:
                    value += (f[h]-f[h-1])/(r+6+z)*integrate(
                        lambda s: pair(m2(-z, s), princess)-old, 1., r, scuts)
            return value

        total += integrate(plus_late, knots[j], knots[j+1], zcuts)
    for sign in (1, -1):

        def new_m3(z):
            j = bin_at(z, knots)
            old = pair(m2(-sign*z, 1.), princess)
            base = f[j]+g[j] if sign > 0 else k[j]
            edge = value_at(M3_TURN, knots, k)-base

            def generator(r):
                return integrate(lambda s: (4+sign*z-r)/(4+sign*z-s)**2
                                 *(pair(m3(sign*z, s), princess)-old), r, 1., scuts)

            value = edge*generator(M3_TURN)
            for h in range(1, n):
                r = knots[h]
                if r > M3_TURN+1e-13:
                    value += (k[h]-k[h-1])*generator(r)
            return value

        total += integrate(new_m3, M3_LEFT, M3_RIGHT, zcuts)

    def cross_edge(z):
        price = full_m3_beta_row(z, knots) @ weights
        old = pair(m2(z, 1.), princess)
        return -price/(s0+6-z)*integrate(lambda s: pair(m2(z, s), princess)-old,
                                        s0, 1., scuts)

    total += integrate(cross_edge, left, right, zcuts)
    return total


def main():
    filename = sys.argv[1] if len(sys.argv) > 1 else 'm3_attached_discovery.json'
    data = json.loads(Path(__file__).with_name(filename).read_text())
    knots = np.asarray(data['knots'])
    weights = np.r_[data['endpoint_mass'], *(data['densities'][name] for name in ('f', 'g', 'k', 'ell'))]
    profile = np.asarray(data['affine_profile'])
    left, right, s0 = data['left'], data['right'], data['turn']
    cases = [(.08, .2, .95, .97), (.48, .75, .98, .99), (.94, .97, -.6, .65)]
    errors = []
    for case in cases:
        parameters = np.asarray(case)
        segments, count = attached_prefix(parameters, knots, weights, left, right, s0)
        expected = attached_features(parameters, segments, count, knots, profile,
                                      left, right, s0) @ weights
        values = []
        for epsilon in (2e-5, 1e-5):
            princess, uv = actual_princess(parameters, segments[:count], epsilon)
            values.append(full_direct(princess, uv, weights, knots, profile, left, right, s0))
        error = abs(2*values[1]-values[0]-expected)
        assert error < 2e-7, (case, count, expected, values, error)
        errors.append(error)
        print('FULL_M3_LAW_CAPTURE', case, 'prefix_segments', count, 'error', error, flush=True)

    prefix_error = 0.
    for record in sorted(data['response_dual_support'], key=lambda x: -x['weight'])[:20]:
        parameters = np.asarray(record['parameters'])
        coarse, nc = attached_prefix(parameters, knots, weights, left, right, s0, 2e-7)
        fine, nf = attached_prefix(parameters, knots, weights, left, right, s0, 2e-9)
        difference = abs((attached_features(parameters, coarse, nc, knots, profile, left, right, s0)
                          -attached_features(parameters, fine, nf, knots, profile, left, right, s0)) @ weights)
        prefix_error = max(prefix_error, difference)
    print('PASS: 3 independent whole-law capture limits; maximum error', max(errors))
    print('PREFIX_TOLERANCE_CHECK', prefix_error)
    print('Scope: admissible normalized floating law and implementation checks; no matching lower law')


if __name__ == '__main__':
    main()
