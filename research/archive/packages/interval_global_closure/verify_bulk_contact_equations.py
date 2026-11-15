#!/usr/bin/env python3
"""Exact physical tests of the bulk M2 / endpoint-route moment identities.

Princess radius is uniform initially, remains still until T in{0,1,2},
then moves outward at unit speed and sticks to1. The independent physical
oracle intersects individual Princess/Monster affine pieces and integrates
the lower envelope of their first contact times. No record formula is used
by that oracle.
"""
from fractions import Fraction as Q
from itertools import combinations
from pathlib import Path
import argparse,json


def clip(rows):
    lo,hi=Q(0),Q(1)
    for a,b in rows: # a*r<=b
        if a>0:hi=min(hi,b/a)
        elif a<0:lo=max(lo,b/a)
        elif b<0:return None
    return None if lo>hi else (lo,hi)


def physical_score(path,T):
    answer=Q(0);branch_count=0
    for sign in (-1,1):
        branches=[]
        # Target position Ar*r+Bt*t+C; temporal guard inequalities a*r+b*t<=c.
        princess=[(Q(sign),Q(0),Q(0),[(0,-1,0),(0,1,T)]),
                  (Q(sign),Q(sign),-Q(sign)*T,[(0,-1,-T),(1,1,T+1)]),
                  (Q(0),Q(0),Q(sign),[(-1,-1,-T-1)])]
        for (s,x),(t,y) in zip(path,path[1:]):
            if t==s:assert x==y;continue
            v=(y-x)/(t-s);d=x-v*s
            assert abs(v)<=1
            for ar,bt,c,guards in princess:
                if v==bt:
                    # Coincidence then occurs only for one initial radius,
                    # which has zero mass under the uniform radial law.
                    assert ar!=0
                    continue
                alpha=ar/(v-bt);beta=(c-d)/(v-bt)
                rows=[(-alpha,beta-s),(alpha,t-beta)]
                rows += [(Q(a)+Q(b)*alpha,Q(k)-Q(b)*beta) for a,b,k in guards]
                interval=clip(rows)
                if interval is not None:branches.append((*interval,alpha,beta))
        cuts={Q(0),Q(1)}
        for lo,hi,_,_ in branches:cuts|={lo,hi}
        for p,q in combinations(branches,2):
            lo,hi=max(p[0],q[0]),min(p[1],q[1])
            slope=p[2]-q[2]
            if slope:
                r=(q[3]-p[3])/slope
                if lo<r<hi:cuts.add(r)
        cuts=sorted(cuts)
        for lo,hi in zip(cuts,cuts[1:]):
            r=(lo+hi)/2
            eligible=[p for p in branches if p[0]<=r<=p[1]]
            assert eligible,("uncaptured rank interval",lo,hi,path,T,sign)
            p=min(eligible,key=lambda z:z[2]*r+z[3])
            answer+=(p[2]*(hi*hi-lo*lo)/2+p[3]*(hi-lo))/2
        branch_count+=len(branches)
    return answer,branch_count


def cdf(t,x,T):
    if x>1:return Q(1)
    if x<-1:return Q(0)
    outward=max(Q(0),t-T)
    radial=max(Q(0),abs(x)-outward)
    return Q(1,2)+(radial/2 if x>0 else -radial/2 if x<0 else 0)


def integral(T,start,end,v,d,cap=None):
    """Integrate F(t,v*t+d), optionally capped by a constant.

    Quarter-point affine recovery handles the endpoint interior-trace /
    exterior-CDF jumps without assigning them positive time mass.
    """
    if start==end:return Q(0)
    cuts={start,end}
    for slope,offset in [(Q(1),-T),(v,d),(v,d-1),(v,d+1),
                         (1+v,d-T),(1-v,-d-T)]:
        if slope:
            t=-offset/slope
            if start<t<end:cuts.add(t)
    cuts=sorted(cuts);answer=Q(0)
    for lo,hi in zip(cuts,cuts[1:]):
        p=(3*lo+hi)/4;q=(lo+3*hi)/4
        fp,fq=cdf(p,v*p+d,T),cdf(q,v*q+d,T)
        slope=(fq-fp)/(q-p);offset=fp-slope*p
        assert cdf((lo+hi)/2,v*(lo+hi)/2+d,T)==slope*(lo+hi)/2+offset
        sub={lo,hi}
        if cap is not None and slope:
            at=(cap-offset)/slope
            if lo<at<hi:sub.add(at)
        sub=sorted(sub)
        for a,b in zip(sub,sub[1:]):
            if cap is not None and slope*(a+b)/2+offset>=cap:answer+=cap*(b-a)
            else:answer+=slope*(b*b-a*a)/2+offset*(b-a)
    return answer


