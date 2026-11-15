"""Exact outer-column loss of the analytic capped incoming correction.

No algebraic inverse or quadrature is evaluated numerically. A rational
lower bracket for one warp inverse gives a positive rectangular integral
bound. This excludes the supplied corrected field at its endpoint target;
it does not give a bound on the game's value.
"""
from fractions import Fraction as Q
import json
from pathlib import Path

from audit_m1 import ExactField
from extract_endpoint_postdata import inward_one_route


def polynomial(coefficients, t):
    a, b, c = coefficients
    return (a*t+b)*t+c


def main():
    folder = Path(__file__).resolve().parent/'snapshots'
    field = ExactField(json.loads((folder/'endpoint_joint_i1_field.json').read_text()))
    payload = json.loads((folder/'endpoint_high_band_warp.json').read_text())
    assert payload['status'].startswith('exact terminal inverse range')
    pieces = [(Q(p['lo']), Q(p['hi']), list(map(Q, p['B'])),
               list(map(Q, p['G'])), Q(p['prefix_G']))
              for p in payload['pieces']]

    def moment_and_target(u):
        lo, hi, bc, gc, earlier = next(p for p in pieces if p[0] <= u <= p[1])
        t = (u-lo)/(hi-lo)
        target = max(earlier, polynomial(gc, Q(0)), polynomial(gc, t))
        a, b, _ = gc
        if a < 0 and 0 < -b/(2*a) < t:
            target = max(target, polynomial(gc, -b/(2*a)))
        current = polynomial(bc, t)
        return current, max(current, target)

    qlo, qhi = Q(payload['qlo']), Q(payload['qhi'])

    def band(value):
        return min(max(value-qlo, Q(0)), qhi-qlo)

    start = Q(5, 8)
    left = Q(1048575, 1048576)
    right = Q(16777201, 16777216)
    inverse_lower = Q(2097151, 2097152)
    assert Q(payload['repair_start']) < left < right < inverse_lower < 1
    # B(inverse_lower)<target(left) proves psi(left)>inverse_lower.
    assert moment_and_target(inverse_lower)[0] < moment_and_target(left)[1]
    # Both psi and A are increasing. The unchanged CDF is increasing in U.
    # Thus this is a lower bound on the entire changed band for every
    # U in [left,right], including the initial-front cap.
    gap = (band(min(field.initial_value(left), field.radial(inverse_lower, -start)))
           -band(field.radial(right, -start)))
    assert gap > 0
    column_lower = (right-left)*gap
    assert column_lower == Q(20483216873, 214748364800000000000)
    endpoint = field.positive_m1(Q(1))
    f = field.positive_m1(start)
    g = field.unit_route_payoff(inward_one_route(start, start))
    # All other changed contributions are nonnegative, and this start is
    # below both bridges, so 4*DeltaCf=4*DeltaCg=-integral DeltaR.
    assert start < Q(payload['bridge_start'])
    new_f_upper = f-column_lower/4
    new_g_upper = g-column_lower/4
    assert new_f_upper < endpoint and new_g_upper < endpoint
    print('PASS: exact positive outer-column loss for the capped two-band field')
    print('Start:', start)
    print('Column increase is at least:', column_lower)
    print('Both positive response costs decrease by at least:', column_lower/4)
    print('New f cost minus endpoint is at most:', new_f_upper-endpoint)
    print('New g cost minus endpoint is at most:', new_g_upper-endpoint)
    print('Scope: supplied-field exclusion and source coupling, not a game-value bound')


if __name__ == '__main__':
    main()
