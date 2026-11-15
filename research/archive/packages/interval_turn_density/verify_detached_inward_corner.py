#!/usr/bin/env python3
"""Exact detached double-corner costs, without positive-M2 indifference.

The independent continuous-rank engine integrates the complete signed CDF
records along the physical monster route.  The comparison side uses only
one-dimensional front moments.  These checks are identities for ordinary
ordered laws; they do not construct an f/ell/I equilibrium.
"""
from collections import Counter
from fractions import Fraction as Q
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'packages/interval_continuous_rank'))
from continuous_rank import PiecewiseCDF, RankLaw


class Fronts:
    def __init__(self, law):
        self.x = tuple(1-a for a in law.a[::-1])
        self.mass = tuple(1-q for q in law.q[::-1])
        self.h_values = tuple(1-u for u in law.u[::-1])
        self.d_values = tuple(1+c for c in law.c[::-1])
        self.r = PiecewiseCDF(self.x, self.mass)
        self.h = PiecewiseCDF(self.x, self.h_values)
        self.d = PiecewiseCDF(self.x, self.d_values)
        self.inverse_d = PiecewiseCDF(self.d_values, self.x)
        self.inverse_h = PiecewiseCDF(self.h_values, self.x)
        self.incoming = PiecewiseCDF(self.h_values, self.mass)

    def moment(self, left, right, function):
        """Integrate a continuous piecewise-affine function against dr."""
        cuts = sorted({left, right} | {x for x in self.x if left < x < right})
        return sum(((function(a)+function(b))/2*(self.r(b)-self.r(a))
                    for a, b in zip(cuts, cuts[1:])), Q(0))


def inward_route(a, v, s):
    return [(Q(0), a), ((a+v)/2, (a-v)/2),
            ((s+v)/2, (s-v)/2), (s+1, Q(-1)), (s+3, Q(1))]


def f_route(a):
    return [(Q(0), a), (1-a, Q(1)), (3-a, Q(-1)), (5-a, Q(1))]


def ell_route(a):
    return [(Q(0), a), (a+1, Q(-1)), (a+3, Q(1))]


def endpoint_route():
    return [(Q(0), Q(1)), (Q(2), Q(-1)), (Q(4), Q(1))]


def ridge_moment(fronts, x, y):
    """Four times the ridge payoff minus the endpoint payoff; Q=Omega=0."""
    tau = fronts.inverse_d(y)
    k = fronts.h(tau)
    m = min(y, fronts.inverse_h(x))
    R, rx, E = fronts.r(m), fronts.r(x), fronts.r(tau)
    assert tau < x <= m
    return (y*rx+(8-y)*E
            -fronts.moment(Q(0), m, fronts.d)
            +fronts.moment(x, m, lambda t: t-x)
            -fronts.moment(tau, x, fronts.h)
            -k*(3-R+2*E))


def slopes(x, y):
    return [(b-a)/(v-u) for u, v, a, b in zip(x, x[1:], y, y[1:])]


def fixtures():
    yield RankLaw([0, 1], [Q(1, 2), 1], [Q(3, 4), 1], [Q(1, 2), -1])
    yield RankLaw([0, Q(1, 3), Q(3, 4), 1],
                  [Q(1, 2), Q(3, 4), Q(15, 16), 1],
                  [Q(4, 5), Q(9, 10), Q(63, 64), 1],
                  [Q(3, 4), Q(1, 4), -Q(1, 2), -1])
    yield RankLaw([0, Q(1, 4), Q(1, 2), Q(7, 8), 1],
                  [Q(1, 4), Q(1, 2), Q(3, 4), Q(31, 32), 1],
                  [Q(3, 4), Q(7, 8), Q(15, 16), Q(511, 512), 1],
                  [Q(7, 8), Q(3, 4), Q(1, 4), -Q(3, 4), -1])


