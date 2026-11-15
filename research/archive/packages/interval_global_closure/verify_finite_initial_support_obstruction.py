#!/usr/bin/env python3
"""Exact rational regression for the finite-initial-support obstruction.

This checks path splicing and chronological first contacts in explicit fixtures.
The continuum nonattainment theorem is proved in
research/12-global-closure/FINITE_INITIAL_SUPPORT_NONATTAINMENT.md;
finite fixtures do not replace its compactness or minimax arguments.
Uses only Python's standard library and Fraction arithmetic.
"""

from fractions import Fraction as F
from itertools import product
import json


class Path:
    """Rational polygonal path, held constant after its final knot."""

    def __init__(self, points):
        self.points = tuple((F(t), F(x)) for t, x in points)
        assert self.points and self.points[0][0] == 0
        assert all(-1 <= x <= 1 for _, x in self.points)
        for (t, x), (u, y) in zip(self.points, self.points[1:]):
            assert u > t
            assert abs(y - x) <= u - t

    def at(self, t):
        t = F(t)
        assert t >= 0
        for (a, x), (b, y) in zip(self.points, self.points[1:]):
            if t <= b:
                return x + (y - x) * (t - a) / (b - a)
        return self.points[-1][1]

    @property
    def start(self):
        return self.points[0][1]


def first_contact(p, m):
    """First coincidence, including equality at t=0 and at any knot.

    None denotes infinite capture time. The difference is affine on every
    interval in the common knot refinement, so the scan is exhaustive.
    """
    times = sorted({t for t, _ in p.points} | {t for t, _ in m.points})
    for a, b in zip(times, times[1:]):
        da = p.at(a) - m.at(a)
        db = p.at(b) - m.at(b)
        if da == 0:
            return a
        if da * db <= 0:
            return a - da * (b - a) / (db - da)
    last = times[-1]
    return last if p.at(last) == m.at(last) else None


def perturb(p, delta):
    x, z = p.start, p.at(delta)
    if x == 1:
        y = x - delta / 2
    elif x == -1:
        y = x + delta / 2
    elif z >= x:
        y = x + delta / 2
    else:
        y = x - delta / 2
    assert abs(y - x) == delta / 2
    assert abs(z - y) <= delta / 2
    q = Path([(0, y), (delta, z)] +
             [(t, u) for t, u in p.points if t > delta])
    return q


def append_visit(points, target):
    t, x = points[-1]
    if x != target:
        points.append((t + abs(target - x), target))


def prefixes(x, h):
    for directions in product((-1, 0, 1), repeat=2):
        points = [(F(0), x)]
        legal = True
        for d in directions:
            t, z = points[-1]
            z += d * h
            if not -1 <= z <= 1:
                legal = False
                break
            points.append((t + h, z))
        if legal:
            yield points


def prefix_fixtures():
    starts = (F(-1), F(-1, 2), F(0), F(1, 2), F(1))
    h, delta = F(1, 64), F(1, 32)
    princesses, monsters = [], []
    for x in starts:
        for points in prefixes(x, h):
            for endpoint in (F(-1), F(1)):
                ppoints = list(points)
                append_visit(ppoints, endpoint)
                princesses.append(Path(ppoints))
            mpoints = list(points)
            append_visit(mpoints, F(-1))
            append_visit(mpoints, F(1))
            monsters.append(Path(mpoints))

    same_start_checks = other_start_checks = equality_at_join = 0
    for p in princesses:
        q = perturb(p, delta)
        old_total = new_total = F(0)
        a_count = 0
        for m in monsters:
            old, new = first_contact(p, m), first_contact(q, m)
            # Each Monster completes an endpoint tour, so both are finite.
            assert old is not None and new is not None
            old_total += old
            new_total += new
            if m.start == p.start:
                a_count += 1
                same_start_checks += 1
                assert old == 0 and new >= delta / 4
                equality_at_join += (new == delta)
            else:
                other_start_checks += 1
                assert old == new and old > delta
        # The common uniform mixture obeys the quantitative integrated gap.
        assert new_total - old_total >= a_count * delta / 4
    assert equality_at_join > 0
    return {
        "princess_paths": len(princesses),
        "monster_paths": len(monsters),
        "own_start_contacts_checked": same_start_checks,
        "other_start_contacts_checked": other_start_checks,
        "contacts_exactly_at_rejoining_time": equality_at_join,
    }


def endpoint_example():
    p = Path([(0, 1)])
    left_sweep = Path([(0, -1), (2, 1)])
    right_sweep = Path([(0, 1), (2, -1)])
    q = perturb(p, F(1, 8))
    old = (first_contact(p, left_sweep) +
           first_contact(p, right_sweep)) / 2
    new = (first_contact(q, left_sweep) +
           first_contact(q, right_sweep)) / 2
    assert first_contact(q, right_sweep) == F(1, 24)
    assert old == 1 and new == F(49, 48)
    return {"old_payoff": str(old), "new_payoff": str(new),
            "strict_gain": str(new - old)}


def support_prefix_example():
    left = Path([(0, F(-1, 2))])
    right = Path([(0, F(1, 2))])
    old = Path([(0, 0), (F(1, 2), F(1, 2)),
                (F(3, 2), F(-1, 2))])
    new = Path([(0, F(1, 2)), (F(1, 2), F(1, 2)),
                (F(3, 2), F(-1, 2))])
    w_left, w_right, tau = F(2, 5), F(3, 5), F(1, 2)
    old_cost = (w_left * first_contact(left, old) +
                w_right * first_contact(right, old))
    new_cost = (w_left * first_contact(left, new) +
                w_right * first_contact(right, new))
    assert old_cost == F(9, 10) and new_cost == F(3, 5)
    assert old_cost - new_cost == w_right * tau == F(3, 10)
    return {"old_payoff": str(old_cost), "new_payoff": str(new_cost),
            "initial_atom_mass_times_first_contact": str(w_right * tau)}


def main():
    print(json.dumps({
        "arithmetic": "fractions.Fraction only",
        "scope": "exact polygonal regressions; continuum theorem is analytic",
        "prefix_perturbation": prefix_fixtures(),
        "endpoint_example": endpoint_example(),
        "support_prefix_replacement": support_prefix_example(),
        "result": "PASS",
    }, indent=2))


if __name__ == "__main__":
    main()
