"""Global finite-label maximization with supermodular pair rewards.

This is an exact finite optimizer when supplied Fraction capacities.  It is
not a discretization-error bound or a continuous princess-response theorem.
Labels for variable i are 0,...,len(unaries[i])-1.  A pair (i,j,table)
must have nonnegative adjacent mixed differences.  An implication
(i,k,j,l) imposes [label_i >= k] => [label_j >= l].
"""

from collections import deque
from dataclasses import dataclass
from itertools import product
from fractions import Fraction
import random
import sys


class _Edge:
    __slots__ = ("to", "rev", "cap")

    def __init__(self, to, rev, cap):
        self.to, self.rev, self.cap = to, rev, cap


class _Flow:
    def __init__(self, n, tolerance=0):
        self.graph = [[] for _ in range(n)]
        self.tolerance = tolerance
        self.original = []

    def add(self, u, v, capacity):
        if capacity < 0:
            raise ValueError("Negative capacity")
        if not capacity:
            return
        a = _Edge(v, len(self.graph[v]), capacity)
        b = _Edge(u, len(self.graph[u]), 0)
        self.graph[u].append(a)
        self.graph[v].append(b)
        self.original.append((u, a, capacity))

    def solve(self, source, sink, bound):
        old_limit = sys.getrecursionlimit()
        sys.setrecursionlimit(max(old_limit, 2 * len(self.graph) + 100))
        result = 0
        try:
            while True:
                level = [-1] * len(self.graph)
                level[source] = 0
                queue = deque([source])
                while queue:
                    u = queue.popleft()
                    for e in self.graph[u]:
                        if e.cap > self.tolerance and level[e.to] < 0:
                            level[e.to] = level[u] + 1
                            queue.append(e.to)
                if level[sink] < 0:
                    break
                pointer = [0] * len(self.graph)

                def augment(u, amount):
                    if u == sink:
                        return amount
                    while pointer[u] < len(self.graph[u]):
                        e = self.graph[u][pointer[u]]
                        if e.cap > self.tolerance and level[e.to] == level[u] + 1:
                            pushed = augment(e.to, min(amount, e.cap))
                            if pushed > self.tolerance:
                                e.cap -= pushed
                                self.graph[e.to][e.rev].cap += pushed
                                return pushed
                        pointer[u] += 1
                    return 0

                while True:
                    pushed = augment(source, bound)
                    if pushed <= self.tolerance:
                        break
                    result += pushed
        finally:
            sys.setrecursionlimit(old_limit)
        reachable = {source}
        queue = deque([source])
        while queue:
            u = queue.popleft()
            for e in self.graph[u]:
                if e.cap > self.tolerance and e.to not in reachable:
                    reachable.add(e.to)
                    queue.append(e.to)
        # Independently check the finite dual certificate: feasible flow,
        # conservation, and a cut with exactly the same capacity.
        balance = [0] * len(self.graph)
        cut_capacity = 0
        allowed_error = self.tolerance * max(1, len(self.original))
        for u, edge, capacity in self.original:
            sent = capacity - edge.cap
            if not -allowed_error <= sent <= capacity + allowed_error:
                raise AssertionError("Infeasible flow capacity")
            balance[u] += sent
            balance[edge.to] -= sent
            if u in reachable and edge.to not in reachable:
                cut_capacity += capacity
        if any(abs(balance[u]) > allowed_error for u in range(len(balance))
               if u not in (source, sink)):
            raise AssertionError("Flow conservation failed")
        if max(abs(balance[source] - result), abs(balance[sink] + result),
               abs(cut_capacity - result)) > allowed_error:
            raise AssertionError("Flow/cut dual certificate failed")
        return result, reachable


@dataclass(frozen=True)
class CutResult:
    labels: tuple
    score: object
    cut_score: object
    threshold_nodes: int


