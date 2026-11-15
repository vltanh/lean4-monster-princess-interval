#!/usr/bin/env python3
"""Exact source corrections for a general curved initial terminal phase.

The tail's first characteristic graph may have several speeds.  Direct
first intersections, rather than the old ordinary-wave formulas, verify
the two additional sources.  This is an identity test, not a construction
of a matched law.  Atomic initial and incoming equality rows are avoided;
the continuous statement uses the strict/closed conventions in the notes.
"""
from collections import Counter
from fractions import Fraction as Q

from verify_positive_cdf_sheet import (HORIZON, Law, Path, direct_cost,
                                       first_capture, wave)


class InitialGraph:
    """Initial deficit graph (eta=1-U, y=1+V), then -1/+1 legs."""

    def __init__(self, x, d, h, shape, width_denominator):
        self.x, self.d, self.h = x, d, h
        self.b = x + (x-h)/width_denominator
        assert 0 < h < x < self.b < d < 1
        self.graph = tuple((x-(x-h)*s, x+(self.b-x)*t)
                           for s, t in shape)
        assert self.graph[0] == (x, x)
        assert self.graph[-1] == (h, self.b)
        for (eta0, y0), (eta1, y1) in zip(self.graph, self.graph[1:]):
            assert eta0 > eta1 and y1 >= y0
        points = list(self.graph) + [(h, d), (-d, d)]
        knots = [((y-eta)/2, 1-(y+eta)/2) for eta, y in points]
        knots.append((HORIZON, Q(1)))
        self.path = Path(knots)

    def eta_at_y(self, y):
        assert y > self.x
        if y >= self.b:
            return self.h
        for (e0, y0), (e1, y1) in zip(self.graph, self.graph[1:]):
            if y0 <= y <= y1 and y1 > y0:
                return e0+(e1-e0)*(y-y0)/(y1-y0)
        raise AssertionError(('missing initial V', y, self.graph))

    def y_at_eta(self, eta):
        assert self.h <= eta <= self.x
        for (e0, y0), (e1, y1) in zip(self.graph, self.graph[1:]):
            if e1 <= eta <= e0:
                return y0+(y1-y0)*(e0-eta)/(e0-e1)
        raise AssertionError(('missing initial U', eta, self.graph))


class CurvedWholePrefix(InitialGraph):
    """Both early and incoming motion curve; there is no constant-U leg."""

    def __init__(self, x, d, bend):
        self.x, self.d, self.h, self.b = x, d, Q(0), d
        self.graph = (
            (x, x), (x/2, Q(101, 100)*x),
            (x/8, Q(21, 20)*x), (x/16, bend*d),
            (x/40, (1+bend)*d/2), (Q(0), d),
        )
        for (eta0, y0), (eta1, y1) in zip(self.graph, self.graph[1:]):
            assert eta0 > eta1 and y1 > y0
        points = list(self.graph)+[(-d, d)]
        knots = [((y-eta)/2, 1-(y+eta)/2) for eta, y in points]
        knots.append((HORIZON, Q(1)))
        self.path = Path(knots)


def fixture(scale, shape, width_denominator):
    low = [wave(Q(1, 5), Q(4, 5), Q(4, 5), 1+Q(1, 10000), Q(9, 10)),
           wave(Q(1, 2), Q(19, 20), Q(1, 2), 1+Q(1, 5000), Q(3, 5)),
           wave(Q(4, 5), 1-Q(1, 10**12), -Q(2, 5), 1, -Q(2, 5))]
    weighted = [(Q(3, 10), path) for path in low]
    tails = []
    for d in [Q(1, 10), Q(1, 20), Q(1, 40)]:
        x = d*d/16
        h = scale*x*x/16
        graph = InitialGraph(x, d, h, shape, width_denominator)
        tails.append((Q(1, 30), graph))
        weighted.append((Q(1, 30), graph.path))
    return (Law(weighted), Law([(Q(1, 3), p) for p in low]),
            Q(9, 10), tails)


def correction_j(tails, y):
    return sum((w*(g.eta_at_y(y)-g.h)
                for w, g in tails if g.x < y < g.b), Q(0))


