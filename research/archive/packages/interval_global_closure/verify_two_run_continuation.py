#!/usr/bin/env python3
"""Exact regressions for the affine-cell two-run continuation theorem.

Uses only the standard library.  Chronological record integration is
independent of the first-visit formulas in the proof.
"""

from fractions import Fraction as Q
from itertools import combinations
import json
import random


def records(legs, alpha, beta, a, b):
    """Return (duration, final position, range integral, lower depth, upper)."""
    y, lower, upper = Q(0), -a, b
    duration, area = Q(0), Q(0)
    for direction, dt in legs:
        speed = alpha if direction == 1 else -beta
        end = y + speed * dt
        area += (upper - lower) * dt
        if speed > 0:
            expansion = max(Q(0), end - upper)
            area += expansion * expansion / (2 * speed)
            upper = max(upper, end)
        elif speed < 0:
            expansion = max(Q(0), lower - end)
            area += expansion * expansion / (-2 * speed)
            lower = min(lower, end)
        y = end
        duration += dt
    return duration, y, area, -lower, upper


def pure_paths(legs, alpha, beta, a, b):
    up = sum((dt for direction, dt in legs if direction == 1), Q(0))
    down = sum((dt for direction, dt in legs if direction == -1), Q(0))
    return (
        records(((1, up), (-1, down)), alpha, beta, a, b),
        records(((-1, down), (1, up)), alpha, beta, a, b),
    )


def hull_dominates(original, pure_up, pure_down):
    """Check a pure-order mixture dominates both exit records and area."""
    lo, hi = Q(0), Q(1)
    for j in (3, 4):
        slope = pure_up[j] - pure_down[j]
        needed = original[j] - pure_down[j]
        if slope > 0:
            lo = max(lo, needed / slope)
        elif slope < 0:
            hi = min(hi, needed / slope)
        else:
            assert needed <= 0
    assert lo <= hi
    best_area = max(
        lo * pure_up[2] + (1 - lo) * pure_down[2],
        hi * pure_up[2] + (1 - hi) * pure_down[2],
    )
    assert best_area >= original[2]


def local_cost(r, B, H, a, b, p, q, total):
    k = p + q
    return (
        total
        - total * (B + H)
        + (p * (H * H - b * b) + q * (B * B - a * a)) / 2
        + k * (B * H + r * (H - a) - r * r)
    )


def check_hessian():
    count = 0
    for p, q in ((Q(1), Q(1)), (Q(2), Q(3)), (Q(3, 7), Q(11, 5))):
        S, a, b, total = Q(11), Q(1, 3), Q(2, 5), Q(17)
        r, B, h = Q(2), Q(3), Q(1, 7)

        def value(x, y):
            return local_cost(x, y, S - x - y, a, b, p, q, total)

        rr = (value(r + h, B) + value(r - h, B) - 2 * value(r, B)) / h**2
        BB = (value(r, B + h) + value(r, B - h) - 2 * value(r, B)) / h**2
        cross = (
            value(r + h, B + h)
            - value(r + h, B)
            - value(r, B + h)
            + value(r, B)
        ) / h**2
        assert rr == -3 * p - 4 * q
        assert BB == -p - q
        assert cross == -p - 2 * q
        assert rr * BB - cross**2 == p * (2 * p + 3 * q) > 0
        count += 4
    return count


def vertices2(inequalities):
    """Each exact halfspace is c0+c1*x+c2*y >= 0."""
    points = set()
    for first, second in combinations(inequalities, 2):
        c0, c1, c2 = first
        d0, d1, d2 = second
        determinant = c1 * d2 - c2 * d1
        if determinant == 0:
            continue
        x = (-c0 * d2 + c2 * d0) / determinant
        y = (-c1 * d0 + c0 * d1) / determinant
        if all(a0 + a1 * x + a2 * y >= 0 for a0, a1, a2 in inequalities):
            points.add((x, y))
    return points


