#!/usr/bin/env python3
"""Exact local bad-response exclusion for a fixed signed-density law.

Only Python's standard library is used.  See
research/09-equilibrium-structure/LOCAL_SCALAR_GAP.md for the two convexity
reductions, the closed-domain conventions, and the scope.
No numerical optimizer or sample grid supplies any asserted inequality.
"""

from bisect import bisect_right
from fractions import Fraction as Q
import json
from pathlib import Path


class Law:
    def __init__(self, data):
        self.knots = tuple(map(Q, data['knots']))
        raw = data['raw_densities']
        n = len(self.knots)-1
        assert set(raw) == {'f', 'g', 'h', 'ell'}
        assert self.knots[0] == 0 and self.knots[-1] == 1
        assert all(a < b for a, b in zip(self.knots, self.knots[1:]))
        assert all(len(v) == n and all(x >= 0 for x in v) for v in raw.values())
        self.normalization = (Q(data['raw_endpoint_mass'])
            + sum((self.knots[i+1]-self.knots[i])
                  * sum(v[i] for v in raw.values()) for i in range(n)))
        assert self.normalization == Q(data['normalization']) > 0
        self.w0 = Q(data['raw_endpoint_mass'])/self.normalization
        self.density = {name: tuple(Q(x)/self.normalization for x in values)
                        for name, values in raw.items()}
        self.cumulative = {}
        for name, values in self.density.items():
            moments = [[Q(0)], [Q(0)]]
            for i, density in enumerate(values):
                lo, hi = self.knots[i:i+2]
                moments[0].append(moments[0][-1] + density*(hi-lo))
                moments[1].append(moments[1][-1] + density*(hi*hi-lo*lo)/2)
            self.cumulative[name] = moments
        assert self.w0+sum(self.primitive(name, 1) for name in raw) == 1
        for values in (self.density['f'],
                       tuple(a+b for a, b in zip(self.density['f'], self.density['g'])),
                       tuple(a+b for a, b in zip(self.density['h'], self.density['ell']))):
            assert all(a <= b for a, b in zip(values, values[1:]))

    def primitive(self, name, z, degree=0):
        z = Q(z)
        assert 0 <= z <= 1
        i = min(bisect_right(self.knots, z)-1, len(self.knots)-2)
        lo = self.knots[i]
        remainder = z-lo if degree == 0 else (z*z-lo*lo)/2
        return self.cumulative[name][degree][i]+self.density[name][i]*remainder

    def integral(self, name, lo, hi, constant=1, linear=0):
        assert 0 <= lo <= hi <= 1, (name, lo, hi)
        return (constant*(self.primitive(name, hi)-self.primitive(name, lo))
                + linear*(self.primitive(name, hi, 1)-self.primitive(name, lo, 1)))

    def payoff(self, a, u, c, y):
        """The continuous limiting scalar K on its entire closed domain."""
        a, u, c, y = map(Q, (a, u, c, y))
        assert 0 <= a <= u <= 1 and -a <= c <= y <= 1, (a, u, c, y)
        I = self.integral
        negc, negy = max(0, -c), max(0, -y)
        posc, posy = max(0, c), max(0, y)
        r, q = min(u, c), max(u, c)
        k4 = self.w0*(5+c)
        k4 += I('f', 0, negc, 8, -4)+I('f', negc, a, u+6, -3)
        k4 += I('f', a, 1, 8+c, -3)
        k4 += 12*I('g', 0, negc)+I('g', negc, a, u+4, -1)
        k4 += (5+c)*I('g', a, 1)
        k4 += 4*I('h', 0, a)+I('h', a, u, -a, 1)+I('h', q, 1, c, 1)
        k4 += I('ell', 0, a, 6, 2)+I('ell', a, u, -a, 1)
        k4 += I('ell', q, 1, c, 1)
        if c >= u:
            k4 += 2*I('h', u, c, 0, 1)+2*I('ell', u, c, 0, 1)
        if c < 0:
            k4 += 8*I('h', 0, 1)+2*I('ell', 0, 1, 1, 1)
        else:
            k4 += I('h', 0, r, u, 1)+I('ell', 0, r, u, 1)
            k4 += 8*I('h', c, 1)+2*I('ell', c, 1, 1, 1)
            if c >= u:
                k4 += 2*I('h', u, c, 0, 1)+2*I('ell', u, c, 0, 1)
        k4 += (y-c)*I('f', a, 1)
        k4 -= I('f', negy, negc, 1, -1)+I('ell', posc, posy, 1, 1)
        return k4/4


