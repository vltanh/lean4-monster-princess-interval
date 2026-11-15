#!/usr/bin/env python3
"""Independent endpoint-release regressions for the integer lattice verifier.

The existing outward-only fixtures do not exercise endpoint atoms which
temporarily shrink. Here an initial endpoint population moves inward until
time 1/2 and then outward. Its persistent endpoint mass is strictly smaller
than its initial endpoint mass. We also mix in a delayed uniform population.

The second checkerboard variant replaces every unused odd-parity table node
by the stationary-endpoint field. Each parity separately obeys the legal
transport inequalities. The searched Monster paths visit only even-parity
nodes; this probes the preceding-row protection in endpoint_floor.

The reference enumerates every normalized path and integrates every edge
with Fraction arithmetic. It reuses no Pareto, pursuit, endpoint-pruning,
or terminal-tour shortcut from C++. Cases at precision 256 compare against
the same independent integral expressed in the enlarged cost units.
"""
from __future__ import annotations

import argparse
from fractions import Fraction as Q
import json
from math import lcm
from pathlib import Path
import subprocess
import tempfile

from test_integer_lattice import (
    assert_fixture_axioms,
    brute_force,
    require,
    write_table,
)


def clipped(q):
    return max(Q(0), min(Q(1), q))


def endpoint_release_table(B, mixed, odd_stationary):
    """Exact interior signed CDF traces, with no atom at the center.

    Release component: R(t,a)=min(1,a+s(t)), a uniform on [1,2],
    s(t)=-t up to 1/2 and s(t)=t-1 afterward. Its whole initial
    population is at the endpoint; the endpoint fraction decreases to
    1/2, then increases to one. Radii remain at least 1/2.

    In the mixed case this component has weight 1/3, and the other 2/3
    has R(t,a)=min(1,a+max(0,t-1/2)), a uniform on [0,1].
    Both components are 1-Lipschitz, outward after time 2 and absorbed
    before time 3. Fair reflection gives the signed CDF below.
    """
    fractions = []
    D = 2
    for n in range(6 * B + 1):
        t = Q(n, B)
        shift = -t if t <= Q(1, 2) else t - 1
        outward_shift = max(Q(0), t - Q(1, 2))
        row = []
        for j in range(2 * B + 1):
            x = Q(j - B, B)
            if x == 0 or (odd_stationary and (n + j) % 2):
                f = Q(1, 2)
            else:
                radial = clipped(abs(x) - shift - 1)
                if mixed:
                    uniform = clipped(abs(x) - outward_shift)
                    radial = (radial + 2 * uniform) / 3
                f = Q(1, 2) + (Q(1, 2) if x > 0 else -Q(1, 2)) * radial
            row.append(f)
            D = lcm(D, f.denominator)
        fractions.append(row)
    table = [[int(f * D) for f in row] for row in fractions]
    assert_fixture_axioms(B, D, table)
    return D, table


def run_case(binary, directory, B, mixed, odd_stationary, precision):
    D, table = endpoint_release_table(B, mixed, odd_stationary)
    label = "{}_B{}_odd{}_P{}".format(
        "mixed_release" if mixed else "endpoint_release",
        B, int(odd_stationary), precision)
    source = directory / (label + ".bin")
    output = directory / (label + ".json")
    write_table(source, B, D, table)
    # This changes only the units of the independent Fraction integral:
    # (precision*a)/(precision*D)=a/D, while C becomes 2*D*B*precision.
    reference = brute_force(
        B, D * precision,
        [[a * precision for a in row] for row in table])
    run = subprocess.run(
        [str(binary), str(source), str(output), str(precision)],
        text=True, capture_output=True, timeout=60)
    require(run.returncode == 0,
            "{}: verifier exit {}\n{}".format(label, run.returncode, run.stderr))
    result = json.loads(output.read_text())
    require(result["cost_precision"] == precision, label + ": precision metadata")
    require(result["cdf_denominator"] == D, label + ": CDF denominator")
    require(result["cost_scale"] == 2 * D * B * precision, label + ": cost units")
    require(result["rounding_budget_units"] == 12 * B,
            label + ": rounding budget must not be multiplied by precision")
    require(result["rounded_minimum_units"] == reference["rounded_minimum_units"],
            "{}: C++ {} differs from exhaustive Fraction {}".format(
                label, result["rounded_minimum_units"],
                reference["rounded_minimum_units"]))
    require(result["beam_truncations"] == 0, label + ": no beam")
    require(len(result["layer_states"]) == 2 * B, label + ": complete horizon")
    return {
        "name": label, "B": B, "D": D, "precision": precision,
        "rounded_minimum_units": result["rounded_minimum_units"],
        "exact_minimum_scaled": reference["exact_minimum_scaled"],
        "enumerated_paths": reference["normalized_paths"],
        "maximum_path_rounding_loss": reference["maximum_path_rounding_loss"],
        "bounded_states": result["bounded"],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path,
                        default=Path(__file__).with_name("verify_integer_lattice.cpp"))
    parser.add_argument("--compiler", default="g++")
    args = parser.parse_args()
    report = {
        "scope": "Independent endpoint-release and checkerboard-pruning regressions",
        "arithmetic": "Python fractions.Fraction against integer C++",
        "cases": [],
    }
    with tempfile.TemporaryDirectory(prefix="endpoint-release-regression-") as tmp:
        directory = Path(tmp)
        binary = directory / "verify_integer_lattice"
        build = subprocess.run(
            [args.compiler, "-std=c++17", "-O2", "-Wall", "-Wextra",
             str(args.source), "-o", str(binary)],
            text=True, capture_output=True, timeout=120)
        require(build.returncode == 0, "C++ compilation failed\n" + build.stderr)
        report["compiler_warnings"] = build.stderr
        for B in (2, 4):
            for mixed in (False, True):
                for odd_stationary in (False, True):
                    report["cases"].append(run_case(
                        binary, directory, B, mixed, odd_stationary, 1))
        for odd_stationary in (False, True):
            report["cases"].append(run_case(
                binary, directory, 4, True, odd_stationary, 256))
    report["status"] = "passed"
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
