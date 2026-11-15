#!/usr/bin/env python3
"""Check physical discovery proposals, integer lifting and resumable acceptance."""
from fractions import Fraction
import json
from pathlib import Path
import random
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from monster_search import ROOT, lift_plan, mutate_routes, normalize_path, route_key


def main():
    seed = json.loads((ROOT/"packages/interval_clock_grid/grid_n2_certificate.json").read_text())
    checked = 0
    for n in (2, 4, 8):
        lifted = [lift_plan(p, n//2) for p in seed["paths"]]
        for path in lifted:
            normalize_path(n, path)
            for name in ("minus_charges", "plus_charges"):
                cumulative = 0
                positions = [path["start_grid"]]
                for step in path["moves"]:
                    positions.append(positions[-1]+step)
                endpoint = positions.index(-2*n if name == "minus_charges" else 2*n)
                charges = dict(path[name])
                for j in range(endpoint):
                    cumulative += charges.get(j, 0)
                    assert cumulative >= j+1
                assert cumulative == endpoint
        routes = mutate_routes(n, lifted, random.Random(314159), 250)
        same = mutate_routes(n, lifted, random.Random(314159), 250)
        assert routes == same and len(routes) >= 150
        assert any(route_key(p) not in {route_key(q) for q in lifted} for p in routes)
        for route in routes:
            assert normalize_path(n, route) == route
            checked += 1
    with tempfile.TemporaryDirectory(prefix="monster_discovery_test_") as folder:
        output = Path(folder)/"first"
        command = [sys.executable, str(HERE/"monster_search.py"), "--n", "4", "--iterations", "2",
                   "--seconds", "60", "--seed", "7", "--family", "mutations", "--mutation-count", "16",
                   "--pricing-paths", "8", "--initial-law", str(ROOT/"packages/interval_clock_grid/grid_n2_certificate.json"),
                   "--output", str(output)]
        subprocess.run(command, check=True, capture_output=True, text=True)
        first = json.loads((output/"summary.json").read_text())
        manifest = json.loads((output/"manifest.json").read_text())
        assert manifest["status"] == "COMPLETED" and "best.physical.json" in manifest["sha256"]
        old_upper = Fraction(first["best_certified_global_upper"])
        # Resume into the same directory, ensuring its saved best certificate
        # is replayed before seed reinitialization can replace it.
        subprocess.run(command + ["--resume", str(output/"checkpoint.json")], check=True, capture_output=True, text=True)
        later = json.loads((output/"summary.json").read_text())
        assert later["iterations_total"] > first["iterations_total"]
        assert Fraction(later["best_certified_global_upper"]) <= old_upper
        replay = subprocess.run(["node", str(ROOT/"packages/interval_clock_grid/qout_primal_certificate.cjs"), str(output/"best.physical.json")],
                                check=True, capture_output=True, text=True)
        assert json.loads(replay.stdout)["global_upper"] == later["best_certified_global_upper"]
    print(json.dumps({"status": "PASS", "legal_mutation_proposals": checked,
                      "checks": ["integer path and clock lifting", "reproducible new physical routes", "exact all-Princess replay", "same-directory resume preserves best"]}))


if __name__ == "__main__":
    main()
