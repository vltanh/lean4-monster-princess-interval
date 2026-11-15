# Exact continuous record and center components

This directory contains rational algebra for the actual-record Bellman and
center-renewal constructions. A component replay is not by itself a global
Princess security certificate. The continuum proof dependencies are
[the record lift](../../../research/12-global-closure/FINITE_RECORD_BELLMAN_LIFT.md),
[center renewal](../../../research/12-global-closure/CENTER_RECORD_RENEWAL_CERTIFICATE.md),
and [finite post-center response](../../../research/12-global-closure/FINITE_POSTCENTER_RESPONSE.md).

| Component | Exact scope |
| --- | --- |
| `exact_quadratic_polytope.py` | Global quadratic minimum on a compact rational polytope in at most four variables; singular faces and implicit lower dimensions included |
| `eliminate_quadratic_interval.py` | Eliminate one bounded scalar decision from a parametric quadratic, returning rational quadratic candidates with polyhedral eligibility domains |
| `build_endpoint_tail_charts.py` | Exact first-endpoint sweep integral for all initial endpoint times in [0,2] and lower records in [0,1] |
| `build_center_excursion_charts.py` | Exact partial outward integral and interior record update for center-return triangles |
| `exact_center_renewal_envelope.py` | Complete finite-depth quadratic center recurrence with exact domain and domination pruning |
| `replay_center_renewal_paths.py` | Independent chronological integration of reconstructed physical routes |
| `exact_n1_precenter.py` | Complete free-start response for the full-width n=1 field, with exact candidate/domain exhaustion |
| `replay_n1_precenter.py` | Independent raw-CDF route integration and whole-interval comparison of the initial-position curve |

The objective convention for the first two components is
`constant + linear*x + x^T*hessian*x`, with a symmetric matrix. A constraint
`(a,b)` means `a*x <= b`. In scalar elimination the decision is the last
coordinate and all preceding coordinates are parameters. The output preserves
closed, possibly lower-dimensional domains; it does not require quadratic
winner regions to be polyhedra.

The chart builders accept expanded radial fields, compact Qout fields, and
normalized Princess artifacts containing a compact nodal profile. Their
interpolation width is always an explicit option; the default is full width
`1/2`. Changing this option defines a different law and carries no security
guarantee from the input artifact's original width.

At excursion height one, the chart's record is an interior trace. Actual
endpoint capture resets that record to zero and uses the direct endpoint-tour
branch. Confusing these branches invalidates a response certificate.

## Independent exact replays

Run from the repository root:

```sh
python packages/interval_global_closure/record_bellman/test_exact_quadratic_polytope.py
python packages/interval_global_closure/record_bellman/test_eliminate_quadratic_interval.py
python packages/interval_global_closure/record_bellman/test_chart_field_parser.py
python packages/interval_global_closure/record_bellman/build_endpoint_tail_charts.py packages/interval_clock_grid/grid_n2_princess.json /tmp/endpoint_tail.json --epsilon 1/4 --direct-replay
python packages/interval_global_closure/record_bellman/build_center_excursion_charts.py packages/interval_clock_grid/grid_n2_princess.json /tmp/center_excursion.json --epsilon 1/4 --direct-replay
```

The polytope tests compare against independent one- and two-dimensional
analytic optima and manufactured higher-dimensional cases. Scalar elimination
is compared against direct rational interval minimization at 3,060 parameter
fibers. Chart replay independently subdivides physical rays, evaluates the
common-threshold CDF, and integrates the chronological record. The finite
coverage and polynomial-branch proofs justify the continuum checks; sampled
values alone would not establish them.

## Complete first-grid center certificate

The [complete n=1 computation](../../../research/12-global-closure/EXACT_CENTER_ENVELOPE_N1.md)
uses all five layers required by the finite response theorem. Its 48
rational quadratic pieces describe the exact center continuation for
every time in [0,2] and both survival records in [0,1/2]. In particular,
the value from `(0,1/2,1/2)` is `79/64`. This is a fixed-field center
value, not the unrestricted game value.

```sh
python packages/interval_global_closure/record_bellman/exact_center_renewal_envelope.py packages/interval_global_closure/record_bellman/center_excursion_n1_fullwidth.json.gz packages/interval_global_closure/record_bellman/center_envelope_n1_exact.json.gz --depth 5 --verify --history-output /tmp/center_n1_history.json.gz
python packages/interval_global_closure/record_bellman/replay_center_renewal_paths.py packages/interval_global_closure/record_bellman/center_envelope_n1_exact.json.gz packages/interval_clock_grid/grid_n1_princess.json /tmp/center_n1_paths_replay.json --raw-history /tmp/center_n1_history.json.gz
```

Regenerate and byte-compare the input charts from the stated field first,
as detailed in the computation note and the dedicated CI job. The generator
repeats every exact candidate and pruning calculation, not merely the saved
hash comparison. The independent physical replay covers 297 routes, 3,886
affine integration intervals and 120 raw-versus-pruned checks.

## Complete continuous first-grid response

The [full n=1 computation](../../../research/12-global-closure/EXACT_N1_CONTINUOUS_RESPONSE.md)
adds the entire pre-center part and free Monster starting positions. With
`z=abs(initial_position)`, the exact cost is

\[
V_F(z)=\begin{cases}
79/64+z/32-15z^2/448,&0\le z\le7/8,\\
37/64+49z/32-57z^2/64,&7/8\le z\le1.
\end{cases}
\]

Its minimum is **39/32**, attained by the endpoint sweep. The proof covers
all six pre-center affine triangles, the actual endpoint branch and the
complete center continuation. In the physical boundary cell the construction
includes four alternating bang legs and a hold with every intermediate
vertex constrained to the legal triangle. Intermediate envelopes describe
continuations constrained to visit the center by time two; a separate
strictly larger cost bound excludes routes missing that deadline.

First regenerate and byte-compare both n=1 chart inputs. The center chart
check is given above; for the endpoint input run:

```sh
python packages/interval_global_closure/record_bellman/build_endpoint_tail_charts.py packages/interval_clock_grid/grid_n1_princess.json /tmp/endpoint_n1_charts.json --epsilon 1/2 --direct-replay
python -c "from pathlib import Path; assert Path('/tmp/endpoint_n1_charts.json').read_bytes() == Path('packages/interval_global_closure/record_bellman/endpoint_tail_n1_fullwidth.json').read_bytes()"
python packages/interval_global_closure/record_bellman/exact_n1_precenter.py --field packages/interval_clock_grid/grid_n1_princess.json --center packages/interval_global_closure/record_bellman/center_envelope_n1_exact.json.gz --center-charts packages/interval_global_closure/record_bellman/center_excursion_n1_fullwidth.json.gz --tail packages/interval_global_closure/record_bellman/endpoint_tail_n1_fullwidth.json --output packages/interval_global_closure/record_bellman/n1_precenter_complete.json.gz --complete --verify
python packages/interval_global_closure/record_bellman/replay_n1_precenter.py packages/interval_global_closure/record_bellman/n1_precenter_complete.json.gz packages/interval_global_closure/record_bellman/center_envelope_n1_exact.json.gz packages/interval_clock_grid/grid_n1_princess.json /tmp/n1_precenter_replay.json
```

The generator recomputes every candidate and pruning decision. The separate
replay checks 67 initial routes, 97 edge states, 1,989 exact affine integration
intervals and 29 exact polynomial comparisons over entire initial intervals.
The full fixed-field completeness proof supplies the all-response scope;
sampling alone would not do so. This small supplied field is not a proposed
unrestricted equilibrium and does not improve the current global bounds.
