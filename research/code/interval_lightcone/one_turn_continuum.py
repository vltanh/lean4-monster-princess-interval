"""
Continuum one-turn game with piecewise-constant Monster start densities (exact integration).

Monster law (pairs = path + mirror, each prob 1/2):
  e          : sweeper pair
  Pp[i]      : P_1(a), a in (g_i,g_{i+1})      (start a>0, run right to U=1, left to -1, right to +1)
  Sp[i]      : S(a),   a in (g_i,g_{i+1})      (start a>0, run right to +1, left to -1)
  Pm[i]      : P_1(-c), c in (g_i,g_{i+1})
  Sm[i]      : S(-c),   c in (g_i,g_{i+1})
Princess: arbitrary radial staircase with corners on the mesh, start radius r0 = g_k.
Rewards are in units of (T_orig + T_mirror) per unit pair mass, i.e. 2*E[T].
"""
import numpy as np, sys, time, pickle
from scipy.optimize import linprog

class PC:
    def __init__(self, g):
        self.g = np.asarray(g, dtype=float); n = len(g) - 1; self.n = n
        g = self.g
        # U nodes
        self.Uc = np.concatenate([g[:n], [1.0, 1.0], 2 - g[n - 1::-1]])         # len 2n+2
        self.NU = 2 * n + 2
        # W nodes
        self.Wc = np.concatenate([-g[::-1], g[1:n], [1.0, 1.0], 2 - g[n - 1::-1]])  # -1..0 (n+1), g1..g_{n-1} (n-1), 1-,1+, 2-g..2 (n)
        self.NW = len(self.Wc)                                                  # 3n+2
        self.nvar = 4 * n + 1
        self.mid = 0.5 * (g[:-1] + g[1:]); self.dg = np.diff(g)

    def unpack(self, mu):
        n = self.n
        return mu[0], mu[1:1 + n], mu[1 + n:1 + 2 * n], mu[1 + 2 * n:1 + 3 * n], mu[1 + 3 * n:1 + 4 * n]

    # ---- geometry helpers -------------------------------------------------
    def bound_iu(self, jw):
        """largest allowed U index at W index jw (endpoint constraint); W<0 only matters."""
        n = self.n
        if jw <= n:                       # W = -g_i, i = n - jw
            i = n - jw
            return n + 1 if i == n else 2 * n + 1 - i
        return 2 * n + 1
    def min_iu(self, jw):
        """smallest allowed U index at W index jw (centre constraint U >= W)."""
        n = self.n
        if jw <= n: return 0
        if jw <= 2 * n - 1: return jw - n          # W = g_i, i = jw-n
        if jw == 2 * n: return n                   # 1-
        if jw == 2 * n + 1: return n + 1           # 1+
        i = 3 * n + 1 - jw                         # W = 2 - g_i
        return 2 * n + 1 - i

    def tail(self, mu):
        """Rtail[k, jw] for jw>=n : reward-to-go when at the endpoint (U=W+2) from W index jw on."""
        n = self.n; e, Pp, Sp, Pm, Sm = self.unpack(mu); g = self.g; mid = self.mid
        K = n + 1
        R = np.zeros((K, self.NW + 1))
        cumPm = np.concatenate([[0], np.cumsum(Pm)])      # sum_{i<k} Pm_i
        Pp_tot = Pp.sum()
        # beyond W=2: mirror S^- with c<r0: reward 2*(2+c)+2 per unit
        beyond = np.concatenate([[0], np.cumsum(Sm * (2 * (2 + mid) + 2))])   # index k
        R[:, self.NW] = 0
        top = beyond.copy()               # value at W = 2 node (jw = 3n+1)
        R[:, 3 * n + 1] = top
        for jw in range(3 * n, n - 1, -1):
            if jw >= 2 * n + 1:           # row from 2-g_{i+1} to 2-g_i
                i = 3 * n - jw
                rew = Sp[i] * (2 * (2 - mid[i]) + 2)
                R[:, jw] = R[:, jw + 1] + rew
            elif jw == 2 * n:             # atom W=1 at U=3
                E2 = e + Pp_tot + cumPm
                R[:, jw] = R[:, jw + 1] + 4 * E2
            else:                         # row from g_i to g_{i+1}, i=jw-n
                i = jw - n
                rew = Pm[i] * 8 + Sm[i] * (2 * mid[i] + 2)
                R[:, jw] = R[:, jw + 1] + rew
        return R

    def dp(self, mu, want_paths=True):
        n = self.n; e, Pp, Sp, Pm, Sm = self.unpack(mu); g = self.g; mid = self.mid
        K = n + 1; NU = self.NU; NW = self.NW
        ks = np.arange(K)
        Rt = self.tail(mu)
        sufPp = np.concatenate([np.cumsum(Pp[::-1])[::-1], [0]])     # sum_{i>=k}
        E1 = e + sufPp                                                # [k]
        cumPm = np.concatenate([[0], np.cumsum(Pm)])
        E2 = e + Pp.sum() + cumPm
        NEG = -1e18
        Phi = np.full((K, NU, NW), NEG)
        dec = np.zeros((K, NU, NW), dtype=np.int8) if want_paths else None
        Uc = self.Uc; Wc = self.Wc
        for jw in range(NW - 1, -1, -1):
            w = Wc[jw]
            imax = self.bound_iu(jw); imin = self.min_iu(jw)
            for iu in range(imax, imin - 1, -1):
                x = Uc[iu]
                if iu == 2 * n + 1 and jw >= n:
                    Phi[:, iu, jw] = Rt[:, jw]; continue
                best = np.full(K, NEG); bd = np.zeros(K, dtype=np.int8)
                # right move
                if iu + 1 <= imax:
                    if iu <= n - 1:
                        i = iu
                        rew = (Pm[i] + Sm[i]) * (mid[i] + w) * (ks <= i)
                    elif iu == n:
                        rew = E1 * (1 + w)
                    else:
                        i = 2 * n - iu          # U from 2-g_{i+1} to 2-g_i
                        rew = Sp[i] * ((2 - mid[i]) + w) * (ks <= i)
                    v = Phi[:, iu + 1, jw] + rew
                    best = v; bd[:] = 1
                # up move
                if jw + 1 < NW and self.min_iu(jw + 1) <= iu <= self.bound_iu(jw + 1):
                    if jw <= n - 1:
                        i = n - 1 - jw          # W from -g_{i+1} to -g_i
                        m = -mid[i]
                        rew = (Pp[i] * ((m + x) if iu <= n else 8.0) + Sp[i] * (m + x)) * (ks > i)
                    elif jw <= 2 * n - 1:
                        i = jw - n
                        rew = Pm[i] * ((mid[i] + x) if iu <= n else 8.0) + Sm[i] * (mid[i] + x)
                        rew = rew * np.ones(K)
                    elif jw == 2 * n:
                        rew = E2 * (1 + x)
                    else:
                        i = 3 * n - jw
                        rew = Sp[i] * ((2 - mid[i]) + x) * np.ones(K)
                    v = Phi[:, iu, jw + 1] + rew
                    upd = v > best
                    best = np.where(upd, v, best); bd = np.where(upd, 2, bd)
                # endpoint diagonal (only for W<0 boundary nodes)
                if jw <= n - 1 and iu == imax:
                    i = n - 1 - jw              # from (2-g_{i+1}, -g_{i+1}) to (2-g_i, -g_i)
                    iu2 = self.bound_iu(jw + 1)
                    rew = (Pp[i] * 8.0 + Sp[i] * (2 * (-mid[i]) + 2)) * (ks > i) + Sp[i] * (2 * (2 - mid[i]) - 2) * (ks <= i)
                    v = Phi[:, iu2, jw + 1] + rew
                    upd = v > best
                    best = np.where(upd, v, best); bd = np.where(upd, 3, bd)
                Phi[:, iu, jw] = best
                if want_paths: dec[:, iu, jw] = bd
        vals = np.array([Phi[k, k if k < n else n, n - k] for k in range(K)])
        self._dec = dec
        return vals, Phi

    def row(self, k):
        """coefficient row (over variables) of the optimal path from start k, using stored decisions."""
        n = self.n; g = self.g; mid = self.mid; dec = self._dec
        c = np.zeros(self.nvar)
        oP, oS, oPm, oSm = 1, 1 + n, 1 + 2 * n, 1 + 3 * n
        iu, jw = (k if k < n else n), n - k
        Uc = self.Uc; Wc = self.Wc
        path = [(iu, jw)]
        while True:
            if iu == 2 * n + 1 and jw >= n:
                # tail
                for j in range(jw, 3 * n + 1):
                    if j >= 2 * n + 1:
                        i = 3 * n - j; c[oS + i] += 2 * (2 - mid[i]) + 2
                    elif j == 2 * n:
                        c[0] += 4; c[oP:oP + n] += 4; c[oPm:oPm + k] += 4
                    else:
                        i = j - n; c[oPm + i] += 8; c[oSm + i] += 2 * mid[i] + 2
                c[oSm:oSm + k] += 2 * (2 + mid[:k]) + 2
                break
            d = dec[k, iu, jw]; x = Uc[iu]; w = Wc[jw]
            if d == 1:
                if iu <= n - 1:
                    i = iu
                    if k <= i: c[oPm + i] += mid[i] + w; c[oSm + i] += mid[i] + w
                elif iu == n:
                    c[0] += 1 + w; c[oP + k:oP + n] += 1 + w
                else:
                    i = 2 * n - iu
                    if k <= i: c[oS + i] += (2 - mid[i]) + w
                iu += 1
            elif d == 2:
                if jw <= n - 1:
                    i = n - 1 - jw
                    if k > i:
                        c[oP + i] += (-mid[i] + x) if iu <= n else 8.0
                        c[oS + i] += -mid[i] + x
                elif jw <= 2 * n - 1:
                    i = jw - n
                    c[oPm + i] += (mid[i] + x) if iu <= n else 8.0
                    c[oSm + i] += mid[i] + x
                elif jw == 2 * n:
                    c[0] += 1 + x; c[oP:oP + n] += 1 + x; c[oPm:oPm + k] += 1 + x
                else:
                    i = 3 * n - jw; c[oS + i] += (2 - mid[i]) + x
                jw += 1
            elif d == 3:
                i = n - 1 - jw
                if k > i:
                    c[oP + i] += 8.0; c[oS + i] += 2 * (-mid[i]) + 2
                else:
                    c[oS + i] += 2 * (2 - mid[i]) - 2
                iu = self.bound_iu(jw + 1); jw += 1
            else:
                raise RuntimeError("dead end at %s" % ((k, iu, jw),))
            path.append((iu, jw))
        return c, path

