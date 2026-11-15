"""Make a legal rational unit-route law from a whole-CDF discovery dual.

This deliberately produces a new law: turn positions are rationalized, all
elapsed times are reconstructed from unit speed, and omitted slow-route mass
is renormalized.  Only a subsequent global response computation is an upper
certificate; the source field LP value has no such interpretation.
"""
from __future__ import annotations
import argparse
from fractions import Fraction as F
import json
from pathlib import Path


def convert(source: Path, prefix: Path, denominator: int = 2**24) -> dict:
    data = json.loads(source.read_text())
    atoms, weights, times_error = [], [], 0.0
    omitted = 0.0
    for item in data["routes"]:
        original = item["route"]
        motion=item.get('motion')
        if motion is None:
            motion='unit' if all(abs((float(b)-float(a))-abs(float(y)-float(x)))<1e-10
                for(a,x),(b,y)in zip(original,original[1:])) else 'wait_or_slow'
        if motion != "unit":
            omitted += item["weight"]
            continue
        assert abs(float(original[0][0])) < 1e-12
        x = [F(str(row[1])).limit_denominator(denominator) for row in original]
        vertices, t = [(F(0), x[0])], F(0)
        for k, position in enumerate(x[1:], 1):
            t += abs(position - x[k - 1])
            times_error = max(times_error, abs(float(t) - float(original[k][0])))
            if position != vertices[-1][1]:
                vertices.append((t, position))
        assert all(-1 <= position <= 1 for _, position in vertices)
        # Remove redundant collinear turns and tails after both endpoints.
        cleaned, walls = [], set()
        for vertex in vertices:
            if len(cleaned) >= 2:
                a, b = cleaned[-2:]
                if (b[1] - a[1]) * (vertex[1] - b[1]) > 0:
                    cleaned.pop()
            cleaned.append(vertex)
            if abs(vertex[1]) == 1:
                walls.add(vertex[1])
            if len(walls) == 2:
                break
        assert len(walls) == 2, item
        light = [[str(t + position), str(t - position)] for t, position in cleaned]
        atoms.append({"kind": "PATH", "parameters": sum(light, []),
                      "exact_light": light,
                      "light": [[float(F(a)), float(F(b))] for a, b in light]})
        weights.append(item["weight"])
    total = sum(weights)
    weights = [w / total for w in weights]
    summary = {"scope": "Renormalized rational unit-route candidate; awaiting unrestricted princess response",
               "source": str(source), "original_master": data["master_value"],
               "omitted_slow_weight": omitted, "turn_position_denominator_limit": denominator,
               "maximum_time_change": times_error, "pairs": len(atoms)}
    prefix.with_suffix(".bank.json").write_text(json.dumps({"atoms": atoms}, separators=(",", ":")) + "\n")
    prefix.with_suffix(".law.json").write_text(json.dumps({**summary,
        "atoms": [{"kind": a["kind"], "parameters": a["parameters"]} for a in atoms],
        "weights": weights}, separators=(",", ":")) + "\n")
    return summary


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("source", type=Path)
    p.add_argument("prefix", type=Path)
    p.add_argument("--denominator", type=int, default=2**24)
    a = p.parse_args()
    print(json.dumps(convert(a.source, a.prefix, a.denominator), indent=2))
