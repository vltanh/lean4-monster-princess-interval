#!/usr/bin/env python3
"""Diagnostic dual repair on legal equal-score positive-prefix contours.

This keeps the attached upper law fixed. It augments canonical response
rows with maximal and intermediate monotone selections on their flat
prefix faces, then asks whether the finite adjoint can set the artificial
f/p/k monotonicity multipliers to zero. An infeasible/deficient finite
repair does not exclude every continuous geometry or every scalar face.
"""
import json
from pathlib import Path

import numpy as np
from scipy.optimize import linprog

from discover_m3_attached import constraints, CONSTRAINT_LABELS
from m3_attached_oracle import (attached_prefix, attached_features, alpha, target,
    beta_integral_row, M3_RIGHT, M3_TURN)
from separated_oracle import value_at
from m3_face_features import general_face_features


def restrict_segments(segments, cuts):
    out = []
    for lo, hi in zip(cuts[:-1], cuts[1:]):
        if hi <= lo+1e-12:
            continue
        mid = (lo+hi)/2
        found = next(s for s in segments if s[0]-1e-10 <= mid <= s[1]+1e-10)
        out.append([lo, hi, found[2], found[3]])
    return np.asarray(out)


def flat_face(parameters, knots, weights, left, right, s0, canonical):
    a, u, c, y = parameters
    if c <= 0 or len(canonical) == 0:
        return []
    n = len(knots)-1
    p = weights[1:1+n]+weights[1+n:1+2*n]
    k = weights[1+2*n:1+3*n]
    cuts = sorted(set([0., c]+[float(z) for z in knots if 0 < z < c]
                      +[float(z) for s in canonical for z in s[:2]]
                      +[z for z in (M3_RIGHT, left, right) if 0 < z < c]))
    base = restrict_segments(canonical, cuts)
    correction = beta_integral_row(left, min(right, a), knots, s0+6)@weights
    upper = []
    labels = []
    for lo, hi, slope, intercept in base:
        mid = (lo+hi)/2
        low = slope*mid+intercept
        cap = max(low, slope*hi+intercept)
        label = 'unique'
        # On either corrected corridor the whole plateau above its lower
        # turn is available when all small M3 starts lie below a.
        if a >= M3_RIGHT-1e-9:
            if 0 <= mid < M3_RIGHT and low >= M3_TURN-1e-9:
                cap, label = 1., 'universal small M3 corridor'
            elif left < mid < right and low >= s0-1e-9:
                cap, label = 1., 'universal negative early corridor'
            else:
                t0 = target(a, lo+1e-10, knots, p, k, left, right, s0, correction)
                t1 = target(a, hi-1e-10, knots, p, k, left, right, s0, correction)
                if abs(t1-t0) < 2e-10:
                    for j in range(n):
                        if knots[j+1] > low+1e-9 and abs(k[j]-t0) < 2e-10:
                            cap = max(cap, knots[j+1])
                            label = 'constant alpha and target'
        upper.append(min(1., cap))
        labels.append(label)
    # Keep a unique branch pointwise unchanged. A pointwise maximal flat
    # plateau is capped by the lowest future maximizing inverse.
    future = 1.
    for i in range(len(upper)-1, -1, -1):
        lo, hi, slope, intercept = base[i]
        if labels[i] == 'unique':
            future = min(future, slope*lo+intercept)
        else:
            upper[i] = min(upper[i], future)
            future = min(future, upper[i])
    variants = []
    for fraction in (1., .5):
        rows = []
        for i, (lo, hi, slope, intercept) in enumerate(base):
            if labels[i] == 'unique':
                rows.append([lo, hi, slope, intercept])
                continue
            if upper[i] < slope*hi+intercept-1e-8:
                raise AssertionError(('nonlegal plateau cap', i, upper[i], base[i]))
            # Convex interpolation between ordered maximizing selections.
            rows.append([lo, hi, (1-fraction)*slope,
                         (1-fraction)*intercept+fraction*upper[i]])
        variants.append((np.asarray(rows), labels, fraction))
    return variants


