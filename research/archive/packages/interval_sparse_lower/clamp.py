#!/usr/bin/env python3
"""Exact closest-seed extension of selected Qout nodal values.

Forward max closure supplies lower envelopes, reverse min closure upper
envelopes. Pointwise clamping of an isotone seed between these two isotone
fields is legal and agrees with every repaired selected value.
"""
from __future__ import annotations

import numpy as np


def forward(table, n):
    R,C=2*n,4*n
    for k in range(2,R+1):
        js=np.arange(k%2,C+1,2)
        left=js[js>0];right=js[js<C]
        table[left,k]=np.maximum(table[left,k],table[left-1,k-1])
        table[right,k]=np.maximum(table[right,k],table[right+1,k-1])
    for j in range(C-2,-1,-2):
        table[j,R]=max(table[j,R],table[j+2,R])
    return table


def backward(table,n):
    R,C=2*n,4*n
    for j in range(2,C+1,2):
        table[j,R]=min(table[j,R],table[j-2,R])
    for k in range(R-1,0,-1):
        js=np.arange(k%2,C+1,2)
        left=js[js>0];right=js[js<C]
        table[left,k]=np.minimum(table[left,k],table[left-1,k+1])
        table[right,k]=np.minimum(table[right,k],table[right+1,k+1])
    return table


def validate_pre_two(table,n,D):
    R,C=2*n,4*n
    assert table.shape==(C+1,R+1)
    assert np.min(table)>=0 and np.max(table)<=D
    assert np.all(table[:,0]==0)
    for k in range(1,R):
        js=np.arange(k%2,C+1,2)
        for step in (-1,1):
            source=js[(js+step>=0)&(js+step<=C)]
            assert np.all(table[source,k]<=table[source+step,k+1])
    assert np.all(table[2:C+1:2,R]<=table[0:C-1:2,R])


def clamp_extend(n,D,nodes,values,seed):
    """Return exact legal full table and rational-rounding diagnostics.

    `values` are floating discovery output. The complete native oracle must
    price the returned table before it carries a game-value lower.
    """
    R,C,H=2*n,4*n,12*n
    seed=np.asarray(seed,dtype=np.uint64)
    if seed.shape!=(H+1,R+1):
        raise ValueError('wrong full seed shape')
    validate_pre_two(seed[:C+1],n,D)
    integers=[min(D,max(0,int(np.floor(float(v)*D)))) for v in values]
    if len(nodes)!=len(integers) or len(set(nodes))!=len(nodes):
        raise ValueError('selected event/value mismatch')
    lower=np.zeros((C+1,R+1),dtype=np.uint64)
    for (j,k),value in zip(nodes,integers):
        if not (0<=j<=C and 1<=k<=R and (j+k)%2==0):
            raise ValueError('invalid selected event')
        lower[j,k]=value
    forward(lower,n)
    repaired=[int(lower[j,k]) for j,k in nodes]
    upper=np.full((C+1,R+1),D,dtype=np.uint64)
    upper[:,0]=0
    for (j,k),value in zip(nodes,repaired):
        upper[j,k]=value
    backward(upper,n)
    legal_mask=np.fromfunction(lambda j,k:(j+k)%2==0,(C+1,R+1),dtype=int)
    assert np.all(lower[legal_mask]<=upper[legal_mask])
    before=np.maximum(lower,np.minimum(seed[:C+1],upper))
    before[~legal_mask]=0
    validate_pre_two(before,n,D)
    for (j,k),value in zip(nodes,repaired):
        assert int(before[j,k])==value
    table=np.zeros((H+1,R+1),dtype=np.uint64)
    table[:C+1]=before
    for j in range(C+1,C+R+1):
        ks=np.arange(1+(j+1)%2,R+1,2)
        ks=ks[ks>j-C]
        table[j,ks]=table[C,ks-j+C]
    delta=np.abs(before.astype(np.int64)-seed[:C+1].astype(np.int64))
    return table,{
        'event_nodes':len(nodes),
        'event_rounding_closure_max_units':max((b-a for a,b in zip(integers,repaired)),default=0),
        'maximum_seed_displacement_units':int(delta.max()),
        'sum_seed_displacement_units':str(int(delta.sum())),
        'changed_pre_two_nodes':int(np.count_nonzero(delta)),
        'denominator':str(D),
        'same_cdf_security_claimed':False}
