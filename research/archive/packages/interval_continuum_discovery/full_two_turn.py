"""Numerical discovery only: optimize fixed grid starts and one interior turn."""
import sys,json,time
from pathlib import Path
import numpy as np
from scipy.optimize import linprog
ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT/'packages/interval_uniform_reduction/research'),str(ROOT/'packages/interval_equilibrium_check/exploratory')]
from integer_deadline import Oracle
from integer_geometry import clean,mirror

n=int(sys.argv[1]);S=4*n;start=time.time();names=[];ps=[];seen=set()
for ix in range(-n,n+1):
 for ic in range(ix,2*n-ix+1):
  x=4*ix;c=4*ic
  q=[[0,x],[(c-x)//2,(c+x)//2],[c+S,-S],[c+3*S,S]]
  if c+x==2*S:q=q[:-1]
  q=clean(q);key=min(tuple(map(tuple,q)),tuple(map(tuple,mirror(q))))
  if key in seen:continue
  seen.add(key);names.append([ix/n,ic/n]);ps.append(q)
ms=[q for p in ps for q in (p,mirror(p))]
o=Oracle(ms,S);print('GEOMETRY',n,len(ps),len(o.graphs),'nodes',sum(g['t']+1 for g in o.graphs),'seconds',time.time()-start,flush=True)
rows=[];records=[];w=np.zeros(len(ps));w[names.index([-1.,3.])]=1.;v=0.
for it in range(160):
 rr=o.response(np.repeat(w/2,2));up=max(z['value'] for z in rr);add=0
 for z in rr:
  if z['value']<=v+1e-9:continue
  row=(np.array(z['r'][::2])+np.array(z['r'][1::2]))/(2*S)
  if any(np.max(abs(row-a))<1e-10 for a in rows):continue
  rows.append(row);records.append(z);add+=1
 print('ITER',it,'value',v,'upper',up,'rows',len(rows),'active',sum(w>1e-9),'add',add,'seconds',time.time()-start,flush=True)
 if not add:break
 A=np.array(rows);sol=linprog(np.r_[np.zeros(len(ps)),1.],A_ub=np.c_[A,-np.ones(len(rows))],b_ub=np.zeros(len(rows)),A_eq=[np.r_[np.ones(len(ps)),0]],b_eq=[1],bounds=[(0,None)]*len(ps)+[(None,None)],method='highs',options={'dual_feasibility_tolerance':1e-9,'primal_feasibility_tolerance':1e-9})
 assert sol.success,sol.message
 w=sol.x[:-1];v=sol.x[-1]
 json.dump(dict(n=n,S=S,value=v,upper=up,names=names,paths=ms,weights=w.tolist(),rows=A.tolist(),records=records,dual=(-sol.ineqlin.marginals).tolist()),open(Path(__file__).parent/f'full_two_turn_{n}.json','w'))
print('ACTIVE',[(names[i],float(z))for i,z in enumerate(w)if z>1e-8],flush=True)
