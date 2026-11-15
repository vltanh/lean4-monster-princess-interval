#!/usr/bin/env python3
"""Test physical-group separation, exact group rounding, and resumable acceptance."""
from fractions import Fraction as Q
import json
from pathlib import Path
import subprocess
import sys
import tempfile

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
from search import C,FixedMaster,physical_marginals,ROOT


def main():
    with tempfile.TemporaryDirectory(prefix="fixed_marginal_test_") as folder:
        folder=Path(folder);n=2;R=2*n
        # Equal scalar clock planes from separate oriented physical groups
        # must not be merged before enforcing their separate probability rows.
        paths=[]
        for direction,weight in [(1,3),(-1,4)]:
            moves=[direction]*R+[-direction]*(2*R)
            left=3*R if direction==1 else R;right=R if direction==1 else 3*R
            paths.append({"start_grid":0,"moves":moves,"minus_charges":[[0,left]],
                "plus_charges":[[0,right]],"weight_numerator":str(weight)})
        law={"n":n,"weight_denominator":"7","paths":paths}
        master=FixedMaster(law,folder/"native")
        for p in paths:master.add_plan(C.lift_plan(p,1))
        assert len(master.columns)==2
        assert master.columns[0]["mass"]==master.columns[1]["mass"]
        assert master.columns[0]["coeff"]==master.columns[1]["coeff"]=={}
        for proposal in ([1.,0.],[0.,1.],[0.,0.],[.2,.8]):
            assert master.rationalize(proposal)==[3,4]
        cp=folder/"seed.checkpoint.json"
        C.write_json(cp,{"n":n,"columns":master.columns,"weights":[3/7,4/7]})
        subprocess.run(["node",str(ROOT/"packages/interval_clock_grid/qout_primal_certificate.cjs"),"--make",str(cp),str(folder/"seed")],
                       check=True,capture_output=True,text=True)
        seed=folder/"seed.physical.json"
        output=folder/"run"
        command=[sys.executable,str(HERE/"search.py"),"--input",str(seed),"--iterations","3","--seconds","60",
                 "--lp-seconds","20","--price-every","1","--alternative-cuts","4","--target-upper","10","--output",str(output)]
        subprocess.run(command,check=True,capture_output=True,text=True)
        first=json.loads((output/"summary.json").read_text())
        subprocess.run(command+["--resume",str(output/"checkpoint.json")],check=True,capture_output=True,text=True)
        second=json.loads((output/"summary.json").read_text())
        assert second["iterations_total"]>first["iterations_total"]
        assert Q(second["best_certified_global_upper"])<=Q(first["best_certified_global_upper"])
        original=json.loads(seed.read_text())
        candidate=json.loads((output/"oracle.current.sparse.json").read_text())
        assert physical_marginals(candidate)==physical_marginals(original)
        dense=subprocess.run(["node",str(ROOT/"packages/interval_mixture_cut/dense_replay.cjs"),str(output/"oracle.current.sparse.json"),str(folder/"dense")],
                             check=True,capture_output=True,text=True)
        assert json.loads(dense.stdout)["global_upper"]==candidate["global_upper"]
        refined=folder/"refined"
        refined_command=list(command);refined_command[-1]=str(refined)
        subprocess.run(refined_command+["--n","4","--native-flow"],check=True,capture_output=True,text=True)
        finer=json.loads((refined/"oracle.current.sparse.json").read_text())
        lifted={"paths":[dict(C.lift_plan(p,2),weight_numerator=p["weight_numerator"]) for p in original["paths"]]}
        assert finer["n"]==4 and physical_marginals(finer)==physical_marginals(lifted)
        dense=subprocess.run(["node",str(ROOT/"packages/interval_mixture_cut/dense_replay.cjs"),str(refined/"oracle.current.sparse.json"),str(folder/"dense_refined")],
                             check=True,capture_output=True,text=True)
        assert json.loads(dense.stdout)["global_upper"]==finer["global_upper"]
        blocked=folder/"blocked"
        blocked_command=list(command);blocked_command[-1]=str(blocked)
        subprocess.run(blocked_command+["--target-upper","0"],check=True,capture_output=True,text=True)
        report=json.loads((blocked/"summary.json").read_text())
        assert report["iterations_total"]==0 and report["stop_reason"]=="all_calendar_qout_family_floor_reaches_target"
        replay=subprocess.run([sys.executable,str(HERE/"verify_obstruction.py"),"--result-directory",str(blocked)],
                              check=True,capture_output=True,text=True)
        assert json.loads(replay.stdout)["status"]=="PASS"
    print(json.dumps({"status":"PASS","checks":["no cross-physical-group column merging","exact group totals including zero floating weights",
        "complete fixed-marginal driver","independent dense replay","same-directory restart retains physical probabilities and best upper",
        "clock refinement with native flow preserves physical paths and probabilities exactly","independent exact all-calendar obstruction and early stop"]}))


if __name__=="__main__":main()
