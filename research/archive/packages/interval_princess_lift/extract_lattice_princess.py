#!/usr/bin/env python3
"""Lift a completed physical lattice lower into a NEW explicit Princess law.

The source computation bounds actual CDF payoffs on the entire physical bank.
Every causal vertex-clock plane dominates that payoff.  This supplies the
per-clock lower required by constructive common-threshold extraction, without
asserting that the original frozen CDF has unrestricted security and without
pretending to rerun the normalized native/BigInt oracle.

`verify` checks source identities, the completed source result, every new Qout
inequality, and deterministic regeneration.  It DOES NOT rerun the large source
lattice search.  Use replay_h3_lattice.py for that separate computation.
"""
from __future__ import annotations

from array import array
import argparse
import base64
from fractions import Fraction as Q
import gzip
import hashlib
import json
from pathlib import Path
import struct
import sys
import zlib

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
DEFAULT_SOURCE = ROOT / 'packages/interval_global_closure/lattice_lower/h3_lattice_certificate.json'
DEFAULT_STRATEGY = HERE / 'lattice_b1536_princess.json'
ORIENTATION = 'k modulo 2n is positive for 0 <= k < n, negative otherwise'
DOMAIN = ('pre-two radial nodes: j=0..4n, then k=1..2n in ascending order with j+k even; '
          'center is zero; after time2 use outward footpoint, zero if footpoint<=0')
METHOD = 'complete-lattice-physical-cost-to-all-vertex-clock-domination'


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def relative(path):
    return str(path.resolve().relative_to(ROOT))


def checked_source(manifest_path):
    manifest_path = Path(manifest_path)
    manifest_bytes = manifest_path.read_bytes()
    manifest = json.loads(manifest_bytes)
    source_dir = manifest_path.parent
    compact_path = source_dir / manifest['compact_field']
    result_path = source_dir / manifest['search_result']
    required = [manifest['compact_field'], manifest['search_result'],
                'verify_integer_lattice.cpp', 'check_frozen_field.py',
                'field_codec.py', 'replay_h3_lattice.py']
    checked_hashes = {}
    for name in required:
        actual = sha256((source_dir / name).read_bytes())
        assert actual == manifest['file_sha256'][name], ('source SHA256 mismatch', name)
        checked_hashes[name] = actual
    result = json.loads(result_path.read_text())
    for key in ('B', 'n', 'cdf_denominator', 'cost_precision', 'outward_cutoff',
                'cost_scale', 'rounded_minimum_units'):
        assert result[key] == manifest[key], ('manifest/result mismatch', key)
    B, D, P = (int(manifest[k]) for k in ('B', 'cdf_denominator', 'cost_precision'))
    assert B > 0 and B % 2 == 0 and D > 0 and D % 2 == 0 and P > 0
    assert manifest['n'] == B // 2
    assert manifest['cost_scale'] == 2 * D * B * P
    assert result['beam_truncations'] == 0
    assert len(result['layer_states']) == manifest['outward_cutoff'] * B
    assert result['layer_states'][-1] == 0
    lower = Q(manifest['rounded_minimum_units'], manifest['cost_scale'])
    assert lower == Q(manifest['lattice_lower'])
    assert lower - Q(1, B) == Q(manifest['global_value_lower'])
    return manifest, compact_path, {
        'manifest': relative(manifest_path),
        'manifest_sha256': sha256(manifest_bytes),
        'compact_field': relative(compact_path),
        'compact_field_sha256': checked_hashes[manifest['compact_field']],
        'completed_search_result': relative(result_path),
        'completed_search_result_sha256': checked_hashes[manifest['search_result']],
        'expanded_table_sha256': manifest['uncompressed_table_sha256'],
        'checked_dependency_sha256': checked_hashes,
        'source_search_transitions': result['generated'],
        'source_search_empty_final_frontier': True,
        'source_search_replayed_by_this_program': False,
        'independent_normalized_repricing_performed': False,
    }


