#!/usr/bin/env python3
"""Exact fixtures for the complete canonical one-turn response formula.

This audits the identities and boundary conventions in
research/13-equilibrium-geometry/ONE_TURN_COMPLETE_DOMAIN.md.  The general
exhaustion and finite-partition theorems are proved there, not by this test.
All arithmetic below is fractions.Fraction; no optimization or CI is used.
"""

from __future__ import annotations

from bisect import bisect_right
from dataclasses import dataclass
from fractions import Fraction as F
import json
from random import Random


@dataclass(frozen=True)
class Path:
    nodes: tuple[tuple[F, F], ...]

    @classmethod
    def make(cls, nodes):
        out = []
        for t, x in nodes:
            t, x = F(t), F(x)
            assert -1 <= x <= 1
            if out and out[-1][0] == t:
                assert out[-1][1] == x
                continue
            if out:
                assert t > out[-1][0]
                assert abs(x - out[-1][1]) <= t - out[-1][0]
            out.append((t, x))
        assert out[0][0] == 0
        return cls(tuple(out))

    def at(self, t):
        t = F(t)
        i = bisect_right([node[0] for node in self.nodes], t) - 1
        assert i >= 0
        if i == len(self.nodes) - 1:
            return self.nodes[i][1]
        t0, x0 = self.nodes[i]
        t1, x1 = self.nodes[i + 1]
        return x0 + (t - t0) * (x1 - x0) / (t1 - t0)

    def reflected(self):
        return Path.make((t, -x) for t, x in self.nodes)


@dataclass(frozen=True)
class Law:
    paths: tuple[Path, ...]
    weights: tuple[F, ...]

    def __post_init__(self):
        assert len(self.paths) == len(self.weights)
        assert all(w > 0 for w in self.weights)
        assert sum(self.weights) == 1
        knots = {t for p in self.paths for t, _ in p.nodes}
        for t in knots:
            xs = [p.at(t) for p in self.paths]
            assert xs == sorted(xs), "CDF identity is for ordered paths"

    def cdf(self, t, x, *, closed):
        if closed:
            return sum((w for p, w in zip(self.paths, self.weights)
                        if p.at(t) <= x), F(0))
        return sum((w for p, w in zip(self.paths, self.weights)
                    if p.at(t) < x), F(0))

    def reflected(self):
        return Law(tuple(p.reflected() for p in reversed(self.paths)),
                   tuple(reversed(self.weights)))


def monster(a, h):
    a, h = F(a), F(h)
    assert -1 <= a <= 1 and 0 <= h <= 1 - a
    H = 1 + a + 2 * h
    return Path.make(((0, a), (h, a + h), (H, -1),
                      (H + 2, 1), (6, 1)))


def direct_first_hit(m, p):
    """Independent physical oracle: solve first intersection in each segment."""
    times = sorted({F(0), F(6)} |
                   {t for t, _ in m.nodes} | {t for t, _ in p.nodes})
    for lo, hi in zip(times, times[1:]):
        d0 = m.at(lo) - p.at(lo)
        d1 = m.at(hi) - p.at(hi)
        if d0 == 0:
            return lo
        if d0 * d1 <= 0:
            return lo + (hi - lo) * d0 / (d0 - d1)
    if m.at(times[-1]) == p.at(times[-1]):
        return times[-1]
    raise AssertionError("complete endpoint tour must capture by six")


def cdf_partition(m, law, end):
    """All exact CDF trace-change times; persistent coincidences stay whole."""
    cuts = {F(0), F(end)}
    cuts.update(t for t, _ in m.nodes if 0 <= t <= end)
    for p in law.paths:
        times = sorted({F(0), F(end)} |
                       {t for t, _ in m.nodes if 0 <= t <= end} |
                       {t for t, _ in p.nodes if 0 <= t <= end})
        cuts.update(times)
        for lo, hi in zip(times, times[1:]):
            delta0 = p.at(lo) - m.at(lo)
            slope = ((p.at(hi) - p.at(lo)) -
                     (m.at(hi) - m.at(lo))) / (hi - lo)
            if slope:
                hit = lo - delta0 / slope
                if lo <= hit <= hi:
                    cuts.add(hit)
    return sorted(cuts)


def trace_formula(a, h, law):
    """Integrate the three formulas from exact marginal traces, not hit times."""
    a, h = F(a), F(h)
    b, H = a + 2 * h, 1 + a + 2 * h
    m = monster(a, h)
    A = law.cdf(0, a, closed=False)
    B = law.cdf(h, a + h, closed=True)
    cuts = cdf_partition(m, law, H + 2)
    answer = F(0)
    for lo, hi in zip(cuts, cuts[1:]):
        t = (lo + hi) / 2
        if t < h:
            survivor = 1 + A - law.cdf(t, a + t, closed=True)
        elif t < H:
            survivor = 1 - B + min(A, law.cdf(t, b - t, closed=False))
        else:
            survivor = 1 - max(B, law.cdf(t, t - H - 1, closed=True))
        assert 0 <= survivor <= 1
        answer += (hi - lo) * survivor
    return answer


