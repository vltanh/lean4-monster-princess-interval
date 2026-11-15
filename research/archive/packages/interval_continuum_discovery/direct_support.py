"""Floating discovery LP: feasible flow certificate for every start chamber."""
import sys,json,time
from pathlib import Path
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix
ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT/'packages/interval_uniform_reduction/research'),str(ROOT/'packages/interval_equilibrium_check/exploratory')]
from integer_deadline import Oracle
from integer_geometry import clean,mirror

def solve_support(ms,S):
 st=time.time();o=Oracle(ms,S);npair=len(ms)//2
 starts=[];nv=npair+1;nr=1
 for g in o.graphs:starts.append((nv,nr));nv+=len(g['us']);nr+=g['s']+1
 er=[];ec=[];ev=[];rhs=[1.]+[0.]*(nr-1);ur=[];uc=[];uv=[];ubs=[]
 bounds=[(0,1)]*npair+[(0,o.H/S)]+[(0,None)]*(nv-npair-1)
 for j in range(npair):er.append(0);ec.append(j);ev.append(1.)
 for g,(vbase,rbase) in zip(o.graphs,starts):
  for k,(u,v,cap,owner)in enumerate(zip(g['us'],g['vs'],g['co'],g['owners'])):
   var=vbase+k
   if u!=g['t']:er.append(rbase+u);ec.append(var);ev.append(1.)
   if v!=g['t']:er.append(rbase+v);ec.append(var);ev.append(-1.)
   if owner>=0:
    row=len(ubs);ur.extend([row,row]);uc.extend([var,int(owner)//2]);uv.extend([1.,-cap/2]);ubs.append(0.)
   else:bounds[var]=(0,cap)
  er.append(rbase+g['s']);ec.append(npair);ev.append(1.);rhs[rbase+g['s']]=o.H/S
 Aeq=coo_matrix((ev,(er,ec)),shape=(nr,nv)).tocsr();Aub=coo_matrix((uv,(ur,uc)),shape=(len(ubs),nv)).tocsr()
 obj=np.zeros(nv);obj[npair]=1.
 print('DIRECT',len(ms),len(o.graphs),'vars',nv,'eq',nr,'ub',len(ubs),'seconds',time.time()-st,flush=True)
 sol=linprog(obj,A_ub=Aub,b_ub=ubs,A_eq=Aeq,b_eq=rhs,bounds=bounds,method='highs-ipm',options={'dual_feasibility_tolerance':1e-9,'primal_feasibility_tolerance':1e-9,'ipm_optimality_tolerance':1e-10,'threads':1})
 assert sol.success,sol.message
 w=sol.x[:npair];r=o.response(np.repeat(w/2,2));u=max(z['value']for z in r)
 print('RESULT',sol.fun,'UPPER',u,'seconds',time.time()-st,flush=True)
 return dict(S=S,value=sol.fun,upper=u,weights=w.tolist(),paths=ms,responses=r)

if __name__=='__main__':
 n=int(sys.argv[1]);S=4*n;names=[];ps=[];seen=set()
 for ix in range(-n,n+1):
  for ic in range(ix,2*n-ix+1):
   x=4*ix;c=4*ic;q=[[0,x],[(c-x)//2,(c+x)//2],[c+S,-S],[c+3*S,S]]
   if c+x==2*S:q=q[:-1]
   q=clean(q);key=min(tuple(map(tuple,q)),tuple(map(tuple,mirror(q))))
   if key in seen:continue
   seen.add(key);names.append([ix/n,ic/n]);ps.append(q)
 ms=[q for p in ps for q in(p,mirror(p))]
 d=solve_support(ms,S);d['names']=names;d['n']=n
 print('ACTIVE',[(names[i],z)for i,z in enumerate(d['weights'])if z>1e-8],flush=True)
 json.dump(d,open(Path(__file__).parent/f'direct_support_{n}.json','w'))
