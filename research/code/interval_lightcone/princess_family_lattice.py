"""Half-offset lattice game with the Princess restricted to a three-parameter family of radial paths.

    G(k0, r, s1, s2):  start in cell k0 (radius (2 k0 + 1) / (2N)); run outward for r steps; run inward until
                       step s1; if the centre is reached, wait there until step s2; run outward to the endpoint
                       and stay.

The Monster is unrestricted (exact frontier dynamic program of lattice_game).  The Princess plays the ordered
law of a mixture of family paths: its nodal field is linear in the mixture weights, so the master problem is the
linear program of lattice_game with the field replaced by B q.

With r = 0 only, the family loses about 2.8e-3 against the unrestricted optimum L_N.  With short outward runs
allowed it is within 4e-5 on N = 8, 16, 24.  Floating-point LP values, not certificates.

Run from the repository root:  python3 research/code/interval_lightcone/princess_family_lattice.py N [max outward run]
"""
import argparse, json, os, sys, time
import numpy as np
from scipy.optimize import linprog

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from lattice_game import Lattice, monster_dp, extract_path, path_cost_and_cut


def family(N, smax, max_out):
    out = []
    for k0 in range(N):
        d0 = 2 * k0 + 1
        for r in range(0, max_out + 1):
            top = d0 + r                               # radius index after the outward run
            if top > 2 * N:
                continue
            for s1 in range(r, r + top + 1):
                if r > 0 and s1 == r:
                    continue                           # no inward step: the same path as r = 0, s1 = 0 from a larger start
                if s1 < r + top:
                    out.append((k0, r, s1, s1))
                else:                                  # centre reached: leave at any later step of the same parity
                    for s2 in range(s1, min(smax, int(2.6 * N)) + 1, 2):
                        out.append((k0, r, s1, s2))
    return out


def trajectory(N, atom, smax):
    """Radius index (odd-lattice position) at every lattice time 0..smax."""
    k0, r, s1, s2 = atom
    d = 2 * k0 + 1
    pos = [d]
    for s in range(1, smax + 1):
        if s <= r:
            d += 1
        elif s <= s1:
            d -= 1
        elif s <= s2:
            d = 1 - d                                  # at the centre: 0, 1, 0, 1, ...
        elif d < 2 * N:
            d += 1
        else:
            d = 2 * N - 1                              # at the endpoint: 2N, 2N - 1, 2N, ...
        assert 0 <= d <= 2 * N
        pos.append(d)
    return np.array(pos)


def solve(N, max_out, iters=1000, tol=1e-7, verbose=True):
    lat = Lattice(N, 5.0)
    smax = lat.var.shape[0] - 1
    A = family(N, smax, max_out)
    traj = np.array([trajectory(N, a, smax) for a in A])
    B = np.zeros((lat.nvar, len(A)))                   # B[node, path] = 1 if the path is strictly inside the node
    for s in range(lat.var.shape[0]):
        for d in range(lat.var.shape[1]):
            k = lat.var[s, d]
            if k >= 0:
                B[k] = traj[:, s] < d
    na = len(A)
    q = np.full(na, 1.0 / na)
    rows, rhs, c_lp, t0 = [], [], np.inf, time.time()
    for it in range(iters):
        F = lat.signed(lat.field(lat.clean(B @ q)))
        vals, Tab, levels, lev = monster_dp(lat, F)
        best = min(vals.values())
        if verbose and it % 10 == 0:
            print(f"it {it:3d} cuts {len(rows):5d} LP {c_lp:.9f} response {best:.9f} gap {c_lp - best:.2e} {time.time() - t0:.0f} s", flush=True)
        if c_lp - best < tol:
            break
        for i in sorted(vals, key=lambda i: vals[i]):
            if vals[i] < c_lp - tol * 0.5:
                p = extract_path(lat, F, Tab, levels, lev, i)
                cost, coef, const = path_cost_and_cut(lat, F, p)
                row = np.zeros(na)
                for kx, vx in coef.items():
                    row += vx * B[kx]
                rows.append(row)
                rhs.append(const)
        del Tab
        A_ub = np.hstack([-np.array(rows), np.ones((len(rows), 1))])
        res = linprog(np.r_[np.zeros(na), -1.0], A_ub=A_ub, b_ub=np.array(rhs),
                      A_eq=np.r_[np.ones(na), 0.0][None, :], b_eq=[1.0],
                      bounds=[(0, None)] * na + [(None, None)], method="highs")
        assert res.status == 0, res.message
        q, c_lp = res.x[:na], res.x[-1]
    return c_lp, best, A, q


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("N", type=int)
    ap.add_argument("max_out", type=int, nargs="?", default=3, help="longest initial outward run, in lattice steps")
    ap.add_argument("--quiet", action="store_true")
    a = ap.parse_args()
    value, response, A, q = solve(a.N, a.max_out, verbose=not a.quiet)
    full = json.load(open(os.path.join(HERE, "results.json")))["half_offset_lattice_value_L_n"]["unrestricted"].get(str(a.N))
    print(f"N = {a.N}, outward runs up to {a.max_out} steps, {len(A)} family paths")
    print(f"  family value {value:.12f}   (Monster response {response:.12f})")
    if full is not None:
        print(f"  unrestricted L_N {full:.12f}   loss {full - value:.3e}")
    by_run, by_type = {}, {}
    for (k0, r, s1, s2), w in zip(A, q):
        if w > 1e-9:
            by_run[r] = by_run.get(r, 0.0) + w
            kind = "stay" if s1 == 0 and r == 0 else ("centre" if s1 == r + 2 * k0 + 1 + r else "turn back")
            by_type[kind] = by_type.get(kind, 0.0) + w
    print("  mass by outward run:", {k: round(v, 4) for k, v in sorted(by_run.items())})
    print("  mass by type:", {k: round(v, 4) for k, v in sorted(by_type.items())})


if __name__ == "__main__":
    main()
