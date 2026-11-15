"""Ordered negative-prefix optimization without monotonicity of p=f+g.

This extends the fixed attached M3 geometry. It keeps k nondecreasing,
the nonnegative M3 edge, all residual conditions, and the old suffix
hypotheses. Only the monotonicity requirement on p is removed.

Negative inverse segments are constant blocks. Their optimum follows from
weighted pool-adjacent-violators and two cases at the small M3 start band.
The fixed-path feature correction is analytic. Scalar optimization and
density discovery remain numerical, not a game-value certificate.
"""
import numpy as np
from numba import njit

from m3_attached_oracle import (M3_LEFT, M3_RIGHT, M3_TURN, attached_prefix)
from m3_early_oracle import cumulative
from m3_face_features import general_face_features
from separated_oracle import bin_at, value_at


@njit
def ordinary_blocks(lo, hi, lower, upper, knots, p, k):
    """Maximize integral[p(-V)*phi-K(phi)] over ordered constant blocks."""
    result = np.zeros((2*len(knots)+4, 4))
    if hi <= lo:
        return result, 0
    cuts = np.empty(len(knots)+2)
    nc = 2
    cuts[0], cuts[1] = lo, hi
    for z in knots:
        if lo < -z < hi:
            cuts[nc] = -z
            nc += 1
    cuts = np.sort(cuts[:nc])
    # (left,right,total weight,weighted coefficient) for each PAVA block.
    stack = np.zeros((len(cuts), 4))
    ns = 0
    for j in range(len(cuts)-1):
        l, r = cuts[j], cuts[j+1]
        if r <= l:
            continue
        w = r-l
        stack[ns] = np.array([l, r, w, w*value_at(-(l+r)/2., knots, p)])
        ns += 1
        while ns > 1 and stack[ns-2, 3]*stack[ns-1, 2] > stack[ns-1, 3]*stack[ns-2, 2]:
            stack[ns-2, 1] = stack[ns-1, 1]
            stack[ns-2, 2] += stack[ns-1, 2]
            stack[ns-2, 3] += stack[ns-1, 3]
            ns -= 1
    count = 0
    for j in range(ns):
        target = stack[j, 3]/stack[j, 2]
        chosen = upper
        if value_at(lower, knots, k) >= target:
            chosen = lower
        else:
            for h in range(len(k)):
                if knots[h] >= lower and knots[h] <= upper and k[h] >= target:
                    chosen = knots[h]
                    break
        if count and abs(result[count-1, 3]-chosen) < 1e-13:
            result[count-1, 1] = stack[j, 1]
        else:
            result[count] = np.array([stack[j, 0], stack[j, 1], 0., chosen])
            count += 1
    return result, count


@njit
def negative_cases(parameters, knots, variables):
    """Return the two exhaustive ordered-prefix candidates for this geometry."""
    a, u, c, y = parameters
    n = len(knots)-1
    p = variables[1:1+n]+variables[1+n:1+2*n]
    k = variables[1+2*n:1+3*n]
    lo, hi = -a, min(c, 0.)
    first = np.zeros((2*len(knots)+4, 4))
    second = np.zeros_like(first)
    if hi <= lo:
        return first, 0, second, -1
    if hi <= -M3_RIGHT:
        first, nf = ordinary_blocks(lo, hi, a, u, knots, p, k)
        return first, nf, second, -1
    nf = -1
    if a <= M3_TURN:
        first, nf = ordinary_blocks(lo, hi, a, min(u, M3_TURN), knots, p, k)
    ns = -1
    if a >= M3_RIGHT and u >= M3_TURN:
        second, ns = ordinary_blocks(lo, min(hi, -M3_RIGHT), a, u, knots, p, k)
        start = max(lo, -M3_RIGHT)
        if hi > start:
            level = max(a, M3_TURN)
            if ns:
                level = max(level, second[ns-1, 3])
            if ns and abs(second[ns-1, 3]-level) < 1e-13:
                second[ns-1, 1] = hi
            else:
                second[ns] = np.array([start, hi, 0., level])
                ns += 1
    return first, nf, second, ns


@njit
def generator_change(r, lo, hi, a, old_u, negative, count):
    """Four-payoff change for a positive-M3 unit generator."""
    total = 0.
    for i in range(count):
        vl, vr, slope, level = negative[i]
        if slope != 0.:
            raise ValueError('Negative inverse pieces must be constant blocks')
        zl, zr = max(lo, -vr), min(hi, -vl)
        if zr > zl:
            total += (zr-zl)*(max(0., level-r)-max(0., old_u-r))
        # This alpha price is present only for positive monster starts z>a.
        total -= (vr-vl)*(cumulative(r, max(lo, a), hi, level, 1)
                          -cumulative(r, max(lo, a), hi, old_u, 1))
    return total


