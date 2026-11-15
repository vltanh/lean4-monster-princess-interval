"""Lattice game with the Monster limited to at most kmax interior turns before its first endpoint
(then a forced sweep).  Same lattice/field conventions as fullgame.py."""
import numpy as np, sys, time, pickle
from scipy.optimize import linprog
from scipy.sparse import coo_matrix, vstack
from lattice_game import Lattice, path_cost_and_cut

INF = 1e18

def monster_dp_k(lat, F, kmax):
    N = lat.N; N2 = lat.D; S = lat.S; delta = lat.delta
    ex = ~np.isnan(F)
    levels = np.unique(F[ex]); K = len(levels)
    lev = np.zeros(F.shape, dtype=np.int64); lev[ex] = np.searchsorted(levels, F[ex])
    W = 2 * N2 + 1
    # sweep costs after first endpoint: Lsw (pushing up with B=1), Rsw (pushing right with A=0)
    Lsw = np.full((S + 2, W), INF); Rsw = np.full((S + 2, W), INF)
    for s in range(S, -1, -1):
        for dd in range(W):
            if not ex[s, dd]: continue
            if dd == 0: Lsw[s, dd] = 0.0
            elif s + 1 <= S: Lsw[s, dd] = Lsw[s + 1, dd - 1] + (s + 0.5) * delta * (F[s, dd] - F[s + 1, dd - 1])
            if dd == W - 1: Rsw[s, dd] = 0.0
            elif s + 1 <= S: Rsw[s, dd] = Rsw[s + 1, dd + 1] + (s + 0.5) * delta * (F[s + 1, dd + 1] - F[s, dd])
    Tab = [[[None] * W for _ in range(S + 1)] for _ in range(kmax + 1)]
    for s in range(S, -1, -1):
        for dd in range(W):
            if not ex[s, dd]: continue
            fP = F[s, dd]; lP = lev[s, dd]; tmid = (s + 0.5) * delta
            # column above and row to the right
            nU = min(S - s, dd); nR = min(S - s, W - 1 - dd)
            nsU = np.arange(1, nU + 1); nsR = np.arange(1, nR + 1)
            colF = F[s + nsU, dd - nsU] if nU else None
            rowF = F[s + nsR, dd + nsR] if nR else None
            a = np.arange(0, lP + 1); b = np.arange(lP, K)
            if nU:
                cntg = np.searchsorted(-colF, -levels[a], side='left'); okU = cntg < nU
                idxU = np.minimum(cntg, nU - 1); nnU = nsU[idxU]
                capU = (s + nnU - 0.5) * delta * (levels[a] - colF[idxU])
            if nR:
                cntl = np.searchsorted(rowF, levels[b], side='left'); okR = cntl < nR
                idxR = np.minimum(cntl, nR - 1); nnR = nsR[idxR]
                capR = (s + nnR - 0.5) * delta * (rowF[idxR] - levels[b])
            for k in range(kmax + 1):
                vec = np.full(K, INF)
                # ---- R states (B = F(P), A = level a) ----
                if dd == W - 1:
                    # right endpoint reached: forced sweep left
                    best = np.full(lP + 1, INF)
                    if nU:
                        val = Lsw[s + nnU, dd - nnU] + capU
                        best = np.where(okU, val, INF)
                else:
                    best = np.full(lP + 1, INF)
                    if s + 1 <= S:
                        best = Tab[k][s + 1][dd + 1][: lP + 1] + tmid * (F[s + 1, dd + 1] - fP)
                    if k >= 1 and nU and dd != 0:
                        tv = np.array([Tab[k - 1][s + n][dd - n][lP] for n in nsU])
                        val = np.where(okU, tv[idxU] + capU, INF)
                        best = np.minimum(best, val)
                # ---- L states (A = F(P), B = level b) ----
                if dd == 0:
                    bestL = np.full(K - lP, INF)
                    if nR:
                        val = Rsw[s + nnR, dd + nnR] + capR
                        bestL = np.where(okR, val, INF)
                else:
                    bestL = np.full(K - lP, INF)
                    if s + 1 <= S:
                        bestL = Tab[k][s + 1][dd - 1][lP:] + tmid * (fP - F[s + 1, dd - 1])
                    if k >= 1 and nR and dd != W - 1:
                        tv = np.array([Tab[k - 1][s + n][dd + n][lP] for n in nsR])
                        val = np.where(okR, tv[idxR] + capR, INF)
                        bestL = np.minimum(bestL, val)
                both = min(best[lP], bestL[0])
                vec[: lP + 1] = best; vec[lP:] = bestL; vec[lP] = both
                Tab[k][s][dd] = vec
    vals = {i: Tab[kmax][0][2 * i + N2][lev[0, 2 * i + N2]] for i in range(-N, N + 1)}
    return vals, Tab, levels, lev, Lsw, Rsw


