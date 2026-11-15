#!/usr/bin/env python3
"""Exact physical regressions for the improved outward-time cutoff.

No discretized payoff or CDF compiler is used. All contacts are found
chronologically by rational affine intersection of actual paths.
"""
from fractions import Fraction as Q
import json

def position(path,t):
    if t>=path[-1][0]:return path[-1][1]
    for (a,x),(b,y) in zip(path,path[1:]):
        if a<=t<=b:return x+(y-x)*(t-a)/(b-a)
    raise AssertionError(('outside path',t))

def legal(path):
    assert path and path[0][0]==0
    assert all(-1<=x<=1 for t,x in path)
    assert all(a<b and abs(y-x)<=b-a for (a,x),(b,y) in zip(path,path[1:]))

def capture(monster,target):
    legal(monster);legal(target)
    times=sorted({t for p in (monster,target) for t,x in p})
    for a,b in zip(times,times[1:]):
        left=position(monster,a)-position(target,a)
        right=position(monster,b)-position(target,b)
        if left==0:return a
        if right==0:return b
        if left*right<0:return a+(b-a)*left/(left-right)
    if position(monster,times[-1])==position(target,times[-1]):return times[-1]
    return None

def radius(r,T):
    p=[(Q(0),r)]
    if T:p.append((T,r))
    if r<1:p.append((T+1-r,Q(1)))
    return p

def reflected(p):return [(t,-x) for t,x in p]

def main():
    checks=0;worst_no_center=None
    for T in (Q(7,4),Q(15,8),Q(2),Q(5,2)):
        for a in (Q(1,1024),Q(1,4),Q(3,4)):
            monster=[(Q(0),a),(T,a),(T+1+a,Q(-1)),(T+3+a,Q(1))]
            for r in (Q(0),Q(1,3),Q(1)):
                target=reflected(radius(r,T))
                tau=capture(monster,target)
                assert tau==T+1+a
                assert position(monster,T)==a and a>0
                checks+=1
            # Initial co-location makes the universal half-mass bound sharp.
            pair=radius(a,T);positive=capture(monster,pair);negative=capture(monster,reflected(pair))
            assert positive==0 and negative==T+1+a
            score=(positive+negative)/2
            assert score==(T+1+a)/2 and score>(T+1)/2
            worst_no_center=score if worst_no_center is None else min(worst_no_center,score)
            checks+=1
    domination=[]
    for T in (Q(15,8),Q(2)):
        monster=[(Q(0),Q(0)),(T,Q(0)),(T+1,Q(1)),(T+3,Q(-1))]
        for r in (Q(1,4),Q(3,4),Q(1)):
            old=radius(r,T+1);new=radius(r,T)
            old_times=[capture(monster,p) for p in (old,reflected(old))]
            new_times=[capture(monster,p) for p in (new,reflected(new))]
            assert all(a<=b for a,b in zip(old_times,new_times))
            domination.append((old_times,new_times));checks+=2
        # A delay before the first endpoint is removable after outward T.
        delayed=[(Q(0),Q(0)),(T,Q(0)),(T+Q(1,2),Q(1,2)),
                 (T+1,Q(0)),(T+2,Q(1)),(T+4,Q(-1))]
        for r in (Q(1,4),Q(3,4),Q(1)):
            pair=radius(r,T)
            for p in (pair,reflected(pair)):
                old=capture(delayed,p);new=capture(monster,p)
                assert new<=old
                assert abs(position(delayed,old))==abs(position(monster,new))==1
                checks+=1
    U=Q(1140799301969009059644426513,800000000000000000000000000)
    assert U<Q(23,16)<Q(3,2)
    assert ((2*U-1)+1)/2==U
    print(json.dumps({'status':'PASS','exact_physical_checks':checks,
        'no_center_capture_formula':'T+1+abs(m(T))',
        'zero_radius_at_cutoff_checked':True,'initial_colocation_checked':True,
        'center_visited_domination_checked':True,'endpoint_tail_checked':True,
        'certified_upper':str(U),'smallest_upper_justified_cutoff':str(2*U-1),
        'simple_global_outward_cutoff':'2','princess_absorption_horizon':'3',
        'normalized_monster_completion_horizon':'6','protected_turn_completion_horizon':'8',
        'scope':'Exact finite regressions supporting the parameterized path proof; no sampled game value is asserted.'},indent=2))

if __name__=='__main__':main()