def correction_k(tails, eta):
    return sum((w*(g.y_at_eta(eta)-g.x)
                for w, g in tails if g.h < eta < g.x), Q(0))


def inward_cost(law, a, v, second_u=Q(1)):
    route = [(Q(0), a), ((a+v)/2, (a-v)/2),
             ((second_u+v)/2, (second_u-v)/2),
             (second_u+1, Q(-1)), (second_u+3, Q(1))]
    return sum((weight*(first_capture(path, route, 1)
                        +first_capture(path, route, -1))/2
                for weight, path in law.paths), Q(0))


def verify_first_turn_corners(law, low, q0, tails, counts):
    """No ell equality is assumed: compare CI directly with Cell."""
    rt = sum(weight for weight, _ in tails)
    n0 = q0*low.integrate(1, -1, 1, horizontal=True, strict=True)
    tail = Law([(weight/rt, graph.path) for weight, graph in tails])
    for _, graph in tails:
        x, y = graph.h, graph.b
        a, v = 1-x, -1+y
        r = sum((weight for weight, g in tails if g.x < x), Q(0))
        i = sum((weight for weight, g in tails if g.x <= graph.x), Q(0))
        e = sum((weight for weight, g in tails if g.d < y), Q(0))
        # At the incoming corner the horizontal strict trace includes
        # the corresponding upper-deficit atom in D.
        assert rt*(1-tail.radial(a, v, strict=True)) == i
        omega = n0-q0*x-q0*low.integrate(a, -a, a,
                                        horizontal=True, strict=True)
        hinge = tail.integrate(v, a, 1, horizontal=False,
                               transform=lambda c: max(Q(0), r-rt*(1-c)))
        assert 0 <= hinge <= x*max(Q(0), r-e)
        expected = x*(3+2*r-i)+omega-(8-y)*max(Q(0), r-e)-hinge
        actual = 4*(inward_cost(law, a, v)-direct_cost(law, 2+a, -a))
        assert actual == expected, ('initial corner', x, y, actual, expected)
        counts['initial-corner CI minus Cell'] += 1
        if e >= r:
            assert actual > 0
            counts['positive corner slack beyond B=A'] += 1


def verify_fully_curved_incoming(counts):
    """The field moments do not need the conditional incoming-cap class."""
    for bend in [Q(1, 4), Q(1, 3), Q(1, 2), Q(2, 3)]:
        _, low, q0, _ = fixture(Q(1), [(Q(0), Q(0)), (Q(1), Q(1))], Q(4))
        tails = [(Q(1, 30), CurvedWholePrefix(d*d/16, d, bend))
                 for d in [Q(1, 10), Q(1, 20), Q(1, 40)]]
        law = Law([(q0*w, path) for w, path in low.paths]
                  + [(w, g.path) for w, g in tails])
        rt = 1-q0
        tail = Law([(w/rt, g.path) for w, g in tails])
        n0 = q0*low.integrate(1, -1, 1, horizontal=True, strict=True)
        endpoint = direct_cost(law, Q(1), Q(1))
        moment = sum((w*g.d for w, g in tails), Q(0))
        assert 4*endpoint == 4+n0+moment
        counts['fully curved endpoint moment'] += 1
        probes = {Q(k, 1003) for k in range(1, 90)}
        for _, g in tails:
            probes.update(g.x*Q(k, 7) for k in range(1, 7))
            probes.update(g.x+(g.d-g.x)*Q(k, 7) for k in range(1, 7))
        probes -= {g.x for _, g in tails}
        for y in sorted(probes):
            z = 1-y
            r = sum((w for w, g in tails if g.x < y), Q(0))
            e = sum((w for w, g in tails if g.d < y), Q(0))
            dpartial = sum((w*g.d for w, g in tails if g.x < y), Q(0))
            post = (q0*y+q0*low.integrate(1+y, -1+y, 1,
                                         horizontal=True, strict=True)-n0)
            omega = (n0-q0*y-q0*low.integrate(z, -z, z,
                                             horizontal=True, strict=True))
            cf = direct_cost(law, 2-z, z)
            cg = direct_cost(law, Q(1), z)
            cell = direct_cost(law, 2+z, -z)
            column = y*rt-rt*tail.integrate(-1+y, 1-y, 1, horizontal=False)
            dmax = max(g.d for _, g in tails)
            row = ((dmax-y)*rt-rt*tail.integrate(z, -z, -1+dmax,
                                                horizontal=True, strict=True))
            eint = dmax*rt-moment
            assert 4*(cf-cg) == y*(3-r)+post-(8-2*y)*e
            assert 4*(cg-endpoint) == (8-y)*e+column-dpartial
            assert 4*(cell-endpoint) == (8-2*y)*r-3*y-omega-row+eint
            # The h=0 characteristic graph also recovers the two general
            # corrections, although the h-contraction does not apply.
            ji, ki = correction_j(tails, y), correction_k(tails, y)
            assert ji == y*r-column
            jfull = sum((w*(g.d-g.x) for w, g in tails), Q(0))
            s = sum((w*max(Q(0), y-g.x) for w, g in tails), Q(0))
            assert 4*(cell-endpoint) == (8-2*y)*r+s-3*y-omega-jfull+ki
            for label in ['fully curved positive difference',
                          'fully curved positive M2 column',
                          'fully curved negative M1 row',
                          'fully curved initial column source',
                          'fully curved negative correction']:
                counts[label] += 1


