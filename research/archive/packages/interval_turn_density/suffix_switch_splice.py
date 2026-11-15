#!/usr/bin/env python3
"""Evaluate a genuine extra-suffix switch under the complete spliced primitives."""
import json
from pathlib import Path
import numpy as np
from scipy.optimize import brentq
from splice_endpoint_tail import TailFamily,Splice


def main():
    here=Path(__file__).resolve().parent
    seed=json.loads((here/'split_edge_affine_discovery.json').read_text())
    splice=json.loads((here/'endpoint_tail_splice.json').read_text())['matches'][1]
    family=TailFamily();law=Splice(seed,family,splice['amplitude'],splice['ell_cutoff_deficit'])
    nodes,weights=family.Bmodel.base.nodes,family.Bmodel.base.weights
    def Gtail(e):
        t=min(e,law.cut)
        val=t*float(family.get('g',t*np.exp(-nodes),law.B,law.w)@weights)
        return val+law.base_integral('g',law.cut,e)
    def Ftail(a):return law.primitive('P',1-a)-Gtail(1-a)
    def loss(beta):
        # All reported beta values lie below the f-tail start.  The integral
        # is therefore an exact polynomial evaluation of the seed density.
        if beta>1-law.cut:raise ValueError('Extend the weighted tail primitive before using this range')
        total=0.
        for j,f in enumerate(law.dens['f']):
            lo=law.knots[j];hi=min(beta,law.knots[j+1])
            if hi>lo:total+=f*((hi-hi*hi/2)-(lo-lo*lo/2))
        return float(total)
    y=seed['late_left']
    assert y<seed['turn'] and all(law.dens['ell'][j]==0 for j in range(len(law.knots)-1)if law.knots[j]<y)
    def gain(a,beta):return ((y+beta)*Ftail(a)-loss(beta))/law.norm
    cases=[(.991696693624,.585131232),(.99013684913,.54648347435),(.99,.55),(.995,.55),(.999,.55)]
    result=[]
    for a,beta in cases:
        row=dict(a=a,c=-beta,y=y,Fbar=Ftail(a)/law.norm,weighted_f_loss=loss(beta)/law.norm,
                 four_payoff_gain=gain(a,beta),payoff_gain=gain(a,beta)/4)
        grid=sorted(set([0.,1-law.cut]+[float(x)for x in law.knots if 0<x<1-law.cut]))
        roots=[]
        for lo,hi in zip(grid,grid[1:]):
            if gain(a,lo)*gain(a,hi)<0:roots.append(brentq(lambda b:gain(a,b),lo,hi,xtol=2e-13))
        row['switch_beta_roots_below_tail']=roots
        result.append(row);print('SWITCH',json.dumps(row))
    out=dict(scope='Exact suffix-gain formula evaluated with analytic spliced primitives; no whole-game value claim.',
        formula='4Delta=(y+beta)Fbar(a)-integral_0^beta (1-x)f(x)dx; y=late_left<turn and ell=0 below y',
        cases=result)
    dest=here/'suffix_switch_splice.json';dest.write_text(json.dumps(out,indent=2));print('OUTPUT',dest)

if __name__=='__main__':main()
