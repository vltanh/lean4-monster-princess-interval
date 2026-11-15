"""Positive-start early sheet: linear features and signed-prefix optimizer.

The new density is
 jE(z,s)=[k(s0)-p(z)]/(s0+6+z)+int_s0^s dk(r)/(r+6+z), p=f+g.
It replaces positive M2 line mass, leaving g as its total start marginal.
Require nonnegative lower edge, residual g0, and the separated support
conditions in SIGNED_EARLY_RESPONSE.md. No density LP is run here.
"""
import numpy as np
from numba import njit
from separated_oracle import (affine_integral, beta, bin_at, phi_integral,
                              value_at, i0, affine_late_base, residual_row_affine)
from positive_sheet_oracle import features_two_late, positive_line_residual


@njit
def plus_log(A, lo, hi):
    return np.log((A+hi)/(A+lo)) if hi>lo else 0.


@njit
def inverse_positive_part(r, parameters, segments, count):
    """Integral over -a<V<c of (phi(V)-r)_+."""
    a,u,c,y=parameters
    total=max(0.,a+min(c,0.))*max(0.,u-r)
    for i in range(count):
        lo,hi,slope,intercept=segments[i]
        if slope==0:
            total+=(hi-lo)*max(0.,intercept-r)
        else:
            lo=max(lo,(r-intercept)/slope)
            total+=affine_integral(lo,hi,intercept-r,slope)
    return total


@njit
def rectangular_component(r, lo, hi, parameters, segments, count):
    """Four-payoff correction per coefficient C for C/(r+6+z)."""
    if hi<=lo:return 0.
    a,u,c,y=parameters;A=r+6
    cutoff=max(0.,-c)
    result=max(0.,u-r)*max(0.,min(hi,a)-max(lo,cutoff))
    result-=(1-r)**2*plus_log(A,lo,min(hi,min(a,cutoff)))
    alpha=-(1-r)**2/2-inverse_positive_part(r,parameters,segments,count)
    result+=plus_log(A,max(lo,a),hi)*alpha
    reflected=affine_integral(r,1.,-4.,1.)+phi_integral(r,1.,parameters,segments,count)
    result+=plus_log(A,lo,hi)*reflected
    return result


@njit
def positive_early_features(parameters, segments, count, knots, left, right, s0):
    n=len(knots)-1;row=np.zeros(1+4*n);ks=bin_at(s0,knots)
    for j in range(n):
        lo=max(left,knots[j]);hi=min(right,knots[j+1])
        if hi<=lo:continue
        factor=rectangular_component(s0,lo,hi,parameters,segments,count)/4
        row[1+2*n+ks]+=factor
        row[1+j]-=factor;row[1+n+j]-=factor
    for j in range(1,n):
        r=knots[j]
        if r<=s0+1e-13:continue
        factor=rectangular_component(r,left,right,parameters,segments,count)/4
        row[1+2*n+j]+=factor;row[1+2*n+j-1]-=factor
    return row


@njit
def positive_early_mass_row(z, j, knots, left, right, s0):
    n=len(knots)-1;row=np.zeros(1+4*n)
    if not left<=z<=right:return row
    ks=bin_at(s0,knots);factor=(1-s0)/(s0+6+z)
    row[1+2*n+ks]+=factor;row[1+j]-=factor;row[1+n+j]-=factor
    for i in range(1,n):
        r=knots[i]
        if r>s0+1e-13:
            factor=(1-r)/(r+6+z)
            row[1+2*n+i]+=factor;row[1+2*n+i-1]-=factor
    return row


@njit
def positive_early_threshold(a, s, knots, pvals, kvals, left, right, s0):
    """J_a(s)=integral over positive starts z>a of jE(z,s)."""
    if s<=s0:return 0.
    lower=max(a,left)
    if lower>=right:return 0.
    ks=value_at(s0,knots,kvals);total=0.
    for j in range(len(pvals)):
        lo=max(lower,knots[j]);hi=min(right,knots[j+1])
        if hi>lo:total+=(ks-pvals[j])*plus_log(s0+6,lo,hi)
    for j in range(1,len(kvals)):
        r=knots[j]
        if s0+1e-13<r<s-1e-13:
            total+=(kvals[j]-kvals[j-1])*plus_log(r+6,lower,right)
    return total


