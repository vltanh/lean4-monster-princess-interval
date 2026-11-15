"""Complete ordered negative-prefix oracle for uniform initial-inward sheets.

The new inward density is i(a,v)=h(a), -a<v<a, with nonnegative
nondecreasing step h. Existing signed-M3 geometry and all its physical
conditions are retained. This module optimizes the negative inverse;
the actual added-density capture feature is defined independently.

On each negative-V density cell, the score of every allowed inverse
level is affine in V. Its U dependence is piecewise affine, except for
a low-start region where the verified turn-floor cap removes the curved
alpha term. A complete pairwise-crossing arrangement followed by ordered
dynamic programming therefore suffices, without a monotonicity rule on p.
"""
import numpy as np
from numba import njit

from m3_attached_oracle import M3_RIGHT, M3_TURN
from separated_oracle import value_at


@njit
def primitive(x, knots, values):
    total = 0.
    for i in range(len(values)):
        total += max(0., min(x, knots[i+1])-knots[i])*values[i]
    return total


@njit
def negative_blocks(parameters, knots, variables, h):
    a, u, c, y = parameters
    n = len(knots)-1
    p = variables[1:1+n]+variables[1+n:1+2*n]
    k = variables[1+2*n:1+3*n]
    lo, hi = -a, min(c, 0.)
    output = np.zeros((len(knots)+3, 4))
    if hi <= lo:
        return output, 0
    cap = min(u, M3_TURN) if a < M3_RIGHT else u
    raw = np.empty(len(knots)+3)
    nr = 2
    raw[0], raw[1] = a, cap
    if a < M3_TURN < cap:
        raw[nr] = M3_TURN
        nr += 1
    for z in knots:
        if a < z < cap:
            raw[nr] = z
            nr += 1
    raw = np.sort(raw[:nr])
    levels = np.empty(nr)
    nl = 0
    for z in raw:
        if nl == 0 or z > levels[nl-1]+1e-14:
            levels[nl] = z
            nl += 1
    levels = levels[:nl]
    K = np.array([primitive(z, knots, k) for z in levels])
    H = np.array([primitive(z, knots, h) for z in levels])
    Ha = primitive(a, knots, h)
    Kr = primitive(M3_TURN, knots, k)
    raw_cuts = np.empty(len(knots)+3)
    nc = 2
    raw_cuts[0], raw_cuts[1] = lo, hi
    if lo < -M3_RIGHT < hi:
        raw_cuts[nc] = -M3_RIGHT
        nc += 1
    for z in knots:
        if lo < -z < hi:
            raw_cuts[nc] = -z
            nc += 1
    raw_cuts = np.sort(raw_cuts[:nc])
    # At most one crossing for every level pair in each density cell.
    maximum = (nc-1)*(nl*(nl-1)//2+2)
    bounds = np.zeros((maximum, 2))
    score = np.zeros((maximum, nl))
    count = 0
    for cell in range(nc-1):
        l, r = raw_cuts[cell], raw_cuts[cell+1]
        if r <= l:
            continue
        midpoint = (l+r)/2.
        pv = value_at(-midpoint, knots, p)
        hv = value_at(-midpoint, knots, h)
        j_intercept = Ha-primitive(-midpoint, knots, h)-hv*midpoint
        slope = hv*levels+2.*H
        intercept = (pv+j_intercept)*levels-K-(1.+c)*H
        if midpoint >= -M3_RIGHT:
            for state in range(nl):
                if levels[state] > M3_TURN:
                    intercept[state] += K[state]-Kr-pv*(levels[state]-M3_TURN)
        cuts = np.empty(nl*(nl-1)//2+2)
        cuts[0], cuts[1] = l, r
        ncut = 2
        for i in range(nl):
            for j in range(i+1, nl):
                denominator = slope[i]-slope[j]
                if abs(denominator) > 1e-15:
                    crossing = (intercept[j]-intercept[i])/denominator
                    if l < crossing < r:
                        cuts[ncut] = crossing
                        ncut += 1
        cuts = np.sort(cuts[:ncut])
        for j in range(ncut-1):
            vl, vr = cuts[j], cuts[j+1]
            if vr <= vl:
                continue
            bounds[count] = np.array([vl, vr])
            score[count] = (vr-vl)*(intercept+slope*(vl+vr)/2.)
            count += 1
    parent = np.zeros((count, nl), dtype=np.int64)
    previous = np.zeros(nl)
    for interval in range(count):
        current = np.empty(nl)
        best = 0
        for state in range(nl):
            if previous[state] > previous[best]:
                best = state
            current[state] = previous[best]+score[interval, state]
            parent[interval, state] = best
        previous = current
    state = int(np.argmax(previous))
    chosen = np.zeros(count, dtype=np.int64)
    for interval in range(count-1, -1, -1):
        chosen[interval] = state
        state = parent[interval, state]
    nout = 0
    for interval in range(count):
        level = levels[chosen[interval]]
        if nout and abs(output[nout-1, 3]-level) < 1e-13:
            output[nout-1, 1] = bounds[interval, 1]
        else:
            output[nout] = np.array([bounds[interval, 0], bounds[interval, 1], 0., level])
            nout += 1
    return output, nout


def verify_zero_component():
    import json
    from pathlib import Path
    from negative_prefix_oracle import negative_cases, negative_feature_change
    data = json.loads(Path(__file__).with_name('negative_prefix_discovery.json').read_text())
    knots = np.asarray(data['knots'])
    variables = np.r_[data['endpoint_mass'], *(data['densities'][x] for x in ('f', 'g', 'k', 'ell'))]
    rng = np.random.default_rng(83245)
    maximum = 0.
    for _ in range(120):
        a = rng.uniform(0., 1.); u = rng.uniform(a, 1.)
        c = rng.uniform(-a, 1.); y = rng.uniform(c, 1.)
        parameters = np.array([a, u, c, y])
        first, nf, second, ns = negative_cases(parameters, knots, variables)
        scores = []
        if nf >= 0:
            scores.append(negative_feature_change(parameters, first, nf, knots)@variables)
        if ns >= 0:
            scores.append(negative_feature_change(parameters, second, ns, knots)@variables)
        arranged, na = negative_blocks(parameters, knots, variables, np.zeros(len(knots)-1))
        value = negative_feature_change(parameters, arranged, na, knots)@variables
        error = abs(value-max(scores))
        assert error < 2e-12, (parameters, value, scores, error)
        maximum = max(maximum, error)
    print('PASS: 120 independent arrangement-DP versus PAVA prefix comparisons; max error', maximum)


if __name__ == '__main__':
    verify_zero_component()
