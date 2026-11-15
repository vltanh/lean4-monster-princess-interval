"""
Full lattice Princess-Monster game on [-1,1] in light-cone coordinates.

delta = 1/(2N).  Monster nodes: (U,W) = (2i,2j)*delta, s=i+j (time s*delta), d=i-j
(position d*delta), |d| <= 2N.  Moves: R (s+1,d+1), U (s+1,d-1).
Princess: radial nodal field G(s,d) on d in [0,2N] (mass of radial Princess curves strictly
inside the node), G(s,0)=0, G(s,2N)=1, front rule beyond U=2 (i>=2N).
Monster cost of a path = sum over edges of t_mid * newly captured mass, where the captured set
is the interval [running min, running max] of the signed field F=(1+-G)/2.

LP: maximize c s.t. c <= L_cal(G) for generated Monster (path, calendar) cuts.
Oracle: exact frontier DP over (node, side, other-record level).
"""
import numpy as np, sys, time, pickle
from scipy.optimize import linprog
from scipy.sparse import coo_matrix, csr_matrix, vstack


class Lattice:
    def __init__(self, N, tmax=5.0):
        self.N = N
        self.delta = 1.0 / (2 * N)
        self.D = 2 * N
        self.S = int(round(tmax * 2 * N))
        N2 = 2 * N
        # free variables: d in [1,2N-1], s>=0, s+d<=4N, parity
        self.var = -np.ones((4 * N + 1, N2 + 1), dtype=np.int64)
        cnt = 0
        for d in range(1, N2):
            for s in range(0, 4 * N - d + 1):
                if (s + d) % 2 == 0:
                    self.var[s, d] = cnt; cnt += 1
        self.nvar = cnt
        # map every positive-side node (s,d), s<=S, to (var index or -1, const)
        self.gidx = -np.ones((self.S + 1, N2 + 1), dtype=np.int64)
        self.gconst = np.zeros((self.S + 1, N2 + 1))
        self.exists = np.zeros((self.S + 1, N2 + 1), dtype=bool)
        for s in range(self.S + 1):
            for d in range(0, N2 + 1):
                if (s + d) % 2: continue
                self.exists[s, d] = True
                if d == 0:
                    continue
                if d == N2:
                    self.gconst[s, d] = 1.0; continue
                if s + d <= 4 * N:
                    self.gidx[s, d] = self.var[s, d]
                else:
                    i = (s + d) // 2; j = (s - d) // 2
                    if j >= N2:
                        continue                      # G = 0
                    s2, d2 = N2 + j, N2 - j           # front node (i=2N, same j)
                    self.gidx[s, d] = self.var[s2, d2]
        self._mono = self._monotone_rows()

    def _monotone_rows(self):
        """rows A x <= b encoding G(s,d) <= G(s+1,d+1) and G(s+1,d-1) <= G(s,d) over the free region
        (including boundary constants)."""
        rows = []; cols = []; vals = []; rhs = []
        r = 0
        N2 = self.D
        def term(s, d):
            return self.gidx[s, d], self.gconst[s, d]
        for s in range(0, 4 * self.N + 1):
            for d in range(0, N2 + 1):
                if (s + d) % 2 or s + d > 4 * self.N: continue
                # right neighbour (s+1,d+1): G(s,d) - G(s+1,d+1) <= 0
                if d + 1 <= N2 and s + 1 + d + 1 <= 4 * self.N + 2 and s + 1 <= self.S:
                    a, ca = term(s, d); b, cb = term(s + 1, d + 1)
                    if not (a < 0 and b < 0):
                        if a >= 0: rows.append(r); cols.append(a); vals.append(1.0)
                        if b >= 0: rows.append(r); cols.append(b); vals.append(-1.0)
                        rhs.append(cb - ca); r += 1
                # up neighbour (s+1,d-1): G(s+1,d-1) - G(s,d) <= 0
                if d - 1 >= 0 and s + 1 <= self.S:
                    a, ca = term(s + 1, d - 1); b, cb = term(s, d)
                    if not (a < 0 and b < 0):
                        if a >= 0: rows.append(r); cols.append(a); vals.append(1.0)
                        if b >= 0: rows.append(r); cols.append(b); vals.append(-1.0)
                        rhs.append(cb - ca); r += 1
        A = coo_matrix((vals, (rows, cols)), shape=(r, self.nvar)).tocsr()
        # drop duplicate / trivial rows
        return A, np.array(rhs)

    def field(self, x):
        """radial G on all positive nodes (S+1, 2N+1) from variable vector x."""
        G = self.gconst.copy()
        m = self.gidx >= 0
        G[m] = x[self.gidx[m]]
        return G

    def clean(self, x, decimals=10):
        """Round and repair tiny monotonicity violations left by the LP solver."""
        x = np.clip(np.round(x, decimals), 0.0, 1.0)
        N2 = self.D
        for _ in range(50):
            G = self.field(x)
            changed = False
            for s in range(0, 4 * self.N):
                for d in range(0, N2 + 1):
                    if (s + d) % 2 or s + d > 4 * self.N: continue
                    g = G[s, d]
                    if d + 1 <= N2 and self.var[s + 1, d + 1] >= 0 if (s + 1 <= 4 * self.N and d + 1 <= N2) else False:
                        if s + 1 + d + 1 <= 4 * self.N and G[s + 1, d + 1] < g:
                            x[self.var[s + 1, d + 1]] = g; G[s + 1, d + 1] = g; changed = True
                    if d - 1 >= 1 and s + 1 + d - 1 <= 4 * self.N and self.var[s + 1, d - 1] >= 0:
                        if G[s + 1, d - 1] > g:
                            x[self.var[s + 1, d - 1]] = g; G[s + 1, d - 1] = g; changed = True
            if not changed: break
        return x

    def check_monotone(self, x):
        A, b = self._mono
        return float((A @ x - b).max())

    def signed(self, G):
        """F on (S+1, 4N+1) indexed [s, d+2N]."""
        N2 = self.D
        F = np.full((self.S + 1, 2 * N2 + 1), np.nan)
        F[:, N2:] = 0.5 * (1 + G)
        F[:, :N2] = 0.5 * (1 - G[:, :0:-1])
        ex = np.zeros_like(F, dtype=bool)
        ex[:, N2:] = self.exists
        ex[:, :N2] = self.exists[:, :0:-1]
        F[~ex] = np.nan
        return F


