"""Joint ordered-CDF discovery by exact record costs and concave cost cuts.

All initial, prefix, and post-wave nodal values move together. This is one
fixed structural collocation, not a grid-refinement bound computation. The
saved field is a complete legal continuum quantile law (up to solver error),
but finite-route feasibility is not an unrestricted game certificate.
"""
from pathlib import Path
import argparse
import json
import time
from fractions import Fraction
from collections import defaultdict
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix, vstack
from joint_cdf_field import (FieldMesh, RouteFunctional, route_pool, two_interior_pool,
                             wait_two_triangle_pool, initial_inward_pool)


OUT = Path(__file__).resolve().parent


def matrix(rows, n):
    rr, cc, vv = [], [], []
    for i, coefficients in enumerate(rows):
        for j, value in coefficients.items():
            if abs(value) > 1e-14:
                rr.append(i);cc.append(j);vv.append(value)
    return coo_matrix((vv, (rr, cc)), shape=(len(rows), n)).tocsr()


def run(maxiter=30, tolerance=2e-5, negative_v=True, positive_v=True,
        extra_routes=None, resume=None, tag='joint_cdf', center_peak=None,
        terminal_barrier=None, include_m3=False, constant_early_cone=None,
        output_dir=None, full_diagnostics=False, include_wait_pool=False, include_inward_pool=False,
        lp_method='highs'):
    started = time.time()
    mesh = FieldMesh()
    out = OUT if output_dir is None else Path(output_dir).resolve()
    out.mkdir(parents=True, exist_ok=True)
    n = len(mesh.nodes)
    pool = route_pool(mesh)
    extra_manifest = []
    if include_m3:
        pool.extend(two_interior_pool(mesh))
    if include_wait_pool:
        assert constant_early_cone is not None, 'wait templates require an exact constant cone'
        pool.extend(wait_two_triangle_pool(mesh, constant_early_cone))
    if include_inward_pool:
        pool.extend(initial_inward_pool(mesh))
    if extra_routes:
        paths = [extra_routes] if isinstance(extra_routes, str) else extra_routes
        for source in paths:
            extra = json.loads(Path(source).read_text())
            if isinstance(extra, dict):
                if 'field_response' in extra:
                    extra = [extra['field_response']]
                elif 'routes' in extra:
                    extra = extra['routes']
                elif 'route' in extra:
                    extra = [extra]
                else:
                    raise ValueError(('unrecognized extra-route payload', source))
            for j, item in enumerate(extra):
                route = item['route'] if isinstance(item, dict) else item
                label = dict(kind='external_separator', source=str(source), index=j)
                pool.append(RouteFunctional(mesh, route, label))
                extra_manifest.append(dict(label=label, route=route))
    values = mesh.seed()
    if resume:
        old = json.loads(Path(resume).read_text())
        assert np.max(np.abs(np.asarray(old['nodes'])-mesh.nodes)) < 1e-12
        values = np.asarray(old['values'])
    structural_rows, structural_rhs, structural_labels = [], [], []
    for lo, hi, axis in mesh.transport:
        structural_rows.append({lo: 1., hi: -1.})
        structural_rhs.append(0.)
        structural_labels.append(dict(kind='transport', axis=axis, lo=lo, hi=hi))
    if positive_v or negative_v:
        for coefficients, rhs, label in mesh.late_rows(negative_v=negative_v):
            if label['kind'] == 'late_positive_v' and not positive_v:
                continue
            structural_rows.append(coefficients)
            structural_rhs.append(rhs)
            structural_labels.append(label)
    if center_peak is not None:
        mesh.additional_order_edges = []
        coordinate_index = {tuple(np.round(point, 13)): i for i, point in enumerate(mesh.nodes)}
        center_nodes = [coordinate_index[tuple(np.round([t, t], 13))] for t in mesh.base]
        assert any(abs(t-center_peak) < 1e-12 for t in mesh.base), 'center peak must be a mesh coordinate'
        for ta, tb, ia, ib in zip(mesh.base, mesh.base[1:], center_nodes, center_nodes[1:]):
            sign = 1 if tb <= center_peak+1e-12 else -1
            structural_rows.append({ia: float(sign), ib: float(-sign)})
            structural_rhs.append(0.)
            structural_labels.append(dict(kind='optional_center_unimodality', start=float(ta),
                                          end=float(tb), peak=float(center_peak)))
            mesh.additional_order_edges.append((ia, ib) if sign == 1 else (ib, ia))
    if terminal_barrier is not None:
        if not hasattr(mesh, 'additional_order_edges'):
            mesh.additional_order_edges = []
        coordinate_index = {tuple(np.round(point, 13)): i for i, point in enumerate(mesh.nodes)}
        assert any(abs(t-terminal_barrier) < 1e-12 for t in mesh.base), 'barrier must be a mesh coordinate'
        peak = coordinate_index[tuple(np.round([terminal_barrier, terminal_barrier], 13))]
        for t in mesh.base:
            if t < terminal_barrier-1e-12:
                continue
            endpoint = coordinate_index[tuple(np.round([t+2, t], 13))]
            structural_rows.append({endpoint: 1., peak: -1.})
            structural_rhs.append(0.)
            structural_labels.append(dict(kind='terminal_center_barrier', departure=float(t),
                                          barrier=float(terminal_barrier), peak_node=peak,
                                          endpoint_node=endpoint))
            mesh.additional_order_edges.append((endpoint, peak))
    if constant_early_cone is not None:
        assert 0 < constant_early_cone < 1
        coordinate_index = {tuple(np.round(point, 13)): i for i, point in enumerate(mesh.nodes)}
        assert any(abs(t-constant_early_cone) < 1e-12 for t in mesh.base), 'cone cutoff must be a mesh coordinate'
        anchor = coordinate_index[tuple(np.round([constant_early_cone, 0.], 13))]
        ratios = []
        for index, (u, v) in enumerate(mesh.nodes):
            if -1e-12 <= v <= u+1e-12 and u <= constant_early_cone+1e-12:
                ratio = Fraction(str(float(u/constant_early_cone))).limit_denominator(10**7)
                ratios.append((index, ratio))
                if index == anchor:
                    continue
                for sign in [-1., 1.]:
                    coefficients = {index: sign}
                    coefficients[anchor] = -sign*float(ratio)
                    structural_rows.append(coefficients)
                    structural_rhs.append(0.)
                    structural_labels.append(dict(kind='optional_constant_early_cone', u=float(u),
                                                  v=float(v), cutoff=constant_early_cone, sign=sign))
        mesh.constant_early_cone = dict(anchor=anchor, cutoff=constant_early_cone, ratios=ratios)
    structural_matrix = matrix(structural_rows, n+1)
    structural_scale = np.array([max(1., max(abs(value) for value in row.values()))
                                 for row in structural_rows])
    scaled_structural = structural_matrix.multiply((1/structural_scale)[:, None]).tocsr()
    cuts, cut_rhs, cut_meta = [], [], []
    history = []
    objective = np.r_[np.zeros(n), -1.]
    bounds = mesh.bounds+[(0., 2.)]
    result = None
    best_actual = -np.inf
    print(json.dumps(dict(event='setup', nodes=n, triangles=len(mesh.triangles), routes=len(pool),
                          structural_rows=len(structural_rows), positive_v=positive_v,
                          negative_v=negative_v, center_peak=center_peak,
                          terminal_barrier=terminal_barrier, include_m3=include_m3,
                          constant_early_cone=constant_early_cone, include_wait_pool=include_wait_pool,
                          include_inward_pool=include_inward_pool)), flush=True)
    for iteration in range(maxiter+1):
        raw_values = values.copy()
        values, repair = mesh.repair_values(values)
        # Keep only sparse gradient entries.  Full existing-coordinate turn
        # families otherwise retain gigabytes of zero gradient components.
        evaluations=[]
        for functional in pool:
            value,gradient=functional.value_gradient(values)
            indices=np.flatnonzero(np.abs(gradient)>1e-14)
            evaluations.append((value,indices,gradient[indices]))
        costs = np.array([item[0] for item in evaluations])
        level = float(np.min(costs)) if result is None else float(result.x[-1])
        gaps = level-costs
        worst = int(np.argmin(costs))
        legal_slack = np.asarray(structural_rhs)-structural_matrix[:, :n]@values
        report = dict(iteration=iteration, linearized_level=level, minimum_route_cost=float(costs[worst]),
                      maximum_cost_cut_gap=float(np.max(gaps)), worst_route=pool[worst].label,
                      minimum_structural_slack=float(legal_slack.min()), cuts=len(cuts),
                      maximum_isotonic_repair=repair,
                      seconds=time.time()-started)
        history.append(report)
        print(json.dumps(report), flush=True)
        payload = dict(options=dict(positive_v=positive_v, negative_v=negative_v, center_peak=center_peak,
                                    terminal_barrier=terminal_barrier, include_m3=include_m3,
                                    constant_early_cone=constant_early_cone, include_wait_pool=include_wait_pool,
                                    include_inward_pool=include_inward_pool),
                       report=report, history=history,
                       route_pool=dict(version='signed_early_and_all_base_M3_v1', count=len(pool),
                                       extra_routes=extra_manifest))
        if full_diagnostics:
            payload['lp_values'] = list(map(float, raw_values))
            payload['route_costs'] = [dict(label=f.label, route=f.route, cost=float(value))
                                      for f, value in zip(pool, costs)]
        if constant_early_cone is not None:
            payload['constant_early_density'] = float(values[mesh.constant_early_cone['anchor']]/constant_early_cone)
        mesh.save(out/f'{tag}_field.json', values, compact=not full_diagnostics, **payload)
        if costs[worst] > best_actual:
            best_actual = float(costs[worst])
            mesh.save(out/f'{tag}_best_field.json', values, compact=not full_diagnostics, **payload)
        if result is not None and np.max(gaps) <= tolerance:
            break
        if iteration == maxiter:
            break
        added = 0
        for j, ((value, indices, gradient), gap) in enumerate(zip(evaluations, gaps)):
            if result is not None and gap <= max(tolerance/4, 1e-8):
                continue
            coefficients = {int(i): -float(g) for i,g in zip(indices,gradient)}
            coefficients[n] = 1.
            rhs = float(value-gradient@values[indices])
            cuts.append(coefficients);cut_rhs.append(rhs)
            cut_meta.append(dict(route_index=j, iteration=iteration, value_at_cut=float(value)))
            added += 1
        assert added
        cut_scale = np.array([max(1., max(abs(value) for value in row.values())) for row in cuts])
        scaled_cuts = matrix(cuts, n+1).multiply((1/cut_scale)[:, None]).tocsr()
        constraints = vstack([scaled_structural, scaled_cuts], format='csr')
        rhs = np.r_[np.asarray(structural_rhs)/structural_scale, np.asarray(cut_rhs)/cut_scale]
        result = linprog(objective, A_ub=constraints, b_ub=rhs, bounds=bounds, method=lp_method,
                         options=dict(dual_feasibility_tolerance=1e-10,
                                      primal_feasibility_tolerance=1e-10))
        if not result.success:
            print(json.dumps(dict(event='lp_failure', message=result.message)), flush=True)
            break
        values = result.x[:n]
    if result is not None and result.success:
        dual = -np.asarray(result.ineqlin.marginals)/np.r_[structural_scale, cut_scale]
        route_mass = np.zeros(len(pool))
        for meta, weight in zip(cut_meta, dual[len(structural_rows):]):
            route_mass[meta['route_index']] += weight
        family_mass = defaultdict(float)
        for functional, weight in zip(pool, route_mass):
            family_mass[functional.label['kind']] += float(weight)
        structural_mass = defaultdict(float)
        for label, weight in zip(structural_labels, dual[:len(structural_rows)]):
            structural_mass[label['kind']] += float(weight)
        dual_payload = dict(
            scope='LP cost-cut and structural multipliers for a fixed CDF mesh; not an upper strategy certificate',
            options=dict(positive_v=positive_v, negative_v=negative_v, center_peak=center_peak,
                         terminal_barrier=terminal_barrier, include_m3=include_m3,
                         constant_early_cone=constant_early_cone, include_wait_pool=include_wait_pool,
                         include_inward_pool=include_inward_pool),
            route_pool=dict(version='signed_early_and_all_base_M3_v1', count=len(pool),
                            extra_routes=extra_manifest),
            omitted_rows_have_zero_multiplier=not full_diagnostics,
            cost_cut_coefficients_included=full_diagnostics,
            total_counts=dict(cost_cuts=len(cuts), routes=len(pool), structural=len(structural_rows)),
            family_mass=dict(family_mass), structural_mass=dict(structural_mass),
            cost_cuts=[dict(meta=meta, multiplier=float(weight), rhs=rhs,
                           **({'coefficients': [[i, value] for i, value in row.items()]}
                              if full_diagnostics else {}))
                       for meta, weight, rhs, row in zip(cut_meta, dual[len(structural_rows):], cut_rhs, cuts)
                       if full_diagnostics or weight != 0.],
            routes=[dict(label=f.label, route=f.route, multiplier=float(weight))
                    for f, weight in zip(pool, route_mass) if full_diagnostics or weight != 0.],
            structural=[dict(label=label, multiplier=float(weight), slack=float(slack))
                        for label, weight, slack in zip(structural_labels, dual[:len(structural_rows)], legal_slack)
                        if full_diagnostics or weight != 0.],
            lower_bound_multipliers=list(map(float, result.lower.marginals)),
            upper_bound_multipliers=list(map(float, result.upper.marginals)),
            history=history)
        (out/f'{tag}_duals.json').write_text(json.dumps(dual_payload, indent=2)+'\n')
        print(json.dumps(dict(event='dual_summary', route_mass=float(route_mass.sum()),
                              structural_mass=float(dual[:len(structural_rows)].sum()),
                              cost_cut_count=len(cuts))), flush=True)
    return values, history


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--maxiter', type=int, default=30)
    parser.add_argument('--tolerance', type=float, default=2e-5)
    parser.add_argument('--no-negative-v', action='store_true')
    parser.add_argument('--no-positive-v', action='store_true')
    parser.add_argument('--extra-routes', nargs='+')
    parser.add_argument('--resume')
    parser.add_argument('--tag', default='joint_cdf')
    parser.add_argument('--center-unimodal-peak', type=float)
    parser.add_argument('--terminal-center-barrier', type=float)
    parser.add_argument('--two-interior-pool', action='store_true')
    parser.add_argument('--constant-early-cone', type=float)
    parser.add_argument('--output-dir')
    parser.add_argument('--full-diagnostics', action='store_true')
    parser.add_argument('--wait-two-triangle-pool', action='store_true')
    parser.add_argument('--initial-inward-pool', action='store_true')
    parser.add_argument('--lp-method', choices=['highs','highs-ds','highs-ipm'],default='highs')
    args = parser.parse_args()
    run(args.maxiter, args.tolerance, not args.no_negative_v, not args.no_positive_v,
        args.extra_routes, args.resume, args.tag, args.center_unimodal_peak,
        args.terminal_center_barrier, args.two_interior_pool, args.constant_early_cone,
        args.output_dir, args.full_diagnostics, args.wait_two_triangle_pool, args.initial_inward_pool,
        args.lp_method)
