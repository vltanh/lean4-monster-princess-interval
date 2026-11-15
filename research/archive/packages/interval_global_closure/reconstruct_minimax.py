#!/usr/bin/env python3
"""Reconstruct and verify exact fixed-bank certificates from discovery output.

Floating output only selects a small matrix basis. All accepted payoff,
normalization, complementary equality, and global cut checks use Fraction.
This certifies the supplied monster bank, not the unrestricted game value.
"""
from __future__ import annotations
import argparse
from fractions import Fraction as Q
import json
from pathlib import Path
import sys
import time

import numpy as np
from scipy.optimize import linprog
from sympy import Matrix, Rational

from survival_minimax import Minimax


def rational_solution(a, b):
    matrix = Matrix([[Rational(x.numerator, x.denominator) for x in row] for row in a])
    rhs = Matrix([Rational(x.numerator, x.denominator) for x in b])
    solution, parameters = matrix.gauss_jordan_solve(rhs)
    if parameters.rows:
        raise ValueError('Selected basis does not determine a unique rational solution')
    return [Q(int(x.p), int(x.q)) for x in solution]


def reconstruct(source, destination, skip_cut=False):
    started = time.monotonic()
    data = json.loads(Path(source).read_text())
    atoms = [dict(kind=a['kind'], parameters=tuple(map(Q,a['parameters']))) for a in data['atoms']]
    problem = Minimax(atoms)
    rows = []
    labels = []
    for entry in data['princess_mixture']:
        label = tuple(entry['labels'])
        values = tuple(problem.model.levels[k] for k in label)
        rows.append(problem.model.row(atoms, values))
        labels.append(label)
    matrix = np.array([[float(x) for x in row] for row in rows])
    # Reoptimize the small finite matrix solely to select basic support.
    result = linprog(np.r_[np.zeros(len(rows)), -1.],
                     A_ub=np.column_stack((-matrix.T, np.ones(len(atoms)))),
                     b_ub=np.zeros(len(atoms)),
                     A_eq=np.array([[1.]*len(rows)+[0.]]), b_eq=[1.],
                     bounds=[(0.,None)]*len(rows)+[(None,None)], method='highs',
                     options={'primal_feasibility_tolerance':1e-9,
                              'dual_feasibility_tolerance':1e-9})
    assert result.success, result.message
    selected_rows = np.flatnonzero(result.x[:-1] > 1e-8).tolist()
    selected_atoms = np.flatnonzero(-result.ineqlin.marginals > 1e-8).tolist()
    # All tight rows may be used; exact overdetermined solve rejects a bad basis.
    tight_atoms = np.flatnonzero(np.abs(matrix.T @ result.x[:-1] - result.x[-1]) < 1e-9).tolist()
    primal_a = [[rows[r][j] for r in selected_rows]+[Q(-1)] for j in tight_atoms]
    primal_a.append([Q(1)]*len(selected_rows)+[Q(0)])
    primal = rational_solution(primal_a, [Q(0)]*len(tight_atoms)+[Q(1)])
    q, value = primal[:-1], primal[-1]
    dual_a = [[rows[r][j] for j in selected_atoms]+[Q(-1)] for r in selected_rows]
    dual_a.append([Q(1)]*len(selected_atoms)+[Q(0)])
    dual = rational_solution(dual_a, [Q(0)]*len(selected_rows)+[Q(1)])
    w, upper = dual[:-1], dual[-1]
    assert value == upper
    assert all(x > 0 for x in q+w) and sum(q) == sum(w) == 1
    lower_payoffs = [sum(p*rows[r][j] for p,r in zip(q,selected_rows)) for j in range(len(atoms))]
    finite_upper_payoffs = [sum(p*rows[r][j] for p,j in zip(w,selected_atoms)) for r in range(len(rows))]
    assert min(lower_payoffs) == value and max(finite_upper_payoffs) == value
    if not skip_cut:
        full_weights = [Q(0)]*len(atoms)
        for j,p in zip(selected_atoms,w):
            full_weights[j]=p
        global_cut = problem.model.solve(full_weights, retain_face=True)
        assert global_cut.value == value, (global_cut.value, value)
    payload = dict(
        scope='Exact minimax for the supplied finite monster bank, against every princess path. '
              'The lower certificate covers only the bank, not arbitrary monsters.',
        source=Path(source).name,
        value=str(value), decimal_value=float(value),
        monster_pairs=[dict(index=j,**data['atoms'][j],weight=str(p)) for j,p in zip(selected_atoms,w)],
        princess_components=[dict(source_index=r,weight=str(p),labels=list(labels[r]))
                             for r,p in zip(selected_rows,q)],
        query_v=data['query_v'], event_labels=data['event_labels'],
        bank_size=len(atoms), all_bank_payoffs=list(map(str,lower_payoffs)),
        all_decomposed_response_payoffs=list(map(str,finite_upper_payoffs)),
        global_rational_cut_verified=not skip_cut,
        seconds=time.monotonic()-started)
    Path(destination).write_text(json.dumps(payload,indent=2)+'\n')
    print(json.dumps({k:payload[k] for k in ['value','decimal_value','bank_size',
                     'global_rational_cut_verified','seconds']},indent=2))
    print('supports',len(w),'monster pairs;',len(q),'princess components',flush=True)
    return payload


if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('source')
    parser.add_argument('destination')
    parser.add_argument('--skip-cut',action='store_true')
    args=parser.parse_args()
    reconstruct(args.source,args.destination,args.skip_cut)
