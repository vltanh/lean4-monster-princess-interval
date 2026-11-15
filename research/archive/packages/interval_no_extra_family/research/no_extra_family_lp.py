"""Exact affine-arrangement LP for p(a,c)=clip(max(a-t,t-c,0))."""
from fractions import Fraction as F
from pathlib import Path
import json,time
import numpy as np
from scipy.optimize import linprog
OUT=Path(__file__).resolve().parent

def A(z,a,c,pa,pc):
 if z<=pa:return 0.
 if z<=pc:return z
 if z<=pc+2:return (z+c)/2
 return z-1

def B(z,a,c,pa,pc):
 if z<=-pa:return 0.
 if z>pc:return z+1
 if z>=pa:return z
 return (z+a)/2

def payoff(a,c,pa,pc,kind,x):
 if kind==1:
  p=B(-x,a,c,pa,pc) if x<pa else A(2-x,a,c,pa,pc)
  n=A(-x,a,c,pa,pc) if x<-pa else B(2-x,a,c,pa,pc)
  return (p+n)/2
 if kind==2:
  p=B(3,a,c,pa,pc) if x<-pc else B(-x,a,c,pa,pc) if x<pa else A(1,a,c,pa,pc)
  n=A(-x,a,c,pa,pc) if x<-pa else B(1,a,c,pa,pc)
  return (p+n)/2
 if pa<=x and pa<=pc:return a
 if pa>x and pc>=x:return a/4+3*x/4+1.5
 return x+2

def clip(poly,aa,cc,offset):
 result=[]
 for p,q in zip(poly,poly[1:]+poly[:1]):
  fp=aa*p[0]+cc*p[1]+offset;fq=aa*q[0]+cc*q[1]+offset
  if fp>=0:result.append(p)
  if (fp>0 and fq<0) or(fp<0 and fq>0):
   t=fp/(fp-fq);result.append((p[0]+t*(q[0]-p[0]),p[1]+t*(q[1]-p[1])))
 clean=[]
 for p in result:
  if p not in clean:clean.append(p)
 return clean

def arrangement(starts,waits):
 aa=sorted(set([0.,1.]+[abs(x) for x in starts]+list(waits)))
 cc=sorted(set([-1.,1.]+[-x for x in starts]+list(waits)))
 rows=[];seen=set();cells=0
 for a0,a1 in zip(aa,aa[1:]):
  for c0,c1 in zip(cc,cc[1:]):
   rect=[(a0,c0),(a1,c0),(a1,c1),(a0,c1)]
   for sign in [-1,1]:
    poly=clip(clip(rect,1,1,0),-sign,sign,0)
    if len(poly)<3:continue
    area=sum(p[0]*q[1]-p[1]*q[0] for p,q in zip(poly,poly[1:]+poly[:1]))
    if abs(area)<1e-16:continue
    cells+=1;pa=sum(p[0] for p in poly)/len(poly);pc=sum(p[1] for p in poly)/len(poly)
    for a,c in poly:
     key=(a,c,pa,pc)
     if key not in seen:rows.append(key);seen.add(key)
 return rows,cells

def rational_solution(matrix,sol):
 import sympy as sp
 support=np.flatnonzero(sol.x[:-1]>1e-9)
 value=sol.x[-1];active=np.flatnonzero(matrix@sol.x[:-1]>=value-2e-8)
 candidates=sorted(active,key=lambda i:sol.ineqlin.marginals[i])
 rr=[np.r_[np.ones(len(support)),0.]];chosen=[];rank=1
 for i in candidates:
  row=np.r_[matrix[i,support],-1.]
  newrank=np.linalg.matrix_rank(np.vstack(rr+[row]),tol=1e-10)
  if newrank>rank:rr.append(row);chosen.append(int(i));rank=newrank
  if rank==len(support)+1:break
 assert rank==len(support)+1,(rank,len(support))
 D=256
 exact=sp.Matrix([[1]*len(support)+[0]]+[[int(round(D*matrix[i,j])) for j in support]+[-D] for i in chosen])
 ans=list(exact.inv()*sp.Matrix([1]+[0]*len(support)))
 weights=[F(str(v)) for v in ans[:-1]];v=F(str(ans[-1]));assert min(weights)>=0 and sum(weights)==1
 ceiling=max(sum(F(int(round(D*matrix[i,j])),D)*w for j,w in zip(support,weights)) for i in range(len(matrix)))
 assert ceiling<=v,(ceiling,v)
 return support,weights,v,chosen

def main():
 start=time.time();etas=[1/64,1/32,1/16,1/8,1/4,1/2]
 starts=sorted(set([i/8 for i in range(-8,9)]+[sign*(1-e) for e in etas for sign in [-1,1]]));waits=[0.,.25,.5,.75,1.]
 monsters=[(k,x) for k in [1,2] for x in starts]+[(3,t) for t in waits]
 rows,cells=arrangement(starts,waits)
 matrix=np.asarray([[payoff(*row,*monster) for monster in monsters] for row in rows])
 assert np.max(np.abs(matrix*256-np.round(matrix*256)))<1e-9
 sol=linprog(np.r_[np.zeros(len(monsters)),1.],A_ub=np.c_[matrix,-np.ones(len(rows))],b_ub=np.zeros(len(rows)),A_eq=[np.r_[np.ones(len(monsters)),0]],b_eq=[1],bounds=[(0,None)]*len(monsters)+[(None,None)],method='highs')
 assert sol.success,sol.message
 support,weights,v,chosen=rational_solution(matrix,sol)
 result=dict(scope='Exact affine-arrangement response ceiling for the specified two-parameter princess family, not the unrestricted game.',cells=cells,row_count=len(rows),value=str(v),decimal=float(v),monsters=[dict(kind=monsters[i][0],parameter=str(F(monsters[i][1])),weight=str(w)) for i,w in zip(support,weights)],starts=[str(F(x)) for x in starts],waits=[str(F(x)) for x in waits],binding_rows=[dict(a=str(F(rows[i][0])),c=str(F(rows[i][1])),probe_a=rows[i][2],probe_c=rows[i][3]) for i in chosen],seconds=time.time()-start)
 json.dump(result,open(OUT/'no_extra_family_lp.json','w'),indent=2)
 print(json.dumps(result,indent=2),flush=True)
if __name__=='__main__':main()
