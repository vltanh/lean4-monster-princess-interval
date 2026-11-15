#!/usr/bin/env python3
"""Exact fixtures for the four-/seven-state physical-clock lift.

Uses only the standard library.  The continuum superposition theorem
is proved/applied in FINITE_STATE_PHYSICAL_CLOCK_LIFT.md; this program
audits the explicit graph completion and pressure formulas.
"""

from fractions import Fraction as Q
from random import Random


CORE_VELOCITIES = (
    (1, -1, -1, -1), (1, 1, -1, -1),
    (0, 0, 1, 0), (0, 0, 0, 1),
)
FULL_VELOCITIES = tuple(v + (0, 0, 0) for v in CORE_VELOCITIES) + (
    (0, 0, 0, 0, 1, 0, 0),
    (0, 0, 0, 0, 0, 1, 0),
    (0, 0, 0, 0, 0, 0, 1),
)


def at(times, values, time):
    if time == times[-1]:
        return values[-1]
    for i, (left, right) in enumerate(zip(times, times[1:])):
        if left <= time < right:
            return values[i] + (values[i + 1] - values[i]) * (time - left) / (right - left)
    raise AssertionError(("outside physical horizon", time))


def legal(times, values, radial=False):
    floor = 0 if radial else -1
    return all(floor <= x <= 1 for x in values) and all(
        right > left and abs(y - x) <= right - left
        for left, right, x, y in zip(times, times[1:], values, values[1:])
    )


def indicator_integral(a, b, length):
    """Integral of 1{affine function > 0}, preserving coincident segments."""
    if a == b == 0:
        return Q(0)
    if a >= 0 and b >= 0:
        return length
    if a <= 0 and b <= 0:
        return Q(0)
    if a > 0:
        return length * a / (a - b)
    return length * b / (b - a)


def phi(radius, position):
    return int(radius < position) + int(radius > -position)


def physical_pressure(times, monster, radius, atom_plus, atom_minus, density_plus, density_minus):
    score = Q(0)
    for i, time in enumerate(times):
        score += atom_minus[i] * phi(radius[i], monster[i]) / 2
        score += atom_plus[i] * phi(radius[i], -monster[i]) / 2
    for i, (left, right) in enumerate(zip(times, times[1:])):
        for sign, density in ((1, density_minus[i]), (-1, density_plus[i])):
            score += density / 2 * (
                indicator_integral(sign * monster[i] - radius[i], sign * monster[i + 1] - radius[i + 1], right - left)
                + indicator_integral(sign * monster[i] + radius[i], sign * monster[i + 1] + radius[i + 1], right - left)
            )
    return score


def graph_pressure(segments, times, radius):
    score = Q(0)
    for before, after, weights, length in segments:
        ra = at(times, radius, before[0])
        rb = at(times, radius, after[0])
        for sign, control in ((-1, 2), (1, 3)):
            score += weights[control] / 2 * (
                indicator_integral(sign * before[1] - ra, sign * after[1] - rb, length)
                + indicator_integral(sign * before[1] + ra, sign * after[1] + rb, length)
            )
    return score


