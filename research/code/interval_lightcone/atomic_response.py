"""Exact Princess response to an atomic Monster law of one-turn pairs P_b(a) and two-turn pairs T2(c, U1).

This is the Python reference for `atomic_upper.cpp`.  Both read the same compact law, place the atoms on the
grid 1/N in integer weights, and maximise the Princess's total reward over all cell staircases.  The two
programs share no code; `check_atomic_upper.py` compares their integer outputs.

Geometry (light coordinates U = t + x, W = t - x, h = 1/N, delta = h/2):

  P_b(a)     start a, right until U = b, left to -1, right to +1.        |a| <= b <= 2 - a
  T2(c, U1)  start c, right until U = U1, left until W = 1, right to +1, left to -1.   |c| <= U1 <= 1

Every atom is a pair: the path and its mirror image, each with half of the atom's weight.  A radial Princess
path is a monotone curve from (r0, -r0) inside 0 <= U - W <= 2.  With w(c) the height at which she first
reaches U = c and u(y) the abscissa at which she first reaches W = y, the capture times are

  P_b(a),   a > r0 :  (b + w(b)) / 2
            a < r0 :  (u(-a) - a) / 2  if u(-a) <= b,  otherwise at most b + 3
  mirror,  -a > r0 :  (-a + w(-a)) / 2
           -a < r0 :  (b + u(b)) / 2
  T2(c,U1), c > r0 :  (U1 + w(U1)) / 2
            c < r0 :  (u(-c) - c) / 2  if u(-c) <= U1, otherwise at most 2
  mirror,  -c > r0 :  (-c + w(-c)) / 2
           -c < r0 :  (U1 + u(U1)) / 2 if u(U1) <= 1,  otherwise at most 4

A curve that avoids the lattice points visits a staircase of cells (m, k): U in (m, m+1) h, W in (k, k+1) h.
Crossing the line U = (m+1) h from the cell (m, k) happens at W < (k+1) h, and crossing W = (k+1) h happens at
U < (m+1) h, so every capture time is at most its value at the far corner of the cell.  Rewards are 2T/delta
times the weight, so the expected capture time is (total reward) / (8 N W), W the total weight.

The proof that this bounds every Princess path is in
research/UPPER_BOUND.md.
"""
import numpy as np


def read_law(path):
    """Compact law: `mesh n`, `levels nb`, `denominator D`, `sweep m`, then bin records

        P1p i m | Sp i m | P1m i m | Sm i m      start bin i of P_1(a), S(a) = P_{2-a}(a), P_1(-c), S(-c)
        Qp i j m | Qm i j m                      P_b(a) / P_b(-c): start bin i, level bin j
        Tp i j m | Tm i j m                      T2(c, U1) / T2(-c, U1): start bin i, U1 bin j

    Start bin i is [i/n, (i+1)/n]; level bin j is [(n - nb + j)/n, (n - nb + j + 1)/n]; U1 bin j is
    [j/n, (j+1)/n].  Masses are integers that sum to D."""
    law = dict(recs=[])
    for line in open(path):
        p = line.split()
        if not p:
            continue
        if p[0] in ("mesh", "levels", "denominator", "sweep"):
            law[p[0]] = int(p[1])
        else:
            law["recs"].append((p[0], [int(x) for x in p[1:-1]], int(p[-1])))
    assert law["sweep"] + sum(m for _, _, m in law["recs"]) == law["denominator"]
    return law


def atoms(law, N):
    """Atoms on the grid 1/N by the product trapezoid rule.  Returns (P, T, W): P[(a, b)] and T[(c, U1)] are
    integer weights in grid indices, W = 4 r^2 D with r = N / mesh is their total."""
    n, nb = law["mesh"], law["levels"]
    assert N % n == 0
    r = N // n
    P, T = {}, {}

    def add(d, key, w):
        d[key] = d.get(key, 0) + w

    def end(t):
        return 1 if t in (0, r) else 2

    add(P, (N, N), law["sweep"] * 4 * r * r)            # P_1(1) and its mirror: the two endpoint sweeps
    for kind, idx, m in law["recs"]:
        i = idx[0]
        for t in range(r + 1):
            a = i * r + t
            if kind == "P1p":
                add(P, (a, N), m * 2 * r * end(t))
            elif kind == "Sp":
                add(P, (a, 2 * N - a), m * 2 * r * end(t))
            elif kind == "P1m":
                add(P, (-a, N), m * 2 * r * end(t))
            elif kind == "Sm":
                add(P, (-a, 2 * N + a), m * 2 * r * end(t))
            else:
                for u in range(r + 1):
                    w = m * end(t) * end(u)
                    if kind in ("Qp", "Qm"):
                        add(P, (a if kind == "Qp" else -a, (n - nb + idx[1]) * r + u), w)
                    elif kind in ("Tp", "Tm"):
                        add(T, (a if kind == "Tp" else -a, idx[1] * r + u), w)
                    else:
                        raise ValueError(kind)
    for (a, b) in P:
        assert abs(a) <= b <= 2 * N - a
    for (c, u) in T:
        assert abs(c) <= u <= N
    W = sum(P.values()) + sum(T.values())
    assert W == law["denominator"] * 4 * r * r
    return P, T, W


