#!/usr/bin/env python3
"""Exact ordinary-wave center actions and finite initial-prefix formulas.

All integrals are over the continuous rank law.  No finite princess sample
or finite capture matrix is used.  See CENTER_BELLMAN_CERTIFICATE.md for the
scope of the corresponding unrestricted-response criterion.
"""
from bisect import bisect_right


class CenterActions:
    def __init__(self, law):
        if law.endpoint_mass != 0:
            raise ValueError("The ordinary-wave certificate has no separate endpoint atom")
        if not all(a + u <= 2 for a, u in zip(law.a, law.u)):
            raise ValueError("Initial outward turns must satisfy a+u<=2")
        self.law = law
        self.zero, self.one = law.zero, law.one
        self._u_primitive = [self.zero]
        for left, right, uleft, uright in zip(law.q, law.q[1:], law.u, law.u[1:]):
            self._u_primitive.append(self._u_primitive[-1] + (right-left)*(uleft+uright)/2)
        self.tau = self._center_peak()

    def _center_peak(self):
        law = self.law
        cuts = sorted({self.zero, self.one, *[x for x in law.u if 0 < x < 1],
                       *[x for x in law.c if 0 < x < 1]})
        for left, right in zip(cuts, cuts[1:]):
            fl = law.B(left)-law.D(left)
            fr = law.B(right)-law.D(right)
            if fl >= 0:
                return left
            if fr >= 0:
                return left+(right-left)*(-fl)/(fr-fl)
        return self.one

    def uint(self, q):
        """Integral from zero to q of the incoming characteristic u(rank)."""
        q = min(self.one, max(self.zero, q))
        law = self.law
        i = min(max(bisect_right(law.q, q)-1, 0), len(law.q)-2)
        width = q-law.q[i]
        slope = (law.u[i+1]-law.u[i])/(law.q[i+1]-law.q[i])
        return self._u_primitive[i]+law.u[i]*width+slope*width*width/2

    def int_u(self, lo, hi):
        return self.uint(hi)-self.uint(lo)

    def alpha(self, q, s):
        a, u, c = self.law.parameters(q)
        if s <= a:
            return self.zero
        if s <= u:
            return (s-a)/2
        return max(s-1, min(s, (s+c)/2))

    def beta(self, q, s):
        a, u, c = self.law.parameters(q)
        if s <= -a:
            return self.zero
        if s <= c:
            return max(s, (u+s)/2)
        return s+1

    def inverse_integral(self, kind, s, lo, hi):
        """Exact affine-cell integration, including inverse jumps at u=s."""
        if hi <= lo:
            return self.zero
        law = self.law
        cuts = {lo, hi, *[q for q in law.q if lo < q < hi]}
        targets = ((law.a, (s,)), (law.u, (s,)), (law.c, (s, s-2)))
        if kind == "beta":
            targets = ((law.a, (-s,)), (law.u, (s,)), (law.c, (s,)))
        for values, levels in targets:
            for q0, q1, v0, v1 in zip(law.q, law.q[1:], values, values[1:]):
                for level in levels:
                    if min(v0, v1) < level < max(v0, v1):
                        root = q0+(q1-q0)*(level-v0)/(v1-v0)
                        if lo < root < hi:
                            cuts.add(root)
        cuts = sorted(cuts)
        function = self.alpha if kind == "alpha" else self.beta
        # The midpoint avoids selecting the wrong trace at an inverse jump.
        return sum(((right-left)*function((left+right)/2, s)
                    for left, right in zip(cuts, cuts[1:])), self.zero)

    def endpoint(self, e, r, n):
        return (e+2)*(1-(r+n)/2)-abs(r-n)/2

    def triangle(self, t, e, m):
        lo, hi = self.law.B(t), self.law.B(e)
        return (self.int_u(lo, hi)+t*(hi-lo))/4+e*max(self.zero, hi-m)/2

    def wait(self, t, e, m):
        lo, hi = self.law.B(t), self.law.B(e)
        return (self.int_u(lo, hi)+self.int_u(m, max(m, hi)))/2

    def sweep(self, t, m):
        lo, hi = self.law.B(t), self.law.D(t)
        return ((self.int_u(lo, hi)+t*(hi-lo))/4
                +(t+1)*(1-hi)/2+(t+3)*(1-m)/2)

    def terminal_triangle(self, t, e, m):
        lo = self.law.B(t)
        r, n = min(self.law.B(e), self.law.D(t)), self.law.D(e)
        return ((self.int_u(lo, r)+t*(r-lo))/4
                +e*max(self.zero, n-m)/2+self.endpoint(e, r, max(m, n)))

    def center_prefix(self, z, v, b):
        law = self.law
        a0 = law.A(z)
        r0 = law.radial((z+v)/2, (z-v)/2)
        r1 = law.radial((b+v)/2, (b-v)/2)
        center = min(law.B(b), law.D(b))
        m = max(a0, r1)
        value = (self.inverse_integral("alpha", b, self.zero, r0)
                 +self.inverse_integral("alpha", z, r0, a0)
                 +self.inverse_integral("beta", v, a0, m)+b*center)/2
        return value, m, center

    def endpoint_prefix(self, z, v, b, w):
        law = self.law
        a0 = law.A(z)
        r0 = law.radial((z+v)/2, (z-v)/2)
        r1 = law.radial((b+v)/2, (b-v)/2)
        r2 = law.radial((b+w)/2, (b-w)/2)
        low, high = min(r0, r2), max(a0, r1)
        return (self.inverse_integral("alpha", z, r0, a0)
                +self.inverse_integral("alpha", b, low, r0)
                +self.inverse_integral("alpha", w+2, self.zero, low)
                +self.inverse_integral("beta", v, a0, high)
                +self.inverse_integral("beta", w, high, self.one)
                +self.inverse_integral("beta", w+2, self.zero, self.one))/2

    def density_breakpoints(self):
        """Fixed incoming-density partition; constant pieces satisfy (K)."""
        return tuple(x for x in self.law.u if 0 < x < self.tau)


def center_prefix_route(z, v, b):
    return [(z*0, z), ((z+v)/2, (z-v)/2),
            ((b+v)/2, (b-v)/2), (b, b*0)]


def endpoint_prefix_route(z, v, b, w):
    return [(z*0, z), ((z+v)/2, (z-v)/2),
            ((b+v)/2, (b-v)/2), ((b+w)/2, (b-w)/2),
            (w+1, w*0+1), (w+3, w*0-1)]


def append_wait(route, e):
    if e > route[-1][0]:
        route.append((e, e*0))


def append_triangle(route, t, e, sign=-1):
    append_wait(route, t)
    if e > t:
        route.extend([((t+e)/2, sign*(e-t)/2), (e, e*0)])


def append_sweep(route, t, sign=-1):
    append_wait(route, t)
    route.extend([(t+1, sign), (t+3, -sign)])


def append_terminal_triangle(route, actions, t, e, m, sign=-1):
    append_triangle(route, t, e, sign)
    r = min(actions.law.B(e), actions.law.D(t))
    n = max(m, actions.law.D(e))
    first = sign if r <= n else -sign
    route.extend([(e+1, first), (e+3, -first)])
