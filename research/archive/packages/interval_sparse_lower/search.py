#!/usr/bin/env python3
"""Adaptive sparse-event Princess discovery; complete pricing is mandatory."""
from pathlib import Path
import json
import sys

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'packages/interval_lower_bundle'))
# Import under an explicit module name: this entrypoint is also named search.
import importlib.util
spec=importlib.util.spec_from_file_location('lower_bundle_search',ROOT/'packages/interval_lower_bundle/search.py')
bundle=importlib.util.module_from_spec(spec)
spec.loader.exec_module(bundle)
from backend import ClampedSparseMaster


def main():
    initial_routes=128
    if '--initial-routes' in sys.argv:
        at=sys.argv.index('--initial-routes')
        initial_routes=int(sys.argv[at+1]);del sys.argv[at:at+2]
    if initial_routes<1:raise ValueError('initial route count must be positive')
    if '--profile-grid' not in sys.argv:
        n=sys.argv[sys.argv.index('--n')+1] if '--n' in sys.argv else '256'
        sys.argv.extend(['--profile-grid',n])
    if '--n' not in sys.argv:sys.argv.extend(['--n','256'])
    bundle.InteriorMaster=ClampedSparseMaster
    # A latest-tie calendar can charge every vertex of a long flat trace.
    # One earliest-record calendar already supplies a valid support plane;
    # exact cached/complete separation will expose any new record choices.
    def add_earliest(master,path,table):
        plan,mass,coeff=master.calendar(path,table,latest=False)
        key=mass,tuple(sorted(coeff.items()))
        if key in master.seen:return 0
        master.seen.add(key)
        master.columns.append({'plan':plan,'mass':mass,'coeff':coeff})
        return 1
    bundle.Master.add=add_earliest
    def load_paths(master,table,paths,directory):
        cache=bundle.CachedPathPricing(master.n,master.D)
        sources=[]
        for path in paths:
            data=bundle.read_json(path)
            if master.n%data['n']:raise ValueError('response mesh must divide search mesh')
            count=cache.add_many(bundle.plans_from(data),source_n=data['n'])
            sources.append({'file':str(path),'sha256':bundle.sha256(path),
                            'n':data['n'],'new_physical_paths':count})
        endpoints=[{'start_grid':master.R,'moves':[-1]*(2*master.R)},
                   {'start_grid':0,'moves':[1]*master.R+[-1]*(2*master.R)}]
        for path in endpoints:
            cache.add(path);master.add(path,table)
        for path in cache.price(table,keep=min(initial_routes,len(cache)))['paths']:
            master.add(path,table)
        bundle.write_json(directory/'sources.json',{
            'sources':sources,'cached_physical_paths':len(cache),
            'initial_lowest_routes':initial_routes,
            'all_paths_retained_in_cached_separator':True,
            'latest_tie_calendars_seeded':False})
        return cache
    bundle.load_physical_paths=load_paths
    original_save=bundle.save_state
    def save(*args,**kwargs):
        original_save(*args,**kwargs)
        config=args[0]
        path=config.output/'manifest.json'
        data=json.loads(path.read_text())
        data['method']='Adaptive sparse-event lower search with exact closest-seed extension'
        data['field_class']='All legal full nodal Qout fields at the response grid; no frozen seed equality restriction'
        data['extension_source_sha256']=bundle.sha256(Path(__file__).with_name('clamp.py'))
        data['projection_source_sha256']=bundle.sha256(ROOT/'packages/interval_sparse_upper/master.py')
        data['initial_lowest_routes']=initial_routes
        data['calendar_tie_policy']='earliest record only; complete oracle unchanged'
        bundle.write_json(path,data)
    bundle.save_state=save
    bundle.main()


if __name__=='__main__':main()
