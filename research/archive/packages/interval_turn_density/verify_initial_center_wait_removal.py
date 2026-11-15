"""Exact physical audit of the initial-center-wait upper replacement."""
from collections import Counter
from fractions import Fraction as Q
from pathlib import Path
import random
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'interval_turn_sheet'))
from verify_center_memory import first_capture


def clean(points):
    return [point for i, point in enumerate(points)
            if i == 0 or point != points[i-1]]


def rows(w, s):
    future = [((w+s)/2, (w-s)/2), (s, Q(0)),
              ((s+1)/2, (1-s)/2), (Q(1), Q(0)),
              (Q(2), Q(-1)), (Q(4), Q(1))]
    old = clean([(Q(0), Q(0)), (w, Q(0))]+future)
    new = clean([(Q(0), w), (w, Q(0))]+future)
    return old, new


def main():
    rng = random.Random(5521)
    counts = Counter()
    paths = []
    for trial in range(24):
        level = rng.randrange(17)
        raw = [(Q(0), Q(level, 16))]
        for i in range(1, 49):
            level = min(16, max(0, level+rng.randrange(-2, 3)))
            raw.append((Q(i, 8), Q(level, 16)))
        epsilon = Q(1, 64)
        paths.append([(t, epsilon+(1-epsilon)*p) for t, p in raw])
    paths.extend([[(Q(0), h), (Q(6), h)]
                  for h in (Q(1, 64), Q(1, 4), Q(3, 4), Q(1))])
    for w, s in [(Q(1, 8), Q(9, 16)), (Q(1, 4), Q(3, 4)),
                 (Q(3, 8), Q(7, 8))]:
        old, new = rows(w, s)
        # After reflection, the three changing directions are precisely
        # M3(x=-w, first U=s, second V=1). Center vertices are collinear.
        m3 = [(Q(0), -w), ((w+s)/2, (s-w)/2),
              ((s+1)/2, (s-1)/2), (Q(2), Q(1)), (Q(4), Q(-1))]
        for path in paths:
            assert all(p > 0 for _, p in path)
            for sign in (-1, 1):
                before = first_capture(path, old, sign)
                after = first_capture(path, new, sign)
                assert before is not None and after is not None and after <= before
                counts['individual strictly positive capture comparisons'] += 1
                reflected = first_capture(path, m3, -sign)
                assert reflected == after
                counts['signed early-M3 physical identities'] += 1
        center = [(Q(0), Q(0)), (Q(6), Q(0))]
        for sign in (-1, 1):
            assert first_capture(center, old, sign) == 0
            assert first_capture(center, new, sign) == w
            counts['center-contact counterexamples retained'] += 1
    print('PASS:', sum(counts.values()), 'initial-center-wait response checks')
    for key, value in counts.items():
        print(' ', key+':', value)
    print('Scope: upper response-supremum replacement; not lower-law domination')


if __name__ == '__main__':
    main()
