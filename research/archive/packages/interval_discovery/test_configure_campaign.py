#!/usr/bin/env python3
"""Guard against campaign typos, accidental fan-out and output injection."""
from copy import deepcopy
import json
from pathlib import Path

from configure_campaign import configure


def main():
    actual = json.loads(Path(__file__).with_name('campaign.json').read_text())
    actual_matrix, _ = configure(actual)
    assert [row['id'] for row in actual_matrix['include']] == actual['selected']
    # Keep restart/override assertions reproducible when a later campaign
    # intentionally chooses other registered experiments or a different run.
    config = deepcopy(actual)
    config['selected'] = ['princess-plain']
    for row in config['experiments']:
        row['resume_run_id'] = '43532597339' if row['id'] == 'princess-plain' else ''
    matrix, summary = configure(config)
    assert [row['id'] for row in matrix['include']] == ['princess-plain']
    assert matrix['include'][0]['resume_run_id'] == '43532597339'
    assert len(matrix['include']) == 1 and '\n' not in summary
    override, _ = configure(config, 'monster-priced, princess-proximal', '123456')
    assert [row['id'] for row in override['include']] == ['monster-priced', 'princess-proximal']
    assert all(row['resume_run_id'] == '123456' for row in override['include'])
    assert config['selected'] == ['princess-plain']  # overrides are not mutations
    rejected = 0

    def reject(candidate, selection='', resume=''):
        nonlocal rejected
        try:
            configure(candidate, selection, resume)
        except ValueError:
            rejected += 1
        else:
            raise AssertionError('malformed campaign accepted')

    for selection in ('unknown', 'princess-plain,', ',',
                      'princess-plain,princess-plain', 'princess-plain\nmatrix=anything'):
        reject(config, selection)
    for resume in ('0', '-1', '1.5', '1\nsummary=anything', '$(touch x)'):
        reject(config, resume=resume)
    for key, value in [('n', True), ('seed', 0), ('iterations', 1.5),
                       ('profile', 3), ('kind', 'typo'),
                       ('family', 'typo'), ('id', 'x\nsummary=injected')]:
        bad = deepcopy(config)
        bad['experiments'][0][key] = value
        reject(bad)
    bad = deepcopy(config)
    bad['selected'] = []
    reject(bad)
    bad = deepcopy(config)
    bad['experiments'].append(deepcopy(bad['experiments'][0]))
    reject(bad)
    bad = deepcopy(config)
    bad['experiments'][0]['iterations_typo'] = 2
    reject(bad)
    print(json.dumps({'status': 'PASS', 'default_search_jobs': 1,
                      'default_resume_run_id': '43532597339', 'rejected_cases': rejected}))


if __name__ == '__main__':
    main()