@njit
def positive_early_beta_row(s, knots, left, right, s0):
    """Linear betaP(s) row in the original density variables."""
    n=len(knots)-1;row=np.zeros(1+4*n)
    if s<=s0:return row
    ks=bin_at(s0,knots)
    for j in range(n):
        lo=max(left,knots[j]);hi=min(right,knots[j+1])
        if hi<=lo:continue
        factor=plus_log(s0+6,lo,hi)
        row[1+2*n+ks]+=factor;row[1+j]-=factor;row[1+n+j]-=factor
    for j in range(1,n):
        r=knots[j]
        if s0+1e-13<r<s-1e-13:
            factor=plus_log(r+6,left,right)
            row[1+2*n+j]+=factor;row[1+2*n+j-1]-=factor
    return row


@njit
def overlap_betaN(a,s,knots,variables,neg_left,neg_right,neg_s0,
                  pos_left,pos_right,pos_s0,edge_trace=True):
    n=len(knots)-1;k=variables[1+2*n:1+3*n]
    result=beta(a,s,knots,k,neg_left,neg_right,neg_s0,edge_trace)
    if s<=neg_s0:return result
    for j in range(n):
        lo=max(neg_left,knots[j]);hi=min(neg_right,a,knots[j+1])
        if hi<=lo:continue
        bp=positive_early_beta_row((lo+hi)/2,knots,pos_left,pos_right,pos_s0)@variables
        result-=bp*i0(neg_s0+6,lo,hi)
    return result


@njit
def negative_rectangle(r,lo,hi,parameters,segments,count):
    a,u,c,y=parameters;A=r+6
    result=max(0.,u-r)*max(0.,min(hi,c)-lo)
    result-=(1-r)**2*i0(A,max(lo,c),hi)
    reflected=affine_integral(r,1.,-4.,1.)+phi_integral(r,1.,parameters,segments,count)
    result+=i0(A,lo,min(a,hi))*reflected
    return result


@njit
def overlap_features(parameters,segments,count,knots,negative_profile,
                     neg_left,neg_right,neg_s0,pos_left,pos_right,pos_s0):
    """Replace ell by ell+betaP in hL and subtract betaP from hE edge."""
    n=len(knots)-1;row=np.zeros(1+4*n);a,u,c,y=parameters
    for j in range(n):
        lo,hi=knots[j],knots[j+1]
        bp=positive_early_beta_row((lo+hi)/2,knots,pos_left,pos_right,pos_s0)
        l=max(lo,neg_left);h=min(hi,neg_right)
        if h>l:
            row-=bp*negative_rectangle(neg_s0,l,h,parameters,segments,count)/4
        v0,v1=negative_profile[j]
        if v0+v1*(lo+hi)/2>1+1e-13:
            row-=bp*affine_late_base(v0,v1,lo,hi,a,c,y)/4
    return row


@njit
def signed_negative_residual(z,j,knots,negative_profile,neg_left,neg_right,neg_s0,
                             pos_left,pos_right,pos_s0):
    row=residual_row_affine(z,j,knots,negative_profile,neg_left,neg_right,neg_s0,True)
    bp=positive_early_beta_row(z,knots,pos_left,pos_right,pos_s0)
    if neg_left<=z<=neg_right:
        row+=bp*(1-neg_s0)/(neg_s0+6-z)
    v=negative_profile[j,0]+negative_profile[j,1]*z
    if v>1:row+=bp*(v-1)/(v+6-z)
    return row


@njit
def signed_positive_residual(z,j,knots,positive_late_profile,pos_left,pos_right,pos_s0):
    return (positive_line_residual(z,j,knots,positive_late_profile)
            -positive_early_mass_row(z,j,knots,pos_left,pos_right,pos_s0))


