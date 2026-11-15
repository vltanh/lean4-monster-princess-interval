#!/usr/bin/env python3
"""Exact physical attack upper against one full-width interpolated CDF.

This checks a single physical path, not an exhaustive response search. Its
causal running-record left rectangles upper-bound the actual capture time.
The full-width common-threshold interpolation fixes every sampled light-grid
vertex; a separate rational JavaScript evaluator checks those sample values.
"""
from __future__ import annotations
import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'packages/interval_clock_grid/normalized_native'))
from verify_native_field import load_table


def verify(field_path, witness_path, check_interpolator=True):
    data,table,field_hash = load_table(field_path)
    witness = json.loads(witness_path.read_text())
    assert witness['field_sha256'] == field_hash
    n,D = data['n'],int(data['field_denominator'])
    assert data.get('normalized_profile') is True
    R,H = 2*n,12*n
    def node(j,k):return int(table[j*(R+1)+abs(k)])
    cones = 0
    for j in range(H+1):
        for k in range(j%2,R+1,2):
            value = node(j,k)
            assert 0 <= value <= D and (k != 0 or value == 0)
            if k < R:
                for step in (-1,1):
                    if 0 <= j+step <= H:
                        assert value <= node(j+step,k+1)
                        cones += 1
    path = witness['path']
    start = path['start_grid']
    assert isinstance(start,int) and not isinstance(start,bool) and abs(start)<=R and start%2 == 0
    positions = [start]
    for step in path['moves']:
        assert isinstance(step,int) and not isinstance(step,bool) and step in (-1,1)
        positions.append(positions[-1]+step)
    assert max(map(abs,positions)) <= R
    assert positions.index(0) <= 4*n
    left,right = positions.index(-R),positions.index(R)
    assert max(left,right) <= H
    upper = Fraction(0)
    calendars = {}
    for name,sign,end in [('minus',1,left),('plus',-1,right)]:
        minimum = Fraction(1);when = 0;counts = {}
        for j in range(end):
            k = sign*positions[j]
            value = Fraction(D+(1 if k>=0 else -1)*node(j,k),2*D)
            if value < minimum:minimum,when = value,j
            counts[when] = counts.get(when,0)+1
            upper += minimum/Fraction(2*n)
        calendars[name] = sorted(counts.items())
    assert upper == Fraction(witness['left_rectangle_upper'])
    threshold = Fraction(witness['known_unrestricted_game_lower'])
    assert upper < threshold
    interpolation_samples = 0
    if check_interpolator:
        strategy = {'format':'clock-grid-princess-p1-v1','n':n,
                    'interpolation_epsilon':'1/2','cdf_denominator':str(D),
                    'radial_nodal':[[j,k,str(node(j,k) if j<=H else 0)]
                         for k in range(R+1) for j in range(k%2,16*n+1,2)],
                    'outward_time':2,'absorption_time':3}
        points = [[str(Fraction(j,2*n)),str(Fraction(k,2*n))]
                  for j,k in enumerate(positions[:max(left,right)])]
        code = '''const fs=require('node:fs');
const E=require(process.argv[1]);const x=JSON.parse(fs.readFileSync(0,'utf8'));
const f=E.createEvaluator(x.strategy);
process.stdout.write(JSON.stringify(x.points.map(([t,r])=>String(f.interiorTrace(t,r)))));'''
        result = subprocess.run(['node','-e',code,str(ROOT/'packages/interval_clock_grid/extract_princess.cjs')],
                input=json.dumps({'strategy':strategy,'points':points}),text=True,
                stdout=subprocess.PIPE,check=True)
        actual = list(map(Fraction,json.loads(result.stdout)))
        expected = [Fraction(D+(1 if k>=0 else -1)*node(j,k),2*D)
                    for j,k in enumerate(positions[:max(left,right)])]
        assert actual == expected
        interpolation_samples = len(actual)
    return {'status':'PASS',
            'scope':'One legal physical Monster path bounds the security of this full-width ordered-quantile Princess law strictly below an already certified unrestricted game lower. This is not a ceiling for all low-variation CDFs.',
            'field_sha256':field_hash,'witness_sha256':hashlib.sha256(witness_path.read_bytes()).hexdigest(),
            'n':n,'physical_start':str(Fraction(start,2*n)),
            'physical_turns':sum(a!=b for a,b in zip(path['moves'],path['moves'][1:])),
            'completion_time':str(Fraction(max(left,right),2*n)),
            'capture_expectation_upper':str(upper),'capture_expectation_upper_decimal':float(upper),
            'known_unrestricted_game_lower':str(threshold),
            'strict_gap_to_game_lower':str(threshold-upper),
            'checked_cone_inequalities':cones,'independent_interpolation_samples':interpolation_samples,
            'causal_calendars':calendars}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('field',type=Path)
    parser.add_argument('witness',type=Path)
    parser.add_argument('--output',type=Path)
    args = parser.parse_args()
    answer = verify(args.field,args.witness)
    if args.output:args.output.write_text(json.dumps(answer,indent=2)+'\n')
    print(json.dumps(answer,indent=2))
