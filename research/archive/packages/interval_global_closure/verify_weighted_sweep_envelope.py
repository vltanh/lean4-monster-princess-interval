"""Exact Fraction regression for the analytic weighted two-sweep envelope."""
from fractions import Fraction as Q
from itertools import product


def first_hit(path, direction):
    def signed(t, x):
        return t - 1 - x if direction == +1 else 1 - t - x
    for (a, x), (b, y) in zip(path, path[1:]):
        da, db = signed(a, x), signed(b, y)
        if da == 0:
            return a
        if da * db < 0 or db == 0:
            return a + (b - a) * (-da) / (db - da)
    raise AssertionError("Completed sweep must hit every legal path")


def score(path, w):
    return w * first_hit(path, +1) + (1 - w) * first_hit(path, -1)


def main():
    grid = [Q(k, 4) for k in range(-4, 5)]
    paths = []
    for x0, x1, x2 in product(grid, repeat=3):
        if abs(x1 - x0) <= 1 and abs(x2 - x1) <= 1:
            paths.append([(Q(0), x0), (Q(1), x1), (Q(2), x2)])
    assert len(paths) == 429
    weights = [Q(0), Q(1, 7), Q(1, 4), Q(1, 2), Q(3, 4), Q(6, 7), Q(1)]
    for w in weights:
        bound = 1 + max(w, 1 - w)
        for path in paths:
            assert score(path, w) <= bound
        for n in range(1, 20):
            epsilon = Q(1, 2**n)
            p = [(Q(0), -1 + epsilon), (2 - epsilon, Q(1)), (Q(2), Q(1))]
            reflected = [(t, -x) for t, x in p]
            best = max(score(p, w), score(reflected, w))
            assert bound - best <= epsilon / 2
    assert score([(Q(0), Q(1)), (Q(2), Q(1))], Q(1)) == 2
    assert score([(Q(0), -Q(1)), (Q(2), -Q(1))], Q(0)) == 2
    print(f"PASS: {len(paths)} paths, {len(weights)} weights, 19 epsilons per weight")


if __name__ == "__main__":
    main()
