#!/usr/bin/env python3
"""Exact direct-capture check of the chained-turn replacement identity."""
from fractions import Fraction as Q
import importlib.util
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location(
    'capture_reference',ROOT/'packages/interval_characteristic_response/verify.py')
ref=importlib.util.module_from_spec(spec)
spec.loader.exec_module(ref)


def m2(z,s):
    return ref.clean([(0,-z),((s+z)/2,(s-z)/2),(s+1,-1),(s+3,1)])


def m3(z,s,t):
    return ref.clean([(0,-z),((s+z)/2,(s-z)/2),
                      ((s+t)/2,(s-t)/2),(t+1,1),(t+3,-1)])


def pair(monster,princess):
    return (ref.direct_capture(monster,princess)
            +ref.direct_capture([(t,-x) for t,x in monster],princess))/2


def main():
    raw=[
        [(0,0),(8,0)],[(0,1),(8,1)],[(0,Q(1,2)),(8,Q(1,2))],
        [(0,1),(1,0),(8,0)],[(0,0),(1,1),(2,0),(8,0)],
        [(0,Q(1,4)),(Q(1,4),0),(Q(3,4),Q(1,2)),(1,Q(1,4)),(8,Q(1,4))],
        [(0,Q(3,4)),(Q(1,2),Q(1,4)),(Q(3,4),Q(1,2)),
         (Q(5,4),0),(Q(3,2),Q(1,4)),(8,Q(1,4))],
        [(0,Q(1,3)),(Q(2,3),Q(1,3)),(Q(4,3),1),(8,1)],
        [(0,Q(2,3)),(Q(1,3),Q(1,3)),(1,1),(2,0),(3,1),(8,1)],
    ]
    count=strict=0
    for points in raw:
        p=ref.clean(points)
        for s in (Q(1,3),Q(2,3),Q(5,6),Q(1)):
            for z in (s/3,2*s/3,s):
                for t in (s,s+Q(1,4),s+Q(3,4),s+2):
                    before=pair(m2(z,s),p)+pair(m2(s,t),p)
                    after=pair(m3(z,s,t),p)+pair(m2(s,s+2),p)
                    assert after<=before,(p,z,s,t,after,before)
                    # Independently evaluate the exact correction identity.
                    B=lambda value:ref.inverse(p,value,-1)
                    a=p[0][1]
                    r=int(B(z)<=(s+z)/2)
                    q=int(B(s)<=(t+s)/2)
                    As=int(a<=s)
                    Az=int(a<=z)
                    correction=(As-r)*(B(t)-B(s+2))
                    correction-=max(0,Az-q)*(B(t+2)-B(s))
                    assert 2*(after-before)==correction,(p,z,s,t,after,before,correction)
                    count+=1
                    strict+=int(after<before)
    print(f'PASS: {count} exact chained-turn inequalities and correction identities')
    print(f'PASS: {strict} strict improvements; equality and initial-capture cases retained')
    print('Coverage includes paths that never reach an endpoint and multiple reversals')
    print('Scope: nonnegative princess plus reflection; unrestricted ceiling transfer needs the symmetry lemma')


if __name__=='__main__':
    main()
