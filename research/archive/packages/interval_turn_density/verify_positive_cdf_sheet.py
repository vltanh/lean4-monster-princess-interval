#!/usr/bin/env python3
"""Exact lower-CDF identities for positive-start early and late turns.

This verifier is independent of the continuum/rank payoff implementations.
It intersects finite piecewise-linear paths directly, integrates their step
CDFs with Fraction arithmetic, and checks the capped inverse-square sheet
algebra.  It is not a matched lower law or an unrestricted lower certificate.
See research/10-turn-density/POSITIVE_TURN_SHEET.md.
"""

from bisect import bisect_right
from collections import Counter
from fractions import Fraction as Q
from functools import lru_cache


ZERO, ONE, TWO = Q(0), Q(1), Q(2)
HORIZON = Q(6)


class Path:
    def __init__(self, knots):
        self.knots = tuple((Q(t), Q(x)) for t, x in knots)
        assert self.knots[0][0] == 0
        self.times = tuple(t for t, _ in self.knots)
        self.segments = []
        for (t0, x0), (t1, x1) in zip(self.knots, self.knots[1:]):
            assert t1 > t0
            slope = (x1 - x0) / (t1 - t0)
            assert abs(slope) <= 1
            self.segments.append((t0, t1, slope, x0 - slope * t0))
        assert all(0 <= x <= 1 for _, x in self.knots)
        assert self.value(TWO) == 1
        assert all(x == 1 for t, x in self.knots if t >= 2)

    @lru_cache(maxsize=None)
    def value(self, t):
        assert 0 <= t <= self.times[-1]
        if t == self.times[-1]:
            return self.knots[-1][1]
        i = bisect_right(self.times, t) - 1
        _, _, slope, intercept = self.segments[i]
        return slope * t + intercept


def clipped_expression(lines, expression):
    """Resolve a min/max of affine lines without numerical root finding."""
    lines = [(Q(m), Q(b)) for m, b in lines]
    cuts = {ZERO, HORIZON}
    for i, (m, b) in enumerate(lines):
        for n, c in lines[i + 1:]:
            if m != n:
                t = (c - b) / (m - n)
                if 0 < t < HORIZON:
                    cuts.add(t)
    knots = [(t, expression([m * t + b for m, b in lines]))
             for t in sorted(cuts)]
    reduced = []
    for point in knots:
        reduced.append(point)
        while len(reduced) >= 3:
            (t0, x0), (t1, x1), (t2, x2) = reduced[-3:]
            if (x1 - x0) * (t2 - t1) != (x2 - x1) * (t1 - t0):
                break
            reduced.pop(-2)
    return Path(reduced)


def wave(a, u, c, v, y):
    a, u, c, v, y = map(Q, (a, u, c, v, y))
    return clipped_expression(
        [(1, a), (-1, u), (1, -c), (-1, v), (1, -y), (0, 0), (0, 1)],
        lambda x: min(x[6], max(x[5], min(x[0], x[1]),
                               min(x[2], x[3]), x[4])))


def slow_wave(a, u, c):
    return clipped_expression(
        [(Q(1, 2), a), (-Q(3, 4), u), (1, -c), (0, 0), (0, 1)],
        lambda x: min(x[4], max(x[3], min(x[0], x[1]), x[2])))


class Law:
    def __init__(self, weighted_paths):
        self.paths = tuple((Q(w), path) for w, path in weighted_paths)
        assert sum(w for w, _ in self.paths) == 1
        assert all(w > 0 for w, _ in self.paths)
        cuts = sorted({t for _, path in self.paths for t, _ in path.knots})
        for t in cuts:
            positions = [path.value(t) for _, path in self.paths]
            assert positions == sorted(positions), ('not ordered', t, positions)

    def initial(self, z):
        # An a=z atom is caught at time zero and belongs to the beta term.
        return sum((w for w, path in self.paths if path.value(ZERO) < z), ZERO)

    @lru_cache(maxsize=None)
    def radial(self, u, v, strict=False):
        t, r = (u + v) / 2, (u - v) / 2
        assert 0 <= r <= 1
        if strict:
            return sum((w for w, path in self.paths if path.value(t) < r), ZERO)
        return sum((w for w, path in self.paths if path.value(t) <= r), ZERO)

    def line_cuts(self, fixed, lo, hi, *, horizontal):
        cuts = {lo, hi}
        for _, path in self.paths:
            for t0, t1, m, b in path.segments:
                for t in (t0, t1):
                    x = 2 * t - fixed
                    if lo < x < hi:
                        cuts.add(x)
                denominator = m + 1 if horizontal else m - 1
                numerator = ((m - 1) * fixed + 2 * b if horizontal
                             else (m + 1) * fixed + 2 * b)
                if denominator:
                    x = -numerator / denominator
                    t = (x + fixed) / 2
                    if lo < x < hi and t0 <= t <= t1:
                        cuts.add(x)
        return sorted(cuts)

    def integrate(self, fixed, lo, hi, *, horizontal, strict=False,
                  transform=lambda value: value):
        if hi == lo:
            return ZERO
        assert hi > lo
        cuts = self.line_cuts(fixed, lo, hi, horizontal=horizontal)
        answer = ZERO
        for left, right in zip(cuts, cuts[1:]):
            middle = (left + right) / 2
            u, v = (fixed, middle) if horizontal else (middle, fixed)
            answer += (right - left) * transform(self.radial(u, v, strict))
        return answer

    def f(self, s, z, *, strict=True):
        a = self.initial(z)
        return self.integrate(s, -z, s, horizontal=True, strict=strict,
                              transform=lambda r: max(ZERO, a - r))

    def column(self, z, lo, hi):
        return self.integrate(-z, lo, hi, horizontal=False)

    def h(self, s):
        return self.integrate(s, s, s + 2, horizontal=False)