def main():
    counts = Counter()
    examples = []
    for law in fixtures():
        fronts = Fronts(law)
        for values, axis in [(fronts.mass, fronts.x),
                             (fronts.mass, fronts.h_values)]:
            density = slopes(axis, values)
            assert all(a >= b for a, b in zip(density, density[1:])), density
        # Work beyond the largest positive outgoing row, so the endpoint
        # tail and all retained low-alpha terms have the stated form.
        for xi in sorted({Q(j, 1000) for j in range(1, 100, 7)}
                         | {Q(1, 64), Q(1, 32), Q(1, 16)}):
            x = fronts.h(xi)
            tau = fronts.inverse_d(xi)
            if not 0 < tau < x < xi < fronts.x[-1]:
                continue
            k = fronts.h(tau)
            a, v, s = 1-x, -1+xi, 1-k
            if 1-x <= max(law.c):
                continue
            R, rx, E = fronts.r(xi), fronts.r(x), fronts.r(tau)
            correction = k*(3-R+2*E)
            corner = (x*(3+2*rx-R)-(8-xi)*(rx-E)
                      -fronts.moment(tau, x, fronts.h)-correction)
            actual = 4*(law.payoff(inward_route(a, v, s)).value
                        -law.payoff(ell_route(a)).value)
            assert actual == corner, ('double corner versus ell', xi, actual, corner)
            counts['double corner versus negative M1'] += 1

            fixed = law.payoff(inward_route(a, v, Q(1))).value
            moved = law.payoff(inward_route(a, v, s)).value
            assert 4*(fixed-moved) == correction
            counts['exact second-ridge correction'] += 1

            moment = fronts.moment(x, xi, lambda t: t-x+fronts.h(t))
            reduced = (8-2*xi)*E-3*xi+xi*rx+moment-correction
            actual = 4*(moved-law.payoff(f_route(1-xi)).value)
            assert actual == reduced, ('double corner versus positive M1', xi, actual, reduced)
            counts['f/ell-free reduced front identity'] += 1
            assert actual != 8*E-3*xi+xi*rx+moment-correction
            counts['nonzero two-xi-E coefficient witnesses'] += 1
            examples.append((xi, x, tau, k, corner, reduced))

        endpoint = law.payoff(endpoint_route()).value
        for x in [Q(1, 1000), Q(1, 300), Q(1, 100), Q(1, 50)]:
            for multiplier in [Q(1), Q(5, 4), Q(3, 2), Q(2), Q(3), Q(4)]:
                y = multiplier*x
                tau = fronts.inverse_d(y)
                if not 0 < tau < x or 1-x <= max(law.c):
                    continue
                k = fronts.h(tau)
                a, v = 1-x, -1+y
                ridge = law.payoff(inward_route(a, v, 1-k)).value
                actual = 4*(ridge-endpoint)
                expected = ridge_moment(fronts, x, y)
                assert actual == expected, ('general ridge moment', x, y, actual, expected)
                counts['general ridge front moments'] += 1

                collapsed = law.payoff(ell_route(a)).value
                lower = min(collapsed, ridge)
                defects = {Q(0), x, k, fronts.h(x)}
                defects.update(x*Q(j, 8) for j in range(1, 8))
                defects.update(k*Q(j, 4) for j in [1, 2, 3])
                defects.update(k+(fronts.h(x)-k)*Q(j, 4) for j in [1, 2, 3])
                for z in sorted(defects):
                    assert 0 <= z <= x
                    cost = law.payoff(inward_route(a, v, 1-z)).value
                    assert cost >= lower, ('second-turn reduction', x, y, z, cost, lower)
                    counts['full-second-turn endpoint/ridge dominance'] += 1
    print('PASS:', sum(counts.values()), 'exact detached-corner checks')
    for name, n in counts.items():
        print(' ', name+':', n)
    print('Scope: exact physical costs; no g equality, no matching-law claim')
    print('The reduced outgoing coefficient is 8-2*xi, not 8.')


if __name__ == '__main__':
    main()
