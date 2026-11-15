#!/usr/bin/env python3
"""Independent exact obstruction for a fixed Monster law's common-warp family.

No optimizer, cut compiler, or floating point is used.  Each supplied query
profile is realized as a clipped, late-fill path over polynomial germs in e.
Every Monster pair is recaptured chronologically.  The limiting capture
coordinates independently validate the claimed linear warp coefficients.
"""
from __future__ import annotations

import argparse
from bisect import bisect_left, bisect_right
from fractions import Fraction as Q
from functools import total_ordering
import gzip
import hashlib
import json
from pathlib import Path


SOURCE_SHA256 = "2a09355539fa015a0b281843a9db108c4a619243118eb0d57d14144cab20d89a"


@total_ordering
class P:
    """A polynomial ordered by its sign for sufficiently small positive e."""

    __slots__ = ("c",)

    def __init__(self, value=0):
        if isinstance(value, P):
            self.c = value.c
            return
        c = list(value) if isinstance(value, (tuple, list)) else [Q(value)]
        while len(c) > 1 and not c[-1]:
            c.pop()
        self.c = tuple(c)

    def __add__(self, other):
        other = P(other)
        n = max(len(self.c), len(other.c))
        return P([(self.c[i] if i < len(self.c) else 0)
                  + (other.c[i] if i < len(other.c) else 0) for i in range(n)])

    __radd__ = __add__

    def __neg__(self):
        return P([-x for x in self.c])

    def __sub__(self, other):
        return self + (-P(other))

    def __rsub__(self, other):
        return P(other) + (-self)

    def __mul__(self, scalar):
        scalar = Q(scalar)
        return P([scalar*x for x in self.c])

    __rmul__ = __mul__

    def __truediv__(self, scalar):
        return self * (1/Q(scalar))

    def __eq__(self, other):
        return self.c == P(other).c

    def __lt__(self, other):
        other = P(other)
        for i in range(max(len(self.c), len(other.c))):
            a = self.c[i] if i < len(self.c) else 0
            b = other.c[i] if i < len(other.c) else 0
            if a != b:
                return a < b
        return False

    def __repr__(self):
        return "P(" + repr(self.c) + ")"

    @property
    def limit(self):
        return Q(self.c[0])


ZERO, ONE, TWO = P(0), P(1), P(2)
EPS = P([0, 1])
CONNECTOR = P([0, 0, 1])
ETA = P([0, 0, 0, 0, 0, 0, 1])


def load_source(path):
    raw = path.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == SOURCE_SHA256, "wrong Monster law"
    data = json.loads(gzip.decompress(raw))
    assert data["pair_law"] == "fair_reflection"
    n, denominator = int(data["n"]), int(data["weight_denominator"])
    assert Q(data["physical_step"]) == Q(1, 2*n)
    merged = {}
    for row in data["paths"]:
        w, x = int(row["weight_numerator"]), int(row["start_grid"])
        assert w > 0 and -2*n <= x <= 2*n
        points, previous = [(0, x)], None
        for j, move in enumerate(row["moves"]):
            assert move in (-1, 1)
            if previous is not None and move != previous:
                points.append((j, x))
            x += move
            assert -2*n <= x <= 2*n
            previous = move
        points.append((len(row["moves"]), x))
        light = tuple((Q(t+x, 2*n), Q(t-x, 2*n)) for t, x in points)
        assert len(light) >= 2
        for (u, v), (a, b) in zip(light, light[1:]):
            assert (a > u and b == v) or (a == u and b > v)
        merged[light] = merged.get(light, 0) + w
    assert sum(merged.values()) == denominator
    atoms = [(w, (route, tuple((v, u) for u, v in route)))
             for route, w in merged.items()]
    return data, denominator, atoms


