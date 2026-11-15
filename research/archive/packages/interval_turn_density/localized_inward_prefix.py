"""Complete negative-prefix response to the localized I plus k-ramp column.

For initial a<=D the localized sheet adds no variable prefix score, so
ordinary pooling uses k0+eta*(U-D)_+. For a>D the coupled score is concave
in U. Independent optimal superlevel tails nest, and a finite affine
arrangement in U reconstructs the entire maximizing inverse graph.
"""
import numpy as np
from numba import njit

from m3_attached_oracle import M3_RIGHT, M3_TURN
from localized_ramp_basis import D
from separated_oracle import value_at


@njit
def ramp_inverse(target, lower, upper, knots, k, eta):
    for j in range(len(k)):
        lo, hi = max(lower, knots[j]), min(upper, knots[j+1])
        if hi < lo:
            continue
        if k[j]+eta*max(0., lo-D) >= target:
            return lo
        if eta > 0.:
            root = D+(target-k[j])/eta
            if max(lo, D) <= root <= hi:
                return root
    return upper


@njit
def ordinary_blocks(lo, hi, lower, upper, knots, p, k, eta):
    output = np.zeros((2*len(knots)+4, 4))
    if hi <= lo:
        return output, 0
    cuts = np.empty(len(knots)+2)
    cuts[0], cuts[1] = lo, hi
    nc = 2
    for z in knots:
        if lo < -z < hi:
            cuts[nc] = -z
            nc += 1
    cuts = np.sort(cuts[:nc])
    stack = np.zeros((len(cuts), 4))
    ns = 0
    for j in range(nc-1):
        l, r = cuts[j], cuts[j+1]
        if r <= l:
            continue
        width = r-l
        stack[ns] = np.array([l, r, width, width*value_at(-(l+r)/2., knots, p)])
        ns += 1
        while ns > 1 and stack[ns-2, 3]*stack[ns-1, 2] > stack[ns-1, 3]*stack[ns-2, 2]:
            stack[ns-2, 1] = stack[ns-1, 1]
            stack[ns-2, 2] += stack[ns-1, 2]
            stack[ns-2, 3] += stack[ns-1, 3]
            ns -= 1
    count = 0
    for j in range(ns):
        chosen = ramp_inverse(stack[j, 3]/stack[j, 2], lower, upper, knots, k, eta)
        if count and abs(output[count-1, 3]-chosen) < 1e-13:
            output[count-1, 1] = stack[j, 1]
        else:
            output[count] = np.array([stack[j, 0], stack[j, 1], 0., chosen])
            count += 1
    return output, count


@njit
def gain_coefficients(cut, end, a, c, height, knots, p, eta):
    """Tail integral of q_U(V,U)=slope*U+intercept on one k0 bin."""
    slope, intercept = 0., 0.
    for j in range(len(p)):
        lo, hi = max(cut, -knots[j+1]), min(end, -knots[j])
        if hi <= lo:
            continue
        left_end = min(hi, -D)
        if left_end > lo:
            intercept += ((p[j]-height+eta*(a+2.*D-1.-c))*(left_end-lo)
                          +1.5*eta*(left_end*left_end-lo*lo))
        right_start, right_end = max(lo, -D), min(hi, -M3_RIGHT)
        if right_end > right_start:
            width = right_end-right_start
            slope -= eta*width
            intercept += (p[j]-height+eta*D)*width
    return slope, intercept


