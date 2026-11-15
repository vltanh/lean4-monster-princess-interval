"""Complete linear admissibility for one localized inward/ramp column.

Public variables are the old (w0,f,g,k,ell), followed by eta>=0.  The added
monster support has i(a,v)=eta for d<a<1,-a<v<-d and the tied old-law change
k=ell=eta*(x-d)+, with every induced early-M2/signed-M3 density included.
"""
from dataclasses import dataclass

import numpy as np

import discover_m3_attached as attached
from m3_attached_oracle import M3_LEFT, M3_RIGHT, positive_late_profile
from localized_ramp_basis import D, KM, density, early_mass


@dataclass
class LocalizedLaw:
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
        self.size = self.old_size+1
        assert self.negative_start_bound <= D < self.turn
        assert self.right < D
        scalar = self.profile[:,0]+self.profile[:,1]*(self.knots[:-1]+self.knots[1:])/2.
        assert np.all(self.knots[1:][scalar>1.+1e-12] <= D+1e-12)
        base, equality = attached.constraints(self.knots, scalar, self.left, self.right,
            self.turn, None, self.profile, self.negative_start_bound, True)
        labels = list(attached.CONSTRAINT_LABELS)
        self.equality_labels = list(attached.EQUALITY_LABELS)
        column = [0.]*(3*(self.n-1))
        for j in range(self.n):
            lo, hi = self.knots[j:j+2]
            column.append(early_mass(hi,self.turn)
                if lo>=self.left-1e-12 and hi<=self.right+1e-12 else 0.)
            vmax = self.profile[j,0]+self.profile[j,1]*hi
            if vmax>1.:
                column.append(0.)
        column.extend([0.]*(self.n-1))  # Gamma: ramp is continuous and zero on late starts
        plus_profile = positive_late_profile(self.knots)
        for j in range(self.n):
            lo, hi = self.knots[j:j+2]
            if lo<M3_RIGHT-1e-12 and hi>M3_LEFT+1e-12:
                column.extend((KM[0]/(3.+max(lo,M3_LEFT)),
                               KM[0]/(3.-min(hi,M3_RIGHT)), 0.))
            elif plus_profile[j]>1.:
                column.append(0.)
            if lo>=self.left-1e-12 and hi<=self.right+1e-12:
                column.append(-density(self.turn))
        assert len(column)==len(base)==len(labels)
        rows = np.c_[base,np.asarray(column)]
        keep = np.asarray([not label.startswith('p=f+g nondecreasing') for label in labels])
        self.inequalities = rows[keep]
        self.labels = [label for label,yes in zip(labels,keep) if yes]
        self.equalities = np.c_[equality,np.zeros(len(equality))]
        self.equalities[0,-1] = 2.*KM[0]
        self.bounds = [(0.,None)]*self.size

    def summary(self,variables):
        values=np.asarray(variables)
        return dict(normalization=float(self.equalities[0]@values),
                    minimum_structural_slack=float(np.min(-self.inequalities@values)),
                    eta=float(values[-1]), threshold=D,
                    localized_I_mass=float(values[-1]*KM[0]),
                    added_k_mass=float(values[-1]*KM[0]),
                    endpoint_ramp_density=float(values[-1]*(1.-D)))
