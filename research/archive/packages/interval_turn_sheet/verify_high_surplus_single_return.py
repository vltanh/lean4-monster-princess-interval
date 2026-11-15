"""Independently audit the high-surplus all-count single-return theorem.

The proof is analytic. This standard-library program checks its rational
coefficients, saved-field sign gates, and 980 independent physical renewal
versus closed-energy comparisons on productive chains with 2..8 returns.
No claim that finitely many fixtures exhaust arbitrary legal paths.
"""
from fractions import Fraction as F
import random, json
K=F(655898601421,62500000000)
EL=F(820954217,12500000000)
D=K-EL
B=F(15,16)
C=-F(7,8)*D
R=EL/K
A=K/8-EL/2
BB=K/4-EL/2
CC=(K+EL)/(4*K)
DD=EL*EL/(8*K)
TT=EL*(3-R)/2
ETA=F(3,8)
MU=(-25*K+4748*EL-1576*EL*EL/K)/8192
HCRIT=16*EL/(K-8*EL+2*EL*EL/K)
assert MU>0 and HCRIT>F(1,16)
assert MU == (-(F(25)*K)+F(4748)*EL-F(1576)*EL*EL/K)/F(8192)
assert K > F(8)*EL and F(0)<R<F(1,8)
def z(t):return D*t+C

def E(h,y):
 m=len(h)
 Q=A*sum(v*v for v in h)-EL/2*sum(h[i]*h[i+1] for i in range(m-1))-3*EL/2*h[-1]
 Q-=y*h[0]/2+y*y/(8*K)+max(F(0),y-D*h[0])**2/(8*K)
 Q-=sum(max(F(0), EL*h[i-1]-D*h[i])**2/(8*K) for i in range(1,m-1))
 if m>=2:Q-=max(F(0),EL*h[-2]-D*h[-1])/2
 return Q

def T(t,q,terminal=False):
 if terminal:return t*q+max(F(0),q-z(t))
 return t*q+max(F(0),q-z(t))**2/(4*K)

def direct(h,y):
 H=sum(h);t=B-H;prev=z(t)+y;total=F(0)
 for j,hi in enumerate(h):
  e=t+hi;new=z(e)+EL*hi
  assert new>=prev
  last=j==len(h)-1
  total+=(T(t,new)-T(t,prev)+T(e,new,last)-T(e,prev,last))/2
  t=e;prev=new
  assert new<=1
 assert t==B
 total+=(B+2)*(1-prev)
 return total

rng=random.Random(20261112)
checks=0; witnesses=[]; tested_counts={}; tested_horizons={}
for H in [F(1,16),F(1,20),F(1,25),F(1,30),F(1,40),F(1,64),F(1,128)]:
 for m in range(2,9):
  for trial in range(20):
   # Monotone-productive construction: choose positive h1 and spread tail
   # in a geometric baseline with a free positive simplex supplement.
   ratio=F(rng.randint(400,940),1000)
   h1=H*ratio
   if m>=2:
    base=[];last=h1
    for i in range(m-1):
     last=R*last
     base.append(last)
    if sum(base)>=H-h1: continue
    remain=H-h1-sum(base)
    shares=[rng.randint(1,100) for _ in base];su=sum(shares)
    # For enough productivity at later steps, allocate extra from left to right,
    # then project to a legal monotone-renewal sequence.
    tail=[];last=h1
    for i in range(len(base)):
     v=base[i]+remain*F(shares[i],su)
     tail.append(v)
    hs=[h1]+tail
    if any(K*hs[i]<EL*hs[i-1] for i in range(1,m)):
     # feasible by choosing a geometric tail supplemented at last.
     tail=[];last=h1
     for i in range(m-2):
      last=R*last;tail.append(last)
     tail.append(H-h1-sum(tail))
     hs=[h1]+tail
    if any(K*hs[i]<EL*hs[i-1] for i in range(1,m)):continue
   if ratio<ETA:continue
   yr=ETA+(ratio-ETA)*F(rng.randint(1,9),10)
   y=K*H*yr
   assert y<=K*hs[0]
   E1=E([H],y);em=E(hs,y)
   g=em-E1
   assert g>=MU*H, (m,H,y,g-MU*H)
   # Independent source-moment energy difference check.
   delta=direct(hs,y)-direct([H],y)
   assert delta==g,(m,H,y,delta,g)
   checks+=1
   tested_counts[m]=tested_counts.get(m,0)+1
   tested_horizons[str(H)]=tested_horizons.get(str(H),0)+1
   if trial==0:witnesses.append({'m':m,'H':str(H),'y':str(y),'gap':str(g),'certified_min_gap':str(MU*H)})
