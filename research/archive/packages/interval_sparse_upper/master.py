#!/usr/bin/env python3
"""Project a physical calendar master onto its charged Qout events.

Floating LPs only discover physical weights.  The sparse integer closure
certificate and the existing full-grid verifier supply the upper proof.
No minimum over a finite route bank is a Princess lower certificate.
"""
from __future__ import annotations

from bisect import bisect_left, bisect_right
from collections import defaultdict
from pathlib import Path
import argparse
import gzip
import json
import sys
import time

import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix, csr_matrix


def read_json(path):
    raw = Path(path).read_bytes()
    return json.loads(gzip.decompress(raw) if raw[:2] == b"\x1f\x8b" else raw)


def projected_order(n, nodes):
    """All cover edges of interval containment, plus endpoint reachability.

    In light coordinates (u,v)=(j+k,k-j), containment is coordinatewise
    order.  At increasing u, only successive record-low eligible v values
    are minimal successors.  The extra endpoint chain represents stopping.
    """
    if len(set(nodes)) != len(nodes):
        raise ValueError("duplicate event")
    groups = defaultdict(list)
    for i, (j, k) in enumerate(nodes):
        if not (0 <= j <= 4*n and 1 <= k <= 2*n and (j+k) % 2 == 0):
            raise ValueError("invalid pre-two radial node")
        groups[j+k].append((k-j, i))
    us = sorted(groups)
    group_values, group_ids = [], []
    for u in us:
        entries = sorted(groups[u])
        group_values.append([v for v, _ in entries])
        group_ids.append([i for _, i in entries])
    edges = set()
    for i, (j, k) in enumerate(nodes):
        u, v = j+k, k-j
        start = bisect_left(us, u)
        best = None
        for z in range(start, len(us)):
            values = group_values[z]
            q = bisect_right(values, v) if z == start else bisect_left(values, v)
            if q == len(values):
                continue
            candidate = values[q]
            if best is None or candidate < best:
                edges.add((i, group_ids[z][q]))
                best = candidate
                if best == v:
                    break
    endpoints = sorted((j, i) for i, (j, k) in enumerate(nodes) if k == 2*n)
    times = [j for j, _ in endpoints]
    for (_, a), (_, b) in zip(endpoints, endpoints[1:]):
        edges.add((b, a))
    for i, (j, k) in enumerate(nodes):
        q = bisect_right(times, min(4*n, j+2*n-k)) - 1
        if q >= 0 and endpoints[q][1] != i:
            edges.add((i, endpoints[q][1]))
    return sorted(edges)


def plan_column(n, plan):
    positions = [int(plan['start_grid'])]
    if positions[0] % 2 or abs(positions[0]) > 2*n:
        raise ValueError("initial point")
    for step in plan['moves']:
        if step not in (-1, 1):
            raise ValueError("nonunit move")
        positions.append(positions[-1]+step)
    if any(abs(k) > 2*n for k in positions) or len(positions)-1 > 16*n:
        raise ValueError("physical path")
    if positions.index(0) > 4*n:
        raise ValueError("center deadline")
    coeff = defaultdict(int)
    mass = 0
    for name, sign, endpoint in [('minus_charges', 1, -2*n), ('plus_charges', -1, 2*n)]:
        end = positions.index(endpoint)
        counts = [0]*end
        for j, amount in plan[name]:
            if not isinstance(j, int) or not isinstance(amount, int) or not (0 <= j < end and amount > 0):
                raise ValueError("calendar entry")
            counts[j] += amount
            mass += amount
            x = sign*positions[j]
            k = abs(x)-max(0, j-4*n)
            if k > 0:
                coeff[min(j, 4*n), k] += amount*(1 if x > 0 else -1)
        cumulative = 0
        for j, amount in enumerate(counts):
            cumulative += amount
            if cumulative < j+1:
                raise ValueError("noncausal calendar")
        if cumulative != end:
            raise ValueError("calendar mass")
    return mass, {point: value for point, value in coeff.items() if value}


