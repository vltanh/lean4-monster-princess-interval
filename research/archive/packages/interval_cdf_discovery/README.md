# Joint ordered-CDF discovery

This package constructs a **complete ordered continuum law** while all
initial, incoming, outgoing, and post-wave parts move together. It is a
fixed-mesh discovery tool. Neither its finite-route optimum nor the saved
candidate is an unrestricted lower certificate or a matched equilibrium.

The later `snapshots/initial_inward_candidate.json` includes the full
existing-coordinate initial-inward family. It also has a **known exact
continuous-start exclusion**: a negative M1 route costs
`1.4232449162430754`, below its finite-pool minimum `1.4234540371285234`.
This continuation is a legal construction checkpoint, not a global
candidate that has passed all response tests. Its terminal slab is being
studied through source-corrected integral equations rather than further
mesh refinement.

The frozen `snapshots/constant_half_wait_candidate.json` is a legal field
with **known improving initial-inward attacks** below its finite-pool
objective. The strongest currently recorded one costs approximately
`1.42146653905` and has the simple existing-coordinate parameters
`a=13/16`, first inward `V=-3/4`, second outward `U=1`. Generic running
records independently reproduce that cost. A preceding continuous
signed-M3 search found cost `1.42276622099746` at reflected parameters
`a≈.55`, `V≈-.4375874`, `U≈.9840351`. The earlier pool did not exhaust
this same-half orientation.

`verify_frozen_attack.py` checks the simple rational-coordinate attack
exactly against both the original and repaired fields. It compares the
closed CDF formula with an independent signed unit-action computation;
both costs are strictly below `142147/100000`. The full exact rational
costs are retained by that verifier.

The field had survived the first independent capped capture-order probe:
32 positive quantiles, 287,744 search nodes, and whole-field route
re-evaluation found only an endpoint sweep at about `1.42347024348`.
The later attack shows why passing that capped probe is not a global
certificate. The frozen snapshot is retained as a construction checkpoint,
not as a successful unrestricted law.

## What is represented exactly

`joint_cdf_field.py` uses one mesh of 3,571 nodes and 6,936 triangles in
light coordinates `(U,V)=(t+r,t-r)`. Each triangle carries an affine
interior radial CDF. The inequalities `R_U>=0` and `R_V<=0` give an ordered
family of 1-Lipschitz radial quantile paths. Paths are at their endpoints
by time two. Exact contact uses the closed endpoint CDF equal to one and
the strict center CDF equal to zero; the stored endpoint value is the
interior trace. Initial center/endpoint atoms and a literal outgoing
time-one atom are excluded in this representation.

All initial and field values are optimized jointly. No old ordinary-tail
mass, first incoming map, cap rank, outgoing front, or upper density is
frozen. Paths may have multiple waves and interior speeds. In particular,
the frozen candidate's low-rank paths do not all start at speed `+1`.

The frozen candidate has two explicit constructive selections:

* On `0<=V<=U<=1/2`,
  `R(U,V)=lambda*U`, with
  `lambda=704044057/2500000000=.2816176228`.
* Every future endpoint-interior trace at `V>=15/16` is at most the
  center rank at `15/16`. That rank, its past-center maximum, and its
  future interior envelope all equal
  `81481882477/125000000000=.651855059816`.

The first selection makes every balanced triangle wholly inside the
early cone no better than center waiting. The second supplies the
candidate-specific hypothesis of the center-memory sweep theorem. These
local conclusions do not settle initial asymmetry or excursions through
the remaining curved slab.

`audit_snapshot.py` checks the realized rational field. All 6,936 triangle
transport cones, all 55 early-cone nodes, and all 16 future boundary
comparisons pass exactly. Coordinates are interpreted as their intended
rational mesh values within `1e-14` of the JSON floats; CDF values are
exact decimal multiples of `1e-12`.

Two optional late-turn derivative conditions were used during discovery.
They are **not exact properties of the frozen field** after solver
tolerances and rounding: their minimum slacks are `-1.396566e-6` and
`-1.279073e-6`. These residuals are recorded in the audit file. No exact
late-response conclusion is inferred from those imperfect inequalities.

The separate `snapshots/constant_half_wait_repaired.json` removes this
local numerical defect exactly. It mixes the CDF with the uniform-outward
law `R0(U,V)=max(0,-V)` at rational weight `1/1000000`, storing all values
as exact rationals as well as floats for response probes. Transport, the
scaled constant cone, and the scaled future-rank barrier remain exact.
Both optional late inequalities then hold strictly, with minimum slacks
`1.353435396566e-6` and `2.145928279073e-6`. The initial-inward attack
still has to be addressed; this repair supplies exact local shape
conditions, not an equilibrium.

The exact [continuous M1 start audit](../../research/10-turn-density/M1_START_AUDIT.md)
also checks every start between mesh coordinates. It partitions the frozen
field into 34 negative-start and 148 positive-start cells and tests all
stationary points. The minima are approximately `1.42325291845` and
`1.42328251252`, respectively. These are family audits of a specified
field, not game-value bounds; they also show that nodal start checks alone
miss smaller M1 costs.

