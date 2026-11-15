#!/usr/bin/env python3
"""Exact unit-amplitude localized initial-inward feature.

Density: i(a,v)=1 on d<a<1 and -a<v<-d.  This is the I component
alone.  The tied k/ell ramp and all induced old-law densities are separate.
"""


class LocalizedInward:
    def __init__(self, d):
        if not 0 <= d < 1:
            raise ValueError("Expected a fixed cutoff in [0,1)")
        self.d, self.zero = d, d*0
        self.mass = (1-d)**2/2

    def constant_four_score(self, b, c):
        below = max(self.zero,b-self.d)**2/2
        return (4*self.mass+(1+c)*(self.mass-below)+8*below
                -max(self.zero,-self.d-c)*(1-b)**2/2)

    def graph_integrand(self, b, c, v, u):
        if b <= self.d or v >= -self.d:
            return self.zero
        return ((b+v)*(v+u-8)-(1+c-self.d-2*v)*(u-b)
                +(u*u-b*b)/2)

    def graph_four_score(self, b, c, graph):
        result = self.constant_four_score(b,c)
        if b <= self.d:
            return result
        for (vl,ul),(vr,ur) in zip(graph,graph[1:]):
            if vl == vr or vl >= -self.d:
                continue
            right = min(vr,-self.d)
            if right <= vl:
                continue
            slope = (ur-ul)/(vr-vl)
            def value(v):
                # The left trace at -d is used for integration.  A value
                # on this zero-measure boundary does not change the law.
                u = ul+slope*(v-vl)
                return ((b+v)*(v+u-8)-(1+c-self.d-2*v)*(u-b)
                        +(u*u-b*b)/2)
            result += (right-vl)*(value(vl)+4*value((vl+right)/2)+value(right))/6
        return result
