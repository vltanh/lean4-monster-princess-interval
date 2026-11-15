#!/usr/bin/env python3
"""Construct the ordinary-wave prefix normalization at a prescribed cut.

This finite-law constructor is used by independent exact fixtures.  It
does not evaluate capture costs.  The theorem for a continuous ordered law
is in ORDINARY_PREFIX_COMPRESSION.md.  Interior coalescence across distinct
initial positions is deliberately rejected rather than approximated.
"""


def position(route, time):
    for (left, x), (right, y) in zip(route, route[1:]):
        if left <= time <= right:
            return x+(time-left)*(y-x)/(right-left)
    if len(route) == 1 and route[0][0] == time:
        return route[0][1]
    raise ValueError("Time outside route")


def first_u(route, level):
    """First closed hitting time of t+m(t)=level; no inverse convention."""
    for (left, x), (right, y) in zip(route, route[1:]):
        lo, hi = left+x, right+y
        if lo <= level <= hi:
            if lo == level:
                return left
            return left+(right-left)*(level-lo)/(hi-lo)
    return None


def check_parameters(parameters):
    for a, u, c in parameters:
        if not (0 <= a <= u <= 2-a and -a <= c <= 1):
            raise ValueError("Illegal ordinary-wave parameters")
    for i, (a, u, c) in enumerate(parameters):
        for b, v, d in parameters[i+1:]:
            if not (a <= b and u <= v and c >= d):
                raise ValueError("Paths are not ordered")
            if a < b and not (u < v and c > d):
                raise ValueError("Cross-initial-rank interior coalescence is excluded")


def compress_prefix(parameters, route, check=True):
    """Normalize a positive same-half prefix at a fixed space-time endpoint.

    The input may contain arbitrary rational speeds of absolute value at
    most one and arbitrary waits.  It has no boundary visit before its
    final point, which may be interior, zero, or one.  The replacement
    joins exactly that point and time; it may visit the center earlier.
    """
    if check:
        check_parameters(parameters)
    start, terminal = route[0][1], route[-1][0]
    boundary = route[-1][1]
    if route[0][0] != 0 or not 0 < start < 1 or not 0 <= boundary <= 1:
        raise ValueError("Expected a positive interior start and endpoint")
    for i, ((left, x), (right, y)) in enumerate(zip(route, route[1:])):
        if not left < right or abs(y-x) > right-left:
            raise ValueError("Illegal monster speed")
        if not 0 < x < 1 or (i < len(route)-2 and not 0 < y < 1):
            raise ValueError("The supplied route already touched a boundary")

    # Initially higher paths can first meet an interior monster only on
    # their incoming characteristic U=u, before the outgoing deadline c.
    # At the first endpoint, other higher paths can be captured there;
    # those endpoint captures are kept at their original terminal time.
    incoming_hits = []
    for a, u, c in parameters:
        if a <= start:
            continue
        time = first_u(route, u)
        if time is None or (boundary == 1 and time == terminal):
            continue
        v = time-position(route, time)
        if v <= c:
            incoming_hits.append((time, u, v))

    zero = start*0
    result = [(zero, start)]

    def append(time, x):
        if time == result[-1][0]:
            if x != result[-1][1]:
                raise AssertionError("Zero-time movement in compressed prefix")
            return
        assert time > result[-1][0]
        assert abs(x-result[-1][1]) <= time-result[-1][0]
        assert 0 <= x <= 1
        result.append((time, x))

    def inward_then_wait(v):
        """Reach V=v with the smallest feasible U from the initial point."""
        if v <= start:
            append((start+v)/2, (start-v)/2)
        else:
            append(start, zero)
            append(v, zero)

    if not incoming_hits:
        w = terminal-boundary
        inward_then_wait(w)
        append(terminal, boundary)
        return result, dict(case="no incoming higher capture", incoming_hits=0,
                            earlier_center=any(t < terminal and x == 0 for t, x in result))

    first = min(incoming_hits)
    v = first[2]
    e = max(u for _, u, _ in incoming_hits)
    inward_then_wait(v)
    append((e+v)/2, (e-v)/2)
    w = terminal-boundary
    if w <= e:
        append((e+w)/2, (e-w)/2)
    else:
        append(e, zero)
        append(w, zero)
    append(terminal, boundary)
    return result, dict(case="incoming block", incoming_hits=len(incoming_hits),
                        v=v, e=e,
                        earlier_center=any(t < terminal and x == 0 for t, x in result))
