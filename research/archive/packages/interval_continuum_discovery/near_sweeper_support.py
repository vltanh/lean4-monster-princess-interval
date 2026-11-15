from pathlib import Path
import sys,json
import numpy as np
from direct_support import solve_support
from integer_geometry import clean,mirror
n=int(sys.argv[1]);S=8*n;names=[];ps=[];seen=set()
for ix in range(-n,n+1):
 x=8*ix
 for c in [2*S-x,S-4,S,S+4]:
  if not x<=c<=2*S-x:continue
  q=[[0,x],[(c-x)//2,(c+x)//2],[c+S,-S],[c+3*S,S]]
  if c+x==2*S:q=q[:-1]
  q=clean(q);key=min(tuple(map(tuple,q)),tuple(map(tuple,mirror(q))))
  if key in seen:continue
  seen.add(key);names.append([x/S,c/S]);ps.append(q)
ms=[q for p in ps for q in(p,mirror(p))]
d=solve_support(ms,S);d['names']=names;d['n']=n
print('ACTIVE',[(names[i],z)for i,z in enumerate(d['weights'])if z>1e-8],flush=True)
json.dump(d,open(Path(__file__).parent/f'near_sweeper_{n}.json','w'))