@njit
def signed_negative_edge(z,j,knots,neg_s0,pos_left,pos_right,pos_s0):
    n=len(knots)-1
    row=-positive_early_beta_row(z,knots,pos_left,pos_right,pos_s0)
    row[1+2*n+bin_at(neg_s0,knots)]+=1;row[1+2*n+j]-=1
    return row


@njit
def signed_positive_prefix(parameters, knots, variables,
                           neg_left, neg_right, neg_s0,
                           pos_left, pos_right, pos_s0, edge_trace=True, overlap=False):
    a,u,c,y=parameters;n=len(knots)-1
    k=variables[1+2*n:1+3*n]
    p=variables[1:1+n]+variables[1+n:1+2*n]
    segments=np.zeros((2*len(knots)+9,4));count=0
    if c<=0:return segments,count
    cuts=np.empty(len(knots)+6);nc=0
    cuts[nc]=0.;nc+=1;cuts[nc]=c;nc+=1
    for t in (u,neg_s0,pos_s0):
        if 0<t<c:cuts[nc]=t;nc+=1
    for t in knots:
        if 0<t<c:cuts[nc]=t;nc+=1
    cuts=np.sort(cuts[:nc])
    for i in range(len(cuts)-1):
        lo,hi=cuts[i],cuts[i+1]
        if hi<=lo+1e-14:continue
        z=(lo+hi)/2;lower=max(u,z)
        if overlap:
            bn=overlap_betaN(a,z,knots,variables,neg_left,neg_right,neg_s0,
                            pos_left,pos_right,pos_s0,edge_trace)
        else:bn=beta(a,z,knots,k,neg_left,neg_right,neg_s0,edge_trace)
        target=value_at(z,knots,k)+bn
        target+=positive_early_threshold(-1.,z,knots,p,k,pos_left,pos_right,pos_s0)
        # At a lower-edge jump the right derivative determines whether the
        # continuous primitive is already maximized at this feasible endpoint.
        alpha=value_at(lower,knots,k)+positive_early_threshold(a,lower+1e-12,knots,p,k,pos_left,pos_right,pos_s0)
        optimum=lower
        if alpha<target-1e-11:
            optimum=1.
            for j in range(n):
                x=knots[j]
                if x<lower-1e-13:continue
                trial=k[j]+positive_early_threshold(a,x+1e-12,knots,p,k,pos_left,pos_right,pos_s0)
                if trial>=target-1e-11:
                    optimum=x;break
        if optimum<=z+1e-12:segments[count]=np.array([lo,hi,1.,0.])
        else:segments[count]=np.array([lo,hi,0.,optimum])
        count+=1
    return segments,count


@njit
def optimal_features_signed_sheets(parameters, knots, negative_profile, variables,
                                   neg_left, neg_right, neg_s0, positive_late_profile,
                                   pos_left, pos_right, pos_s0, edge_trace=True, overlap=False):
    if overlap and not edge_trace:
        raise ValueError('Overlapping signed early sheets require the edge-trace construction')
    seg,count=signed_positive_prefix(parameters,knots,variables,neg_left,neg_right,neg_s0,
                                    pos_left,pos_right,pos_s0,edge_trace,overlap)
    result=(features_two_late(parameters,seg,count,knots,negative_profile,neg_left,neg_right,
                             neg_s0,positive_late_profile,edge_trace)
            +positive_early_features(parameters,seg,count,knots,pos_left,pos_right,pos_s0))
    if overlap:
        result+=overlap_features(parameters,seg,count,knots,negative_profile,
                                 neg_left,neg_right,neg_s0,pos_left,pos_right,pos_s0)
    return result


