"""Small exhaustive cross-checks; exact arithmetic throughout."""
from fractions import Fraction as F
from random import Random
from exact_response import solve,build_paths,capture
from finite_grid import verify as verify_grid
from pathlib import Path
R=Random(20261110)

def clean(p):
    out=[]
    for z in p:
        if out and z==out[-1]:continue
        out.append(z)
        while len(out)>=3:
            (a,x),(b,y),(c,z)=out[-3:]
            if (y-x)*(c-b)==(z-y)*(b-a):out.pop(-2)
            else:break
    return out

def at(p,t):
    for(a,x),(b,y)in zip(p,p[1:]):
        if a<=t<=b:return F(x)+F((y-x)*(t-a),b-a)
    return F(p[-1][1])

def order_sample():
    S=16;raw=[]
    for j in range(3):
        x=R.randrange(1,8)*2;p=[[0,x]]
        for k in range(1,6):
            x=max(0,min(S,x+2*R.choice([-1,0,1])));p.append([2*k,x])
        raw.append(p)
    times=set(t for p in raw for t,x in p)
    for a,b in zip(range(0,10,2),range(2,12,2)):
        for i in range(3):
            for j in range(i):
                u=at(raw[i],a)-at(raw[j],a);v=at(raw[i],b)-at(raw[j],b)
                if u*v<0:times.add(F(a)+F(b-a)*abs(u)/(abs(u)+abs(v)))
    hs=[[]for _ in raw]
    for t in sorted(times):
        xs=sorted(at(p,t)for p in raw)
        for p,x in zip(hs,xs):
            assert (2*t).denominator==(2*x).denominator==1
            p.append([int(2*t),int(2*x)])
    hs=[clean(p)for p in hs]
    return [[ [t,-x]for t,x in p]for p in hs[::-1]]+hs,[1]*6,2*S

def cdf_check(raw,weights,S):
    # A unit-speed complete sweep, preceded by a randomized short walk.
    x=R.randrange(-S//2,S//2+1)*2;m=[[0,x]];t=0
    for _ in range(4):
        y=x+R.choice([-2,0,2]);y=max(-S,min(S,y));t+=2;m.append([t,y]);x=y
    first=-S if x<0 else S
    if x!=first:t+=abs(x-first);m.append([t,first])
    t+=2*S;m.append([t,-first]);H=F(t);m=clean(m)
    events={F(0),H}
    for p in raw:
        ts=sorted(set([F(t)for t,x in p+m]+[H]));ts=[t for t in ts if t<=H]
        events.update(ts)
        for a,b in zip(ts,ts[1:]):
            u=at(p,a)-at(m,a);v=at(p,b)-at(m,b)
            if u*v<0:events.add(a+(b-a)*abs(u)/(abs(u)+abs(v)))
    events=sorted(events);L=F(1);Rr=F(0);val=F(0);W=sum(weights)
    for a,b in zip(events,events[1:]):
        x=at(m,a);lo=F(sum(w for p,w in zip(raw,weights)if at(p,a)<x),W);hi=F(sum(w for p,w in zip(raw,weights)if at(p,a)<=x),W)
        L=min(L,lo);Rr=max(Rr,hi);val+=(b-a)*(1-Rr+L)
    direct=sum(w*min(capture(m,p),H)for p,w in zip(raw,weights))/W
    assert val==direct,(val,direct)

for case in range(40):
    ps,ws,S=order_sample();a,_,_=solve(ps,ws,S,cached=True);b,_,_=solve(ps,ws,S,cached=False);c,_,_=solve(ps,ws,S,prune=False)
    assert a==b==c
    cdf_check(ps,ws,S)
print('PASS: 40 cached / naive / unpruned exact searches agree.')
print('PASS: 40 CDF survival identities agree with direct capture-time integration.')
verify_grid(str(Path(__file__).resolve().parent/'grid_case.json'))
