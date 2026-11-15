from fractions import Fraction as F
from decimal import Decimal, getcontext
import json


def mat_vec(theta, x):
    m=len(x); out=[]
    for i in range(m):
        v=(1+theta*theta)*x[i]
        if i: v-=theta*x[i-1]
        if i+1<m: v-=theta*x[i+1]
        out.append(v)
    return out


def green_columns(theta,m):
    den=1-theta**(2*m+2)
    left=[]; right=[]
    for j in range(1,m+1):
        left.append(theta**(j-1)*(1-theta**(2*(m+1-j)))/den)
        right.append(theta**(m-j)*(1-theta**(2*j))/den)
    return left,right


def endpoint_uv(theta,m):
    den=1-theta**(2*m+2)
    u=(1-theta**(2*m))/den
    v=theta**(m-1)*(1-theta**2)/den
    return u,v


def cP(theta,m):
    c=(1-theta**m)/((1-theta)*(1+theta**(m+1)))
    P=(F(m)-2*theta*c)/(1-theta)**2
    return c,P


def fixed_duration_solution(theta,m,alpha,gamma,H):
    L,R=green_columns(theta,m)
    c,P=cP(theta,m)
    zeta=((alpha+gamma)*c-H)/P
    # K^-1 1 is the sum of all Green columns. Build it independently.
    ones=[]
    for j in range(m):
        e=[F(0)]*m; e[j]=F(1)
        # solve through the closed-form full Green kernel by symmetry/columns
        col=[]
        den=1-theta**(2*m+2)
        for i in range(1,m+1):
            a=min(i,j+1); b=max(i,j+1)
            col.append(theta**(b-a)*(1-theta**(2*a))*(1-theta**(2*(m+1-b))) / ((1-theta**2)*den))
        ones.append(col)
    w=[sum(ones[j][i] for j in range(m)) for i in range(m)]
    h=[alpha*L[i]+gamma*R[i]-zeta*w[i] for i in range(m)]
    return h,zeta,w


def full_direct_energy(theta,y,hs):
    # Exact physical renewal recurrence in an affine cell, k=1. Terminal row
    # is the closed endpoint row beta_b=b below z(b), b+1 above it.
    k=F(1); ell=theta/(2*(1+theta)**2); d=k-ell
    z=lambda t:d*t
    def T(t,q): return t*q+max(F(0),q-z(t))**2/(4*k)
    t=F(0); n=y; cost=F(0)
    for j,h in enumerate(hs):
        e=t+h
        N=max(n,z(t)+k*h)
        if N==n: return None
        left=T(t,N)-T(t,n)
        if j==len(hs)-1:
            right=(e*N+max(F(0),N-z(e)))-(e*n+max(F(0),n-z(e)))
        else:
            right=T(e,N)-T(e,n)
        cost+=(left+right)/2
        t=e; n=N
    cost+=(t+2)*(1-n)
    baseline=d*t*t/2+(t+2)*(1-z(t))
    return cost-baseline


def full_formula(theta,y,hs):
    k=F(1); ell=theta/(2*(1+theta)**2); d=k-ell
    A=k/F(8)-ell/F(2); m=len(hs)
    Q=A*sum(h*h for h in hs)-ell*sum(hs[j]*hs[j+1] for j in range(m-1))/2-3*ell*hs[-1]/2
    E=Q-y*hs[0]/2-y*y/(8*k)
    E-=max(F(0),y-d*hs[0])**2/(8*k)
    for j in range(1,m-1):
        E-=max(F(0),ell*hs[j-1]-d*hs[j])**2/(8*k)
    if m>=2:
        E-=max(F(0),ell*hs[-2]-d*hs[-1])/2
    return E


def normalized_value(theta,m,q):
    # Fixed duration H*=gamma/(1-theta), divided by C0*gamma^2; constants
    # independent of m are omitted. q=alpha/gamma=y/(3 ell).
    c,P=cP(theta,m); u,v=endpoint_uv(theta,m); s=1/(1-theta)
    return -u*(1+q*q)-2*v*q+(((1+q)*c-s)**2)/P


checks=0
# Exact Green and fixed-duration KKT identities.
for theta in [F(1,100),F(1,20),F(1,10),F(1,4),F(1,2),F(2,3)]:
    ell=theta/(2*(1+theta)**2); gamma=3*theta
    for m in range(1,9):
        L,R=green_columns(theta,m)
        assert mat_vec(theta,L)==[F(1)]+[F(0)]*(m-1)
        assert mat_vec(theta,R)==[F(0)]*(m-1)+[F(1)]
        checks+=2*m
        u,v=endpoint_uv(theta,m)
        assert L[0]==u and R[-1]==u and L[-1]==v and R[0]==v
        checks+=4
        c,P=cP(theta,m)
        assert sum(L)==c and sum(R)==c
        checks+=2
        for q in [F(1,1000000),F(1,10000),F(1,100)]:
            alpha=q*gamma; H=gamma/(1-theta)
            h,zeta,w=fixed_duration_solution(theta,m,alpha,gamma,H)
            rhs=[F(0)]*m; rhs[0]+=alpha; rhs[-1]+=gamma
            rhs=[rhs[i]-zeta for i in range(m)]
            assert mat_vec(theta,h)==rhs
            assert sum(h)==H
            checks+=m+1
            if all(x>0 for x in h):
                # Verify the closed fixed-m objective formula exactly.
                lhs=sum(h[i]*mat_vec(theta,h)[i] for i in range(m))-2*alpha*h[0]-2*gamma*h[-1]
                target=gamma*gamma*normalized_value(theta,m,q)
                assert lhs==target
                checks+=1

