#!/usr/bin/env python3
"""Independent center-wait and continuous-node response verification."""
from fractions import Fraction as Q
import json
from pathlib import Path
import subprocess
import tempfile

from continuum_field import ExtendedFieldMesh,ExtendedExactField,coordinate
from continuous_response_cost import route_payoff
from continuous_response_grid import Geometry


def main():
    here=Path(__file__).resolve().parent;reports=[]
    with tempfile.TemporaryDirectory(prefix='verify_continuous_node_')as temporary:
        work=Path(temporary);binary=work/'search'
        subprocess.run(['g++','-O3','-std=c++17',str(here/'continuous_response_grid.cpp'),'-o',str(binary)],check=True)
        mesh=ExtendedFieldMesh(base=[0,.25,.5,.75,1],vmax=2)
        nodes=[tuple(map(coordinate,p))for p in mesh.nodes]
        for name,formula,expected in [
            ('early_center',lambda u,v:max(Q(0),min(u,Q(1),2-v)),Q(1,2)),
            ('post_one_center',lambda u,v:max(Q(0),min(Q(1),max((u-v)*Q(2,3),(u-Q(1,2))*Q(4,3)),(2-v)*Q(4,3))),Q(7,8))]:
            values=[formula(u,v)for u,v in nodes];source=work/(name+'.json')
            mesh.save(source,list(map(float,values)),rational_values=list(map(str,values)))
            data=json.loads(source.read_text());field=ExtendedExactField(data)
            wait=[(Q(0),Q(0)),(Q(3),Q(0)),(Q(4),Q(1)),(Q(6),Q(-1))]
            assert route_payoff(field,wait)==expected
            # Independent layer-cake integration for the whole center wait:
            # capture by t is the largest center mass observed so far.
            knots=sorted({Q(0),Q(3)}|{u for u,v in nodes if u==v})
            peak=Q(0);integral=Q(0)
            for a,b in zip(knots,knots[1:]):
                ra,rb=field.radial(a,a),field.radial(b,b)
                assert ra<=peak
                if rb<=peak:integral+=(b-a)*(1-peak)
                else:
                    assert ra==peak
                    integral+=(b-a)*(2-ra-rb)/2
                peak=max(peak,ra,rb)
            assert peak==1 and integral==expected
            geometry=Geometry(data,16);inp=work/'input.txt';out=work/'output.json';geometry.write(inp)
            subprocess.run([str(binary),str(inp),str(out),'20'],check=True,capture_output=True)
            result=json.loads(out.read_text());wait_routes=0;checked=0
            for route in result['routes']:
                attack=geometry.rescore(route['node_ids']);wait_routes+=attack['center_waits']>0;checked+=1
                for completion in geometry.prefix_completions(attack,all_routes=True):
                    assert Q(completion['payoff'])==route_payoff(field,completion['route'])
            assert wait_routes>0
            reports.append(dict(name=name,center_wait_value=str(expected),nodes=len(geometry.nodes),
                                decoded_routes=checked,routes_with_waits=wait_routes,
                                exact_edge_moments='pass',independent_survival_integrals='pass',
                                mixed_full_route_costs='pass'))
        # Exhaust the entire small physical node graph independently. Giving
        # the DP every nodal CDF record removes all record interpolation.
        small=ExtendedFieldMesh(base=[0,1],vmax=2)
        values=[max(Q(0),min(coordinate(u),Q(1),2-coordinate(v)))for u,v in small.nodes]
        source=work/'coarse.json';small.save(source,list(map(float,values)),rational_values=list(map(str,values)))
        geometry=Geometry(json.loads(source.read_text()),4)
        geometry.set_record_knots({Q(0),Q(1)}|{n[k]for n in geometry.nodes for k in ('a','b')})
        inp=work/'nonuniform.txt';out=work/'nonuniform.json';geometry.write(inp)
        subprocess.run([str(binary),str(inp),str(out),'20'],check=True,capture_output=True)
        dp=json.loads(out.read_text());best=None;leaves=0
        def walk(ids):
            nonlocal best,leaves
            node=geometry.nodes[ids[-1]]
            if node['terminal']:
                value=Q(geometry.rescore(ids)['payoff']);leaves+=1
                best=value if best is None else min(best,value);return
            for key in ('right','up','wait'):
                if node[key]>=0:walk(ids+[node[key]])
        for i,node in enumerate(geometry.nodes):
            if node['initial']and node['x']>=0:walk([i])
        assert abs(min(r['estimate']for r in dp['routes'])-float(best))<1e-13
        reports.append(dict(name='all_node_records_vs_exhaustive_graph',nodes=len(geometry.nodes),
                            exact_value=str(best),exhaustive_complete_routes=leaves,
                            nonuniform_record_knots=list(map(str,geometry.record_knots)),
                            floating_dp_agrees_with_exact_enumeration=True))
    target=here/'continuous_response_grid_verification.json'
    target.write_text(json.dumps(dict(scope='Exact physical route verification, including late center atoms; no equilibrium claim.',fixtures=reports),indent=2)+'\n')
    print('PASS 2 center-wait fixtures and exhaustive 97-route nonuniform graph; exact moments, survival, mixed routes and prefix completions')


if __name__=='__main__':main()
