"""Exact shape-free first-U1 moments against direct physical capture."""
from collections import Counter
from fractions import Fraction as Q
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'packages/interval_turn_density'))
from verify_positive_cdf_sheet import Law, Path as Princess, finite_fixtures, wave
from verify_two_interior_cdf import direct_route


def first(path,level,sign):
    if sign*path.value(Q(0)) >= level:
        return Q(0)
    for left,right,slope,intercept in path.segments:
        speed=1+sign*slope
        if speed and right+sign*path.value(right) >= level:
            answer=(level-sign*intercept)/speed
            if left<=answer<=right:
                return answer
    raise AssertionError(('first contact absent',level,sign,path.knots))


def extend(path):
    return Princess(list(path.knots)+([(Q(8),Q(1))]
                    if path.knots[-1][0]<8 else []))


def main():
    counts=Counter()
    laws=[Law([(w,extend(path)) for w,path in law.paths])
          for law in finite_fixtures()]
    extra=[
        Princess([(0,Q(4,5)),(Q(3,20),Q(19,20)),
                  (Q(11,20),Q(11,20)),(1,1),(8,1)]),
        Princess([(0,Q(4,5)),(Q(1,5),Q(9,10)),
                  (Q(3,5),Q(1,2)),(Q(11,10),1),(8,1)]),
        wave(Q(7,10),Q(9,10),Q(-3,10),Q(11,10),Q(1,10)),
        wave(Q(4,5),Q(19,20),Q(-2,5),Q(6,5),Q(1,5)),
        wave(Q(9,10),Q(39,40),Q(-3,5),Q(11,10),Q(1,4)),
        Princess([(0,0),(1,0),(2,1),(8,1)]),
        Princess([(0,1),(8,1)]),
    ]
    low=Princess([(0,0),(Q(3,4),0),(Q(7,4),1),(8,1)])
    for path in extra:
        path=extend(path)
        laws.append(Law([(Q(1),path)]))
        if all(low.value(t)<=path.value(t)
               for t in sorted(set(low.times)|set(path.times))):
            laws.append(Law([(Q(2,3),low),(Q(1,3),path)]))
    for law in laws:
        endpoint=direct_route(law,[(Q(0),Q(1)),(Q(2),Q(-1))])
        alpha1={path:first(path,Q(1),1) for _,path in law.paths}
        beta1={path:first(path,Q(1),-1) for _,path in law.paths}
        expected_end=2*sum(w*(alpha1[path]+beta1[path]) for w,path in law.paths)
        assert 4*endpoint==expected_end
        counts['endpoint first-inverse moment']+=1
        H1=2*sum(w*(2-beta1[path]) for w,path in law.paths)
        starts={Q(j,20) for j in range(1,20)}
        starts.update(path.value(Q(0)) for _,path in law.paths
                      if 0<path.value(Q(0))<1)
        for z in sorted(starts):
            x=1-z
            route=[(Q(0),z),(x,Q(1)),(2+x,Q(-1))]
            actual=4*(direct_route(law,route)-endpoint)
            source=Q(0);gap=Q(0);moment=Q(0);A=Q(0)
            outward_high=True
            for w,path in law.paths:
                alpha=first(path,1+x,1)
                beta=first(path,-1+x,-1)
                assert first(path,1+x,-1)==2+x
                assert alpha-alpha1[path]>=x/2
                source+=w*(2*alpha-2*alpha1[path]-x)
                b=path.value(Q(0))
                if b>=z:
                    gap+=w*(alpha-beta)
                    assert alpha>=beta
                    moment+=w*alpha1[path]
                    outward_high &= all(path.value(t)>=b
                        for t in list(path.times)+[alpha1[path]]
                        if t<=alpha1[path])
                else:
                    A+=w
            predicted=3*x+source+H1-2*gap
            assert actual==predicted,(z,actual,predicted)
            assert source>=0
            bound=x*(2+A)-2*moment+H1
            assert actual>=bound,(z,actual,bound)
            counts['Q_all identity versus direct captures']+=1
            counts['universal first-hit moment bound']+=1
            if any(path.value(Q(0))==z for _,path in law.paths):
                counts['initial atom traces']+=1
            if H1:
                counts['V1 first-contact correction']+=1
            if source:
                counts['strictly positive post-one source']+=1
            if outward_high:
                assert moment<=x*(1-A)
                assert actual>=3*x*A+H1
                counts['monotone initial post-one exclusion bound']+=1
    print('PASS:',sum(counts.values()),'exact post-one first-hit checks')
    for label,count in counts.items():print(' ',label+':',count)
    print('Scope: shape-free moment identities and necessary activity gate')


if __name__=='__main__':
    main()
