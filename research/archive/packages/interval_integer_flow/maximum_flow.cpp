// Untrusted discovery optimizer. Every emitted witness is checked with BigInt.
#include <algorithm>
#include <cstdint>
#include <iostream>
#include <limits>
#include <stdexcept>
#include <string>
#include <vector>

using U = std::uint64_t;
static constexpr U LIMIT = std::numeric_limits<std::int64_t>::max();

U number() {
    std::string token;
    if (!(std::cin >> token) || token.empty()) throw std::runtime_error("missing integer");
    U value = 0;
    for (char c : token) {
        if (c < '0' || c > '9' || value > (LIMIT - U(c-'0'))/10)
            throw std::runtime_error("invalid or overflowing integer");
        value = value*10 + U(c-'0');
    }
    return value;
}

struct Edge { int to; U cap; };

int main() {
    try {
        std::ios::sync_with_stdio(false);
        std::cin.tie(nullptr);
        std::string magic;
        std::cin >> magic;
        if (magic != "PMFLOW1") throw std::runtime_error("bad format");
        U n64=number(), m64=number(), s64=number(), t64=number(), bound=number();
        if (n64<2 || n64>5000000 || m64>50000000 || s64>=n64 || t64>=n64 || s64==t64)
            throw std::runtime_error("invalid graph dimensions");
        int n=int(n64), m=int(m64), s=int(s64), t=int(t64);
        std::vector<std::vector<int>> adj(n);
        std::vector<Edge> edges;
        edges.reserve(std::size_t(m)*2);
        std::vector<U> capacities;
        capacities.reserve(m);
        U source_total=0;
        for (int i=0; i<m; ++i) {
            U a=number(), b=number(), cap=number();
            if (a>=n64 || b>=n64 || a==b) throw std::runtime_error("invalid edge");
            if (a==s64) {
                if (source_total>LIMIT-cap) throw std::runtime_error("source capacity overflow");
                source_total+=cap;
            }
            int id=int(edges.size());
            adj[a].push_back(id); edges.push_back({int(b),cap});
            adj[b].push_back(id+1); edges.push_back({int(a),0});
            capacities.push_back(cap);
        }
        std::string extra;
        if (std::cin >> extra) throw std::runtime_error("extra edge or trailing token");
        if (source_total!=bound) throw std::runtime_error("wrong source capacity bound");

        std::vector<int> level(n), next(n), queue(n), path_nodes, path_edges;
        std::vector<U> path_caps;
        path_nodes.reserve(n); path_edges.reserve(n); path_caps.reserve(n);
        U flow=0;
        for (;;) {
            std::fill(level.begin(),level.end(),-1);
            int head=0, tail=1; queue[0]=s; level[s]=0;
            while (head<tail) {
                int a=queue[head++];
                for (int id:adj[a]) {
                    const auto &e=edges[id];
                    if (e.cap && level[e.to]<0) {level[e.to]=level[a]+1;queue[tail++]=e.to;}
                }
            }
            if (level[t]<0) break;
            std::fill(next.begin(),next.end(),0);
            for (;;) {
                path_nodes.assign(1,s); path_edges.clear(); path_caps.assign(1,bound);
                U sent=0;
                while (!path_nodes.empty()) {
                    int a=path_nodes.back();
                    if (a==t) {
                        sent=path_caps.back();
                        if (!sent) throw std::runtime_error("zero augmenting path");
                        for (int id:path_edges) {
                            if (edges[id].cap<sent || edges[id^1].cap>LIMIT-sent)
                                throw std::runtime_error("residual capacity overflow");
                            edges[id].cap-=sent; edges[id^1].cap+=sent;
                        }
                        break;
                    }
                    auto &pos=next[a];
                    while (pos<int(adj[a].size())) {
                        const auto &e=edges[adj[a][pos]];
                        if (e.cap && level[e.to]==level[a]+1) break;
                        ++pos;
                    }
                    if (pos==int(adj[a].size())) {
                        level[a]=-1;
                        path_nodes.pop_back(); path_caps.pop_back();
                        if (!path_edges.empty()) path_edges.pop_back();
                    } else {
                        int id=adj[a][pos];
                        path_nodes.push_back(edges[id].to); path_edges.push_back(id);
                        path_caps.push_back(std::min(path_caps.back(),edges[id].cap));
                    }
                }
                if (!sent) break;
                if (flow>bound-sent) throw std::runtime_error("flow exceeds source bound");
                flow+=sent;
            }
        }
        std::vector<unsigned char> reached(n,0);
        int head=0,tail=1;queue[0]=s;reached[s]=1;
        while (head<tail) {
            int a=queue[head++];
            for (int id:adj[a]) if (edges[id].cap && !reached[edges[id].to]) {
                reached[edges[id].to]=1;queue[tail++]=edges[id].to;
            }
        }
        if (reached[t]) throw std::runtime_error("residual sink still reachable");
        std::cout << "{\"graph_nodes\":" << n << ",\"graph_arcs\":" << m
                  << ",\"flow\":\"" << flow << "\",\"entries\":[";
        bool comma=false;
        for (int i=0;i<m;++i) {
            if (edges[2*i].cap>capacities[i]) throw std::runtime_error("negative forward flow");
            U amount=capacities[i]-edges[2*i].cap;
            if (amount) {
                if (comma) std::cout << ','; comma=true;
                std::cout << '[' << i << ",\"" << amount << "\"]";
            }
        }
        std::cout << "],\"source_side\":[";comma=false;
        for(int i=0;i<n;++i) if(reached[i]) {
            if(comma)std::cout<<',';comma=true;std::cout<<i;
        }
        std::cout << "]}\n";
        return 0;
    } catch (const std::exception &error) {
        std::cerr << "integer flow rejected input/result: " << error.what() << '\n';
        return 2;
    }
}
