#!/usr/bin/env python3
"""Independent exact audits of the global atomic survival closure."""
from collections import Counter
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
import random
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"interval_turn_sheet"))
from atom_survival_cut import SurvivalCut,light_route
from verify_center_memory import first_capture


def physical_route(atom,reflected=False):
    return [((u+v)/2,(u-v)/2) for u,v in light_route(atom,reflected)]


def reward_value(model,rewards,values):
    labels=[model.levels.index(value) for value in values]
    value=Q(0)
    for (positive,bits),weight in rewards.items():
        if all((labels[i]>=k)==positive for i,k in bits):
            value+=weight
    return value/4


def main():
    counts=Counter()
    small=[
        [{"kind":"M1","parameters":[Q(0)]}],
        [{"kind":"M1","parameters":[Q(-1)]}],
        [{"kind":"M2","parameters":[Q(0),Q(1)]}],
        [{"kind":"M3","parameters":[Q(0),Q(1,2),Q(1)]}],
        [{"kind":"I","parameters":[Q(1,2),Q(0),Q(1)]}],
    ]
    for atoms in small:
        model=SurvivalCut(atoms)
        weights=[Q(1)]*len(atoms)
        rewards=model.rewards(weights)
        best=None
        for labels in product(*(range(lo,hi+1) for lo,hi in model.bounds)):
            if any(x>y for x,y in zip(labels,labels[1:])): continue
            values=tuple(model.levels[k] for k in labels)
            direct=sum((w*model.atom_value(atom,values)
                        for atom,w in zip(atoms,weights)),Q(0))
            expanded=reward_value(model,rewards,values)
            assert direct==expanded,(atoms,values,direct,expanded)
            best=direct if best is None else max(best,direct)
            counts["exhaustive capture/reward identities"]+=1
        answer=model.solve(weights,retain_face=True)
        assert answer.value==best
        assert model.atom_value(atoms[0],answer.minimum_values)==best
        assert model.atom_value(atoms[0],answer.maximum_values)==best
        counts["exact exhaustive global cuts and both lattice extrema"]+=1

    for atoms in small[:3]:
        model=SurvivalCut(atoms,lexicographic=True)
        rewards=model.rewards([Q(1)])
        best=None
        for labels in product(*(range(lo,hi+1) for lo,hi in model.bounds)):
            if any(x>y for x,y in zip(labels,labels[1:])): continue
            values=tuple(model.levels[k] for k in labels)
            direct=model.atom_value(atoms[0],values)
            assert reward_value(model,rewards,values)==direct
            best=direct if best is None else max(best,direct)
            counts["exhaustive lexicographic capture/reward identities"]+=1
        answer=model.solve([Q(1)],retain_face=True)
        assert answer.value==best
        counts["exact lexicographic global cuts"]+=1

    atoms=[{"kind":"M1","parameters":[x]} for x in
           (Q(-1),Q(-3,4),Q(-1,3),Q(0),Q(1,3),Q(3,4),Q(1))]
    atoms += [{"kind":"M2","parameters":[x,s]} for x,s in
              ((Q(-3,4),Q(7,8)),(Q(-1,4),Q(5,4)),(Q(0),Q(1)),
               (Q(1,4),Q(3,4)),(Q(3,4),Q(5,4)))]
    atoms += [{"kind":"M3","parameters":[x,s,t]} for x,s,t in
              ((Q(-1,4),Q(1,2),Q(3,4)),(Q(0),Q(1,2),Q(1)),
               (Q(1,4),Q(3,4),Q(1)))]
    atoms += [{"kind":"I","parameters":[z,v,s]} for z,v,s in
              ((Q(1,2),Q(-1,4),Q(3,4)),(Q(3,4),Q(-1,2),Q(3,2)),
               (Q(1,2),Q(1,2),Q(1)),(Q(1),Q(-1),Q(1)))]
    model=SurvivalCut(atoms,trace=Q(1,128))
    rng=random.Random(327610)
    units=[model.unit_rewards(j) for j in range(len(atoms))]
    for fixture in range(24):
        labels,previous=[],0
        for lo,hi in model.bounds:
            k=rng.randrange(max(lo,previous),hi+1)
            labels.append(k)
            previous=k
        values=tuple(model.levels[k] for k in labels)
        path=model.realize(values,epsilon=Q(1,2**32))
        for j,atom in enumerate(atoms):
            expected=model.atom_value(atom,values)
            expanded=reward_value(model,units[j],values)
            assert expanded==expected
            counts["mixed-family exact capture/reward identities"]+=1
            times=[first_capture(path,physical_route(atom),sign) for sign in (1,-1)]
            assert None not in times
            actual=sum(times,Q(0))/2
            assert actual>=expected-Q(1,2**26),(fixture,atom,actual,expected)
            counts["legal strict-speed physical pair comparisons"]+=1
    weights=[Q(j+1,sum(range(1,len(atoms)+1))) for j in range(len(atoms))]
    result=model.solve(weights,retain_face=True)
    for values in (result.minimum_values,result.maximum_values):
        path=model.realize(values,epsilon=Q(1,2**36))
        actual=Q(0)
        for atom,weight in zip(atoms,weights):
            times=[first_capture(path,physical_route(atom),sign) for sign in (1,-1)]
            assert None not in times
            actual+=weight*sum(times,Q(0))/2
        assert actual>=result.value-Q(1,2**30)
        counts["complete-law physical realization of cut extrema"]+=1
    lex=SurvivalCut(atoms,lexicographic=True)
    answer=lex.solve(weights,retain_face=True)
    for values in (answer.minimum_values,answer.maximum_values):
        path=lex.realize(values,epsilon=Q(1,2**28))
        actual=Q(0)
        for atom,weight in zip(atoms,weights):
            times=[first_capture(path,physical_route(atom),sign) for sign in (1,-1)]
            assert None not in times
            actual+=weight*sum(times,Q(0))/2
        assert actual>=answer.value-Q(1,2**24)
        counts["complete-law lexicographic strict-speed realizations"]+=1
    print("PASS:",sum(counts.values()),"atomic survival-cut checks")
    for key,value in counts.items(): print(" ",key+":",value)
    print("Scope: exact event reward/closure identities and legal limit realizations; no game equilibrium claim")


if __name__=="__main__":
    main()