print(json.dumps({'status':'PASS','checks':checks,'exact_margin_coefficient':str(MU),'margin_decimal':float(MU),'duration_critical':str(HCRIT),'duration_critical_decimal':float(HCRIT),'counts':tested_counts,'horizons':tested_horizons,'last_gap_positive':g>=MU*H},indent=2))

# Separate exact departure-time theorem: one-return after a center wait.
# No new rank is captured during the wait; the return is productive at b.
# The time-excess functional is strictly concave in the final tent length.
def one_wait_cost(h, H, y):
    g=y-D*H
    nnew=z(B)+EL*h
    ns=z(B-H)+y
    assert h >= 0 and g+D*h >= 0 and nnew >= ns
    return ((B-h/F(2))*(EL*h-g)+K*h*h/F(8)
            -(g+D*h)**2/(F(8)*K)
            +(EL*h-max(F(0),g))/F(2)
            +(B+2)*(1-z(B)-EL*h))

wait_checks=0
for H in [F(1,16),F(1,20),F(1,30),F(1,64)]:
    for yr in [F(1,8),F(1,4),F(3,8),F(1,2),F(3,4),F(15,16)]:
        y=yr*K*H
        g=y-D*H
        low=max(F(0), H-y/D, max(F(0),g)/EL)
        assert 0<=low<H
        for a,b in [(F(1,5),F(4,5)),(F(0),F(1)),(F(1,3),F(2,3))]:
            x=low+(H-low)*a
            e=low+(H-low)*b
            m=(x+e)/2
            for h in [x,e,m]:
                assert one_wait_cost(h,H,y)==direct([h],g+D*h)
                wait_checks+=1
            exact_gap=one_wait_cost(m,H,y)-(one_wait_cost(x,H,y)+one_wait_cost(e,H,y))/2
            assert exact_gap==EL*(2*K+EL)*(e-x)**2/(32*K)
            assert exact_gap>0
            assert one_wait_cost(m,H,y)>=min(one_wait_cost(low,H,y),one_wait_cost(H,H,y))
            wait_checks+=1
print(json.dumps({'wait_departure_status':'PASS',
    'additional_exact_checks':wait_checks,
    'concave_quadratic_coefficient':str(-EL*(2*K+EL)/(8*K)),
    'endpoints_only':True},indent=2))

# Corollary: a high-surplus prefix can wait for a bounded interval and
# the entire (waiting time, all-count suffix) search reduces to two endpoints.
waited_chain_checks=0
for H in [F(1,16),F(1,24),F(1,40),F(1,64)]:
 for yr in [F(2,5),F(1,2),F(5,8),F(3,4),F(7,8)]:
  y=K*H*yr
  wcrit=(y-ETA*K*H)/(D-ETA*K)
  wmax=min(H,wcrit,y/D,(K*H-y)/EL)
  assert wmax>0 and D-ETA*K>0
  for frac in [F(1,4),F(1,2),F(3,4)]:
   w=wmax*frac
   remaining=H-w
   ynew=y-D*w
   assert 0<=ynew<=K*remaining
   assert ynew>=ETA*K*remaining
   # Two-source suffix with three productive returns.
   h1=(K*remaining+ynew)/(2*K)
   tail=remaining-h1
   h2=tail*F(2,3)
   h3=tail-h2
   assert K*h1>=ynew and K*h2>=EL*h1 and K*h3>=EL*h2
   seq=[h1,h2,h3]
   mult=direct(seq,ynew)
   sing=direct([remaining],ynew)
   assert mult-sing==E(seq,ynew)-E([remaining],ynew)
   assert mult-sing>=MU*remaining
   # The single tent's optimal wait is at w=0 or w=wmax.
   assert sing==one_wait_cost(remaining,H,y)
   assert sing>=min(one_wait_cost(H,H,y),one_wait_cost(H-wmax,H,y))
   waited_chain_checks+=1
