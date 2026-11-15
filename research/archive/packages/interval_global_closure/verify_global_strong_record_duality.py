"""Exact strict/closed radial identities and finite-selector LP dual regression.

Finite discretization is a regression, NOT a certificate for the full game.
Requires scipy for LP component. Exact contact/order fixtures use Fraction.
"""
from fractions import Fraction as Q
from itertools import product
import numpy as np
from scipy.optimize import linprog
import random

def radial_selector_value(p,x):
    a=int(p<x)+int(p>-x)
    r=abs(p)
    if x>0:
        b=1+int(r<x)
    elif x<0:
        b=int(r>-x)
    else:
        b=int(r>0)
    assert a==b
    return a

for ip,ix in product(range(-10,11),repeat=2):
    radial_selector_value(Q(ip,10),Q(ix,10))

step=Q(1,2)
times=[k*step for k in range(9)]
D=Q(4)
def interpolate(vertices,t):
    for (a,x),(b,y) in zip(vertices,vertices[1:]):
        if a<=t<=b:
            return x+(y-x)*(t-a)/(b-a)
    assert t>=vertices[-1][0]
    return vertices[-1][1]

monster_vertices=[
    [(Q(0),Q(-1)),(Q(2),Q(1)),(Q(4),Q(1))],
    [(Q(0),Q(1)),(Q(2),Q(-1)),(Q(4),Q(-1))],
    [(Q(0),Q(0)),(Q(1),Q(-1)),(Q(3),Q(1)),(Q(4),Q(1))],
    [(Q(0),Q(0)),(Q(1),Q(1)),(Q(3),Q(-1)),(Q(4),Q(-1))]
]
rng=random.Random(223311)
paths=[]
starts=[Q(-1),Q(-1,2),Q(0),Q(1,2),Q(1)]
for a in starts:
    paths.append([a for _ in times])
for a in starts:
    paths.append([max(Q(-1),min(Q(1),a+t)) for t in times])
    paths.append([max(Q(-1),min(Q(1),a-t)) for t in times])
for a in starts:
    v=a
    p=[v]
    for _ in times[1:]:
        v=max(Q(-1),min(Q(1),v+rng.choice([-step,Q(0),step])))
        p.append(v)
    paths.extend([p,[-x for x in p]])
paths=list(dict.fromkeys(tuple(p) for p in paths))
npth,nm,nt=len(paths),len(monster_vertices),len(times)
M=[[interpolate(vertices,t) for t in times] for vertices in monster_vertices]
assert all({Q(-1),Q(1)}.issubset(set(track)) for track in M)
assert all(all(abs(p[k]-p[k-1])<=step for k in range(1,nt)) for p in paths)

# Left-endpoint Riemann score; finite LP is a DIAGNOSTIC, not a game bound.
score_times=list(range(nt-1))
strict={};closed={}
for j,k,h in ((j,k,h) for j in range(nm) for k in score_times for h in range(k+1)):
    strict[(j,k,h)]=[int(p[h]<M[j][h]) for p in paths]
    closed[(j,k,h)]=[int(p[h]<=M[j][h]) for p in paths]

# Primal lifted-record program.
rec=[(j,k) for j in range(nm) for k in score_times]
nr=len(rec)
ac={v:npth+i for i,v in enumerate(rec)}
bc={v:npth+nr+i for i,v in enumerate(rec)}
cc=npth+2*nr
N=cc+1
A=[];B=[]
for j,k in rec:
    for h in range(k+1):
        row=np.zeros(N)
        row[ac[(j,k)]]=1
        row[:npth]-=strict[(j,k,h)]
        A.append(row);B.append(0.)
        row=np.zeros(N)
        row[bc[(j,k)]]=-1
        row[:npth]+=closed[(j,k,h)]
        A.append(row);B.append(0.)
for j in range(nm):
    row=np.zeros(N)
    row[cc]=1
    for k in score_times:
        row[ac[(j,k)]]-=float(step)
        row[bc[(j,k)]]+=float(step)
    A.append(row);B.append(float(D))
