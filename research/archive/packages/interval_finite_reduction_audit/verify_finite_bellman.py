#!/usr/bin/env python3
"""Exact prototype of the finite local Bellman verification reduction.

Checks arbitrary-speed local derivative identities and critical controls,
then a complete polynomial certificate for a specified endpoint-supported
law. This does NOT solve the unrestricted Princess-Monster game.
"""
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
import argparse,json,random
from exact_quadratic import Quadratic,box,vertices,minimum,dot,self_test


def equality(A,b,row,rhs):
    return A+[row,[-v for v in row]],b+[rhs,-rhs]


def residual(q,state,ft,fx,velocity,lower_active,upper_active):
    g=q.gradient(state)
    df=ft+velocity*fx
    ld=min(df,Q(0)) if lower_active else Q(0)
    hd=max(df,Q(0)) if upper_active else Q(0)
    return g[0]+velocity*g[1]+g[2]*ld+g[3]*hd+state[2]+1-state[3]


def local_tests():
    rng=random.Random(20261111); counts=dict(derivative_identities=0,critical_speed_comparisons=0)
    for case in range(40):
        fx=Q(rng.randrange(1,9),8);ft=fx*Q(rng.randrange(-3,4),4)
        matrix=[[Q(0)]*4 for _ in range(4)]
        for i in range(4):
            for j in range(i,4):matrix[i][j]=matrix[j][i]=Q(rng.randrange(-3,4),5)
        q=Quadratic.make(0,[Q(rng.randrange(-4,5),3) for _ in range(4)],matrix)
        speeds=[Q(-1),-ft/fx,Q(1)]
        for low,high in product((False,True),repeat=2):
            state=[Q(0),Q(0),Q(1,2) if low else Q(1,4),Q(1,2) if high else Q(3,4)]
            crit=min(residual(q,state,ft,fx,v,low,high) for v in speeds)
            for v in sorted(set(speeds+[Q(j,16) for j in range(-16,17)])):
                res=residual(q,state,ft,fx,v,low,high)
                assert res>=crit;counts['critical_speed_comparisons']+=1
                df=ft+v*fx
                def difference(dt):
                    f=Q(1,2)+df*dt
                    new=[dt,v*dt,min(state[2],f),max(state[3],f)]
                    S0=state[2]+1-state[3];S1=new[2]+1-new[3]
                    return q.value(new)-q.value(state)+(S0+S1)*dt/2
                step=Q(1,1000)
                derivative=(4*difference(step/2)-difference(step))/step
                assert derivative==res;counts['derivative_identities']+=1
    q=Quadratic.make(0,[-Q(11,10),0,-1,1])
    state=[Q(0),Q(0),Q(1,2),Q(1,2)]
    assert residual(q,state,0,1,-1,True,True)==Q(9,10)
    assert residual(q,state,0,1,1,True,True)==Q(9,10)
    assert residual(q,state,0,1,0,True,True)==-Q(1,10)
    counts['tracking_control_false_positive_detected']=1
    return counts


def endpoint_certificate(mass):
    """Full certificate for mass at -1 and 1-mass at +1, t in [0,2]."""
    m=Q(mass); n=4
    H=[[Q(0)]*n for _ in range(n)]
    H[1][2]=H[2][1]=Q(1,2);H[1][3]=H[3][1]=Q(1,2)
    W=Quadratic.make(1,[0,-1,1,-1],H)
    A,b=box([(0,2),(-1,1),(0,m),(m,1)])
    counts=dict(local_vertex_checks=0,endpoint_tangency_checks=0,quadratic_obligations=0)
    for low,high in product((False,True),repeat=2):
        AA,bb=A[:],b[:]
        if low: AA,bb=equality(AA,bb,[0,0,1,0],m)
        if high: AA,bb=equality(AA,bb,[0,0,0,1],m)
        for z in vertices(AA,bb,4):
            for v in [-1,0,1]:
                assert residual(W,z,0,0,v,low,high)>=0
                counts['local_vertex_checks']+=1
    for x in [-1,1]:
        AA,bb=equality(A,b,[0,1,0,0],x)
        AA,bb=equality(AA,bb,[0,0,1,0] if x==-1 else [0,0,0,1],0 if x==-1 else 1)
        for z in vertices(AA,bb,4):
            assert residual(W,z,0,0,0,False,False)>=0
            counts['endpoint_tangency_checks']+=1
    for x in [-1,1]:
        p=[Q(0),Q(x),Q(0),Q(0)]
        cols=[[Q(1),0,0,0],[0,0,Q(1),0],[0,0,0,Q(1)]]
        pre=W.pullback(p,cols)
        postp=p[:];postcols=[c[:] for c in cols]
        if x==-1:postcols[1]=[Q(0)]*4
        else:postp[3]=Q(1);postcols[2]=[Q(0)]*4
        diff=W.pullback(postp,postcols).subtract(pre)
        assert diff.constant==0 and not any(diff.linear) and not any(v for row in diff.matrix for v in row)
        counts['quadratic_obligations']+=1
    Hl=[[Q(0)]*4 for _ in range(4)];Hr=[[Q(0)]*4 for _ in range(4)]
    Hl[1][2]=Hl[2][1]=Q(1,2);Hl[1][3]=Hl[3][1]=-Q(1,2)
    Hr[1][2]=Hr[2][1]=-Q(1,2);Hr[1][3]=Hr[3][1]=Q(1,2)
    El=Quadratic.make(3,[0,1,1,-3],Hl)
    Er=Quadratic.make(1,[0,-1,3,-1],Hr)
    AA,bb=equality(A,b,[1,0,0,0],2)
    terminals=[]
    for E in (El,Er):
        ans=minimum(E.subtract(W),AA,bb);assert ans is not None and ans[0]>=0
        counts['quadratic_obligations']+=1;terminals.append(str(ans[0]))
    initial=W.pullback([0,0,m,m],[[0,1,0,0]])
    ia,ib=box([(-1,1)]);ans=minimum(initial,ia,ib)
    target=2*min(m,1-m)
    assert ans[0]==target;counts['quadratic_obligations']+=1
    assert W.value([0,-1,0,m])==2*(1-m)
    assert W.value([0,1,m,1])==2*m
    return dict(endpoint_minus_mass=str(m),exact_response_value=str(target),
                terminal_minima=terminals,counts=counts)


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    result=dict(scope='Finite certificate verifier prototype; no completeness or game-value claim',
                quadratic_solver_fixtures=self_test(),local_tests=local_tests(),
                complete_certificates=[endpoint_certificate(x) for x in [Q(1,5),Q(1,3),Q(1,2),Q(2,3),Q(4,5)]])
    if args.output:args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