def cross(v, w):
    return v[0]*w[1]-v[1]*w[0]


def subtract(v, w):
    return v[0]-w[0], v[1]-w[1]


def interpolate(v, w, t):
    return v[0]+t*(w[0]-v[0]), v[1]+t*(w[1]-v[1])


def clip(polygon, alpha, beta, gamma):
    """Intersect a closed rational polygon with alpha*x+beta*y<=gamma."""
    if not polygon:
        return []
    result = []
    for v, w in zip(polygon, polygon[1:]+polygon[:1]):
        fv, fw = alpha*v[0]+beta*v[1]-gamma, alpha*w[0]+beta*w[1]-gamma
        if fv <= 0:
            result.append(v)
        if (fv < 0 < fw) or (fw < 0 < fv):
            result.append(interpolate(v, w, fv/(fv-fw)))
    unique = []
    for point in result:
        if point not in unique:
            unique.append(point)
    return unique


def quadratic_maximum(polygon, evaluate):
    """Exact max of a known degree<=2 polynomial on a convex polygon.

    Six exact values on an inscribed triangle recover its coefficients.
    Vertices, edge critical points, and a nonsingular interior critical
    point suffice.  A singular interior maximum also occurs on an edge.
    Degenerate point/segment cells are retained explicitly.
    """
    if not polygon:
        return None
    if len(polygon) == 1:
        return evaluate(polygon[0]), polygon[0]
    v0, v1 = polygon[:2]
    v2 = next((v for v in polygon[2:]
               if cross(subtract(v1, v0), subtract(v, v0)) != 0), None)
    if v2 is None:
        v0, v1 = min(polygon), max(polygon)
        f0, f1 = evaluate(v0), evaluate(v1)
        half = evaluate(interpolate(v0, v1, Q(1, 2)))
        aa = 2*(f1+f0-2*half)
        bb = f1-f0-aa
        choices = [(f0, v0), (f1, v1)]
        if aa < 0 and 0 < -bb/(2*aa) < 1:
            t = -bb/(2*aa)
            choices.append((aa*t*t+bb*t+f0, interpolate(v0, v1, t)))
        return max(choices)

    b1, b2 = subtract(v1, v0), subtract(v2, v0)
    det = cross(b1, b2)

    def coordinates(point):
        delta = subtract(point, v0)
        return cross(delta, b2)/det, cross(b1, delta)/det

    def physical(point):
        s, t = point
        return (v0[0]+s*b1[0]+t*b2[0], v0[1]+s*b1[1]+t*b2[1])

    f00, f10, f01 = evaluate(v0), evaluate(v1), evaluate(v2)
    fhalf0 = evaluate(interpolate(v0, v1, Q(1, 2)))
    f0half = evaluate(interpolate(v0, v2, Q(1, 2)))
    fhalfhalf = evaluate(interpolate(v1, v2, Q(1, 2)))
    aa, bb = 2*(f10+f00-2*fhalf0), 2*(f01+f00-2*f0half)
    dd, ee = f10-f00-aa, f01-f00-bb
    cc = 4*(fhalfhalf-f00-(dd+ee)/2-(aa+bb)/4)

    def polynomial(point):
        s, t = point
        return aa*s*s+bb*t*t+cc*s*t+dd*s+ee*t+f00

    # This is an implementation check, not the proof of polynomial degree.
    centroid = (sum(v[0] for v in polygon)/len(polygon),
                sum(v[1] for v in polygon)/len(polygon))
    assert polynomial(coordinates(centroid)) == evaluate(centroid)
    local = [coordinates(v) for v in polygon]
    choices = [(polynomial(v), physical(v)) for v in local]
    for v, w in zip(local, local[1:]+local[:1]):
        ds, dt = subtract(w, v)
        edge_a = aa*ds*ds+bb*dt*dt+cc*ds*dt
        edge_b = (2*aa*v[0]*ds+2*bb*v[1]*dt
                  + cc*(v[0]*dt+v[1]*ds)+dd*ds+ee*dt)
        if edge_a < 0 and 0 < -edge_b/(2*edge_a) < 1:
            point = interpolate(v, w, -edge_b/(2*edge_a))
            choices.append((polynomial(point), physical(point)))
    hessian_det = 4*aa*bb-cc*cc
    if hessian_det:
        point = ((cc*ee-2*bb*dd)/hessian_det,
                 (cc*dd-2*aa*ee)/hessian_det)
        signs = [cross(subtract(w, v), subtract(point, v))
                 for v, w in zip(local, local[1:]+local[:1])]
        if all(s >= 0 for s in signs) or all(s <= 0 for s in signs):
            choices.append((polynomial(point), physical(point)))
    return max(choices)


