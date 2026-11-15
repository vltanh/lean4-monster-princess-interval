#!/usr/bin/env python3
"""Independent whole-score checks of the modified positive-prefix optimizer."""
import json
from pathlib import Path

import numpy as np

from inward_attached_law import InwardLaw
from inward_attached_oracle import frozen_features, freeze_response
from negative_prefix_oracle import optimal_features as old_optimal
from uniform_inward_prefix import negative_blocks


def main():
    data = json.loads(Path(__file__).with_name('negative_prefix_discovery.json').read_text())
    law = InwardLaw(data['knots'], data['affine_profile'], data['left'],
                    data['right'], data['turn'], data['negative_start_bound'])
    old = np.r_[data['endpoint_mass'],
        *(data['densities'][name] for name in ('f', 'g', 'k', 'ell'))]
    rng = np.random.default_rng(43983)
    zero_errors = []
    for _ in range(60):
        a = rng.uniform(0., 1.); u = rng.uniform(a, 1.)
        c = rng.uniform(-a, 1.); y = rng.uniform(c, 1.)
        p = np.array([a, u, c, y])
        variables = np.r_[old, np.zeros(law.n)]
        row, packed = freeze_response(p, law, variables)
        reference = old_optimal(p, law.knots, law.profile, old,
                                law.left, law.right, law.turn)
        zero_errors.append(abs(row@variables-reference@old))
    assert max(zero_errors) < 2e-10

    h = np.linspace(.004, .05, law.n)
    variables = np.r_[old, h]
    count, greatest_improvement = 0, 0.
    interpolation_error = 0.
    for _ in range(60):
        a = rng.uniform(0., 1.); u = rng.uniform(a, 1.)
        c = rng.uniform(.05, 1.); y = rng.uniform(c, 1.)
        p = np.array([a, u, c, y])
        row, packed = freeze_response(p, law, variables)
        accurate, _ = freeze_response(p, law, variables, tolerance=2e-9)
        interpolation_error = max(interpolation_error, abs((accurate-row)@variables))
        negative, nn = negative_blocks(p, law.knots, old, h)
        cuts = np.sort(np.r_[0., law.knots[(law.knots > 0.) & (law.knots < c)], c])
        for _ in range(32):
            levels = np.sort(rng.uniform(u, 1., len(cuts)-1))
            graph = np.zeros((nn+len(levels), 4))
            graph[:nn] = negative[:nn]
            for j, (lo, hi) in enumerate(zip(cuts[:-1], cuts[1:])):
                graph[nn+j] = np.array([lo, hi, 0., max(hi, levels[j])])
            candidate = frozen_features(p, graph, len(graph), law.knots,
                law.profile, law.left, law.right, law.turn)
            gain = float((candidate-row)@variables)
            greatest_improvement = max(greatest_improvement, gain)
            assert gain < 2e-9, (p.tolist(), gain, graph.tolist())
            count += 1
    assert interpolation_error < 2e-9, interpolation_error
    print('ZERO_H_WHOLE_ORACLE', len(zero_errors), 'max error', max(zero_errors))
    print('NONZERO_H_POSITIVE_COMPARISONS', count, 'greatest competing gain', greatest_improvement)
    print('PREFIX_TOLERANCE_SCORE_CHANGE', interpolation_error)
    print('PASS: whole-law feature comparison with zero and nonzero independent h')


if __name__ == '__main__':
    main()