def compact_to_profile(compact_path, manifest):
    """Read only the compact positive half; retain the defining checkerboard."""
    B, D, P = (int(manifest[k]) for k in ('B', 'cdf_denominator', 'cost_precision'))
    n = B // 2
    radial_denominator = D * P
    assert radial_denominator <= 0xffffffff
    radial = array('I')
    with gzip.open(compact_path, 'rb') as src:
        header = src.read(24)
        assert struct.unpack('<IIIIQ', header) == (2, B, 2 * B + 1, B + 1, D)
        for j in range(2 * B + 1):
            row_bytes = src.read(2 * B)
            assert len(row_bytes) == 2 * B
            increments = array('H')
            increments.frombytes(row_bytes)
            if sys.byteorder != 'little':
                increments.byteswap()
            f = D // 2
            for k, increment in enumerate(increments, start=1):
                f += increment
                assert D // 2 <= f <= D
                if (j + k) % 2 == 0:
                    # (2 f - D)/D is the radial CDF.  Scaling by P makes the
                    # existing strategy format's 4nD denominator equal to the
                    # rounded physical certificate's 2*D*B*P denominator.
                    radial.append((2 * f - D) * P)
        assert src.read(1) == b''
    assert len(radial) == (2 * B + 1) * n

    def node(j, k):
        assert 0 <= j <= 2 * B and 0 <= k <= B and (j + k) % 2 == 0
        return 0 if k == 0 else radial[j * n + (k - 1) // 2]

    cones = 0
    for j in range(2 * B + 1):
        for k in range(1 + (j % 2 == 0), B + 1, 2):
            value = node(j, k)
            assert 0 <= value <= radial_denominator
            if k < B:
                for step in (-1, 1):
                    if 0 <= j + step <= 2 * B:
                        assert value <= node(j + step, k + 1), ('transport', j, k, step)
                        cones += 1
    for j in range(0, 2 * B, 2):
        assert node(j + 2, B) <= node(j, B), ('nonsticky endpoint', j)
    # Outward1 is inherited for the supplied table, but extraction only needs
    # Qout2.  Check the stronger inherited identity independently when declared.
    outward_checks = 0
    cutoff = manifest['outward_cutoff'] * B
    if cutoff == B:
        for j in range(B, 2 * B + 1):
            for k in range(1 + (j % 2 == 0), B + 1, 2):
                foot = k - (j - B)
                expected = 0 if foot <= 0 else node(B, foot)
                assert node(j, k) == expected, ('outward1', j, k)
                outward_checks += 1
    assert 4 * n * radial_denominator == manifest['cost_scale']
    if sys.byteorder != 'little':
        radial.byteswap()
    raw = radial.tobytes()
    profile = {
        'format': 'qout-clock-grid-field-u32-zlib-v1',
        'n': n,
        'field_denominator': str(radial_denominator),
        'normalized_profile': True,
        'encoding': {'domain': DOMAIN, 'integer_type': 'uint32 little-endian',
                     'compression': 'zlib', 'count': len(radial),
                     'uncompressed_sha256': sha256(raw)},
        'pre_two_values_base64': base64.b64encode(zlib.compress(raw, 9)).decode('ascii'),
    }
    return profile, {'stored_radial_nodes': len(radial), 'cone_inequalities': cones,
                     'sticky_endpoint_inequalities': B,
                     'inherited_outward1_equalities': outward_checks}


def make_strategy(manifest_path=DEFAULT_SOURCE, epsilon=None):
    manifest, compact_path, provenance = checked_source(manifest_path)
    B = int(manifest['B'])
    epsilon = Q(1, B) if epsilon is None else Q(epsilon)
    assert 0 < epsilon <= Q(1, 2)
    profile, validation = compact_to_profile(compact_path, manifest)
    c = Q(manifest['lattice_lower'])
    loss = (1 + epsilon) / B
    guarantee = c - loss
    assert guarantee < Q(3, 2), 'late-center comparison must be checked'
    return {
        'format': 'normalized-qout-princess-p1-v1',
        'scope': ('NEW explicit continuous Princess law obtained by common-threshold '
                  'interpolation of the certified physical lattice field. The displayed '
                  'security covers every continuous Monster. It is NOT a security claim '
                  'for the original frozen characteristic-P1 CDF.'),
        'certificate_method': METHOD,
        'n': B // 2,
        'interpolation_epsilon': str(epsilon),
        'cdf_denominator': profile['field_denominator'],
        'nodal_profile': profile,
        'cell_orientation': ORIENTATION,
        'quantile_rule': ('Choose u uniformly in [0,1), use inf {r in [0,1] : '
                          'radialCDF(t,r) > u}, and choose one independent fair sign '
                          'for the entire path.'),
        'outward_time': 2,
        'absorption_time': 3,
        'source_input_sha256': provenance['compact_field_sha256'],
        'source_input_kind': 'Original compact physical-lattice CDF; see lattice_provenance.',
        'verified_lower_units': str(manifest['rounded_minimum_units']),
        'objective_denominator': str(manifest['cost_scale']),
        'finite_dual_lower': str(c),
        'exact_transfer_loss': str(loss),
        'guaranteed_security': str(guarantee),
        'lattice_provenance': provenance,
        'validation': validation,
        'proof': ('research/12-global-closure/PHYSICAL_LATTICE_PRINCESS_EXTRACTION.md, '
                  'physical-to-clock domination and feasible-level constructive extraction. '
                  'The source complete lattice search is an independently replayable '
                  'dependency, not a new search performed by this extractor.'),
    }


def decoded_profile(strategy):
    p = strategy['nodal_profile']
    raw = zlib.decompress(base64.b64decode(p['pre_two_values_base64'], validate=True))
    assert len(raw) == 4 * p['encoding']['count']
    assert sha256(raw) == p['encoding']['uncompressed_sha256']
    return raw


def verify_strategy(strategy_path=DEFAULT_STRATEGY, manifest_path=DEFAULT_SOURCE):
    strategy_path = Path(strategy_path)
    actual = json.loads(strategy_path.read_text())
    expected = make_strategy(manifest_path, actual['interpolation_epsilon'])
    assert decoded_profile(actual) == decoded_profile(expected), 'decoded strategy changed'
    # Different zlib implementations can encode identical exact node arrays.
    for obj in (actual, expected):
        del obj['nodal_profile']['pre_two_values_base64']
    assert actual == expected, 'strategy metadata/guarantee differs from exact regeneration'
    return {
        'status': 'PASS', 'certificate_method': METHOD,
        'scope': ('Exact source binding, full Qout validation and deterministic extraction. '
                  'The source complete lattice minimum is a previously certified dependency; '
                  'this command does not replay its exhaustive search.'),
        'strategy_sha256': sha256(strategy_path.read_bytes()),
        'decoded_nodal_profile_sha256': actual['nodal_profile']['encoding']['uncompressed_sha256'],
        'guaranteed_security': actual['guaranteed_security'],
        'guaranteed_security_decimal': format(float(Q(actual['guaranteed_security'])), '.17g'),
        'exact_transfer_loss': actual['exact_transfer_loss'],
        'lattice_search_replayed': False,
        'independent_normalized_repricing_performed': False,
        'validation': actual['validation'],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['generate', 'verify'])
    parser.add_argument('--manifest', type=Path, default=DEFAULT_SOURCE)
    parser.add_argument('--strategy', type=Path, default=DEFAULT_STRATEGY)
    parser.add_argument('--epsilon', help='positive rational; default 1/B when generating')
    parser.add_argument('--output', type=Path, help='optional exact verification report')
    args = parser.parse_args()
    if args.command == 'generate':
        strategy = make_strategy(args.manifest, args.epsilon)
        args.strategy.parent.mkdir(parents=True, exist_ok=True)
        args.strategy.write_text(json.dumps(strategy, indent=2) + '\n')
    else:
        assert args.epsilon is None, 'verify reads epsilon from the strategy'
    report = verify_strategy(args.strategy, args.manifest)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
