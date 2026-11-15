"""Compact, immutable retention of every complete Princess pricing result.

The native exhaustive result is retained, not independently reproved here.
The exact input can be regenerated from the pre-two field and its hash checked.
Cached response minima and floating cut-master values are never accepted.
"""
from fractions import Fraction
import base64
import gzip
import hashlib
import json
from pathlib import Path
import shutil
import struct
import zlib

import numpy as np
from verify_native_field import load_table


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
NATIVE = ROOT / "packages/interval_clock_grid/normalized_native"
SCOPE = ("Complete native integer pricing on the normalized physical grid bank; "
         "the unrestricted game-value lower subtracts 1/(2n). This retention "
         "check does not repeat the response search or claim security for this CDF.")


def sha(data):
    return hashlib.sha256(data).hexdigest()


def file_sha(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def encoded(data):
    return (json.dumps(data, sort_keys=True, separators=(",", ":")) + "\n").encode()


def atomic(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_bytes(data)
    temporary.replace(path)


def rooted(root, name):
    relative = Path(name)
    if relative.is_absolute() or ".." in relative.parts:
        raise ValueError("unsafe retained candidate path")
    path = root / relative
    if not path.resolve().is_relative_to(root.resolve()):
        raise ValueError("retained candidate escapes archive")
    return path


def input_hash(n, denominator, table):
    values = np.ascontiguousarray(table, dtype="<u8")
    h = hashlib.sha256(struct.pack("<IIQ", 1, n, denominator))
    h.update(memoryview(values).cast("B"))
    return h.hexdigest()


def descriptor(root, manifest_path, manifest):
    return {"candidate_id": manifest["candidate_id"],
            "manifest": str(manifest_path.relative_to(root)),
            "manifest_sha256": file_sha(manifest_path),
            "field": str((manifest_path.parent / "field.json").relative_to(root)),
            "field_sha256": manifest["files_sha256"]["field.json"],
            "normalized_bank_dual_value": manifest["normalized_bank_dual_value"],
            "global_value_lower": manifest["global_value_lower"],
            "scope": SCOPE}


def verify_archive(root, decoded_inputs=False, check_pointer=True):
    """Check byte bindings and exact arithmetic; optionally regenerate inputs."""
    root = Path(root)
    results = []
    for path in sorted((root / "complete_princess/candidates").glob("*/manifest.json")):
        m = json.loads(path.read_bytes())
        for name, digest in m["files_sha256"].items():
            if file_sha(rooted(path.parent, name)) != digest:
                raise ValueError("retained Princess file hash mismatch: " + str(path.parent / name))
        metadata = rooted(root, m["discovery_metadata_file"])
        if file_sha(metadata) != m["discovery_metadata_sha256"]:
            raise ValueError("retained discovery provenance hash mismatch")
        report_bytes = gzip.decompress((path.parent / "native_report.json.gz").read_bytes())
        if sha(report_bytes) != m["native_report_sha256"]:
            raise ValueError("native result byte binding mismatch")
        answer = json.loads(report_bytes)
        n, denominator = m["n"], int(m["field_denominator"])
        if (answer.get("status") != "PASS" or answer.get("certifies_lower") is False
                or answer.get("n") != n or int(answer["field_denominator"]) != denominator
                or int(answer["objective_denominator"]) != 4*n*denominator):
            raise ValueError("retained result was not a complete matching bank pricing")
        bank = Fraction(int(answer["minimum_units"]), 4*n*denominator)
        if bank != Fraction(m["normalized_bank_dual_value"]) or bank-Fraction(1, 2*n) != Fraction(m["global_value_lower"]):
            raise ValueError("retained exact Princess objective mismatch")
        field = json.loads((path.parent / "field.json").read_bytes())
        if (field.get("n") != n or int(field["field_denominator"]) != denominator
                or field.get("normalized_profile") is not True
                or int(field["minimum_units"]) != int(answer["minimum_units"])
                or int(field["objective_denominator"]) != 4*n*denominator
                or field["raw_pricing_input_sha256"] != m["raw_pricing_input_sha256"]
                or field["native_report_sha256"] != m["native_report_sha256"]
                or field["native_source_sha256"] != m["source_sha256"]["price_normalized.cpp"]
                or Fraction(field["normalized_bank_dual_value"]) != bank
                or Fraction(field["global_lower"]) != bank-Fraction(1, 2*n)):
            raise ValueError("field/report provenance mismatch")
        if decoded_inputs:
            data, table, _ = load_table(path.parent / "field.json")
            if input_hash(n, denominator, table) != m["raw_pricing_input_sha256"]:
                raise ValueError("decoded field changes the native raw pricing input")
        results.append(descriptor(root, path, m))
    pointer = root / "best_complete_bank.json"
    if check_pointer and pointer.exists():
        saved = json.loads(pointer.read_bytes())
        by_id = {d["candidate_id"]: d for d in results}
        if saved.get("candidate_id") not in by_id or saved != by_id[saved["candidate_id"]]:
            raise ValueError("best complete-bank pointer binding mismatch")
        if any(Fraction(d["normalized_bank_dual_value"]) > Fraction(saved["normalized_bank_dual_value"]) for d in results):
            raise ValueError("best complete-bank pointer is not the exact maximum")
    return results


class CompleteBankArchive:
    def __init__(self, root, resume_root=None):
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)
        merging = resume_root is not None and Path(resume_root).resolve() != self.root.resolve()
        if merging:
            source = Path(resume_root)
            verify_archive(source)
            verify_archive(self.root)
            for old in (source / "complete_princess").rglob("*"):
                if not old.is_file() or old.name == "index.json":
                    continue
                new = self.root / old.relative_to(source)
                if new.exists() and file_sha(new) != file_sha(old):
                    raise ValueError("resume would overwrite a retained Princess candidate")
                if not new.exists():
                    new.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copyfile(old, new)
        self.candidates = verify_archive(self.root, check_pointer=not merging)
        self._pointers()

    def _pointers(self):
        if not self.candidates:
            return
        best = max(self.candidates, key=lambda d: Fraction(d["normalized_bank_dual_value"]))
        atomic(self.root / "best_complete_bank.json", encoded(best))
        atomic(self.root / "complete_princess/index.json", encoded({
            "format": "complete-princess-pricing-index-v1", "scope": SCOPE,
            "candidate_count": len(self.candidates), "candidates": self.candidates,
            "best_candidate_id": best["candidate_id"]}))

    def retain(self, master, table, answer, pricing_round, discovery_metadata):
        n, denominator = master.n, master.D
        if (not master.normalized_profile or not 0 < denominator < 2**32
                or answer.get("status") != "PASS" or answer.get("certifies_lower") is False
                or answer.get("n") != n or int(answer["field_denominator"]) != denominator
                or int(answer["objective_denominator"]) != 4*n*denominator):
            raise ValueError("only complete matching normalized-bank pricing can be retained")
        raw_hash = input_hash(n, denominator, table)
        if file_sha(master.binary) != raw_hash:
            raise ValueError("raw native input differs from the candidate table")
        report_bytes = encoded(answer)
        report_hash = sha(report_bytes)
        source_hashes = {name: file_sha(NATIVE / name) for name in
                         ("price_normalized.cpp", "solve_normalized.py", "verify_native_field.py")}
        source_hashes["princess_retention.py"] = file_sha(Path(__file__))
        executable_hash = file_sha(master.executable)
        metadata_bytes = Path(discovery_metadata).read_bytes()
        metadata_hash = sha(metadata_bytes)
        metadata_name = "complete_princess/provenance/" + metadata_hash + ".json"
        atomic(self.root / metadata_name, metadata_bytes)
        bank = Fraction(int(answer["minimum_units"]), 4*n*denominator)
        lower = bank-Fraction(1, 2*n)
        pre = np.concatenate([table[j, 2 if j%2 == 0 else 1::2] for j in range(4*n+1)])
        if len(pre) != (4*n+1)*n or np.max(pre) > denominator:
            raise ValueError("compact Princess field range")
        raw = pre.astype("<u4").tobytes()
        field = {"format": "qout-clock-grid-field-u32-zlib-v1", "n": n,
                 "field_denominator": str(denominator), "normalized_profile": True,
                 "encoding": {"domain": "pre-two radial parity nodes in increasing time then radius",
                              "integer_type": "uint32 little-endian", "compression": "zlib",
                              "count": len(pre), "uncompressed_sha256": sha(raw)},
                 "pre_two_values_base64": base64.b64encode(zlib.compress(raw, 9)).decode(),
                 "scope": SCOPE, "minimum_units": str(answer["minimum_units"]),
                 "objective_denominator": str(4*n*denominator),
                 "normalized_bank_dual_value": str(bank), "global_lower": str(lower),
                 "global_lower_decimal": float(lower), "raw_pricing_input_sha256": raw_hash,
                 "native_report_sha256": report_hash,
                 "native_source_sha256": source_hashes["price_normalized.cpp"]}
        identity = sha(encoded({"raw_input": raw_hash, "report": report_hash,
                                "metadata": metadata_hash, "sources": source_hashes,
                                "executable": executable_hash, "pricing_round": pricing_round}))
        name = "n%d-round%06d-%s" % (n, pricing_round, identity[:24])
        folder = self.root / "complete_princess/candidates" / name
        field_bytes = encoded(field)
        report_gzip = gzip.compress(report_bytes, mtime=0)
        m = {"format": "complete-princess-pricing-candidate-v1", "candidate_id": name,
             "scope": SCOPE, "n": n, "field_denominator": str(denominator),
             "pricing_round": pricing_round, "normalized_bank_dual_value": str(bank),
             "global_value_lower": str(lower), "raw_pricing_input_sha256": raw_hash,
             "raw_input_format": "little-endian IIQ header (version=1,n,D), then full row-major uint64 table",
             "native_report_sha256": report_hash,
             "report_encoding": "canonical JSON of the returned native result, gzip mtime=0; not original stdout bytes",
             "source_sha256": source_hashes, "native_executable_sha256": executable_hash,
             "discovery_metadata_file": metadata_name, "discovery_metadata_sha256": metadata_hash,
             "independent_response_search_replayed": False,
             "files_sha256": {"field.json": sha(field_bytes), "native_report.json.gz": sha(report_gzip)}}
        if (folder / "manifest.json").exists():
            if (folder / "manifest.json").read_bytes() != encoded(m):
                raise ValueError("retained candidate identity collision")
            return descriptor(self.root, folder / "manifest.json", m)
        atomic(folder / "field.json", field_bytes)
        # This independent decoder must reproduce the exact full native input,
        # including the deterministic outward extension after time two.
        _, decoded, _ = load_table(folder / "field.json")
        if input_hash(n, denominator, decoded) != raw_hash:
            raise AssertionError("compact field changed the priced native input")
        atomic(folder / "native_report.json.gz", report_gzip)
        atomic(folder / "manifest.json", encoded(m))
        result = descriptor(self.root, folder / "manifest.json", m)
        self.candidates.append(result)
        self._pointers()
        atomic(self.root / "last_complete_bank.json", encoded(result))
        return result
