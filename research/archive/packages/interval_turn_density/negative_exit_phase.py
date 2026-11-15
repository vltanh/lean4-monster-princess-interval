#!/usr/bin/env python3
"""Construct a positive-start late sheet with a supplied lower-rank flux.

The cap mass d may vary from row to row.  J(s) is the actual lower-rank
post-incoming flux for this start, not an arbitrary omitted error term.
For fixed z,A,d,J, one monotone scalar equation determines the exit and
then E is explicit.  This local row construction does not solve global
quantile matching or the remaining upper/lower phases.
"""
from dataclasses import dataclass
from fractions import Fraction as F


@dataclass
class SourceResolvedCap:
    z: float
    A: float
    d: float
    source: object
    epsabs: float = 2e-11

    def __post_init__(self):
        from scipy.integrate import quad
        from scipy.optimize import brentq
        if not 0 < self.z < 1 or not 0 <= self.A <= 1 or self.d < 0:
            raise ValueError("Invalid start, initial CDF, or cap mass")
        self.endpoint_turn = 2-self.z
        self.L0 = 7+self.z
        self.T = self.A+2+2*self.d
        self.L = self.T/2
        self.integral = lambda lo,hi: (quad(self.source,lo,hi,epsabs=self.epsabs,
                                           epsrel=2e-11)[0] if hi>lo else 0.)
        self.moment = lambda s: (quad(lambda r:(6+r+self.z)*self.source(r),1,s,
                                      epsabs=self.epsabs,epsrel=2e-11)[0] if s>1 else 0.)
        def gap(v):
            return self.T*(self.endpoint_turn-v)-8*self.d+self.integral(v,self.endpoint_turn)
        self.lower_edge_gap = gap(1.)
        if self.lower_edge_gap < -self.epsabs:
            raise ValueError("No cap exit in the legal turn interval")
        self.v = self.endpoint_turn if self.d == 0 else brentq(gap,1.,self.endpoint_turn,xtol=2e-13)
        self.Wv = 6+self.v+self.z
        self.E = (self.d+self.L*((self.Wv/self.L0)**2-1)
                  +self.moment(self.v)/self.L0**2)
        self.K = (1+self.A/2+self.E)*self.L0**2
        self.initial_rank_slack = 1-self.A-self.E

    def B(self,s):
        if not 1 <= s <= self.endpoint_turn:
            raise ValueError("Turn outside the positive late domain")
        if s >= self.v:
            return 1-self.d
        W=6+s+self.z
        return 2+self.A/2-(self.K-self.moment(s))/W**2

    def B_derivative(self,s):
        if s >= self.v:return 0.
        W=6+s+self.z
        return (4+self.A+self.source(s)-2*self.B(s))/W

    def negative_flux_moment(self):
        D=1+self.A/2+self.E
        return (2*self.L*self.Wv-2*D*self.L0+8*(D-self.L)
                +self.integral(1.,self.v))

    def endpoint_minus_line_four_cost(self):
        return ((1-self.z)*(self.A+2)-(6+2*self.z)*self.E
                +self.integral(1.,self.endpoint_turn)-self.negative_flux_moment())


def exact_verification():
    """Independent rational check with affine nonnegative flux sources."""
    count=0;nonzero=0;legal=0
    for z in (F(1,8),F(1,4),F(1,2),F(3,4),F(7,8)):
        L0=7+z;sstar=2-z
        for A in (F(0),F(1,10),F(2,5),F(7,10)):
            for fraction in (F(1,8),F(1,4),F(1,2),F(3,4),F(7,8)):
                v=1+(1-z)*fraction;Wv=6+v+z;gap=sstar-v
                for j0,j1 in ((F(0),F(0)),(F(1,20),F(0)),
                              (F(0),F(1,10)),(F(1,20),F(1,10))):
                    J=lambda s:j0+j1*(s-1)
                    Q=lambda lo,hi:j0*(hi-lo)+j1*((hi-1)**2-(lo-1)**2)/2
                    TJ=lambda s: (j1*((6+s+z)**3-L0**3)/3
                                  +(j0-j1*L0)*((6+s+z)**2-L0**2)/2)
                    d=((A+2)*gap+Q(v,sstar))/(8-2*gap)
                    T=A+2+2*d;L=T/2
                    E=d+L*(Wv**2/L0**2-1)+TJ(v)/L0**2
                    D=1+A/2+E;K=D*L0**2
                    B=lambda s:2+A/2-(K-TJ(s))/(6+s+z)**2
                    assert B(1)==1-E
                    assert B(v)==1-d
                    assert T*(sstar-v)==8*d-Q(v,sstar)
                    count+=3
                    if E<=1-A:legal+=1
                    # Direct polynomial / reciprocal-square integration of
                    # B(s)-(1-E), independent of the simplified moment.
                    offset=2+A/2+(j0-j1*L0)/2
                    constant=K+j1*L0**3/3+(j0-j1*L0)*L0**2/2
                    first=((offset-(1-E))*(v-1)+j1*(Wv**2-L0**2)/6
                           +constant*(1/Wv-1/L0))
                    qneg=first+(E-d)*(sstar-v)
                    simplified=2*L*Wv-2*D*L0+8*(D-L)+Q(1,v)
                    assert qneg==simplified
                    assert (1-z)*(A+2)-(6+2*z)*E+Q(1,sstar)-qneg==0
                    count+=2
                    for s in (1,(1+v)/2,v):
                        W=6+s+z
                        derivative=J(s)/W+2*(K-TJ(s))/W**3
                        assert W*derivative+2*B(s)==4+A+J(s)
                        assert derivative>=0
                        count+=2
                    nonzero+=int(j0>0 or j1>0)
    print(f'PASS: {count} exact source-resolved cap identities; {nonzero} nonzero-source rows, {legal} initial-rank-legal rows')


if __name__=='__main__':exact_verification()
