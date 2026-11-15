"""Fast unit-amplitude four-score for the localized I component alone."""
from uniform_inward_features import njit


@njit(cache=True)
def _localized_integrand(d,b,c,v,u):
    return ((b+v)*(v+u-8.)-(1.+c-d-2.*v)*(u-b)
            +(u*u-b*b)/2.)


@njit(cache=True)
def localized_inward_feature(d,b,c,segments):
    mass=(1.-d)**2/2.
    below=max(0.,b-d)**2/2.
    result=(4.*mass+(1.+c)*(mass-below)+8.*below
            -max(0.,-d-c)*(1.-b)**2/2.)
    if b<=d:
        return result
    for segment in segments:
        vl,vr,alpha,beta=segment
        right=min(vr,-d)
        if right<=vl:
            continue
        middle=(vl+right)/2.
        result+=(right-vl)*(
            _localized_integrand(d,b,c,vl,alpha*vl+beta)
            +4.*_localized_integrand(d,b,c,middle,alpha*middle+beta)
            +_localized_integrand(d,b,c,right,alpha*right+beta))/6.
    return result
