"""Exact query geometry for efficient-master discovery snapshots.

The efficient master retains event coordinates from older legal responses.
Its labels therefore must not be interpreted in a newly constructed bank-
only SurvivalCut model. This restores the supplied finite rational geometry.
"""
from bisect import bisect_left, bisect_right
from fractions import Fraction as Q

from survival_minimax import SurvivalCut


def efficient_profile_model(data):
    atoms=[dict(kind=a['kind'],parameters=tuple(map(Q,a['parameters'])))
           for a in data['atoms']]
    model=SurvivalCut(atoms,lexicographic=True)
    original_vertices={v for pair in model.routes for route in pair for u,v in route}
    original_levels={u for pair in model.routes for route in pair for u,v in route if u>=0}
    model.v=tuple(map(Q,data['query_v']))
    model.levels=tuple((Q(value),int(side)) for value,side in data['event_labels'])
    model.keys=model.levels
    assert model.v==tuple(sorted(set(model.v))) and model.v[0]==-1
    assert model.levels==tuple(sorted(set(model.levels)))
    assert original_vertices<=set(model.v)
    assert original_levels<={value for value,side in model.levels if side==0}
    assert all(side in(-1,0,1) for value,side in model.levels)
    bases=sorted({value for value,side in model.levels})
    assert model.levels==tuple((value,side) for value in bases for side in(-1,0,1))
    model.end=model.v[-1]
    model.bounds=[(bisect_left(model.keys,(max(0,v),0)),
                   bisect_right(model.keys,(v+2,0))-1) for v in model.v]
    first=model.keys.index((Q(0),0));model.bounds[0]=(first,first)
    last=model.keys.index((model.end+2,0));model.bounds[-1]=(last,last)
    model.query={v:i for i,v in enumerate(model.v)}
    model._unit_rewards=[None]*len(atoms)
    return model


def exact_profile_rows(data, model=None):
    model=efficient_profile_model(data) if model is None else model
    rows=[]
    for item in data['princess_mixture']:
        labels=item['labels']
        assert len(labels)==len(model.v)
        assert all(lo<=labels[i]<=hi for i,(lo,hi) in enumerate(model.bounds))
        assert all(a<=b for a,b in zip(labels,labels[1:]))
        values=tuple(model.levels[k] for k in labels)
        rows.append(model.row(model.atoms,values))
    return rows