def check_vertices():
    count = 0
    for a, b, f, S in (
        (Q(0), Q(0), Q(1), Q(7)),
        (Q(1), Q(2), Q(1), Q(9)),
        (Q(1, 3), Q(2, 7), Q(8, 7), Q(31, 7)),
        (Q(4, 5), Q(3, 2), Q(0), Q(7)),
    ):
        right = (
            (-b, Q(1), Q(0)),
            (-a, Q(0), Q(1)),
            (S, Q(-2), Q(-1)),
            (S - f, Q(-1), Q(-1)),
        )
        for r, B in vertices2(right):
            H = S - r - B
            assert r == b or r == H or B == a
            count += 1
        left = (
            (-a, Q(1), Q(0)),
            (-max(b, f), Q(0), Q(1)),
            (S, Q(-2), Q(-1)),
        )
        for l, H in vertices2(left):
            B = S - l - H
            assert l == a or l == B
            count += 1
    return count


def check_terminal_excursion():
    count = 0
    for p, q in ((Q(1), Q(1)), (Q(2), Q(3)), (Q(3, 7), Q(11, 5))):
        for a, b, f, spare in (
            (Q(0), Q(0), Q(1), Q(0)),
            (Q(1, 3), Q(2, 7), Q(5, 7), Q(1, 2)),
            (Q(3), Q(1), Q(2), Q(4)),
            (Q(0), Q(9, 10), Q(1), Q(7, 3)),
        ):
            C = a + f + spare
            A = C + f
            total = p * A + q * C
            up = records(((1, p * A), (-1, q * C)), 1 / p, 1 / q, a, b)
            down = records(((-1, q * C), (1, p * A)), 1 / p, 1 / q, a, b)
            excursion = records(
                ((1, p * f), (-1, q * C), (1, p * C)),
                1 / p,
                1 / q,
                a,
                b,
            )
            assert all(s[0] == total and s[1] == f for s in (up, down, excursion))
            theta = f / C
            actual = C * (theta * up[2] + (1 - theta) * down[2] - excursion[2])
            expected = (
                (p + q) * b * C * (C - f)
                + p * f * C * C / 2
                + q * f * (C * C - a * a) / 2
                + q * f * f * C / 2
                + p * a * f * f
            )
            assert actual == expected >= 0
            assert theta * up[3] + (1 - theta) * down[3] >= excursion[3]
            assert theta * up[4] + (1 - theta) * down[4] >= excursion[4]
            count += 1
    return count


def check_words():
    count = 0
    for nup in range(1, 5):
        for ndn in range(1, 5):
            n = nup + ndn
            for alpha, beta in ((Q(1), Q(1)), (Q(1), Q(2)), (Q(2), Q(1)), (Q(2), Q(3))):
                for a, b in ((Q(0), Q(0)), (Q(0), Q(1)), (Q(1), Q(0)), (Q(1), Q(2)), (Q(2), Q(1))):
                    for ups in combinations(range(n), nup):
                        directions = [-1] * n
                        for i in ups:
                            directions[i] = 1
                        legs = tuple((direction, Q(1)) for direction in directions)
                        original = records(legs, alpha, beta, a, b)
                        up, down = pure_paths(legs, alpha, beta, a, b)
                        hull_dominates(original, up, down)
                        count += 1
    return count


def check_random_continuations():
    rng = random.Random(20261113)
    count = 0
    for _ in range(1200):
        alpha, beta = Q(rng.randint(1, 9), rng.randint(1, 7)), Q(rng.randint(1, 9), rng.randint(1, 7))
        a, b = Q(rng.randint(0, 8), 3), Q(rng.randint(0, 8), 3)
        legs = tuple(
            (rng.choice((-1, 1)), Q(rng.randint(1, 8), rng.randint(1, 9)))
            for _ in range(rng.randint(2, 10))
        )
        original = records(legs, alpha, beta, a, b)
        up, down = pure_paths(legs, alpha, beta, a, b)
        hull_dominates(original, up, down)
        # A minimum of affine decreasing functions is concave and decreasing.
        planes = tuple(
            (Q(rng.randint(-9, 9), 3), Q(rng.randint(0, 9), 3), Q(rng.randint(0, 9), 3))
            for _ in range(4)
        )

        def full_cost(s):
            continuation = min(offset - left * s[3] - right * s[4] for offset, left, right in planes)
            return s[0] - s[2] + continuation

        assert min(full_cost(up), full_cost(down)) <= full_cost(original)
        count += 1
    return count


def main():
    result = {
        "hessian_identities": check_hessian(),
        "vertex_reductions": check_vertices(),
        "terminal_excursion_identities": check_terminal_excursion(),
        "exhaustive_unit_word_mixtures": check_words(),
        "rational_continuation_cases": check_random_continuations(),
    }
    print(json.dumps({"status": "PASS", **result}, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
