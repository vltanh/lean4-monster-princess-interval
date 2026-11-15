"""Complete ordered-prefix response for the fixed singular-tail attachment.

The public coefficient order and truncation matrix are supplied by TailLaw.
Prefix pieces are frozen before producing a linear feature row.  The two
negative-prefix cases are exhaustive under the documented M3 geometry;
positive-prefix interpolation and scalar maximization remain numerical.
"""
import numpy as np
from numba import njit

from negative_prefix_oracle import general_features
from singular_tail_negative import general_tail_feature, negative_tail_cases
from singular_tail_prefix import tail_prefix


@njit
def frozen_features(parameters, packed, count, aug_knots, aug_profile,
                    mapping, left, right, turn):
    step = general_features(parameters, packed, count, aug_knots, aug_profile,
                            left, right, turn, True)
    tail = general_tail_feature(parameters, packed, count, aug_knots, aug_profile,
                                left, right)
    row = np.zeros(mapping.shape[1]+1)
    row[:-1] = step@mapping
    row[-1] = tail
    return row


@njit
def freeze_arrays(parameters, aug_knots, aug_profile, mapping, variables,
                  left, right, turn, tolerance=2e-7):
    step_variables = mapping@variables[:-1]
    amplitude = variables[-1]
    positive, npiece = tail_prefix(parameters, aug_knots, step_variables,
                                   left, right, turn, amplitude, tolerance)
    first, nf, second, ns = negative_tail_cases(parameters, aug_knots,
                                                step_variables, amplitude)
    best_row = np.zeros(len(variables))
    best_packed = np.zeros((len(positive)+len(first), 4))
    best_count = 0
    best_score = -np.inf
    for candidate in range(2):
        negative = first if candidate == 0 else second
        nnegative = nf if candidate == 0 else ns
        if nnegative < 0:
            continue
        packed = np.zeros((nnegative+npiece, 4))
        packed[:nnegative] = negative[:nnegative]
        packed[nnegative:] = positive[:npiece]
        row = frozen_features(parameters, packed, len(packed), aug_knots,
                              aug_profile, mapping, left, right, turn)
        score = row@variables
        if score > best_score:
            best_row = row
            best_count = len(packed)
            best_packed[:best_count] = packed
            best_score = score
    return best_row, best_packed, best_count


def freeze_response(parameters, law, variables, tolerance=2e-7):
    row, packed, count = freeze_arrays(np.asarray(parameters), law.aug_knots,
        law.aug_profile, law.mapping, np.asarray(variables), law.left,
        law.right, law.turn, tolerance)
    return row, packed[:count].copy()


def optimal_features(parameters, law, variables, tolerance=2e-7):
    return freeze_arrays(np.asarray(parameters), law.aug_knots,
        law.aug_profile, law.mapping, np.asarray(variables), law.left,
        law.right, law.turn, tolerance)[0]