def monster_dp(lat, F, starts=None, tol=0.0):
    """Exact Monster best responses.  Returns (values per start index i in [-N..N], paths)."""
    N = lat.N; N2 = lat.D; S = lat.S; delta = lat.delta
    off = N2
    ex = ~np.isnan(F)
    levels = np.unique(F[ex])
    K = len(levels)
    lev = np.zeros(F.shape, dtype=np.int64)
    lev[ex] = np.searchsorted(levels, F[ex])
    # Tab[s][dd] = vector over levels: for level<=lev(P): R(P,a); for level>=lev(P): L(P,b)
    INF = 1e18
    Tab = [[None] * (2 * N2 + 1) for _ in range(S + 1)]
    for s in range(S, -1, -1):
        for dd in range(2 * N2 + 1):
            if not ex[s, dd]: continue
            fP = F[s, dd]; lP = lev[s, dd]
            vec = np.full(K, INF)
            tmid = (s + 0.5) * delta
            # ---------------- R states: a <= lP ----------------
            a = np.arange(0, lP + 1)
            best = np.full(lP + 1, INF)
            if fP >= 1.0 - 1e-15:
                pass
            # push right
            if dd + 1 <= 2 * N2 and s + 1 <= S:
                tgt = Tab[s + 1][dd + 1]
                best = np.minimum(best, tgt[: lP + 1] + tmid * (F[s + 1, dd + 1] - fP))
            # switch: travel up the column: nodes (s+n, dd-n)
            nmax = min(S - s, dd)
            if nmax >= 1:
                ns = np.arange(1, nmax + 1)
                colF = F[s + ns, dd - ns]
                # first n with colF <= v_a  -> count of entries with colF > v_a
                cntg = np.searchsorted(-colF, -levels[a], side='left')
                okm = cntg < nmax
                idx = np.minimum(cntg, nmax - 1)
                nn = ns[idx]
                # gather L(Q, b=lP)
                tv = np.array([Tab[s + n][dd - n][lP] for n in ns])
                val = tv[idx] + (s + nn - 0.5) * delta * (levels[a] - colF[idx])
                val = np.where(okm, val, INF)
                best = np.minimum(best, val)
            # terminal: everything captured
            if fP >= 1.0 - 1e-15:
                best[0] = min(best[0], 0.0) if levels[0] <= 1e-15 else best[0]
            vec[: lP + 1] = best
            # ---------------- L states: b >= lP ----------------
            b = np.arange(lP, K)
            bestL = np.full(K - lP, INF)
            if dd - 1 >= 0 and s + 1 <= S:
                tgt = Tab[s + 1][dd - 1]
                bestL = np.minimum(bestL, tgt[lP:] + tmid * (fP - F[s + 1, dd - 1]))
            nmax = min(S - s, 2 * N2 - dd)
            if nmax >= 1:
                ns = np.arange(1, nmax + 1)
                rowF = F[s + ns, dd + ns]
                cntl = np.searchsorted(rowF, levels[b], side='left')   # entries with rowF < v_b
                okm = cntl < nmax
                idx = np.minimum(cntl, nmax - 1)
                nn = ns[idx]
                tv = np.array([Tab[s + n][dd + n][lP] for n in ns])
                val = tv[idx] + (s + nn - 0.5) * delta * (rowF[idx] - levels[b])
                val = np.where(okm, val, INF)
                bestL = np.minimum(bestL, val)
            if fP <= 1e-15:
                bestL[-1] = min(bestL[-1], 0.0) if levels[-1] >= 1 - 1e-15 else bestL[-1]
            # level lP is shared between R(P,lP) and L(P,lP): both mean A=B=F(P)
            both = min(best[lP], bestL[0])
            vec[lP:] = bestL
            vec[lP] = both
            Tab[s][dd] = vec
    # start values
    vals = {}
    for i in range(-N, N + 1):
        dd = 2 * i + off
        vals[i] = Tab[0][dd][lev[0, dd]]
    return vals, Tab, levels, lev


