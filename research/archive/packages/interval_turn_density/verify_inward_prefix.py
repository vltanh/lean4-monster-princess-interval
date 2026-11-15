"""Independent whole-feature checks of initial-inward negative-prefix optimization."""
from pathlib import Path

import numpy as np
from inward_attached_oracle import frozen_features as whole_features


def verify_negative_optimization():
    """Compare the optimizer with independently evaluated complete-law routes."""
    import json
    from m3_attached_oracle import attached_prefix
    from uniform_inward_prefix import negative_blocks
    data = json.loads(Path(__file__).with_name('negative_prefix_discovery.json').read_text())
    knots = np.asarray(data['knots'])
    profile = np.asarray(data['affine_profile'])
    old = np.r_[data['endpoint_mass'], *(data['densities'][x] for x in ('f', 'g', 'k', 'ell'))]
    left, right, s0 = data['left'], data['right'], data['turn']
    rng = np.random.default_rng(517389)
    count = 0
    maximum_beat = 0.
    for _ in range(32):
        a = rng.uniform(.01, .999); u = rng.uniform(a, 1.)
        c = rng.uniform(-a, .99); y = rng.uniform(max(c, 0.), .999)
        parameters = np.array([a, u, c, y])
        h = np.sort(rng.uniform(0., .08, len(knots)-1))
        variables = np.r_[old, h]
        positive, npiece = attached_prefix(parameters, knots, old, left, right, s0)
        chosen, nc = negative_blocks(parameters, knots, old, h)
        full = np.vstack((chosen[:nc], positive[:npiece]))
        best = whole_features(parameters, full, len(full), knots, profile, left, right, s0)@variables
        for trial in range(80):
            n = 1+trial % 6
            cuts = np.r_[-a, np.sort(rng.uniform(-a, min(c, 0.), n-1)), min(c, 0.)]
            levels = np.sort(rng.uniform(a, u, n))
            candidate = np.c_[cuts[:-1], cuts[1:], np.zeros(n), levels]
            full = np.vstack((candidate, positive[:npiece]))
            actual = whole_features(parameters, full, len(full), knots, profile, left, right, s0)@variables
            maximum_beat = max(maximum_beat, actual-best)
            assert actual <= best+5e-12, (parameters, chosen[:nc], candidate, best, actual)
            count += 1
    print('PASS:', count, 'whole-law comparisons against independent nonzero-inward prefix routes')
    print('Largest sampled improvement over complete arrangement optimum:', maximum_beat)
    print('Scope: implementation check of the analytic prefix theorem, not a game optimum')


if __name__ == '__main__':
    verify_negative_optimization()
