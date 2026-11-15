#!/usr/bin/env python3
"""Self-contained exact full-width h/4 transfer counterexample.

The profile is a feasible Qout dual, not asserted to be globally optimal for
its finite grid. Uses only standard-library Fraction and exhaustive record DP.
"""
from fractions import Fraction as Q
import json

N = 2
D = 49
R = 2*N
C = 4*N
H = 16*N
PRE = {
    (0,2):14, (0,4):D,
    (1,1):12, (1,3):D,
    (2,2):D, (2,4):D,
    (3,1):48, (3,3):D,
    (4,2):48, (4,4):D,
    (5,1):0, (5,3):48,
    (6,2):0, (6,4):D,
    (7,1):0, (7,3):D,
    (8,2):0, (8,4):D,
}
PATH = [(Q(0),Q(1,4)), (Q(5,8),Q(-3,8)), (Q(2),Q(1)), (Q(4),Q(-1))]


def gnum(j,k):
    assert 0 <= j <= H and 0 <= k <= R and (j+k)%2 == 0
    if k == 0:
        return 0
    if j > C:
        k -= j-C
        j = C
    return 0 if k <= 0 else PRE[j,k]


def price(j,k):
    return D + (1 if k > 0 else -1 if k < 0 else 0)*gnum(j,abs(k))


def check_profile():
    nodes = [(j,k) for j in range(H+1) for k in range(R+1) if (j+k)%2 == 0]
    cones=0
    for j,k in nodes:
        v = gnum(j,k)
        assert 0 <= v <= D
        for t,r in nodes:
            if r >= k+abs(t-j):
                assert v <= gnum(t,r)
                cones+=1
        if j>=C:
            foot=k-j+C
            assert v == (gnum(C,foot) if foot>0 else 0)
    for j in range(0,H,2):
        assert gnum(j+2,R) <= gnum(j,R)
    return len(nodes),cones


def exact_bank():
    layer = {(k,k==-R,k==R,k==0,None,None):0 for k in range(-R,R+1,2)}
    best=None
    states=transitions=0
    for j in range(H+1):
        states+=len(layer)
        nxt={}
        for (k,em,ep,center,l,r),cost in layer.items():
            if em and ep:
                best=cost if best is None else min(best,cost)
                continue
            if j==H or (not center and j>=C):
                continue
            if not em:
                p=price(j,k)
                l=p if l is None else min(l,p)
            if not ep:
                p=price(j,-k)
                r=p if r is None else min(r,p)
            cost2=cost+(0 if em else l)+(0 if ep else r)
            for step in (-1,1):
                x=k+step
                if abs(x)>R:
                    continue
                cc=center or x==0
                if not cc and j+1>=C:
                    continue
                mm,pp=em or x==-R,ep or x==R
                key=x,mm,pp,cc,None if mm else l,None if pp else r
                if key not in nxt or cost2<nxt[key]:
                    nxt[key]=cost2
                transitions+=1
        layer=nxt
    assert best is not None
    return Q(best,4*N*D),states,transitions,best


def rounding(z,threshold):
    y=N*z
    k=y.numerator//y.denominator
    alpha=y-k
    if not alpha:
        return k
    plus=k%(2*N)<N
    theta=threshold if plus else 1-threshold
    return k+int(alpha>theta if plus else alpha>=theta)


def trace(t,x):
    cuts={Q(0),Q(1)}
    for z in (t+x,t-x):
        y=N*z;k=y.numerator//y.denominator;alpha=y-k
        if alpha:
            cuts.add(alpha if k%(2*N)<N else 1-alpha)
    cuts=sorted(cuts)
    out=Q(0)
    for a,b in zip(cuts,cuts[1:]):
        z=(a+b)/2
        u,w=rounding(t+x,z),rounding(t-x,z)
        j,k=u+w,u-w
        out+=(b-a)*Q(price(j,k),2*D)
    return out


def integrate_record(record,a,b,dt):
    # record <= a. A new record occurs only on a decreasing affine piece.
    record=min(record,a)
    if b>=record:
        return dt*record,record,None
    z=(a-record)/(a-b)
    assert 0<=z<=1
    integral=dt*(record*z+(1-z)*(record+b)/2)
    return integral,b,z


