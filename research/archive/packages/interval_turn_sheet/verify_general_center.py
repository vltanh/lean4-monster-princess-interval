#!/usr/bin/env python3
"""Exact general center actions, including slow outward and multi-wave laws."""
from fractions import Fraction as Q
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT/'packages/interval_continuous_rank'))
from continuous_rank import MultiLegRankLaw, RankLaw
from general_center_bellman import (GeneralCenterActions, append_endpoint_completion,
                                    append_general_triangle, record_frontiers)


class SlowWaveRankLaw(RankLaw):
    """An exact non-unit-speed fixture; its CDF is affine on line cells."""
    def __init__(self, q, a, u, c, speeds, endpoint_mass=0):
        super().__init__(q, a, u, c, endpoint_mass=endpoint_mass)
        self.outward_speed, self.inward_speed, self.final_speed = map(Q, speeds)
        assert all(0 < speed <= 1 for speed in speeds)
        assert max(self.c)+1/self.final_speed < 2

    def radial(self, t, r):
        return min(max(self.A(r-self.outward_speed*t),
                       self.B(r+self.inward_speed*t)),
                   self.D(t-r/self.final_speed))

    def position(self, t, q):
        a, u, c = self.parameters(q)
        return min(self.one, max(self.zero,
                   min(a+self.outward_speed*t, u-self.inward_speed*t),
                   self.final_speed*(t-c)))

    def _components(self, r_velocity, r_intercept):
        return ((self.A, (r_velocity-self.outward_speed, r_intercept)),
                (self.B, (r_velocity+self.inward_speed, r_intercept)),
                (self.D, (1-r_velocity/self.final_speed,
                          -r_intercept/self.final_speed)))


def fixtures():
    return [
        SlowWaveRankLaw([0, 1], [Q(1, 20), Q(7, 10)],
                        [Q(3, 20), Q(9, 10)], [Q(3, 5), Q(-2, 5)],
                        [Q(1, 2), Q(3, 4), Q(3, 4)]),
        SlowWaveRankLaw([0, Q(2, 5), 1],
                        [Q(1, 20), Q(1, 2), Q(4, 5)],
                        [Q(1, 10), Q(3, 5), Q(19, 20)],
                        [Q(2, 5), Q(1, 20), Q(-3, 5)],
                        [Q(1), Q(1, 2), Q(2, 3)], endpoint_mass=Q(1, 13)),
        MultiLegRankLaw([0, 1], [Q(1, 10), Q(2, 5)],
                        [[Q(1, 5), Q(1, 2)], [Q(4, 5), Q(11, 10)]],
                        [[Q(2, 5), Q(0)], [Q(9, 10), Q(3, 5)]],
                        endpoint_mass=Q(1, 11)),
        MultiLegRankLaw([0, 1], [Q(1, 10), Q(4, 5)],
                        [[Q(1, 5), Q(9, 10)], [Q(19, 20), Q(11, 10)],
                         [Q(6, 5), Q(7, 5)]],
                        [[Q(1, 10), Q(-1, 2)], [Q(3, 5), Q(1, 5)],
                         [Q(19, 20), Q(3, 5)]]),
    ]


def prefixes():
    result = [[(Q(0), Q(0))]]
    result += [[(Q(0), z), (z, Q(0))]
               for z in [Q(1, 10), Q(7, 20), Q(3, 5), Q(17, 20)]]
    result += [
        [(Q(0), Q(0)), (Q(1, 5), Q(1, 5)), (Q(2, 5), Q(0)),
         (Q(11, 20), Q(-3, 20)), (Q(7, 10), Q(0))],
        [(Q(0), Q(3, 10)), (Q(3, 10), Q(0)), (Q(1, 2), Q(0)),
         (Q(13, 20), Q(3, 20)), (Q(4, 5), Q(0))],
        [(Q(0), Q(0)), (Q(9, 10), Q(0))],
    ]
    return result