class SparseMaster:
    def __init__(self, n, denominator=10**9):
        self.n, self.D = n, denominator
        self.columns, self.seen = [], set()
        self.nodes, self.index, self.order = [], {}, []

    def add_plan(self, plan):
        mass, coeff = plan_column(self.n, plan)
        key = mass, tuple(sorted(coeff.items()))
        if key in self.seen:
            return False
        self.seen.add(key)
        self.columns.append({'plan': plan, 'mass': mass, 'coeff': coeff})
        return True

    def assemble(self):
        started = time.monotonic()
        self.nodes = sorted({point for column in self.columns for point in column['coeff']})
        self.index = {point: i for i, point in enumerate(self.nodes)}
        self.order = projected_order(self.n, self.nodes)
        K, E, scale = len(self.nodes), len(self.order), 4*self.n
        rr, cc, vv = [], [], []
        for row, (a, b) in enumerate(self.order):
            rr.extend((row, row)); cc.extend((a, b)); vv.extend((1., -1.))
        rhs = [0.]*E
        for row, column in enumerate(self.columns, E):
            rr.append(row); cc.append(K); vv.append(1.)
            for point, value in column['coeff'].items():
                rr.append(row); cc.append(self.index[point]); vv.append(-value/scale)
            rhs.append(column['mass']/scale)
        self.matrix = coo_matrix((vv, (rr, cc)), shape=(E+len(self.columns), K+1)).tocsr()
        self.rhs = np.asarray(rhs)
        self.assembly_seconds = time.monotonic()-started

    def solve(self, seconds=600, method='highs-ipm'):
        self.assemble()
        K = len(self.nodes)
        objective = np.zeros(K+1); objective[-1] = -1.
        result = linprog(objective, A_ub=self.matrix, b_ub=self.rhs,
                         bounds=[(0., 1.)]*K+[(0., 2.)], method=method,
                         options={'time_limit': float(seconds), 'primal_feasibility_tolerance': 1e-9,
                                  'dual_feasibility_tolerance': 1e-9})
        if not result.success:
            raise RuntimeError(result.message)
        return result, -result.ineqlin.marginals[len(self.order):]

    def extend_integer(self, values):
        """The least full Qout extension of the rounded event values.

        This is a feasible discovery field, not a certified lower.  Exact
        isotone closure also repairs floating feasibility tolerances.
        """
        n, D = self.n, self.D
        R, C, H = 2*n, 4*n, 12*n
        table = np.zeros((H+1, R+1), dtype=np.uint64)
        for (j, k), value in zip(self.nodes, values):
            table[j, k] = min(D, max(0, int(np.floor(float(value)*D))))
        for k in range(2, R+1):
            js = np.arange(k % 2, C+1, 2)
            left = js[js > 0]
            right = js[js < C]
            table[left, k] = np.maximum(table[left, k], table[left-1, k-1])
            table[right, k] = np.maximum(table[right, k], table[right+1, k-1])
        for j in range(C-2, -1, -2):
            table[j, R] = max(table[j, R], table[j+2, R])
        for j in range(C+1, C+R+1):
            ks = np.arange(1+(j+1) % 2, R+1, 2)
            ks = ks[ks > j-C]
            table[j, ks] = table[C, ks-j+C]
        return table

    def checkpoint(self, result, weights):
        return {'scope': 'Floating sparse-event master; physical weights require exact closure replay.',
                'n': self.n, 'event_nodes': [list(point) for point in self.nodes],
                'event_profile': result.x[:-1].tolist(), 'upper': float(-result.fun),
                'columns': [{'plan': c['plan']} for c in self.columns], 'weights': weights.tolist(),
                'projected_order': [list(edge) for edge in self.order]}


