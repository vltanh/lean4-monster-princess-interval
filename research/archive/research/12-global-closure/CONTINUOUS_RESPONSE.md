# Global responses to a supplied continuous ordered law

Two complementary computer-assisted procedures are implemented in
`packages/interval_global_closure/continuous_response_*`.

1. Exact finite-quantile capture-order search supplies an unrestricted
   response interval for a specified continuous law, using a uniform
   discrepancy theorem. It also supplies legal attacking routes.
2. A physical light-coordinate node search prices every edge against the
   actual continuous CDF. It efficiently finds routes with no prescribed
   number of reversals. Its floating interpolation is used for discovery;
   the returned routes are independently rescored with rational arithmetic.

Neither procedure asserts that the supplied princess law is an equilibrium.
The second procedure has already found a substantial omitted response to
the whole-field construction, described in Section 5.

## 1. Common finite horizon for response values

Let an ordered family of legal princess paths be absorbed at the two
endpoints by time `H`. Here absorption means that every path is constant at
either `-1` or `+1` after `H`. The existing class has `H=2`; the extended
class supports `H=3`.

Set `T=H+4`. Every monster is dominated, as a response to this law, by one
which completes capture by `T`: keep its prefix through `H`, then visit the
endpoints directly in the order in which the original continuation first
visits them. If an endpoint is never visited, place it last. At time `H`
all remaining princesses are stationary endpoints, so this modification
does not delay any first contact. The first endpoint is at most two time
units away and the other is two further time units away. The argument
preserves a specified initial monster position when one is imposed.

Consequently the infimum of full expected capture time equals the infimum
of capture time truncated at `T`. This is a response theorem for an
endpoint-absorbed law, not a proof that every optimal princess law must
have a finite absorption horizon.

## 2. Uniform quantile transfer, including atoms

Write the positive radial quantile paths as `p_q`, `0<q<1`, and reflect
with probability one half. For an integer `n>=1` and phase `0<theta<1`,
take the radial ranks

```
q_i=(i+theta)/n,       0<=i<n,
```

and give their positive and negative copies weight `1/(2n)` each. Put
`rho=max(theta,1-theta)`. At every time and position, both the strict and
closed CDFs of this empirical law differ from the continuous law by at most
`rho/(2n)`. This is the usual equally spaced rank-count bound, applied to
both reflected halves. It remains valid at center and endpoint atoms.

For any continuous monster path `m`, the ranks it has encountered by time
`t` form an interval. Its remaining left mass is the infimum, over the
prefix, of the strict CDF along `m`; its remaining right mass is one minus
the corresponding supremum of the closed CDF. Thus

```
S_m(t)=inf_{s<=t} F^-(s,m(s)) + 1-sup_{s<=t} F^+(s,m(s)).
```

Changing each CDF trace by at most `rho/(2n)` changes survival by at most
`rho/n`. Integrating to the common horizon gives the uniform estimate

```
|J_T(m)-J_{n,theta,T}(m)| <= T*rho/n.                 (1)
```

The estimate holds simultaneously for every monster: arbitrary start,
waiting, any speed in `[-1,1]`, and any number of reversals. There is no
first-capture continuity assumption.

If an exact finite-law search proves

```
B <= inf_m J_{n,theta}(m) <= C,
```

then (1) and Section 1 prove

```
B-T*rho/n <= inf_m J(m) <= C+T*rho/n.                (2)
```

The actual route returned by the search is rescored against the exact
continuous field, usually giving a much better upper endpoint than (2).
For midpoint ranks `theta=1/2` and `N=2n` reflected paths, the error is
`T/N`. Bounds from a fixed-start search apply to that fixed-start response
only. They are deliberately excluded from the unrestricted lower endpoint
in `continuous_response_probe.py`.

### Exact extraction from a complete field

`continuous_response_extract.py` reads rational nodal values, or the exact
decimal rationals in a discovery field. It checks the complete declared
mesh, all triangle transport inequalities `R_U>=0`, `R_V<=0`, normalization,
and the absorbing boundary. It then intersects each quantile level with
every affine triangle using rational arithmetic. Boundary gaps are filled
at the center or endpoint; the resulting paths are checked for speed,
arena constraints, and order. A level equal to a nodal value is rejected
explicitly so that a degenerate contour is never silently chosen.

For every extracted law, the output records the source SHA-256, exact
ranks, weights, path vertices, absorption horizon, and error in (1).

## 3. Exact finite response and unfinished-frontier certificates

`continuous_response_search.cpp` uses GMP rationals. It applies the
capture-order theorem from `research/07-structural-audit/CAPTURE_ORDER.md`,
not a fixed-turn restriction. A free monster can start on a princess's
initial position: follow the original first-captured princess from time
zero to the original first contact, and then resume the original route.
This captures that princess earlier and delays no other contact.

