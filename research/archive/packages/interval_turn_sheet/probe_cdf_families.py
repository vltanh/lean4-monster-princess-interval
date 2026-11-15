#!/usr/bin/env python3
"""Continuous attacks in full signed two-turn and center-wait families.

The three monster parameters cover both signs of start, a first turn
before the center, and a second turn on either half.  No turn-count
theorem or certified global numerical minimum is asserted.  Every result
is a legal route evaluated on the entire supplied continuous CDF.
"""
import argparse
import json
from pathlib import Path
import time

import numpy as np
from scipy.optimize import LinearConstraint, minimize

from probe_cdf_field import Field


def m3(parameters):
    x, s, t = map(float, parameters)
    return [[0., x], [(s-x)/2, (s+x)/2], [(s+t)/2, (s-t)/2],
            [t+1, 1.], [t+3, -1.]]


def waiting(parameters, final_sign):
    s, t, e = map(float, parameters)
    return [[0., 0.], [s, 0.], [(s+t)/2, (t-s)/2], [t, 0.],
            [(t+e)/2, -(e-t)/2], [e, 0.],
            [e+1, float(final_sign)], [e+3, float(-final_sign)]]


def search(field, seconds=45., include_waits=True):
    began = time.monotonic()
    best = field.payoff([[0., 1.], [2., -1.]])
    history = []
    class Cap(Exception):
        pass
    families = []
    # x<=s<=2-x and -x<=t<=s+2 are exactly the route's spatial
    # and chronological conditions, without a hidden center-crossing rule.
    mat = np.array([[-1., 1., 0.], [1., 1., 0.],
                    [1., 0., 1.], [0., -1., 1.]])
    lo = np.array([0., -np.inf, 0., -np.inf])
    hi = np.array([np.inf, 2., np.inf, 2.])
    seeds = []
    for x in [.125, .5, .875, .95]:
        for s, t in [(.9375, -.5*x), (1.03125, .5*x), (1., .75)]:
            if s >= x and s+x < 2:
                seeds.append([x, s, t])
    for x in [-.125, -.5, -.875, -.95]:
        for ratio in [.25, .75]:
            seeds.append([x, x*(1-2*ratio), 1.])
    seeds += [[.05, .3, 1.], [.2, .7, 1.], [-.1, .4, 1.], [.5, .9, 1.]]
    families.append(('full_signed_M3', m3, seeds, mat, lo, hi,
                     [(-1., 1.), (-1., 3.), (-1., 5.)]))
    if include_waits:
        matw = np.array([[-1., 1., 0.], [0., -1., 1.]])
        low = np.array([0., 0.]); high = np.array([np.inf, np.inf])
        seedw = [[s, t, 1.] for s, t in
                 [(.125, .5), (.25, .625), (.5, .5625), (.5, .75), (.5, .9375)]]
        for sign in [-1, 1]:
            families.append((f'center_wait_two_returns_{sign}',
                             lambda p, sign=sign: waiting(p, sign),
                             seedw, matw, low, high, [(0., .5), (0., 1.), (1., 1.)]))
    for label, build, seeds, matrix, lower, upper, bounds in families:
        for seed in seeds:
            if time.monotonic()-began >= seconds:
                return dict(best=best, history=history, seconds=time.monotonic()-began,
                            complete_seed_list=False)
            calls = 0
            local_best = None
            def objective(parameters):
                nonlocal best, calls, local_best
                calls += 1
                if time.monotonic()-began >= seconds:
                    raise Cap
                image = matrix @ parameters
                violation = (np.maximum(lower-image, 0).sum()
                             + np.maximum(image-upper, 0).sum())
                if violation > 2e-10:
                    return 10.+100.*float(violation)
                route = build(parameters)
                # Only roundoff at an exactly constrained endpoint may be
                # projected. Larger violations are rejected above.
                route = [[t, float(np.clip(x, -1., 1.))] for t, x in route]
                result = field.payoff(route)
                if local_best is None or result['value'] < local_best['value']:
                    local_best = dict(result, parameters=list(map(float, parameters)))
                if result['value'] < best['value']:
                    best = dict(result, family=label, parameters=list(map(float, parameters)))
                return result['value']
            try:
                result = minimize(objective, seed, method='SLSQP', bounds=bounds,
                                  constraints=[LinearConstraint(matrix, lower, upper)],
                                  options=dict(maxiter=100, ftol=5e-12))
                status = str(result.message)
            except Cap:
                status = 'wall-time cap'
            history.append(dict(family=label, seed=seed, calls=calls,
                                status=status, best=local_best))
    return dict(best=best, history=history, seconds=time.monotonic()-began,
                complete_seed_list=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', type=Path)
    parser.add_argument('--seconds', type=float, default=45.)
    parser.add_argument('--no-waits', action='store_true')
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    field = Field(json.loads(args.input.read_text()))
    if field.cone_violation > 2e-7:
        raise ValueError(f'Field transport slope violation {field.cone_violation}')
    result = search(field, args.seconds, not args.no_waits)
    output = dict(scope='Heuristic continuous family separation on the entire field; no exhaustive response or game-value claim.',
                  input=str(args.input), field_response=result.pop('best'), **result)
    if args.output:
        args.output.write_text(json.dumps(output, indent=2)+'\n')
    print(json.dumps(output, indent=2))


if __name__ == '__main__':
    main()
