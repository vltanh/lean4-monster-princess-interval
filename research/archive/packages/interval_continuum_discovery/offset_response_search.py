import sys,json,pathlib,time
import numpy as np
from numba import njit
sys.path.insert(0,str(pathlib.Path(__file__).parent))
from central_wait_exploit import Q,clean
HERE=pathlib.Path(__file__).parent

def hpath(a,u,c,delta=1e-9,corrected=False):
 a=max(a,delta);p=[(0.,a),((u-a)/2,(u+a)/2)]
 if c>=u-2*delta:p += [(u-delta,delta),(c+delta,delta)]
 else:p += [((u+c)/2,(u-c)/2)]
 if corrected and c>=0:
  eta=delta;p += [((1+eta+c)/2,(1+eta-c)/2),(1.,delta),(2-delta,1.)]
 else:p += [(c+1,1.)]
 out=[]
 for t,x in p:
  if out and abs(t-out[-1][0])<1e-12:
   assert abs(x-out[-1][1])<1e-9;continue
  out.append((t,x))
 return np.array(out)

def load(name,corrected=False):
 d=json.load(open(HERE/name));hh=[];ww=[]
 for row,w in zip(d['names_h'],d['weights_h']):
  if row[0]==1:p=np.array([[0.,1.]])
  else:p=hpath(*row,corrected=corrected)
  hh += [p,p*np.array([1.,-1.])];ww += [w/2,w/2]
 K=max(map(len,hh));hs=np.zeros((len(hh),K,2));ns=np.zeros(len(hh),dtype=np.int64)
 for i,p in enumerate(hh):hs[i,:len(p)]=p;ns[i]=len(p)
 return hs,ns,np.array(ww)

@njit
def pos(p,n,t):
 for i in range(n-1):
  a,x=p[i];b,y=p[i+1]
  if a<=t<=b:return x+(y-x)*(t-a)/(b-a)
 return p[n-1,1]

@njit
def payoff(m,hs,ns,ws):
 N=len(hs);ts=np.zeros(10000);nk=0
 for i in range(len(m)):ts[nk]=m[i,0];nk+=1
 for i in range(N):
  cuts=np.zeros(len(m)+ns[i]);j=0
  for k in range(len(m)):cuts[j]=m[k,0];j+=1
  for k in range(ns[i]):cuts[j]=hs[i,k,0];j+=1
  cuts.sort()
  for k in range(len(cuts)-1):
   a,b=cuts[k],cuts[k+1]
   if b<a+1e-14:continue
   x=pos(m,len(m),a)-pos(hs[i],ns[i],a);y=pos(m,len(m),b)-pos(hs[i],ns[i],b)
   if x*y<0:
    ts[nk]=a+(b-a)*abs(x)/(abs(x)+abs(y));nk+=1
   if abs(x)<1e-12:ts[nk]=a;nk+=1
   if abs(y)<1e-12:ts[nk]=b;nk+=1
 ts=np.unique(ts[:nk]);aa=1.;bb=0.;out=0.
 for k in range(len(ts)):
  t=ts[k];x=pos(m,len(m),t);left=0.;right=0.
  for j in range(N):
   y=pos(hs[j],ns[j],t)
   if y<x-1e-12:left+=ws[j]
   if y<x+1e-12:right+=ws[j]
  aa=min(aa,left);bb=max(bb,right)
  if k+1<len(ts):
   nt=ts[k+1];mid=(nt+t)/2;x=pos(m,len(m),mid);left=0.;right=0.
   for j in range(N):
    y=pos(hs[j],ns[j],mid)
    if y<x-1e-12:left+=ws[j]
    if y<x+1e-12:right+=ws[j]
   aa=min(aa,left);bb=max(bb,right);out+=(nt-t)*(1-bb+aa)
 return out

def mpath(x,c):
 p=[(0.,x),((c-x)/2,(c+x)/2),(c+1,-1.),(c+3,1.)]
 out=[]
 for t,y in p:
  if out and abs(t-out[-1][0])<1e-12:continue
  out.append((t,y))
 return np.array(out)

if __name__=='__main__':
 name=sys.argv[1] if len(sys.argv)>1 else 'corrected_central_candidate_32_monotone.json'
 hs,ns,ws=load(name,corrected=name.startswith('corrected'));best=(100,None);st=time.time()
 for x in np.linspace(-1,1,129):
  for c in np.linspace(x,2-x,129):
   m=mpath(x,c);v=payoff(m,hs,ns,ws)
   if v<best[0]:
    best=(v,m.tolist())
    print('BEST',v,best[1],'secs',time.time()-st,flush=True)
 print('FINAL',best,flush=True)
 (HERE/('offset_response_'+name)).write_text(json.dumps(dict(value=best[0],route=best[1],source=name)))
