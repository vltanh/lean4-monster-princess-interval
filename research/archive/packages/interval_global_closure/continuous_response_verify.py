#!/usr/bin/env python3
"""Independent rational validation of quantile extraction and frontier bounds."""
from fractions import Fraction as Q
import json
from pathlib import Path
import subprocess
import sys
import tempfile

from continuous_response_extract import extract

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'packages/interval_exact_reduction'))
import exact_oracles
sys.path.insert(0,str(ROOT/'packages/interval_cdf_discovery'))
from audit_m1 import ExactField


def run(binary,folder,paths,weights,limit,horizon=2,start=None):
    lines=[str(len(paths))+' '+str(horizon)]
    for p,w in zip(paths,weights):
        lines.append(str(w)+' '+str(len(p)))
        lines.extend(str(t)+' '+str(x)for t,x in p)
    file=folder/'paths.txt';file.write_text('\n'.join(lines)+'\n')
    command=[str(binary),str(file),str(limit)]
    if start is not None:command.extend(['--start',str(start)])
    result=subprocess.run(command,capture_output=True,text=True,check=True)
    return json.loads(result.stdout)


def independent_fixed_response(paths,weights,start):
    """Unpruned mask search using the independent segment-wise ray solver."""
    n=len(paths);full=(1<<n)-1;best=None;states=0
    def walk(mask,t,x,cost):
        nonlocal best,states
        states+=1
        for j,p in enumerate(paths):
            if not(mask>>j&1)and exact_oracles.position(p,t)==x:
                mask|=1<<j;cost+=weights[j]*t
        if mask==full:
            best=cost if best is None else min(best,cost);return
        for d in (-1,1):
            hits=[exact_oracles.ray_hit(p,t,x,d)for j,p in enumerate(paths)if not(mask>>j&1)]
            hits=[s for s in hits if s is not None]
            if hits:
                end=min(hits);assert end>t
                walk(mask,end,x+d*(end-t),cost)
    walk(0,Q(0),Q(start),Q(0))
    return best,states


def main():
    source=ROOT/'packages/interval_cdf_discovery/snapshots/initial_inward_repaired.json'
    field=ExactField(json.loads(source.read_text()))
    small=extract(source,2);paths=[[tuple(map(Q,p))for p in path]for path in small['paths']]
    weights=list(map(Q,small['weights']))
    fixtures=[('actual_four_quantiles',paths,weights,2)]
    inner=[(Q(0),-Q(1,4)),(Q(1,4),Q(0)),(Q(3,4),Q(0)),(Q(7,4),Q(-1)),(Q(2),Q(-1))]
    outer=[(Q(0),-Q(3,4)),(Q(1),-Q(3,4)),(Q(5,4),Q(-1)),(Q(2),Q(-1))]
    fixtures.append(('center_coalescence_then_split',
                     [outer,inner,[(t,-x)for t,x in inner],[(t,-x)for t,x in outer]],
                     [Q(1,8),Q(3,8),Q(3,8),Q(1,8)],2))
    inner=[(Q(0),-Q(1,4)),(Q(1,4),Q(0)),(Q(3,2),Q(0)),(Q(5,2),Q(-1)),(Q(3),Q(-1))]
    outer=[(Q(0),-Q(3,4)),(Q(2),-Q(3,4)),(Q(9,4),Q(-1)),(Q(3),Q(-1))]
    fixtures.append(('time_three_late_center_split',
                     [outer,inner,[(t,-x)for t,x in inner],[(t,-x)for t,x in outer]],
                     [Q(1,8),Q(3,8),Q(3,8),Q(1,8)],3))
    reports=[]
    with tempfile.TemporaryDirectory(prefix='verify_continuous_response_')as temp:
        folder=Path(temp);binary=folder/'search'
        subprocess.run(['g++','-O3','-std=c++17',str(Path(__file__).with_name('continuous_response_search.cpp')),
                        '-lgmpxx','-lgmp','-o',str(binary)],check=True,capture_output=True,text=True)
        for name,ps,ws,horizon in fixtures:
            oracle=exact_oracles.monster_best_response(ps,ws)
            completed=run(binary,folder,ps,ws,100000,horizon)
            assert completed['complete'] and Q(completed['value'])==oracle['value']
            assert Q(completed['lower_bound'])==oracle['value']
            stopped=run(binary,folder,ps,ws,0,horizon)
            assert Q(stopped['lower_bound'])<=oracle['value']<=Q(stopped['value'])
            route=[tuple(map(Q,p))for p in completed['route']]
            assert route[-1][0]<=horizon+4
            assert any(x==-1 for t,x in route)and any(x==1 for t,x in route)
            actual=sum(w*exact_oracles.first_meeting(route,p)for w,p in zip(ws,ps))
            assert actual==oracle['value']
            fixed_value,fixed_states=independent_fixed_response(ps,ws,0)
            fixed=run(binary,folder,ps,ws,100000,horizon,start=0)
            assert fixed['complete']and Q(fixed['value'])==fixed_value and fixed['fixed_start']=='0'
            reports.append(dict(name=name,exact_value=str(actual),independent_states=oracle['states'],
                                exact_search_states=completed['processed'],
                                stopped_lower=stopped['lower_bound'],stopped_upper=stopped['value'],
                                exact_fixed_center_value=str(fixed_value),fixed_center_independent_states=fixed_states))
        sampled=extract(source,16)
        ps=[[tuple(map(Q,p))for p in path]for path in sampled['paths']]
        completed=run(binary,folder,ps,list(map(Q,sampled['weights'])),100000)
        archived=json.loads(Path(__file__).with_name('continuous_response_initial_inward_16_search.json').read_text())
        assert completed['complete'] and Q(completed['value'])==Q(archived['value'])
        route=[tuple(map(Q,p))for p in completed['route']]
        captures=[exact_oracles.first_meeting(route,p)for p in ps]
        assert all(t is not None for t in captures)
        assert sum(captures)/len(captures)==Q(completed['value'])
    # Independent CDF evaluation at vertices and midsegments verifies that the
    # geometric level-set extraction produced the claimed quantiles, including
    # center and endpoint atoms, not merely some legal ordered paths.
    level_checks=0;center_checks=0;endpoint_checks=0
    for i,p in enumerate(ps[len(ps)//2:]):
        q=Q(2*i+1,32)
        points=list(p)+[((a+b)/2,(x+y)/2)for(a,x),(b,y)in zip(p,p[1:])]
        for t,x in points:
            value=field.radial(t+x,t-x)
            if x==0:assert q<=value;center_checks+=1
            elif x==1:assert q>=value;endpoint_checks+=1
            else:assert q==value;level_checks+=1
    output=dict(scope='Exact extraction, independent unrestricted finite-response, and stopped-frontier checks; no equilibrium claim.',
                fixtures=reports,field_sha256=small['input_sha256'],
                quantile_level_checks=level_checks,center_atom_checks=center_checks,
                endpoint_atom_checks=endpoint_checks,independent_32_path_captures=len(captures),
                complete_32_path_value=completed['value'])
    target=Path(__file__).with_name('continuous_response_verification.json')
    target.write_text(json.dumps(output,indent=2)+'\n')
    print('PASS',len(reports),'independent small response fixtures;',level_checks,'interior quantile checks;',
          center_checks,'center checks;',endpoint_checks,'endpoint checks; stopped frontier;32 direct captures')


if __name__=='__main__':main()