def reduced_slices(law, left, right):
    """Maximize u and a by exact affine/convex reductions on [left,right]."""
    i = bisect_right(law.knots, left)-1
    assert right == law.knots[i+1]
    f, g, h, ell = (law.density[name][i] for name in ('f', 'g', 'h', 'ell'))
    k_tail = [a+b for a, b in zip(law.density['h'][i:], law.density['ell'][i:])]
    assert all(x == k_tail[0] for x in k_tail)
    # These are 4*K_aa with fixed u and 4*d^2 K(a,a,c,y)/da^2.
    assert -g+h+3*ell >= 0
    assert 2*f+g-h+ell >= 0
    for a in (left, right):
        for u in (a, Q(1)):
            yield f'a={a},u={u}', -a, Q(1), (u,), lambda c, y, a=a, u=u: (a, u, c, y)
    # At c=-a, K_u=0.  The remaining moving a-boundary needs just u=1.
    yield 'a=-c,u=1', -right, -left, (), lambda c, y: (-c, Q(1), c, y)


def certify_bad_region(law, left, right, width, negative_c):
    signed_knots = sorted(set(law.knots+tuple(-x for x in law.knots)))
    best = None
    count = 0
    for name, clo, chi, extra_c_cuts, parameters in reduced_slices(law, left, right):
        if negative_c:
            chi = min(chi, Q(0))
        c_cuts = sorted({clo, chi} | {x for x in signed_knots+list(extra_c_cuts) if clo < x < chi})
        for ca, cb in zip(c_cuts, c_cuts[1:]):
            for ya, yb in zip(signed_knots, signed_knots[1:]):
                polygon = [(ca, ya), (cb, ya), (cb, yb), (ca, yb)]
                polygon = clip(polygon, 1, -1, 0)  # c<=y
                if not negative_c:
                    polygon = clip(polygon, -1, 1, width)  # y-c<=width
                if not polygon:
                    continue
                maximum = quadratic_maximum(polygon, lambda v: law.payoff(*parameters(*v)))
                count += 1
                result = maximum[0], parameters(*maximum[1]), name
                if best is None or result > best:
                    best = result
    return best, count


