"""Exact Monster best response against a finite ordered Princess law in continuous time (prototype).

The law is a finite set of signed paths x_0 <= x_1 <= ... <= x_{M-1} (ordered at all times), piecewise linear with
speed at most 1, with masses.  Three facts make the Monster's problem finite:

  1. the captured set is always an interval [i, j] of the paths, and the Monster is on path i or on path j when the
     interval grows;
  2. being on a path earlier dominates being on it later, because the Monster can follow the path, so between
     captures he runs at full speed towards the next path on the left or on the right, and he starts on a path;
  3. paths that are at the meeting point at the meeting time are captured together.

The program is a shortest-path computation over states (i, j, side) with Pareto sets of labels (time, cost), in exact
fractions.  It is a prototype: O(M^2) states, pure Python.  `python3 capture_order_pricing.py` runs the test: on
random ordered families of unit-speed lattice paths the value equals an exhaustive search over lattice Monster paths
(state: time, position, captured set).

capture_order_pricing.cpp is the same program in integers (unit-speed or waiting pieces on integer breakpoints,
coordinates doubled so that every meeting time is an integer).  `--compare` checks it against this file.

First numbers (exact prices of explicit finite laws, so each is a lower bound on V):
  * quantile paths of the N = 8 lattice optimum on M shifted copies of the lattice, 20 or 40 levels each:
    1.1020 (20 x 2), 1.1070 (40 x 2), 1.2517 (40 x 4), against L_8 = 1.4012.  A lattice optimum puts large masses
    on single paths, a Monster that starts on such a bundle takes it at time 0, and the loss decays like 1/M.
  * K equal-mass family paths (out, in, wait at the centre, out, stay) sampled from the N = 24 family solution of
    princess_family_lattice.py and spread inside the lattice cells; the law priced is the ordered law of the sorted
    positions: 1.381741 (K = 300), 1.398481 (K = 1000, 22 s).
  * for a smooth one-parameter family of such paths the price converges like 0.25/K (1.169578, 1.170528, 1.170672
    at K = 200, 800, 2000 for one test law), with fewer than one label per state.
  * the retained n = 512 field, drawn as `levels` quantile paths on each of M shifted copies of the lattice
    (the common-threshold construction), sorted at the sample times and priced by
    capture_order_pricing_samples.cpp (paths given by integer samples, binary search for the meetings):
        levels x M      paths    exact value
        100 x 2          200     228661/163840     = 1.3956360
        250 x 2          500     2869947/2048000   = 1.4013413
        1000 x 2        2000     11506283/8192000  = 1.4045756
        500 x 4         2000     11570411/8192000  = 1.4124037
        1000 x 4        4000     46324427/32768000 = 1.4137093   (151 s, 9.2e7 labels)
    The error is about 0.04/M in the number of copies: a sweep that starts slightly inside the endpoint takes a
    whole copy of the group that runs just ahead of the sweep line.  The limit, near 1.423, is consistent with the
    lattice certificate, but M of a few hundred is out of reach for an O(paths^2) program.
The engine is not the obstacle; a finite law good enough to beat the lattice certificate is.
"""
import random
from fractions import Fraction as F

class Path:
    def __init__(self, pts):                       # pts: [(t, x)], t increasing from 0; constant after the last point
        self.t = [F(t) for t, _ in pts]; self.x = [F(x) for _, x in pts]
    def at(self, t):
        ts, xs = self.t, self.x
        if t >= ts[-1]: return xs[-1]
        lo, hi = 0, len(ts) - 1
        while hi - lo > 1:
            mid = (lo + hi) // 2
            if ts[mid] <= t: lo = mid
            else: hi = mid
        return xs[lo] + (xs[hi] - xs[lo]) * (t - ts[lo]) / (ts[hi] - ts[lo])
    def meet(self, tau, y, direction):
        """first t >= tau with direction * (x(t) - (y + direction * (t - tau))) <= 0: a full-speed runner from (tau, y)"""
        ts, xs = self.t, self.x
        g0 = direction * (self.at(tau) - y)
        if g0 <= 0: return tau
        # g(t) = direction * (x(t) - y) - (t - tau) is nonincreasing; find its first zero segment by segment
        k = 0
        while k + 1 < len(ts) and ts[k + 1] <= tau: k += 1
        t0, g = tau, g0
        while True:
            if k + 1 < len(ts):
                t1 = ts[k + 1]; slope = direction * (xs[k + 1] - xs[k]) / (ts[k + 1] - ts[k]) - 1
            else:
                t1 = None; slope = F(-1)
            if slope < 0:
                tz = t0 + g / (-slope)
                if t1 is None or tz <= t1: return tz
            if t1 is None: raise RuntimeError('no meeting')
            g = g + slope * (t1 - t0); t0 = t1; k += 1

