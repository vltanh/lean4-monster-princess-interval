"""Bounded continuous-law structural experiment; no game-value certificate."""
import json,sys,time
from pathlib import Path
import numpy as np
from scipy.optimize import minimize, differential_evolution, LinearConstraint
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'packages/interval_continuous_rank'))
from continuous_rank import RankLaw
OUT=Path(__file__).resolve().parent
Q=np.array([0.,.35,.75,1.]);N=len(Q);EPS=1e-4
rows=[];lbs=[]
for block,sign in [(0,1),(N,1),(2*N,-1)]:
 for i in range(N-1):
  row=np.zeros(3*N+2);row[block+i+1]=sign;row[block+i]=-sign;rows.append(row);lbs.append(EPS)
for i in range(N):
 row=np.zeros(3*N+2);row[N+i]=1;row[i]=-1;rows.append(row);lbs.append(0)
 row=np.zeros(3*N+2);row[2*N+i]=1;row[i]=1;rows.append(row);lbs.append(0)
M=np.asarray(rows);LB=np.asarray(lbs)
BOUNDS=[(0,1)]*N+[(0,2)]*N+[(-1,1)]*N+[(0,.4),(0,2)]

def make_law(z):
 # Projection only extends the objective to infeasible SLSQP trial points.
 # The reported final vector is checked against all original inequalities.
 tiny=1e-10
 a=np.sort(np.clip(z[:N],N*tiny,1-N*tiny))
 for i in range(N-2,-1,-1):a[i]=min(a[i],a[i+1]-tiny)
 u=np.maximum(np.sort(z[N:2*N]),a)
 for i in range(1,N):u[i]=max(u[i],u[i-1]+tiny)
 c=np.minimum(np.sort(np.clip(z[2*N:3*N],-1,1))[::-1],1.)
 for i in range(1,N):c[i]=min(c[i],c[i-1]-tiny)
 c=np.maximum(c,-a)
 return RankLaw(Q,a,u,c,np.clip(z[3*N],0,1),exact=False)

def clean(route):
 result=[]
 for t,x in route:
  t=float(t);x=float(x)
  if result and t<=result[-1][0]+1e-11:
   assert abs(x-result[-1][1])<1e-7
   continue
  result.append((t,x))
  if len(result)>=3:
   t0,x0=result[-3];t1,x1=result[-2];t2,x2=result[-1]
   if abs((x1-x0)*(t2-t1)-(x2-x1)*(t1-t0))<1e-10:
    result[-2:]=[(t2,x2)]
 return result

def position_route(pos):
 t=0.;r=[(t,pos[0])]
 for x in pos[1:]:
  t+=abs(x-r[-1][1]);r.append((t,x))
 return clean(r)

def centered(z,signs,final):
 x=z[0];t=x;r=[(0.,x),(t,0.)];j=1
 for sign in signs:
  wait,height=z[j:j+2];j+=2
  t+=wait;r.append((t,0.));t+=height;r.append((t,sign*height));t+=height;r.append((t,0.))
 t+=z[j];r.append((t,0.));t+=1;r.append((t,float(final)));t+=2;r.append((t,float(-final)))
 return clean(r)

def oracle(law,seed,deep=False):
 families=[]
 for k in range(4 if deep else 3):
  for endpoint in [-1,1]:
   families.append((f'{k}turn_end{endpoint}',[(0,1)]+[(-1,1)]*k,
    lambda z,e=endpoint:position_route(list(z)+[e,-e])))
 for sign in [-1,1]:
  for final in [-1,1]:
   families.append((f'center1_{sign}_{final}',[(0,1),(0,1),(0,1),(0,1)],
    lambda z,sg=sign,f=final:centered(z,[sg],f)))
 if deep:
  for s1 in [-1,1]:
   for s2 in [-1,1]:
    for final in [-1,1]:
     families.append((f'center2_{s1}_{s2}_{final}',[(0,1),(0,1),(0,.5),(0,1),(0,.5),(0,1)],
      lambda z,sg=[s1,s2],f=final:centered(z,sg,f)))
 found=[]
 for j,(name,bounds,builder) in enumerate(families):
  def fun(z):return law.payoff(builder(z)).value
  opt=differential_evolution(fun,bounds,seed=seed+j,popsize=5,maxiter=24 if deep else 18,
                             tol=1e-7,polish=True,updating='immediate')
  route=builder(opt.x);value=law.payoff(route).value
  found.append(dict(name=name,value=value,route=route))
 found.sort(key=lambda d:d['value'])
 return found

