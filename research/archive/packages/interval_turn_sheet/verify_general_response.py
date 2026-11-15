#!/usr/bin/env python3
"""Independent exact capture audit for the full negative-M2 CDF formula.

Line integrals use the existing continuous-rank piecewise-affine engine;
the reference payoff follows the monster and integrates its capture
records. No turn-indifference or upper-density equation is used.
"""
from fractions import Fraction as Q
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'packages/interval_continuous_rank'))
from continuous_rank import MultiLegRankLaw


def integrate_line(law,start,end,velocity,intercept,threshold=None):
    result=Q(0)
    scale=1-law.endpoint_mass
    for lo,hi,(slope,constant),region in law._radial_cells(start,end,velocity,intercept):
        assert region in (0,1,2)
        slope*=scale
        constant*=scale
        if threshold is not None:
            constant-=threshold
        cuts=[lo,hi]
        if threshold is not None and slope:
            zero=-constant/slope
            if lo<zero<hi:
                cuts.insert(1,zero)
        for left,right in zip(cuts[:-1],cuts[1:]):
            if threshold is None or slope*(left+right)/2+constant>0:
                result+=slope*(right*right-left*left)/2+constant*(right-left)
    return result


def formula(law,z,s):
    assert 0<z<s<z+2
    A=(1-law.endpoint_mass)*law.A(z)
    radial=(1-law.endpoint_mass)*law.radial((s+z)/2,(s-z)/2)
    # Nbar: U=z, -z<V<z; Irow: V=z,z<U<s.
    Nbar=2*integrate_line(law,Q(0),z,Q(-1),z)
    Irow=2*integrate_line(law,z,(s+z)/2,Q(1),-z)
    G=2*integrate_line(law,s,s+1,Q(1),-s,A)
    return (Nbar+4*s+8-2*(s+1)*A-(s+6-z)*radial-Irow-G)/4


def main():
    laws=[
        MultiLegRankLaw([0,1],[Q(1,10),Q(9,10)],
                        [[Q(1,10),Q(9,10)]],[[Q(9,10),Q(1,10)]]),
        MultiLegRankLaw([0,Q(2,5),1],[Q(1,8),Q(1,2),Q(7,8)],
                        [[Q(1,4),Q(5,8),Q(15,16)],
                         [Q(17,16),Q(9,8),Q(5,4)]],
                        [[Q(1,5),Q(1,10),Q(-1,2)],
                         [Q(19,20),Q(3,4),Q(1,4)]],endpoint_mass=Q(1,11)),
        MultiLegRankLaw([0,1],[Q(1,10),Q(4,5)],
                        [[Q(1,5),Q(9,10)],
                         [Q(19,20),Q(11,10)],
                         [Q(6,5),Q(7,5)]],
                        [[Q(1,10),Q(-1,2)],
                         [Q(3,5),Q(1,5)],
                         [Q(19,20),Q(3,5)]],endpoint_mass=Q(2,17)),
    ]
    count=0
    for law in laws:
        for z in (Q(1,13),Q(3,13),Q(5,13),Q(7,13),Q(9,13),Q(11,13)):
            for s in ((z+1)/2,Q(1),Q(17,16),Q(5,4),z+Q(7,4)):
                monster=[(Q(0),-z),((s+z)/2,(s-z)/2),
                         (s+1,Q(-1)),(s+3,Q(1))]
                direct=law.payoff(monster).value
                predicted=formula(law,z,s)
                assert predicted==direct,(z,s,direct,predicted)
                count+=1
    print(f'PASS: {count} exact CDF identities, including early and late turns')
    print('PASS: one-, two-, and three-wave laws, center waits, negative exits, endpoint atoms')
    print('Scope: response identity only; no equilibrium or game-value certificate')


if __name__=='__main__':
    main()
