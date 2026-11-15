"""Discovery LP on a planar directed path network.
Integer geometry; floating LP/objective. Not itself an exact certificate.
"""
import bisect,json,sys,time,subprocess
from fractions import Fraction as Q
from collections import defaultdict
import numpy as np
from scipy.optimize._highspy import _core as hc
from shape_search import monster
from integer_geometry import clean
from dither import br

class Network:
 def __init__(self,paths,S):
  self.paths=paths;self.S=S;self.H=max(p[-1][0]for p in paths);self.NF=0
  beams=defaultdict(list)
  for p in paths:
   for (a,x),(b,y) in zip(p,p[1:]):
    assert b>a and (y-x)%(b-a)==0
    v=(y-x)//(b-a);assert abs(v)<=1;beams[v,x-v*a].append((a,b))
   if p[-1][0]<self.H:beams[0,p[-1][1]].append((p[-1][0],self.H))
  segs=[]
  for (v,c),ints in beams.items():
   out=[]
   for a,b in sorted(ints):
    if out and a<=out[-1][1]:out[-1][1]=max(b,out[-1][1])
    else:out.append([a,b])
   segs.extend((a,b,v,c)for a,b in out)
  self.segs=segs;events=set(t for a,b,v,c in segs for t in(a,b))
  for j,(a,b,v,c)in enumerate(segs):
   for d,e,w,f in segs[:j]:
    if v==w:continue
    num=f-c;den=v-w
    if num%den:raise ValueError('noninteger crossing')
    t=num//den
    if max(a,d)<t<min(b,e):events.add(t)
  self.ts=sorted(events);self.slabs=[];self.orders=set();prev=None
  for a,b in zip(self.ts,self.ts[1:]):
   lines=sorted(set((v,c)for d,e,v,c in segs if d<=a and b<=e),key=lambda z:z[0]*(a+b)+2*z[1])
   aa=[v*a+c for v,c in lines];bb=[v*b+c for v,c in lines]
   assert aa==sorted(aa) and bb==sorted(bb)
   gaps=[-1]
   if prev:
    pa=prev['bb'];pg=prev['g'];assert sorted(set(pa))==sorted(set(aa))
   for j in range(1,len(lines)):
    if prev and aa[j-1]<aa[j]:
     k=bisect.bisect_right(pa,aa[j-1]);gaps.append(pg[k])
    else:gaps.append(self.NF);self.NF+=1
   gaps.append(-2)
   for i,j in zip(gaps,gaps[1:]):
    if i>=0 and j>=0 and i!=j:self.orders.add((i,j))
   slab=dict(a=a,b=b,lines=lines,aa=aa,bb=bb,g=gaps);self.slabs.append(slab);prev=slab
 def fv(self,k,F):return 0. if k==-1 else 1. if k==-2 else F[k]
 def cdf(self,t,x):
  if t>=self.H:
   assert all(p[-1][1]==self.S for p in self.paths)
   return (-1,-1) if x<self.S else(-1,-2)if x==self.S else(-2,-2)
  k=bisect.bisect_right(self.ts,t)-1;s=self.slabs[k]
  xs=[v*t+c for v,c in s['lines']]
  return s['g'][bisect.bisect_left(xs,x)],s['g'][bisect.bisect_right(xs,x)]
 def records(self,m):
  times=set(t for t,x in m);end=m[-1][0]
  for (a,x),(b,y) in zip(m,m[1:]):
   assert abs(y-x)==b-a
   v=(y-x)//(b-a);c=x-v*a
   for d,e,w,f in self.segs:
    lo=max(a,d);hi=min(b,e)
    if lo>hi:continue
    if v==w:
     if c==f:times.update([lo,hi])
    else:
     num=f-c;den=v-w
     if num%den:raise ValueError(('fractional monster crossing',num,den))
     t=num//den
     if lo<=t<=hi:times.add(t)
   # The only hider tail is the fixed endpoint +1.
   if b>=self.H:
    t=(self.S-c)//v
    if max(a,self.H)<=t<=b:times.add(t)
  out=[];mt=[t for t,x in m]
  for t in sorted(times):
   if t==end:continue
   j=bisect.bisect_right(mt,t)-1
   if j+1==len(m):x=m[j][1]
   else:
    a,x=m[j];b,y=m[j+1];x+=(t-a)*((y-x)//(b-a))
   lo,hi=self.cdf(t,x)
   if not out or out[-1][1:]!=(lo,hi):out.append((t,lo,hi))
  return out,end
 def payoff(self,m,F):
  total=0.
  for sign in(1,-1):
   rr,end=self.records([[t,sign*x]for t,x in m]);L=1.;R=0.
   for j,(t,lo,hi)in enumerate(rr):
    L=min(L,self.fv(lo,F));R=max(R,self.fv(hi,F));b=rr[j+1][0]if j+1<len(rr)else end
    total+=(b-t)*(1-R+L)/(2*self.S)
  return total
 def quantiles(self,F):
  f=np.round(F,8);qs=np.unique(np.r_[0,1,f]);qs=qs[(qs>=0)&(qs<=1)];hs=[];ws=[];err=0.
  for a,b in zip(qs,qs[1:]):
   if b-a<1e-8:continue
   q=(a+b)/2;p=[];bad=False
   for s in self.slabs:
    gs=[self.fv(k,f)for k in s['g']];j=np.searchsorted(gs,q)-1
    if not 0<=j<len(s['lines']):bad=True;break
    v,c=s['lines'][j];z=[s['a'],v*s['a']+c]
    if p and z!=p[-1]:bad=True;break
    if not p:p.append(z)
    p.append([s['b'],v*s['b']+c])
   if bad:
    if b-a>1e-6:raise ValueError(('quantile mismatch',a,b))
    err+=b-a;continue
   p=[[int(t),int(x)]for t,x in clean(p)]
   if hs and hs[-1]==p:ws[-1]+=b-a
   else:hs.append(p);ws.append(b-a)
  ws=np.array(ws);ws/=ws.sum();return hs,ws,err
 def from_mixture(self,weights):
  vals=np.full(self.NF,np.nan)
  def position(p,t):
   ts=[a for a,x in p];j=bisect.bisect_right(ts,t)-1
   if j+1==len(p):return p[-1][1]
   a,x=p[j];b,y=p[j+1];return x+(y-x)*(t-a)/(b-a)
  for s in self.slabs:
   tm=(s['a']+s['b'])/2;xx=[position(p,tm)for p in self.paths]
   gx=[v*tm+c for v,c in s['lines']]
   for j,g in enumerate(s['g'][1:-1],1):
    probe=(gx[j-1]+gx[j])/2;v=sum(w for x,w in zip(xx,weights)if x<probe)
    if np.isfinite(vals[g]):assert abs(vals[g]-v)<1e-8
    vals[g]=v
  assert np.all(np.isfinite(vals));return vals

class LP:
 def __init__(self,net):
  self.net=net;self.NF=net.NF;self.N=self.NF+1;self.rows=[];self.lb=[];self.ub=[];self.pushed=0;self.mrows=[];self.ms=[]
  self.h=hc._Highs();self.h.setOptionValue('output_flag',False);self.h.setOptionValue('solver','simplex');self.h.setOptionValue('threads',1);self.h.setOptionValue('primal_feasibility_tolerance',1e-9);self.h.setOptionValue('dual_feasibility_tolerance',1e-9)
  self.h.addVars(self.N,np.zeros(self.N),np.r_[np.ones(self.NF),hc.kHighsInf]);self.h.changeColCost(self.NF,-1.)
  for i,j in net.orders:self.le([(i,1),(j,-1)],0)
  self.push()
 def le(self,terms,b):
  row={}
  for k,c in terms:row[k]=row.get(k,0)+c
  self.rows.append(row);self.lb.append(-hc.kHighsInf);self.ub.append(b)
 def push(self):
  nn=len(self.rows)-self.pushed
  if not nn:return
  ptr=[0];jj=[];vv=[]
  for row in self.rows[self.pushed:]:
   for k,c in row.items():
    if c:jj.append(k);vv.append(c)
   ptr.append(len(jj))
  self.h.addRows(nn,np.array(self.lb[self.pushed:]),np.array(self.ub[self.pushed:]),len(jj),np.array(ptr,np.int32),np.array(jj,np.int32),np.array(vv));self.pushed=len(self.rows)
 def add(self,m):
  m=[[int(t),int(x)]for t,x in clean(m)]
  if m in self.ms or [[t,-x]for t,x in m]in self.ms:return False
  self.ms.append(m);terms=[(self.NF,1)];rhs=0.
  for sign in(1,-1):
   rr,end=self.net.records([[t,sign*x]for t,x in m]);K=len(rr);L=list(range(self.N,self.N+K));R=list(range(self.N+K,self.N+2*K));self.N+=2*K;self.h.addVars(2*K,np.zeros(2*K),np.ones(2*K))
   for j,(t,lo,hi)in enumerate(rr):
    if lo<0:self.le([(L[j],1)],self.net.fv(lo,[]))
    else:self.le([(L[j],1),(lo,-1)],0)
    if hi<0:self.le([(R[j],-1)],-self.net.fv(hi,[]))
    else:self.le([(hi,1),(R[j],-1)],0)
    if j:self.le([(L[j],1),(L[j-1],-1)],0);self.le([(R[j-1],1),(R[j],-1)],0)
    b=rr[j+1][0]if j+1<K else end;dt=(b-t)/(2*self.net.S);rhs+=dt;terms.extend([(R[j],dt),(L[j],-dt)])
  self.mrows.append(len(self.rows));self.le(terms,rhs);self.push();return True
 def solve(self):
  self.h.run()
  if self.h.getModelStatus()!=hc.HighsModelStatus.kOptimal:
   print('LP RESTART',self.h.getModelStatus(),flush=True)
   self.h.clearSolver();self.h.setOptionValue('solver','ipm');self.h.run();self.h.setOptionValue('solver','simplex')
  assert self.h.getModelStatus()==hc.HighsModelStatus.kOptimal,self.h.getModelStatus()
  ss=self.h.getSolution();x=np.array(ss.col_value);w=-np.array(ss.row_dual)[self.mrows]
  return x[self.NF],x[:self.NF],w

def load_basis(kind):
 S=3_200_000;paths=[];weights=[]
 d=json.load(open('/mnt/data/interval_equilibrium_check/exploratory/princess_strategy.json'))
 for row in d['rows']:
  paths.append([[int(Q(t)*S),int(Q(x)*S)]for t,x in row['path']]);weights.append(row['numerator']/100000)
 for p in paths:
  if p[-1][0]<2*S:p.append([2*S,p[-1][1]])
 if kind!='old':
  d=json.load(open('dither_16.json'));ss=d['scale']
  for p in d['paths'][len(d['paths'])//2:]:
   # dither scale is 6.4m, divide 2; all vertices have suitable parity except clips, hence allow choose scale doubled.
   if ss!=S:
    assert ss%S==0
    div=ss//S
    if any(t%div or x%div for t,x in p):raise ValueError('rescale')
    p=[[t//div,x//div]for t,x in p]
   if p not in paths:paths.append(p);weights.append(0.)
 # Double scale to preserve even characteristic intercepts.
 paths=[[[2*t,2*x]for t,x in p]for p in paths];S*=2
 return paths,weights,S
if __name__=='__main__':
 kind=sys.argv[1]if len(sys.argv)>1 else 'old';st=time.time();ps,ww,S=load_basis(kind);net=Network(ps,S);print('NETWORK',kind,'paths',len(ps),'beams',len(net.segs),'slabs',len(net.slabs),'faces',net.NF,'order',len(net.orders),'secs',time.time()-st,flush=True)
 F=net.from_mixture(ww);hs,ws,err=net.quantiles(F)
 full=[[[t,-x]for t,x in p]for p in hs[::-1]]+hs;fw=np.r_[ws[::-1],ws]/2
 val,m,info=br(full,fw,S,limit=30_000_000);print('BASE',val,info,'cdf',net.payoff(m,F),flush=True);assert abs(net.payoff(m,F)-val)<1e-7
 l=LP(net)
 for j in range(-16,17):
  for c in [j/16,1.,2-j/16]:
   if j/16<=c<=2-j/16:
    mm=monster(j/16,c);l.add([[int(round(t*S)),int(round(x*S))]for t,x in mm])
 l.add(m);log=[]
 for it in range(300):
  v,F,mw=l.solve();hs,ws,err=net.quantiles(F);full=[[[t,-x]for t,x in p]for p in hs[::-1]]+hs;fw=np.r_[ws[::-1],ws]/2
  val,m,info=br(full,fw,S,limit=50_000_000);cdf=net.payoff(m,F);assert abs(cdf-val)<1e-6,(cdf,val)
  print('LP',it,'v',v,'response',val,'m',len(l.ms),'h',len(hs),'vars',l.N,'nodes',info['nodes'],'complete',info['complete'],'secs',time.time()-st,flush=True)
  print('PATH',[[t/S,x/S]for t,x in m],flush=True)
  log.append(dict(it=it,value=v,response=val,**info))
  # End-reflecting completion guarantees capture against all future princesses.
  for j,(t,x)in enumerate(m):
   if abs(x)==S:m=m[:j+1]+[[t+2*S,-x]];break
  else:
   t,x=m[-1];wall=S if x>=0 else -S;m+=[[t+abs(wall-x),wall],[t+abs(wall-x)+2*S,-wall]]
  json.dump(dict(S=S,basis=ps,F=F.tolist(),paths_h=hs,weights_h=ws.tolist(),paths_m=l.ms,weights_m=mw.tolist(),log=log),open(f'network_{kind}.json','w'))
  if not info['complete']:print('NODE CAP',flush=True);break
  if v-val<2e-7:print('CLOSED NETWORK',flush=True);break
  if not l.add(m):print('REPEATED',flush=True);break
