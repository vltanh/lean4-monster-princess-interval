#!/usr/bin/env python3
"""Bounded global rank-phase probes, rescored on the actual continuous CDF.

Every finite search is unrestricted against its supplied quantile law. The
rank-discrepancy lower bound and exact continuous attack cost are kept separate.
Phases change at fixed support size; this is not a mesh-refinement loop.
"""
import argparse
from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import time

from continuous_response_extract import extract

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'packages/interval_cdf_discovery'))
from continuum_field import ExtendedExactField


def main():
    parser=argparse.ArgumentParser();parser.add_argument('field');parser.add_argument('--binary',required=True)
    parser.add_argument('--radial-count',type=int,default=16);parser.add_argument('--phases',default='1/4,1/2,3/4')
    parser.add_argument('--starts',default='free',help='Comma-separated free and/or exact fixed starting positions')
    parser.add_argument('--node-limit',type=int,default=200000);parser.add_argument('--output',required=True)
    args=parser.parse_args();started=time.time()
    raw=Path(args.field).read_bytes();data=json.loads(raw);field=ExtendedExactField(data)
    results=[]
    with tempfile.TemporaryDirectory(prefix='continuous_response_')as temp:
        frozen=Path(temp)/'field.json';frozen.write_bytes(raw)
        for phase in map(Q,args.phases.split(',')):
            quantiles=extract(frozen,args.radial_count,phase)
            text=[str(quantiles['total_count'])+' '+quantiles['terminal_time']]
            for weight,path in zip(quantiles['weights'],quantiles['paths']):
                text.append(weight+' '+str(len(path)));text.extend(t+' '+x for t,x in path)
            file=Path(temp)/'quantiles.txt';file.write_text('\n'.join(text)+'\n')
            for start in args.starts.split(','):
                command=[args.binary,str(file),str(args.node_limit)]
                if start!='free':command.extend(['--start',str(Q(start))])
                run=subprocess.run(command,check=True,text=True,capture_output=True)
                result=json.loads(run.stdout)
                actual=field.unit_route_payoff(result['route'])
                assert Q(0)<=actual
                error=Q(quantiles['uniform_payoff_error'])
                assert abs(actual-Q(result['value']))<=error
                result.update(rank_phase=str(phase),uniform_payoff_error=str(error),
                              continuous_route_payoff=str(actual),continuous_route_decimal=float(actual),
                              continuous_lower_bound=str(Q(result['lower_bound'])-error))
                results.append(result)
                print('PHASE',str(phase),'START',start,'complete',result['complete'],'states',result['processed'],
                      'continuous attack',float(actual),flush=True)
    best=min(results,key=lambda r:Q(r['continuous_route_payoff']))
    lower=max([Q(0)]+[Q(r['continuous_lower_bound'])for r in results if r['fixed_start']is None])
    output=dict(scope='Exact unrestricted finite-quantile responses with uniform all-monster transfer; '
                'a bracket and supplied attacks for this specified continuous law, not a game-value certificate.',
                input=Path(args.field).name,input_sha256=hashlib.sha256(raw).hexdigest(),
                radial_count=args.radial_count,phases=args.phases,starts=args.starts,
                best_attack=best,continuous_response_bracket=[str(lower),best['continuous_route_payoff']],
                probes=results,seconds=time.time()-started,
                stopping_rule='Fixed rank count and the supplied phase/start choices; no rank-refinement loop.',
                lower_bound_scope='Only free-start probes contribute to the unrestricted lower bound; fixed-start bounds are conditional.')
    Path(args.output).write_text(json.dumps(output,indent=2)+'\n')
    print('BEST',best['continuous_route_decimal'],'phase',best['rank_phase'],'seconds',output['seconds'])


if __name__=='__main__':main()
