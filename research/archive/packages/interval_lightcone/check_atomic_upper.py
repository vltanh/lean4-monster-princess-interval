"""Checks for the atomic upper bound (atomic_upper.cpp, atomic_response.py).

1. Physical capture times.  For every legal atom on small grids and random Princess staircases, the first
   meeting time is computed from the two piecewise-linear trajectories in (t, x) with exact fractions and
   compared with the capture-time table: equal in the cases the table states as exact, and not larger than
   the stated bound in the others.
2. Exhaustive dynamic program.  On the grids N = 1, 2 every cell staircase is enumerated and its reward is
   summed atom by atom from the table.  The maximum must equal the output of both dynamic programs.
3. The two implementations must return identical integers for every start cell on the committed law.

Run from the repository root:  python3 packages/interval_lightcone/check_atomic_upper.py [--grids 16 32 64 128]
"""
import argparse, os, random, subprocess, sys, tempfile
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from atomic_response import read_law, atoms, response

LAW = os.path.join(HERE, "atomic_law_16bins.txt")


# ---------------------------------------------------------------- physical trajectories ----------------
def monster_P(N, a, b, sign):
    A, B = F(a, N), F(b, N)
    v = [(F(0), A), ((B - A) / 2, (A + B) / 2), (B + 1, F(-1)), (B + 3, F(1))]
    return [(t, sign * x) for t, x in v]


def monster_T(N, c, u, sign):
    C, U1 = F(c, N), F(u, N)
    v = [(F(0), C), ((U1 - C) / 2, (U1 + C) / 2), ((1 + U1) / 2, (U1 - 1) / 2), (F(2), F(1)), (F(4), F(-1))]
    return [(t, sign * x) for t, x in v]


def princess(N, k0, moves):
    """Unit-speed path through the cell centres: a right move raises x, an up move lowers it."""
    d = F(1, 2 * N)
    t, x = F(0), (2 * k0 + 1) * d
    v = [(t, x)]
    for mv in moves:
        t += d
        x += d if mv == 0 else -d
        v.append((t, x))
    while t < 7:                                   # any legal continuation
        step = -d if x >= d else d
        for s in (step, -step):
            t += d
            x += s
            v.append((t, x))
    return v


def position(v, t):
    for (t0, x0), (t1, x1) in zip(v, v[1:]):
        if t0 <= t <= t1:
            return x0 if t1 == t0 else x0 + (x1 - x0) * (t - t0) / (t1 - t0)
    return v[-1][1]


def first_meeting(mv, pv):
    times = sorted(set(t for t, _ in mv) | set(t for t, _ in pv))
    for t0, t1 in zip(times, times[1:]):
        f0 = position(mv, t0) - position(pv, t0)
        f1 = position(mv, t1) - position(pv, t1)
        if f0 == 0:
            return t0
        if f0 * f1 < 0:
            return t0 + (t1 - t0) * f0 / (f0 - f1)
    raise AssertionError("no meeting")


# ---------------------------------------------------------------- staircases and the table --------------
def crossing_data(N, k0, moves):
    m, k = k0, -k0 - 1
    K, M = {}, {}
    for mv in moves:
        if mv == 0:
            K[m + 1] = k
            m += 1
        else:
            M[k + 1] = m
            k += 1
    return K, M


def random_staircase(N, k0, rng):
    m, k = k0, -k0 - 1
    moves = []
    while k < 3 * N:
        can_r = (m + 1 - k) <= 2 * N and m + 1 <= 5 * N
        can_u = (m - (k + 1)) >= 0
        mv = rng.randrange(2) if (can_r and can_u) else (0 if can_r else 1)
        m, k = (m + 1, k) if mv == 0 else (m, k + 1)
        moves.append(mv)
    return moves


def all_staircases(N, k0):
    out = []

    def rec(m, k, moves):
        if k == 3 * N:
            out.append(list(moves))
            return
        if m + 1 - k <= 2 * N and m + 1 <= 5 * N:
            moves.append(0); rec(m + 1, k, moves); moves.pop()
        if m - (k + 1) >= 0:
            moves.append(1); rec(m, k + 1, moves); moves.pop()

    rec(k0, -k0 - 1, [])
    return out


def table(N, k0, K, M, kind, s, l):
    """(reward of the path, exact?, reward of the mirror, exact?) in units of 2T/delta, far-corner convention."""
    if kind == "P":
        a, b = s, l
        if a >= k0 + 1:
            o = (2 * b + 2 * (K[b] + 1), True)
        elif M[-a] + 1 <= b:
            o = (2 * (M[-a] + 1) + 2 * (-a), True)
        else:
            o = (4 * b + 12 * N, False)
        if -a >= k0 + 1:
            mi = (2 * (-a) + 2 * (K[-a] + 1), True)
        else:
            mi = (2 * (M[b] + 1) + 2 * b, True)
    else:
        c, u = s, l
        if c >= k0 + 1:
            o = (2 * u + 2 * (K[u] + 1), True)
        elif M[-c] + 1 <= u:
            o = (2 * (M[-c] + 1) + 2 * (-c), True)
        else:
            o = (8 * N, False)
        if -c >= k0 + 1:
            mi = (2 * (-c) + 2 * (K[-c] + 1), True)
        elif M[u] + 1 <= N:
            mi = (2 * (M[u] + 1) + 2 * u, True)
        else:
            mi = (16 * N, False)
    return o[0], o[1], mi[0], mi[1]


