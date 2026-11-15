#!/usr/bin/env python3
"""Exact cut/mixture separation versus the complete small-grid order LP."""
from fractions import Fraction as Q
import json
from pathlib import Path
import subprocess
import sys
import tempfile

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
from search import ROOT,make_closure_server,CutBank,Master,load_model,rationalize,lift_plan,boundary_routes
from physical_screen import analyze_physical_law,marginal_change,loop_cut,EndpointLoopSeparator,rectangle_field,rectangle_loop_payoff
from princess_retention import verify_archive
import numpy as np


def main():
    total_calls=0
    with tempfile.TemporaryDirectory(prefix="mixture_cut_test_") as folder:
        folder=Path(folder)
        source=json.loads((ROOT/"packages/interval_clock_grid/grid_n2_certificate.json").read_text())
        for n in (2,4):
            work=folder/str(n);work.mkdir()
            master=Master(n,work/"native")
            for p in source["paths"]:master.add_plan(lift_plan(p,n//2))
            complete,_,_=master.solve_lp()
            target=-complete.fun
            cuts=CutBank(master);cuts.sync_columns()
            cuts.add(np.zeros(master.K,dtype=np.uint8));cuts.add(np.ones(master.K,dtype=np.uint8))
            server=make_closure_server(work/"native",native=n==4)
            try:
                extension,_=load_model(server,master,work/"model.json")
                for iteration in range(128):
                    lp=cuts.solve(20);weights=rationalize(lp.x[:-1]);total_calls+=1
                    result=server.ask({"weights":list(map(str,weights)),"denominator":str(10**12),"prefix":str(work/"oracle"),"alternative_cuts":6,"seed":iteration+17})
                    event=np.zeros(len(extension.nodes),dtype=np.uint8);event[result["source_side"]]=1
                    table=extension.extend_integer(event)
                    field=np.asarray([table[j,k] for j,k in master.nodes],dtype=np.uint8)
                    assert all(field[a]<=field[b] for a,b in master.order)
                    row=cuts.row(field)
                    actual=Q(sum(int(v)*w for v,w in zip(row,weights)),4*n*10**12)
                    assert actual==Q(result["global_upper"])
                    cuts.add(field)
                    for side in result["alternative_source_sides"]:
                        event=np.zeros(len(extension.nodes),dtype=np.uint8);event[side]=1
                        alternate=extension.extend_integer(event)
                        alternate=np.asarray([alternate[j,k] for j,k in master.nodes],dtype=np.uint8)
                        assert all(alternate[a]<=alternate[b] for a,b in master.order)
                        alternate_row=cuts.row(alternate)
                        assert Q(sum(int(v)*w for v,w in zip(alternate_row,weights)),4*n*10**12)==actual
                        cuts.add(alternate)
                    if float(actual)-lp.fun<1e-9:break
                else:raise AssertionError("small finite cut problem did not close")
                assert abs(lp.fun-target)<1e-8
                assert abs(float(actual)-target)<1e-8
                dual=cuts.dual_field(lp)
                assert all(dual[a]<=dual[b]+1e-12 for a,b in master.order)
                try:
                    server.ask({"weights":["0"]*len(master.columns),"denominator":str(10**12)})
                except RuntimeError as error:
                    assert "probability" in str(error)
                else:raise AssertionError("accepted zero total mass")
            finally:server.close()
            dense=subprocess.run(["node",str(HERE/"dense_replay.cjs"),str(work/"oracle.sparse.json"),str(work/"dense")],check=True,capture_output=True,text=True)
            assert json.loads(dense.stdout)["global_upper"]==result["global_upper"]
        # End-to-end driver plus actual same-directory restart.
        output=folder/"driver"
        command=[sys.executable,str(HERE/"search.py"),"--n","4","--initial-law",str(work/"dense.physical.json"),
                 "--iterations","3","--seconds","60","--lp-seconds","20","--initial-cuts","3",
                 "--boundary-points","4","--pricing-paths","8","--price-every","2","--mutation-count","8",
                 "--native-flow","--loop-screen","--full-every","1","--output",str(output)]
        subprocess.run(command,check=True,capture_output=True,text=True)
        first=json.loads((output/"summary.json").read_text())
        first_princess=verify_archive(output,decoded_inputs=True)
        assert first_princess
        subprocess.run(command+["--resume",str(output/"checkpoint.json")],check=True,capture_output=True,text=True)
        second=json.loads((output/"summary.json").read_text())
        assert second["iterations_total"]>first["iterations_total"]
        assert Q(second["best_certified_global_upper"])<=Q(first["best_certified_global_upper"])
        assert second["native_flow"] is True
        second_princess=verify_archive(output,decoded_inputs=True)
        assert len(second_princess)>len(first_princess)
        assert second["retained_complete_princess_candidates"]==len(second_princess)
        assert not (output/"last_complete_bank.dual.json").exists()
        assert not (output/"last_complete_bank.checkpoint.json").exists()
        assert (output/"native_optimizer.json").exists()
        # The loop cut is a physical response witness, not an inference from
        # finite test paths. Independently intersect its actual affine paths.
        sys.path.insert(0,str(ROOT/"packages/interval_global_closure"))
        from verify_boundary_layer_kernel import clean,pair_score,princess
        loop_checks=0
        for n in (2,4):
            R=2*n;master=Master(n,folder/("screen"+str(n)))
            plans=[{"start_grid":R,"moves":[-1]*(2*R)+[1]*(2*R),"weight_numerator":"3"},
                   {"start_grid":0,"moves":[1]*R+[-1]*(2*R),"weight_numerator":"7"}]
            law={"n":n,"weight_denominator":"10","paths":plans}
            diagnostic,marginals=analyze_physical_law(law)
            reflected={"n":n,"weight_denominator":"10","paths":[
                dict(p,start_grid=-p["start_grid"],moves=[-x for x in p["moves"]]) for p in plans]}
            reflected["paths"][0]["moves"] += [1,-1]  # A dead, legal post-capture suffix.
            _,same=analyze_physical_law(reflected)
            assert marginal_change(same,marginals)["only_calendars_changed"]
            changed={"n":n,"weight_denominator":"10","paths":[dict(plans[0],weight_numerator="4"),dict(plans[1],weight_numerator="6")]}
            _,different=analyze_physical_law(changed)
            changes=marginal_change(different,marginals)
            assert changes["physical_probability_l1_from_seed"]=="1/5" and changes["new_physical_path_mass"]=="0"
            for target in (Q(17,10),Q(177,100)):
                field,witness=loop_cut(master,diagnostic,target)
                target_path=princess(Q(witness["epsilon"]),Q(witness["h"]))
                actual=Q(0)
                for p in plans:
                    x=p["start_grid"];vertices=[(Q(0),Q(x,R))]
                    for j,d in enumerate(p["moves"],1):
                        x+=d;vertices.append((Q(j,R),Q(x,R)))
                    actual+=Q(int(p["weight_numerator"]),10)*pair_score(clean(vertices),target_path)
                    loop_checks+=1
                assert actual==Q(witness["actual_physical_loop_payoff"])>target
                assert all(field[a]<=field[b] for a,b in master.order)
                # Every generated causal clock majorizes this actual response.
                table=master.repair(np.zeros(master.K))
                clock=Q(0)
                for p in plans:
                    _,mass,coeff=master.calendar(p,table)
                    clock+=Q(int(p["weight_numerator"]),10)*Q(mass+sum(v*int(field[i]) for i,v in coeff.items()),4*n)
                assert clock>=actual
            unsupported={"n":n,"weight_denominator":"1","paths":[{"start_grid":R,
                "moves":[-1,1]+[-1]*(2*R),"weight_numerator":"1"}]}
            diagnostic,_=analyze_physical_law(unsupported)
            assert not diagnostic["endpoint_loop_supported"] and loop_cut(master,diagnostic,Q(0)) is None
        rectangle_checks=rectangle_contact_checks=0
        rng=np.random.default_rng(314159)
        for n in (1,2,3,4):
            master=Master(n,folder/("rectangles"+str(n)))
            unique={}
            for p in boundary_routes(n,n):unique[p["start_grid"],tuple(p["moves"])]=p
            routes=list(unique.values())
            for _ in range(2):
                table=master.repair(rng.random(master.K))
                for p in routes:master.add(p,table)
            cuts=CutBank(master);cuts.sync_columns()
            weights=[1+i%7 for i in range(len(master.columns))];W=sum(weights)
            separator=EndpointLoopSeparator(master)
            mass,suffix=separator.clock_units(cuts,weights)
            found=separator.maximize(cuts,weights,W)
            physical={"n":n,"weight_denominator":str(len(routes)),
                      "paths":[dict(p,weight_numerator="1") for p in routes]}
            chronological=[]
            for p in routes:
                x=p["start_grid"];vertices=[(Q(0),Q(x,2*n))]
                for j,d in enumerate(p["moves"]):
                    if j and d!=p["moves"][j-1]:vertices.append((Q(j,2*n),Q(x,2*n)))
                    x+=d
                vertices.append((Q(len(p["moves"]),2*n),Q(x,2*n)))
                chronological.append(clean(vertices))
            brute_best=None
            for a in range(1,n+1):
                for b in range(1-a,a+1):
                    field=rectangle_field(master,a,b)
                    direct=np.asarray([int((j+k)//2>=a and (k-j)//2>=b) for j,k in master.nodes],dtype=np.uint8)
                    assert np.array_equal(field,direct)
                    units=sum(w*(int(c["mass"])+sum(int(v)*int(field[i]) for i,v in c["coeff"].items()))
                              for c,w in zip(master.columns,weights))
                    assert units==mass+int(suffix[a,b+separator.shift])
                    brute_best=units if brute_best is None else max(brute_best,units)
                    h,epsilon=Q(2*n-2*b+1,2*n),Q(2*n-2*a+1,2*n)
                    # This independent oracle includes actual endpoint contacts
                    # and center-touching loop representatives (a+b=1).
                    turn=(h-epsilon)/2
                    target=clean([(Q(0),1-epsilon),(turn,1-epsilon-turn),(h,Q(1)),(Q(4),Q(1))])
                    actual=sum((pair_score(route,target) for route in chronological),Q(0))/len(routes)
                    assert rectangle_loop_payoff(physical,a,b)==actual
                    rectangle_checks+=1;rectangle_contact_checks+=len(routes)
            assert Q(found["clock_plane_value"])==Q(brute_best,4*n*W)
            assert found["rectangles_separated"]==n*(n+1)
    print(json.dumps({"status":"PASS","exact_closure_calls":total_calls,
        "independent_physical_loop_checks":loop_checks,
        "all_small_grid_rectangles_checked":rectangle_checks,"independent_rectangle_route_contacts":rectangle_contact_checks,
        "checks":["small-grid full LP equality","exact feasible cut extension","dual mixed-field transport",
                  "rational probability rejection","independent dense exact replay","native and BigInt oracle agreement",
                  "checkpoint restart retains best","complete Princess fields survive resumed joint search compactly",
                  "actual loop witness and feasible field cut",
                  "exact physical-probability change versus new geometry","unsupported endpoint loops are not screened",
                  "every n<=4 rectangle versus full weighted clock sums","shifted physical contacts including center and endpoint ties"]}))


if __name__=="__main__":main()
