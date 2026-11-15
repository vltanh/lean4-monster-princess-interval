#!/usr/bin/env python3
"""Generate and exactly replay the 588-path initial-atom split regression.

This fixture improves the old lower by about 2.37e-9. Its purpose is to test
legal initial mass spreading with the existing unrestricted response oracle;
it does not solve the game or construct an attaining continuous Princess CDF.
"""
from __future__ import annotations

import argparse
from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path

from verify_geometry import SOURCE, Polygon, expectation, ordered, solve

HERE = Path(__file__).resolve().parent
FIXTURE = HERE / "prefix_split_princess.json"


def construct(data):
    raw, weights, scale = data["paths_h"], data["weights_h"], data["S"]
    delta_ticks = 2
    assert scale == 256000000
    groups = []
    for i, p in enumerate(raw):
        if not groups or raw[groups[-1][0]][0][1] != p[0][1]:
            groups.append([])
        groups[-1].append(i)
    starts = [raw[g[0]][0][1] for g in groups]
    assert 0 < delta_ticks < min(starts)
    assert all(b-a > 2*delta_ticks for a, b in zip(starts, starts[1:]))
    assert all(x == scale or x+delta_ticks < scale for x in starts)

    hiders, new_weights = [], []
    for group in groups:
        x = raw[group[0]][0][1]
        # Every original path in this atom is constant on [0, delta].
        for i in group:
            first_motion = next((a for (a, u), (b, v) in
                                 zip(raw[i], raw[i][1:]) if u != v), raw[i][-1][0])
            assert delta_ticks < first_motion
        # Double weights so an initial atom is split in exactly equal halves.
        midpoint = sum(weights[i] for i in group)
        cumulative = 0
        for i in group:
            left, right = cumulative, cumulative + 2*weights[i]
            cumulative = right
            for a, b, direction in [
                (left, min(right, midpoint), -1),
                (max(left, midpoint), right, 1),
            ]:
                if a >= b:
                    continue
                # The positive endpoint atom spreads only inward.
                initial = x + direction*delta_ticks if (x < scale or direction == -1) else x
                path = [[0, initial], [delta_ticks, x]] + [
                    vertex for vertex in raw[i][1:] if vertex[0] > delta_ticks]
                hiders.append(path)
                new_weights.append(b-a)
        assert cumulative == 2*midpoint
    assert len(hiders) == 294
    assert sum(new_weights) == 2*sum(weights) == 200000000
    return hiders, new_weights, delta_ticks


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="write the regenerated exact fixture")
    parser.add_argument("--output", type=Path, help="save the replay report")
    args = parser.parse_args()
    data = json.loads(SOURCE.read_text())
    hiders, weights, delta_ticks = construct(data)
    scale = data["S"]
    positive = [Polygon(p, scale) for p in hiders]
    ordered(positive)
    assert all(min(p.x) > 0 and p.at(Q(2)) == 1 for p in positive)
    raw = [[[t, -x] for t, x in p] for p in hiders[::-1]] + hiders
    all_weights = weights[::-1] + weights
    value, monster, search = solve(raw, all_weights, scale)
    assert value == Q(9072574958621987, 6400000000000000)
    assert expectation(positive, weights, Polygon(monster, scale)) == value
    gain = value-Q(data["value"])
    assert gain == Q(60590851, 25600000000000000) and gain > 0
    fixture = {
        "S": scale,
        "paths_h": hiders,
        "weights_h": weights,
        "weight_total": sum(weights),
        "value": str(value),
        "attaining_monster": monster,
        "search": search,
        "construction": {
            "name": "equal initial-atom rank split and common-time rejoining",
            "source_sha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
            "prefix_ticks": delta_ticks,
            "prefix_time": str(Q(delta_ticks, scale)),
            "positive_interior_starts": "x-delta and x+delta, each half the initial atom mass",
            "positive_endpoint_starts": "1-delta and 1, each half the endpoint atom mass",
            "prefix": "linear interpolation to the original starting point at time delta",
            "tail": "original ordered quantile tail, preserving every marginal after delta",
            "weight_scale_multiplier": 2,
            "scope": "finite atomic regression; no continuous-CDF or equilibrium claim",
        },
    }
    if args.write:
        FIXTURE.write_text(json.dumps(fixture, separators=(",", ":"), sort_keys=True) + "\n")
    else:
        assert json.loads(FIXTURE.read_text()) == fixture, "fixture differs from deterministic reconstruction"
    report = {
        "status": "PASS",
        "source_sha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
        "fixture_sha256": hashlib.sha256(FIXTURE.read_bytes()).hexdigest(),
        "oriented_princess_paths": 2*len(hiders),
        "prefix_time": str(Q(delta_ticks, scale)),
        "all_monster_lower": str(value),
        "gain_above_old_lower": str(gain),
        "independent_attaining_payoff": str(expectation(positive, weights, Polygon(monster, scale))),
        "search": search,
        "scope": "all-Monster lower certificate; tiny numerical gain, retained as a structural regression",
    }
    encoded = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(encoded)
    print(encoded, end="")


if __name__ == "__main__":
    main()
