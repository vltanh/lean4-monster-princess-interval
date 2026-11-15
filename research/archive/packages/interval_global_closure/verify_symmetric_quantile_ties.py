#!/usr/bin/env python3
"""Exact audit of reflected quantile sampling at CDF plateau ranks.

The general two-trace quantile theorem is proved in
GLOBAL_MINIMAX_AND_CDF_DUALITY.md. This regression first exhibits the
ordinary lower-quantile error, then checks moving atomic laws. Every
temporal breakpoint and first contact is rational and exact. These
fixtures do not certify the infinite-dimensional minimax theorem.
"""
from fractions import Fraction as Q


ZERO, ONE = Q(0), Q(1)
TIMES = (ZERO, Q(1, 2), Q(3, 4), ONE, Q(3, 2), Q(2), Q(4))
HORIZON = TIMES[-1]


def inverse(atoms, q, upper=False):
    """Lower inverse uses CDF >= q; upper inverse uses CDF > q."""
    assert ZERO < q < ONE
    cumulative = ZERO
    for x, weight in sorted(atoms.items()):
        cumulative += weight
        if cumulative > q or (not upper and cumulative == q):
            return x
    raise AssertionError("quantile rank not reached")


def symmetric_quantile(atoms, q):
    return (inverse(atoms, q) + inverse(atoms, q, upper=True)) / 2


counterexample = {Q(-1): Q(1, 4), ZERO: Q(1, 2), ONE: Q(1, 4)}
assert (inverse(counterexample, Q(1, 4)),
        inverse(counterexample, Q(3, 4))) == (Q(-1), ZERO)
assert inverse(counterexample, Q(1, 4)) != -inverse(counterexample, Q(3, 4))
assert (symmetric_quantile(counterexample, Q(1, 4)),
        symmetric_quantile(counterexample, Q(3, 4))) == (Q(-1, 2), Q(1, 2))


def atomic_law(t, a, b):
    """Two reflected runner pairs plus a stationary center atom."""
    r1 = min(ONE, abs(t - ONE))
    r2 = min(ONE, abs(t - Q(1, 2)))
    entries = [(-r1, Q(a, 16)), (r1, Q(a, 16)),
               (-r2, Q(b, 16)), (r2, Q(b, 16)),
               (ZERO, Q(16 - 2 * a - 2 * b, 16))]
    atoms = {}
    for x, weight in entries:
        atoms[x] = atoms.get(x, ZERO) + weight
    assert sum(atoms.values()) == ONE
    return atoms


def interpolate(path, t):
    for (s, x), (u, y) in zip(path, path[1:]):
        if s <= t <= u:
            return x + (t - s) * (y - x) / (u - s)
    raise AssertionError("time outside path")


def legal(path):
    assert path[0][0] == ZERO and path[-1][0] == HORIZON
    for (s, x), (t, y) in zip(path, path[1:]):
        assert ZERO <= s < t <= HORIZON
        assert -ONE <= x <= ONE and -ONE <= y <= ONE
        assert abs(y - x) <= t - s


def first_contact(monster, princess):
    times = sorted({t for t, _ in monster} | {t for t, _ in princess})
    for s, t in zip(times, times[1:]):
        ds = interpolate(monster, s) - interpolate(princess, s)
        dt = interpolate(monster, t) - interpolate(princess, t)
        if ds == ZERO:
            return s
        if ds * dt <= ZERO:
            return s - ds * (t - s) / (dt - ds)
    raise AssertionError("completed Monster failed to capture")


def endpoint_tour(start):
    first = ONE if start >= ZERO else -ONE
    sigma = abs(first - start)
    points = [(ZERO, start)]
    if sigma > ZERO:
        points.append((sigma, first))
    points += [(sigma + 2, -first), (HORIZON, -first)]
    legal(points)
    return points


reflection_cases = contact_cases = survival_cases = 0
monsters = [endpoint_tour(Q(k, 4)) for k in range(-4, 5)]
for a in range(1, 4):
    for b in range(1, 4):
        phase_mids = [(s + t) / 2 for s, t in zip(TIMES, TIMES[1:])]
        inspect_times = sorted(set(TIMES) | set(phase_mids))
        # All possible atom-order changes occur in TIMES. CDF rank cuts
        # on those phases produce an exact finite ordered realization.
        rank_cuts = {ZERO, ONE}
        for t in inspect_times:
            cumulative = ZERO
            for _, weight in sorted(atomic_law(t, a, b).items()):
                cumulative += weight
                rank_cuts.add(cumulative)
        rank_cuts = sorted(rank_cuts)
        cells = [((l + r) / 2, r - l)
                 for l, r in zip(rank_cuts, rank_cuts[1:])]

        def path_at(q):
            path = [(t, symmetric_quantile(atomic_law(t, a, b), q))
                    for t in TIMES]
            legal(path)
            # Each original atom is affine with fixed order on a phase;
            # hence these are the complete affine quantile pieces.
            for t in phase_mids:
                assert interpolate(path, t) == symmetric_quantile(atomic_law(t, a, b), q)
            return path

        continuum = [(path_at(q), weight) for q, weight in cells]
        for t in inspect_times:
            reconstructed = {}
            for path, weight in continuum:
                x = interpolate(path, t)
                reconstructed[x] = reconstructed.get(x, ZERO) + weight
            assert reconstructed == atomic_law(t, a, b)

        for npaths in (2, 4, 6, 8, 16):
            ranks = [Q(2 * j + 1, 2 * npaths) for j in range(npaths)]
            sampled = [path_at(q) for q in ranks]
            for q, path in zip(ranks, sampled):
                opposite = path_at(ONE - q)
                assert all(x == -y for (_, x), (_, y) in zip(path, opposite))
                for t in inspect_times:
                    atoms = atomic_law(t, a, b)
                    assert inverse(atoms, ONE - q) == -inverse(atoms, q, upper=True)
                    reflection_cases += 1

            for monster in monsters:
                true_hits = [(first_contact(monster, path), weight)
                             for path, weight in continuum]
                sample_hits = [first_contact(monster, path) for path in sampled]
                true_cost = sum(t * weight for t, weight in true_hits)
                sample_cost = sum(sample_hits, ZERO) / npaths
                assert abs(true_cost - sample_cost) <= HORIZON / npaths
                contact_cases += 1
                events = sorted({ZERO, HORIZON} | {t for t, _ in true_hits}
                                | set(sample_hits))
                checks = events + [(s + t) / 2 for s, t in zip(events, events[1:])]
                for t in checks:
                    true_survival = sum((w for hit, w in true_hits if hit > t), ZERO)
                    sample_survival = Q(sum(hit > t for hit in sample_hits), npaths)
                    assert abs(true_survival - sample_survival) <= Q(1, npaths)
                    survival_cases += 1

print("Ordinary lower-inverse reflection fails; midpoint of both traces repairs it.")
print(f"Exact reflected-trace checks: {reflection_cases}")
print(f"Continuous-time first-contact/rank error checks: {contact_cases}")
print(f"Strict-survival checks at all capture events and intervening phases: {survival_cases}")
print("PASS: 9 moving atomic laws, 5 sample sizes, 9 completed Monster paths.")