def extract_path(lat, F, Tab, levels, lev, i0):
    """Follow optimal decisions from start index i0. Returns list of nodes (s,dd)."""
    N2 = lat.D; S = lat.S; delta = lat.delta
    s, dd = 0, 2 * i0 + N2
    A = F[s, dd]; B = F[s, dd]
    path = [(s, dd)]
    side = None   # 'R' or 'L'
    eps = 1e-12
    guard = 0
    while not (A <= 1e-15 and B >= 1 - 1e-15):
        guard += 1
        if guard > 100000: raise RuntimeError("path extraction loop")
        fP = F[s, dd]; lP = lev[s, dd]
        tmid = (s + 0.5) * delta
        cands = []
        la = int(np.searchsorted(levels, A)); lb = int(np.searchsorted(levels, B))
        atR = abs(fP - B) < eps
        atL = abs(fP - A) < eps
        if atR:
            if dd + 1 <= 2 * N2 and s + 1 <= S:
                c = Tab[s + 1][dd + 1][la] + tmid * (F[s + 1, dd + 1] - fP)
                cands.append((c, 'pushR'))
            n = 1
            while s + n <= S and dd - n >= 0 and F[s + n, dd - n] > A + eps: n += 1
            if s + n <= S and dd - n >= 0:
                c = Tab[s + n][dd - n][lP] + (s + n - 0.5) * delta * (A - F[s + n, dd - n])
                cands.append((c, ('travU', n)))
        if atL:
            if dd - 1 >= 0 and s + 1 <= S:
                c = Tab[s + 1][dd - 1][lb] + tmid * (fP - F[s + 1, dd - 1])
                cands.append((c, 'pushU'))
            n = 1
            while s + n <= S and dd + n <= 2 * N2 and F[s + n, dd + n] < B - eps: n += 1
            if s + n <= S and dd + n <= 2 * N2:
                c = Tab[s + n][dd + n][lP] + (s + n - 0.5) * delta * (F[s + n, dd + n] - B)
                cands.append((c, ('travR', n)))
        if not cands:
            raise RuntimeError("no candidates at %s A=%g B=%g f=%g" % ((s, dd), A, B, fP))
        c, mv = min(cands, key=lambda z: z[0])
        if mv == 'pushR':
            s, dd = s + 1, dd + 1; path.append((s, dd))
        elif mv == 'pushU':
            s, dd = s + 1, dd - 1; path.append((s, dd))
        elif mv[0] == 'travU':
            for _ in range(mv[1]):
                s, dd = s + 1, dd - 1; path.append((s, dd))
        else:
            for _ in range(mv[1]):
                s, dd = s + 1, dd + 1; path.append((s, dd))
        B = max(B, F[s, dd]); A = min(A, F[s, dd])
    # Extend to both physical endpoints so that the calendar cut is valid for EVERY field:
    # the cut's survival sum must end at a time when all mass is caught whatever the field is.
    W = 2 * N2
    seen_right = any(d == W for (_, d) in path); seen_left = any(d == 0 for (_, d) in path)
    while not (seen_right and seen_left):
        if not seen_right and not seen_left:
            step = 1 if dd >= N2 else -1
        else:
            step = 1 if not seen_right else -1
        while 0 < dd < W or (dd == 0 and step == 1) or (dd == W and step == -1):
            s, dd = s + 1, dd + step; path.append((s, dd))
            if dd == 0 or dd == W: break
        seen_right = seen_right or dd == W; seen_left = seen_left or dd == 0
    return path


