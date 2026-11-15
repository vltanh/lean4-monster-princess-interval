#!/usr/bin/env python3
"""Exact continuum witness for the moving-rank first-inverse flux.

This standalone reconstruction was preserved during the 2026-11-11 executor
outage.  It evaluates a physical ordered ordinary-wave family with Fraction
arithmetic.  The cost is integrated from its first inverses independently of
the proposed derivative formula.  No finite rank approximation is used.

The unit-speed initial segment for rank q starts at a(q), turns at incoming
coordinate u(q), and finally departs on outgoing coordinate c(q), with center
waiting if u(q)<c(q).  Every path absorbs at its first endpoint hit.
"""
from fractions import Fraction as Q
import json


def a(q):
    return Q(1, 5) + q / 2


def u(q):
    return Q(2, 5) + q / 2


def c(q):
    return Q(3, 4) - q / 2


def alpha(S, q):
    """First time t+p_q(t) reaches S, including first-contact traces."""
    aq, uq, cq = a(q), u(q), c(q)
    if S <= aq:
        return Q(0)
    if S <= uq:
        return (S - aq) / 2
    if uq < cq and S <= cq:
        return S
    if S <= cq + 2:
        return (S + cq) / 2
    return S - 1


def beta(V, q):
    """First time t-p_q(t) reaches V, including first-contact traces."""
    aq, uq, cq = a(q), u(q), c(q)
    if V <= -aq:
        return Q(0)
    if V <= min(uq, cq):
        return (uq + V) / 2
    if uq < cq and V <= cq:
        return V
    return V + 1


def clip(q):
    return min(Q(1), max(Q(0), q))


def A(x):
    return clip(2 * (x - Q(1, 5)))


def I(U):
    return clip(2 * (U - Q(2, 5)))


def C(V):
    return clip(2 * (Q(3, 4) - V))


def R(U, V):
    return min(C(V), max(A(-V), I(U)))


def RU_right(U, V):
    incoming = I(U)
    if Q(0) < incoming < Q(1) and incoming >= A(-V) and incoming < C(V):
        return Q(2)
    return Q(0)


def integrate_affine(fn, lo, hi):
    """Exact trapezoid; also verifies the asserted affine rank regime."""
    if lo == hi:
        return Q(0)
    assert lo < hi
    left, mid, right = fn(lo), fn((lo + hi) / 2), fn(hi)
    assert 2 * mid == left + right, (lo, hi, left, mid, right)
    return (hi - lo) * (left + right) / 2


U0, V, w, s = Q(3, 5), Q(-11, 20), Q(-3, 10), Q(4, 5)
L, M = Q(3, 5), Q(7, 10)


def moment2(U):
    """Twice the unresolved absolute moment of the fixed future plan."""
    ell = R(U, w)
    upper = max(M, R(s, w))
    assert Q(7, 20) < ell < L
    assert R(U, V) == M
    assert upper == Q(4, 5)
    first = integrate_affine(lambda q: alpha(U, q), ell, L)
    lower = integrate_affine(lambda q: alpha(s, q), Q(0), ell)
    higher = integrate_affine(lambda q: beta(w, q), M, upper)
    last_positive = (s + 3) * (1 - upper)
    reflected = integrate_affine(lambda q: beta(s, q), Q(0), Q(1))
    return first + lower + higher + last_positive + reflected


ell = R(U0, w)
assert ell == Q(2, 5)
assert R(U0, V) == M
assert moment2(U0) == Q(2311, 800)

# The direct first-inverse expression is quadratic on this open U interval.
step = Q(1, 10000)
values = [moment2(U0 + j * step) for j in (-1, 0, 1, 2)]
assert values[3] - 3 * values[2] + 3 * values[1] - values[0] == 0
direct = (values[2] - values[0]) / (2 * step)

# Integrate the prefix flux only over [-U,w], with the strict condition R<L.
cuts = sorted(set([-U0, -a(L), -a(ell), w]))
assert cuts[0] == -U0 and cuts[-1] == w
prefix_flux = sum(
    (right - left) * RU_right(U0, (left + right) / 2)
    for left, right in zip(cuts, cuts[1:])
    if R(U0, (left + right) / 2) < L
)
assert prefix_flux == Q(1, 5)
first_turn = (U0 + w) / 2
current_time = (U0 + V) / 2
incoming_term = (alpha(s, ell) - first_turn) * RU_right(U0, w)
upper_term = (beta(w, M) - current_time) * RU_right(U0, V)
correct = (L - ell + prefix_flux) / 2 + incoming_term - upper_term

# The pointwise inverse derivative is 1/2 for every q strictly above ell.
# It misses a positive moving-rank jump at q=ell.
pointwise_only = (L - ell) / 2 + incoming_term - upper_term
assert direct == correct == Q(5, 4)
assert pointwise_only == Q(23, 20)
assert direct - pointwise_only == Q(1, 10)
assert alpha(U0, ell) == Q(1, 10)
assert first_turn == Q(3, 20)

print(json.dumps({
    "status": "PASS",
    "scope": "one exact continuum moving-rank flux witness",
    "twice_absolute_moment": str(moment2(U0)),
    "direct_cost_derivative": str(direct),
    "correct_prefix_flux_derivative": str(correct),
    "pointwise_inverse_derivatives_only": str(pointwise_only),
    "missing_jump_flux": str(direct - pointwise_only),
    "finite_rank_discretization": False
}, indent=2))
