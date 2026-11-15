#!/usr/bin/env python3
"""Independent exact replay of a characteristic-mesh exit potential.

Only the Python standard library is used. Geometry, affine interpolation,
line integrals, polytope intersections, and quadratic/cubic polarization are
computed directly with Fraction. No floating LP rows or claimed coefficient
lattice are imported or reconstructed.
"""

import argparse
from collections import Counter
from fractions import Fraction as Q
from functools import lru_cache
import hashlib
from itertools import combinations, combinations_with_replacement, product
import json
from pathlib import Path


def dot(a, b):
    return sum((x * y for x, y in zip(a, b)), Q(0))


def average(*points):
    return tuple(sum(values, Q(0)) / len(points) for values in zip(*points))


@lru_cache(None)
def inverse(matrix):
    size = len(matrix)
    work = [
        list(row) + [Q(i == j) for j in range(size)]
        for i, row in enumerate(matrix)
    ]
    for col in range(size):
        pivot = next(
            (row for row in range(col, size) if work[row][col]), None
        )
        if pivot is None:
            return None
        work[col], work[pivot] = work[pivot], work[col]
        scale = work[col][col]
        work[col] = [x / scale for x in work[col]]
        for row in range(size):
            if row == col or not work[row][col]:
                continue
            scale = work[row][col]
            work[row] = [
                x - scale * y for x, y in zip(work[row], work[col])
            ]
    return tuple(tuple(row[size:]) for row in work)


def polytope_vertices(constraints):
    """All vertices of a bounded rational polytope in dimension two or three."""
    dimension = len(constraints[0][0])
    points = set()
    for active in combinations(range(len(constraints)), dimension):
        matrix = tuple(constraints[i][0] for i in active)
        inv = inverse(matrix)
        if inv is None:
            continue
        rhs = tuple(constraints[i][1] for i in active)
        point = tuple(dot(row, rhs) for row in inv)
        if all(dot(normal, point) <= bound
               for normal, bound in constraints):
            points.add(point)
    return tuple(sorted(points))


def box_constraints(lower, upper):
    dimension = len(lower)
    rows = []
    for i in range(dimension):
        unit = tuple(Q(j == i) for j in range(dimension))
        rows.append((unit, upper[i]))
        rows.append((tuple(-x for x in unit), -lower[i]))
    return rows


class Checks:
    def __init__(self):
        self.counts = Counter()
        self.minimum = {}

    def check(self, kind, margin, context=None):
        assert isinstance(margin, (Q, int)), ("non-rational arithmetic", kind, margin)
        margin = Q(margin)
        self.counts[kind] += 1
        self.minimum[kind] = min(self.minimum.get(kind, margin), margin)
        if margin < 0:
            raise AssertionError({
                "kind": kind, "margin": str(margin), "context": context,
            })


