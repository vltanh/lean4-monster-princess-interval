"""Fraction physical first-contact audit of the exact fixed-start runner response."""
from fractions import Fraction as Q


def position(path, t):
    for (a, x), (b, y) in zip(path, path[1:]):
        if a <= t <= b:
            return x + (y - x) * (t - a) / (b - a)
    return path[-1][1]


def hit(monster, princess):
    knots = sorted({t for t, _ in monster + princess})
    for a, b in zip(knots, knots[1:]):
        da = position(monster, a) - position(princess, a)
        db = position(monster, b) - position(princess, b)
        if da == 0:
            return a
        if da * db < 0 or db == 0:
            return a + (b - a) * (-da) / (db - da)
    raise AssertionError("No physical contact")


def runners(a):
    left = [(Q(0), -a), (a + 1, Q(1)), (Q(4), Q(1))]
    return left, [(t, -x) for t, x in left]


def response(a, x):
    if x >= 0:
        t = (a - x) / 2
        m = [(Q(0), x), (t, x + t), (a, Q(0)),
             (a + 1, -Q(1)), (a + 3, Q(1))]
    else:
        t = (a + x) / 2
        m = [(Q(0), x), (t, x - t), (a, Q(0)),
             (a + 1, Q(1)), (a + 3, -Q(1))]
    return [v for i, v in enumerate(m) if i == 0 or v[0] != m[i-1][0]]


def main():
    count = 0
    for a in [Q(1, 2), Q(3, 4), Q(7, 8)]:
        pL, pR = runners(a)
        for k in range(-8, 9):
            x = Q(k, 8)
            if abs(x) > a:
                continue
            m = response(a, x)
            assert all(b > aa and abs(y - xx) <= b - aa
                       for (aa, xx), (b, y) in zip(m, m[1:]))
            assert (hit(m, pL) + hit(m, pR))/2 == (3*a - abs(x))/4
            count += 1
    assert count == 37
    print(f"PASS: {count} exact physical fixed-start response fixtures")


if __name__ == '__main__':
    main()
