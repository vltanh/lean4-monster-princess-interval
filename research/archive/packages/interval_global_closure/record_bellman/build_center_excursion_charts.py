#!/usr/bin/env python3
"""Exact partial outward-record charts for the center-renewal certificate.

I(t,h,r)=integral_0^h min(r,F(t+s,-s))ds, with t in[0,2], h in[0,1],
r in[0,1/2]. By symmetry the integrand is min(r,1-F(t+s,s)).
At h=1 the reported record is an interior trace; endpoint capture is separate.
"""
from fractions import Fraction as Q
from itertools import combinations
from pathlib import Path
import argparse
import gzip
import hashlib
import json

from build_endpoint_tail_charts import Field, add, scale, affine, encode

ZERO = (Q(0),)*10


def product(a, b):
    return (a[0]*b[0], a[0]*b[1]+a[1]*b[0],
            a[0]*b[2]+a[2]*b[0], a[0]*b[3]+a[3]*b[0],
            a[1]*b[1], a[1]*b[2]+a[2]*b[1],
            a[1]*b[3]+a[3]*b[1], a[2]*b[2],
            a[2]*b[3]+a[3]*b[2], a[3]*b[3])


def value(poly, t, h, r):
    return sum(a*b for a, b in zip(poly, (1, t, h, r, t*t, t*h, t*r, h*h, h*r, r*r)))


def det(a, b, c):
    return (a[0]*(b[1]*c[2]-b[2]*c[1])
            -a[1]*(b[0]*c[2]-b[2]*c[0])
            +a[2]*(b[0]*c[1]-b[1]*c[0]))


def vertices(rows):
    points = set()
    for selection in combinations(rows, 3):
        matrix = [row[:3] for row in selection]
        denominator = det(*matrix)
        if denominator == 0:
            continue
        rhs = [row[3] for row in selection]
        point = []
        for i in range(3):
            replaced = [list(row) for row in matrix]
            for j in range(3):
                replaced[j][i] = rhs[j]
            point.append(det(*replaced)/denominator)
        point = tuple(point)
        if all(sum(a*x for a, x in zip(row[:3], point)) <= row[3] for row in rows):
            points.add(point)
    return sorted(points)


def segments(field, lo, hi):
    middle, n = (lo+hi)/2, field.n
    iu = (n*middle).numerator//(n*middle).denominator
    lines = {(Q(0), Q(0)), (Q(1), Q(0))}
    for iw in range(iu-1, iu+2*n+2):
        for offset in (Q(0), field.a, field.b, Q(1)):
            lines.add(((Q(iw)+offset)/(2*n), Q(-1, 2)))
        if field.orientation(iu) == field.orientation(iw):
            lines.add((Q(iw-iu, 2*n), Q(0)))
        else:
            lines.add((Q(iu+iw+1, 2*n), Q(-1)))
    lines = sorted((line for line in lines if 0 <= affine(line, middle) <= 1), key=lambda line: affine(line, middle))
    assert lines[0] == (0, 0) and lines[-1] == (1, 0)
    result = []
    for a, b in zip(lines, lines[1:]):
        assert affine(a, middle) < affine(b, middle)
        assert affine(a, lo) <= affine(b, lo) and affine(a, hi) <= affine(b, hi)
        s = (affine(a, middle)+affine(b, middle))/2
        # The endpoint-ray parameter substitution is exact:
        # (t_B,u_B)=(t-1,s+1) gives actual time t+s and position -s.
        A, B, C = field.trace_plane(middle-1, s+1)
        plane = (A-B+C, B, C)
        assert plane[2] <= 0
        for t in (lo, middle, hi):
            for at in (affine(a, t), affine(b, t)):
                direct = field.cdf(t+at, -at)
                assert plane[0]+plane[1]*t+plane[2]*at == direct
                assert direct == 1-field.cdf(t+at, at)
        result.append((a, b, plane))
    return result


def full_integral(segment):
    a, b, (A, B, C) = segment
    aa, bb, q = (*a, Q(0), Q(0)), (*b, Q(0), Q(0)), (A, B, Q(0), Q(0))
    return add(product(q, add(bb, scale(aa, -1))),
               scale(add(product(bb, bb), scale(product(aa, aa), -1)), C/2))


def direct_integral(field, t, h, r):
    n = field.n
    fixed = n*t
    alpha = fixed-fixed.numerator//fixed.denominator
    cuts = {Q(0), h}
    first = fixed.numerator//fixed.denominator
    upper = n*(t+2*h)
    last = upper.numerator//upper.denominator
    for k in range(first-1, last+2):
        for f in (Q(0), field.a, field.b, alpha, 1-alpha, Q(1)):
            s = ((Q(k)+f)/n-t)/2
            if 0 < s < h:
                cuts.add(s)
    cuts = sorted(cuts)
    total = Q(0)
    for a, b in zip(cuts, cuts[1:]):
        fa, fb = field.cdf(t+a, -a), field.cdf(t+b, -b)
        assert fa >= fb
        assert field.cdf(t+(a+b)/2, -(a+b)/2) == (fa+fb)/2
        if r <= fb:
            total += (b-a)*r
        elif r >= fa:
            total += (b-a)*(fa+fb)/2
        else:
            z = (fa-r)/(fa-fb)
            total += (b-a)*(r*z+(r+fb)*(1-z)/2)
    return total, min(r, field.cdf(t+h, -h))


