#!/usr/bin/env python3
"""Global free-CDF maximin synthesis against one combined attack bank.

Only physical transport and normalization are imposed. No endpoint tail,
constant center cone, late derivative, or unimodality ansatz is imposed.
The existing fixed mesh still represents symmetric half-interval quantile
laws with endpoint absorption by time two; it is not proved sufficient for
the unrestricted equilibrium. Every output is an actual complete CDF field,
not merely a list of local matching equations.
"""
from __future__ import annotations
import argparse
from fractions import Fraction
import json
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'packages/interval_cdf_discovery'))
from joint_cdf_field import m1,wait_two_triangles
from joint_cdf_collocation import run


def prepare_routes(extra=(),output=None):
    routes={};rejected=[]
    def add(route,source,label='saved_route'):
        try:
            route=[tuple(float(Fraction(v)) if isinstance(v,str) else float(v) for v in p) for p in route]
        except (TypeError,ValueError):return
        if not route or any(len(p)!=2 for p in route):return
        if abs(route[0][0])>1e-8:return
        route[0]=(0.,route[0][1])
        clean=[]
        for t,x in route:
            if abs(x)>1+1e-8 or t<0:return
            x=max(-1.,min(1.,x))
            if clean and t<=clean[-1][0]+1e-13:
                if abs(x-clean[-1][1])<1e-10:continue
                return
            if clean and abs(x-clean[-1][1])>t-clean[-1][0]+1e-8:
                rejected.append(dict(source=source,reason='speed_bound'));return
            clean.append((t,x))
        if len(clean)<2:return
        # Complete a genuine route to both walls. Only post-prefix motion
        # is added, so this does not hide or replace a discovered attack.
        visited={int(round(x)) for t,x in clean if abs(abs(x)-1)<1e-10}
        for wall in ((1.,-1.) if clean[-1][1]>=0 else (-1.,1.)):
            if len(visited)==2:break
            t,x=clean[-1]
            if x!=wall:clean.append((t+abs(wall-x),wall))
            visited.add(int(wall))
        key=tuple((round(t,11),round(x,11)) for t,x in clean)
        reflected=tuple((t,-x) for t,x in key)
        key=min(key,reflected)
        if key not in routes:
            routes[key]=dict(route=clean,source=source,kind=label)
    def visit(obj,source):
        if isinstance(obj,dict):
            for k,v in obj.items():
                if k in ('route','monster_route','attacking_route'):add(v,source)
                if k=='families' and isinstance(v,list):
                    for row in v:
                        if isinstance(row,dict) and row.get('sign') in ('positive','negative') and 'start' in row:
                            try:add(m1(float(Fraction(row['start']))),source,'continuous_M1_stationary')
                            except (TypeError,ValueError):pass
                visit(v,source)
        elif isinstance(obj,list):
            for item in obj:visit(item,source)
    sources=[]
    for directory in ['interval_cdf_discovery','interval_turn_sheet','interval_turn_density']:
        sources.extend(sorted((ROOT/'packages'/directory).rglob('*.json')))
    for p in extra:
        p=Path(p)
        if p.exists():sources.append(p)
    for source in sources:
        try:payload=json.loads(source.read_text())
        except (ValueError,OSError):continue
        visit(payload,str(source.relative_to(ROOT) if source.is_relative_to(ROOT) else source))
    # Waiting is unconstrained here, so use physical generic route costs,
    # not the optional constant-cone specialized formula.
    for i in range(17):
        for j in range(i,17):
            for sign in (-1,1):
                add(wait_two_triangles(i/16,j/16,1.,sign),'complete_sixteenth_wait_bank','wait_two_triangles')
    result=list(routes.values())
    path=Path(output) if output is not None else HERE/'continuum_attack_routes.json'
    path.write_text(json.dumps(dict(scope='Combined saved attacks and one full fixed wait bank; '
                'not an exhaustive all-monster family.',routes=result,rejected=rejected),indent=2)+'\n')
    print(json.dumps(dict(event='combined_attack_bank',routes=len(result),sources=len(sources),
                         rejected=len(rejected),path=str(path))),flush=True)
    return path


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--maxiter',type=int,default=15)
    parser.add_argument('--tolerance',type=float,default=2e-7)
    parser.add_argument('--tag',default='continuum_free')
    parser.add_argument('--resume',default=str(ROOT/'packages/interval_cdf_discovery/snapshots/initial_inward_repaired.json'))
    parser.add_argument('--extra',nargs='*',default=[str(HERE/'continuum_bank_routes.json')])
    parser.add_argument('--prepare-only',action='store_true')
    parser.add_argument('--lp-method',choices=['highs','highs-ds','highs-ipm'],default='highs-ipm')
    args=parser.parse_args()
    extra=prepare_routes(args.extra)
    if args.prepare_only:return
    run(maxiter=args.maxiter,tolerance=args.tolerance,negative_v=False,positive_v=False,
        extra_routes=str(extra),resume=args.resume,tag=args.tag,include_m3=True,
        output_dir=str(HERE),full_diagnostics=False,include_wait_pool=False,
        include_inward_pool=False,lp_method=args.lp_method)


if __name__=='__main__':main()
