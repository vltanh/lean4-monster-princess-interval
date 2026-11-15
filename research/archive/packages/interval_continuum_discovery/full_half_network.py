import json, sys, time, pathlib
import numpy as np

REPO=pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0,str(REPO/'packages/interval_uniform_reduction/research'))
from network_transport import Network, LP
from integer_geometry import clean, meet

def clipshift(p,eps,S):
    out=[]
    for j,(t,x) in enumerate(p):
        y=x+eps
        if j:
            a,z=p[j-1]; z+=eps
            if (y-S)*(z-S)<0:
                assert abs(y-z)==t-a
                out.append([a+abs(S-z),S])
        out.append([t,min(y,S)])
    return clean(out)

def basis(n,S,eps):
    h=S//n
    ps=[];seen=set()
    for i in range(2*n):
        for j in range(max(0,i-n),n+1):
            for k in (j-1,j,j+1):
                if not max(0,i+1-n)<=k<=n:continue
                t=i*h; s=(i+1)*h; x=j*h; y=k*h
                p=clean([[0,x],[t,x],[s,y],[s+S-y,S],[2*S,S]])
                p=clipshift(p,eps,S)
                key=tuple(map(tuple,p))
                if key not in seen:seen.add(key);ps.append(p)
    return ps

def monsters(n,S):
    ms=[];names=[]
    for kind in (1,2):
        for i in range(-n,n+1):
            x=i*S//n;c=2*S-x if kind==1 else S
            assert (c-x)%2==0 and (c+x)%2==0
            p=[[0,x],[(c-x)//2,(c+x)//2],[c+S,-S],[c+3*S,S]]
            if c+x==2*S:p=p[:-1]
            p=clean(p)
            ms.append(p);names.append((kind,i/n))
    return ms,names

if __name__=='__main__':
    n=int(sys.argv[1]) if len(sys.argv)>1 else 16
    nm=int(sys.argv[2]) if len(sys.argv)>2 else 32
    S=4*n*nm*10000;eps=4
    st=time.time();ps=basis(n,S,eps)
    print('BASIS',n,len(ps),'scale',S,'epsilon',eps/S,flush=True)
    net=Network(ps,S)
    print('NETWORK',len(net.segs),len(net.slabs),net.NF,len(net.orders),'secs',time.time()-st,flush=True)
    lp=LP(net);ms,names=monsters(nm,S);kept=[]
    for m,name in zip(ms,names):
        if lp.add(m):kept.append(name)
    print('LP',len(lp.ms),lp.N,len(lp.rows),'secs',time.time()-st,flush=True)
    v,F,mw=lp.solve();hs,ws,err=net.quantiles(F)
    checks=[net.payoff(m,F) for m in lp.ms]
    print('RESULT',v,'min_cdf',min(checks),'paths',len(hs),'round_error',err,'secs',time.time()-st,flush=True)
    out=dict(n=n,nm=nm,S=S,epsilon=eps,paths_h=hs,weights_h=ws.tolist(),paths_m=lp.ms,weights_m=mw.tolist(),names_m=kept,F=F.tolist(),value=v,round_error=err)
    dest=pathlib.Path(__file__).parent/f'full_half_network_{n}.json'
    dest.write_text(json.dumps(out))
    print('ACTIVE M',[(name,float(w)) for name,w in zip(kept,mw) if w>1e-8],flush=True)
    for i in np.argsort(ws)[-20:][::-1]:
        print('HIDER',i,ws[i],[[t/S,x/S] for t,x in hs[i]],flush=True)