def build(field, direct_replay=False):
    out, band_data = [], []
    checks = 0
    times = field.bands()
    # field.bands describes a fixed U=t+1. Period-one band locations give the
    # same knot set for fixed U=t, including both symmetric threshold offsets.
    for band, (lo, hi) in enumerate(zip(times, times[1:])):
        pieces = segments(field, lo, hi)
        band_data.append({'t_interval': [lo, hi], 'segments': [
            {'s_start': a, 's_end': b, 'cdf': p} for a, b, p in pieces]})
        prefix = [ZERO]
        for piece in pieces:
            prefix.append(add(prefix[-1], full_integral(piece)))

        def emit(end, cross, poly, update, extra):
            nonlocal checks
            a, b, _ = pieces[end]
            rows = [(Q(-1), Q(0), Q(0), -lo), (Q(1), Q(0), Q(0), hi),
                    (Q(0), Q(-1), Q(0), Q(0)), (Q(0), Q(1), Q(0), Q(1)),
                    (Q(0), Q(0), Q(-1), Q(0)), (Q(0), Q(0), Q(1), Q(1, 2)),
                    (a[1], Q(-1), Q(0), -a[0]), (-b[1], Q(1), Q(0), b[0]), *extra]
            rows = list(dict.fromkeys(rows))
            points = vertices(rows)
            if not points:
                return
            if direct_replay:
                samples = [*points, *[tuple((a+b)/2 for a, b in zip(p, q)) for p, q in combinations(points, 2)],
                           tuple(sum(p[i] for p in points)/len(points) for i in range(3))]
                for t, h, r in samples:
                    integral, record = direct_integral(field, t, h, r)
                    assert value(poly, t, h, r) == integral
                    assert update[0]+update[1]*t+update[2]*h+update[3]*r == record
                    checks += 1
            out.append({'band': band, 't_interval': [lo, hi], 'ending_segment': end,
                        'crossing_segment': cross, 'inequalities': rows,
                        'coefficients': poly, 'record_update': update, 'vertices': points})

        for j, (start, end, (A, B, C)) in enumerate(pieces):
            emit(j, None, (Q(0), Q(0), Q(0), Q(0), Q(0), Q(0), Q(0), Q(0), Q(1), Q(0)),
                 (Q(0), Q(0), Q(0), Q(1)), [(-B, -C, Q(1), A)])
            qj, h, aj = (A, B, Q(0), Q(0)), (Q(0), Q(0), Q(1), Q(0)), (*start, Q(0), Q(0))
            partial_last = add(product(qj, add(h, scale(aj, -1))),
                               scale(add(product(h, h), scale(product(aj, aj), -1)), C/2))
            for i in range(j+1):
                ai, bi, (AA, BB, CC) = pieces[i]
                if CC == 0:
                    continue
                qi, diff = (AA, BB, Q(0), Q(0)), (-AA, -BB, Q(0), Q(1))
                upper = h if i == j else (*bi, Q(0), Q(0))
                poly = add(product(qi, upper), scale(product(upper, upper), CC/2), scale(product(diff, diff), 1/(2*CC)))
                if i < j:
                    poly = add(poly, add(prefix[j], scale(prefix[i+1], -1)), partial_last)
                fa = (AA+CC*ai[0], BB+CC*ai[1])
                fb = (AA+CC*bi[0], BB+CC*bi[1])
                emit(j, i, poly, (A, B, C, Q(0)),
                     [(-fa[1], Q(0), Q(1), fa[0]),
                      (fb[1], Q(0), Q(-1), -fb[0]),
                      (B, C, Q(-1), -A)])
    return {'format': 'center-excursion-charts-v1',
            'scope': 'Exact partial center-outward integral and interior record update; no standalone security claim.',
            'n': field.n, 'epsilon': field.epsilon,
            'domain': {'t': [Q(0), Q(2)], 'h': [Q(0), Q(1)], 'r': [Q(0), Q(1, 2)]},
            'polynomial_basis': ['1', 't', 'h', 'r', 't^2', 't*h', 't*r', 'h^2', 'h*r', 'r^2'],
            'record_update_basis': ['1', 't', 'h', 'r'],
            'inequality_convention': 'A*t+B*h+C*r <= D',
            'endpoint_note': 'At h=1 record_update is the interior-limit record. A physical endpoint contact resets it to zero and uses the separate direct-tour guard.',
            'bands': band_data, 'charts': out,
            'replay': {'status': 'PASS', 'pre_two_nodes': len(field.pre), 'cone_checks': field.cone_checks,
                       'time_bands': len(band_data), 'charts': len(out), 'direct_integral_and_record_checks': checks}}


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
    Path(args.output).write_text(json.dumps(out, default=encode, indent=2)+'\n')
    print(json.dumps(out['replay'], indent=2))


if __name__ == '__main__':
    main()