At any state the captured ordered paths form a contiguous index interval.
The next new capture can be taken to be the earliest possible contact
with its immediate left or right neighbor. Pursue that neighbor at unit
speed; after the earlier contact, following its legal path until the old
contact would permit the old continuation without delaying anything.
Repeating this domination gives the complete binary capture-order search.

The implementation:

- normalizes every simultaneous contact before branching;
- computes exact earliest contact by inverting the monotone characteristic
  `t-d*p(t)` for direction `d`;
- uses an independent earliest-contact time for every remaining target as
  an admissible lower bound on a state's remaining cost;
- uses exact time/cost dominance for the same captured interval and anchor
  path;
- completes a one-sided remainder by direct pursuit, and an endpoint-only
  remainder by the better endpoint order;
- returns the minimum pending frontier bound when a node budget is
  exhausted, rather than calling a stopped search complete.

If two states have the same captured interval and anchor path, the earlier
state can follow that anchor to the later state. Any extra captures on the
way only help. Therefore an earlier state with no larger accumulated cost
dominates the later state. All comparisons are rational; no numerical
tolerance is used in search or pruning.

The search can also retain an arbitrary fixed initial position using
`--start rational`. It then starts with the appropriate empty captured
interval and branches toward the first left or right target. The subsequent
response remains unrestricted. Returned routes are completed through both
arena endpoints so they are also valid finite-horizon continuum attacks.

### Executed independent checks

`continuous_response_verify.py` compares the completed search with the
independent unpruned mask oracle in `interval_exact_reduction/exact_oracles.py`.
Three small laws cover actual field quantiles, center coalescence and
splitting, and absorption at time three. Fixed-center responses are checked
with a separate unpruned segment-intersection search. Zero-budget runs are
checked to bracket the independent optimum.

For the actual 32-path midpoint law, the verifier additionally checks every
capture with the independent `first_meeting` routine, 1,464 interior
quantile-level identities, 42 center-atom inequalities, and 48 endpoint-atom
inequalities. Results are recorded in `continuous_response_verification.json`.
The 32-path value for `initial_inward_repaired.json` is about
`1.337635600492566`; its returned route costs about `1.4233805893388332`
against the continuous law. This sizeable difference explains why simply
solving a small discrete law is not a continuum best-response certificate.

## 4. Physical node routes with continuous capture costs

The second method avoids replacing the princess law by initial point atoms.
It uses the light coordinates `U=t+x`, `V=t-x` and the complete field's
nonuniform coordinate axes. The axes are closed under the arena and time
faces. Nodes satisfy `0<=t<=H`, `|x|<=1`; a move to the adjacent node in the
positive `U` direction is a physical unit-speed right leg, and a positive
`V` move is a physical unit-speed left leg. Adjacent center nodes also
have a stationary edge, representing an exact wait at `x=0`. The directed graph is finite,
but paths may turn at every visited node. No externally chosen number of
reversals is imposed.

At a node retain the uncaptured left and right rank masses `a,b`. On a
right leg, `G(t)=1-F^+(t,m(t))` is nonincreasing and only `b` can decrease.
Writing `b'=min(b,G(end))`, the absolute capture-time contribution of that
leg is

```
end*(b-b') - integral_start^end (b-G(t))_+ dt.         (3)
```

The left formula uses `G=F^-` and `a`. Formula (3) follows by integrating
the capture measure by parts. All affine pieces of `G` are extracted from
the field, so its hinge integral is explicit. The open-leg limiting trace
is used in the integral, while the exact strict/closed end trace is used
in `b'` or `a'`. A center or endpoint atom is therefore charged at its
actual contact time, including when it lies at a leg endpoint.

On a center-wait edge the common trace
`g(t)=(1-R(t,t))/2` is affine. Both surviving records have the update
`q'=min(q,min(g(start),g(end)))`; the new capture moment is (3), with
the running minimum of `g`. If `g` increases there is no new capture.
Both left and right contributions are charged. Exact waiting matters
when the field has center atoms: a fixed finite zigzag grid must not be
assumed to reproduce every first contact of a waiting monster.

`continuous_response_grid.cpp` runs backward dynamic programming on a
64- or 128-bin record grid. It interpolates the continuation value to
guide route selection. These computations use floating arithmetic and
are labelled attack discovery, not an unrestricted lower certificate.
The geometry and returned routes are rational. For every decoded route,
`continuous_response_grid.py` independently sums (3) with Fractions and
checks equality with survival integration and the full-route scorer.
Unit-only routes use `ExtendedExactField.unit_route_payoff`; mixed routes
use the exact extension in `continuous_response_cost.py`. It also tries
both endpoint completions after every discovered
turning prefix. This can remove short excursions caused by interpolation
without assuming that such excursions are always dispensable.
Every output is truncated at its second distinct endpoint visit, when
continuity ensures that all princess paths have been encountered.

`continuous_response_grid_verify.py` independently checks two time-three
fields whose whole-center-wait payoffs are exactly `1/2` and `7/8`. The
latter has new center arrivals after time one. Its layer-cake integral,
decoded node moments, mixed full-route costs, and every endpoint-prefix
completion agree exactly. Results are in
`continuous_response_grid_verification.json`.