def first_capture(path, route, reflection):
    """First zero of two affine paths; inclusive first contact at every knot."""
    end = route[-1][0]
    cuts = sorted({t for t, _ in route}
                  | {t for t, _ in path.knots if t <= end})
    route_times = [t for t, _ in route]

    def monster(t):
        if t == end:
            return route[-1][1]
        i = bisect_right(route_times, t) - 1
        (t0, x0), (t1, x1) = route[i:i + 2]
        return x0 + (x1 - x0) * (t - t0) / (t1 - t0)

    for left, right in zip(cuts, cuts[1:]):
        dl = monster(left) - reflection * path.value(left)
        dr = monster(right) - reflection * path.value(right)
        if dl == 0:
            return left
        if dl * dr <= 0:
            return left + (right - left) * dl / (dl - dr)
    raise AssertionError(('incomplete route', route, reflection))


def direct_cost(law, s, z):
    route = [(ZERO, z), ((s - z) / 2, (s + z) / 2),
             (s + 1, -ONE), (s + 3, ONE)]
    return sum((w * (first_capture(path, route, 1)
                     + first_capture(path, route, -1)) / 2
                for w, path in law.paths), ZERO)


def four_cost(law, s, z, *, row_strict=True, turn_closed=True,
              retain_h=True):
    a = law.initial(z)
    b = law.radial(s, -z, strict=not turn_closed)
    return ((4 + 2 * a) * s + 8 - (6 + s + z) * b
            - law.column(z, z, s) - law.f(s, z, strict=row_strict)
            - (law.h(s) if retain_h else ZERO))


def finite_fixtures():
    paths = [
        wave(Q(1, 8), Q(3, 8), Q(3, 4), Q(9, 8), Q(7, 8)),
        wave(Q(3, 8), Q(5, 8), Q(1, 4), Q(5, 4), Q(5, 8)),
        wave(Q(5, 8), Q(7, 8), -Q(1, 4), Q(11, 8), Q(3, 8)),
        wave(Q(7, 8), Q(15, 16), -Q(3, 4), Q(3, 2), -Q(3, 4)),
    ]
    multi = Law([(Q(i + 1, 10), path) for i, path in enumerate(paths)])
    slow = Law([
        (Q(1, 5), slow_wave(Q(1, 10), Q(2, 5), Q(3, 4))),
        (Q(3, 10), slow_wave(Q(2, 5), Q(7, 10), Q(1, 5))),
        (Q(1, 2), slow_wave(Q(3, 4), Q(19, 20), -Q(1, 2))),
    ])
    center = wave(ZERO, ZERO, ONE, ONE, ONE)
    endpoint = Path([(ZERO, ONE), (HORIZON, ONE)])
    atoms = Law([(Q(1, 9), center)]
                + [(Q(7, 9) * w, path) for w, path in multi.paths]
                + [(Q(1, 9), endpoint)])
    return [multi, slow, atoms]


