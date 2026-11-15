#!/usr/bin/env python3
"""Direct Fraction intersections for ordinary first-boundary compression.

The reference engine uses polygonal path intersections, not CDF records,
rank inverses, or the compression's characteristic capture classification.
Two explicit counterfixtures enforce the exclusion of cross-initial-rank
incoming and outgoing coalescence.
"""
from fractions import Fraction as Q
from random import Random

from prefix_compression import check_parameters, compress_prefix
from verify_center_memory import first_capture, position


def princess_path(parameters, horizon=Q(16)):
    a, u, c = parameters
    lines = [(Q(0), Q(0)), (Q(0), Q(1)), (Q(1), a), (Q(-1), u), (Q(1), -c)]
    cuts = {Q(0), horizon}
    for i, (v, b) in enumerate(lines):
        for w, d in lines[i+1:]:
            if v != w:
                time = (d-b)/(v-w)
                if 0 < time < horizon:
                    cuts.add(time)
    path = [(time, min(Q(1), max(Q(0), min(a+time, u-time), time-c)))
            for time in sorted(cuts)]
    reduced = []
    for point in path:
        reduced.append(point)
        while len(reduced) >= 3:
            (s, x), (t, y), (v, z) = reduced[-3:]
            if (y-x)*(v-t) != (z-y)*(t-s):
                break
            reduced.pop(-2)
    return reduced


def laws():
    raw = [
        [(Q(1,10), Q(1,4), 1), (Q(3,10), Q(1,2), Q(3,4)),
         (Q(1,2), Q(3,4), Q(1,3)), (Q(7,10), Q(19,20), Q(-1,4)),
         (Q(9,10), Q(11,10), Q(-4,5))],
        [(Q(1,5), Q(2,5), Q(4,5)), (Q(1,5), Q(1,2), Q(3,4)),
         (Q(2,5), Q(3,5), Q(1,2)), (Q(2,5), Q(3,4), Q(1,3)),
         (Q(3,5), Q(9,10), 0), (Q(4,5), Q(11,10), Q(-3,5))],
        [(Q(1,10), Q(1,4), 1), (Q(1,3), Q(3,5), Q(4,5)),
         (Q(1,3), Q(3,5), Q(4,5)), (Q(2,3), Q(9,10), Q(1,10)),
         (Q(9,10), Q(21,20), Q(-4,5))],
        [(0, Q(1,5), 1), (Q(1,4), Q(1,4), Q(3,4)),
         (Q(1,2), Q(1,2), Q(1,4)), (Q(3,4), Q(3,4), Q(-1,2))],
        [(Q(k,8), Q(k+1,8), Q(-k,8)) for k in range(1,7)],
    ]
    return [[tuple(map(Q, row)) for row in law] for law in raw]


def routes(starts, seed=47231, samples=150):
    rng = Random(seed)
    result = []
    for index in range(samples):
        start = starts[index % len(starts)]
        route = [(Q(0), start)]
        for _ in range(rng.randrange(5, 36)):
            time, x = route[-1]
            velocity = rng.choice([Q(-1), Q(-1,2), Q(0), Q(1,2), Q(1)])
            duration = rng.choice([Q(1,32), Q(1,16), Q(1,8), Q(1,4)])
            y = x+velocity*duration
            if y <= 0:
                route.append((time+x/(-velocity), Q(0)))
                break
            if y >= 1:
                route.append((time+(1-x)/velocity, Q(1)))
                break
            route.append((time+duration, y))
        else:
            time, x = route[-1]
            if index % 3:
                target = Q(index % 2)
                route.append((time+abs(target-x), target))
        result.append(route)
    return result


def counterfixtures():
    incoming = [(Q(1,5), Q(4,5), Q(9,10)),
                (Q(2,5), Q(4,5), Q(4,5)),
                (Q(3,5), Q(1), Q(1,2))]
    monster_i = [(Q(0), Q(3,10)), (Q(1,4), Q(11,20)),
                 (Q(3,10), Q(1,2)), (Q(2,5), Q(3,5)), (Q(1), Q(0))]
    outgoing = [(Q(1,5), Q(3,10), Q(3,5)),
                (Q(2,5), Q(7,10), Q(3,5)),
                (Q(3,5), Q(9,10), Q(3,5))]
    monster_c = [(Q(0), Q(3,10)), (Q(1,5), Q(1,2)),
                 (Q(13,20), Q(1,20)), (Q(3,4), Q(3,20)), (Q(9,10), Q(0))]
    for parameters, monster in [(incoming, monster_i), (outgoing, monster_c)]:
        try:
            check_parameters(parameters)
        except ValueError as error:
            assert "coalescence" in str(error)
        else:
            raise AssertionError("An invalid atomic extension was accepted")
        replacement, _ = compress_prefix(parameters, monster, check=False)
        low = princess_path(parameters[0])
        before, after = first_capture(low, monster), first_capture(low, replacement)
        assert before is not None and after is not None and after > before
        yield before, after


def main():
    counts = dict(law_checks=0, prefixes=0, pointwise_capture=0,
                  initial_atom=0, earlier_center=0, endpoint_prefix=0, interior_cut=0,
                  atom_counterexamples=0)
    for law_index, parameters in enumerate(laws()):
        check_parameters(parameters)
        paths = [princess_path(row) for row in parameters]
        times = sorted({time for path in paths for time, _ in path})
        for time in times:
            values = [position(path, time) for path in paths]
            assert values == sorted(values)
            counts['law_checks'] += 1
        for path in paths:
            assert all(abs(y-x) <= t-s for (s,x),(t,y) in zip(path,path[1:]))
            assert position(path, Q(2)) == 1
        starts = sorted({Q(k,16) for k in range(1,16)} |
                        {a for a, _, _ in parameters if 0 < a < 1})
        for original in routes(starts, seed=47231+law_index):
            replacement, metadata = compress_prefix(parameters, original)
            assert replacement[0] == original[0] and replacement[-1] == original[-1]
            counts['prefixes'] += 1
            counts['earlier_center'] += bool(metadata.get('earlier_center'))
            counts['endpoint_prefix'] += original[-1][1] == 1
            counts['interior_cut'] += 0 < original[-1][1] < 1
            for path in paths:
                for sign in [-1, 1]:
                    before = first_capture(path, original, sign)
                    after = first_capture(path, replacement, sign)
                    if before is not None:
                        assert after is not None and after <= before, (
                            parameters, original, replacement, sign, path, before, after)
                    counts['pointwise_capture'] += 1
                if path[0][1] == original[0][1]:
                    assert first_capture(path, replacement) == 0
                    counts['initial_atom'] += 1
    for before, after in counterfixtures():
        counts['atom_counterexamples'] += 1
        print(f'Excluded atomic extension: low capture would move from {before} to {after}')
    assert all(counts[key] > 0 for key in counts)
    print(f'PASS: {sum(counts.values())} exact prefix-compression checks')
    for key, value in counts.items():
        print(f'  {key}: {value}')
    print('PASS: arbitrary-speed prefixes, moving negative c, initial atoms, inverse gaps')
    print('PASS: outgoing caps and incoming characteristics above one')
    print('Scope: ordinary capped waves with separated cross-initial characteristics; no game value')


if __name__ == '__main__':
    main()
