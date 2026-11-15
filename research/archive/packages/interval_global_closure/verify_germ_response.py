#!/usr/bin/env python3
"""Independent exact finite checks for the epsilon-germ response oracle.

The rational checker enumerates all target visitation permutations, uses
segment intersections rather than ordered characteristic inverses, and has
neither dominance nor lower-bound pruning. It is used only on small fixtures.
"""
from fractions import Fraction as Q
from itertools import permutations
import json
from pathlib import Path
import sys
import germ_response as g

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'interval_exact_reduction'))
import exact_oracles


def position(path,t):
    for (a,x),(b,y) in zip(path,path[1:]):
        if a <= t <= b:
            return x+(y-x)*(t-a)/(b-a)
    assert t >= path[-1][0]
    return path[-1][1]


def first_hit(path,t,x,d):
    pieces = list(zip(path,path[1:]))
    pieces.append((path[-1],(max(t,path[-1][0])+Q(10),path[-1][1])))
    for (a,u),(b,v) in pieces:
        if b < t:
            continue
        start = max(a,t)
        speed = (v-u)/(b-a)
        gap = u+speed*(start-a)-x-d*(start-t)
        if gap == 0:
            return start
        relative = d-speed
        if relative:
            candidate = start+gap/relative
            if start <= candidate <= b:
                return candidate
    raise AssertionError('Missing rational meeting')


def capture(route,path):
    times = sorted(set(t for t,x in route+path))
    previous = None
    for t in times:
        difference = position(route,t)-position(path,t)
        if difference == 0:
            return t
        if previous:
            a,old = previous
            if old*difference < 0:
                return a+(t-a)*old/(old-difference)
        previous=t,difference
    raise AssertionError('No rational capture')


def exhaustive_rational(paths,weights):
    best = None
    count = 0
    for order in permutations(range(len(paths))):
        t=Q(0)
        x=paths[order[0]][0][1]
        route=[(t,x)]
        for j in order[1:]:
            y=position(paths[j],t)
            if y == x:
                continue
            d=1 if y>x else -1
            nt=first_hit(paths[j],t,x,d)
            x+=d*(nt-t)
            t=nt
            route.append((t,x))
        cost=sum(w*capture(route,p)for w,p in zip(weights,paths))
        best=cost if best is None else min(best,cost)
        count+=1
    return best,count


def fixture_paths():
    E=g.E
    yield 'distinct_same_limit',[
        g.Path([(0,-E)],Q(1,4)),g.Path([(0,0)],Q(1,2)),
        g.Path([(0,E)],Q(1,4))]
    yield 'asymmetric_stationary',[
        g.Path([(0,-Q(3,4)+E)],Q(1,8)),
        g.Path([(0,-Q(1,4)-E**2)],Q(1,4)),
        g.Path([(0,Q(1,3)+E)],Q(3,8)),
        g.Path([(0,Q(3,4)-E)],Q(1,4))]
    edge=1-E**6
    speed=1-2*E**6
    positive=[]
    for a,wait,weight in [(Q(1,4),Q(1,4),Q(1,5)),(Q(3,4),Q(0),Q(3,10))]:
        start=a+E
        positive.append(g.Path([(0,start),(wait,start),(wait+(edge-start)/speed,edge)],weight))
    yield 'rational_speed_outgoing',[p.reflected()for p in positive[::-1]]+positive
    positive=[
        g.Path([(0,Q(1,4)+E),(Q(1,4),E),(Q(3,4),Q(1,2)+E),(1, Q(1,2)+E)],Q(1,4)),
        g.Path([(0,Q(3,4)+E),(Q(1,4),Q(1,2)+E),(Q(3,4),1-E),(1,1-E)],Q(1,4))]
    yield 'inward_outward',[p.reflected()for p in positive[::-1]]+positive
    yield 'moving_coalescence',[
        g.Path([(0,-Q(1,2)),(Q(1,2),0)],Q(1,3)),
        g.Path([(0,0)],Q(1,3)),
        g.Path([(0,Q(1,2)),(Q(1,2),0)],Q(1,3))]
    yield 'initial_tie_then_split',[
        g.Path([(0,-Q(1,2))],Q(1,4)),
        g.Path([(0,0),(Q(1,4),-Q(1,4))],Q(1,4)),
        g.Path([(0,0),(Q(1,4),Q(1,4))],Q(1,4)),
        g.Path([(0,Q(1,2))],Q(1,4))]


def main():
    # Equality alone must guard a positive isolated root inside the radius.
    before=g.RADIUS
    assert g.Germ(1)-1000*g.E != 0
    assert g.RADIUS <= Q(1,2000)
    reports=[]
    permutations_checked=0
    for name,paths in fixture_paths():
        value,route,stats=g.solve(paths,node_limit=100000)
        unpruned,_,other=g.solve(paths,node_limit=100000,use_pruning=False)
        assert value==unpruned
        assert sum((p.weight*g.direct_capture(route,p)for p in paths),g.Germ(0))==value
        epsilon=g.RADIUS/2
        specialized=[[(t.evaluate(epsilon),x.evaluate(epsilon))for t,x in p.vertices]for p in paths]
        answer,count=exhaustive_rational(specialized,[p.weight for p in paths])
        assert answer==value.evaluate(epsilon),(name,answer,value.evaluate(epsilon))
        independent=exact_oracles.monster_best_response(specialized,[p.weight for p in paths])
        assert independent['value']==answer
        permutations_checked+=count
        reports.append(dict(name=name,limit=str(value.limit()),nodes=stats['nodes'],
                            unpruned_nodes=other['nodes'],permutations=count,
                            independent_oracle_states=independent['states'],epsilon=str(epsilon)))
    # Independently intersect every one of the reconstructed eighteen paths
    # with the simple straight-left attacker at one valid rational epsilon.
    root=Path(__file__).resolve().parent
    data=json.loads((root/'global_minimax_grid4_exact.json').read_text())
    certificate=json.loads((root/'global_minimax_grid4_exact.germ.json').read_text())
    paths,_,_=g.load_discovery(data)
    epsilon=min(g.RADIUS,Q(certificate['valid_epsilon_radius']))/2
    initial=Q(3,4)+epsilon**2-epsilon**6/2-2*epsilon**8
    monster=[(Q(0),initial),(1+initial,Q(-1))]
    physical=[[(t.evaluate(epsilon),x.evaluate(epsilon))for t,x in p.vertices]for p in paths]
    captures=[exact_oracles.first_meeting(monster,p)for p in physical]
    assert all(t is not None for t in captures)
    actual=sum(p.weight*t for p,t in zip(paths,captures))
    expected=(108090289-38175128*epsilon+38175128*epsilon**2-139830322*epsilon**6+
              76350256*epsilon**7-76350256*epsilon**8)/(152700512*(1-epsilon**6))
    assert actual==expected
    output=dict(scope='Exact oracle regressions; these fixtures are not game bounds.',
                fixtures=reports,total_rational_permutations=permutations_checked,
                equality_radius_guard=True,
                exact_grid4_independent_capture_check=dict(paths=len(paths),epsilon=str(epsilon),
                                                         payoff=str(actual)))
    target=Path(__file__).with_name('germ_verification.json')
    target.write_text(json.dumps(output,indent=2)+'\n')
    print('PASS',len(reports),'germ fixtures;',permutations_checked,
          'independent rational permutations; existing exact oracle; equality root guard;',
          len(paths),'independent grid4 captures')


if __name__=='__main__':
    main()
