"""Persistent HiGHS bases for response-cut masters.

Uses the HiGHS binding bundled with the installed SciPy. Appended response
rows and changed proximal levels retain the simplex basis. This changes only
the numerical algorithm, never the set of game columns or constraints.
"""
from __future__ import annotations
from types import SimpleNamespace
import numpy as np
from scipy.sparse import csr_matrix
from scipy.optimize._highspy import _core


def engine(cost, lower, upper):
    h=_core._Highs()
    for key,value in [('output_flag',False),('solver','simplex'),('threads',1),
        ('primal_feasibility_tolerance',1e-9),('dual_feasibility_tolerance',1e-9)]:
        assert h.setOptionValue(key,value)==_core.HighsStatus.kOk
    n=len(cost)
    assert h.addCols(n,np.asarray(cost),np.asarray(lower),np.asarray(upper),0,
        np.zeros(n+1,dtype=np.int32),np.array([],dtype=np.int32),np.array([],dtype=float))==_core.HighsStatus.kOk
    return h


def add_rows(h,matrix,lower,upper):
    a=csr_matrix(matrix)
    assert h.addRows(a.shape[0],np.asarray(lower),np.asarray(upper),a.nnz,
        a.indptr.astype(np.int32),a.indices.astype(np.int32),a.data)==_core.HighsStatus.kOk


def solve(h):
    assert h.run()==_core.HighsStatus.kOk
    assert h.getModelStatus()==_core.HighsModelStatus.kOptimal, h.getModelStatus()
    return h.getSolution()


class GlobalMasters:
    def __init__(self,count):
        self.count=count;self.added=0
        self.master=engine(np.r_[np.zeros(count),1.],np.r_[np.zeros(count),-np.inf],
                           np.full(count+1,np.inf))
        add_rows(self.master,np.array([[1.]*count+[0.]]),[1.],[1.])
        self.proximal=engine(np.r_[np.zeros(count),np.ones(count)],np.zeros(2*count),np.full(2*count,np.inf))
        add_rows(self.proximal,np.array([[1.]*count+[0.]*count]),[1.],[1.])
        # Anchor inequalities precede the game rows and keep their indices.
        indices=np.arange(count)
        from scipy.sparse import coo_matrix
        ri=np.r_[indices,indices,count+indices,count+indices]
        ci=np.r_[indices,count+indices,indices,count+indices]
        vv=np.r_[np.ones(count),-np.ones(count),-np.ones(count),-np.ones(count)]
        anchor=coo_matrix((vv,(ri,ci)),shape=(2*count,2*count)).tocsr()
        add_rows(self.proximal,anchor,np.full(2*count,-np.inf),np.zeros(2*count))

    def append(self,matrix):
        if len(matrix)==self.added:return
        assert len(matrix)>self.added
        a=np.asarray(matrix[self.added:],dtype=float);n=len(a)
        add_rows(self.master,np.c_[a,-np.ones(n)],np.full(n,-np.inf),np.zeros(n))
        from scipy.sparse import hstack
        add_rows(self.proximal,hstack((csr_matrix(a),csr_matrix(a.shape))),
                 np.full(n,-np.inf),np.zeros(n))
        self.added=len(matrix)

    def primary(self,matrix):
        self.append(matrix);answer=solve(self.master)
        return SimpleNamespace(success=True,x=np.asarray(answer.col_value),
            fun=self.master.getObjectiveValue(),
            ineqlin=SimpleNamespace(marginals=np.asarray(answer.row_dual[1:])))

    def prox(self,matrix,anchor,target):
        self.append(matrix);n=self.count;h=self.proximal
        for j,value in enumerate(anchor):
            h.changeRowBounds(1+j,-np.inf,float(value))
            h.changeRowBounds(1+n+j,-np.inf,-float(value))
        for j in range(self.added):h.changeRowBounds(1+2*n+j,-np.inf,float(target))
        answer=solve(h)
        return SimpleNamespace(success=True,x=np.asarray(answer.col_value),fun=h.getObjectiveValue())
