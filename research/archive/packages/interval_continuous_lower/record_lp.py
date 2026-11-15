#!/usr/bin/env python3
"""All causal calendar minima for each selected physical path in one LP.

Auxiliary running records form an exact hypograph, not a new lower oracle.
The complete physical response search remains the candidate acceptance gate.
"""
from fractions import Fraction as Q
import time

import numpy as np
from scipy.sparse import coo_matrix

import event_lp
from event_lp import EventLP,_check,SolveError,projected_order
from cached_path_pricing import normalize_path
from clamp import clamp_extend
from front_model import canonical,coefficients,project


def path_records(n,path,front=False):
    path=normalize_path(n,path)
    positions=[path['start_grid']]
    for step in path['moves']:positions.append(positions[-1]+step)
    R,C=2*n,4*n;center=positions.index(0);records=[]
    cutoff=next(j for j in range(center,C+1) if j+abs(positions[j])>=C) if front else C
    for sign,endpoint in ((1,-R),(-1,R)):
        end=positions.index(endpoint);previous=None
        for j in range(min(end,cutoff+1)):
            x=sign*positions[j]
            # Transport makes the price nondecreasing along this direction.
            # After center, a far-side price is >=1 while its record is <=1.
            update=(j==0 or (sign*path['moves'][j-1]<0 and not(j>center and x>=0)))
            if update:
                point=(j,abs(x)) if x else None
                if front and point is not None:point=canonical(n,point)
                coefficient=(1 if x>0 else -1) if point is not None else 0
                records.append({'point':point,'coefficient':coefficient,'previous':previous,'weight':0})
                previous=len(records)-1
            assert previous is not None
            records[previous]['weight']+=end-cutoff if j==cutoff else 1
    assert sum(r['weight'] for r in records)==positions.index(-R)+positions.index(R)
    return path,records