def extract_path_k(lat, F, Tab, levels, lev, Lsw, Rsw, i0, kmax):
    N2 = lat.D; S = lat.S; delta = lat.delta; W = 2 * N2 + 1
    s, dd = 0, 2 * i0 + N2
    A = B = F[s, dd]; path = [(s, dd)]; k = kmax
    eps = 1e-12
    # phase 1: until first endpoint
    while dd != 0 and dd != W - 1:
        fP = F[s, dd]; lP = lev[s, dd]; tmid = (s + 0.5) * delta
        la = int(np.searchsorted(levels, A)); lb = int(np.searchsorted(levels, B))
        cands = []
        if abs(fP - B) < eps:
            cands.append((Tab[k][s + 1][dd + 1][la] + tmid * (F[s + 1, dd + 1] - fP), ('R', 1, k)))
            if k >= 1:
                n = 1
                while dd - n > 0 and F[s + n, dd - n] > A + eps: n += 1
                if F[s + n, dd - n] <= A + eps:
                    c = Tab[k - 1][s + n][dd - n][lP] + (s + n - 0.5) * delta * (A - F[s + n, dd - n])
                    cands.append((c, ('U', n, k - 1)))
        if abs(fP - A) < eps:
            cands.append((Tab[k][s + 1][dd - 1][lb] + tmid * (fP - F[s + 1, dd - 1]), ('U', 1, k)))
            if k >= 1:
                n = 1
                while dd + n < W - 1 and F[s + n, dd + n] < B - eps: n += 1
                if F[s + n, dd + n] >= B - eps:
                    c = Tab[k - 1][s + n][dd + n][lP] + (s + n - 0.5) * delta * (F[s + n, dd + n] - B)
                    cands.append((c, ('R', n, k - 1)))
        c, (d, n, k) = min(cands, key=lambda z: z[0])
        for _ in range(n):
            s += 1; dd += 1 if d == 'R' else -1; path.append((s, dd))
            A = min(A, F[s, dd]); B = max(B, F[s, dd])
    # phase 2: sweep to the other endpoint
    step = -1 if dd == W - 1 else 1
    while (dd != 0 if step == -1 else dd != W - 1):
        s += 1; dd += step; path.append((s, dd))
    return path


def solve_k(N, kmax, iters=400, tol=1e-7, verbose=True, tmax=5.0):
    lat = Lattice(N, tmax)
    Amono, bmono = lat._mono; nv = lat.nvar
    cut_rows = []; cut_rhs = []; cut_paths = []
    x = np.zeros(nv)
    for s in range(4 * N + 1):
        for d in range(1, 2 * N):
            if lat.var[s, d] >= 0: x[lat.var[s, d]] = d / (2 * N)
    c_lp = np.inf
    for it in range(iters):
        x = lat.clean(x)
        G = lat.field(x); F = lat.signed(G)
        vals, Tab, levels, lev, Lsw, Rsw = monster_dp_k(lat, F, kmax)
        best = min(vals.values())
        if verbose: print(f"k={kmax} it {it:3d} cuts {len(cut_rows):5d} LP {c_lp:.8f} BR {best:.8f} gap {c_lp - best:.2e}", flush=True)
        if c_lp - best < tol: break
        for i in sorted(vals, key=lambda i: vals[i]):
            if vals[i] < c_lp - tol * 0.5:
                p = extract_path_k(lat, F, Tab, levels, lev, Lsw, Rsw, i, kmax)
                cost, coef, const = path_cost_and_cut(lat, F, p)
                if abs(cost - vals[i]) > 1e-9: print("WARNING cost mismatch", i, cost, vals[i])
                cut_rows.append(coef); cut_rhs.append(const); cut_paths.append((i, p))
        del Tab
        nr = len(cut_rows); rr = []; cc = []; vv = []
        for ri, coef in enumerate(cut_rows):
            for kx, vx in coef.items(): rr.append(ri); cc.append(kx); vv.append(-vx)
            rr.append(ri); cc.append(nv); vv.append(1.0)
        Acut = coo_matrix((vv, (rr, cc)), shape=(nr, nv + 1)).tocsr()
        Am = Amono.tocoo()
        A_ub = vstack([Acut, coo_matrix((Am.data, (Am.row, Am.col)), shape=(Am.shape[0], nv + 1)).tocsr()]).tocsr()
        b_ub = np.concatenate([np.array(cut_rhs), bmono])
        cobj = np.zeros(nv + 1); cobj[-1] = -1.0
        res = linprog(cobj, A_ub=A_ub, b_ub=b_ub, bounds=[(0, 1)] * nv + [(None, None)], method="highs")
        if res.status != 0: raise RuntimeError(res.message)
        x = res.x[:nv]; c_lp = res.x[-1]; duals = -res.ineqlin.marginals[:nr]
    return dict(N=N, kmax=kmax, x=x, value_lp=c_lp, value_br=best, cuts=(cut_rows, cut_rhs, cut_paths), duals=duals)

if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(description="Lattice game with at most kmax interior Monster turns before the first endpoint.")
    ap.add_argument("N", type=int); ap.add_argument("kmax", type=int)
    ap.add_argument("--out"); ap.add_argument("--verbose", action="store_true")
    a = ap.parse_args()
    t0 = time.time()
    out = solve_k(a.N, a.kmax, verbose=a.verbose)
    print("N", a.N, "kmax", a.kmax, "lattice value", out['value_lp'], "best response", out['value_br'],
          "time", round(time.time() - t0, 1), flush=True)
    if a.out:
        pickle.dump(out, open(a.out, 'wb'))
