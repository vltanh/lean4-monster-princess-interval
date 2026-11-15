#!/usr/bin/env python3
"""Exact finite-target exhaustion for a front-one projection counterexample.

Standard library only.  Every target path is piecewise affine and sticky.
The mathematical capture-order completeness proof is in the companion note.
This is a fixed-law calculation, not a bound on the unrestricted game value.
"""

from __future__ import annotations

import argparse
from fractions import Fraction as Q
from hashlib import sha256
from itertools import permutations
import json
from pathlib import Path


SOURCE_RADII = (
    ((Q(0), Q(1, 20)), (Q(21, 20), Q(1, 20)), (Q(2), Q(1))),
    ((Q(0), Q(4, 5)), (Q(13, 20), Q(3, 20)),
     (Q(17, 20), Q(3, 20)), (Q(17, 10), Q(1))),
    ((Q(0), Q(19, 20)), (Q(1, 20), Q(19, 20)),
     (Q(1, 10), Q(1))),
)
RADIAL_WEIGHTS = (Q(1, 10), Q(7, 10), Q(1, 5))


def position(path, t):
    t = Q(t)
    assert t >= 0
    for (s, y), (e, z) in zip(path, path[1:]):
        if s <= t <= e:
            return y + (z - y) * (t - s) / (e - s)
    assert t >= path[-1][0]
    return path[-1][1]


def validate_radial_law(radials):
    assert sum(RADIAL_WEIGHTS) == 1
    for path in radials:
        assert path[0][0] == 0 and path[-1][1] == 1
        for (s, y), (e, z) in zip(path, path[1:]):
            assert 0 <= y <= 1 and 0 <= z <= 1
            assert s < e and abs(z - y) <= e - s
    knots = sorted({t for path in radials for t, _ in path})
    for t in knots:
        values = [position(path, t) for path in radials]
        assert values == sorted(values)
    return len(knots)


def complete_at_front_one(path):
    """First t+r(t)=1, followed by the legal maximal outward suffix."""
    if path[0][1] == 1:
        return ((Q(0), Q(1)),), Q(0)
    for (s, y), (e, z) in zip(path, path[1:]):
        if e + z >= 1:
            speed = (z - y) / (e - s)
            assert 1 + speed > 0
            hit = s + (1 - s - y) / (1 + speed)
            assert s <= hit <= e
            radius = 1 - hit
            result = [(t, x) for t, x in path if t < hit]
            result.append((hit, radius))
            if radius < 1:
                result.append((2 * hit, Q(1)))
            return tuple(result), hit
    raise AssertionError("front must have been hit before endpoint arrival")


def signed_targets(radials):
    return tuple(tuple((t, sign * x) for t, x in path)
                 for path in radials for sign in (1, -1))


def earliest_contact(path, time, x):
    """First contact reachable from (time,x) at speed at most one.

    On each target segment solve both light-cone boundary equations.
    If an entire segment boundary is already reachable, use its left end.
    The last appended constant segment is long enough to guarantee contact.
    """
    time, x = Q(time), Q(x)
    last_time, endpoint = path[-1]
    end = max(time, last_time) + 2
    extended = path + ((end, endpoint),)
    for (s, y), (e, z) in zip(extended, extended[1:]):
        if e < time:
            continue
        lo = max(s, time)
        speed = (z - y) / (e - s)
        intercept = y - speed * s
        if abs(speed * lo + intercept - x) <= lo - time:
            return lo, speed * lo + intercept
        candidates = []
        for direction in (-1, 1):
            denominator = speed - direction
            if denominator:
                hit = (x - direction * time - intercept) / denominator
                if lo <= hit <= e:
                    candidates.append(hit)
        if candidates:
            hit = min(candidates)
            value = speed * hit + intercept
            assert abs(value - x) <= hit - time
            return hit, value
    raise AssertionError("sticky target must be reachable")


