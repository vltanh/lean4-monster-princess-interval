#!/usr/bin/env python3
"""Exact endpoint-sweep charts for a common-threshold Qout CDF.

The output is B(t,L)=integral_0^2 min(L,F(t+u,1-u))du on
0<=t<=2, 0<=L<=1.  It is a tail component, not a security certificate.
Only Python's standard library and Fraction are used.
"""
from fractions import Fraction as Q
from pathlib import Path
import argparse
import base64
import gzip
import hashlib
import json
import re
import struct
import zlib

ZERO = (Q(0),) * 6


def integer(value):
    if type(value) is int:
        return value
    if isinstance(value, str) and re.fullmatch(r'[+-]?[0-9]+', value):
        return int(value)
    raise ValueError('exact integer input required')


def field_denominator(data):
    """Read either public denominator spelling, rejecting conflicting copies."""
    values = [integer(data[key]) for key in ('field_denominator', 'cdf_denominator')
              if key in data]
    if not values or any(value != values[0] for value in values[1:]):
        raise ValueError('missing or inconsistent field denominator')
    return values[0]


def unwrap_field_data(data):
    """Accept an explicit strategy wrapper without importing its security claim.

    The caller's epsilon remains authoritative: chart construction may ask
    for a different interpolation width from the saved strategy.  Only its
    validated nodal profile, with consistent scale metadata, is reused.
    """
    if not isinstance(data, dict):
        raise ValueError('field input must be a JSON object')
    if data.get('format') != 'normalized-qout-princess-p1-v1':
        return data
    profile = data.get('nodal_profile')
    if not isinstance(profile, dict):
        raise ValueError('normalized strategy needs a nodal_profile object')
    if profile.get('format') == 'normalized-qout-princess-p1-v1':
        raise ValueError('nested strategy wrappers are not nodal profiles')
    if integer(data['n']) != integer(profile['n']):
        raise ValueError('strategy and nodal profile grid sizes differ')
    if field_denominator(data) != field_denominator(profile):
        raise ValueError('strategy and nodal profile denominators differ')
    return profile


def add(*vectors):
    return tuple(sum(entries, Q(0)) for entries in zip(*vectors))


def scale(vector, scalar):
    return tuple(scalar*x for x in vector)


def product(a, b):
    """Multiply affine forms in (t,L), in the documented six-term basis."""
    return (a[0]*b[0], a[0]*b[1]+a[1]*b[0],
            a[0]*b[2]+a[2]*b[0], a[1]*b[1],
            a[1]*b[2]+a[2]*b[1], a[2]*b[2])


def evaluate(poly, t, ell):
    return sum(a*b for a, b in zip(poly, (1, t, ell, t*t, t*ell, ell*ell)))


def affine(line, t):
    return line[0]+line[1]*t


def unique_cycle(points):
    out = []
    for point in points:
        if not out or point != out[-1]:
            out.append(point)
    if len(out)>1 and out[0] == out[-1]:
        out.pop()
    return out


def clip_polygon(points, inequality):
    if not points:
        return []
    a, b, c = inequality
    out = []
    for p, q in zip(points, points[1:]+points[:1]):
        sp = a*p[0]+b*p[1]-c
        sq = a*q[0]+b*q[1]-c
        if sp <= 0:
            out.append(p)
        if (sp < 0 < sq) or (sq < 0 < sp):
            z = sp/(sp-sq)
            out.append((p[0]+z*(q[0]-p[0]), p[1]+z*(q[1]-p[1])))
    return unique_cycle(out)


