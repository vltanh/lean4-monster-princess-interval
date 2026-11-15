#!/usr/bin/env python3
"""Independent Fraction fixtures for the center-memory endpoint-sweep theorem.

Capture times here come from direct intersections of polygonal paths.
No Bellman action formula or continuous-CDF integration engine is used.
The fixtures include a slow outward layer, an exact outgoing characteristic
atom, stationary endpoint mass, and a path that leaves an earlier endpoint.
"""
from fractions import Fraction as Q


def position(path, time):
    for (a, x), (b, y) in zip(path, path[1:]):
        if a <= time <= b:
            return x+(time-a)*(y-x)/(b-a)
    raise ValueError('Time outside path')


def first_capture(path, monster, sign=1):
    hits = []
    for (a, x), (b, y) in zip(path, path[1:]):
        pv = sign*(y-x)/(b-a)
        pi = sign*x-pv*a
        for (c, z), (d, w) in zip(monster, monster[1:]):
            if d == c:
                continue
            left, right = max(a, c), min(b, d)
            if right < left:
                continue
            mv = (w-z)/(d-c)
            mi = z-mv*c
            slope, intercept = pv-mv, pi-mi
            if slope == 0:
                if intercept == 0:
                    hits.append(left)
            else:
                root = -intercept/slope
                if left <= root <= right:
                    hits.append(root)
    if len(monster) == 1:
        time, radius = monster[0]
        if sign*position(path, time) == radius:
            hits.append(time)
    return min(hits) if hits else None


def fixtures():
    low = [
        [(0, Q(1, 10)), (Q(1, 2), 0), (1, Q(1, 10)), (Q(19, 10), 1), (8, 1)],
        [(0, Q(1, 5)), (Q(1, 2), 0), (1, Q(1, 5)), (Q(9, 5), 1), (8, 1)],
        [(0, Q(3, 10)), (Q(1, 2), 0), (1, Q(3, 10)), (Q(17, 10), 1), (8, 1)],
    ]
    simple = low+[
        [(0, Q(3, 5)), (Q(2, 5), 1), (8, 1)],
        [(0, 1), (8, 1)],
    ]
    departure = low+[
        [(0, 1), (Q(3, 2), 1), (Q(8, 5), Q(9, 10)), (Q(17, 10), 1), (8, 1)],
        [(0, 1), (8, 1)],
    ]
    weights = [Q(1, 10), Q(1, 5), Q(1, 5), Q(1, 4), Q(1, 4)]
    return [([[tuple(map(Q, point)) for point in path] for path in paths], weights)
            for paths in [simple, departure]]


def center_memory(paths, weights, time):
    times = {Q(0), time}
    times.update(t for path in paths for t, _ in path if t <= time)
    return max(sum(weight for path, weight in zip(paths, weights)
                   if position(path, t) == 0) for t in times)


def future_interior_front(paths, weights, time):
    """Exact supremum of R over the future reachable interior cone."""
    flags = []
    for path in paths:
        possible = False
        for (a, x), (b, y) in zip(path, path[1:]):
            if b < time or x == y == 1:
                continue
            # On every segment V=s-p(s) is nondecreasing.  At its right
            # endpoint the limiting maximum may belong only to p=1.
            maximum = b-y
            if maximum > time:
                possible = True
            elif maximum == time and (y < 1 or b-a == y-x):
                possible = True
        flags.append(possible)
    assert flags == sorted(flags, reverse=True), flags
    return sum(weight for weight, flag in zip(weights, flags) if flag)


def captured_prefix(paths, monster, sign):
    flags = [first_capture(path, monster, sign) is not None for path in paths]
    assert flags == sorted(flags, reverse=True), (monster, sign, flags)
    return sum(flags)


def cost(paths, weights, monster, plus=0, minus=0):
    total = Q(0)
    for sign, old in [(1, plus), (-1, minus)]:
        for path, weight in zip(paths[old:], weights[old:]):
            hit = first_capture(path, monster, sign)
            assert hit is not None, (monster, path)
            total += weight*hit/2
    return total


def sweep(time, sign):
    return [(time, Q(0)), (time+1, Q(sign)), (time+3, Q(-sign))]


def prefixes(time):
    result = [[(Q(0), Q(0)), (time, Q(0))]]
    for start in [Q(1, 8), Q(1, 4), Q(1, 2)]:
        for sign in [-1, 1]:
            result.append([(Q(0), sign*start), (time-start, sign*start), (time, Q(0))])
            result.append([(Q(0), sign*start), ((time-start)/2, sign*(time+start)/2), (time, Q(0))])
    return result