def solve(g, iters=400, tol=1e-9, verbose=True, mu0=None, rows=None):
    pc = PC(g); n = pc.n
    if mu0 is None:
        mu0 = np.zeros(pc.nvar); mu0[0] = 1.0
    rows = [] if rows is None else rows
    mu = mu0; v = -np.inf; duals = None
    paths = []
    for it in range(iters):
        vals, Phi = pc.dp(mu)
        ub = vals.max() / 4
        if verbose: print(f"it {it:3d} rows {len(rows):5d} LP {v:.9f} BR {ub:.9f} gap {ub - v:.2e}", flush=True)
        if ub - v < tol: break
        for k in np.argsort(-vals):
            if vals[k] / 4 > v + tol * 0.5:
                c, p = pc.row(k)
                if abs(c @ mu - vals[k]) > 1e-9: print("row mismatch", k, c @ mu, vals[k])
                rows.append(c / 4); paths.append((k, p))
        A = np.array(rows)
        cobj = np.zeros(pc.nvar + 1); cobj[-1] = 1
        A_ub = np.hstack([A, -np.ones((len(rows), 1))])
        A_eq = np.zeros((1, pc.nvar + 1)); A_eq[0, :pc.nvar] = 1
        res = linprog(cobj, A_ub=A_ub, b_ub=np.zeros(len(rows)), A_eq=A_eq, b_eq=[1.0],
                      bounds=[(0, None)] * pc.nvar + [(None, None)], method="highs")
        if res.status != 0: raise RuntimeError(res.message)
        mu = res.x[:pc.nvar]; v = res.x[-1]
        duals = -res.ineqlin.marginals
    return pc, mu, v, ub, rows, paths, duals

if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(description="Continuum one-turn game, piecewise-constant start densities, levels b=1 and b=2-a only.")
    ap.add_argument("n", type=int, help="number of uniform bins on [0,1]")
    ap.add_argument("--verbose", action="store_true")
    a = ap.parse_args()
    g = np.linspace(0, 1, a.n + 1)
    t0 = time.time()
    pc, mu, v, ub, rows, paths, duals = solve(g, verbose=a.verbose)
    print("n", a.n, "value", v, "best response on the mesh", ub, "time", round(time.time() - t0, 1), flush=True)
    e, Pp, Sp, Pm, Sm = pc.unpack(mu)
    print("sweeper pair", e, " P_1(a>0)", Pp.sum(), " S(a>0)", Sp.sum(), " P_1(a<0)", Pm.sum(), " S(a<0)", Sm.sum())
