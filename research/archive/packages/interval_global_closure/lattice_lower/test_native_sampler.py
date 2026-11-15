#!/usr/bin/env python3
"""Native all-entry regression of the NumPy lattice source-field sampler.

This is an optional native regression, not a required standard-library CI
dependency. It constructs legal rational characteristic P1 fixtures, compares
every sampled entry with independent Fraction triangle barycentric evaluation,
and runs the complete C++ wrapper on a constant-endpoint fixture.
"""
from __future__ import annotations

import argparse
from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path
import platform
import tempfile

import numpy as np

from verify_integer_lattice import ExactField, exact_sample, verify


def require(ok, message):
    if not ok:
        raise AssertionError(message)


def cdf(t, x, components):
    if x == 0:
        return Q(1, 2)
    radial = Q(0)
    for weight, lo, hi, release in components:
        if lo is None:
            continue
        shift = max(Q(0), t - release)
        radial += weight * max(Q(0), min(Q(1), (abs(x) - shift - lo) / (hi - lo)))
    return Q(1, 2) + (Q(1, 2) if x > 0 else Q(-1, 2)) * radial


FIXTURES = (
    ("constant_endpoints", ((Q(1), None, None, Q(0)),)),
    ("stationary_uniform_until_two", ((Q(1), Q(0), Q(1), Q(2)),)),
    ("three_component_mixture", (
        (Q(1, 7), None, None, Q(0)),
        (Q(2, 7), Q(0), Q(2, 3), Q(1, 2)),
        (Q(4, 7), Q(1, 5), Q(4, 5), Q(2)),
    )),
)


def write_field(path, H, components):
    h, last = Q(1, H), Q(5)
    lo, hi = -H, 6 * H
    points = [(i, j) for i in range(lo, hi + 1) for j in range(lo, hi + 1)
              if 0 <= i + j <= 10 * H and abs(i - j) <= 2 * H]
    points.sort(key=lambda p: (p[0] + p[1], p[0] - p[1]))
    values = [cdf((i + j) * h / 2, (i - j) * h / 2, components)
              for i, j in points]
    payload = {
        "mesh_kind": "light", "center_aligned": True, "step": str(h),
        "mesh_horizon": 5, "outward_horizon": 2, "absorption_horizon": 3,
        "signed_cdf_nodal": [str(v) for v in values],
    }
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    return points, values


def check_all_entries(field, refinement):
    B, D, table = exact_sample(field, refinement)
    count, before_absorption, even_parity, odd_parity = 0, 0, 0, 0
    for n in range(6 * B + 1):
        for j in range(-B, B + 1):
            actual = Q(int(table[n, j + B]), D)
            expected = field.value(Q(n, B), Q(j, B))
            require(actual == expected,
                    "all-entry mismatch r={} n={} j={}: {} != {}".format(
                        refinement, n, j, actual, expected))
            count += 1
            before_absorption += n < 3 * B
            even_parity += (n + j) % 2 == 0
            odd_parity += (n + j) % 2 != 0
    require(count == table.size, "all sampled entries compared")
    require(even_parity and odd_parity, "both physical sampling parities checked")
    return {
        "refinement": refinement, "B": B, "cdf_denominator": D,
        "entries_compared": count, "entries_before_absorption": before_absorption,
        "even_parity_entries": even_parity, "odd_parity_entries": odd_parity,
        "raw_table_sha256": hashlib.sha256(
            table.astype("<u8", copy=False).tobytes()).hexdigest(),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path,
                        default=Path(__file__).with_name("native_sampler_replay.json"))
    args = parser.parse_args()
    report = {
        "scope": "Exact all-entry sampler regression and easy full native wrapper fixture; no improved unrestricted game bound.",
        "python": platform.python_version(), "numpy": np.__version__,
        "fixtures": [], "wrapper_fixtures": [],
    }
    source_dir = Path(__file__).resolve().parent
    report["sampler_source_sha256"] = hashlib.sha256(
        (source_dir / "verify_integer_lattice.py").read_bytes()).hexdigest()
    report["verifier_source_sha256"] = hashlib.sha256(
        (source_dir / "verify_integer_lattice.cpp").read_bytes()).hexdigest()
    with tempfile.TemporaryDirectory(prefix="lattice-sampler-regression-") as tmp:
        directory = Path(tmp)
        endpoint_fields = {}
        for H in (2, 3):
            for name, components in FIXTURES:
                path = directory / "{}_H{}.json".format(name, H)
                points, values = write_field(path, H, components)
                field = ExactField(path)
                require(field.points == points and field.values == values,
                        "fixture metadata/nodal ordering")
                # Independent evaluator must recover every supplied node too.
                for (i, j), value in zip(points, values):
                    t, x = Q(i + j, 2 * H), Q(i - j, 2 * H)
                    require(field.value(t, x) == value, "nodal Fraction evaluator")
                kinds = {"center_diagonal": 0, "ordinary_diagonal": 0, "boundary": 0}
                for (i, j), triangles in field.cells.items():
                    kinds["boundary" if len(triangles) == 1 else
                          "center_diagonal" if i == j else "ordinary_diagonal"] += 1
                require(all(kinds.values()), "fixture exercises every triangle family")
                item = {
                    "name": name, "H": H, "field_sha256": hashlib.sha256(
                        path.read_bytes()).hexdigest(), "nodes_checked": len(points),
                    "triangle_families": kinds,
                    "refinements": [check_all_entries(field, r) for r in (1, 2, 3)],
                }
                report["fixtures"].append(item)
                if name == "constant_endpoints":
                    endpoint_fields[H] = path
        for H, refinement in ((2, 3), (3, 2)):
            result = verify(endpoint_fields[H], directory / "wrapper_H{}.json".format(H),
                            refinement=refinement, keep_input=True, quiet=True)
            B = 2 * H * refinement
            require(result["B"] == B, "wrapper grid")
            require(result["rounded_minimum_units"] == result["cost_scale"],
                    "constant endpoint CDF has exact lattice value one")
            require(Q(result["lattice_lower"]) == 1, "wrapper lattice normalization")
            require(Q(result["quantization_penalty"]) == Q(1, B), "wrapper transfer penalty")
            require(Q(result["global_value_lower"]) == 1 - Q(1, B),
                    "wrapper global-value arithmetic")
            require(result["beam_truncations"] == 0, "wrapper uses no beam")
            require(len(result["layer_states"]) == 2 * B, "wrapper completed all layers")
            report["wrapper_fixtures"].append({
                key: result[key] for key in (
                    "B", "n", "refinement", "cdf_denominator", "cost_scale",
                    "rounded_minimum_units", "lattice_lower", "quantization_penalty",
                    "global_value_lower", "beam_truncations", "layer_states",
                    "sampled_table_sha256", "exact_sampling_spot_checks",
                )
            })
    report["total_entries_compared"] = sum(
        r["entries_compared"] for f in report["fixtures"] for r in f["refinements"])
    report["status"] = "passed"
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": report["status"], "fixtures": len(report["fixtures"]),
        "refinements": sum(len(f["refinements"]) for f in report["fixtures"]),
        "entries_compared": report["total_entries_compared"],
        "wrapper_fixtures": len(report["wrapper_fixtures"]), "output": str(args.output),
    }, sort_keys=True))


if __name__ == "__main__":
    main()

