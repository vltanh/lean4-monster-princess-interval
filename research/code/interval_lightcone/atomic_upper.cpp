// Exact all-Princess upper bound for an atomic Monster law of one-turn pairs P_b(a) and two-turn pairs T2(c, U1).
//
// Usage: atomic_upper LAW.txt N [values_out.txt [staircases_out.txt [count]]]
//
// LAW.txt is the compact law (bin masses over a common denominator).  N must be a multiple of the law's mesh.
// The program places the atoms on the grid 1/N by the product trapezoid rule, in integer weights, and maximises
// the Princess's total reward over all cell staircases by an integer dynamic program.  All arithmetic is in
// 64-bit integers with an a-priori overflow guard.  Output: the maximum K and the bound K / (8 N W), W the total
// atom weight.  With a fourth argument the program also writes a maximising staircase for each of the `count`
// best start cells (lines `U c k`: the line U = c h is crossed in row k; `W y m`: W = y h is crossed in
// column m); optimize_atomic_law.py uses them as cutting planes.  `count` may instead be a list `@k1,k2,...`
// of start cells to trace (strategy_page_data.py uses this).  The staircase output does not affect the bound.  A law file that starts with `atoms` lists
// atoms directly (`P a b w`, `T c u w`); the tests use this.
#include <algorithm>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <string>
#include <vector>
#include <omp.h>
typedef long long ll;
typedef __int128 i128;

struct Atom { int s, l; ll w; };          // start index, level index (b or U1), weight

static void die(const char* msg) { fprintf(stderr, "error: %s\n", msg); exit(1); }

static void print128(i128 x) {
    if (x == 0) { printf("0"); return; }
    char buf[64]; int n = 0; bool neg = x < 0; if (neg) x = -x;
    while (x > 0) { buf[n++] = '0' + (int)(x % 10); x /= 10; }
    if (neg) putchar('-');
    while (n--) putchar(buf[n]);
}

