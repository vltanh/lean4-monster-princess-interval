#!/usr/bin/env python3
"""Independent exact full-CDF Bellman actions, including interior atoms."""
from bisect import bisect_right
from fractions import Fraction as Q

from verify_general_center import RankLaw, fixtures as continuum_fixtures
from signed_bellman import SignedLegActions, append_endpoint_tail, capture_records


class AtomicPathLaw(RankLaw):
    """A polygonal radial path and its reflection, each with probability 1/2.

    This fixture deliberately permits entire incoming/coinciding/center
    atoms; its strict CDF is not inferred from its closed radial CDF.
    """
    def __init__(self, vertices):
        self.vertices = [(Q(t), Q(x)) for t, x in vertices]
        self.zero, self.one = Q(0), Q(1)
        self.endpoint_mass, self.tol, self.exact = Q(0), Q(0), True
        self.times = [p[0] for p in self.vertices]
        assert self.vertices[0][0] == 0 and self.vertices[-1][1] == 1
        assert self.vertices[-1][0] <= 2
        assert all(abs(y-x) <= e-t for (t, x), (e, y)
                   in zip(self.vertices, self.vertices[1:]))

    def p_line(self, t):
        if t >= self.times[-1]:
            return Q(0), Q(1)
        i = max(bisect_right(self.times, t)-1, 0)
        (start, x), (end, y) = self.vertices[i:i+2]
        slope = (y-x)/(end-start)
        return slope, x-slope*start

    def p(self, t):
        slope, constant = self.p_line(t)
        return slope*t+constant

    def radial(self, t, r):
        return Q(int(self.p(t) <= r))

    def cdf_sides(self, t, x):
        p = self.p(t)
        return (Q(int(-p < x)+int(p < x), 2),
                Q(int(-p <= x)+int(p <= x), 2))

    def _cdf_lines(self, radial, region):
        strict, closed = region
        return (Q(0), strict), (Q(0), closed)

    def _radial_cells(self, start, end, velocity, intercept):
        cuts = {start, end, *[t for t in self.times if start < t < end]}
        if velocity:
            zero = -intercept/velocity
            if start < zero < end:
                cuts.add(zero)
        cuts = sorted(cuts)
        for lo, hi in zip(cuts, cuts[1:]):
            slope, constant = self.p_line((lo+hi)/2)
            local = {lo, hi}
            for sign in [-1, 1]:
                denominator = velocity-sign*slope
                if denominator:
                    crossing = (sign*constant-intercept)/denominator
                    if lo < crossing < hi:
                        local.add(crossing)
            local = sorted(local)
            for left, right in zip(local, local[1:]):
                middle = (left+right)/2
                x = velocity*middle+intercept
                yield left, right, (Q(0), self.radial(middle, abs(x))), self.cdf_sides(middle, x)


def fixtures():
    return continuum_fixtures()+[
        AtomicPathLaw([(0, Q(1, 4)), (Q(1, 4), 0), (1, 0), (2, 1)]),
        AtomicPathLaw([(0, Q(1, 4)), (Q(3, 8), Q(5, 8)),
                       (Q(3, 4), Q(1, 4)), (Q(3, 2), 1)]),
        AtomicPathLaw([(0, 1)]),
    ]


def prefixes():
    return [
        [(Q(0), x)] for x in [Q(0), Q(1, 4), Q(2, 5), Q(-3, 5), Q(1), Q(-1)]
    ]+[
        [(Q(0), Q(3, 10)), (Q(2, 5), Q(-1, 10))],
        [(Q(0), Q(-1, 5)), (Q(1, 2), Q(3, 10)), (Q(9, 10), Q(-1, 10))],
        [(Q(0), Q(0)), (Q(3, 10), Q(3, 10)), (Q(3, 5), Q(0)),
         (Q(9, 10), Q(0))],
        [(Q(0), Q(1)), (Q(1), Q(1))],
        [(Q(0), Q(-1)), (Q(1), Q(-1))],
        [(Q(0), Q(1, 2)), (Q(3, 2), Q(1, 2))],
        [(Q(0), Q(0)), (Q(3, 2), Q(0))],
    ]


