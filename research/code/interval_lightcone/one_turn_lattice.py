"""
One-turn Monster family versus an unrestricted lattice Princess, in light-cone
coordinates U = t + x, W = t - x.

Units: delta = 1/(2N).  Monster parameters live on even multiples of delta
(a = i*h, b = j*h with h = 1/N); the Princess lives on odd multiples, so no
ties ever occur.

Monster path P_b(a) (original): start x=a, run right until t+x=b, run left to
-1, run right to +1.  Its mirror is used with probability 1/2.
Family: a = i*h, i in [-N, N]; b = j*h with max(|a|, a) <= b <= 2-a.

Princess: radial staircase below the diagonal, 0 <= U-W <= 2, used with a fair
sign.  State of her best-response DP: (k0, m, k) with r0=(2*k0+1)*delta,
U=(2m+1)*delta, W=(2k+1)*delta.
"""
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import csr_matrix, vstack, hstack
import time, sys


class Game:
    def __init__(self, N, bmask=None):
        self.N = N
        N_ = N
        self.ia = np.arange(-N, N + 1)            # a index
        self.nb = 3 * N + 1                        # b index 0..3N
        ii, jj = np.meshgrid(self.ia, np.arange(self.nb), indexing="ij")
        ok = (jj >= np.abs(ii)) & (jj <= 2 * N - ii)
        if bmask is not None:
            ok &= bmask(ii, jj, N)
        self.ok = ok
        self.vars = np.argwhere(ok)                # rows: (a_row, j)
        self.nvar = len(self.vars)
        self.varid = -np.ones(ok.shape, dtype=np.int64)
        self.varid[ok] = np.arange(self.nvar)

    # ---- capture-time row for one Princess curve -------------------------
    def curve_cross(self, k0, moves):
        """moves: array of 0 (right, U+=2) / 1 (up, W+=2) from the start.
        Returns wc[c] (W when crossing U-line index c), uc[c + N] (U when
        crossing W-line index c, c from -N..3N)."""
        N = self.N
        m, k = k0, -k0 - 1
        wc = np.full(5 * N + 3, np.iinfo(np.int64).min, dtype=np.int64)
        uc = np.full(4 * N + 3, np.iinfo(np.int64).min, dtype=np.int64)
        for mv in moves:
            if mv == 0:
                m += 1
                wc[m] = 2 * k + 1
            else:
                k += 1
                uc[k + N] = 2 * m + 1
        return wc, uc

    def cost_row(self, k0, moves):
        """Return vector over variables of (2T_o + 2T_m) in delta units."""
        N = self.N
        wc, uc = self.curve_cross(k0, moves)
        i = self.ia[self.vars[:, 0]]
        j = self.vars[:, 1]
        To = np.empty(self.nvar, dtype=np.float64)
        outside = i >= k0 + 1
        To[outside] = 2 * j[outside] + wc[j[outside]]
        ins = ~outside
        u = uc[-i[ins] + N]
        caught = u < 2 * j[ins]
        To_in = np.where(caught, u - 2 * i[ins], 4 * j[ins] + 12 * N - 1)
        To[ins] = To_in
        Tm = np.empty(self.nvar, dtype=np.float64)
        mo = -i >= k0 + 1
        Tm[mo] = -2 * i[mo] + wc[-i[mo]]
        mi = ~mo
        Tm[mi] = 2 * j[mi] + uc[j[mi] + N]
        if (To < 0).any() or (Tm < 0).any():
            raise RuntimeError("curve does not cross a needed line")
        return To + Tm

    # ---- Princess best response by DP -----------------------------------
    def best_response(self, mu, want_curves=True):
        """mu: vector over variables. Returns (values[k0], curves[k0])."""
        N = self.N
        M = np.zeros(self.ok.shape)
        M[self.ok] = mu
        # M[a_row, j]; a index i = a_row - N
        # M1[k0][j] = sum_{i >= k0+1} M[i][j]
        suf = np.cumsum(M[::-1], axis=0)[::-1]      # suf[r][j] = sum_{rows >= r}
        suf = np.vstack([suf, np.zeros((1, self.nb))])
        k0s = np.arange(N)
        M1 = suf[k0s + 1 + N]                        # (N, nb)
        M2 = suf[-k0s + N]                           # (N, nb)   i >= -k0
        ma = M.sum(axis=1)                           # per a_row
        # originals caught/escape tables per a_row and m:
        # Cw[r][m] = sum_{j >= m+1} M[r][j];  Er[r][m] = sum_{j <= m} M[r][j]*(4j+12N)
        sufj = np.cumsum(M[:, ::-1], axis=1)[:, ::-1]
        sufj = np.hstack([sufj, np.zeros((2 * N + 1, 5 * N + 3 - self.nb + 1))])
        esc = np.cumsum(M * (4 * np.arange(self.nb) + 12 * N - 1)[None, :], axis=1)
        esc = np.hstack([esc, np.repeat(esc[:, -1:], 5 * N + 3 - self.nb + 1, axis=1)])
        smax = 5 * N + 3 * N                          # m up to 5N, k up to 3N
        D = 2 * N                                     # d = m-k in [0, 2N]
        nd = D + 1
        phi_next = np.zeros((N, nd))
        dec = np.zeros((smax + 2, N, nd), dtype=np.uint8) if want_curves else None
        NEG = -1e18
        for s in range(smax, -2, -1):
            # points (m,k) with m+k = s, d=m-k same parity as s
            d = np.arange(s % 2 if s >= 0 else 1, nd, 2)
            m = (s + d) // 2
            k = (s - d) // 2
            valid = (m >= 0) & (m <= 5 * N) & (k >= -N) & (k <= 3 * N)
            phi = np.full((N, nd), NEG)
            if not valid.any():
                phi_next = phi
                continue
            d = d[valid]; m = m[valid]; k = k[valid]
            # right step -> (m+1,k): d+1; crosses U-line index c = m+1 at height W=2k+1
            c = m + 1
            wv = np.zeros((N, len(d)))
            cb = np.minimum(c, self.nb - 1)
            inb = c <= self.nb - 1
            wv[:, inb] += M1[:, cb[inb]]
            ina = c <= N
            if ina.any():
                # mirrors starting at +c (a index -c), only if c >= k0+1
                add = ma[-c[ina] + N][None, :] * (c[ina][None, :] >= (k0s[:, None] + 1))
                wv[:, ina] += add
            Rv = wv * (2 * m + 2 + 2 * k + 1)[None, :]
            right_ok = (d + 1 <= D) & (m + 1 <= 5 * N)
            vr = np.full((N, len(d)), NEG)
            vr[:, right_ok] = phi_next[:, d[right_ok] + 1] + Rv[:, right_ok]
            # up step -> (m,k+1): d-1; crosses W-line index c = k+1 at U=2m+1
            c2 = k + 1
            Rh = np.zeros((N, len(d)))
            inb2 = (c2 >= 0) & (c2 <= self.nb - 1)
            if inb2.any():
                Rh[:, inb2] += M2[:, c2[inb2]] * (2 * c2[inb2] + 2 * m[inb2] + 1)[None, :]
            ina2 = (c2 >= -N) & (c2 <= N)
            if ina2.any():
                r = -c2[ina2] + N
                mm = m[ina2]
                Rh[:, ina2] += (sufj[r, mm + 1] * (2 * c2[ina2] + 2 * mm + 1) + esc[r, mm])[None, :]
            up_ok = (d - 1 >= 0) & (k + 1 <= 3 * N)
            vu = np.full((N, len(d)), NEG)
            vu[:, up_ok] = phi_next[:, d[up_ok] - 1] + Rh[:, up_ok]
            best = np.maximum(vr, vu)
            # terminal: if neither move possible (top corner) value 0
            none = ~(right_ok | up_ok)
            best[:, none] = 0.0
            # if k == 3N and at boundary, also allow termination
            term = (k >= 3 * N)
            best[:, term] = np.maximum(best[:, term], 0.0)
            phi[:, d] = best
            if want_curves:
                dec[s + 1][:, d] = (vu > vr).astype(np.uint8) + 2 * (np.maximum(vr, vu) < 0).astype(np.uint8)
            phi_next = phi
        # start: s = -1, d = 2k0+1
        vals = phi_next[k0s, 2 * k0s + 1]
        curves = None
        if want_curves:
            curves = []
            for k0 in range(N):
                m, k = k0, -k0 - 1
                mv = []
                while True:
                    s = m + k
                    if s > smax:
                        break
                    dd = dec[s + 1][k0, m - k]
                    if dd >= 2 or (k >= 3 * N):
                        break
                    if dd == 1:
                        k += 1; mv.append(1)
                    else:
                        m += 1; mv.append(0)
                # pad: go up along boundary / right until k = 3N
                while k < 3 * N:
                    if m - k < 2 * N and m < 5 * N:
                        m += 1; mv.append(0)
                    else:
                        k += 1; mv.append(1)
                curves.append(np.array(mv, dtype=np.uint8))
        return vals, curves


