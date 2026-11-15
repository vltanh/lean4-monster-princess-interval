#!/usr/bin/env python3
"""Check retained hashes, exact refined-seed identity, and the field witness."""
import gzip
import hashlib
import json
from pathlib import Path
import subprocess
import sys

HERE=Path(__file__).resolve().parent
manifest=json.loads((HERE/"manifest.json").read_text())
for name,expected in manifest["files_sha256"].items():
    if Path(name).name!=name:raise ValueError("nonlocal manifest filename")
    assert hashlib.sha256((HERE/name).read_bytes()).hexdigest()==expected
report=json.loads((HERE/"blocking.report.json").read_text())
seed_path=HERE.parent/"seed_plain_n128.sparse.json.gz"
assert hashlib.sha256(seed_path.read_bytes()).hexdigest()==report["provenance"]["committed_seed_compressed_sha256"]
seed=json.loads(gzip.decompress(seed_path.read_bytes()))
compact=json.loads((HERE/"physical_marginals.json").read_text())
ratio=compact["n"]//seed["n"]
assert compact["n"]==ratio*seed["n"] and ratio==report["provenance"]["refinement_factor"]
assert int(compact["weight_denominator"])==int(seed["weight_denominator"])
expected={}
for plan in seed["paths"]:
    key=plan["start_grid"]*ratio,tuple(d for d in plan["moves"] for _ in range(ratio))
    expected[key]=expected.get(key,0)+int(plan["weight_numerator"])
actual={}
for plan in compact["physical_pairs"]:
    moves=[]
    for direction,count in plan["runs"]:
        assert direction in (-1,1) and type(count) is int and count>0
        moves.extend([direction]*count)
    key=plan["start_grid"],tuple(moves)
    assert key not in actual
    actual[key]=int(plan["weight_numerator"])
assert actual==expected and len(actual)==676
verifier=HERE.parent/"verify_obstruction.py"
assert hashlib.sha256(verifier.read_bytes()).hexdigest()==manifest["verification_script_sha256"]
replay=subprocess.run([sys.executable,str(verifier),"--result-directory",str(HERE)],check=True,text=True,capture_output=True)
result=json.loads(replay.stdout)
assert result==json.loads((HERE/"independent_replay.json").read_text())
print(json.dumps({"status":"PASS","refined_seed_physical_pairs_checked":len(actual),"field_replay":result},indent=2))
