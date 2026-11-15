"""Price an optimum of the half-offset lattice game with the repository's exact integer engine
(research/code/interval_clock_grid/normalized_native/price_normalized.cpp), on its own grid and, after the
common-threshold (full-width) interpolation of solve_normalized.Master.interpolate_seed, on finer grids.

The engine is compiled into a temporary directory; nothing is written into the repository.
"""
import argparse, json, os, struct, subprocess, sys, tempfile, time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from lattice_game import Lattice, solve

SOURCE = os.path.join(HERE, "..", "interval_clock_grid", "normalized_native", "price_normalized.cpp")


def build_table(n, value, D):
    """value(j, k) is the radial field at time index j <= 4n and radius index 1 <= k <= 2n, (j + k) even.
    Floor to integers over D, take the order closure of Master.repair, extend past t = 2 by the outward rule."""
    R, C, H = 2 * n, 4 * n, 12 * n
    val = {}
    for j in range(C + 1):
        for k in range(1, R + 1):
            if (j + k) % 2 == 0:
                val[j, k] = min(D, max(0, int(np.floor(float(value(j, k)) * D))))
    for k in range(2, R + 1):
        for j in range(k % 2, C + 1, 2):
            for s in (-1, 1):
                if 0 <= j + s <= C:
                    val[j, k] = max(val[j, k], val[j + s, k - 1])
    for j in range(C - 2, -1, -2):
        val[j, R] = max(val[j, R], val[j + 2, R])
    table = np.zeros((H + 1, R + 1), dtype=np.uint64)
    for j in range(H + 1):
        for k in range(1, R + 1):
            if (j + k) % 2 == 0:
                jj, kk = j, k
                if jj > C:
                    kk -= jj - C; jj = C
                    if kk <= 0:
                        continue
                table[j, k] = val[jj, kk]
    return table


def interpolate(G, coarse, n):
    """Port of solve_normalized.Master.interpolate_seed for a coarse field G[j, k]."""
    def node(j, k):
        if k == 0 or j >= 6 * coarse:
            return 0.0
        return (1.0 if k > 0 else -1.0) * G[j, abs(k)]

    def coordinate(z):
        cell = int(np.floor(z)); alpha = z - cell
        if alpha < 1e-12:
            alpha = 0.0
        elif alpha > 1 - 1e-12:
            cell += 1; alpha = 0.0
        plus = cell % (2 * coarse) < coarse
        return cell, alpha, plus, (alpha if plus else 1 - alpha)

    def value(j, k):
        u = coordinate(coarse * (j + k) / (2 * n)); w = coordinate(coarse * (j - k) / (2 * n))
        cuts = sorted(set([0.0, 1.0, u[3], w[3]])); v = 0.0
        for left, right in zip(cuts, cuts[1:]):
            if right - left < 1e-14:
                continue
            z = (left + right) / 2

            def rnd(c):
                cell, a, plus, _ = c
                return cell + int(a > 0 and (z < a if plus else z > 1 - a))
            U, W = rnd(u), rnd(w)
            v += (right - left) * node(U + W, U - W)
        return v
    return value


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("N", type=int, help="grid of the lattice optimum")
    ap.add_argument("fine", type=int, nargs="*", help="finer grids on which to price its interpolant")
    ap.add_argument("--denominator", type=int, default=10**9)
    a = ap.parse_args()
    D = a.denominator
    with tempfile.TemporaryDirectory() as tmp:
        exe = os.path.join(tmp, "price_normalized")
        subprocess.run(["g++", "-O3", "-std=c++17", SOURCE, "-o", exe], check=True)

        def price(n, table):
            path = os.path.join(tmp, "input.bin")
            with open(path, "wb") as f:
                f.write(struct.pack("<IIQ", 1, n, D) + table.astype("<u8").tobytes())
            ans = json.loads(subprocess.run([exe, path, "0"], check=True, text=True, stdout=subprocess.PIPE).stdout)
            return int(ans["minimum_units"])

        out = solve(a.N, iters=5000, verbose=False)
        lat = Lattice(a.N, tmax=6.0)
        G = lat.field(lat.clean(out["x"]))
        print(f"N = {a.N}: lattice value L_N = {out['value_lp']:.12f}, L_N + 1/(4N) = {out['value_lp'] + 1 / (4 * a.N):.12f}")
        for n in [a.N] + list(a.fine):
            t0 = time.time()
            value = (lambda j, k: G[j, k]) if n == a.N else interpolate(G, a.N, n)
            K = price(n, build_table(n, value, D))
            print(f"  priced on n = {n}: bank minimum {K}/{4 * n * D} = {K / (4 * n * D):.12f}"
                  f"   bank - 1/(2n) = {K / (4 * n * D) - 1 / (2 * n):.12f}   ({time.time() - t0:.0f} s)", flush=True)


if __name__ == "__main__":
    main()
