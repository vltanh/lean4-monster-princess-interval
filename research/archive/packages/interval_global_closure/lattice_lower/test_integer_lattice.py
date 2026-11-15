#!/usr/bin/env python3
"""Independent, standard-library regression for verify_integer_lattice.cpp.

Compile the verifier and compare it with exhaustive Fraction integration of
every normalized grid path for B=2 and B=4.  The reference search has no beam,
dominance, dynamic-programming memoization, pursuit bound, or cost pruning.
It explicitly integrates both endpoint tours at time 2, rather than using
the verifier's closed terminal formula.

Run:
    python3 test_integer_lattice.py
    python3 test_integer_lattice.py --source /path/to/verify_integer_lattice.cpp

The original draft and the precision/endpoint-pruning implementation were
compiled and replayed locally on 2026-11-13. This is an independent rational
regression, not a claim of Lean compilation or a remote CI result.
"""
from __future__ import annotations

import argparse
from fractions import Fraction
import json
from math import gcd
from pathlib import Path
import struct
import subprocess
import tempfile

Q = Fraction
ZERO = Q(0)
ONE = Q(1)
HALF = Q(1, 2)
UINT64_MAX = (1 << 64) - 1


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def lcm(a, b):
    return a // gcd(a, b) * b


def clamp01(q):
    return max(ZERO, min(ONE, q))


# A component is (weight, lower initial radius, upper initial radius,
# release time).  None as the lower radius denotes an endpoint atom.
FIXTURES = (
    ("endpoint_only", ((ONE, None, None, ZERO),)),
    ("uniform_immediate", ((ONE, ZERO, ONE, ZERO),)),
    ("two_releases", (
        (HALF, ZERO, HALF, ONE),
        (HALF, Q(1, 3), ONE, Q(2)),
    )),
    ("endpoint_and_released_annulus", (
        (Q(1, 3), None, None, ZERO),
        (Q(2, 3), Q(1, 4), Q(3, 4), HALF),
    )),
    # This fixture has a fractional-cost minimizing grid path at B=4:
    # D=48, exact minimum=10127/24 scaled units, rounded minimum=421.
    ("early_two_annuli", (
        (Q(3, 8), Q(5, 8), Q(3, 4), Q(1, 4)),
        (Q(5, 8), Q(3, 8), Q(3, 4), Q(1, 4)),
    )),
)


def cdf_value(t, x, components, speed=ONE):
    """Interior signed CDF trace of a symmetric outward radial mixture."""
    if x == 0:
        return HALF
    radial = ZERO
    for weight, lo, hi, release in components:
        if lo is not None:
            shift = speed * max(ZERO, t - release)
            radial += weight * clamp01((abs(x) - shift - lo) / (hi - lo))
    return HALF + (HALF if x > 0 else -HALF) * radial


