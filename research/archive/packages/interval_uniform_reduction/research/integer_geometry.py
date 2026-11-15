"""Exact integer geometry; every rational division is checked."""
import bisect,subprocess
import numpy as np

def clean(p):
 out=[]
 for t,x in p:
  assert isinstance(t,int)and isinstance(x,int)
  if out and t==out[-1][0]:assert x==out[-1][1];continue
  assert not out or t>out[-1][0]
  out.append([t,x])
  while len(out)>2:
   (a,x),(b,y),(c,z)=out[-3:]
   if (y-x)*(c-b)==(z-y)*(b-a):out.pop(-2)
   else:break
 return out

def pos(p,t):
 i=bisect.bisect_right([a for a,x in p],t)-1;assert i>=0
 if i+1==len(p):return p[-1][1]
 a,x=p[i];b,y=p[i+1];assert (y-x)%(b-a)==0
 return x+(t-a)*((y-x)//(b-a))

def meet(p,q):
 ts=sorted(set(t for t,x in p+q));prev=None
 for t in ts:
  d=pos(p,t)-pos(q,t)
  if not d:return t
  if prev is not None:
   a,e=prev
   if (d<0)!=(e<0):
    assert (d-e)%(t-a)==0
    v=(d-e)//(t-a);assert e%v==0
    return a-e//v
  prev=t,d
 return None

def mirror(p):return [[t,-x]for t,x in p]

def complete(m,S):
 m=clean(m)
 for i,(t,x)in enumerate(m):
  if abs(x)==S:return clean(m[:i+1]+[[t+2*S,-x]])
 t,x=m[-1];w=S if x>=0 else -S
 return clean(m+[[t+abs(w-x),w],[t+abs(w-x)+2*S,-w]])

def envelope(curves,maximum):
 ts=sorted(set(t for p in curves for t,x in p));out=[]
 for a,b in zip(ts,ts[1:]):
  va=[pos(p,a)for p in curves];vb=[pos(p,b)for p in curves];vv=[(y-x)//(b-a)for x,y in zip(va,vb)];cuts={a,b}
  for i in range(len(curves)):
   for j in range(i):
    d=va[i]-va[j];e=vb[i]-vb[j]
    if d and e and (d<0)!=(e<0):
     v=vv[i]-vv[j];assert d%v==0;cuts.add(a-d//v)
  for t in sorted(cuts)[:-1]:out.append([t,(max if maximum else min)(x+(t-a)*v for x,v in zip(va,vv))])
 out.append([ts[-1],(max if maximum else min)(pos(p,ts[-1])for p in curves)])
 return clean(out)

def witness(ms,r,initial,S,delta=None,style='play'):
 H=max(p[-1][0]for p in ms)
 if delta is None:delta=max(4,S//1_000_000)
 ups=[[[0,S],[H,S]]];lows=[[[0,0],[H,0]]]
 for m,ri in zip(ms,r):
  e=max(0,ri-delta);dr=-1 if m[0][1]<initial else 1
  q=[[t,x]for t,x in m if t<e]+[[e,pos(m,e)]]
  if e<H:q.append([H,pos(m,e)+(H-e)*dr])
  (lows if dr<0 else ups).append(clean(q))
 L=envelope(lows,True);U=envelope(ups,False);ts=sorted(set(t for t,x in L+U));gap=min(pos(U,t)-pos(L,t)for t in ts);assert gap>4,('gap',gap,S)
 eta=gap//4;L=[[t,x+eta]for t,x in L];U=[[t,x-eta]for t,x in U]
 x=min(max(initial,pos(L,0)),pos(U,0));out=[[0,x]]
 for a,b in zip(ts,ts[1:]):
  la,lb=pos(L,a),pos(L,b);ua,ub=pos(U,a),pos(U,b);assert la<=x<=ua
  if style=='upper':
   # Greedily move toward +1 until encountering U, but never violate L.
   if x+(b-a)<=ub:out.append([b,x+b-a]);x+=b-a
   else:
    v=(ub-ua)//(b-a)
    if v==1:raise AssertionError('upper moving away')
    num=ua-x;den=1-v;assert num%den==0
    h=a+num//den
    if h>a:out.append([h,x+h-a])
    out.append([b,ub]);x=ub
  elif lb>x:
   assert lb-la==b-a;hit=a+x-la
   if hit>a:out.append([hit,x])
   out.append([b,lb]);x=lb
  elif ub<x:
   assert ua-ub==b-a;hit=a+ua-x
   if hit>a:out.append([hit,x])
   out.append([b,ub]);x=ub
  else:out.append([b,x])
 p=clean(out)
 caps=[meet(m,p)for m in ms];assert all(t is not None and t>=ri-delta for t,ri in zip(caps,r))
 # At first endpoint, become absorbing. Finish at +1 when the corridor ends.
 for j,(t,x)in enumerate(p):
  if x==S:p=p[:j+1];break
 else:
  t,x=p[-1]
  if x<S:p.append([t+S-x,S])
 return clean(p)

def br(hs,ws,S,limit=30_000_000):
 inp=[f'{len(hs)} {limit} {S}']
 for p,w in zip(hs,ws):
  inp.append(f'{len(p)} {w:.18g}')
  for t,x in p:inp.extend([f'1 {t}',f'1 {x}'])
 proc=subprocess.run(['./ordered_monster'],input='\n'.join(inp)+'\n',text=True,capture_output=True)
 if proc.returncode:raise RuntimeError(proc.stderr)
 out=proc.stdout.splitlines();v,nodes,leaves,pr,done,k=out[0].split();it=iter(out[1:]);p=[]
 for j in range(int(k)):
  a=list(map(int,next(it).split()));b=list(map(int,next(it).split()));assert a[0]==b[0]==1;p.append([a[1],b[1]])
 p=clean(p);val=sum(w*meet(p,h)/S for w,h in zip(ws,hs));assert abs(val-float(v))<1e-7
 return val,p,dict(nodes=int(nodes),leaves=int(leaves),complete=bool(int(done)))

def br_batch(hs,ws,S,limit=30_000_000):
 inp=[f'{len(hs)} {limit} {S}']
 for p,w in zip(hs,ws):
  inp.append(f'{len(p)} {w:.18g}')
  for t,x in p:inp.extend([f'1 {t}',f'1 {x}'])
 proc=subprocess.run(['./ordered_batch'],input='\n'.join(inp)+'\n',text=True,capture_output=True)
 if proc.returncode:raise RuntimeError(proc.stderr)
 lines=proc.stdout.splitlines();nr,nodes,done=map(int,lines[0].split());it=iter(lines[1:]);ans=[]
 for j in range(nr):
  v,k=next(it).split();p=[]
  for z in range(int(k)):
   a=list(map(int,next(it).split()));b=list(map(int,next(it).split()));assert a[0]==b[0]==1;p.append([a[1],b[1]])
  p=clean(p);val=sum(w*meet(p,h)/S for w,h in zip(ws,hs));assert abs(val-float(v))<1e-7
  ans.append((val,p))
 return ans,dict(nodes=nodes,complete=bool(done),leaves=nr)
