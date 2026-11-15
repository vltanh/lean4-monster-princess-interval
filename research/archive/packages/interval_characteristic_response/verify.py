"""Exact first-capture checks for the M1/M2 characteristic formulas.

Uses only Python's standard library and fractions.Fraction. The reference
calculation intersects the actual piecewise-linear paths directly; it does
not use a characteristic classification or a threshold branch formula.
"""

from fractions import Fraction as F
from random import Random


def clean(path):
    out = []
    for t, x in path:
        t, x = F(t), F(x)
        if out and t == out[-1][0]:
            assert x == out[-1][1]
        else:
            out.append((t, x))
    return out


def at(path, t):
    for (a, x), (b, y) in zip(path, path[1:]):
        if a <= t <= b:
            return x + (y - x) * (t - a) / (b - a)
    assert t >= path[-1][0]
    return path[-1][1]


def direct_capture(monster, princess):
    """Reference: first zero of the difference on common linear pieces."""
    times = sorted({t for t, _ in monster + princess})
    previous = None
    for t in times:
        difference = at(monster, t) - at(princess, t)
        if difference == 0:
            return t
        if previous is not None:
            old_t, old_difference = previous
            if difference * old_difference < 0:
                return old_t + (t - old_t) * abs(old_difference) / (
                    abs(old_difference) + abs(difference))
        previous = (t, difference)
    raise AssertionError("The supplied monster must capture by time four")


def inverse(princess, c, sign, strict=False):
    """First >= inverse, or infimum of > times for the plateau endpoint."""
    c = F(c)
    values = [(t, t + sign * x) for t, x in princess]
    if values[0][1] > c or (not strict and values[0][1] == c):
        return F(0)
    for (a, u), (b, v) in zip(values, values[1:]):
        if v > c or (not strict and v == c):
            if u == c:
                return a
            assert u < c <= v and v > u
            return a + (b - a) * (c - u) / (v - u)
    t, value = values[-1]
    return t + c - value


def monster_path(family, x):
    if family == 1:
        return clean([(0, x), (1-x, 1), (3-x, -1), (4, -1)])
    return clean([(0, x), ((1-x)/2, (1+x)/2), (2, -1), (4, 1)])


def predicted(princess, family, x, reflected):
    a = princess[0][1]
    A = lambda c: inverse(princess, c, 1)
    B = lambda c: inverse(princess, c, -1)
    if reflected:
        if x < -a:
            return A(-x)
        if x == -a:
            return F(0)
        return B(2-x) if family == 1 else B(1)
    if x == a:
        return F(0)
    if family == 1:
        return B(-x) if x < a else A(2-x)
    if x > a:
        return A(1)
    e = inverse(princess, 1, 1, strict=True)
    cutoff = 1 - 2*e
    return B(3) if x < cutoff else B(-x)


def check(princess):
    assert princess[0][0] == 0 and princess[-1][0] == 4
    assert all(0 <= x <= 1 for _, x in princess)
    assert all(abs(y-x) <= b-a for (a,x),(b,y)
               in zip(princess,princess[1:]))
    a = princess[0][1]
    s = inverse(princess, 1, 1)
    e = inverse(princess, 1, 1, strict=True)
    assert 0 <= s <= e <= 1
    cutoff = 1 - 2*e
    assert -1 <= cutoff <= a
    starts = {F(j, 8) for j in range(-8, 9)} | {a, -a, cutoff, 1-2*s}
    count = 0
    for x in starts:
        for family in (1, 2):
            original = monster_path(family, x)
            for reflected in (False, True):
                path = ([(t,-y) for t,y in original]
                        if reflected else original)
                expected = predicted(princess, family, x, reflected)
                actual = direct_capture(path, princess)
                assert actual == expected, (princess, family, x, reflected,
                                            actual, expected)
                count += 1
    return count


def main():
    plateau = clean([(0,F(1,2)),(F(1,2),F(1,2)),(1,0),(4,0)])
    early = clean([(0,F(1,4)),(F(1,4),F(1,4)),(1,1),(4,1)])
    assert direct_capture(monster_path(2,F(-1,4)),plateau) == F(5,8)
    assert direct_capture(monster_path(2,0),early) == F(1,4)
    fixtures = [plateau, early, clean([(0,0),(4,0)]),
                clean([(0,1),(4,1)]), clean([(0,1),(1,0),(4,0)]),
                clean([(0,0),(1,1),(2,0),(3,1),(4,0)])]
    count = sum(check(path) for path in fixtures)
    rng = Random(20261110)
    for _ in range(200):
        position = rng.randrange(9)
        path = [(F(0),F(position,8))]
        for step in range(1,33):
            choices = [position+d for d in (-1,0,1) if 0<=position+d<=8]
            position = rng.choice(choices)
            path.append((F(step,8),F(position,8)))
        count += check(path)
    print(f"PASS: {count} exact direct intersections match all four formulas.")
    print("PASS: initial equalities, both plateau endpoints, and cutoff equality.")
    print("PASS: explicit s-versus-e counterexample captures at 5/8, not 3.")


if __name__ == "__main__":
    main()
