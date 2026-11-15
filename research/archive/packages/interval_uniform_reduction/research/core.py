"""Exploratory floating-point oracles; exact certificates are separate."""
import numpy as np
from scipy.optimize import linprog
from numba import njit


def simplify(p,tol=1e-10):
    out=[]
    for t,x in p:
        if out and abs(t-out[-1][0])<tol:
            assert abs(x-out[-1][1])<tol;continue
        out.append([float(t),float(x)])
        while len(out)>=3:
            (a,x),(b,y),(c,z)=out[-3:]
            if abs((y-x)*(c-b)-(z-y)*(b-a))<tol:out.pop(-2)
            else:break
    return np.array(out)

def pos(p,t):return np.interp(t,p[:,0],p[:,1])

def mirror(p):return p*np.array([1.,-1.])

def mpath(k,x):
    if k==1:return simplify([[0,x],[1-x,1],[3-x,-1]])
    if k==2:return simplify([[0,x],[(1-x)/2,(1+x)/2],[2,-1],[4,1]])
    raise ValueError(k)

def meet(p,q,H=None):
    ts=np.unique(np.r_[p[:,0],q[:,0]])
    if H is not None:ts=np.unique(np.r_[ts[ts<H],H])
    da=pos(p,ts)-pos(q,ts)
    for k in range(len(ts)):
        if abs(da[k])<1e-9:return ts[k]
        if k+1<len(ts) and da[k]*da[k+1]<0:return ts[k]+(ts[k+1]-ts[k])*abs(da[k])/(abs(da[k])+abs(da[k+1]))
    return np.inf

@njit
def dinic(N,us,vs,caps,s,t):
    ne=len(us);head=np.full(N,-1,np.int64);dest=np.empty(2*ne,np.int64);nxt=np.empty(2*ne,np.int64);cap=np.zeros(2*ne)
    for i in range(ne):
        u=us[i];v=vs[i];dest[2*i]=v;nxt[2*i]=head[u];head[u]=2*i;cap[2*i]=caps[i]
        dest[2*i+1]=u;nxt[2*i+1]=head[v];head[v]=2*i+1
    level=np.empty(N,np.int64);q=np.empty(N,np.int64);ptr=np.empty(N,np.int64)
    stack=np.empty(N,np.int64);edge=np.empty(N,np.int64);flow=0.
    while True:
        level[:]=-1;level[s]=0;q[0]=s;lo=0;hi=1
        while lo<hi:
            u=q[lo];lo+=1;e=head[u]
            while e>=0:
                v=dest[e]
                if cap[e]>1e-12 and level[v]<0:level[v]=level[u]+1;q[hi]=v;hi+=1
                e=nxt[e]
        if level[t]<0:break
        ptr[:]=head;stack[0]=s;depth=0
        while depth>=0:
            u=stack[depth]
            if u==t:
                amt=1e100
                for j in range(depth):amt=min(amt,cap[edge[j]])
                first=depth
                for j in range(depth):
                    e=edge[j];cap[e]-=amt;cap[e^1]+=amt
                    if cap[e]<1e-12 and j<first:first=j
                flow+=amt;depth=first
                continue
            e=ptr[u]
            while e>=0 and (cap[e]<1e-12 or level[dest[e]]!=level[u]+1):e=nxt[e]
            ptr[u]=e
            if e<0:
                level[u]=-1;depth-=1
                if depth>=0:ptr[stack[depth]]=nxt[edge[depth]]
            else:
                edge[depth]=e;depth+=1;stack[depth]=dest[e]
    return flow,level>=0,cap

