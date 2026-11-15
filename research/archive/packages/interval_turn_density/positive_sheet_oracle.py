"""Analytic positive-M2 late-sheet features for the separated response oracle.

The positive profile is constant within each fixed start bin.  Densities
remain linear in the original variables w0,f,g_total,k,ell.  The positive
line residual g_total-Hplus must be nonnegative.
"""
import numpy as np
from numba import njit
from separated_oracle import bin_at,features_affine,optimal_features_affine

@njit
def log_integral(A,lo,hi):
    return np.log((A+hi)/(A+lo))if hi>lo else 0.

@njit
def component(parameters,A,H,M,lo,hi):
    a,u,c,y=parameters
    result=M*(2*log_integral(A,lo,min(hi,a))+3*log_integral(A,max(lo,a),hi)
        +2*log_integral(A,lo,min(hi,min(a,max(0.,-y)))))
    result+=H*(y-c)*log_integral(A,max(lo,a),hi)
    l=max(lo,max(0.,-y));r=min(hi,min(a,max(0.,-c)))
    if r>l:result-=H*((r-l)+(7-A)*log_integral(A,l,r))
    return result/4

@njit
def positive_sheet_features(parameters,knots,profile):
    n=len(knots)-1;row=np.zeros(1+4*n)
    for j in range(n):
        lo,hi=knots[j],knots[j+1];v=profile[j]
        if v<=1:continue
        factor=component(parameters,v+6,v-1,(v-1)**2/2,lo,hi)
        row[1+bin_at(2-v,knots)]+=factor;row[1+j]-=factor
        for h in range(1,n):
            r=2-knots[h]
            if 1<r<v:
                factor=component(parameters,r+6,r-1,(r-1)**2/2,lo,hi)
                row[1+h]+=factor;row[h]-=factor
    return row

@njit
def positive_sheet_mass_row(z,j,knots,profile):
    n=len(knots)-1;row=np.zeros(1+4*n);v=profile[j]
    if v<=1:return row
    factor=(v-1)/(v+6+z)
    row[1+bin_at(2-v,knots)]+=factor;row[1+j]-=factor
    for h in range(1,n):
        r=2-knots[h]
        if 1<r<v:
            factor=(r-1)/(r+6+z)
            row[1+h]+=factor;row[h]-=factor
    return row

@njit
def positive_line_residual(z,j,knots,profile):
    row=-positive_sheet_mass_row(z,j,knots,profile)
    row[1+len(knots)-1+j]+=1
    return row

@njit
def features_two_late(parameters,segments,count,knots,negative_profile,left,right,s0,
                      positive_profile,edge_trace=False):
    return features_affine(parameters,segments,count,knots,negative_profile,left,right,s0,edge_trace)+positive_sheet_features(parameters,knots,positive_profile)

@njit
def optimal_features_two_late(parameters,knots,negative_profile,weights,left,right,s0,
                              positive_profile,edge_trace=False):
    return optimal_features_affine(parameters,knots,negative_profile,weights,left,right,s0,edge_trace)+positive_sheet_features(parameters,knots,positive_profile)


def verify():
    from separated_oracle import baseline_prefix,value_at
    from verify_separated import actual_princess,integrate,m2,pair
    knots=np.array([0.,.25,.5,.75,.875,.9375,1.]);n=len(knots)-1
    profile=np.array([1.,1.125,1.125,1.,1.,1.])
    f=np.array([.1,.2,.3,.8,1.2,2.])
    weights=np.r_[.5,f,[.2]*n,[.1]*n,[.05]*n]
    cases=[(.2,.4,.8,.9),(.6,.95,.7,.9),(.92,.94,-.3,.7),
           (.92,.95,-.7,.65),(.97,.98,-.7,-.5)]
    errors=[]
    for case in cases:
        params=np.array(case);seg,count=baseline_prefix(params,knots)
        expected=float(positive_sheet_features(params,knots,profile)@weights)
        values=[]
        for eps in [2e-5,1e-5]:
            princess,uv=actual_princess(params,seg[:count],eps)
            zcuts=list(knots)+[params[0],-params[2],-params[3]]
            scuts=[U for U,V in uv]+[V for U,V in uv]+[2-x for x in knots]
            total=0.
            for j in range(n):
                v=profile[j]
                if v<=1:continue
                def at_z(z):
                    old=pair(m2(-z,1.),princess)
                    edge=(value_at(2-v,knots,f)-f[j])/(v+6+z)
                    val=edge*integrate(lambda s:pair(m2(-z,s),princess)-old,1.,v,scuts)
                    for h in range(1,n):
                        r=2-knots[h]
                        if 1<r<v:
                            val+=(f[h]-f[h-1])/(r+6+z)*integrate(
                                lambda s:pair(m2(-z,s),princess)-old,1.,r,scuts)
                    return val
                total+=integrate(at_z,knots[j],knots[j+1],zcuts)
            values.append(total)
        error=abs(2*values[1]-values[0]-expected);errors.append(error)
        assert error<3e-9,(case,expected,values,error)
        print('POSITIVE_CAPTURE',case,'error',error)
    print('PASS: 5 independent first-capture positive-sheet feature limits; maximum error',max(errors))

if __name__=='__main__':verify()
