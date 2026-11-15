#!/usr/bin/env python3
"""Exact U=2 coefficient projection for the sufficient incoming-front class."""
from fractions import Fraction as Q
import numpy as np

import event_lp

_plan_column=event_lp.plan_column
_clamp_extend=event_lp.clamp_extend


def canonical(n,point):
    j,k=point;C=4*n
    if not k or j-k>=C:return None
    if j+k<=C:return j,k
    return (C+j-k)//2,(C-j+k)//2


def coefficients(n,coef):
    result={}
    for point,a in coef.items():
        target=canonical(n,point)
        if target is not None:result[target]=result.get(target,0)+a
    return {p:a for p,a in result.items() if a}


def project(n,table):
    result=table.copy()
    for j in range(table.shape[0]):
        for k in range(j%2,2*n+1,2):
            point=canonical(n,(j,k))
            result[j,k]=0 if point is None else table[point]
    return result


def front_column(n,plan):
    mass,coef=_plan_column(n,plan)
    return mass,coefficients(n,coef)


def front_clamp(n,D,nodes,values,seed):
    if any(canonical(n,p)!=p for p in nodes):raise ValueError('noncanonical front event')
    table,stats=_clamp_extend(n,D,nodes,values,seed)
    result=project(n,table)
    stats.update(incoming_front='2',projection_changed_nodes=int(np.count_nonzero(result!=table)),
                 sufficient_class_theorem='GLOBAL_INCOMING_FRONT_COMPLETION.md')
    return result,stats


class FrontEventLP(event_lp.EventLP):
    def add_plane(self,plane):
        coef=coefficients(self.master.n,{(int(j),int(k)):Q(a) for j,k,a in plane['coefficients']})
        return super().add_plane(dict(plane,coefficients=[[j,k,str(a)] for (j,k),a in sorted(coef.items())]))


def install():
    # This module is used only in the isolated front-search process. Source
    # modules remain unchanged and the native verifier still sees full tables.
    event_lp.plan_column=front_column
    event_lp.clamp_extend=front_clamp
    return FrontEventLP