def m2(a,b,T):
    h=(b-a)/2;f=cdf(0,a,T);k=cdf(h,(b+a)/2,T)
    I=integral(T,0,h,1,a)
    H=integral(T,0,b+1,-1,b,f)
    return b+3-I-(b+3-h)*k+H


def endpoint(a,T):
    sigma=1-a;f=cdf(0,a,T)
    return sigma-integral(T,0,sigma,1,a)+integral(T,0,sigma+2,-1,sigma+1,f)


def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('output');args=ap.parse_args()
    counts={"physical_M2":0,"physical_endpoint":0,"quadratic_M2":0,
            "quadratic_endpoint":0,"smooth_start_derivatives":0,
            "smooth_turn_derivatives":0,"endpoint_trace_jump":0,
            "negative_start_balance_dominance":0,"endpoint_survivor_derivatives":0}
    branches=0
    for T in (Q(0),Q(1),Q(2)):
        for ai in range(-7,8):
            a=Q(ai,8)
            for bi in range(1,24):
                b=Q(bi,8);h=(b-a)/2;peak=(b+a)/2
                if h<0 or not 0<=peak<1:continue
                path=[(Q(0),a),(h,peak),(b+1,Q(-1)),(b+3,Q(1))]
                actual,n=physical_score(path,T);branches+=n
                assert actual==m2(a,b,T),("M2",a,b,T,actual,m2(a,b,T))
                counts['physical_M2']+=1
                gap=1-cdf(h,peak,T)-cdf(0,a,T)
                if a<0 and gap>0:
                    monotone,_=physical_score([(Q(0),a),(1-a,Q(1)),(3-a,Q(-1))],T)
                    assert actual-monotone>=2*gap
                    counts['negative_start_balance_dominance']+=1
                if T==2 and b<=1:
                    f=(1+a)/2
                    assert actual==2-f*f+h*(1-f)-3*h*h/4
                    counts['quadratic_M2']+=1
                    # Exact polynomial derivatives: independent central
                    # physical first-contact evaluations, not cost moments.
                    e=Q(1,1024)
                    if -b<a<b and 0<peak<1 and b<1:
                        vals=[]
                        for aa,bb in [(a+e,b),(a-e,b),(a,b+e),(a,b-e)]:
                            hh=(bb-aa)/2;pp=(bb+aa)/2
                            value,_=physical_score([(Q(0),aa),(hh,pp),(bb+1,Q(-1)),(bb+3,Q(1))],T)
                            vals.append(value)
                        assert (vals[0]-vals[1])/(2*e)==h/4-f/2-Q(1,2)
                        assert (vals[2]-vals[3])/(2*e)==(1-f)/2-3*h/4
                        counts['smooth_start_derivatives']+=1;counts['smooth_turn_derivatives']+=1
        for ai in range(-8,9):
            a=Q(ai,8);sigma=1-a
            actual,n=physical_score([(Q(0),a),(sigma,Q(1)),(sigma+2,Q(-1))],T);branches+=n
            assert actual==endpoint(a,T),("endpoint",a,T,actual,endpoint(a,T))
            counts['physical_endpoint']+=1
            if T==2:
                expected=1+sigma-sigma*sigma/4 if a>=0 else 2-sigma*sigma/4
                assert actual==expected
                counts['quadratic_endpoint']+=1
                if -1<a<1 and a:
                    e=Q(1,1024);values=[]
                    for aa in (a+e,a-e):
                        ss=1-aa
                        value,_=physical_score([(Q(0),aa),(ss,Q(1)),(ss+2,Q(-1))],T)
                        values.append(value)
                    f=(1+a)/2
                    if a>0:
                        tau=2*sigma;Le=sigma/2;Bo=sigma/2;Bi=a+sigma/2
                    else:
                        tau=sigma+2;Le=f;Bo=sigma/2;Bi=Q(0)
                    # k_S=1 and f'=1/2. Le is a real endpoint
                    # survivor mass, including its necessary cap by f.
                    rhs=tau/2-(Le+Bo+Bi)
                    assert (values[0]-values[1])/(2*e)==rhs
                    counts['endpoint_survivor_derivatives']+=1
            if -1<a<1:
                # The nominal interior-turn formula at the boundary delays
                # the endpoint atom by exactly four additional time units.
                k=cdf(sigma,Q(1),T)
                assert m2(a,2-a,T)-actual==4*(1-k)
                counts['endpoint_trace_jump']+=1
    report={"status":"PASS","scope":"Exact physical capture tests of contact-moment identities; not an equilibrium certificate.",
            "counts":counts,"physical_affine_contact_branches":branches,
            "princess_family":"uniform initial radius; stationary until T in{0,1,2}, then unit outward and endpoint-sticky"}
    Path(args.output).write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))

if __name__=='__main__':main()
