"""Complete induced old-law column for k=ell=(U-d)+, d=7/8.

The coefficient is tied to the localized initial-inward triangle. This
module contains only the old-law ramp contribution; the I-only feature is
independently defined in interval_turn_sheet/localized_inward_features.py.
All line, negative-early and signed-M3 changes are included. Late-sheet
starts end at d, so ellRamp has no late-start contribution.
"""
import numpy as np
from numba import njit
from m3_attached_oracle import M3_LEFT, M3_RIGHT
from singular_tail_basis import kernel_moment

D = .875
CUTOFF = D
ORDER = 12

@njit
def density(x):
    return max(0., min(x,1.)-D)

@njit
def moment(eps, degree=0, cutoff=D):
    e = min(1.-cutoff, max(0.,eps))
    return (1.-D)*e**(degree+1)/(degree+1)-e**(degree+2)/(degree+2)

KM = np.array([moment(1.-D,j) for j in range(ORDER+4)])

@njit
def kbar(x):
    return moment(1.-x)

@njit
def kcum(x):
    return max(0.,x-D)**2/2.

@njit
def kcum_primitive(x):
    return max(0.,x-D)**3/6.

@njit
def kbar_primitive_eps(eps):
    return eps*moment(eps)-moment(eps,1)

@njit
def density_affine(lo,hi,intercept,slope):
    lo,hi=max(lo,D),min(hi,1.)
    if hi<=lo:return 0.
    m0=moment(1.-lo)-moment(1.-hi)
    m1=moment(1.-lo,1)-moment(1.-hi,1)
    return (intercept+slope)*m0-slope*m1

@njit
def early_cum(x,s0):
    return max(0.,(x-D)**2-(s0-D)**2)/2. if x>s0 else 0.

@njit
def early_cum_primitive(x,s0):
    if x<=s0:return 0.
    e=1.-x
    return moment(1.-s0,1,s0)-moment(e,1,s0)-e*early_cum(x,s0)

@njit
def early_cum_inverse_integral(lo,hi,segments,count,s0):
    total=0.
    for i in range(count):
        sl,sr,slope,intercept=segments[i]
        sl,sr=max(sl,lo),min(sr,hi)
        if sr<=sl:continue
        if slope==0.:
            total+=(sr-sl)*early_cum(intercept,s0)
        else:
            total+=(early_cum_primitive(slope*sr+intercept,s0)-early_cum_primitive(slope*sl+intercept,s0))/slope
    return total

@njit
def line_negative_m1(parameters, segments, count):
    a, u, c, y = parameters
    total = 0.
    for i in range(count):
        lo, hi, slope, intercept = segments[i]
        total += density_affine(lo, hi, intercept, 1.+slope)
    total += density_affine(max(c, 0.), max(y, 0.), 1., 1.)
    total += density_affine(max(y, 0.), 1., 2., 2.)
    total += density_affine(0., a, 6., 2.)
    total += density_affine(a, 1., -a, 1.)
    total += max(0., a+min(c, 0.))*kbar(u)
    for i in range(count):
        lo, hi, slope, intercept = segments[i]
        if slope == 0.:
            total += (hi-lo)*kbar(intercept)
        else:
            e0 = 1.-slope*lo-intercept
            e1 = 1.-slope*hi-intercept
            total += (kbar_primitive_eps(e0)-kbar_primitive_eps(e1))/slope
    return total


@njit
def kcum_inverse_integral(lo, hi, segments, count):
    total = 0.
    for i in range(count):
        sl, sr, slope, intercept = segments[i]
        sl, sr = max(sl, lo), min(sr, hi)
        if sr <= sl:
            continue
        if slope == 0.:
            total += (sr-sl)*kcum(intercept)
        else:
            total += (kcum_primitive(slope*sr+intercept)-kcum_primitive(slope*sl+intercept))/slope
    return total


@njit
def phi_coefficients(x, parameters, segments, count):
    a, u, c, y = parameters
    for i in range(count):
        if segments[i, 0]-1e-13 <= x <= segments[i, 1]+1e-13:
            return segments[i, 2], segments[i, 3]
    if x <= y:
        return 0., 1.
    return 1., 2.


@njit
def early_negative_k(parameters, segments, count, left, right, s0):
    a, u, c, y = parameters
    EM = np.array([moment(1.-s0, j, s0) for j in range(ORDER+4)])
    total = early_cum_inverse_integral(left, min(right, c), segments, count, s0)
    for n in range(ORDER+1):
        total -= (n+2.)*EM[n+1]*kernel_moment(7., max(left, c), right, -1, n)
    upper = min(a, right)
    if upper <= left:
        return total
    cuts = np.zeros(2*count+6)
    nc = 2
    cuts[0], cuts[1] = s0, 1.
    for v in (c, y):
        if s0 < v < 1.:
            cuts[nc] = v; nc += 1
    for i in range(count):
        for j in (0, 1):
            v = segments[i, j]
            if s0 < v < 1.:
                cuts[nc] = v; nc += 1
    cuts = np.sort(cuts[:nc])
    B = 0.
    for i in range(nc-2, -1, -1):
        lo, hi = cuts[i], cuts[i+1]
        if hi <= lo+1e-15:
            continue
        slope, intercept = phi_coefficients((lo+hi)/2., parameters, segments, count)
        e0, e1 = 1.-hi, 1.-lo
        b0, b1 = slope+intercept-3., -(1.+slope)
        constant = B-b0*e0-b1*e0*e0/2.
        dm = np.zeros(ORDER+3)
        for n in range(ORDER+3):
            dm[n] = moment(e1, n, s0)-moment(e0, n, s0)
        for n in range(ORDER+1):
            In = kernel_moment(7., left, upper, -1, n)
            Inext = kernel_moment(7., left, upper, -1, n+1)
            total += In*(b0*dm[n]+b1*dm[n+1])
            total += (n+1.)*Inext*(constant*dm[n]+b0*dm[n+1]+b1*dm[n+2]/2.)
        B += b0*(e1-e0)+b1*(e1*e1-e0*e0)/2.
    return total


