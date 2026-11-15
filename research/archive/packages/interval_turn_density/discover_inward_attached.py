#!/usr/bin/env python3
"""Fit an additional independent uniform initial-inward density.

All old density coordinates and all old physical residual conditions remain.
There is one new nondecreasing h profile on those same intervals.  The graph
response uses exact negative-prefix arrangement and ordered positive crossing.
This is structural discovery, not a certified game bound or lower strategy.
"""
import argparse
import json
import time
from pathlib import Path

import numpy as np
from scipy.optimize import differential_evolution, linprog, minimize

from separated_oracle import baseline_prefix, parameters_to_unit, unit_to_parameters
from inward_attached_law import InwardLaw
from inward_attached_oracle import frozen_features, freeze_response, optimal_features


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--rounds', type=int, default=8)
    parser.add_argument('--output', default='inward_attached_discovery.json')
    parser.add_argument('--seed', default='negative_prefix_discovery.json')
    parser.add_argument('--h-mode', choices=('monotone', 'curvature'), default='monotone')
    args = parser.parse_args()
    started = time.time()
    directory = Path(__file__).parent
    source = json.loads((directory/args.seed).read_text())
    law_type = InwardLaw
    if args.h_mode == 'curvature':
        from inward_curvature_law import CurvatureInwardLaw
        law_type = CurvatureInwardLaw
    law = law_type(source['knots'], source['affine_profile'], source['left'],
                    source['right'], source['turn'], source['negative_start_bound'])
    parameters, paths, rows = [], [], []
    def add_frozen(p, packed):
        packed = np.asarray(packed, dtype=float).reshape((-1, 4))
        p = np.asarray(p, dtype=float)
        row = frozen_features(p, packed, len(packed), law.knots, law.profile,
                               law.left, law.right, law.turn)
        parameters.append(p); paths.append(packed); rows.append(row)
    for p, path in zip(source['active_shape_samples'], source['active_prefix_samples']):
        add_frozen(p, path)
    signed = sorted(set(law.knots.tolist()+(-law.knots).tolist()))
    for a in law.knots:
        for u in sorted(set((a, 1.))):
            for c in signed:
                if c < -a:
                    continue
                for y in sorted(set((c, 0., law.right, law.negative_start_bound, 1.))):
                    if y < c:
                        continue
                    p = np.array([a, u, c, y])
                    seg, count = baseline_prefix(p, law.knots)
                    add_frozen(p, seg[:count])
    matrix = np.asarray(rows)
    logs = []
    print('INWARD_ATTACHED', dict(density_bins=law.n, old_variables=law.old_size,
        variables=law.size, initial_rows=len(rows)), flush=True)
    for outer in range(args.rounds):
        response_rows = np.c_[matrix, -np.ones(len(matrix))]
        inequalities = np.vstack((response_rows,
            np.c_[law.inequalities, np.zeros(len(law.inequalities))]))
        equality = np.c_[law.equalities, np.zeros(len(law.equalities))]
        rhs = np.zeros(len(equality)); rhs[0] = 1.
        solution = linprog(np.r_[np.zeros(law.size), 1.], A_ub=inequalities,
            b_ub=np.zeros(len(inequalities)), A_eq=equality, b_eq=rhs,
            bounds=law.bounds+[(None, None)], method='highs',
            options={'primal_feasibility_tolerance': 1e-9,
                     'dual_feasibility_tolerance': 1e-9})
        if not solution.success:
            raise RuntimeError(solution.message)
        variables = solution.x[:-1]
        solved_count = len(matrix)
        def objective(unit):
            p = unit_to_parameters(unit)
            return -float(optimal_features(p, law, variables)@variables)
        candidate_results = []
        result = differential_evolution(objective, [(0., 1.)]*4, maxiter=100,
            popsize=12, seed=542613+outer, tol=2e-8, polish=True)
        candidate_results.append((-float(result.fun), unit_to_parameters(result.x)))
        scores = matrix@variables
        for index in np.argsort(scores)[-36:]:
            result = minimize(objective, parameters_to_unit(parameters[index]),
                method='SLSQP', bounds=[(0., 1.)]*4,
                options={'maxiter': 110, 'ftol': 2e-11})
            candidate_results.append((-float(result.fun), unit_to_parameters(result.x)))
        # Search the y=c boundary separately, including the a≈1 terminal face.
        result = differential_evolution(lambda x: objective(np.r_[x, 0.]),
            [(0., 1.)]*3, maxiter=70, popsize=10, seed=642613+outer,
            tol=2e-8, polish=True)
        candidate_results.append((-float(result.fun), unit_to_parameters(np.r_[result.x, 0.])))
        best, maximizer = max(candidate_results, key=lambda item: item[0])
        structural = solution.ineqlin.marginals[solved_count:]
        log = dict(round=outer, objective=float(solution.fun), response=best,
            parameters=maximizer.tolist(), rows=solved_count,
            inward_mass=float(law.mass_row@variables[law.old_size:]),
            seconds=time.time()-started)
        logs.append(log); print('ROUND', log, flush=True)
        active = np.where(scores > solution.fun-2e-6)[0]
        h_description=('nondecreasing' if args.h_mode=='monotone'
                       else 'curvature-gated and corridor-gated')
        data = dict(scope='A normalized floating full signed-M3 law with an independent '
            +h_description+' uniform initial-inward density on the existing intervals. '
            'Negative-prefix arrangement is exact conditional on the coefficients; '
            'positive-prefix approximation and scalar separation are numerical. '
            'Not a certified game-value bound or a matching lower strategy.',
            source=args.seed, h_mode=args.h_mode, knots=law.knots.tolist(), affine_profile=law.profile.tolist(),
            left=law.left, right=law.right, turn=law.turn,
            negative_start_bound=law.negative_start_bound, endpoint_mass=float(variables[0]),
            densities={name:variables[1+j*law.n:1+(j+1)*law.n].tolist()
                       for j, name in enumerate(('f', 'g', 'k', 'ell'))},
            h=variables[law.old_size:].tolist(), inward=law.summary(variables),
            variables=variables.tolist(), objective=float(solution.fun), response=best,
            log=logs, active_shape_samples=[parameters[i].tolist() for i in active],
            active_prefix_samples=[paths[i].tolist() for i in active],
            response_dual_support=[dict(parameters=parameters[i].tolist(), prefix=paths[i].tolist(),
                weight=float(-dual)) for i, dual in enumerate(solution.ineqlin.marginals[:solved_count])
                if dual < -1e-10],
            structural_constraints=[dict(label=label, slack=float(-row@variables), multiplier=float(dual))
                for label, row, dual in zip(law.labels, law.inequalities, structural)],
            structural_equalities=[dict(label=label, residual=float(row@variables), multiplier=float(dual))
                for label, row, dual in zip(law.equality_labels[1:], law.equalities[1:], solution.eqlin.marginals[1:])],
            normalization_dual=float(solution.eqlin.marginals[0]),
            response_dual_mass=float(-solution.ineqlin.marginals[:solved_count].sum()),
            structural_dual_mass=float(abs(structural).sum()),
            stopping_rule=f'One additional path family on unchanged density coordinates, at most {args.rounds} response rounds.')
        (directory/args.output).write_text(json.dumps(data, indent=2))
        added = 0
        for value, p in candidate_results:
            if value > solution.fun+2e-8:
                row, packed = freeze_response(p, law, variables)
                parameters.append(p); paths.append(packed); rows.append(row)
                added += 1
        if not added:
            break
        matrix = np.asarray(rows)
    print('INWARD_SUMMARY', law.summary(variables), flush=True)
    print('NONZERO_CONSTRAINT_NORMALS', [(r['label'], r['multiplier'])
        for r in data['structural_constraints'] if abs(r['multiplier']) > 1e-9], flush=True)
    print('OUTPUT', str(directory/args.output), flush=True)


if __name__ == '__main__':
    main()
