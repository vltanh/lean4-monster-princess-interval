"""One integrable pantograph tail column for the complete signed-M3 law.

For eps=1-x, use f=eps^(-2/3) H(log(16/eps)) on eps<1/64
and k=ell=.5 eps^(-1/6) H(log(16/eps)) on eps<1e-5.
All induced M2/M3 sheets are included. There is no extra density bin or
endpoint atom. The coefficient of this entire column is nonnegative.

The finite kernel series below converge with ratio at most (1/64)/3.
Moment quadrature evaluates the nonsingular exponential representation;
the separate verifier compares it with adaptive integration.
"""
import math
import numpy as np
from numba import njit
from numpy.polynomial.laguerre import laggauss

from endpoint_tail import coefficients, GAMMA
from m3_attached_oracle import M3_LEFT, M3_RIGHT, positive_late_profile


F_DELTA = 1./64.
K_DELTA = 1e-5
F_CUTOFF = 1.-F_DELTA
CUTOFF = 1.-K_DELTA
ORDER = 7
COEFF = coefficients(12)
LAG_X, LAG_W = laggauss(24)


@njit
def H(x):
    inv = 1./x
    power, total = 1., 0.
    for c in COEFF:
        total += c*power
        power *= inv
    return x**GAMMA*total


@njit
def moment(eps, power, degree=0, scale=1.):
    eps = min(F_DELTA if power > .5 else K_DELTA, max(0., eps))
    if eps <= 0.:
        return 0.
    rate = 1.-power+degree
    x = math.log(16./eps)
    total = 0.
    for i in range(len(LAG_X)):
        total += LAG_W[i]*H(x+LAG_X[i]/rate)
    return scale*eps**rate*total/rate


FM = np.array([moment(F_DELTA, 2./3., j, 1.) for j in range(ORDER+4)])
KM = np.array([moment(K_DELTA, 1./6., j, .5) for j in range(ORDER+4)])


@njit
def density(x, power, scale):
    if x < (F_CUTOFF if power > .5 else CUTOFF):
        return 0.
    eps = max(1.-x, 1e-16)
    return scale*eps**(-power)*H(math.log(16./eps))


@njit
def kbar(x):
    return moment(1.-x, 1./6., 0, .5)


@njit
def kcum(x):
    return KM[0]-kbar(x) if x > CUTOFF else 0.


@njit
def kcum_primitive(x):
    if x <= CUTOFF:
        return 0.
    eps = max(0., 1.-x)
    return KM[1]-moment(eps, 1./6., 1, .5)-eps*kcum(x)


@njit
def kbar_primitive_eps(eps):
    eps = max(0., eps)
    return eps*moment(eps, 1./6., 0, .5)-moment(eps, 1./6., 1, .5)


@njit
def density_affine(lo, hi, intercept, slope, power, scale):
    lo, hi = max(lo, F_CUTOFF if power > .5 else CUTOFF), min(hi, 1.)
    if hi <= lo:
        return 0.
    m0 = moment(1.-lo, power, 0, scale)-moment(1.-hi, power, 0, scale)
    m1 = moment(1.-lo, power, 1, scale)-moment(1.-hi, power, 1, scale)
    return (intercept+slope)*m0-slope*m1


@njit
def kernel_moment(D, lo, hi, sign, degree):
    """Integral dz/(D+sign*z)^(degree+1)."""
    if hi <= lo:
        return 0.
    left, right = D+sign*lo, D+sign*hi
    if degree == 0:
        return sign*np.log1p((right-left)/left)
    return sign*(left**(-degree)-right**(-degree))/degree


@njit
def line_f(parameters):
    a, u, c, y = parameters
    cuts = np.sort(np.array([F_CUTOFF, 1., a, -c, -y]))
    total = 0.
    for lo, hi in zip(cuts[:-1], cuts[1:]):
        lo, hi = max(lo, F_CUTOFF), min(hi, 1.)
        if hi <= lo:
            continue
        x = (lo+hi)/2.
        if x < a:
            if -x <= c:
                intercept, slope = 6.+u, -3.
            elif -x <= y:
                intercept, slope = 7., -3.
            else:
                intercept, slope = 8., -4.
        else:
            intercept, slope = 8.+y, -3.
        total += density_affine(lo, hi, intercept, slope, 2./3., 1.)
    return total


