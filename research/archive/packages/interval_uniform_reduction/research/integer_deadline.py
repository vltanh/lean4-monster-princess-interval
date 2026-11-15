from integer_geometry import *
from core import dinic
class Oracle:
 def __init__(self,ms,S):
  self.ms=ms;self.S=S;self.H=max(m[-1][0]for m in ms);self.N=len(ms);self.starts=[m[0][1]for m in ms]
  ss=sorted(set([0,S]+[x for x in self.starts if 0<=x<=S]));self.chambers=list(zip(ss,ss[1:]));self.ds=[];self.pairs={}
  for i,m in enumerate(ms):
   self.ds.append([meet(m,[[0,0],[self.H,0]]),meet(m,[[0,S],[self.H,S]])]);assert all(t is not None for t in self.ds[-1])
   for j in range(i):self.pairs[i,j]=self.pairs[j,i]=meet(m,ms[j])
  self.graphs=[self.build((a+b)//2)for a,b in self.chambers]
 def build(self,x):
  B=[p<x for p in self.starts];ds=[self.ds[i][int(B[i])]for i in range(self.N)];E=[{0,self.H,d}for d in ds];pairs=[]
  for i in range(self.N):
   if not B[i]:continue
   for j in range(self.N):
    if B[j]:continue
    t=self.pairs[i,j]
    if t is not None and t<self.H:pairs.append((i,j,t));E[i].add(t);E[j].add(t)
  E=[sorted(e)for e in E];K=[len(e)-1 for e in E];offset=[];k=0
  for n in K:offset.append(k);k+=n
  s=k;t=k+1;us=[];vs=[];co=[];owners=[]
  def add(u,v,c,owner=-1):us.append(u);vs.append(v);co.append(c);owners.append(owner)
  for i in range(self.N):
   o=offset[i]
   for j,(a,b)in enumerate(zip(E[i],E[i][1:])):
    if B[i]:add(s,o+j,(b-a)/self.S,i)
    else:add(o+j,t,(b-a)/self.S,i)
   for j in range(K[i]-1):
    if B[i]:add(o+j+1,o+j,self.H/self.S+1)
    else:add(o+j,o+j+1,self.H/self.S+1)
   if ds[i]<self.H:
    j=E[i].index(ds[i])
    if B[i]:add(o+j,t,self.H/self.S+1)
    else:add(s,o+j,self.H/self.S+1)
  for i,j,tm in pairs:add(offset[i]+E[i].index(tm),offset[j]+E[j].index(tm),self.H/self.S+1)
  return dict(us=np.array(us,np.int64),vs=np.array(vs,np.int64),co=np.array(co),owners=np.array(owners,np.int64),s=s,t=t,B=B,E=E,K=K,offset=offset,initial=x,ds=ds,pairs=pairs)
 def response(self,w):
  out=[]
  for g in self.graphs:
   cap=g['co'].copy();o=g['owners'];ids=o>=0;cap[ids]*=w[o[ids]]
   f,src,_=dinic(g['t']+1,g['us'],g['vs'],cap,g['s'],g['t']);r=[]
   for i in range(self.N):
    a=g['offset'][i];z=src[a:a+g['K'][i]];z=z if g['B'][i]else ~z
    assert np.all(np.diff(z.astype(int))<=0);r.append(g['E'][i][int(z.sum())])
   assert all(r[i]<=g['ds'][i]for i in range(self.N));assert all(min(r[i],r[j])<=tm for i,j,tm in g['pairs'])
   v=sum(wi*ri/self.S for wi,ri in zip(w,r));assert abs(v-(self.H/self.S-f))<1e-7
   out.append(dict(value=v,r=r,initial=g['initial']))
  return out
