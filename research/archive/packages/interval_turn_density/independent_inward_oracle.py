"""Complete response for an independent localized initial-inward triangle."""
from pathlib import Path
import sys

import numpy as np
from numba import njit

sys.path.insert(0,str(Path(__file__).parent.parent/'interval_turn_sheet'))
from localized_inward_features import localized_inward_feature
from localized_independent_prefix import negative_blocks
from localized_ramp_basis import D
from m3_attached_oracle import attached_prefix
from inward_attached_oracle import complete_graph
from negative_prefix_oracle import general_features


@njit
def frozen_features(parameters,packed,count,knots,profile,left,right,turn):
    old=general_features(parameters,packed,count,knots,profile,left,right,turn,True)
    graph=complete_graph(parameters,packed,count)
    row=np.zeros(len(old)+1)
    row[:-1]=old
    row[-1]=localized_inward_feature(D,parameters[0],parameters[2],graph)/4.
    return row


@njit
def freeze_arrays(parameters,knots,profile,variables,left,right,turn,tolerance=2e-7):
    old,eta=variables[:-1],variables[-1]
    negative,nn=negative_blocks(parameters,knots,old,eta)
    positive,npiece=attached_prefix(parameters,knots,old,left,right,turn,tolerance)
    packed=np.zeros((nn+npiece,4))
    packed[:nn],packed[nn:]=negative[:nn],positive[:npiece]
    row=frozen_features(parameters,packed,len(packed),knots,profile,left,right,turn)
    return row,packed


def freeze_response(parameters,law,variables,tolerance=2e-7):
    return freeze_arrays(np.asarray(parameters),law.knots,law.profile,
        np.asarray(variables),law.left,law.right,law.turn,tolerance)


def optimal_features(parameters,law,variables,tolerance=2e-7):
    return freeze_response(parameters,law,variables,tolerance)[0]
