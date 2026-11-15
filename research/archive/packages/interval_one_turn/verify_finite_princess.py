#!/usr/bin/env python3
"""Exact all-B1 pricing for finite actual polygonal Princess laws.

Proof: research/13-equilibrium-geometry/ONE_TURN_FINITE_PRINCESS_ATTACK_SET.md.
Input example:
{"format":"one-turn-finite-princess-v1","paths":[
 {"weight":"1/2","vertices":[["0","-1"],["6","-1"]]},
 {"weight":"1/2","vertices":[["0","1"],["6","1"]]}]}
All arithmetic is integer/Fraction. Actual initial and turning contacts count.
"""
from __future__ import annotations

import argparse
from bisect import bisect_left
from fractions import Fraction as Q
import json
from math import gcd, lcm
from pathlib import Path
from random import Random

from verify_domain import Path as PhysicalPath, direct_first_hit, monster


def validate(path):
    assert path.nodes[0][0] == 0 and path.nodes[-1][0] == 6
    for (s, x), (t, y) in zip(path.nodes, path.nodes[1:]):
        assert t > s and -1 <= x <= 1 and -1 <= y <= 1
        assert (abs(y-x) == t-s or
                (x == y and abs(x) == 1)), (
                    "only unit legs and stationary endpoint segments are accepted")


def validate_general(path):
    assert path.nodes[0][0] == 0 and path.nodes[-1][0] == 6
    for (s, x), (t, y) in zip(path.nodes, path.nodes[1:]):
        assert t > s and -1 <= x <= 1 and -1 <= y <= 1
        assert abs(y-x) <= t-s


def read_law(data, *, general=False):
    assert data["format"] == "one-turn-finite-princess-v1"
    paths, weights = [], []
    for row in data["paths"]:
        knots = [(Q(t), Q(x)) for t, x in row["vertices"]]
        assert knots and knots[0][0] == 0
        whole = PhysicalPath.make(knots)
        if knots[-1][0] > 6:
            knots = [node for node in knots if node[0] < 6]
            knots.append((Q(6), whole.at(6)))
        if knots[-1][0] < 6:
            if not general:
                assert abs(knots[-1][1]) == 1, "unfinished supplied path"
            knots.append((Q(6), knots[-1][1]))
        path = PhysicalPath.make(knots)
        (validate_general if general else validate)(path)
        weight = Q(row["weight"])
        assert weight > 0
        paths.append(path)
        weights.append(weight)
    assert paths and sum(weights) == 1
    return paths, weights


def normalize_line(a, b, c):
    a, b, c = Q(a), Q(b), Q(c)
    denominator = lcm(a.denominator, b.denominator, c.denominator)
    a, b, c = (int(x*denominator) for x in (a, b, c))
    divisor = gcd(a, b, c)
    assert divisor and (a or b)
    a, b, c = a//divisor, b//divisor, c//divisor
    if a < 0 or (a == 0 and b < 0):
        a, b, c = -a, -b, -c
    return a, b, c


def general_attacks(paths):
    """Full rational line arrangement, including all Monster-turn contacts."""
    lines = {normalize_line(1, 0, -1), normalize_line(1, 0, 1),
             normalize_line(1, -1, 0), normalize_line(1, 1, 2)}
    for path in paths:
        validate_general(path)
        for sign in (-1, 1):
            knots = [(t, sign*x) for t, x in path.nodes]
            for t, x in knots:
                lines.add(normalize_line(1, 0, x-t))
                lines.add(normalize_line(0, 1, t+x))
                lines.add(normalize_line(0, 1, t-x-2))
            for (s, x), (t, y) in zip(knots, knots[1:]):
                velocity = (y-x)/(t-s)
                intercept = x-velocity*s
                lines.add(normalize_line(1+velocity, 1-velocity, 2*intercept))
    corners = ((-1, -1), (-1, 3), (1, 1))
    kept = []
    for a, b, c in lines:
        values = [a*x+b*y-c for x, y in corners]
        if min(values) <= 0 <= max(values):
            kept.append((a, b, c))
    kept.sort()
    points = {(Q(x), Q(y)) for x, y in corners}
    for i, (a, b, c) in enumerate(kept):
        for d, e, f in kept[:i]:
            determinant = a*e-d*b
            if not determinant:
                continue
            xnum, ynum = c*e-f*b, a*f-d*c
            if determinant < 0:
                xnum, ynum, determinant = -xnum, -ynum, -determinant
            if (-determinant <= xnum <= determinant and
                    xnum <= ynum <= 2*determinant-xnum):
                points.add((Q(xnum, determinant), Q(ynum, determinant)))
    return kept, sorted(points)


