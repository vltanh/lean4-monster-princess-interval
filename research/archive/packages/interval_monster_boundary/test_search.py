#!/usr/bin/env python3
"""Independent contact checks and exact certificate acceptance of discovery."""
from fractions import Fraction as Q
import json
from pathlib import Path
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
from search import ROOT, boundary_routes, inward_boundary_route, endpoint_diagnostic
sys.path.insert(0,str(ROOT/"packages/interval_global_closure"))
from verify_boundary_layer_kernel import clean, kernel, pair_score, princess


def vertices(n, route):
    x = route["start_grid"]
    out = [(Q(0),Q(x,2*n))]
    for j,step in enumerate(route["moves"]):
        if j and step != route["moves"][j-1]:
            out.append((Q(j,2*n),Q(x,2*n)))
        x += step
    out.append((Q(len(route["moves"]),2*n),Q(x,2*n)))
    return clean(out)


def main():
    legality = contacts = 0
    for n in (2,4,8):
        for a in range(n):
            for z in range(a,n):
                for f in range(-a,z+1):
                    path = vertices(n,inward_boundary_route(n,a,z,f))
                    assert path[-1][0] <= 6
                    assert all(abs(y-x)==t-s for (s,x),(t,y) in zip(path,path[1:]))
                    # The generalized fronts remain physical, including the
                    # actual endpoint-touching case f=z and vanishing middle.
                    legality += 1
                physical = vertices(n,inward_boundary_route(n,a,z))
                for h in range(n):
                    for e in range(h+1):
                        actual = pair_score(physical,princess(Q(e,n),Q(h,n)))
                        expected,_ = kernel(Q(a,n),Q(z,n),Q(e,n),Q(h,n))
                        assert actual == expected,(n,a,z,e,h,actual,expected)
                        contacts += 1
        assert any(route["start_grid"] == 2*n-2 for route in boundary_routes(n,8))
    with tempfile.TemporaryDirectory(prefix="boundary_discovery_test_") as folder:
        folder = Path(folder)
        source = json.loads((ROOT/"packages/interval_clock_grid/grid_n2_certificate.json").read_text())
        cp = folder/"seed.json"
        cp.write_text(json.dumps({"n":2,"columns":[{"plan":{k:v for k,v in p.items() if k != "weight_numerator"}} for p in source["paths"]],
            "weights":[int(p["weight_numerator"])/int(source["weight_denominator"]) for p in source["paths"]]}))
        certifier = ROOT/"packages/interval_clock_grid/qout_primal_certificate.cjs"
        subprocess.run(["node",str(certifier),"--make",str(cp),str(folder/"seed")],check=True,capture_output=True,text=True)
        seed = folder/"seed.physical.json"
        out = folder/"result"
        command = [sys.executable,str(HERE/"search.py"),"--n","4","--initial-law",str(seed),
                   "--iterations","2","--seconds","60","--lp-seconds","20","--boundary-points","4",
                   "--pricing-paths","8","--mutation-count","8","--sparse-master","--output",str(out)]
        subprocess.run(command,check=True,capture_output=True,text=True)
        first = json.loads((out/"summary.json").read_text())
        subprocess.run(command+["--resume",str(out/"checkpoint.json")],check=True,capture_output=True,text=True)
        second = json.loads((out/"summary.json").read_text())
        assert second["iterations"] > first["iterations"]
        assert Q(second["best_certified_global_upper"]) <= Q(first["best_certified_global_upper"])
        replay = subprocess.run(["node",str(certifier),str(out/"best.physical.json")],check=True,capture_output=True,text=True)
        assert json.loads(replay.stdout)["global_upper"] == second["best_certified_global_upper"]
        diagnostic = endpoint_diagnostic(json.loads((out/"best.physical.json").read_text()))
        assert Q(diagnostic["certified_upper_minus_loop_witness"]) >= 0
    print(json.dumps({"status":"PASS","independent_physical_kernel_contacts":contacts,
                      "generalized_front_routes":legality,"checks":["chronological rational first contacts, including atoms",
                      "independent-front physical validity","exact all-Princess certificate","same-directory resume preserves best"]}))


if __name__ == "__main__":
    main()
