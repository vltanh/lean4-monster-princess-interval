// Exact Monster best response against a finite ordered Princess law in continuous time.
//
// Input (text): M, then for each signed path (in increasing order of position): mass nb  t_1 x_1 ... t_nb x_nb
// with integer breakpoints, t_1 = 0, slopes in {-1, 0, 1}; the path is constant after its last breakpoint.
// All coordinates are doubled internally, so that every meeting time is an integer.
// Output: minimal total cost sum_i mass_i * (capture time of path i), in the input time unit times 2 (reported
// as numerator over 2), the number of labels, and the itineraries of the best responses for the `nroots` best
// starting paths: lines "it root cost n" followed by n lines "i j side time2".
//
// States: captured interval [i, j] and the side on which the Monster stands; labels (time, cost) kept as Pareto
// sets.  Between captures the Monster runs at full speed to the next path on the left or on the right.
#include <algorithm>
#include <cstdio>
#include <cstdlib>
#include <vector>
typedef long long ll;

struct Path { std::vector<ll> t, x; ll mass; };
static std::vector<Path> P;
static int M;

static inline ll pos(const Path& p, ll t) {
    const int n = (int)p.t.size();
    if (t >= p.t[n - 1]) return p.x[n - 1];
    int lo = 0, hi = n - 1;
    while (hi - lo > 1) { int mid = (lo + hi) / 2; if (p.t[mid] <= t) lo = mid; else hi = mid; }
    ll dt = p.t[hi] - p.t[lo], dx = p.x[hi] - p.x[lo];
    return p.x[lo] + (dx / dt) * (t - p.t[lo]);          // slope is -1, 0 or 1
}
// first t >= tau with dir * (x(t) - (y + dir * (t - tau))) <= 0
static ll meet(const Path& p, ll tau, ll y, int dir) {
    const int n = (int)p.t.size();
    ll g = dir * (pos(p, tau) - y);
    if (g <= 0) return tau;
    int k = 0;
    while (k + 1 < n && p.t[k + 1] <= tau) k++;
    ll t0 = tau;
    while (true) {
        ll t1 = -1; ll s = -1;                           // slope of g on this piece: dir * slope - 1
        if (k + 1 < n) { t1 = p.t[k + 1]; s = dir * ((p.x[k + 1] - p.x[k]) / (p.t[k + 1] - p.t[k])) - 1; }
        if (s < 0) {
            if (g % (-s) != 0) { fprintf(stderr, "non-integer meeting time\n"); exit(1); }
            ll tz = t0 + g / (-s);
            if (t1 < 0 || tz <= t1) return tz;
        }
        if (t1 < 0) { fprintf(stderr, "no meeting\n"); exit(1); }
        g += s * (t1 - t0); t0 = t1; k++;
    }
}

struct Label { ll tau, cost; int parent; int state; int root; int next; };
static std::vector<Label> pool;
static std::vector<int> head;                             // per state: first label
static inline size_t sid(int i, int j, int side) { return ((size_t)i * M + j) * 2 + side; }

static void push(int i, int j, int side, ll tau, ll cost, int parent, int root) {
    size_t s = sid(i, j, side);
    int prev = -1;
    for (int l = head[s]; l >= 0; l = pool[l].next) if (pool[l].tau <= tau && pool[l].cost <= cost) return;
    // remove dominated labels
    for (int l = head[s]; l >= 0;) {
        int nx = pool[l].next;
        if (tau <= pool[l].tau && cost <= pool[l].cost) { if (prev < 0) head[s] = nx; else pool[prev].next = nx; }
        else prev = l;
        l = nx;
    }
    pool.push_back({tau, cost, parent, (int)s, root, head[s]});
    head[s] = (int)pool.size() - 1;
}