def verify(data):
    law = Law(data)
    left, right = map(Q, data['initial_interval'])
    jleft, jright = map(Q, data['forcing_interval'])
    width = Q(data['suffix_width'])
    witness = tuple(map(Q, data['reference_tuple']))
    assert 0 < left < right < 1 and 0 < width < 1
    assert left <= jleft < jright < right
    # The displayed comparison tuple itself is an interior legal scalar
    # tuple, so its limiting payoff is at most the scalar supremum S.
    assert 0 <= witness[0] <= witness[1] < 1 and -witness[0] <= witness[2] <= witness[3] < 1
    reference = law.payoff(*witness)
    tail_i = bisect_right(law.knots, left)-1
    margin = min(law.density['f'][tail_i:])-max(law.density['ell'])
    assert margin > 0
    forcing_mass = law.integral('f', jleft, jright)
    forcing_separation = right-jright
    rho = forcing_separation/(6+forcing_separation)
    assert forcing_mass > 0 and rho > 0
    negative, nnegative = certify_bad_region(law, left, right, width, True)
    short, nshort = certify_bad_region(law, left, right, width, False)
    ceiling = max(negative[0], short[0])
    assert ceiling < reference
    gap = reference-ceiling
    d0 = gap/2
    # NEGATIVE_M2_SHIFT.md, section 6: these four rational law weights
    # prove strict improvement relative to the (uncomputed) original S.
    assert 0 < law.w0 and 0 < forcing_mass < 1
    eta = Q(data['shift_eta'])
    htotal = law.primitive('h', 1)
    hmax = max(law.density['h'])
    D, E = forcing_separation/2, 3+forcing_separation/2
    L0 = law.w0*width/7
    omega = L0/(2*E)
    assert 0 < eta < 1-right and eta*htotal < omega*D
    constants = (Q(4, 7)+4*hmax/(margin*eta), L0/d0, 2*omega/forcing_mass)
    cstar = max(constants)
    unnormalized = {
        'M': cstar/2-omega/forcing_mass,
        'M_rest': omega*(1-forcing_mass)/forcing_mass,
        'F_r': omega,
        'M_eta': Q(1),
    }
    assert all(x >= 0 for x in unnormalized.values())
    mixture_total = 1+cstar/2
    assert sum(unnormalized.values()) == mixture_total
    mixture = {name: str(weight/mixture_total) for name, weight in unnormalized.items()}
    decrease = (omega*D-eta*htotal)/mixture_total
    assert decrease > 0
    result = {
        'normalization': str(law.normalization),
        'endpoint_mass': str(law.w0),
        'reference_tuple': list(map(str, witness)),
        'reference_payoff': str(reference),
        'negative_c_maximum': str(negative[0]),
        'negative_c_maximizer': list(map(str, negative[1])),
        'negative_c_closed_cells': nnegative,
        'short_suffix_maximum': str(short[0]),
        'short_suffix_maximizer': list(map(str, short[1])),
        'short_suffix_closed_cells': nshort,
        'bad_region_ceiling': str(ceiling),
        'reference_minus_bad_ceiling': str(gap),
        'local_near_optimality_threshold': str(d0),
        'tail_density_margin': str(margin),
        'forcing_mass': str(forcing_mass),
        'forcing_rho': str(rho),
        'shift_eta': str(eta),
        'h_total': str(htotal),
        'h_maximum': str(hmax),
        'mixture_L0': str(L0),
        'mixture_omega': str(omega),
        'mixture_Cstar_candidates': list(map(str, constants)),
        'mixture_Cstar': str(cstar),
        'mixture_total': str(mixture_total),
        'normalized_improving_mixture': mixture,
        'guaranteed_decrease_from_original_S': str(decrease),
    }
    if 'expected' in data:
        assert data['expected'] == result
    return result


def main():
    data = json.loads(Path(__file__).with_name('local_gap_certificate.json').read_text())
    result = verify(data)
    print(json.dumps(result, indent=2))
    print('PASS: exact normalized nonnegative densities and all three monotonicities')
    print('PASS: every closed-domain scalar tuple in I with c<=0 or y-c<=1/16 is below the legal reference payoff')
    print('PASS: explicit rational four-law mixture has a strictly smaller ceiling than the original law')
    print('Scope: local exclusion for this fixed signed-density law; no exact game value is claimed')


if __name__ == '__main__':
    main()