def verify_ridge_source(counts):
    """Move the second I turn to a real incoming/outgoing ridge."""
    shapes = [
        [(Q(0), Q(0)), (Q(1), Q(1))],
        [(Q(0), Q(0)), (Q(1, 2), Q(1, 4)), (Q(1), Q(1))],
    ]
    for scale in [Q(1, 2), Q(1), Q(3, 2)]:
        for shape in shapes:
            law, low, q0, tails = fixture(scale, shape, Q(4))
            n0 = q0*low.integrate(1, -1, 1, horizontal=True, strict=True)
            endpoint = direct_cost(law, Q(1), Q(1))
            for x in [Q(1, 10000), Q(1, 3000), Q(1, 200), Q(1, 50)]:
                a = 1-x
                r = sum((weight for weight, g in tails if g.x < x), Q(0))
                for y in sorted({x, 2*x, Q(3, 100), Q(3, 50), Q(2, 25)}):
                    if y < x:
                        continue
                    e = sum((weight for weight, g in tails if g.d < y), Q(0))
                    if e >= r:
                        continue
                    # Atomic analogue of h(d^{-1}(y)): every higher
                    # initial rank with d>y has completed its initial arc.
                    eligible = [g for _, g in tails if g.d > y]
                    k = min(g.h for g in eligible)
                    assert all(g.b < y for g in eligible if g.h == k)
                    s, v = 1-k, -1+y
                    D = 1-law.radial(a, v, strict=True)
                    assert D <= 1-q0
                    assert law.radial(s, v) == law.radial(1, v) == 1-e
                    omega = (n0-q0*k-q0*low.integrate(s, -s, s,
                                                    horizontal=True, strict=True))
                    correction = k*(3-D+2*e)+omega
                    actual = 4*(inward_cost(law, a, v)-inward_cost(law, a, v, s))
                    assert actual == correction > 0
                    counts['free second-turn ridge correction'] += 1
                    if y == x:
                        assert D == r
                        cf = direct_cost(law, 2-a, a)
                        cg = direct_cost(law, s, a)
                        post = (q0*x+q0*low.integrate(1+x, -1+x, 1,
                                            horizontal=True, strict=True)-n0)
                        assert 4*(cf-cg) == x*(3-r)+post-(8-2*x)*e+correction
                        assert cg == inward_cost(law, a, -a, s)
                        counts['moving positive M2 difference'] += 1