def main():
    counts = dict(order=0, memory=0, triangle=0, wait=0, concrete_continuation=0, trace=0)
    for paths, weights in fixtures():
        cumulative = [Q(0)]
        for weight in weights:
            cumulative.append(cumulative[-1]+weight)
        times = sorted({t for path in paths for t, _ in path})
        for time in times:
            radii = [position(path, time) for path in paths]
            assert radii == sorted(radii)
            counts['order'] += 1
        for path in paths:
            assert all(abs(y-x) <= b-a for (a, x), (b, y) in zip(path, path[1:]))
            assert position(path, Q(2)) == 1
        for t in [Q(3, 4), Q(4, 5), Q(9, 10), Q(1)]:
            H = center_memory(paths, weights, t)
            Y = future_interior_front(paths, weights, t)
            assert H >= Y
            for prefix in prefixes(t):
                plus, minus = (captured_prefix(paths, prefix, sign) for sign in [1, -1])
                assert max(cumulative[plus], cumulative[minus]) >= H
                counts['memory'] += 1
                sign = 1 if plus <= minus else -1
                baseline = cost(paths, weights, sweep(t, sign), plus, minus)
                for e in [t+(1-t)/3, t+(1-t)*2/3, t+Q(1, 2)]:
                    for direction in [-1, 1]:
                        route = [(t, Q(0)), ((t+e)/2, direction*(e-t)/2), (e, Q(0)),
                                 (e+1, Q(-direction)), (e+3, Q(direction))]
                        assert cost(paths, weights, route, plus, minus) >= baseline
                        counts['concrete_continuation'] += 1
            # Artificial frontiers also satisfy the stronger state theorem;
            # reachability is used only to infer max frontier >= H.
            for plus in range(len(cumulative)):
                for minus in range(len(cumulative)):
                    if max(cumulative[plus], cumulative[minus]) < Y:
                        continue
                    sign = 1 if plus <= minus else -1
                    baseline = cost(paths, weights, sweep(t, sign), plus, minus)
                    assert baseline == min(cost(paths, weights, sweep(t, d), plus, minus)
                                           for d in [-1, 1])
                    for duration in [Q(1, 8), Q(1, 2), Q(1), Q(2)]:
                        e = t+duration
                        for direction in [-1, 1]:
                            tri = [(t, Q(0)), ((t+e)/2, direction*(e-t)/2), (e, Q(0))]
                            best = min(cost(paths, weights, tri+[(e+1, Q(d)), (e+3, Q(-d))], plus, minus)
                                       for d in [-1, 1])
                            assert best >= baseline, (t, plus, minus, duration, direction, best, baseline)
                            counts['triangle'] += 1
                        wait = [(t, Q(0)), (e, Q(0))]
                        best = min(cost(paths, weights, wait+[(e+1, Q(d)), (e+3, Q(-d))], plus, minus)
                                   for d in [-1, 1])
                        assert best >= baseline
                        counts['wait'] += 1
    # A final unit-speed characteristic can be captured before its endpoint
    # arrival even though the strict spatial CDF at that endpoint excludes it.
    paths, weights = fixtures()[0]
    t = Q(4, 5)
    inside = sum(w for p, w in zip(paths, weights)
                 if first_capture(p, [(t, Q(0)), (t+1, Q(1))]) < t+1)
    endpoint_strict = sum(w for p, w in zip(paths, weights) if position(p, t+1) < 1)
    assert inside == Q(3, 10) and endpoint_strict == Q(1, 10)
    counts['trace'] += 1
    # Endpoint-by-two alone allows an earlier endpoint visit followed by
    # departure.  A single row endpoint trace then understates the tail cone.
    paths, weights = fixtures()[1]
    t = Q(1, 2)
    first_row = sum(w for p, w in zip(paths, weights)
                    if first_capture(p, [(t, Q(0)), (t+1, Q(1))]) < t+1)
    assert first_row == Q(1, 2)
    assert future_interior_front(paths, weights, t) == Q(3, 4)
    counts['trace'] += 1
    print(f'PASS: {sum(counts.values())} exact center-memory checks')
    for key, number in counts.items():
        print(f'  {key}: {number}')
    print('PASS: slow outward paths after the center peak and exact outgoing atoms')
    print('PASS: endpoint departure requires the full future interior cone')
    print('Scope: attained continuation value on the memory region; earlier game costs remain open')


if __name__ == '__main__':
    main()
