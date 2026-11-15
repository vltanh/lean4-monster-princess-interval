from network_transport import Network,LP
from integer_geometry import clean,mirror,complete,witness,br,br_batch
from integer_deadline import Oracle
import json,numpy as np,time,sys
S=2**140*5**6
D=json.load(open('adaptive_inner.json' if '--inner' in sys.argv else 'adaptive_checkpoint.json' if '--resume' in sys.argv else 'network_old.json'));scale=S//D['S'];assert scale*D['S']==S
basis=[[[t*scale,x*scale]for t,x in p]for p in D['basis'] if True] if '--inner' in sys.argv else [[[t*scale,x*scale]for t,x in p]for p in D['paths_h']]
monsters=[[[t*scale,x*scale]for t,x in p]for p in D['paths_m']]
weights=D['weights_m'];outerlog=D.get('outerlog',[]);st=time.time()
start=0
if '--inner' in sys.argv:
 outerlog=json.load(open('adaptive_checkpoint.json'))['outerlog'];start=D['outer']
if '--resume' in sys.argv:
 am=[];aw=[]
 for m,w in zip(monsters,weights):
  if w>1e-8:am.extend([m,mirror(m)]);aw.extend([w/2,w/2])
 aw=np.array(aw);aw/=aw.sum();rr=Oracle(am,S).response(aw);oldv=outerlog[-1]['matrix']
 added=[witness(am,r['r'],r['initial'],S)for r in rr if r['value']>oldv+1e-6]
 basis+=added;start=outerlog[-1]['outer']+1
for outer in range(start,start+30):
 net=Network(basis,S);print('NETWORK',outer,'basis',len(basis),'slabs',len(net.slabs),'faces',net.NF,'H',net.H/S,'elapsed',time.time()-st,flush=True)
 l=LP(net)
 for m in monsters:l.add(m)
 log=[]
 for it in range(200):
  v,F,mw=l.solve();hs,ws,err=net.quantiles(F);full=[mirror(p)for p in hs[::-1]]+hs;fw=np.r_[ws[::-1],ws]/2
  ans,info=br_batch(full,fw,S,limit=30_000_000);val,m=min(ans,key=lambda z:z[0]);assert abs(val-net.payoff(m,F))<1e-6
  print('LP',outer,it,'v',v,'L',val,'h',len(hs),'m',len(l.ms),'faces',net.NF,'nodes',info['nodes'],'done',info['complete'],'elapsed',time.time()-st,flush=True)
  log.append(dict(it=it,value=v,response=val,**info))
  json.dump(dict(S=S,basis=basis,F=F.tolist(),paths_h=hs,weights_h=ws.tolist(),paths_m=l.ms,weights_m=mw.tolist(),log=log,outer=outer),open('adaptive_inner.json','w'))
  if not info['complete']:break
  if v-val<3e-7:break
  new=sum(l.add(complete(p,S))for a,p in ans if a<v-1e-7)
  if not new:print('REPEATED',flush=True);break
 if not info['complete']:break
 active=[j for j,w in enumerate(mw)if w>1e-8];ams=[];ww=[]
 for j in active:ams.extend([l.ms[j],mirror(l.ms[j])]);ww.extend([mw[j]/2,mw[j]/2])
 ww=np.array(ww);ww/=ww.sum();oracle=Oracle(ams,S);resp=oracle.response(ww);U=max(r['value']for r in resp)
 print('CHECK',outer,'L',val,'matrix',v,'U',U,'active_m',len(active),'chambers',len(resp),'elapsed',time.time()-st,flush=True)
 outerlog.append(dict(outer=outer,lower=val,matrix=v,upper=U,active_m=len(active),network_faces=net.NF,network_basis=len(basis),hiders=len(hs),log=log))
 json.dump(dict(S=S,basis=basis,F=F.tolist(),paths_h=hs,weights_h=ws.tolist(),paths_m=l.ms,weights_m=mw.tolist(),outerlog=outerlog),open('adaptive_checkpoint.json','w'))
 if U-val<1e-7:print('MATCH',flush=True);break
 added=[]
 for r in resp:
  if r['value']>v+1e-6:
   p=witness(ams,r['r'],r['initial'],S,style='play')
   if p not in hs+added:added.append(p)
 print('ADD',len(added),flush=True)
 if not added:print('NO NEW PATH',flush=True);break
 # Retain all current positive quantile paths; discarded zero-flow edges are unnecessary for this candidate.
 basis=hs+added;monsters=l.ms
