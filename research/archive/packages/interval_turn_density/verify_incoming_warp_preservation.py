#!/usr/bin/env python3
"""Exact first-capture audit of causal high-start warp preservation."""
from collections import Counter
from fractions import Fraction as Q
from itertools import product

from verify_positive_cdf_sheet import Law,Path,wave,first_capture


def envelope(left,right,minimum):
    cuts=sorted(set(left.times)|set(right.times))
    extra=[]
    for a,b in zip(cuts,cuts[1:]):
        fa=left.value(a)-right.value(a);fb=left.value(b)-right.value(b)
        if fa*fb<0:
            extra.append(a+(b-a)*fa/(fa-fb))
    function=min if minimum else max
    return Path([(t,function(left.value(t),right.value(t)))for t in sorted(cuts+extra)])


def ordinary(a,u,c):
    return wave(a,u,c,u,c)


def pairs():
    old=[ordinary(Q(1,5),Q(3,5),Q(3,5)),
         ordinary(Q(1,2),Q(9,10),Q(2,5)),
         ordinary(Q(7,10),Q(49,50),Q(1,5))]
    new=[ordinary(Q(1,5),Q(1,2),Q(3,5)),
         ordinary(Q(1,2),Q(4,5),Q(2,5)),
         ordinary(Q(7,10),Q(9,10),Q(1,5))]
    endpoint=Path([(0,1),(6,1)])
    weights=[Q(1,4)]*4
    yield Law(list(zip(weights,old+[endpoint]))),Law(list(zip(weights,new+[endpoint]))),False

    # Lower ranks can change when independently moved rank bands cross.
    # Sort the two physical paths at each time instead of pretending their
    # original labels remain ordered.
    first=ordinary(Q(1,5),Q(9,10),Q(3,5))
    second=ordinary(Q(1,2),Q(1),Q(2,5))
    moved=ordinary(Q(1,2),Q(3,5),Q(2,5))
    low,high=envelope(first,moved,True),envelope(first,moved,False)
    weights=[Q(2,5),Q(2,5),Q(1,5)]
    yield Law(list(zip(weights,[first,second,endpoint]))),Law(list(zip(weights,[low,high,endpoint]))),True


def route(start,controls,endpoint_first):
    result=[(Q(0),start)]
    t,x=Q(0),start
    for direction in controls:
        remaining=Q(1,4)
        while remaining:
            if not direction:
                t+=remaining;remaining=Q(0);result.append((t,x));continue
            if x==direction:direction=-direction
            length=min(remaining,1-direction*x)
            t+=length;x+=direction*length;remaining-=length
            result.append((t,x))
            if remaining:direction=-direction
    for endpoint in [Q(endpoint_first),Q(-endpoint_first)]:
        t+=abs(endpoint-x);x=endpoint
        if result[-1]!=(t,x):result.append((t,x))
    return result


def main():
    counts=Counter()
    for old,new,reordered in pairs():
        cuts=sorted({t for law in [old,new]for _,p in law.paths for t in p.times})
        for (wo,po),(wn,pn) in zip(old.paths,new.paths):
            assert wo==wn and po.value(Q(0))==pn.value(Q(0))
            assert all(pn.value(t)<=po.value(t)for t in cuts)
        for a in [Q(3,4),Q(4,5),Q(19,20),Q(1)]:
            for controls in product([-1,0,1],repeat=4):
                for endpoint_first in [-1,1]:
                    monster=route(a,controls,endpoint_first)
                    oldcost=newcost=Q(0)
                    for (weight,po),(_,pn) in zip(old.paths,new.paths):
                        oldpos=first_capture(po,monster,1);newpos=first_capture(pn,monster,1)
                        oldneg=first_capture(po,monster,-1);newneg=first_capture(pn,monster,-1)
                        assert newpos>=oldpos
                        assert newneg==oldneg
                        oldcost+=weight*(oldpos+oldneg)/2
                        newcost+=weight*(newpos+newneg)/2
                    assert newcost>=oldcost
                    counts['arbitrary control/endpoint-tour expected costs']+=1
                    if 0 in controls:counts['monster waits retained']+=1
                    if reordered:counts['actual quantile-reordering witnesses']+=1
                    if newcost>oldcost:counts['strict high-start cost increases']+=1
    print('PASS:',sum(counts.values()),'exact incoming-warp preservation checks')
    for name,value in counts.items():print(' ',name+':',value)
    print('Every reflected first capture is unchanged; positive first captures never advance')


if __name__=='__main__':main()