@njit
def line_negative_m1(parameters, segments, count):
    a, u, c, y = parameters
    total = 0.
    for i in range(count):
        lo, hi, slope, intercept = segments[i]
        total += density_affine(lo, hi, intercept, 1.+slope, 1./6., .5)
    total += density_affine(max(c, 0.), max(y, 0.), 1., 1., 1./6., .5)
    total += density_affine(max(y, 0.), 1., 2., 2., 1./6., .5)
    total += density_affine(0., a, 6., 2., 1./6., .5)
    total += density_affine(a, 1., -a, 1., 1./6., .5)
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
def late_f_column(parameters, knots, negative_profile):
    """Integration by parts against df; no singular derivative quadrature."""
    a, u, c, y = parameters
    result = 0.
    plus = positive_late_profile(knots)
    for j in range(len(knots)-1):
        lo, hi = knots[j], knots[j+1]
        v = negative_profile[j, 0]+negative_profile[j, 1]*(lo+hi)/2.
        if v > 1.+1e-12:
            if v-1. < F_DELTA-1e-12:
                raise ValueError('Tail support reaches beyond the fixed late cap')
            ml, mh = max(lo, max(c, 0.)), min(hi, max(y, 0.))
            result -= max(0., mh-ml)*FM[0]
            for n in range(ORDER+1):
                coef = (kernel_moment(7., lo, min(hi, a), -1, n)
                        +kernel_moment(7., max(lo, max(y, 0.)), hi, -1, n)
                        +kernel_moment(7., ml, mh, -1, n))
                result += (n+2.)*((-1.)**n)*coef*FM[n+1]
        if plus[j] > 1.+1e-12:
            if plus[j]-1. < F_DELTA-1e-12:
                raise ValueError('Positive late cap lies inside the tail generator range')
            ml, mh = max(lo, max(0., -y)), min(hi, min(a, max(0., -c)))
            result -= max(0., mh-ml)*FM[0]
            for n in range(ORDER+1):
                ia = kernel_moment(7., lo, min(hi, a), 1, n)
                ib = kernel_moment(7., max(lo, a), hi, 1, n)
                ic = kernel_moment(7., lo, min(hi, min(a, max(0., -y))), 1, n)
                im = kernel_moment(7., ml, mh, 1, n)
                result += ((-1.)**n)*((n+2.)*(ia+1.5*ib+ic+im)*FM[n+1]
                              +(y-c)*(n+1.)*ib*FM[n])
    return result


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
def early_negative_k(parameters, segments, count, left, right):
    a, u, c, y = parameters
    total = kcum_inverse_integral(left, min(right, c), segments, count)
    for n in range(ORDER+1):
        total -= (n+2.)*KM[n+1]*kernel_moment(7., max(left, c), right, -1, n)
    upper = min(a, right)
    if upper <= left:
        return total
    cuts = np.zeros(2*count+6)
    nc = 2
    cuts[0], cuts[1] = CUTOFF, 1.
    for v in (c, y):
        if CUTOFF < v < 1.:
            cuts[nc] = v; nc += 1
    for i in range(count):
        for j in (0, 1):
            v = segments[i, j]
            if CUTOFF < v < 1.:
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
            dm[n] = moment(e1, 1./6., n, .5)-moment(e0, 1./6., n, .5)
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
        numerator = KM[n+1]-moment(eps, 1./6., n+1, .5)-eps**(n+1)*cum
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
def tail_feature(parameters, segments, count, knots, negative_profile, left, right):
    return (line_f(parameters)+line_negative_m1(parameters, segments, count)
            +late_f_column(parameters, knots, negative_profile)
            +early_negative_k(parameters, segments, count, left, right)
            +m3_both_k(parameters, segments, count))/4.


@njit
def m3_price(a, U, sign, below=False):
    lo, hi = M3_LEFT, M3_RIGHT
    if below:
        hi = min(hi, a)
    else:
        lo = max(lo, a)
    if U <= CUTOFF or hi <= lo:
        return 0.
    return (density(U, 1./6., .5)*kernel_moment(4.-U, lo, hi, sign, 0)
            +kcum(U)*kernel_moment(4.-U, lo, hi, sign, 1))


@njit
def negative_early_price(a, U, left, right):
    hi = min(a, right)
    if U <= CUTOFF or hi <= left:
        return 0.
    result = density(U, 1./6., .5)*kernel_moment(U+6., left, hi, -1, 0)
    eps = 1.-U
    for n in range(ORDER+1):
        coef = (7.-hi)**(-n-1)-(7.-left)**(-n-1)
        result += coef*(KM[n]-moment(eps, 1./6., n, .5))
    return result


@njit
def early_mass(z):
    result = 0.
    for n in range(ORDER+1):
        result += (n+1.)*KM[n]/(7.-z)**(n+1.)
    return result


@njit
def late_mass(z, sign):
    result = 0.
    for n in range(ORDER+1):
        result += (n+1.)*((-1.)**n)*FM[n]/(7.+sign*z)**(n+1.)
    return result


def verify_moments():
    from scipy.integrate import quad
    from endpoint_tail import modulation
    errors = []
    for power, scale in ((2/3, 1.), (1/6, .5)):
        for degree in (0, 1, 3, 8):
            for eps in (F_DELTA if power > .5 else K_DELTA, 1e-6, 1e-12):
                rate = 1-power+degree
                L = math.log(16/eps)
                expected = scale*eps**rate*quad(lambda t: math.exp(-rate*t)*float(modulation(L+t)),
                                                0, np.inf, epsabs=1e-12, epsrel=1e-12)[0]
                actual = moment(eps, power, degree, scale)
                error = abs(actual/expected-1)
                errors.append(error)
                assert error < 3e-11, (power, degree, eps, error)
    print('TAIL_MOMENTS', len(errors), 'max relative error', max(errors))
    print('TAIL_NORMALIZATION_COLUMN', FM[0]+KM[0])


if __name__ == '__main__':
    verify_moments()