int main(int argc, char** argv) {
    if (argc < 2) { fprintf(stderr, "usage: capture_dp LAW.txt [nroots [itineraries_out]]\n"); return 1; }
    int nroots = argc > 2 ? atoi(argv[2]) : 0;
    FILE* f = fopen(argv[1], "r");
    if (fscanf(f, "%d", &M) != 1) return 1;
    P.resize(M);
    for (int i = 0; i < M; i++) {
        int nb; if (fscanf(f, "%lld %d", &P[i].mass, &nb) != 2) return 1;
        P[i].t.resize(nb); P[i].x.resize(nb);
        for (int k = 0; k < nb; k++) { if (fscanf(f, "%lld %lld", &P[i].t[k], &P[i].x[k]) != 2) return 1; P[i].t[k] *= 2; P[i].x[k] *= 2; }
        if (P[i].t[0] != 0) { fprintf(stderr, "path must start at time 0\n"); return 1; }
        for (int k = 0; k + 1 < nb; k++) {
            ll dt = P[i].t[k + 1] - P[i].t[k], dx = P[i].x[k + 1] - P[i].x[k];
            if (dt <= 0 || (dx != dt && dx != -dt && dx != 0)) { fprintf(stderr, "bad segment in path %d\n", i); return 1; }
        }
    }
    fclose(f);
    // order check at all breakpoints
    for (int i = 0; i + 1 < M; i++) {
        for (ll t : P[i].t) if (pos(P[i], t) > pos(P[i + 1], t)) { fprintf(stderr, "paths %d and %d are not ordered\n", i, i + 1); return 1; }
        for (ll t : P[i + 1].t) if (pos(P[i], t) > pos(P[i + 1], t)) { fprintf(stderr, "paths %d and %d are not ordered\n", i, i + 1); return 1; }
    }
    std::vector<ll> pre(M + 1, 0);
    for (int i = 0; i < M; i++) pre[i + 1] = pre[i] + P[i].mass;
    head.assign((size_t)M * M * 2, -1);
    pool.reserve((size_t)4 * M * M / 2 + 16);
    auto tied = [&](int& i, int& j, ll t, ll y) {
        while (i > 0 && pos(P[i - 1], t) == y) i--;
        while (j < M - 1 && pos(P[j + 1], t) == y) j++;
    };
    for (int k = 0; k < M; k++) {
        int i = k, j = k; ll y = pos(P[k], 0); tied(i, j, 0, y);
        push(i, j, 0, 0, 0, -1, k); push(i, j, 1, 0, 0, -1, k);
    }
    for (int w = 1; w < M; w++) for (int i = 0; i + w - 1 < M; i++) {
        int j = i + w - 1;
        for (int side = 0; side < 2; side++) for (int l = head[sid(i, j, side)]; l >= 0; l = pool[l].next) {
            const ll tau = pool[l].tau, cost = pool[l].cost; const int root = pool[l].root;
            const ll y = pos(side ? P[j] : P[i], tau);
            if (j < M - 1) {
                ll t2 = meet(P[j + 1], tau, y, +1), y2 = pos(P[j + 1], t2);
                int i2 = i, j2 = j + 1; tied(i2, j2, t2, y2);
                ll c2 = cost + t2 * ((pre[i] - pre[i2]) + (pre[j2 + 1] - pre[j + 1]));
                push(i2, j2, 1, t2, c2, l, root);
                if (pos(P[i2], t2) == y2) push(i2, j2, 0, t2, c2, l, root);
            }
            if (i > 0) {
                ll t2 = meet(P[i - 1], tau, y, -1), y2 = pos(P[i - 1], t2);
                int i2 = i - 1, j2 = j; tied(i2, j2, t2, y2);
                ll c2 = cost + t2 * ((pre[i] - pre[i2]) + (pre[j2 + 1] - pre[j + 1]));
                push(i2, j2, 0, t2, c2, l, root);
                if (pos(P[j2], t2) == y2) push(i2, j2, 1, t2, c2, l, root);
            }
        }
    }
    // terminal labels: best cost per root
    std::vector<ll> bestc(M, -1); std::vector<int> bestl(M, -1);
    for (int side = 0; side < 2; side++) for (int l = head[sid(0, M - 1, side)]; l >= 0; l = pool[l].next) {
        int r = pool[l].root;
        if (bestc[r] < 0 || pool[l].cost < bestc[r]) { bestc[r] = pool[l].cost; bestl[r] = l; }
    }
    std::vector<int> order;
    for (int r = 0; r < M; r++) if (bestc[r] >= 0) order.push_back(r);
    std::sort(order.begin(), order.end(), [&](int a, int b) { return bestc[a] < bestc[b]; });
    if (order.empty()) { fprintf(stderr, "no terminal label\n"); return 1; }
    printf("{\"paths\": %d, \"total_mass\": %lld, \"cost_times_2\": %lld, \"labels\": %zu, \"best_root\": %d}\n",
           M, pre[M], bestc[order[0]], pool.size(), order[0]);
    if (argc > 3) {
        FILE* g = fopen(argv[3], "w");
        for (int q = 0; q < nroots && q < (int)order.size(); q++) {
            std::vector<int> chain;
            for (int l = bestl[order[q]]; l >= 0; l = pool[l].parent) chain.push_back(l);
            std::reverse(chain.begin(), chain.end());
            fprintf(g, "it %d %lld %zu\n", order[q], bestc[order[q]], chain.size());
            for (int l : chain) { size_t s = pool[l].state; int side = s & 1; size_t ij = s >> 1; fprintf(g, "%d %d %d %lld\n", (int)(ij / M), (int)(ij % M), side, pool[l].tau); }
        }
        fclose(g);
    }
    return 0;
}
