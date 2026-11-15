#!/usr/bin/env python3
"""Standard-library exact checker for the scoped two-parameter ceiling.

The finite chamber arrangement covers every 0<=a<=1, -a<=c<=1.
Boundary capture coincidences can lower the actual payoff; open-chamber
affine extensions therefore give a valid response ceiling on the closure.
"""
from fractions import Fraction as F
from pathlib import Path
import json


def first_A(z, a, c, probe_a, probe_c):
    if z <= probe_a:
        return F(0)
    if z <= probe_c:
        return z
    if z <= probe_c+2:
        return (z+c)/2
    return z-1


def first_B(z, a, c, probe_a, probe_c):
    if z <= -probe_a:
        return F(0)
    if z > probe_c:
        return z+1
    if z >= probe_a:
        return z
    return (z+a)/2


def pair_germ(monster, a, c, probe_a, probe_c):
    """Affine chamber formula, evaluated at a possibly boundary vertex."""
    kind, x = monster['kind'], F(monster['parameter'])
    A = lambda z: first_A(F(z), a, c, probe_a, probe_c)
    B = lambda z: first_B(F(z), a, c, probe_a, probe_c)
    if kind == 'M1':
        positive = B(-x) if x < probe_a else A(2-x)
        negative = A(-x) if x < -probe_a else B(2-x)
    elif kind == 'M2':
        positive = B(3) if x < -probe_c else B(-x) if x < probe_a else A(1)
        negative = A(-x) if x < -probe_a else B(1)
    elif kind == 'early_turn':
        # Starting at zero, turning at (s/2,s/2), then -1 and +1.
        s = x
        assert 0 < s < 1
        positive = a/2 if probe_a <= s and probe_c >= 0 else s+3
        negative = B(s)
    else:
        raise ValueError(kind)
    return (positive+negative)/2


def clip(poly, a_coefficient, c_coefficient, offset=0):
    """Intersect a rational polygon with one closed rational half-plane."""
    out = []
    for p, q in zip(poly, poly[1:]+poly[:1]):
        fp = a_coefficient*p[0]+c_coefficient*p[1]+offset
        fq = a_coefficient*q[0]+c_coefficient*q[1]+offset
        if fp >= 0:
            out.append(p)
        if (fp > 0 > fq) or (fp < 0 < fq):
            ratio = fp/(fp-fq)
            out.append((p[0]+ratio*(q[0]-p[0]), p[1]+ratio*(q[1]-p[1])))
    return list(dict.fromkeys(out))


def cells(monsters):
    a_cuts, c_cuts = {F(0), F(1)}, {F(-1), F(0), F(1)}
    for monster in monsters:
        x = F(monster['parameter'])
        if monster['kind'] in ('M1', 'M2'):
            thresholds = (-x, 2-x, F(1), F(3))
            a_cuts.add(abs(x))
            c_cuts.add(-x)
        else:
            thresholds = (x,)
            a_cuts.add(x)
            c_cuts.add(x)
        for z in thresholds:
            for candidate in (z, -z):
                if 0 <= candidate <= 1:
                    a_cuts.add(candidate)
            for candidate in (z, z-2):
                if -1 <= candidate <= 1:
                    c_cuts.add(candidate)
    a_cuts, c_cuts = sorted(a_cuts), sorted(c_cuts)
    for a0, a1 in zip(a_cuts, a_cuts[1:]):
        for c0, c1 in zip(c_cuts, c_cuts[1:]):
            rectangle = [(a0,c0),(a1,c0),(a1,c1),(a0,c1)]
            for sign in (-1, 1):
                polygon = clip(clip(rectangle, 1, 1), -sign, sign)
                if len(polygon) < 3:
                    continue
                twice_area = sum(p[0]*q[1]-p[1]*q[0]
                                 for p,q in zip(polygon, polygon[1:]+polygon[:1]))
                if twice_area == 0:
                    continue
                probe_a = sum(p[0] for p in polygon)/len(polygon)
                probe_c = sum(p[1] for p in polygon)/len(polygon)
                yield polygon, probe_a, probe_c


def verify(data):
    monsters = data['monsters']
    weights = [F(m['weight']) for m in monsters]
    assert all(w >= 0 for w in weights) and sum(weights) == 1
    maximum, witness = F(0), None
    cell_count = vertex_count = 0
    for polygon, probe_a, probe_c in cells(monsters):
        cell_count += 1
        for a,c in polygon:
            vertex_count += 1
            value = sum(w*pair_germ(m,a,c,probe_a,probe_c)
                        for m,w in zip(monsters,weights))
            if value > maximum:
                maximum, witness = value, (a,c,probe_a,probe_c)
    if 'ceiling' in data:
        assert maximum == F(data['ceiling'])
    lower = F(36290299773897097,25600000000000000)
    return dict(ceiling=str(maximum), decimal=float(maximum), cells=cell_count,
                vertex_limits=vertex_count, witness=[str(x) for x in witness],
                below_known_lower=maximum < lower)


def main():
    data = json.loads((Path(__file__).resolve().parent/'response_ceiling.json').read_text())
    result = verify(data)
    print(json.dumps(result, indent=2))
    print('PASS: exact ceiling for the specified princess family.')
    if not result['below_known_lower']:
        print('EXCLUSION NOT ACHIEVED: the ceiling is above the known unrestricted lower guarantee.')


if __name__ == '__main__':
    main()