class InversePath:
    """Exact first-level inverse of the two monotone light coordinates."""
    def __init__(self, path):
        self.times = tuple(t for t, _ in path.nodes)
        self.U = tuple(t+x for t, x in path.nodes)
        self.W = tuple(t-x for t, x in path.nodes)
        self.start = path.nodes[0][1]
        assert list(self.U) == sorted(self.U)
        assert list(self.W) == sorted(self.W)

    def first_reach(self, values, level):
        i = bisect_left(values, level)
        if i == 0:
            return Q(0)
        assert i < len(values), "six-unit horizon must contain required contact"
        left, right = values[i-1], values[i]
        assert left < level <= right
        return self.times[i-1]+(self.times[i]-self.times[i-1])*(level-left)/(right-left)

    def capture(self, a, b):
        if self.start == a:
            return Q(0)
        if self.start < a:
            return self.first_reach(self.U, b)
        first = self.first_reach(self.W, -a)
        if 2*first <= b-a:
            return first
        return self.first_reach(self.W, b+2)


def price_general(paths, weights):
    assert len(paths) == len(weights) and all(w > 0 for w in weights)
    assert sum(weights) == 1
    lines, points = general_attacks(paths)
    curves = {1: [InversePath(p) for p in paths],
              -1: [InversePath(p.reflected()) for p in paths]}
    best = winner = None
    for a, b in points:
        for orientation in (-1, 1):
            score = sum((w*p.capture(a, b)
                         for w, p in zip(weights, curves[orientation])), Q(0))
            if best is None or score < best:
                best, winner = score, (a, b, orientation)
    a, b, orientation = winner
    physical = monster(a, (b-a)/2)
    if orientation == -1:
        physical = physical.reflected()
    independent = sum((w*direct_first_hit(physical, p)
                       for w, p in zip(weights, paths)), Q(0))
    assert independent == best
    return {
        "status": "PASS",
        "scope": "exact all-B1 security of a finite actual rational-PL Princess law",
        "mode": "general rational slopes and interior waits",
        "princess_paths": len(paths),
        "arrangement_lines": len(lines),
        "attack_vertices": len(points),
        "oriented_inverse_evaluations": 2*len(points)*len(paths),
        "all_B1_lower": str(best),
        "all_B1_lower_decimal": float(best),
        "attaining_attack": {
            "a": str(a), "b": str(b),
            "h": str((b-a)/2), "orientation": orientation,
        },
        "independent_fraction_check_at_minimizer": True,
    }


def vertex_denominator(paths):
    return lcm(*(coordinate.denominator
                 for path in paths for node in path.nodes for coordinate in node))


def complete_attacks(paths, D=None):
    """Return integer (a*D,b*D) arrangement vertices; include both orientations."""
    if D is None:
        D = vertex_denominator(paths)
    aa, bb = {-D, D}, {-D, 3*D}
    for path in paths:
        for tq, xq in path.nodes:
            assert (tq*D).denominator == 1 and (xq*D).denominator == 1
            t, x = int(tq*D), int(xq*D)
            for sign in (-1, 1):
                u, w = t+sign*x, t-sign*x
                if -D <= -w <= D:
                    aa.add(-w)
                for b in (u, w-2*D):
                    if -D <= b <= 3*D:
                        bb.add(b)
    points = {(a, b) for a in aa for b in bb if a <= b <= 2*D-a}
    for a in aa:
        points.add((a, a))
        points.add((a, 2*D-a))
    for b in bb:
        if -D <= b <= D:
            points.add((b, b))
        if -D <= 2*D-b <= D:
            points.add((2*D-b, b))
    assert all(-D <= a <= D and a <= b <= 2*D-a for a, b in points)
    return D, sorted(points)


