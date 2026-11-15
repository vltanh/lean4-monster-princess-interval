#!/usr/bin/env python3
"""Exact dual derivatives with independent initial and incoming CDFs.

This checks formulas for an initial outward/inward/center-wait/outward
law. It does not set the incoming characteristic equal to the initial
position. Reference values come from complete direct capture-record
integration, not from the asserted derivative identities.
"""
from fractions import Fraction as Q
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'packages/interval_continuous_rank'))
from continuous_rank import RankLaw


def cost(law,kind,z):
    if kind=='f':
        route=[(0,z),(1-z,1),(3-z,-1)]
    elif kind=='g':
        route=[(0,z),((1-z)/2,(1+z)/2),(2,-1),(4,1)]
    else:
        route=[(0,-z),((1+z)/2,(1-z)/2),(2,-1),(4,1)]
    return law.payoff(route).value


def main():
    laws=[
        RankLaw([0,1],[Q(1,10),Q(3,4)],
                [Q(1,4),Q(19,20)],[Q(9,10),Q(1,10)]),
        RankLaw([0,Q(2,5),1],[Q(1,10),Q(2,5),Q(7,10)],
                [Q(1,4),Q(13,20),Q(19,20)],
                [Q(9,10),Q(3,5),Q(3,20)]),
        RankLaw([0,Q(1,3),Q(2,3),1],
                [Q(1,20),Q(1,4),Q(1,2),Q(4,5)],
                [Q(1,5),Q(9,20),Q(3,4),Q(49,50)],
                [Q(19,20),Q(4,5),Q(2,5),Q(1,20)]),
        RankLaw([0,1],[Q(1,5),Q(9,10)],
                [Q(2,5),Q(49,50)],[Q(4,5),Q(-3,5)]),
        RankLaw([0,Q(1,2),1],[Q(1,10),Q(1,2),Q(19,20)],
                [Q(1,4),Q(3,4),Q(99,100)],
                [Q(9,10),Q(1,5),Q(-4,5)]),
    ]
    count=0
    branches=set()
    epsilon=Q(1,10**8)
    for law in laws:
        for z in [Q(k,37) for k in range(1,37)]:
            A,I,C=law.A(z),law.B(z),law.D(z)
            rho=law.A.affine_at(z)[0]
            ip=law.B.affine_at(z)[0]
            cp=law.D.affine_at(z)[0]
            alpha=law.parameters(I)[0]
            beta=law.parameters(C)[1]
            gamma=law.parameters(I)[2]
            if C>I:
                hprime=A+2*I+C+(alpha+z)*ip-4*rho-(8-z-beta)*cp
                branches.add('C>I')
            else:
                hprime=A+3*C+(alpha+gamma)*ip-4*rho-(8-2*z)*cp
                branches.add('C<I')
            _,u,c=law.parameters(A)
            E=1-law.D(-z)
            ep=law.D.affine_at(-z)[0]
            uminus=law.parameters(1-E)[1]
            predictions={'f':(2+c-u)*rho-3-E+(2-z-uminus)*ep,
                         'g':(1+z+c-u)*rho-(1-A)+E+(8+z-uminus)*ep,
                         'h':hprime}
            for kind,expected in predictions.items():
                derivative=4*(cost(law,kind,z+epsilon)-cost(law,kind,z-epsilon))/(2*epsilon)
                assert derivative==expected,(kind,z,derivative,expected)
                count+=1
    assert branches=={'C>I','C<I'}
    print(f'PASS: {count} exact derivatives with initial a and incoming u independent')
    print('PASS: both incoming/outgoing-front orderings and support gaps')
    print('PASS: moving negative-c fronts, including the capped negative-V part of N')
    print('Scope: dual identities; no solved boundary system or equilibrium')


if __name__=='__main__':
    main()