@njit
def high_start_blocks(parameters, knots, p, k, eta):
    a, u, c, y = parameters
    lo, hi = -a, min(c, 0.)
    if hi <= lo or u <= a:
        output = np.zeros((1, 4))
        if hi > lo:
            output[0] = np.array([lo, hi, 0., a])
            return output, 1
        return output, 0
    ucuts = np.empty(len(knots)+2)
    ucuts[0], ucuts[1] = a, u
    nu = 2
    for U in knots:
        if a < U < u:
            ucuts[nu] = U
            nu += 1
    ucuts = np.sort(ucuts[:nu])
    capacity = (nu-1)*(2*len(knots)+5)**2
    thresholds = np.zeros((capacity, 3))
    nth = 0
    for ubin in range(nu-1):
        ul, ur = ucuts[ubin], ucuts[ubin+1]
        if ur <= ul:
            continue
        height = value_at((ul+ur)/2., knots, k)
        cuts = np.empty(2*len(knots)+5)
        cuts[0], cuts[1] = lo, hi
        nc = 2
        for V in (-D, -M3_RIGHT):
            if lo < V < hi:
                cuts[nc] = V
                nc += 1
        for j in range(len(p)):
            V = -knots[j]
            if lo < V < hi:
                cuts[nc] = V
                nc += 1
            if eta > 0.:
                root = (height-p[j]-eta*(a+2.*D-1.-c))/(3.*eta)
                if max(lo, -knots[j+1]) < root < min(hi, -D, -knots[j]):
                    cuts[nc] = root
                    nc += 1
        cuts = np.sort(cuts[:nc])
        # Repeated cell boundaries have the same tail function.
        unique = np.empty(nc)
        nv = 0
        for V in cuts:
            if nv == 0 or V > unique[nv-1]+1e-14:
                unique[nv] = V
                nv += 1
        cuts = unique[:nv]
        slopes, intercepts = np.zeros(nv), np.zeros(nv)
        for j in range(nv):
            slopes[j], intercepts[j] = gain_coefficients(cuts[j], hi, a, c,
                                                         height, knots, p, eta)
        switches = np.empty(nv*(nv-1)//2+2)
        switches[0], switches[1] = ul, ur
        ns = 2
        for i in range(nv):
            for j in range(i+1, nv):
                den = slopes[i]-slopes[j]
                if abs(den) > 1e-16:
                    crossing = (intercepts[j]-intercepts[i])/den
                    if ul < crossing < ur:
                        switches[ns] = crossing
                        ns += 1
        switches = np.sort(switches[:ns])
        for j in range(ns-1):
            l, r = switches[j], switches[j+1]
            if r <= l:
                continue
            mid = (l+r)/2.
            index = 0
            best = slopes[0]*mid+intercepts[0]
            for h in range(1, nv):
                value = slopes[h]*mid+intercepts[h]
                if value > best+2e-15:
                    index, best = h, value
            threshold = cuts[index]
            if nth and threshold < thresholds[nth-1, 0]-2e-10:
                raise ValueError('Optimal superlevel tails did not nest')
            if nth and abs(threshold-thresholds[nth-1, 0]) < 2e-12:
                thresholds[nth-1, 2] = r
            else:
                thresholds[nth] = np.array([threshold, l, r])
                nth += 1
    output = np.zeros((nth+1, 4))
    start, level, count = lo, a, 0
    for i in range(nth):
        threshold, l, r = thresholds[i]
        threshold = min(hi, max(lo, threshold))
        if threshold > start:
            output[count] = np.array([start, threshold, 0., level])
            count += 1
            start = threshold
        level = r
    if start < hi:
        output[count] = np.array([start, hi, 0., level])
        count += 1
    return output, count


@njit
def negative_cases(parameters, knots, variables, eta):
    a, u, c, y = parameters
    n = len(knots)-1
    p = variables[1:1+n]+variables[1+n:1+2*n]
    k = variables[1+2*n:1+3*n]
    empty = np.zeros((2*len(knots)+4, 4))
    if a > D:
        first, nf = high_start_blocks(parameters, knots, p, k, eta)
        return first, nf, empty, -1
    lo, hi = -a, min(c, 0.)
    if hi <= lo:
        return empty, 0, empty, -1
    if hi <= -M3_RIGHT:
        first, nf = ordinary_blocks(lo, hi, a, u, knots, p, k, eta)
        return first, nf, empty, -1
    first, second = empty.copy(), empty.copy()
    nf, ns = -1, -1
    if a <= M3_TURN:
        first, nf = ordinary_blocks(lo, hi, a, min(u, M3_TURN), knots, p, k, eta)
    if a >= M3_RIGHT and u >= M3_TURN:
        second, ns = ordinary_blocks(lo, min(hi, -M3_RIGHT), a, u, knots, p, k, eta)
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


def verify_zero_component():
    import json
    from pathlib import Path
    from negative_prefix_oracle import negative_cases as previous_cases, negative_feature_change
    data = json.loads(Path(__file__).with_name('negative_prefix_discovery.json').read_text())
    knots = np.asarray(data['knots'])
    variables = np.r_[data['endpoint_mass'], *(data['densities'][x] for x in ('f', 'g', 'k', 'ell'))]
    rng = np.random.default_rng(563809)
    maximum = 0.
    for i in range(160):
        a = rng.uniform(D, 1.) if i % 2 else rng.uniform(0., D)
        u = rng.uniform(a, 1.); c = rng.uniform(-a, 1.); y = rng.uniform(c, 1.)
        parameters = np.array([a, u, c, y])
        scores = []
        for routine in (previous_cases, lambda p, k, v: negative_cases(p, k, v, 0.)):
            first, nf, second, ns = routine(parameters, knots, variables)
            values = []
            if nf >= 0:
                values.append(negative_feature_change(parameters, first, nf, knots)@variables)
            if ns >= 0:
                values.append(negative_feature_change(parameters, second, ns, knots)@variables)
            scores.append(max(values))
        error = abs(scores[0]-scores[1])
        assert error < 2e-12, (parameters, scores)
        maximum = max(maximum, error)
    print('PASS: 160 zero-localized-component comparisons against independent PAVA; max error', maximum)


if __name__ == '__main__':
    verify_zero_component()
