#!/usr/bin/env python3
"""Structural two-sided late-sheet run using the existing global oracle.

This adds a positive start band [.5,.625] with turn cap 17/16.  The choice
tests the new phase and its predicted earlier initial positions.  It is
not a certified value calculation or a density-mesh refinement.
"""
import numpy as np
import json,sys
from pathlib import Path
import discover_separated as discovery
from positive_sheet_oracle import (positive_sheet_features,positive_line_residual)


def profile(knots):
    v=np.ones(len(knots)-1)
    for j in range(len(v)):
        if knots[j]>=.5-1e-12 and knots[j+1]<=.625+1e-12:v[j]=17/16
    return v


original_features=discovery.features_affine
original_optimal=discovery.optimal_features_affine
original_freeze=discovery.freeze_response_affine
original_constraints=discovery.constraints

def features(parameters,segments,count,knots,*args):
    return original_features(parameters,segments,count,knots,*args)+positive_sheet_features(parameters,knots,profile(knots))

def optimal(parameters,knots,*args):
    return original_optimal(parameters,knots,*args)+positive_sheet_features(parameters,knots,profile(knots))

def freeze(parameters,knots,*args):
    row,segments=original_freeze(parameters,knots,*args)
    return row+positive_sheet_features(parameters,knots,profile(knots)),segments

def constraints(knots,*args):
    rows,eq=original_constraints(knots,*args);v=profile(knots)
    extra=[-positive_line_residual(knots[j],j,knots,v)for j in range(len(v))if v[j]>1]
    return np.vstack([rows,extra]),eq

discovery.features_affine=features
discovery.optimal_features_affine=optimal
discovery.freeze_response_affine=freeze
discovery.constraints=constraints

if __name__=='__main__':
    discovery.main()
    name=sys.argv[sys.argv.index('--output')+1]if '--output'in sys.argv else'separated_discovery.json'
    path=Path(__file__).with_name(name)
    if path.exists():
        data=json.loads(path.read_text())
        data['positive_profile']=profile(np.array(data['knots'])).tolist()
        data['positive_start_band']=[.5,.625]
        data['scope']='Floating two-sided late-sheet structural discovery with analytic four-scalar response reduction; not an exact bound or a lower strategy.'
        path.write_text(json.dumps(data,indent=2))
