"""Optional independent C++ exact-response cross-check.
Build first: g++ -O2 -std=c++17 exact_ordered.cpp -o exact_ordered
"""
from pathlib import Path
from fractions import Fraction
import json, subprocess
root=Path(__file__).resolve().parent
d=json.loads((root/'princess_strategy.json').read_text())
h=d['paths_h'];w=d['weights_h'];S=d['S']
paths=[[[t,-x] for t,x in p] for p in h[::-1]]+h
weights=w[::-1]+w
lines=[f'{len(paths)} 1000000000 {S}']
for p,a in zip(paths,weights):
    lines.append(f'{len(p)} {a}')
    lines.extend(f'{t} {x}' for t,x in p)
for option in ([],['--naive']):
    run=subprocess.run([str(root/'exact_ordered'),*option],input='\n'.join(lines)+'\n',text=True,capture_output=True,check=True)
    header=list(map(int,run.stdout.splitlines()[0].split()))
    num,den,nodes,leaves,dominated,bounded,complete,count=header
    assert complete==1 and Fraction(num,den)==Fraction(d['value'])
    assert (nodes,leaves,dominated,bounded)==(48228,7,21262,2904)
    print('PASS: C++ '+('naive' if option else 'cached')+' exact response = '+str(Fraction(num,den)))
    print('Nodes, terminal, dominated, lower-bound pruned:',nodes,leaves,dominated,bounded)
