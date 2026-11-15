"""Fast linear four-score feature row for step uniform-inward density.

segments is an (n,4) float array: (V_left,V_right,alpha,beta), with
U(V)=alpha*V+beta on the open interval.  Vertical graph jumps contribute
zero.  A row dotted with h gives FOUR times the unnormalized upper score.
The h mass row is knots[1:]**2-knots[:-1]**2.  This is additional mass.
"""
import numpy as np
try:
    from numba import njit
except ImportError:
    def njit(**_options):
        return lambda function: function


@njit(cache=True)
def _bin_integrand(b, c, v, u, left, right):
    j = max(0., min(b,right)-max(abs(v),left))
    length = max(0., min(u,right)-max(b,v,left))
    return j*(v+u-8.)-(1.+c-2.*v)*length


@njit(cache=True)
def uniform_inward_feature_row(knots, b, c, segments):
    result = np.zeros(len(knots)-1)
    for index in range(len(result)):
        left, right = knots[index], knots[index+1]
        mass = right*right-left*left
        cut = min(right,max(left,b))
        below = cut*cut-left*left
        value = 4.*mass+(1.+c)*(mass-below)+8.*below
        lo = max(left,b,c)
        if lo < right:
            value += ((right**3-lo**3)/3.-(1.+c)*(right*right-lo*lo)/2.
                      +c*(right-lo))
        for segment in segments:
            vl, vr, alpha, beta = segment
            if vr <= vl:
                continue
            cuts = np.empty(12)
            count = 2
            cuts[0], cuts[1] = vl, vr
            for point in (0.,b,-b,left,right,-left,-right):
                if vl < point < vr:
                    cuts[count] = point
                    count += 1
            if alpha != 0.:
                for level in (left,right):
                    point = (level-beta)/alpha
                    if vl < point < vr:
                        cuts[count] = point
                        count += 1
            cuts = np.sort(cuts[:count])
            for i in range(count-1):
                l, r = cuts[i], cuts[i+1]
                if l == r:
                    continue
                m = (l+r)/2.
                value += (r-l)*(
                    _bin_integrand(b,c,l,alpha*l+beta,left,right)
                    +4.*_bin_integrand(b,c,m,alpha*m+beta,left,right)
                    +_bin_integrand(b,c,r,alpha*r+beta,left,right))/6.
        result[index] = value
    return result
