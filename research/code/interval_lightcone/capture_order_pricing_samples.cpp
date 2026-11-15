// Exact Monster best response against a finite ordered Princess law given by sample positions.
//
// Input (binary, little endian): int32 K, int32 T, then K * (T + 1) int32 positions X[k][t], k = 0..K-1 ascending
// at every t, |X[k][t+1] - X[k][t]| <= 1, X >= 0.  Path k is the linear interpolation of its samples and is
// constant after T.  The law is the 2K signed paths -X[K-1] .. -X[0], X[0] .. X[K-1], each with mass 1.
// Times and positions are doubled internally; every meeting time is then an integer (checked).
// Output: total cost (sum of capture times, doubled), labels, and optionally itineraries.
#include <algorithm>
#include <cstdio>
#include <cstdlib>
#include <vector>
typedef long long ll;
static int K, T, M;
static std::vector<int> X;
static inline ll pos2(int s, ll n) {                       // doubled position of signed path s at doubled time n
    const int k = s < K ? K - 1 - s : s - K; const int* row = &X[(size_t)k * (T + 1)];
    ll q = n >> 1, v;
    if (q >= T) v = 2LL * row[T];
    else if (n & 1) v = (ll)row[q] + row[q + 1];
    else v = 2LL * row[q];
    return s < K ? -v : v;
}
static ll meet(int s, ll tau, ll y, int dir) {             // first n >= tau with dir * (pos2(s, n) - y) <= n - tau
    ll g0 = dir * (pos2(s, tau) - y);
    if (g0 <= 0) return tau;
    ll lo = tau, hi = std::max(tau, (ll)2 * T) + dir * (pos2(s, std::max(tau, (ll)2 * T)) - y) + 2;   // g(hi) <= 0
    hi = std::max(hi, tau + 1);
    while (hi - lo > 1) {
        ll mid = (lo + hi) / 2;
        if (dir * (pos2(s, mid) - y) - (mid - tau) <= 0) hi = mid; else lo = mid;
    }
    if (dir * (pos2(s, hi) - y) - (hi - tau) != 0) { fprintf(stderr, "meeting between half-steps\n"); exit(1); }
    return hi;
}
struct Label { ll tau, cost; int parent, state, next; };
static std::vector<Label> pool;
static std::vector<int> head;
static inline size_t sid(int i, int j, int side) { return ((size_t)i * M + j) * 2 + side; }
static void push(int i, int j, int side, ll tau, ll cost, int parent) {
    size_t s = sid(i, j, side);
    for (int l = head[s]; l >= 0; l = pool[l].next) if (pool[l].tau <= tau && pool[l].cost <= cost) return;
    int prev = -1;
    for (int l = head[s]; l >= 0;) {
        int nx = pool[l].next;
        if (tau <= pool[l].tau && cost <= pool[l].cost) { if (prev < 0) head[s] = nx; else pool[prev].next = nx; }
        else prev = l;
        l = nx;
    }
    pool.push_back({tau, cost, parent, (int)s, head[s]});
    head[s] = (int)pool.size() - 1;
}
int main(int argc, char** argv) {
    if (argc < 2) { fprintf(stderr, "usage: capture_cols LAW.bin [itinerary_out]\n"); return 1; }
    FILE* f = fopen(argv[1], "rb");
    if (fread(&K, 4, 1, f) != 1 || fread(&T, 4, 1, f) != 1) return 1;
    X.resize((size_t)K * (T + 1));
    if (fread(X.data(), 4, X.size(), f) != X.size()) return 1;
    fclose(f);
    M = 2 * K;
    for (int k = 0; k < K; k++) for (int t = 0; t <= T; t++) {
        int v = X[(size_t)k * (T + 1) + t];
        if (v < 0) { fprintf(stderr, "negative position\n"); return 1; }
        if (t < T && std::abs(X[(size_t)k * (T + 1) + t + 1] - v) > 1) { fprintf(stderr, "speed above 1 in path %d\n", k); return 1; }
        if (k + 1 < K && X[(size_t)(k + 1) * (T + 1) + t] < v) { fprintf(stderr, "paths not ordered at time %d\n", t); return 1; }
    }
    head.assign((size_t)M * M * 2, -1);
    auto tied = [&](int& i, int& j, ll n, ll y) {
        while (i > 0 && pos2(i - 1, n) == y) i--;
        while (j < M - 1 && pos2(j + 1, n) == y) j++;
    };
    for (int k = 0; k < M; k++) {
        int i = k, j = k; ll y = pos2(k, 0); tied(i, j, 0, y);
        push(i, j, 0, 0, 0, -1); push(i, j, 1, 0, 0, -1);
    }
    for (int w = 1; w < M; w++) for (int i = 0; i + w - 1 < M; i++) {
        int j = i + w - 1;
        for (int side = 0; side < 2; side++) for (int l = head[sid(i, j, side)]; l >= 0; l = pool[l].next) {
            const ll tau = pool[l].tau, cost = pool[l].cost;
            const ll y = pos2(side ? j : i, tau);
            if (j < M - 1) {
                ll t2 = meet(j + 1, tau, y, +1), y2 = pos2(j + 1, t2);
                int i2 = i, j2 = j + 1; tied(i2, j2, t2, y2);
                ll c2 = cost + t2 * ((i - i2) + (j2 - j));
                push(i2, j2, 1, t2, c2, l);
                if (pos2(i2, t2) == y2) push(i2, j2, 0, t2, c2, l);
            }
            if (i > 0) {
                ll t2 = meet(i - 1, tau, y, -1), y2 = pos2(i - 1, t2);
                int i2 = i - 1, j2 = j; tied(i2, j2, t2, y2);
                ll c2 = cost + t2 * ((i - i2) + (j2 - j));
                push(i2, j2, 0, t2, c2, l);
                if (pos2(j2, t2) == y2) push(i2, j2, 1, t2, c2, l);
            }
        }
    }
    ll best = -1; int bl = -1;
    for (int side = 0; side < 2; side++) for (int l = head[sid(0, M - 1, side)]; l >= 0; l = pool[l].next)
        if (best < 0 || pool[l].cost < best) { best = pool[l].cost; bl = l; }
    if (best < 0) { fprintf(stderr, "no terminal label\n"); return 1; }
    printf("{\"paths\": %d, \"samples\": %d, \"cost_times_2\": %lld, \"labels\": %zu}\n", M, T, best, pool.size());
    if (argc > 2) {
        std::vector<int> chain;
        for (int l = bl; l >= 0; l = pool[l].parent) chain.push_back(l);
        std::reverse(chain.begin(), chain.end());
        FILE* g = fopen(argv[2], "w");
        for (int l : chain) { size_t s = pool[l].state; fprintf(g, "%d %d %d %lld\n", (int)((s >> 1) / M), (int)((s >> 1) % M), (int)(s & 1), pool[l].tau); }
        fclose(g);
    }
    return 0;
}