# Full hinge energy: direct renewal scorer versus closed piecewise formula.
for theta in [F(1,20),F(1,10),F(1,4)]:
    for y in [F(1,1000),F(1,100)]:
        vals=[F(1,80),F(1,40),F(1,20),F(1,10),F(1,5)]
        samples=[
            [vals[2]], [vals[3]],
            [vals[1],vals[3]], [vals[3],vals[0]], [vals[3],vals[1],vals[4]],
            [vals[4],vals[0],vals[3]], [vals[2],vals[0],vals[0],vals[4]],
        ]
        for hs in samples:
            direct=full_direct_energy(theta,y,hs)
            if direct is None: continue
            assert direct==full_formula(theta,y,hs)
            checks+=1

# Active incoming-hinge curvature is strictly negative.
for theta in [F(1,100),F(1,20),F(1,4),F(2,3)]:
    k=F(1); ell=theta/(2*(1+theta)**2); d=k-ell
    A=k/F(8)-ell/F(2)
    coeff=A-d*d/(8*k)
    assert coeff == -ell*(2*k+ell)/(8*k)
    assert coeff<0
    checks+=2

# Saved terminal cell: high-precision adjacent-count transition roots at H*.
getcontext().prec=100
kD=Decimal(655898601421)/Decimal(62500000000)
ellD=Decimal(820954217)/Decimal(12500000000)
rD=ellD/kD
wD=(Decimal(1)-Decimal(8)*rD).sqrt()
tD=(Decimal(1)-wD)/(Decimal(1)+wD)
gD=Decimal(3)*tD
Hstar=gD/(Decimal(1)-tD)
sD=Decimal(1)/(Decimal(1)-tD)

def decimal_coeffs(m):
    def abc(mm):
        c=(Decimal(1)-tD**mm)/((Decimal(1)-tD)*(Decimal(1)+tD**(mm+1)))
        P=(Decimal(mm)-Decimal(2)*tD*c)/(Decimal(1)-tD)**2
        u=(Decimal(1)-tD**(2*mm))/(Decimal(1)-tD**(2*mm+2))
        v=tD**(mm-1)*(Decimal(1)-tD**2)/(Decimal(1)-tD**(2*mm+2))
        return (-u+c*c/P,
                -Decimal(2)*v+Decimal(2)*c*(c-sD)/P,
                -u+(c-sD)*(c-sD)/P)
    a,b,c=abc(m); A,B,C=abc(m+1)
    return A-a,B-b,C-c

transitions=[]
for m in range(1,9):
    A,B,C=decimal_coeffs(m)
    disc=(B*B-Decimal(4)*A*C).sqrt()
    roots=[(-B-disc)/(Decimal(2)*A),(-B+disc)/(Decimal(2)*A)]
    roots=sorted(x for x in roots if x>0)
    q=roots[0]; y=Decimal(3)*ellD*q
    transitions.append({
        "m":m,"small_q_root":str(q),"y_root":str(y),
        "q_over_theta_m1":str(q/(tD**(m+1))),
        "positive_roots":[str(x) for x in roots],
    })

# Exact turn-count masses from the certified 280-pair law (integer data).
turn_mass={0:F(6522690337,10**10),1:F(1635690466,10**10),2:F(1800647156,10**10),3:F(35750697,10**10),4:F(45196,10**10),5:F(5027102,10**10),7:F(149046,10**10)}
assert sum(turn_mass.values(),F(0))==1
checks+=1
report={
  "scope":"Exact Green/KKT identities for the fixed-duration two-source affine-center chain, exact full hinge-energy identities from the renewal recurrence, active-hinge curvature checks, and certified 280-pair turn-mass arithmetic. Saved-cell transition roots are high-precision evaluations of the explicit quadratic adjacent-count equations.",
  "checks":checks,
  "fixed_duration_formula":"Psi_m(q)=-u_m(1+q^2)-2v_m q+(((1+q)c_m-1/(1-theta))^2)/P_m at H*=3theta/(1-theta)",
  "active_hinge_curvature":"A-d^2/(8k)=-ell(2k+ell)/(8k)<0",
  "saved_terminal_cell":{
    "k":str(kD),"ell":str(ellD),"r":str(rD),"theta":str(tD),"H_star":str(Hstar),
    "adjacent_count_transitions":transitions,
    "asymptotic":"small q_m ~ ((1+theta)/2) theta^(m+1); y_m=3 ell q_m"
  },
  "certified_280_pair_turn_mass":{str(j):str(v) for j,v in turn_mass.items()},
  "tail_mass":{
    ">=3":str(sum(v for j,v in turn_mass.items() if j>=3)),
    ">=5":str(sum(v for j,v in turn_mass.items() if j>=5)),
    ">=7":str(sum(v for j,v in turn_mass.items() if j>=7)),
  }
}
print(json.dumps(report,indent=2))
