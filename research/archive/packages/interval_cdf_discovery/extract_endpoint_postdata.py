#!/usr/bin/env python3
"""Extract exact characteristic moments for a joint endpoint/f component.

The saved field remains a diagnostic input.  These data do not assert
endpoint or f indifference, and do not select an incoming obstacle.
The ExactField representation used here has no outgoing V=1 atom;
the explicit H1 check below is part of the supported input scope.
"""
import argparse
from bisect import bisect_right
from fractions import Fraction as Q
import json
from pathlib import Path

from audit_m1 import ExactField


def pack(value):
    return dict(exact=str(value), value=float(value))


def line(field, fixed, left, right, axis):
    """Ordered exact vertices on U=fixed (axis0) or V=fixed (axis1)."""
    i = max(0, min(len(field.grid[axis])-2,
                   bisect_right(field.grid[axis], fixed)-1))
    possible = (set(field.strips[axis].get(i, []))
                | set(field.strips[axis].get(i-1, [])))
    cuts = {left, right}
    other = 1-axis
    for number in possible:
        points = field.triangles[number][0]
        for a, b in zip(points, points[1:]+points[:1]):
            if a[axis] == b[axis]:
                if a[axis] == fixed:
                    cuts.update(p[other] for p in (a, b) if left < p[other] < right)
            elif min(a[axis], b[axis]) <= fixed <= max(a[axis], b[axis]):
                z = a[other]+(fixed-a[axis])*(b[other]-a[other])/(b[axis]-a[axis])
                if left < z < right:
                    cuts.add(z)
    vertices = [(z, field.radial(fixed, z) if axis == 0
                 else field.radial(z, fixed)) for z in sorted(cuts)]
    assert all((a[1] >= b[1] if axis == 0 else a[1] <= b[1])
               for a, b in zip(vertices, vertices[1:]))
    return vertices


def serialize(vertices):
    return dict(vertices=[[float(x), float(y)] for x, y in vertices],
                rational_vertices=[[str(x), str(y)] for x, y in vertices])


def hinge(vertices, threshold):
    """Integral (value-threshold)+ along a piecewise affine line."""
    total = Q(0)
    for (a, fa), (b, fb) in zip(vertices, vertices[1:]):
        fa, fb = fa-threshold, fb-threshold
        if fa <= 0 and fb <= 0:
            continue
        if fa >= 0 and fb >= 0:
            total += (b-a)*(fa+fb)/2
        else:
            total += (b-a)*max(fa, fb)**2/(2*abs(fb-fa))
    return total


def positive_measure(vertices, threshold, closed=False):
    total = Q(0)
    for (a, fa), (b, fb) in zip(vertices, vertices[1:]):
        fa, fb = fa-threshold, fb-threshold
        if fa == fb == 0:
            if closed:
                total += b-a
        elif min(fa, fb) >= 0:
            total += b-a
        elif max(fa, fb) > 0:
            total += (b-a)*max(fa, fb)/abs(fb-fa)
    return total


def primitive(vertices, y, deficit):
    return 2*y*deficit+hinge(vertices, 1-deficit)


def endpoint_route(a, b):
    return [(Q(0), a), ((a-b)/2, (a+b)/2),
            (1-b, Q(1)), (3-b, Q(-1))]


