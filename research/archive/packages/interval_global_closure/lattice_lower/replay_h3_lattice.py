#!/usr/bin/env python3
"""Replay the frozen unrestricted game-value lower certificate.

Default: verify all hashes and CDF inequalities, compile the exhaustive C++
search, replay it to completion, and recompute the final bound with Fraction.
--check-only verifies the saved input and arithmetic, not the search minimum.
Python's standard library and a C++17 compiler are sufficient; no floating
discovery code, optimizer, NumPy, or external solver is used.
"""
import argparse
import json
from pathlib import Path
import subprocess
import tempfile

from check_frozen_field import check_field, check_result, file_hash, require
from field_codec import expand


HERE = Path(__file__).resolve().parent


def replay(folder, manifest, check_only, compiler):
    for name, expected in manifest['file_sha256'].items():
        require(file_hash(HERE / name) == expected, 'source/input hash mismatch: ' + name)
    field_path = folder / 'field.bin'
    expanded_hash = expand(HERE / manifest['compact_field'], field_path)
    require(expanded_hash == manifest['uncompressed_table_sha256'],
            'expanded frozen field hash mismatch')
    saved = json.loads((HERE / manifest['search_result']).read_text())
    field = check_field(field_path, saved['outward_cutoff'])
    bound = check_result(field, saved)
    require(bound['global_value_lower'] == manifest['global_value_lower'],
            'manifest lower fraction differs from exact arithmetic')
    if not check_only:
        binary = folder / 'verify_integer_lattice'
        subprocess.run([compiler, '-O3', '-std=c++17', '-Wall', '-Wextra',
                        str(HERE / 'verify_integer_lattice.cpp'), '-o', str(binary)],
                       check=True)
        output = folder / 'search.json'
        subprocess.run([str(binary), str(field_path), str(output),
                        str(saved['cost_precision']), str(saved['outward_cutoff'])],
                       check=True)
        actual = json.loads(output.read_text())
        require(actual == saved, 'exhaustive replay differs from frozen search result')
        bound = check_result(field, actual)
    return {
        'status': 'INPUT_AND_ARITHMETIC_ONLY' if check_only else 'FULL_REPLAY_PASS',
        'scope': ('The unrestricted game-value lower bound uses the complete lattice '
                  'search and the proved 1/B quantization transfer. It is not a '
                  'direct all-Monster security certificate for this same CDF.'),
        'search_replayed': not check_only,
        'input': field,
        'bound': bound,
        'frozen_search_sha256': file_hash(HERE / manifest['search_result']),
        'manifest_sha256': file_hash(HERE / 'h3_lattice_certificate.json'),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check-only', action='store_true')
    parser.add_argument('--compiler', default='g++')
    parser.add_argument('--work-dir', type=Path,
                        help='Keep expanded input and replay files in this directory')
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    manifest = json.loads((HERE / 'h3_lattice_certificate.json').read_text())
    if args.work_dir:
        args.work_dir.mkdir(parents=True, exist_ok=True)
        report = replay(args.work_dir, manifest, args.check_only, args.compiler)
    else:
        with tempfile.TemporaryDirectory(prefix='princess-lattice-replay-') as tmp:
            report = replay(Path(tmp), manifest, args.check_only, args.compiler)
    encoded = json.dumps(report, indent=2) + '\n'
    if args.report:
        args.report.write_text(encoded)
    print(encoded, end='')


if __name__ == '__main__':
    main()
