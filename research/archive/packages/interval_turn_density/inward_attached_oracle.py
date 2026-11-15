"""Full four-scalar ceiling for the added uniform inward sheet.

The old signed-M3 feature and the independently verified uniform-inward
feature are kept separate.  The latter bounds arbitrary first-touch paths;
its ceiling is approached jointly by the canonical epsilon paths with a
single U=1 crossing and eventual endpoint arrival.  Numerical optimization
and nonzero shape multipliers still prevent a matching-law claim.
"""
from pathlib import Path
import sys

import numpy as np
from numba import njit

sys.path.insert(0, str(Path(__file__).parent.parent/'interval_turn_sheet'))
from uniform_inward_features import uniform_inward_feature_row
from uniform_inward_prefix import negative_blocks
from negative_prefix_oracle import general_features
from inward_attached_prefix import inward_prefix


@njit
def complete_graph(parameters, packed, count):
    a, u, c, y = parameters
    missing = count == 0 or packed[0, 0] >= 0.
    if missing and min(c, 0.) > -a:
        result = np.zeros((count+1, 4))
        result[0] = np.array([-a, min(c, 0.), 0., u])
        result[1:] = packed[:count]
        return result
    return packed[:count].copy()


@njit
def frozen_features(parameters, packed, count, knots, profile,
                    left, right, turn):
    old = general_features(parameters, packed, count, knots, profile,
                           left, right, turn, True)
    graph = complete_graph(parameters, packed, count)
    added = uniform_inward_feature_row(knots, parameters[0], parameters[2], graph)/4.
    result = np.zeros(len(old)+len(added))
    result[:len(old)], result[len(old):] = old, added
    return result


@njit
def freeze_arrays(parameters, knots, profile, variables, left, right, turn,
                  tolerance=2e-7):
    n = len(knots)-1
    old, h = variables[:1+4*n], variables[1+4*n:]
    negative, nnegative = negative_blocks(parameters, knots, old, h)
    positive, npositive = inward_prefix(parameters, knots, old, h,
                                         left, right, turn, tolerance)
    packed = np.zeros((nnegative+npositive, 4))
    packed[:nnegative], packed[nnegative:] = negative[:nnegative], positive[:npositive]
    row = frozen_features(parameters, packed, len(packed), knots, profile,
                           left, right, turn)
    return row, packed


def freeze_response(parameters, law, variables, tolerance=2e-7):
    return freeze_arrays(np.asarray(parameters), law.knots, law.profile,
        np.asarray(variables), law.left, law.right, law.turn, tolerance)


def optimal_features(parameters, law, variables, tolerance=2e-7):
    return freeze_response(parameters, law, variables, tolerance)[0]