def best_response(paths, mass):
    M = len(paths)
    def tied(i, j, t, y):
        """extend [i, j] by all paths at position y at time t"""
        while i > 0 and paths[i - 1].at(t) == y: i -= 1
        while j < M - 1 and paths[j + 1].at(t) == y: j += 1
        return i, j
    labels = {}                                     # (i, j, side) -> list of (tau, cost)
    def push(key, tau, cost):
        L = labels.setdefault(key, [])
        for (a, b) in L:
            if a <= tau and b <= cost: return False
        L[:] = [(a, b) for (a, b) in L if not (tau <= a and cost <= b)]
        L.append((tau, cost)); return True
    for k in range(M):
        y = paths[k].at(F(0)); i, j = tied(k, k, F(0), y)
        push((i, j, 0), F(0), F(0)); push((i, j, 1), F(0), F(0))
    best = None; nlab = 0
    for width in range(1, M + 1):                   # process intervals by size
        for i in range(0, M - width + 1):
            j = i + width - 1
            for side in (0, 1):
                for (tau, cost) in labels.get((i, j, side), []):
                    nlab += 1
                    if width == M:
                        best = cost if best is None else min(best, cost); continue
                    y = paths[i].at(tau) if side == 0 else paths[j].at(tau)
                    if j < M - 1:
                        t2 = paths[j + 1].meet(tau, y, +1); y2 = paths[j + 1].at(t2)
                        i2, j2 = tied(i, j + 1, t2, y2)
                        c2 = cost + t2 * sum(mass[k] for k in list(range(i2, i)) + list(range(j + 1, j2 + 1)))
                        push((i2, j2, 1), t2, c2)
                        if paths[i2].at(t2) == y2: push((i2, j2, 0), t2, c2)
                    if i > 0:
                        t2 = paths[i - 1].meet(tau, y, -1); y2 = paths[i - 1].at(t2)
                        i2, j2 = tied(i - 1, j, t2, y2)
                        c2 = cost + t2 * sum(mass[k] for k in list(range(i2, i)) + list(range(j + 1, j2 + 1)))
                        push((i2, j2, 0), t2, c2)
                        if paths[j2].at(t2) == y2: push((i2, j2, 1), t2, c2)
    return best, nlab


# ---------------------------------------------------------------- test ----------------
def random_family(N, K, T, rng):
    """K radial unit-speed lattice paths on even positions at even times, sorted at every time step"""
    W = 2 * N
    pos = [[rng.randrange(0, N + 1) * 2 for _ in range(K)]]
    for t in range(1, T + 1):
        cur = []
        for p in pos[-1]:
            q = p + rng.choice((-1, 1))
            if q < 0: q = 1
            if q > W: q = W - 1
            cur.append(q)
        pos.append(cur)
    pos = [sorted(r) for r in pos]
    # after T everybody keeps bouncing between two adjacent points: continue the last motion as a zigzag
    return pos