@njit
def negative_feature_change(parameters, negative, count, knots):
    """Exact feature difference from the old constant-negative-inverse path."""
    a, u, c, y = parameters
    n = len(knots)-1
    row = np.zeros(1+4*n)
    for i in range(count):
        vl, vr, slope, level = negative[i]
        if slope != 0.:
            raise ValueError('Negative inverse pieces must be constant blocks')
        width = vr-vl
        for j in range(n):
            lo, hi = knots[j], knots[j+1]
            overlap = max(0., min(hi, -vl)-max(lo, -vr))
            delta = overlap*(level-u)/4.
            row[1+j] += delta
            row[1+n+j] += delta
            tail_delta = max(0., hi-max(lo, level))-max(0., hi-max(lo, u))
            row[1+2*n+j] += width*tail_delta/4.
    edge_bin = bin_at(M3_TURN, knots)
    for j in range(n):
        lo, hi = max(M3_LEFT, knots[j]), min(M3_RIGHT, knots[j+1])
        if hi <= lo:
            continue
        factor = generator_change(M3_TURN, lo, hi, a, u, negative, count)/4.
        row[1+2*n+edge_bin] += factor
        row[1+j] -= factor
        row[1+n+j] -= factor
    for j in range(1, n):
        r = knots[j]
        if r <= M3_TURN+1e-13:
            continue
        factor = generator_change(r, M3_LEFT, M3_RIGHT, a, u, negative, count)/4.
        row[1+2*n+j] += factor
        row[1+2*n+j-1] -= factor
    return row


@njit
def general_features(parameters, packed, count, knots, profile, left, right,
                     s0, edge_trace=True):
    """Frozen rows accept negative blocks followed by positive affine pieces."""
    split = 0
    while split < count and packed[split, 0] < 0.:
        split += 1
    row = general_face_features(parameters, packed[split:count], count-split,
                                knots, profile, left, right, s0)
    if split:
        row += negative_feature_change(parameters, packed[:split], split, knots)
    return row


@njit
def optimal_features(parameters, knots, profile, variables, left, right,
                     s0, edge_trace=True):
    positive, npiece = attached_prefix(parameters, knots, variables, left, right, s0)
    base = general_face_features(parameters, positive, npiece, knots, profile, left, right, s0)
    first, nf, second, ns = negative_cases(parameters, knots, variables)
    best = base
    score = -np.inf
    if nf >= 0:
        best = base+negative_feature_change(parameters, first, nf, knots)
        score = best@variables
    if ns >= 0:
        other = base+negative_feature_change(parameters, second, ns, knots)
        if other@variables > score:
            best = other
    return best


def freeze_response(parameters, knots, profile, variables, left, right,
                    s0, edge_trace=True):
    positive, npiece = attached_prefix(parameters, knots, variables, left, right, s0)
    first, nf, second, ns = negative_cases(parameters, knots, variables)
    candidates = []
    if nf >= 0:
        candidates.append(first[:nf])
    if ns >= 0:
        candidates.append(second[:ns])
    negative = max(candidates, key=lambda rows: negative_feature_change(
        parameters, rows, len(rows), knots)@variables)
    packed = np.vstack((negative, positive[:npiece]))
    row = general_features(parameters, packed, len(packed), knots, profile, left, right, s0)
    return row, packed


def actual_princess(parameters, packed, epsilon):
    """Legal epsilon path for an arbitrary saved negative/positive prefix."""
    a, u, c, y = parameters
    points = [(a, -a)]
    def append(U, V):
        assert U >= points[-1][0]-1e-10 and V >= points[-1][1]-1e-10
        assert U >= V-1e-10 and U <= V+2.+1e-10
        if abs(U-points[-1][0])+abs(V-points[-1][1]) > 1e-12:
            points.append((U, V))
    if len(packed) == 0 or packed[0, 0] >= 0.:
        append(min(u, 1.-epsilon), -a)
        append(min(u, 1.-epsilon), min(c, 0.))
    for lo, hi, slope, intercept in packed:
        append(min(slope*lo+intercept, 1.-epsilon), lo)
        append(min(slope*hi+intercept, 1.-epsilon), hi)
    append(1.-epsilon, c)
    append(1.+epsilon, c)
    append(1.+epsilon, y)
    append(y+2., y)
    path = np.asarray([((U+V)/2., (U-V)/2.) for U, V in points]+[(6., 1.)])
    return path, points


def verify_capture():
    import json
    from pathlib import Path
    from m3_face_features import direct_density_capture
    data = json.loads(Path(__file__).with_name('m3_attached_settled.json').read_text())
    knots = np.asarray(data['knots'])
    variables = np.r_[data['endpoint_mass'], *(data['densities'][x] for x in ('f', 'g', 'k', 'ell'))]
    profile = np.asarray(data['affine_profile'])
    left, right, s0 = data['left'], data['right'], data['turn']
    cases = [
        (np.array([.7, .9, -.1, .8]), np.array([[-.7, -.4, 0., .72], [-.4, -.1, 0., .85]])),
        (np.array([.08, .8, .3, .8]), np.array([[-.08, -.04, 0., .13], [-.04, 0., 0., .2], [0., .3, 0., .8]])),
        (np.array([.2, .8, .3, .8]), np.array([[-.2, -.15, 0., .21], [-.15, -.08, 0., .26], [-.08, 0., 0., .7], [0., .3, 0., .8]])),
    ]
    errors = []
    for parameters, packed in cases:
        predicted = general_features(parameters, packed, len(packed), knots, profile, left, right, s0)@variables
        actual = []
        for epsilon in (2e-5, 1e-5):
            path, uv = actual_princess(parameters, packed, epsilon)
            actual.append(direct_density_capture(path, uv, variables, knots, profile, left, right, s0))
        error = abs(2.*actual[1]-actual[0]-predicted)
        assert error < 3e-8, (parameters, predicted, actual, error)
        errors.append(error)
        print('GENERAL_NEGATIVE_PREFIX_CAPTURE', parameters.tolist(), 'error', error, flush=True)
    print('PASS: 3 independent whole-law negative-prefix capture limits; maximum error', max(errors))


if __name__ == '__main__':
    verify_capture()