def exhaust_orders(radials):
    targets = signed_targets(radials)
    weights = tuple(w / 2 for w in RADIAL_WEIGHTS for _ in range(2))
    by_start = {}
    best = None
    count = 0
    for order in permutations(range(len(targets))):
        count += 1
        time = Q(0)
        x = targets[order[0]][0][1]
        planned = [Q(0)] * len(targets)
        route = [(time, x)]
        for target in order[1:]:
            time, x = earliest_contact(targets[target], time, x)
            planned[target] = time
            route.append((time, x))
        value = sum(w * t for w, t in zip(weights, planned))
        item = (value, order, tuple(planned), tuple(route))
        if best is None or item < best:
            best = item
        first = order[0]
        if first not in by_start or value < by_start[first]:
            by_start[first] = value
    assert count == 720
    assert best is not None
    for i in (0, 2, 4):
        assert by_start[i] == by_start[i + 1]
    return best, by_start, count


def first_hit_on_monster(target, monster):
    """Independent chronological intersection, not pursuit-cone pricing."""
    deadline = monster[-1][0]
    cuts = sorted({Q(0), deadline}
                  | {t for t, _ in target if t <= deadline}
                  | {t for t, _ in monster})
    for left, right in zip(cuts, cuts[1:]):
        delta_left = position(monster, left) - position(target, left)
        if delta_left == 0:
            return left
        delta_right = position(monster, right) - position(target, right)
        if delta_left * delta_right <= 0:
            hit = left - delta_left * (right - left) / (delta_right - delta_left)
            assert left <= hit <= right
            return hit
    if position(monster, deadline) == position(target, deadline):
        return deadline
    raise AssertionError("displayed complete route missed a target")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    source_knots = validate_radial_law(SOURCE_RADII)
    completed = [complete_at_front_one(path) for path in SOURCE_RADII]
    projected = tuple(path for path, _ in completed)
    projected_knots = validate_radial_law(projected)
    assert projected[1:] == SOURCE_RADII[1:]
    assert projected[0] == ((Q(0), Q(1, 20)),
                            (Q(19, 20), Q(1, 20)),
                            (Q(19, 10), Q(1)))
    monster = ((Q(0), Q(4, 5)), (Q(1, 5), Q(1)),
               (Q(11, 5), Q(-1)))
    report = {
        "format": "front-one-projection-counterexample-v1",
        "source_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
        "radial_weights": [str(w) for w in RADIAL_WEIGHTS],
        "source_radii": [[[str(t), str(x)] for t, x in p] for p in SOURCE_RADII],
        "front_hit_times": [str(t) for _, t in completed],
        "projected_radii": [[[str(t), str(x)] for t, x in p] for p in projected],
        "ordered_law_knot_checks": source_knots + projected_knots,
        "attaining_monster": [[str(t), str(x)] for t, x in monster],
        "cases": {},
        "scope": "Exact six-target fixed-law security; not a game-value bound or a high-security counterexample.",
    }
    for label, radials, expected in (("source", SOURCE_RADII, Q(47, 40)),
                                      ("projected", projected, Q(469, 400))):
        best, starts, count = exhaust_orders(radials)
        assert best[0] == expected
        hits = [first_hit_on_monster(p, monster) for p in signed_targets(radials)]
        direct = sum(RADIAL_WEIGHTS[i] * (hits[2*i] + hits[2*i+1]) / 2
                     for i in range(3))
        assert direct == expected
        report["cases"][label] = {
            "capture_orders": count,
            "exact_security": str(expected),
            "best_initial_target_order": list(best[1]),
            "planned_hits_for_best_order": [str(t) for t in best[2]],
            "minimum_by_positive_initial_target": [str(starts[i]) for i in (0, 2, 4)],
            "independent_displayed_route_hits": [str(t) for t in hits],
            "independent_displayed_route_cost": str(direct),
        }
    assert Q(47, 40) - Q(469, 400) == Q(1, 400)
    report["strict_security_loss"] = "1/400"
    report["status"] = "PASS"
    text = json.dumps(report, indent=2) + "\n"
    if args.output:
        args.output.write_text(text)
    print(text, end="")


if __name__ == "__main__":
    main()