def segments(knots):
    """Integer positions/times at scale 2D; return start and (end,slope)."""
    clean = []
    for t, x in knots:
        if clean and t == clean[-1][0]:
            assert x == clean[-1][1]
            continue
        clean.append((t, x))
    result = []
    for (s, x), (t, y) in zip(clean, clean[1:]):
        assert t > s and (y-x) % (t-s) == 0
        slope = (y-x)//(t-s)
        assert slope in (-1, 0, 1)
        result.append((t, slope))
    return clean[0][1], tuple(result)


def integer_princess(path, D):
    return segments([(int(t*2*D), int(x*2*D)) for t, x in path.nodes])


def integer_monster(a, b, D, orientation=1):
    assert orientation in (-1, 1)
    knots = [(0, 2*a), (b-a, a+b),
             (2*D+2*b, -2*D), (6*D+2*b, 2*D), (12*D, 2*D)]
    return segments([(t, orientation*x) for t, x in knots])


def first_hit_twice(m, p):
    """Return 4D times first capture, using only integer relative velocities."""
    mx, ms = m
    px, ps = p
    i = j = t = 0
    while i < len(ms) and j < len(ps):
        if mx == px:
            return 2*t
        end = min(ms[i][0], ps[j][0])
        mv, pv = ms[i][1], ps[j][1]
        relative, velocity = mx-px, mv-pv
        if velocity and relative*(relative+velocity*(end-t)) <= 0:
            assert (2*relative) % velocity == 0
            return 2*t-(2*relative)//velocity
        mx += mv*(end-t)
        px += pv*(end-t)
        t = end
        if t == ms[i][0]:
            i += 1
        if t == ps[j][0]:
            j += 1
    assert mx == px, "complete Monster endpoint tour must capture by six"
    return 2*t


def price_law(paths, weights):
    for path in paths:
        validate(path)
    assert len(paths) == len(weights) and all(w > 0 for w in weights)
    assert sum(weights) == 1
    D, points = complete_attacks(paths)
    W = lcm(*(w.denominator for w in weights))
    wi = [int(w*W) for w in weights]
    pp = [integer_princess(p, D) for p in paths]
    best = None
    winner = None
    comparisons = 0
    for a, b in points:
        for orientation in (-1, 1):
            m = integer_monster(a, b, D, orientation)
            score = sum(w*first_hit_twice(m, p) for w, p in zip(wi, pp))
            comparisons += len(pp)
            if best is None or score < best:
                best = score
                winner = (a, b, orientation)
    assert winner is not None
    lower = Q(best, 4*D*W)
    a, b, orientation = winner
    physical = monster(Q(a, D), Q(b-a, 2*D))
    if orientation == -1:
        physical = physical.reflected()
    independent = sum((w*direct_first_hit(physical, p)
                       for w, p in zip(weights, paths)), Q(0))
    assert independent == lower
    return {
        "status": "PASS",
        "scope": "exact security of the supplied actual finite Princess law against all B1",
        "princess_paths": len(paths),
        "vertex_denominator": D,
        "weight_denominator": W,
        "attack_vertices": len(points),
        "oriented_physical_intersections": comparisons,
        "all_B1_lower": str(lower),
        "all_B1_lower_decimal": float(lower),
        "attaining_attack": {
            "a": str(Q(a, D)), "b": str(Q(b, D)),
            "h": str(Q(b-a, 2*D)), "orientation": orientation,
        },
        "independent_fraction_check_at_minimizer": True,
    }