def lift(times, monster, atom_plus, atom_minus, density_plus, density_minus, register=False):
    horizon = times[-1]
    velocities = FULL_VELOCITIES if register else CORE_VELOCITIES
    dimension = len(velocities)
    state = tuple([Q(0), monster[0], Q(0), Q(0)] + ([Q(0)] * 3 if register else []))
    graph_time = Q(0)
    segments = []

    def move(length, weights):
        nonlocal state, graph_time
        if length == 0:
            return
        assert length > 0 and sum(weights) == 1 and min(weights) >= 0
        velocity = tuple(sum(weights[j] * velocities[j][i] for j in range(dimension)) for i in range(dimension))
        after = tuple(value + length * speed for value, speed in zip(state, velocity))
        graph_time += length
        assert 0 <= after[0] <= horizon and -1 <= after[1] <= 1
        assert all(0 <= queue <= horizon - after[0] for queue in after[2:4])
        if register:
            assert all(0 <= value <= 1 for value in after[4:])
        assert 3 * after[0] + sum(after[2:]) == graph_time
        segments.append((state, after, tuple(weights), length))
        state = after

    def pure(length, control):
        weights = [Q(0)] * dimension
        weights[control] = Q(1)
        move(length, weights)

    for i, time in enumerate(times):
        assert state[0] == time and state[1] == monster[i]
        if register:
            for index, position in enumerate((-1, 0, 1)):
                if state[4 + index] == 0 and monster[i] == position and (index != 1 or time <= 3):
                    pure(Q(1), 4 + index)
        pure(atom_plus[i], 2)
        pure(atom_minus[i], 3)
        if i == len(times) - 1:
            break
        dt = times[i + 1] - time
        physical_speed = (monster[i + 1] - monster[i]) / dt
        scale = 1 + density_plus[i] + density_minus[i]
        weights = [
            (1 - physical_speed) / (2 * scale),
            (1 + physical_speed) / (2 * scale),
            density_plus[i] / scale,
            density_minus[i] / scale,
        ] + ([Q(0)] * 3 if register else [])
        move(dt * scale, weights)

    assert state[0] == horizon and state[2] == state[3] == 0
    assert graph_time == 3 * horizon + (3 if register else 0)
    if register:
        assert state[4:] == (1, 1, 1)
    for control in (2, 3):
        assert sum(length * weights[control] for _, _, weights, length in segments) == horizon
    if register:
        for control, position in ((4, -1), (5, 0), (6, 1)):
            charge = Q(0)
            for before, after, weights, length in segments:
                if weights[control]:
                    assert before[1] == after[1] == position
                    if control == 5:
                        assert before[0] <= 3 and after[0] <= 3
                    charge += length * weights[control]
            assert charge == 1
    return segments


def atomic_clock(rng, intervals, step):
    # Each scoring block j selects a node k<=j. The choice need not be
    # monotone; sorting produces its identical causal quantile clock.
    indices = [rng.randrange(j + 1) for j in range(intervals)]
    atoms = [Q(0)] * (intervals + 1)
    for index in indices:
        atoms[index] += step
    sorted_indices = sorted(indices)
    assert all(index <= j for j, index in enumerate(sorted_indices))
    cumulative = Q(0)
    for i in range(intervals):
        cumulative += atoms[i]
        assert cumulative >= (i + 1) * step
    assert atoms[-1] == 0 and sum(atoms) == intervals * step
    # Independent pushforward moment comparison with the original
    # potentially nonmonotone scoring selector.
    for power in range(5):
        assert sum(step * (index * step) ** power for index in indices) == sum(
            mass * (i * step) ** power for i, mass in enumerate(atoms)
        )
    return atoms


def determinant(matrix):
    rows = [[Q(x) for x in row] for row in matrix]
    out = Q(1)
    for i in range(len(rows)):
        pivot = next(j for j in range(i, len(rows)) if rows[j][i])
        if pivot != i:
            rows[i], rows[pivot] = rows[pivot], rows[i]
            out = -out
        value = rows[i][i]
        out *= value
        rows[i] = [x / value for x in rows[i]]
        for j in range(i + 1, len(rows)):
            factor = rows[j][i]
            rows[j] = [a - factor * b for a, b in zip(rows[j], rows[i])]
    return out