def make_table(B, components, scale=1, speed=ONE):
    require(sum(c[0] for c in components) == ONE, "mixture mass")
    fractions = [
        [cdf_value(Q(n, B), Q(j - B, B), components, speed)
         for j in range(2 * B + 1)]
        for n in range(6 * B + 1)
    ]
    base = 2
    for row in fractions:
        for q in row:
            base = lcm(base, q.denominator)
    D = base * scale
    require(32 * D * B <= UINT64_MAX // 2, "fixture exceeds verifier bounds")
    table = [[int(q * D) for q in row] for row in fractions]
    return D, table


def write_table(path, B, D, table):
    with path.open("wb") as handle:
        handle.write(struct.pack("<IIIIQ", 1, B, 6 * B + 1, 2 * B + 1, D))
        for row in table:
            handle.write(struct.pack("<" + "Q" * len(row), *row))


def assert_fixture_axioms(B, D, table, outward=True):
    """Check fixture hypotheses independently of the C++ parser."""
    for n, row in enumerate(table):
        for j, a in enumerate(row):
            require(0 <= a <= D, "fixture range")
            require(a + row[2 * B - j] == D, "fixture symmetry")
            if n >= 3 * B:
                require(a == D // 2, "fixture absorption by time 3")
            if n + 1 == len(table):
                continue
            if j:
                require(table[n + 1][j - 1] <= a, "fixture left transport")
            if j < 2 * B:
                require(table[n + 1][j + 1] >= a, "fixture right transport")
            if outward and n >= 2 * B:
                if B <= j < 2 * B:
                    require(table[n + 1][j + 1] == a,
                            "fixture positive outward equality")
                if 0 < j <= B:
                    require(table[n + 1][j - 1] == a,
                            "fixture negative outward equality")


def brute_force(B, D, table, cost_precision=1, decision_cutoff=2):
    """Enumerate normalized paths; integrate every individual edge exactly."""
    require(type(cost_precision) is int and cost_precision > 0,
            "positive integer cost precision")
    require(decision_cutoff in (1, 2), "decision cutoff one or two")
    C = 2 * D * B * cost_precision
    F = [[Q(a, D) for a in row] for row in table]
    stats = {
        "normalized_paths": 0,
        "late_center_paths_rejected": 0,
        "prefix_edges": 0,
        "tail_edges": 0,
        "partial_record_crossings": 0,
        "maximum_crossing_square_bits": 0,
    }
    minimum_rounded = None
    minimum_exact = None
    maximum_loss = ZERO

    def clock_edge(record, a, b):
        # Integrate the capped running minimum as a polygon in the unit
        # edge-time interval.  This deliberately does not use the C++
        # integer ceiling formula.
        record = min(record, a)
        if b >= record:
            area = record
        else:
            require(a > b, "decreasing edge at a record crossing")
            if a == record:
                area = (a + b) / 2
            else:
                crossing_time = (a - record) / (a - b)
                require(0 < crossing_time < 1, "interior record crossing")
                area = (record * crossing_time
                        + (record + b) * (1 - crossing_time) / 2)
                difference = (record - b) * D
                require(difference.denominator == 1, "integral record")
                bits = (difference.numerator ** 2).bit_length()
                stats["partial_record_crossings"] += 1
                stats["maximum_crossing_square_bits"] = max(
                    stats["maximum_crossing_square_bits"], bits)
        exact_units = area * Q(C, B)
        floor_units = exact_units.numerator // exact_units.denominator
        require(0 <= exact_units - floor_units < 1, "one-edge floor error")
        return min(record, b), exact_units, floor_units

    def step(state, direction, tail=False):
        n, j, left, right, exact, rounded, centered = state
        k = j + direction
        require(0 <= k <= 2 * B, "physical edge")
        require(n + 1 < len(table), "fixture horizon")
        left, le, lr = clock_edge(left, F[n][j], F[n + 1][k])
        right, re, rr = clock_edge(right, 1 - F[n][j], 1 - F[n + 1][k])
        if k == 0:
            left = ZERO
        if k == 2 * B:
            right = ZERO
        centered = centered or (k == B and n + 1 <= 2 * B)
        stats["tail_edges" if tail else "prefix_edges"] += 1
        return n + 1, k, left, right, exact + le + re, rounded + lr + rr, centered

    def accept(state):
        nonlocal minimum_rounded, minimum_exact, maximum_loss
        n, j, left, right, exact, rounded, centered = state
        require(j in (0, 2 * B), "completed endpoint tour")
        require(left == right == 0, "both endpoint records removed")
        require(n <= 6 * B, "normalized completion deadline")
        if not centered:
            stats["late_center_paths_rejected"] += 1
            return
        loss = exact - rounded
        require(0 <= loss < 12 * B, "whole-path rounding budget")
        maximum_loss = max(maximum_loss, loss)
        stats["normalized_paths"] += 1
        minimum_rounded = rounded if minimum_rounded is None else min(
            minimum_rounded, rounded)
        minimum_exact = exact if minimum_exact is None else min(
            minimum_exact, exact)

    def finish_to(state, target):
        direction = 1 if target > state[1] else -1
        while state[1] != target:
            state = step(state, direction, tail=True)
        return state

    def visit(state):
        n, j, left, right, exact, rounded, centered = state
        if j in (0, 2 * B):
            accept(finish_to(state, 2 * B - j))
        elif n == decision_cutoff * B:
            if not centered and decision_cutoff == 2:
                stats["late_center_paths_rejected"] += 1
                return
            # At time one an uncentered Monster is positive; under the
            # outward-after-one hypothesis its exact optimal continuation
            # is direct left, then right. We integrate that entire path,
            # rather than reusing the C++ pursuit/terminal formulas.
            first_endpoints = (0, 2 * B) if centered else (0,)
            for first in first_endpoints:
                accept(finish_to(finish_to(state, first), 2 * B - first))
        else:
            # All prefixes, including those which already cannot meet the
            # center deadline, are still enumerated.  No C++ pruning reused.
            visit(step(state, -1))
            visit(step(state, 1))

    for j in range(B, 2 * B + 1, 2):
        visit((0, j, F[0][j], ZERO if j == 2 * B else 1 - F[0][j],
               ZERO, 0, j == B))
    require(minimum_rounded is not None, "nonempty normalized path bank")
    require(minimum_rounded <= minimum_exact, "rounded minimum below true minimum")
    stats.update({
        "rounded_minimum_units": minimum_rounded,
        "exact_minimum_scaled": str(minimum_exact),
        "maximum_path_rounding_loss": str(maximum_loss),
    })
    return stats


def run_valid(binary, directory, label, B, D, table):
    assert_fixture_axioms(B, D, table)
    reference = brute_force(B, D, table)
    source = directory / (label + ".bin")
    output = directory / (label + ".json")
    write_table(source, B, D, table)
    run = subprocess.run([str(binary), str(source), str(output)],
                         text=True, capture_output=True, timeout=60)
    require(run.returncode == 0,
            "{}: C++ exit {}\nstdout={}\nstderr={}".format(
                label, run.returncode, run.stdout, run.stderr))
    got = json.loads(output.read_text())
    require(got["B"] == B and got["n"] == B // 2, label + ": grid metadata")
    require(got["cdf_denominator"] == D and got["cost_scale"] == 2 * D * B,
            label + ": normalization")
    require(got["rounded_minimum_units"] == reference["rounded_minimum_units"],
            "{}: C++ {} differs from exhaustive Fraction {}".format(
                label, got["rounded_minimum_units"],
                reference["rounded_minimum_units"]))
    require(got["beam_truncations"] == 0, label + ": no beam truncation")
    require(got["rounding_budget_units"] == 12 * B, label + ": rounding budget")
    require(len(got["layer_states"]) == 2 * B, label + ": full horizon")
    if label.startswith("endpoint_only"):
        require(got["rounded_minimum_units"] == 2 * D * B,
                label + ": constant endpoint strategy exact value one")
    if label == "early_two_annuli_B4_scale1":
        require(reference["rounded_minimum_units"] == 421,
                label + ": independently checked fractional optimum")
        require(reference["exact_minimum_scaled"] == "10127/24",
                label + ": independently checked exact optimum")
    return {
        "name": label, "B": B, "D": D, "reference": reference,
        "verifier": {key: got[key] for key in (
            "rounded_minimum_units", "generated", "dominated", "bounded",
            "deadline_pruned", "maximum_node_frontier")},
    }


def run_rejection(binary, directory, label, B, D, table, codes):
    source = directory / (label + ".bin")
    output = directory / (label + ".json")
    write_table(source, B, D, table)
    run = subprocess.run([str(binary), str(source), str(output)],
                         text=True, capture_output=True, timeout=30)
    require(run.returncode in codes,
            "{}: expected rejection {}, received {} ({})".format(
                label, sorted(codes), run.returncode, run.stderr))
    require(not output.exists(), label + ": invalid table produced a certificate")
    return {"name": label, "exit_code": run.returncode}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path,
                        default=Path(__file__).with_name("verify_integer_lattice.cpp"))
    parser.add_argument("--compiler", default="g++")
    args = parser.parse_args()
    require(args.source.is_file(), "C++ source file missing: " + str(args.source))
    report = {
        "scope": "Small exhaustive exact regression; no unrestricted-game numerical certificate.",
        "reference_arithmetic": "Python fractions.Fraction; edge-by-edge polygon integration",
        "fixtures": [], "rejections": [],
    }
    with tempfile.TemporaryDirectory(prefix="integer-lattice-regression-") as tmp:
        directory = Path(tmp)
        binary = directory / "verify_integer_lattice"
        command = [args.compiler, "-std=c++17", "-O2", "-Wall", "-Wextra",
                   str(args.source), "-o", str(binary)]
        build = subprocess.run(command, text=True, capture_output=True, timeout=120)
        require(build.returncode == 0,
                "C++ compilation failed\n" + build.stdout + build.stderr)
        report["compiler_warnings"] = build.stderr
        for B in (2, 4):
            for name, components in FIXTURES:
                for scale in (1, 997):
                    D, table = make_table(B, components, scale)
                    label = "{}_B{}_scale{}".format(name, B, scale)
                    report["fixtures"].append(
                        run_valid(binary, directory, label, B, D, table))
        # Large exact CDF integers force the crossing numerator beyond 64
        # bits while remaining well below the verifier's input bound.
        for name, components in FIXTURES[2:]:
            B = 4
            scale = 10 ** 10 + 19
            D, table = make_table(B, components, scale)
            label = "{}_B{}_scale{}".format(name, B, scale)
            report["fixtures"].append(
                run_valid(binary, directory, label, B, D, table))
        require(max(item["reference"]["maximum_crossing_square_bits"]
                    for item in report["fixtures"]) > 64,
                "stress fixtures did not exercise a 128-bit crossing square")
        B = 4
        D, table = make_table(B, FIXTURES[0][1], 997)
        table[1][B - 1] = D
        table[1][B + 1] = 0
        report["rejections"].append(
            run_rejection(binary, directory, "bad_transport", B, D, table, {6, 7}))
        components = ((ONE, HALF, ONE, Q(2)),)
        D, table = make_table(B, components, 997, speed=HALF)
        assert_fixture_axioms(B, D, table, outward=False)
        report["rejections"].append(
            run_rejection(binary, directory, "bad_outward_tail", B, D, table,
                          {11, 12}))
        D, table = make_table(B, FIXTURES[0][1], 997)
        table[0][B] += 1
        report["rejections"].append(
            run_rejection(binary, directory, "bad_symmetry", B, D, table, {5}))
    report["status"] = "passed"
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
