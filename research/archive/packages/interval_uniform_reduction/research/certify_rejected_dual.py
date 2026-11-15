from integer_geometry import mirror,witness,meet
from integer_deadline import Oracle
from fractions import Fraction as Q
from functools import reduce
from math import gcd
import json,numpy as np,time
D=json.load(open('adaptive_checkpoint.json'));S=D['S'];active=[j for j,w in enumerate(D['weights_m'])if w>1e-8]
ms=[D['paths_m'][j]for j in active];w=np.array([D['weights_m'][j]for j in active]);w/=w.sum();n=np.rint(w*10**9).astype(np.int64);n[np.argmax(n)]+=10**9-int(sum(n));assert np.all(n>0)
full=[p for m in ms for p in(m,mirror(m))];fw=np.repeat(n/(2*10**9),2)
st=time.time();R=Oracle(full,S).response(fw);r=max(R,key=lambda z:z['value']);print('Oracle',r['value'],time.time()-st,flush=True)
p=witness(full,r['r'],r['initial'],S);caps=[meet(m,p)for m in full];assert all(t is not None for t in caps)
value=Q(sum(int(a)*t for a,t in zip(np.repeat(n,2),caps)),2*10**9*S);print('Exact defeating payoff',value,float(value),flush=True)
g=reduce(gcd,[S]+caps+[z for path in full+[p]for v in path for z in v]);scale=S//g
out=dict(scale=scale,monsters=[[[t//g,x//g]for t,x in m]for m in ms],pair_weights=[int(a)for a in n],princess=[[t//g,x//g]for t,x in p],payoff=str(value),captured_times=[t//g for t in caps])
assert all(t%g==0 for t in caps)
json.dump(out,open('/mnt/data/interval_uniform_reduction/rejected_dual.json','w'),separators=(',',':'))