obj=np.zeros(N);obj[cc]=-1
Psol=linprog(obj,A_ub=np.array(A),b_ub=np.array(B),
    A_eq=np.array([[1.]*npth+[0.]*(N-npth)]),b_eq=[1.],
    bounds=[(0.,1.)]*npth+[(0.,1.)]*(2*nr)+[(0.,float(D))],method='highs')
assert Psol.success,Psol.message

# Dual joint causal selector distributions.
keys=list(strict)
Ndual=nm+2*len(keys)+1
low={v:nm+i for i,v in enumerate(keys)}
high={v:nm+len(keys)+i for i,v in enumerate(keys)}
zz=Ndual-1
Ae=[];Be=[]
row=np.zeros(Ndual);row[:nm]=1;Ae.append(row);Be.append(1.)
for j,k in rec:
    for inds in (low,high):
        row=np.zeros(Ndual)
        row[j]=-float(step)
        for h in range(k+1):
            row[inds[(j,k,h)]]=1
        Ae.append(row);Be.append(0.)
Ad=[];Bd=[]
for i in range(npth):
    row=np.zeros(Ndual);row[zz]=-1
    for v in keys:
        row[low[v]]+=strict[v][i]
        row[high[v]]-=closed[v][i]
    Ad.append(row);Bd.append(-float(D))
objd=np.zeros(Ndual);objd[zz]=1
Dsol=linprog(objd,A_ub=np.array(Ad),b_ub=np.array(Bd),
    A_eq=np.array(Ae),b_eq=np.array(Be),
    bounds=[(0.,1.)]*nm+[(0.,float(D))]*(2*len(keys))+[(0.,float(D))],
    method='highs')
assert Dsol.success,Dsol.message
assert abs(-Psol.fun-Dsol.fun)<1e-8

w=Psol.x[:npth]
for j in range(nm):
    exact_records=0.
    for k in score_times:
        a=min(np.dot(w,strict[(j,k,h)]) for h in range(k+1))
        b=max(np.dot(w,closed[(j,k,h)]) for h in range(k+1))
        exact_records+=float(step)*(1+a-b)
    lifted=sum(float(step)*(1+Psol.x[ac[(j,k)]]-Psol.x[bc[(j,k)]])
               for k in score_times)
    assert lifted<=exact_records+1e-8

for p,x in product([Q(-1),Q(-1,2),Q(0),Q(1,2),Q(1)],repeat=2):
    assert Q(1)+Q(int(p<x))-Q(int(p<=-x))==Q(radial_selector_value(p,x))

# Convert the solver outputs to genuine exact rational primal and dual
# witnesses, and check EVERY finite LP constraint with Fractions.
def rat(x):
    return Q(float(x)).limit_denominator(100000)
def dot(row,xs):
    return sum((rat(v)*xs[i] for i,v in enumerate(row) if v!=0),Q(0))
P=[rat(x) for x in Psol.x]
Z=[rat(x) for x in Dsol.x]
assert sum(P[:npth])==1 and sum(Z[:nm])==1
assert all(Q(0)<=v<=1 for v in P[:cc])
assert Q(0)<=P[cc]<=D and all(v>=0 for v in Z)
assert all(dot(row,P)<=rat(rhs) for row,rhs in zip(A,B))
assert all(dot(row,Z)<=rat(rhs) for row,rhs in zip(Ad,Bd))
assert all(dot(row,Z)==rat(rhs) for row,rhs in zip(Ae,Be))
assert P[cc]==Z[zz]==Q(3,2)

print("PASS: 441 exact strict/closed radial equality fixtures.")
print(f"PASS: {npth} Princess paths, {nm} completed Monsters, "
      f"{nt} time knots, {len(keys)} past selectors.")
print("PASS: rational primal/dual witnesses match at 3/2; all finite "
      "constraints independently verified in exact Fraction arithmetic.")
print("SCOPE: diagnostic finite-sample LP only; NOT an unrestricted bound.")
