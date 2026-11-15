#!/usr/bin/env python3
"""Exact integrated terminal identities, checked against capture records.

No equilibrium is assumed.  Each formula predicts the *cost residual* of
an arbitrary ordinary ordered wave, so the checks do not manufacture
indifference by reusing its asserted differential equations.
"""
from fractions import Fraction as Q
import importlib.util
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'packages/interval_continuous_rank'))
from continuous_rank import RankLaw

spec = importlib.util.spec_from_file_location(
    'terminal_capture_reference',
    ROOT / 'packages/interval_characteristic_response/verify.py')
capture_reference = importlib.util.module_from_spec(spec)
spec.loader.exec_module(capture_reference)


def rank_integral(law, values, left=Q(0), right=Q(1)):
    cuts = sorted({left, right, *(q for q in law.q if left < q < right)})
    def at(q):
        for j in range(len(law.q)-1):
            if law.q[j] <= q <= law.q[j+1]:
                w = (q-law.q[j])/(law.q[j+1]-law.q[j])
                return values[j]+w*(values[j+1]-values[j])
        raise AssertionError(q)
    return sum((b-a)*(at(a)+at(b))/2 for a,b in zip(cuts,cuts[1:]))


def cdf_tail_integral(law, z):
    cuts = sorted({z, Q(1), *(a for a in law.a if z < a < 1)})
    return sum((b-a)*(2-law.A(a)-law.A(b))/2
               for a,b in zip(cuts,cuts[1:]))


def cost(law, kind, z):
    if kind == 'f':
        route = [(0,z),(1-z,1),(3-z,-1)]
    elif kind == 'g':
        route = [(0,z),((1-z)/2,(1+z)/2),(2,-1),(4,1)]
    else:
        route = [(0,-z),(1+z,1),(3+z,-1)]
    return law.payoff(route).value


def verify_endpoint_traces():
    count = 0
    for a in (Q(0),Q(1,4),Q(1,2),Q(3,4)):
        for u in (a,(a+1)/2,Q(1)):
            for c in (-a,Q(0),Q(1,2),Q(9,10),Q(1)):
                times = sorted(t for t in {Q(0),(u-a)/2,u,(u+c)/2,c,1+c,Q(8)}
                               if t >= 0)
                p = capture_reference.clean([
                    (t,min(Q(1),max(min(a+t,u-t),t-c,Q(0)))) for t in times])
                def paired(kind,z):
                    if kind == 'f':
                        m = capture_reference.clean([(0,z),(1-z,1),(3-z,-1)])
                    else:
                        m = capture_reference.clean([(0,-z),(1+z,1),(3+z,-1)])
                    return (capture_reference.direct_capture(m,p)
                            +capture_reference.direct_capture([(t,-x) for t,x in m],p))/2
                e = Q(1,1000)
                flimit = 2*paired('f',1-e/2)-paired('f',1-e)
                llimit = 2*paired('ell',1-e/2)-paired('ell',1-e)
                assert 4*flimit == 5+c
                assert 4*(flimit-llimit) == 2*int(c==1)+(a+c)*int(u==1)
                count += 1
    return count


def main():
    laws = [
        RankLaw([0,1],[Q(1,10),1],[Q(1,4),1],[Q(7,10),-1]),
        RankLaw([0,Q(2,5),1],[Q(1,20),Q(2,5),1],
                [Q(1,5),Q(3,5),1],[Q(9,10),Q(1,4),-1]),
        RankLaw([0,Q(1,3),Q(3,4),1],
                [Q(1,20),Q(1,3),Q(4,5),1],
                [Q(1,4),Q(3,5),Q(19,20),1],
                [Q(3,4),Q(1,2),Q(-1,2),-1]),
    ]
    count = 0
    for law in laws:
        reference = 5+rank_integral(law,law.c)
        assert 4*cost(law,'f',Q(1)) == reference
        for z in [Q(k,41) for k in range(1,41)]:
            a_rank = law.A(z)
            negative_rank = law.D(-z)
            eps = 1-z
            main_integral = rank_integral(law,
                tuple(2+c-u for c,u in zip(law.c,law.u)),a_rank)
            correction = rank_integral(law,
                tuple(eps+1-u for u in law.u),negative_rank)
            predicted_f = 3*eps-main_integral+correction
            assert 4*cost(law,'f',z)-reference == predicted_f
            predicted_difference = -eps*(2+law.A(z))+2*(3+z)*(1-law.D(-z))
            assert 4*(cost(law,'g',z)-cost(law,'f',z)) == predicted_difference
            count += 2

            u = law.parameters(a_rank)[1]
            if z <= law.a[0] or law.D(u) > law.B(u):
                continue
            eta = 1-u
            H = (8-2*eta)*(1-law.A(u))-3*eta+cdf_tail_integral(law,u)
            integral = rank_integral(law,
                tuple(a+c for a,c in zip(law.a,law.c)),a_rank)
            front = law.D(u)
            front_moment = rank_integral(law,
                tuple(c-u for c in law.c),Q(0),front)
            assert 4*cost(law,'ell',u)-reference == H-integral-2*front-front_moment
            count += 1
    print(f'PASS: {count} exact cost-residual identities against capture records')
    print('PASS: endpoint reference, moving negative front, and outgoing-front Volterra term')
    traces = verify_endpoint_traces()
    print(f'PASS: {traces} exact endpoint traces, including central and incoming atoms')
    print('Scope: identities for supplied ordinary waves; no equilibrium certificate')


if __name__ == '__main__':
    main()
