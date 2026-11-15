#!/usr/bin/env python3
"""Check exact anchors and replay a freshly regularized field independently."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile

import numpy as np
from shape_search import (Master, InterpolatedMaster, ROOT, save_field, read_json,
                          initial_integer_bounds, anchored_trial, digest)
from verify_shape_attack import verify


def main():
    with tempfile.TemporaryDirectory(prefix='cdf_shape_test_') as folder:
        directory = Path(folder)
        m = Master(2,directory/'initial.work',10**6,True)
        values = np.asarray([k/m.R*(.55+.3*np.sin(2*np.pi*j/m.C)) for j,k in m.nodes])
        answer,table = m.price(values,keep=12)
        source = directory/'seed.json'
        save_field(source,m,table,answer,'test')
        f = InterpolatedMaster(4,2,directory/'fine.work',10**6)
        fine = f.repair(f.interpolate_seed(read_json(source)))
        bounds = initial_integer_bounds(f,fine)
        for perturbation in (-1e-8,0,1e-8):
            trial = f.profile_values(fine)+perturbation
            repaired = f.repair(anchored_trial(f,trial,bounds))
            for i,value in bounds[2].items():
                j,k = f.coarse.nodes[i]
                assert int(repaired[2*j,2*k]) == value*4
        for fixed in (False,True):
            output = directory/('fixed' if fixed else 'free')
            command = [sys.executable,str(Path(__file__).with_name('shape_search.py')),
                       '--seed-field',str(source),'--n','4','--profile-grid','2',
                       '--output',str(output),'--loss','1/100','--iterations','80',
                       '--seconds','60','--independent-replay','--denominator','1000000']
            if fixed:command.append('--fixed-initial')
            subprocess.run(command,cwd=ROOT,check=True,stdout=subprocess.DEVNULL)
            manifest = read_json(output/'manifest.json')
            assert manifest['status'] == 'PASS'
            assert manifest['exact_security_floor_verified']
            assert manifest['independent_bigint_replay'] == 'PASS'
            assert manifest['after']['temporal_total_variation_decimal'] <= manifest['before']['temporal_total_variation_decimal']
            assert manifest['accepted_new_profiles'] > 0
        # With half the Princess mass at each endpoint, a Monster starting at
        # the left endpoint captures that half at time zero, the rest at two.
        # This independently exercises strict endpoint exclusion in the plane.
        endpoint = Master(1,directory/'endpoint.work',101,True)
        endpoint_answer,endpoint_table = endpoint.price(np.zeros(endpoint.K),keep=1)
        endpoint_field = directory/'endpoint.json'
        save_field(endpoint_field,endpoint,endpoint_table,endpoint_answer,'test')
        witness = directory/'endpoint_attack.json'
        witness.write_text(json.dumps({'field_sha256':digest(endpoint_field),
            'path':{'start_grid':-2,'moves':[1,1,1,1]},
            'left_rectangle_upper':'1','known_unrestricted_game_lower':'3050023091/2147483648'}))
        report = verify(endpoint_field,witness)
        assert report['capture_expectation_upper'] == '1'
        assert report['independent_interpolation_samples'] == 4
    print(json.dumps({'status':'PASS','fixed_and_free_initial':True,
                      'exact_anchor_rounding_checks':3,
                      'independent_bigint_replays':2,
                      'time_zero_endpoint_attack':True},indent=2))


if __name__ == '__main__':main()
