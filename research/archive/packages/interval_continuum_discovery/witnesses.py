import json,sys,numpy as np
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'packages/interval_equilibrium_check/exploratory'))
def pos(p,t):return np.interp(t,p[:,0],p[:,1])
def simplify(p):
 out=[]
 for t,x in p:
  if out and abs(t-out[-1][0])<1e-11:
   assert abs(x-out[-1][1])<1e-9
   continue
  out.append([float(t),float(x)])
  while len(out)>=3:
   (a,x),(b,y),(c,z)=out[-3:]
   if abs((y-x)*(c-b)-(z-y)*(b-a))<1e-12:out.pop(-2)
   else:break
 return np.array(out)
def meet(p,q):
 ts=np.unique(np.r_[p[:,0],q[:,0]]);da=pos(p,ts)-pos(q,ts)
 for k in range(len(ts)):
  if abs(da[k])<1e-9:return ts[k]
  if k+1<len(ts) and da[k]*da[k+1]<0:return ts[k]+(ts[k+1]-ts[k])*abs(da[k])/(abs(da[k])+abs(da[k+1]))
 return np.inf
D=json.load(open(ROOT/'packages/interval_uniform_reduction/research/upper_continuum_32.json'))
ms=[np.array(p) for p in D['paths']];H=4;e=1e-6

def env(curves,maximum):
 ts=np.unique(np.concatenate([q[:,0] for q in curves]));out=[]
 for a,b in zip(ts,ts[1:]):
  va=np.array([pos(q,a) for q in curves]);vb=np.array([pos(q,b) for q in curves]);cuts=[a,b]
  for i in range(len(curves)):
   for j in range(i):
    d=va[i]-va[j];f=vb[i]-vb[j]
    if d*f< -1e-22:cuts.append(a+(b-a)*abs(d)/(abs(d)+abs(f)))
  for t in np.unique(cuts)[:-1]:
   z=va+(vb-va)*(t-a)/(b-a);out.append([t,max(z) if maximum else min(z)])
 vals=[pos(q,H) for q in curves];out.append([H,max(vals) if maximum else min(vals)])
 return simplify(out)

paths=[]
for k,z in enumerate(D['responses']):
 a=z['initial'];lows=[np.array([[0,0],[H,0]])];ups=[np.array([[0,1],[H,1]])]
 for m,ri in zip(ms,z['r']):
  d=max(0,ri-e);below=m[0,1]<a;dr=-1 if below else 1
  q=simplify(np.vstack([m[m[:,0]<d-1e-12],[d,pos(m,d)],[H,pos(m,d)+dr*(H-d)]]))
  (lows if below else ups).append(q)
 L=env(lows,True);U=env(ups,False);L[:,1]+=e/10;U[:,1]-=e/10
 q=env([env([np.array([[0,a],[H,a]]),U],False),L],True)
 w=np.repeat(np.array(D['weights'])/2,2);val=sum(ww*meet(m,q) for ww,m in zip(w,ms) if ww>0)
 if k in [0,5,10,15,20,25,28]:print('CASE',k,'a',a,'value',val,'path',np.round(q,7).tolist(),flush=True)
 paths.append(q.tolist())
json.dump({'paths':paths},open(Path(__file__).parent/'witnesses32.json','w'))