def run():
    assert abs(determinant(CORE_VELOCITIES)) == 2
    assert abs(determinant(FULL_VELOCITIES)) == 2
    for velocities in (CORE_VELOCITIES, FULL_VELOCITIES):
        for velocity in velocities:
            assert 3 * velocity[0] + sum(velocity[2:]) == 1
    rng = Random(20261113)
    step, intervals = Q(1, 2), 14
    times = [i * step for i in range(intervals + 1)]
    fixtures = 0
    segments_checked = 0
    pressure_checks = 0
    for attempt in range(1200):
        monster = [Q(rng.randrange(-2, 3), 2)]
        for _ in range(intervals):
            possible = [monster[-1] + move * step for move in (-1, 0, 1) if -1 <= monster[-1] + move * step <= 1]
            monster.append(rng.choice(possible))
        if not ({Q(-1), Q(1)} <= set(monster)) or not any(x == 0 and t <= 3 for t, x in zip(times, monster)):
            continue
        assert legal(times, monster)
        raw_plus = atomic_clock(rng, intervals, step)
        raw_minus = atomic_clock(rng, intervals, step)
        mix_plus, mix_minus = Q(rng.randrange(4), 3), Q(rng.randrange(4), 3)
        atom_plus = [mix_plus * x for x in raw_plus]
        atom_minus = [mix_minus * x for x in raw_minus]
        density_plus = [1 - mix_plus] * intervals
        density_minus = [1 - mix_minus] * intervals
        core = lift(times, monster, atom_plus, atom_minus, density_plus, density_minus)
        full = lift(times, monster, atom_plus, atom_minus, density_plus, density_minus, register=True)
        segments_checked += len(core) + len(full)
        radii = [[Q(0)] * len(times), [Q(1, 2)] * len(times), [Q(1)] * len(times), [abs(x) for x in monster]]
        random_radius = [Q(rng.randrange(3), 2)]
        for _ in range(intervals):
            possible = [random_radius[-1] + move * step for move in (-1, 0, 1) if 0 <= random_radius[-1] + move * step <= 1]
            random_radius.append(rng.choice(possible))
        radii.append(random_radius)
        for radius in radii:
            assert legal(times, radius, radial=True)
            physical = physical_pressure(times, monster, radius, atom_plus, atom_minus, density_plus, density_minus)
            assert physical == graph_pressure(core, times, radius)
            assert physical == graph_pressure(full, times, radius)
            pressure_checks += 2
        fixtures += 1
        if fixtures == 120:
            break
    assert fixtures == 120

    # Continuous full-horizon two-sweep clocks: eta_- is Lebesgue on
    # [0,2] plus 5 delta_2, while eta_+=7 delta_0. Exactly six units of
    # projected mass are inert at x=-1. Active mass is exactly one.
    inert_checks = 0
    for denominator in range(2, 42):
        epsilon = Q(1, denominator)
        nodes = sorted({Q(0), 1 - epsilon, 2 - epsilon, Q(1), Q(2), Q(7)})
        monster = [max(Q(-1), 1 - t) for t in nodes]
        radius = [abs(min(Q(1), -1 + epsilon + t)) for t in nodes]
        ap = [Q(7) if t == 0 else Q(0) for t in nodes]
        am = [Q(5) if t == 2 else Q(0) for t in nodes]
        dp = [Q(0)] * (len(nodes) - 1)
        dm = [Q(1) if t < 2 else Q(0) for t in nodes[:-1]]
        full = lift(nodes, monster, ap, am, dp, dm, register=True)
        active = inert = Q(0)
        for before, after, weights, length in full:
            for sign, control in ((-1, 2), (1, 3)):
                mass = weights[control] * length / 2
                if sign * before[1] == sign * after[1] == -1:
                    inert += mass
                else:
                    active += mass
        assert active == 1 and inert == 6
        assert graph_pressure(full, nodes, radius) == Q(3, 2) - epsilon / 4
        assert physical_pressure(nodes, monster, radius, ap, am, dp, dm) == Q(3, 2) - epsilon / 4
        contact_radius = [abs(1 - t) if t <= 2 else Q(1) for t in nodes]
        assert graph_pressure(full, nodes, contact_radius) == Q(1, 2)
        inert_checks += 1

    print(
        f"PASS: {fixtures} exact four-/seven-state clock fixtures; "
        f"{segments_checked} compact-state/control segments; "
        f"{pressure_checks} independent strict-pressure projection comparisons; "
        f"{inert_checks} continuous two-sweep inert-mass/contact-germ checks."
    )
    print("Graph horizons:21 (core),24 (visit-enforced); both clocks total7; causal quantile checks passed.")
    print("Scope: finite arithmetic regression; continuum sufficiency uses the proved superposition argument, not fixture enumeration.")


if __name__ == "__main__":
    run()