def path_cost(path):
    assert path[0][0]==0
    l=trace(*path[0]);r=1-l
    if path[0][1]==-1:l=Q(0)
    if path[0][1]==1:r=Q(0)
    cost=Q(0);pieces=0;records=[]
    for (ta,xa),(tb,xb) in zip(path,path[1:]):
        assert tb-ta==abs(xb-xa) and -1<=xa<=1 and -1<=xb<=1
        plus=xb>xa;const=ta-xa if plus else ta+xa
        free0,free1=2*ta-const,2*tb-const
        fract=N*const-(N*const).numerator//(N*const).denominator
        cuts={ta,tb}
        for k in range((N*free0).numerator//(N*free0).denominator-1,
                       (N*free1).numerator//(N*free1).denominator+2):
            for f in (Q(0),fract,1-fract,Q(1)):
                t=(Q(k)+f)/N/2+const/2
                if ta<t<tb:cuts.add(t)
        cuts=sorted(cuts)
        def pos(t):return xa+(t-ta)*(1 if plus else -1)
        for a,b in zip(cuts,cuts[1:]):
            va,vb=trace(a,pos(a)),trace(b,pos(b))
            assert trace((a+b)/2,pos((a+b)/2))==(va+vb)/2
            cl,l,zl=integrate_record(l,va,vb,b-a)
            cr,r,zr=integrate_record(r,1-va,1-vb,b-a)
            cost+=cl+cr;pieces+=1
            records.append({'from':str(a),'to':str(b),'F_from':str(va),'F_to':str(vb),
                            'piece_cost':str(cl+cr),'left_record':str(l),'right_record':str(r)})
        if xb==-1:l=Q(0)
        if xb==1:r=Q(0)
    assert l==r==0
    return cost,pieces,records


def main():
    nodes,cones=check_profile()
    c,states,transitions,units=exact_bank()
    value,pieces,records=path_cost(PATH)
    # Qout common-threshold interpolation is legal; also check identities on
    # an independent rational sample including all special geometric seams.
    field_checks=0
    for it in range(25):
        t=Q(it,8)
        for ix in range(9):
            r=Q(ix,8)
            f=trace(t,r)
            assert Q(1,2)<=f<=1 and trace(t,-r)==1-f
            if t>2:
                foot=r-t+2
                assert f==(Q(1,2) if foot<=0 else trace(Q(2),foot))
            field_checks+=1
    gap=c-value
    assert c==Q(429,392)
    assert value==Q(3039,3136)
    assert gap==Q(393,3136)
    first_values=[trace(Q(j,8),Q(1,4)-Q(j,8)) for j in range(6)]
    assert first_values==[Q(4,7),Q(55,98),Q(1,2),Q(43,98),Q(19,98),Q(1,196)]
    assert sum((a+b)/16 for a,b in zip(first_values,first_values[1:]))==Q(111,448)
    assert gap>Q(1,4*N)
    print(json.dumps({
        'status':'PASS',
        'scope':'Feasible exact n=2 Qout profile, exhaustive full-grid dual lower, legal full-width interpolated Princess field, and a strict counterexample to security >= c - 1/(4n). No finite-grid optimality or global response optimality is claimed.',
        'n':N,'field_denominator':D,'pre_two_radial_nodes':[[j,k,v] for (j,k),v in PRE.items()],
        'profile_nodes':nodes,'cone_checks':cones,'full_bank_record_states':states,'full_bank_transitions':transitions,
        'exact_grid_dual':str(c),'grid_integer_units':units,'objective_denominator':4*N*D,
        'path':[[str(t),str(x)] for t,x in PATH],'exact_attack_payoff':str(value),
        'exact_transfer_loss':str(gap),'proposed_error':str(Q(1,4*N)),
        'strict_excess':str(gap-Q(1,4*N)),
        'affine_record_integration_pieces':pieces,'field_identity_checks':field_checks,
        'piece_integrals':records,
    },indent=2))


if __name__=='__main__':
    main()
