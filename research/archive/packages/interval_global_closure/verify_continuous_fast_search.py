"""Independent capture/contact checks for the aggregate exact response engine."""
from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
from continuous_response_extract import extract
from continuous_response_verify import ROOT, run, independent_fixed_response, exact_oracles


def main():
    here=Path(__file__).resolve().parent
    source=ROOT/'packages/interval_cdf_discovery/snapshots/initial_inward_repaired.json'
    data=extract(source,2)
    paths=[[tuple(map(Q,p)) for p in path] for path in data['paths']]
    fixtures=[('four_actual_quantiles',paths,list(map(Q,data['weights'])),2)]
    for horizon,release in [(2,Q(3,4)),(3,Q(3,2))]:
        inner=[(Q(0),-Q(1,4)),(Q(1,4),Q(0)),(release,Q(0)),(release+1,Q(-1)),(Q(horizon),Q(-1))]
        wait=Q(horizon-1)
        outer=[(Q(0),-Q(3,4)),(wait,-Q(3,4)),(wait+Q(1,4),Q(-1)),(Q(horizon),Q(-1))]
        ps=[outer,inner,[(t,-x) for t,x in inner],[(t,-x) for t,x in outer]]
        fixtures.append((f'weighted_center_atom_H{horizon}',ps,[Q(1,8),Q(3,8),Q(3,8),Q(1,8)],horizon))
    records=[]
    with tempfile.TemporaryDirectory(prefix='verify_fast_response_') as temp:
        folder=Path(temp);binary=folder/'search'
        cpp=here/'continuous_response_fast_search.cpp'
        subprocess.run(['g++','-O3','-std=c++17',str(cpp),'-lgmpxx','-lgmp','-o',str(binary)],check=True)
        for name,ps,weights,horizon in fixtures:
            oracle=exact_oracles.monster_best_response(ps,weights)
            answer=run(binary,folder,ps,weights,100000,horizon)
            assert answer['complete'] and Q(answer['value'])==oracle['value']
            route=[tuple(map(Q,p)) for p in answer['route']]
            captures=[exact_oracles.first_meeting(route,p) for p in ps]
            assert sum(w*t for w,t in zip(weights,captures))==oracle['value']
            stopped=run(binary,folder,ps,weights,0,horizon)
            assert Q(stopped['lower_bound'])<=oracle['value']<=Q(stopped['value'])
            fixed_value,_=independent_fixed_response(ps,weights,0)
            fixed=run(binary,folder,ps,weights,100000,horizon,start=0)
            assert fixed['complete'] and Q(fixed['value'])==fixed_value
            records.append(dict(name=name,value=answer['value'],fixed_center_value=fixed['value'],
                scalar_inverse_point_checks=answer['inverse_point_checks'],
                independent_physical_captures=len(captures),stopped_frontier_checked=True))
        sampled=extract(source,16)
        ps=[[tuple(map(Q,p)) for p in path] for path in sampled['paths']]
        answer=run(binary,folder,ps,list(map(Q,sampled['weights'])),100000,2)
        archived=json.loads((here/'continuous_response_initial_inward_16_search.json').read_text())
        assert answer['complete'] and answer['value']==archived['value']
        route=[tuple(map(Q,p)) for p in answer['route']]
        assert sum(exact_oracles.first_meeting(route,p) for p in ps)/len(ps)==Q(answer['value'])
        benchmark=dict(paths=32,value=answer['value'],processed=answer['processed'],
            inverse_pieces=answer['inverse_pieces'],scalar_inverse_point_checks=answer['inverse_point_checks'],
            independent_physical_captures=32)
    report=dict(scope='Exact aggregate inverse-hit implementation and unchanged unrestricted finite capture-order objective; no game equilibrium claim.',
        cpp_sha256=hashlib.sha256(cpp.read_bytes()).hexdigest(),fixtures=records,archived_quantile_regression=benchmark)
    (here/'continuous_response_fast_verification.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))


if __name__=='__main__':main()
