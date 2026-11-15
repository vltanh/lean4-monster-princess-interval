#!/usr/bin/env python3
"""Exact algebra and polytope regressions for the four-leg record theorem."""

from fractions import Fraction as Q
from itertools import combinations


def solve(matrix, rhs):
    size = len(rhs)
    rows = [list(row) + [bound] for row, bound in zip(matrix, rhs)]
    for col in range(size):
        pivot = next((i for i in range(col, size) if rows[i][col]), None)
        if pivot is None:
            return None
        rows[col], rows[pivot] = rows[pivot], rows[col]
        divisor = rows[col][col]
        rows[col] = [x / divisor for x in rows[col]]
        for i in range(size):
            if i == col:
                continue
            multiplier = rows[i][col]
            rows[i] = [x - multiplier * y for x, y in zip(rows[i], rows[col])]
    return tuple(row[-1] for row in rows)


def dot(row, point):
    return sum((a * b for a, b in zip(row, point)), Q(0))


def polytope_vertices(partial, a, b, B, H, budget):
    dimension = len(partial)
    if not dimension:
        return [()]
    rows, bounds = [], []
    for i in range(dimension):
        lower, upper = (b, H) if i % 2 == 0 else (a, B)
        unit = tuple(Q(j == i) for j in range(dimension))
        rows += [unit, tuple(-x for x in unit)]
        bounds += [upper, -lower]
        if i >= 2:
            rows.append(tuple(Q(j == i - 2) - Q(j == i) for j in range(dimension)))
            bounds.append(Q(0))
    rows.append((Q(1),) * dimension)
    bounds.append(budget)
    vertices = set()
    for active in combinations(range(len(rows)), dimension):
        point = solve([rows[i] for i in active], [bounds[i] for i in active])
        if point is not None and all(dot(row, point) <= bound
                                     for row, bound in zip(rows, bounds)):
            vertices.add(point)
    return sorted(vertices)


def full_turns(partial, B, H):
    return tuple(partial) + ((H, B) if len(partial) % 2 == 0 else (B, H))


def extra_cost(partial, a, B, H):
    turns = full_turns(partial, B, H)
    result = turns[0] * (B - a)
    for i in range(1, len(turns)):
        first, second = turns[i - 1:i + 1]
        result += (first + second) * (
            (H - first) if i % 2 else (B - first)
        )
    return result


def analytic_cost(partial, a, b, B, H, alpha, beta):
    direct = (H * H - b * b) / (2 * alpha)
    direct += (B * B - a * a) / (2 * beta)
    return direct + (1 / alpha + 1 / beta) * extra_cost(partial, a, B, H)


def signed_turns(partial, B, H):
    return [magnitude if i % 2 == 0 else -magnitude
            for i, magnitude in enumerate(full_turns(partial, B, H))]


def range_integral(points, a, b, alpha, beta, horizon):
    low, high, position, time, result = -a, b, Q(0), Q(0), Q(0)
    for destination in points:
        if destination == position:
            continue
        velocity = alpha if destination > position else -beta
        duration = (destination - position) / velocity
        cuts = {Q(0), duration}
        for record in (low, high):
            crossing = (record - position) / velocity
            if 0 < crossing < duration:
                cuts.add(crossing)
        ordered = sorted(cuts)
        for left, right in zip(ordered, ordered[1:]):
            y_left = position + velocity * left
            y_right = position + velocity * right
            r_left = max(high, y_left) - min(low, y_left)
            r_right = max(high, y_right) - min(low, y_right)
            result += (r_left + r_right) * (right - left) / 2
        low, high = min(low, destination), max(high, destination)
        position = destination
        time += duration
    assert time <= horizon
    result += (horizon - time) * (high - low)
    return result, low, high, time


def compress(turns, final, a, b):
    low, high = -a, b
    records = []
    for value in turns:
        if value < low or value > high:
            records.append(value)
            low, high = min(low, value), max(high, value)
    points = [Q(0)]
    for value in records + [final]:
        if value == points[-1]:
            continue
        if len(points) >= 2 and (value - points[-1]) * (points[-1] - points[-2]) > 0:
            points[-1] = value
        else:
            points.append(value)
    return points[1:]


