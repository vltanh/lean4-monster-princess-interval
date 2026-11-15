#!/usr/bin/env python3
"""Small two-parameter structural search; fixed density bins throughout."""

import json
import subprocess
import sys
from pathlib import Path

import numpy as np
from scipy.optimize import minimize


def main():
    directory=Path(__file__).resolve().parent
    trial=directory/'affine_outer_trial.json'
    history=[];best=None;cache={}
    def evaluate(x):
        nonlocal best
        offset,slope=map(float,x)
        key=(round(offset,10),round(slope,10))
        if key in cache:return cache[key]
        command=[sys.executable,'-B',str(directory/'discover_separated.py'),
                 '--left','0.625','--offset',str(offset),'--slope',str(slope),
                 '--rounds','5','--output',trial.name]
        result=subprocess.run(command,text=True,capture_output=True)
        if result.returncode:
            raise RuntimeError(result.stderr[-3000:])
        data=json.loads(trial.read_text())
        row=dict(offset=offset,slope=slope,objective=data['objective'],
                 response=data['response'],
                 inequality_dual_mass=data['log'][-1]['structural_dual_mass'],
                 equality_dual_mass=data['log'][-1]['structural_equality_dual_mass'])
        history.append(row)
        if best is None or row['response']<best['response']:
            best=data
            best['outer_parameters']=dict(offset=offset,slope=slope)
            (directory/'affine_optimized_discovery.json').write_text(json.dumps(best,indent=2))
        cache[key]=row['response']
        (directory/'affine_outer_search.json').write_text(json.dumps(dict(
            scope='Fixed-bin two-parameter structural discovery; no exact bound or saddle.',
            trials=history,stopping_rule='At most ten fixed-profile density solves; no bin refinement.'),indent=2))
        print('AFFINE_TRIAL',row,flush=True)
        return row['response']
    result=minimize(evaluate,np.array([.01,.12]),method='Nelder-Mead',
                    bounds=[(0,.08),(.005,.4)],
                    options={'maxfev':10,'xatol':.002,'fatol':1e-7,
                             'initial_simplex':np.array([[.01,.12],[.03,.12],[.01,.24]])})
    print('BEST',best['outer_parameters'],'RESPONSE',best['response'],flush=True)
    print('STOP',result.message,flush=True)
    trial.unlink(missing_ok=True)


if __name__=='__main__':main()