def solve(N, iters=200, tol=1e-7, bmask=None, verbose=True, init_curves=None, add_per_iter=None):
    g = Game(N, bmask)
    delta = 1.0 / (2 * N)
    rows = []
    meta = []

    def add_curve(k0, mv):
        rows.append(g.cost_row(k0, mv) * delta / 4.0)
        meta.append((k0, mv))

    # initial cuts: static-ish paths via best response to the sweeper pair
    mu0 = np.zeros(g.nvar)
    mu0[g.varid[N + N, N]] = 1.0          # a=1,b=1
    vals, curves = g.best_response(mu0)
    for k0 in range(N):
        add_curve(k0, curves[k0])
    if init_curves:
        for k0, mv in init_curves:
            add_curve(k0, mv)
    hist = []
    mu = mu0
    for it in range(iters):
        A = np.array(rows)
        nr = A.shape[0]
        # variables: mu (nvar), v ; minimize v ; A mu - v <= 0 ; sum mu = 1
        c = np.zeros(g.nvar + 1); c[-1] = 1.0
        A_ub = np.hstack([A, -np.ones((nr, 1))])
        b_ub = np.zeros(nr)
        A_eq = np.zeros((1, g.nvar + 1)); A_eq[0, :g.nvar] = 1.0
        res = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=[1.0],
                      bounds=[(0, None)] * g.nvar + [(None, None)], method="highs")
        if res.status != 0:
            raise RuntimeError(res.message)
        mu = res.x[:g.nvar]; v = res.x[-1]
        duals = -res.ineqlin.marginals
        vals, curves = g.best_response(mu)
        vals = vals * delta / 4.0
        ub = vals.max()
        hist.append((v, ub))
        if verbose:
            print(f"it {it:3d} rows {nr:5d} LP lower {v:.8f}  BR upper {ub:.8f}  gap {ub - v:.2e}", flush=True)
        if ub - v < tol:
            break
        order = np.argsort(-vals)
        cnt = 0
        for k0 in order:
            if vals[k0] > v + tol * 0.5:
                add_curve(int(k0), curves[k0]); cnt += 1
                if add_per_iter and cnt >= add_per_iter:
                    break
    return g, mu, v, ub, rows, meta, duals


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(description="One-turn Monster family P_b(a), |a| <= b <= 2-a, versus a lattice Princess.")
    ap.add_argument("N", type=int)
    ap.add_argument("--only-main-levels", action="store_true", help="restrict to b = 1 and b = 2 - a")
    ap.add_argument("--verbose", action="store_true")
    a = ap.parse_args()
    mask = (lambda ii, jj, N: (jj == N) | (jj == 2 * N - ii)) if a.only_main_levels else None
    t0 = time.time()
    g, mu, v, ub, rows, meta, duals = solve(a.N, iters=2000, bmask=mask, verbose=a.verbose)
    print("N", a.N, "lattice value", v, "best response", ub, "sup-model value (+1/(4N))", v + 1 / (4 * a.N),
          "time", round(time.time() - t0, 1))
    M = np.zeros(g.ok.shape); M[g.ok] = mu
    for r, j in np.argwhere(M > 1e-7):
        print("a=%+.4f b=%.4f  w=%.6f" % ((r - a.N) / a.N, j / a.N, M[r, j]))
