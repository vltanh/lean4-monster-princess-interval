"""Affine germ payoffs for fixed unit-speed / central-wait monsters."""
import no_extra_family_lp as base
from pathlib import Path
import numpy as np,json,time
from scipy.optimize import linprog

def clean(points):
 out=[]
 for t,x in points:
  if out and t==out[-1][0]:assert x==out[-1][1];continue
  out.append((float(t),float(x)))
 return out

def route(kind,p):
 if kind==1:
  x=p;return clean([(0,x),(1-x,1),(3-x,-1)])
 if kind==2:
  x=p;return clean([(0,x),((1-x)/2,(1+x)/2),(2,-1),(4,1)])
 if kind==3:
  return clean([(0,0),(p,0),(p+1,1),(p+3,-1)])
 if kind==4:
  s,x=p;return clean([(0,x),((s-x)/2,(s+x)/2),(s+1,-1),(s+3,1)])
 if kind==5:
  x,t,sign=p
  return clean([(0,x),(x,0),(t,0),(t+1,sign),(t+3,-sign)])
 if kind==6:
  start,end,wait,sign=p
  return clean([(0,0),(start,0),((start+end)/2,(end-start)/2),(end,0),(wait,0),(wait+1,sign),(wait+3,-sign)])
 middle,end,wait,side,finish=p
 return clean([(0,0),(middle/2,middle/2),(middle,0),((middle+end)/2,side*(end-middle)/2),(end,0),(wait,0),(wait+1,finish),(wait+3,-finish)])

def capture(points,a,c,pa,pc):
 horizon=points[-1][0]+1
 if pa>pc:
  princess=[(-1,a,pa,0,0,(a+c)/2,(pa+pc)/2),
            (1,-c,-pc,(a+c)/2,(pa+pc)/2,1+c,1+pc)]
 else:
  princess=[(-1,a,pa,0,0,a,pa),(0,0,0,a,pa,c,pc),
            (1,-c,-pc,c,pc,1+c,1+pc)]
 princess.append((0,1,1,1+c,1+pc,horizon,horizon))
 for (t0,x0),(t1,x1) in zip(points,points[1:]):
  velocity=(x1-x0)/(t1-t0);intercept=x0-velocity*t0
  candidates=[]
  for speed,const,const_probe,start,start_probe,end,end_probe in princess:
   low=max(t0,start_probe);high=min(t1,end_probe)
   if high<low-1e-12:continue
   if abs(velocity-speed)<1e-12:
    if abs(intercept-const_probe)>1e-12:continue
    tprobe=low;tvalue=t0 if t0>=start_probe else start
   else:
    tprobe=(const_probe-intercept)/(velocity-speed)
    if tprobe<low-1e-12 or tprobe>high+1e-12:continue
    tvalue=(const-intercept)/(velocity-speed)
   candidates.append((tprobe,tvalue))
  if candidates:return min(candidates,key=lambda pair:pair[0])[1]
 raise AssertionError((points,a,c,pa,pc))

def payoff(points,a,c,pa,pc):
 return (capture(points,a,c,pa,pc)+capture([(t,-x)for t,x in points],a,c,pa,pc))/2

def main():
 start=time.time();etas=[1/64,1/32,1/16,1/8,1/4,1/2]
 starts=sorted(set([i/8 for i in range(-8,9)]+[s*(1-e)for e in etas for s in[-1,1]]));waits=sorted(set(abs(x)for x in starts))
 monsters=[(k,x)for k in[1,2]for x in starts]+[(3,t)for t in waits]
 monsters.extend((5,(x,t,sign))for x in[.25,.5,.75]for t in[.5,.75,.875,1.]if x<=t for sign in[-1,1])
 monsters.extend((6,(s,e,w,sign))for s in[0.,.25,.5]for e in[.5,.75,.875,.9375]if s<e for w in sorted(set([e,.9375]))for sign in[-1,1])
 monsters.extend((7,(middle,e,w,side,finish))for middle in[.25,.5]for e in[.75,.875,.9375]for w in sorted(set([e,.9375]))for side in[-1,1]for finish in[-1,1])
 rows,cells=base.arrangement(starts,waits)
 paths=[route(*monster)for monster in monsters]
 matrix=np.asarray([[payoff(path,*row)for path in paths]for row in rows])
 for j,(kind,p)in enumerate(monsters):
  if kind>3:continue
  assert max(abs(matrix[i,j]-base.payoff(*row,kind,p))for i,row in enumerate(rows))<1e-10,(kind,p)
 assert np.max(np.abs(matrix*256-np.round(matrix*256)))<1e-8
 sol=linprog(np.r_[np.zeros(len(monsters)),1.],A_ub=np.c_[matrix,-np.ones(len(rows))],b_ub=np.zeros(len(rows)),A_eq=[np.r_[np.ones(len(monsters)),0]],b_eq=[1],bounds=[(0,None)]*len(monsters)+[(None,None)],method='highs')
 assert sol.success,sol.message
 support,weights,v,chosen=base.rational_solution(matrix,sol)
 output=dict(value=str(v),decimal=float(v),monsters=[dict(kind=monsters[i][0],parameter=monsters[i][1],path=paths[i],weight=str(w),decimal=float(w))for i,w in zip(support,weights)],starts=starts,waits=waits,seconds=time.time()-start)
 json.dump(output,open(base.OUT/'no_extra_paths.json','w'),indent=2)
 print(json.dumps(output,indent=2))
if __name__=='__main__':main()
