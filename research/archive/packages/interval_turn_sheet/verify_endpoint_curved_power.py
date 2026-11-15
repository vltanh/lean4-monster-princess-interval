"""Physical endpoint-inward audit of a curved initial power.

The endpoint route and positive M1 coincide after their initial prefixes.
The compared scores below come from first intersections of actual paths.
The displayed remainder is checked independently, not used as a capture
oracle. This is a local necessary-balance fixture, not a matched law.
"""
import argparse

import mpmath as mp

from verify_curved_initial_power import PowerWave


def routes(b, delta):
    a = b + delta
    f = [(mp.mpf(0), b), (1-b, mp.mpf(1)),
         (3-b, mp.mpf(-1))]
    endpoint = [(mp.mpf(0), a), (delta/2, b+delta/2),
                (1-b, mp.mpf(1)), (3-b, mp.mpf(-1))]
    return f, endpoint


def physical_score(wave, route, cuts):
    total = mp.mpf(0)
    for left, right in zip(cuts, cuts[1:]):
        if right > left:
            total += mp.quad(lambda initial:
                             wave.capture(initial, route, 1)
                             + wave.capture(initial, route, -1),
                             [left, right])
    return wave.rho*total/2


def remainder(wave, b, delta):
    gamma, kappa = wave.gamma, wave.kappa
    d = 2 + wave.c0 - 2*b
    return wave.rho*(
        d*kappa*delta**gamma/2**gamma
        - 2*gamma/(gamma+1)*kappa**(-1/gamma)*delta**(1+1/gamma)
        + delta**2/2
        - kappa*gamma/((gamma+1)*2**gamma)*delta**(gamma+1)
        - kappa*kappa/2**(2*gamma+1)*delta**(2*gamma))


def run(quick=False):
    mp.mp.dps = 45
    b = mp.mpf(3)/10
    phi = (1+mp.sqrt(5))/2
    d = 2 + mp.mpf(9)/10 - 2*b
    balanced = (2**(phi+1)/(phi*d))**(1/phi)
    cases = [("quadratic", mp.mpf(2), mp.mpf(1)),
             ("three_halves", mp.mpf(3)/2, mp.mpf(1)),
             ("golden_balanced", phi, balanced)]
    exponents = [12, 16] if quick else list(range(12, 19))
    checks = 0
    for name, gamma, kappa in cases:
        wave = PowerWave(gamma, kappa)
        for exponent in exponents:
            delta = mp.mpf(2)**(-exponent)
            assert delta < wave.s0
            cut = b+kappa*(delta/2)**gamma
            cuts = sorted({wave.low, b, cut, b+delta, wave.high})
            f, endpoint = routes(b, delta)
            f_score = physical_score(wave, f, cuts)
            endpoint_score = physical_score(wave, endpoint, cuts)
            actual = 4*(endpoint_score-f_score)
            expected = remainder(wave, b, delta)
            assert abs(actual-expected) < mp.mpf("1e-35"), (
                name, exponent, actual, expected)
            assert (actual < 0) if name == "quadratic" else (actual > 0)
            checks += 1
            # Individual first-capture checks also retain the initial and
            # first-turn equalities. Outside this band, coalescence gives
            # the same first capture on each reflection separately.
            for initial in (wave.low, b, b+delta, wave.high):
                for sign in (-1, 1):
                    left = wave.capture(initial, f, sign)
                    right = wave.capture(initial, endpoint, sign)
                    if initial in (wave.low, wave.high) or sign == -1:
                        assert abs(left-right) < mp.mpf("1e-38")
                        checks += 1
            print(name, "delta=2^-"+str(exponent),
                  "four-cost gain", mp.nstr(actual, 17))
    print("PASS:", checks, "45-digit endpoint curved-power comparisons")
    print("Scope: physical local germ; no equilibrium or interval certificate")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--quick", action="store_true")
    run(parser.parse_args().quick)