## Costs and the finite pool

`RouteFunctional` integrates the running signed CDF records of any supplied
polygonal monster route. It evaluates the entire continuum field and gives
a supporting supergradient of its concave capture cost. The template
classes use the independently checked full-CDF identities to avoid weak
record selections on flat transport faces.

The frozen solve controls 17,131 routes on the same mesh:

| Family | Coverage |
|---|---|
| M1/M2 | 1,601 signed early/late routes, including selected first turns before crossing the center. |
| Opposite-half M3 | All 14,910 existing-base triples `abs(start)<=firstU<=secondV<=1`, with both initial signs. |
| Wait and two triangles | 610 existing-base choices `wait<=1/2`, `wait<=first_return<=1`, final return one, and both endpoint orders. |
| External separators | Ten fixed routes found against earlier complete fields, retained verbatim in `external_routes.json`. |

Its actual minimum over this finite pool is `1.4234654225724466`; the final
supporting-cut LP level is `1.423470243477793`, a residual gap of about
`4.82e-6`. These numbers are feasibility diagnostics, not game bounds.
The full same-half M3 domains have exact formulas and rational checks in
the turn-density package, but are not silently included in this pool.

The active dual support has approximate total masses `.810305` on M1,
`.171801` on M2, `.015278` on M3, and `.002598` on waiting/triangles.
Most waiting mass is a center wait followed by one nonzero triangle.
The constant-cone selection has a nonzero multiplier. Therefore these
LP multipliers are not already a continuous upper strategy.

## Full initial-inward continuation

The separate `initial_inward_*` snapshots retain a continuation on the
same mesh with 71,289 fixed routes. It adds all 54,145 legal
initial-inward/outward triples and thirteen previously discovered
continuous-family routes. Its final supporting-cut level is
`1.4234619451776183`; its actual finite-pool minimum is
`1.4234540371285234`. The remaining cut gap is about `7.91e-6`.

All physical transport and selection checks pass exactly. The early
constant density is `.28170124376`, and the future-memory rank at
`15/16` is `.651793830336`. The raw optional late inequalities have small
negative residuals; the separate rational mixture
`initial_inward_repaired.json`, with uniform-outward weight `1/200000`,
makes both inequalities strictly positive. All 71,289 route costs were
re-evaluated on that mixture, with minimum `1.4234593504089983`.

The exact M1 arrangement still finds lower costs between start knots:
`1.4232449162430754` and `1.423367215371144` for the original negative
and positive families, respectively. For the repaired law the minima
are `1.4232434250304151` and `1.4233682961819143`. A separate continuous
signed-M3 search found about `1.4233085909`, degenerating to an existing
M2 family. The capped all-order search found only an endpoint sweep;
the exact M1 exclusions show why that search result is not a certificate.

The nonzero dual rows are retained in `initial_inward_duals.json`.
The raw initial-inward family mass `.519252` consists mostly of
zero-length M1/M2 duplicates. Genuine initial-inward prefixes carry
`.00262456` on interior second turns and `.000396995` on endpoint
second turns. They mostly use second `U=1`, with starts around
`.45`–`.55` and above `.875`. Genuine opposite-half M3 mass is
`.00113395`. These are diagnostic support weights, not a normalized
unrestricted upper law; the constant-cone selection still has a nonzero
multiplier.

The continuation changes the free initial attachment materially. Several
branches that formerly began at speed `+1` now have interior speeds around
`.91`–`.98`. The post-one incoming flux remains approximately
`J0=.550876`, shared by both signs of `V`. Therefore the conditional
ordinary terminal asymptotic coefficient is about `(3+J0)/2=1.775438`;
the older no-post-wave coefficient `1.5` is not appropriate for this
field. This asymptotic observation does not establish the required
terminal attachment.

## Reproduce or restart

Requirements are Python, NumPy, and SciPy. From the repository root, an
exact physical/selection audit is:

```bash
python packages/interval_cdf_discovery/audit_snapshot.py \
  packages/interval_cdf_discovery/snapshots/constant_half_wait_candidate.json
```

Evaluate the frozen route pool without an optimization step:

```bash
python packages/interval_cdf_discovery/joint_cdf_collocation.py \
  --maxiter 0 \
  --resume packages/interval_cdf_discovery/snapshots/constant_half_wait_candidate.json \
  --extra-routes packages/interval_cdf_discovery/external_routes.json \
  --two-interior-pool --constant-early-cone .5 \
  --terminal-center-barrier .9375 --wait-two-triangle-pool \
  --tag frozen_check --output-dir /tmp/interval-cdf-discovery
```

For a new continuation, use a new output tag, set `--maxiter 35`, and add
new independent routes to `--extra-routes`. Preserve all previous routes.
The frozen snapshot should not be overwritten. The earlier failed
`joint_cdf_m3_full_field.json` snapshot can also seed the constant-cone
construction if the geometry selection itself is to be reproduced.