def initial():
 D=json.load(open(ROOT/'packages/interval_uniform_reduction/princess_strategy.json'))
 paths=[np.asarray(path,dtype=float)/D['S'] for path in D['paths_h']]
 weights=np.asarray(D['weights_h'],dtype=float)/D['weight_total']
 aa=np.asarray([path[0,1] for path in paths])
 cc=np.asarray([path[np.flatnonzero(path[:,1]>=1)[0],0]-1 for path in paths])
 times=np.linspace(0,2,257);uu=[]
 for path,initial_a,final_c in zip(paths,aa,cc):
  target=np.interp(times,path[:,0],path[:,1]);choices=np.linspace(initial_a,1,501)
  predicted=np.minimum(1,np.maximum(np.maximum(np.minimum(initial_a+times[None,:],choices[:,None]-times[None,:]),times[None,:]-final_c),0))
  uu.append(choices[np.mean((predicted-target)**2,axis=1).argmin()])
 assert aa[-1]==1 and np.all(paths[-1][:,1]==1)
 w=weights[:-1];a=aa[:-1];u=np.asarray(uu[:-1]);c=cc[:-1];lam=float(weights[-1]);q=(np.cumsum(w)-w/2)/(1-lam)
 H=np.stack([np.interp(q,Q,np.eye(N)[i]) for i in range(N)],1)
 target=np.r_[a,u,c]
 def loss(z):return sum(np.sum(w*(H@z[k*N:(k+1)*N]-y)**2) for k,y in enumerate([a,u,c]))
 z=np.r_[*[np.linalg.lstsq(H*w[:,None]**.5,y*w**.5,rcond=None)[0] for y in [a,u,c]],lam,1.3]
 z[0]=max(0,z[0]);z[N-1]=min(1,z[N-1]);z[2*N:3*N]=np.clip(z[2*N:3*N],-1,1)
 fit=minimize(loss,z,method='SLSQP',bounds=BOUNDS,constraints=[LinearConstraint(M,LB,np.inf)],options={'maxiter':150,'ftol':1e-11})
 print('FIT',fit.success,fit.fun,fit.x.tolist(),flush=True)
 return fit.x

def description(law):
 return dict(q=list(law.q),a=list(law.a),u=list(law.u),c=list(law.c),endpoint_mass=law.endpoint_mass)

def main():
 start=time.time();z=initial();history=[];cuts=[]
 for x in [0,.25,.5,.625,.75,.875,1]:
  for e in [-1,1]:cuts.append(position_route([x,e,-e]))
  cuts.append(position_route([x,-(1-x)/2,1,-1]))
 cuts.append([(0.,0.),(.8,0.),(1.8,1.),(3.8,-1.)])
 for iteration in range(4):
  law=make_law(z);z[-1]=min(law.payoff(r).value for r in cuts)-1e-6
  def constraint(x):
   l=make_law(x)
   return np.asarray([l.payoff(route).value-x[-1] for route in cuts])
  opt=minimize(lambda x:-x[-1],z,method='SLSQP',bounds=BOUNDS,
               constraints=[LinearConstraint(M,LB,np.inf),{'type':'ineq','fun':constraint}],
               options={'maxiter':100,'ftol':2e-9})
  z=opt.x;law=make_law(z);found=oracle(law,117+100*iteration,deep=iteration==3)
  active=[dict(value=law.payoff(r).value,route=r) for r in cuts if law.payoff(r).value<=z[-1]+2e-5]
  event=dict(iteration=iteration,seconds=time.time()-start,optimizer_success=bool(opt.success),
             constraint_violation=float(min(np.min(M@z-LB),np.min(constraint(z)))),
             restricted_objective=float(z[-1]),law=description(law),active=active,
             responses=found)
  history.append(event)
  json.dump(dict(scope='Finite bounded structural search, not an all-monster certificate.',history=history),open(OUT/'continuous_candidate.json','w'),indent=2)
  print('ROUND',iteration,'secs',round(time.time()-start,1),'success',opt.success,'violation',event['constraint_violation'],'restricted',z[-1],flush=True)
  print('LAW',description(law),flush=True)
  for item in found[:6]:print('RESPONSE',item,flush=True)
  existing={str(np.round(r,8).tolist()) for r in cuts}
  for item in found[:8]:
   route=item['route'];key=str(np.round(route,8).tolist())
   if key not in existing and item['value']<z[-1]-1e-7:
    cuts.append(route);existing.add(key)
 print('DONE',time.time()-start,flush=True)
if __name__=='__main__':main()
