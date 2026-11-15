#!/usr/bin/env python3
"""Remove p-monotonicity using the verified ordered-block prefix response."""
import json
from pathlib import Path
import sys

import numpy as np

import discover_m3_attached as attached
import discover_separated as discovery
from negative_prefix_oracle import general_features, optimal_features, freeze_response


LABELS = []


def constraints(*args, **kwargs):
    rows, equalities = attached.constraints(*args, **kwargs)
    keep = [i for i, label in enumerate(attached.CONSTRAINT_LABELS)
            if not label.startswith('p=f+g nondecreasing')]
    LABELS[:] = [attached.CONSTRAINT_LABELS[i] for i in keep]
    return rows[keep], equalities


discovery.constraints = constraints
discovery.features_affine = general_features
discovery.optimal_features_affine = optimal_features
discovery.freeze_response_affine = freeze_response


def main():
    defaults = {'--slope': '0.015625', '--left': '.125', '--right': '.5',
                '--turn': '.9375', '--late-left': '.625', '--late-right': '.875',
                '--output': 'negative_prefix_discovery.json'}
    for flag, value in defaults.items():
        if flag not in sys.argv:
            sys.argv.extend([flag, value])
    if '--edge-trace' not in sys.argv:
        sys.argv.append('--edge-trace')
    discovery.main()
    path = Path(__file__).with_name(sys.argv[sys.argv.index('--output')+1])
    if not path.exists():
        return
    data = json.loads(path.read_text())
    knots = np.asarray(data['knots'])
    variables = np.r_[data['endpoint_mass'], *(data['densities'][x] for x in ('f', 'g', 'k', 'ell'))]
    rows, equalities = constraints(knots, np.asarray(data['profile']), data['left'], data['right'],
        data['turn'], None, np.asarray(data['affine_profile']), data['negative_start_bound'], True)
    data['scope'] = ('Normalized floating M3 density law with arbitrary nonnegative p=f+g. '
        'Its negative-prefix response is optimized by ordered blocks; all other structural '
        'conditions remain. Scalar separation is numerical. Not an exact game bound or matching saddle.')
    data['negative_prefix'] = 'Two exact PAVA cases; saved prefix rows include negative V blocks.'
    data['structural_constraints'] = [dict(label=label, slack=float(-row@variables), multiplier=float(dual))
        for label, row, dual in zip(LABELS, rows, data['structural_duals'])]
    data['structural_equalities'] = [dict(label=label, residual=float(row@variables), multiplier=float(dual))
        for label, row, dual in zip(attached.EQUALITY_LABELS[1:], equalities[1:], data['structural_equality_duals'])]
    data['normalization'] = float(equalities[0]@variables)
    data['minimum_structural_slack'] = float(np.min(-rows@variables))
    path.write_text(json.dumps(data, indent=2))
    print('NORMALIZATION', data['normalization'], 'MIN_SLACK', data['minimum_structural_slack'], flush=True)
    print('LABELLED_STRUCTURAL_DUALS', [(row['label'], row['multiplier'])
        for row in data['structural_constraints'] if abs(row['multiplier']) > 1e-9], flush=True)


if __name__ == '__main__':
    main()
