import json, sys, time, pathlib
import numpy as np
from full_half_network import Network,LP,basis,monsters,REPO
from integer_geometry import complete,clean
sys.path.insert(0,str(REPO/'packages/interval_uniform_reduction'))
from exact_response import solve

n=int(sys.argv[1]) if len(sys.argv)>1 else 16
nm=32;S=4*n*nm*10000;eps=4;st=time.time()
net=Network(basis(n,S,eps),S);lp=LP(net)
for m in monsters(nm,S)[0]:lp.add(m)
seed=json.load(open(pathlib.Path(__file__).parent/f'full_half_network_{n}.json'))
lp.add(complete(seed['response'],S))
log=[]
for it in range(24):
    v,F,mw=lp.solve();hs,ws,err=net.quantiles(F)
    iw=[round(w*100000000) for w in ws];assert min(iw)>0
    raw=[[[t,-x] for t,x in p] for p in hs[::-1]]+hs
    vv,m,stats=solve(raw,iw[::-1]+iw,S,node_limit=2000000)
    m=clean(m)
    row=dict(iteration=it,upper=v,response=str(vv),nodes=stats['nodes'],hiders=len(hs),monsters=len(lp.ms),seconds=time.time()-st,route=m)
    log.append(row)
    print('ITER',it,'v',v,'response',float(vv),'hiders',len(hs),'monsters',len(lp.ms),'nodes',stats['nodes'],'seconds',time.time()-st,flush=True)
    print('ROUTE',[[t/S,x/S] for t,x in m],flush=True)
    d=dict(n=n,nm=nm,S=S,epsilon=eps,paths_h=hs,weights_h=iw,paths_m=lp.ms,weights_m=mw.tolist(),F=F.tolist(),value=v,response=str(vv),response_path=m,log=log)
    (pathlib.Path(__file__).parent/f'full_half_separation_{n}.json').write_text(json.dumps(d))
    if v-float(vv)<2e-7: print('CLOSED_NETWORK',flush=True);break
    if not lp.add(complete(m,S)):print('REPEATED',flush=True);break
