"""Restore the text-safe gzip snapshot artifacts and check their input hashes."""
from __future__ import annotations
import argparse
import base64
import gzip
import hashlib
import json
from pathlib import Path


def unpack(manifest: dict, repository: Path, destination: Path) -> list[dict]:
    decoded = []
    for item in manifest["archives"]:
        encoded = "".join((repository / item["path"]).read_text().split())
        data = gzip.decompress(base64.b64decode(encoded, validate=True))
        digest = hashlib.sha256(data).hexdigest()
        if digest != item["source_sha256"]:
            raise ValueError(f"Uncompressed hash mismatch: {item['path']}")
        name = Path(item["name"]).name
        if not name.endswith(".gz"):
            raise ValueError("Expected a gzip artifact name")
        decoded.append((name[:-3], data, digest))
    destination.mkdir(parents=True, exist_ok=True)
    result = []
    for name, data, digest in decoded:
        (destination / name).write_bytes(data)
        result.append({"name": name, "bytes": len(data), "sha256": digest})
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", type=Path)
    parser.add_argument("repository", type=Path)
    parser.add_argument("destination", type=Path)
    args = parser.parse_args()
    print(json.dumps(unpack(json.loads(args.manifest.read_text()), args.repository, args.destination), indent=2))
