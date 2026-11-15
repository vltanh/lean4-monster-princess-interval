#!/usr/bin/env python3
"""Rebuild and independently verify the saved physical one-turn upper.

Input probabilities, physical moves and selected clocks are all exact integers.
Graph generation and native maximum flow are untrusted proposal steps. Existing
JavaScript BigInt verification and a separate Python integer replay check the
result. No numerical LP or discovery checkpoint is needed.
"""
from __future__ import annotations

from collections import defaultdict
from fractions import Fraction as Q
import argparse
import gzip
import hashlib
import json
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
PACKAGES = HERE.parent
sys.path.insert(0, str(PACKAGES / 'interval_integer_flow'))
sys.path.insert(0, str(PACKAGES / 'interval_sparse_upper'))
from native_closure import compile_helper
from master import plan_column, projected_order
from verify_upper import verify


def expand_law(compact):
    assert compact['format'] == 'one-turn-run-length-v1'
    data = {k: v for k, v in compact.items() if k not in ('format', 'paths')}
    paths = []
    for row in compact['paths']:
        moves = []
        for sign, count in row['move_runs']:
            assert type(sign) is int and sign in (-1, 1)
            assert type(count) is int and count > 0
            moves.extend([sign] * count)
        plan = {'weight_numerator': row['weight_numerator'],
                'start_grid': row['start_grid'], 'moves': moves}
        for side in ('minus', 'plus'):
            charges = []
            for start, count, amount in row[side + '_charge_runs']:
                assert all(type(x) is int for x in (start, count, amount))
                assert start >= 0 and count > 0 and amount > 0
                charges.extend([start + j, amount] for j in range(count))
            plan[side + '_charges'] = charges
        paths.append(plan)
    data['paths'] = paths
    return data


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--law', type=Path, default=HERE / 'one_turn_upper.json.gz')
    parser.add_argument('--output', type=Path, required=True,
                        help='directory for generated certificate and native binary')
    parser.add_argument('--require-counterexample', action='store_true')
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    raw = args.law.read_bytes()
    payload = gzip.decompress(raw) if raw[:2] == b'\x1f\x8b' else raw
    data = expand_law(json.loads(payload))
    expected = Q(data['global_upper'])
    pressure = defaultdict(int)
    for plan in data['paths']:
        _, column = plan_column(data['n'], plan)
        for point, value in column.items():
            pressure[point] += int(plan['weight_numerator']) * value
    nodes = sorted(point for point, value in pressure.items() if value)
    data['qout_nodes'] = [list(p) for p in nodes]
    data['qout_order'] = [list(e) for e in projected_order(data['n'], nodes)]
    data['source_sha256'] = hashlib.sha256(raw).hexdigest()
    draft = args.output / 'one_turn_upper.input.json'
    draft.write_text(json.dumps(data, separators=(',', ':')) + '\n')
    binary = compile_helper(args.output)
    certificate = args.output / 'one_turn_upper.sparse.json'
    subprocess.run(['node', str(HERE / 'solve_upper.cjs'), str(draft),
                    str(certificate), str(binary)], check=True)
    result = json.loads(certificate.read_text())
    report = verify(result, require_counterexample=args.require_counterexample)
    assert Q(report['global_upper']) == expected
    report['compact_law_sha256'] = hashlib.sha256(raw).hexdigest()
    report['compact_law_uncompressed_sha256'] = hashlib.sha256(payload).hexdigest()
    replay = args.output / 'one_turn_upper.python_replay.json'
    replay.write_text(json.dumps(report, indent=2, sort_keys=True) + '\n')
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
