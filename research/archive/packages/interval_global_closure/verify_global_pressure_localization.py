#!/usr/bin/env python3
"""Exact finite regression for the global physical pressure constructions.

Uses only the Python standard library and rational arithmetic. The accompanying
manuscripts supply the measure-level theorem; this script checks simultaneous
fractional rerouting, atomic front completion, and physical boundary-turn
accounting on nontrivial exact fixtures.
"""

from collections import defaultdict
from fractions import Fraction as F


def solve_linear(matrix, rhs):
    """Exact Gauss--Jordan solve of a nonsingular square rational system."""
    n = len(rhs)
    a = [list(map(F, row)) + [F(value)] for row, value in zip(matrix, rhs)]
    for col in range(n):
        pivot = next(row for row in range(col, n) if a[row][col])
        a[col], a[pivot] = a[pivot], a[col]
        scale = a[col][col]
        a[col] = [value / scale for value in a[col]]
        for row in range(n):
            if row == col or not a[row][col]:
                continue
            scale = a[row][col]
            a[row] = [x - scale * y for x, y in zip(a[row], a[col])]
    return [a[row][-1] for row in range(n)]


def push_kernel(kernel, measure):
    n = len(measure)
    return [
        sum((measure[i] * kernel[i][j] for i in range(n)), F(0))
        for j in range(n)
    ]


def verify_fractional_resource_cycle():
    # p0,p1 are paired positive resources with a genuine fractional cycle;
    # p2 is an unpaired tail positive resource. p3,p4 form an independent
    # closed alternating cycle carrying no initial deficiency.
    positive = [F(1)] * 5
    negative = [F(1)] * 5
    mate = {0: 0, 1: 1, 3: 3, 4: 4}
    matching = [[F(0) for _ in negative] for _ in positive]
    for p, n, mass in [
        (0, 0, F(1, 4)), (1, 0, F(1, 2)), (2, 0, F(1, 8)),
        (0, 1, F(1, 2)), (1, 1, F(1, 4)), (2, 1, F(1, 8)),
        (0, 2, F(1, 8)), (1, 2, F(1, 8)), (2, 2, F(1, 2)),
        (4, 3, F(1)), (3, 4, F(1)),
    ]:
        matching[p][n] = mass

    source = [sum(row, F(0)) for row in matching]
    target = [
        sum((matching[p][n] for p in range(5)), F(0)) for n in range(5)
    ]
    assert all(x <= cap for x, cap in zip(source, positive))
    assert all(x <= cap for x, cap in zip(target, negative))
    assert negative[0] - target[0] == F(1, 8)
    assert negative[1] - target[1] == F(1, 8)
    unmatched = [cap - used for cap, used in zip(positive, source)]
    assert unmatched == [F(1, 8), F(1, 8), F(1, 4), F(0), F(0)]

    kernel = [[F(0) for _ in positive] for _ in positive]
    for p, n in mate.items():
        for destination in range(5):
            kernel[p][destination] = matching[destination][n] / negative[n]
    assert kernel[0][1] == kernel[1][0] == F(1, 2)
    assert kernel[3][4] == kernel[4][3] == 1
    pushed_capacity = push_kernel(kernel, positive)
    assert all(u + k <= cap for u, k, cap
               in zip(unmatched, pushed_capacity, positive))

    # Only the component reached from initial deficiency enters the minimal
    # Neumann solution. The independent closed cycle must retain zero flow.
    reachable = {p for p, mass in enumerate(unmatched) if mass}
    while True:
        enlarged = reachable | {
            j for i in reachable for j, mass in enumerate(kernel[i]) if mass
        }
        if enlarged == reachable:
            break
        reachable = enlarged
    indices = sorted(reachable)
    matrix = [
        [F(i == j) - kernel[j][i] for j in indices] for i in indices
    ]
    solution = solve_linear(matrix, [unmatched[i] for i in indices])
    xi = [F(0)] * 5
    for i, value in zip(indices, solution):
        xi[i] = value
    assert xi == [F(1, 2), F(1, 2), F(3, 8), F(0), F(0)]
    assert all(F(0) <= value <= cap for value, cap in zip(xi, positive))
    pushed_xi = push_kernel(kernel, xi)
    assert xi == [u + k for u, k in zip(unmatched, pushed_xi)]

    partial = [F(0)] * 5
    term = list(unmatched)
    for _ in range(12):
        partial = [x + y for x, y in zip(partial, term)]
        assert all(x <= y for x, y in zip(partial, xi))
        term = push_kernel(kernel, term)
    assert sum(term, F(0)) > 0  # A finite truncation is not the exact answer.

    retimed_fraction = [F(0)] * 5
    for p, n in mate.items():
        retimed_fraction[n] = xi[p] / negative[n]
    # n2 models an already protected unpaired negative tail. Matching
    # edges use it, but no paired reflection can select it for retiming.
    assert target[2] == F(3, 4)
    assert retimed_fraction[2] == 0
    removed = [
        [matching[p][n] * retimed_fraction[n] for n in range(5)]
        for p in range(5)
    ]
    removed_source = [sum(row, F(0)) for row in removed]
    assert removed_source == pushed_xi
    assert removed_source == [x - u for x, u in zip(xi, unmatched)]

    retained = [
        [matching[p][n] - removed[p][n] for n in range(5)]
        for p in range(5)
    ]
    for n in range(5):
        assert sum((retained[p][n] for p in range(5)), F(0)) <= (
            1 - retimed_fraction[n]
        ) * negative[n]
    updated = [row[:] for row in retained]
    for p, n in mate.items():
        updated[p][n] += xi[p]
    updated_source = [sum(row, F(0)) for row in updated]
    updated_target = [
        sum((updated[p][n] for p in range(5)), F(0)) for n in range(5)
    ]
    final_unmatched = [
        cap - used for cap, used in zip(positive, updated_source)
    ]
    assert final_unmatched == [F(0), F(0), F(3, 8), F(0), F(0)]
    assert all(x <= cap for x, cap in zip(updated_target, negative))
    assert sum(final_unmatched, F(0)) == F(3, 8)
    assert sum(final_unmatched, F(0)) < sum(unmatched, F(0))
    return {
        "initial_deficiency": str(sum(unmatched, F(0))),
        "tail_deficiency": str(sum(final_unmatched, F(0))),
        "closed_cycle_flow": str(xi[3] + xi[4]),
    }


