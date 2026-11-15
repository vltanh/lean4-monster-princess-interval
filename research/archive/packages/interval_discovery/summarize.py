#!/usr/bin/env python3
"""Read discovery artifacts and independently replay prospective improvements.

A successful workflow is not an improvement. The retained bounds change only
after an exact replay of a new input, and every report keeps that distinction.
"""
from __future__ import annotations

import argparse
from fractions import Fraction
import gzip
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
LOWER = max(Fraction(3050023091, 2147483648),
            Fraction(json.loads((ROOT/'packages/interval_clock_grid/lower_n256_field.json').read_text())['global_lower']))
UPPER = Fraction(364842628535291, 256000000000000)
RETAINED_UPPER = ROOT/'packages/interval_discovery_certificates/monster_mutations_n128_manifest.json'
if RETAINED_UPPER.exists():
    retained = json.loads(RETAINED_UPPER.read_text())
    if retained['status'] != 'PASS' or retained['exact_result']['status'] != 'PASS':
        raise ValueError('retained upper manifest is not a completed certificate')
    UPPER = min(UPPER, Fraction(retained['exact_result']['global_upper']))


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def run(command, log):
    with log.open('w') as output:
        subprocess.run(command, stdout=output, stderr=subprocess.STDOUT,
                       check=True, cwd=ROOT, timeout=1800)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('directory', type=Path)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--bigint', action='store_true',
                        help='Also require the separate, potentially expensive BigInt full-bank replay.')
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    report = {'scope': 'Discovery campaign; only independently replayed new inputs can improve the retained game bounds.',
              'github_run_id': os.environ.get('GITHUB_RUN_ID'),
              'github_sha': os.environ.get('GITHUB_SHA'),
              'baseline_game_lower': str(LOWER), 'baseline_game_upper': str(UPPER),
              'experiments': [], 'promotions': [], 'errors': []}
    lower, upper = LOWER, UPPER
    candidates = []
    for path in sorted(args.directory.rglob('manifest.json')):
        if any(p.endswith('.work') for p in path.parts):
            continue
        try:
            data = json.loads(path.read_text())
            entry = {'experiment': str(path.parent.relative_to(args.directory)),
                     'manifest_sha256': digest(path), 'status': data.get('status'),
                     'family': data.get('options', {}).get('family'),
                     'best_exact': data.get('best_exact'),
                     'best_upper': data.get('best_upper'),
                     'error': data.get('error')}
            entry['source_manifest_game_lower'] = data.get('baseline_game_lower')
            if entry['best_exact']:
                entry['best_exact'] = dict(entry['best_exact'])
                entry['best_exact']['source_manifest_claimed_improvement'] = entry['best_exact'].get('improves_retained_game_lower')
                entry['best_exact']['improves_retained_game_lower'] = (
                    Fraction(entry['best_exact']['certified_game_value_lower']) > LOWER)
            if entry['best_upper'] is not None:
                entry['improves_retained_game_upper'] = Fraction(entry['best_upper']) < UPPER
            report['experiments'].append(entry)
            # Select recorded complete candidates, then independently validate
            # their exact contents. No floating LP objective is considered.
            for field in list(path.parent.glob('*.dual.json')) + list(path.parent.glob('*.dual.json.gz')):
                content = field.read_bytes()
                raw = json.loads(gzip.decompress(content) if content[:2] == b'\x1f\x8b' else content)
                if 'global_lower' not in raw or raw.get('pricing', {}).get('status') != 'PASS':
                    continue
                candidate = Fraction(raw['global_lower'])
                if candidate > LOWER:
                    candidates.append((candidate, field))
        except Exception as exc:
            report['errors'].append({'file': str(path), 'error': str(exc)})
    if candidates:
        proposed, field = max(candidates, key=lambda x: x[0])
        try:
            native_report = args.output/'best_lower_native_replay.json'
            run([sys.executable, str(ROOT/'packages/interval_clock_grid/normalized_native/verify_native_field.py'),
                 str(field.resolve()), '--output', str(native_report.resolve())],
                args.output/'best_lower_native.log')
            # A full native exact replay, independent input decoding, and exact
            # transfer arithmetic are a computer-assisted certificate. A second
            # complete implementation is useful but is not a theorem premise.
            if args.bigint:
                run(['node', '--max-old-space-size=8192',
                     str(ROOT/'packages/interval_clock_grid/normalized_record_pricing.cjs'),
                     str(field.resolve()), '--target-bound'], args.output/'best_lower_bigint.log')
            # Independently check all Qout field inequalities with the existing
            # JavaScript reader, without repricing the bank yet again.
            field_check = [
                'node', '-e',
                'const x=require("./packages/interval_clock_grid/extract_normalized_princess.cjs");'
                'const p=x.inspectProfile(x.readSource(process.argv[1]).data);'
                'console.log(JSON.stringify({status:"PASS",n:p.n,nodes:p.count,cone_checks:p.coneChecks,endpoint_checks:p.endpointChecks}));',
                str(field.resolve())]
            run(field_check, args.output/'best_lower_independent_field.json')
            checked = json.loads(native_report.read_text())
            if checked['status'] != 'PASS' or Fraction(checked['global_value_lower']) != proposed:
                raise ValueError('independent lower replay disagreement')
            lower = proposed
            report['promotions'].append({'kind': 'unrestricted_game_value_lower',
                'value': str(lower), 'candidate': str(field.relative_to(args.directory)),
                'sha256': digest(field), 'same_cdf_continuum_security_claimed': False,
                'complete_native_integer_replay': 'PASS',
                'independent_field_and_fraction_checks': 'PASS',
                'independent_bigint_replay': 'PASS' if args.bigint else 'not requested',
                'trust_boundary': 'Existing exhaustive integer C++ recurrence and pruning, with Fraction regression coverage; not Lean kernel verification.'})
        except Exception as exc:
            report['errors'].append({'candidate': str(field), 'error': str(exc)})
    # Recompute every retained physical upper in independent node invocations.
    # These are generally small enough that a failed optimization still leaves
    # its best earlier physical strategy reviewable.
    for field in sorted(args.directory.rglob('*.physical.json')):
        try:
            raw = json.loads(field.read_text())
            proposed = Fraction(raw['global_upper'])
            if proposed >= upper:
                continue
            completed = subprocess.run(['node', str(ROOT/'packages/interval_clock_grid/qout_primal_certificate.cjs'),
                                        str(field.resolve())], check=True, capture_output=True,
                                       text=True, cwd=ROOT, timeout=600)
            checked = json.loads(completed.stdout)
            if checked['status'] != 'PASS' or Fraction(checked['global_upper']) != proposed:
                raise ValueError('independent physical upper disagreement')
            upper = proposed
            name = 'upper_replay_' + digest(field)[:12] + '.json'
            (args.output/name).write_text(json.dumps(checked, indent=2)+'\n')
            report['promotions'].append({'kind': 'unrestricted_physical_monster_upper',
                'value': str(upper), 'candidate': str(field.relative_to(args.directory)),
                'sha256': digest(field), 'exact_all_princess_replay': 'PASS'})
        except Exception as exc:
            report['errors'].append({'candidate': str(field), 'error': str(exc)})
    report.update({'certified_game_lower': str(lower), 'certified_game_upper': str(upper),
                   'certified_gap': str(upper-lower),
                   'lower_decimal': float(lower), 'upper_decimal': float(upper),
                   'improved_game_bound': lower > LOWER or upper < UPPER,
                   'exact_equilibrium_solved': False,
                   'status': 'PASS' if not report['errors'] else 'REVIEW_REQUIRED'})
    (args.output/'campaign.json').write_text(json.dumps(report, indent=2)+'\n')
    lines = ['# Unrestricted Princess–Monster discovery', '',
             f"Certified game interval after independent promotion checks: **{lower} ≤ V ≤ {upper}**.",
             '', f"Decimal interval: **{float(lower):.15f} ≤ V ≤ {float(upper):.15f}**.", '',
             'A green search job means the experiment completed; it does not by itself improve a bound.', '',
             '| Experiment | Status |', '|---|---|']
    for entry in report['experiments']:
        lines.append(f"| {entry['experiment']} | {entry['status']} |")
    lines += ['', '## Mathematical outcome', '',
              'A new bound passed exact replay.' if report['improved_game_bound'] else
              'No new unrestricted game bound passed the promotion gate in this campaign.',
              '', 'The exact equilibrium and a terminating sufficient classification remain open.', '',
              'See campaign.json and the per-experiment artifacts for candidate hashes, seeds, solver logs, and precise certificate scope.']
    if report['errors']:
        lines += ['', 'Some candidates failed or need review; no failed candidate was promoted.']
    summary='\n'.join(lines)+'\n'
    (args.output/'SUMMARY.md').write_text(summary)
    if os.environ.get('GITHUB_STEP_SUMMARY'):
        with open(os.environ['GITHUB_STEP_SUMMARY'], 'a') as stream:
            stream.write(summary)
    print(json.dumps(report, indent=2), flush=True)
    if report['errors']:
        sys.exit(1)


if __name__ == '__main__':
    main()
