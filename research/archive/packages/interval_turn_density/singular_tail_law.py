"""Fixed singular-tail attachment and its complete linear admissibility rows.

Variables are the old vector (w0, f, g, k, ell), followed by one amplitude B.
The last old f coefficient is fixed to zero: the analytic f tail replaces it.
The last old k and ell coefficients stop at K_CUTOFF.  Their common analytic
tail replaces the remaining interval.  The extra integration knot has no new
optimized density coefficient.  The ordinary g coefficient is retained.

This module removes only p=f+g monotonicity, using the separately proved
ordered-block response.  All remaining density, suffix and edge conditions
are retained and labelled.  Numerical integration is not an exact certificate.
"""
from dataclasses import dataclass

import numpy as np

import discover_m3_attached as attached
from m3_attached_oracle import M3_LEFT, M3_RIGHT, positive_late_profile
from singular_tail_basis import (F_CUTOFF, CUTOFF, FM, KM, density, moment,
                                 early_mass, late_mass)


@dataclass
class TailLaw:
    """A fixed linear map from old coefficients to the truncated step field."""

    knots: np.ndarray
    profile: np.ndarray
    left: float
    right: float
    turn: float
    negative_start_bound: float

    def __post_init__(self):
        self.knots = np.asarray(self.knots, dtype=float)
        self.profile = np.asarray(self.profile, dtype=float)
        assert self.profile.shape == (len(self.knots)-1, 2)
        assert abs(self.knots[-2]-F_CUTOFF) < 1e-13
        assert self.knots[-1] == 1.
        assert self.negative_start_bound < F_CUTOFF < CUTOFF < 1.
        self.n = len(self.knots)-1
        self.old_size = 1+4*self.n
        self.size = self.old_size+1
        self.aug_knots = np.sort(np.r_[self.knots, CUTOFF])
        self.aug_n = len(self.aug_knots)-1
        self.aug_size = 1+4*self.aug_n
        self.mapping = np.zeros((self.aug_size, self.old_size))
        self.mapping[0, 0] = 1.
        self.aug_profile = np.zeros((self.aug_n, 2))
        for j in range(self.aug_n):
            middle = (self.aug_knots[j]+self.aug_knots[j+1])/2.
            old = min(self.n-1, int(np.searchsorted(self.knots, middle)-1))
            self.aug_profile[j] = self.profile[old]
            for group in range(4):
                if group in (2, 3) and self.aug_knots[j] >= CUTOFF-1e-13:
                    continue
                self.mapping[1+group*self.aug_n+j, 1+group*self.n+old] = 1.
        self.bounds = [(0., None)]*self.size
        self.bounds[self.n] = (0., 0.)  # final f coefficient
        self.inequalities, self.equalities, self.labels, self.equality_labels = self._constraints()

    def expand(self, variables):
        """Return (augmented step coefficients, common tail amplitude)."""
        values = np.asarray(variables)
        assert len(values) == self.size
        return self.mapping@values[:-1], float(values[-1])

    def pullback(self, step_row, tail_column):
        """Frozen full-law feature row in the public variable order."""
        return np.r_[np.asarray(step_row)@self.mapping, float(tail_column)]

    @staticmethod
    def _f_primitive(t):
        if t <= F_CUTOFF:
            return 0.
        return FM[0]-moment(1.-min(t, 1.), 2./3., 0, 1.)

    def _gamma_tail(self, z, j, trace):
        v = self.aug_profile[j, 0]+self.aug_profile[j, 1]*z
        # A bin trace matters only at the analytic ell jump.
        ell = density(z, 1./6., .5) if trace else 0.
        return self._f_primitive(2.-v)-(z+2.-v)*ell

    def _constraints(self):
        knots, n = self.aug_knots, self.aug_n
        profile = self.aug_profile[:, 0]+self.aug_profile[:, 1]*(knots[:-1]+knots[1:])/2.
        base, equalities = attached.constraints(knots, profile, self.left, self.right,
            self.turn, None, self.aug_profile, self.negative_start_bound, True)
        labels = list(attached.CONSTRAINT_LABELS)
        eq_labels = list(attached.EQUALITY_LABELS)
        column = []
        # Exact same order as discover_separated.constraints.
        for group in ('f', 'p', 'k'):
            for j in range(n-1):
                z = knots[j+1]
                if group in ('f', 'p') and abs(z-F_CUTOFF) < 1e-13:
                    value = -density(F_CUTOFF, 2./3., 1.)
                elif group == 'k' and abs(z-CUTOFF) < 1e-13:
                    value = -density(CUTOFF, 1./6., .5)
                else:
                    value = 0.
                column.append(value)
        for j in range(n):
            lo, hi = knots[j], knots[j+1]
            mass = 0.
            if lo >= self.left-1e-12 and hi <= self.right+1e-12:
                mass += early_mass(hi)
            vmax = self.aug_profile[j, 0]+self.aug_profile[j, 1]*hi
            if vmax > 1.+1e-13:
                assert 2.-vmax < F_CUTOFF
                mass += late_mass(hi, -1)
            column.append(mass)  # inequality is minus the line residual
            if vmax > 1.:
                column.append(0.)  # both upper-edge arguments precede tails
        for j in range(n-1):
            z = knots[j+1]
            left_trace = knots[j] >= CUTOFF-1e-13
            right_trace = knots[j+1] >= CUTOFF-1e-13
            column.append(self._gamma_tail(z, j+1, right_trace)
                          -self._gamma_tail(z, j, left_trace))
        plus_profile = positive_late_profile(knots)
        for j in range(n):
            lo, hi = knots[j], knots[j+1]
            if lo < M3_RIGHT-1e-12 and hi > M3_LEFT+1e-12:
                z = max(lo, M3_LEFT)
                mass = KM[0]/(3.+z)
                if plus_profile[j] > 1.:
                    mass += late_mass(z, 1)
                column.append(mass)
                z = min(hi, M3_RIGHT)
                mass = KM[0]/(3.-z)
                if lo >= self.left-1e-12 and hi <= self.right+1e-12:
                    mass += early_mass(z)
                if self.aug_profile[j, 0]+self.aug_profile[j, 1]*z > 1.+1e-13:
                    mass += late_mass(z, -1)
                column.extend((mass, 0.))
            elif plus_profile[j] > 1.:
                column.append(late_mass(lo, 1))
            if lo >= self.left-1e-12 and hi <= self.right+1e-12:
                column.append(0.)  # all lower-edge price arguments are <K_CUTOFF
        assert len(column) == len(base) == len(labels)
        rows = np.c_[base@self.mapping, np.asarray(column)]
        eq_column = np.zeros(len(equalities))
        eq_column[0] = FM[0]+KM[0]
        eq = np.c_[equalities@self.mapping, eq_column]
        keep = np.array([not label.startswith('p=f+g nondecreasing') for label in labels])
        return rows[keep], eq, [label for label, yes in zip(labels, keep) if yes], eq_labels

    def summary(self, variables):
        values = np.asarray(variables)
        return dict(normalization=float(self.equalities[0]@values),
                    minimum_structural_slack=float(np.min(-self.inequalities@values)),
                    tail_amplitude=float(values[-1]),
                    f_tail_mass=float(values[-1]*FM[0]),
                    k_tail_mass=float(values[-1]*KM[0]),
                    f_join=float(values[-1]*density(F_CUTOFF, 2./3., 1.)),
                    k_join=float(values[-1]*density(CUTOFF, 1./6., .5)),
                    tail_cutoffs=dict(f=F_CUTOFF, k_ell=CUTOFF))