def radial_interval(point):
    time, radius = point
    return time - radius, time + radius


def dominates(negative_point, positive_point):
    left_n, right_n = radial_interval(negative_point)
    left_p, right_p = radial_interval(positive_point)
    return left_n <= left_p and right_p <= right_n


def verify_atomic_front(q, residual):
    if any(not F(0) < t < F(1) or mass <= 0
           for t, mass in residual.items()):
        raise ValueError("Residual atoms must be strictly inside the front.")
    d = sum(residual.values(), F(0))
    if q < d / 2:
        raise ValueError("There is insufficient fast-sweep probability.")
    replacement = defaultdict(F)
    for t, mass in residual.items():
        replacement[t / 2] += mass / 2
    assert sum(replacement.values(), F(0)) == d / 2

    breakpoints = {F(0), F(1), *residual}
    for h in replacement:
        breakpoints.update([h, 2 * h])
        positive_atom = (F(0), 1 - 2 * h)
        for s in [F(0), h / 2, h]:
            assert dominates((s, 1 - 2 * h + s), positive_atom)
        assert dominates((h, 1 - h), positive_atom)
        # Exact pressure conservation and internal atom cancellation.
        prefix = h / 2
        freeze = (4 - h) / 2
        positive_atom_mass = h
        assert prefix + h / 2 == positive_atom_mass
        assert freeze - h / 2 == 2 - h

    checks = 0
    for a in sorted(breakpoints):
        for closed in [False, True]:
            def includes(x):
                return x <= a if closed else x < a
            removed = sum(
                (mass * min(a, 2 * h) / 2
                 for h, mass in replacement.items()), F(0)
            )
            gained = sum(
                (mass * (2 - h) for h, mass in replacement.items()
                 if includes(h)), F(0)
            )
            demand = sum(
                (mass for t, mass in residual.items() if includes(t)), F(0)
            )
            assert removed + gained >= demand
            checks += 1

    removed_total = sum(
        (mass * h for h, mass in replacement.items()), F(0)
    )
    gained_total = sum(
        (mass * (2 - h) for h, mass in replacement.items()), F(0)
    )
    assert removed_total + gained_total == d
    assert sum(replacement.values(), F(0)) / 2 <= q / 2
    assert 2 * sum(replacement.values(), F(0)) == d
    return checks


def value_at(vertices, time):
    for (ta, xa), (tb, xb) in zip(vertices, vertices[1:]):
        if ta <= time <= tb:
            return xa + (xb - xa) * (time - ta) / (tb - ta)
    raise ValueError("Time is outside the supplied physical path.")


def first_light_crossing(vertices):
    for (ta, xa), (tb, xb) in zip(vertices, vertices[1:]):
        ua, ub = ta + xa, tb + xb
        if ua >= 1:
            return ta
        if ub >= 1:
            return ta + (1 - ua) * (tb - ta) / (ub - ua)
    raise ValueError("The path never crosses U=1.")


def assert_legal(vertices):
    assert all(-1 <= x <= 1 for _, x in vertices)
    for (ta, xa), (tb, xb) in zip(vertices, vertices[1:]):
        assert ta < tb
        assert abs(xb - xa) <= tb - ta


