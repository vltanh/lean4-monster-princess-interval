#!/usr/bin/env python3
"""Exact minimum of a rational quadratic on a simplex.

Reconstructed after the 2026-11-11 executor outage. The matching algorithm
was independently executed with BigInt rationals in V8; Python was not
rerun during the outage. No Lean compilation or CI is involved.

All nonempty faces are checked. Singular stationary systems may be skipped:
a nonzero null pair (d,eta) has sum(d)=0 and 2Qd=eta*1. At a stationary
point the quadratic is constant along that tangent direction until a
proper face is reached. Iterating reaches an invertible face or a vertex.
This argument does not assume that the quadratic is convex.
"""
import argparse
from fractions import Fraction as Q
from itertools import combinations
import json
from pathlib import Path


def solve_invertible(matrix, rhs):
    n = len(matrix)
    assert len(rhs) == n and all(len(row) == n for row in matrix)
    a = [[Q(x) for x in row] + [Q(rhs[i])] for i, row in enumerate(matrix)]
    for col in range(n):
        pivot = next((i for i in range(col, n) if a[i][col]), None)
        if pivot is None:
            return None
        a[col], a[pivot] = a[pivot], a[col]
        scale = a[col][col]
        a[col] = [x / scale for x in a[col]]
        for i in range(n):
            if i != col and a[i][col]:
                scale = a[i][col]
                a[i] = [x - scale*y for x, y in zip(a[i], a[col])]
    return [row[-1] for row in a]


def evaluate(matrix, weights):
    return sum(Q(matrix[i][j])*weights[i]*weights[j]
               for i in range(len(weights)) for j in range(len(weights)))


def minimum(matrix):
    matrix = [[Q(x) for x in row] for row in matrix]
    n = len(matrix)
    assert n and all(len(row) == n for row in matrix)
    assert all(matrix[i][j] == matrix[j][i] for i in range(n) for j in range(n))
    best = None
    faces = dict(total=0, singular=0, feasible=0)
    for size in range(1, n+1):
        for support in combinations(range(n), size):
            faces['total'] += 1
            system = [[2*matrix[i][j] for j in support] + [Q(-1)] for i in support]
            system.append([Q(1)]*size + [Q(0)])
            answer = solve_invertible(system, [Q(0)]*size + [Q(1)])
            if answer is None:
                faces['singular'] += 1
                continue
            if min(answer[:-1]) < 0:
                continue
            faces['feasible'] += 1
            weights = [Q(0)]*n
            for index, value in zip(support, answer[:-1]):
                weights[index] = value
            value = evaluate(matrix, weights)
            assert sum(weights) == 1 and value == answer[-1]/2
            if best is None or value < best['value']:
                best = dict(value=value, weights=tuple(weights), support=support)
    assert best is not None
    return dict(best, faces=faces)


def matrix_from_function(vertices, function):
    vertices = [tuple(map(Q, vertex)) for vertex in vertices]
    values = [Q(function(vertex)) for vertex in vertices]
    matrix = [[Q(0) for _ in vertices] for _ in vertices]
    for i, vertex in enumerate(vertices):
        matrix[i][i] = values[i]
        for j in range(i):
            midpoint = tuple((x+y)/2 for x, y in zip(vertex, vertices[j]))
            matrix[i][j] = matrix[j][i] = 2*function(midpoint)-(values[i]+values[j])/2
    return matrix


def self_check():
    cases = [
        ([[1, 1, 1], [1, 1, 1], [1, 1, 1]], Q(1)),
        ([[-1, -1], [-1, -1]], Q(-1)),
        ([[1, 0, 0], [0, 2, 0], [0, 0, 3]], Q(6, 11)),
        ([[1, 2], [2, 1]], Q(1)),
        ([[2, -1, -1], [-1, 2, -1], [-1, -1, 2]], Q(0)),
        ([[1, -1, -1], [-1, 1, -1], [-1, -1, 1]], Q(-1, 3)),
        ([[0, 0, 1], [0, 0, 1], [1, 1, 2]], Q(0)),
        ([[Q(7, 13)]], Q(7, 13)),
    ]
    for matrix, expected in cases:
        answer = minimum(matrix)
        assert answer['value'] == expected
    vertices = [(0, 0), (1, 0), (0, 1)]
    matrix = matrix_from_function(vertices,
        lambda p: (p[0]-Q(1, 3))**2 + 2*(p[1]-Q(1, 4))**2)
    answer = minimum(matrix)
    assert answer['value'] == 0
    assert answer['weights'] == (Q(5, 12), Q(1, 3), Q(1, 4))
    return dict(status='PASS', exact_fixtures=len(cases)+1)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--self-check', action='store_true')
    parser.add_argument('--input', type=Path)
    args = parser.parse_args()
    if args.self_check or args.input is None:
        print(json.dumps(self_check(), indent=2))
    if args.input:
        data = json.loads(args.input.read_text())
        answer = minimum(data['matrix'] if isinstance(data, dict) else data)
        print(json.dumps(answer, default=str, indent=2))


if __name__ == '__main__':
    main()
