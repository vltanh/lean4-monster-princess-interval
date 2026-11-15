#!/usr/bin/env python3
"""Exact I-sheet moment checks against independent physical intersections.

Uses only the standard library and the chronological physical oracle from
verify_bulk_contact_equations.py. No equality/optimality of an I-sheet or
equilibrium is inferred from these fixtures.
"""
from fractions import Fraction as Q
from pathlib import Path
import argparse
import json
from verify_bulk_contact_equations import cdf, integral, physical_score


def route(a,z):
    d=(z-a)/2;h=z/2
    return [(Q(0),1-a),(d,1-(a+z)/2),(h,1-z/2),
            (Q(2),Q(-1)),(Q(4),Q(1))]


def moments(a,z,T):
    d=(z-a)/2;h=z/2
    f=cdf(0,1-a,T);l=cdf(d,1-(a+z)/2,T);k=cdf(h,1-z/2,T)
    J=integral(T,Q(0),d,Q(-1),1-a)
    raw=integral(T,d,h,Q(1),1-z)
    clipped=integral(T,d,h,Q(1),1-z,f)
    R=raw+f*(h-d)-clipped
    H=integral(T,Q(0),Q(2),Q(-1),Q(1),l)
    cost=4+H+J-R-d*(f+l)-(4-h)*max(f,k)
    return cost,(f,l,k,J,R,H)


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("output",type=Path)
    args=ap.parse_args()
    counts={"physical_I_costs":0,"nontrivial_peak_below_initial_record":0,
        "peak_above_initial_record":0,"direct_inward_dominance":0,
        "monotone_scalar_chords":0,"smooth_z_derivatives":0,
        "sweep_boundary":0,"principal_boundary":0}
    branches=0
    for T in (Q(0),Q(1),Q(2)):
        for zi in range(1,16):
            z=Q(zi,16)
            for ai in range(zi+1):
                a=Q(ai,16)
                physical,n=physical_score(route(a,z),T);branches+=n
                formula,(f,l,k,J,R,H)=moments(a,z,T)
                assert physical==formula,(T,a,z,physical,formula)
                counts["physical_I_costs"]+=1
                if k<f and a>0:
                    counts["nontrivial_peak_below_initial_record"]+=1
                if k>f:
                    counts["peak_above_initial_record"]+=1
                if k<=f and a>0:
                    direct,n=physical_score([(Q(0),1-a),(2-a,Q(-1)),(4-a,Q(1))],T)
                    branches+=n
                    assert physical-direct>=a*(1-f),(T,a,z,physical,direct,f)
                    counts["direct_inward_dominance"]+=1
                if a==0:
                    sweep,_=physical_score([(Q(0),Q(1)),(Q(2),Q(-1))],T)
                    assert physical==sweep
                    counts["sweep_boundary"]+=1
                if a==z:
                    pure,_=physical_score([(Q(0),1-z),(z/2,1-z/2),
                                          (Q(2),Q(-1)),(Q(4),Q(1))],T)
                    assert physical==pure
                    counts["principal_boundary"]+=1
                # The front may have flat intervals; this global chord
                # inequality does not replace its derivative by z/2.
                d=(z-a)/2
                for left,right in ((Q(0),k/3),(k/3,2*k/3),(2*k/3,k)):
                    Hleft=integral(T,Q(0),Q(2),Q(-1),Q(1),left)
                    Hright=integral(T,Q(0),Q(2),Q(-1),Q(1),right)
                    assert Hright-Hleft-d*(right-left)>=a*(right-left)/2
                    counts["monotone_scalar_chords"]+=1
                # Stationary-until2 gives a smooth active max branch:
                # L=1-(a+z)/4, -L_z=1/4, beta=2a-z,
                # and H'(L)=(a+z)/2. Check the derived z equation
                # against a central difference of PHYSICAL first contacts.
                if T==2 and 0<a<z<min(1,2*a):
                    e=Q(1,4096)
                    minus,_=physical_score(route(a,z-e),T)
                    plus,_=physical_score(route(a,z+e),T)
                    derivative=(plus-minus)/(2*e)
                    beta=2*a-z
                    denom=2*((a+z)/2)-z+a
                    rhs=-denom/4+beta/4+(k-f)+(8-z)/4
                    assert 2*derivative==rhs
                    assert derivative==1+a/4-3*z/8
                    counts["smooth_z_derivatives"]+=1
    report={"status":"PASS",
        "scope":"Physical first-contact replay of the I-sheet cost, dominance and derivative identities; no active-sheet or equilibrium claim.",
        "princess_family":"Uniform initial radius; stationary until T in{0,1,2}, then unit outward and endpoint-sticky.",
        "counts":counts,"physical_affine_contact_branches":branches}
    text=json.dumps(report,indent=2)+"\n"
    args.output.write_text(text)
    print(text,end="")


if __name__=="__main__":
    main()
