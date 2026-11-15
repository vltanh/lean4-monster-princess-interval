"""Complete negative-prefix optimizer for an independently weighted I triangle.

The original k is a nondecreasing step function.  The added monster sheet
has density eta on D<a<1, -a<v<-D, without a tied change of k or ell.
For each negative V, the local score is convex or affine between k knots.
Shared monotone randomized rounding therefore reduces every inverse graph
to finitely many U levels.  Their score differences are affine in V;
pairwise crossings and ordered dynamic programming give the full optimum.

Floating discovery implementation of that exact finite-arrangement theorem.
No bound on the number of turns of the competing princess is assumed.
"""
import numpy as np
from numba import njit

from m3_attached_oracle import M3_RIGHT, M3_TURN
from localized_ramp_basis import D
from separated_oracle import value_at
from uniform_inward_prefix import primitive


@njit
def negative_blocks(parameters, knots, variables, eta):
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
    raw[0], raw[1] = a, cap
    nr = 2
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
    Kr = primitive(M3_TURN, knots, k)
    raw_cuts = np.empty(len(knots)+4)
    raw_cuts[0], raw_cuts[1] = lo, hi
    nc = 2
    for edge in (-M3_RIGHT, -D):
        if lo < edge < hi:
            raw_cuts[nc] = edge
            nc += 1
    for z in knots:
        if lo < -z < hi:
            raw_cuts[nc] = -z
            nc += 1
    raw_cuts = np.sort(raw_cuts[:nc])
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
        slope = np.zeros(nl)
        intercept = pv*levels-K
        if a > D and midpoint < -D:
            slope += 3.*eta*levels
            intercept += eta*((a+D-1.-c)*levels+levels*levels/2.)
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


if __name__ == '__main__':
    import json
    from pathlib import Path
    from negative_prefix_oracle import negative_cases, negative_feature_change
    data = json.loads(Path(__file__).with_name('negative_prefix_discovery.json').read_text())
    knots = np.asarray(data['knots'])
    variables = np.r_[data['endpoint_mass'], *(data['densities'][x] for x in ('f','g','k','ell'))]
    rng = np.random.default_rng(420386)
    maximum = 0.
    for i in range(160):
        a = rng.uniform(D, 1.) if i % 2 else rng.uniform(0., D)
        u = rng.uniform(a, 1.); c = rng.uniform(-a, 1.); y = rng.uniform(c, 1.)
        params = np.array([a,u,c,y])
        first, nf, second, ns = negative_cases(params, knots, variables)
        old = []
        if nf >= 0:
            old.append(negative_feature_change(params, first, nf, knots)@variables)
        if ns >= 0:
            old.append(negative_feature_change(params, second, ns, knots)@variables)
        blocks, nb = negative_blocks(params, knots, variables, 0.)
        actual = negative_feature_change(params, blocks, nb, knots)@variables
        error = abs(actual-max(old))
        assert error < 2e-12, (params, actual, old)
        maximum = max(maximum,error)
    print('PASS: 160 zero-I comparisons against independent PAVA; max error',maximum)
