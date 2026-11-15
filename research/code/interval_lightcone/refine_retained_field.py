"""Exact factor-2 refinement of the retained n = 512 Princess field, and its native pricing at n = 1024.

The retained field (packages/interval_discovery_certificates/princess_front_n512/field.json) is refined by the
repository's common-threshold rule (solve_normalized.Master.interpolate_seed).  With factor 2 every fine node is
a coarse node or the midpoint of two coarse nodes, so the interpolant is exact over twice the denominator and no
flooring is needed.  The table is then closed under the order relations of Master.repair, extended beyond t = 2
by the outward rule, and priced by price_normalized.cpp.  For any table the engine accepts, with minimum K in
units of 1/(4 n D), the repository's theorems give the game-value lower bound  V >= (K - 2D) / (4 n D).

    python3 packages/interval_lightcone/refine_retained_field.py --selftest     # refinement rule against a literal port
    python3 packages/interval_lightcone/refine_retained_field.py --price        # hours; writes the report next to this file
"""
import argparse, base64, hashlib, json, os, struct, subprocess, sys, tempfile, time, zlib
from fractions import Fraction
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
FIELD = os.path.join(HERE, "..", "interval_discovery_certificates", "princess_front_n512", "field.json")
ENGINE = os.path.join(HERE, "..", "interval_clock_grid", "normalized_native", "price_normalized.cpp")


def load_retained():
    f = json.load(open(FIELD))
    n, D = int(f["n"]), int(f["field_denominator"])
    v = np.frombuffer(zlib.decompress(base64.b64decode(f["pre_two_values_base64"])), dtype="<u4").astype(np.int64)
    C, R = 4 * n, 2 * n
    assert len(v) == (C + 1) * n
    v = v.reshape(C + 1, n)
    pre = np.zeros((C + 1, R + 1), dtype=np.int64)          # pre[j, k], j + k even, 1 <= k <= 2n
    for j in range(C + 1):
        pre[j, np.arange(2 if j % 2 == 0 else 1, R + 1, 2)] = v[j]
    return n, D, pre, f


def refine(n, pre):
    """Integers over 2D on the grid 2n.  pre: integers over D on the grid n (pre-two nodes)."""
    C, R = 4 * n, 2 * n
    Cf, Rf = 8 * n, 4 * n

    def node(J, K):                                          # signed coarse value; beyond t = 2 the outward rule
        ok = (K != 0) & (J < 6 * n) & (J >= 0)
        Ka = np.abs(K)
        Kb = np.where(J > C, Ka - (J - C), Ka)
        val = np.where(Kb > 0, pre[np.clip(J, 0, C), np.clip(Kb, 0, R)], 0)
        return np.where(ok, np.sign(K) * val, 0)

    j, k = np.meshgrid(np.arange(Cf + 1), np.arange(Rf + 1), indexing="ij")
    a, b = (j + k) // 2, (j - k) // 2                        # fine light-cone indices; coarse coordinates a/2, b/2
    cu, au = a // 2, a % 2
    cw, aw = np.floor_divide(b, 2), np.mod(b, 2)
    plus_u, plus_w = np.mod(cu, 2 * n) < n, np.mod(cw, 2 * n) < n
    tot = np.zeros((Cf + 1, Rf + 1), dtype=np.int64)
    for low in (True, False):                                # threshold below / above one half
        U = cu + (au * (plus_u if low else ~plus_u)).astype(np.int64)
        W = cw + (aw * (plus_w if low else ~plus_w)).astype(np.int64)
        tot += node(U + W, U - W)
    fine = np.zeros_like(tot)
    par = ((j + k) % 2 == 0) & (k >= 1)
    fine[par] = tot[par]
    return fine


def reference(n, pre, D):
    """Literal port of interpolate_seed with fractions (slow; for the self-test)."""
    C, R = 4 * n, 2 * n

    def node(J, K):
        if K == 0 or J >= 6 * n:
            return Fraction(0)
        JJ, KK = J, abs(K)
        if JJ > C:
            KK -= JJ - C
            JJ = C
            if KK <= 0:
                return Fraction(0)
        return (1 if K > 0 else -1) * Fraction(int(pre[JJ, KK]), D)

    def coordinate(z):
        cell = z.numerator // z.denominator
        alpha = z - cell
        plus = cell % (2 * n) < n
        return cell, alpha, plus, (alpha if plus else 1 - alpha)

    out = {}
    for j in range(8 * n + 1):
        for k in range(1, 4 * n + 1):
            if (j + k) % 2:
                continue
            u = coordinate(Fraction(n * (j + k), 4 * n))
            w = coordinate(Fraction(n * (j - k), 4 * n))
            cuts = sorted(set([Fraction(0), Fraction(1), u[3], w[3]]))
            v = Fraction(0)
            for left, right in zip(cuts, cuts[1:]):
                z = (left + right) / 2

                def rnd(c):
                    cell, al, plus, _ = c
                    return cell + int(al > 0 and (z < al if plus else z > 1 - al))
                U, W = rnd(u), rnd(w)
                v += (right - left) * node(U + W, U - W)
            out[j, k] = v
    return out


