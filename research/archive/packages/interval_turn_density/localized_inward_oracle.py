"""Full response rows for the localized I law with its tied density ramp."""
from pathlib import Path
import sys

import numpy as np
from numba import njit

sys.path.insert(0, str(Path(__file__).parent.parent/'interval_turn_sheet'))
from localized_inward_features import localized_inward_feature
from localized_inward_prefix import negative_cases
from localized_ramp_basis import D, general_ramp_feature
from localized_ramp_prefix import ramp_prefix
from inward_attached_oracle import complete_graph
from negative_prefix_oracle import general_features


@njit
def frozen_features(parameters, packed, count, knots, profile, left, right, turn):
    old = general_features(parameters, packed, count, knots, profile,
                           left, right, turn, True)
    graph = complete_graph(parameters, packed, count)
    extra = general_ramp_feature(parameters, packed, count, left, right, turn)
    extra += localized_inward_feature(D, parameters[0], parameters[2], graph)/4.
    row = np.zeros(len(old)+1)
    row[:-1], row[-1] = old, extra
    return row


@njit
def freeze_arrays(parameters, knots, profile, variables, left, right, turn,
                  tolerance=2e-7):
    old, eta = variables[:-1], variables[-1]
    positive, npositive = ramp_prefix(parameters, knots, old,
                                       left, right, turn, eta, tolerance)
    first, nf, second, ns = negative_cases(parameters, knots, old, eta)
    best_score = -np.inf
    best_row = np.zeros(len(variables))
    best_packed = np.zeros((len(positive)+max(len(first),len(second)), 4))
    count = 0
    for which in range(2):
        negative = first if which == 0 else second
        nn = nf if which == 0 else ns
        if nn < 0:
            continue
        packed = np.zeros((nn+npositive, 4))
        packed[:nn], packed[nn:] = negative[:nn], positive[:npositive]
        row = frozen_features(parameters, packed, len(packed), knots, profile,
                               left, right, turn)
        value = row@variables
        if value > best_score:
            best_score, best_row, count = value, row, len(packed)
            best_packed[:count] = packed
    return best_row, best_packed, count


def freeze_response(parameters, law, variables, tolerance=2e-7):
    row, packed, count = freeze_arrays(np.asarray(parameters), law.knots,
        law.profile, np.asarray(variables), law.left, law.right, law.turn, tolerance)
    return row, packed[:count].copy()


def optimal_features(parameters, law, variables, tolerance=2e-7):
    return freeze_response(parameters, law, variables, tolerance)[0]
