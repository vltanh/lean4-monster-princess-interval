#!/usr/bin/env python3
"""Independent exact unit-path checks for the global survival representation."""
from fractions import Fraction as Q
from pathlib import Path
import random
import sys

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'packages/interval_turn_density'))
sys.path.insert(0,str(ROOT/'packages/interval_turn_sheet'))
from atom_survival_cut import SurvivalCut,light_route
from verify_center_memory import first_capture


def path_atom(route):
    return dict(kind='PATH',parameters=tuple(c for point in route for c in point))


def main():
    # Every old named family embeds identically, in both orientations.
    named=[dict(kind='M1',parameters=(Q(-1),)),
           dict(kind='M1',parameters=(Q(2,3),)),
           dict(kind='M2',parameters=(Q(-3,4),Q(7,8))),
           dict(kind='M2',parameters=(Q(1,4),Q(5,4))),
           dict(kind='M3',parameters=(Q(-1,4),Q(1,2),Q(3,4))),
           dict(kind='M3',parameters=(Q(1,4),Q(3,4),Q(1))),
           dict(kind='I',parameters=(Q(3,4),Q(-1,2),Q(3,2)))]
    generic=[path_atom(light_route(a)) for a in named]
    counts={'named_embeddings':0,'reward_identities':0,'physical_limits':0,
            'rational_global_cut':0,'invalid_routes_rejected':0}
    for old,new in zip(named,generic):
        for reflect in (False,True):
            assert light_route(old,reflect)==light_route(new,reflect)
            counts['named_embeddings']+=1
    # Additional genuine multi-turn routes; no fixed turn-family assumption.
    rng=random.Random(20261111)
    for k in (3,4,5,7):
        x=Q(rng.randrange(-6,7),8); t=Q(0); physical=[(t,x)]
        direction=1
        for j in range(k):
            target=Q(rng.randrange(-7,8),8)
            if target==x: target=Q(1,16)+x
            t+=abs(target-x);x=target;physical.append((t,x))
        for target in (Q(-1),Q(1)):
            if target!=x: t+=abs(target-x);x=target;physical.append((t,x))
        generic.append(path_atom([(t+x,t-x) for t,x in physical]))
    model=SurvivalCut(generic,lexicographic=True)
    for sample in range(12):
        labels=[];previous=0
        for lo,hi in model.bounds:
            label=rng.randrange(max(lo,previous),hi+1)
            labels.append(label);previous=label
        values=tuple(model.levels[k] for k in labels)
        path=model.realize(values,epsilon=Q(1,2**30))
        for j,atom in enumerate(generic):
            rewards=model.unit_rewards(j)
            reward=sum((weight for (positive,bits),weight in rewards.items()
                        if all((labels[i]>=k)==positive for i,k in bits)),Q(0))/4
            expected=model.atom_value(atom,values)
            assert reward==expected
            counts['reward_identities']+=1
            monster=[((u+v)/2,(u-v)/2) for u,v in light_route(atom)]
            captures=[first_capture(path,monster,sign) for sign in (1,-1)]
            assert None not in captures
            actual=sum(captures,Q(0))/2
            assert actual>=expected-Q(1,2**20),(sample,j,actual,expected)
            counts['physical_limits']+=1
    weights=[Q(j+1,sum(range(1,len(generic)+1))) for j in range(len(generic))]
    cut=model.solve(weights)
    assert sum(w*model.atom_value(a,cut.minimum_values)
               for a,w in zip(generic,weights))==cut.value
    counts['rational_global_cut']+=1
    invalid=[[(0,0),(1,1),(3,1),(3,5)], # waiting / diagonal in light coordinates
             [(0,0),(3,0),(3,5)],       # leaves arena
             [(0,0),(1,0),(1,3)],       # only one endpoint
             [(Q(1,2),0),(2,0),(2,4)]] # starts after time zero
    for route in invalid:
        try: light_route(path_atom(route))
        except AssertionError: counts['invalid_routes_rejected']+=1
        else: raise AssertionError(('invalid route accepted',route))
    print('PASS',sum(counts.values()),'generic unit-route checks:',counts)


if __name__=='__main__': main()
