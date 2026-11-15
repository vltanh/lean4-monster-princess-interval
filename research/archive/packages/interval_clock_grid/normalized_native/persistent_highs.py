#!/usr/bin/env python3
"""Persistent HiGHS backend for solve_normalized.Master.

This module changes only floating discovery. Exact integer pricing remains
the certificate gate. Construct PersistentMaster(master) once and call its
solve_lp(anchor, level_lower) in place of master.solve_lp.

The available SciPy distribution exposes the HiGHS native binding at
scipy.optimize._highspy._core. HiGHS keeps its internal basis across model
modifications; addRows appends newly discovered calendar inequalities.
The L1 level model is separate and persistent. Fixed auxiliary anchor
columns make every anchor/level update one changeColsBounds call.
"""
from __future__ import annotations

import time
import numpy as np
from scipy.optimize import OptimizeResult
from scipy.optimize._highspy import _core as highs
from scipy.sparse import coo_matrix, csr_matrix, hstack, vstack


def _check(status, action):
    if status == highs.HighsStatus.kError:
        raise RuntimeError("HiGHS " + action + " failed")


class SolveError(RuntimeError):
    """A correctly constructed model did not finish with an optimum."""


class PersistentLP:
    def __init__(self, objective, matrix, rhs, lower, upper, time_limit=120.):
        self.highs = highs._Highs()
        self.time_limit = float(time_limit)
        if not self.time_limit > 0:
            raise ValueError('time limit must be positive')
        for name, value in (
            ("output_flag", False), ("solver", "simplex"),
            ("simplex_strategy", 1), ("parallel", "off"),
            ("time_limit", float(time_limit)),
            ("primal_feasibility_tolerance", 1e-9),
            ("dual_feasibility_tolerance", 1e-9),
        ):
            _check(self.highs.setOptionValue(name, value), "set option " + name)
        matrix = csr_matrix(matrix, dtype=np.float64)
        matrix.sum_duplicates()
        matrix.sort_indices()
        lp = highs.HighsLp()
        lp.num_col_, lp.num_row_ = matrix.shape[1], matrix.shape[0]
        lp.col_cost_ = np.asarray(objective, dtype=np.float64)
        lp.col_lower_ = np.asarray(lower, dtype=np.float64)
        lp.col_upper_ = np.asarray(upper, dtype=np.float64)
        lp.row_lower_ = np.full(matrix.shape[0], -np.inf)
        lp.row_upper_ = np.asarray(rhs, dtype=np.float64)
        sparse = highs.HighsSparseMatrix()
        sparse.num_col_, sparse.num_row_ = matrix.shape[1], matrix.shape[0]
        sparse.format_ = highs.MatrixFormat.kRowwise
        sparse.start_ = np.asarray(matrix.indptr, dtype=np.int32)
        sparse.index_ = np.asarray(matrix.indices, dtype=np.int32)
        sparse.value_ = np.asarray(matrix.data, dtype=np.float64)
        lp.a_matrix_ = sparse
        _check(self.highs.passModel(lp), "pass initial model")
        self.rhs = np.asarray(rhs, dtype=np.float64).copy()
        self.calls = 0
        self.last_stats = {}

    def add_rows(self, matrix, rhs):
        matrix = csr_matrix(matrix, dtype=np.float64)
        if not matrix.shape[0]:
            return
        matrix.sum_duplicates()
        matrix.sort_indices()
        rhs = np.asarray(rhs, dtype=np.float64)
        _check(self.highs.addRows(
            matrix.shape[0], np.full(matrix.shape[0], -np.inf), rhs,
            matrix.nnz, np.asarray(matrix.indptr, dtype=np.int32),
            np.asarray(matrix.indices, dtype=np.int32),
            np.asarray(matrix.data, dtype=np.float64)), "append rows")
        self.rhs = np.r_[self.rhs, rhs]

    def fix_columns(self, indices, values):
        indices = np.asarray(indices, dtype=np.int32)
        values = np.asarray(values, dtype=np.float64)
        _check(self.highs.changeColsBounds(len(indices), indices, values, values),
               "update fixed columns")

    def solve(self):
        basis_before = self.highs.getBasis().valid
        # A persistent HiGHS model accumulates its run clock across run()
        # calls. Its time_limit is compared with that cumulative clock.
        # Give this solve a fresh budget without discarding the warm basis.
        run_time_before = float(self.highs.getRunTime())
        _check(self.highs.setOptionValue('time_limit', run_time_before+self.time_limit),
               'refresh cumulative solver deadline')
        began = time.monotonic()
        run_status = self.highs.run()
        status = self.highs.getModelStatus()
        fallback = None
        if status in (highs.HighsModelStatus.kUnknown, highs.HighsModelStatus.kSolveError):
            fallback = {"original_status": self.highs.modelStatusToString(status),
                        "original_run_status": str(run_status),
                        "method": "IPM with crossover, then restore dual simplex"}
            # Keep the model and its appended cuts. Only discard the failed
            # basis; an IPM crossover produces a fresh basis for warm updates.
            _check(self.highs.setBasis(), "clear failed basis")
            _check(self.highs.setOptionValue("solver", "ipm"), "select fallback IPM")
            _check(self.highs.setOptionValue("run_crossover", "on"), "enable crossover")
            _check(self.highs.setOptionValue("ipm_optimality_tolerance", 1e-9), "set IPM tolerance")
            try:
                run_status = self.highs.run()
                status = self.highs.getModelStatus()
            finally:
                _check(self.highs.setOptionValue("solver", "simplex"), "restore dual simplex")
        _check(run_status, "run")
        elapsed = time.monotonic() - began
        if status != highs.HighsModelStatus.kOptimal:
            raise SolveError("HiGHS status: " + self.highs.modelStatusToString(status))
        solution, info = self.highs.getSolution(), self.highs.getInfo()
        self.calls += 1
        self.last_stats = {
            "seconds": elapsed, "simplex_iterations": info.simplex_iteration_count,
            "cumulative_run_time_before": run_time_before,
            "cumulative_run_time_after": float(self.highs.getRunTime()),
            "per_solve_time_budget": self.time_limit,
            "basis_valid_before": bool(basis_before),
            "basis_valid_after": bool(self.highs.getBasis().valid),
            "rows": self.highs.getNumRow(), "columns": self.highs.getNumCol(),
            "nonzeros": self.highs.getNumNz(),
            "max_primal_infeasibility": info.max_primal_infeasibility,
            "max_dual_infeasibility": info.max_dual_infeasibility,
            "ipm_iterations": info.ipm_iteration_count,
            "crossover_iterations": info.crossover_iteration_count,
        }
        if fallback is not None:
            self.last_stats["fallback"] = fallback
        return OptimizeResult(
            success=True, status=0, message="Optimal (persistent HiGHS)",
            x=np.asarray(solution.col_value, dtype=float),
            fun=float(self.highs.getObjectiveValue()),
            nit=info.simplex_iteration_count,
            ineqlin=OptimizeResult(
                residual=self.rhs - np.asarray(solution.row_value, dtype=float),
                marginals=np.asarray(solution.row_dual, dtype=float)),
        )


