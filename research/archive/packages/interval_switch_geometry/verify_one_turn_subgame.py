#!/usr/bin/env python3
"""Exact rational one/two-interior-turn Monster subgame upper witness.

Uses the previously certified complete physical Monster upper, preserving its
independent flow/cut verification as a separate proof dependency.
"""
import gzip
import hashlib
import json
from collections import defaultdict
from fractions import Fraction as Q
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PACK = ROOT / "packages/interval_discovery_certificates"
GZIP_SHA = "80580dae8551c2838172d7f419861a3a9774793a8d039bdad087e21d24526f39"
PLAIN_SHA = "5c736b0c6ef59b418cce0e2e2ef24b0a8dbe4d017a6eca7578d9e1c79616b31d"
LOWER = Q(36409808231, 25600000000)
UPPER = Q(291849329389899, 204800000000000)

def classify(path, R):
    pos = path["start_grid"]
    assert isinstance(pos, int) and -R <= pos <= R
    moves = path["moves"]
    turns, prev, first = 0, None, None
    if abs(pos) == R:
        first = 0
    else:
        for i, direction in enumerate(moves, 1):
            assert direction in (-1, 1)
            if prev is not None and direction != prev:
                turns += 1
            prev = direction
            pos += direction
            assert abs(pos) <= R
            if abs(pos) == R:
                first = i
                break
    assert first is not None
    # All saved paths have an immediate unit-speed opposite-endpoint tour.
    tail = moves[first:]
    assert len(tail) == 2 * R
    assert all(direction == (-1 if pos == R else 1) for direction in tail)
    return turns

def main():
    packed = (PACK / "monster_boundary_n256.physical.json.gz").read_bytes()
    assert hashlib.sha256(packed).hexdigest() == GZIP_SHA
    raw = gzip.decompress(packed)
    assert hashlib.sha256(raw).hexdigest() == PLAIN_SHA
    data = json.loads(raw)
    manifest = json.loads((PACK / "monster_boundary_n256_manifest.json").read_text())
    assert manifest["certificate_gzip_sha256"] == GZIP_SHA
    assert manifest["uncompressed_certificate_sha256"] == PLAIN_SHA
    assert manifest["status"] == manifest["exact_result"]["status"] == "PASS"
    assert Q(manifest["exact_result"]["global_upper"]) == UPPER
    assert Q(data["global_upper"]) == UPPER
    assert data["pair_law"] == "fair_reflection" and data["n"] == 256
    assert data["physical_step"] == "1/512"
    W, R = int(data["weight_denominator"]), 2 * data["n"]
    assert W == 10**12 and len(data["paths"]) == 770
    weight, count, start_bound = defaultdict(int), defaultdict(int), defaultdict(lambda: Q(0))
    for path in data["paths"]:
        k = classify(path, R)
        w = int(path["weight_numerator"])
        assert w > 0
        weight[k] += w
        count[k] += 1
        # Weight w is a fair reflected PAIR at starts ±(start_grid/R).
        start_bound[k] += Q(w * abs(path["start_grid"]), 2 * R * W)
    assert sum(weight.values()) == W
    assert dict(weight) == {0: 824951536886, 1: 168892467811,
                            2: 6054719396, 3: 92665891, 4: 8610016}
    result = {"status": "PASS",
              "scope": "Restricted Monster all-Princess upper witness, not exact equilibrium",
              "original_upper": str(UPPER), "unrestricted_lower": str(LOWER),
              "per_turn_mass": {str(k): str(Q(w, W)) for k,w in sorted(weight.items())},
              "per_turn_plan_count": {str(k): count[k] for k in sorted(weight)},
              "subgames": {}}
    for cap, expected in [(1, Q(1458323028259559, 1017696260809728)),
                          (2, Q(1459235032632867, 1023896293471232))]:
        removed = sum(w for k,w in weight.items() if k > cap)
        q = Q(removed,W)
        a = sum((v for k,v in start_bound.items() if k > cap), Q(0))
        value = (UPPER - a) / (1-q)
        assert value == expected and value < Q(3,2)
        result["subgames"][str(cap)] = {
            "removed_mass": str(q), "universal_removed_payoff": str(a),
            "inherited_all_princess_upper": str(value), "decimal": float(value),
        }
    assert sum(count[k] for k in (0,1)) == 345
    print(json.dumps(result,indent=2,sort_keys=True))
if __name__ == "__main__":
    main()

