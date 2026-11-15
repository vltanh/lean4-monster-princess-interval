import numpy as np,json,sys,time
from scipy.optimize import linprog
from numba import njit,prange
@njit
def at(p,k,t):
 for j in range(k-1):
  if t<=p[j+1,0]:
   return p[j,1]+(p[j+1,1]-p[j,1])*(t-p[j,0])/(p[j+1,0]-p[j,0])
 return p[k-1,1]
@njit
def meet(p,np_,q,nq,sign=1):
 i=0;j=0;t=0.;v=p[0,1]-sign*q[0,1]
 if abs(v)<1e-12:return 0.
 while i<np_-1 or j<nq-1:
  b=p[i+1,0] if i<np_-1 else 1e100
  c=q[j+1,0] if j<nq-1 else 1e100
  s=min(b,c);v2=at(p,np_,s)-sign*at(q,nq,s)
  if abs(v2)<1e-12:return s
  if v*v2<0:return t+(s-t)*abs(v)/(abs(v)+abs(v2))
  if b<=s+1e-13:i+=1
  if c<=s+1e-13:j+=1
  t=s;v=v2
 return 1e3
@njit(parallel=True)
def payoffs(hs,nh,ms,nm):
 a=np.empty((len(hs),len(ms)))
 for i in prange(len(hs)):
  for j in range(len(ms)):
   a[i,j]=(meet(ms[j],nm[j],hs[i],nh[i])+meet(ms[j],nm[j],hs[i],nh[i],-1))/2
 return a

def clean(q):
 out=[]
 for t,x in q:
  if out and abs(t-out[-1][0])<1e-13:assert abs(x-out[-1][1])<1e-12;continue
  out.append([float(t),float(x)])
  while len(out)>2:
   (a,x),(b,y),(c,z)=out[-3:]
   if abs((y-x)*(c-b)-(z-y)*(b-a))<1e-13:out.pop(-2)
   else:break
 return out

def monster(x,c):
 q=[[0,x],[(c-x)/2,(c+x)/2],[c+1,-1],[c+3,1]]
 if abs(c+x-2)<1e-12:q=q[:-1]
 return clean(q)

def princess(k,a,b,u,e=1e-6):
 if a==1:return [[0,1]]
 a=max(a,2*e);b=max(b,e);u=max(a,u-e)
 if k=='wait':
  b=min(a,b);return clean([[0,a],[u-a,a],[u-b,b],[u+1-2*b,1]])
 assert k=='out';b=min(b,(u+a)/2);return clean([[0,a],[(u-a)/2,(u+a)/2],[u-b,b],[u+1-2*b,1]])
def packed(ps):
 K=max(len(p) for p in ps);a=np.zeros((len(ps),K,2));ns=[]
 for i,p in enumerate(ps):a[i,:len(p)]=p;ns.append(len(p))
 return a,np.array(ns,np.int64)

def solve(A,tol=2e-9):
 nh,nm=A.shape
 s=linprog(np.r_[np.zeros(nm),1],A_ub=np.c_[A,-np.ones(nh)],b_ub=np.zeros(nh),A_eq=[np.r_[np.ones(nm),0]],b_eq=[1],bounds=[(0,None)]*nm+[(None,None)],method='highs',options={'dual_feasibility_tolerance':1e-9,'primal_feasibility_tolerance':1e-9})
 assert s.success,s.message
 return s.x[-1],s.x[:-1],-s.ineqlin.marginals
if __name__=='__main__':
 n=int(sys.argv[1]);st=time.time()
 hn=[('end',1,1,1)];hs=[[[0,1]]]
 for kind in ['wait','out']:
  for ia in range(n):
   for iu in range(ia,2*n-ia+1):
    for ib in range(ia+1 if kind=='wait' else (iu+ia)//2+1):
     # Sweep-aligned and later early turns; all rational grid parameters.
     hn.append((kind,ia/n,ib/n,iu/n));hs.append(princess(kind,ia/n,ib/n,iu/n))
 mn=[];ms=[]
 for ix in range(-n,n+1):
  for ic in range(ix,2*n-ix+1):
   mn.append((ix/n,ic/n));ms.append(monster(ix/n,ic/n))
 hp,nh=packed(hs);mp,nm=packed(ms);print('MATRIX',len(hs),len(ms),'secs',time.time()-st,flush=True)
 A=payoffs(hp,nh,mp,nm);print('PAYOFFS',time.time()-st,flush=True)
 # Solve using generated rows and columns to keep dense LPs small.
 rows=[0];cols=list(range(0,len(ms),max(1,len(ms)//100)))
 for it in range(500):
  v,w,q=solve(A[np.ix_(rows,cols)]);hr=A[:,cols]@w;mr=q@A[rows,:];U=hr.max();L=mr.min()
  print('ITER',it,len(rows),len(cols),v,L,U,'secs',time.time()-st,flush=True)
  if U-L<1e-8:break
  nr=np.argsort(hr)[-min(50,np.count_nonzero(hr>v+1e-8)): ] if np.any(hr>v+1e-8) else []
  nc=np.argsort(mr)[:min(50,np.count_nonzero(mr<v-1e-8))] if np.any(mr<v-1e-8) else []
  rows+=list(set(map(int,nr))-set(rows));cols+=list(set(map(int,nc))-set(cols))
 hw=np.zeros(len(hs));mw=np.zeros(len(ms));hw[rows]=q;mw[cols]=w
 hi=np.where(hw>1e-9)[0];mi=np.where(mw>1e-9)[0]
 D=dict(n=n,value=v,paths_h=[hs[i] for i in hi],names_h=[hn[i] for i in hi],weights_h=hw[hi].tolist(),paths_m=[ms[i] for i in mi],names_m=[mn[i] for i in mi],weights_m=mw[mi].tolist())
 json.dump(D,open('shapes_%d.json'%n,'w'));print('ACTIVE H',[(hn[i],float(hw[i]))for i in hi]);print('ACTIVE M',[(mn[i],float(mw[i]))for i in mi]);print('DONE',time.time()-st,flush=True)
