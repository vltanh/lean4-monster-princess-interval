"""Independent frozen-feature checks of localized negative-prefix optimization."""
import json
from pathlib import Path

import numpy as np

from localized_inward_prefix import negative_cases
from localized_inward_oracle import frozen_features
from m3_attached_oracle import attached_prefix


def main():
    data = json.loads(Path(__file__).with_name('negative_prefix_discovery.json').read_text())
    knots = np.asarray(data['knots'])
    profile = np.asarray(data['affine_profile'])
    old = np.r_[data['endpoint_mass'], *(data['densities'][x] for x in ('f', 'g', 'k', 'ell'))]
    left, right, s0 = data['left'], data['right'], data['turn']
    rng = np.random.default_rng(517993)
    comparisons = 0
    maximum_beat = 0.
    for i in range(48):
        a = rng.uniform(.875, .999) if i % 2 else rng.uniform(.001, .875)
        u = rng.uniform(a, 1.)
        c = rng.uniform(-a, .99); y = rng.uniform(max(c, 0.), .999)
        eta = (0.003, .03, .3)[i % 3]
        parameters = np.array([a, u, c, y])
        variables = np.r_[old, eta]
        positive, npiece = attached_prefix(parameters, knots, old, left, right, s0)
        first, nf, second, ns = negative_cases(parameters, knots, old, eta)
        possible = []
        if nf >= 0:
            possible.append(first[:nf])
        if ns >= 0:
            possible.append(second[:ns])
        def value(negative):
            full = np.vstack((negative, positive[:npiece]))
            return frozen_features(parameters, full, len(full), knots,
                                    profile, left, right, s0)@variables
        best = max(value(negative) for negative in possible)
        for trial in range(80):
            n = 1+trial % 6
            cuts = np.r_[-a, np.sort(rng.uniform(-a, min(c, 0.), n-1)), min(c, 0.)]
            levels = np.sort(rng.uniform(a, u, n))
            candidate = np.c_[cuts[:-1], cuts[1:], np.zeros(n), levels]
            actual = value(candidate)
            maximum_beat = max(maximum_beat, actual-best)
            assert actual <= best+5e-12, (parameters, eta, best, actual, possible, candidate)
            comparisons += 1
    print('PASS:', comparisons, 'complete-feature comparisons against independent nonzero-localized prefix routes')
    print('Largest sampled improvement over the analytic prefix optimum:', maximum_beat)
    print('Scope: linear prefix-functional check; density feasibility is a separate law constraint')


if __name__ == '__main__':
    main()
