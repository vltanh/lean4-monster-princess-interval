#!/usr/bin/env python3
"""Exact self-contained n=1 interpolation-loss witness; standard library only."""
from collections import defaultdict
from fractions import Fraction as Q
import json

def gnum(j, k):
    assert 0 <= j <= 16 and 0 <= k <= 2 and (j-k) % 2 == 0
    if k == 2 and j in (0, 2, 4):
        return 8
    if k == 1 and j == 1:
        return 7
    return 0

def price(j, k):
    return 8 + (1 if k > 0 else -1 if k < 0 else 0) * gnum(j, abs(k))

def check_profile():
    nodes = [(j, k) for j in range(17) for k in range(3) if (j-k) % 2 == 0]
    cones = 0
    for j, k in nodes:
        assert 0 <= gnum(j, k) <= 8
        if k == 0:
            assert gnum(j, k) == 0
        if j >= 4:
            foot = k - j + 4
            assert gnum(j, k) == (0 if foot <= 0 else gnum(4, foot))
        for s, r in nodes:
            if r >= k + abs(s-j):
                assert gnum(j, k) <= gnum(s, r)
                cones += 1
    for j in range(0, 16, 2):
        assert gnum(j+2, 2) <= gnum(j, 2)
    return len(nodes), cones

def check_primal():
    plans = [
        (7, 2, [-1]*4, {0:1,1:1,2:1,3:1}, {}),
        (1, 0, [1,-1,-1,-1,1,1,1,1], {0:3,3:1}, {0:1,1:7}),
    ]
    pressure = defaultdict(int)
    mass = 0
    prefixes = 0
    for weight, start, moves, minus, plus in plans:
        pos = [start]
        for move in moves:
            assert move in (-1, 1)
            pos.append(pos[-1] + move)
            assert -2 <= pos[-1] <= 2
        assert pos.index(0) <= 4
        for endpoint, calendar, sign in [(-2, minus, 1), (2, plus, -1)]:
            K = pos.index(endpoint)
            assert sum(calendar.values()) == K
            assert all(0 <= j < K and a >= 0 for j, a in calendar.items())
            for j in range(K):
                assert sum(a for i, a in calendar.items() if i <= j) >= j+1
                prefixes += 1
            for j, a in calendar.items():
                pressure[j, sign*pos[j]] += weight*a
                mass += weight*a
    assert pressure[1, 1] >= 7 and pressure[1, -1] >= 7
    assert 1 >= 1 + abs(1-1)
    positive = sum(a for (j,k),a in pressure.items() if k > 0)
    assert mass == 40 and positive == 14
    upper = Q(mass+positive-7, 32)
    assert upper == Q(47,32)
    return upper, prefixes

def exact_full_bank_dual():
    # Each record is in units of 1/8. A row step costs record/4,
    # hence the final integer path cost is divided by 32.
    layer = {}
    for k in (-2, 0, 2):
        layer[k,k==-2,k==2,k==0,None,None] = 0
    best = None
    states = transitions = 0
    for j in range(17):
        states += len(layer)
        nxt = {}
        for (k,em,ep,center,rm,rp),cost in layer.items():
            if em and ep:
                best = cost if best is None else min(best,cost)
                continue
            if j == 16 or (not center and j >= 4):
                continue
            if not em:
                p = price(j,k)
                rm = p if rm is None else min(rm,p)
            if not ep:
                p = price(j,-k)
                rp = p if rp is None else min(rp,p)
            nc = cost + (0 if em else rm) + (0 if ep else rp)
            for move in (-1,1):
                kk = k+move
                if abs(kk)>2:
                    continue
                cc = center or kk==0
                if not cc and j+1 >= 4:
                    continue
                mm,pp = em or kk==-2, ep or kk==2
                key = kk,mm,pp,cc,None if mm else rm,None if pp else rp
                if key not in nxt or nc<nxt[key]:
                    nxt[key]=nc
                transitions += 1
        layer=nxt
    assert best == 47
    return Q(best,32), states, transitions

def threshold_map(x, z):
    k = x.numerator // x.denominator
    a = x-k
    if a == 0:
        return k
    plus = k % 2 == 0
    theta = z if plus else 1-z
    up = a > theta if plus else a >= theta
    return k + int(up)

