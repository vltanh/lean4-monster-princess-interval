#!/usr/bin/env python3
"""Exact fixtures for the global upper-law center-wait replacement."""
from fractions import Fraction as Q
import json
from pathlib import Path
import sys

from continuous_response_waits import unitize_center_waits

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'packages/interval_exact_reduction'))
from exact_oracles import first_meeting,position,admissible


def reflect(route):return[(t,-x)for t,x in route]


def main():
    fixtures=[
        ('initial',[(0,0),(Q(1,2),0),(Q(3,2),1),(Q(7,2),-1)]),
        ('intermediate',[(0,Q(1,2)),(Q(1,2),0),(Q(5,4),0),(Q(9,4),1),(Q(17,4),-1)]),
        ('two_waits',[(0,-Q(1,2)),(Q(1,2),0),(1,0),(Q(3,2),Q(1,2)),(2,0),(Q(9,4),0),(Q(13,4),-1),(Q(21,4),1)]),
        ('long_wait',[(0,0),(Q(9,2),0),(Q(11,2),1),(Q(15,2),-1)])]
    princesses=[[(0,Q(1,4))],[(0,Q(1,2))],[(0,1)],
                [(0,Q(1,8)),(Q(1,2),Q(5,8))],
                [(0,Q(7,8)),(Q(3,4),Q(1,8)),(Q(3,2),Q(7,8))],
                [(0,Q(1,2)),(1,Q(1,2)),(Q(11,8),Q(1,8)),(Q(15,8),Q(5,8))],
                [(Q(k,2),Q(1,4)if k%2==0 else Q(3,4))for k in range(17)]]
    princesses=[[(Q(t),Q(x))for t,x in p]for p in princesses]
    assert all(admissible(p)and all(x>0 for t,x in p)for p in princesses)
    checked=0;timestamps=0;unchanged_checks=0;reports=[]
    for name,raw in fixtures:
        old=[(Q(t),Q(x))for t,x in raw];new=unitize_center_waits(old)
        assert admissible(old)and admissible(new)
        assert unitize_center_waits(reflect(old),direction=-1)==reflect(new)
        for t,x in old:assert position(new,t)==x;timestamps+=1
        for(a,x),(b,y)in zip(old,old[1:]):
            if x!=y:
                for t in (a,(a+b)/2,b):assert position(new,t)==position(old,t);unchanged_checks+=1
        for p in princesses:
            for sign in (-1,1):
                first=first_meeting([(t,sign*x)for t,x in old],p)
                replaced=first_meeting([(t,sign*x)for t,x in new],p)
                assert first is not None and replaced is not None and replaced<=first
                checked+=1
        reports.append(dict(name=name,original_vertices=len(old),unit_vertices=len(new),
                            final_time=str(old[-1][0]),timestamps_preserved=True,both_orientations='pass'))
    old=[(Q(t),Q(x))for t,x in fixtures[0][1]];new=unitize_center_waits(old)
    atom=[(Q(0),Q(1,4)),(Q(1,4),Q(0))]
    old_pair=sum(first_meeting(p,atom)for p in (old,reflect(old)))/2
    new_pair=sum(first_meeting(p,atom)for p in (new,reflect(new)))/2
    assert old_pair==Q(1,4)and new_pair==Q(5,16)>old_pair
    result=dict(scope='Exact fixtures for the upper supremum replacement; the general theorem is in CENTER_WAIT_UNITIZATION.md.',
                fixtures=reports,strict_positive_capture_comparisons=checked,
                original_timestamp_checks=timestamps,unchanged_leg_checks=unchanged_checks,
                center_contact_counterexample=dict(old_pair=str(old_pair),unitized_pair=str(new_pair),
                                                   conclusion='No pointwise lower-law domination'))
    Path(__file__).with_name('center_wait_unitization_verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print('PASS',checked,'exact strict-positive capture comparisons;',timestamps,'timestamps;',
          unchanged_checks,'unchanged-leg checks; long waits and center-contact counterexample')


if __name__=='__main__':main()