class PersistentMaster:
    """Adapter retaining master/prox matrices and simplex bases between calls."""

    def __init__(self, master, time_limit=120.):
        self.master, self.K, self.time_limit = master, master.K, time_limit
        self.order_rows = len(master.order)
        objective = np.zeros(self.K + 1)
        objective[-1] = -1.
        self.main = PersistentLP(
            objective, master.order_matrix, np.zeros(self.order_rows),
            np.zeros(self.K + 1), np.r_[np.ones(self.K), 2.], time_limit)
        self.main_columns = 0
        self.prox = None
        self.prox_columns = 0
        self.last_stats = {}

    def _cuts(self, start):
        columns = self.master.columns[start:]
        rr, cc, vv, rhs = [], [], [], []
        scale = 4 * self.master.n
        for row, column in enumerate(columns):
            rr.append(row); cc.append(self.K); vv.append(1.)
            for i, value in column["coeff"].items():
                rr.append(row); cc.append(int(i)); vv.append(-value / scale)
            rhs.append(column["mass"] / scale)
        matrix = coo_matrix((vv, (rr, cc)),
                            shape=(len(columns), self.K + 1)).tocsr()
        return matrix, np.asarray(rhs, dtype=float)

    def _sync_main(self):
        if len(self.master.columns) < self.main_columns:
            raise RuntimeError("Persistent master requires append-only columns")
        cuts, rhs = self._cuts(self.main_columns)
        self.main.add_rows(cuts, rhs)
        self.main_columns = len(self.master.columns)

    def _make_prox(self, anchor, level):
        K = self.K
        # Variables [g (K), z (1), u (K), a (K)].  The a variables are fixed
        # to the anchor; u >= |g-a|. Keeping z fixes the desired master level.
        rr, cc, vv = [], [], []
        for i in range(K):
            rr.extend((i, i, i, K + i, K + i, K + i))
            cc.extend((i, K + 1 + i, 2 * K + 1 + i,
                       i, K + 1 + i, 2 * K + 1 + i))
            vv.extend((1., -1., -1., -1., -1., 1.))
        distance = coo_matrix((vv, (rr, cc)), shape=(2 * K, 3 * K + 1)).tocsr()
        order = hstack([self.master.order_matrix, csr_matrix((self.order_rows, 2 * K))],
                       format="csr")
        matrix = vstack([order, distance], format="csr")
        objective = np.r_[np.zeros(K + 1), np.ones(K), np.zeros(K)]
        lower = np.r_[np.zeros(K), level, np.zeros(K), anchor]
        upper = np.r_[np.ones(K), level, np.full(K, np.inf), anchor]
        self.prox = PersistentLP(
            objective, matrix, np.zeros(self.order_rows + 2 * K),
            lower, upper, self.time_limit)
        self.prox_columns = 0

    def _sync_prox(self):
        cuts, rhs = self._cuts(self.prox_columns)
        padded = hstack([cuts, csr_matrix((cuts.shape[0], 2 * self.K))], format="csr")
        self.prox.add_rows(padded, rhs)
        self.prox_columns = len(self.master.columns)

    def solve_lp(self, anchor=None, level_lower=None):
        self._sync_main()
        result = self.main.solve()
        weights = -result.ineqlin.marginals[self.order_rows:]
        trial = result.x[:-1].copy()
        self.last_stats = {"highs_version": self.main.highs.version(),
                           "main": self.main.last_stats.copy()}
        if anchor is not None and level_lower is not None and -result.fun > level_lower + 1e-9:
            anchor = np.asarray(anchor, dtype=float)
            if anchor.shape != (self.K,):
                raise ValueError("wrong anchor size")
            level = level_lower + .5 * (-result.fun - level_lower)
            if self.prox is None:
                self._make_prox(anchor, level)
            else:
                indices = np.r_[self.K, np.arange(2 * self.K + 1, 3 * self.K + 1)]
                self.prox.fix_columns(indices, np.r_[level, anchor])
            self._sync_prox()
            try:
                proximal = self.prox.solve()
            except SolveError as error:
                # Match the original master: the optional stabilizer may
                # fail without discarding the valid main LP optimum.
                self.last_stats["prox_failure"] = str(error)
            else:
                trial = proximal.x[:self.K].copy()
                self.last_stats["prox"] = dict(
                    self.prox.last_stats, level=float(level),
                    l1_distance=float(np.abs(trial - anchor).sum()))
        return result, weights, trial