def verify_general_second_turn_source(counts):
    """No cap or ridge: retain every row/column term for a free second U."""
    fixtures = []
    shape = [(Q(0), Q(0)), (Q(1, 2), Q(1, 4)), (Q(1), Q(1))]
    fixtures.append(fixture(Q(1), shape, Q(4)))
    fixtures.append(fixture(Q(10000), shape, Q(4)))
    _, low, q0, _ = fixtures[0]
    tails = [(Q(1, 30), CurvedWholePrefix(d*d/16, d, Q(1, 3)))
             for d in [Q(1, 10), Q(1, 20), Q(1, 40)]]
    whole = Law([(q0*w, path) for w, path in low.paths]
                +[(w, g.path) for w, g in tails])
    fixtures.append((whole, low, q0, tails))
    for law, low, q0, tails in fixtures:
        rt = 1-q0
        tail = Law([(weight/rt, g.path) for weight, g in tails])
        n0 = q0*low.integrate(1, -1, 1, horizontal=True, strict=True)
        dmax = max(g.d for _, g in tails)
        for x in [Q(1, 10000), Q(1, 3000), Q(1, 200), Q(1, 50)]:
            a = 1-x
            r = sum((weight for weight, g in tails if g.x < x), Q(0))
            for y in sorted({x, 2*x, Q(3, 100), Q(3, 50), Q(2, 25)}):
                if y < x:
                    continue
                v = -1+y
                D0 = 1-law.radial(a, v, strict=True)
                assert D0 <= rt
                def F(z):
                    return tail.integrate(1-z, v, -1+dmax,
                        horizontal=True, strict=True,
                        transform=lambda C: max(Q(0), rt*(1-C)-D0))
                def m(z):
                    return min(r, rt*(1-tail.radial(1-z, v)))
                baseline = inward_cost(law, a, v)
                for fraction in [Q(0), Q(1, 7), Q(1, 2), Q(6, 7), Q(1)]:
                    k = fraction*x
                    s = 1-k
                    omega = (n0-q0*k-q0*low.integrate(s, -s, s,
                                                    horizontal=True, strict=True))
                    im = tail.integrate(v, s, 1, horizontal=False,
                                        transform=lambda C: min(r, rt*(1-C)))
                    correction = (k*(3-D0)+omega+F(k)-F(Q(0))+im
                                  -(8-y-k)*m(k)+(8-y)*m(Q(0)))
                    actual = 4*(baseline-inward_cost(law, a, v, s))
                    assert actual == correction, ('free second turn', x, y, k,
                                                   actual, correction)
                    counts['general free-second source identity'] += 1
                    if k == x:
                        assert inward_cost(law, a, v, s) == direct_cost(law, 2+a, -a)
                        counts['collapsed second leg equals negative M1'] += 1
                    if y == x:
                        post = (q0*x+q0*low.integrate(1+x, -1+x, 1,
                                            horizontal=True, strict=True)-n0)
                        e = sum((weight for weight, g in tails if g.d < x), Q(0))
                        assert 4*(direct_cost(law, 2-a, a)-direct_cost(law, s, a)) \
                            == x*(3-r)+post-(8-2*x)*e+correction
                        counts['general moving positive M2 identity'] += 1


