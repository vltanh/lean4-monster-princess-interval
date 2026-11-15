#!/usr/bin/env python3
"""Independent exhaustive rational replay on inward-moving CDF fixtures.

The reference enumerates every normalized path and integrates capped CDF
records with Fraction. It does not reuse the C++ recurrence, dominance,
integer ceiling formula, or pursuit pruning. These are verifier regression
fixtures, not new game-value certificates.
"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile

CHECKERS = Path(__file__).resolve().parent
sys.path.insert(0, str(CHECKERS))
from test_integer_lattice import assert_fixture_axioms, brute_force, write_table


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path,
                        default=CHECKERS / 'verify_integer_lattice.cpp')
    args = parser.parse_args()
    source = args.source.resolve()
    fixture_path = Path(__file__).with_name('inward_lattice_fixtures.json')
    fixtures = json.loads(fixture_path.read_text())['fixtures']
    report = {'scope': 'Independent exhaustive Fraction verification on inward CDFs; no game-value claim.',
              'verifier_source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
              'fixture_sha256': hashlib.sha256(fixture_path.read_bytes()).hexdigest(),
              'fixtures': []}
    with tempfile.TemporaryDirectory(prefix='inward-lattice-review-') as tmp:
        folder = Path(tmp)
        exe = folder / 'verify'
        subprocess.run(['g++', '-O2', '-std=c++17', str(source), '-o', str(exe)], check=True)
        for fixture in fixtures:
            B, D = fixture['B'], fixture['D']
            table = fixture['rows_to_absorption']
            assert len(table) == 3 * B + 1
            table = table + [[D // 2] * (2 * B + 1) for _ in range(3 * B)]
            assert_fixture_axioms(B, D, table)
            # An outward-only field has a nonincreasing positive-side CDF
            # at fixed x. Require this fixture to exercise genuine inward
            # movement by exhibiting a strict increase before time two.
            assert any(table[n + 1][j] > table[n][j]
                       for n in range(2 * B) for j in range(B + 1, 2 * B))
            binary = folder / f'B{B}.bin'
            write_table(binary, B, D, table)
            assert hashlib.sha256(binary.read_bytes()).hexdigest() == fixture['input_table_sha256']
            for precision in (1, 256):
                reference = brute_force(B, D, table, cost_precision=precision)
                assert reference['partial_record_crossings'] > 0
                if precision == 1:
                    assert reference['rounded_minimum_units'] == fixture['expected_rounded_minimum']
                output = folder / f'B{B}_P{precision}.json'
                subprocess.run([str(exe), str(binary), str(output), str(precision)], check=True,
                               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                actual = json.loads(output.read_text())
                assert actual['rounded_minimum_units'] == reference['rounded_minimum_units']
                assert actual['cost_precision'] == precision
                assert actual['cost_scale'] == 2 * D * B * precision
                assert actual['beam_truncations'] == 0
                assert len(actual['layer_states']) == 2 * B
                report['fixtures'].append({'B': B, 'D': D, 'cost_precision': precision,
                                           'reference': reference,
                                           'cpp_rounded_minimum': actual['rounded_minimum_units']})
    report['status'] = 'PASS'
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
