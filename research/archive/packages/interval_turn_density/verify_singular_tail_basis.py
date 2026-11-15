#!/usr/bin/env python3
"""Independent Stieltjes reconstruction of the continuous tail feature.

The reference integrates the previously capture-checked step generators.
Its quadrature nodes are not density variables and are never optimized.
"""
import json
import math
from pathlib import Path

import numpy as np
from numpy.polynomial.legendre import leggauss

from endpoint_tail import modulation
from m3_face_features import general_face_features
from separated_oracle import baseline_prefix
from singular_tail_basis import (F_DELTA, K_DELTA, moment, tail_feature,
                                  line_f, line_negative_m1, late_f_column,
                                  early_negative_k, m3_both_k)


def step_feature(kind, r, parameters, segments, knots, profile, left, right, s0):
    augmented = np.array(sorted(set(knots.tolist()+[r])))
    n = len(augmented)-1
    v = np.zeros(1+4*n)
    q = np.ones((n, 2)); q[:, 1] = 0.
    for j in range(n):
        mid = (augmented[j]+augmented[j+1])/2
        old = min(len(knots)-2, max(0, np.searchsorted(knots, mid, side='right')-1))
        q[j] = profile[old]
        if augmented[j] >= r-1e-14:
            if kind == 'f':
                v[1+j] = 1.
            else:
                v[1+2*n+j] = v[1+3*n+j] = 1.
    return float(general_face_features(parameters, segments, len(segments), augmented, q,
                                       left, right, s0)@v)


def reconstructed(kind, parameters, segments, knots, profile, left, right, s0):
    power, scale, cutoff = (2/3, 1., F_DELTA) if kind == 'f' else (1/6, .5, K_DELTA)
    rate = 1-power
    def response(eps):
        return step_feature(kind, 1-eps, parameters, segments, knots, profile, left, right, s0)
    a, u, c, y = parameters
    cuts = [1-a, 1-u, 1+c, 1+y, 1-c, 1-y]
    for lo, hi, slope, intercept in segments:
        cuts.extend((1-lo, 1-hi, 1+lo, 1+hi,
                     1-slope*lo-intercept, 1-slope*hi-intercept))
    positive = [x for x in cuts if x > 1e-10]
    small = min(1e-7, cutoff/100, min(positive)/16 if positive else cutoff/100)
    # The tail response is differentiable in its small support width once
    # all finite characteristic breakpoints are outside this interval.
    limit = 2*response(small/2)/(small/2)-response(small)/small
    h = lambda e: scale*e**(-power)*float(modulation(math.log(16/e)))
    result = h(cutoff)*response(cutoff)
    result += limit*(moment(small, power, 0, scale)-small*h(small))
    grid = sorted(set([small, cutoff]+[x for x in cuts if small < x < cutoff]))
    refined = [grid[0]]
    for lo, hi in zip(grid[:-1], grid[1:]):
        pieces = max(1, math.ceil(math.log(hi/lo)/math.log(4)))
        refined.extend(np.geomspace(lo, hi, pieces+1)[1:].tolist())
    nodes, weights = leggauss(20)
    for lo, hi in zip(refined[:-1], refined[1:]):
        yl, yh = lo**rate, hi**rate
        middle, half = (yl+yh)/2, (yh-yl)/2
        for node, weight in zip(nodes, weights):
            eps = (middle+half*node)**(1/rate)
            L = math.log(16/eps)
            derivative_factor = power*float(modulation(L))+float(modulation(L, derivative=True))
            result += scale*half*weight/rate*derivative_factor*response(eps)/eps
    return result


def main():
    data = json.loads(Path(__file__).with_name('m3_attached_settled.json').read_text())
    knots = np.asarray(data['knots'])
    profile = np.asarray(data['affine_profile'])
    left, right, s0 = data['left'], data['right'], data['turn']
    cases = [(np.array([.2, .5, .9, .95]), None),
             (np.array([.995, .9998, -.6, .4]), None),
             (np.array([.999, .99999, -.99, -.98]), None),
             (np.array([.95, .95, .4, .8]), np.array([[0., .4, .1, .95]]))]
    errors = []
    for parameters, custom in cases:
        if custom is None:
            seg, count = baseline_prefix(parameters, knots)
            seg = seg[:count]
        else:
            seg = custom
        f_reference = reconstructed('f', parameters, seg, knots, profile, left, right, s0)
        k_reference = reconstructed('k', parameters, seg, knots, profile, left, right, s0)
        f_actual = (line_f(parameters)+late_f_column(parameters, knots, profile))/4
        k_actual = (line_negative_m1(parameters, seg, len(seg))
                    +early_negative_k(parameters, seg, len(seg), left, right)
                    +m3_both_k(parameters, seg, len(seg)))/4
        error = max(abs(f_reference-f_actual), abs(k_reference-k_actual))
        errors.append(error)
        print('TAIL_FEATURE', parameters.tolist(), 'f', f_actual, f_reference,
              'k', k_actual, k_reference, 'error', error, flush=True)
        assert error < 3e-8
        assert abs(tail_feature(parameters, seg, len(seg), knots, profile, left, right)
                   -f_actual-k_actual) < 1e-12
    print('PASS: 8 independent f/k Stieltjes feature reconstructions; max error', max(errors))


if __name__ == '__main__':
    main()
