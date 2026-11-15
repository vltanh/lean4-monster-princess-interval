#!/usr/bin/env python3
"""Exact pricing of a cache of known physical Monster paths.

This is a separation accelerator only. Its minimum is an UPPER bound on the
full-bank dual minimum, and must never be saved as a lower certificate. A
known violating path supplies a new running-record calendar; clearing this
cache still requires the exhaustive oracle.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from numbers import Integral
from typing import Iterable

import numpy as np

UINT64_MAX = (1 << 64) - 1


def _integer(value, name):
    if isinstance(value, bool) or not isinstance(value, Integral):
        raise ValueError(f"{name} must be an integer")
    return int(value)


def normalize_path(n: int, path: dict, *, source_n: int | None = None,
                   canonical_reflection: bool = True) -> dict:
    """Retain the prefix to the first endpoint or time 2, then its old tour.

    Input paths must visit the center by time 2 and both endpoints by time 8.
    Integer grid refinement is supported by repeating each old physical move.
    The returned path completes by time 6. Later negative positions are never
    suppressed by the optional initial reflection convention.
    """
    n = _integer(n, "n")
    if n < 1 or n > 10000:
        raise ValueError("n outside supported grid range")
    source_n = n if source_n is None else _integer(source_n, "source_n")
    if source_n < 1 or n % source_n:
        raise ValueError("physical refinement must be a positive integer")
    ratio, radius, cutoff = n // source_n, 2 * n, 4 * n
    start = _integer(path["start_grid"], "start_grid")
    if abs(start) > 2 * source_n or start % 2:
        raise ValueError("illegal physical start")
    start *= ratio
    moves = []
    for value in path["moves"]:
        step = _integer(value, "physical move")
        if step not in (-1, 1):
            raise ValueError("physical moves must be -1 or +1")
        moves.extend([step] * ratio)
    positions = [start]
    for step in moves:
        x = positions[-1] + step
        if abs(x) > radius:
            raise ValueError("physical route leaves the interval")
        positions.append(x)
    try:
        left, right, center = positions.index(-radius), positions.index(radius), positions.index(0)
    except ValueError as exc:
        raise ValueError("route must visit center and both endpoints") from exc
    if center > cutoff:
        raise ValueError("route misses the time-2 center deadline")
    if max(left, right) > 16 * n:
        raise ValueError("route misses the time-8 completion deadline")
    first = -radius if left < right else radius
    stop = min(left, right, cutoff)
    result = moves[:stop]
    x = positions[stop]
    for target in (first, -first):
        step = 1 if target > x else -1
        result.extend([step] * abs(target - x))
        x = target
    if len(result) > 12 * n:
        raise AssertionError("normalized tour exceeds time 6")
    if canonical_reflection and (start < 0 or start == 0 and result and result[0] < 0):
        start = -start
        result = [-step for step in result]
    return {"start_grid": start, "moves": result}


@dataclass(frozen=True)
class _Route:
    start: int
    moves: bytes                 # 0 means -1; 1 means +1
    left: int
    right: int


@dataclass
class _Batch:
    first: int
    absolute_positions: np.ndarray
    negative: np.ndarray
    left_active: np.ndarray
    right_active: np.ndarray
    times: np.ndarray


class CachedPathPricing:
    """Append-only physical-path cache, evaluated in vectorized exact chunks.

    Typical integration (the exhaustive oracle remains mandatory for a lower):

        cache = CachedPathPricing(master.n, master.D)
        cache.update_columns(master.columns)
        table = master.repair(trial)
        found = cache.price(table, keep=48, level=bundle_level)
        if found['violating_paths']:
            for route in found['violating_paths']:
                master.add(route, table)
        else:
            answer, table = master.price(trial, keep=48)
            cache.add_many(answer['paths'])

    All returned route costs are integers divided by 4*n*D. No floating point
    arithmetic enters a route price. Optional level/tolerance comparison is
    converted from decimal strings to exact Fractions.
    """

    def __init__(self, n: int, denominator: int, chunk_size: int = 64,
                 canonical_reflection: bool = True):
        self.n = _integer(n, "n")
        self.D = _integer(denominator, "denominator")
        self.chunk_size = _integer(chunk_size, "chunk_size")
        if not 1 <= self.n <= 10000 or self.D <= 0 or self.chunk_size < 1:
            raise ValueError("invalid cached-pricing parameters")
        # Each normalized route has at most 12*n ticks. At most two alive
        # clocks contribute at each tick, each at most 2*D, so uint64 sums
        # cannot wrap under this conservative bound.
        if 48 * self.n * self.D > UINT64_MAX:
            raise OverflowError("the conservative complete-route uint64 bound is exceeded")
        self.R = 2 * self.n
        self.scale = 4 * self.n * self.D
        self.canonical_reflection = bool(canonical_reflection)
        self._routes: list[_Route] = []
        self._seen: set[tuple[int, bytes]] = set()
        self._full_batches: list[_Batch] = []
        self._tail_batch: _Batch | None = None
        self._tail_count = -1
        self._column_source = None
        self._column_count = 0
        self._column_grid = None

    def __len__(self):
        return len(self._routes)

    def add(self, path: dict, *, source_n: int | None = None) -> bool:
        route = normalize_path(self.n, path, source_n=source_n,
                               canonical_reflection=self.canonical_reflection)
        packed = bytes((step + 1) // 2 for step in route["moves"])
        key = route["start_grid"], packed
        if key in self._seen:
            return False
        position, left, right, center = route["start_grid"], None, None, None
        for j in range(len(packed) + 1):
            if position == -self.R and left is None:
                left = j
            if position == self.R and right is None:
                right = j
            if position == 0 and center is None:
                center = j
            if j < len(packed):
                position += 2 * packed[j] - 1
        if left is None or right is None or center is None or center > 4 * self.n:
            raise AssertionError("normalization did not preserve a legal grid path")
        self._seen.add(key)
        self._routes.append(_Route(route["start_grid"], packed, left, right))
        return True

    def add_many(self, paths: Iterable[dict], *, source_n: int | None = None) -> int:
        return sum(self.add(path, source_n=source_n) for path in paths)

    def update_columns(self, columns: list[dict], *, source_n: int | None = None) -> int:
        """Read only newly appended master columns; deduplicate their paths."""
        if self._column_source is not columns or self._column_grid != source_n or len(columns) < self._column_count:
            self._column_source, self._column_grid, self._column_count = columns, source_n, 0
        added = self.add_many((column["plan"] for column in columns[self._column_count:]), source_n=source_n)
        self._column_count = len(columns)
        return added

    def _make_batch(self, first: int, end: int) -> _Batch:
        routes = self._routes[first:end]
        length = max(len(route.moves) for route in routes)
        dtype = np.int16 if self.R <= np.iinfo(np.int16).max else np.int32
        positions = np.zeros((len(routes), length), dtype=dtype)
        left = np.empty(len(routes), dtype=np.int32)
        right = np.empty(len(routes), dtype=np.int32)
        for row, route in enumerate(routes):
            positions[row, 0] = route.start
            if len(route.moves) > 1:
                steps = np.frombuffer(route.moves, dtype=np.uint8).astype(np.int32) * 2 - 1
                positions[row, 1:len(route.moves)] = route.start + np.cumsum(steps[:-1], dtype=np.int32)
            left[row], right[row] = route.left, route.right
        times = np.arange(length, dtype=np.int32)[None, :]
        return _Batch(first, np.abs(positions), positions < 0,
                      times < left[:, None], times < right[:, None], times)

    def _batches(self):
        full_count = len(self._routes) // self.chunk_size
        while len(self._full_batches) < full_count:
            first = len(self._full_batches) * self.chunk_size
            self._full_batches.append(self._make_batch(first, first + self.chunk_size))
        yield from self._full_batches
        first = full_count * self.chunk_size
        if first < len(self._routes):
            if self._tail_count != len(self._routes):
                self._tail_batch = self._make_batch(first, len(self._routes))
                self._tail_count = len(self._routes)
            yield self._tail_batch

    def _validate_table(self, table):
        table = np.asarray(table)
        if table.ndim != 2 or table.shape != (12 * self.n + 1, self.R + 1):
            raise ValueError("field must have shape (12*n+1, 2*n+1)")
        if table.dtype.kind not in "ui":
            raise ValueError("field values must have an integer dtype")
        if np.any(table[:, 0] != 0):
            raise ValueError("center field values must be zero")
        if table.dtype.kind == "i" and np.any(table < 0) or int(table.max()) > self.D:
            raise ValueError("field value outside [0,D]")
        return table.astype(np.uint64, copy=False)

    def price(self, table, keep: int = 48, *, level=None, tolerance="1e-7") -> dict:
        """Return exact cheapest cached witnesses, never a dual lower bound."""
        keep = _integer(keep, "keep")
        if keep < 0:
            raise ValueError("keep must be nonnegative")
        table = self._validate_table(table)
        costs = np.empty(len(self._routes), dtype=np.uint64)
        D = np.uint64(self.D)
        batch_count = 0
        for batch in self._batches():
            values = table[batch.times, batch.absolute_positions]
            charges = np.where(batch.negative, D - values, D + values)
            left = np.minimum.accumulate(charges, axis=1)
            right = np.minimum.accumulate(np.uint64(2 * self.D) - charges, axis=1)
            totals = np.where(batch.left_active, left, np.uint64(0)).sum(axis=1, dtype=np.uint64)
            totals += np.where(batch.right_active, right, np.uint64(0)).sum(axis=1, dtype=np.uint64)
            costs[batch.first:batch.first + len(totals)] = totals
            batch_count += 1
        chosen = np.argsort(costs, kind="stable")[:keep]
        paths = []
        for index in chosen:
            route = self._routes[int(index)]
            paths.append({"units": str(int(costs[index])), "start_grid": route.start,
                          "moves": [2 * step - 1 for step in route.moves]})
        result = {
            "status": "CACHED_WITNESSES",
            "scope": "Exact costs of known normalized physical paths only; an upper bound on the full-bank dual minimum, never a lower certificate.",
            "bound_direction": "upper", "certifies_lower": False,
            "n": self.n, "field_denominator": str(self.D),
            "objective_denominator": str(self.scale), "cached_paths": len(self._routes),
            "cached_minimum_units": str(int(costs.min())) if len(costs) else None,
            "chunk_size": self.chunk_size, "chunks": batch_count,
            "paths": paths,
        }
        if level is not None:
            level_q, tol_q = Fraction(str(level)), Fraction(str(tolerance))
            if tol_q < 0:
                raise ValueError("tolerance must be nonnegative")
            threshold = level_q - tol_q
            result["violating_paths"] = [route for route in paths if
                int(route["units"]) * threshold.denominator < threshold.numerator * self.scale]
            result["level"] = str(level_q)
            result["tolerance"] = str(tol_q)
        return result


__all__ = ["CachedPathPricing", "normalize_path"]