def nodal_trace(U,W):
    j,k = U+W,U-W
    return Q(8+(1 if k>0 else -1 if k<0 else 0)*gnum(j,abs(k)),16)

def trace(t,x,eps):
    lo,hi = Q(1,2)-eps,Q(1,2)+eps
    cuts = [lo,hi]
    for v in (t+x,t-x):
        k=v.numerator//v.denominator
        a=v-k
        if a:
            z=a if k%2==0 else 1-a
            if lo<z<hi:
                cuts.append(z)
    cuts=sorted(set(cuts))
    total=Q(0)
    for a,b in zip(cuts,cuts[1:]):
        z=(a+b)/2
        total += (b-a)*nodal_trace(threshold_map(t+x,z),threshold_map(t-x,z))
    return total/(hi-lo)

def descent_integral(start,eps):
    # U=start is fixed, W=2t-start. For the two tested starts,
    # T(U)=1 almost surely, so only threshold-band endpoints matter.
    lo,hi=Q(1,2)-eps,Q(1,2)+eps
    end=start+1
    cuts={Q(0),end}
    for k in range(-2,5):
        for f in (Q(0),lo,hi,Q(1)):
            t=(Q(k)+f+start)/2
            if 0<t<end:
                cuts.add(t)
    cuts=sorted(cuts)
    total=Q(0)
    assert trace(Q(0),start,eps)==1
    last=Q(1)
    checks=0
    for a,b in zip(cuts,cuts[1:]):
        fa=trace(a,start-a,eps)
        fb=trace(b,start-b,eps)
        mid=(a+b)/2
        fm=trace(mid,start-mid,eps)
        assert fm==(fa+fb)/2
        assert last>=fa>=fb
        total+=(b-a)*(fa+fb)/2
        last=fb
        checks+=1
    assert last==0
    return total,checks

def replay():
    nodes,cones=check_profile()
    upper,prefixes=check_primal()
    dual,states,transitions=exact_full_bank_dual()
    assert upper==dual
    widths=sorted({Q(a,b) for b in range(2,25) for a in range(1,b) if Q(a,b)<=Q(1,2)})
    pieces=field_checks=0
    for eps in widths:
        a=Q(1,2)+eps
        attack,c=descent_integral(a,eps)
        fast,d=descent_integral(Q(1),eps)
        assert attack==Q(31,32)+eps/2
        assert fast==Q(39,32)
        assert upper-attack==Q(1,2)-eps/2
        pieces+=c+d
        for t in (Q(0),Q(1,4),Q(1),Q(7,4),Q(2),Q(9,4),Q(5,2),Q(3)):
            for r in (Q(0),Q(1,4),Q(1,2),Q(3,4),Q(1)):
                f=trace(t,r,eps)
                assert Q(1,2)<=f<=1
                assert trace(t,-r,eps)==1-f
                if t<=2:
                    assert trace(t,Q(1),eps)==1
                else:
                    foot=r-t+2
                    expect=Q(1,2) if foot<=0 else trace(Q(2),foot,eps)
                    assert f==expect
                field_checks+=1
    return {
        "status":"PASS",
        "scope":"Self-contained n=1 optimal Qout profile, physical primal, exhaustive atomic bank dual, legal common-threshold field and exact attacking-path integrals. The attack is not claimed to be the field's globally optimal response.",
        "finite_value":str(upper),
        "profile_nodes":nodes,"profile_cone_checks":cones,
        "physical_clock_prefixes":prefixes,
        "full_bank_record_states":states,"full_bank_transitions":transitions,
        "rational_widths_checked":len(widths),
        "exact_affine_integration_pieces":pieces,
        "field_identity_checks":field_checks,
        "attack":"start a=1/2+epsilon, sweep to -1 at 1+a, optionally to +1 at 3+a",
        "exact_attack_payoff":"31/32 + epsilon/2",
        "exact_loss_from_finite_value":"1/2 - epsilon/2",
        "limiting_loss":"1/2",
        "full_width_fast_sweep_payoff":"39/32"
    }

if __name__=="__main__":
    print(json.dumps(replay(),indent=2))