int main(int argc, char** argv) {
    if (argc < 3) die("usage: atomic_upper LAW.txt N [values_out.txt [staircases_out.txt [count]]]");
    const int N = atoi(argv[2]);
    FILE* f = fopen(argv[1], "r"); if (!f) die("cannot open law");
    int n = 0, nb = 0; ll D = 0, sweep = 0; bool raw = false;
    std::vector<Atom> rawP, rawT;
    struct Rec { char kind[8]; int i, j; ll m; };
    std::vector<Rec> recs;
    char key[64];
    while (fscanf(f, "%63s", key) == 1) {
        if (!strcmp(key, "mesh")) { if (fscanf(f, "%d", &n) != 1) die("mesh"); }
        else if (!strcmp(key, "levels")) { if (fscanf(f, "%d", &nb) != 1) die("levels"); }
        else if (!strcmp(key, "denominator")) { if (fscanf(f, "%lld", &D) != 1) die("denominator"); }
        else if (!strcmp(key, "sweep")) { if (fscanf(f, "%lld", &sweep) != 1) die("sweep"); }
        else if (!strcmp(key, "atoms")) { raw = true; }
        else if (raw && (!strcmp(key, "P") || !strcmp(key, "T"))) {
            Atom a; if (fscanf(f, "%d %d %lld", &a.s, &a.l, &a.w) != 3) die("bad atom");
            (key[0] == 'P' ? rawP : rawT).push_back(a);
        }
        else {
            Rec r; memset(&r, 0, sizeof r); strncpy(r.kind, key, 7); r.j = -1;
            if (!strcmp(key, "P1p") || !strcmp(key, "Sp") || !strcmp(key, "P1m") || !strcmp(key, "Sm")) {
                if (fscanf(f, "%d %lld", &r.i, &r.m) != 2) die("bad 1d record");
            } else if (!strcmp(key, "Qp") || !strcmp(key, "Qm") || !strcmp(key, "Tp") || !strcmp(key, "Tm")) {
                if (fscanf(f, "%d %d %lld", &r.i, &r.j, &r.m) != 3) die("bad 2d record");
            } else die("unknown keyword");
            if (r.m < 0) die("negative mass");
            recs.push_back(r);
        }
    }
    fclose(f);
    if (raw) n = N;
    if (n <= 0 || N <= 0 || N % n) die("N must be a positive multiple of the mesh");
    const int r = N / n;
    // ---- atoms ------------------------------------------------------------------------------------------
    std::vector<Atom> P, T;
    ll bins = sweep;
    if (raw) { P = rawP; T = rawT; }
    else P.push_back({N, N, sweep * 4LL * r * r});
    auto e = [&](int t) { return (t == 0 || t == r) ? 1LL : 2LL; };      // trapezoid end weights
    for (const Rec& q : recs) {
        bins += q.m;
        if (q.m == 0) continue;
        std::string k = q.kind;
        if (q.i < 0 || q.i >= n) die("bin out of range");
        if (k == "P1p" || k == "Sp" || k == "P1m" || k == "Sm") {
            for (int t = 0; t <= r; t++) {
                int a = q.i * r + t; ll w = q.m * 2LL * r * e(t);
                if (k == "P1p") P.push_back({a, N, w});
                if (k == "Sp")  P.push_back({a, 2 * N - a, w});
                if (k == "P1m") P.push_back({-a, N, w});
                if (k == "Sm")  P.push_back({-a, 2 * N + a, w});
            }
        } else if (k == "Qp" || k == "Qm") {
            if (q.j < 0 || q.j >= 2 * nb) die("level bin out of range");
            for (int t = 0; t <= r; t++) for (int u = 0; u <= r; u++) {
                int a = q.i * r + t, b = (n - nb + q.j) * r + u; ll w = q.m * e(t) * e(u);
                P.push_back({k == "Qp" ? a : -a, b, w});
            }
        } else {
            if (q.j < 0 || q.j >= n) die("U1 bin out of range");
            for (int t = 0; t <= r; t++) for (int u = 0; u <= r; u++) {
                int c = q.i * r + t, u1 = q.j * r + u; ll w = q.m * e(t) * e(u);
                T.push_back({k == "Tp" ? c : -c, u1, w});
            }
        }
    }
    if (!raw && bins != D) die("bin masses do not sum to the denominator");
    i128 total = 0;
    for (const Atom& a : P) { if (std::abs(a.s) > a.l || a.l > 2 * N - a.s || a.w < 0) die("illegal one-turn atom"); total += a.w; }
    for (const Atom& a : T) { if (std::abs(a.s) > a.l || a.l > N || a.w < 0) die("illegal two-turn atom"); total += a.w; }
    if (!raw && total != (i128)D * 4 * r * r) die("total weight mismatch");
    if (total <= 0) die("empty law");
    // every atom is rewarded at most twice, each reward at most (24N + 4) * weight
    if (total * (48LL * N + 8) >= ((i128)1 << 62)) die("overflow guard: weights too large for 64-bit arithmetic");
    const ll W = (ll)total;
    // ---- capped rows of the originals: row y = -start, cap = level; y in [-N, N], cap in [0, 3N] ----------------
    const int NC = 3 * N + 1;                       // m index 0..3N
    std::vector<ll> CW((size_t)(2 * N + 1) * NC, 0), ER((size_t)(2 * N + 1) * NC, 0);
    {
        // capmass[y][cap], capesc[y][cap]
        std::vector<ll> cm((size_t)(2 * N + 1) * (NC + 1), 0), ce((size_t)(2 * N + 1) * (NC + 1), 0);
        for (const Atom& a : P) { size_t y = (size_t)(-a.s + N); cm[y * (NC + 1) + a.l] += a.w; ce[y * (NC + 1) + a.l] += a.w * (4LL * a.l + 12LL * N); }
        for (const Atom& a : T) { size_t y = (size_t)(-a.s + N); cm[y * (NC + 1) + a.l] += a.w; ce[y * (NC + 1) + a.l] += a.w * (8LL * N); }
        for (size_t y = 0; y < (size_t)(2 * N + 1); y++) {
            // CW[y][m] = sum_{cap >= m+1} mass ; ER[y][m] = sum_{cap <= m} mass * esc
            ll suf = 0;
            for (int m = NC - 1; m >= 0; m--) { suf += cm[y * (NC + 1) + m + 1]; CW[y * NC + m] = suf; }
            ll pre = 0;
            for (int m = 0; m < NC; m++) { pre += ce[y * (NC + 1) + m]; ER[y * NC + m] = pre; }
        }
    }
    // mirrors that start at +c (c >= 1): vertical line c
    std::vector<ll> Vm(5 * N + 3, 0);
    for (const Atom& a : P) if (-a.s >= 1) Vm[-a.s] += a.w;
    for (const Atom& a : T) if (-a.s >= 1) Vm[-a.s] += a.w;
    // ---- dynamic program, one start cell at a time -------------------------------------------------------------
    std::vector<ll> val(N, 0);
    const ll NEG = -((ll)1 << 62);
    #pragma omp parallel
    {
        std::vector<ll> Vw(5 * N + 3), M2(4 * N + 2), M3(4 * N + 2), cur(5 * N + 3), up(5 * N + 3);
        #pragma omp for schedule(dynamic, 1)
        for (int k0 = N - 1; k0 >= 0; k0--) {
            std::fill(Vw.begin(), Vw.end(), 0); std::fill(M2.begin(), M2.end(), 0); std::fill(M3.begin(), M3.end(), 0);
            for (const Atom& a : P) { if (a.s >= k0 + 1) Vw[a.l] += a.w; if (a.s >= -k0) M2[a.l + N] += a.w; }
            for (const Atom& a : T) { if (a.s >= k0 + 1) Vw[a.l] += a.w; if (a.s >= -k0) M3[a.l + N] += a.w; }
            for (int c = k0 + 1; c <= N; c++) Vw[c] += Vm[c];
            for (int k = 3 * N; k >= -k0 - 1; k--) {
                const int mlo = std::max(k, k0), mhi = std::min(5 * N, k + 2 * N);
                const int y = k + 1;
                const bool up_row = (k + 1 <= 3 * N);
                const ll* cw = (y <= N) ? &CW[(size_t)(y + N) * NC] : nullptr;
                const ll* er = (y <= N) ? &ER[(size_t)(y + N) * NC] : nullptr;
                const ll m2 = up_row ? M2[y + N] : 0, m3 = up_row ? M3[y + N] : 0;
                for (int m = mhi; m >= mlo; m--) {
                    const ll coord = 2LL * (m + 1) + 2LL * (k + 1);
                    ll best = NEG; bool any = false;
                    if (m + 1 <= mhi) { best = cur[m + 1] + Vw[m + 1] * coord; any = true; }
                    if (up_row && m >= k + 1) {
                        const int mc = std::min(m, NC - 1);
                        ll wgt = m2 + (cw ? cw[mc] : 0), add = er ? er[mc] : 0;
                        if (m + 1 <= N) wgt += m3; else add += m3 * 16LL * N;
                        const ll v = up[m] + wgt * coord + add;
                        if (!any || v > best) best = v;
                        any = true;
                    }
                    if (!any) best = 0;
                    if (k >= 3 * N && best < 0) best = 0;
                    cur[m] = best;
                }
                std::swap(cur, up);       // row k becomes the row above for k - 1
            }
            val[k0] = up[k0];
        }
    }
    ll K = -1; int arg = -1;
    for (int k0 = 0; k0 < N; k0++) if (val[k0] > K) { K = val[k0]; arg = k0; }
    if (argc > 4) {
      std::vector<int> order(N);
      for (int i = 0; i < N; i++) order[i] = i;
      std::sort(order.begin(), order.end(), [&](int x, int y) { return val[x] > val[y]; });
      int npaths = 1;
      if (argc > 5 && argv[5][0] == '@') {               // explicit list of start cells
        order.clear();
        for (const char* c = argv[5] + 1; *c;) {
          char* end; long k = strtol(c, &end, 10);
          if (end == c || k < 0 || k >= N) die("bad start-cell list");
          order.push_back((int)k); c = (*end == ',') ? end + 1 : end;
          if (*end && *end != ',') die("bad start-cell list");
        }
        npaths = (int)order.size();
      } else if (argc > 5) npaths = atoi(argv[5]);
      FILE* g = fopen(argv[4], "w");
      for (int pi = 0; pi < npaths && pi < (int)order.size(); pi++) {
        // rerun the start cell with the decisions stored, then trace a maximising staircase
        const int k0 = order[pi];
        const int rows = 4 * N + 2, cols = 5 * N + 3;
        std::vector<unsigned char> dec((size_t)rows * cols, 2);
        std::vector<ll> Vw(5 * N + 3, 0), M2(4 * N + 2, 0), M3(4 * N + 2, 0), cur(5 * N + 3), up(5 * N + 3);
        for (const Atom& a : P) { if (a.s >= k0 + 1) Vw[a.l] += a.w; if (a.s >= -k0) M2[a.l + N] += a.w; }
        for (const Atom& a : T) { if (a.s >= k0 + 1) Vw[a.l] += a.w; if (a.s >= -k0) M3[a.l + N] += a.w; }
        for (int c = k0 + 1; c <= N; c++) Vw[c] += Vm[c];
        for (int k = 3 * N; k >= -k0 - 1; k--) {
            const int mlo = std::max(k, k0), mhi = std::min(5 * N, k + 2 * N);
            const int y = k + 1;
            const bool up_row = (k + 1 <= 3 * N);
            const ll* cw = (y <= N) ? &CW[(size_t)(y + N) * NC] : nullptr;
            const ll* er = (y <= N) ? &ER[(size_t)(y + N) * NC] : nullptr;
            const ll m2 = up_row ? M2[y + N] : 0, m3 = up_row ? M3[y + N] : 0;
            for (int m = mhi; m >= mlo; m--) {
                const ll coord = 2LL * (m + 1) + 2LL * (k + 1);
                ll best = NEG; bool any = false; unsigned char d = 2;
                if (m + 1 <= mhi) { best = cur[m + 1] + Vw[m + 1] * coord; any = true; d = 0; }
                if (up_row && m >= k + 1) {
                    const int mc = std::min(m, NC - 1);
                    ll wgt = m2 + (cw ? cw[mc] : 0), add = er ? er[mc] : 0;
                    if (m + 1 <= N) wgt += m3; else add += m3 * 16LL * N;
                    const ll v = up[m] + wgt * coord + add;
                    if (!any || v > best) { best = v; d = 1; }
                    any = true;
                }
                if (!any) { best = 0; d = 2; }
                if (k >= 3 * N) { if (best <= 0) { best = 0; d = 2; } }
                cur[m] = best;
                dec[(size_t)(k + N + 1) * cols + m] = d;
            }
            std::swap(cur, up);
        }
        if (up[k0] != val[k0]) die("path rerun mismatch");
        fprintf(g, "start %d %lld\n", k0, val[k0]);
        int m = k0, k = -k0 - 1;
        while (true) {
            unsigned char d = dec[(size_t)(k + N + 1) * cols + m];
            if (d == 0) { fprintf(g, "U %d %d\n", m + 1, k); m++; }
            else if (d == 1) { fprintf(g, "W %d %d\n", k + 1, m); k++; }
            else break;
        }
        fprintf(g, "end %d %d\n", m, k);
      }
      fclose(g);
    }
    if (argc > 3) { FILE* g = fopen(argv[3], "w"); for (int k0 = 0; k0 < N; k0++) fprintf(g, "%lld\n", val[k0]); fclose(g); }
    i128 den = (i128)8 * N * W;
    printf("{\"N\": %d, \"mesh\": %d, \"one_turn_atoms\": %zu, \"two_turn_atoms\": %zu, \"total_weight\": %lld, \"maximum\": %lld, \"best_start_cell\": %d, \"bound_numerator\": %lld, \"bound_denominator\": ",
           N, n, P.size(), T.size(), W, K, arg, K);
    print128(den);
    printf(", \"bound\": %.15f}\n", (double)((long double)K / (long double)den));
    return 0;
}
