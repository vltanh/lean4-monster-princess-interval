#!/usr/bin/env python3
"""Exact finite isotonic checks of the signed-early compression mechanism.

This independently optimizes all nondecreasing inverse sequences by
dynamic programming, then compares their optimum with the best constant
inverse. It exercises the lower-edge derivative jump and both initial
position cases. It checks the finite comparison, not a continuous-field
existence theorem or a numerical game bound.
"""
from fractions import Fraction as F


def positive(x):
    return max(F(0), x)


def score(z, u, a, p0, p1, k0, k1, left, right, s0, j):
    """Integral of the independently stated derivative (4)."""
    def ordinary(lo, hi):
        return (p0+p1*z-k0)*(hi-lo)-k1*(hi*hi-lo*lo)/2
    if left < z < right:
        stop=min(u,s0)
        result=ordinary(a,stop) if stop>a else F(0)
    else:
        result=ordinary(a,u)
    result-=j*(positive(u-s0)**2-positive(a-s0)**2)/2
    return result


def main():
    count=0;jump_cases=0
    profiles=[(F(1,10),F(1,2),F(1,5),F(4,5)),
              (F(1,10),F(11,10),F(1,10),F(4,5)),
              (F(1,20),F(3,4),F(1,10),F(7,10)),
              (F(1,4),F(1,4),F(1,10),F(3,5))]
    for left,right,s0 in [(F(1,8),F(1,2),F(3,4)),
                          (F(1,4),F(5,8),F(7,8))]:
        for p0,p1,k0,k1 in profiles:
            if k0+k1*s0<p0+p1*right:continue
            for ai in range(1,16):
                a=F(ai,16)
                for ci in range(1,9):
                    cutoff=a*F(ci-1,8)
                    zs=[cutoff+(a-cutoff)*F(2*i+1,18) for i in range(8,-1,-1)]
                    us=sorted(set([a,s0] if s0>=a else [a])
                              | {a+(1-a)*F(i,10) for i in range(11)})
                    for j in ([F(0)] if a>right else [F(0),F(1,3),F(2)]):
                        rows=[[score(z,u,a,p0,p1,k0,k1,left,right,s0,j) for u in us]
                              for z in zs]
                        dp=rows[0]
                        for row in rows[1:]:
                            best=dp[0];new=[]
                            for old,value in zip(dp,row):
                                best=max(best,old);new.append(best+value)
                            dp=new
                        constant=max(sum(row[i] for row in rows) for i in range(len(us)))
                        assert max(dp)==constant,(a,cutoff,profiles,constant,max(dp))
                        count+=1
                        if a<s0 and any(left<z<right and p0+p1*z<k0+k1*s0 for z in zs):
                            jump_cases+=1
    print(f'PASS: {count} exact signed-early isotonic comparisons, including {jump_cases} lower-edge-jump cases')


if __name__=='__main__':main()
