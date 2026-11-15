from symbolic import *
from poly_bridge import monster,matrix
from scipy.optimize import linprog
import json,time,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
D=json.load(open(ROOT/'support_16.json'));ms=[simplify([(P(str(t)),P(str(x))) for t,x in D['paths'][2*i]]) for i in range(len(D['weights']))]
D=json.load(open(ROOT/'princess_strategy.json'));hs=[simplify([(P(F(t)),P(F(x))) for t,x in p]) for p in D['paths'][::2]]
A=matrix(hs,ms);st=time.time();log=[]
def candidate(m):
 if m in ms or mirror(m) in ms or m in addedm or mirror(m) in addedm:return
 addedm.append(m)
for it in range(100):
 nh,nm=A.shape
 sol=linprog(np.r_[np.zeros(nm),1.],A_ub=np.column_stack([A,-np.ones(nh)]),b_ub=np.zeros(nh),A_eq=[np.r_[np.ones(nm),0]],b_eq=[1.],bounds=[(0,None)]*nm+[(None,None)],method='highs',options={'dual_feasibility_tolerance':1e-9,'primal_feasibility_tolerance':1e-9})
 assert sol.success,sol.message
 mw=np.maximum(0,sol.x[:-1]);mw/=mw.sum();hw=np.maximum(0,-sol.ineqlin.marginals);hw/=hw.sum();val=sol.x[-1]
 mi=np.where(mw>1e-8)[0];hi=np.where(hw>1e-8)[0]
 print('ITER',it,'matrix',A.shape,'active',len(hi),len(mi),'VALUE',val,'elapsed',time.time()-st,flush=True)
 am=[]
 for j in mi:am.extend([ms[j],mirror(ms[j])])
 oracle=HalfOracle(am);resp=oracle.response(np.repeat(mw[mi]/2,2));U=max(z['value'] for z in resp)
 addedh=[]
 for r in resp:
  if r['value']>val+1e-7:
   p=witness_play(am,r['r'],r['initial'],delta=P(F(1,1000000)))
   if p not in hs+addedh:addedh.append(p)
 ah=[];aw=[]
 for j in hi:ah.extend([hs[j],mirror(hs[j])]);aw.extend([hw[j]/2]*2)
 ah += [[(P(0),P(-1))],[(P(0),P(1))]];aw +=[0.,0.]
 br=monster(ah,aw,limit=500000);L=br['value'];m=complete(br['path']);addedm=[]
 if L<val-1e-7:candidate(m)
 starts=sorted(set([p[0][1] for p in hs+addedh]+[-p[0][1] for p in hs+addedh]))
 # Add translations of the same two-turn topology at all hider starts.
 if len(m)==4:
  if m[1][1]<m[0][1]:m=mirror(m)
  c=m[1][0]+m[1][1]
  for x in starts:
   if x<c and c+x<2:
    q=simplify([(P(0),x),((c-x)/2,(c+x)/2),(c+1,P(-1)),(c+3,P(1))]);candidate(q)
 for x in starts:
  if -1<=x<1:candidate(simplify([(P(0),x),(1-x,P(1)),(3-x,P(-1))]))
 # Select only improving columns against the current dual, retaining the unrestricted response.
 if addedm:
  b=matrix([hs[i] for i in hi],addedm);vals=hw[hi]@b
  addedm=[q for q,v in zip(addedm,vals) if v<val-1e-7]
 print(' RESPONSE',L,U,'complete',br['complete'],'nodes',br['nodes'],'add',len(addedh),len(addedm),'m',[(float(t),float(x)) for t,x in m],flush=True)
 log.append(dict(iteration=it,value=val,upper=U,lower_candidate=L,complete=br['complete'],matrix=[nh,nm],active=[len(hi),len(mi)],nodes=br['nodes']))
 json.dump(dict(paths_m=[encode(m) for m in ms],paths_h=[encode(p) for p in hs],weights_m=mw.tolist(),weights_h=hw.tolist(),matrix=A.tolist(),log=log),open(ROOT/'play_checkpoint.json','w'))
 if not addedh and not addedm:print('STOP',flush=True);break
 if addedh:A=np.vstack([A,matrix(addedh,ms)]);hs+=addedh
 if addedm:A=np.column_stack([A,matrix(hs,addedm)]);ms+=addedm
