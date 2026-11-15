#!/usr/bin/env python3
"""Sparse two-objective model: a fixed native floor and continuous screens."""
from __future__ import annotations

from fractions import Fraction as Q
from pathlib import Path
import sys
import time

import numpy as np
from scipy.sparse import coo_matrix,csr_matrix

ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT/'packages/interval_sparse_upper'),
              str(ROOT/'packages/interval_clock_grid/normalized_native'),
              str(ROOT/'packages/interval_sparse_lower')]
from master import projected_order,plan_column
from persistent_highs import PersistentLP,_check,SolveError
from clamp import clamp_extend


class EventLP:
    def __init__(self,master,floor,seconds=180.,level_fraction=.5):
        self.master=master;self.floor=Q(floor);self.seconds=seconds
        self.level_fraction=level_fraction
        self.nodes=[];self.index={};self.edges=set()
        self.bank_count=0;self.attack_count=0
        self.attacks=[];self.attack_seen=set()
        self.main=PersistentLP([-1.],csr_matrix((0,1)),[],[0.],[3.],seconds)
        self.prox=PersistentLP([0.],csr_matrix((0,1)),[],[0.],[3.],seconds)
        for model in (self.main,self.prox):
            _check(model.highs.setOptionValue('solver','ipm'),'initial event IPM')
            _check(model.highs.setOptionValue('run_crossover','on'),'event crossover')

    def add_plane(self,plane):
        const=Q(plane['constant'])
        coeff={(int(j),int(k)):Q(a) for j,k,a in plane['coefficients'] if Q(a)}
        key=const,tuple(sorted(coeff.items()))
        if key in self.attack_seen:return False
        self.attack_seen.add(key)
        self.attacks.append({'constant':const,'coeff':coeff})
        return True

    def _sync(self):
        began=time.monotonic()
        bank=[plan_column(self.master.n,c['plan']) for c in self.master.columns[self.bank_count:]]
        attacks=self.attacks[self.attack_count:]
        new=sorted({point for _,coef in bank for point in coef if point not in self.index}|
                   {point for p in attacks for point in p['coeff'] if point not in self.index})
        first=len(self.nodes)
        if new:
            count=len(new)
            _check(self.main.highs.addCols(count,np.zeros(count),np.zeros(count),np.ones(count),
                0,np.zeros(count+1,dtype=np.int32),np.zeros(0,dtype=np.int32),np.zeros(0)), 'new event coordinates')
            _check(self.prox.highs.addCols(3*count,np.tile([0.,1.,0.],count),np.zeros(3*count),
                np.tile([1.,np.inf,1.],count),0,np.zeros(3*count+1,dtype=np.int32),
                np.zeros(0,dtype=np.int32),np.zeros(0)),'new level coordinates')
            for p in new:self.index[p]=len(self.nodes);self.nodes.append(p)
            edges=[e for e in projected_order(self.master.n,self.nodes) if e not in self.edges]
            rr=[];cc=[];vv=[]
            for row,i in enumerate(range(first,len(self.nodes))):
                g,u,a=3*i+1,3*i+2,3*i+3
                rr.extend((2*row,)*3+(2*row+1,)*3)
                cc.extend((g,u,a,g,u,a));vv.extend((1.,-1.,-1.,-1.,-1.,1.))
            self.prox.add_rows(coo_matrix((vv,(rr,cc)),shape=(2*count,3*len(self.nodes)+1)),np.zeros(2*count))
        else:edges=[]
        rr=[];cc=[];vv=[];rhs=[]
        for a,b in edges:
            row=len(rhs);rhs.append(0.)
            rr.extend((row,row));cc.extend((a+1,b+1));vv.extend((1.,-1.))
        # These rows deliberately have NO continuous-objective coefficient.
        for mass,coef in bank:
            row=len(rhs);rhs.append(float(Q(mass,4*self.master.n)-self.floor))
            for p,value in coef.items():
                rr.append(row);cc.append(self.index[p]+1);vv.append(-value/(4*self.master.n))
        for plane in attacks:
            row=len(rhs);rhs.append(float(plane['constant']))
            rr.append(row);cc.append(0);vv.append(1.)
            for p,value in plane['coeff'].items():
                rr.append(row);cc.append(self.index[p]+1);vv.append(-float(value))
        K=len(self.nodes)
        self.main.add_rows(coo_matrix((vv,(rr,cc)),shape=(len(rhs),K+1)),rhs)
        self.prox.add_rows(coo_matrix((vv,(rr,[0 if c==0 else 3*(c-1)+1 for c in cc])),
                                     shape=(len(rhs),3*K+1)),rhs)
        self.edges.update(edges);self.bank_count=len(self.master.columns);self.attack_count=len(self.attacks)
        return time.monotonic()-began

    def solve(self,seed,screen,radius):
        assembly=self._sync();K=len(self.nodes)
        values=np.array([int(seed[j,k])/self.master.D for j,k in self.nodes])
        low=np.maximum(0.,values-radius);high=np.minimum(1.,values+radius)
        _check(self.main.highs.changeColsBounds(K,np.arange(1,K+1,dtype=np.int32),low,high),'event trust bounds')
        main=self.main.solve()
        _check(self.main.highs.setOptionValue('solver','simplex'),'event warm basis')
        events=main.x[1:];upper=float(-main.fun);level=upper
        stats=dict(self.main.last_stats,event_nodes=K,order_edges=len(self.edges),
                   bank_calendar_rows=self.bank_count,continuous_plane_rows=self.attack_count,
                   assembly_seconds=assembly,continuous_restricted_upper=upper)
        if upper>float(screen)+1e-9:
            level=float(screen)+self.level_fraction*(upper-float(screen))
            _check(self.prox.highs.changeColsBounds(K,3*np.arange(K,dtype=np.int32)+1,low,high),'level trust bounds')
            self.prox.fix_columns(np.r_[0,3*np.arange(K)+3],np.r_[level,values])
            try:prox=self.prox.solve()
            except SolveError as error:
                stats['prox_failure']=str(error);level=upper
            else:
                events=prox.x[1::3]
                _check(self.prox.highs.setOptionValue('solver','simplex'),'level warm basis')
                stats['prox']=dict(self.prox.last_stats,level=level,
                                   l1_event_displacement=float(np.abs(events-values).sum()))
        table,clamp=clamp_extend(self.master.n,self.master.D,self.nodes,events,seed)
        stats['exact_clamp']=clamp
        return table,upper,level,stats
