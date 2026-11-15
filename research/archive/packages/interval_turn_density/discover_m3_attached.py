#!/usr/bin/env python3
"""One fixed-geometry full-law M3 attachment, with all structural duals.

Uses the existing eleven density bins. This is a structural experiment,
not a certified interval, lower strategy, or solved equilibrium.
"""
import json
import sys
from pathlib import Path

import numpy as np

import discover_separated as discovery
from m3_attached_oracle import (M3_LEFT, M3_RIGHT, M3_TURN,
    attached_features, optimal_features_attached, freeze_response_attached,
    full_m3_beta_row, positive_late_profile)
from m3_early_oracle import m3_early_mass_row
from positive_sheet_oracle import positive_line_residual
from separated_oracle import bin_at, residual_row_affine


ORIGINAL_CONSTRAINTS = discovery.constraints
CONSTRAINT_LABELS = []
EQUALITY_LABELS = []


def constraints(knots, profile, left, right, s0, cap_level,
                affine_profile=None, negative_start_bound=None, edge_trace=False):
    assert edge_trace and affine_profile is not None and cap_level is None
    n = len(knots)-1
    base, equalities = ORIGINAL_CONSTRAINTS(knots, profile, left, right, s0,
        cap_level, affine_profile, negative_start_bound, edge_trace)
    labels = []
    for group in ('f', 'p=f+g', 'k'):
        labels.extend(f'{group} nondecreasing at {knots[j+1]:.12g}' for j in range(n-1))
    for j in range(n):
        labels.append(f'conservative negative-line residual bin {j}')
        vmax = affine_profile[j, 0]+affine_profile[j, 1]*knots[j+1]
        if vmax > 1.:
            labels.append(f'negative-late edge nonnegative bin {j}')
    labels.extend(f'late Gamma jump at {knots[j+1]:.12g}' for j in range(n-1))
    assert len(labels) == len(base)
    eq_labels = ['normalization']
    eq_labels.extend(f'no negative M2 starts in bin {j}'
                     for j in range(n) if knots[j] >= negative_start_bound-1e-12)
    assert len(eq_labels) == len(equalities)
    rows = list(base)
    plus_profile = positive_late_profile(knots)
    for j in range(n):
        lo, hi = knots[j], knots[j+1]
        if lo < M3_RIGHT-1e-12 and hi > M3_LEFT+1e-12:
            z = max(lo, M3_LEFT)
            rows.append(-(positive_line_residual(z, j, knots, plus_profile)
                          -m3_early_mass_row(z, j, knots, M3_LEFT, M3_RIGHT, M3_TURN, 1)))
            labels.append(f'positive-line after M3 residual bin {j}')
            z = min(hi, M3_RIGHT)
            rows.append(-(residual_row_affine(z, j, knots, affine_profile,
                                              left, right, s0, True)
                          -m3_early_mass_row(z, j, knots, M3_LEFT, M3_RIGHT, M3_TURN, -1)))
            labels.append(f'negative-line after M3 residual bin {j}')
            edge = np.zeros(1+4*n)
            edge[1+j] = edge[1+n+j] = 1.
            edge[1+2*n+bin_at(M3_TURN, knots)] = -1.
            rows.append(edge)
            labels.append(f'positive-M3 lower edge bin {j}')
        elif plus_profile[j] > 1.:
            rows.append(-positive_line_residual(lo, j, knots, plus_profile))
            labels.append(f'positive-line after late sheet residual bin {j}')
        if lo >= left-1e-12 and hi <= right+1e-12:
            # The full M3 beta price is monotone, so the upper bin endpoint
            # is the exact worst lower-edge test for fixed k(z).
            edge = full_m3_beta_row(hi-1e-12, knots)
            edge[1+2*n+j] += 1.
            edge[1+2*n+bin_at(s0, knots)] -= 1.
            rows.append(edge)
            labels.append(f'negative-early edge after both M3 beta prices bin {j}')
    CONSTRAINT_LABELS[:] = labels
    EQUALITY_LABELS[:] = eq_labels
    return np.asarray(rows), equalities


discovery.features_affine = attached_features
discovery.optimal_features_affine = optimal_features_attached
discovery.freeze_response_affine = freeze_response_attached
discovery.constraints = constraints


def main():
    if '--slope' not in sys.argv:
        sys.argv.extend(['--slope', str(1/64)])
    if '--left' not in sys.argv:
        sys.argv.extend(['--left', '.125'])
    if '--right' not in sys.argv:
        sys.argv.extend(['--right', '.5'])
    if '--turn' not in sys.argv:
        sys.argv.extend(['--turn', '.9375'])
    if '--late-left' not in sys.argv:
        sys.argv.extend(['--late-left', '.625'])
    if '--late-right' not in sys.argv:
        sys.argv.extend(['--late-right', '.875'])
    if '--edge-trace' not in sys.argv:
        sys.argv.append('--edge-trace')
    if '--output' not in sys.argv:
        sys.argv.extend(['--output', 'm3_attached_discovery.json'])
    discovery.main()
    name = sys.argv[sys.argv.index('--output')+1]
    path = Path(__file__).with_name(name)
    if not path.exists():
        return
    data = json.loads(path.read_text())
    knots = np.asarray(data['knots'])
    weights = np.r_[data['endpoint_mass'], *(data['densities'][x] for x in ('f', 'g', 'k', 'ell'))]
    rows, equalities = constraints(knots, np.asarray(data['profile']), data['left'],
        data['right'], data['turn'], None, np.asarray(data['affine_profile']),
        data['negative_start_bound'], True)
    data['scope'] = ('A normalized floating full-law M3 attachment on the existing density bins. '
                     'The continuous response reduction has explicit common-edge and residual hypotheses; '
                     'prefix quadrature and four-scalar optimization are numerical. Not a certified game bound '
                     'or a matching lower strategy.')
    data['m3_geometry'] = dict(start_band=[M3_LEFT, M3_RIGHT], first_turn_floor=M3_TURN,
                               second_turn=1., signs=[-1, 1])
    data['positive_profile'] = positive_late_profile(knots).tolist()
    data['structural_constraints'] = [dict(label=label, slack=float(-row@weights), multiplier=float(dual))
        for label, row, dual in zip(CONSTRAINT_LABELS, rows, data['structural_duals'])]
    data['structural_equalities'] = [dict(label=label, residual=float(row@weights), multiplier=float(dual))
        for label, row, dual in zip(EQUALITY_LABELS[1:], equalities[1:], data['structural_equality_duals'])]
    data['normalization'] = float(equalities[0]@weights)
    data['minimum_structural_slack'] = float(np.min(-rows@weights))
    # All discovery rows and line constraints are retained; a nonzero
    # structural multiplier is never silently included in a princess law.
    data['conservative_constraints'] = [label for label in CONSTRAINT_LABELS if label.startswith('conservative')]
    path.write_text(json.dumps(data, indent=2))
    print('NORMALIZATION', data['normalization'], 'MIN_SLACK', data['minimum_structural_slack'], flush=True)
    print('LABELLED_STRUCTURAL_DUALS', [(r['label'], r['multiplier']) for r in data['structural_constraints']
                                       if abs(r['multiplier']) > 1e-9], flush=True)


if __name__ == '__main__':
    main()