def response(N, P, T):
    """Maximum total reward for each start cell k0 = 0..N-1 (the Princess starts in (k0, k0+1) h).
    Integer arithmetic in int64; the caller keeps (48 N + 8) * (total weight) below 2^62."""
    assert (48 * N + 8) * (sum(P.values()) + sum(T.values())) < 2 ** 62
    dt = np.int64
    NU = 5 * N + 3
    NY = 4 * N + 3
    k0s = np.arange(N)
    VA = np.zeros((2 * N + 2, NU), dtype=dt)     # vertical legs of originals, by start index
    Vm = np.zeros(NU, dtype=dt)                  # vertical legs of mirrors, at the line U = -start
    MA = np.zeros((2 * N + 2, NY), dtype=dt)     # horizontal legs of one-turn mirrors, by start index
    MT = np.zeros((2 * N + 2, NY), dtype=dt)     # horizontal legs of two-turn mirrors (caught only while U < 1)
    capped = {}                                  # horizontal legs of originals: (row, cap, escape reward) -> weight
    for (a, b), w in P.items():
        VA[a + N, b] += w
        if -a >= 1:
            Vm[-a] += w
        key = (-a, b, 4 * b + 12 * N)
        capped[key] = capped.get(key, 0) + w
        MA[a + N, b + N] += w
    for (c, u), w in T.items():
        VA[c + N, u] += w
        if -c >= 1:
            Vm[-c] += w
        key = (-c, u, 8 * N)
        capped[key] = capped.get(key, 0) + w
        MT[c + N, u + N] += w
    V1 = np.cumsum(VA[::-1], axis=0)[::-1][k0s + 1 + N]          # starts > r0
    M2 = np.cumsum(MA[::-1], axis=0)[::-1][-k0s + N]             # mirrors that start left of the Princess
    M3 = np.cumsum(MT[::-1], axis=0)[::-1][-k0s + N]
    CW = np.zeros((NY, NU + 1), dtype=dt)
    ER = np.zeros((NY, NU + 1), dtype=dt)
    for (y, cap, esc), w in capped.items():
        CW[y + N, :cap] += w                     # crossing row y in column m is a capture iff m + 1 <= cap
        ER[y + N, cap:] += w * esc
    D = 2 * N
    NEG = -(1 << 62)
    phi_next = np.zeros((N, D + 1), dtype=dt)
    for s in range(8 * N, -2, -1):               # antidiagonals s = m + k of the cells
        d = np.arange(s % 2 if s >= 0 else 1, D + 1, 2)
        m = (s + d) // 2
        k = (s - d) // 2
        valid = (m >= 0) & (m <= 5 * N) & (k >= -N) & (k <= 3 * N)
        phi = np.full((N, D + 1), NEG, dtype=dt)
        if not valid.any():
            phi_next = phi
            continue
        d, m, k = d[valid], m[valid], k[valid]
        coord = (2 * (m + 1) + 2 * (k + 1)).astype(dt)
        c = m + 1
        wv = V1[:, c].copy()
        inm = c <= N
        if inm.any():
            wv[:, inm] += Vm[c[inm]][None, :] * (c[inm][None, :] >= (k0s[:, None] + 1))
        right_ok = (d + 1 <= D) & (m + 1 <= 5 * N)
        vr = np.full((N, len(d)), NEG, dtype=dt)
        vr[:, right_ok] = phi_next[:, d[right_ok] + 1] + (wv * coord[None, :])[:, right_ok]
        y = k + 1
        yy = y + N
        cap1 = (m + 1 <= N)
        rew = (CW[yy, m][None, :] + M2[:, yy] + M3[:, yy] * cap1[None, :]) * coord[None, :] \
            + ER[yy, m][None, :] + M3[:, yy] * (~cap1)[None, :] * (16 * N)
        up_ok = (d - 1 >= 0) & (k + 1 <= 3 * N)
        vu = np.full((N, len(d)), NEG, dtype=dt)
        vu[:, up_ok] = phi_next[:, d[up_ok] - 1] + rew[:, up_ok]
        best = np.maximum(vr, vu)
        top = (k >= 3 * N)
        best[:, top] = np.maximum(best[:, top], 0)
        best[:, ~(right_ok | up_ok)] = 0
        phi[:, d] = best
        phi_next = phi
    return phi_next[k0s, 2 * k0s + 1]            # start cell (k0, -k0-1): s = -1, d = 2 k0 + 1
