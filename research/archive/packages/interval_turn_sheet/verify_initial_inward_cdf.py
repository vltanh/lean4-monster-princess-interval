#!/usr/bin/env python3
"""Exact CDF identity for an initial-inward monster and its free boundary.

The reference integrates capture records along the complete monster route.
The proposed identity instead uses characteristic line integrals and the
first U=1 moment.  No turn indifference or upper-density fit is assumed.
"""
from fractions import Fraction as Q
import importlib.util
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'packages/interval_continuous_rank'))
from continuous_rank import RankLaw, MultiLegRankLaw
from verify_general_response import integrate_line


def route(a,v):
    return [(0,a),((a+v)/2,(a-v)/2),((1+v)/2,(1-v)/2),(2,-1),(4,1)]


def formula(law,a,v):
    assert law.endpoint_mass == 0 and -a <= v <= a
    A = law.A(a)
    # The families used here have no interior atoms.  At the center the
    # strict radial CDF is zero even when the closed CDF has a waiting atom.
    r = Q(0) if a == v else law.radial((a+v)/2,(a-v)/2)
    B = Q(1) if v == -1 else law.radial((1+v)/2,(1-v)/2)
    initial = 2*integrate_line(law,Q(0),(a+v)/2,Q(-1),a)
    middle = 2*integrate_line(law,(a+v)/2,(1+v)/2,Q(1),-v,A)
    # J(r)=integral_0^r [2 alpha_q(1)-1]dq.  Layer cake supplies an
    # independent CDF integral, valid even when U=1 is reached on an early
    # incoming wave and the final outgoing characteristic is different.
    J = 2*(integrate_line(law,Q(0),Q(1),Q(-1),Q(1))
           -integrate_line(law,Q(0),Q(1),Q(-1),Q(1),r))-r
    center = 2*(2-a)*law.radial(a,Q(0)) if v == a else Q(0)
    return (12-8*A+initial+(1-a-v)*r+J
            -(7-v)*max(Q(0),B-A)-middle-center)/4


def verify_initial_atom_traces():
    spec = importlib.util.spec_from_file_location('inward_cdf_capture_reference',
        ROOT/'packages/interval_characteristic_response/verify.py')
    reference = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(reference)
    a = Q(1,2)
    princesses = [
        [(0,a),(Q(1,2),1),(4,1)],
        [(0,a),(Q(1,2),0),(Q(3,2),1),(4,1)],
    ]
    count = 0
    for j,p in enumerate(princesses):
        for v in (Q(-1,2),Q(-1,4),Q(0),Q(1,4),Q(1,2)):
            m = reference.clean(route(a,v))
            direct = (reference.direct_capture(m,p)
                      +reference.direct_capture([(t,-x) for t,x in m],p))/2
            expected = Q(1,4) if j == 1 and v == a else Q(1)
            assert direct == expected
            # A=1, r_strict=0 and the strict U=a row is zero; all
            # positive-part terms vanish, giving four-score 12-8=4.
            strict_prediction = Q(12-8,4)-(2-a)/2 if j == 1 and v == a else Q(12-8,4)
            assert strict_prediction == direct
            if j == 1:
                # On the coincident incoming U=a segment the closed row
                # is identically one.  Its substitution would be wrong.
                wrong_closed = (12-8+(a+v)+(1-a-v)+Q(1,2))/4
                if v == a:
                    wrong_closed -= (2-a)/2
                assert wrong_closed-direct == Q(3,8)
            count += 1
    return count


def verify_ordinary_obstruction(laws):
    from verify_terminal_integrals import rank_integral
    derivatives = finite = 0
    h = Q(1,100000)
    for law in laws:
        for a in (Q(k,17) for k in range(1,17)):
            rank = law.A(a)
            initial,u,c = law.parameters(rank)
            if initial != a or not a < u < 1 or not c > -a:
                continue
            four = lambda z,v:4*law.payoff(route(z,v)).value
            # These fixtures are piecewise quadratic in the parameters.
            # Agreement at h and h/2 checks that no regime boundary was
            # silently crossed by the finite-difference stencil.
            def direction(step):
                dv = (-3*four(a,-a)+4*four(a,-a+step)-four(a,-a+2*step))/(2*step)
                dg = (four(a+step,-a-step)-four(a-step,-a+step))/(2*step)
                return dv,dg
            dv,dg = direction(h)
            assert direction(h/2) == (dv,dg)
            density = law.A.affine_at(a)[0]
            assert dv+dg+(u-a)*density == 0
            derivatives += 1
            # A finite attack is stronger than stationarity: increasing
            # the start while keeping V=-a fixed only changes captures in
            # the newly enclosed initial rank interval.
            delta = min(Q(1,1000),(u-a)/4,(1-a)/4)
            q1 = law.A(a+delta)
            while law.parameters(q1)[2] <= -a:
                delta /= 2
                q1 = law.A(a+delta)
            integrand = tuple(2*a+delta-b-incoming for b,incoming in zip(law.a,law.u))
            predicted = rank_integral(law,integrand,rank,q1)
            actual = four(a+delta,-a)-four(a,-a)
            assert actual == predicted < 0,(a,delta,actual,predicted)
            finite += 1
    return derivatives,finite


def main():
    laws = [
        RankLaw([0,1],[Q(1,10),1],[Q(1,4),1],[Q(7,10),-1]),
        RankLaw([0,Q(2,5),1],[Q(1,20),Q(2,5),1],
                [Q(1,5),Q(3,5),1],[Q(9,10),Q(1,4),-1]),
        RankLaw([0,Q(1,3),Q(3,4),1],
                [Q(1,20),Q(1,3),Q(4,5),1],
                [Q(1,4),Q(3,5),Q(19,20),1],
                [Q(3,4),Q(1,2),Q(-1,2),-1]),
        MultiLegRankLaw([0,Q(2,5),1],[Q(1,8),Q(1,2),Q(7,8)],
                [[Q(1,4),Q(5,8),Q(15,16)],[Q(17,16),Q(9,8),Q(5,4)]],
                [[Q(1,5),Q(1,10),Q(-1,2)],[Q(19,20),Q(3,4),Q(1,4)]]),
        MultiLegRankLaw([0,1],[Q(1,10),Q(4,5)],
                [[Q(1,5),Q(9,10)],[Q(19,20),Q(11,10)],[Q(6,5),Q(7,5)]],
                [[Q(1,10),Q(-1,2)],[Q(3,5),Q(1,5)],[Q(19,20),Q(3,5)]]),
    ]
    count = 0
    for law in laws:
        for a in sorted({Q(k,11) for k in range(12)} | set(law.a)):
            for fraction in (Q(-1),Q(-7,8),Q(-3,4),Q(-1,2),Q(-1,4),
                             Q(0),Q(1,3),Q(2,3),Q(1)):
                v = a*fraction
                actual = law.payoff(route(a,v)).value
                predicted = formula(law,a,v)
                assert actual == predicted,(a,v,actual,predicted)
                count += 1
    traces = verify_initial_atom_traces()
    derivatives,finite = verify_ordinary_obstruction(laws[:3])
    print('PASS:',count,'exact initial-inward CDF identities against capture records')
    print('PASS:',traces,'initial and incoming-atom first-contact fixtures')
    print('PASS:',derivatives,'exact directional identities and',finite,'strict finite inward attacks')
    print('Includes center turns and one, two, and three princess waves; no equilibrium assumption')


if __name__ == '__main__':
    main()