def path_cost_and_cut(lat, F, path):
    """True cost of a node path under F, and the calendar cut as (coef vector over G vars, const):
       cost(G') <= const + coef . x'  for every feasible field."""
    N2 = lat.D; delta = lat.delta
    coef = {}
    const = 0.0
    def addF(s, dd, w):
        nonlocal const
        d = dd - N2
        if d >= 0:
            # F = (1 + G)/2
            const += 0.5 * w
            gi = lat.gidx[s, d]
            if gi >= 0: coef[gi] = coef.get(gi, 0.0) + 0.5 * w
            else: const += 0.5 * w * lat.gconst[s, d]
        else:
            const += 0.5 * w
            gi = lat.gidx[s, -d]
            if gi >= 0: coef[gi] = coef.get(gi, 0.0) - 0.5 * w
            else: const -= 0.5 * w * lat.gconst[s, -d]
    s0, dd0 = path[0]
    A = B = F[s0, dd0]; PA = PB = path[0]
    cost = 0.0
    # survival form: cost = t_1 + sum_{k>=1} delta*(1 - B_k + A_k), k = step index, until complete
    const += 0.5 * delta      # t_1 = delta/2
    for k in range(1, len(path)):
        s, dd = path[k]
        f = F[s, dd]
        tm = (k - 0.5) * delta
        if f > B:
            cost += tm * (f - B); B = f; PB = (s, dd)
        if f < A:
            cost += tm * (A - f); A = f; PA = (s, dd)
        if k < len(path) - 1:
            const += delta
            addF(PB[0], PB[1], -delta)
            addF(PA[0], PA[1], +delta)
    return cost, coef, const


