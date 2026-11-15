# Sparse charged-event physical upper discovery

The [projected-order proof](../../research/12-global-closure/SPARSE_CHARGED_EVENT_QOUT.md)
removes uncharged spacetime variables from the Qout master. It preserves
the fixed-calendar optimization exactly. All numerical LP values are
discovery estimates; physical laws are accepted only by integer replay.

`master.py` supplies a persistent adapter for the existing route/calendar
master. The first solve uses IPM with crossover, then warm simplex. New
charged nodes and valid order edges are appended without losing the basis.
The adapter also reconstructs a full feasible integer field for separation.
That field has no lower certificate until the complete response oracle runs.

```sh
python packages/interval_sparse_upper/test_projection.py
python packages/interval_sparse_upper/make_certificate.py packages/interval_discovery_certificates/monster_mutations_n128.physical.json.gz --output /tmp/sparse-retained
node packages/interval_sparse_upper/sparse_certificate.cjs /tmp/sparse-retained.sparse.json
```

The second command reproduces the retained exact upper on a smaller graph.
It accepts either an existing physical law or a floating master checkpoint.
For checkpoints, largest-remainder rounding creates exact rational weights;
the Node replay checks the resulting actual paths and both causal clocks.
Each supplied sparse order edge is validated geometrically. Omitting an
edge can only weaken the upper, so certificate acceptance does not trust
the projected graph generator's completeness.

`SparseMaster.solve` and `solve_existing_master` provide floating discovery
only. `make_certificate.py` and `sparse_certificate.cjs` produce and check
unrestricted **upper** certificates. None supplies a Princess lower from a
finite set of observed Monster routes.
