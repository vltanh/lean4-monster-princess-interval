"""Exact free-second-turn anchor against independent physical captures."""
from collections import Counter
from fractions import Fraction as Q
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'packages/interval_turn_density'))
from verify_positive_cdf_sheet import Law,Path as Princess,finite_fixtures
from verify_two_interior_cdf import direct_route,initial_inward_route


def anchor(law,a,v,s):
    x,y,z=1-a,1+v,1-s
    A=sum((mass for mass,path in law.paths if path.value(Q(0))<=a),Q(0))
    As=sum((mass for mass,path in law.paths if path.value(Q(0))<=s),Q(0))
    rx,rz=1-A,1-As
    d=1-law.radial(a,v,strict=True)
    W=z*d+law.integrate(s,-s,s,horizontal=True,strict=True,
                       transform=lambda rank:max(Q(0),rank-(1-d)))
    row=(y-x)-law.integrate(a,-a,v,horizontal=True,strict=True)
    middle_deficit=1-law.radial(s,v)
    column=law.integrate(v,a,s,horizontal=False,
                         transform=lambda rank:max(Q(0),rank-A))
    return ((8-2*z)*(rx-rz)-(W+(x-y-z)*d)-row
            -(8-z-y)*max(Q(0),rx-middle_deficit)-column)


def main():
    counts=Counter()
    for original in finite_fixtures():
        law=Law([(w,Princess(list(p.knots)+[(Q(8),Q(1))])) for w,p in original.paths])
        starts={Q(1,10),Q(1,4),Q(1,2),Q(3,4),Q(9,10)}
        starts.update(p.value(Q(0)) for _,p in law.paths if 0<p.value(Q(0))<1)
        for a in sorted(starts):
            for v in [-a,-a/2,Q(0),a/2]:
                for s in sorted({a,(3*a+1)/4,(a+1)/2,(a+3)/4,Q(1)}):
                    inward=direct_route(law,initial_inward_route(a,v,s))
                    left=direct_route(law,[(Q(0),s),(s+1,Q(-1)),(s+3,Q(1))])
                    actual=4*(inward-left)
                    predicted=anchor(law,a,v,s)
                    assert actual==predicted,(a,v,s,actual,predicted)
                    counts['free-second anchor versus direct captures']+=1
                    if a==s:
                        assert predicted==0
                        counts['direct-M1 endpoint of the turn interval']+=1
                    if v==-a:
                        counts['zero initial inward leg']+=1
                    if any(p.value(Q(0))==a for _,p in law.paths):
                        counts['initial atom starts']+=1
                    if law.radial(a,v)!=law.radial(a,v,strict=True):
                        counts['strict initial-turn trace witnesses']+=1
    print('PASS:',sum(counts.values()),'exact free-second inward-field checks')
    for name,count in counts.items():
        print(f'  {name}: {count}')
    print('Scope: exact source-free field identity; no support or equilibrium claim')


if __name__=='__main__':
    main()