def main():
    counts = Counter()
    shapes = [
        [(Q(0), Q(0)), (Q(1), Q(1))],
        [(Q(0), Q(0)), (Q(1, 2), Q(1, 4)), (Q(1), Q(1))],
        [(Q(0), Q(0)), (Q(1, 3), Q(1, 2)), (Q(1), Q(1))],
        # The identities also apply to this forbidden-for-matching unit
        # run.  They do not certify its inward response inequalities.
        [(Q(0), Q(0)), (Q(1, 3), Q(0)),
         (Q(2, 3), Q(1, 4)), (Q(1), Q(1))],
    ]
    for scale in [Q(1, 2), Q(1), Q(3, 2)]:
        for shape in shapes:
            for width_denominator in [Q(4), Q(7)]:
                law, low, q0, tails = fixture(scale, shape, width_denominator)
                verify_first_turn_corners(law, low, q0, tails, counts)
                rt = sum(weight for weight, _ in tails)
                tail = Law([(weight/rt, graph.path) for weight, graph in tails])
                n0 = q0*low.integrate(1, -1, 1, horizontal=True, strict=True)
                endpoint = direct_cost(law, Q(1), Q(1))
                moment = sum((w*g.d for w, g in tails), Q(0))
                assert 4*endpoint == 4+n0+moment
                counts['endpoint moment'] += 1
                epsilons = {Q(k, 1003) for k in range(1, 90)}
                for _, g in tails:
                    epsilons.update(g.x+(g.b-g.x)*Q(k, 7) for k in range(1, 7))
                    epsilons.update(g.h+(g.x-g.h)*Q(k, 7) for k in range(1, 7))
                hs = sorted(g.h for _, g in tails)
                epsilons.update([hs[0]/2, (hs[0]+hs[1])/2,
                                (hs[1]+hs[2])/2, 2*hs[2]])
                excluded = {v for _, g in tails for v in [g.x, g.h]}
                for e in sorted(epsilons-excluded):
                    z = 1-e
                    r = sum((w for w, g in tails if g.x < e), Q(0))
                    E = sum((w for w, g in tails if g.d < e), Q(0))
                    P = sum((w*(g.d+g.h) for w, g in tails if g.x < e), Q(0))
                    delayed = sum((w*g.h for w, g in tails if g.d < e), Q(0))
                    Qpost = (q0*e+q0*low.integrate(1+e, -1+e, 1,
                                horizontal=True, strict=True)-n0)
                    omega = (n0-q0*e-q0*low.integrate(1-e, -1+e, 1-e,
                                horizontal=True, strict=True))
                    cf = direct_cost(law, 2-z, z)
                    cg = direct_cost(law, Q(1), z)
                    cell = direct_cost(law, 2+z, -z)
                    ji = correction_j(tails, e)
                    ki = correction_k(tails, e)
                    assert ji >= 0 and ki >= 0
                    assert 4*(cf-endpoint) == 3*e+Qpost+e*E+delayed-P-ji
                    assert 4*(cf-cg) == e*(3-r)+Qpost-(8-2*e)*E
                    J = sum((w*(g.d-g.x) for w, g in tails if g.h < e), Q(0))
                    S = sum((w*max(Q(0), e-g.x) for w, g in tails), Q(0))
                    assert 4*(cell-endpoint) == (8-2*e)*r+S-3*e-omega-J+ki
                    column = e*rt-rt*tail.integrate(-1+e, 1-e, 1,
                                                    horizontal=False)
                    dpartial = sum((w*g.d for w, g in tails if g.x < e), Q(0))
                    hpartial = sum((w*g.h for w, g in tails if g.x < e), Q(0))
                    assert ji == e*r-column+delayed-hpartial
                    assert 4*(cg-endpoint) == (8-e)*E+column-dpartial
                    dmax = max(g.d for _, g in tails)
                    row = ((dmax-e)*rt-rt*tail.integrate(1-e, -1+e, -1+dmax,
                                             horizontal=True, strict=True))
                    eint = dmax*rt-moment
                    assert 4*(cell-endpoint) == (8-2*e)*r-3*e-omega-row+eint
                    counts['positive M1 corrected difference'] += 1
                    counts['unchanged positive M1/M2 difference'] += 1
                    counts['negative M1 corrected difference'] += 1
                    counts['positive source as a CDF column moment'] += 1
                    counts['positive M2 column identity'] += 1
                    counts['negative M1 row identity'] += 1
                    if ji:
                        counts['nonzero initial positive source'] += 1
                    if ki:
                        counts['nonzero initial negative source'] += 1
                    if Qpost and omega:
                        counts['simultaneous low post and prefix sources'] += 1
    # A wider incoming offset puts actual high initial ranks above some
    # first-turn starts, so the corner formula is also checked with its
    # positive-part terms present.
    for shape in shapes:
        for width_denominator in [Q(4), Q(7)]:
            law, low, q0, tails = fixture(Q(10000), shape, width_denominator)
            verify_first_turn_corners(law, low, q0, tails, counts)
    verify_fully_curved_incoming(counts)
    verify_ridge_source(counts)
    verify_general_second_turn_source(counts)
    print('PASS:', sum(counts.values()), 'exact curved-terminal source checks')
    for label, n in counts.items():
        print(' ', label+':', n)
    print('Scope: source identities only; no active-I solution or equilibrium claim')


if __name__ == '__main__':
    main()