@njit
def m3_cumulative(t, lo, hi, sign):
    if hi <= lo or t <= CUTOFF:
        return 0.
    return kcum(t)*kernel_moment(4.-t, lo, hi, sign, 0)


@njit
def m3_primitive(t, lo, hi, sign):
    if hi <= lo or t <= CUTOFF:
        return 0.
    eps = max(0., 1.-t)
    cum = kcum(t)
    result = 0.
    for n in range(ORDER+1):
        numerator = KM[n+1]-moment(eps, n+1)-eps**(n+1)*cum
        result += ((-1.)**n)*kernel_moment(3., lo, hi, sign, n)*numerator/(n+1.)
    return result


@njit
def m3_reflected(parameters, segments, count, lo, hi, sign):
    result = 4.*m3_cumulative(1., lo, hi, sign)
    for i in range(count):
        sl, sr, slope, intercept = segments[i]
        sl, sr = max(sl, CUTOFF), min(sr, 1.)
        if sr <= sl:
            continue
        b, d = 1.+slope, intercept-8.
        result += ((b*sr+d)*m3_cumulative(sr, lo, hi, sign)
                   -(b*sl+d)*m3_cumulative(sl, lo, hi, sign)
                   -b*(m3_primitive(sr, lo, hi, sign)-m3_primitive(sl, lo, hi, sign)))
    return result


@njit
def m3_both_k(parameters, segments, count):
    a, u, c, y = parameters
    lo, hi = M3_LEFT, M3_RIGHT
    if a >= hi and c <= -hi:
        return 0.
    cutoff = max(0., -c)
    total = kcum(u)*max(0., min(hi, a)-max(lo, cutoff))
    total -= 4.*m3_cumulative(1., lo, min(hi, min(a, cutoff)), 1)
    al = max(lo, a)
    if al < hi:
        total -= m3_primitive(1., al, hi, 1)
        total -= max(0., a+min(c, 0.))*m3_cumulative(u, al, hi, 1)
        for i in range(count):
            sl, sr, slope, intercept = segments[i]
            if slope == 0.:
                total -= (sr-sl)*m3_cumulative(intercept, al, hi, 1)
            else:
                total -= (m3_primitive(slope*sr+intercept, al, hi, 1)
                          -m3_primitive(slope*sl+intercept, al, hi, 1))/slope
    total += m3_reflected(parameters, segments, count, lo, hi, 1)
    total += kcum_inverse_integral(lo, min(hi, c), segments, count)
    total -= 4.*m3_cumulative(1., max(lo, c), hi, -1)
    total += m3_reflected(parameters, segments, count, lo, min(hi, a), -1)
    return total



@njit
def ramp_feature(parameters,segments,count,left,right,s0):
    return (line_negative_m1(parameters,segments,count)
            +early_negative_k(parameters,segments,count,left,right,s0)
            +m3_both_k(parameters,segments,count))/4.

@njit
def negative_ramp_change(parameters,negative,count):
    a,u,c,y=parameters
    total=0.
    for i in range(count):
        vl,vr,slope,level=negative[i]
        if slope!=0.:raise ValueError('Ramp negative inverses must be constant blocks')
        width=vr-vl
        total+=width*(kbar(level)-kbar(u))
        overlap=max(0.,min(M3_RIGHT,-vl)-max(M3_LEFT,-vr))
        total+=overlap*(kcum(level)-kcum(u))
        total-=width*(m3_cumulative(level,max(a,M3_LEFT),M3_RIGHT,1)
                      -m3_cumulative(u,max(a,M3_LEFT),M3_RIGHT,1))
    return total/4.

@njit
def general_ramp_feature(parameters,packed,count,left,right,s0):
    split=0
    while split<count and packed[split,0]<0.:split+=1
    result=ramp_feature(parameters,packed[split:count],count-split,left,right,s0)
    if split:result+=negative_ramp_change(parameters,packed[:split],split)
    return result

@njit
def m3_price(a,U,sign,below=False):
    lo,hi=M3_LEFT,M3_RIGHT
    if below:hi=min(hi,a)
    else:lo=max(lo,a)
    if U<=D or hi<=lo:return 0.
    return density(U)*kernel_moment(4.-U,lo,hi,sign,0)+kcum(U)*kernel_moment(4.-U,lo,hi,sign,1)

@njit
def negative_early_price(a,U,left,right,s0):
    hi=min(a,right)
    if U<=s0 or hi<=left:return 0.
    result=density(U)*kernel_moment(U+6.,left,hi,-1,0)
    e=1.-U
    for n in range(ORDER+1):
        coef=(7.-hi)**(-n-1)-(7.-left)**(-n-1)
        result+=coef*(moment(1.-s0,n,s0)-moment(e,n,s0))
    return result

@njit
def early_mass(z,s0):
    result=0.
    for n in range(ORDER+1):
        result+=(n+1.)*moment(1.-s0,n,s0)/(7.-z)**(n+1.)
    return result
