#!/usr/bin/env python3
"""Compile and test the untrusted native optimizer against exact JS witnesses."""
import json
from pathlib import Path
import subprocess
import tempfile

from native_closure import compile_helper

HERE=Path(__file__).resolve().parent

with tempfile.TemporaryDirectory(prefix="princess_monster_flow_") as folder:
    binary=compile_helper(folder)
    result=subprocess.run(["node","--stack-size=16384",str(HERE/"test_flow.cjs"),str(binary)],check=True,text=True,capture_output=True)
    print(json.dumps(json.loads(result.stdout),indent=2))
