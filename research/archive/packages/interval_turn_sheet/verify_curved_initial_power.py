"""Independent high-precision capture audit of a curved initial phase.

This is a local asymptotic fixture, not a matching strategy.  The capture
engine intersects the actual curved/linear princess with every monster leg;
it does not use the initial-inward CDF response identity.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import mpmath as mp


def _first_root(fun, lo, hi):
    flo, fhi = fun(lo), fun(hi)
    if flo == 0:
        return lo
    if fhi == 0:
        return hi
    if flo * fhi > 0:
        return None
    # The relative displacement is monotone on a unit-speed monster leg.
    for _ in range(mp.mp.prec + 8):
        mid = (lo + hi) / 2
        fm = fun(mid)
        if fm == 0:
            return mid
        if flo * fm < 0:
            hi = mid
        else:
            lo, flo = mid, fm
    return (lo + hi) / 2


def polygon_capture(princess, monster, sign):
    best = mp.inf
    for (ta, xa), (tb, xb) in zip(monster, monster[1:]):
        mv = (xb-xa)/(tb-ta)
        mi = xa-mv*ta
        for (pa, ya), (pb, yb) in zip(princess, princess[1:]):
            lo, hi = max(ta, pa), min(tb, pb)
            if lo > hi:
                continue
            pv = sign*(yb-ya)/(pb-pa)
            pi = sign*ya-pv*pa
            slope, offset = pv-mv, pi-mi
            if slope == 0:
                if offset == 0:
                    best = min(best, lo)
            else:
                root = -offset/slope
                if lo <= root <= hi:
                    best = min(best, root)
    assert mp.isfinite(best)
    return best


class PowerWave:
    def __init__(self, gamma, kappa):
        self.gamma, self.kappa = mp.mpf(gamma), mp.mpf(kappa)
        self.low, self.high = mp.mpf(1) / 5, mp.mpf(2) / 5
        self.t0, self.c0 = mp.mpf(1) / 32, mp.mpf(9) / 10
        self.rho = 1 / (self.high - self.low)
        self.s0 = self.kappa * self.t0**self.gamma
        self.u0 = 2 * self.t0 - self.s0
        assert self.kappa * self.gamma * self.t0**(self.gamma-1) < 2
        assert self.high + self.u0 < self.c0 - self.high

    def princess_linear_vertices(self, b, sign):
        return [(self.t0, sign*(b+self.t0-self.s0)),
                (b+self.u0, mp.mpf(0)),
                (self.c0-b, mp.mpf(0)),
                (1+self.c0-b, mp.mpf(sign)),
                (mp.mpf(4), mp.mpf(sign))]

    def capture(self, b, monster, sign=1):
        """First actual equality, retaining initial and turn contacts."""
        best = mp.inf
        for (ta, xa), (tb, xb) in zip(monster, monster[1:]):
            velocity = (xb-xa)/(tb-ta)
            intercept = xa-velocity*ta
            lo, hi = max(ta, mp.mpf(0)), min(tb, self.t0)
            if lo <= hi:
                def difference(t):
                    return sign*(b+t-self.kappa*t**self.gamma) - (intercept+velocity*t)
                root = _first_root(difference, lo, hi)
                if root is not None:
                    best = min(best, root)
            vertices = self.princess_linear_vertices(b, sign)
            for (pa, ya), (pb, yb) in zip(vertices, vertices[1:]):
                lo, hi = max(ta, pa), min(tb, pb)
                if lo > hi:
                    continue
                pv = (yb-ya)/(pb-pa)
                pi = ya-pv*pa
                slope, offset = pv-velocity, pi-intercept
                if slope == 0:
                    if offset == 0:
                        best = min(best, lo)
                else:
                    root = -offset/slope
                    if lo <= root <= hi:
                        best = min(best, root)
        assert mp.isfinite(best)
        return best

    @staticmethod
    def monster(a, delta):
        v = -a+delta
        pts = [(mp.mpf(0), a)]
        if delta:
            pts.append((delta/2, a-delta/2))
        pts += [((1+v)/2, (1-v)/2),
                (mp.mpf(2), mp.mpf(-1)),
                (mp.mpf(4), mp.mpf(1))]
        return pts

    def direct_cost(self, a, delta):
        monster = self.monster(a, delta)
        # Rank cuts come from intersections at the initial princess turn
        # and the monster's first turn.  They are only quadrature cuts;
        # capture times are independently recomputed by segment equality.
        br = a-delta+self.kappa*(delta/2)**self.gamma
        cuts = sorted(set([self.low, self.high, a,
                           max(self.low, min(self.high, br)),
                           max(self.low, min(self.high, a+self.s0-delta))]))
        total = mp.mpf(0)
        for left, right in zip(cuts, cuts[1:]):
            if right > left:
                total += mp.quad(lambda b: self.capture(b, monster, 1)
                                  + self.capture(b, monster, -1), [left, right])
        return self.rho*total/2

    def g_derivative(self):
        # Independently differentiating the direct rank integral at delta=0.
        return self.rho*(1+self.c0-self.high-2*self.t0+self.s0)/4

    def exact_remainder(self, a, delta):
        g, k = self.gamma, self.kappa
        d = 1+self.c0-a
        return self.rho*(
            d*k/2**g*delta**g
            - 2*g/(g+1)*k**(-1/g)*delta**(1+1/g)
            + delta**2/2
            + k/((g+1)*2**g)*delta**(g+1)
            - k*k/2**(2*g+1)*delta**(2*g))

    def derivative_remainder(self, a, delta):
        g, k = self.gamma, self.kappa
        d = 1+self.c0-a
        return self.rho*(
            d*k*g/2**g*delta**(g-1)
            - 2*k**(-1/g)*delta**(1/g)
            + delta
            + k/2**g*delta**g
            - g*k*k/2**(2*g)*delta**(2*g-1))

    def flat_g_mixture(self, a, delta, wave_cost):
        """An ordered actual law, with g exactly constant near a."""
        wave_mass = mp.mpf(1)/20
        high_mass = 4*wave_mass*self.g_derivative()
        low_mass = 1-wave_mass-high_mass
        assert 0 < high_mass < 1-wave_mass
        low = [(mp.mpf(0), mp.mpf(0)),
               (mp.mpf(19)/20, mp.mpf(0)),
               (mp.mpf(39)/20, mp.mpf(1)),
               (mp.mpf(4), mp.mpf(1))]
        high = [(mp.mpf(0), mp.mpf(4)/5),
                (mp.mpf(1)/20, mp.mpf(17)/20),
                (mp.mpf(13)/20, mp.mpf(1)/4),
                (mp.mpf(7)/5, mp.mpf(1)),
                (mp.mpf(4), mp.mpf(1))]
        monster = self.monster(a, delta)
        low_cost = sum(polygon_capture(low, monster, s) for s in [-1, 1])/2
        high_cost = sum(polygon_capture(high, monster, s) for s in [-1, 1])/2
        return wave_mass*wave_cost+low_mass*low_cost+high_mass*high_cost


def run(quick=False):
    mp.mp.dps = 45
    a = mp.mpf(3)/10
    phi = (1+mp.sqrt(5))/2
    d = 1+mp.mpf(9)/10-a
    balanced = (2**(phi+1)/(phi*d))**(1/phi)
    cases = [("quadratic", mp.mpf(2), mp.mpf(1)),
             ("three_halves", mp.mpf(3)/2, mp.mpf(1)),
             ("golden_balanced", phi, balanced)]
    exponents = [12, 16] if quick else list(range(12, 19))
    rows, largest_error = [], mp.mpf(0)
    for label, gamma, kappa in cases:
        law = PowerWave(gamma, kappa)
        base = law.direct_cost(a, mp.mpf(0))
        mixed_base = law.flat_g_mixture(a, mp.mpf(0), base)
        for offset in [-mp.mpf(1)/100, mp.mpf(1)/100]:
            probe = law.direct_cost(a+offset, mp.mpf(0))
            assert abs(law.flat_g_mixture(a+offset, mp.mpf(0), probe)-mixed_base) < mp.mpf("1e-33")
        previous = None
        for power in exponents:
            delta = mp.mpf(2)**(-power)
            cost = law.direct_cost(a, delta)
            direct = 4*(cost-base+delta*law.g_derivative())
            formula = law.exact_remainder(a, delta)
            error = abs(direct-formula)
            largest_error = max(largest_error, error)
            assert error < mp.mpf("1e-33"), (label, power, error)
            actual_gain = 4*(law.flat_g_mixture(a, delta, cost)-mixed_base)
            assert abs(actual_gain-formula/20) < mp.mpf("1e-33")
            # Check the derivative independently from two direct capture
            # integrals, rather than differentiating the closed expression.
            step = delta*mp.mpf("1e-7")
            derivative = 4*((law.direct_cost(a, delta+step)
                            -law.direct_cost(a, delta-step))/(2*step)
                           +law.g_derivative())
            predicted_derivative = law.derivative_remainder(a, delta)
            assert abs(derivative-predicted_derivative) < mp.mpf("2e-11")*max(delta, abs(predicted_derivative))
            order = None if previous is None else mp.log(abs(previous[1]/direct))/mp.log(previous[0]/delta)
            rows.append(dict(case=label, delta=str(delta),
                             four_cost_remainder=str(direct),
                             actual_flat_g_four_cost_gain=str(actual_gain),
                             four_derivative_remainder=str(derivative),
                             observed_cost_order=None if order is None else str(order)))
            previous = delta, direct
    return dict(scope="Independent high-precision local fixtures; no equilibrium claim",
                precision_digits=mp.mp.dps, capture_checks=len(rows)*3+3*len(cases),
                largest_absolute_formula_error=str(largest_error),
                golden_ratio=str(phi), balanced_kappa=str(balanced), rows=rows)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--quick", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = run(args.quick)
    body = json.dumps(result, indent=2)
    if args.output:
        args.output.write_text(body+"\n")
    print(body)
