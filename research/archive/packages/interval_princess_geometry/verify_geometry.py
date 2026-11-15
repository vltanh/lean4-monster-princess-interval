#!/usr/bin/env python3
"""Exact audit of the 338-path seed's two contact fronts and support ceiling.

Standard library only. No LP, floating-point pruning, or sampled Monster bank
is used to prove a lower bound. The unrestricted minima are replayed by the
existing exhaustive oracle; all displayed direct-route payoffs, legality,
uniform path distances and the fixed-support upper are independently checked
here with Fraction arithmetic.
"""
from __future__ import annotations

import argparse
from bisect import bisect_right
from collections import Counter
from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "packages/interval_uniform_reduction/princess_strategy.json"
DUAL = ROOT / "packages/interval_uniform_reduction/rejected_dual.json"
sys.path.insert(0, str(SOURCE.parent))
from exact_response import solve  # existing all-Monster finite capture-order oracle


class Polygon:
    def __init__(self, vertices, scale):
        assert vertices and vertices[0][0] == 0 and scale > 0
        self.t = [Q(t, scale) for t, x in vertices]
        self.x = [Q(x, scale) for t, x in vertices]
        assert all(-1 <= x <= 1 for x in self.x)
        assert all(a < b for a, b in zip(self.t, self.t[1:]))
        self.v = [(y - x) / (b - a) for a, b, x, y in
                  zip(self.t, self.t[1:], self.x, self.x[1:])]
        assert all(abs(v) <= 1 for v in self.v)

    def at(self, t):
        k = bisect_right(self.t, t) - 1
        return (self.x[k] if k + 1 == len(self.t) else
                self.x[k] + self.v[k] * (t - self.t[k]))

    def reflected(self):
        return Polygon(list(zip(self.t, [-x for x in self.x])), 1)


def first_capture(m, p):
    """Intersect polygons directly, independently of characteristic hit code."""
    previous = None
    for t in sorted(set(m.t + p.t)):
        difference = m.at(t) - p.at(t)
        if difference == 0:
            return t
        if previous is not None:
            a, old_difference = previous
            if difference * old_difference < 0:
                return a + (t-a) * abs(old_difference) / (
                    abs(old_difference) + abs(difference))
        previous = t, difference
    raise AssertionError("A listed Princess was not captured")


def ordered(paths):
    for a, b in zip(paths, paths[1:]):
        assert all(a.at(t) <= b.at(t) for t in set(a.t + b.t))


def expectation(paths, weights, monster):
    return sum(w * (first_capture(monster, p) +
                    first_capture(monster, p.reflected()))
               for p, w in zip(paths, weights)) / (2 * sum(weights))


def snap(raw, scale):
    """Nearest 1/128 knot coordinates, exact round-half-to-even convention."""
    result = []
    for path in raw:
        snapped = []
        for t, x in path:
            vertex = [round(Q(128*t, scale)), round(Q(128*x, scale))]
            if not snapped or vertex != snapped[-1]:
                snapped.append(vertex)
        result.append(snapped)
    return result