def maximize(unaries, pairs=(), implications=(), bounds=None, tolerance=0):
    """Maximize all unary and pair rewards over the entire finite feasible set."""
    unaries = [list(row) for row in unaries]
    pairs = list(pairs)
    implications = list(implications)
    if any(not row for row in unaries):
        raise ValueError("Every variable needs at least one label")
    nodes = {}
    for i, row in enumerate(unaries):
        for k in range(1, len(row)):
            nodes[i, k] = len(nodes)
    linear = [0] * len(nodes)
    constant = sum(row[0] for row in unaries)
    arcs = []
    for i, row in enumerate(unaries):
        for k in range(1, len(row)):
            linear[nodes[i, k]] += row[k] - row[k - 1]
    for i, j, table in pairs:
        if i == j:
            raise ValueError("Pair variables must be distinct")
        if len(table) != len(unaries[i]) or any(len(row) != len(unaries[j]) for row in table):
            raise ValueError("Pair table has incorrect shape")
        constant += table[0][0]
        for k in range(1, len(table)):
            linear[nodes[i, k]] += table[k][0] - table[k - 1][0]
        for l in range(1, len(table[0])):
            linear[nodes[j, l]] += table[0][l] - table[0][l - 1]
        for k in range(1, len(table)):
            for l in range(1, len(table[0])):
                mixed = table[k][l] - table[k - 1][l] - table[k][l - 1] + table[k - 1][l - 1]
                if mixed < -tolerance:
                    raise ValueError("Pair reward is not supermodular")
                if mixed <= tolerance:
                    continue
                # mixed*b_i*b_j = mixed*b_i - mixed*b_i*(1-b_j).
                linear[nodes[i, k]] += mixed
                arcs.append((nodes[i, k], nodes[j, l], mixed))
    source, sink = len(nodes), len(nodes) + 1
    graph = _Flow(len(nodes) + 2, tolerance=tolerance)
    finite_bound = 1 + sum(abs(c) for c in linear) + sum(c for _, _, c in arcs)
    for u, v, capacity in arcs:
        graph.add(u, v, capacity)
    upper = constant
    for node, coefficient in enumerate(linear):
        if coefficient >= 0:
            graph.add(source, node, coefficient)
            upper += coefficient
        else:
            graph.add(node, sink, -coefficient)
    # Each label is represented by a prefix of true threshold bits.
    for i, row in enumerate(unaries):
        for k in range(2, len(row)):
            graph.add(nodes[i, k], nodes[i, k - 1], finite_bound)
    for i, k, j, l in implications:
        if (i, k) not in nodes or (j, l) not in nodes:
            raise ValueError("Implications require actual nonzero thresholds")
        graph.add(nodes[i, k], nodes[j, l], finite_bound)
    if bounds is None:
        bounds = [(0, len(row) - 1) for row in unaries]
    if len(bounds) != len(unaries):
        raise ValueError("Wrong number of bounds")
    for i, (lo, hi) in enumerate(bounds):
        if not 0 <= lo <= hi < len(unaries[i]):
            raise ValueError("Invalid label bounds")
        if lo:
            graph.add(source, nodes[i, lo], finite_bound)
        if hi + 1 < len(unaries[i]):
            graph.add(nodes[i, hi + 1], sink, finite_bound)
    flow, reachable = graph.solve(source, sink, finite_bound)
    for i, row in enumerate(unaries):
        if any(nodes[i, k] in reachable and nodes[i, k - 1] not in reachable
               for k in range(2, len(row))):
            raise ValueError("Infeasible hard constraints")
    labels = tuple(sum(nodes[i, k] in reachable for k in range(1, len(row)))
                   for i, row in enumerate(unaries))
    if not all(lo <= labels[i] <= hi for i, (lo, hi) in enumerate(bounds)):
        raise ValueError("Infeasible hard constraints")
    if any(labels[i] >= k and labels[j] < l for i, k, j, l in implications):
        raise ValueError("Infeasible hard constraints")
    score = sum(row[labels[i]] for i, row in enumerate(unaries))
    score += sum(table[labels[i]][labels[j]] for i, j, table in pairs)
    cut_score = upper - flow
    if abs(score - cut_score) > tolerance * max(1, len(nodes) + len(arcs)):
        raise AssertionError(("Cut/value mismatch", score, cut_score))
    return CutResult(labels, score, cut_score, len(nodes))


def chain_implications(variables, label_count, increasing=True):
    """Enforce index order for variables sharing the same label levels."""
    result = []
    for a, b in zip(variables, variables[1:]):
        if not increasing:
            a, b = b, a
        result.extend((a, k, b, k) for k in range(1, label_count))
    return result


def _self_check():
    rng = random.Random(1072)
    checked = examined = 0
    for n in (2, 4, 6):
        for count in (2, 3, 4):
            for trial in range(10):
                unary = [[Fraction(rng.randrange(-12, 13), 7) for _ in range(count)]
                         for _ in range(n)]
                pairs = []
                for i in range(n // 2):
                    # Actual endpoint-type reward: -W*C(P), with C decreasing.
                    increments = [Fraction(rng.randrange(0, 7), 17) for _ in range(count)]
                    cdf_tail = [sum(increments[k:]) for k in range(count)]
                    w = [Fraction(k - count, 5) for k in range(count)]
                    table = [[-ww * cc for ww in w] for cc in cdf_tail]
                    pairs.append((i, i + n // 2, table))
                implications = chain_implications(range(n // 2), count)
                implications += chain_implications(range(n // 2, n), count, increasing=False)
                bounds = [(0, count - 1) for _ in range(n)]
                if trial % 2:
                    bounds[0] = (0, count - 2)
                    bounds[-1] = (1, count - 1)
                expected = None
                for labels in product(range(count), repeat=n):
                    if not all(lo <= labels[i] <= hi for i, (lo, hi) in enumerate(bounds)):
                        continue
                    if any(labels[i] >= k and labels[j] < l for i, k, j, l in implications):
                        continue
                    examined += 1
                    score = sum(row[labels[i]] for i, row in enumerate(unary))
                    score += sum(t[labels[i]][labels[j]] for i, j, t in pairs)
                    expected = score if expected is None else max(expected, score)
                got = maximize(unary, pairs, implications, bounds)
                assert got.score == expected, (n, count, trial, got, expected)
                checked += 1
    try:
        maximize([[0, 0], [0, 0]], [(0, 1, [[0, 0], [0, -1]])])
    except ValueError:
        checked += 1
    else:
        raise AssertionError("Failed to reject a submodular reward")
    try:
        maximize([[0, 0], [0, 0]], implications=[(0, 1, 1, 1)], bounds=[(1, 1), (0, 0)])
    except ValueError:
        checked += 1
    else:
        raise AssertionError("Failed to reject contradictory hard constraints")
    print(f"PASS: {checked} exact global finite-cut comparisons/rejections; {examined} exhaustive feasible assignments")
    print("Scope: finite supermodular/control-order optimizer; no continuous-response claim")


if __name__ == "__main__":
    _self_check()