class PersistentSparseMaster:
    """Append charged nodes and exact order rows while retaining the LP basis.

    Old order edges stay sound when new nodes arrive; new cover edges complete
    the enlarged projected order.  The objective variable stays at column0.
    """
    def __init__(self, master, seconds=600):
        native = Path(__file__).resolve().parents[1]/'interval_clock_grid/normalized_native'
        sys.path.insert(0, str(native))
        from persistent_highs import PersistentLP, _check
        self.check = _check
        self.master = master
        self.sparse = SparseMaster(master.n, master.D)
        self.nodes, self.index, self.edges, self.calendar_rows = [], {}, set(), []
        self.columns = 0
        self.lp = PersistentLP([-1.], csr_matrix((0, 1)), [], [0.], [2.], seconds)
        _check(self.lp.highs.setOptionValue('solver', 'ipm'), 'initial sparse IPM')
        _check(self.lp.highs.setOptionValue('run_crossover', 'on'), 'sparse crossover')

    def solve(self, seconds):
        began = time.monotonic()
        if len(self.master.columns) < self.columns:
            raise ValueError('sparse master requires append-only calendars')
        columns = []
        for column in self.master.columns[self.columns:]:
            mass, coeff = plan_column(self.master.n, column['plan'])
            columns.append((mass, coeff))
        new_nodes = sorted({point for _, coeff in columns for point in coeff if point not in self.index})
        if new_nodes:
            count = len(new_nodes)
            self.check(self.lp.highs.addCols(count, np.zeros(count), np.zeros(count), np.ones(count),
                                            0, np.zeros(count+1, dtype=np.int32),
                                            np.zeros(0, dtype=np.int32), np.zeros(0)), 'append charged event variables')
            for point in new_nodes:
                self.index[point] = len(self.nodes)
                self.nodes.append(point)
            order = projected_order(self.master.n, self.nodes)
            new_edges = [edge for edge in order if edge not in self.edges]
        else:
            new_edges = []
        rr, cc, vv = [], [], []
        for row, (a, b) in enumerate(new_edges):
            rr.extend((row, row)); cc.extend((a+1, b+1)); vv.extend((1., -1.))
        rhs = [0.]*len(new_edges)
        first_row = self.lp.highs.getNumRow()
        for row, (mass, coeff) in enumerate(columns, len(new_edges)):
            rr.append(row); cc.append(0); vv.append(1.)
            for point, value in coeff.items():
                rr.append(row); cc.append(self.index[point]+1); vv.append(-value/(4*self.master.n))
            rhs.append(mass/(4*self.master.n))
            self.calendar_rows.append(first_row+row)
        matrix = coo_matrix((vv, (rr, cc)), shape=(len(rhs), len(self.nodes)+1)).tocsr()
        self.lp.add_rows(matrix, rhs)
        self.edges.update(new_edges)
        self.columns = len(self.master.columns)
        assembly = time.monotonic()-began
        self.lp.time_limit = float(seconds)
        result = self.lp.solve()
        self.check(self.lp.highs.setOptionValue('solver', 'simplex'), 'warm sparse simplex')
        weights = -result.ineqlin.marginals[np.asarray(self.calendar_rows, dtype=np.int64)]
        self.sparse.nodes = self.nodes
        table = self.sparse.extend_integer(result.x[1:])
        profile = self.master.profile_values(table)
        result.x = np.r_[profile, -result.fun]
        result.sparse_stats = dict(self.lp.last_stats, event_nodes=len(self.nodes),
                                   order_edges=len(self.edges), full_nodes=self.master.K,
                                   assembly_seconds=assembly, method='persistent projected Qout')
        return result, weights, profile


def solve_existing_master(master, seconds=600, method='persistent'):
    """Discovery adapter preserving existing route/calendar and checkpoint APIs.

    The returned full profile is an order extension.  Its rational repair
    does not inherit a lower guarantee from this finite calendar master.
    """
    if method == 'persistent':
        if not hasattr(master, '_persistent_sparse_master'):
            master._persistent_sparse_master = PersistentSparseMaster(master, seconds)
        return master._persistent_sparse_master.solve(seconds)
    sparse = SparseMaster(master.n, master.D)
    for column in master.columns:
        if not sparse.add_plan(column['plan']):
            raise ValueError('unexpected duplicate calendar under projection')
    result, weights = sparse.solve(seconds, method)
    events = result.x[:-1].copy()
    table = sparse.extend_integer(events)
    profile = master.profile_values(table)
    result.x = np.r_[profile, -result.fun]
    result.sparse_stats = {'event_nodes': len(sparse.nodes), 'order_edges': len(sparse.order),
                           'full_nodes': master.K, 'assembly_seconds': sparse.assembly_seconds,
                           'method': method}
    return result, weights, profile


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', type=Path)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--seconds', type=float, default=600)
    parser.add_argument('--method', choices=('highs-ipm', 'highs-ds'), default='highs-ipm')
    args = parser.parse_args()
    source = read_json(args.input)
    master = SparseMaster(source['n'])
    plans = source.get('paths') or [c['plan'] for c in source['columns']]
    for plan in plans:
        master.add_plan(plan)
    began = time.monotonic()
    result, weights = master.solve(args.seconds, args.method)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(master.checkpoint(result, weights), separators=(',', ':'))+'\n')
    print(json.dumps({'scope': 'Floating discovery estimate only', 'n': master.n,
                      'plans': len(master.columns), 'event_nodes': len(master.nodes),
                      'order_edges': len(master.order), 'assembly_seconds': master.assembly_seconds,
                      'restricted_master_upper': float(-result.fun), 'seconds': time.monotonic()-began}))


if __name__ == '__main__':
    main()
