"""Eliminate one bounded scalar from a rational parametric quadratic.

The objective is c + linear*x + x^T*hessian*x, x=(theta,h).
Inequalities are (a,b), meaning a*x <= b. The explicit interval for h
makes every nonempty fiber compact. The result is an exact finite lower
envelope on polyhedral eligibility domains, without winner-region splits.

This primitive does not assert that a supplied game response class is
exhaustive. No floating arithmetic or third-party dependency is used.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction as Q


def rational(value):
    if isinstance(value, bool) or not isinstance(value, (int, Q, str)):
        raise TypeError("exact rational data required")
    return Q(value)


def dot(a, b):
    return sum((x*y for x, y in zip(a, b)), Q(0))


@dataclass(frozen=True)
class Quadratic:
    constant: Q
    linear: tuple[Q, ...]
    hessian: tuple[tuple[Q, ...], ...]

    def __post_init__(self):
        c = rational(self.constant)
        linear = tuple(map(rational, self.linear))
        hessian = tuple(tuple(map(rational, row)) for row in self.hessian)
        n = len(linear)
        if len(hessian) != n or any(len(row) != n for row in hessian):
            raise ValueError("wrong Hessian dimensions")
        if any(hessian[i][j] != hessian[j][i]
               for i in range(n) for j in range(n)):
            raise ValueError("Hessian must be symmetric")
        object.__setattr__(self, "constant", c)
        object.__setattr__(self, "linear", linear)
        object.__setattr__(self, "hessian", hessian)

    def evaluate(self, point):
        point = tuple(map(rational, point))
        if len(point) != len(self.linear):
            raise ValueError("wrong point dimension")
        return self.constant + dot(self.linear, point) + sum(
            (point[i]*self.hessian[i][j]*point[j]
             for i in range(len(point)) for j in range(len(point))), Q(0))


@dataclass(frozen=True)
class IntervalCandidate:
    origins: tuple[str, ...]
    h_constant: Q
    h_linear: tuple[Q, ...]
    objective: Quadratic
    inequalities: tuple[tuple[tuple[Q, ...], Q], ...]

    def eligible(self, theta):
        theta = tuple(map(rational, theta))
        if len(theta) != len(self.h_linear):
            raise ValueError("wrong parameter dimension")
        return all(dot(a, theta) <= b for a, b in self.inequalities)

    def height(self, theta):
        theta = tuple(map(rational, theta))
        if len(theta) != len(self.h_linear):
            raise ValueError("wrong parameter dimension")
        return self.h_constant + dot(self.h_linear, theta)


def substitute_last(objective, offset, slopes):
    """Substitute h=offset+slopes*theta, retaining symmetric H notation."""
    if not isinstance(objective, Quadratic) or not objective.linear:
        raise ValueError("a quadratic with at least one variable is required")
    offset = rational(offset)
    slopes = tuple(map(rational, slopes))
    n = len(objective.linear)-1
    if len(slopes) != n:
        raise ValueError("wrong substitution dimension")
    alpha = objective.hessian[-1][-1]
    cross = objective.hessian[-1][:-1]
    lh = objective.linear[-1]
    constant = objective.constant + lh*offset + alpha*offset*offset
    linear = tuple(objective.linear[i] + lh*slopes[i] +
                   2*offset*cross[i] + 2*alpha*offset*slopes[i]
                   for i in range(n))
    hessian = tuple(tuple(objective.hessian[i][j] +
                         cross[i]*slopes[j] + slopes[i]*cross[j] +
                         alpha*slopes[i]*slopes[j]
                         for j in range(n)) for i in range(n))
    return Quadratic(constant, linear, hessian)


def _canonical_constraints(rows):
    """Remove tautologies/positive multiples; None means a false constant."""
    result = set()
    for a, b in rows:
        scale = next((abs(x) for x in a if x), None)
        if scale is None:
            if b < 0:
                return None
            continue
        result.add((tuple(x/scale for x in a), b/scale))
    return tuple(sorted(result))


def eliminate_last_variable(inequalities, c, linear, hessian, interval=(0, 1)):
    """Return all needed exact minimizer candidates for the last variable.

    At every fixed theta with a feasible h, the least eligible candidate
    objective is exactly the fiber minimum, with an attaining h witness.
    If the fiber is empty, no candidate is eligible. Parameter domains may
    be unbounded or lower-dimensional; no full-dimensional assumption is
    made. Empty nonconstant domains are retained unless later proved empty.
    """
    objective = Quadratic(c, linear, hessian)
    dimension = len(objective.linear)
    if not dimension:
        raise ValueError("at least the eliminated variable is required")
    if len(interval) != 2:
        raise ValueError("interval needs two finite rational endpoints")
    lo, hi = map(rational, interval)
    if lo > hi:
        raise ValueError("interval endpoints are reversed")
    rows = []
    for a, b in inequalities:
        a = tuple(map(rational, a))
        if len(a) != dimension:
            raise ValueError("constraint dimension mismatch")
        rows.append((a, rational(b)))
    unit = (Q(0),)*(dimension-1)+(Q(1),)
    rows += [(unit, hi), (tuple(-x for x in unit), -lo)]

    # Each fiber endpoint equals at least one affine constraint boundary.
    # An interior minimum is possible only for positive h^2 coefficient.
    forms = {}
    for i, (a, b) in enumerate(rows):
        if a[-1]:
            form = (b/a[-1], tuple(-x/a[-1] for x in a[:-1]))
            forms.setdefault(form, []).append("boundary:"+str(i))
    alpha = objective.hessian[-1][-1]
    if alpha > 0:
        form = (-objective.linear[-1]/(2*alpha),
                tuple(-x/alpha for x in objective.hessian[-1][:-1]))
        forms.setdefault(form, []).append("stationary")

    result = []
    for (offset, slopes), origins in forms.items():
        domain = _canonical_constraints(
            (tuple(a[j]+a[-1]*slopes[j] for j in range(dimension-1)),
             b-a[-1]*offset) for a, b in rows)
        if domain is None:
            continue
        result.append(IntervalCandidate(tuple(origins), offset, slopes,
                      substitute_last(objective, offset, slopes), domain))
    return tuple(result)


def minimum_at(candidates, theta):
    """Evaluate the exact envelope; return (value,h,index), or None."""
    theta = tuple(map(rational, theta))
    choices = [(candidate.objective.evaluate(theta), candidate.height(theta), i)
               for i, candidate in enumerate(candidates) if candidate.eligible(theta)]
    return min(choices) if choices else None


__all__ = ["Quadratic", "IntervalCandidate", "substitute_last",
           "eliminate_last_variable", "minimum_at"]