def tests():
    stationary = [PhysicalPath.make(((0, s), (6, s))) for s in (-1, 1)]
    first = price_law(stationary, [Q(1, 2)]*2)
    assert Q(first["all_B1_lower"]) == 1
    outward = PhysicalPath.make(((0, Q(1, 2)), (Q(1, 2), 1), (6, 1)))
    second = price_law([outward, outward.reflected()], [Q(1, 2)]*2)
    assert Q(second["all_B1_lower"]) == Q(3, 4)

    zigzag = PhysicalPath.make(((0, Q(1, 2)), (Q(1, 2), 0),
                               (1, Q(1, 2)), (Q(3, 2), 0),
                               (2, Q(1, 2)), (Q(5, 2), 1), (6, 1)))
    for b in (Q(-33, 64), Q(-1, 2), Q(-31, 64)):
        m = monster(Q(-3, 4), (b+Q(3, 4))/2)
        actual = direct_first_hit(m, zigzag)
        expected = Q(7, 4)+b/2 if b <= Q(-1, 2) else b+3
        assert actual == expected

    base = [
        zigzag,
        PhysicalPath.make(((0, Q(1, 4)), (Q(3, 4), 1), (6, 1))),
        PhysicalPath.make(((0, Q(3, 4)), (Q(1, 2), Q(1, 4)),
                           (Q(5, 4), 1), (6, 1))),
        PhysicalPath.make(((0, Q(-1, 4)), (Q(3, 4), Q(1, 2)),
                           (Q(9, 4), -1), (6, -1))),
    ]
    weights0 = [Q(3, 10), Q(2, 10), Q(4, 10), Q(1, 10)]
    paths = [p for original in base for p in (original, original.reflected())]
    weights = [w/2 for w in weights0 for _ in (0, 1)]
    report = price_law(paths, weights)

    # Independent physical comparisons at arrangement vertices.
    D, attacks = complete_attacks(paths)
    # This fixture belongs to the n=4 shared-parity bank: all initial
    # positions and light vertices lie on 1/4, with clock step 1/8.
    # Audit the complete grid, rather than only the arrangement subset.
    assert D == 4
    full_grid = [(a, b) for a in range(-D, D+1)
                 for b in range(a, 2*D-a+1)]
    assert len(full_grid) == (2*D+1)**2
    assert set(attacks) <= set(full_grid)
    for path in paths:
        assert (path.nodes[0][1]*D).denominator == 1
        assert all(((t+x)*D).denominator == 1 and
                   ((t-x)*D).denominator == 1
                   for t, x in path.nodes)
    parity_checks = 0
    grid_min = None
    for a, b in full_grid:
        for orientation in (-1, 1):
            im = integer_monster(a, b, D, orientation)
            scores = []
            for path in paths:
                twice_clock = first_hit_twice(im, integer_princess(path, D))
                assert twice_clock % 2 == 0
                scores.append(Q(twice_clock, 4*D))
                parity_checks += 1
            score = sum((w*t for w, t in zip(weights, scores)), Q(0))
            grid_min = score if grid_min is None else min(grid_min, score)
    assert grid_min == Q(report["all_B1_lower"])
    rng = Random(20261114)
    sample = attacks if len(attacks) <= 80 else rng.sample(attacks, 80)
    checks = 0
    for a, b in sample:
        for orientation in (-1, 1):
            im = integer_monster(a, b, D, orientation)
            fm = monster(Q(a, D), Q(b-a, 2*D))
            if orientation == -1:
                fm = fm.reflected()
            for path in paths:
                assert Q(first_hit_twice(im, integer_princess(path, D)), 4*D) == \
                    direct_first_hit(fm, path)
                checks += 1

    # Off-arrangement points exercise the theorem on additional genuine paths;
    # finite testing does not replace the manuscript's arrangement proof.
    off_checks = 0
    for _ in range(160):
        a = Q(rng.randrange(-32, 33), 32)
        b = a+(2-2*a)*Q(rng.randrange(65), 64)
        fm = monster(a, (b-a)/2)
        score = sum((w*direct_first_hit(fm, p)
                     for w, p in zip(weights, paths)), Q(0))
        assert score >= Q(report["all_B1_lower"])
        off_checks += 1

    # An interior wait must not silently receive the rectangle-only reduction.
    invalid = PhysicalPath.make(((0, 0), (1, 0), (2, 1), (6, 1)))
    try:
        validate(invalid)
    except AssertionError:
        pass
    else:
        raise AssertionError("interior wait was incorrectly accepted")

    # The full line arrangement agrees on the unit-leg subclass.
    generic_unit = price_general(paths, weights)
    assert generic_unit["all_B1_lower"] == report["all_B1_lower"]
    stationary_inner = [PhysicalPath.make(((0, s), (6, s)))
                        for s in (Q(-1, 2), Q(1, 2))]
    generic_wait = price_general(stationary_inner, [Q(1, 2)]*2)
    assert Q(generic_wait["all_B1_lower"]) == Q(1, 2)

    slow = PhysicalPath.make(((0, Q(1, 3)), (Q(1, 2), Q(1, 3)),
                             (Q(3, 2), Q(2, 3)), (2, Q(1, 2)),
                             (3, 1), (6, 1)))
    other = PhysicalPath.make(((0, Q(-1, 2)), (Q(1, 2), Q(-1, 4)),
                              (1, Q(-1, 4)), (2, Q(1, 2)),
                              (Q(5, 2), 1), (6, 1)))
    general_paths = [slow, slow.reflected(), other, other.reflected()]
    general_weights = [Q(1, 5), Q(1, 5), Q(3, 10), Q(3, 10)]
    generic = price_general(general_paths, general_weights)
    _, general_points = general_attacks(general_paths)
    inverse_checks = 0
    for a, b in general_points:
        for orientation in (-1, 1):
            fm = monster(a, (b-a)/2)
            if orientation == -1:
                fm = fm.reflected()
            for path in general_paths:
                curve = InversePath(path if orientation == 1 else path.reflected())
                assert curve.capture(a, b) == direct_first_hit(fm, path)
                inverse_checks += 1
    # Strictly contracted paths include subunit legs and stationary interior
    # segments, as in the existing physical-germ realization API.
    eta = Q(1, 1000)
    contracted = PhysicalPath.make((t, (1-2*eta)*x+eta) for t, x in zigzag.nodes)
    generic_contracted = price_general(
        [contracted, contracted.reflected()], [Q(1, 2)]*2)

    return {
        "status": "PASS",
        "known_exact_examples": {
            "stationary_endpoint_pair": first["all_B1_lower"],
            "outward_half_start_pair": second["all_B1_lower"],
        },
        "third_leg_jump_regressions": 3,
        "independent_integer_fraction_intersections": checks,
        "shared_parity_grid": {
            "n": D,
            "physical_clock": str(Q(1, 2*D)),
            "parameter_pairs": len(full_grid),
            "exact_clock_capture_checks": parity_checks,
            "full_grid_matches_complete_arrangement": True,
        },
        "off_arrangement_physical_checks": off_checks,
        "interior_wait_rejected": True,
        "nontrivial_actual_law": report,
        "general_unit_subclass_agrees": True,
        "general_stationary_inner_pair": generic_wait["all_B1_lower"],
        "general_vertex_inverse_chronology_checks": inverse_checks,
        "general_rational_velocity_law": generic,
        "general_contracted_actual_law": generic_contracted,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--law", type=Path)
    parser.add_argument("--general", action="store_true",
                        help="use full line arrangement for rational slopes and interior waits")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--require-separation", action="store_true",
                        help="require an actual-law lower strictly above the frozen unrestricted upper")
    args = parser.parse_args()
    if args.law:
        data = json.loads(args.law.read_text())
        paths, weights = read_law(data, general=args.general)
        report = (price_general if args.general else price_law)(paths, weights)
        if "claim_lower" in data:
            assert Q(report["all_B1_lower"]) >= Q(data["claim_lower"])
    else:
        assert not args.require_separation, "--require-separation requires --law"
        report = tests()
    if args.require_separation:
        benchmark = Q(291849329389899, 204800000000000)
        margin = Q(report["all_B1_lower"])-benchmark
        assert margin > 0, "actual law does not strictly separate W1 from U*"
        report["strict_separation_margin"] = str(margin)
    text = json.dumps(report, indent=2, sort_keys=True)+"\n"
    if args.output:
        args.output.write_text(text)
    print(text, end="")


if __name__ == "__main__":
    main()

