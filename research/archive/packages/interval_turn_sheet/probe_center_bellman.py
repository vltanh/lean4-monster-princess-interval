#!/usr/bin/env python3
"""Continuous monster-response search over the complete ordinary-wave reduction.

This is a response-discovery oracle, not a certified numerical optimizer.
The searched structural class is exhaustive for a piecewise-affine RankLaw;
the differential-evolution minimizations can still miss its true minimum.
No princess quantile rows, capture matrix, or law discretization is formed.
"""
import argparse
import json
from pathlib import Path
import sys
import time

import numpy as np
from scipy.optimize import differential_evolution, minimize

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT/'packages/interval_continuous_rank'))
from continuous_rank import RankLaw
from center_bellman import (CenterActions, append_sweep, append_terminal_triangle,
                            append_triangle, append_wait, center_prefix_route,
                            endpoint_prefix_route)


def load_law(path):
    if path is None:
        data = dict(q=[0, .4, 1], a=[.1, .45, .7],
                    u=[.2, .7, 1.2], c=[.95, .3, -.6])
    else:
        data = json.loads(Path(path).read_text())
        if 'history' in data:
            data = data['history'][-1]
        if 'law' in data:
            data = data['law']
    law = RankLaw(data['q'], data['a'], data['u'], data.get('c', data.get('C')),
                  data.get('endpoint_mass', 0), exact=False)
    return law


