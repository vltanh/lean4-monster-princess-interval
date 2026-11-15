"""Optimize a binned one-turn and two-turn Monster law for the atomic upper bound on a given grid.

Variables are the bin masses of the compact law format (see atomic_response.read_law) on the mesh 1/n:
the endpoint sweeps, P_1(a), S(a), P_1(-c), S(-c), P_b(+-a) with b in the L level bins on each side of 1,
and T2(+-c, U1).  The grid is 1/N with N = r n.  Each cutting plane is the exact reward of one cell staircase
returned by atomic_upper.cpp, which is linear in the bin masses; the master problem is a floating-point LP.
The result is a law file.  Its bound is whatever atomic_upper.cpp returns for it: the LP only proposes laws.

A law found for one grid is good on that grid only.  It uses the positions of the atoms, and its bound gets
worse on finer grids (see research/14-light-cone-lattice/ATOMIC_TWO_TURN_UPPER.md).

Run from the repository root, for example
    python3 packages/interval_lightcone/optimize_atomic_law.py 32 4 32 --out /tmp/law.txt --budget 3600
"""
import argparse, json, os, subprocess, sys, tempfile, time
import numpy as np
from scipy.optimize import linprog

HERE = os.path.dirname(os.path.abspath(__file__))


class Model:
    def __init__(self, n, L, r, two_turn=True):
        self.n, self.L, self.r = n, L, r
        N = self.N = n * r
        self.vars = [("sweep", ())]
        for kind in ("P1p", "Sp", "P1m", "Sm"):
            for i in range(n):
                self.vars.append((kind, (i,)))
        for i in range(n):
            for j in range(2 * L):
                lo = n - L + j                               # level bin [lo/n, (lo + 1)/n]
                if lo >= i + 1 and lo + 1 <= 2 * n - (i + 1):
                    self.vars.append(("Qp", (i, j)))
                if lo >= i + 1:
                    self.vars.append(("Qm", (i, j)))
        if two_turn:
            for i in range(n):
                for j in range(i + 1, n):
                    self.vars.append(("Tp", (i, j)))
                    self.vars.append(("Tm", (i, j)))
        self.nv = len(self.vars)
        # atoms of every variable, with weights that sum to 1 per variable
        vi, isT, S, Lv, Wt = [], [], [], [], []
        t = np.arange(r + 1)
        e1 = np.where((t == 0) | (t == r), 1.0, 2.0)
        for idx, (kind, ix) in enumerate(self.vars):
            if kind == "sweep":
                vi.append([idx]); isT.append([0]); S.append([N]); Lv.append([N]); Wt.append([1.0])
                continue
            a = ix[0] * r + t
            if kind in ("P1p", "Sp", "P1m", "Sm"):
                s = a if kind in ("P1p", "Sp") else -a
                l = {"P1p": np.full(r + 1, N), "Sp": 2 * N - a, "P1m": np.full(r + 1, N), "Sm": 2 * N + a}[kind]
                w = e1 / e1.sum()
                two = 0
            else:
                A, B = np.meshgrid(a, t, indexing="ij")
                w = np.outer(e1, e1)
                w = (w / w.sum()).ravel()
                s = (A if kind in ("Qp", "Tp") else -A).ravel()
                base = (n - L + ix[1]) * r if kind[0] == "Q" else ix[1] * r
                l = (base + B).ravel()
                two = 1 if kind[0] == "T" else 0
            vi.append(np.full(len(w), idx)); isT.append(np.full(len(w), two)); S.append(s); Lv.append(l); Wt.append(w)
        self.vi = np.concatenate(vi)
        self.isT = np.concatenate(isT).astype(bool)
        self.S = np.concatenate(S).astype(np.int64)
        self.Lv = np.concatenate(Lv).astype(np.int64)
        self.Wt = np.concatenate(Wt)

    def write_law(self, mu, path, D=1 << 24):
        m = np.floor(np.maximum(mu, 0) / max(mu.sum(), 1e-300) * D + 0.5).astype(np.int64)
        m[int(np.argmax(m))] += D - m.sum()                  # the largest bin absorbs the rounding
        assert m.min() >= 0 and m.sum() == D
        with open(path, "w") as f:
            f.write(f"mesh {self.n}\nlevels {self.L}\ndenominator {D}\nsweep {int(m[0])}\n")
            for idx in range(1, self.nv):
                if m[idx] > 0:
                    kind, ix = self.vars[idx]
                    f.write(kind + " " + " ".join(str(x) for x in ix) + f" {int(m[idx])}\n")
        return m / D

    def cut(self, k0, Ku, Mw):
        """Expected capture time of a unit mass of every variable along one staircase (the capture-time table of
        atomic_response.py): Ku[c] is the row in which U = c h is crossed, Mw[y + N] the column in which W = y h is."""
        N, S, Lv = self.N, self.S, self.Lv
        Kl = Ku[np.clip(Lv, 0, len(Ku) - 1)]
        Mrow = Mw[np.clip(-S + N, 0, len(Mw) - 1)]
        esc = np.where(self.isT, 8 * N, 4 * Lv + 12 * N)
        orig = np.where(S >= k0 + 1, 2 * Lv + 2 * (Kl + 1), np.where(Mrow + 1 <= Lv, 2 * (Mrow + 1) + 2 * (-S), esc))
        Kneg = Ku[np.clip(-S, 0, len(Ku) - 1)]
        Ml = Mw[np.clip(Lv + N, 0, len(Mw) - 1)]
        mir_h = np.where(self.isT & (Ml + 1 > N), 16 * N, 2 * (Ml + 1) + 2 * Lv)
        mir = np.where((-S) >= k0 + 1, 2 * (-S) + 2 * (Kneg + 1), mir_h)
        return np.bincount(self.vi, weights=(orig + mir) * self.Wt / (8.0 * N), minlength=self.nv)

    def oracle(self, exe, mu, work, npaths=4):
        law, vals, stairs = (os.path.join(work, x) for x in ("law.txt", "values.txt", "stairs.txt"))
        rounded = self.write_law(mu, law)
        out = json.loads(subprocess.run([exe, law, str(self.N), vals, stairs, str(npaths)],
                                        check=True, text=True, stdout=subprocess.PIPE).stdout)
        value = out["maximum"] / (8.0 * self.N * out["total_weight"])
        N, cuts, cur = self.N, [], None
        for line in open(stairs):
            p = line.split()
            if p[0] == "start":
                cur = [int(p[1]), np.full(5 * N + 3, -10 ** 9, dtype=np.int64), np.full(4 * N + 3, -10 ** 9, dtype=np.int64)]
            elif p[0] == "U":
                cur[1][int(p[1])] = int(p[2])
            elif p[0] == "W":
                cur[2][int(p[1]) + N] = int(p[2])
            else:                                            # complete the staircase to the row 3N: any legal completion
                m, k = int(p[1]), int(p[2])
                while k < 3 * N:
                    if m >= k + 1:
                        cur[2][k + 1 + N] = m; k += 1
                    else:
                        cur[1][m + 1] = k; m += 1
                cuts.append(self.cut(*cur))
        return value, rounded, cuts