The callable interface is `Geometry(data,bins)`, followed by `write`,
`rescore`, and `prefix_completions`. The command-line interface is:

```
python packages/interval_global_closure/continuous_response_grid.py FIELD \
  --bins 64 --route-count 8 --all-prefixes \
  --work SCRATCH_DIRECTORY --output REPORT.json
```

The report contains all unique exact rescored attacks in `attacks` and
their minimum in `best_attack`. It is suitable for a whole-CDF exchange
loop: synthesize the entire legal field, run the global route separator,
add the returned physical routes, and synthesize again.
Every distinct endpoint completion is included by default; the optional
`--best-prefix-only` returns just the best completion of each decoded route.
Center-wait edges are included by default; `--unit-only` disables them.
The callable `prefix_completions` retains its default single-best result;
pass `all_routes=True` to obtain its full list.

### Global adaptive record knots

The optional `--adaptive-records ROUNDS` keeps the same physical node
graph and replaces the uniform record coordinates by one global set of
rational knots. It starts with the uniform knots and every initial CDF
survival value. A supplied same-field `--seed-attacks REPORT` can add the
carried records of its best exact routes and preserve an earlier adaptive
knot set.

Along a unit run, the record which changes is either its previous value
or the next node's CDF bound. Every node includes its own bound as the
last grid coordinate. The other record is constant from the initial
position or the last turn. Thus adding those carried values as global
knots removes interpolation at every state along that entire decoded
route. Center waits update both records; the records retained after a
wait are added in the same way. The next round may select a different
route, whose carried records are then added globally. These are additions
to the whole dynamic program, not extra restrictions on candidate paths.

There are only finitely many nodal CDF records. In exact arithmetic,
eventually including all of them eliminates record interpolation on every
reachable node path. The implementation remains a floating discovery
program and does not turn numerical agreement into an exact lower
certificate. It records the difference between its guide estimate and
the best exactly scored attack, every knot set, the round limit, and a
state-count memory gate. Each completed round also writes a reproducible
scratch checkpoint before continuing.

The nonuniform implementation was independently checked on all 97
complete routes of an 18-node graph. With every nodal record included,
its numerical value agreed with the exact exhaustive value `1/2`.
On frozen `continuum_complete_h3_iter_01.json`, an independent 128-bin
audit found cost `1.4211463110867124`, below the 64-bin response
`1.4229844183987477`. The initial adaptive pass improved the exact attack
to `1.4211227645876614`; its first four rounds raised the guide estimate
from `1.4153113316063806` to `1.4188172156145975` with only 135 to 149
global knots. Continuing from those knots closed the numerical finite-node
gap: with 161 knots and 84,064,397 states, the guide value was
`1.4210347274776596`, and an exactly scored four-interior-turn route cost
`1.4210347274776594`. The final knots, routes and history are in
`continuous_response_grid_h3_iter01_adaptive_complete.json`.

This closes the measured numerical record-interpolation gap on the finite
physical node graph. It is not an all-continuous-monster certificate, and
floating agreement is not an exact lower bound. The remaining physical
geometry requires a separate global argument or subsolution certificate.
The final same-field report can seed a one-round reproduction with
`--seed-count 0`; `--seed-routes` accepts routes from another field but
recomputes their costs and carried probabilities on the current field.

## 5. An executed whole-field separation

The frozen field `continuum_free_candidate_12.json`, SHA-256
`515cc2541dad42983b76fb411986ff69adcec7a08f0990235f455c6fb05aaa89`,
had minimum approximately `1.42355500174` on its 17,862-route construction
bank. The physical node search used 9,385 nodes and 7,047,877 record states.
Its decoded routes included a six-interior-turn attack costing
`1.4151895867174151`. Completing an earlier turning prefix improved this
to the following two-interior-turn route.

Let

```
a=9/16,       v=-21/40,       u=262145/262144.
```

Start at `a`, move left along `U=a` until `V=v`, move right along `V=v`
until `U=u`, then move left to `-1` and right to `+1`. Its vertices are

```
(0,a), ((a+v)/2,(a-v)/2), ((u+v)/2,(u-v)/2),
(u+1,-1), (u+3,1).
```

Its exact continuous payoff is

```
555099926958200233389716470214185333481
--------------------------------------------------
392575871405919815430307840000000000000
```

or approximately `1.41399400062525`. Holding the same first start and
inward turn but replacing `u` by `1` gives about `1.4235725061855111`.
The omitted response lies just above `U=1`, in a thin native field layer.
This was found by the whole-domain search, without assuming that a
two-turn family was complete. It rejects this particular field as a
matching lower strategy; it does not improve an upper guarantee against
all princess laws or disprove the separately certified earlier lower
bound. Exact routes, moments, and source identity are stored in
`continuous_response_grid_h2_12.json`.
