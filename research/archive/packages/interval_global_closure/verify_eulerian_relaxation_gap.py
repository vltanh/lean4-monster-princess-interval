#!/usr/bin/env python3
"""Exact arithmetic audit of the fake Eulerian clock occupation.

The analytic continuum proof is EULERIAN_RELAXATION_GAP.md.  This file
does not claim to solve the original game or mechanically prove an
infinite-dimensional lifting theorem.  No third-party modules are used.
"""

from fractions import Fraction as Q
from math import comb


# Polynomials in independent variables (t,q); keys are their exponents.
ZERO = {}
ONE = {(0, 0): Q(1)}
T = {(1, 0): Q(1)}
PAR = {(0, 1): Q(1)}


def add(*polys):
    out = {}
    for poly in polys:
        for key, value in poly.items():
            out[key] = out.get(key, Q(0)) + value
    return {key: value for key, value in out.items() if value}


def scale(poly, factor):
    return {key: value * factor for key, value in poly.items() if value * factor}


def mul(a, b):
    out = {}
    for (at, aq), av in a.items():
        for (bt, bq), bv in b.items():
            key = (at + bt, aq + bq)
            out[key] = out.get(key, Q(0)) + av * bv
    return {key: value for key, value in out.items() if value}


def power(a, n):
    out = ONE
    for _ in range(n):
        out = mul(out, a)
    return out


def rectangle_integral(poly, left, right):
    """Integrate in q from 0 to 1, then in t from left to right."""
    return sum(
        (
            value * (right ** (nt + 1) - left ** (nt + 1))
            / Q((nt + 1) * (nq + 1))
            for (nt, nq), value in poly.items()
        ),
        Q(0),
    )


def sigma_moment(i, j):
    # sigma = 1/2 * dt at (t,1-t), 0<t<2.
    return sum(
        (
            Q(comb(j, h) * (-1) ** h, 2)
            * Q(2) ** (i + h + 1) / Q(i + h + 1)
            for h in range(j + 1)
        ),
        Q(0),
    )


def alpha_moment(i, j):
    # alpha = delta_0(time) [dx/4 on [-1,1] + delta_{-1/2}/2].
    if i:
        return Q(0)
    uniform = Q(1, 2 * (j + 1)) if j % 2 == 0 else Q(0)
    return uniform + Q(1, 2) * Q(-1, 2) ** j


def backlog_derivative_moment(i, j):
    """Integral beta*phi_t+k*phi_x for phi(s,x)=s**i*x**j.

    In the segment parametrization s=t*q, ds=t*dq, x=a+q*d,
    d=1-t-a.  Multiplication by t cancels the velocity denominator.
    Both branches therefore require only polynomial integration.
    """
    selected_time = mul(T, PAR)
    branches = [
        (Q(0), Q(1), add(ONE, scale(T, -2)), T),
        (Q(1), Q(2), scale(ONE, Q(-1, 2)), add(scale(ONE, Q(3, 2)), scale(T, -1))),
    ]
    result = Q(0)
    for left, right, origin, displacement in branches:
        position = add(origin, mul(PAR, displacement))
        integrand = ZERO
        if i:
            integrand = add(
                integrand,
                scale(mul(T, mul(power(selected_time, i - 1), power(position, j))), i),
            )
        if j:
            integrand = add(
                integrand,
                scale(mul(displacement, mul(power(selected_time, i), power(position, j - 1))), j),
            )
        result += Q(1, 2) * rectangle_integral(integrand, left, right)
    return result


def at(path, time):
    for (ta, xa), (tb, xb) in zip(path, path[1:]):
        if ta <= time <= tb:
            return xa + (xb - xa) * (time - ta) / (tb - ta)
    raise AssertionError(("time outside fixture", time))


def first_contact(a, b):
    events = sorted(set(t for t, _ in a) | set(t for t, _ in b))
    for left, right in zip(events, events[1:]):
        dl = at(a, left) - at(b, left)
        dr = at(a, right) - at(b, right)
        if dl == 0:
            return left
        if dl * dr <= 0:
            return left + (right - left) * (-dl) / (dr - dl)
    if at(a, events[-1]) == at(b, events[-1]):
        return events[-1]
    raise AssertionError("fixture has no contact")


def legal(path):
    return all(-1 <= x <= 1 for _, x in path) and all(
        tb > ta and abs(xb - xa) <= tb - ta
        for (ta, xa), (tb, xb) in zip(path, path[1:])
    )


def phi(radius, position):
    return int(radius < position) + int(radius > -position)