def solve(model, exe, out_path, budget, tol=2e-7, alpha=0.5, verbose=True):
    """In-out cutting planes: the oracle is queried between the LP solution and the best law found."""
    rows = []
    mu_lp = np.zeros(model.nv)
    mu_lp[0] = 1.0
    best, lp_value, t0 = (np.inf, None), -np.inf, time.time()
    with tempfile.TemporaryDirectory() as work:
        for it in range(10 ** 6):
            query = mu_lp if best[1] is None else alpha * mu_lp + (1 - alpha) * best[1]
            value, rounded, cuts = model.oracle(exe, query, work)
            assert abs(cuts[0] @ rounded - value) < 1e-9       # the cut reproduces the exact response
            if value < best[0]:
                best = (value, rounded.copy())
                model.write_law(best[1], out_path)
            if verbose and it % 10 == 0:
                print(f"it {it:4d} cuts {len(rows):5d} LP floor {lp_value:.9f} best law {best[0]:.9f} {time.time() - t0:.0f} s", flush=True)
            if best[0] - lp_value < tol or time.time() - t0 > budget:
                break
            rows.extend(cuts)
            A_ub = np.hstack([np.array(rows), -np.ones((len(rows), 1))])
            res = linprog(np.r_[np.zeros(model.nv), 1.0], A_ub=A_ub, b_ub=np.zeros(len(rows)),
                          A_eq=np.r_[np.ones(model.nv), 0.0][None, :], b_eq=[1.0],
                          bounds=[(0, None)] * model.nv + [(None, None)], method="highs")
            assert res.status == 0, res.message
            mu_lp, lp_value = res.x[:model.nv], res.x[-1]
    return best[0], lp_value


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("n", type=int, help="mesh of the bins")
    ap.add_argument("L", type=int, help="level bins on each side of b = 1")
    ap.add_argument("r", type=int, help="grid points per bin; the grid is 1/(r n)")
    ap.add_argument("--one-turn", action="store_true", help="leave out the two-turn family")
    ap.add_argument("--out", required=True, help="law file to write")
    ap.add_argument("--budget", type=float, default=3600.0, help="seconds")
    a = ap.parse_args()
    with tempfile.TemporaryDirectory() as tmp:
        exe = os.path.join(tmp, "atomic_upper")
        subprocess.run(["g++", "-O3", "-fopenmp", "-std=c++17", os.path.join(HERE, "atomic_upper.cpp"), "-o", exe], check=True)
        model = Model(a.n, a.L, a.r, not a.one_turn)
        best, floor = solve(model, exe, a.out, a.budget)
    print(f"grid 1/{model.N}, {model.nv} variables: best law {best:.9f} (floating point; run atomic_upper for the exact bound), "
          f"LP floor for this class of laws {floor:.9f}")


if __name__ == "__main__":
    main()
