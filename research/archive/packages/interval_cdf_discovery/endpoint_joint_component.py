#!/usr/bin/env python3
"""Fixed-data endpoint/f front construction on the existing tail mesh.

This is a feasibility experiment, not a game-value calculation. All post-one
rows and columns are fixed. The old pre-one field is an explicit incoming
upper obstacle; the new initial trace is solved together with the field.
"""
from pathlib import Path
from fractions import Fraction as Q
import argparse
import json
import math
import sys
import numpy as np

PACKAGE = Path(__file__).resolve().parent
from audit_snapshot import coordinate
from audit_m1 import ExactField


def positive_integral(xs, values):
    """Integral of the positive part of a continuous affine polygon."""
    total = 0.
    for a, b, fa, fb in zip(xs, xs[1:], values, values[1:]):
        if fa <= 0 and fb <= 0:
            continue
        if fa >= 0 and fb >= 0:
            total += (b-a)*(fa+fb)/2
        else:
            positive = max(fa, fb)
            total += (b-a)*positive*positive/(2*abs(fa-fb))
    return total


def integral(xs, values):
    return sum((b-a)*(fa+fb)/2 for a, b, fa, fb in zip(xs, xs[1:], values, values[1:]))


class PostRow:
    def __init__(self, row):
        self.y = row['y']
        self.V, self.R = np.asarray(row['post_row']['vertices'], float).T
        self.D = 1-self.R
        vertices = np.asarray(row['post_column']['vertices'], float)
        self.delta, self.column = vertices[:, 0], vertices[:, 1]
        self.G = row['G']['value']
        self.e = self.column[0]
        self.J = row['Jpost']['value']
        self.original_r = row['initial_deficit']['value']

    def P(self, d):
        return 2*self.y*d + positive_integral(self.V, d-self.D)

    def derivative(self, d):
        result = 2*self.y
        for a, b, da, db in zip(self.V, self.V[1:], self.D, self.D[1:]):
            if max(da, db) < d:
                result += b-a
            elif min(da, db) < d:
                result += (b-a)*(d-min(da, db))/abs(db-da)
        return result

    def inverse(self, target, subtract=0., cap=1., lower=0.):
        if target <= self.P(lower)-subtract*lower:
            return lower
        if self.P(cap)-subtract*cap <= target:
            return cap
        lo, hi = lower, cap
        for _ in range(65):
            mid = (lo+hi)/2
            if self.P(mid)-subtract*mid < target:
                lo = mid
            else:
                hi = mid
        return (lo+hi)/2

    def hinge(self, threshold):
        return positive_integral(self.delta, self.column-threshold)


