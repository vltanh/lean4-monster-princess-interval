"""Exact ordered-polynomial geometry over Q(epsilon), epsilon -> 0+.
Coordinates are dyadic multiples of 1/5**6, stored on a sufficiently fine
common integer scale; every division checks exact divisibility.
"""
from fractions import Fraction as F
from functools import total_ordering
import numpy as np
from core import dinic
S=2**512*5**6

@total_ordering
class P:
    __slots__=('c',)
    def __init__(self,x=0,coeff=None):
        if coeff is not None:c=tuple(coeff)
        elif isinstance(x,P):c=x.c
        else:
            q=F(x);assert S%q.denominator==0,(q,'unsupported denominator');c=(q.numerator*(S//q.denominator),)
        while len(c)>1 and c[-1]==0:c=c[:-1]
        self.c=c
    def __add__(a,b):
        if not isinstance(b,P):b=P(b)
        n=max(len(a.c),len(b.c));return P(coeff=tuple((a.c[i] if i<len(a.c) else 0)+(b.c[i] if i<len(b.c) else 0) for i in range(n)))
    __radd__=__add__
    def __neg__(a):return P(coeff=tuple(-x for x in a.c))
    def __sub__(a,b):return a+-P(b)
    def __rsub__(a,b):return P(b)+-a
    def __mul__(a,b):
        assert isinstance(b,int);return P(coeff=tuple(x*b for x in a.c))
    __rmul__=__mul__
    def __truediv__(a,b):
        assert isinstance(b,int) and b!=0
        assert all(x%b==0 for x in a.c),('scale exhausted',b)
        return P(coeff=tuple(x//b for x in a.c))
    def __eq__(a,b):return isinstance(b,P) and a.c==b.c or not isinstance(b,P) and a.c==P(b).c
    def __lt__(a,b):
        if not isinstance(b,P):b=P(b)
        for i in range(max(len(a.c),len(b.c))):
            x=a.c[i] if i<len(a.c) else 0;y=b.c[i] if i<len(b.c) else 0
            if x!=y:return x<y
        return False
    def __hash__(a):return hash(a.c)
    def __abs__(a):return -a if a<P(0) else a
    def __float__(a):return float(F(a.c[0],S))
    def __repr__(a):return '['+','.join(str(F(x,S)) for x in a.c)+']'
    def data(a):return [str(F(x,S)) for x in a.c]
    @classmethod
    def load(cls,c):return cls(coeff=tuple(int(F(x)*S) for x in c))

def eps(k):return P(coeff=(0,)*k+(S,))

def slope(t0,x0,t1,x1):
    dt=t1-t0;dx=x1-x0
    assert dt>0
    if dx==0:return 0
    if dx==dt:return 1
    if dx==-dt:return -1
    raise ValueError(('non-bang-bang segment',t0,x0,t1,x1))

def simplify(path):
    out=[]
    for t,x in path:
        t,x=P(t),P(x)
        if out and t==out[-1][0]:assert x==out[-1][1];continue
        assert not out or t>out[-1][0]
        out.append((t,x))
        while len(out)>=3:
            (a,x),(b,y),(c,z)=out[-3:]
            if slope(a,x,b,y)==slope(b,y,c,z):out.pop(-2)
            else:break
    return out

def pos(p,t):
    for (a,x),(b,y) in zip(p,p[1:]):
        if a<=t<=b:return x+(t-a)*slope(a,x,b,y)
    assert t>=p[-1][0];return p[-1][1]

def meet(p,q):
    ts=sorted(set(t for t,x in p+q));ds=[pos(p,t)-pos(q,t) for t in ts]
    for k,t in enumerate(ts):
        if ds[k]==0:return t
        if k+1<len(ts) and (ds[k]<0)!=(ds[k+1]<0):
            # Difference has slope in {-2,-1,1,2}.
            dt=ts[k+1]-t;dv=ds[k+1]-ds[k]
            for v in (-2,-1,1,2):
                if dv==dt*v:return t-ds[k]/v
            raise ValueError('bad slopes')
    return None

def mirror(p):return [(t,-x) for t,x in p]
def fold(p):
    ts=set(t for t,x in p)
    for (a,x),(b,y) in zip(p,p[1:]):
        if x!=0 and y!=0 and (x<0)!=(y<0):ts.add(a-x/slope(a,x,b,y))
    return simplify([(t,abs(pos(p,t))) for t in sorted(ts)])

def complete(m):
    for i,(t,x) in enumerate(m):
        if abs(x)==1:return simplify(m[:i+1]+[(t+2,-x)])
    t,x=m[-1];wall=P(1) if x>=0 else P(-1)
    return simplify(m+[(t+abs(wall-x),wall),(t+abs(wall-x)+2,-wall)])

def pairpay(m,h):
    a=meet(m,h);b=meet(m,mirror(h));assert a is not None and b is not None
    return (a+b)/2

def encode(path):return [[t.data(),x.data()] for t,x in path]
def decode(path):return [(P.load(t),P.load(x)) for t,x in path]

def degree(paths):return max(max(len(t.c),len(x.c))-1 for p in paths for t,x in p)

class Oracle:
    def __init__(self,ms):
        self.ms=ms;self.N=len(ms);self.H=max(p[-1][0] for p in ms)
        self.starts=[p[0][1] for p in ms]
        ss=sorted(set([P(-1),P(0),P(1)]+self.starts))
        self.chambers=[(a,b) for a,b in zip(ss,ss[1:]) if a>=0 and a<b]
        self.ds=[];self.pairs={}
        for i,m in enumerate(ms):
            ds=[meet(m,[(P(0),P(w)),(self.H,P(w))]) for w in(-1,1)]
            assert all(d is not None for d in ds);self.ds.append(ds)
            for j in range(i):self.pairs[i,j]=self.pairs[j,i]=meet(m,ms[j])
        self.graphs=[self.build((a+b)/2) for a,b in self.chambers]
    def build(self,initial):
        N=self.N;H=self.H;B=[x<initial for x in self.starts]
        ds=[self.ds[i][int(B[i])] for i in range(N)]
        pairs=[(i,j,self.pairs[i,j]) for i in range(N) if B[i] for j in range(N) if not B[j] and self.pairs[i,j] is not None and self.pairs[i,j]<H]
        ts=sorted(set([P(0),H]+ds+[t for i,j,t in pairs]));K=len(ts)-1;idx={t:k for k,t in enumerate(ts)}
        us=[];vs=[];co=[];owners=[];s=N*K;t=s+1
        def add(u,v,c,owner=-1):us.append(u);vs.append(v);co.append(float(c));owners.append(owner)
        for i in range(N):
            for k in range(K):
                dt=ts[k+1]-ts[k]
                if B[i]:add(s,i*K+k,dt,i)
                else:add(i*K+k,t,dt,i)
            for k in range(K-1):
                if B[i]:add(i*K+k+1,i*K+k,H+1)
                else:add(i*K+k,i*K+k+1,H+1)
            if ds[i]<H:
                k=idx[ds[i]]
                if B[i]:add(i*K+k,t,H+1)
                else:add(s,i*K+k,H+1)
        for i,j,tm in pairs:add(i*K+idx[tm],j*K+idx[tm],H+1)
        return dict(us=np.array(us,np.int64),vs=np.array(vs,np.int64),co=np.array(co),owners=np.array(owners,np.int64),s=s,t=t,ts=ts,B=np.array(B),K=K,initial=initial,ds=ds,pairs=pairs)
    def response(self,w):
        ans=[]
        for g in self.graphs:
            cap=g['co'].copy();o=g['owners'];ids=o>=0;cap[ids]*=w[o[ids]]
            flow,src,_=dinic(g['t']+1,g['us'],g['vs'],cap,g['s'],g['t'])
            labels=src[:g['s']].reshape(self.N,g['K']);surv=np.where(g['B'][:,None],labels,~labels)
            r=[]
            for i in range(self.N):
                # Zero-capacity event intervals still obey implications.
                assert np.all(np.diff(surv[i].astype(int))<=0)
                r.append(g['ts'][int(surv[i].sum())])
            assert all(r[i]<=g['ds'][i] for i in range(self.N))
            assert all(min(r[i],r[j])<=t for i,j,t in g['pairs'])
            v=sum(ww*float(rr) for ww,rr in zip(w,r));assert abs(v-(float(self.H)-flow))<1e-7
            ans.append(dict(value=v,r=r,initial=g['initial']))
        return ans

def witness(ms,r,initial,level=None):
    H=max(m[-1][0] for m in ms)
    if level is None:level=degree(ms)+1
    delta=eps(level);eta=eps(level+1)
    ups=[[(P(0),P(1)),(H,P(1))]];lows=[[(P(0),P(-1)),(H,P(-1))]]
    for m,ri in zip(ms,r):
        e=max(P(0),ri-delta);dr=-1 if m[0][1]<initial else 1
        q=[(t,x) for t,x in m if t<e]+[(e,pos(m,e))]
        if e<H:q.append((H,pos(m,e)+(H-e)*dr))
        q=simplify(q);(lows if dr<0 else ups).append(q)
    # Build the exact upper envelope by finding all pairwise intersections on common pieces.
    curves=ups
    ts=sorted(set(t for q in curves for t,x in q));cuts=set(ts)
    for a,b in zip(ts,ts[1:]):
        va=[pos(q,a) for q in curves];vb=[pos(q,b) for q in curves]
        for i in range(len(curves)):
            for j in range(i):
                d=va[i]-va[j];e=vb[i]-vb[j]
                if d!=0 and e!=0 and (d<0)!=(e<0):
                    dv=e-d;dt=b-a
                    for slope in(-2,-1,1,2):
                        if dv==dt*slope:cuts.add(a-d/slope);break
                    else:raise ValueError('bad envelope slopes')
    U=simplify([(t,min(pos(q,t) for q in curves)) for t in sorted(cuts)])
    p=simplify([(t,x-eta) for t,x in U])
    # Explicitly check all requested survival deadlines in the ordered field.
    caps=[meet(m,p) for m in ms]
    assert all(t is not None and t>=ri-delta for t,ri in zip(caps,r)),('witness',caps,r)
    assert all(-1<=x<=1 for t,x in p)
    return p

def envelope(curves,maximum=False):
    ts=sorted(set(t for q in curves for t,x in q));cuts=set(ts)
    for a,b in zip(ts,ts[1:]):
        va=[pos(q,a) for q in curves];vb=[pos(q,b) for q in curves]
        for i in range(len(curves)):
            for j in range(i):
                d=va[i]-va[j];e=vb[i]-vb[j]
                if d!=0 and e!=0 and (d<0)!=(e<0):
                    dv=e-d;dt=b-a
                    for v in(-2,-1,1,2):
                        if dv==dt*v:cuts.add(a-d/v);break
                    else:raise ValueError('bad slopes')
    select=max if maximum else min
    return simplify([(t,select(pos(q,t) for q in curves)) for t in sorted(cuts)])

def witness_clamp(ms,r,initial,level=None):
    H=max(m[-1][0] for m in ms)
    if level is None:level=degree(ms)+1
    delta=eps(level);eta=eps(level+1)
    ups=[[(P(0),P(1)),(H,P(1))]];lows=[[(P(0),P(-1)),(H,P(-1))]]
    for m,ri in zip(ms,r):
        e=max(P(0),ri-delta);dr=-1 if m[0][1]<initial else 1
        q=[(t,x) for t,x in m if t<e]+[(e,pos(m,e))]
        if e<H:q.append((H,pos(m,e)+(H-e)*dr))
        q=simplify(q);(lows if dr<0 else ups).append(q)
    L=[(t,x+eta) for t,x in envelope(lows,True)]
    U=[(t,x-eta) for t,x in envelope(ups,False)]
    lo=envelope([[(P(0),initial),(H,initial)],U],False)
    p=envelope([L,lo],True)
    caps=[meet(m,p) for m in ms]
    assert all(t is not None and t>=ri-delta for t,ri in zip(caps,r)),('witness clamp',caps,r)
    assert all(-1<=x<=1 for t,x in p)
    return p

class HalfOracle(Oracle):
    def __init__(self,ms):
        super().__init__(ms)
        for i,m in enumerate(ms):
            self.ds[i][0]=meet(m,[(P(0),P(0)),(self.H,P(0))])
            assert self.ds[i][0] is not None
        self.graphs=[self.build((a+b)/2) for a,b in self.chambers]

def quantiles(paths,weights,K=64,return_debug=False):
    """Exact geometry; numeric quantile weights for discovery only."""
    assert len(paths)==len(weights)
    weights=np.array(weights,float);weights/=weights.sum()
    ts=sorted(set(t for p in paths for t,x in p));cuts=set(ts)
    n=len(paths)
    for a,b in zip(ts,ts[1:]):
        va=[pos(p,a) for p in paths];vb=[pos(p,b) for p in paths]
        ss=[slope(a,x,b,y) for x,y in zip(va,vb)]
        for i in range(n):
            for j in range(i):
                d=va[i]-va[j];e=vb[i]-vb[j]
                if d!=0 and e!=0 and (d<0)!=(e<0):
                    cuts.add(a-d/(ss[i]-ss[j]))
    ts=sorted(cuts);out=[[] for _ in range(K)]
    qs=(np.arange(K)+.5)/K
    for a,b in zip(ts,ts[1:]):
        mid=(a+b)/2;order=sorted(range(n),key=lambda j:pos(paths[j],mid))
        cw=np.cumsum(weights[order]);inds=np.minimum(np.searchsorted(cw,qs),n-1)
        for k,i in enumerate(inds):
            j=order[i]
            if not out[k] or out[k][-1][0]!=a:out[k].append((a,pos(paths[j],a)))
            else:assert out[k][-1][1]==pos(paths[j],a)
            out[k].append((b,pos(paths[j],b)))
    out=[simplify(p) for p in out]
    if return_debug:return out,dict(time_intervals=len(ts)-1,input_paths=n,output_paths=K)
    return out

def witness_play(ms,r,initial,delta=None,half=True):
    """Lazy speed-one path in the exact survival corridor, constant or formal."""
    H=max(m[-1][0] for m in ms)
    if delta is None:delta=eps(degree(ms)+1)
    ups=[[(P(0),P(1)),(H,P(1))]];lows=[[(P(0),P(0 if half else -1)),(H,P(0 if half else -1))]]
    for m,ri in zip(ms,r):
        e=max(P(0),ri-delta);dr=-1 if m[0][1]<initial else 1
        q=[(t,x) for t,x in m if t<e]+[(e,pos(m,e))]
        if e<H:q.append((H,pos(m,e)+(H-e)*dr))
        q=simplify(q);(lows if dr<0 else ups).append(q)
    L=envelope(lows,True);U=envelope(ups,False)
    ts=sorted(set(t for t,x in L+U));gap=min(pos(U,t)-pos(L,t) for t in ts);assert gap>0
    eta=gap/4
    L=[(t,x+eta) for t,x in L];U=[(t,x-eta) for t,x in U]
    x=min(max(initial,pos(L,P(0))),pos(U,P(0)));out=[(P(0),x)]
    for a,b in zip(ts,ts[1:]):
        la,lb=pos(L,a),pos(L,b);ua,ub=pos(U,a),pos(U,b)
        assert la<=x<=ua
        if lb>x:
            assert lb-la==b-a
            hit=a+x-la
            if hit>a:out.append((hit,x))
            out.append((b,lb));x=lb
        elif ub<x:
            assert ua-ub==b-a
            hit=a+ua-x
            if hit>a:out.append((hit,x))
            out.append((b,ub));x=ub
        else:out.append((b,x))
    p=simplify(out)
    caps=[meet(m,p) for m in ms]
    assert all(t is not None and t>=ri-delta for t,ri in zip(caps,r))
    assert all(0<=x<=1 for t,x in p) if half else all(-1<=x<=1 for t,x in p)
    return p