def verify():
    from separated_oracle import baseline_prefix
    from verify_separated import actual_princess,integrate,m2,pair
    knots=np.array([0.,.125,.25,.5,.75,.875,.9375,1.]);n=len(knots)-1
    left,right,s0=.125,.75,.875
    f=np.array([0.,.03,.05,.07,.1,.2,.4]);g=np.full(n,.06)
    k=np.array([.02,.03,.05,.08,.12,.25,.55])
    variables=np.r_[.5,f,g,k,np.zeros(n)]
    cases=[(.07,.4,.8,.9),(.2,.6,.96,.98),(.6,.92,.7,.94),
           (.92,.96,-.3,.7),(.92,.97,-.7,-.5),(.97,.985,-.8,-.8)]
    errors=[]
    for case in cases:
        parameters=np.array(case);seg,count=baseline_prefix(parameters,knots)
        expected=positive_early_features(parameters,seg,count,knots,left,right,s0)@variables
        vals=[]
        for eps in (2e-5,1e-5):
            princess,uv=actual_princess(parameters,seg[:count],eps)
            zcuts=list(knots)+[parameters[0],-parameters[2],-parameters[3]]
            scuts=list(knots)+[U for U,V in uv]+[V for U,V in uv]
            def at_z(z):
                j=bin_at(z,knots);old=pair(m2(-z,1.),princess)
                edge=(value_at(s0,knots,k)-f[j]-g[j])/(s0+6+z)
                total=edge*integrate(lambda s:pair(m2(-z,s),princess)-old,s0,1.,scuts)
                for h in range(1,n):
                    r=knots[h]
                    if r>s0+1e-13:
                        total+=(k[h]-k[h-1])/(r+6+z)*integrate(
                            lambda s:pair(m2(-z,s),princess)-old,r,1.,scuts)
                return total
            vals.append(integrate(at_z,left,right,zcuts))
        error=abs(2*vals[1]-vals[0]-expected);errors.append(error)
        assert error<3e-9,(case,expected,vals,error)
        print('POSITIVE_EARLY_CAPTURE',case,'error',error)
    print('PASS: 6 independent positive-early capture feature limits; maximum error',max(errors))

    # Independent check of both signed cross-price corrections. No helper
    # from overlap_features is used to evaluate the actual captures.
    pos_left,pos_right,pos_s0=.125,.25,.5
    neg_left,neg_right,neg_s0=.5,.75,.875
    kop=np.array([.02,.03,.05,.14,.2,.3,.6])
    variables_overlap=np.r_[.5,f,g,kop,np.zeros(n)]
    negative_profile=np.c_[np.ones(n),np.zeros(n)]
    negative_profile[bin_at(.5,knots),0]=1.125
    errors=[]
    for case in [(.2,.6,.96,.98),(.7,.93,.6,.9),(.94,.97,-.6,.7)]:
        parameters=np.array(case);seg,count=baseline_prefix(parameters,knots)
        expected=overlap_features(parameters,seg,count,knots,negative_profile,
                                  neg_left,neg_right,neg_s0,pos_left,pos_right,pos_s0)@variables_overlap
        vals=[]
        for eps in (2e-5,1e-5):
            princess,uv=actual_princess(parameters,seg[:count],eps)
            zcuts=list(knots)+list(parameters)
            scuts=list(knots)+[U for U,V in uv]+[V for U,V in uv]
            def at_z(z):
                bp=positive_early_threshold(-1.,z,knots,f+g,kop,pos_left,pos_right,pos_s0)
                old=pair(m2(z,1.),princess);total=0.
                if neg_left<z<neg_right:
                    total-=bp/(neg_s0+6-z)*integrate(
                        lambda s:pair(m2(z,s),princess)-old,neg_s0,1.,scuts)
                j=bin_at(z,knots);v=negative_profile[j,0]+negative_profile[j,1]*z
                if v>1:
                    total-=bp/(v+6-z)*integrate(
                        lambda s:pair(m2(z,s),princess)-old,1.,v,scuts)
                return total
            vals.append(integrate(at_z,0.,1.,zcuts))
        error=abs(2*vals[1]-vals[0]-expected);errors.append(error)
        assert error<3e-9,(case,expected,vals,error)
        print('SIGNED_OVERLAP_CAPTURE',case,'error',error)
    print('PASS: 3 independent signed-overlap capture feature limits; maximum error',max(errors))


if __name__=='__main__':verify()
