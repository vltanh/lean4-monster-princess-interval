#!/usr/bin/env python3
"""Complete small-bank replay, immutable retention, and resumed best selection."""
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path[:0] = [str(HERE), str(ROOT / "packages/interval_clock_grid/normalized_native")]
from solve_normalized import Master
from princess_retention import CompleteBankArchive, verify_archive
from verify_native_field import verify


def main():
    with tempfile.TemporaryDirectory(prefix="complete_princess_retention_") as folder:
        folder = Path(folder)
        output = folder / "first"
        output.mkdir()
        metadata = output / "metadata.json"
        metadata.write_text('{"seed":271828,"github_run_id":"small-regression"}\n')
        master = Master(2, output / "work")
        archive = CompleteBankArchive(output)
        good_answer, good_table = master.price(np.zeros(master.K), keep=0)
        good = archive.retain(master, good_table, good_answer, 1, metadata)
        native = verify(output / good["field"])
        assert Fraction(native["exact_bank_dual"]) == Fraction(good["normalized_bank_dual_value"])
        bigint = subprocess.run(["node", str(ROOT / "packages/interval_clock_grid/normalized_record_pricing.cjs"),
                                 str(output / good["field"]), "--target-bound"],
                                check=True, capture_output=True, text=True)
        assert json.loads(bigint.stdout)["status"] == "PASS"
        original = {p: hashlib.sha256(p.read_bytes()).hexdigest()
                    for p in (output / "complete_princess/candidates").rglob("*") if p.is_file()}
        bad_answer, bad_table = master.price(np.ones(master.K), keep=0)
        bad = archive.retain(master, bad_table, bad_answer, 2, metadata)
        assert Fraction(good["normalized_bank_dual_value"]) > Fraction(bad["normalized_bank_dual_value"])
        assert json.loads((output / "best_complete_bank.json").read_text()) == good
        assert json.loads((output / "last_complete_bank.json").read_text()) == bad
        assert len(verify_archive(output, decoded_inputs=True)) == 2
        # Same-directory resume retains the better earlier field. A separate
        # output directory also receives byte-exact historical capsules.
        archive = CompleteBankArchive(output)
        resumed = folder / "resumed"
        archive = CompleteBankArchive(resumed, output)
        assert json.loads((resumed / "best_complete_bank.json").read_text()) == good
        resumed_metadata = resumed / "metadata.json"
        resumed_metadata.write_text('{"seed":271828,"github_run_id":"resumed-regression"}\n')
        good_answer, good_table = master.price(np.zeros(master.K), keep=0)
        newer = archive.retain(master, good_table, good_answer, 1, resumed_metadata)
        assert newer["candidate_id"] != good["candidate_id"]  # Even a reused round cannot overwrite.
        assert len(verify_archive(resumed, decoded_inputs=True)) == 3
        for p, digest in original.items():
            assert hashlib.sha256(p.read_bytes()).hexdigest() == digest
            assert hashlib.sha256((resumed / p.relative_to(output)).read_bytes()).hexdigest() == digest
        # The input binding and complete-search flag are enforced before
        # retention, independently of any floating discovery objective.
        for answer in (dict(good_answer, certifies_lower=False), dict(good_answer, status="CACHED_ONLY")):
            try:
                archive.retain(master, good_table, answer, 4, resumed_metadata)
            except ValueError:
                pass
            else:
                raise AssertionError("retained an incomplete response-bank result")
        input_bytes = master.binary.read_bytes()
        master.binary.write_bytes(input_bytes[:-1] + bytes([input_bytes[-1] ^ 1]))
        try:
            archive.retain(master, good_table, good_answer, 4, resumed_metadata)
        except ValueError as error:
            assert "raw native input" in str(error)
        else:
            raise AssertionError("retained a field unrelated to the priced input")
        finally:
            master.binary.write_bytes(input_bytes)
        field_path = resumed / newer["field"]
        field_bytes = field_path.read_bytes()
        field_path.write_bytes(field_bytes + b" ")
        try:
            verify_archive(resumed)
        except ValueError as error:
            assert "hash mismatch" in str(error)
        else:
            raise AssertionError("retention accepted altered field bytes")
        field_path.write_bytes(field_bytes)
        pointer = resumed / "best_complete_bank.json"
        pointer.write_text(json.dumps(bad))
        try:
            CompleteBankArchive(resumed)
        except ValueError as error:
            assert "not the exact maximum" in str(error)
        else:
            raise AssertionError("resume silently accepted a weaker best pointer")
    print(json.dumps({"status": "PASS", "complete_fields": 3,
                      "independent_replays": ["fresh native complete search", "BigInt target-bank replay"],
                      "checks": ["exact raw-input reconstruction", "all fields retained compactly",
                                 "better earlier field survives later weaker field", "same-directory resume",
                                 "cross-directory resume", "reused-round immutable naming", "byte-exact old capsules",
                                 "cached/incomplete result rejection", "input/field/pointer corruption rejection"]}))


if __name__ == "__main__":
    main()