def physical_expectation(m, law):
    return sum((w * direct_first_hit(m, p)
                for p, w in zip(law.paths, law.weights)), F(0))


def static_law(points, weights=None):
    points = sorted(set(map(F, points)))
    if weights is None:
        weights = [F(1, len(points))] * len(points)
    return Law(tuple(Path.make(((0, x), (6, x))) for x in points),
               tuple(map(F, weights)))


def random_ordered_law(rng):
    # Sorting each time slice preserves the speed bound of the original
    # finite particle system (one-dimensional bottleneck matching).
    count = 7
    raw = [rng.randrange(-4, 5) for _ in range(count)]
    slices = [sorted(raw)]
    for _ in range(12):
        raw = [max(-4, min(4, x + rng.randrange(-2, 3))) for x in raw]
        slices.append(sorted(raw))
    paths = tuple(Path.make((F(j, 2), F(slices[j][i], 4))
                            for j in range(13)) for i in range(count))
    numerators = [rng.randrange(1, 8) for _ in range(count)]
    total = sum(numerators)
    return Law(paths, tuple(F(n, total) for n in numerators))


def fixtures():
    endpoints = static_law([-1, 1])
    dense = static_law([F(-1), F(-3, 4), F(-1, 2), F(0),
                       F(1, 4), F(3, 4), F(1)],
                      [F(n, 16) for n in [1, 2, 3, 4, 3, 2, 1]])
    ranks = [F(i, 4) for i in range(-4, 5)]
    collapse = Law(tuple(Path.make(((0, r), (1, 0), (2, 0),
                                    (3, r), (6, r))) for r in ranks),
                   tuple([F(1, 9)] * 9))
    shifts = [F(0), F(1, 2), F(0), F(-1, 2), F(0),
              F(1, 2), F(0), F(1), F(0), F(-1)]
    times = [F(0), F(1, 2), F(1), F(3, 2), F(2), F(5, 2),
             F(3), F(4), F(5), F(6)]
    wave = Law(tuple(Path.make((t, max(F(-1), min(F(1), r + shift)))
                               for t, shift in zip(times, shifts))
                     for r in ranks), tuple([F(1, 9)] * 9))
    rng = Random(20261114)
    return [endpoints, dense, collapse, wave] + [
        random_ordered_law(rng) for _ in range(12)]


def main():
    laws = fixtures()
    cases = sorted({(F(i, 4), (1 - F(i, 4)) * F(k, 8))
                    for i in range(-4, 5) for k in range(9)} |
                   {(F(-7, 8), F(123, 128)),
                    (F(-7, 8), F(1, 16)),
                    (F(-3, 4), F(3, 4))})
    checks = 0
    for law in laws:
        reflected = law.reflected()
        for a, h in cases:
            m = monster(a, h)
            assert trace_formula(a, h, law) == physical_expectation(m, law)
            assert trace_formula(a, h, reflected) == physical_expectation(
                m.reflected(), law)
            checks += 2

    # Each parameter receives an initial atom and an atom precisely at its
    # turning location, plus a positive-mass path coinciding with the Monster.
    tie_checks = 0
    for a, h in cases:
        tied_static = static_law([-1, a, a + h, 0, 1])
        m = monster(a, h)
        tied_moving = Law((Path.make(((0, -1), (6, -1))), m,
                          Path.make(((0, 1), (6, 1)))),
                         (F(1, 4), F(1, 2), F(1, 4)))
        for law in (tied_static, tied_moving):
            assert trace_formula(a, h, law) == physical_expectation(m, law)
            tie_checks += 1

    # Added endpoint-face routes may be noncanonical, but are all dominated
    # pathwise by the immediate endpoint sweep represented at (-1,0).
    domination_checks = 0
    sweep = monster(-1, 0)
    for law in laws:
        for p in law.paths:
            for k in range(17):
                assert direct_first_hit(sweep, p) <= direct_first_hit(
                    monster(-1, F(k, 8)), p)
                domination_checks += 1

    endpoints = laws[0]
    for h in [F(1, 8), F(1, 2), F(7, 8), F(127, 128)]:
        assert trace_formula(0, h, endpoints) == 2 + 2 * h
    assert trace_formula(0, 1, endpoints) == 2
    assert trace_formula(0, F(1, 2), static_law([F(1, 2)])) == F(1, 2)

    late = trace_formula(F(-7, 8), F(123, 128), laws[1])
    print(json.dumps({
        "status": "PASS",
        "parameter_pairs": len(cases),
        "ordered_laws": len(laws),
        "oriented_formula_comparisons": checks,
        "initial_and_turn_tie_comparisons": tie_checks,
        "pathwise_endpoint_face_comparisons": domination_checks,
        "endpoint_jump": {"interior_limit": "4", "actual": "2"},
        "late_turn_fixture_cost": str(late),
        "scope": "exact fixtures; continuum theorems proved in manuscript",
    }, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
