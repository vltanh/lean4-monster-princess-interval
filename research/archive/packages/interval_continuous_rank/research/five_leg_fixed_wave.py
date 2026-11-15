"""Bounded structural test of one fixed-complexity continuous five-leg family.

No floating search here is an all-monster or game-value certificate.
"""
from pathlib import Path
import json,sys,time
import numpy as np
from scipy.optimize import minimize, differential_evolution, LinearConstraint
ROOT=Path(__file__).resolve().parents[3]
OUT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'packages/interval_continuous_rank'))
from continuous_rank import FiveLegLaw
Q=np.array([0.,.35,.75,1.]);N=4;GAP=1e-4
A2=1.001+Q*1e-6
NP=4*N+1
ANCHOR=np.r_[[.02,.4,.7,.96],[.45,.7,.88,.99],[.4,.25,.1,-.3],[.98,.9,.7,.1],.1]
BOUNDS=[(0,1)]*N+[(0,float(A2[-1]))]*N+[(-1,1)]*(2*N)+[(0,.4)]
rows=[];rhs=[];constraint_names=[]
def inequality(name,entries,value):
 row=np.zeros(NP)
 for i,coefficient in entries:row[i]=coefficient
 rows.append(row);rhs.append(value);constraint_names.append(name)
for block,sign,label in [(0,1,'a'),(N,1,'A1'),(2*N,-1,'C1'),(3*N,-1,'C2')]:
 for i in range(N-1):inequality(f'{label}_strict_{i}',[(block+i+1,sign),(block+i,-sign)],GAP)
for i in range(N):
 inequality(f'A1_ge_a_{i}',[(N+i,1),(i,-1)],0)
 inequality(f'A2_ge_A1_{i}',[(N+i,-1)],-A2[i])
 inequality(f'C1_ge_minus_a_{i}',[(2*N+i,1),(i,1)],0)
 inequality(f'C2_ge_C1_{i}',[(3*N+i,1),(2*N+i,-1)],0)
 inequality(f'first_peak_{i}',[(i,-1),(N+i,-1)],-2)
 inequality(f'second_peak_{i}',[(2*N+i,1)],A2[i]-2)
inequality('no_center_first_wave',[(N,1),(2*N,-1)],0)
M=np.asarray(rows);RHS=np.asarray(rhs)
PM=M.copy();PRHS=RHS.copy()
for i,(lo,hi) in enumerate(BOUNDS):
 row=np.zeros(NP);row[i]=1;PM=np.vstack([PM,row,-row]);PRHS=np.r_[PRHS,lo,-hi]
assert np.min(PM@ANCHOR-PRHS)>1e-3

def project(z):
 """Radial feasible extension toward a fixed strictly feasible anchor."""
 raw=np.asarray(z[:NP]);slack=PM@raw-PRHS-1e-11
 bad=slack<0
 if not np.any(bad):return raw
 anchor_slack=PM@ANCHOR-PRHS-1e-11
 fraction=float(np.max(-slack[bad]/(anchor_slack[bad]-slack[bad])))
 fraction=min(1.,fraction+1e-11)
 return (1-fraction)*raw+fraction*ANCHOR

def law_from(z):
 p=project(z)
 return FiveLegLaw(Q,p[:N],p[N:2*N],p[2*N:3*N],A2,p[3*N:4*N],p[-1],exact=False)

def law_data(law):
 return dict(q=list(law.q),a=list(law.a),A1=list(law.incoming[0]),C1=list(law.outgoing[0]),A2=list(law.incoming[1]),C2=list(law.outgoing[1]),endpoint_mass=law.endpoint_mass)

def clean(route):
 result=[]
 for t,x in route:
  t=float(t);x=float(x)
  if result and t<=result[-1][0]+1e-12:
   assert abs(x-result[-1][1])<1e-8
   continue
  result.append((t,x))
  if len(result)>=3:
   t0,x0=result[-3];t1,x1=result[-2];t2,x2=result[-1]
   if abs((x1-x0)*(t2-t1)-(x2-x1)*(t1-t0))<1e-11:
    result[-2:]=[(t2,x2)]
 return result

def via(positions):
 result=[(0.,float(positions[0]))];time0=0.
 for x in positions[1:]:
  time0+=abs(float(x)-result[-1][1]);result.append((time0,float(x)))
 return clean(result)
def m1(x):return via([x,1,-1])
def m2(x):return via([x,(1+x)/2,-1,1])
def shifted(eta):return clean([(0,-1+eta),(1,eta),(2+eta,-1),(4+eta,1)])

def moving_routes(law):
 result=[]
 for i,a in enumerate(law.a):
  for sign in [-1,1]:
   result.append((f'M1_a{i}_{sign}',m1(sign*a)))
   result.append((f'M2_a{i}_{sign}',m2(sign*a)))
 for i,c in enumerate(law.outgoing[0]):result.append((f'M2_C1_{i}',m2(-c)))
 for i,c in enumerate(law.outgoing[1]):
  result.append((f'M1_C2_{i}',m1(-c)))
  eta=float(np.clip(1-c,1e-8,1-1e-8))
  result.append((f'Q_C2_{i}',shifted(eta)))
 return result

