#!/usr/bin/env python3
"""Independent step-generator reconstruction of negative-block tail features."""
import json
from pathlib import Path

import numpy as np

import verify_singular_tail_basis as reference
from negative_prefix_oracle import general_features, negative_cases
from singular_tail_negative import general_tail_feature, negative_tail_cases


def main():
    # The Stieltjes reference now uses the independently capture-checked
    # general step-law feature instead of the constant-negative shortcut.
    reference.general_face_features = general_features
    data = json.loads(Path(__file__).with_name('m3_attached_settled.json').read_text())
    knots = np.asarray(data['knots'])
    profile = np.asarray(data['affine_profile'])
    left, right, s0 = data['left'], data['right'], data['turn']
    cases = [
        (np.array([.995, .9999995, -.9, .4]),
         np.array([[-.995, -.99, 0., .997], [-.99, -.9, 0., .9999993]])),
        (np.array([.08, .9999995, .8, .9]),
         np.array([[-.08, -.04, 0., .2], [-.04, 0., 0., .9999993], [0., .8, 0., .9999995]])),
        (np.array([.2, .9999995, .8, .9]),
         np.array([[-.2, -.1, 0., .23], [-.1, 0., 0., .9999993], [0., .8, 0., .9999995]])),
    ]
    errors = []
    for parameters, packed in cases:
        expected = sum(reference.reconstructed(kind, parameters, packed, knots,
                         profile, left, right, s0) for kind in ('f', 'k'))
        actual = general_tail_feature(parameters, packed, len(packed), knots,
                                     profile, left, right)
        error = abs(actual-expected)
        assert error < 3e-8, (parameters, actual, expected, error)
        errors.append(error)
        print('NEGATIVE_BLOCK_TAIL', parameters.tolist(), 'error', error, flush=True)
    variables = np.r_[data['endpoint_mass'], *(data['densities'][x] for x in ('f', 'g', 'k', 'ell'))]
    rng = np.random.default_rng(99555)
    for _ in range(24):
        a = rng.uniform(0., 1.); u = rng.uniform(a, 1.)
        c = rng.uniform(-a, 1.); y = rng.uniform(c, 1.)
        parameters = np.array([a, u, c, y])
        old = negative_cases(parameters, knots, variables)
        new = negative_tail_cases(parameters, knots, variables, 0.)
        for offset in (0, 2):
            assert old[offset+1] == new[offset+1]
            n = old[offset+1]
            if n > 0:
                assert np.max(abs(old[offset][:n]-new[offset][:n])) < 2e-13
    print('PASS: 6 independent tail component reconstructions; maximum whole-column error', max(errors))
    print('PASS: 24 zero-tail ordered-prefix consistency checks')


if __name__ == '__main__':
    main()
