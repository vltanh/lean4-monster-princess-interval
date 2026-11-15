#!/usr/bin/env python3
"""Check horizon extension against independent exact running-CDF costs.

The nontrivial fixture has positive center mass after time one, so these
checks exercise precisely the part of the domain excluded by the old mesh.
They validate representation/scoring code, not an equilibrium certificate.
"""
from fractions import Fraction as Q
import json
from pathlib import Path
import tempfile
import numpy as np

from continuum_field import ExtendedFieldMesh,ExtendedExactField
from continuum_inward_scan import InwardScanner
from continuum_master import full_native_m2_pool
from joint_cdf_field import FieldMesh,RouteFunctional,route_pool,two_interior_pool


def main():
    old=FieldMesh();same=ExtendedFieldMesh(vmax=1)
    assert np.array_equal(old.nodes,same.nodes)
    assert np.array_equal(old.triangles,same.triangles)
    assert old.bounds==same.bounds and old.transport==same.transport
    full=ExtendedFieldMesh(vmax=2)
    triangles=full.nodes[full.triangles]
    edges=triangles[:,1:]-triangles[:,:1]
    area=np.abs(edges[:,0,0]*edges[:,1,1]-edges[:,0,1]*edges[:,1,0]).sum()/2
    # The triangles occupy disjoint grid rectangles. Their full domain
    # area is 1+2*Vmax, so this also detects holes at the diagonal faces.
    assert abs(area-5)<1e-12,area
    for t in np.linspace(0,2,101):full.weights(t,t)
    for t in np.linspace(0,3,101):full.weights(t+1,t-1)
    mesh=ExtendedFieldMesh(base=np.linspace(0,1,9),vmax=2)
    # This is an actual legal CDF: R_U>=0, R_V<=0, initial R(r,-r)=r,
    # and endpoint absorption at time three. ExactField checks every
    # triangle's two derivative inequalities over rational arithmetic.
    values=np.clip(np.minimum(np.minimum(mesh.nodes[:,0],1),2-mesh.nodes[:,1]),0,1)
    values,repair=mesh.repair_values(values)
    assert repair==0
    with tempfile.TemporaryDirectory() as directory:
        path=Path(directory)/'field.json';mesh.save(path,values)
        fixture_data=json.loads(path.read_text())
        exact=ExtendedExactField(fixture_data)
    assert exact.radial(Q(3,2),Q(3,2))==Q(1,2)
    assert exact.terminal_time==3
    pool=route_pool(mesh)+two_interior_pool(mesh)
    chosen=pool[::max(1,len(pool)//100)]
    max_error=0.
    for functional in chosen:
        specialized=functional.value_gradient(values)[0]
        generic=RouteFunctional(mesh,functional.route).value_gradient(values)[0]
        max_error=max(max_error,abs(specialized-generic))
    assert max_error<2e-11,max_error
    native_m2=full_native_m2_pool(mesh)
    native_m2_chosen=native_m2[::max(1,len(native_m2)//100)]
    native_m2_error=0.
    for functional in native_m2_chosen:
        generic=RouteFunctional(mesh,functional.route).value_gradient(values)[0]
        native_m2_error=max(native_m2_error,abs(generic-functional.value_gradient(values)[0]))
    assert native_m2_error<2e-11,native_m2_error
    scanner=InwardScanner(fixture_data);inward_costs=scanner.evaluate()
    selected=np.linspace(0,len(inward_costs)-1,min(100,len(inward_costs)),dtype=int)
    inward_error=0.
    for index in selected:
        generic=RouteFunctional(mesh,scanner.route(index)).value_gradient(values)[0]
        inward_error=max(inward_error,abs(generic-inward_costs[index]))
    assert inward_error<2e-11,inward_error
    routes=[[(0,Q(1,3)),(Q(2,3),1),(Q(8,3),-1)],
            [(0,Q(-1,3)),(Q(4,3),1),(Q(10,3),-1)],
            [(0,0),(Q(3,4),Q(3,4)),(Q(7,4),Q(-1,4)),(3,1),(5,-1)]]
    payoffs=[]
    for route in routes:
        rational=exact.unit_route_payoff(route)
        generic=RouteFunctional(mesh,route).value_gradient(values)[0]
        assert abs(float(rational)-generic)<2e-11,(rational,generic)
        payoffs.append(str(rational))
    print(json.dumps(dict(status='PASS',same_old_domain=True,
                         whole_extended_domain_area=area,
                         exact_late_center_mass='1/2',specialized_comparisons=len(chosen),
                         maximum_specialized_error=max_error,native_inward_checks=len(selected),
                         full_native_m2_checks=len(native_m2_chosen),maximum_native_m2_error=native_m2_error,
                         maximum_native_inward_error=inward_error,exact_unit_costs=payoffs)))


if __name__=='__main__':main()
