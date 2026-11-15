#!/usr/bin/env python3
"""Exact physical-contact regression for the global 3/4/7 horizon theorem.

This checks the domination arguments on rational polygonal paths. It does
not mechanically certify the global minimax, quantile, or compactness
theorems used in GLOBAL_EXACT_HORIZON_REDUCTION.md.
"""
from fractions import Fraction as Q


ZERO, ONE = Q(0), Q(1)
H = Q(3)
FINAL = Q(10)
STEP = Q(1, 2)
PREFIX_TIMES = [STEP * i for i in range(7)]


def value(path, t):
    for (a, x), (b, y) in zip(path, path[1:]):
        if a <= t <= b:
            return x + (t - a) * (y - x) / (b - a)
    raise AssertionError(("time not covered", t))


def legal(path, radial=False):
    assert path[0][0] == ZERO and path[-1][0] == FINAL
    for (a, x), (b, y) in zip(path, path[1:]):
        assert a < b
        assert (-ONE if not radial else ZERO) <= x <= ONE
        assert (-ONE if not radial else ZERO) <= y <= ONE
        assert abs(y - x) <= b - a


def first_contact(first, second, start=ZERO):
    events = sorted({start, FINAL} | {t for t, _ in first if t >= start}
                    | {t for t, _ in second if t >= start})
    for a, b in zip(events, events[1:]):
        da = value(first, a) - value(second, a)
        db = value(first, b) - value(second, b)
        if da == ZERO:
            return a
        if da * db <= ZERO:
            return a - da * (b - a) / (db - da)
    if value(first, FINAL) == value(second, FINAL):
        return FINAL
    raise AssertionError("completed fixture has no required contact")


def constant(x):
    return [(ZERO, x), (FINAL, x)]


def reflect(path):
    return [(t, -x) for t, x in path]


def walks(levels, length):
    rows = [(x,) for x in levels]
    for _ in range(length - 1):
        rows = [row + (y,) for row in rows for y in levels
                if abs(y - row[-1]) <= STEP]
    return rows


