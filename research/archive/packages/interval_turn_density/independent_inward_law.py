"""One independent localized inward triangle without a tied ramp.

The old density law remains unchanged.  The last variable eta>=0 adds
i(a,v)=eta on D<a<1,-a<v<-D.  This component has mass eta*(1-D)^2/2.
Its negative-prefix optimizer uses convex rounding within the existing
step-k intervals, so no extra monotonicity restriction is imposed.
"""
from dataclasses import dataclass

import numpy as np

import discover_m3_attached as attached
from localized_ramp_basis import D


@dataclass
class IndependentLocalizedLaw:
    knots: np.ndarray
    profile: np.ndarray
    left: float
    right: float
    turn: float
    negative_start_bound: float

    def __post_init__(self):
        self.knots=np.asarray(self.knots,dtype=float)
        self.profile=np.asarray(self.profile,dtype=float)
        self.n=len(self.knots)-1
        self.old_size=1+4*self.n
        self.size=self.old_size+1
        scalar=self.profile[:,0]+self.profile[:,1]*(self.knots[:-1]+self.knots[1:])/2.
        old,equality=attached.constraints(self.knots,scalar,self.left,self.right,
            self.turn,None,self.profile,self.negative_start_bound,True)
        labels=list(attached.CONSTRAINT_LABELS)
        keep=np.asarray([not label.startswith('p=f+g nondecreasing') for label in labels])
        self.inequalities=np.c_[old[keep],np.zeros(np.count_nonzero(keep))]
        self.labels=[label for label,yes in zip(labels,keep) if yes]
        self.equality_labels=list(attached.EQUALITY_LABELS)
        self.equalities=np.c_[equality,np.zeros(len(equality))]
        self.component_mass=(1.-D)**2/2.
        self.equalities[0,-1]=self.component_mass
        self.bounds=[(0.,None)]*self.size

    def summary(self,variables):
        values=np.asarray(variables)
        return dict(normalization=float(self.equalities[0]@values),
                    minimum_structural_slack=float(np.min(-self.inequalities@values)),
                    eta=float(values[-1]),threshold=D,
                    localized_I_mass=float(values[-1]*self.component_mass),
                    added_k_mass=0.)
