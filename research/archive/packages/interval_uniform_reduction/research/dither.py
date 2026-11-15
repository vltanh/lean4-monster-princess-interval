import json,numpy as np,subprocess,sys
from shape_search import clean
from scipy.optimize import linprog

def shiftpath(p,mul,shift,wall):
 p=[[int(t)*mul,int(x)*mul+shift]for t,x in p];out=[]
 for j,(t,x) in enumerate(p):
  if j:
   a,y=p[j-1]
   if (x-wall)*(y-wall)<0:
    assert abs(x-y)==t-a
    tt=a+abs(wall-y);out.append([tt,wall])
  out.append([t,min(wall,x)])
 return [[int(t),int(x)]for t,x in clean(out)]

def br(hs,ws,scale,limit=30000000):
 inp=[f'{len(hs)} {limit}']
 for p,w in zip(hs,ws):inp.append(f'{len(p)} {w:.17g}');inp.extend(f'{t} {x}'for t,x in p)
 proc=subprocess.run(['./grid_monster'],input='\n'.join(inp)+'\n',text=True,capture_output=True)
 if proc.returncode:raise RuntimeError(proc.stderr)
 out=proc.stdout.splitlines();v,nodes,leaves,pr,done,k=out[0].split();p=[list(map(int,z.split()))for z in out[1:]]
 return float(v)/scale,p,dict(nodes=int(nodes),leaves=int(leaves),complete=bool(int(done)))
if __name__=='__main__':
 n=int(sys.argv[1]);D=json.load(open(f'warm_{n}.json' if n>8 else 'transport_8_16.json'));ph=D['paths_h'];ww=D['weights_h'];pos=[];pw=[];cum=0
 for p,w in zip(ph,ww):
  lo=max(.5,cum);hi=min(1.,cum+w)
  if hi>lo+1e-9:pos.append(p);pw.append(hi-lo)
  cum+=w
 Q=100000;scale=4*n*Q;pp=[shiftpath(p,2*Q,2*(j+1),scale)for j,p in enumerate(pos)]
 hs=[[[t,-x]for t,x in p]for p in pp[::-1]]+pp;ws=np.r_[pw[::-1],pw];ws/=ws.sum()
 v,m,info=br(hs,ws,scale);print('DITHER',n,v,info,m,flush=True)
 json.dump(dict(scale=scale,paths=hs,weights=ws.tolist(),value=v,response=m,info=info),open(f'dither_{n}.json','w'))
