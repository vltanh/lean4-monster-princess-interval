from pathlib import Path
import sys,json
from direct_support import solve_support
from integer_geometry import clean,mirror
n=int(sys.argv[1]);S=8*n;names=[];ps=[];seen=set()
for ix in range(-n,n+1):
 x=8*ix
 for kind in [1,2,3]:
  if kind==1:q=[[0,x],[S-x,S],[3*S-x,-S]]
  elif kind==2:q=[[0,x],[(S-x)//2,(S+x)//2],[2*S,-S],[4*S,S]]
  else:q=[[0,x],[(S-x)//2,(S+x)//2],[S,0],[2*S,S],[4*S,-S]]
  q=clean(q);key=min(tuple(map(tuple,q)),tuple(map(tuple,mirror(q))))
  if key in seen:continue
  seen.add(key);names.append([kind,x/S]);ps.append(q)
ms=[q for p in ps for q in(p,mirror(p))]
d=solve_support(ms,S);d['names']=names;d['n']=n
print('ACTIVE',[(names[i],z)for i,z in enumerate(d['weights'])if z>1e-8],flush=True)
json.dump(d,open(Path(__file__).parent/f'center_return_{n}.json','w'))
