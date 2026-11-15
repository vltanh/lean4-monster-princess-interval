#!/usr/bin/env python3
"""Exact unrestricted upper certificate; Python standard library only.

Build the full-interval deadline network from rational path geometry, compute
an integer max flow, and independently verify its capacity/conservation and
the matching deadline assignment. No floating-point optimization is used.
"""
from collections import deque
from fractions import Fraction as Q
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parent


def position(path, t):
    for (a, x), (b, y) in zip(path, path[1:]):
        if a <= t <= b:
            numerator = (y-x)*(t-a)
            assert numerator % (b-a) == 0
            return x + numerator//(b-a)
    assert t >= path[-1][0]
    return path[-1][1]


def first_meeting(p, q):
    times = sorted({t for t, _ in p+q})
    old = None
    for t in times:
        d = position(p, t)-position(q, t)
        if d == 0:
            return t
        if old is not None:
            a, e = old
            if d*e < 0:
                assert ((t-a)*e) % (e-d) == 0
                return a + ((t-a)*e)//(e-d)
        old = t, d
    return None


def make_paths(spec):
    S = spec['space_time_scale']
    H = 4*S
    paths, weights = [], []
    for item in spec['families']:
        x = Q(item['start'])*S
        assert x.denominator == 1 and -S <= x < S
        x = int(x)
        if item['kind'] == 1:
            p = [(0,x),(S-x,S),(3*S-x,-S),(H,-S)]
        else:
            assert item['kind'] == 2 and (S-x) % 2 == 0
            p = [(0,x),((S-x)//2,(S+x)//2),(2*S,-S),(H,S)]
        p = list(dict.fromkeys(p))
        assert p[0][0] == 0 and p[-1][0] == H
        assert all(-S <= z <= S for _, z in p)
        assert all(b>a and abs(y-x)<=b-a for (a,x),(b,y) in zip(p,p[1:]))
        w = item['weight_numerator']
        assert isinstance(w,int) and w > 0
        paths.extend([p,[(t,-z) for t,z in p]])
        weights.extend([w,w])
    assert sum(weights) == 2*spec['weight_denominator']
    return paths, weights


def network(paths, weights, S, D, initial, meetings, walls):
    """Compressed per-path event lists, with full walls -1 and +1."""
    H = 4*S
    N = len(paths)
    below = [p[0][1] < initial for p in paths]
    assert all(p[0][1] != initial for p in paths)
    deadlines = [walls[i][int(below[i])] for i in range(N)]
    assert all(d is not None for d in deadlines)
    events = [{0,H,d} for d in deadlines]
    pairs = []
    for i in range(N):
        if not below[i]:
            continue
        for j in range(N):
            if below[j]:
                continue
            t = meetings[i][j]
            if t is not None and t < H:
                pairs.append((i,j,t))
                events[i].add(t)
                events[j].add(t)
    events = [sorted(e) for e in events]
    offsets, indices, n = [], [], 0
    for e in events:
        offsets.append(n)
        indices.append({t:k for k,t in enumerate(e)})
        n += len(e)-1
    source, sink = n, n+1
    # A cut of cost <= H*scale always exists. Thus no minimum cut uses an
    # implication arc, which has strictly larger capacity.
    scale = 2*D*S
    inf = 4*scale+1
    arcs = []
    for i, e in enumerate(events):
        o = offsets[i]
        for k,(a,b) in enumerate(zip(e,e[1:])):
            cap = weights[i]*(b-a)
            arcs.append((source,o+k,cap) if below[i] else (o+k,sink,cap))
        for k in range(len(e)-2):
            arcs.append((o+k+1,o+k,inf) if below[i] else (o+k,o+k+1,inf))
        if deadlines[i] < H:
            node = o+indices[i][deadlines[i]]
            arcs.append((node,sink,inf) if below[i] else (source,node,inf))
    for i,j,t in pairs:
        arcs.append((offsets[i]+indices[i][t],offsets[j]+indices[j][t],inf))
    return arcs,source,sink,scale,events,offsets,below,deadlines,pairs


def max_flow(arcs, source, sink):
    size = sink+1
    adj = [[] for _ in range(size)]
    to, capacity = [], []
    for u,v,c in arcs:
        k = len(to)
        adj[u].append(k)
        adj[v].append(k+1)
        to.extend([v,u])
        capacity.extend([c,0])
    total = 0
    while True:
        level = [-1]*size
        level[source] = 0
        queue = deque([source])
        while queue:
            u = queue.popleft()
            for k in adj[u]:
                v = to[k]
                if capacity[k] and level[v] < 0:
                    level[v] = level[u]+1
                    queue.append(v)
        if level[sink] < 0:
            break
        ptr = [0]*size
        nodes, edges = [source], []
        while nodes:
            u = nodes[-1]
            if u == sink:
                amount = min(capacity[k] for k in edges)
                first = len(edges)
                for j,k in enumerate(edges):
                    capacity[k] -= amount
                    capacity[k^1] += amount
                    if capacity[k] == 0:
                        first = min(first,j)
                total += amount
                nodes = nodes[:first+1]
                edges = edges[:first]
                continue
            while ptr[u] < len(adj[u]):
                k = adj[u][ptr[u]]
                if capacity[k] and level[to[k]] == level[u]+1:
                    break
                ptr[u] += 1
            if ptr[u] == len(adj[u]):
                level[u] = -1
                nodes.pop()
                if edges:
                    edges.pop()
                    ptr[nodes[-1]] += 1
            else:
                k = adj[u][ptr[u]]
                edges.append(k)
                nodes.append(to[k])
    flows = [c-capacity[2*k] for k,(_,_,c) in enumerate(arcs)]
    # Independent primal feasibility check, with no reliance on Dinic's state.
    balance = [0]*size
    for (u,v,c),f in zip(arcs,flows):
        assert 0 <= f <= c
        balance[u] += f
        balance[v] -= f
    assert balance[source] == total and balance[sink] == -total
    balance[source] = balance[sink] = 0
    assert not any(balance)
    return total, [d >= 0 for d in level]


def main():
    spec = json.loads((ROOT/'strategy.json').read_text())
    S, D = spec['space_time_scale'], spec['weight_denominator']
    assert isinstance(S,int) and S>0 and isinstance(D,int) and D>0
    paths, weights = make_paths(spec)
    N, H = len(paths), 4*S
    meetings = [[None]*N for _ in range(N)]
    walls = []
    for i,p in enumerate(paths):
        walls.append([first_meeting(p,[(0,w),(H,w)]) for w in (-S,S)])
        for j in range(i):
            meetings[i][j] = meetings[j][i] = first_meeting(p,paths[j])
    starts = sorted({0,S}|{abs(p[0][1]) for p in paths})
    results, max_arcs, total_arcs = [], 0, 0
    for a,b in zip(starts,starts[1:]):
        initial = Q(a+b,2)
        graph = network(paths,weights,S,D,initial,meetings,walls)
        arcs,source,sink,scale,events,offsets,below,deadlines,pairs = graph
        flow, reachable = max_flow(arcs,source,sink)
        r = []
        for i,e in enumerate(events):
            alive = reachable[offsets[i]:offsets[i]+len(e)-1]
            if not below[i]:
                alive = [not z for z in alive]
            assert all(x>=y for x,y in zip(alive,alive[1:]))
            r.append(e[sum(alive)])
        assert all(r[i]<=deadlines[i] for i in range(N))
        assert all(min(r[i],r[j])<=t for i,j,t in pairs)
        value = Q(sum(w*t for w,t in zip(weights,r)),scale)
        assert value == 4-Q(flow,scale)
        max_arcs = max(max_arcs,len(arcs))
        total_arcs += len(arcs)
        results.append(value)
        print(f'Chamber ({Q(a,S)}, {Q(b,S)}): {value}',flush=True)
    upper = max(results)
    print('Exact unrestricted upper:',upper,flush=True)
    print('Decimal display:',float(upper),flush=True)
    print('Paths:',N,'chambers:',len(results),'arcs:',total_arcs,'maximum per chamber:',max_arcs,flush=True)
    if 'expected_upper' in spec:
        assert upper == Q(spec['expected_upper'])
    old_upper = Q(5717477,4000000)
    assert upper < old_upper
    print('Exact improvement:',old_upper-upper,flush=True)
    print('PASS: every integer flow is feasible and matches a feasible deadline cut.',flush=True)
    print('SCOPE: an improved upper bound, not the unrestricted exact value.',flush=True)


if __name__ == '__main__':
    main()
