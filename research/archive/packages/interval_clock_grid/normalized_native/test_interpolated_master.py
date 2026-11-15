#!/usr/bin/env python3
"""Cross-check interpolation coefficients against the existing exact CDF evaluator."""
from fractions import Fraction as Q
import json
from pathlib import Path
import subprocess
import tempfile
import numpy as np

from interpolated_master import InterpolatedMaster


def main():
    here=Path(__file__).resolve().parent
    rng=np.random.default_rng(60813);requests=[];expected=[];calendars=0
    with tempfile.TemporaryDirectory(prefix='interpolated_field_') as folder:
        for coarse_n in (1,2):
            for ratio in (2,3):
                model=InterpolatedMaster(coarse_n*ratio,coarse_n,Path(folder),101)
                values=rng.random(model.K)
                coarse=model.coarse.repair(values);fine=model.repair(values)
                nodes=[]
                for k in range(2*coarse_n+1):
                    for j in range(k%2,16*coarse_n+1,2):
                        a=int(coarse[j,k]) if j<=12*coarse_n else 0
                        nodes.append([j,k,str(a)])
                strategy={'format':'clock-grid-princess-p1-v1','n':coarse_n,
                          'interpolation_epsilon':'1/2','cdf_denominator':'101',
                          'radial_nodal':nodes,'outward_time':2,'absorption_time':3}
                points=[];want=[]
                for j in range(model.C+1):
                    for k in range(j%2,model.R+1,2):
                        points.append([str(Q(j,2*model.n)),str(Q(k,2*model.n))])
                        want.append(Q(int(fine[j,k]),model.D))
                requests.append({'strategy':strategy,'points':points});expected.append(want)
                priced,_=model.price(values,12)
                for path in priced['paths']:
                    plan,mass,coeff=model.calendar(path,fine)
                    positions=[plan['start_grid']]
                    for step in plan['moves']:positions.append(positions[-1]+step)
                    direct=Q(0)
                    for name,sign in [('minus_charges',1),('plus_charges',-1)]:
                        for j,a in plan[name]:
                            k=sign*positions[j]
                            direct+=a*Q(model.D+(1 if k>=0 else -1)*int(fine[j,abs(k)]),model.D)
                    W=model.interpolation_denominator
                    algebra=Q(mass)+sum(Q(round(v*W),W)*Q(int(coarse[model.nodes[i]]),101)
                                           for i,v in coeff.items())
                    assert direct==algebra
                    calendars+=1
        code='''const fs=require('node:fs');const E=require(process.argv[1]);
const data=JSON.parse(fs.readFileSync(0,'utf8'));const answer=data.map(x=>{
const f=E.createEvaluator(x.strategy);return x.points.map(([t,r])=>String(f.rawTrace(t,r).mul(2).sub(1)));});
process.stdout.write(JSON.stringify(answer));'''
        result=subprocess.run(['node','-e',code,str(here.parent/'extract_princess.cjs')],
                              input=json.dumps(requests),text=True,stdout=subprocess.PIPE,check=True)
        actual=json.loads(result.stdout)
        for row,want in zip(actual,expected):
            assert list(map(Q,row))==want
    print(json.dumps({'status':'PASS','coarse_grids':[1,2],'refinements':[2,3],
                      'exact_cdf_nodes':sum(map(len,expected)),
                      'independent_clock_column_identities':calendars},indent=2))


if __name__=='__main__':main()