def verify_capture_identities(counts):
    laws = finite_fixtures()
    for law in laws:
        starts = {Q(i, 10) for i in range(1, 10)}
        starts.update(path.value(ZERO) for _, path in law.paths
                      if 0 < path.value(ZERO) < 1)
        for z in sorted(starts):
            end = 2 - z
            turns = {ONE + (end - 1) * Q(i, 4) for i in range(5)}
            turns.update(z+(1-z)*Q(i, 4) for i in range(5))
            # These include coalescent incoming light lines of the fixtures.
            turns.update(s for s in [Q(9, 8), Q(5, 4), Q(11, 8), Q(3, 2)]
                         if 1 <= s <= end)
            turns.update(s for s in [Q(3, 8), Q(5, 8), Q(7, 8), Q(15, 16)]
                         if z <= s < 1)
            for s in sorted(turns):
                expected = 4 * direct_cost(law, s, z)
                assert four_cost(law, s, z) == expected, (z, s, 'capture')
                counts['direct capture identities'] += 1
                if s < 1:
                    counts['early positive-turn capture identities'] += 1
                if law.f(s, z) != law.f(s, z, strict=False):
                    assert four_cost(law, s, z, row_strict=False) != expected
                    counts['strict incoming trace witnesses'] += 1
                if s == end:
                    assert law.radial(s, -z) == 1
                    if law.radial(s, -z, strict=True) < 1:
                        assert four_cost(law, s, z, turn_closed=False) != expected
                        counts['closed endpoint trace witnesses'] += 1
                if law.h(s):
                    assert s <= 1
                    assert four_cost(law, s, z, retain_h=False) != expected
                    if s < 1:
                        counts['early outgoing-row correction witnesses'] += 1
                    else:
                        counts['outgoing-atom correction witnesses'] += 1

            a, e = law.initial(z), 1 - law.radial(ONE, -z)
            flow = (end - 1) * a - (law.f(end, z) - law.f(ONE, z))
            fneg = law.column(z, ONE, end) - (end - 1) * (1 - e)
            assert flow >= 0 and fneg >= 0
            difference = (1 - z) * (a + 2) - (6 + 2 * z) * e
            difference += flow - fneg + law.h(ONE)
            assert difference == 4 * (direct_cost(law, end, z)
                                      - direct_cost(law, ONE, z))
            counts['positive M1/M2 difference identities'] += 1
            if fneg:
                assert difference + 2 * fneg != difference
                counts['nonzero negative-row flux witnesses'] += 1


def sheet(a, e, z, s):
    w0, w = 7 + z, 6 + s + z
    dp = 1 + a / 2 + e
    return 2 + a / 2 - dp * w0 * w0 / (w * w)


def verify_sheet_algebra(counts):
    for a in [Q(0), Q(1, 8), Q(1, 4), Q(1, 2)]:
        for z in [Q(i, 10) for i in range(2, 9)]:
            for d in [Q(0), Q(1, 20), Q(1, 10), Q(3, 20)]:
                l = 1 + a / 2 + d
                sbar = (1 - z) * (a + 2 + d) / (7 + z)
                if sbar < d:
                    continue
                e = sbar + (sbar - d) ** 2 / (4 * l)
                if e > 1 - a:
                    continue
                ratio = 1 + (sbar - d) / (2 * l)
                v = 1 + (7 + z) * (ratio - 1)
                dp = 1 + a / 2 + e
                assert dp == l * ratio * ratio
                assert v == 2 - z - 8 * d / (a + 2 + 2 * d)
                assert 1 <= v <= 2 - z
                assert sheet(a, e, z, ONE) == 1 - e
                assert sheet(a, e, z, v) == 1 - d
                counts['cap and explicit exit identities'] += 1

                qneg = dp * (v - 1) ** 2 / (6 + v + z)
                qneg += (e - d) * (2 - z - v)
                closed_form = (e - d) * (1 - z)
                closed_form -= (7 + z) * l * (ratio - 1) ** 2
                assert qneg == closed_form
                assert (1 - z) * (a + 2) - (6 + 2 * z) * e - qneg == 0
                assert (2 + a + 2 * d) * (2 - z - v) == 8 * d
                counts['corrected boundary and endpoint jump identities'] += 1

                for fraction in [Q(0), Q(1, 3), Q(2, 3), Q(1)]:
                    s = 1 + (v - 1) * fraction
                    w0, w = 7 + z, 6 + s + z
                    bs = 2 * dp * w0 * w0 / (w ** 3)
                    assert w * bs + 2 * sheet(a, e, z, s) == 4 + a
                    counts['inverse-square turn indifference identities'] += 1

                # An elementary sufficient cone test, including its equality edge.
                for factor in [Q(1), Q(3, 2), Q(2)]:
                    rho = 2 * dp * factor / (7 + z)
                    for ep in [Q(0), -Q(1, 10), -Q(1, 2)]:
                        for fraction in [Q(0), Q(1, 2), Q(1)]:
                            s = 1 + (v - 1) * fraction
                            w0, w = 7 + z, 6 + s + z
                            k = dp * w0 * w0
                            kp = (rho / 2 + ep) * w0 * w0 + 2 * dp * w0
                            bz = (rho * (1 - w0 * w0 / (w * w)) / 2
                                  - ep * w0 * w0 / (w * w)
                                  - 2 * dp * w0 * (s - 1) / (w ** 3))
                            assert bz >= 0
                            assert w ** 3 * bz == rho * w ** 3 / 2 - kp * w + 2 * k
                            counts['transport and cubic identities'] += 1

                # Differentiate the eliminated E(A,z) at constant terminal mass d.
                for rho in [Q(1, 4), Q(1, 2), Q(1)]:
                    sa = (1 - z) / (7 + z)
                    sz = -8 * (a + 2 + d) / (7 + z) ** 2
                    ea = sa * (1 + (sbar - d) / (2 * l))
                    ea -= (sbar - d) ** 2 / (8 * l * l)
                    ez = sz * (1 + (sbar - d) / (2 * l))
                    ep = ea * rho + ez
                    sp = sa * rho + sz
                    differentiated = sp + (sbar - d) * sp / (2 * l)
                    differentiated -= (sbar - d) ** 2 * rho / (8 * l * l)
                    assert ep == differentiated
                    w0, wv = 7 + z, 6 + v + z
                    edge_bz = (rho * (1 - w0 * w0 / (wv * wv)) / 2
                               - ep * w0 * w0 / (wv * wv)
                               - 2 * dp * w0 * (v - 1) / (wv ** 3))
                    edge_bs = 2 * dp * w0 * w0 / (wv ** 3)
                    vp = -1 + 8 * d * rho / (a + 2 + 2 * d) ** 2
                    assert edge_bz == -edge_bs * vp
                    counts['eliminated E and exit cone derivatives'] += 1


