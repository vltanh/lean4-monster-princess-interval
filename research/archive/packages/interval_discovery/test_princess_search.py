#!/usr/bin/env python3
"""Physical seed checks and an independent BigInt replay of fresh discovery."""
from fractions import Fraction
import json
from pathlib import Path
import random
import subprocess
import sys
import tempfile

from princess_search import ROOT, random_path, read_json, run_logged


def main():
    count = 0
    for n in (1,2,5,16):
        for seed in (0,1,17,20261114):
            rng = random.Random(seed)
            first = random_path(n,rng)
            assert first == random_path(n,random.Random(seed))
            for path in [first]+[random_path(n,rng) for _ in range(50)]:
                positions = [path['start_grid']]
                for step in path['moves']:
                    assert step in (-1,1)
                    positions.append(positions[-1]+step)
                assert positions[0] % 2 == 0
                assert max(map(abs,positions)) <= 2*n
                assert positions.index(0) <= 4*n
                assert max(positions.index(-2*n),positions.index(2*n)) <= 12*n
                count += 1
    with tempfile.TemporaryDirectory(prefix='princess_discovery_test_') as folder:
        directory = Path(folder)
        command = [sys.executable, str(Path(__file__).with_name('princess_search.py')),
                   '--n','2','--family','randomized','--seed','17','--iterations','12',
                   '--output',folder,'--refine','4','--refine-threshold','0',
                   '--independent-replay','--seconds','60']
        subprocess.run(command, cwd=ROOT, check=True, stdout=subprocess.DEVNULL)
        manifest = read_json(directory/'manifest.json')
        assert manifest['status'] == 'PASS'
        assert manifest['independent_bigint_replay'] == 'PASS'
        assert manifest['refined_exact']['n'] == 4
        best = manifest['best_exact']
        field = read_json(directory/best['file'])
        value = Fraction(int(field['minimum_units']),int(field['objective_denominator']))-Fraction(1,2*field['n'])
        assert value == Fraction(best['certified_game_value_lower'])
        assert best['same_cdf_continuum_security_claimed'] is False
        assert not list(directory.glob('*.work/pricing.input.bin'))
        # A restart must retain and improve the exact best, not merely reuse
        # a floating cached-path minimum as its lower certificate.
        command = command[:command.index('--refine')] + ['--resume','--seconds','60']
        subprocess.run(command,cwd=ROOT,check=True,stdout=subprocess.DEVNULL)
        restarted = read_json(directory/'manifest.json')
        assert restarted['resumed_manifest_sha256']
        assert Fraction(restarted['coarse_exact']['certified_game_value_lower']) >= Fraction(manifest['coarse_exact']['certified_game_value_lower'])
        assert Fraction(restarted['best_exact']['certified_game_value_lower']) >= value
        # A stopped LP must retain a completed exact field, and a different
        # solver error must still fail instead of becoming a budget stop.
        saved = directory/'candidate.dual.json'
        stop = [sys.executable,'-c',
                'import sys; print("HiGHS status: Time limit reached"); sys.exit(1)']
        assert run_logged(stop,directory,'budget_regression',10,saved) == 'BUDGET_STOPPED'
        bad = [sys.executable,'-c','import sys; print("unexpected solver failure"); sys.exit(1)']
        try:
            run_logged(bad,directory,'unexpected_error_regression',10,saved)
        except RuntimeError:
            pass
        else:
            raise AssertionError('unexpected solver error was swallowed')
    print(json.dumps({'status':'PASS','legal_seed_paths':count,
                      'independent_bigint_fresh_discovery':True,
                      'refinement_and_restart':True,
                      'budget_stop_preserves_only_completed_exact_field':True},indent=2))


if __name__ == '__main__':
    main()