def legal_atoms(N):
    P = [(a, b) for a in range(-N, N + 1) for b in range(abs(a), 2 * N - a + 1)]
    T = [(c, u) for c in range(-N, N + 1) for u in range(abs(c), N + 1)]
    return P, T


def check_physical(rng):
    exact = bound = 0
    for N, reps in ((1, 16), (2, 60), (3, 40), (4, 25)):
        P, T = legal_atoms(N)
        for k0 in range(N):
            pool = all_staircases(N, k0) if N <= 2 else None
            for _ in range(reps):
                moves = rng.choice(pool) if pool else random_staircase(N, k0, rng)
                K, M = crossing_data(N, k0, moves)
                pv = princess(N, k0, moves)
                for kind, lst, make in (("P", P, monster_P), ("T", T, monster_T)):
                    for s, l in lst:
                        ro, eo, rm, em = table(N, k0, K, M, kind, s, l)
                        for sign, r, ex in ((1, ro, eo), (-1, rm, em)):
                            t = 4 * N * first_meeting(make(N, s, l, sign), pv)      # 2T/delta
                            if ex:
                                assert t == r - 1, (N, k0, kind, s, l, sign, t, r)  # cell centre: half a step early
                                exact += 1
                            else:
                                assert t <= r, (N, k0, kind, s, l, sign, t, r)
                                bound += 1
    print(f"1. physical capture times: {exact} exact table entries and {bound} bound entries agree")


def reward(N, k0, K, M, P, T):
    tot = 0
    for kind, d in (("P", P), ("T", T)):
        for (s, l), w in d.items():
            ro, _, rm, _ = table(N, k0, K, M, kind, s, l)
            tot += w * (ro + rm)
    return tot


def run_cpp(exe, law_path, N, tmp):
    out = os.path.join(tmp, "values.txt")
    subprocess.run([exe, law_path, str(N), out], check=True, stdout=subprocess.DEVNULL)
    return [int(x) for x in open(out).read().split()]


def check_exhaustive(exe, tmp, rng):
    cases = 0
    for N, trials in ((1, 200), (2, 60)):
        data = {k0: [crossing_data(N, k0, mv) for mv in all_staircases(N, k0)] for k0 in range(N)}
        for _ in range(trials):
            P, T = {}, {}
            for _ in range(rng.randint(1, 9)):
                a = rng.randint(-N, N); b = rng.randint(abs(a), 2 * N - a)
                P[(a, b)] = P.get((a, b), 0) + rng.randint(1, 1000)
            for _ in range(rng.randint(0, 6)):
                c = rng.randint(-N, N); u = rng.randint(abs(c), N)
                T[(c, u)] = T.get((c, u), 0) + rng.randint(1, 1000)
            best = [max(reward(N, k0, K, M, P, T) for K, M in data[k0]) for k0 in range(N)]
            assert [int(x) for x in response(N, P, T)] == best
            raw = os.path.join(tmp, "raw.txt")
            with open(raw, "w") as f:
                f.write("atoms\n")
                for (a, b), w in P.items():
                    f.write(f"P {a} {b} {w}\n")
                for (c, u), w in T.items():
                    f.write(f"T {c} {u} {w}\n")
            assert run_cpp(exe, raw, N, tmp) == best
            cases += 1
    print(f"2. exhaustive enumeration: both dynamic programs equal the maximum over all staircases on {cases} random laws")


def check_implementations(exe, tmp, grids):
    law = read_law(LAW)
    for N in grids:
        P, T, W = atoms(law, N)
        py = [int(x) for x in response(N, P, T)]
        assert run_cpp(exe, LAW, N, tmp) == py
        print(f"3. N = {N}: C++ and Python agree on all {N} start cells; maximum {max(py)}, "
              f"bound {max(py)}/{8 * N * W} = {max(py) / (8 * N * W):.12f}")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--grids", type=int, nargs="*", default=[16, 32, 64, 128])
    a = ap.parse_args()
    rng = random.Random(20261115)
    with tempfile.TemporaryDirectory() as tmp:
        exe = os.path.join(tmp, "atomic_upper")
        subprocess.run(["g++", "-O3", "-fopenmp", "-std=c++17", os.path.join(HERE, "atomic_upper.cpp"), "-o", exe], check=True)
        check_physical(rng)
        check_exhaustive(exe, tmp, rng)
        check_implementations(exe, tmp, a.grids)
    print("PASS")


if __name__ == "__main__":
    main()