class ResponseProbe:
    def __init__(self, law):
        self.law = law
        self.action = CenterActions(law)
        self.tau = float(self.action.tau)
        # One unbalanced triangle and at most one balanced triangle per fixed
        # incoming-density breakpoint. The crossing-tau triangle is terminal.
        self.complete_early_triangles = len(self.action.density_breakpoints())+1

    @staticmethod
    def _clip(x):
        return np.clip(np.asarray(x, dtype=float), 0, 1)

    def early(self, x, count, terminal, *, route_only=False):
        x = self._clip(x)
        b = self.tau*x[0]
        z = b*x[1]
        v = z*(2*x[2]-1)
        route = center_prefix_route(z, v, b)
        partial = self.law.payoff(route, require_complete=False)
        value = float(partial.value-b*partial.survival)
        # Earlier zero contacts at degenerate parameter boundaries are already
        # included by the direct prefix record integration.
        m = float(np.clip(2*(1-partial.survival)-self.law.B(b), self.law.B(b), 1))
        times = b+(self.tau-b)*np.sort(x[3:3+2*count+1])
        current = b
        for index in range(count):
            start, end = times[2*index:2*index+2]
            value += self.action.wait(current, start, m)
            m = max(m, self.law.B(start))
            value += self.action.triangle(start, end, m)
            append_triangle(route, start, end)
            m = max(m, self.law.B(end))
            current = end
        start = times[-1]
        value += self.action.wait(current, start, m)
        m = max(m, self.law.B(start))
        if terminal == 'sweep':
            value += self.action.sweep(start, m)
            append_sweep(route, start)
        else:
            end = self.tau+(2-self.tau)*x[-1]
            if end-start >= 2:
                value += self.action.sweep(start, m)
                append_sweep(route, start)
            else:
                value += self.action.terminal_triangle(start, end, m)
                append_terminal_triangle(route, self.action, start, end, m)
        return route if route_only else float(value)

    def late(self, x, *, route_only=False):
        x = self._clip(x)
        z = x[0]
        v = z*(2*x[1]-1)
        lower = max(z, self.tau)
        b = lower+(v+2-lower)*x[2]
        prefix = center_prefix_route(z, v, b)
        routes = [prefix+[(b+1, first), (b+3, -first)] for first in [-1, 1]]
        costs = [float(self.law.payoff(route).value) for route in routes]
        winner = int(np.argmin(costs))
        return routes[winner] if route_only else costs[winner]

    def endpoint(self, x, *, route_only=False):
        x = self._clip(x)
        z = x[0]
        v = z*(2*x[1]-1)
        b = z+(v+2-z)*x[2]
        w = v+(b-v)*x[3]
        route = endpoint_prefix_route(z, v, b, w)
        return route if route_only else float(self.law.payoff(route).value)

    def optimize(self, *, iterations=80, population=7, seed=1729, triangle_cap=None,
                 callback=None):
        cap = self.complete_early_triangles if triangle_cap is None else triangle_cap
        if cap < 0:
            raise ValueError('triangle_cap must be nonnegative')
        charts = [('first_endpoint', 4, self.endpoint),
                  ('late_first_center', 3, self.late)]
        if self.tau > 0:
            for count in range(cap+1):
                for terminal in ['sweep', 'triangle']:
                    dimension = 4+2*count+(terminal == 'triangle')
                    def function(x, route_only=False, count=count, terminal=terminal):
                        return self.early(x, count, terminal, route_only=route_only)
                    charts.append((f'early_{count}_{terminal}', dimension, function))
        results = []
        for chart_index, (name, dimension, function) in enumerate(charts):
            started = time.monotonic()
            result = differential_evolution(function, [(0, 1)]*dimension,
                                            maxiter=iterations, popsize=population,
                                            rng=seed+chart_index, polish=False,
                                            tol=1e-9, atol=1e-10)
            polished = minimize(function, result.x, method='Powell',
                                bounds=[(0, 1)]*dimension,
                                options=dict(maxiter=200, xtol=1e-10, ftol=1e-10))
            point = polished.x if polished.fun < result.fun else result.x
            predicted = float(function(point))
            route = function(point, route_only=True)
            direct = float(self.law.payoff(route).value)
            error = abs(predicted-direct)
            if error > 2e-8:
                raise ArithmeticError(f'{name}: action/direct mismatch {error}')
            item = dict(chart=name, value=direct, formula_value=predicted,
                        formula_direct_error=error, parameters=point.tolist(),
                        route=[[float(t), float(x)] for t, x in route],
                        seconds=time.monotonic()-started,
                        de_success=bool(result.success), evaluations=int(result.nfev),
                        polish_success=bool(polished.success))
            results.append(item)
            if callback is not None:
                callback(item)
        results.sort(key=lambda item: item['value'])
        return dict(
            scope='Continuous response discovery; optimization is not a certified global minimum.',
            structural_class_complete=cap >= self.complete_early_triangles,
            completeness_reason='Fixed piecewise-constant incoming-density partition; center Bellman reduction.',
            center_peak=self.tau,
            incoming_density_breakpoints=[float(x) for x in self.action.density_breakpoints()],
            exhaustive_early_triangle_count=self.complete_early_triangles,
            searched_early_triangle_count=cap,
            best=results[0], charts=results)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--law', help='JSON with q,a,u,c, optionally nested under law/history')
    parser.add_argument('--output', help='Write full response data to this JSON file')
    parser.add_argument('--iterations', type=int, default=80)
    parser.add_argument('--population', type=int, default=7)
    parser.add_argument('--seed', type=int, default=1729)
    parser.add_argument('--triangle-cap', type=int,
                        help='Optional incomplete exploratory cap; reported explicitly in output')
    args = parser.parse_args()
    law = load_law(args.law)
    probe = ResponseProbe(law)
    print(f'center peak: {probe.tau:.12g}; complete early-triangle count: '
          f'{probe.complete_early_triangles}', flush=True)
    result = probe.optimize(iterations=args.iterations, population=args.population,
                            seed=args.seed, triangle_cap=args.triangle_cap,
                            callback=lambda item: print(
                                f"{item['chart']}: {item['value']:.12g}; "
                                f"direct residual {item['formula_direct_error']:.3g}; "
                                f"{item['seconds']:.1f}s", flush=True))
    result['law'] = {key: [float(x) for x in getattr(law, key)]
                     for key in ['q', 'a', 'u', 'c']}
    if args.output:
        Path(args.output).write_text(json.dumps(result, indent=2)+'\n')
    print(f"best response: {result['best']['chart']} at {result['best']['value']:.12g}")
    print(f"complete structural family searched: {result['structural_class_complete']}")
    print('No certified global minimum or game-value conclusion follows from this optimizer.')


if __name__ == '__main__':
    main()
