#!/usr/bin/env python3
"""Check exploratory integration and legal rational route construction.

The floating optimizer never certifies a lower. Its inputs and scores are
nevertheless compared against the independent Fraction chronological
integrators, including endpoint and collapsed-turn parameter boundaries.
"""
from fractions import Fraction as Q
import json
from pathlib import Path
import random

from extract_quantiles import Field, ROOT, read
from score_continuous_attack import supporting_plane
from search_continuous_attacks import (
    FastField, FAMILIES, positions, route_from_positions, snap_route,
)


def main():
    rng=random.Random(20261114)
    checks=0;maximum_error=0.0
    for name in ('grid_n1_princess.json','grid_n3_princess.json'):
        data,_=read(ROOT/'packages/interval_clock_grid'/name)
        field=Field(data);fast=FastField(field)
        for family in FAMILIES:
            dim=3 if family in ('two_turn','precenter_loop') else 2
            parameters=[[Q(0)]*dim,[Q(1)]*dim]
            parameters += [[Q(rng.randrange(101),100) for _ in range(dim)]
                           for _ in range(3)]
            for params in parameters:
                route=route_from_positions(positions(family,params))
                assert route==snap_route(family,list(map(float,params)),1000000)
                assert route[0][0]==0 and abs(route[0][1])<=1
                assert {x for t,x in route} >= {-1,1}
                assert all(abs(x-y)==s-t>0 and abs(y)<=1
                           for (t,x),(s,y) in zip(route,route[1:]))
                actual=Q(supporting_plane(field,route)['value'])
                floating=fast.cost([(float(t),float(x)) for t,x in route])
                error=abs(floating-float(actual))
                maximum_error=max(maximum_error,error)
                assert error<2e-11,(name,family,params,actual,floating)
                checks+=1
    print(json.dumps({'status':'PASS','exact_route_comparisons':checks,
                      'maximum_absolute_floating_error':maximum_error,
                      'scope':'Exploratory scorer and physical route regression, not a game bound.'},indent=2))


if __name__=='__main__':main()
