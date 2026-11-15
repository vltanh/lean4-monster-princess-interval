#!/usr/bin/env python3
"""Append-only sparse calendar LP with seed-clamped exact field extension."""
from __future__ import annotations

from pathlib import Path
import sys
import time

import numpy as np
from scipy.sparse import coo_matrix,csr_matrix

ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT/'packages/interval_sparse_upper'),
              str(ROOT/'packages/interval_clock_grid/normalized_native')]
from master import projected_order,plan_column
from persistent_highs import PersistentLP,_check,SolveError
from clamp import clamp_extend


class ClampedSparseMaster:
    def __init__(self,master,seconds=120.,crossover=True,
                 component_prox=False,level_fraction=.5):
        if hasattr(master,'coarse') or hasattr(master,'base'):
            raise ValueError('sparse event search uses the full physical nodal grid; profile-grid must equal n')
        self.master,self.seconds=master,float(seconds)
        self.component_prox=component_prox
        self.level_fraction=level_fraction
        self.nodes,self.index,self.edges,self.calendar_rows=[],{},set(),[]
        self.columns=0
        self.main=PersistentLP([-1.],csr_matrix((0,1)),[],[0.],[2.],seconds)
        _check(self.main.highs.setOptionValue('solver','ipm'),'initial sparse IPM')
        _check(self.main.highs.setOptionValue('run_crossover','on'),'sparse crossover')
        self.prox=None
        if component_prox:
            self.prox=PersistentLP([0.],csr_matrix((0,1)),[],[0.],[2.],seconds)
            _check(self.prox.highs.setOptionValue('solver','ipm'),'initial sparse level IPM')
            _check(self.prox.highs.setOptionValue('run_crossover','on'),'sparse level crossover')

    def _sync(self):
        began=time.monotonic()
        if len(self.master.columns)<self.columns:
            raise ValueError('calendar columns must be append-only')
        columns=[plan_column(self.master.n,c['plan']) for c in self.master.columns[self.columns:]]
        new_nodes=sorted({point for _,coef in columns for point in coef if point not in self.index})
        first_new=len(self.nodes)
        if new_nodes:
            count=len(new_nodes)
            _check(self.main.highs.addCols(count,np.zeros(count),np.zeros(count),np.ones(count),
                0,np.zeros(count+1,dtype=np.int32),np.zeros(0,dtype=np.int32),np.zeros(0)),
                'append sparse lower events')
            for point in new_nodes:
                self.index[point]=len(self.nodes);self.nodes.append(point)
            new_edges=[edge for edge in projected_order(self.master.n,self.nodes) if edge not in self.edges]
            if self.prox is not None:
                _check(self.prox.highs.addCols(3*count,np.tile([0.,1.,0.],count),
                    np.zeros(3*count),np.tile([1.,np.inf,1.],count),
                    0,np.zeros(3*count+1,dtype=np.int32),np.zeros(0,dtype=np.int32),np.zeros(0)),
                    'append sparse level variables')
                rr=[];cc=[];vv=[]
                for row,i in enumerate(range(first_new,len(self.nodes))):
                    g,u,a=3*i+1,3*i+2,3*i+3
                    rr.extend((2*row,)*3+(2*row+1,)*3)
                    cc.extend((g,u,a,g,u,a));vv.extend((1.,-1.,-1.,-1.,-1.,1.))
                matrix=coo_matrix((vv,(rr,cc)),shape=(2*count,3*len(self.nodes)+1)).tocsr()
                self.prox.add_rows(matrix,np.zeros(2*count))
        else:
            new_edges=[]
        rr=[];cc=[];vv=[]
        for row,(a,b) in enumerate(new_edges):
            rr.extend((row,row));cc.extend((a+1,b+1));vv.extend((1.,-1.))
        rhs=[0.]*len(new_edges)
        first_row=self.main.highs.getNumRow()
        for row,(mass,coef) in enumerate(columns,len(new_edges)):
            rr.append(row);cc.append(0);vv.append(1.)
            for point,value in coef.items():
                rr.append(row);cc.append(self.index[point]+1);vv.append(-value/(4*self.master.n))
            rhs.append(mass/(4*self.master.n));self.calendar_rows.append(first_row+row)
        matrix=coo_matrix((vv,(rr,cc)),shape=(len(rhs),len(self.nodes)+1)).tocsr()
        self.main.add_rows(matrix,rhs)
        if self.prox is not None:
            prox_cc=[0 if c==0 else 3*(c-1)+1 for c in cc]
            prox_matrix=coo_matrix((vv,(rr,prox_cc)),shape=(len(rhs),3*len(self.nodes)+1)).tocsr()
            self.prox.add_rows(prox_matrix,rhs)
        self.edges.update(new_edges);self.columns=len(self.master.columns)
        return time.monotonic()-began

    def solve_box(self,anchor,radius,lower=None):
        assembly=self._sync()
        K=len(self.nodes)
        # The incumbent comes from an exact integer table. Nearest-integer
        # recovery preserves those bytes; flooring a binary round-trip would
        # unnecessarily change them before the clamping construction.
        integers=np.rint(np.asarray(anchor)*self.master.D).astype(np.uint64)
        seed=np.zeros((self.master.H+1,self.master.R+1),dtype=np.uint64)
        for (j,k),value in zip(self.master.nodes,integers):seed[j,k]=value
        n=self.master.n;R,C,H=2*n,4*n,12*n
        for j in range(C+1,C+R+1):
            ks=np.arange(1+(j+1)%2,R+1,2);ks=ks[ks>j-C]
            seed[j,ks]=seed[C,ks-j+C]
        event_anchor=np.asarray([int(seed[j,k])/self.master.D for j,k in self.nodes])
        low=np.maximum(0.,event_anchor-radius);high=np.minimum(1.,event_anchor+radius)
        _check(self.main.highs.changeColsBounds(K,np.arange(1,K+1,dtype=np.int32),low,high),
               'sparse trust box')
        result=self.main.solve()
        _check(self.main.highs.setOptionValue('solver','simplex'),'warm sparse lower basis')
        events=result.x[1:].copy();self.trial_level=float(-result.fun)
        self.last_stats=dict(self.main.last_stats,event_nodes=K,order_edges=len(self.edges),
            original_profile_variables=self.master.K,assembly_seconds=assembly,
            method='exact projected order with closest-seed extension')
        if self.prox is not None and lower is not None and -result.fun>lower+1e-9:
            level=lower+self.level_fraction*(-result.fun-lower)
            _check(self.prox.highs.changeColsBounds(K,3*np.arange(K,dtype=np.int32)+1,low,high),
                   'sparse level trust box')
            self.prox.fix_columns(np.r_[0,3*np.arange(K)+3],np.r_[level,event_anchor])
            try:
                proximal=self.prox.solve()
            except SolveError as error:
                self.last_stats['level_prox_failure']=str(error)
            else:
                events=proximal.x[1::3].copy();self.trial_level=float(level)
                self.last_stats['level_prox']=dict(self.prox.last_stats,target_level=float(level),
                    l1_event_displacement=float(np.abs(events-event_anchor).sum()))
                _check(self.prox.highs.setOptionValue('solver','simplex'),'warm sparse level basis')
        weights=-result.ineqlin.marginals[np.asarray(self.calendar_rows,dtype=np.int64)]
        table,stats=clamp_extend(n,self.master.D,self.nodes,events,seed)
        self.last_stats['exact_clamp']=stats
        values=self.master.profile_values(table)
        result.x=np.r_[values,-result.fun]
        # Inherited Master.repair floors its input. Quarter-unit guard makes
        # that final pass reproduce exactly the constructed integer table.
        trial=np.minimum(1.,(np.rint(values*self.master.D)+.25)/self.master.D)
        return result,weights,trial
