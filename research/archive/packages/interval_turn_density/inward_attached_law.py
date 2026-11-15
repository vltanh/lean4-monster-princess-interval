"""Independent monotone initial-inward density on the existing outer bins.

Public variables are (w0,f,g,k,ell,h).  The first five groups are the same
signed-M3 law as before, with p=f+g unrestricted.  The last group adds the
monster density i(a,v)=h(a), -a<v<a, and mass integral 2a*h(a) da.
No old component is silently reallocated to this additional support.
"""
from dataclasses import dataclass

import numpy as np

import discover_m3_attached as attached


@dataclass
class InwardLaw:
    knots: np.ndarray
    profile: np.ndarray
    left: float
    right: float
    turn: float
    negative_start_bound: float

    def __post_init__(self):
        self.knots = np.asarray(self.knots, dtype=float)
        self.profile = np.asarray(self.profile, dtype=float)
        self.n = len(self.knots)-1
        self.old_size = 1+4*self.n
        self.size = self.old_size+self.n
        assert self.profile.shape == (self.n, 2)
        scalar_profile = self.profile[:, 0]+self.profile[:, 1]*(self.knots[:-1]+self.knots[1:])/2.
        old_rows, old_equalities = attached.constraints(self.knots, scalar_profile,
            self.left, self.right, self.turn, None, self.profile,
            self.negative_start_bound, True)
        keep = np.array([not label.startswith('p=f+g nondecreasing')
                         for label in attached.CONSTRAINT_LABELS])
        self.labels = [label for label, yes in zip(attached.CONSTRAINT_LABELS, keep) if yes]
        self.equality_labels = list(attached.EQUALITY_LABELS)
        rows = [np.r_[row, np.zeros(self.n)] for row in old_rows[keep]]
        for j in range(self.n-1):
            row = np.zeros(self.size)
            row[self.old_size+j], row[self.old_size+j+1] = 1., -1.
            rows.append(row)
            self.labels.append(f'h nondecreasing at {self.knots[j+1]:.12g}')
        self.inequalities = np.asarray(rows)
        self.equalities = np.c_[old_equalities, np.zeros((len(old_equalities), self.n))]
        self.mass_row = self.knots[1:]**2-self.knots[:-1]**2
        self.equalities[0, self.old_size:] = self.mass_row
        self.bounds = [(0., None)]*self.size

    def split(self, variables):
        values = np.asarray(variables)
        assert len(values) == self.size
        return values[:self.old_size], values[self.old_size:]

    def summary(self, variables):
        values = np.asarray(variables)
        return dict(normalization=float(self.equalities[0]@values),
                    minimum_structural_slack=float(np.min(-self.inequalities@values)),
                    inward_mass=float(self.mass_row@values[self.old_size:]),
                    h=values[self.old_size:].tolist())
