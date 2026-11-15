#!/usr/bin/env python3
"""Independent Fraction check of exact continuation at the time-one cutoff.

For each genuinely inward-moving fixture, enumerate the entire normalized
time-two path bank and the time-one bank with its proved terminal tours.
Their minimum exact costs must agree. Independently integrate every edge
and compare the time-one rounded minimum with the C++ verifier. A rounded
minimum need not equal the full time-two rounded minimum, since the two
normalizations preserve exact cost rather than each edge's flooring error.
"""
import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile

from check_frozen_field import check_field, check_result
from test_integer_lattice import (
    FIXTURES, assert_fixture_axioms, brute_force, make_table, write_table,
)


def main():
    folder = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, default=folder / 'verify_integer_lattice.cpp')
    args = parser.parse_args()
    source = args.source.resolve()
    fixture_path = folder / 'inward_lattice_fixtures.json'
    fixtures = json.loads(fixture_path.read_text())['fixtures']
    report = {
        'scope': 'Independent exact comparison of time-one and time-two normalized path banks.',
        'verifier_source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
        'fixture_sha256': hashlib.sha256(fixture_path.read_bytes()).hexdigest(),
        'cases': [],
    }
    with tempfile.TemporaryDirectory(prefix='early-outward-review-') as tmp:
        work = Path(tmp)
        exe = work / 'verify'
        subprocess.run(['g++', '-O2', '-std=c++17', str(source), '-o', str(exe)], check=True)
        for fixture in fixtures:
            B, D = fixture['B'], fixture['D']
            table = fixture['rows_to_absorption']
            table = table + [[D // 2] * (2 * B + 1) for _ in range(3 * B)]
            assert_fixture_axioms(B, D, table)
            binary = work / f'B{B}.bin'
            write_table(binary, B, D, table)
            field = check_field(binary, outward_cutoff=1)
            for precision in (1, 256):
                full = brute_force(B, D, table, cost_precision=precision, decision_cutoff=2)
                early = brute_force(B, D, table, cost_precision=precision, decision_cutoff=1)
                assert full['partial_record_crossings'] > 0
                assert early['partial_record_crossings'] > 0
                assert full['exact_minimum_scaled'] == early['exact_minimum_scaled']
                assert early['rounded_minimum_units'] <= Fraction(full['exact_minimum_scaled'])
                output = work / f'B{B}_P{precision}.json'
                subprocess.run([str(exe), str(binary), str(output), str(precision), '1'],
                               check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                actual = json.loads(output.read_text())
                assert actual['rounded_minimum_units'] == early['rounded_minimum_units']
                bound = check_result(field, actual)
                report['cases'].append({
                    'B': B, 'D': D, 'cost_precision': precision,
                    'full_time_two_reference': full, 'early_time_one_reference': early,
                    'cpp_rounded_minimum': actual['rounded_minimum_units'],
                    'complete_time_layers': bound['complete_time_layers'],
                })

        # An admissible time-two field is not automatically a time-one field.
        late_components = dict(FIXTURES)['two_releases']
        D, table = make_table(4, late_components)
        binary, output = work / 'late.bin', work / 'late.json'
        write_table(binary, 4, D, table)
        check_field(binary, outward_cutoff=2)
        try:
            check_field(binary, outward_cutoff=1)
        except AssertionError:
            pass
        else:
            raise AssertionError('independent checker accepted an invalid early cutoff')
        rejected = subprocess.run([str(exe), str(binary), str(output), '256', '1'],
                                  stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        assert rejected.returncode in (10, 11, 12)
        report['late_release_early_cutoff_rejected'] = True
    report['status'] = 'PASS'
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
