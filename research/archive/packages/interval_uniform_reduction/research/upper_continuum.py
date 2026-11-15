from compressed_ipm import CompressedOracle
from shape_search import monster
import numpy as np,json,time,sys
n=int(sys.argv[1]);st=time.time();names=[(1,-1.)]+[(1,j/n)for j in range(n//2,n)]+[(2,j/n)for j in range(-n+1,n)if abs(j)>=n//8]
ps=[monster(x,2-x if k==1 else 1.)for k,x in names];ms=[np.array(q)for p in ps for q in(p,[[t,-x]for t,x in p])];o=CompressedOracle(ms);print('GEOMETRY',n,len(ms),len(o.graphs),time.time()-st,flush=True)
v,w=o.solve();rr=o.response(np.repeat(w/2,2));up=max(z['value']for z in rr);print('RESULT',n,v,up,'seconds',time.time()-st,flush=True)
print('ACTIVE',[(a,float(b))for a,b in zip(names,w)if b>1e-8],flush=True)
json.dump(dict(n=n,value=v,upper=up,names=names,weights=w.tolist(),paths=[p.tolist()for p in ms],responses=rr),open(f'upper_continuum_{n}.json','w'))
