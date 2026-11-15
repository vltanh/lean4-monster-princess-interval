#!/usr/bin/env python3
"""Replay packed native witnesses and optionally compare the old oracle.

--reference-source is an optional archival source, not a dependency of normal
replay. Exact Fraction integration checks every emitted physical witness.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import struct
import subprocess
import tempfile
import time

from test_price_normalized import binary_input, order_profile, replay_route

HERE = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, default=HERE / "price_normalized.cpp")
    parser.add_argument("--reference-source", type=Path)
    parser.add_argument("--input", type=Path, action="append", default=[])
    parser.add_argument("--output", type=Path, default=HERE / "bounded_witness_comparison.json")
    args = parser.parse_args()
    with tempfile.TemporaryDirectory(prefix="bounded-witness-") as directory:
        directory = Path(directory)
        binaries = {}
        for name, source in (("bounded", args.source), ("reference", args.reference_source)):
            if source is None:
                continue
            binary = directory / name
            done = subprocess.run(["g++", "-O3", "-std=c++17", "-Wall", "-Wextra",
                                   str(source), "-o", str(binary)], text=True, capture_output=True, check=True)
            if done.stderr:
                raise AssertionError("compiler diagnostics: " + done.stderr)
            binaries[name] = binary
        inputs = []
        for index, seeds in enumerate(([], [(0, 2, 37)], [(1, 1, 67), (7, 1, 29)])):
            n, D = 2, 101
            field = order_profile(n, D, seeds)
            filename = directory / f"small_{index}.bin"
            binary_input(filename, n, D, field)
            inputs.append(filename)
        inputs += args.input
        cases = []
        for filename in inputs:
            content = filename.read_bytes()
            version, n, D = struct.unpack_from("<IIQ", content)
            assert version == 1 and len(content) == 16 + 8 * (12*n+1) * (2*n+1)
            field = [list(struct.unpack_from("<" + "Q" * (2*n+1), content, 16+8*(2*n+1)*j))
                     for j in range(12*n+1)]
            case = {"n": n, "input_sha256": hashlib.sha256(content).hexdigest(), "runs": []}
            minimum = None
            for keep in (0, 1, 48):
                begin = time.monotonic()
                answer = json.loads(subprocess.check_output([str(binaries["bounded"]), str(filename), str(keep)], text=True))
                seconds = time.monotonic() - begin
                if minimum is None:
                    minimum = answer["minimum_units"]
                assert answer["minimum_units"] == minimum
                assert answer["witness_storage"] == "packed current-layer prefixes"
                if keep == 0:
                    assert answer["paths"] == [] and answer["peak_packed_trace_bytes"] == 0
                maximum_prefix = 0
                for route in answer["paths"]:
                    replay_route(n, D, field, route)
                    x = route["start_grid"]
                    first = 0 if abs(x) == 2*n else None
                    for j, step in enumerate(route["moves"], 1):
                        x += step
                        if first is None and abs(x) == 2*n:
                            first = j
                    maximum_prefix = max(maximum_prefix, min(first, 4*n))
                run = {"keep": keep, "minimum_units": minimum, "seconds": seconds,
                       "routes_fraction_replayed": len(answer["paths"]),
                       "maximum_witness_prefix_steps": maximum_prefix,
                       "peak_packed_trace_bytes": answer["peak_packed_trace_bytes"],
                       "retained_states": answer["retained_states"], "maximum_layer": answer["maximum_layer"]}
                if "reference" in binaries:
                    begin = time.monotonic()
                    old = json.loads(subprocess.check_output([str(binaries["reference"]), str(filename), str(keep)], text=True))
                    run["reference_seconds"] = time.monotonic() - begin
                    assert all(answer[key] == value for key, value in old.items()), "original search or witnesses changed"
                    run["all_original_output_fields_identical"] = True
                case["runs"].append(run)
            cases.append(case)
    report = {"status": "PASS", "scope": "Every packed witness independently Fraction-replayed; value-only and witness minima agree. Optional old-source comparison includes all routes and every search/pruning count.",
              "source_sha256": hashlib.sha256(args.source.read_bytes()).hexdigest(), "cases": cases}
    if args.reference_source:
        report["reference_source_sha256"] = hashlib.sha256(args.reference_source.read_bytes()).hexdigest()
    args.output.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({"status": "PASS", "cases": len(cases),
                      "runs": sum(len(case["runs"]) for case in cases),
                      "routes_replayed": sum(run["routes_fraction_replayed"] for case in cases for run in case["runs"])}))


if __name__ == "__main__":
    main()
