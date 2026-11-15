from network_transport import Network,LP
from integer_geometry import clean,mirror,complete,br_batch
from integer_deadline import Oracle
import json,numpy as np,time,sys
from fractions import Fraction as Q
n=int(sys.argv[1]);S=2**140*5**6;eps=S//1_000_000;T=S;st=time.time();basis=[]
def add(p):
 p=clean(p)
 if p not in basis:basis.append(p)
add([[0,S]])
lo=eps;hi=S-eps
for j in range(0,2*n+1):
 for shift in(-eps,0,eps):
  c=j*S//n+shift;a=max(0,c-hi);b=min(T,c-lo)
  if b>a:
   x=c-a;y=c-b;add([[0,x],[a,x],[b,y],[b+S-y,S]])
for j in range(-n,n+1):
 for shift in(-eps,0,eps):
  c=j*S//n+shift;a=max(0,c+lo);b=min(T,c+hi)
  if b>a:
   x=a-c;y=b-c;add([[0,x],[a,x],[b,y],[b+S-y,S]])
for j in range(n+1):
 for shift in(-eps,0,eps):
  x=min(hi,max(lo,j*S//n+shift));add([[0,x],[T,x],[T+S-x,S]])
net=Network(basis,S);print('BEAM NETWORK',n,'basis',len(basis),'beams',len(net.segs),'faces',net.NF,'slabs',len(net.slabs),'secs',time.time()-st,flush=True)
l=LP(net)
D=json.load(open('network_old.json'));mul=S//D['S'];assert mul*D['S']==S
for m in D['paths_m']:l.add(complete([[t*mul,x*mul]for t,x in m],S))
starts=sorted(set(p[0][1]for p in basis))
for x in starts:
 for c in [x,2*S-x,S-eps,S,S+eps]:
  if x<=c<=2*S-x:
   assert (c-x)%2==0
   l.add(complete(clean([[0,x],[(c-x)//2,(c+x)//2],[c+S,-S],[c+3*S,S]]),S))
log=[]
for it in range(200):
 v,F,mw=l.solve();hs,ws,err=net.quantiles(F);full=[mirror(p)for p in hs[::-1]]+hs;fw=np.r_[ws[::-1],ws]/2
 ans,info=br_batch(full,fw,S,limit=20_000_000);val,m=min(ans,key=lambda z:z[0]);assert abs(val-net.payoff(m,F))<1e-6
 print('LP',it,'v',v,'L',val,'h',len(hs),'m',len(l.ms),'nodes',info['nodes'],'done',info['complete'],'seconds',time.time()-st,flush=True)
 log.append(dict(it=it,value=v,response=val,**info))
 json.dump(dict(n=n,S=S,basis=basis,F=F.tolist(),paths_h=hs,weights_h=ws.tolist(),paths_m=l.ms,weights_m=mw.tolist(),log=log),open(f'beam_grid_{n}.json','w'))
 if not info['complete']:print('NODE CAP',flush=True);break
 if v-val<4e-7:
  am=[];aw=[]
  for m,w in zip(l.ms,mw):
   if w>1e-8:am.extend([m,mirror(m)]);aw.extend([w/2,w/2])
  aw=np.array(aw);aw/=aw.sum();resp=Oracle(am,S).response(aw);U=max(r['value']for r in resp)
  print('CLOSED NETWORK',v,val,'UPPER',U,'seconds',time.time()-st,flush=True);break
 new=sum(l.add(complete(p,S))for a,p in ans if a<v-1e-7)
 if not new:print('REPEATED',flush=True);break