def repair(n, vals, D):
    """Order closure of Master.repair on integers in [0, D] (grid n)."""
    C, R = 4 * n, 2 * n
    v = np.clip(vals, 0, D).astype(np.int64)
    for k in range(2, R + 1):
        js = np.arange(k % 2, C + 1, 2)
        left = np.where(js - 1 >= 0, v[np.clip(js - 1, 0, C), k - 1], 0)
        right = np.where(js + 1 <= C, v[np.clip(js + 1, 0, C), k - 1], 0)
        v[js, k] = np.maximum(v[js, k], np.maximum(left, right))
    for j in range(C - 2, -1, -2):
        v[j, R] = max(v[j, R], v[j + 2, R])
    return v


def full_table(n, pre):
    """Engine table for 0 <= j <= 12n: the pre-two field, then the outward rule."""
    C, R, H = 4 * n, 2 * n, 12 * n
    table = np.zeros((H + 1, R + 1), dtype=np.uint64)
    table[:C + 1] = pre
    for j in range(C + 1, H + 1):
        sh = j - C
        if sh >= R:
            break
        table[j, sh + 1:] = pre[C, 1:R + 1 - sh]
    jj, kk = np.meshgrid(np.arange(H + 1), np.arange(R + 1), indexing="ij")
    table[(jj + kk) % 2 == 1] = 0
    table[:, 0] = 0
    return table


def selftest():
    rng = np.random.default_rng(3)
    for n in (4, 6):
        D = 10 ** 6
        C, R = 4 * n, 2 * n
        pre = np.zeros((C + 1, R + 1), dtype=np.int64)
        for j in range(C + 1):
            for k in range(1, R + 1):
                if (j + k) % 2 == 0:
                    pre[j, k] = rng.integers(0, D + 1)
        pre = repair(n, pre, D)                              # a legal field
        fine, ref = refine(n, pre), reference(n, pre, D)
        assert all(Fraction(int(fine[j, k]), 2 * D) == v for (j, k), v in ref.items())
        print(f"n = {n} -> {2 * n}: {len(ref)} nodes agree with the literal port")
    print("PASS")


def price():
    n, D, pre, meta = load_retained()
    fine = refine(n, pre)
    n2, D2 = 2 * n, 2 * D
    closed = repair(n2, fine, D2)
    changed = int((closed != fine).sum())
    table = full_table(n2, closed)
    digest = hashlib.sha256(table.astype("<u8").tobytes()).hexdigest()
    print(f"refined n = {n} -> {n2}, denominator {D2}; order closure changed {changed} nodes; table sha256 {digest}", flush=True)
    with tempfile.TemporaryDirectory() as tmp:
        exe, path = os.path.join(tmp, "price_normalized"), os.path.join(tmp, "input.bin")
        subprocess.run(["g++", "-O3", "-std=c++17", ENGINE, "-o", exe], check=True)
        with open(path, "wb") as f:
            f.write(struct.pack("<IIQ", 1, n2, D2) + table.astype("<u8").tobytes())
        t0 = time.time()
        ans = json.loads(subprocess.run([exe, path, "0"], check=True, text=True, stdout=subprocess.PIPE).stdout)
        seconds = time.time() - t0
    K = int(ans["minimum_units"])
    scale = 4 * n2 * D2
    report = {
        "scope": "exact full-width factor-2 refinement of the retained n512 field, priced by price_normalized.cpp; "
                 "game-value lower bound by the existing 1/(2n) transfer",
        "source_field_sha256": hashlib.sha256(open(FIELD, "rb").read()).hexdigest(),
        "engine_sha256": hashlib.sha256(open(ENGINE, "rb").read()).hexdigest(),
        "n": n2, "field_denominator": str(D2), "table_sha256": digest, "order_closure_changed_nodes": changed,
        "minimum_units": str(K), "objective_denominator": str(scale),
        "normalized_bank_dual_value": str(Fraction(K, scale)),
        "global_lower": str(Fraction(K - 2 * D2, scale)), "global_lower_decimal": float(Fraction(K - 2 * D2, scale)),
        "previous_global_lower": meta["global_lower"],
        "improves_previous": bool(Fraction(K - 2 * D2, scale) > Fraction(meta["global_lower"])),
        "engine_report": {k: v for k, v in ans.items() if k != "paths"}, "seconds": round(seconds, 1),
    }
    out = os.path.join(HERE, "refined_n1024_lower_replay.json")
    json.dump(report, open(out, "w"), indent=1)
    print(json.dumps({k: v for k, v in report.items() if k != "engine_report"}, indent=1))


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--price", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        selftest()
    if a.price:
        price()
    if not (a.selftest or a.price):
        ap.print_help()