Default outputs contain compact complete fields and nonzero dual rows.
Every omitted multiplier is zero, and all active routes retain their
exact vertices and labels. `--full-diagnostics` additionally saves all
route costs, raw LP values, every zero dual row, and every cost-cut
coefficient. Those full diagnostics can be large and are regenerated
rather than repeated in the checked-in snapshots.

The options `--no-positive-v` and `--no-negative-v` separately disable the
optional sufficient late inequalities. `--center-unimodal-peak` is another
labelled construction restriction; it was not used for the frozen
candidate. `--constant-early-cone` preserves its affine relation during
the integer transport repair rather than only to floating LP tolerance.
`--initial-inward-pool` adds all 54,145 legal existing-coordinate triples
for the initial-inward/outward orientation, including post-one interior
turns and the endpoint faces. That continuation is distinct from the
frozen failed pool recorded above.
`--lp-method highs-ipm` selects the interior-point LP solver for the larger
pool; it does not change any constraints or the underlying field class.

The full initial-inward continuation can be reproduced without changing
the mesh:

```bash
python packages/interval_cdf_discovery/joint_cdf_collocation.py \
  --maxiter 35 \
  --resume packages/interval_cdf_discovery/snapshots/constant_half_wait_candidate.json \
  --extra-routes packages/interval_cdf_discovery/external_routes.json \
    packages/interval_cdf_discovery/additional_family_routes.json \
  --two-interior-pool --constant-early-cone .5 \
  --terminal-center-barrier .9375 --wait-two-triangle-pool \
  --initial-inward-pool --lp-method highs-ipm \
  --tag initial_inward --output-dir /tmp/interval-cdf-discovery
```

The independent separator is a separate implementation:

```bash
python packages/interval_turn_sheet/probe_cdf_field.py \
  packages/interval_cdf_discovery/snapshots/constant_half_wait_candidate.json \
  --quantiles 32 --nodes 300000 --seconds 20 --polish-seconds 20 \
  --output /tmp/interval-cdf-discovery/independent_probe.json
```

It uses finite quantiles to discover routes, then evaluates and polishes
those routes against the whole field. The finite-quantile minimum is never
substituted for the complete-field payoff.

## Exact identities and remaining work

### Endpoint component and analytic incoming correction

`endpoint_joint_component.py` solves the endpoint obstacle and initial
positive-M1 front together on the existing 13 tail coordinates. The
`endpoint_joint_i1_*` snapshots additionally retain the fixed-U1 inward
inequality. Every exported field passes the exact transport cones, but
the snapshots are feasibility diagnostics, not unrestricted lower bounds.

The negative-M1 defect between the last coordinates is repaired by an
actual continuous incoming transformation, defined in
`snapshots/endpoint_two_band_field.json`. Its two rank-band contributions
use exact quadratic inverse envelopes and an initial-front cap. The
implementation is `terminal_band_warp.py`; `WarpedField` evaluates the
algebraic field, rather than interpolating sampled warp values.

The exact whole-cell continuation gates are reproduced by
`audit_postone_branch_gates.py`. They pass on the entire terminal
triangle and are preserved by the analytic correction. A separate causal
theorem proves that every monster with absolute initial position at least
`255/256` has nondecreasing payoff under this correction, regardless of
its later turns. Neither result supplies missing inequalities for the
base field.

`audit_band_warp_columns.py` independently integrates the remaining
outer coupling. It records a definite loss in some coarser positive-M1
and positive-M2 costs, so the current corrected field is still attacked.
Its quadrature errors are numerical estimates, not exact enclosures.
`verify_warp_outer_column.py` separately proves a strict outer failure
by exact rational inverse brackets and a positive integral lower bound.
The construction, failures of narrower repair bands, and proof scopes
are explained in `research/10-turn-density/JOINT_ENDPOINT_COMPONENT.md`
and `INCOMING_WARP_RESPONSE_PRESERVATION.md`.

The related notes are
`research/10-turn-density/POSITIVE_TURN_SHEET.md`,
`TWO_INTERIOR_TURN_CDF.md`, `CENTER_WAIT_TWO_TRIANGLES.md`, and
`CENTER_MEMORY_SWEEP.md`. Their independent verifiers include:

```bash
python packages/interval_turn_density/verify_positive_cdf_sheet.py
python packages/interval_turn_density/verify_two_interior_cdf.py
python packages/interval_turn_density/verify_wait_two_triangles.py
python packages/interval_cdf_discovery/verify_frozen_attack.py
python packages/interval_cdf_discovery/audit_m1.py \
  packages/interval_cdf_discovery/snapshots/constant_half_wait_candidate.json
```

They establish capture identities and local conditions. A completed
solution still needs an unrestricted response certificate for the actual
field or an analytically reconstructed law, a compatible continuous upper
law, and exact global indifference/attachment conditions. The saved phase
and dual files are evidence for that construction; they are not a proof
that those remaining conditions hold.
