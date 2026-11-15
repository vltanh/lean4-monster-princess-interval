"""Turn the old attached-density candidate into a new finite legal law.

The original conditional response formula is not used.  Every new column is
an actual rational unit-speed route and all probabilities are checked before
normalization.  Mass is moved from the old line routes to midpoint samples of
the continuous sheets.  The mass of each M3 kernel interval is integrated
analytically.  This is a strategy-discovery construction, not a quadrature
error certificate for the original density law.  The finite law must be
checked by the unrestricted survival-cut oracle in its own right.
"""
from __future__ import annotations
import argparse
from collections import defaultdict
from fractions import Fraction as Q
import json
from pathlib import Path
import sys
import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'interval_turn_density'))
from m3_attached_oracle import full_m3_beta_row
from efficient_union import canonical


def m1(x):
    return [(Q(0), x), (1-x, Q(1)), (3-x, Q(-1))]


def m2(z, s):
    return [(Q(0), -z), ((s+z)/2, (s-z)/2), (s+1, Q(-1)), (s+3, Q(1))]


def m3(z, s):
    return [(Q(0), z), ((s-z)/2, (s+z)/2), ((s+1)/2, (s-1)/2),
            (Q(2), Q(1)), (Q(4), Q(-1))]


def construct(source, prefix, starts=128, subdivisions=2):
    data = json.loads(source.read_text())
    knots = [Q(str(x)) for x in data['knots']]
    assert all((x*starts).denominator == 1 for x in knots)
    f, g, k, ell = (data['densities'][name] for name in ('f', 'g', 'k', 'ell'))
    variables = np.r_[data['endpoint_mass'], f, g, k, ell]
    knots_np = np.array(list(map(float, knots)))
    left, right, s0 = (Q(str(data[key])) for key in ('left', 'right', 'turn'))
    weights = defaultdict(float)
    family_mass = defaultdict(float)
    min_residual = float('inf')

    def add(route, mass, family):
        if mass == 0:
            return
        route = [(t, x) for j, (t, x) in enumerate(route)
                 if j == 0 or t != route[j-1][0]]
        assert route[0][0] == 0
        assert all(-1 <= x <= 1 for _, x in route)
        assert all(b-a == abs(y-x) for (a, x), (b, y) in zip(route, route[1:]))
        key = canonical([(t+x, t-x) for t, x in route])
        weights[key] += mass
        family_mass[family] += mass

    def index(x):
        return min(len(knots)-2, max(i for i, a in enumerate(knots) if a <= x))

    def partition(lo, hi):
        cuts = sorted({lo, hi, *(x for x in knots if lo < x < hi),
                       *(2-x for x in knots if lo < 2-x < hi)})
        for a, b in zip(cuts, cuts[1:]):
            for q in range(subdivisions):
                yield a+(b-a)*q/subdivisions, a+(b-a)*(q+1)/subdivisions

    add(m1(Q(-1)), data['endpoint_mass'], 'endpoint')
    for jz in range(starts):
        z = Q(2*jz+1, 2*starts)
        dz = 1/starts
        j = index(z)
        positive, negative = g[j], k[j]-ell[j]
        add(m1(z), f[j]*dz, 'M1_positive')
        add(m1(-z), ell[j]*dz, 'M1_negative')

        def sheet(zparam, lo, hi, coefficient, family):
            if hi <= lo or coefficient == 0:
                return 0.
            for a, b in partition(lo, hi):
                add(m2(zparam, (a+b)/2), coefficient*float(b-a)*dz, family)
            return coefficient*float(hi-lo)

        # Negative early sheet, including the full attached-M3 cross price.
        if left <= z <= right:
            price = float(full_m3_beta_row(float(z), knots_np) @ variables)
            coefficient = (k[index(s0)]-k[j]-price)/float(s0+6-z)
            negative -= sheet(z, s0, Q(1), coefficient, 'M2_negative_early')
            for h in range(1, len(knots)-1):
                r = knots[h]
                if r > s0:
                    coefficient = (k[h]-k[h-1])/float(r+6-z)
                    negative -= sheet(z, r, Q(1), coefficient, 'M2_negative_early')

        # Negative late sheet with its affine top edge.
        v0, v1 = map(lambda x: Q(str(x)), data['affine_profile'][j])
        v = v0+v1*z
        if v > 1:
            coefficient = (f[index(2-v)]-ell[j])/float(v+6-z)
            negative -= sheet(z, Q(1), v, coefficient, 'M2_negative_late')
            for h in range(1, len(knots)-1):
                r = 2-knots[h]
                if 1 < r < v:
                    coefficient = (f[h]-f[h-1])/float(r+6-z)
                    negative -= sheet(z, Q(1), r, coefficient, 'M2_negative_late')

        # Positive late sheet.
        v = Q(str(data['positive_profile'][j]))
        if v > 1:
            coefficient = (f[index(2-v)]-f[j])/float(v+6+z)
            positive -= sheet(-z, Q(1), v, coefficient, 'M2_positive_late')
            for h in range(1, len(knots)-1):
                r = 2-knots[h]
                if 1 < r < v:
                    coefficient = (f[h]-f[h-1])/float(r+6+z)
                    positive -= sheet(-z, Q(1), r, coefficient, 'M2_positive_late')

        # The two M3 attachments move line mass without changing start mass.
        if 0 <= z < Q(1, 8):
            for sign in (1, -1):
                moved = 0.
                base = f[j]+g[j] if sign == 1 else k[j]
                generators = [(Q(1, 4), k[index(Q(1, 4))]-base)]
                generators += [(knots[h], k[h]-k[h-1])
                               for h in range(1, len(knots)-1) if knots[h] > Q(1, 4)]
                for r, coefficient in generators:
                    for a, b in partition(r, Q(1)):
                        # Integral (4+sign*z-r)/(4+sign*z-s)^2 ds.
                        integral = (4+sign*z-r)*(1/(4+sign*z-b)-1/(4+sign*z-a))
                        mass = coefficient*float(integral)
                        add(m3(sign*z, (a+b)/2), mass*dz, 'M3')
                        moved += mass
                if sign == 1:
                    positive -= moved
                else:
                    negative -= moved
        min_residual = min(min_residual, positive, negative)
        assert min(positive, negative) >= -2e-12, (z, positive, negative)
        add(m2(-z, Q(1)), max(0., positive)*dz, 'M2_positive_line')
        add(m2(z, Q(1)), max(0., negative)*dz, 'M2_negative_line')

    assert min(weights.values()) >= -2e-12
    weights = {key: value for key, value in weights.items() if value > 1e-16}
    mass = sum(weights.values())
    assert abs(mass-1) < 1e-9, mass
    atoms = [dict(kind='PATH', parameters=sum((list(p) for p in key), []),
                  exact_light=[list(p) for p in key],
                  light=[[float(Q(u)), float(Q(v))] for u, v in key]) for key in weights]
    summary = dict(scope='New normalized finite rational-route law; unrestricted response required.',
                   source=str(source.relative_to(HERE.parent.parent)), pairs=len(atoms),
                   start_bins=starts, turn_subdivisions=subdivisions,
                   original_numerical_response=data['response'], raw_mass=mass,
                   minimum_line_residual=min_residual, family_mass=dict(family_mass))
    prefix.with_suffix('.bank.json').write_text(json.dumps(dict(atoms=atoms), separators=(',', ':'))+'\n')
    prefix.with_suffix('.law.json').write_text(json.dumps({**summary,
        'atoms': [dict(kind=a['kind'], parameters=a['parameters']) for a in atoms],
        'weights': [v/mass for v in weights.values()]}, separators=(',', ':'))+'\n')
    return summary


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', type=Path, default=HERE.parent/'interval_turn_density/m3_attached_settled.json')
    parser.add_argument('--prefix', type=Path, default=HERE/'efficient_density128')
    parser.add_argument('--starts', type=int, default=128)
    parser.add_argument('--subdivisions', type=int, default=2)
    args = parser.parse_args()
    print(json.dumps(construct(args.source, args.prefix, args.starts, args.subdivisions), indent=2))
