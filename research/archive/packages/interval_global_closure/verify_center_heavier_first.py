#!/usr/bin/env python3
"""Exact algebra regression for CENTER_HEAVIER_FIRST_BALANCE.md.

No pricing, approximation-transfer, or new game-value claim is made here.
The analytic proof uses these identities for all admissible fields and
continuations; this finite test exercises them independently with Fractions.
"""

from fractions import Fraction as F
from itertools import product
import json


def capped_future(left, right, pieces):
    return sum(weight * (min(left, a) + min(right, b))
               for weight, a, b in pieces)


def symmetric_envelope(left, right, families):
    return min(capped_future(x, y, pieces)
               for pieces in families
               for x, y in ((left, right), (right, left)))


def triangle(t, h):
    assert 0 <= t <= 2*h
    return min(t, 2*h-t)


def verify():
    grid = [F(k, 16) for k in range(9)]
    heights = (F(1, 8), F(1, 3), F(3, 4))
    # Positive weights sum to one; the last cap is the peak cap. The
    # interior caps are nonincreasing, as on a legal outward ray.
    normalized_weights = (F(1, 7), F(2, 7), F(4, 7))
    future_families = (
        ((F(1, 3), F(1, 8), F(3, 8)),
         (F(5, 3), F(0), F(1, 4))),
        ((F(3, 2), F(1, 2), F(1, 16)),
         (F(1, 2), F(3, 16), F(0))),
        ((F(2), F(1, 2), F(1, 2)),),
    )
    algebra = reflection = envelope = direct = 0
    for l in grid:
        for r in grid:
            if l > r:
                continue
            for peak in grid:
                for middle in grid:
                    if middle < peak:
                        continue
                    caps = (F(1, 2), middle, peak)
                    p, q = min(l, peak), min(r, peak)
                    sorted_heavy = tuple(sorted((l, q)))
                    assert sorted_heavy == (p, max(l, q))
                    assert sorted_heavy[0] == p and sorted_heavy[1] <= r
                    for h in heights:
                        i_l = h * sum(w * min(l, cap)
                                      for w, cap in zip(normalized_weights, caps))
                        i_r = h * sum(w * min(r, cap)
                                      for w, cap in zip(normalized_weights, caps))
                        assert 0 <= i_r-i_l <= h*(r-l)
                        assert 0 <= q-p <= r-l
                        heavy = 2*h*l + i_r + h*q
                        light = 2*h*r + i_l + h*p
                        assert heavy <= light
                        algebra += 1
                        for pieces in future_families:
                            # Reuse either the original fixed continuation
                            # or its reflection; no value oracle is used.
                            old = capped_future(p, r, pieces)
                            reused = min(capped_future(l, q, pieces),
                                         capped_future(q, l, pieces))
                            assert reused <= old
                            assert heavy + reused <= light + old
                            reflection += 1
                        assert symmetric_envelope(l, q, future_families) <= \
                            symmetric_envelope(p, r, future_families)
                        envelope += 1
                    unit_l = sum(w * min(l, cap)
                                 for w, cap in zip(normalized_weights, caps))
                    unit_r = sum(w * min(r, cap)
                                 for w, cap in zip(normalized_weights, caps))
                    assert (3*l+unit_r)-(3*r+unit_l) <= -2*(r-l)
                    direct += 1

    merging = 0
    for h1, h2 in product((F(k, 16) for k in range(1, 8)), repeat=2):
        h = h1+h2
        assert h < 1
        # Every piecewise-linear breakpoint plus a uniform exact mesh.
        times = {F(0), h1, 2*h1, 2*h1+h2, 2*h, h}
        times.update(2*h*F(k, 32) for k in range(33))
        for t in times:
            old = triangle(t, h1) if t <= 2*h1 else triangle(t-2*h1, h2)
            assert triangle(t, h) >= old
            merging += 1

    held_merging = 0
    for h1, h2, wait in product((F(k, 16) for k in range(1, 6)),
                               (F(k, 16) for k in range(1, 6)),
                               (F(k, 16) for k in range(4))):
        h = h1+h2+wait/2
        assert h < 1
        times = {F(0), h1, 2*h1, 2*h1+wait,
                 2*h1+wait+h2, 2*h, h}
        times.update(2*h*F(k, 32) for k in range(33))
        for t in times:
            if t <= 2*h1:
                old = triangle(t, h1)
            elif t <= 2*h1+wait:
                old = F(0)
            else:
                old = triangle(t-2*h1-wait, h2)
            assert triangle(t, h) >= old
            held_merging += 1

    return {
        "status": "PASS",
        "scope": "exact heavier-first and rank-balance algebra regression",
        "cap_cost_checks": algebra,
        "fixed_continuation_reflection_checks": reflection,
        "symmetric_monotone_envelope_checks": envelope,
        "direct_tour_checks": direct,
        "same_sign_triangle_pointwise_checks": merging,
        "same_sign_triangles_with_center_hold_checks": held_merging,
        "new_game_value_bound_claimed": False,
    }


if __name__ == "__main__":
    print(json.dumps(verify(), sort_keys=True, indent=2))
