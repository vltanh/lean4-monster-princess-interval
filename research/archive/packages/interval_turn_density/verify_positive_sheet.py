#!/usr/bin/env python3
"""Exact positive-M2 late-sheet corridor and envelope identities.

The alpha cross-price vanishes only when the initial princess position
is above the entire positive-sheet start support.  This verifier checks
that high-initial branch and makes no unrestricted-response claim.
"""
from fractions import Fraction as Q

def main():
    count=0
    for zi in range(1,8):
        z=Q(zi,8)
        def f(x):return (8+z)*x-x*x/2
        def F(x):return (8+z)*x*x/2-x*x*x/6
        for vi in range(1,5):
            v=1+(1-z)*Q(vi,4);W=v+6+z
            edge=(f(2-v)-f(z))/W
            assert edge>=0
            def j(s):return edge+v-s
            Gamma=F(2-v)-f(z)*(2-z-v)
            for ai in range(9):
                a=z+(1-z)*Q(ai,8)
                def score(u):
                    R=max(Q(0),F(2-u)-F(a))
                    integral=Q(0)
                    if u<v:
                        def integrand(s):return (2*s+6+z-u)*j(s)
                        integral=(v-u)*(integrand(u)+4*integrand((u+v)/2)+integrand(v))/6
                    return R-f(z)*(2-z-u)-integral
                bound=max(Q(0),Gamma-F(a))
                for ui in range(17):
                    u=1+(1-z)*Q(ui,16)
                    assert score(u)<=bound,(z,v,a,u,score(u),bound)
                    if u<=min(v,2-a):
                        assert score(u)==Gamma-F(a)
                        tail=(v-u)*(j(u)+j(v))/2
                        assert -f(2-u)+f(z)+tail+(u+6+z)*j(u)==0
                    count+=1
                assert score(2-z)==0
                if Gamma>=F(a):assert score(Q(1))==bound
    print(f'PASS: {count} exact positive-sheet corridor/envelope checks')
    print('Scope: high initial positions; low-initial alpha cross-price remains explicit')

if __name__=='__main__':main()
