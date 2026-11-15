"""Data for the strategy page research/strategies.html.

Everything is computed from committed files:
  * the Monster law  atomic_law_32bins_grid2048.txt  (the law behind V <= 1.4240199);
  * the retained Princess field  princess_front_n512/field.json  (the field behind both lower bounds);
  * atomic_upper.cpp, for the Princess's best payoff from every start and her best-response paths.

    python3 research/code/interval_lightcone/strategy_page_data.py --out /tmp/strategies_data.json

The page builder (build_strategy_page.py) embeds the JSON in the page.  Nothing here is a certificate:
the cost map and the page's duel use the half-offset lattice cost on the time grid 1/1024 against the nodal
field, which differs from a continuous cost by O(1/n); the map is shown as an excess over its own minimum.
"""
import argparse, base64, json, os, subprocess, sys, tempfile, time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from atomic_response import read_law
from refine_retained_field import load_retained, full_table

LAW = os.path.join(HERE, "atomic_law_32bins_grid2048.txt")
TRACE_R0 = (0.05, 0.2, 0.4, 0.6, 0.8, 0.9, 0.975, 0.996)
DT = 1.0 / 256          # sampling of curves on the page
TMAX = 2.5


def monster_law():
    law = read_law(LAW)
    D = law["denominator"]
    recs = [[k] + list(idx) + [round(m / D, 9)] for k, idx, m in law["recs"]]
    return dict(mesh=law["mesh"], levels=law["levels"], sweep=round(law["sweep"] / D, 9), records=recs)


def princess_against_law(exe, N=2048):
    """Best payoff from every start cell, and best-response paths for a few starts."""
    with tempfile.TemporaryDirectory() as tmp:
        vals, stairs = os.path.join(tmp, "v.txt"), os.path.join(tmp, "s.txt")
        cells = [min(N - 1, int(r * N)) for r in TRACE_R0]
        out = json.loads(subprocess.run([exe, LAW, str(N), vals, stairs, "@" + ",".join(map(str, cells))],
                                        check=True, text=True, stdout=subprocess.PIPE).stdout)
        W = out["total_weight"]
        pay = np.loadtxt(vals) / (8.0 * N * W)
        paths, cur = [], None
        for line in open(stairs):
            p = line.split()
            if p[0] == "start":
                m, k = int(p[1]), -int(p[1]) - 1
                cur = [(m, k)]
            elif p[0] == "U":
                m += 1; cur.append((m, k))
            elif p[0] == "W":
                k += 1; cur.append((m, k))
            else:
                # the staircase itself: cell centres at the times j/(2N), j = 0, 1, ..., stored as d_j = m - k,
                # so that the centre is at x = d_j/(2N); a path close to the bound hugs the far corners instead
                J = int(round(TMAX * 2 * N))
                ds = [m_ - k_ for (m_, k_) in cur][:J + 1]
                paths.append(dict(r0=round((ds[0]) / (2.0 * N), 4), payoff=round(float(pay[cur[0][0]]), 8), N=N, d=ds))
    return dict(N=N, bound=out["maximum"] / (8.0 * N * W), payoff=[round(float(v), 8) for v in pay]), paths


def princess_field():
    n, D, pre, meta = load_retained()
    G = full_table(n, pre).astype(np.float64) / D            # G[j, k]: time j/(2n), radius k/(2n), j + k even
    C, R = 4 * n, 2 * n
    # the full nodal field, as in field.json: time index j <= 4n, radius index k = 1..2n with j + k even,
    # stored as round(65535 G); the page applies the outward rule after t = 2 itself
    vals = np.array([G[j, (2 if j % 2 == 0 else 1)::2][:n] for j in range(C + 1)])
    assert vals.shape == (C + 1, n)
    q16 = np.round(np.clip(vals, 0, 1) * 65535).astype("<u2")
    field = dict(n=n, b64=base64.b64encode(np.ascontiguousarray(q16).tobytes()).decode())
    # rank curves from the full field: radial rank q -> radius where G crosses q (linear between nodes)
    qs = (np.arange(48) + 0.5) / 48
    ts = np.arange(0, TMAX + 1e-9, DT)
    rad = np.zeros((len(qs), len(ts)))
    for i, t in enumerate(ts):
        j = int(round(t * 2 * n))
        ks = np.arange(j % 2, R + 1, 2)
        g = G[j, ks].copy()
        g[ks == 0] = 0.0
        if ks[-1] == R:
            g[-1] = 1.0
        g = np.maximum.accumulate(g)
        rad[:, i] = np.interp(qs, g, ks / (2.0 * n))
    ranks = dict(q=[round(float(v), 5) for v in qs], dt=DT,
                 r=[[int(round(v * 10000)) for v in row] for row in rad])
    return field, ranks, (n, G)