class PrincessOracle:
    def __init__(self,ms,symmetric=True):
        self.ms=ms;self.N=len(ms);self.H=max(max(p[:,0]) for p in ms)
        self.starts=np.array([p[0,1] for p in ms]);self.symmetric=symmetric
        starts=np.unique(np.r_[-1,self.starts,1]);starts=starts[(starts>=-1)&(starts<=1)]
        self.chambers=[(a,b) for a,b in zip(starts,starts[1:]) if b>a+1e-8 and (not symmetric or a>=-1e-8)]
        if symmetric and not any(abs(starts)<1e-9):
            a=max(starts[starts<0]);b=min(starts[starts>0]);self.chambers.insert(0,(a,b))
        self.meets=np.full((self.N,self.N),np.inf)
        self.ds=np.zeros((self.N,2))
        for i,m in enumerate(ms):
            for wall in (-1,1):
                self.ds[i,(wall+1)//2]=meet(m,np.array([[0,wall],[self.H,wall]]))
                if not np.isfinite(self.ds[i,(wall+1)//2]):raise ValueError('Monster does not reach both walls')
            for j in range(i):self.meets[i,j]=self.meets[j,i]=meet(m,ms[j])
        self.graphs=[self.build((a+b)/2) for a,b in self.chambers]
    def build(self,initial):
        N=self.N;H=self.H;B=self.starts<initial
        ds=self.ds[np.arange(N),B.astype(int)]
        pairs=[(i,j,self.meets[i,j]) for i in range(N) if B[i] for j in range(N) if not B[j] and self.meets[i,j]<H-1e-10]
        ts=np.unique(np.round(np.r_[0,H,ds,[z[2] for z in pairs]],11));K=len(ts)-1
        us=[];vs=[];co=[];owners=[]
        s=N*K;t=s+1
        def add(u,v,c,owner=-1):us.append(u);vs.append(v);co.append(c);owners.append(owner)
        for i in range(N):
            for k,dt in enumerate(np.diff(ts)):
                if B[i]:add(s,i*K+k,dt,i)
                else:add(i*K+k,t,dt,i)
            for k in range(K-1):
                if B[i]:add(i*K+k+1,i*K+k,H+1)
                else:add(i*K+k,i*K+k+1,H+1)
            if ds[i]<H-1e-9:
                k=int(np.argmin(abs(ts-ds[i])))
                if B[i]:add(i*K+k,t,H+1)
                else:add(s,i*K+k,H+1)
        for i,j,tm in pairs:
            k=int(np.argmin(abs(ts-tm)));add(i*K+k,j*K+k,H+1)
        return dict(us=np.array(us,np.int64),vs=np.array(vs,np.int64),co=np.array(co),owners=np.array(owners,np.int64),s=s,t=t,ts=ts,B=B,K=K,initial=initial)
    def response(self,w,all_chambers=False):
        ans=[]
        for g in self.graphs:
            cap=g['co'].copy();o=g['owners'];ids=o>=0;cap[ids]*=w[o[ids]]
            flow,src,_=dinic(g['t']+1,g['us'],g['vs'],cap,g['s'],g['t'])
            z=src[:g['s']].reshape(self.N,g['K']);surv=np.where(g['B'][:,None],z,~z)
            r=surv@np.diff(g['ts']);value=r@w
            assert abs(value-(self.H-flow))<1e-7, (value,self.H-flow,w.min(),w.sum(),initial if False else g['initial'])
            ans.append(dict(value=value,r=r,initial=g['initial'],graph=g))
        return ans if all_chambers else max(ans,key=lambda z:z['value'])

def optimize_support(ms,tol=2e-9,maxiter=500,verbose=False,half=False):
    """ms are full ordered reflection pairs. Row entries are averaged deadlines."""
    oracle=HalfOracle(ms) if half else PrincessOracle(ms);n=len(ms)//2
    rows=[];records=[]
    w=np.full(n,1/n);v=0
    for step in range(maxiter):
        responses=oracle.response(np.repeat(w/2,2),True)
        ub=max(z['value'] for z in responses)
        if verbose and (step%10==0 or ub-v<tol):print('lp',step,'constraints',len(rows),'value',v,'best response',ub,flush=True)
        added=0
        for z in responses:
            if not rows or z['value']>v+tol:
                row=(z['r'][::2]+z['r'][1::2])/2
                if any(np.max(abs(row-a))<1e-8 for a in rows):continue
                rows.append(row);records.append(z);added+=1
        if not added:break
        A=np.column_stack([np.array(rows),-np.ones(len(rows))])
        sol=linprog(np.r_[np.zeros(n),1.],A_ub=A,b_ub=np.zeros(len(rows)),A_eq=[np.r_[np.ones(n),0]],b_eq=[1.],bounds=[(0,None)]*n+[(None,None)],method='highs',options={'dual_feasibility_tolerance':1e-9,'primal_feasibility_tolerance':1e-9})
        assert sol.success,sol.message
        w=sol.x[:-1];v=sol.x[-1]
    dual=-sol.ineqlin.marginals
    return dict(value=v,upper=ub,weights=w,dual=dual,rows=np.array(rows),records=records,oracle=oracle,iterations=step+1)


def witness(ms,r,initial,delta=1e-5,side=0):
    H=max(m[-1,0] for m in ms)
    lows=[np.array([[0,-1],[H,-1]])];ups=[np.array([[0,1],[H,1]])]
    for m,ri in zip(ms,r):
        d=max(0,ri-delta);below=m[0,1]<initial;dr=-1 if below else 1
        q=np.vstack([m[m[:,0]<d-1e-12],[d,pos(m,d)],[H,pos(m,d)+dr*(H-d)]])
        q=simplify(q)
        (lows if below else ups).append(q)
    def env(curves,maximum):
        ts=np.unique(np.concatenate([q[:,0] for q in curves]));out=[]
        for a,b in zip(ts,ts[1:]):
            va=np.array([pos(q,a) for q in curves]);vb=np.array([pos(q,b) for q in curves]);cuts=[a,b]
            for i in range(len(curves)):
                for j in range(i):
                    d=va[i]-va[j];e=vb[i]-vb[j]
                    if d*e<-1e-20:cuts.append(a+(b-a)*abs(d)/(abs(d)+abs(e)))
            cuts=np.unique(cuts)
            for t in cuts[:-1]:
                z=va+(vb-va)*(t-a)/(b-a);out.append([t,max(z) if maximum else min(z)])
        vals=[pos(q,H) for q in curves];out.append([H,max(vals) if maximum else min(vals)])
        return simplify(out)
    L=env(lows,True);U=env(ups,False);ts=np.unique(np.r_[L[:,0],U[:,0]])
    gap=np.min(pos(U,ts)-pos(L,ts));assert gap>1e-12
    if side<0:p=L.copy();p[:,1]+=gap/3
    elif side>0:p=U.copy();p[:,1]-=gap/3
    else:
        blend=(initial-L[0,1])/(U[0,1]-L[0,1]);p=np.column_stack([ts,(1-blend)*pos(L,ts)+blend*pos(U,ts)])
    p=simplify(p)
    caps=np.array([meet(m,p) for m in ms]);assert np.min(caps-r)>-delta-1e-8
    return p,caps

class HalfOracle(PrincessOracle):
    """Exact geometry reduction to p(t)>=0 for symmetric monster mixtures.
    Justification: uncross the equal mixture of p and -p into +/-abs(p).
    """
    def __init__(self,ms):
        super().__init__(ms,True)
        starts=np.unique(np.r_[0,1,self.starts[self.starts>=0]])
        self.chambers=[(a,b) for a,b in zip(starts,starts[1:]) if b-a>1e-10]
        for i,m in enumerate(ms):self.ds[i,0]=meet(m,np.array([[0.,0.],[self.H,0.]]))
        self.graphs=[self.build((a+b)/2) for a,b in self.chambers]
