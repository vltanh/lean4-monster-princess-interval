#!/usr/bin/env python3
"""Independent continuous mass and join audit for the attached tail law.

The reference integrates the generating density against the exact path-mass
kernel, rather than using the feature module's moment series.  It audits all
sheet masses that enter the physical nonnegativity rows, the two singular
joins, the complete normalization, and a feasible normalized attachment.
"""
import json
import math
from pathlib import Path

import numpy as np
from scipy.integrate import quad
from scipy.optimize import linprog

from endpoint_tail import modulation
from singular_tail_basis import (F_DELTA, K_DELTA, FM, KM, density,
                                 early_mass, late_mass)
from singular_tail_law import TailLaw


def mass_integral(power, scale, cutoff, kernel):
    rate = 1.-power
    x = math.log(16./cutoff)
    return scale*cutoff**rate*quad(lambda t: math.exp(-rate*t)
        *float(modulation(x+t))*kernel(cutoff*math.exp(-t)), 0., np.inf,
        epsabs=2e-13, epsrel=2e-13)[0]


def projected_seed(law, data, amplitude=.06):
    original = np.r_[data['endpoint_mass'],
        *(data['densities'][name] for name in ('f', 'g', 'k', 'ell')), amplitude]
    n = law.size
    matrix = np.vstack((np.c_[law.inequalities, np.zeros((len(law.inequalities), n))],
                        np.c_[np.eye(n), -np.eye(n)], np.c_[-np.eye(n), -np.eye(n)]))
    rhs = np.r_[np.zeros(len(law.inequalities)), original, -original]
    equality = np.c_[law.equalities, np.zeros((len(law.equalities), n))]
    erhs = np.zeros(len(equality)); erhs[0] = 1.
    bounds = list(law.bounds); bounds[-1] = (amplitude, amplitude)
    result = linprog(np.r_[np.zeros(n), np.ones(n)], A_ub=matrix, b_ub=rhs,
        A_eq=equality, b_eq=erhs, bounds=bounds+[(0., None)]*n, method='highs')
    assert result.success, result.message
    return result.x[:n]


def main():
    errors = []
    f_mass = mass_integral(2/3, 1., F_DELTA, lambda e: 1.)
    k_mass = mass_integral(1/6, .5, K_DELTA, lambda e: 1.)
    errors.extend((abs(f_mass-FM[0]), abs(k_mass-KM[0])))
    for z in (.0, .0625, .125, .25, .5, .625, .75, .875):
        for sign in (-1, 1):
            d = 7.+sign*z
            expected = mass_integral(2/3, 1., F_DELTA,
                                     lambda e: d/(d+e)**2)
            errors.append(abs(late_mass(z, sign)-expected))
        d = 7.-z
        expected = mass_integral(1/6, .5, K_DELTA,
                                 lambda e: d/(d-e)**2)
        errors.append(abs(early_mass(z)-expected))
        for sign in (-1, 1):
            expected = mass_integral(1/6, .5, K_DELTA,
                                     lambda e: 1./(3.+sign*z))
            errors.append(abs(KM[0]/(3.+sign*z)-expected))
    assert max(errors) < 5e-11, max(errors)

    data = json.loads(Path(__file__).with_name('negative_prefix_discovery.json').read_text())
    law = TailLaw(data['knots'], data['affine_profile'], data['left'], data['right'],
                  data['turn'], data['negative_start_bound'])
    seed = projected_seed(law, data)
    step, amplitude = law.expand(seed)
    augmented_widths = np.diff(law.aug_knots)
    n = law.aug_n
    direct_mass = step[0]+sum(float(step[1+j*n:1+(j+1)*n]@augmented_widths)
                               for j in (0, 1, 2))+amplitude*(f_mass+k_mass)
    assert abs(direct_mass-1.) < 5e-12
    assert max(abs(law.equalities[1:]@seed)) < 1e-12
    assert np.min(-law.inequalities@seed) > -2e-10
    f_join = amplitude*density(1.-F_DELTA, 2/3, 1.)
    k_join = amplitude*density(1.-K_DELTA, 1/6, .5)
    assert f_join >= seed[law.n-1]-1e-10
    assert k_join >= seed[3*law.n]-1e-10
    assert not any(label.startswith('p=f+g nondecreasing') for label in law.labels)
    print('TAIL_MASS_CHECKS', len(errors), 'max absolute error', max(errors))
    print('ADMISSIBLE_ATTACHMENT', law.summary(seed))
    print('LINEAR_ROWS', len(law.inequalities), 'equalities', len(law.equalities),
          'old density bins', law.n, 'integration intervals', law.aug_n)
    print('PASS: complete sheet-mass kernels, joins, normalized feasible attachment')


if __name__ == '__main__':
    main()