def check_case(a, b, B, H, alpha, beta, final, partial):
    partial = tuple(partial)
    kappa = 1 / alpha + 1 / beta
    budget = sum(partial, Q(0))
    last_is_right = len(full_turns(partial, B, H)) % 2 == 1
    base_time = kappa * (B + H) + (
        -final / beta if last_is_right else final / alpha
    )
    horizon = base_time + kappa * budget
    area, low, high, elapsed = range_integral(
        signed_turns(partial, B, H) + [final], a, b, alpha, beta, horizon
    )
    assert elapsed == horizon
    assert (low, high) == (-B, H)
    original_cost = horizon * (B + H) - area
    assert original_cost == analytic_cost(partial, a, b, B, H, alpha, beta)

    # The independent chronological integral checks the polynomial, and its
    # finite differences check every Hessian entry, not only one coordinate.
    e0 = extra_cost(partial, a, B, H)
    for i in range(len(partial)):
        plus, minus = list(partial), list(partial)
        plus[i] += 1
        minus[i] -= 1
        assert extra_cost(plus, a, B, H) + extra_cost(minus, a, B, H) - 2 * e0 == -2
        for j in range(i + 1, len(partial)):
            pi, pj, both = list(partial), list(partial), list(partial)
            pi[i] += 1
            pj[j] += 1
            both[i] += 1
            both[j] += 1
            mixed = (extra_cost(both, a, B, H) - extra_cost(pi, a, B, H)
                     - extra_cost(pj, a, B, H) + e0)
            assert mixed == (-1 if j == i + 1 else 0)

    vertices = polytope_vertices(partial, a, b, B, H, budget)
    assert vertices
    for vertex in vertices:
        interior_blocks = 0
        for parity, lower, upper in ((0, b, H), (1, a, B)):
            previous = None
            for value in vertex[parity::2]:
                if lower < value < upper and value != previous:
                    interior_blocks += 1
                previous = value
        assert interior_blocks <= 1
        candidate_turns = signed_turns(vertex, B, H)
        candidate_area, lo, hi, _ = range_integral(
            candidate_turns + [final], a, b, alpha, beta, horizon
        )
        assert (lo, hi) == (-B, H)
        assert horizon * (B + H) - candidate_area == analytic_cost(
            vertex, a, b, B, H, alpha, beta
        )
        shortened = compress(candidate_turns, final, a, b)
        assert len(shortened) <= 4
        shorter_area, lo, hi, _ = range_integral(
            shortened, a, b, alpha, beta, horizon
        )
        assert (lo, hi) == (-B, H)
        assert shorter_area >= candidate_area
    best = min(analytic_cost(v, a, b, B, H, alpha, beta) for v in vertices)
    assert best <= original_cost
    direct = (H * H - b * b) / (2 * alpha) + (B * B - a * a) / (2 * beta)
    low_time = kappa * (B + H) - final / beta
    high_time = kappa * (B + H) + final / alpha
    explicit = []
    if low_time <= horizon:
        explicit.append(([-B, H, final], direct + kappa * B * (H - b)))
    if high_time <= horizon:
        explicit.append(([H, -B, final], direct + kappa * H * (B - a)))
    right = (horizon - low_time) / kappa
    if b <= right <= H:
        explicit.append((
            [right, -B, H, final],
            direct + kappa * (B * H + right * (H - a) - right * right),
        ))
    left = (horizon - high_time) / kappa
    if a <= left <= B:
        explicit.append((
            [-left, H, -B, final],
            direct + kappa * (B * H + left * (B - b) - left * left),
        ))
    assert explicit
    for route, predicted in explicit:
        candidate_area, lo, hi, _ = range_integral(
            route, a, b, alpha, beta, horizon
        )
        assert (lo, hi) == (-B, H)
        assert horizon * (B + H) - candidate_area == predicted
    assert min(cost for _, cost in explicit) <= best
    return len(vertices)


def boundary_projection_checks():
    # A legal affine field on a positive boundary half-cell, with a
    # decreasing endpoint trace. The hypothetical path briefly exceeds1,
    # while its field value remains inside the actual entry record interval.
    start_t, start_x = Q(13, 20), Q(19, 20)
    turn_t, turn_x = Q(31, 40), Q(43, 40)
    end_t, end_x = Q(9, 10), Q(19, 20)

    def hypothetical(t):
        return start_x + t - start_t if t <= turn_t else turn_x - (t - turn_t)

    def field(t, x):
        return Q(1, 2) + x / 5 - t / 10

    knots = [start_t, Q(7, 10), turn_t, Q(17, 20), end_t]
    knots += [(a + b) / 2 for a, b in zip(knots, knots[1:])]
    for t in sorted(knots):
        x = hypothetical(t)
        clipped = min(Q(1), max(Q(-1), x))
        y = field(t, x)
        assert Q(3, 5) <= y <= Q(7, 10)
        assert Q(3, 2) <= t + clipped <= 2
        assert Q(-1, 2) <= t - clipped <= 0
        if x > 1:
            assert field(t, 1) <= y <= 1
            reflected_y = 1 - y
            assert 0 <= reflected_y <= 1 - field(t, 1)
        else:
            assert field(t, clipped) == y
    assert hypothetical(start_t) == start_x and hypothetical(end_t) == end_x
    return len(knots)


def main():
    cases = [
        (Q(1), Q(1), Q(3), Q(4), Q(2), Q(3), Q(0), ()),
        (Q(19, 100), Q(0), Q(1, 5), Q(1, 100), Q(1), Q(1),
         Q(1, 200), (Q(1, 1000),)),
        (Q(1, 5), Q(1, 10), Q(1), Q(3, 2), Q(3), Q(2),
         Q(2, 5), (Q(3, 10), Q(2, 5))),
        (Q(1), Q(1), Q(3), Q(4), Q(2), Q(3), Q(-1),
         (Q(3, 2), Q(3, 2), Q(5, 2))),
        (Q(1), Q(1), Q(3), Q(4), Q(3), Q(2), Q(1),
         (Q(3, 2), Q(3, 2), Q(5, 2), Q(2))),
    ]
    vertex_count = sum(check_case(*case) for case in cases)
    a, b, B, H, alpha, beta, final, partial = cases[1]
    horizon = Q(417, 1000)
    original = range_integral(
        signed_turns(partial, B, H) + [final], a, b, alpha, beta, horizon
    )[0]
    low_first = range_integral([-B, H, final], a, b, alpha, beta, horizon)[0]
    high_first_time = H / alpha + (H + B) / beta + (B + final) / alpha
    assert original == Q(20483, 250000)
    assert low_first == Q(8157, 100000)
    assert high_first_time == Q(425, 1000) > horizon
    assert original - low_first == Q(181, 500000)
    projection_count = boundary_projection_checks()
    print("PASS: exact chronological first-visit and quadratic formulas")
    print("PASS:", vertex_count, "rational polytope vertices and four-leg compressions")
    print("PASS: full Hessian, including adjacent cross terms")
    print("PASS: explicit four-candidate quadratic envelope")
    print("PASS: strict four-versus-three-leg counterexample", original - low_first)
    print("PASS:", projection_count, "strict/inclusive boundary projection checks")


if __name__ == "__main__":
    main()
