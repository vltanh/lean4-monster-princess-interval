#!/usr/bin/env python3
"""Differential LP checks against exact chronological physical integration."""
from fractions import Fraction as Q
from pathlib import Path
import json
import tempfile

import numpy as np

from search import Master, Field, pack_field, supporting_plane, add_calendar, price_table
from hybrid_lp import HybridLP
from front_model import project
from test_record_lp import full_model
from test_continuous_record_hypographs import legal_test_fields, physical_routes, secant_perspective
from score_continuous_attack import leg_intervals


def secant_cost(field, route, count):
    """Exact evaluation without optimization, coefficients, or LP histories."""
    records = [Q(1), Q(1)]
    stopped = [route[0][1] == -1, route[0][1] == 1]
    value = loss_budget = Q(0)
    for first, last in zip(route, route[1:]):
        for a, b in leg_intervals(field, *first, *last):
            dt = b[0]-a[0]
            f0, f1 = field.cdf(*a), field.cdf(*b)
            for side in (0, 1):
                if stopped[side]:
                    continue
                q0, q1 = (f0, f1) if side == 0 else (1-f0, 1-f1)
                r = min(records[side], q0)
                if q1 < q0:
                    drop = q0-q1
                    v = secant_perspective(max(Q(0), r-q1), drop, count)
                    value += dt*(r-v/2)
                    loss_budget += dt*drop/(8*count**2)
                else:
                    value += dt*r
                records[side] = min(r, q1)
        stopped[0] |= last[1] == -1
        stopped[1] |= last[1] == 1
    return value, loss_budget


def run():
    counts = dict(fixed_field_lp_scores=0, exact_chronological_comparisons=0,
                  independent_full_node_lps=0, changed_field_scores=0,
                  endpoint_atom_fields=0, dynamic_appends=0, invalid_routes_rejected=0)
    rng = np.random.default_rng(2026111321)
    with tempfile.TemporaryDirectory() as folder:
        for n in (1, 2, 3):
            master = Master(n, Path(folder)/str(n), 10**8)
            routes = physical_routes()[::3]
            routes += [[(t, -x) for t, x in routes[-1]]]
            for field, atoms in legal_test_fields(n):
                counts['endpoint_atom_fields'] += atoms
                seed = master.repair([Q(field.gnum(j, k), field.den) for j, k in master.nodes])
                # Exact small denominators ensure the fixed table really is
                # this field, including initial endpoint atoms.
                field = Field(pack_field(master, seed), Q(1, 2))
                for route in routes:
                    master.columns = []
                    model = HybridLP(master, Q(0), 30., secants=4)
                    assert model.add_route(route) and not model.add_route(route)
                    _, objective, _, _ = model.solve(seed, Q(3), 0.)
                    expected, budget = secant_cost(field, route, 4)
                    exact = Q(supporting_plane(field, route)['value'])
                    assert abs(objective-float(expected)) < 2e-8, (n, route, objective, expected)
                    assert 0 <= exact-expected <= budget <= Q(len(route)-1, 16*n*4**2)
                    counts['fixed_field_lp_scores'] += 1
                    counts['exact_chronological_comparisons'] += 1
            for front in (False, True):
                master.columns = []
                master.seen = set()
                master.bank_model = 'calendars'
                seed = master.repair(rng.random(master.K))
                if front:
                    seed = project(n, seed)
                answer = price_table(master, seed, 4)
                paths = list({(p['start_grid'], tuple(p['moves'])): p
                              for p in answer['paths']}.values())[:3]
                floor = Q(int(answer['minimum_units']), 4*n*master.D)-Q(1, 1000)
                model = HybridLP(master, floor, 30., front=front, secants=4)
                planes = [supporting_plane(Field(pack_field(master, seed), Q(1, 2)), r) for r in routes[:2]]
                for p in planes:
                    model.add_plane(p)
                for path in paths:
                    add_calendar(master, path, seed)
                    assert not model.note_violation(path, 2)
                    assert model.note_violation(path, 2)
                    assert not model.note_violation(path, 2)
                for _ in range(2):
                    trial, objective, _, _ = model.solve(seed, Q(3), .03)
                    expected = full_model(master, model.promoted_paths, planes, seed, floor, .03, front)
                    assert abs(objective-expected) < 2e-7
                    counts['independent_full_node_lps'] += 1
                    route = routes[len(model.continuous_routes)]
                    assert model.add_route(route)
                    # Adding a route after field and record columns already
                    # exist exercises the noncontiguous append mappings.
                    _, objective, _, _ = model.solve(trial, Q(3), 0.)
                    field = Field(pack_field(master, trial), Q(1, 2))
                    expected = min(float(secant_cost(field, r, 4)[0]) for r in model.continuous_routes)
                    expected = min(expected, *(float(Q(p['constant'])+sum(Q(a)*Q(int(trial[j,k]), master.D)
                                                                   for j,k,a in p['coefficients'])) for p in planes))
                    assert abs(objective-expected) < 2e-7
                    counts['changed_field_scores'] += 1
                    counts['dynamic_appends'] += 1
                    saved = json.loads(json.dumps(model.checkpoint()))
                    restored = HybridLP(master, floor, 30., front=front, secants=4)
                    restored.restore(saved)
                    for p in planes:
                        restored.add_plane(p)
                    assert restored.checkpoint() == saved
                    _, again, _, _ = restored.solve(trial, Q(3), 0.)
                    assert abs(again-objective) < 2e-7
                    # Restore a model without continuous constraints for the
                    # next independent full-node comparison.
                    model = HybridLP(master, floor, 30., front=front, secants=4)
                    for p in planes:
                        model.add_plane(p)
                    for path in paths:
                        model.promote(path)
        model = HybridLP(master, Q(0))
        reports = [dict(route=r, value=str(v))
                   for r, v in zip(routes[:3], (Q(7,4), Q(5,4), Q(3,2)))]
        assert model.select_routes(reports) == 2
        assert set(model.continuous_routes) == {
            tuple(tuple(map(Q,p)) for p in reports[i]['route']) for i in (1,2)}
        assert model.select_routes(reports) == 0
        # A formerly inactive route can acquire its exact hypograph later.
        reports[0]['value'] = '1'
        assert model.select_routes(reports) == 1
        model = HybridLP(master, Q(0))
        invalid = [[], [(0, 0), (2, 1), (4, -1)], [(0, 0), (1, 1)],
                   [(0, 2), (3, -1), (5, 1)], [(1, 1), (3, -1)]]
        for route in invalid:
            before = len(model.pending), model.auxiliary_count, len(model.continuous_routes)
            try:
                model.add_route(route)
            except ValueError:
                pass
            else:
                raise AssertionError('invalid route accepted')
            assert before == (len(model.pending), model.auxiliary_count, len(model.continuous_routes))
            counts['invalid_routes_rejected'] += 1
    return dict(status='PASS', counts=counts, all_monster_security_claimed=False)


if __name__ == '__main__':
    print(json.dumps(run(), indent=2))
