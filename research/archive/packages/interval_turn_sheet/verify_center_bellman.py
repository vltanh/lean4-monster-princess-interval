#!/usr/bin/env python3
"""Independent exact capture checks for the two-state center certificate.

The asserted formulas integrate inverse characteristics over rank.  The
reference values are computed independently by continuous_rank's exact
running-CDF-record integration along the complete monster route.
"""
from fractions import Fraction as Q
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT/'packages/interval_continuous_rank'))
from continuous_rank import RankLaw
from center_bellman import (CenterActions, append_sweep, append_terminal_triangle,
                            append_triangle, append_wait, center_prefix_route,
                            endpoint_prefix_route)


def fixtures():
    return [
        RankLaw([0, 1], [Q(1, 10), Q(3, 4)],
                [Q(1, 4), Q(19, 20)], [Q(9, 10), Q(1, 10)]),
        RankLaw([0, Q(1, 2), 1], [Q(1, 10), Q(1, 2), Q(19, 20)],
                [Q(1, 4), Q(3, 4), Q(99, 100)],
                [Q(9, 10), Q(1, 5), Q(-4, 5)]),
        RankLaw([0, Q(2, 5), 1], [Q(1, 10), Q(9, 20), Q(7, 10)],
                [Q(1, 5), Q(7, 10), Q(6, 5)],
                [Q(19, 20), Q(3, 10), Q(-3, 5)]),
    ]


def main():
    counts = dict(prefix=0, endpoint_prefix=0, sweep=0, early=0, terminal=0,
                  lagging_dominance=0)
    seen = set()
    for law in fixtures():
        action = CenterActions(law)
        tau = action.tau
        assert law.B(tau) == law.D(tau)
        for z in [Q(1, 10), Q(3, 10), Q(7, 10), Q(9, 10), Q(1)]:
            for vfrac in [Q(1, 5), Q(1, 2), Q(4, 5)]:
                v = -z+2*z*vfrac
                for bfrac in [Q(0), Q(1, 5), Q(1, 2), Q(4, 5)]:
                    b = z+(v+2-z)*bfrac
                    route = center_prefix_route(z, v, b)
                    value, m, center = action.center_prefix(z, v, b)
                    direct = law.payoff(route, require_complete=False)
                    captured = direct.value-b*direct.survival
                    assert captured == value, ("prefix", z, v, b, captured, value)
                    assert direct.survival == 1-(m+center)/2
                    counts['prefix'] += 1
                    for wfrac in [Q(1, 5), Q(3, 5)]:
                        w = v+(b-v)*wfrac
                        endpoint_route = endpoint_prefix_route(z, v, b, w)
                        predicted = action.endpoint_prefix(z, v, b, w)
                        actual = law.payoff(endpoint_route).value
                        assert predicted == actual, ("endpoint prefix", z, v, b, w,
                                                     predicted, actual)
                        counts['endpoint_prefix'] += 1
                    if b > tau:
                        completed = route+[(b+1, -1), (b+3, 1)]
                        predicted = value+action.endpoint(b, m, center)
                        assert predicted == law.payoff(completed).value
                        continue
                    assert center == law.B(b)
                    assert m == max(law.A(z), law.B(b))
                    completed = list(route)
                    append_sweep(completed, b)
                    predicted = value+action.sweep(b, m)
                    assert predicted == law.payoff(completed).value
                    counts['sweep'] += 1
                    t = b+(tau-b)/3
                    e = t+2*(tau-t)/3
                    waited_m = max(m, law.B(t))
                    final_m = max(waited_m, law.B(e))
                    completed = list(route)
                    append_wait(completed, t)
                    append_triangle(completed, t, e)
                    append_sweep(completed, e)
                    predicted = (value+action.wait(b, t, m)
                                 +action.triangle(t, e, waited_m)
                                 +action.sweep(e, final_m))
                    assert predicted == law.payoff(completed).value, ("early", z, v, b)
                    counts['early'] += 1
                    seen.add('balanced' if final_m == law.B(e) else 'unbalanced')
                    for frac in [Q(1, 5), Q(1, 2), Q(4, 5)]:
                        end = tau+(2-tau)*frac
                        completed = list(route)
                        append_terminal_triangle(completed, action, b, end, m)
                        predicted = value+action.terminal_triangle(b, end, m)
                        actual = law.payoff(completed).value
                        assert predicted == actual, ("terminal", z, v, b, end,
                                                     predicted, actual)
                        counts['terminal'] += 1
                        # Compare the leading-side triangle with either endpoint order.
                        lead = list(route)
                        append_triangle(lead, b, end, sign=1)
                        best_lead = min(law.payoff(lead+[(end+1, first),
                                                       (end+3, -first)]).value
                                        for first in [-1, 1])
                        assert actual <= best_lead
                        counts['lagging_dominance'] += 1
    assert seen == {'balanced', 'unbalanced'}
    total = sum(counts.values())
    print(f'PASS: {total} exact center-action / initial-prefix checks')
    for key, count in counts.items():
        print(f'  {key}: {count}')
    print('PASS: independent a and u, negative c, central waits, and u>1')
    print('Scope: exact action identities and sign dominance, not a solved Bellman potential')


if __name__ == '__main__':
    main()
