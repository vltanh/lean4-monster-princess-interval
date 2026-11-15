#!/usr/bin/env python3
"""Independent exact fixture for the signed primal-dual payoff derivatives."""
from fractions import Fraction as Q
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'interval_continuous_rank'))
from continuous_rank import RankLaw, FiveLegLaw


def main():
    # Uniform initial a=q, incoming u=q, outgoing c=y=1-q. This has a
    # genuine central waiting atom and crosses C(z)=A(z) at z=1/2.
    law = RankLaw([0, 1], [0, 1], [0, 1], [1, 0])

    def payoff(kind, z, selected_law=law):
        if kind == 'f':
            route = [(0, z), (1-z, 1), (3-z, -1)]
        elif kind == 'g':
            route = [(0, z), ((1-z)/2, (1+z)/2), (2, -1), (4, 1)]
        elif kind == 'h':
            route = [(0, -z), ((1+z)/2, (1-z)/2), (2, -1), (4, 1)]
        else:
            route = [(0, -z), (1+z, 1), (3+z, -1)]
        return selected_law.payoff(route).value

    checks = 0
    for z in (Q(1, 4), Q(3, 4)):
        # Every payoff is quadratic on the indicated open regime. The
        # centered rational difference is consequently its exact derivative.
        step = Q(1, 1000)
        A, rho, C, Cp = z, Q(1), 1-z, Q(-1)
        alpha, c = 1-z, 1-z
        derivatives = {
            'f': ((2-z+c)*rho-3)/4,
            'g': ((1+c)*rho-(1-A))/4,
        }
        if C > A:
            derivatives['h'] = (3*A+C+(2*z-4)*rho+(alpha+z-8)*Cp)/4
            derivatives['ell'] = (4+A-C-6*rho+(alpha-z-2)*Cp)/4
        else:
            derivatives['h'] = (A+3*C+(z+c-4)*rho+2*(z-4)*Cp)/4
            derivatives['ell'] = (4-A+C-(6+z-c)*rho-2*Cp)/4
        for kind, expected in derivatives.items():
            actual = (payoff(kind, z+step)-payoff(kind, z-step))/(2*step)
            assert actual == expected, (kind, z, actual, expected)
            checks += 1

    # Distinct outgoing fronts c=1-q, y=1-q/2 exercise the Y' terms.
    # For the fixed monster parameters below, the second incoming line
    # A2=1+epsilon(1+q) changes only the extra-leg B captures, affinely in
    # epsilon. Two exact evaluations therefore recover its one-sided limit.
    epsilon = Q(1, 1000)
    extra_laws = [FiveLegLaw([0, 1], [0, 1], [0, 1], [1, 0],
                            [1+e, 1+2*e], [1, Q(1, 2)])
                  for e in (epsilon, epsilon/2)]

    def limit_payoff(kind, z):
        return 2*payoff(kind, z, extra_laws[1])-payoff(kind, z, extra_laws[0])

    for z in (Q(1, 4), Q(3, 4)):
        step = Q(1, 1000)
        A, rho, C, Cp = z, Q(1), 1-z, Q(-1)
        alpha, c, y = 1-z, 1-z, 1-z/2
        Y, Yp = (Q(1), Q(0)) if z < Q(1, 2) else (2-2*z, Q(-2))
        derivatives = {
            'f': ((2-z+y)*rho-3)/4,
            'g': ((1+c)*rho-(1-A))/4,
        }
        if C > A:
            derivatives['h'] = (3*A+C+(2*z-4)*rho+(alpha+z-8)*Cp)/4
            derivatives['ell'] = (4+A-Y-6*rho+(alpha-1)*Cp-(1+z)*Yp)/4
        else:
            derivatives['h'] = (A+3*C+(z+c-4)*rho+2*(z-4)*Cp)/4
            derivatives['ell'] = (4-A+2*C-Y-(6+z-c)*rho+(z-1)*Cp-(1+z)*Yp)/4
        for kind, expected in derivatives.items():
            actual = (limit_payoff(kind, z+step)-limit_payoff(kind, z-step))/(2*step)
            assert actual == expected, ('extra', kind, z, actual, expected)
            checks += 1
    print(f'PASS: {checks} exact dual derivative fixtures against independent rank integration')
    print('Coverage: four monster families, both front orders, center waiting and distinct c/y fronts')
    print('Scope: capture-regime identities only; not an equilibrium certificate')


if __name__ == '__main__':
    main()