def oracle(law,seed,deep=False):
 found=[]
 maxturns=4 if deep else 2
 cases=[(False,k,e) for k in range(maxturns+1) for e in [-1,1]]
 if deep:cases.extend((True,k,e) for k in range(1,5) for e in [-1,1])
 for j,(endpoint_start,k,end) in enumerate(cases):
  if endpoint_start:
   bounds=[(-1,1)]*k
   builder=lambda z,e=end:via([1]+list(z)+[e,-e])
  else:
   bounds=[(0,1)]+[(-1,1)]*k
   builder=lambda z,e=end:via(list(z)+[e,-e])
  def fun(z):return law.payoff(builder(z)).value
  opt=differential_evolution(fun,bounds,seed=seed+j,popsize=6,maxiter=26 if deep else 20,tol=1e-7,polish=True)
  route=builder(opt.x)
  found.append(dict(name=f'{k}turn_end{end}'+('_start1' if endpoint_start else ''),value=law.payoff(route).value,route=route))
 found.sort(key=lambda row:row['value'])
 return found

def optimize(seed,cuts,maxiter=60):
 law=law_from(seed)
 routes=cuts+moving_routes(law)
 value=min(law.payoff(route).value for _,route in routes)-1e-6
 initial=np.r_[seed[:NP],value]
 def constraints(z):
  law=law_from(z);routes=cuts+moving_routes(law)
  return np.asarray([law.payoff(route).value-z[-1] for _,route in routes])
 linear=np.c_[M,np.zeros(len(M))]
 # Clipping the moving Q parameter keeps the constraint count fixed.
 opt=minimize(lambda z:-z[-1],initial,method='SLSQP',bounds=BOUNDS+[(0,2)],
              constraints=[LinearConstraint(linear,RHS,np.inf),{'type':'ineq','fun':constraints}],
              options={'maxiter':maxiter,'ftol':2e-9})
 z=project(opt.x);law=law_from(z)
 values=[(name,law.payoff(route).value,route) for name,route in cuts+moving_routes(law)]
 return z,dict(success=bool(opt.success),message=str(opt.message),iterations=int(opt.nit),
               restricted_objective=float(opt.x[-1]),minimum_tested=float(min(v[1] for v in values)),
               raw_constraint_violation=float(np.min(M@opt.x[:NP]-RHS)),
               projection_distance=float(np.max(np.abs(z-opt.x[:NP]))),
               active=[dict(name=n,value=float(v),route=r) for n,v,r in values if v<=min(w[1] for w in values)+2e-5],
               active_parameter_constraints=[constraint_names[i] for i,v in enumerate(M@z-RHS) if v<2e-5])

def main():
 start=time.time();etas=[1/64,1/32,1/16,1/8,1/4,1/2]
 starts=sorted(set([i/8 for i in range(-8,9)]+[sign*(1-eta) for eta in etas for sign in [-1,1]]))
 cuts=[(f'M{kind}({x})',builder(x)) for kind,builder in [(1,m1),(2,m2)] for x in starts]
 cuts.extend((f'Q({eta})',shifted(eta)) for eta in etas)
 seeds=[ANCHOR,np.r_[[.001,.65,.9,.999],[.3,.75,.96,1.0001],[.25,.2,.1,-.2],[.999,.998,.8,-.1],.1]]
 history=[];seed_results=[]
 for index,seed in enumerate(seeds):
  z,summary=optimize(project(seed),cuts,maxiter=50)
  law=law_from(z);responses=oracle(law,820+100*index)
  row=dict(seed=index,seconds=time.time()-start,law=law_data(law),optimization=summary,responses=responses)
  seed_results.append((responses[0]['value'],z,row))
  print('SEED',index,'seconds',round(time.time()-start,1),'optimization',summary,flush=True)
  print('LAW',law_data(law),flush=True)
  print('WORST',responses[:3],flush=True)
 seed_results.sort(key=lambda item:item[0],reverse=True)
 _,z,chosen=seed_results[0]
 for index in range(3):
  if index==0:previous=chosen['responses']
  else:previous=history[-1]['responses']
  for response in previous[:6]:cuts.append((f'added_{index}_{response["name"]}',response['route']))
  z,summary=optimize(z,cuts,maxiter=65)
  law=law_from(z);responses=oracle(law,1120+100*index,deep=index==2)
  row=dict(round=index,seconds=time.time()-start,law=law_data(law),optimization=summary,responses=responses)
  history.append(row)
  output=dict(scope='Bounded fixed-complexity five-leg structural experiment; no game-value certificate.',epsilon=.001,q_knots=Q.tolist(),seed_results=[r[2] for r in seed_results],history=history)
  json.dump(output,open(OUT/'five_leg_fixed_wave.json','w'),indent=2)
  print('ROUND',index,'seconds',round(time.time()-start,1),'optimization',summary,flush=True)
  print('LAW',law_data(law),flush=True)
  for response in responses[:5]:print('RESPONSE',response,flush=True)
 print('DONE',time.time()-start,flush=True)
if __name__=='__main__':main()