class ExactMesh:
    def __init__(self, step, horizon):
        self.step = step
        self.last = horizon + 2
        assert (1 / step).denominator == 1
        assert (horizon / step).denominator == 1
        lower = int(-1 / step)
        upper = int((self.last + 1) / step)

        def allowed(i, j):
            u, v = i * step, j * step
            return 0 <= u + v <= 2 * self.last and -2 <= u - v <= 2

        grid = {
            (i, j)
            for i in range(lower, upper + 1)
            for j in range(lower, upper + 1)
            if allowed(i, j)
        }
        ordered = sorted(grid, key=lambda p: (p[0] + p[1], p[0] - p[1]))
        lookup = {point: i for i, point in enumerate(ordered)}
        self.vertices = tuple(
            ((i + j) * step / 2, (i - j) * step / 2) for i, j in ordered
        )
        self.reflection = tuple(lookup[j, i] for i, j in ordered)
        triangles = []
        for i in range(lower, upper):
            for j in range(lower, upper):
                corners = [(i, j), (i + 1, j), (i, j + 1), (i + 1, j + 1)]
                inside = [point for point in corners if point in grid]
                if len(inside) < 3:
                    continue
                if len(inside) == 3:
                    local = [inside]
                elif i == j:
                    local = [
                        [corners[0], corners[1], corners[3]],
                        [corners[0], corners[2], corners[3]],
                    ]
                else:
                    local = [
                        [corners[0], corners[1], corners[2]],
                        [corners[1], corners[2], corners[3]],
                    ]
                triangles.extend(tuple(lookup[p] for p in tri) for tri in local)
        self.triangles = tuple(triangles)
        self.inverses = tuple(
            inverse(tuple((Q(1), *self.vertices[v]) for v in tri))
            for tri in self.triangles
        )
        assert all(inv is not None for inv in self.inverses)
        self.potential_vertices = tuple(
            i for i, (t, _) in enumerate(self.vertices) if t <= horizon
        )
        assert self.potential_vertices == tuple(range(len(self.potential_vertices)))
        self.potential_triangles = tuple(
            i for i, tri in enumerate(self.triangles)
            if all(self.vertices[v][0] <= horizon for v in tri)
        )
        triangle_sets = {frozenset(tri) for tri in self.triangles}
        assert all(
            frozenset(self.reflection[v] for v in tri) in triangle_sets
            for tri in self.triangles
        )
        assert not any(
            min(self.vertices[v][0] for v in tri) < horizon
            < max(self.vertices[v][0] for v in tri)
            for tri in self.triangles
        )
        # Verify the mesh covers the physical rectangle exactly by area.
        total_area = Q(0)
        potential_area = Q(0)
        for k, tri in enumerate(self.triangles):
            p, q, r = (self.vertices[v] for v in tri)
            area = abs(
                (q[0] - p[0]) * (r[1] - p[1])
                - (q[1] - p[1]) * (r[0] - p[0])
            ) / 2
            total_area += area
            if k in self.potential_triangles:
                potential_area += area
        assert total_area == 2 * self.last
        assert potential_area == 2 * horizon

    def barycentric(self, triangle, t, x):
        inv = self.inverses[triangle]
        return tuple(
            inv[0][j] + t * inv[1][j] + x * inv[2][j]
            for j in range(3)
        )