def main():
    counts = dict(leg_cost=0, record_update=0, endpoint_tail=0, concavity=0,
                  atomic_phase=0)
    laws = fixtures()
    for law in laws:
        action = SignedLegActions(law)
        for prefix in prefixes():
            t, x = prefix[-1]
            old = law.payoff(prefix, require_complete=False)
            old_captured = old.value-t*old.survival
            lower, upper = capture_records(law, prefix)
            assert old.survival == 1-upper+lower
            strict, closed = law.cdf_sides(t, x)
            assert lower <= strict <= closed <= upper
            for velocity in [-1, 1]:
                duration = min(2-t, 1-velocity*x)
                if duration == 0:
                    continue
                for fraction in [Q(1, 3), Q(2, 3), Q(1)]:
                    e = t+duration*fraction
                    value, y, newlower, newupper = action.leg(t, x, e, lower, upper, velocity)
                    route = prefix+[(e, y)]
                    direct = law.payoff(route, require_complete=False)
                    new_captured = direct.value-e*direct.survival
                    assert value == new_captured-old_captured, (t, x, e, velocity,
                                                               value, new_captured-old_captured)
                    counts['leg_cost'] += 1
                    assert (newlower, newupper) == capture_records(law, route)
                    counts['record_update'] += 1
            # Wait to the actual endpoint absorption horizon; the boundary
            # cost is then exact even for a positive atom arriving at time 2.
            at_two = prefix+[(Q(2), x)]
            partial = law.payoff(at_two, require_complete=False)
            captured = partial.value-2*partial.survival
            lo2, hi2 = capture_records(law, at_two)
            completed = list(at_two)
            append_endpoint_tail(completed, Q(2), x, lo2, hi2)
            predicted = captured+action.endpoint_tail(Q(2), x, lo2, hi2)
            assert predicted == law.payoff(completed).value
            counts['endpoint_tail'] += 1
        for t, x in [(Q(1, 5), Q(0)), (Q(3, 5), Q(1, 4)),
                     (Q(11, 10), Q(-1, 4))]:
            strict, closed = law.cdf_sides(t, x)
            vectors = [(strict*a, closed+(1-closed)*b)
                       for a, b in [(Q(0), Q(1)), (Q(1), Q(0)),
                                    (Q(1, 5), Q(1, 3)), (Q(4, 5), Q(2, 3))]]
            for velocity in [-1, 1]:
                e = t+min(2-t, 1-velocity*x)/2
                def rhs(vector):
                    value, y, lower, upper = action.leg(t, x, e, *vector, velocity)
                    return value+action.endpoint_tail(e, y, lower, upper)
                for left, right in zip(vectors, vectors[1:]+vectors[:1]):
                    weight = Q(2, 5)
                    middle = tuple(weight*a+(1-weight)*b for a, b in zip(left, right))
                    assert rhs(middle) >= weight*rhs(left)+(1-weight)*rhs(right)
                    counts['concavity'] += 1
    # Deliberate first-touch phases, with exact values rather than a limit.
    center_atom, incoming_atom, endpoints = laws[-3:]
    assert center_atom.cdf_sides(Q(1, 2), Q(0)) == (Q(0), Q(1))
    assert center_atom.payoff([(Q(0), Q(1)), (Q(2), Q(-1))]).value == 1
    counts['atomic_phase'] += 2
    assert incoming_atom.cdf_sides(Q(1, 2), Q(1, 2)) == (Q(1, 2), Q(1))
    assert incoming_atom.cdf_sides(Q(1, 2), Q(-1, 2)) == (Q(0), Q(1, 2))
    counts['atomic_phase'] += 2
    assert endpoints.cdf_sides(Q(0), Q(1)) == (Q(1, 2), Q(1))
    assert endpoints.payoff([(Q(0), Q(1)), (Q(2), Q(-1))]).value == 1
    counts['atomic_phase'] += 2
    print(f'PASS: {sum(counts.values())} exact full-signed-CDF checks')
    for key, count in counts.items():
        print(f'  {key}: {count}')
    print('PASS: strict left / closed right first touch, including entire interior atoms')
    print('PASS: center waits, endpoint starts, and positive mass absorbed exactly at time two')
    print('PASS: slow-speed and multi-wave continuum laws, plus joint frontier concavity')
    print('Scope: global action/certificate identities; no instantiated equilibrium potential')


if __name__ == '__main__':
    main()
