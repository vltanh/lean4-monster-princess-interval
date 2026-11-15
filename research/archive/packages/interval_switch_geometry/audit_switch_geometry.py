#!/usr/bin/env python3
"""Exact switch-geometry audit, physical ablation, and contact discontinuity.

The original physical upper is an already certified dependency; this script
checks its source bytes and physical paths, not its max-flow certificate.
The ablation tests do NOT exclude arbitrary reweightings of whole families.
Uses only the Python standard library, with Fraction for every payoff.
"""
from __future__ import annotations
import argparse
from collections import Counter, defaultdict
from fractions import Fraction as Q
import gzip
import hashlib
from itertools import groupby
import json
from pathlib import Path

SOURCE_SHA = '5c736b0c6ef59b418cce0e2e2ef24b0a8dbe4d017a6eca7578d9e1c79616b31d'
UPPER = Q(291849329389899, 204800000000000)
CORE = {'sweep', 'endpoint_first', 'one_interior_turn_t2'}


def collision_segments(m, p):
    """Chronological affine intersection of pairs of physical segments."""
    for (ta, x), (tb, y) in zip(m, m[1:]):
        vm = (y-x)/(tb-ta); cm = x-vm*ta
        for (pa, a), (pb, b) in zip(p, p[1:]):
            lo, hi = max(ta, pa), min(tb, pb)
            if lo > hi:
                continue
            vp = (b-a)/(pb-pa); cp = a-vp*pa
            if vm == vp:
                if cm == cp:
                    return lo
            else:
                t = (cp-cm)/(vm-vp)
                if lo <= t <= hi:
                    return t
    raise AssertionError('uncaptured Princess')


def position(path, t):
    for (ta, a), (tb, b) in zip(path, path[1:]):
        if ta <= t <= tb:
            return a+(b-a)*(t-ta)/(tb-ta)
    raise AssertionError('time outside route')


def collision_knots(m, p):
    """Independent merged-time partition, using signs of relative position."""
    times = sorted({t for t, x in m+p})
    old = None
    for t in times:
        d = position(m, t)-position(p, t)
        if d == 0:
            return t
        if old is not None and old[1]*d < 0:
            return old[0]+(t-old[0])*old[1]/(old[1]-d)
        old = (t, d)
    raise AssertionError('uncaptured Princess')


def legal(path):
    assert path[0][0] == 0
    assert all(-1 <= x <= 1 for _, x in path)
    assert all(tb > ta and abs(b-a) <= tb-ta
               for (ta, a), (tb, b) in zip(path, path[1:]))


def pair_score(m, p):
    legal(m); legal(p)
    result = Q(0)
    for sign in (-1, 1):
        reflected = [(t, sign*x) for t, x in m]
        t = collision_segments(reflected, p)
        assert t == collision_knots(reflected, p)
        result += t/2
    return result


def princess(eps):
    return [(Q(0), eps), (Q(1), eps), (2-eps, Q(1)), (Q(8), Q(1))]


def principal(a, b):
    return [(Q(0), a), ((b-a)/2, (a+b)/2),
            (b+1, Q(-1)), (b+3, Q(1)), (Q(8), Q(1))]


def formula(eps, b):
    if b <= 1-eps:
        return b
    if b <= 1+eps:
        return b+(1-eps)/2
    return 3*(b+1)/4-eps/4


def timing_checks():
    cases = 0
    for eps in (Q(1, 16), Q(1, 64), Q(1, 65536)):
        for a in (Q(1, 8), Q(3, 8), Q(1, 2), Q(3, 4)):
            for b in (Q(3, 4), 1-2*eps, 1-eps, 1-eps/2,
                      Q(1), 1+eps/2, 1+eps, 1+2*eps, Q(5, 4)):
                if eps < a < b < 2-a:
                    assert pair_score(principal(a, b), princess(eps)) == formula(eps, b)
                    cases += 1
    eps = Q(1, 65536); a = Q(1, 2)
    early, normal = principal(a, 1-2*eps), principal(a, Q(1))
    knots = sorted({t for t, x in early+normal})
    distance = max(abs(position(early, t)-position(normal, t)) for t in knots)
    assert distance == 2*eps
    x, y = pair_score(early, princess(eps)), pair_score(normal, princess(eps))
    assert y-x == Q(1, 2)+3*eps/2
    return {'fraction_regressions': cases, 'epsilon': str(eps),
            'uniform_path_distance': str(distance),
            'early_switch_payoff': str(x), 'on_front_payoff': str(y),
            'payoff_difference': str(y-x)}