def reversing_witness():
    """Second fake: a real reversing Monster law, plus all named cuts."""
    delta = Q(1, 4)
    x0 = 1 - delta / 2
    edge = 1 - delta
    monster = [
        (Q(0), x0), (delta / 4, 1 - 3 * delta / 4),
        (delta, Q(1)), (delta + 2, Q(-1)),
    ]
    reflected = [(t, -x) for t, x in monster]
    assert legal(monster) and legal(reflected)
    princess = [(Q(0), -1 + delta), (2 - delta, Q(1)), (2 + delta, Q(1))]
    assert legal(princess)
    assert first_contact(monster, princess) == 1
    assert first_contact(reflected, princess) == 2 + delta
    assert (first_contact(monster, princess) + first_contact(reflected, princess)) / 2 == Q(13, 8)

    # Each tuple is (left,right,source-position,sink-position,weight).
    bridges = []
    for sign in (Q(1), Q(-1)):
        bridges.extend([
            (Q(0), delta / 4, scale(ONE, sign * x0),
             scale(add(scale(ONE, x0), scale(T, -1)), sign), Q(1, 2)),
            (delta / 4, delta, scale(ONE, sign * x0),
             scale(add(scale(ONE, 1 - delta), T), sign), Q(1, 2)),
        ])
    tail = add(scale(ONE, 1 + delta), scale(T, -1))
    bridges.extend([
        (delta, Q(1), add(scale(ONE, 1 + delta), scale(T, -2)), tail, Q(1, 2)),
        (Q(1), delta + 2, scale(ONE, delta - 1), tail, Q(1, 2)),
    ])

    moments = 0
    for total in range(9):
        for i in range(total + 1):
            j = total - i
            alpha = Q(0)
            if i == 0:
                alpha = delta / 2 * (x0 ** j + (-x0) ** j)
                alpha += (edge ** (j + 1) - (-edge) ** (j + 1)) / (4 * (j + 1))
                alpha += (1 + delta) / 2 * (-edge) ** j
            sigma = Q(0)
            backlog = Q(0)
            for left, right, origin, sink, weight in bridges:
                sigma += weight * rectangle_integral(mul(power(T, i), power(sink, j)), left, right)
                displacement = add(sink, scale(origin, -1))
                selected_time = mul(T, PAR)
                position = add(origin, mul(PAR, displacement))
                integrand = ZERO
                if i:
                    integrand = add(integrand, scale(mul(T, mul(power(selected_time, i - 1), power(position, j))), i))
                if j:
                    integrand = add(integrand, scale(mul(displacement, mul(power(selected_time, i), power(position, j - 1))), j))
                backlog += weight * rectangle_integral(integrand, left, right)
            assert alpha - sigma == -backlog
            moments += 1

    # The pressure plan matches the continuous parts and the prefix atoms
    # diagonally. Direct strict scoring checks contact at BOTH atom radii.
    radial_checks = 0
    for denominator in range(1, 61):
        for numerator in range(denominator + 1):
            radius = Q(numerator, denominator)
            continuous = Q(1, 4) * (max(0, edge - radius) + min(2 * edge, edge + radius))
            score = continuous + delta / 2 * (phi(radius, x0) + phi(radius, -x0))
            score += (1 + delta) / 2 * phi(radius, -edge)
            expected = (1 + delta) / 2 * (1 + int(radius > edge)) - delta / 2 * int(radius == x0)
            assert score == expected <= 1 + delta
            radial_checks += 1
    assert (1 + delta) / 2 * (1 + int(Q(1) > edge)) == Q(5, 4)
    positive_mass = delta / 2 + edge / 4
    assert positive_mass == Q(5, 16)  # all is matched

    upper = Q(57045188913812444387410009, 40000000000000000000000000)
    lower = Q(36290299773897097, 25600000000000000)
    assert 1 + delta == Q(5, 4) < lower
    assert x0 >= 2 - upper
    assert delta <= upper - 1
    assert delta > Q(181, 20000)
    a = Q(3, 2) - upper
    assert 0 < a < Q(1, 10)
    # d_* < (6/7)a < 1/4 follows because its square-root radicand > 1.
    assert 6 * a - 5 * a * a > 0 and 6 * a / 7 < delta
    assert Q(1) >= 4 * a / (3 + x0)  # q=0 canonical support inequality
    # Weakened effort inequality has zero right side, by exact squaring.
    test = Q(1, 2) - Q(3, 2) * delta
    assert test > 0 and test * test < 2 * delta
    # Unweakened mean-delay envelope at delta=1/4.
    assert Q(3, 2) - Q(1, 2) - delta / 4 == Q(15, 16) <= 1 + delta

    continuum_checks = 0
    for denominator in range(2, 81):
        for numerator in range(1, denominator):
            width = Q(numerator, denominator)
            if width <= delta:
                envelope = Q(1, 2) - width / 4
            else:
                envelope = Q(3, 2) - width / 8 - (1 / width + Q(3, 4)) * delta + 5 * delta * delta / (8 * width)
                factorization = (16 * (width - Q(1, 4)) ** 2 + 26) / (128 * width)
                assert 1 + delta - envelope == factorization > 0
            assert envelope <= 1 + delta
            continuum_checks += 1
    return moments, radial_checks, continuum_checks