def describe(paths, weights):
    total = sum(weights)
    center = sum(w for p, w in zip(paths, weights) if p.at(Q(1)) == 0)
    mean_radius = sum(w * p.at(Q(1)) for p, w in zip(paths, weights)) / total
    return {
        "center_atom_at_time_1": str(Q(center, total)),
        "mean_absolute_position_at_time_1": str(mean_radius),
        "two_sweep_center_atom_upper": str(Q(3, 2) - Q(center, 2*total) - mean_radius/4),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    data = json.loads(SOURCE.read_text())
    dual = json.loads(DUAL.read_text())
    raw, weights, scale = data["paths_h"], data["weights_h"], data["S"]
    assert len(raw) == len(weights) == 169
    assert all(isinstance(w, int) and w > 0 for w in weights)
    assert sum(weights) == 100_000_000
    original = [Polygon(p, scale) for p in raw]
    ordered(original)
    assert all(min(p.x) > 0 and p.at(Q(2)) == 1 for p in original)
    snapped_raw = snap(raw, scale)
    snapped = [Polygon(p, 128) for p in snapped_raw]
    ordered(snapped)

    # Two piecewise-affine graphs have maximal distance at a joint knot.
    max_distance = max(abs(p.at(t) - q.at(t)) for p, q in
                       zip(original, snapped) for t in set(p.t + q.t))
    assert max_distance == Q(3, 100_000)
    sweep = Polygon([[0, -1], [2, 1]], 1)
    original_sweep = expectation(original, weights, sweep)
    snapped_sweep = expectation(snapped, weights, sweep)
    assert original_sweep == Q(18145150023847037, 12800000000000000)
    assert snapped_sweep == Q(3977106327, 3200000000)

    def replay(hiders, hscale):
        complete = [[[t, -x] for t, x in p] for p in hiders[::-1]] + hiders
        return solve(complete, weights[::-1] + weights, hscale)

    original_lower, original_route, original_stats = replay(raw, scale)
    assert original_lower == Q(data["value"])
    assert expectation(original, weights, Polygon(original_route, scale)) == original_lower
    # Doubling coordinates keeps every opposite-direction hit integral.
    doubled = [[[2*t, 2*x] for t, x in p] for p in snapped_raw]
    snapped_lower, snapped_route, snapped_stats = replay(doubled, 256)
    assert snapped_lower == snapped_sweep
    assert expectation(snapped, weights, Polygon(snapped_route, 256)) == snapped_lower

    # A genuine Monster law gives an upper for every mixture on this support.
    # The same law has a known unrestricted counterexample; no global upper
    # is asserted here. Symmetry makes the per-path value equal for +/-p.
    monsters = [Polygon(m, dual["scale"]) for m in dual["monsters"]]
    monster_weights = dual["pair_weights"]
    assert len(monsters) == len(monster_weights) == 164
    assert all(isinstance(w, int) and w > 0 for w in monster_weights)
    assert sum(monster_weights) == 1_000_000_000
    column_payoffs = []
    for p in original:
        value = sum(w * (first_capture(m, p) + first_capture(m, p.reflected()))
                    for m, w in zip(monsters, monster_weights)) / (2 * sum(monster_weights))
        column_payoffs.append(value)
    support_upper = max(column_payoffs)
    assert support_upper == Q(362903002466223591, 256000000000000000)
    support_gap = support_upper - original_lower
    assert support_gap == Q(4727252621, 256000000000000000)

    signed_losses = {}
    for sign, label in [(1, "positive_half"), (-1, "negative_half")]:
        old = original if sign == 1 else [p.reflected() for p in original]
        new = snapped if sign == 1 else [p.reflected() for p in snapped]
        old_mean = sum(w * first_capture(sweep, p) for p, w in zip(old, weights))/sum(weights)
        new_mean = sum(w * first_capture(sweep, p) for p, w in zip(new, weights))/sum(weights)
        affected = sum(w for p, q, w in zip(old, new, weights)
                       if first_capture(sweep, p)-first_capture(sweep, q) > Q(1, 100))
        signed_losses[label] = {
            "old_conditional_mean_capture": str(old_mean),
            "snapped_conditional_mean_capture": str(new_mean),
            "contribution_to_unconditional_sweep_loss": str((old_mean-new_mean)/2),
            "conditional_mass_with_loss_above_1_100": str(Q(affected, sum(weights))),
        }

    init = Counter()
    for p, w in zip(original, weights):
        init[p.x[0]] += w
    inward_quarter = sum(w for p, w in zip(original, weights)
                         if p.v[bisect_right(p.t, Q(1, 4))-1] == -1)
    outgoing_leads = []
    for p in original:
        endpoint_time = next(t for t, x in zip(p.t, p.x) if x == 1)
        outgoing_leads.append(1-max(t-x for t, x in zip(p.t, p.x)
                                    if t <= endpoint_time))
    assert Q(inward_quarter, sum(weights)) == Q(79632761, 100000000)
    assert min(outgoing_leads) == Q(3, 100000)
    assert len(init) == 125
    report = {
        "schema": "princess-contact-geometry-v1",
        "source_sha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
        "restricted_dual_sha256": hashlib.sha256(DUAL.read_bytes()).hexdigest(),
        "positive_support_size": len(raw),
        "distinct_positive_initial_positions": len(init),
        "endpoint_mass_each": str(Q(init[Q(1)], 2*sum(weights))),
        "positive_half_inward_mass_at_time_1_4": str(Q(inward_quarter, sum(weights))),
        "minimum_outgoing_lead_before_first_endpoint": str(min(outgoing_leads)),
        "positive_half_minimum_radius": str(min(min(p.x) for p in original)),
        "positive_half_endpoint_mass_at_time_2": "1",
        "original_all_monster_lower": str(original_lower),
        "original_search": original_stats,
        "fixed_support_upper": str(support_upper),
        "fixed_support_upper_argmax_positive_index": column_payoffs.index(support_upper),
        "fixed_support_room_above_current_lower": str(support_gap),
        "fixed_support_column_payoffs": [str(v) for v in column_payoffs],
        "snapping_mesh": "1/128",
        "uniform_path_distance": str(max_distance),
        "snapped_all_monster_value": str(snapped_lower),
        "snapped_search": snapped_stats,
        "security_loss_from_snapping": str(original_lower-snapped_lower),
        "original_endpoint_sweep": str(original_sweep),
        "snapped_endpoint_sweep": str(snapped_sweep),
        "sweep_loss_decomposition": signed_losses,
        "original_time_1": describe(original, weights),
        "snapped_time_1": describe(snapped, weights),
        "status": "PASS",
    }
    encoded = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(encoded)
    print(encoded, end="")


if __name__ == "__main__":
    main()