def load_routes(path):
    raw = path.read_bytes()
    if raw[:2] == b'\x1f\x8b':
        raw = gzip.decompress(raw)
    assert hashlib.sha256(raw).hexdigest() == SOURCE_SHA
    law = json.loads(raw)
    assert Q(law['global_upper']) == UPPER and law['pair_law'] == 'fair_reflection'
    R, D = 2*law['n'], int(law['weight_denominator'])
    merged = defaultdict(int)
    for entry in law['paths']:
        a, moves = entry['start_grid'], tuple(entry['moves'])
        assert all(s in (-1, 1) for s in moves)
        x = a
        assert -R <= x <= R
        for s in moves:
            x += s
            assert -R <= x <= R
        if a < 0 or (a == 0 and moves[0] < 0):
            a, moves = -a, tuple(-s for s in moves)
        merged[a, moves] += int(entry['weight_numerator'])
    assert sum(merged.values()) == D
    rows = []
    for (a, moves), w in merged.items():
        legs = [(s, len(tuple(part))) for s, part in groupby(moves)]
        t, x = 0, a; pts = [(t, x)]
        for s, count in legs:
            t += count; x += s*count; pts.append((t, x))
        if len(legs) == 1:
            assert abs(a) == R and pts[-1][1] == -a
            kind = 'sweep'
        else:
            endpoint = next(i for i, (t, x) in enumerate(pts) if abs(x) == R)
            assert endpoint == len(pts)-2
            assert pts[-1][0]-pts[-2][0] == 2*R
            assert pts[-1][1] == -pts[-2][1]
            if len(legs) == 2:
                kind = 'endpoint_first'
                assert legs[0][1] == R-legs[0][0]*a
            elif len(legs) == 3:
                kind = 'one_interior_turn_t2' if pts[2][0] == 2*R else 'one_interior_turn_off_t2'
                if kind == 'one_interior_turn_t2':
                    assert 2*legs[0][1] == R-legs[0][0]*a
            else:
                kind = f'{len(legs)-2}_interior_turns'
        route = [(Q(t, R), Q(x, R)) for t, x in pts]
        route.append((Q(8), route[-1][1]))
        legal(route)
        rows.append({'weight': w, 'kind': kind, 'route': route})
    return rows, D, len(law['paths'])


def audit(path):
    rows, D, plans = load_routes(path)
    count, mass = Counter(), Counter()
    for r in rows:
        count[r['kind']] += 1; mass[r['kind']] += r['weight']
    assert len(rows) == 752 and plans == 770
    assert sum(mass[k] for k in CORE) == 987707900672
    eps = Q(1, 65536); p = princess(eps)
    scores = [pair_score(r['route'], p) for r in rows]
    cases = {
        'original': lambda r: True,
        'three_families_renormalized': lambda r: r['kind'] in CORE,
        'remove_off_schedule_only': lambda r: r['kind'] != 'one_interior_turn_off_t2',
        'remove_extra_turns_only': lambda r: r['kind'] in CORE | {'one_interior_turn_off_t2'}}
    outcomes = {}
    for name, keep in cases.items():
        W = sum(r['weight'] for r in rows if keep(r))
        J = sum(r['weight']*s for r, s in zip(rows, scores) if keep(r))/W
        outcomes[name] = {'retained_mass': str(Q(W, D)), 'exact_payoff': str(J),
                          'decimal': float(J), 'exceeds_original_upper': J > UPPER}
    assert Q(outcomes['original']['exact_payoff']) == Q(373447515557123123, 262144000000000000)
    assert Q(outcomes['three_families_renormalized']['exact_payoff']) == Q(370929262655146955, 258921699913760768)
    assert all(outcomes[n]['exceeds_original_upper'] for n in cases if n != 'original')
    deleted = Q(mass['3_interior_turns']+mass['4_interior_turns'], D)
    simplified = UPPER/(1-deleted)
    assert simplified == Q(1459246646949495, 1023896293471232)
    Jcore = Q(outcomes['three_families_renormalized']['exact_payoff'])
    return {
        'status': 'PASS', 'source_uncompressed_sha256': SOURCE_SHA,
        'scope': 'Exact fixed-law decomposition and ablation; no exclusion of all continuous E/P mixtures, no new best unrestricted bound, no Lean formalization.',
        'physical_pairs': len(rows), 'calendar_plans': plans,
        'groups': {k: {'pairs': count[k], 'probability': str(Q(v, D)), 'percent': float(Q(100*v, D))} for k, v in sorted(mass.items())},
        'witness_route': [[str(t), str(x)] for t, x in p],
        'independent_oriented_capture_comparisons': 2*len(rows),
        'outcomes': outcomes, 'timing_discontinuity': timing_checks(),
        'minimum_replacement_of_fixed_core': str(1-UPPER/Jcore),
        'simplified_at_most_two_interior_turns': {
            'pairs': sum(count[k] for k in count if k not in {'3_interior_turns', '4_interior_turns'}),
            'deleted_probability': str(deleted), 'inherited_global_upper': str(simplified),
            'decimal': float(simplified),
            'proof': 'For nonnegative capture time, retaining mass w and renormalizing increases a verified all-Princess upper by at most the factor 1/w.',
            'original_upper_replayed': False}}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    root = Path(__file__).resolve().parents[2]
    parser.add_argument('--certificate', type=Path, default=root/'packages/interval_discovery_certificates/monster_boundary_n256.physical.json.gz')
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    report = audit(args.certificate)
    text = json.dumps(report, indent=2)+'\n'
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text)
    print(text, end='')
