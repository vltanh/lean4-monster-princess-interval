"""Discovery probability master for immutable physical Princess rows.

Every matrix coefficient is an exact limiting first-capture cost, rounded only
at the LP boundary. Results are discovery data, never unrestricted certificates.
"""
from pathlib import Path
from fractions import Fraction
import json
import time
import numpy as np
from scipy.optimize import linprog

HERE = Path(__file__).resolve().parent

def matrix_from_snapshot(snapshot):
    values = np.asarray([float(Fraction(v)) for v in snapshot['exact_matrix']['values']])
    return values[np.asarray(snapshot['exact_matrix']['indices'], dtype=int)]

def solve_master(A):
    started = time.perf_counter()
    rows, columns = A.shape
    result = linprog(-np.ones(columns), A_ub=A, b_ub=np.ones(rows),
                     bounds=(0, None), method='highs-ds',
                     options={'primal_feasibility_tolerance':1e-9,
                              'dual_feasibility_tolerance':1e-9})
    if not result.success:
        raise RuntimeError(result.message)
    raw_monster = result.x
    raw_princess = -result.ineqlin.marginals
    if min(raw_monster.min(), raw_princess.min()) < -1e-9:
        raise ArithmeticError('LP returned a materially negative weight')
    repair = {'monster_negative_count':int(np.count_nonzero(raw_monster<0)),
              'princess_negative_count':int(np.count_nonzero(raw_princess<0)),
              'monster_removed_negative_mass':float(-np.minimum(raw_monster,0).sum()),
              'princess_removed_negative_mass':float(-np.minimum(raw_princess,0).sum())}
    monster = np.maximum(raw_monster,0)
    total = monster.sum()
    monster /= total
    princess = np.maximum(raw_princess,0)
    princess /= princess.sum()
    row_payoffs = A @ monster
    column_payoffs = princess @ A
    report = {
        'rows': rows, 'columns': columns,
        'packing_value': 1 / total,
        'minimum_column_payoff': float(column_payoffs.min()),
        'maximum_row_payoff': float(row_payoffs.max()),
        'duality_gap': float(row_payoffs.max()-column_payoffs.min()),
        'monster_support': int(np.count_nonzero(monster > 1e-10)),
        'princess_support': int(np.count_nonzero(princess > 1e-10)),
        'iterations': result.nit, 'seconds': time.perf_counter()-started,
        'nonnegative_probability_repair':repair,
    }
    if min(monster.min(), princess.min()) < -1e-9 or report['duality_gap'] > 1e-7:
        raise ArithmeticError(report)
    return {'report': report, 'monster_weights': monster.tolist(),
            'princess_weights': princess.tolist(),
            'row_payoffs': row_payoffs.tolist(), 'column_payoffs': column_payoffs.tolist()}

if __name__ == '__main__':
    snapshot = json.loads((HERE/'frozen159_initial_matrix.json').read_text())
    output = solve_master(matrix_from_snapshot(snapshot))
    (HERE/'frozen159_master_initial.json').write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps(output['report'],indent=2))