def solve_adjoint(rows, structural, equalities, keep):
    nr, nv = rows.shape
    matrix = np.vstack((np.c_[rows, -np.ones(nr)],
                         np.c_[structural[keep], np.zeros(len(keep))]))
    eq = np.c_[equalities, np.zeros(len(equalities))]
    rhs = np.zeros(len(eq)); rhs[0] = 1.
    result = linprog(np.r_[np.zeros(nv), 1.], A_ub=matrix,
                     b_ub=np.zeros(len(matrix)), A_eq=eq, b_eq=rhs,
                     bounds=[(0, None)]*nv+[(None, None)], method='highs',
                     options={'primal_feasibility_tolerance': 1e-9,
                              'dual_feasibility_tolerance': 1e-9})
    if not result.success:
        return dict(success=False, status=result.message)
    return dict(success=True, level=float(result.fun),
                response_dual_mass=float(-sum(result.ineqlin.marginals[:nr])),
                structural_multiplier_mass=float(np.sum(abs(result.ineqlin.marginals[nr:]))),
                weights=result.x[:-1].tolist(),
                primal_residual=float(np.max(matrix@result.x)),
                monotonicity_violations=[dict(label=CONSTRAINT_LABELS[j], violation=float(structural[j]@result.x[:-1]))
                                         for j in range(len(structural))
                                         if 'nondecreasing' in CONSTRAINT_LABELS[j]
                                         and structural[j]@result.x[:-1] > 1e-8])


def main():
    path = Path(__file__).with_name('m3_attached_settled.json')
    data = json.loads(path.read_text())
    knots = np.asarray(data['knots'])
    profile = np.asarray(data['affine_profile'])
    weights = np.r_[data['endpoint_mass'], *(data['densities'][name] for name in ('f', 'g', 'k', 'ell'))]
    left, right, s0 = data['left'], data['right'], data['turn']
    structural, equalities = constraints(knots, np.asarray(data['profile']), left, right, s0,
        None, profile, data['negative_start_bound'], True)
    shapes = data['active_shape_samples']+[r['parameters'] for r in data['response_dual_support']]
    canonical_rows, augmented_rows, additions = [], [], []
    distinct = set()
    max_equal_score_error = 0.
    max_feature_change = 0.
    for shape in shapes:
        key = tuple(round(x, 10) for x in shape)
        if key in distinct:
            continue
        distinct.add(key)
        parameters = np.asarray(shape)
        segments, count = attached_prefix(parameters, knots, weights, left, right, s0)
        segments = segments[:count]
        base = attached_features(parameters, segments, len(segments), knots, profile, left, right, s0)
        if base@weights < data['objective']-2e-6:
            continue
        canonical_rows.append(base)
        augmented_rows.append(base)
        for variant, labels, fraction in flat_face(parameters, knots, weights, left, right, s0, segments):
            row = general_face_features(parameters, variant, len(variant), knots, profile, left, right, s0)
            error = float(abs((row-base)@weights))
            change = float(np.max(abs(row-base)))
            max_equal_score_error = max(max_equal_score_error, error)
            if error <= 2e-8:
                augmented_rows.append(row)
                max_feature_change = max(max_feature_change, change)
                additions.append(dict(parameters=shape, fraction=fraction,
                    score_difference=float((row-base)@weights), maximum_feature_change=change,
                    interval_labels=labels, prefix=variant.tolist()))
    canonical_rows = np.asarray(canonical_rows)
    augmented_rows = np.asarray(augmented_rows)
    all_rows = list(range(len(structural)))
    without_shape = [j for j, label in enumerate(CONSTRAINT_LABELS) if 'nondecreasing' not in label]
    solves = dict(canonical_all_constraints=solve_adjoint(canonical_rows, structural, equalities, all_rows),
                  augmented_all_constraints=solve_adjoint(augmented_rows, structural, equalities, all_rows),
                  canonical_zero_monotonicity_duals=solve_adjoint(canonical_rows, structural, equalities, without_shape),
                  augmented_zero_monotonicity_duals=solve_adjoint(augmented_rows, structural, equalities, without_shape))
    n = len(knots)-1
    p = weights[1:1+n]+weights[1+n:1+2*n]
    k = weights[1+2*n:1+3*n]
    output = dict(scope='Finite equality-face adjoint diagnostic; no exhaustive scalar-face or game certificate.',
        upper_law=path.name, fixed_law_response=data['response'], canonical_row_count=len(canonical_rows),
        retained_equal_score_variants=len(additions), maximum_checked_score_error=max_equal_score_error,
        maximum_retained_feature_change=max_feature_change,
        minimum_raw_p_k_height_difference=float(np.min(abs(p[:, None]-k[None, :]))),
        solves=solves, variants=additions)
    destination = Path(__file__).with_name('m3_response_face_repair.json')
    destination.write_text(json.dumps(output, indent=2))
    print('EQUALITY_FACE_ROWS', len(canonical_rows), len(additions),
          'MAX_FEATURE_CHANGE', max_feature_change, 'MAX_SCORE_ERROR', max_equal_score_error)
    for label, answer in solves.items():
        print(label, {key: value for key, value in answer.items() if key != 'weights'})
    print('OUTPUT', destination)


if __name__ == '__main__':
    main()