def main():
    counts = dict(sweep=0, terminal=0, early=0, wait=0, frontier=0, concavity=0)
    laws = fixtures()
    slow = GeneralCenterActions(laws[0])
    assert slow.center(Q(3, 5)) == 0
    assert slow.radial(Q(4, 5), Q(3, 5)) > 0
    for law in laws:
        action = GeneralCenterActions(law)
        for prefix in prefixes():
            t = prefix[-1][0]
            old = law.payoff(prefix, require_complete=False)
            captured = old.value-t*old.survival
            plus, minus = record_frontiers(law, prefix)
            assert old.survival == 1-(plus+minus)/2
            assert min(plus, minus) >= action.center(t)
            for sign in [-1, 1]:
                route = prefix+[(t+1, sign), (t+3, -sign)]
                predicted = captured+action.sweep(t, plus, minus, sign)
                assert predicted == law.payoff(route).value
                counts['sweep'] += 1
                for fraction in [Q(0), Q(1, 3), Q(2, 3), Q(1)]:
                    e = 1+(t+1)*fraction
                    route = list(prefix)
                    append_general_triangle(route, t, e, sign)
                    value, newplus, newminus = action.triangle(t, e, plus, minus, sign)
                    gotplus, gotminus = record_frontiers(law, route)
                    assert (newplus, newminus) == (gotplus, gotminus)
                    counts['frontier'] += 1
                    append_endpoint_completion(route, e, newplus, newminus)
                    predicted = captured+value+action.endpoint(e, newplus, newminus)
                    actual = law.payoff(route).value
                    assert predicted == actual, ('terminal', t, e, sign, predicted, actual)
                    counts['terminal'] += 1
                    if e == t+2:
                        assert (value+action.endpoint(e, newplus, newminus)
                                == action.sweep(t, plus, minus, sign))
                for fraction in [Q(1, 3), Q(2, 3)]:
                    e = t+(1-t)*fraction
                    route = list(prefix)
                    append_general_triangle(route, t, e, sign)
                    value, newplus, newminus = action.triangle(t, e, plus, minus, sign)
                    assert (newplus, newminus) == record_frontiers(law, route)
                    counts['frontier'] += 1
                    f = 1+(e+1)/2
                    append_general_triangle(route, e, f, -sign)
                    second, finalplus, finalminus = action.triangle(
                        e, f, newplus, newminus, -sign)
                    append_endpoint_completion(route, f, finalplus, finalminus)
                    predicted = (captured+value+second
                                 +action.endpoint(f, finalplus, finalminus))
                    assert predicted == law.payoff(route).value
                    counts['early'] += 1
            for e in [(t+1)/2, Q(1)]:
                route = list(prefix)+[(e, Q(0))]
                value, newplus, newminus = action.wait(t, e, plus, minus)
                assert (newplus, newminus) == record_frontiers(law, route)
                counts['frontier'] += 1
                f = 1+(e+1)/2
                append_general_triangle(route, e, f, 1)
                second, finalplus, finalminus = action.triangle(e, f, newplus, newminus, 1)
                append_endpoint_completion(route, f, finalplus, finalminus)
                predicted = captured+value+second+action.endpoint(f, finalplus, finalminus)
                assert predicted == law.payoff(route).value
                counts['wait'] += 1
        # Cross clipping boundaries in both frontiers. E is a concave future
        # potential with both partial slopes <= -e/2, as required by the lemma.
        for t in [Q(0), Q(1, 5), Q(3, 5)]:
            e = (t+1)/2
            z = action.center(t)
            vectors = [(z+(1-z)*a, z+(1-z)*b)
                       for a, b in [(Q(0), Q(1)), (Q(1), Q(0)),
                                    (Q(1, 5), Q(1, 3)), (Q(4, 5), Q(2, 3))]]
            for left, right in zip(vectors, vectors[1:]+vectors[:1]):
                weight = Q(1, 3)
                middle = tuple(weight*x+(1-weight)*y for x, y in zip(left, right))
                for kind in ['triangle', 'wait']:
                    def rhs(vector):
                        if kind == 'triangle':
                            value, p, n = action.triangle(t, e, *vector)
                        else:
                            value, p, n = action.wait(t, e, *vector)
                        return value+action.endpoint(e, p, n)
                    assert rhs(middle) >= weight*rhs(left)+(1-weight)*rhs(right)
                    counts['concavity'] += 1
    print(f"PASS: {sum(counts.values())} exact general-center checks")
    for key, count in counts.items():
        print(f'  {key}: {count}')
    print('PASS: non-unit inward/outward speeds, multiple waves, endpoint atoms')
    print('PASS: new interior captures after a center return with zero center mass')
    print('PASS: closed endpoint turn, both surviving frontiers, and center-record waits')
    print('Scope: action/concavity identities; no instantiated verification potential')


if __name__ == '__main__':
    main()
