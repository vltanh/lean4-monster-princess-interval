#!/usr/bin/env python3
"""Recover a restricted-class response dual from archived active paths.

The structural multipliers are retained.  This is a geometry diagnostic,
not a princess strategy certified against arbitrary monster paths.
"""

import argparse
import json
from pathlib import Path

import numpy as np
from scipy.optimize import linprog

from discover_separated import constraints
from separated_oracle import features, features_affine


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("input",nargs="?",default="split_edge_affine_discovery.json")
    parser.add_argument("--output",default="split_edge_affine_dual_seed.json")
    args=parser.parse_args()
    base=Path(__file__).resolve().parent
    data=json.loads((base/args.input).read_text())
    knots=np.array(data["knots"]);profile=np.array(data["profile"])
    affine=None if data["affine_profile"] is None else np.array(data["affine_profile"])
    left,right,s0=data["left"],data["right"],data["turn"]
    structural,equalities=constraints(knots,profile,left,right,s0,data["cap_level"],
        affine,data["negative_start_bound"],data["edge_trace"])
    feature_fn=features if affine is None else features_affine
    active_profile=profile if affine is None else affine
    matrix=[]
    for shape,prefix in zip(data["active_shape_samples"],data["active_prefix_samples"]):
        seg=np.array(prefix,dtype=float).reshape((-1,4))
        matrix.append(feature_fn(np.array(shape),seg,len(seg),knots,active_profile,
                                 left,right,s0,data["edge_trace"]))
    matrix=np.array(matrix);m,N=matrix.shape
    rows=np.vstack((np.c_[matrix,-np.ones(m)],np.c_[structural,np.zeros(len(structural))]))
    eq=np.c_[equalities,np.zeros(len(equalities))]
    rhs=np.zeros(len(eq));rhs[0]=1
    result=linprog(np.r_[np.zeros(N),1.],A_ub=rows,b_ub=np.zeros(len(rows)),
        A_eq=eq,b_eq=rhs,bounds=[(0,None)]*N+[(None,None)],method="highs",
        options={"primal_feasibility_tolerance":1e-9,"dual_feasibility_tolerance":1e-9})
    if not result.success:
        raise RuntimeError(result.message)
    support=[dict(parameters=shape,prefix=prefix,weight=float(-dual))
        for shape,prefix,dual in zip(data["active_shape_samples"],
                                     data["active_prefix_samples"],
                                     result.ineqlin.marginals[:m]) if dual < -1e-10]
    support.sort(key=lambda item:item["parameters"][0])
    output=dict(scope="Restricted-class dual reconstructed from archived active response rows; not a global lower law.",
        source=args.input,original_objective=data["objective"],objective=float(result.fun),
        response_mass=sum(item["weight"] for item in support),support=support,
        structural_inequality_duals=result.ineqlin.marginals[m:].tolist(),
        structural_equality_duals=result.eqlin.marginals[1:].tolist(),
        structural_inequality_mass=float(abs(result.ineqlin.marginals[m:]).sum()),
        structural_equality_mass=float(abs(result.eqlin.marginals[1:]).sum()),
        normalization_dual=float(result.eqlin.marginals[0]),
        recovered_weights=result.x[:-1].tolist())
    dest=base/args.output;dest.write_text(json.dumps(output,indent=2))
    print(json.dumps({key:output[key] for key in ("objective","original_objective", "response_mass",
        "structural_inequality_mass","structural_equality_mass")},indent=2))
    for item in support:
        print("ACTIVE",item["weight"],item["parameters"])
    print("OUTPUT",dest)


if __name__=="__main__":main()
