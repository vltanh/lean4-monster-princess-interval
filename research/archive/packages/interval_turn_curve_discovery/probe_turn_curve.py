#!/usr/bin/env python3
"""One fixed-support structural probe; floating output is not a certificate.

Compare the classical M1/M2 support with paths turning at time one at a
positive position. No mesh-refinement loop or new game-bound claim is made.
"""

import json
import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "packages/interval_continuum_discovery"))
from direct_support import solve_support
from integer_geometry import clean, mirror


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--families", choices=("q", "fq", "flq"), default="flq")
    args = parser.parse_args()
    scale = 128
    names, positive, seen = [], [], set()

    def add(name, vertices):
        path = clean(vertices)
        reflected = mirror(path)
        key = min(tuple(map(tuple, path)), tuple(map(tuple, reflected)))
        if key not in seen:
            seen.add(key)
            names.append(name)
            positive.append(path)

    for k in range(-8, 9):
        x = 16 * k
        add(["M1", k / 8], [[0, x], [scale-x, scale],
                             [3*scale-x, -scale]])
        add(["M2", k / 8], [[0, x], [(scale-x)//2, (scale+x)//2],
                             [2*scale, -scale], [4*scale, scale]])

    for eta in [2, 4, 8, 16, 32, 64, 96, 128]:
        x = scale-eta
        if "f" in args.families:
            add(["F", eta/scale], [[0, x], [eta, scale],
                                    [2*scale+eta, -scale]])
        if "l" in args.families:
            add(["L", eta/scale], [[0, -x], [2*scale-eta, scale],
                                    [4*scale-eta, -scale]])
        add(["Q", eta/scale], [[0, -scale+eta], [scale, eta],
                                [2*scale+eta, -scale],
                                [4*scale+eta, scale]])

    paths = [p for path in positive for p in (path, mirror(path))]
    result = solve_support(paths, scale)
    result["names"] = names
    result["scope"] = "Floating fixed-support discovery only; no rational game certificate."
    result["added_families"] = args.families
    filename = {"q": "turn_curve_probe.json", "fq": "paired_turn_curve_probe.json",
                "flq": "signed_turn_curve_probe.json"}[args.families]
    destination = Path(__file__).with_name(filename)
    destination.write_text(json.dumps(result))
    active = [(name, weight) for name, weight in zip(names, result["weights"])
              if weight > 1e-8]
    print("ACTIVE", active, flush=True)
    print("Q_MASS", sum(w for name, w in active if name[0] == "Q"), flush=True)
    print("L_MASS", sum(w for name, w in active if name[0] == "L"), flush=True)


if __name__ == "__main__":
    main()