def lattice_costs(n, G, step_cells=16):
    """Half-offset lattice cost of one-turn and two-turn Monster paths against the nodal field (grid 1/(2n))."""
    R = 2 * n
    dl = 1.0 / (2 * n)

    def F(s, d):
        g = G[np.minimum(s, G.shape[0] - 1), np.abs(d)]
        f = np.where(d >= 0, 0.5 * (1 + g), 0.5 * (1 - g))
        return np.where(d >= R, 1.0, np.where(d <= -R, 0.0, f))   # a Monster at an endpoint meets the Princesses resting there

    def cost(starts, moves):
        L = max(len(m) for m in moves)
        M = np.zeros((len(moves), L), dtype=np.int64)
        for i, m in enumerate(moves):
            M[i, :len(m)] = m
        d = np.concatenate([np.array(starts)[:, None], np.array(starts)[:, None] + np.cumsum(M, axis=1)], axis=1)
        s = np.broadcast_to(np.arange(L + 1), d.shape)
        f = F(s, d)
        width = np.maximum.accumulate(f, axis=1) - np.minimum.accumulate(f, axis=1)
        assert np.all(width[:, -1] > 1 - 1e-12)
        return (np.diff(width, axis=1) * ((np.arange(1, L + 1) - 0.5) * dl)[None, :]).sum(axis=1)

    one = []
    for a2 in range(-R, R + 1, step_cells):
        bs = [b for b in range(abs(a2), 2 * R - a2 + 1, step_cells)]
        if not bs:
            continue
        mv = []
        for b2 in bs:
            n1 = (b2 - a2) // 2
            mv.append([1] * n1 + [-1] * (a2 + n1 + R) + [1] * (2 * R))
        for b2, v in zip(bs, cost([a2] * len(bs), mv)):
            one.append((a2 // step_cells, b2 // step_cells, float(v)))
    two = []
    for c2 in range(-R // 2, R // 2 + 1, step_cells):
        us = [u for u in range(abs(c2), R + 1, step_cells) if u > abs(c2) or c2 == 0]
        mv = []
        for u2 in us:
            n1 = (u2 - c2) // 2
            x1 = c2 + n1
            n2 = (R - (n1 - x1)) // 2
            mv.append([1] * n1 + [-1] * n2 + [1] * (R - (x1 - n2)) + [-1] * (2 * R))
        for u2, v in zip(us, cost([c2] * len(us), mv)):
            two.append((c2 // step_cells, u2 // step_cells, float(v)))
    lo = min(min(v for *_, v in one), min(v for *_, v in two))
    unit = step_cells / (2.0 * n)
    pack = lambda rows: dict(i=[r[0] for r in rows], j=[r[1] for r in rows],
                             excess=[float("%.3g" % (r[2] - lo)) for r in rows])
    return dict(unit=unit, minimum=round(lo, 7), one_turn=pack(one), two_turn=pack(two))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    t0 = time.time()
    with tempfile.TemporaryDirectory() as tmp:
        exe = os.path.join(tmp, "atomic_upper")
        subprocess.run(["g++", "-O3", "-fopenmp", "-std=c++17", os.path.join(HERE, "atomic_upper.cpp"), "-o", exe], check=True)
        payoff, _ = princess_against_law(exe)                 # the proof's grid: payoff from every start
        _, responses = princess_against_law(exe, N=512)       # best paths against the version the page plays
        # the version of the law that the page averages against: atoms on the grid 1/512, with its own exact bound
        out = json.loads(subprocess.run([exe, LAW, "512"], check=True, text=True, stdout=subprocess.PIPE).stdout)
        page_law = dict(N=512, maximum=out["maximum"], total_weight=out["total_weight"],
                        bound=out["maximum"] / (8.0 * 512 * out["total_weight"]))
    field, ranks, (n, G) = princess_field()
    costs = lattice_costs(n, G)
    data = dict(
        bounds=dict(lower_old="36409808231/25600000000", lower_old_dec=1.4222581340234375,
                    lower="9322984150699/6553600000000", lower_dec=1.4225744858854674,
                    upper_old="142472349375511/100000000000003", upper_old_dec=1.424723493755067,
                    upper="1603303881142469/1125899906842624", upper_dec=1.4240199074521955,
                    upper_w1="25661865897887875/18014398509481984", upper_w1_dec=1.4245197187339118,
                    estimate=1.42397),
        law=monster_law(), page_law=page_law, princess_payoff=payoff, best_responses=responses,
        field=field, ranks=ranks, costs=costs, tmax=TMAX)
    with open(a.out, "w") as f:
        json.dump(data, f, separators=(",", ":"))
    print(f"wrote {a.out}: {os.path.getsize(a.out) / 1e6:.2f} MB in {time.time() - t0:.0f} s; "
          f"bound check {payoff['bound']:.10f}, lattice cost minimum {costs['minimum']}")


if __name__ == "__main__":
    main()
