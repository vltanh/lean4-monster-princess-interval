"""A gated nonmonotone-h extension on the same density coordinates.

h is supported above 7/8.  In addition to monotone k, monotone k+2h
preserves the positive-prefix U ordering.  The full signed-M3 curvature
controls its V ordering.  Separate integral gates preserve the actual flat
M2/M3 corridors, where the raw target-minus-alpha derivative is insufficient.
All sufficient-condition normals are labelled; none is a princess mass.
"""
import numpy as np
from numba import njit

from inward_attached_law import InwardLaw
from m3_attached_oracle import M3_LEFT, M3_RIGHT, M3_TURN
from separated_oracle import bin_at


@njit
def generator_curvature(r, lo, hi, s, sign):
    if hi <= lo:
        return 0.
    wl, wr = 4.-s+sign*lo, 4.-s+sign*hi
    i2 = sign*(1./wl-1./wr)
    i3 = sign*(1./(wl*wl)-1./(wr*wr))/2.
    return 2.*i2+2.*(s-r)*i3


@njit
def full_m3_curvature_row(s, knots):
    """Right derivative of the full positive plus full negative beta price."""
    n = len(knots)-1
    row = np.zeros(1+4*n)
    if s < M3_TURN:
        return row
    edge = bin_at(M3_TURN, knots)
    for sign in (-1, 1):
        for j in range(n):
            lo, hi = max(M3_LEFT, knots[j]), min(M3_RIGHT, knots[j+1])
            factor = generator_curvature(M3_TURN, lo, hi, s, sign)
            row[1+2*n+edge] += factor
            if sign > 0:
                row[1+j] -= factor
                row[1+n+j] -= factor
            else:
                row[1+2*n+j] -= factor
        for j in range(1, n):
            r = knots[j]
            if M3_TURN+1e-13 < r <= s+1e-13:
                factor = generator_curvature(r, M3_LEFT, M3_RIGHT, s, sign)
                row[1+2*n+j] += factor
                row[1+2*n+j-1] -= factor
    return row


class CurvatureInwardLaw(InwardLaw):
    h_start = .875

    def __post_init__(self):
        super().__post_init__()
        keep = [i for i, label in enumerate(self.labels)
                if not label.startswith('h nondecreasing')]
        rows = [row.copy() for row in self.inequalities[keep]]
        self.labels = [self.labels[i] for i in keep]
        equalities = [row.copy() for row in self.equalities]
        for j in range(self.n):
            if self.knots[j] < self.h_start-1e-12:
                row = np.zeros(self.size)
                row[self.old_size+j] = 1.
                equalities.append(row)
                self.equality_labels.append(f'no initial-inward starts bin {j}')
        for j in range(self.n-1):
            row = np.zeros(self.size)
            row[1+2*self.n+j], row[1+2*self.n+j+1] = 1., -1.
            row[self.old_size+j], row[self.old_size+j+1] = 2., -2.
            rows.append(row)
            self.labels.append(f'k+2h nondecreasing at {self.knots[j+1]:.12g}')
        for j in range(self.n):
            if self.knots[j] < self.h_start-1e-12:
                continue
            curvature = full_m3_curvature_row(self.knots[j], self.knots)
            for later in range(j+1, self.n):
                row = np.zeros(self.size)
                row[:self.old_size] = -curvature
                row[self.old_size+j] = 1.
                row[self.old_size+later] = -2.
                rows.append(row)
                self.labels.append(f'h positive-prefix order Vbin {j} Ubin {later}')
            # H(U) is maximal at the bin's right trace.  For U>=s0 the
            # largest calibrated positive V is right=.5; before s0 only
            # the smaller M3 start band is flat.  h vanishes on both bands.
            vmax = self.right if self.knots[j] >= self.turn-1e-12 else M3_RIGHT
            row = np.zeros(self.size)
            row[self.old_size:self.old_size+j+1] = np.diff(self.knots)[:j+1]/(1.-vmax)
            row[self.old_size+j] -= 1.
            rows.append(row)
            family = 'M2' if self.knots[j] >= self.turn-1e-12 else 'M3'
            self.labels.append(f'h {family} flat-corridor gate bin {j}')
        self.inequalities, self.equalities = np.asarray(rows), np.asarray(equalities)

    def summary(self, variables):
        result = super().summary(variables)
        result.update(h_mode='curvature and integrated corridor gates', h_start=self.h_start)
        return result