def verify_boundary_turn(n):
    # The initial inward leg makes this more than a single monotone approach.
    old = [
        (F(0), F(3, 5)),
        (F(1, 5), F(2, 5)),
        (F(4, 5), F(1)),
        (F(14, 5), F(-1)),
    ]
    assert_legal(old)
    sigma = F(4, 5)
    h = first_light_crossing(old)
    assert h == F(2, 5)
    eta = min(F(1, n), (sigma - h) / 2)
    a = sigma - eta
    epsilon = 1 - value_at(old, a)
    assert 0 < epsilon <= eta <= F(1, n)
    assert h < a < sigma
    endpoint_time = a + 2 - epsilon
    new = [v for v in old if v[0] < a] + [
        (a, 1 - epsilon),
        (endpoint_time, F(-1)),
        (endpoint_time + 2, F(1)),
    ]
    assert_legal(new)
    assert endpoint_time >= sigma + 1
    assert all(abs(x) < 1 for _, x in new[:-2])
    assert value_at(new, h) == 1 - h
    # The new first-plus representative is the reflection of this path.
    # Its ENTIRE unpaired tail is in the newly frozen negative pool.
    for scoring_time in [
        endpoint_time,
        endpoint_time + F(1, 3),
        endpoint_time + F(3, 2),
    ]:
        selected_time = h
        selected_position = -value_at(new, h)
        assert a <= scoring_time < endpoint_time + 2
        assert selected_time < a <= scoring_time
        assert selected_position < 0
        paired = scoring_time < endpoint_time
        uncovered_positive = selected_position > 0
        assert not paired and not uncovered_positive

    times = {F(0), h, a, endpoint_time}
    times.update(t for t, _ in old if t <= endpoint_time)
    times.update(t for t, _ in new if t <= endpoint_time)
    ordered = sorted(times)
    times.update((x + y) / 2 for x, y in zip(ordered, ordered[1:]))
    for s in sorted(times):
        old_x, new_x = value_at(old, s), value_at(new, s)
        assert new_x <= old_x
        if s <= a:
            assert new_x == old_x
        if old_x < 0:
            assert new_x < 0
            assert dominates((s, -new_x), (s, -old_x))
        if new_x > 0:
            assert old_x > 0
            assert dominates((s, old_x), (s, new_x))

    deleted_original = (eta + epsilon) / 2
    deleted_reflected = eta / 2
    fresh_negative = (4 - epsilon) / 2
    baseline_gain = 2 - eta - epsilon
    assert fresh_negative - deleted_original - deleted_reflected == baseline_gain
    old_baseline = (sigma + sigma + 2) / 2
    new_baseline = (endpoint_time + endpoint_time + 2) / 2
    assert new_baseline - old_baseline == baseline_gain

    for residual in [F(1, 7), F(3, 8), F(1, 2)]:
        gamma = residual / 2
        assert gamma <= F(1, 4)
        old_residual_left = residual - gamma * fresh_negative
        assert old_residual_left == gamma * epsilon / 2
        possible_lost_capacity = gamma * (
            deleted_original + deleted_reflected
        )
        remaining_bound = old_residual_left + possible_lost_capacity
        assert remaining_bound == gamma * (eta + epsilon)
        assert remaining_bound <= residual / n
        assert gamma * baseline_gain + remaining_bound == residual
    return len(times)


def main():
    cycle = verify_fractional_resource_cycle()
    atomic_cases = [
        (F(0), {}),
        (F(1, 10), {F(1, 7): F(1, 20), F(2, 3): F(3, 20)}),
        (F(3, 7), {
            F(1, 1000000): F(1, 7),
            F(999999, 1000000): F(1, 7),
        }),
        (F(1, 4), {F(1, 3): F(1, 8), F(2, 3): F(1, 8)}),
    ]
    front_checks = sum(
        verify_atomic_front(q, residual) for q, residual in atomic_cases
    )
    for q, residual in [
        (F(1), {F(0): F(1, 2)}),
        (F(1), {F(1): F(1, 2)}),
        (F(1, 10), {F(1, 2): F(1, 2)}),
    ]:
        try:
            verify_atomic_front(q, residual)
        except ValueError:
            pass
        else:
            raise AssertionError("An invalid completion input was accepted.")
    geometry_checks = sum(verify_boundary_turn(n) for n in [2, 3, 10, 100])
    print("PASS: exact global pressure-localization regressions")
    print("Fractional cycle:", cycle)
    print("Atomic front cumulative checks:", front_checks)
    print("Boundary-turn physical geometry checks:", geometry_checks)
    print("Boundary-turn baseline plus deficiency: conserved exactly")


if __name__ == "__main__":
    main()
