"""Construct a dyadic law while retaining all light-coordinate orders.

One strictly order-preserving map is applied to every U and V coordinate.
It commutes with reflection and integer translation, retaining initial
times, endpoint contacts, common characteristics and unit-speed legs.
Its response is not inferred from the source: rerun the unrestricted oracle.
Independent rounding of turn positions can destroy common characteristics
and was observed to worsen a response by 0.008 despite a tiny perturbation.
"""
from __future__ import annotations
import argparse
from fractions import Fraction as Q
import json
from pathlib import Path
from efficient_union import canonical


def convert(source, bankfile, prefix, bits=24):
    data = json.loads(source.read_text())
    bank = json.loads(bankfile.read_text())
    assert len(data['weights']) == len(bank['atoms'])
    denominator = 2**bits
    assert bits >= 1
    coordinates = {Q(q) for atom in bank['atoms'] for p in atom['exact_light'] for q in p}
    radii = {Q(0), Q(1, 2)}
    for q in coordinates:
        r = q-q.numerator//q.denominator
        radii.add(min(r, 1-r))
    radii = sorted(radii)
    assert len(radii) <= denominator//2+1
    mapped, previous = {}, -1
    for i, r in enumerate(radii):
        v = min(max(round(r*denominator), previous+1), denominator//2-(len(radii)-1-i))
        mapped[r] = Q(v, denominator)
        previous = v

    def transform(q):
        n = q.numerator//q.denominator
        r = q-n
        return n+(mapped[r] if r <= Q(1, 2) else 1-mapped[1-r])

    ordered = sorted(coordinates)
    assert all(transform(a) < transform(b) for a, b in zip(ordered, ordered[1:]))
    assert all(transform(-q) == -transform(q) and transform(q+2) == transform(q)+2 for q in coordinates)
    atoms, error = [], Q(0)
    for atom in bank['atoms']:
        old = [(Q(u), Q(v)) for u, v in atom['exact_light']]
        route = [(transform(u), transform(v)) for u, v in old]
        for (u, v), (a, b) in zip(old, route):
            error = max(error, abs((a+b-u-v)/2), abs((a-b-u+v)/2))
        key = canonical(route)
        atoms.append(dict(kind='PATH', parameters=sum((list(p) for p in key), []),
                          exact_light=[list(p) for p in key],
                          light=[[float(Q(u)), float(Q(v))] for u, v in key]))
    summary = dict(scope='New legal finite monster law; recompute its unrestricted response.',
                   source=source.name, source_bank=bankfile.name, dyadic_bits=bits,
                   coordinate_rule='Common strictly increasing reflection/translation-equivariant map on light coordinates.',
                   common_coordinate_orders_verified=True, coordinates=len(coordinates),
                   maximum_vertex_change=str(error), pairs=len(atoms))
    prefix.with_suffix('.bank.json').write_text(json.dumps(dict(atoms=atoms), separators=(',', ':'))+'\n')
    prefix.with_suffix('.law.json').write_text(json.dumps({**summary,
        'atoms': [dict(kind=a['kind'], parameters=a['parameters']) for a in atoms],
        'weights': data['weights']}, separators=(',', ':'))+'\n')
    return summary


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('source', type=Path)
    p.add_argument('bank', type=Path)
    p.add_argument('prefix', type=Path)
    p.add_argument('--bits', type=int, default=24)
    args = p.parse_args()
    print(json.dumps(convert(args.source, args.bank, args.prefix, args.bits), indent=2))