class RecordLP(EventLP):
    def __init__(self,master,floor,seconds=180.,level_fraction=.5,front=False):
        super().__init__(master,floor,seconds,level_fraction)
        self.front=front;self.path_seen=set();self.paths=[];self.record_variables=0
        self.main_events=[];self.prox_events=[];self.prox_anchors=[]
        self.records=[];self.record_index={};self.main_records=[];self.prox_records=[]

    def add_plane(self,plane):
        if self.front:
            coeff=coefficients(self.master.n,{(int(j),int(k)):Q(a) for j,k,a in plane['coefficients']})
            plane=dict(plane,coefficients=[[j,k,str(a)] for (j,k),a in sorted(coeff.items())])
        return super().add_plane(plane)

    def _sync(self):
        began=time.monotonic();fresh=[];old_records=len(self.records)
        for column in self.master.columns[self.bank_count:]:
            path,records=path_records(self.master.n,column['plan'],self.front)
            key=path['start_grid'],tuple(path['moves'])
            if key not in self.path_seen:
                self.path_seen.add(key);self.paths.append(path)
                local=[];weights={}
                for r in records:
                    previous=local[r['previous']] if r['previous'] is not None else None
                    key=(previous,r['point'],r['coefficient'])
                    # Equal causal record histories can share one auxiliary:
                    # all path floors are simultaneously feasible at their
                    # actual maximal records. Sharing changes no field set.
                    if previous is not None and (self.records[previous]['point'],self.records[previous]['coefficient'])==(r['point'],r['coefficient']):
                        index=previous
                    elif key in self.record_index:index=self.record_index[key]
                    else:
                        index=len(self.records);self.record_index[key]=index
                        self.records.append(dict(r,previous=previous))
                    local.append(index);weights[index]=weights.get(index,0)+r['weight']
                fresh.append(weights)
        attacks=self.attacks[self.attack_count:]
        new=sorted({r['point'] for r in self.records[old_records:] if r['point'] is not None and r['point'] not in self.index}|
                   {p for plane in attacks for p in plane['coeff'] if p not in self.index})
        old_count=len(self.nodes);count=len(new)
        if count:
            main_start=self.main.highs.getNumCol();prox_start=self.prox.highs.getNumCol()
            _check(self.main.highs.addCols(count,np.zeros(count),np.zeros(count),np.ones(count),
                0,np.zeros(count+1,dtype=np.int32),np.zeros(0,dtype=np.int32),np.zeros(0)),'append record-model field nodes')
            _check(self.prox.highs.addCols(3*count,np.tile([0.,1.,0.],count),np.zeros(3*count),
                np.tile([1.,np.inf,1.],count),0,np.zeros(3*count+1,dtype=np.int32),np.zeros(0,dtype=np.int32),np.zeros(0)),
                'append record-model prox nodes')
            rr=[];cc=[];vv=[]
            for offset,point in enumerate(new):
                self.index[point]=len(self.nodes);self.nodes.append(point)
                self.main_events.append(main_start+offset)
                g,u,a=prox_start+3*offset,prox_start+3*offset+1,prox_start+3*offset+2
                self.prox_events.append(g);self.prox_anchors.append(a)
                rr.extend((2*offset,)*3+(2*offset+1,)*3)
                cc.extend((g,u,a,g,u,a));vv.extend((1.,-1.,-1.,-1.,-1.,1.))
            self.prox.add_rows(coo_matrix((vv,(rr,cc)),shape=(2*count,self.prox.highs.getNumCol())),np.zeros(2*count))
            edges=[e for e in projected_order(self.master.n,self.nodes) if e not in self.edges]
        else:edges=[]
        record_count=len(self.records)-old_records
        main_record=self.main.highs.getNumCol();prox_record=self.prox.highs.getNumCol()
        if record_count:
            for lp in (self.main,self.prox):
                _check(lp.highs.addCols(record_count,np.zeros(record_count),np.zeros(record_count),2*np.ones(record_count),
                    0,np.zeros(record_count+1,dtype=np.int32),np.zeros(0,dtype=np.int32),np.zeros(0)),
                    'append exact path-record hypograph')
            self.main_records.extend(range(main_record,main_record+record_count))
            self.prox_records.extend(range(prox_record,prox_record+record_count))
        rr=[];main_cc=[];prox_cc=[];vv=[];rhs=[]
        def row(terms,bound):
            at=len(rhs);rhs.append(float(bound))
            for m,p,a in terms:rr.append(at);main_cc.append(m);prox_cc.append(p);vv.append(float(a))
        for a,b in edges:
            row([(self.main_events[a],self.prox_events[a],1),(self.main_events[b],self.prox_events[b],-1)],0)
        for i in range(old_records,len(self.records)):
            r=self.records[i];mc,pc=self.main_records[i],self.prox_records[i]
            if r['previous'] is not None:
                previous=r['previous'];row([(mc,pc,1),(self.main_records[previous],self.prox_records[previous],-1)],0)
            terms=[(mc,pc,1)]
            if r['point'] is not None:
                q=self.index[r['point']];terms.append((self.main_events[q],self.prox_events[q],-r['coefficient']))
            row(terms,1)
        for weights in fresh:
            row([(self.main_records[i],self.prox_records[i],-Q(weight,4*self.master.n)) for i,weight in weights.items()],-self.floor)
        for plane in attacks:
            terms=[(0,0,1)]
            for point,a in plane['coeff'].items():
                q=self.index[point];terms.append((self.main_events[q],self.prox_events[q],-a))
            row(terms,plane['constant'])
        self.main.add_rows(coo_matrix((vv,(rr,main_cc)),shape=(len(rhs),self.main.highs.getNumCol())),rhs)
        self.prox.add_rows(coo_matrix((vv,(rr,prox_cc)),shape=(len(rhs),self.prox.highs.getNumCol())),rhs)
        self.edges.update(edges);self.bank_count=len(self.master.columns);self.attack_count=len(self.attacks)
        self.record_variables+=record_count
        return time.monotonic()-began

    def solve(self,seed,screen,radius):
        assembly=self._sync();K=len(self.nodes)
        values=np.array([int(seed[j,k])/self.master.D for j,k in self.nodes])
        low=np.maximum(0.,values-radius);high=np.minimum(1.,values+radius)
        _check(self.main.highs.changeColsBounds(K,np.asarray(self.main_events,dtype=np.int32),low,high),'record field trust bounds')
        result=self.main.solve();_check(self.main.highs.setOptionValue('solver','simplex'),'record warm basis')
        events=result.x[np.asarray(self.main_events)];upper=float(-result.fun);level=upper
        stats=dict(self.main.last_stats,event_nodes=K,order_edges=len(self.edges),bank_model='all calendars via running-record hypographs',
                   physical_path_rows=len(self.paths),record_variables=self.record_variables,
                   continuous_plane_rows=self.attack_count,assembly_seconds=assembly,continuous_restricted_upper=upper)
        if upper>float(screen)+1e-9:
            level=float(screen)+self.level_fraction*(upper-float(screen))
            _check(self.prox.highs.changeColsBounds(K,np.asarray(self.prox_events,dtype=np.int32),low,high),'record level trust bounds')
            self.prox.fix_columns(np.r_[0,self.prox_anchors],np.r_[level,values])
            try:prox=self.prox.solve()
            except SolveError as error:stats['prox_failure']=str(error);level=upper
            else:
                events=prox.x[np.asarray(self.prox_events)]
                _check(self.prox.highs.setOptionValue('solver','simplex'),'record level warm basis')
                stats['prox']=dict(self.prox.last_stats,level=level,l1_event_displacement=float(np.abs(events-values).sum()))
        table,clamp=clamp_extend(self.master.n,self.master.D,self.nodes,events,seed)
        if self.front:
            projected=project(self.master.n,table)
            clamp.update(incoming_front='2',projection_changed_nodes=int(np.count_nonzero(projected!=table)))
            table=projected
        stats['exact_clamp']=clamp
        return table,upper,level,stats