print(json.dumps({'waited_high_surplus_status':'PASS',
 'additional_exact_checks':waited_chain_checks,
 'reduction':'all-turn suffixes and intermediate departure times removed below first rank threshold'},indent=2))

# Entire terminal short-hinge regime: merging the final two productive returns
# strictly improves cost for every initial surplus (not just high surplus).
terminal_merge_checks=0
rhomin=EL/K
rhomax=EL/D
assert rhomin<rhomax
for H in [F(1,16),F(1,24),F(1,32),F(1,64),F(1,128)]:
 for m in range(2,13):
  for f in [F(1,4),F(1,2),F(3,4)]:
   rho=rhomin+f*(rhomax-rhomin)
   a=H/(F(m-1)+rho)
   hs=[a]*(m-1)+[a*rho]
   y=K*hs[0]*f
   assert sum(hs)==H and K*hs[0]>y
   assert all(K*hs[i]>=EL*hs[i-1] for i in range(1,m))
   assert EL*hs[-2]>D*hs[-1]  # terminal hinge is active
   merged=hs[:-2]+[hs[-2]+hs[-1]]
   gap=E(merged,y)-E(hs,y)
   assert gap<0
   assert gap<=-F(15,32)*EL*hs[-2],(m,H,gap)
   assert gap==direct(merged,y)-direct(hs,y)
   terminal_merge_checks+=1
print(json.dumps({'terminal_hinge_status':'PASS',
 'merge_checks':terminal_merge_checks,
 'uniform_cost_improvement':'at least (15/32) ell h_(m-1) for H<=2 and ell/k<1/8'},indent=2))

# Algebraic fixtures for the general (0 < ell/k < 1/8, H <= 2) theorem,
# independently of the specific saved field and its small horizon.
def general_energy(k,ell,hs,y):
 d=k-ell;A=k/F(8)-ell/F(2);m=len(hs)
 Q=A*sum(h*h for h in hs)-ell/F(2)*sum(hs[j]*hs[j+1] for j in range(m-1))
 Q-=F(3)*ell*hs[-1]/F(2)+y*hs[0]/F(2)+y*y/(F(8)*k)
 Q-=max(F(0),y-d*hs[0])**2/(F(8)*k)
 for j in range(1,m-1):Q-=max(F(0),ell*hs[j-1]-d*hs[j])**2/(F(8)*k)
 if m>=2:Q-=max(F(0),ell*hs[-2]-d*hs[-1])/F(2)
 return Q

universal_merge_checks=0
for ratio in [F(1,100),F(1,20),F(1,10),F(1,9)]:
 k=F(1);e=ratio;d=k-e
 for H in [F(1,16),F(1,2),F(1),F(2)]:
  for m in range(2,8):
   rho=(e/k+e/d)/F(2)
   a=H/(F(m-1)+rho)
   hs=[a]*(m-1)+[rho*a]
   assert all(k*hs[j]>=e*hs[j-1] for j in range(1,m))
   assert e*hs[-2]-d*hs[-1]>0
   new=hs[:-2]+[hs[-2]+hs[-1]]
   for yratio in [F(1,4),F(1,2),F(3,4)]:
    y=k*hs[0]*yratio
    gain=general_energy(k,e,new,y)-general_energy(k,e,hs,y)
    assert gain<=-F(15,32)*e*hs[-2]
    universal_merge_checks+=1
print(json.dumps({'universal_terminal_hinge':'PASS',
 'arithmetic_fixture_checks':universal_merge_checks,
 'ratio_values':'1/100,1/20,1/10,1/9',
 'maximum_duration':'2'},indent=2))
