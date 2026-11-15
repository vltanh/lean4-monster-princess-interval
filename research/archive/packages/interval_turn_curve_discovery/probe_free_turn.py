#!/usr/bin/env python3
"""One fixed structural test of independent negative-M2 turn offsets.

The start/offset lists are prescribed once. This is discovery, not an
exact certificate or a mesh-refinement experiment.
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "packages/interval_continuum_discovery"))
from direct_support import solve_support
from integer_geometry import clean, mirror


def main():
    scale = 256
    names, representatives, seen = [], [], set()

    def add(name, vertices):
        path = clean(vertices)
        reflection = mirror(path)
        key = min(tuple(map(tuple, path)), tuple(map(tuple, reflection)))
        if key not in seen:
            seen.add(key)
            names.append(name)
            representatives.append(path)

    for k in range(-8, 9):
        x = 32*k
        add(["M1", k/8], [[0,x], [scale-x,scale], [3*scale-x,-scale]])
        add(["M2", k/8, 1], [[0,x], [(scale-x)//2,(scale+x)//2],
                              [2*scale,-scale], [4*scale,scale]])
    for eta in [4,8,16,32,64,128,192,256]:
        x = scale-eta
        add(["F", eta/scale], [[0,x], [eta,scale], [2*scale+eta,-scale]])
        add(["L", eta/scale], [[0,-x], [2*scale-eta,scale],
                               [4*scale-eta,-scale]])
        add(["Q", eta/scale], [[0,-scale+eta], [scale,eta],
                               [2*scale+eta,-scale], [4*scale+eta,scale]])
    for z in [32,64,96,128,160,192,224]:
        for delta in [2,8,32,64,128]:
            b = scale+delta
            x = -z
            add(["free_negative_M2", z/scale, b/scale],
                [[0,x], [(b-x)//2,(b+x)//2],
                 [b+scale,-scale], [b+3*scale,scale]])

    paths = [p for representative in representatives
             for p in (representative, mirror(representative))]
    result = solve_support(paths,scale)
    result["names"] = names
    result["scope"] = ("Floating fixed-support discovery of turning geometry; "
                       "not a rational certificate or an unrestricted saddle.")
    Path(__file__).with_name("free_turn_probe.json").write_text(json.dumps(result))
    active = [(name,weight) for name,weight in zip(names,result["weights"])
              if weight > 1e-8]
    print("ACTIVE",active,flush=True)
    print("FREE_TURN_MASS",sum(w for name,w in active
                              if name[0] == "free_negative_M2"),flush=True)


if __name__ == "__main__":
    main()