def monotone_minorant(values):
    result = values.copy()
    n = len(values)
    for i in reversed(range(n)):
        for j in reversed(range(i, n)):
            if i < j:
                result[i, j] = min(result[i, j], result[i+1, j])
            if j+1 < n:
                result[i, j] = min(result[i, j], result[i, j+1])
    return result


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--field',type=Path,default=PACKAGE/'snapshots/initial_inward_candidate.json')
    parser.add_argument('--postdata',type=Path,default=PACKAGE/'snapshots/endpoint_postdata.json')
    parser.add_argument('--output-prefix',type=Path,default=PACKAGE/'snapshots/endpoint_joint')
    parser.add_argument('--include-fixed-one',action='store_true',
                        help='Include the fixed-U1 inward inequality in the local minimum of obstacles.')
    parser.add_argument('--ell-row-cap',action='store_true',
                        help='Replace the frozen incoming cap by an ell row-area cap; hold the outer initial rank fixed.')
    parser.add_argument('--cap-slope',type=float,default=0.,
                        help='Slope in y of the incoming upper cap; its intercept is still fixed by the ell row moment.')
    parser.add_argument('--trace-exponential',type=float,
                        help='Use the trace-preserving ceiling e1(y)+cap(x)*exp(rate*(y/Y-1)).')
    args=parser.parse_args()
    args.output_prefix.parent.mkdir(parents=True,exist_ok=True)
    source = json.loads(args.field.read_text())
    post = json.loads(args.postdata.read_text())
    rows = [PostRow(row) for row in sorted(post['rows'], key=lambda r:r['y'])]
    grid = np.array([row.y for row in rows])
    n, Y = len(grid), grid[-1]
    nodes = np.asarray(source['nodes'], float)
    values = np.asarray(source['values'], float)
    lookup = {(round(1-u, 14), round(1+v, 14)):i for i, (u,v) in enumerate(nodes)
              if u <= 1+1e-14 and v <= -1+Y+1e-14}
    old = np.full((n,n), np.nan)
    indices = {}
    for i,x in enumerate(grid):
        for j in range(i,n):
            idx = lookup[(round(x,14),round(grid[j],14))]
            indices[i,j]=idx
            old[i,j]=1-values[idx]
    assert len(indices)==len(lookup)
    exactsource=ExactField(source)
    endpoint_value=exactsource.positive_m1(Q(1))
    old_ell=np.array([float(exactsource.negative_m1(Q(1)-Q(str(x)))-endpoint_value)for x in grid])
    future_y=min(1+v for _,v in source['nodes']if 1+v>Y+1e-14)
    wing=(future_y-Y)/2
    old_areas=np.array([integral(grid[i:],old[i,i:])+wing*old[i,-1]for i in range(n)])
    D = old.copy()
    history=[]
    for iteration in range(200):
        r = np.zeros(n)
        for j in range(1,n):
            r[j]=rows[j].inverse(rows[j].G+integral(grid[:j+1],D[:j+1,j]))
        outer_proposal=float(r[-1])
        if args.ell_row_cap:
            r[-1]=old[-1,-1]
        assert np.min(np.diff(r))>0
        raw=np.full_like(D,np.nan)
        floor_events=[]
        for i,x in enumerate(grid):
            for j in range(i,n):
                y=grid[j]
                if i==j:
                    raw[i,j]=r[i]
                    continue
                column_min=integral(grid[:j+1],D[:j+1,j])-positive_integral(grid[:j+1],D[:j+1,j]-r[i])
                row_integral=integral(grid[i:j+1],D[i,i:j+1])
                target=rows[j].G+column_min-row_integral-rows[j].hinge(r[i])
                root=rows[j].inverse(target,subtract=y-x,cap=r[j])
                if args.include_fixed_one:
                    first_hinge=positive_integral(grid[:i+1],r[i]-D[:i+1,j])
                    target_one=8*r[i]-(8-y)*max(r[i]-rows[j].e,0)-row_integral-first_hinge
                    root_one=rows[0].inverse(target_one,subtract=y-x,cap=r[j],lower=rows[j].e)
                    root=min(root,root_one)
                if root<r[i]-1e-13:
                    floor_events.append((i,j,r[i]-root))
                physical=max(r[i],rows[j].e,min(root,r[j]))
                # Explicit old incoming attachment, with the new initial
                # lower rank barrier. This is not an asserted active phase.
                upper=max(r[i],old[i,j])
                raw[i,j]=physical if args.ell_row_cap else min(physical,upper)
        normalized=monotone_minorant(raw)
        cap_failures=[]
        cap_values=[]
        if args.ell_row_cap:
            for i,x in enumerate(grid):
                target=old_areas[i]+(8-2*x)*(r[i]-old[i,i])+4*old_ell[i]
                outgoing=np.array([row.e for row in rows[i:]])
                shape=(np.exp(args.trace_exponential*(grid[i:]/Y-1))
                       if args.trace_exponential is not None else None)
                def capped(cap):
                    ceiling=(outgoing+cap*shape if shape is not None
                             else cap+args.cap_slope*(grid[i:]-x))
                    return np.maximum(np.maximum(outgoing,r[i]),np.minimum(ceiling,normalized[i,i:]))
                def area(cap):
                    vals=capped(cap)
                    return integral(grid[i:],vals)+wing*vals[-1]
                if shape is None:
                    lo,hi=r[i]-args.cap_slope*(Y-x),max(normalized[i,i:])
                else:
                    lo,hi=0.,max(np.maximum(normalized[i,i:]-outgoing,0)/shape)
                minimum,maximum=area(lo),area(hi)
                if target<minimum-1e-16:
                    cap_failures.append(dict(x=float(x),target=float(target),minimum=float(minimum),
                                             deficit=float(minimum-target)))
                    cap=lo
                elif target>=maximum:
                    cap=hi
                else:
                    for _ in range(65):
                        mid=(lo+hi)/2
                        if area(mid)>target:hi=mid
                        else:lo=mid
                    cap=(lo+hi)/2
                normalized[i,i:]=capped(cap)
                cap_values.append(float(cap))
        new=monotone_minorant(normalized)
        error=float(np.nanmax(abs(new-D)))
        projection=float(np.nanmax(raw-new))
        history.append(dict(iteration=iteration,error=error,projection=projection,
                            floor_events=len(floor_events),front_outer=float(r[-1]),
                            outer_front_proposal=outer_proposal,ell_cap_failures=cap_failures,
                            cap_values=cap_values))
        D=new
        if error<2e-15:
            break
    else:
        raise RuntimeError('The fixed-data map did not converge in 200 iterations')

    r=np.diag(D).copy()
    f_slack=[];g_slack=[];endpoint=[];fixed_one=[]
    for j in range(1,n):
        y=grid[j];col=integral(grid[:j+1],D[:j+1,j])
        sf=(rows[j].G+col-rows[j].P(r[j]))/4
        sg=((8-y)*rows[j].e+col-rows[0].P(r[j]))/4
        f_slack.append(dict(y=float(y),slack=sf,r=float(r[j]),old_r=float(old[j,j]),
                            inverse_slope=rows[j].derivative(r[j])))
        g_slack.append(dict(y=float(y),slack=sg))
        for i in range(j):
            x=grid[i];d=D[i,j]
            row_integral=integral(grid[i:j+1],D[i,i:j+1])
            hinge_pre=positive_integral(grid[:j+1],D[:j+1,j]-r[i])
            gap=rows[j].P(r[j])-rows[j].P(d)+(y-x)*d-row_integral-hinge_pre-rows[j].hinge(r[i])
            endpoint.append(dict(x=float(x),y=float(y),slack=sf+gap/4,gap_to_f=gap/4,
                                 D=float(d),old_D=float(old[i,j]),
                                 cap_gap=float(max(r[i],old[i,j])-d)))
            # General fixed-U1 I formula, H1=0 in this supplied field.
            assert post['H1']['value']==0
            incoming_hinge=positive_integral(grid[:i+1],r[i]-D[:i+1,j])
            one=(8*r[i]-rows[0].P(d)-(x-y)*d-row_integral
                 -(8-y)*max(r[i]-rows[j].e,0)-incoming_hinge)/4
            fixed_one.append(dict(x=float(x),y=float(y),slack=one))

    output=dict(source)
    output['scope']='Fixed-post endpoint/f component feasibility experiment; no game bound or full equilibrium claim'
    output['values']=list(source['values'])
    for key,idx in indices.items():
        output['values'][idx]=float(1-D[key])
    output.pop('rational_values',None)
    newvalues=np.asarray(output['values'])
    tri=np.asarray(source['triangles'],int)
    verts=nodes[tri]
    matrix=np.concatenate((verts,np.ones((*verts.shape[:2],1))),axis=2)
    coeff=np.linalg.solve(matrix,newvalues[tri][...,None])[...,0]
    violations=[]
    exactnodes=[tuple(coordinate(v) for v in p)for p in source['nodes']]
    exactvalues=[Q(str(v))for v in output['values']]
    for index,inds in enumerate(source['triangles']):
        p,q,s=[exactnodes[k]for k in inds]
        a,b,c=[exactvalues[k]for k in inds]
        eu,ev=q[0]-p[0],q[1]-p[1]
        fu,fv=s[0]-p[0],s[1]-p[1]
        det=eu*fv-ev*fu
        ru=((b-a)*fv-(c-a)*ev)/det
        rv=(eu*(c-a)-fu*(b-a))/det
        if ru<0 or rv>0:
            violations.append(dict(triangle=index,ru=float(ru),rv=float(rv),
                                   ru_exact=str(ru),rv_exact=str(rv),
                                   nodes=[list(map(float,p))for p in verts[index]],
                                   values=list(map(float,newvalues[tri[index]]))))
    realized=ExactField(output) if not violations else None
    ell=[]
    if realized is not None:
        for i,x in enumerate(grid):
            actual=realized.negative_m1(Q(1)-Q(str(x)))-endpoint_value
            rowchange=(integral(grid[i:],D[i,i:])+wing*D[i,-1])-old_areas[i]
            predicted=old_ell[i]+((8-2*x)*(r[i]-old[i,i])-rowchange)/4
            ell.append(dict(x=float(x),slack=float(actual),exact=str(actual),
                            row_prediction=predicted,prediction_residual=float(actual)-predicted))
    report=dict(scope=output['scope'],include_fixed_one=args.include_fixed_one,ell_row_cap=args.ell_row_cap,
                cap_slope=args.cap_slope,
                trace_exponential=args.trace_exponential,
                Y=float(Y),node_count=len(indices),iterations=len(history),
                final_change=history[-1]['error'],history=history,
                fixed_post_boundary_error=float(np.max(abs(D[0]-old[0]))),
                max_local_nodal_change=float(np.nanmax(abs(D-old))),
                initial_outer_change=float(r[-1]-old[-1,-1]),
                f_node_max_abs=max(abs(item['slack'])for item in f_slack),
                endpoint_node_min=min(endpoint,key=lambda item:item['slack']),
                g_node_min=min(g_slack,key=lambda item:item['slack']),
                fixed_one_node_min=min(fixed_one,key=lambda item:item['slack']),
                ell_node_min=min(ell,key=lambda item:item['slack']) if ell else None,
                exterior_row_wing=float(wing),ell_cap_failures=cap_failures,
                physical_cone_violation_count=len(violations),physical_cone_violations=violations,
                exact_triangle_checks=len(source['triangles']),
                f=f_slack,g=g_slack,ell=ell,endpoint=endpoint,fixed_one=fixed_one)
    output['source_report']=output.pop('report',None)
    output['component_report']={k:report[k]for k in ['Y','node_count','iterations','f_node_max_abs',
        'fixed_post_boundary_error','endpoint_node_min','g_node_min','fixed_one_node_min','ell_node_min','physical_cone_violation_count']}
    def path(suffix):
        return args.output_prefix.parent/(args.output_prefix.name+suffix)
    path('_field.json').write_text(json.dumps(output,indent=2)+'\n')
    path('_report.json').write_text(json.dumps(report,indent=2)+'\n')
    local=dict(scope=output['scope'],grid=list(map(float,grid)),D=[[None if math.isnan(x)else float(x)for x in row]for row in D],
               incoming_upper_obstacle=[[None if math.isnan(x)else float(x)for x in row]for row in old],
               source_postdata=args.postdata.name,complete_field=path('_field.json').name)
    path('_local.json').write_text(json.dumps(local,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items()if k not in ['history','f','g','ell','endpoint','fixed_one','physical_cone_violations']},indent=2))
    for item in violations[:8]:print('cone failure',item)


if __name__=='__main__':
    main()
