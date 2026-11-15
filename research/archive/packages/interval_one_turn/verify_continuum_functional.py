#!/usr/bin/env python3
"""Exact physical integration fixtures for the continuum P_b functional."""
from fractions import Fraction as Q
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from verify_domain import Path as PhysicalPath, monster, direct_first_hit
from verify_finite_princess import general_attacks


def complete(nodes):
    nodes=[(Q(t),Q(x)) for t,x in nodes]
    assert nodes[-1][0]==2
    s=nodes[-1][1]
    nodes.extend(((3-s,Q(1)),(Q(6),Q(1))))
    return PhysicalPath.make(nodes)


def physical_integral(path,b,interval=None):
    lo,hi=interval or (-min(b,Q(1)),min(b,2-b,Q(1)))
    lines,_=general_attacks([path])
    breaks={lo,hi}
    for A,B,C in lines:
        if A:
            a=(Q(C)-B*b)/A
            if lo<a<hi:breaks.add(a)
    total=Q(0)
    breaks=sorted(breaks)
    for x,y in zip(breaks,breaks[1:]):
        a=(x+y)/2
        route=monster(a,(b-a)/2)
        total+=(y-x)*(direct_first_hit(route,path)+direct_first_hit(route,path.reflected()))/2
    return total/(hi-lo)


def functional(path,b,interval=None):
    lo,hi=interval or (-min(b,Q(1)),min(b,2-b,Q(1)))
    def cdf(z):return max(Q(0),min(Q(1),(z-lo)/(hi-lo)))
    r=path.nodes[0][1]
    breaks={Q(0),Q(2)}
    tau=None
    for (s,x),(t,y) in zip(path.nodes,path.nodes[1:]):
        if s>=2:break
        t=min(t,Q(2));y=path.at(t)
        breaks.update((s,t))
        for sign in (-1,1):
            A=s+sign*x;B=t+sign*y
            assert A<B
            for level in (b,-lo,-hi):
                if A<level<B:breaks.add(s+(t-s)*(level-A)/(B-A))
            if sign==1 and A<=b<=B and tau is None:
                tau=s+(t-s)*(b-A)/(B-A)
    total=Q(0)
    breaks=sorted(breaks)
    for s,t in zip(breaks,breaks[1:]):
        mid=(s+t)/2;p=path.at(mid);U=mid+p;W=mid-p
        G=(2-cdf(r)-cdf(-r)+cdf(-U)+cdf(-W) if U<b
           else 1-cdf(-r) if W<b else Q(0))
        total+=(t-s)*G
    if r>=b:total+=b+3
    else:
        assert tau is not None
        total+=(b+3-tau)*cdf(-(tau-path.at(tau)))
    if b>1 and 2-path.at(2)<b:total+=(b-1)*(1-cdf(-r))
    return total/2


def main():
    paths=[complete([(0,r),(2,r)]) for r in map(Q,('1/4','1/2','3/4','7/8','15/16'))]
    paths.extend((complete([(0,'1/4'),(1,'1/2'),(2,'1/4')]),
                  complete([(0,'7/8'),(1,'1/2'),(2,'3/4')]),
                  complete([(0,'3/4'),(1,'7/8'),(2,'1/2')]),
                  complete([(0,'1/8'),(1,'7/8'),(2,'1/8')]),
                  complete([(0,'7/8'),(1,'1/8'),(2,'7/8')]),
                  complete([(0,'3/5'),('1/2','1/5'),(1,'3/5'),('3/2','2/5'),(2,'4/5')])))
    count=above=equal=late=0
    subinterval_checks=0
    for b in map(Q,('1/2','3/4','15/16','31/32','1','17/16','3/2')):
        for path in paths:
            actual=physical_integral(path,b);formula=functional(path,b)
            assert actual==formula,(b,path.nodes,actual,formula)
            count+=1;above+=path.nodes[0][1]>b;equal+=path.nodes[0][1]==b
            late+=(2-path.at(2)<b)
            lo,hi=-min(b,Q(1)),min(b,2-b,Q(1))
            for j in range(4):
                interval=(lo+(hi-lo)*Q(j,4),lo+(hi-lo)*Q(j+1,4))
                actual=physical_integral(path,b,interval);formula=functional(path,b,interval)
                assert actual==formula,(b,interval,path.nodes,actual,formula)
                subinterval_checks+=1
    print({'exact_physical_functional_checks':count,'initially_past_U_boundary':above,
           'initially_on_U_boundary':equal,'late_W_terminal_cases':late,
           'additional_density_subinterval_checks':subinterval_checks})

if __name__=='__main__':main()
