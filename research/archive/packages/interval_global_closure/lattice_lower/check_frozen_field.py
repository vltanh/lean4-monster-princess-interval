#!/usr/bin/env python3
"""Independent standard-library check of a frozen lattice CDF and exact bound.

Usage: python check_frozen_field.py field.bin[.gz] result.json [--report out.json]

Reads the field one row at a time. All legality and final-bound arithmetic is
integer/Fraction arithmetic. This checks the whole frozen CDF and the result's
normalization; the exhaustive dynamic program must still be replayed by the
C++ verifier. It does not reconstruct any floating-point discovery field.
"""
from array import array
import argparse
from decimal import Decimal, localcontext
from fractions import Fraction
import gzip
import hashlib
import json
from pathlib import Path
import struct
import sys


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def decimal(q):
    with localcontext() as context:
        context.prec = 60
        return str(Decimal(q.numerator) / Decimal(q.denominator))


def file_hash(path):
    digest = hashlib.sha256()
    with path.open('rb') as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b''):
            digest.update(chunk)
    return digest.hexdigest()


def check_field(path, outward_cutoff=2):
    require(type(outward_cutoff) is int and outward_cutoff in (1, 2),
            'invalid outward cutoff')
    path = Path(path)
    opener = gzip.open if path.suffix == '.gz' else open
    digest = hashlib.sha256()
    with opener(path, 'rb') as handle:
        header = handle.read(24)
        require(len(header) == 24, 'truncated field header')
        digest.update(header)
        version, B, NT, NX, D = struct.unpack('<IIIIQ', header)
        require(version == 1, 'unsupported field format')
        require(0 < B <= 1 << 20 and B % 2 == 0, 'invalid even B')
        require(NT == 6 * B + 1 and NX == 2 * B + 1, 'incorrect field dimensions')
        require(D > 0 and D % 2 == 0, 'invalid even CDF denominator')
        require(32 * D * B <= ((1 << 64) - 1) // 2, 'C++ cost overflow bound')
        row_bytes = 8 * NX
        absorption_row = (outward_cutoff + 1) * B
        constant_row = struct.pack('<Q', D // 2) * NX
        previous = None
        nonconstant_rows = 0
        for n in range(NT):
            raw = handle.read(row_bytes)
            require(len(raw) == row_bytes, f'truncated field row {n}')
            digest.update(raw)
            if n > absorption_row:
                # The preceding row and this row are both exactly 1/2;
                # all range, reflection, cone and outward identities follow.
                require(raw == constant_row, f'nonconstant absorbed row {n}')
                continue
            current = array('Q')
            current.frombytes(raw)
            if sys.byteorder != 'little':
                current.byteswap()
            require(current.itemsize == 8, 'uint64 array required')
            require(max(current) <= D, f'CDF outside [0,1] in row {n}')
            require(current[B] == D // 2, f'incorrect center trace in row {n}')
            require(all(current[j] + current[2 * B - j] == D for j in range(B)),
                    f'failed reflection in row {n}')
            if n == absorption_row:
                require(raw == constant_row,
                        f'CDF not absorbed by time {outward_cutoff + 1}')
            if previous is not None:
                require(all(b <= a for a, b in zip(previous[1:], current[:-1])),
                        f'failed left characteristic transport into row {n}')
                require(all(b >= a for a, b in zip(previous[:-1], current[1:])),
                        f'failed right characteristic transport into row {n}')
                if n > outward_cutoff * B:
                    require(current[B + 1:] == previous[B:-1],
                            f'failed positive outward identity into row {n}')
                    require(current[:B] == previous[1:B + 1],
                            f'failed negative outward identity into row {n}')
            previous = current
            nonconstant_rows += raw != constant_row
        require(handle.read(1) == b'', 'unexpected bytes after the field table')
    result = {
        'B': B, 'n': B // 2, 'cdf_denominator': D,
        'outward_cutoff': outward_cutoff,
        'time_rows': NT, 'position_nodes': NX, 'sampled_values': NT * NX,
        'uncompressed_bytes': 24 + NT * row_bytes,
        'uncompressed_table_sha256': digest.hexdigest(),
        'nonconstant_rows': nonconstant_rows,
        'characteristic_inequalities_checked_or_implied_by_constant_tail': 2 * (NT - 1) * (NX - 1),
        'outward_equalities_checked_or_implied_by_constant_tail': 2 * (NT - 1 - outward_cutoff * B) * B,
        'range_reflection_center_absorption': 'PASS',
        'characteristic_transport_and_outward_tail': 'PASS',
    }
    result['stored_file_sha256'] = file_hash(path) if path.suffix == '.gz' else digest.hexdigest()
    return result


def check_result(field, result):
    B, D = field['B'], field['cdf_denominator']
    cutoff = result.get('outward_cutoff', 2)
    require(type(cutoff) is int and cutoff in (1, 2), 'invalid outward cutoff')
    require(field.get('outward_cutoff', 2) == cutoff, 'field checked at wrong outward cutoff')
    precision = result.get('cost_precision', 1)
    require(type(precision) is int and 0 < precision < 1 << 32,
            'invalid cost precision')
    scale = 2 * D * B * precision
    require(32 * D * B * precision <= ((1 << 64) - 1) // 2,
            'C++ precision-adjusted cost overflow bound')
    for name, value in [('format_version', 1), ('B', B), ('n', B // 2),
                        ('cdf_denominator', D), ('cost_scale', scale),
                        ('rounding_budget_units', 12 * B), ('beam_truncations', 0)]:
        require(result.get(name) == value, f'incorrect result field {name}')
    layers = result.get('layer_states')
    require(isinstance(layers, list) and len(layers) == cutoff * B, 'incomplete time-layer count')
    require(all(isinstance(n, int) and n >= 0 for n in layers), 'invalid layer size')
    require(layers[-1] == 0, 'nonempty final frontier')
    minimum = result.get('rounded_minimum_units')
    require(isinstance(minimum, int) and 0 <= minimum < 1 << 64, 'invalid integer minimum')
    lattice = Fraction(minimum, scale)
    penalty = Fraction(1, B)
    lower = lattice - penalty
    for key, value in [('lattice_lower', lattice), ('quantization_penalty', penalty),
                       ('global_value_lower', lower)]:
        if key in result:
            require(Fraction(result[key]) == value, f'incorrect claimed {key}')
    for key in ['sampled_table_sha256', 'uncompressed_table_sha256']:
        if key in result:
            require(result[key] == field['uncompressed_table_sha256'], f'failed {key}')
    return {
        'rounded_minimum_units': minimum, 'cost_scale': scale,
        'cost_precision': precision, 'outward_cutoff': cutoff,
        'complete_time_layers': len(layers), 'beam_truncations': 0,
        'lattice_lower': str(lattice), 'lattice_lower_decimal': decimal(lattice),
        'quantization_penalty': str(penalty),
        'global_value_lower': str(lower), 'global_value_lower_decimal': decimal(lower),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('field', type=Path)
    parser.add_argument('result', type=Path)
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    result = json.loads(args.result.read_text())
    field = check_field(args.field, outward_cutoff=result.get('outward_cutoff', 2))
    report = {
        'status': 'PASS',
        'scope': 'Independent full-table legality and exact final-bound check; exhaustive DP requires its separate C++ replay.',
        'arithmetic': 'Python standard library: integers, uint64 row decoding, Fraction; Decimal for display only',
        'field': field, 'bound': check_result(field, result),
        'result_sha256': file_hash(args.result),
        'checker_source_sha256': file_hash(Path(__file__)),
    }
    encoded = json.dumps(report, indent=2) + '\n'
    if args.report:
        args.report.write_text(encoded)
    print(encoded, end='')


if __name__ == '__main__':
    main()
