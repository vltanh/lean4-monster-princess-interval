#!/usr/bin/env python3
"""Exact independent finite-arrangement checks for negative-prefix pooling."""
from fractions import Fraction as Q
from itertools import accumulate
import random


def pool(coefficients, weights):
    stack = []
    for j, (p, w) in enumerate(zip(coefficients, weights)):
        stack.append([j, j+1, w, p*w])
        while len(stack) > 1 and stack[-2][3]*stack[-1][2] > stack[-1][3]*stack[-2][2]:
            b = stack.pop(); a = stack[-1]
            a[1] = b[1]; a[2] += b[2]; a[3] += b[3]
    return stack


def ordinary(coefficients, weights, levels, primitive, cap):
    result = []
    allowed = [i for i, x in enumerate(levels) if x <= cap]
    for lo, hi, weight, total in pool(coefficients, weights):
        mean = total/weight
        choice = max(allowed, key=lambda i: mean*levels[i]-primitive[i])
        result.extend([choice]*(hi-lo))
    assert result == sorted(result)
    return result


def check_case(coefficients, weights, levels, primitive, edge, band_start,
               low_start=False):
    n = len(coefficients)
    edge_index = levels.index(edge)
    def utility(j, i):
        x = levels[i]
        if j >= band_start and x > edge:
            value = coefficients[j]*edge-primitive[edge_index]
            if low_start:
                value -= (x-edge)**2
            return value
        return coefficients[j]*x-primitive[i]
    # Independent complete dynamic program over all nondecreasing choices.
    previous = [Q(0)]*len(levels)
    for j in range(n):
        prefix = list(accumulate(previous, max))
        previous = [prefix[i]+weights[j]*utility(j, i) for i in range(len(levels))]
    exhaustive = max(previous)
    candidates = []
    if band_start == n:
        candidates.append(ordinary(coefficients, weights, levels, primitive, levels[-1]))
    else:
        candidates.append(ordinary(coefficients, weights, levels, primitive, edge))
        if not low_start:
            left = ordinary(coefficients[:band_start], weights[:band_start], levels,
                            primitive, levels[-1])
            final = max(edge_index, left[-1] if left else 0)
            candidates.append(left+[final]*(n-band_start))
    pooled = max(sum(weights[j]*utility(j, i) for j, i in enumerate(route))
                 for route in candidates)
    assert pooled == exhaustive, (coefficients, weights, band_start, low_start, pooled, exhaustive)
    return exhaustive


def main():
    rng = random.Random(924228)
    count = 0
    for trial in range(720):
        n = 1+trial % 6
        levels = [Q(j, 5) for j in range(6)]
        slopes = sorted(Q(rng.randrange(0, 13), 4) for _ in range(5))
        primitive = [Q(0)]
        for j, slope in enumerate(slopes):
            primitive.append(primitive[-1]+slope*(levels[j+1]-levels[j]))
        edge_index = 1+trial % 4
        edge = levels[edge_index]
        coefficients = [Q(rng.randrange(0, 17), 4) for _ in range(n)]
        weights = [Q(1+rng.randrange(5), 7) for _ in range(n)]
        for band_start in range(n+1):
            # Nonnegative lower-edge generators require p<=k(edge) on band.
            p = coefficients.copy()
            for j in range(band_start, n):
                p[j] = min(p[j], slopes[min(edge_index, 4)])
            check_case(p, weights, levels, primitive, edge, band_start)
            count += 1
        p = [min(z, slopes[min(edge_index, 4)]) for z in coefficients]
        check_case(p, weights, levels, primitive, edge, 0, True)
        count += 1
    levels = [Q(j, 4) for j in range(5)]
    primitive = [Q(0), Q(0), Q(1, 4), Q(3, 4), Q(3, 2)]
    p, weights = [Q(0), Q(3)], [Q(1), Q(1)]
    ordered = check_case(p, weights, levels, primitive, Q(1, 2), 2)
    constant = max(sum(pj*x-k for pj in p) for x, k in zip(levels, primitive))
    assert ordered-constant == Q(1, 2)
    print('PASS:', count, 'exact ordered-prefix PAVA versus complete dynamic-program comparisons')
    print('Nonmonotone coefficient example: ordered score', ordered,
          'constant score', constant, 'strict gain', ordered-constant)
    print('Scope: exact prefix optimization identities; no equilibrium or game bound')


if __name__ == '__main__':
    main()
