#!/usr/bin/env python3
"""Exact endpoint-I obstacle and the active-f initial-run obstruction."""
from collections import Counter
from fractions import Fraction as Q
from pathlib import Path
import sys

from verify_positive_cdf_sheet import finite_fixtures,direct_cost
from verify_curved_terminal_sources import inward_cost
from verify_repeated_same_half import alpha_moment
from verify_detached_inward_corner import fixtures as ordinary_fixtures, inward_route,f_route

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'packages/interval_continuous_rank'))
from continuous_rank import RankLaw


def inverse(path,coordinate,target):
    sign=1 if coordinate=='U' else -1
    if sign*path.knots[0][1]>=target:return Q(0)
    for t0,t1,slope,intercept in path.segments:
        m=1+sign*slope;b=sign*intercept
        if m*t1+b>=target:
            assert m>0
            return max(t0,(target-b)/m)
    raise AssertionError('inverse outside path horizon')


def initial_band_kernel(law,a,b):
    meeting=(a-b)/2;S=2-b
    answer=Q(0)
    for weight,path in law.paths:
        initial=path.value(Q(0))
        if not b<=initial<=a:continue
        first=inverse(path,'U',a)
        old=inverse(path,'V',-b)
        new=first if first<=meeting else inverse(path,'U',S)
        answer+=2*weight*(new-old)
    return answer


def field_obstacle(law,a,b):
    x,y=1-a,1-b;S=2-b
    # The lower initial boundary includes an a=b atom caught by Cf at 0;
    # the upper boundary includes the initial-a atom caught by I at 0.
    rx=1-sum((w for w,p in law.paths if p.value(Q(0))<=a),Q(0))
    ry=1-sum((w for w,p in law.paths if p.value(Q(0))<b),Q(0))
    D0=1-law.radial(a,-b,strict=True)
    row=(a-b)-law.integrate(a,-a,-b,horizontal=True,strict=True)
    column=law.integrate(-b,b,S,horizontal=False,
                         transform=lambda R:max(Q(0),1-R-rx))
    return (alpha_moment(law,S,ry)-alpha_moment(law,S,D0)
            +(y-x)*D0-row-column)


def ordinary_band_upper(law,a,b):
    low,high=law.A(b),law.A(a)
    cuts=sorted({low,high}|{q for q in law.q if low<q<high})
    def integrand(q):
        initial,incoming,_=law.parameters(q)
        return a+b-initial-incoming
    return sum(((v-u)*(integrand(u)+integrand(v))/2
                for u,v in zip(cuts,cuts[1:])),Q(0))


def rank_integral(law,lo,hi,function):
    answer=Q(0);cumulative=Q(0)
    for weight,path in law.paths:
        width=max(Q(0),min(hi,cumulative+weight)-max(lo,cumulative))
        answer+=width*function(path)
        cumulative+=weight
    return answer


def main():
    counts=Counter()
    for law in finite_fixtures():
        starts={Q(1,10),Q(1,4),Q(1,2),Q(3,4),Q(9,10)}
        starts.update(p.value(Q(0)) for _,p in law.paths if 0<p.value(Q(0))<1)
        for b in sorted(starts):
            ends={b,(3*b+1)/4,(b+1)/2,(b+3)/4,Q(1)}
            ends.update(p.value(Q(0)) for _,p in law.paths if b<=p.value(Q(0))<=1)
            for a in sorted(ends):
                actual=4*(inward_cost(law,a,-b,2-b)-direct_cost(law,2-b,b))
                assert actual==initial_band_kernel(law,a,b),(a,b,'capture kernel')
                assert actual==field_obstacle(law,a,b),(a,b,'field obstacle')
                counts['endpoint-I initial-band kernels']+=1
                counts['full post-one endpoint field obstacles']+=1
                # Hold the input row/column moments fixed, and put the
                # formal local deficit at the initial upper boundary.
                rx=1-sum((w for w,p in law.paths if p.value(Q(0))<=a),Q(0))
                ry=1-sum((w for w,p in law.paths if p.value(Q(0))<b),Q(0))
                row=(a-b)-law.integrate(a,-a,-b,horizontal=True,strict=True)
                column=law.integrate(-b,b,2-b,horizontal=False,
                                     transform=lambda R:max(Q(0),1-R-rx))
                raw=(4*direct_cost(law,2-b,b)
                     +alpha_moment(law,2-b,ry)-alpha_moment(law,2-b,rx)
                     +(a-b)*rx-row-column)
                assert raw>=4*direct_cost(law,2-a,a)+(2+rx)*(a-b)
                counts['formal initial-rank lower barriers']+=1
                if ry>rx:
                    d0=rx+(ry-rx)/3;d1=rx+2*(ry-rx)/3
                    slope=(alpha_moment(law,2-b,d1)-alpha_moment(law,2-b,d0)
                           -(a-b)*(d1-d0))
                    assert slope>=(2-a-b)*(d1-d0)
                    counts['monotone endpoint inverse slopes']+=1
                if any(p.value(Q(0)) in (a,b) for _,p in law.paths):
                    counts['initial-atom boundary witnesses']+=1
                if law.radial(a,-b,strict=True)!=law.radial(a,-b):
                    counts['strict first-turn trace witnesses']+=1
                A0=1-ry;A=1-rx;L=law.radial(a,-b,strict=True)
                B1=law.radial(Q(1),-b);M=max(A,B1)
                cross=2*((inward_cost(law,a,-b,2-b)-inward_cost(law,a,-b))
                         -(direct_cost(law,2-b,b)-direct_cost(law,Q(1),b)))
                rhs=(rank_integral(law,A0,L,
                                   lambda p:inverse(p,'U',2-b)-inverse(p,'U',Q(1)))
                     +rank_integral(law,B1,M,
                                    lambda p:inverse(p,'V',Q(3))-inverse(p,'V',-b)))
                assert cross==rhs>=((1-b)/2*(L-A0)+(3+b)*(M-B1))
                counts['endpoint versus fixed-turn cross identities']+=1
                if rhs>0:counts['strict positive-M2 slack witnesses']+=1

    ordinary=list(ordinary_fixtures())
    ordinary.append(RankLaw([0,1],[0,1],[Q(1,2),1],[0,-1]))
    for law in ordinary:
        for b in [Q(3,5),Q(7,10),Q(4,5),Q(9,10),Q(19,20)]:
            q=law.A(b);_,u,_=law.parameters(q)
            for fraction in [Q(1,4),Q(1,2),Q(3,4)]:
                a=b+fraction*(u-b)
                kernel=ordinary_band_upper(law,a,b)
                actual=4*(law.payoff(inward_route(a,-b,2-b)).value
                          -law.payoff(f_route(b)).value)
                assert actual<=kernel<0,(a,b,actual,kernel)
                counts['strict finite attacks on positive M1']+=1
                if actual==kernel:
                    counts['exact ordinary first-leg kernels']+=1
                else:
                    counts['strict kernel bounds when old capture is later']+=1
    print('PASS:',sum(counts.values()),'exact endpoint-inward checks')
    for name,n in counts.items():print(' ',name+':',n)
    print('Scope: active positive M1 also forbids an ordinary initial unit run')


if __name__=='__main__':main()
