#!/usr/bin/env python3
"""Refine a saved isotone dual, then exactly price the finer physical bank.

Interpolation is candidate construction; the repaired integer profile and
exhaustive normalized pricing establish the reported game-value lower.
"""
import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import time

from solve_normalized import Master


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('seed',type=Path)
    parser.add_argument('n',type=int)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--denominator',type=int,default=10**9)
    parser.add_argument('--paths',type=int,default=0)
    args=parser.parse_args();started=time.monotonic()
    seed=json.loads(args.seed.read_text())
    master=Master(args.n,args.output.parent/(args.output.stem+'.work'),args.denominator,True)
    candidate=master.interpolate_seed(seed)
    priced,table=master.price(candidate,args.paths)
    units=int(priced['minimum_units']);scale=4*args.n*args.denominator
    output={'scope':'Exact feasible dual on a refined normalized physical grid bank; global game-value lower uses left-floor atomization, bank normalization and common quantization.',
            'n':args.n,'field_denominator':str(args.denominator),'normalized_profile':True,
            'radial_nodes':[[j,k,str(int(table[j,k]))] for j in range(master.H+1)
                            for k in range(1,master.R+1) if (j+k)%2==0],
            'minimum_units':str(units),'objective_denominator':str(scale),
            'normalized_bank_dual_value':str(Fraction(units,scale)),
            'global_lower':str(Fraction(units-2*args.denominator,scale)),
            'global_lower_decimal':float(Fraction(units-2*args.denominator,scale)),
            'pricing':priced,'source_seed_sha256':hashlib.sha256(args.seed.read_bytes()).hexdigest(),
            'native_source_sha256':hashlib.sha256((Path(__file__).parent/'price_normalized.cpp').read_bytes()).hexdigest(),
            'seconds':time.monotonic()-started}
    args.output.write_text(json.dumps(output,separators=(',',':'))+'\n')
    print(json.dumps({k:v for k,v in output.items() if k not in ['radial_nodes','pricing']},indent=2))


if __name__=='__main__':
    main()
