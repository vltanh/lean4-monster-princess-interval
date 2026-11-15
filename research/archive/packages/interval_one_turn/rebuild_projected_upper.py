#!/usr/bin/env python3
"""Rebuild an exact all-Princess upper from a rational physical B1 law.

The JavaScript graph builder and native maximum-flow helper propose the
witness. A separate standard-library Python verifier reconstructs the
physical geometry, rewards, capacities, and integer flow/cut equality.
No floating-point optimizer is used in this reconstruction.
"""
from __future__ import annotations

import argparse
from fractions import Fraction
import gzip
import hashlib
import json
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "interval_integer_flow"))
from native_closure import compile_helper
from verify_projected_upper import reconstruct_geometry, verify_certificate

BENCHMARK = Fraction(291849329389899, 204800000000000)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--law", type=Path,
                        default=HERE / "one_turn_projected_upper.json.gz")
    parser.add_argument("--output", type=Path, required=True,
                        help="directory for the reconstructed certificate and flow helper")
    parser.add_argument("--require-counterexample", action="store_true")
    args = parser.parse_args()
    raw = args.law.read_bytes()
    payload = gzip.decompress(raw) if raw[:2] == b"\x1f\x8b" else raw
    law = json.loads(payload)
    if law.get("format") != "one-turn-rational-law-v1":
        raise ValueError("unexpected saved physical-law format")
    denominator = int(law["weights_denominator"])
    # Reject a nonphysical law before calling the untrusted proposal code.
    reconstruct_geometry(law["atoms"], denominator)
    expected = Fraction(law["exact_upper"])
    args.output.mkdir(parents=True, exist_ok=True)
    draft = args.output / "one_turn_projected_upper.input.json"
    draft.write_text(json.dumps(law, separators=(",", ":")) + "\n")
    binary = compile_helper(args.output)
    certificate = args.output / "one_turn_projected_upper.certificate.json"
    subprocess.run(["node", "--stack-size=16384",
                    str(HERE / "solve_projected_upper.cjs"),
                    str(draft), str(certificate), str(binary)], check=True)
    report = verify_certificate(json.loads(certificate.read_text()))
    actual = Fraction(report["exact_upper"])
    if actual != expected:
        raise ValueError("rebuilt exact upper differs from saved law manifest")
    if args.require_counterexample and actual > BENCHMARK:
        raise ValueError("exact one-turn upper is above the separation benchmark")
    report.update({
        "benchmark": str(BENCHMARK),
        "exact_upper_minus_benchmark": str(actual-BENCHMARK),
        "disproves_strict_separation_target": actual <= BENCHMARK,
        "law_sha256": hashlib.sha256(raw).hexdigest(),
        "law_uncompressed_sha256": hashlib.sha256(payload).hexdigest(),
        "certificate_sha256": hashlib.sha256(certificate.read_bytes()).hexdigest(),
    })
    replay = args.output / "one_turn_projected_upper.python_replay.json"
    replay.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
