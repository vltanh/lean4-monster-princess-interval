"""Exact quadratic minima on bounded rational polytopes in dimension <= 4.

The complete method enumerates active faces, not sampled points. Singular
stationary sets need no arbitrary pseudoinverse: a stationary null direction
preserves the quadratic, so a minimum can be moved to a smaller face until
its KKT system is nonsingular. Vertices are included explicitly.

Inequalities and equalities are (coefficient_vector, rhs), with a*x <= rhs
and a*x == rhs respectively. The objective is c + linear*x + x^T*hessian*x.
All data must be exact integers, Fractions, or rational strings; floats are
rejected. No third-party libraries are used.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction as Q
from itertools import combinations


def rational(value):
    if isinstance(value, bool) or not isinstance(value, (int, Q, str)):
        raise TypeError("coefficients must be exact rational data, not floats")
    return Q(value)


def dot(a, b):
    return sum((x*y for x, y in zip(a, b)), Q(0))


def solve_unique(matrix, rhs):
    """Solve a square rational system; return None when it is singular."""
    n = len(rhs)
    if len(matrix) != n or any(len(row) != n for row in matrix):
        raise ValueError("linear system must be square")
    a = [list(row) + [value] for row, value in zip(matrix, rhs)]
    for j in range(n):
        pivot = next((i for i in range(j, n) if a[i][j]), None)
        if pivot is None:
            return None
        a[j], a[pivot] = a[pivot], a[j]
        divisor = a[j][j]
        a[j] = [v/divisor for v in a[j]]
        for i in range(n):
            if i != j and a[i][j]:
                multiplier = a[i][j]
                a[i] = [v-multiplier*w for v, w in zip(a[i], a[j])]
    return tuple(row[-1] for row in a)


def independent_equalities(rows, dimension):
    """Equivalent independent RREF equalities, or None if inconsistent."""
    a = [list(row) + [rhs] for row, rhs in rows]
    rank = 0
    for j in range(dimension):
        pivot = next((i for i in range(rank, len(a)) if a[i][j]), None)
        if pivot is None:
            continue
        a[rank], a[pivot] = a[pivot], a[rank]
        divisor = a[rank][j]
        a[rank] = [v/divisor for v in a[rank]]
        for i in range(len(a)):
            if i != rank and a[i][j]:
                multiplier = a[i][j]
                a[i] = [v-multiplier*w for v, w in zip(a[i], a[rank])]
        rank += 1
    if any(not any(row[:-1]) and row[-1] for row in a):
        return None
    return tuple((tuple(row[:-1]), row[-1]) for row in a[:rank])


def feasible(point, inequalities, equalities):
    return all(dot(a, point) <= b for a, b in inequalities) and all(
        dot(a, point) == b for a, b in equalities)


def vertex_candidates(inequalities, equalities, dimension):
    needed = dimension-len(equalities)
    for selected in combinations(inequalities, needed):
        rows = equalities + selected
        point = solve_unique([a for a, _ in rows], [b for _, b in rows])
        if point is not None and feasible(point, inequalities, equalities):
            yield point


def stationary_point(rows, linear, hessian):
    d, r = len(linear), len(rows)
    matrix = [[2*hessian[i][j] for j in range(d)] + [a[i] for a, _ in rows]
              for i in range(d)]
    matrix += [list(a) + [Q(0)]*r for a, _ in rows]
    answer = solve_unique(matrix, [-v for v in linear] + [b for _, b in rows])
    return None if answer is None else answer[:d]


def any_feasible_point(inequalities, equalities, dimension):
    """Exact feasibility via the coercive objective ||x||^2.

    Its minimizer exists on every nonempty closed polyhedron, bounded or not.
    Its equality-restricted Hessian is positive definite, so one of the finite
    independent active-face systems below returns that feasible point.
    """
    identity = tuple(tuple(Q(int(i == j)) for j in range(dimension))
                     for i in range(dimension))
    zero = (Q(0),)*dimension
    for count in range(dimension-len(equalities)+1):
        for selected in combinations(inequalities, count):
            point = stationary_point(equalities+selected, zero, identity)
            if point is not None and feasible(point, inequalities, equalities):
                return point
    return None


def recession_witness(inequalities, equalities, dimension):
    """Return a nonzero recession direction, or prove there is none.

    The recession cone intersected with [-1,1]^d is a compact polytope.
    It contains a nonzero point iff it has a nonzero vertex. Every nonzero
    recession direction can be rescaled into that box.
    """
    rows = tuple((a, Q(0)) for a, _ in inequalities)
    eq = tuple((a, Q(0)) for a, _ in equalities)
    box = []
    for i in range(dimension):
        a = tuple(Q(int(i == j)) for j in range(dimension))
        box.extend([(a, Q(1)), (tuple(-v for v in a), Q(1))])
    for point in vertex_candidates(rows+tuple(box), eq, dimension):
        if any(point):
            return point
    return None


class UnboundedPolytope(ValueError):
    def __init__(self, feasible_point, direction):
        self.feasible_point = feasible_point
        self.direction = direction
        super().__init__("quadratic guard domain is unbounded; rational recession witness supplied")


@dataclass(frozen=True)
class QuadraticMinimum:
    value: Q
    point: tuple[Q, ...]
    stats: dict[str, int]


def minimize_quadratic(inequalities, c, linear, hessian, equalities=()):
    """Return an exact attained minimum, or None for an empty polytope.

    Raises UnboundedPolytope for a nonempty unbounded domain, even if this
    particular objective happens to have a finite minimum there. The method
    certifies every stated boundedness/feasibility condition independently.
    """
    linear = tuple(map(rational, linear));dimension = len(linear)
    if not 0 <= dimension <= 4:
        raise ValueError("supported ambient dimensions are zero through four")
    c = rational(c)
    hessian = tuple(tuple(map(rational, row)) for row in hessian)
    if len(hessian) != dimension or any(len(row) != dimension for row in hessian):
        raise ValueError("wrong Hessian dimensions")
    if any(hessian[i][j] != hessian[j][i]
           for i in range(dimension) for j in range(dimension)):
        raise ValueError("hessian must be symmetric")

    def constraints(rows):
        result = []
        for a, b in rows:
            a = tuple(map(rational, a))
            if len(a) != dimension:
                raise ValueError("constraint dimension mismatch")
            result.append((a, rational(b)))
        return tuple(result)

    inequalities = constraints(inequalities)
    equalities = independent_equalities(constraints(equalities), dimension)
    if equalities is None:
        return None
    if dimension == 0:
        return QuadraticMinimum(c, (), {"vertices": 1, "stationary_systems": 0,
                                       "singular_systems": 0}) if feasible((), inequalities, equalities) else None

    vertices = set(vertex_candidates(inequalities, equalities, dimension))
    witness = next(iter(vertices), None)
    if witness is None:
        witness = any_feasible_point(inequalities, equalities, dimension)
        if witness is None:
            return None
    recession = recession_witness(inequalities, equalities, dimension)
    if recession is not None:
        raise UnboundedPolytope(witness, recession)
    if not vertices:
        raise AssertionError("nonempty bounded polytope must have a vertex")

    def value(point):
        return c+dot(linear, point)+sum(
            (point[i]*hessian[i][j]*point[j]
             for i in range(dimension) for j in range(dimension)), Q(0))

    candidates = set(vertices)
    systems = singular = 0
    # Full-rank point faces are already included by vertex enumeration.
    for count in range(dimension-len(equalities)):
        for selected in combinations(inequalities, count):
            systems += 1
            point = stationary_point(equalities+selected, linear, hessian)
            if point is None:
                singular += 1
            elif feasible(point, inequalities, equalities):
                candidates.add(point)
    best = min(candidates, key=lambda point: (value(point), point))
    return QuadraticMinimum(value(best), best,
                            {"vertices": len(vertices), "candidates": len(candidates),
                             "stationary_systems": systems, "singular_systems": singular})


__all__ = ["minimize_quadratic", "QuadraticMinimum", "UnboundedPolytope"]
