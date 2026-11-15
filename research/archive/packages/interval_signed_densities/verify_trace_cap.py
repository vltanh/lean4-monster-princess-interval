#!/usr/bin/env python3
"""Exact boundary fixtures for the arbitrary-path trace cap.

Integrates actual segment-intersection capture times over continuous
linear monster densities. It does not substitute scalar response shapes.
"""

from fractions import Fraction as Q
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location(
    "capture_reference", ROOT/"packages/interval_characteristic_response/verify.py")
ref = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ref)


def cap(path, delta):
    graph = [(t+x,t-x) for t,x in path]
    result = []
    stop, level = 3-delta, 1-delta
    for (u,v),(uu,vv) in zip(graph,graph[1:]):
        cuts = {Q(0),Q(1)}
        if uu != u and u < stop < uu:
            cuts.add((stop-u)/(uu-u))
        if vv != v and v < level < vv:
            cuts.add((level-v)/(vv-v))
        for r in sorted(cuts):
            U,V = u+r*(uu-u),v+r*(vv-v)
            if U > stop:
                continue
            V = min(V,level)
            point = ((U+V)/2,(U-V)/2)
            if not result or point != result[-1]:
                result.append(point)
    assert result[-1] == (2-delta,1)
    result.append((Q(4),Q(1)))
    result = ref.clean(result)
    assert all(0 <= x <= 1 for t,x in result)
    assert all(abs(y-x) <= s-t for (t,x),(s,y) in zip(result,result[1:]))
    return result


def density_integral(d, lo, hi):
    return d[0]*(hi-lo)+d[1]*(hi*hi-lo*lo)/2


def payoff(path, w0, densities, negative_b=Q(1)):
    a = path[0][1]
    c = 2*ref.inverse(path,1,1,strict=True)-1
    xcuts = {Q(-1),Q(0),Q(1),a,-a,-c}
    xcuts.add(negative_b-2*ref.inverse(path,negative_b,1,strict=True))
    for t,p in path:
        for z in (t+p,t-p):
            xcuts.update((-z,2-z))
    result = Q(0)
    for family,sign,density in zip((1,2,2,1),(1,1,-1,-1),densities):
        cuts = sorted({Q(0),Q(1)} | {sign*x for x in xcuts if 0 < sign*x < 1})

        def cost(z):
            if family == 2 and sign == -1:
                x,b = -z,negative_b
                route = ref.clean([(0,x),((b-x)/2,(b+x)/2),
                                   (b+1,-1),(b+3,1)])
            else:
                route = ref.monster_path(family,sign*z)
            opposite = [(t,-x) for t,x in route]
            return (ref.direct_capture(route,path)+ref.direct_capture(opposite,path))/2

        for lo,hi in zip(cuts,cuts[1:]):
            x,y = (2*lo+hi)/3,(lo+2*hi)/3
            fx,fy = cost(x),cost(y)
            slope = (fy-fx)/(y-x)
            intercept = fx-slope*x
            assert cost((lo+hi)/2) == slope*(lo+hi)/2+intercept
            d0,d1 = density
            result += (intercept*d0*(hi-lo)
                       +(intercept*d1+slope*d0)*(hi**2-lo**2)/2
                       +slope*d1*(hi**3-lo**3)/3)
    sweep = ref.monster_path(1,Q(-1))
    result += w0*(ref.direct_capture(sweep,path)
                  +ref.direct_capture([(t,-x) for t,x in sweep],path))/2
    return result


def main():
    fixtures = [
        [(0,0),(4,0)], [(0,1),(4,1)],
        [(0,1),(1,0),(4,0)],
        [(0,0),(1,1),(2,0),(3,1),(4,0)],
        [(0,Q(1,2)),(Q(1,2),Q(1,2)),(1,0),(4,0)],
        [(0,Q(1,4)),(Q(1,4),Q(1,4)),(1,1),(4,1)],
        [(0,Q(3,4)),(Q(1,2),Q(1,4)),(Q(3,4),Q(1,2)),
         (Q(5,4),0),(Q(3,2),Q(1,4)),(4,Q(1,4))],
    ]
    laws = [
        (Q(1,7),((1,0),(2,0),(3,0),(4,0))),
        (Q(1,3),((0,2),(2,-1),(1,2),(2,-1))),
    ]
    checks = shifts = 0
    for raw in fixtures:
        path = ref.clean(raw)
        a = path[0][1]
        c = 2*ref.inverse(path,1,1,strict=True)-1
        B1,B3 = ref.inverse(path,1,-1),ref.inverse(path,3,-1)
        for w0,densities in laws:
            densities = [tuple(map(Q,d)) for d in densities]
            f,g,h,ell = densities
            mass = w0+sum(density_integral(d,Q(0),Q(1)) for d in densities)
            B0 = w0+density_integral(g,Q(0),Q(1))+density_integral(h,Q(0),a)
            T0 = density_integral(h,max(Q(0),c),Q(1))
            if c < 0:
                T0 += density_integral(g,Q(0),-c)
            gain = (B0*(2-B1)+T0*(4-B3))/2
            old = payoff(path,w0,densities)
            for delta in (Q(1,8),Q(1,3)):
                changed = cap(path,delta)
                assert ref.inverse(changed,1,-1) == 2
                assert ref.inverse(changed,3,-1) == 4
                actual = payoff(changed,w0,densities)-old
                assert actual >= gain-delta*mass/4, (path,delta,actual,gain)
                checks += 1
            for eta in (Q(1,8),Q(1,3)):
                ce = 2*ref.inverse(path,1+eta,1,strict=True)-(1+eta)
                htail = density_integral(h,min(Q(1),max(Q(0),ce)),Q(1))
                hearly = density_integral(h,Q(0),a)
                predicted = (htail*(ref.inverse(path,3+eta,-1)-B3)
                             +hearly*(ref.inverse(path,1+eta,-1)-B1))
                lo,hi = max(Q(0),c),min(Q(1),ce)
                if hi > lo:
                    cuts = sorted({lo,hi} | {t-p for t,p in path if lo < t-p < hi})
                    for low,high in zip(cuts,cuts[1:]):
                        x,y = (2*low+high)/3,(low+2*high)/3
                        fx,fy = B3-ref.inverse(path,x,-1),B3-ref.inverse(path,y,-1)
                        slope = (fy-fx)/(y-x)
                        intercept = fx-slope*x
                        d0,d1 = h
                        predicted -= (intercept*d0*(high-low)
                                      +(intercept*d1+slope*d0)*(high**2-low**2)/2
                                      +slope*d1*(high**3-low**3)/3)
                actual = 2*(payoff(path,w0,densities,1+eta)-old)
                assert actual == predicted, (path,eta,actual,predicted)
                shifts += 1
    print(f"PASS: {checks} exact continuous-density trace-cap inequalities")
    print("Coverage: center/endpoints, initial coincidence, U/V plateaus, repeated turns")
    print(f"PASS: {shifts} exact arbitrary-path negative-M2 shift identities")
    print("Scope: boundary fixtures for the hand proof; no equilibrium certificate")


if __name__ == "__main__":
    main()
