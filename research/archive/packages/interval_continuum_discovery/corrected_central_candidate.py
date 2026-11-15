"""Floating discovery on a specified princess family, not a certificate.

For c>=0 include the limiting inward detour after U=1; for c<0 retain
the original outward suffix. The omitted partial negative-c detours and
unrestricted monster responses are not certified by this calculation.
The sampled dual fails a separate unrestricted-monster response check.

Every mode uses only M1(-1), nonnegative-parameter M1 paths, and M2 paths:
the displayed detour formula is not valid for other negative M1 parameters.
In monotone mode, the dual is valid only for the constrained set of monster
mixtures; its individual sampled M1/M2 payoffs need not exceed the objective.
"""
import json,sys,time,pathlib
import numpy as np
from scipy.optimize import linprog
from numba import njit,prange

@njit
def A(z,a,u,c):
    if z<=a:return 0.
    if z<=u:return (z-a)/2
    if c>=u and z<=c:return z
    if z<=c+2:return (z+c)/2
    return z-1

@njit
def B(z,a,u,c):
    if z<=-a:return 0.
    if z<=min(u,c):return (z+u)/2
    if c>=u and z<=c:return z
    return z+1

@njit
def payoff(a,u,c,kind,x):
    assert kind!=1 or x==-1 or 0<=x<1
    if a==1:
        if kind==1:
            return 1 if abs(x)==1 else 2-x
        return 2 if x==-1 else 1 if x==1 else 3
    if kind==1:
        q=B(-x,a,u,c) if x<a else 0. if x==a else A(2-x,a,u,c)
        r=A(-x,a,u,c) if x<-a else 0. if x==-a else B(2-x,a,u,c)
    else:
        q=B(3,a,u,c) if x<-c else B(-x,a,u,c) if x<a else 0. if x==a else A(1,a,u,c)
        r=A(-x,a,u,c) if x<-a else 0. if x==-a else B(1,a,u,c)
    return (q+r)/2 + ((1-c)/4 if c>=0 and kind==1 and 0<x<1 and x>a else 0.)

@njit(parallel=True)
def matrix(hs,ms):
    out=np.zeros((len(hs),len(ms)))
    for i in prange(len(hs)):
        for j in range(len(ms)):
            out[i,j]=payoff(hs[i,0],hs[i,1],hs[i,2],ms[j,0],ms[j,1])
    return out

def generate(n,eps):
    hs=[(1.,1.,1.)];seen=set(hs)
    aa=sorted(set([eps,1-2*eps]+[i/n+s*eps for i in range(1,n) for s in (-1,1)]))
    for a in aa:
        us=sorted(set([a,1-eps]+[i/n-eps for i in range(1,n) if i/n-eps>=a]))
        cs=sorted(set([-a,1-eps]+[i/n-eps for i in range(-n,n) if i/n-eps>=-a]))
        for u in us:
            for c in cs:
                if u>=a and c>=-a and u<1 and c<1:
                    key=(a,u,c)
                    if key not in seen:seen.add(key);hs.append(key)
    ms=[(1,-1.)]+[(1,i/n) for i in range(n)]+[(2,i/n) for i in range(-n,n)]
    return np.array(hs),np.array(ms)

def solve_rows(mat,rows,extra=None):
    nr,nm=mat.shape
    Aub=np.c_[mat[rows],-np.ones(len(rows))]
    if extra is not None:Aub=np.vstack([Aub,extra])
    s=linprog(np.r_[np.zeros(nm),1.],A_ub=Aub,b_ub=np.zeros(len(Aub)),A_eq=[np.r_[np.ones(nm),0.]],b_eq=[1.],bounds=[(0,None)]*nm+[(None,None)],method='highs',options={'primal_feasibility_tolerance':1e-9,'dual_feasibility_tolerance':1e-9})
    assert s.success,s.message
    return s.x[-1],s.x[:-1],-s.ineqlin.marginals

if __name__=='__main__':
    n=int(sys.argv[1]) if len(sys.argv)>1 else 32
    eps=1e-7;st=time.time();hs,ms=generate(n,eps);print('SIZE',len(hs),len(ms),flush=True)
    suffix=''
    if len(sys.argv)>2 and sys.argv[2] in ('positive_m1','monotone'):
        ms=ms[(ms[:,0]==2)|(ms[:,1]==-1)|(ms[:,1]>=0)]
        suffix='_positive_m1'
    extra=None
    if len(sys.argv)>2 and sys.argv[2]=='monotone':
        suffix='_monotone';extra=[]
        sets=[np.where((ms[:,0]==1)&(ms[:,1]>=0))[0],np.where((ms[:,0]==2)&(ms[:,1]<0)&(ms[:,1]>-1))[0][::-1]]
        for ss in sets:
            for i,j in zip(ss,ss[1:]):
                row=np.zeros(len(ms)+1);row[i]=1;row[j]=-1;extra.append(row)
        extra=np.array(extra)
    mat=matrix(hs,ms);print('MATRIX',time.time()-st,flush=True)
    rows=[0]+list(np.linspace(1,len(hs)-1,100,dtype=int))
    for it in range(100):
        v,w,q=solve_rows(mat,rows,extra);q=q[:len(rows)];rr=mat@w;gap=rr.max()-v
        print('ITER',it,'v',v,'upper',rr.max(),'rows',len(rows),'secs',time.time()-st,flush=True)
        if gap<1e-8:break
        new=np.where(rr>v+max(1e-8,gap/10))[0]
        new=new[np.argsort(rr[new])[-100:]]
        rows=sorted(set(rows)|set(map(int,new)))
    hw=np.zeros(len(hs));hw[rows]=q
    ip=np.where(hw>1e-8)[0];im=np.where(w>1e-8)[0]
    dual_scope=('Only monotonicity-constrained monster mixtures; not all sampled pure paths'
                if extra is not None else 'Only the specified finite sampled monster family')
    d=dict(n=n,epsilon=eps,value=v,upper=float(rr.max()),dual_scope=dual_scope,names_h=hs[ip].tolist(),weights_h=hw[ip].tolist(),names_m=ms[im].tolist(),weights_m=w[im].tolist())
    (pathlib.Path(__file__).parent/f'corrected_central_candidate_{n}{suffix}.json').write_text(json.dumps(d))
    print('HIDERS',list(zip(d['names_h'],d['weights_h'])),flush=True)
    print('MONSTERS',list(zip(d['names_m'],d['weights_m'])),flush=True)
