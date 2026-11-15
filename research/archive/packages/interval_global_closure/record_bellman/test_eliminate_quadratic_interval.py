"""Independent exact fiber checks for bounded scalar quadratic elimination."""
from fractions import Fraction as Q
from pathlib import Path
import hashlib
import json
import random
import sys

from eliminate_quadratic_interval import eliminate_last_variable, minimum_at


def direct_value(c, linear, hessian, theta, h):
    x = tuple(theta)+(h,)
    return c+sum(a*b for a, b in zip(linear, x))+sum(
        hessian[i][j]*x[i]*x[j] for i in range(len(x)) for j in range(len(x)))


def direct_minimum(rows, c, linear, hessian, theta, interval):
    lo, hi = map(Q, interval)
    for a, b in rows:
        residual = b-sum(x*y for x, y in zip(a[:-1], theta))
        if not a[-1]:
            if residual < 0:
                return None
        elif a[-1] > 0:
            hi = min(hi, residual/a[-1])
        else:
            lo = max(lo, residual/a[-1])
    if lo > hi:
        return None
    heights = [lo, hi]
    aa = hessian[-1][-1]
    bb = linear[-1]+sum((hessian[-1][j]+hessian[j][-1])*theta[j]
                        for j in range(len(theta)))
    if aa > 0 and lo <= -bb/(2*aa) <= hi:
        heights.append(-bb/(2*aa))
    return min(direct_value(c, linear, hessian, theta, h) for h in heights)


def main():
    rng = random.Random(204209)
    counts = {"random_parameter_fibers": 0, "eligible_substitutions": 0,
              "point_and_empty_fibers": 0, "zero_parameter_cases": 0,
              "malformed_rejections": 0}
    for dimension in range(1, 5):
        for case in range(45):
            linear = tuple(Q(rng.randrange(-6, 7), rng.randrange(1, 5))
                           for _ in range(dimension))
            H = [[Q(0)]*dimension for _ in range(dimension)]
            for i in range(dimension):
                for j in range(i+1):
                    H[i][j] = H[j][i] = Q(rng.randrange(-4, 5), rng.randrange(1, 4))
            # Force genuinely affine and constant-in-h cases, as well as both curvatures.
            if case % 5 == 0:
                H[-1][-1] = Q(0)
            c = Q(rng.randrange(-4, 5))
            rows = [(tuple(Q(rng.randrange(-3, 4)) for _ in range(dimension)),
                     Q(rng.randrange(-4, 5))) for _ in range(case % 7)]
            interval = (Q(-1), Q(2))
            candidates = eliminate_last_variable(rows, c, linear, H, interval)
            for _ in range(17):
                theta = tuple(Q(rng.randrange(-6, 7), rng.randrange(1, 5))
                              for _ in range(dimension-1))
                expected = direct_minimum(rows, c, linear, H, theta, interval)
                actual = minimum_at(candidates, theta)
                assert (actual is None) == (expected is None)
                if actual is not None:
                    assert actual[0] == expected
                for candidate in candidates:
                    if candidate.eligible(theta):
                        h = candidate.height(theta)
                        assert interval[0] <= h <= interval[1]
                        assert all(sum(x*y for x, y in zip(a, theta+(h,))) <= b
                                   for a, b in rows)
                        assert candidate.objective.evaluate(theta) == direct_value(c, linear, H, theta, h)
                        counts["eligible_substitutions"] += 1
                counts["random_parameter_fibers"] += 1
                if dimension == 1:
                    counts["zero_parameter_cases"] += 1
    # Equality h=theta and incompatible parameter fibers are represented by closed inequalities.
    rows = [((Q(-1), Q(1)), Q(0)), ((Q(1), Q(-1)), Q(0))]
    candidates = eliminate_last_variable(rows, 1, (2, 3), ((4, 5), (5, 6)))
    for theta in (Q(-1), Q(0), Q(1, 7), Q(1), Q(2)):
        result = minimum_at(candidates, (theta,))
        assert (result is not None) == (0 <= theta <= 1)
        if result is not None:
            assert result[:2] == (1+5*theta+20*theta*theta, theta)
        counts["point_and_empty_fibers"] += 1
    assert not eliminate_last_variable([((0, 0), -1)], 0, (0, 0), ((0, 0), (0, 0)))
    singleton = eliminate_last_variable([], 0, (0,), ((-1,),), interval=(Q(1, 3), Q(1, 3)))
    assert minimum_at(singleton, ())[:2] == (Q(-1, 9), Q(1, 3))
    counts["point_and_empty_fibers"] += 2
    bad_calls = [
        lambda: eliminate_last_variable([], 0.1, (0,), ((0,),)),
        lambda: eliminate_last_variable([], 0, (0,), ((0,),), interval=(1, 0)),
        lambda: eliminate_last_variable([], 0, (), ()),
        lambda: eliminate_last_variable([], 0, (0, 0), ((0, 1), (0, 0))),
        lambda: eliminate_last_variable([((0, 1), 0)], 0, (0,), ((0,),)),
    ]
    for call in bad_calls:
        try:
            call()
        except (ValueError, TypeError):
            counts["malformed_rejections"] += 1
        else:
            raise AssertionError("malformed input accepted")
    source = Path(__file__).with_name('eliminate_quadratic_interval.py')
    report = {"status": "PASS", "scope": "Exact bounded scalar elimination; independent rational fiber optima and direct original-polynomial substitution. This is a component, not a game-value certificate.",
              "counts": counts, "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest()}
    encoded = json.dumps(report, indent=2)+'\n'
    if len(sys.argv) > 1:
        Path(sys.argv[1]).write_text(encoded)
    print(encoded, end='')


if __name__ == '__main__':
    main()