class Arrangement:
    def __init__(self, atoms):
        queries, bases = {Q(-1)}, {Q(0)}
        for _, pair in atoms:
            for route in pair:
                for u, v in route:
                    queries.add(v)
                    if u >= 0:
                        bases.add(u)
        self.v = sorted(queries)
        for v in self.v:
            bases.update((max(v, 0), v+2))
        self.bases = sorted(bases)
        self.query = {v: i for i, v in enumerate(self.v)}
        self.bounds = [(self.ge(max(v, 0)), self.ge(v+2)) for v in self.v]
        self.bounds[0] = (self.ge(0), self.ge(0))
        last = self.ge(self.v[-1]+2)
        self.bounds[-1] = (last, last)

    def ge(self, x):
        j = bisect_left(self.bases, x)
        return 3*j + int(j < len(self.bases) and self.bases[j] == x)

    def gt(self, x):
        j = bisect_left(self.bases, x)
        return 3*j + 2*int(j < len(self.bases) and self.bases[j] == x)

    def validate(self, labels):
        assert len(labels) == len(self.v)
        assert all(isinstance(x, int) for x in labels)
        assert all(lo <= k <= hi for k, (lo, hi) in zip(labels, self.bounds))
        assert all(a <= b for a, b in zip(labels, labels[1:]))

    def claimed_capture(self, route, labels):
        u, v = route[0]
        p = labels[self.query[v]]
        if self.ge(u) <= p < self.gt(u):
            return u, v
        above = p >= self.gt(u)
        for a, b in route[1:]:
            if a > u and above:
                p = labels[self.query[v]]
                if p < self.gt(a):
                    point = self.bases[p//3], v
                    assert u <= point[0] <= a
                    return point
            elif b > v and not above:
                at = bisect_left(labels, self.ge(u))
                assert at < len(labels)
                cross = min(u, self.v[at])
                if cross <= b:
                    assert v <= cross
                    return u, cross
            u, v = a, b
        raise AssertionError("no claimed capture")


def realize(arrangement, labels):
    """Late-fill realization, then exact clipping to [e^6,1-e^6]."""
    values = [min(max(P(arrangement.bases[k//3]) + (k % 3-1)*EPS,
                      P(v), ZERO), P(v+2))
              for v, k in zip(arrangement.v, labels)]
    raw = [(ZERO, P(-1))]

    def add(u, v):
        old_u, old_v = raw[-1]
        if (u, v) == (old_u, old_v):
            return
        assert u >= old_u and v >= old_v and ZERO <= u-v <= TWO
        raw.append((u, v))

    for j in range(1, len(arrangement.v)):
        v, previous, target = P(arrangement.v[j]), values[j-1], values[j]
        before = v-CONNECTOR
        assert before > arrangement.v[j-1]
        add(previous, min(before, previous))
        if before > previous:
            add(before, before)
        add(min(target, before+2), before)
        if target > before+2:
            add(target, target-2)
        add(target, v)

    clipped = []
    for (u, v), (a, b) in zip(raw, raw[1:]):
        ta, xa, tb, xb = (u+v)/2, (u-v)/2, (a+b)/2, (a-b)/2
        dt, dx = tb-ta, xb-xa
        assert dt > 0
        slope = 0 if dx == 0 else 1 if dx == dt else -1 if dx == -dt else None
        assert slope is not None, "unexpected non-axis or non-boundary connector"
        cuts = [ta, tb]
        if ta < 0 < tb:
            cuts.append(ZERO)
        if slope:
            for level in (ETA, ONE-ETA):
                cut = ta+(level-xa)/slope
                if ta < cut < tb:
                    cuts.append(cut)
        for t in sorted(cuts):
            if t < 0:
                continue
            x = min(max(xa+slope*(t-ta), ETA), ONE-ETA)
            point = t+x, t-x
            if not clipped or point != clipped[-1]:
                clipped.append(point)
    assert clipped and clipped[0][0]+clipped[0][1] == 0
    for (u, v), (a, b) in zip(clipped, clipped[1:]):
        assert a >= u and b >= v and a+b > u+v
        assert 2*ETA <= a-b <= 2-2*ETA
        assert a == u or b == v or a-u == b-v
    return clipped


def slice_at(path, axis_values, axis, target):
    """Exact interval cut out by one fixed U or V coordinate."""
    target = P(target)
    lo, hi = bisect_left(axis_values, target), bisect_right(axis_values, target)
    other = 1-axis
    if lo != hi:
        return path[lo][other], path[hi-1][other]
    if lo == 0 or lo == len(path):
        return None
    p, q = path[lo-1], path[lo]
    da, db = q[axis]-p[axis], q[other]-p[other]
    assert da > 0 and (db == 0 or db == da)
    value = p[other] if db == 0 else p[other]+target-p[axis]
    return value, value


def physical_capture(route, path, axes):
    """First polygonal intersection, in chronological Monster-leg order."""
    for (u, v), (a, b) in zip(route, route[1:]):
        axis, fixed, left, right = (1, v, u, a) if a > u else (0, u, v, b)
        interval = slice_at(path, axes[axis], axis, fixed)
        if interval is None:
            continue
        low, high = max(interval[0], P(left)), min(interval[1], P(right))
        if low <= high:
            return (low, P(fixed)) if axis == 1 else (P(fixed), low)
    raise AssertionError("uncaught realized target")


def fold(q):
    period = q//2
    r = q-2*period
    return (2*period, 1, r) if r <= 1 else (2*period+2, -1, 2-r)


def verify(source, candidate):
    data, denominator, atoms = load_source(source)
    payload = candidate.read_bytes()
    cert = json.loads(gzip.decompress(payload) if candidate.suffix == ".gz" else payload)
    assert cert["format"] == "common-warp-family-obstruction-v1"
    knots = list(map(Q, cert["knots"]))
    assert knots[0] == 0 and knots[-1] == 1
    assert all(a < b for a, b in zip(knots, knots[1:]))
    index, size = {q: k for k, q in enumerate(knots)}, len(knots)-1
    arrangement = Arrangement(atoms)
    for q in arrangement.v + arrangement.bases:
        assert fold(q)[2] in index
    mixture_denominator = int(cert["weight_denominator"])
    assert mixture_denominator > 0
    weights, feature_rows, counters = [], [], []
    for profile_index, profile in enumerate(cert["profiles"]):
        labels, weight = profile["labels"], int(profile["weight_numerator"])
        assert weight > 0
        arrangement.validate(labels)
        path = realize(arrangement, labels)
        axes = ([p[0] for p in path], [p[1] for p in path])
        difference, constant, equal, later = [0]*(size+1), 0, 0, 0
        for w, pair in atoms:
            for route in pair:
                point = arrangement.claimed_capture(route, labels)
                actual = physical_capture(route, path, axes)
                limiting = tuple(q.limit for q in actual)
                # A later capture along this monotone Monster route only
                # strengthens the lower bound for every increasing warp.
                assert all(a >= b for a, b in zip(limiting, point)), (
                    "early limiting capture", profile_index, route, point, limiting)
                if limiting == point:
                    equal += 1
                else:
                    later += 1
                for q in point:
                    c, sign, radius = fold(q)
                    k = index[radius]
                    constant += w*c
                    difference[0] += w*sign
                    difference[k] -= w*sign
        running, row = constant, []
        for k in range(size):
            running += difference[k]
            row.append(running)
        assert row == list(map(int, profile["numerators"])), ("feature mismatch", profile_index)
        assert int(profile["denominator"]) == 4*denominator
        weights.append(weight)
        feature_rows.append(row)
        counters.append({"profile": profile_index, "path_vertices": len(path),
                         "equal_capture_limits": equal, "later_capture_limits": later})
    assert sum(weights) == mixture_denominator
    columns = [Q(sum(w*row[k] for w, row in zip(weights, feature_rows)),
                 4*denominator*mixture_denominator) for k in range(size)]
    assert columns == list(map(Q, cert["column_lower"]))
    lower = min(columns)
    assert lower == Q(cert["lower"])
    return {
        "status": "PASS",
        "scope": "Fixed weights and routes under all continuous strictly increasing odd two-periodic light-coordinate warps; not an unrestricted game lower bound.",
        "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "certificate_sha256": hashlib.sha256(payload).hexdigest(),
        "calendar_plans": len(data["paths"]), "distinct_physical_pairs": len(atoms),
        "queries": len(arrangement.v), "base_levels": len(arrangement.bases),
        "profiles": len(weights), "warp_increments": size,
        "exact_symbolic_captures": sum(c["equal_capture_limits"]+c["later_capture_limits"] for c in counters),
        "equal_capture_limits": sum(c["equal_capture_limits"] for c in counters),
        "later_capture_limits": sum(c["later_capture_limits"] for c in counters),
        "family_lower": str(lower), "source_n64_upper": data["global_upper"],
        "maximum_possible_upper_improvement": str(Q(data["global_upper"])-lower),
        "minimum_column_indices": [i for i, value in enumerate(columns) if value == lower],
        "realization": "Late connectors of width e^2; queried side offsets e; clipping to [e^6,1-e^6]; all comparisons use exact leading polynomial coefficients.",
        "profile_audit": counters,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--physical-certificate", type=Path, required=True)
    parser.add_argument("--family-certificate", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    result = verify(args.physical_certificate, args.family_certificate)
    args.report.write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps({k: v for k, v in result.items() if k != "profile_audit"}, indent=2))


if __name__ == "__main__":
    main()
