#!/usr/bin/env python3
"""Select a validated discovery matrix; do not repeat completed experiments.

SELECT_EXPERIMENTS is an optional comma-separated list of registered IDs.
RESUME_RUN_ID optionally overrides the source run for every selected row.
Empty environment values leave the checked-in campaign settings intact.
The selected matrix and a one-line summary are written to GITHUB_OUTPUT.
No configuration value is evaluated as shell code.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import re
import sys

DEFAULT_CONFIG = Path(__file__).with_name('campaign.json')
ROW_KEYS = {'id', 'kind', 'family', 'n', 'profile', 'seed', 'iterations', 'resume_run_id'}
FAMILIES = {'princess': {'proximal', 'randomized', 'plain'},
            'monster': {'mutations', 'priced'}}
IDENTIFIER = re.compile(r'[a-z][a-z0-9-]{0,63}\Z')
RUN_ID = re.compile(r'[1-9][0-9]*\Z')


def require(condition, message):
    if not condition:
        raise ValueError(message)


def validate_run_id(value, context):
    require(isinstance(value, str), f'{context} must be a string')
    require(value == '' or RUN_ID.fullmatch(value) is not None,
            f'{context} must be empty or a positive decimal GitHub run ID')
    return value


def configure(config, select_override='', resume_override=''):
    require(isinstance(config, dict), 'campaign must be a JSON object')
    require(set(config) == {'version', 'selected', 'experiments'},
            'campaign requires exactly version, selected and experiments')
    require(type(config['version']) is int and config['version'] == 1,
            'unsupported campaign version')
    rows = config['experiments']
    require(isinstance(rows, list) and rows, 'experiments must be a nonempty list')
    registry = {}
    for row in rows:
        require(isinstance(row, dict) and set(row) == ROW_KEYS,
                'each experiment requires exactly ' + ', '.join(sorted(ROW_KEYS)))
        ident = row['id']
        require(isinstance(ident, str) and IDENTIFIER.fullmatch(ident) is not None,
                'experiment id must contain only lowercase letters, digits and hyphens')
        require(ident not in registry, f'duplicate experiment id: {ident}')
        kind, family = row['kind'], row['family']
        require(isinstance(kind, str) and kind in FAMILIES, f'{ident}: unknown kind')
        require(isinstance(family, str) and family in FAMILIES[kind],
                f'{ident}: unknown family for {kind}')
        for key in ('n', 'profile', 'seed', 'iterations'):
            require(type(row[key]) is int and row[key] > 0,
                    f'{ident}: {key} must be a positive integer')
        require(row['profile'] <= row['n'] and row['n'] % row['profile'] == 0,
                f'{ident}: profile must divide n and be no larger than n')
        validate_run_id(row['resume_run_id'], f'{ident}: resume_run_id')
        registry[ident] = dict(row)

    selected = config['selected']
    require(isinstance(selected, list) and selected,
            'selected must be a nonempty list of experiment IDs')
    require(all(isinstance(ident, str) for ident in selected),
            'selected IDs must be strings')
    require(len(selected) == len(set(selected)), 'selected contains duplicate IDs')
    require(all(ident in registry for ident in selected),
            'selected contains an unregistered experiment ID')
    require(isinstance(select_override, str), 'SELECT_EXPERIMENTS must be a string')
    require(isinstance(resume_override, str), 'RESUME_RUN_ID must be a string')
    if select_override:
        selected = [item.strip() for item in select_override.split(',')]
        require(all(selected), 'SELECT_EXPERIMENTS contains an empty ID')
        require(len(selected) == len(set(selected)), 'SELECT_EXPERIMENTS contains duplicate IDs')
        unknown = [ident for ident in selected if ident not in registry]
        require(not unknown, 'unknown SELECT_EXPERIMENTS IDs: ' + ', '.join(unknown))
    if resume_override:
        validate_run_id(resume_override, 'RESUME_RUN_ID')
    include = [dict(registry[ident]) for ident in selected]
    if resume_override:
        for row in include:
            row['resume_run_id'] = resume_override
    summary = f'{len(include)} experiment(s): ' + ', '.join(
        row['id'] + (f" (resume {row['resume_run_id']})" if row['resume_run_id'] else ' (fresh)')
        for row in include)
    return {'include': include}, summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config', type=Path, default=DEFAULT_CONFIG)
    args = parser.parse_args()
    matrix, summary = configure(json.loads(args.config.read_text()),
                                os.environ.get('SELECT_EXPERIMENTS', ''),
                                os.environ.get('RESUME_RUN_ID', ''))
    encoded = json.dumps(matrix, separators=(',', ':'))
    if os.environ.get('GITHUB_OUTPUT'):
        with open(os.environ['GITHUB_OUTPUT'], 'a', encoding='utf-8') as stream:
            stream.write(f'matrix={encoded}\nsummary={summary}\n')
    print(encoded)
    print(summary, file=sys.stderr)


if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError, KeyError) as error:
        print(f'Invalid discovery campaign: {error}', file=sys.stderr)
        raise SystemExit(2)
