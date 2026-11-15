#!/usr/bin/env python3
"""Construct an exact sparse Qout witness from physical plans or LP weights."""
from collections import defaultdict
from fractions import Fraction
from pathlib import Path
import argparse
import hashlib
import json
import math
import subprocess
import time

from master import plan_column, projected_order, read_json

HERE = Path(__file__).resolve().parent


def make(input_path, prefix, denominator=10**12):
    started = time.monotonic()
    source = read_json(input_path)
    n = source['n']
    if 'paths' in source:
        plans = source['paths']
        denominator = int(source['weight_denominator'])
    else:
        positive = [(i, max(0., float(w))) for i, w in enumerate(source['weights']) if float(w) > 0.]
        total = sum(w for _, w in positive)
        if not total > 0 or not math.isfinite(total):
            raise ValueError('invalid mixture')
        entries = []
        for i, w in positive:
            x = w/total*denominator; q = int(math.floor(x))
            entries.append([i, q, x-q])
        remainder = denominator-sum(e[1] for e in entries)
        if not 0 <= remainder <= len(entries):
            raise ValueError('rounding remainder')
        entries.sort(key=lambda e: (-e[2], e[0]))
        for entry in entries[:remainder]:
            entry[1] += 1
        plans = [dict(source['columns'][i]['plan'], weight_numerator=str(q))
                 for i, q, _ in sorted(entries) if q > 0]
    coeff = defaultdict(int)
    for plan in plans:
        _, column = plan_column(n, plan)
        for point, value in column.items():
            coeff[point] += int(plan['weight_numerator'])*value
    nodes = sorted(point for point, value in coeff.items() if value)
    order = projected_order(n, nodes)
    certificate = dict(scope='Exact physical upper via sparse Qout inequalities, not a restricted-response estimate.',
                       n=n, pair_law='fair_reflection', center_deadline=2, completion_horizon=8,
                       physical_step=f'1/{2*n}', weight_denominator=str(denominator), paths=plans,
                       qout_nodes=[list(point) for point in nodes], qout_order=[list(edge) for edge in order],
                       source_sha256=hashlib.sha256(Path(input_path).read_bytes()).hexdigest())
    prefix = Path(prefix); prefix.parent.mkdir(parents=True, exist_ok=True)
    draft = prefix.with_suffix('.input.json')
    draft.write_text(json.dumps(certificate, separators=(',', ':'))+'\n')
    result = subprocess.run(['node', str(HERE/'sparse_certificate.cjs'), '--solve', str(draft), str(prefix)],
                            check=True, text=True, capture_output=True)
    replay = json.loads(result.stdout)
    replay['construction_seconds'] = time.monotonic()-started
    replay['global_upper_decimal'] = float(Fraction(replay['global_upper']))
    return replay


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', type=Path)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(make(args.input, args.output), indent=2))