class ExactReplay:
    def __init__(self, data):
        assert data.get("mesh_kind") == "light"
        assert data.get("center_aligned") is True
        self.horizon = Q(str(data.get("absorption_horizon", 3)))
        self.queues = tuple(Q(str(q)) for q in data["queue_knots"])
        assert self.queues[0] == 0 and self.queues[-1] == 4
        assert all(a < b for a, b in zip(self.queues, self.queues[1:]))
        self.nq = len(self.queues)
        self.mesh = ExactMesh(Q(str(data["step"])), self.horizon)
        count = len(self.mesh.potential_vertices) * self.nq**2
        values = tuple(Q(value) for value in data["coefficients"])
        assert len(values) == count + len(self.mesh.vertices) + 1
        self.w = values[:count]
        self.field = values[count:-1]
        self.lower = values[-1]
        assert self.lower == Q(data["lower"])
        self.checks = Checks()
        self.polytopes = Counter()
        self.field_coefficients = tuple(
            tuple(
                sum((inv[row][j] * self.field[v]
                     for j, v in enumerate(tri)), Q(0))
                for row in range(3)
            )
            for tri, inv in zip(self.mesh.triangles, self.mesh.inverses)
        )
        self.build_tail_partition()

    def value(self, vertex, plus, minus):
        return self.w[(vertex * self.nq + plus) * self.nq + minus]

    def build_tail_partition(self):
        knots = sorted({
            t + x for t, x in self.mesh.vertices
            if -1 <= t + x <= self.horizon + 1
        })
        self.bands = []
        self.charts = []
        for left, right in zip(knots, knots[1:]):
            middle = (left + right) / 2
            segments = []
            for k, tri in enumerate(self.mesh.triangles):
                points = [
                    (self.mesh.vertices[v][0] + self.mesh.vertices[v][1],
                     self.mesh.vertices[v][0])
                    for v in tri
                ]
                if not min(a for a, _ in points) < middle < max(a for a, _ in points):
                    continue
                crossings = []
                for i, j in combinations(range(3), 2):
                    a0, v0 = points[i]
                    a1, v1 = points[j]
                    if min(a0, a1) < middle < max(a0, a1):
                        slope = (v1 - v0) / (a1 - a0)
                        crossings.append((slope, v0 - slope * a0))
                assert len(crossings) == 2
                crossings.sort(key=lambda line: line[0] * middle + line[1])
                lo, hi = crossings
                segments.append((lo, hi, k))
            segments.sort(key=lambda item: item[0][0] * middle + item[0][1])
            assert segments
            assert segments[0][0][0] * middle + segments[0][0][1] == max(0, middle - 1)
            assert segments[-1][1][0] * middle + segments[-1][1][1] == middle + 1
            for previous, following in zip(segments, segments[1:]):
                assert previous[1] == following[0]
            for lo, hi, _ in segments:
                assert all(lo[0] * a + lo[1] <= hi[0] * a + hi[1]
                           for a in (left, right))
                self.charts.append((left, right, lo, hi))
            self.charts.append((
                left, right, (Q(1), Q(1)),
                (Q(0), self.horizon + 4),
            ))
            self.bands.append((left, right, tuple(segments)))

    @lru_cache(None)
    def tail(self, a, b):
        """Direct exact integral; no chart polynomial coefficients are trusted."""
        if b >= a + 1:
            return Q(0)
        assert -1 <= a <= self.horizon + 1
        assert max(0, a - 1) <= b
        band = next(segments for left, right, segments in self.bands
                    if left <= a <= right)
        result = Q(0)
        integrated_length = Q(0)
        for lower, upper, triangle in band:
            lo = max(b, lower[0] * a + lower[1])
            hi = upper[0] * a + upper[1]
            if hi <= lo:
                continue
            constant, ft, fx = self.field_coefficients[triangle]
            # Along (physical time,position)=(v,a-v), F=A+fx*a+(ft-fx)*v.
            result += (constant + fx * a) * (hi - lo)
            result += (ft - fx) * (hi * hi - lo * lo) / 2
            integrated_length += hi - lo
        assert integrated_length == a + 1 - b
        assert 0 <= result <= integrated_length
        return result

    def intersections(self, constraints, base_vertices, avec, aoffset, bvec, boffset):
        mapped = [
            (dot(avec, point) + aoffset, dot(bvec, point) + boffset)
            for point in base_vertices
        ]
        for left, right, (pl, rl), (pu, ru) in self.charts:
            if max(a for a, _ in mapped) < left or min(a for a, _ in mapped) > right:
                continue
            if max(b - pl * a for a, b in mapped) < rl:
                continue
            if min(b - pu * a for a, b in mapped) > ru:
                continue
            rows = list(constraints) + [
                (tuple(-v for v in avec), aoffset - left),
                (tuple(avec), right - aoffset),
                (tuple(pl * a - b for a, b in zip(avec, bvec)),
                 boffset - pl * aoffset - rl),
                (tuple(b - pu * a for a, b in zip(avec, bvec)),
                 pu * aoffset + ru - boffset),
            ]
            vertices = polytope_vertices(rows)
            if vertices:
                yield vertices

    def quadratic_guard(self, vertices, potential, avec, aoffset, bvec, boffset, kind):
        @lru_cache(None)
        def difference(point):
            return self.tail(
                dot(avec, point) + aoffset,
                dot(bvec, point) + boffset,
            ) - potential(point)
        values = tuple(difference(point) for point in vertices)
        for i, j in combinations_with_replacement(range(len(vertices)), 2):
            polar = 2 * difference(average(vertices[i], vertices[j]))
            polar -= (values[i] + values[j]) / 2
            self.checks.check(kind, polar, (vertices[i], vertices[j]))
        self.polytopes[kind] += 1

    def field_and_controls(self):
        for v, field in enumerate(self.field):
            self.checks.check("cdf_range", field)
            self.checks.check("cdf_range", 1 - field)
            assert field + self.field[self.mesh.reflection[v]] == 1
            if self.mesh.vertices[v][0] >= self.horizon:
                assert field == Q(1, 2)
        for _, ft, fx in self.field_coefficients:
            self.checks.check("cdf_transport", fx - ft)
            self.checks.check("cdf_transport", fx + ft)
        for triangle in self.mesh.potential_triangles:
            tri = self.mesh.triangles[triangle]
            inv = self.mesh.inverses[triangle]
            for p in range(self.nq - 1):
                hp = self.queues[p + 1] - self.queues[p]
                for m in range(self.nq - 1):
                    hm = self.queues[m + 1] - self.queues[m]
                    for v in tri:
                        for pp, mm in product((p, p + 1), (m, m + 1)):
                            wt = sum((inv[1][j] * self.value(vertex, pp, mm)
                                      for j, vertex in enumerate(tri)), Q(0))
                            wx = sum((inv[2][j] * self.value(vertex, pp, mm)
                                      for j, vertex in enumerate(tri)), Q(0))
                            wp = (self.value(v, p + 1, mm) - self.value(v, p, mm)) / hp
                            wm = (self.value(v, pp, m + 1) - self.value(v, pp, m)) / hm
                            for direction in (-1, 1):
                                self.checks.check("move", wt + direction * wx - wp - wm,
                                                  (triangle, p, m, v, pp, mm, direction))
                        for mm in (m, m + 1):
                            wp = (self.value(v, p + 1, mm) - self.value(v, p, mm)) / hp
                            self.checks.check("charge", wp + self.field[self.mesh.reflection[v]])
                        for pp in (p, p + 1):
                            wm = (self.value(v, pp, m + 1) - self.value(v, pp, m)) / hm
                            self.checks.check("charge", wm + self.field[v])
        for v in self.mesh.potential_vertices:
            if self.mesh.vertices[v][0] == 0:
                self.checks.check("initial", self.value(v, 0, 0) - self.lower)
        self.checks.check("lower_range", self.lower)
        self.checks.check("lower_range", Q(3, 2) - self.lower)

    def endpoint_guards(self):
        for plus in (True, False):
            position = Q(1 if plus else -1)
            edge = sorted(
                (self.mesh.vertices[v][0], v) for v in self.mesh.potential_vertices
                if self.mesh.vertices[v][1] == position
            )
            for (t0, v0), (t1, v1) in zip(edge, edge[1:]):
                for cell in range(self.nq - 1):
                    q0, q1 = self.queues[cell:cell + 2]
                    constraints = box_constraints((t0, q0), (t1, q1))
                    base = tuple(product((t0, t1), (q0, q1)))
                    pieces = tuple(self.intersections(
                        constraints, base, (Q(1), Q(0)), Q(1),
                        (Q(1), Q(1)), Q(0),
                    ))
                    for own in range(self.nq):
                        def potential(point):
                            t, q = point
                            rt, rq = (t - t0) / (t1 - t0), (q - q0) / (q1 - q0)
                            result = Q(0)
                            for v, wt in ((v0, 1 - rt), (v1, rt)):
                                for other, wq in ((cell, 1 - rq), (cell + 1, rq)):
                                    result += wt * wq * (
                                        self.value(v, own, other) if plus
                                        else self.value(v, other, own)
                                    )
                            return result
                        for vertices in pieces:
                            self.quadratic_guard(
                                vertices, potential, (Q(1), Q(0)), Q(1),
                                (Q(1), Q(1)), Q(0), "endpoint_boundary",
                            )

    def queue_guards(self):
        for plus in (True, False):
            for triangle in self.mesh.potential_triangles:
                tri = self.mesh.triangles[triangle]
                inv = self.mesh.inverses[triangle]
                for cell in range(self.nq - 1):
                    q0, q1 = self.queues[cell:cell + 2]
                    constraints = [
                        ((-inv[1][j], -inv[2][j], Q(0)), inv[0][j])
                        for j in range(3)
                    ]
                    constraints += [
                        ((Q(0), Q(0), Q(-1)), -q0),
                        ((Q(0), Q(0), Q(1)), q1),
                    ]
                    base = tuple(
                        (*self.mesh.vertices[v], q) for v in tri for q in (q0, q1)
                    )
                    avec = (Q(1), Q(1 if plus else -1), Q(0))
                    bvec = (Q(1), Q(0), Q(1))

                    def potential(point):
                        t, x, q = point
                        bary = self.mesh.barycentric(triangle, t, x)
                        fraction = (q - q0) / (q1 - q0)
                        result = Q(0)
                        for vertex, weight in zip(tri, bary):
                            for other, wq in ((cell, 1 - fraction), (cell + 1, fraction)):
                                result += weight * wq * (
                                    self.value(vertex, self.nq - 1, other) if plus
                                    else self.value(vertex, other, self.nq - 1)
                                )
                        return result
                    for vertices in self.intersections(
                            constraints, base, avec, Q(0), bvec, Q(0)):
                        self.quadratic_guard(
                            vertices, potential, avec, Q(0), bvec, Q(0),
                            "queue_boundary",
                        )

    def time_guards(self):
        nodes = sorted(
            (self.mesh.vertices[v][1], v) for v in self.mesh.potential_vertices
            if self.mesh.vertices[v][0] == self.horizon
        )
        for (x0, v0), (x1, v1) in zip(nodes, nodes[1:]):
            for p in range(self.nq - 1):
                p0, p1 = self.queues[p:p + 2]
                for m in range(self.nq - 1):
                    m0, m1 = self.queues[m:m + 2]
                    base_constraints = box_constraints((x0, p0, m0), (x1, p1, m1))

                    @lru_cache(None)
                    def potential(point):
                        x, qp, qm = point
                        rx, rp, rm = (x - x0) / (x1 - x0), (qp - p0) / (p1 - p0), (qm - m0) / (m1 - m0)
                        return sum((
                            wx * wp * wm * self.value(v, pp, mm)
                            for (v, wx), (pp, wp), (mm, wm) in product(
                                ((v0, 1 - rx), (v1, rx)),
                                ((p, 1 - rp), (p + 1, rp)),
                                ((m, 1 - rm), (m + 1, rm)),
                            )
                        ), Q(0))

                    for first_plus in (True, False):
                        cp, xp = (Q(1), Q(-1)) if first_plus else (Q(3), Q(1))
                        cm, xm = (Q(3), Q(-1)) if first_plus else (Q(1), Q(1))
                        vp, vm = (xp, Q(-1), Q(0)), (xm, Q(0), Q(-1))

                        @lru_cache(None)
                        def difference(point):
                            cost = (max(Q(0), cp + dot(vp, point))
                                    + max(Q(0), cm + dot(vm, point))) / 2
                            return cost - potential(point)

                        for active_p, active_m in product((False, True), repeat=2):
                            sp, sm = Q(1 if active_p else -1), Q(1 if active_m else -1)
                            constraints = list(base_constraints) + [
                                (tuple(-sp * x for x in vp), sp * cp),
                                (tuple(-sm * x for x in vm), sm * cm),
                            ]
                            vertices = polytope_vertices(constraints)
                            if not vertices:
                                continue
                            values = tuple(difference(point) for point in vertices)
                            for i, j, k in combinations_with_replacement(range(len(vertices)), 3):
                                u, v, w = vertices[i], vertices[j], vertices[k]
                                polar = Q(9, 2) * difference(average(u, v, w))
                                polar -= Q(4, 3) * sum((
                                    difference(average(u, v)), difference(average(u, w)),
                                    difference(average(v, w)),
                                ), Q(0))
                                polar += (values[i] + values[j] + values[k]) / 6
                                self.checks.check("time_boundary", polar, (u, v, w, first_plus))
                            self.polytopes["time_boundary"] += 1

    def run(self):
        self.field_and_controls()
        print("Exact CDF, control, and initial checks passed.", flush=True)
        self.endpoint_guards()
        print("Exact endpoint integral/polar checks passed.", flush=True)
        self.queue_guards()
        print("Exact queue-cap integral/polar checks passed.", flush=True)
        self.time_guards()
        print("Exact terminal-tour cubic-polar checks passed.", flush=True)
        return {
            "status": "PASS",
            "lower": str(self.lower),
            "absorption_horizon": str(self.horizon),
            "physical_completion_horizon": str(self.horizon + 4),
            "field_vertices": len(self.mesh.vertices),
            "potential_vertices": len(self.mesh.potential_vertices),
            "field_triangles": len(self.mesh.triangles),
            "queue_knots": list(map(str, self.queues)),
            "analytic_checks_by_kind": dict(self.checks.counts),
            "minimum_margin_by_kind": {k: str(v) for k, v in self.checks.minimum.items()},
            "boundary_polytopes": dict(self.polytopes),
            "distinct_exact_tail_integrals": self.tail.cache_info().currsize,
            "arithmetic": "Python Fraction only; direct exact geometry and line integrals",
            "scope": "Global lower certificate, not an improvement on the archived best lower bound.",
        }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("certificate", type=Path)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    raw = args.certificate.read_bytes()
    result = ExactReplay(json.loads(raw)).run()
    result["certificate_sha256"] = hashlib.sha256(raw).hexdigest()
    encoded = json.dumps(result, indent=2) + "\n"
    if args.report:
        args.report.write_text(encoded)
    print(encoded, end="")


if __name__ == "__main__":
    main()