def run():
    # Distributional equality alpha-sigma = div(beta,k), including t=0.
    moments = 0
    for total in range(9):
        for i in range(total + 1):
            j = total - i
            assert alpha_moment(i, j) - sigma_moment(i, j) == -backlog_derivative_moment(i, j)
            moments += 1
    assert alpha_moment(0, 0) == sigma_moment(0, 0) == 1

    # The chronological sweep's continuity equation has its own,
    # independent initial source and endpoint sink.
    source_checks = 0
    for total in range(9):
        for i in range(total + 1):
            j = total - i
            derivative = (i * sigma_moment(i - 1, j) if i else 0)
            derivative -= (j * sigma_moment(i, j - 1) if j else 0)
            source = (Q(1, 2) if i == 0 else Q(0))
            sink = Q(1, 2) * Q(2) ** i * Q(-1) ** j
            assert -derivative == source - sink
            source_checks += 1

    # Exact legal segments for many nontrivial rational parameter values;
    # the continuous speed bound is proved separately in the manuscript.
    segment_checks = 0
    for denominator in range(2, 41):
        for numerator in range(1, 2 * denominator):
            end_time = Q(numerator, denominator)
            origin = 1 - 2 * end_time if end_time <= 1 else Q(-1, 2)
            end_position = 1 - end_time
            assert legal([(Q(0), origin), (end_time, end_position)])
            # Source precedes sink in the full physical speed cone.
            assert abs(end_position - origin) <= end_time
            segment_checks += 1

    # Direct integration of the strict radial reward for the continuum
    # measure, including the negative atom exactly on its contact graph.
    radial_checks = 0
    for denominator in range(1, 61):
        for numerator in range(denominator + 1):
            radius = Q(numerator, denominator)
            uniform_score = Q(1, 4) * ((1 - radius) + (1 + radius))
            score = uniform_score + Q(1, 2) * phi(radius, Q(-1, 2))
            expected = Q(1, 2) + Q(1, 2) * int(radius > Q(1, 2))
            assert score == expected <= 1
            radial_checks += 1
    assert Q(1, 2) + Q(1, 2) * phi(Q(1), Q(-1, 2)) == 1
    assert phi(Q(1, 2), Q(-1, 2)) == 0  # exact contact is captured

    # Finite atomic analogues: match every positive atom diagonally to
    # the equal-radius negative atom.  Exhaust every threshold and germ
    # interval to verify the independent physical strict oracle is 1.
    matching_checks = 0
    for count in range(1, 65):
        radii = [Q(2 * i + 1, 2 * count) for i in range(count)]
        weight = Q(1, 4 * count)
        positive = [(radius, weight) for radius in radii]
        negative = [(radius, weight) for radius in radii] + [(Q(1, 2), Q(1, 2))]
        assert sum(mass for _, mass in positive) == Q(1, 4)
        assert all(v >= u + abs(Q(0) - Q(0)) for (u, _), (v, _) in zip(positive, negative))
        levels = sorted(set([Q(0), Q(1), Q(1, 2)] + radii))
        thresholds = levels + [(a + b) / 2 for a, b in zip(levels, levels[1:])]
        scores = [
            sum(mass * phi(radius, x) for x, mass in positive)
            + sum(mass * phi(radius, -x) for x, mass in negative)
            for radius in thresholds
        ]
        assert max(scores) == 1
        matching_checks += len(thresholds)

    # The same chronological Monster law has real Princess responses
    # tending to 3/2.  This uses first physical contact, not the fake alpha.
    sweep_right = [(Q(0), Q(-1)), (Q(2), Q(1))]
    sweep_left = [(Q(0), Q(1)), (Q(2), Q(-1))]
    response_checks = 0
    for denominator in range(2, 102):
        epsilon = Q(1, denominator)
        princess = [(Q(0), -1 + epsilon), (2 - epsilon, Q(1)), (Q(2), Q(1))]
        assert legal(princess) and legal(sweep_right) and legal(sweep_left)
        t_right = first_contact(sweep_right, princess)
        t_left = first_contact(sweep_left, princess)
        assert t_right == 2 and t_left == 1 - epsilon / 2
        assert (t_right + t_left) / 2 == Q(3, 2) - epsilon / 4 > 1
        response_checks += 1

    lower = Q(36290299773897097, 25600000000000000)
    assert lower > Q(17, 12) > 1
    # The fake occupation charges historical time zero at negative x;
    # the actual only active Monster path starts at positive endpoint +1.
    assert Q(1, 2) > 0  # its explicit negative atom mass
    print(
        "PASS: exact Eulerian relaxation value 1; "
        f"{moments} clock-conservation moments, {source_checks} source/sink moments, "
        f"{segment_checks} legal transport segments, {radial_checks} strict radial integrals, "
        f"{matching_checks} atomic threshold/germ checks, {response_checks} physical sweep responses."
    )
    robust_moments, robust_radial, continuum_cuts = reversing_witness()
    print(
        "PASS: reversing-path fake value 5/4; actual Princess payoff 13/8; "
        f"{robust_moments} conservation moments, {robust_radial} strict radial integrals, "
        f"{continuum_cuts} exact envelope-factorization checks and all listed scalar cuts."
    )
    print("Scope: a rigorous nonphysical relaxation counterexample; no new original-game bound or equilibrium.")


if __name__ == "__main__":
    run()