def brute(N, pos, mass, T):
    """exact minimum over Monster lattice paths (even starts), by forward search over (position, captured set)"""
    K = len(pos[0]); W = 2 * N; M = 2 * K
    def signed(t):
        r = pos[min(t, len(pos) - 1)] if t < len(pos) else None
        return r
    full = (1 << M) - 1
    def caught(t, x):
        m = 0
        row = pos[t]
        for k in range(K):
            if row[k] == x: m |= 1 << (K + k)
            if -row[k] == x: m |= 1 << (K - 1 - k)
        return m
    msk_mass = lambda m: sum(mass[i] for i in range(M) if m >> i & 1)
    cur = {}
    for x in range(-W, W + 1, 2):
        cur[(x, caught(0, x))] = F(0)
    best = None
    for t in range(0, T):
        nxt = {}
        for (x, m), c in cur.items():
            if m == full:
                best = c if best is None else min(best, c); continue
            for dx in (-1, 1):
                x2 = x + dx
                if abs(x2) > W: continue
                new = caught(t + 1, x2) & ~m
                c2 = c + (t + 1) * msk_mass(new)
                key = (x2, m | new)
                if key not in nxt or c2 < nxt[key]: nxt[key] = c2
        cur = nxt
    for (x, m), c in cur.items():
        if m == full: best = c if best is None else min(best, c)
    return best

def selftest():
    rng = random.Random(5)
    ok = 0
    for trial in range(40):
        N = rng.choice((2, 3)); K = rng.choice((2, 3, 4)); T = 10 * N
        pos = random_family(N, K, T, rng)
        # make the family end at the endpoint: after time 4N everybody runs outward and stays (legal, keeps the order)
        W = 2 * N
        for t in range(1, len(pos)):
            pass
        mass_r = [F(rng.randint(1, 5)) for _ in range(K)]
        mass = mass_r[::-1] + mass_r                    # signed order: -p_K .. -p_1, p_1 .. p_K
        # beyond T the lattice paths are frozen at their last position in both programs
        paths = [Path([(t, -pos[t][k]) for t in range(T + 1)]) for k in reversed(range(K))] + \
                [Path([(t, pos[t][k]) for t in range(T + 1)]) for k in range(K)]
        b = brute(N, pos + [pos[-1]] * (6 * N + 2), mass, T + 6 * N)
        d, nlab = best_response(paths, mass)
        assert b == d, (trial, N, K, b, d)
        ok += 1
    print('capture-order program equals the exhaustive lattice search on', ok, 'random ordered families')


def compare_cpp(trials=60):
    """C++ program against best_response on random ordered families with waiting pieces and unequal masses"""
    import json, os, subprocess, tempfile
    here = os.path.dirname(os.path.abspath(__file__))
    rng = random.Random(11)
    with tempfile.TemporaryDirectory() as tmp:
        exe = os.path.join(tmp, 'capture'); law = os.path.join(tmp, 'law.txt')
        subprocess.run(['g++', '-O3', '-std=c++17', os.path.join(here, 'capture_order_pricing.cpp'), '-o', exe], check=True)
        for trial in range(trials):
            N = rng.choice((2, 3, 4)); K = rng.choice((2, 3, 5, 8)); T = 8 * N; W = 2 * N
            pos = [[rng.randrange(0, N + 1) * 2 for _ in range(K)]]
            for t in range(1, T + 1):
                pos.append([min(W, max(0, p + rng.choice((-1, 0, 1)))) for p in pos[-1]])
            pos = [sorted(r) for r in pos]
            mass_r = [rng.randint(1, 5) for _ in range(K)]
            signed = [([(t, -pos[t][k]) for t in range(T + 1)], mass_r[k]) for k in reversed(range(K))] + \
                     [([(t, pos[t][k]) for t in range(T + 1)], mass_r[k]) for k in range(K)]
            with open(law, 'w') as f:
                f.write(f'{len(signed)}\n')
                for pts, m in signed:
                    c = [pts[0]] + [b for a, b, d in zip(pts, pts[1:], pts[2:]) if (b[1] - a[1]) != (d[1] - b[1])] + [pts[-1]]
                    f.write(f'{m} {len(c)} ' + ' '.join(f'{t} {x}' for t, x in c) + '\n')
            out = json.loads(subprocess.run([exe, law], check=True, text=True, stdout=subprocess.PIPE).stdout)
            d, _ = best_response([Path(p) for p, _ in signed], [F(m) for _, m in signed])
            assert F(out['cost_times_2'], 2) == d, (trial, out, d)
    print('C++ program equals the Python program on', trials, 'random families with waiting pieces and unequal masses')


if __name__ == '__main__':
    import sys
    selftest()
    if '--compare' in sys.argv:
        compare_cpp()