def solve(N, iters=300, tol=1e-7, verbose=True, tmax=5.0, state=None):
    lat = Lattice(N, tmax)
    Amono, bmono = lat._mono
    nv = lat.nvar
    cut_rows = []; cut_rhs = []; cut_paths = []
    if state is not None:
        cut_rows, cut_rhs, cut_paths = state
    # initial field: uniform static
    x = np.zeros(nv)
    for s in range(4 * N + 1):
        for d in range(1, 2 * N):
            if lat.var[s, d] >= 0:
                x[lat.var[s, d]] = d / (2 * N)
    hist = []
    c_lp = np.inf
    for it in range(iters):
        x = lat.clean(x)
        viol = lat.check_monotone(x)
        if viol > 0: print("monotone violation after clean", viol)
        G = lat.field(x)
        F = lat.signed(G)
        t0 = time.time()
        vals, Tab, levels, lev = monster_dp(lat, F)
        tdp = time.time() - t0
        best = min(vals.values())
        hist.append((c_lp, best))
        if verbose:
            print(f"it {it:3d} cuts {len(cut_rows):5d} LP {c_lp:.8f} BR {best:.8f} gap {c_lp - best:.2e} K {len(levels)} dp {tdp:.1f}s", flush=True)
        if c_lp - best < tol:
            break
        # add cuts from all starts whose value is below the LP value
        added = 0
        for i in sorted(vals, key=lambda i: vals[i]):
            if vals[i] < c_lp - tol * 0.5:
                p = extract_path(lat, F, Tab, levels, lev, i)
                cost, coef, const = path_cost_and_cut(lat, F, p)
                if abs(cost - vals[i]) > 1e-9:
                    print("WARNING cost mismatch", i, cost, vals[i])
                cut_rows.append(coef); cut_rhs.append(const); cut_paths.append((i, p))
                added += 1
        del Tab
        # LP: max c  s.t.  c - row.x <= const ; mono
        nr = len(cut_rows)
        rr = []; cc = []; vv = []
        for ri, coef in enumerate(cut_rows):
            for kx, vx in coef.items():
                rr.append(ri); cc.append(kx); vv.append(-vx)
            rr.append(ri); cc.append(nv); vv.append(1.0)
        Acut = coo_matrix((vv, (rr, cc)), shape=(nr, nv + 1)).tocsr()
        Am = Amono.tocoo()
        A_ub = vstack([Acut, coo_matrix((Am.data, (Am.row, Am.col)), shape=(Am.shape[0], nv + 1)).tocsr()]).tocsr()
        b_ub = np.concatenate([np.array(cut_rhs), bmono])
        cobj = np.zeros(nv + 1); cobj[-1] = -1.0
        res = linprog(cobj, A_ub=A_ub, b_ub=b_ub, bounds=[(0, 1)] * nv + [(None, None)], method="highs")
        if res.status != 0:
            raise RuntimeError(res.message)
        x = res.x[:nv]; c_lp = res.x[-1]
        duals = -res.ineqlin.marginals[:nr]
    return dict(N=N, lat=lat, x=x, value_lp=c_lp, value_br=best, cuts=(cut_rows, cut_rhs, cut_paths), duals=duals, hist=hist)


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(description="Unrestricted half-offset lattice game (field LP + exact Monster DP).")
    ap.add_argument("N", type=int)
    ap.add_argument("--iters", type=int, default=5000)
    ap.add_argument("--out", help="pickle the field, cuts and Monster mixture here")
    ap.add_argument("--quiet", action="store_true")
    a = ap.parse_args()
    t0 = time.time()
    out = solve(a.N, iters=a.iters, verbose=not a.quiet)
    print("N", a.N, "lattice value", out['value_lp'], "best response", out['value_br'],
          "sup-model value (+1/(4N))", out['value_lp'] + 1 / (4 * a.N), "time", round(time.time() - t0, 1))
    out.pop('lat')
    if a.out:
        pickle.dump(out, open(a.out, 'wb'))