def sampled(rows, maximum):
    # Include the first and last rows, with deterministic coverage between.
    stride = max(1, len(rows) // maximum)
    return sorted(set(rows[::stride] + [rows[-1]]))


def append_point(path, t, x):
    if t == path[-1][0]:
        assert x == path[-1][1]
    else:
        path.append((t, x))


def endpoint_tour(prefix, endpoint):
    """Preserve the prefix through H, then use one of the two exact tours."""
    path = [(t, x) for t, x in prefix if t <= H]
    x = value(prefix, H)
    if path[-1][0] < H:
        path.append((H, x))
    first_time = H + abs(endpoint - x)
    append_point(path, first_time, endpoint)
    append_point(path, first_time + 2, -endpoint)
    append_point(path, FINAL, -endpoint)
    legal(path)
    assert first_time + 2 <= H + 4
    return path


def outward(radius):
    path = [(t, x) for t, x in radius if t <= H]
    x = value(radius, H)
    if path[-1][0] < H:
        path.append((H, x))
    append_point(path, H + 1 - x, ONE)
    append_point(path, FINAL, ONE)
    legal(path, radial=True)
    assert value(path, H + 1) == ONE
    return path


def monster_fixture(row, index):
    path = list(zip(PREFIX_TIMES, row))
    # Nontrivial old continuations: waits, reversals, then endpoint visits.
    for j in range(4):
        t, x = path[-1]
        direction = (-1, 0, 1, -1, 1)[(index + j) % 5]
        y = max(-ONE, min(ONE, x + STEP * direction))
        path.append((t + STEP, y))
    t, x = path[-1]
    endpoint = ONE if index % 2 else -ONE
    append_point(path, t + abs(endpoint - x), endpoint)
    append_point(path, path[-1][0] + 2, -endpoint)
    append_point(path, FINAL, -endpoint)
    legal(path)
    return path


def radius_fixture(row, index):
    path = list(zip(PREFIX_TIMES, row))
    for j in range(14):
        t, x = path[-1]
        direction = (-1, 0, 1, 1, 0, -1)[(index + j) % 6]
        y = max(ZERO, min(ONE, x + STEP * direction))
        path.append((t + STEP, y))
    legal(path, radial=True)
    return path


monster_rows = sampled(walks([Q(i, 2) for i in range(-2, 3)], 7), 96)
radius_rows = sampled(walks([ZERO, STEP, ONE], 7), 12)
monsters = [monster_fixture(row, i) for i, row in enumerate(monster_rows)]
radii = [radius_fixture(row, i) for i, row in enumerate(radius_rows)]
pairs = [(r, reflect(r), outward(r), reflect(outward(r))) for r in radii]
outward_paths = [p for _, _, plus, minus in pairs for p in (plus, minus)]
zero_path = constant(ZERO)

center_barriers = outward_comparisons = normalized_comparisons = 0
avoid_center_barriers = endpoint_only_checks = tail_formula_checks = 0
for monster in monsters:
    center_time = first_contact(monster, zero_path)
    x = value(monster, H)
    if center_time <= H:
        post_plus = first_contact(monster, constant(ONE), H)
        post_minus = first_contact(monster, constant(-ONE), H)
        first_endpoint = ONE if post_plus < post_minus else -ONE
        normalized = endpoint_tour(monster, first_endpoint)
        assert first_contact(normalized, zero_path) == center_time

    for old_plus, old_minus, new_plus, new_minus in pairs:
        old_hits = [first_contact(monster, p) for p in (old_plus, old_minus)]
        new_hits = [first_contact(monster, p) for p in (new_plus, new_minus)]
        assert sum(old_hits) / 2 >= center_time / 2
        center_barriers += 1
        if center_time <= H:
            for sign, old_hit, new_hit, new_path in zip(
                (ONE, -ONE), old_hits, new_hits, (new_plus, new_minus)
            ):
                assert new_hit >= old_hit
                outward_comparisons += 1
                if new_hit > H:
                    assert new_hit == (post_plus if sign > ZERO else post_minus)
                    endpoint_only_checks += 1
                assert first_contact(normalized, new_path) <= new_hit
                normalized_comparisons += 1
        else:
            assert x != ZERO
            assert sum(new_hits) / 2 >= (H + abs(x)) / 2 > H / 2
            avoid_center_barriers += 1

    if center_time <= H:
        hits = [first_contact(monster, p) for p in outward_paths]
        count = len(outward_paths)
        prefix_cost = sum((min(t, H) for t in hits), ZERO) / count
        w_plus = Q(sum(hits[j] > H for j in range(0, count, 2)), count)
        w_minus = Q(sum(hits[j] > H for j in range(1, count, 2)), count)
        formula_minus = prefix_cost + w_minus * (x + 1) + w_plus * (x + 3)
        formula_plus = prefix_cost + w_plus * (1 - x) + w_minus * (3 - x)
        actual_costs = []
        for endpoint, formula in ((-ONE, formula_minus), (ONE, formula_plus)):
            tour = endpoint_tour(monster, endpoint)
            actual = sum((first_contact(tour, p) for p in outward_paths), ZERO) / count
            assert actual == formula
            actual_costs.append(actual)
            tail_formula_checks += 1
        assert min(actual_costs) <= sum(hits, ZERO) / count

print(f"PASS: {len(monsters)} Monster paths and {len(radii)} reflected radial pairs.")
print(f"Center lower bounds: {center_barriers}; strict center-avoidance barriers: {avoid_center_barriers}.")
print(f"Outward first-contact domination: {outward_comparisons}; endpoint-only captures: {endpoint_only_checks}.")
print(f"Universal tail normalization: {normalized_comparisons}; exact weighted tour formulas: {tail_formula_checks}.")
print("Scope: exact physical-contact fixtures; global horizon/minimax proof remains analytic.")