def verify_flux_cap_algebra(counts):
    """Independently integrate rows with nonzero affine other-sheet flux.

    These are exact local algebra fixtures, not globally realized CDFs.
    The active-row Laurent polynomial has no W^-1 term, so every integral
    below remains rational and can be checked without numerical quadrature.
    """
    for a in [Q(0), Q(1, 4), Q(1, 2)]:
        for z in [Q(1, 4), Q(1, 2), Q(3, 4)]:
            for fraction in [Q(1, 4), Q(1, 2), Q(3, 4)]:
                end = 2-z
                v = 1+(end-1)*fraction
                w0, wv = 7+z, 6+v+z
                for j0, j1 in [(Q(0), Q(0)), (Q(1, 16), Q(0)),
                               (Q(0), Q(1, 8)), (Q(1, 16), Q(1, 8))]:
                    # J(s)=j0+j1*(s-1); choose the mass from the independent
                    # cap-to-endpoint cost integral, then recover the row.
                    jcap = j0*(end-v)+j1*((end-1)**2-(v-1)**2)/2
                    d = ((a+2)*(end-v)+jcap)/(8-2*(end-v))
                    l = 1+a/2+d
                    tj = j0*(wv*wv-w0*w0)/2
                    tj += j1*((wv**3-w0**3)/3-w0*(wv*wv-w0*w0)/2)
                    dp = (l*wv*wv+tj)/(w0*w0)
                    e = dp-1-a/2
                    assert 0 <= d <= e <= 1-a

                    # Expand B(W) directly; integrate each Laurent monomial.
                    tj_constant = -j0*w0*w0/2+j1*w0**3/6
                    coefficients = {
                        -2: -dp*w0*w0+tj_constant,
                        0: 2+a/2+j0/2-j1*w0/2,
                        1: j1/3,
                    }
                    def value(w):
                        return sum(coef*w**power for power, coef in coefficients.items())
                    def derivative(w):
                        return sum(power*coef*w**(power-1)
                                   for power, coef in coefficients.items())
                    integrated = sum(coef*(wv**(power+1)-w0**(power+1))/(power+1)
                                     for power, coef in coefficients.items())
                    assert value(w0) == 1-e
                    assert value(wv) == 1-d
                    qneg = integrated-(v-1)*(1-e)+(e-d)*(end-v)
                    jactive = j0*(v-1)+j1*(v-1)**2/2
                    assert qneg == 2*l*wv-2*dp*w0+8*(dp-l)+jactive
                    qlow = j0*(end-1)+j1*(end-1)**2/2
                    assert (1-z)*(a+2)-(6+2*z)*e+qlow-qneg == 0
                    assert 2*l*(end-v)+jcap == 8*d
                    counts['nonzero-flux cap and endpoint identities'] += 1
                    for sample in [Q(0), Q(1, 3), Q(2, 3), Q(1)]:
                        s = 1+(v-1)*sample
                        w = 6+s+z
                        assert w*derivative(w)+2*value(w) == 4+a+j0+j1*(s-1)
                        counts['nonzero-flux turn indifference identities'] += 1


def main():
    counts = Counter()
    verify_capture_identities(counts)
    verify_sheet_algebra(counts)
    verify_flux_cap_algebra(counts)
    for key in ['strict incoming trace witnesses', 'closed endpoint trace witnesses',
                'outgoing-atom correction witnesses', 'nonzero negative-row flux witnesses']:
        assert counts[key] > 0, key
    print(f'PASS: {sum(counts.values())} exact positive-CDF sheet checks')
    for key, value in counts.items():
        print(f'  {key}: {value}')
    print('Scope: exact identities and local sheet algebra; no matched global law')


if __name__ == '__main__':
    main()