def inward_one_route(a, b):
    return [(Q(0), a), ((a-b)/2, (a+b)/2),
            ((1-b)/2, (1+b)/2), (Q(2), Q(-1)), (Q(4), Q(1))]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('field', type=Path)
    parser.add_argument('--activity', type=Path)
    parser.add_argument('--maximum-y', default='1/128')
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    data = json.loads(args.field.read_text())
    field = ExactField(data)
    maximum = Q(args.maximum_y)
    ys = sorted({Q(0), maximum} | {1-a for a in field.initial_knots if 0 <= 1-a <= maximum})
    row0 = line(field, Q(1), Q(-1), Q(1), 0)
    p01 = primitive(row0, Q(0), Q(1))
    h1 = field.integral(Q(1), Q(1), Q(3), 1)
    assert h1 == 0, 'This extractor uses the no-V=1-atom endpoint baseline'
    basecost = field.positive_m1(Q(1))
    out = dict(scope='Exact post-one characteristic data from a saved diagnostic field; '
                     'neither active costs nor an incoming attachment are assumed.',
               source_field=str(args.field.resolve()),
               maximum_y=str(maximum), P0_at_one=pack(p01), H1=pack(h1),
               endpoint_sweep_cost=pack(basecost), rows=[], endpoint_rows=[])
    rows = {}
    for y in ys:
        postrow = line(field, 1+y, -1+y, Q(1), 0)
        if y:
            postcol = [(u-1, 1-r) for u, r in
                       line(field, -1+y, Q(1), 1+y, 1)]
        else:
            postcol = [(Q(0), 1-field.radial(Q(1), Q(-1)))]
        jpost = sum(((b-a)*(fa+fb)/2 for (a, fa), (b, fb)
                     in zip(postcol, postcol[1:])), Q(0))
        assert jpost == y-field.integral(-1+y, Q(1), 1+y, 1)
        py1 = primitive(postrow, y, Q(1))
        qall = py1-p01-y
        gy = 3*y+qall+h1+jpost
        r = 1-field.initial_value(1-y)
        precol = y-field.integral(-1+y, 1-y, Q(1), 1)
        pyr = primitive(postrow, y, r)
        cf = field.positive_m1(1-y)
        assert pyr-gy-precol == -4*(cf-basecost)
        derivlo = 2*y+positive_measure(postrow, 1-r)
        derivhi = 2*y+positive_measure(postrow, 1-r, closed=True)
        item = dict(y=float(y), y_exact=str(y), U_exact=str(1+y),
                    post_row=serialize(postrow), post_column=serialize(postcol),
                    endpoint_interior_trace=pack(postrow[0][1]),
                    Jpost=pack(jpost), P_at_one=pack(py1), Q_all=pack(qall), G=pack(gy),
                    initial_deficit=pack(r), P_at_initial_deficit=pack(pyr),
                    alpha_derivative_left=pack(derivlo), alpha_derivative_right=pack(derivhi),
                    pre_column_deficit_integral=pack(precol),
                    f_cost=pack(cf), f_minus_endpoint=pack(cf-basecost),
                    front_equation_residual=pack(pyr-gy-precol))
        if y:
            item['alpha_sqrt_coefficient'] = [float(derivlo)/(float(y)**.5),
                                              float(derivhi)/(float(y)**.5)]
        rows[y] = (item, postrow)
        out['rows'].append(item)
    if args.activity:
        activity = json.loads(args.activity.read_text())
        for source in activity['endpoint_rows']:
            x, y = Q(source['x']), Q(source['y'])
            if y > maximum:
                continue
            item, postrow = rows[y]
            a, b = 1-x, 1-y
            rx, ry = 1-field.initial_value(a), 1-field.initial_value(b)
            d0 = 1-field.radial(a, -b)
            prow = (y-x)-field.integral(a, -a, -b, 0)
            pcol = field.integral(-b, b, 1+y, 1, 1-rx)
            pyr, pyd = primitive(postrow, y, ry), primitive(postrow, y, d0)
            ce = field.unit_route_payoff(endpoint_route(a, b))
            cf = field.positive_m1(b)
            ci1 = field.unit_route_payoff(inward_one_route(a, b))
            cg = field.unit_route_payoff(inward_one_route(b, b))
            rhs = pyr-pyd+(y-x)*d0-prow-pcol
            assert rhs == 4*(ce-cf)
            dl = 2*y+positive_measure(postrow, 1-d0)
            dr = 2*y+positive_measure(postrow, 1-d0, closed=True)
            slope = float(item['alpha_derivative_left']['value'])
            ratio = float(x/y)
            shape = 2/3-ratio**.5+ratio-2/3*ratio**1.5
            out['endpoint_rows'].append(dict(
                x=pack(x), y=pack(y), x_over_y=ratio, mass=source['mass'],
                r_x=pack(rx), r_y=pack(ry), D0=pack(d0), initial_band_deficit=pack(ry-d0),
                P_at_D0=pack(pyd), alpha_at_D0_derivatives=[pack(dl), pack(dr)],
                pre_row_deficit_integral=pack(prow), full_column_hinge=pack(pcol),
                endpoint_cost=pack(ce), endpoint_minus_f=pack(ce-cf),
                g_minus_f=pack(cg-cf), I1_minus_f=pack(ci1-cf),
                endpoint_obstacle_residual=pack(rhs),
                post_alpha_excess_at_r=pack(pyr-primitive(row0, Q(0), ry)-y*ry),
                post_alpha_excess_at_D0=pack(pyd-primitive(row0, Q(0), d0)-y*d0),
                outer_profile_predicted_gap=(float(ry)*float(y)*shape/slope if slope else None)))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(out, indent=2)+'\n')
    print('Saved', args.output)
    print('Exact post rows:', len(out['rows']), 'endpoint cost/obstacle audits:', len(out['endpoint_rows']))
    print('P0(1)=',float(p01),'H1=',float(h1))
    for row in out['endpoint_rows']:
        print(row['x']['exact'], row['y']['exact'],
              'D0=', f"{row['D0']['value']:.12g}",
              'gap=', f"{row['initial_band_deficit']['value']:.6g}",
              'pred=', f"{row['outer_profile_predicted_gap']:.6g}",
              'end-f=', f"{row['endpoint_minus_f']['value']:.6g}")


if __name__ == '__main__':
    main()
