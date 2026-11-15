#!/usr/bin/env python3
"""Replay the physical seed, exact marginals, and direct endpoint-loop tests."""
from fractions import Fraction as Q
import gzip
import hashlib
import json
from pathlib import Path
import subprocess
import sys

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
sys.path.insert(0,str(ROOT/"packages/interval_global_closure"))
from verify_boundary_layer_kernel import clean,pair_score,princess


def main():
    manifest=json.loads((HERE/"seed_manifest.json").read_text())
    for name,expected in manifest["files_sha256"].items():
        if Path(name).name!=name:raise ValueError("nonlocal manifest name")
        assert hashlib.sha256((HERE/name).read_bytes()).hexdigest()==expected
    compressed=(HERE/"seed_plain_n128.sparse.json.gz").read_bytes();raw=gzip.decompress(compressed)
    assert hashlib.sha256(compressed).hexdigest()==manifest["compressed_source_sha256"]
    assert hashlib.sha256(raw).hexdigest()==manifest["uncompressed_source_sha256"]
    law=json.loads(raw);n=law["n"];W=int(law["weight_denominator"])
    groups={}
    for p in law["paths"]:
        key=p["start_grid"],tuple(p["moves"])
        groups[key]=groups.get(key,0)+int(p["weight_numerator"])
    compact=json.loads((HERE/"seed_plain_marginals.json").read_text())
    decoded={}
    for p in compact["physical_pairs"]:
        moves=[];last=None
        for direction,count in p["runs"]:
            assert direction in (-1,1) and isinstance(count,int) and count>0 and direction!=last
            moves.extend([direction]*count);last=direction
        key=p["start_grid"],tuple(moves)
        assert key not in decoded;decoded[key]=int(p["weight_numerator"])
    assert decoded==groups and len(groups)==manifest["physical_pairs"]==676
    assert sum(groups.values())==W
    baseline=Q(0);endpoint_mass=Q(0);interior=[];routes=[]
    for (start,moves),mass in groups.items():
        x=start;positions=[start];vertices=[(Q(0),Q(x,2*n))]
        for j,direction in enumerate(moves):
            if j and direction!=moves[j-1]:vertices.append((Q(j,2*n),Q(x,2*n)))
            x+=direction;positions.append(x)
        vertices.append((Q(len(moves),2*n),Q(x,2*n)));route=clean(vertices)
        assert positions.index(0)<=4*n and all(abs(x)<=2*n for x in positions)
        left,right=positions.index(-2*n),positions.index(2*n)
        assert max(left,right)<=12*n
        baseline+=Q(mass,W)*Q(left+right,4*n)
        if abs(start)==2*n:
            assert moves[:4*n]==tuple([-1 if start>0 else 1]*(4*n))
            endpoint_mass+=Q(mass,W)
        else:interior.append(abs(start))
        routes.append((route,Q(mass,W)))
    delta=1-Q(max(interior),2*n);floor=baseline+endpoint_mass*delta/4
    diagnostic=manifest["endpoint_diagnostic"]
    assert str(baseline)==diagnostic["endpoint_baseline"]
    assert str(endpoint_mass)==diagnostic["endpoint_sweep_mass"]
    assert str(delta)==diagnostic["initial_gap"]
    assert str(floor)==diagnostic["endpoint_loop_supremum_lower"]
    checks=0
    for factor in (Q(1,2),Q(3,4),Q(7,8)):
        h=delta*factor
        for epsilon in (h/2,h):
            target=princess(epsilon,h)
            actual=sum((weight*pair_score(route,target) for route,weight in routes),Q(0))
            assert actual==baseline+endpoint_mass*h/4
            checks+=len(routes)
    replay=subprocess.run(["node",str(ROOT/"packages/interval_sparse_upper/sparse_certificate.cjs"),str(HERE/"seed_plain_n128.sparse.json.gz")],
                          check=True,capture_output=True,text=True)
    report=json.loads(replay.stdout)
    assert report["status"]=="PASS" and report["global_upper"]==manifest["exact_upper"]
    assert report==json.loads((HERE/"seed_plain_replay.json").read_text())
    assert str(Q(report["global_upper"])-floor)==diagnostic["certified_upper_minus_loop_witness"]
    print(json.dumps({"status":"PASS","physical_pairs":len(groups),"calendar_plans":len(law["paths"]),
        "independent_pair_loop_checks":checks,"exact_upper":report["global_upper"],"fixed_law_loop_floor":str(floor),
        "scope":"Exact upper for this seed; the loop floor is a fixed-law response lower and is not a game lower."},indent=2))


if __name__=="__main__":main()
