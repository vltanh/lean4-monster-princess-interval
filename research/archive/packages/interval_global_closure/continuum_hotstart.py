"""Persistent HiGHS basis for whole-CDF supporting-cut models.

Reuses the installed and independently exercised helpers from
efficient_hotstart.py. Only new global supporting rows are appended;
physical constraints, previous cuts, and the simplex basis are retained.
"""
from __future__ import annotations
from types import SimpleNamespace
import numpy as np
from scipy.sparse import csr_matrix
from scipy.optimize._highspy import _core
from efficient_hotstart import engine,add_rows


class FieldMaster:
    def __init__(self,objective,bounds,structural,time_limit=300.):
        lo=np.asarray([-np.inf if a is None else a for a,b in bounds],float)
        hi=np.asarray([np.inf if b is None else b for a,b in bounds],float)
        self.h=engine(np.asarray(objective),lo,hi)
        self.lower,self.upper=lo,hi
        assert self.h.setOptionValue('small_matrix_value',1e-12)==_core.HighsStatus.kOk
        self.structural_count=structural.shape[0];self.added=0;self.solved=False
        self.time_limit=float(time_limit)
        add_rows(self.h,structural,np.full(self.structural_count,-np.inf),
                 np.zeros(self.structural_count))

    def append(self,matrix,rhs):
        matrix=csr_matrix(matrix)
        if matrix.shape[0]==self.added:return
        assert matrix.shape[0]>self.added
        part=matrix[self.added:].copy();row_upper=np.asarray(rhs[self.added:],float).copy()
        tiny=abs(part.data)<=1e-12
        if np.any(tiny):
            # HiGHS discards these coefficients internally. Remove them
            # explicitly and relax each RHS by the removed term's minimum
            # over the variable bounds, so every original feasible point
            # remains feasible. Raw coefficients stay in our checkpoint.
            rows=np.repeat(np.arange(part.shape[0]),np.diff(part.indptr))
            a=part.data[tiny];columns=part.indices[tiny]
            minimum=np.minimum(a*self.lower[columns],a*self.upper[columns])
            assert np.all(np.isfinite(minimum))
            row_upper-=np.bincount(rows[tiny],weights=minimum,minlength=part.shape[0])
            part.data[tiny]=0.;part.eliminate_zeros()
        add_rows(self.h,part,np.full(part.shape[0],-np.inf),row_upper)
        self.added=matrix.shape[0]

    def primary(self,matrix,rhs):
        self.append(matrix,rhs)
        # The first solve supplies a crossover basis. Subsequent additions
        # start dual simplex from that basis instead of rebuilding a cold LP.
        self.h.setOptionValue('solver','simplex' if self.solved else 'ipm')
        self.h.setOptionValue('run_crossover','on')
        self.h.setOptionValue('time_limit',self.time_limit)
        run_status=self.h.run();model_status=self.h.getModelStatus()
        success=(run_status==_core.HighsStatus.kOk and model_status==_core.HighsModelStatus.kOptimal)
        solution=self.h.getSolution()
        if success:self.solved=True
        return SimpleNamespace(success=success,message=self.h.modelStatusToString(model_status),
            x=np.asarray(solution.col_value),fun=self.h.getObjectiveValue(),
            ineqlin=SimpleNamespace(marginals=np.asarray(solution.row_dual)))

    def basis(self):
        basis=self.h.getBasis()
        return dict(valid=bool(basis.valid),col_status=[int(x)for x in basis.col_status],
                    row_status=[int(x)for x in basis.row_status])

    def restore_basis(self,data):
        if not data or not data.get('valid'):return
        assert len(data['col_status'])==self.h.getNumCol()
        assert len(data['row_status'])==self.h.getNumRow()
        basis=_core.HighsBasis();basis.valid=True
        basis.col_status=[_core.HighsBasisStatus(x)for x in data['col_status']]
        basis.row_status=[_core.HighsBasisStatus(x)for x in data['row_status']]
        assert self.h.setBasis(basis)==_core.HighsStatus.kOk
        self.solved=True
