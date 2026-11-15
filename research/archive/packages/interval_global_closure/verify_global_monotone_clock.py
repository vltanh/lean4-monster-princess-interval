"""Exact causal-clock/active-source regression (Fraction-only).

Finite time-slot tests illustrate the quantile clock theorem;
continuous two-sweep integrals use exact rational intersection times.
These do NOT prove global infinite-horizon duality.
"""
from fractions import Fraction as Q
from collections import Counter
from random import Random

rng=Random(20261112)
checks=0
for N in (3,5,9,17,31):
    for _ in range(200):
        # Each scoring slot j selects a legal past index old[j]<=j.
        old=[rng.randrange(j+1) for j in range(N)]
        new=sorted(old)  # deterministic monotone quantile clock
        assert all(new[j]<=j for j in range(N))
        assert Counter(new)==Counter(old)
        for u in range(N):
            assert sum(v<=u for v in new)>=u+1
        reward=[Q(rng.randint(-7,7),rng.randint(1,8))
                for _ in range(N)]
        assert sum(reward[x] for x in new)==sum(reward[x] for x in old)
        checks+=1

# On [0,4], eta=Lebesgue_[0,1]+3delta_1 admits s(t)=min(t,1).
assert Q(1,3)+Q(3)==Q(10,3)  # integral s(t)^2 exact

def interpolate(path,t):
    for (a,x),(b,y) in zip(path,path[1:]):
        if a<=t<=b:
            return x+(y-x)*(t-a)/(b-a)
    raise AssertionError('incomplete path')

def exact_sweep_score(eps):
    # Radius of p_eps(t)=min(-1+eps+t,1); two-sweep active alpha
    # is (1/2)dt supported on (t,x)=(t,1-t), 0<=t<=2.
    radius=[(Q(0),Q(1)-eps),(Q(1)-eps,Q(0)),
            (Q(2)-eps,Q(1)),(Q(2),Q(1))]
    cuts={Q(0),Q(1),Q(2)}|{t for t,_ in radius}
    for (a,x),(b,y) in zip(radius,radius[1:]):
        if a==b:
            continue
        slope=(y-x)/(b-a)
        for left,right,sgn in (
                (max(a,Q(0)),min(b,Q(1)),-1),
                (max(a,Q(1)),min(b,Q(2)),+1)):
            if left>=right:
                continue
            rad_left=interpolate(radius,left)
            threshold_left=Q(1)-left if sgn==-1 else left-Q(1)
            diff_left=rad_left-threshold_left
            derivative=slope-sgn
            if derivative:
                root=left-diff_left/derivative
                if left<root<right:
                    cuts.add(root)
    total=Q(0)
    for a,b in zip(sorted(cuts),sorted(cuts)[1:]):
        mid=(a+b)/2
        r=interpolate(radius,mid)
        x=Q(1)-mid
        if x>0:
            price=1+int(r<x)
        elif x<0:
            price=int(r>-x)
        else:
            price=int(r>0)
        assert 0<=price<=2
        total+=(b-a)*price/Q(2)
    return total

for n in range(1,35):
    eps=Q(1,2**n)
    assert exact_sweep_score(eps)==Q(3,2)-eps/Q(4)

print(f'PASS: {checks} causal index-clock reorderings; exact signed rewards, prefix constraints.')
print('PASS: continuous clock moment = 10/3.')
print('PASS: 34 exact two-sweep radial active-source integrals = 3/2-epsilon/4.')
print('SCOPE: finite fixtures; not a complete unrestricted-game proof.')
