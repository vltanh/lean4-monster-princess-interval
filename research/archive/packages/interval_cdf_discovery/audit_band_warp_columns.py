#!/usr/bin/env python3
"""Independent physical-column audit of the selected two-band warp.

The cost-difference identity and base costs are exact. Integration of the
algebraic warped field is numerical; reported errors are quadrature
estimates, not certified enclosures.
"""
import argparse
import json
from pathlib import Path
from fractions import Fraction as Q
import warnings
import numpy as np
from scipy.integrate import quad,IntegrationWarning

PACKAGE=Path(__file__).resolve().parent
from audit_m1 import ExactField
from joint_cdf_field import FieldMesh,RadialLine
from terminal_band_warp import Warp,WarpedField
from extract_endpoint_postdata import inward_one_route


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifest',type=Path,default=PACKAGE/'snapshots/endpoint_two_band_field.json')
    parser.add_argument('--output',type=Path,default=PACKAGE/'snapshots/endpoint_two_band_columns_audit.json')
    args=parser.parse_args()
    manifest=json.loads(args.manifest.read_text())
    source=args.manifest.parent/manifest['base_field']
    paths=[args.manifest.parent/name for name in manifest['bands']]
    data=json.loads(source.read_text());mesh=FieldMesh(data['base']);values=np.array(data['values'])
    exact=ExactField(data);level=exact.positive_m1(Q(1))
    provider=WarpedField(args.manifest)
    initial_x=np.array([float(x)for x,_ in exact.initial])
    initial_a=np.array([float(a)for _,a in exact.initial])
    warps=[]
    for path in paths:
        payload=json.loads(path.read_text())
        assert payload['status'].startswith('exact terminal inverse range')
        warps.append((float(Q(payload['qlo'])),float(Q(payload['qhi'])),Warp(payload)))
    def R(u,v):
        return sum(values[k]*w for k,w in mesh.weights(float(u),float(v)))
    def h(value,lo,hi):return max(0.,min(hi-lo,value-lo))
    def delta(u,v):
        old=R(u,v)
        initial=float(np.interp(u,initial_x,initial_a))
        return sum(h(min(initial,R(w(u),v)),lo,hi)-h(old,lo,hi) for lo,hi,w in warps)
    output=dict(scope='Corrected initial-front-capped two-band construction; numerical integration of an exact physical fixed-positive-start cost difference. Supersedes the uncapped diagnostic. Not an all-monster certificate.',
                quadrature_scope='Error estimates are not rigorous enclosures; numerical inverse evaluation also uses doubles.',
                exact_identity='4*DeltaCf(a)=4*DeltaCg(a)=-integral_a^1(Rnew-Rold)(U,-a)dU for a below every bridge.',
                manifest=args.manifest.name,base=source.name,warps=[path.name for path in paths],
                endpoint_value=float(level),endpoint_value_exact=str(level),rows=[])
    for a in [Q(1,4),Q(1,2),Q(5,8),Q(3,4),Q(13,16),Q(7,8),Q(15,16),Q(31,32),Q(49,50)]:
        af=float(a);v=-af;lo=min(w.bridge for _,_,w in warps)
        assert af<lo
        cuts={lo,1.}
        cuts.update(float(u)for u in mesh.ugrid if lo<u<1)
        for _,_,w in warps:
            cuts.update(x for piece in w.pieces for x in piece[:2] if lo<x<1)
            cuts.update(x for x in [w.bridge,w.start,w.repair_end,w.at_end]if lo<x<1)
        # Retain the original affine column's threshold crossings and the
        # preimages of all its knots under each monotone warp.
        column=RadialLine(mesh,v,lo,1.,False)
        original=[lo];at=lo
        for width,left,right in column.cells:
            fl,fr=left.value(values),right.value(values)
            for qlo,qhi,_ in warps:
                for q in [qlo,qhi]:
                    if (fl-q)*(fr-q)<0:
                        original.append(at+width*(q-fl)/(fr-fl))
            at+=width;original.append(at)
        cuts.update(x for x in original if lo<x<1)
        for _,_,w in warps:
            for target in original:
                if not w(lo)<target<w(1.):continue
                aa,bb=lo,1.
                for _ in range(60):
                    mid=(aa+bb)/2
                    if w(mid)<target:aa=mid
                    else:bb=mid
                cuts.add((aa+bb)/2)
        cuts=sorted(cuts)
        agreement=0.
        for left,right in zip(cuts,cuts[1:]):
            u=(left+right)/2
            agreement=max(agreement,abs(provider.radial(u,v)-R(u,v)-delta(u,v)))
        assert agreement<1e-8,('independent band/provider mismatch',a,agreement)
        integral=error=0.;evaluations=0
        def f(u):
            nonlocal evaluations
            evaluations+=1
            return delta(u,v)
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter('always',IntegrationWarning)
            for left,right in zip(cuts,cuts[1:]):
                val,err=quad(f,left,right,epsabs=2e-14,epsrel=2e-10,limit=100)
                integral+=val;error+=err
        cf=exact.positive_m1(a)
        cg=exact.unit_route_payoff(inward_one_route(a,a))
        row=dict(start=str(a),column_integral=integral,quadrature_error_estimate=error,
                 four_cost_change=-integral,cost_change=-integral/4,
                 old_f=float(cf),old_g=float(cg),
                 old_f_exact=str(cf),old_g_exact=str(cg),
                 new_f=float(cf)-integral/4,new_g=float(cg)-integral/4,
                 new_f_slack=float(cf-level)-integral/4,new_g_slack=float(cg-level)-integral/4,
                 integration_pieces=len(cuts)-1,evaluations=evaluations,
                 independent_provider_max_discrepancy=agreement,
                 quadrature_warnings=sorted(set(str(w.message)for w in caught)))
        output['rows'].append(row)
        print(a,'delta=',f'{row["cost_change"]:.12g}',
              'fslack=',f'{row["new_f_slack"]:.12g}',
              'gslack=',f'{row["new_g_slack"]:.12g}',flush=True)
    path=args.output
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(output,indent=2)+'\n')
    print('Saved',path)


if __name__=='__main__':main()