class Field:
    def __init__(self, data, epsilon=Q(1, 2)):
        data = unwrap_field_data(data)
        self.n = integer(data['n'])
        self.den = field_denominator(data)
        assert self.n > 0 and self.den > 0
        self.epsilon = Q(epsilon)
        assert 0 < self.epsilon <= Q(1, 2)
        self.a, self.b = Q(1, 2)-self.epsilon, Q(1, 2)+self.epsilon
        self.width = self.b-self.a
        self.R, self.C = 2*self.n, 4*self.n
        self.pre = {}
        if data.get('format') == 'qout-clock-grid-field-u32-zlib-v1':
            raw = zlib.decompress(base64.b64decode(data['pre_two_values_base64']))
            count = (self.C+1)*self.n
            assert data['encoding']['count'] == count and len(raw) == 4*count
            assert data['encoding']['integer_type'] == 'uint32 little-endian'
            assert data['encoding']['compression'] == 'zlib'
            assert hashlib.sha256(raw).hexdigest() == data['encoding']['uncompressed_sha256']
            values = struct.unpack('<'+'I'*count, raw)
            for j in range(self.C+1):
                for k in range(1, self.R+1):
                    if (j+k)%2 == 0:
                        self.pre[j, k] = int(values[j*self.n+(k-1)//2])
        else:
            for j, k, value in data.get('radial_nodes', data.get('radial_nodal', [])):
                j, k, value = integer(j), integer(k), integer(value)
                assert j >= 0 and 0 <= k <= self.R and (j+k)%2 == 0
                if k == 0:
                    assert value == 0
                if 0 <= j <= self.C and k > 0:
                    assert (j, k) not in self.pre
                    self.pre[j, k] = value
        expected = {(j, k) for j in range(self.C+1) for k in range(1, self.R+1) if (j+k)%2 == 0}
        assert set(self.pre) == expected
        self.cone_checks = 0
        for (j, k), value in self.pre.items():
            assert 0 <= value <= self.den
            if k < self.R:
                for dt in (-1, 1):
                    if 0 <= j+dt <= self.C:
                        assert value <= self.pre[j+dt, k+1]
                        self.cone_checks += 1
        for j in range(0, self.C, 2):
            assert self.pre[j+2, self.R] <= self.pre[j, self.R]

    def gnum(self, j, k):
        assert j >= 0 and 0 <= k <= self.R and (j+k)%2 == 0
        if k == 0:
            return 0
        if j > self.C:
            k -= j-self.C
            j = self.C
        return 0 if k <= 0 else self.pre[j, k]

    def nodal(self, i, k):
        time, position = i+k, i-k
        g = self.gnum(time, abs(position))
        return Q(self.den+(1 if position>0 else -1 if position<0 else 0)*g, 2*self.den)

    def orientation(self, index):
        return index%(2*self.n) < self.n

    def cdf(self, time, position):
        """Independent direct averaging over the common threshold Z."""
        coords = (self.n*(time+position), self.n*(time-position))
        indices = [x.numerator//x.denominator for x in coords]
        fractions = [x-i for x, i in zip(coords, indices)]
        cuts = {self.a, self.b}
        for i, alpha in zip(indices, fractions):
            threshold = alpha if self.orientation(i) else 1-alpha
            if self.a < threshold < self.b:
                cuts.add(threshold)
        cuts = sorted(cuts)
        answer = Q(0)
        for lo, hi in zip(cuts, cuts[1:]):
            z = (lo+hi)/2
            rounded = [i+int(alpha > (z if self.orientation(i) else 1-z))
                       for i, alpha in zip(indices, fractions)]
            answer += (hi-lo)/self.width*self.nodal(*rounded)
        return answer

    def bands(self):
        points = {Q(0), Q(2)}
        for i in range(self.n, 3*self.n):
            for offset in (Q(0), self.a, self.b, Q(1)):
                points.add((i+offset)/self.n-1)
        return sorted(t for t in points if 0 <= t <= 2)

    def trace_plane(self, t, u):
        """Return A+B*t+C*u for the affine trace cell containing (t,u)."""
        n = self.n
        U, W = t+1, t-1+2*u
        iu = (n*U).numerator//(n*U).denominator
        iw = (n*W).numerator//(n*W).denominator
        alpha_u, alpha_w = n*U-iu, n*W-iw

        def clamped_form(alpha, form):
            if alpha <= self.a:
                return (Q(0), Q(0), Q(0))
            if alpha >= self.b:
                return (Q(1), Q(0), Q(0))
            return ((form[0]-self.a)/self.width, form[1]/self.width, form[2]/self.width)

        qu = clamped_form(alpha_u, (Q(n-iu), Q(n), Q(0)))
        qw = clamped_form(alpha_w, (Q(-n-iw), Q(n), Q(2*n)))
        one, zero = (Q(1), Q(0), Q(0)), (Q(0), Q(0), Q(0))
        vu, vw = qu[0]+qu[1]*t+qu[2]*u, qw[0]+qw[1]*t+qw[2]*u
        if self.orientation(iu) == self.orientation(iw):
            if vu >= vw:
                weights = (add(one, scale(qu, -1)), add(qu, scale(qw, -1)), zero, qw)
            else:
                weights = (add(one, scale(qw, -1)), zero, add(qw, scale(qu, -1)), qu)
        elif vu+vw <= 1:
            weights = (add(one, scale(qu, -1), scale(qw, -1)), qu, qw, zero)
        else:
            weights = (zero, add(one, scale(qw, -1)), add(one, scale(qu, -1)), add(qu, qw, scale(one, -1)))
        plane = zero
        for weight, (du, dw) in zip(weights, ((0, 0), (1, 0), (0, 1), (1, 1))):
            if any(weight):
                plane = add(plane, scale(weight, self.nodal(iu+du, iw+dw)))
        assert plane[2] <= 0
        assert plane[0]+plane[1]*t+plane[2]*u == self.cdf(t+u, 1-u)
        return plane

    def segments(self, lo, hi):
        middle = (lo+hi)/2
        n = self.n
        iu = (n*(middle+1)).numerator//(n*(middle+1)).denominator
        lines = {(Q(0), Q(0)), (Q(2), Q(0))}
        for iw in range(iu-2*n-1, iu+2*n+2):
            for offset in (Q(0), self.a, self.b, Q(1)):
                lines.add(((Q(iw)+offset)/n/2+Q(1, 2), Q(-1, 2)))
            if self.orientation(iu) == self.orientation(iw):
                lines.add((1+Q(iw-iu, 2*n), Q(0)))
            else:
                lines.add((Q(iu+iw+1, 2*n), Q(-1)))
        lines = sorted((line for line in lines if 0 <= affine(line, middle) <= 2), key=lambda line: affine(line, middle))
        for first, second in zip(lines, lines[1:]):
            assert affine(first, middle) < affine(second, middle)
            assert affine(first, lo) <= affine(second, lo) and affine(first, hi) <= affine(second, hi)
        assert lines[0] == (0, 0) and lines[-1] == (2, 0)
        result = []
        for start, end in zip(lines, lines[1:]):
            u = (affine(start, middle)+affine(end, middle))/2
            plane = self.trace_plane(middle, u)
            A, B, C = plane
            for t in (lo, middle, hi):
                for at in (affine(start, t), affine(end, t)):
                    assert A+B*t+C*at == self.cdf(t+at, 1-at)
            result.append((start, end, plane))
        return result

    def direct_tail(self, t, ell):
        """Independent chronological integration at one exact query."""
        n = self.n
        fixed = n*(t+1)
        alpha = fixed-fixed.numerator//fixed.denominator
        cuts = {Q(0), Q(2)}
        first = (n*(t-1)).numerator//(n*(t-1)).denominator
        last = (n*(t+3)).numerator//(n*(t+3)).denominator
        for k in range(first-1, last+2):
            for f in (Q(0), self.a, self.b, alpha, 1-alpha, Q(1)):
                u = ((Q(k)+f)/n-t+1)/2
                if 0 < u < 2:
                    cuts.add(u)
        cuts = sorted(cuts)
        total = Q(0)
        for a, b in zip(cuts, cuts[1:]):
            fa, fb = self.cdf(t+a, 1-a), self.cdf(t+b, 1-b)
            assert fa >= fb
            assert self.cdf(t+(a+b)/2, 1-(a+b)/2) == (fa+fb)/2
            if ell <= fb:
                total += (b-a)*ell
            elif ell >= fa:
                total += (b-a)*(fa+fb)/2
            else:
                z = (fa-ell)/(fa-fb)
                total += (b-a)*(ell*z+(ell+fb)*(1-z)/2)
        return total


def segment_integral(segment):
    start, end, (A, B, C) = segment
    a, b, q = (*start, Q(0)), (*end, Q(0)), (A, B, Q(0))
    return add(product(q, add(b, scale(a, -1))), scale(add(product(b, b), scale(product(a, a), -1)), C/2))


def build(field, direct_replay=False):
    charts, band_data = [], []
    direct_checks = 0
    bands = field.bands()
    for band_id, (lo, hi) in enumerate(zip(bands, bands[1:])):
        segments = field.segments(lo, hi)
        band_data.append({'t_interval': [lo, hi], 'segments': [
            {'u_start': a, 'u_end': b, 'cdf': plane} for a, b, plane in segments]})
        future = [ZERO]*(len(segments)+1)
        for i in range(len(segments)-1, -1, -1):
            future[i] = add(segment_integral(segments[i]), future[i+1])

        def emit(kind, cross, poly, extra):
            nonlocal direct_checks
            inequalities = [(Q(-1), Q(0), -lo), (Q(1), Q(0), hi),
                            (Q(0), Q(-1), Q(0)), (Q(0), Q(1), Q(1)), *extra]
            vertices = [(lo, Q(0)), (hi, Q(0)), (hi, Q(1)), (lo, Q(1))]
            for inequality in inequalities:
                vertices = clip_polygon(vertices, inequality)
            if not vertices:
                return
            chart = {'band': band_id, 't_interval': [lo, hi], 'kind': kind,
                     'crossing_segment': cross, 'inequalities': inequalities,
                     'coefficients': poly, 'vertices': vertices}
            if direct_replay:
                points = [*vertices,
                          *[((p[0]+q[0])/2, (p[1]+q[1])/2)
                            for p, q in zip(vertices, vertices[1:]+vertices[:1])],
                          (sum(t for t, ell in vertices)/len(vertices),
                           sum(ell for t, ell in vertices)/len(vertices))]
                for t, ell in points:
                    assert evaluate(poly, t, ell) == field.direct_tail(t, ell)
                    direct_checks += 1
            charts.append(chart)

        first_start, _, (A, B, C) = segments[0]
        top = (A+C*first_start[0], B+C*first_start[1])
        _, last_end, (A, B, C) = segments[-1]
        bottom = (A+C*last_end[0], B+C*last_end[1])
        emit('below_trace', None, (Q(0), Q(0), Q(2), Q(0), Q(0), Q(0)),
             [(-bottom[1], Q(1), bottom[0])])
        emit('above_trace', None, future[0], [(top[1], Q(-1), -top[0])])
        for i, (start, end, (A, B, C)) in enumerate(segments):
            if C == 0:
                continue
            q, b, diff = (A, B, Q(0)), (*end, Q(0)), (-A, -B, Q(1))
            poly = add(future[i+1], product(q, b), scale(product(b, b), C/2), scale(product(diff, diff), 1/(2*C)))
            fa = (A+C*start[0], B+C*start[1])
            fb = (A+C*end[0], B+C*end[1])
            emit('crossing', i, poly, [(-fa[1], Q(1), fa[0]), (fb[1], Q(-1), -fb[0])])
    return {'format': 'endpoint-tail-charts-v1',
            'scope': 'Exact endpoint-sweep component B(t,L); no standalone lower or optimality claim.',
            'n': field.n, 'epsilon': field.epsilon,
            'domain': {'t': [Q(0), Q(2)], 'L': [Q(0), Q(1)]},
            'field_rule': 'Common-threshold interpolation of validated pre-two nodes, with exact Qout extension after two.',
            'polynomial_basis': ['1', 't', 'L', 't^2', 't*L', 'L^2'],
            'inequality_convention': 'A*t+B*L <= C',
            'bands': band_data, 'charts': charts,
            'replay': {'status': 'PASS', 'pre_two_nodes': len(field.pre),
                       'cone_checks': field.cone_checks, 'time_bands': len(band_data),
                       'charts': len(charts), 'direct_integral_checks': direct_checks}}


def encode(value):
    if isinstance(value, Q):
        return str(value)
    raise TypeError(type(value).__name__)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('field')
    parser.add_argument('output')
    parser.add_argument('--epsilon', default='1/2')
    parser.add_argument('--direct-replay', action='store_true')
    args = parser.parse_args()
    raw = Path(args.field).read_bytes()
    data = json.loads(gzip.decompress(raw) if raw[:2] == b'\x1f\x8b' else raw)
    field = Field(data, Q(args.epsilon))
    out = build(field, args.direct_replay)
    out['source_sha256'] = hashlib.sha256(raw).hexdigest()
    text = json.dumps(out, default=encode, indent=2)+'\n'
    Path(args.output).write_text(text)
    print(json.dumps(out['replay'], indent=2))


if __name__ == '__main__':
    main()
