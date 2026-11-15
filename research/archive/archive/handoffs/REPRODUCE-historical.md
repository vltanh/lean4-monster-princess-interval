# Reproduce the available exact checks

## Exact finite grid values and constructive Princess extraction — 2026-11-13

~~~sh
node packages/interval_clock_grid/verify_grid.cjs packages/interval_clock_grid/grid_n1_certificate.json
node packages/interval_clock_grid/record_pricing.cjs packages/interval_clock_grid/grid_n1_certificate.json
node packages/interval_clock_grid/verify_grid.cjs packages/interval_clock_grid/grid_n2_certificate.json
node packages/interval_clock_grid/record_pricing.cjs packages/interval_clock_grid/grid_n2_certificate.json
node packages/interval_clock_grid/verify_grid.cjs packages/interval_clock_grid/grid_n3_certificate.json
node packages/interval_clock_grid/record_pricing.cjs packages/interval_clock_grid/grid_n3_certificate.json
node packages/interval_global_closure/verify_randomized_interpolation.cjs
node packages/interval_clock_grid/verify_princess_extraction.cjs packages/interval_clock_grid/grid_n3_certificate.json packages/interval_clock_grid/grid_n3_princess.json
~~~

The module bodies and supplied witnesses passed these exact operations in the
available JavaScript runtime. The credit DAG and physical-record algorithms
independently certify \(U_1=47/32\), \(U_2=4893/3376\), and
\(U_3=3153038167/2187120435\). The extraction replays the finite dual,
regenerates the full rational CDF description, and checks it against the saved
artifact. The independent common-threshold regression checks the construction
for grids 1 through 4 and three positive rational threshold widths.

To produce a Princess law with a chosen positive interpolation width:

~~~sh
node packages/interval_clock_grid/extract_princess.cjs packages/interval_clock_grid/grid_n2_certificate.json 1/100 /tmp/grid_n2_princess.json
~~~

Its guaranteed security is \(U_n-1/(2n)-\varepsilon/(2n)\); this is distinct
from the stronger value-only enclosure \(U_n-1/(2n)\le V\).
The [proof](research/12-global-closure/CONSTRUCTIVE_PRINCESS_GRID_DUAL.md)
covers all continuous Monster responses. Finite sampling checks are
implementation regressions, not substitutes for that proof.

A focused GitHub Actions workflow replays these certificates and compiles
the new integer-lattice verifier with its independent exhaustive Fraction
regression:

~~~sh
python3 packages/interval_global_closure/lattice_lower/test_integer_lattice.py
~~~

At this commit the C++/Python regression is awaiting its first native CI run.
Its draft status is retained until that execution succeeds. The standalone
NumPy field sampler has not yet been run. No new global lower bound is
claimed from the lattice implementation.

## Effective finite reduction: exact quantization replay — 2026-11-13

~~~sh
python packages/interval_global_closure/verify_common_quantization.py
~~~

This standard-library replay passed natively before the compute environment
became unavailable. It checks 3,615 exact rounding identities, 32 physical
clock repairs (including 18 earlier endpoint arrivals), 56 legal simultaneous
jump fills, 11 examples requiring the full half-mesh buffer, 400 transported
matching containments, 15 center collapses, and four joint integer-calendar
decompositions. The recorded result is
[common_quantization_replay_report.json](packages/interval_global_closure/common_quantization_replay_report.json).

The [quantization theorem](research/12-global-closure/EFFECTIVE_FINITE_UPPER_REDUCTION.md)
proves \(U_n-1/(2n)\le V\le U_n\). The
[occupancy theorem](research/12-global-closure/POLYNOMIAL_CLOCK_GRID_LP.md)
gives an equivalent rational LP with \(O(n^4)\) states, arcs and matching
variables. The exact fixtures check the constructions; the measure-level
proof establishes the unrestricted claim. No finite exact termination or
Lean compilation is asserted.

## Two-run continuation regression — 2026-11-13

```sh
python packages/interval_global_closure/verify_two_run_continuation.py
```

This standard-library exact replay checks the scalar two-run theorem against
chronological record integration: 4,840 directional words, 1,200 concave
continuations, 26 rational vertex reductions, 12 Hessian identities, and
12 terminal-excursion identities. The theorem is applied to interior
characteristic cells; boundary cells retain the earlier five-piece rule.
[Proof and scope](research/12-global-closure/TWO_RUN_AFFINE_CELL_WITH_CONTINUATION.md).

The independently reviewed [sticky-density proof](research/12-global-closure/STICKY_CDF_DENSITY.md)
uses a pathwise stopping and regularization argument. It does not infer
value-density from a numerical mesh experiment. Neither result changes
the retained global numerical interval or supplies a Lean proof.


## Sharp outward cutoff and finite affine-CDF response — 2026-11-13

```sh
python packages/interval_global_closure/verify_sharp_outward_horizon.py
python packages/interval_global_closure/verify_four_leg_record_response.py
```

Both commands passed natively. The first checks 72 exact physical cases,
including zero radius at the cutoff, initial co-location, survivor-order
capture comparisons, and endpoint completion. The second compares direct
first-visit integrals to the full quadratic formula, checks every Hessian
entry, compresses 23 rational polytope vertices to four directional legs,
reproduces the strict three-leg counterexample, and checks nine actual
strict/inclusive endpoint projections.

The [horizon proof](research/12-global-closure/SHARP_OUTWARD_HORIZON_REDUCTION.md)
gives outward time 2, absorption time 3, normalized Monster completion 6,
and attained full-matching completion 8. The [cell proof](research/12-global-closure/FOUR_LEG_AFFINE_RECORD_RESPONSE.md)
and [finite quadratic-program reduction](research/12-global-closure/BOUNDARY_CELL_RECORD_PROJECTION.md)
cover arbitrary turns against any supplied rational characteristic P1 CDF.
No exhaustive global QP enumeration or optimal-CDF mesh bound is claimed.


## Finite analytic-exit lower certificate and exact replay — 2026-11-13

```sh
python packages/interval_global_closure/analytic_exit/replay_certificate.py packages/interval_global_closure/analytic_exit/coarse_characteristic_certificate.json
python packages/interval_global_closure/analytic_exit/test_replay.py
```

Both commands passed natively. The first returns exact lower
`2677462523/2000000000`, checking 105,733 rational analytic inequalities,
804 direct tail line integrals, all endpoint/queue/time polar guards,
and exact characteristic-mesh coverage and symmetry. It uses only the
Python standard library and never imports a floating discovery matrix.
Input SHA256:
`39da8088fbe2aa7e19051aa34f96083b25bf683cbea8ddcaf579b27eb5eba781`.
The second verifies the static-endpoint closed-form potential, 150
constant/uniform-CDF tail integrals, and rejection of a derivative-preserving
potential shift that violates the endpoint boundary.

The [potential theorem](research/12-global-closure/ANALYTIC_EXIT_POTENTIAL.md)
explains why this certificate covers every Monster path. Its value is below
the retained best lower bound. The [completeness proof](research/12-global-closure/FINITE_POTENTIAL_HIERARCHY_COMPLETENESS.md)
proves that finite rational certificates with absorption horizon 3 approach
V, using the sharp outward-time reduction; the displayed operational fixture
uses that same horizon. No finite exact
termination, optimum certificate, Lean compilation, or new game bound is claimed.


## Global full-pressure-matching normal form — 2026-11-13

```bash
python packages/interval_global_closure/verify_global_pressure_localization.py
```

Expected: exact fractional cycle deficiency `1/2 -> 3/8`, zero propagated
flow in an unrelated closed cycle, 38 atomic-front cumulative checks,
44 physical boundary-turn checks, protected negative-tail checks, and
exact conservation of the bound.
The [attainment proof](research/12-global-closure/GLOBAL_ZERO_DEFICIENCY_ATTAINMENT.md)
establishes the full unrestricted identity `V = min_{D=0, H=9} E tau_-`;
these finite rational checks verify its formulas and do not replace that
argument. This theorem does not evaluate the infimum or change either
current numerical bound. No Lean compilation is claimed.


## Current strongest upper — full ordered-CDF discovery

```sh
node --stack-size=16384 packages/interval_global_closure/verify_full_order_upper.cjs
```

This command passed natively. It checks the rational 241-pair physical
law, computes its complete Princess response using integer max flow,
and replays the resulting flow on a rebuilt graph. It returns exactly
`1140799301969009059644426513/800000000000000000000000000`.
The graph has 75,268 nodes, 191,435 arcs, and 83,601 positive-flow entries.
The older common-warp commands below remain valid checks of historical,
weaker bounds. [Proof and scope](research/12-global-closure/FULL_ORDER_CDF_UPPER_CERTIFICATE.md).

## Independent continuous clock and matching replay

```sh
python packages/interval_global_closure/replay_continuum_clock_certificate.py packages/interval_global_closure/reweighted_physical_clock_certificate.json.gz
```

This standard-library-only command rebuilds the 241 reflected path pairs,
482 oriented paths, and 203 common light-coordinate knots. Its native
replay checks 85,268 physical causal prefixes, 12,214 exact matching-flow
edges, every source and target capacity, and all three residual front
cells. It verifies the same upper as the max-flow oracle, then the exact
hypotheses and parameters of the
[continuum completion](research/12-global-closure/ENDPOINT_FRONT_DEFICIENCY_COMPLETION.md).
The input includes the complete rational physical law and requires no
optimizer, saved numerical matrix, or external discovery checkpoint.

## Exact horizon and sufficient physical-clock lift — 2026-11-13

```sh
python packages/interval_global_closure/verify_exact_horizon_reduction.py
python packages/interval_global_closure/verify_finite_state_clock_lift.py
```

Both commands passed with exact rational arithmetic. The first checks
98 Monster paths against 13 reflected radial pairs, including 2,106
outward contact comparisons, 2,106 common endpoint-tail normalizations,
and 162 exact two-tour formulas. The second checks 120 clock pairs,
6,298 state/control segments, 1,200 strict-pressure projections, and
40 continuous two-sweep inert-mass/contact-germ cases. It verifies
physical horizon 7, clock mass 7 each, and graph horizons 21 and 24.

The corresponding universal results are the
[horizon theorem](research/12-global-closure/GLOBAL_EXACT_HORIZON_REDUCTION.md)
and [physical lifting theorem](research/12-global-closure/FINITE_STATE_PHYSICAL_CLOCK_LIFT.md).
These fixture tests support the analytic proofs; they do not enumerate
the continuum, certify a finite equilibrium classification, or constitute
a Lean check. [Fixed-template verification](research/12-global-closure/FINITE_GLOBAL_CERTIFICATE_SYNTHESIS.md)
is an analytic reduction to exact real-algebraic feasibility; no matching
optimal template or quantifier-elimination run is claimed.

## Native proof audit and tight upper replay — 2026-11-13

```sh
python packages/interval_uniform_reduction/exact_response.py packages/interval_uniform_reduction/princess_strategy.json
node --stack-size=16384 packages/interval_common_warp/verify_upper_warp_tight.cjs
python packages/interval_global_closure/verify_symmetric_quantile_ties.py
python packages/interval_global_closure/verify_eulerian_relaxation_gap.py
```

The lower response returned exactly
`36290299773897097/25600000000000000` after 48,228 complete search nodes.
The tight upper returned exactly
`57045188913812444387410009/40000000000000000000000000`.
Its dedicated verifier checks the stored exact flow/cut and physical
routes, then independently recompiles the actual warped geometry and
matches all 53,588 rational reward coefficients. The reproducible result
is [upper_warp_tight_replay.json](packages/interval_common_warp/upper_warp_tight_replay.json).

The quantile regression exhibits the old reflection failure at a CDF
plateau rank and checks the corrected two-trace construction, including
physical first contacts. The Eulerian regression audits an exact
nonphysical relaxation counterexample; its value 1 is **not** an upper
bound for the original game. All four commands were run in native
Python/Node. The continuum proofs remain hand arguments; no Lean or CI
result is claimed.

## Global causal-pressure transport regression — 2026-11-13

```sh
python packages/interval_global_closure/verify_global_pressure_matching.py
```

This standalone Fraction verifier was executed and its committed Git blob matched the tested source. It checks 200 exact atomic matching/closure/radius instances, 1,875 causal clock/backlog identities and 27 singular two-sweep germ cases. Full theorem: [GLOBAL_CAUSAL_PRESSURE_MATCHING.md](research/12-global-closure/GLOBAL_CAUSAL_PRESSURE_MATCHING.md). This is a finite formula audit, not an unrestricted equilibrium certificate or a new bound on V.

## Consolidated global-handoff replay (2026-11-13)

Read [HANDOFF_2026-11-13.md](HANDOFF_2026-11-13.md) before using these checks. From a full checkout, the following give targeted tests of global theory and recent all-path support restrictions (some are substantial exact checks):

~~~sh
python packages/interval_global_closure/verify_global_minimax_reduction.py
python packages/interval_global_closure/verify_cdf_record_variation.py
python packages/interval_global_closure/verify_global_strong_record_duality.py
python packages/interval_global_closure/verify_global_monotone_clock.py
python packages/interval_global_closure/verify_global_dual_two_sweep.py
python packages/interval_global_closure/verify_weighted_sweep_envelope.py
python packages/interval_global_closure/verify_fixed_start_runner_response.py
python packages/interval_global_closure/verify_global_sweep_stability.py
node packages/interval_global_closure/verify_g2_ray_exclusions.cjs
node packages/interval_global_closure/verify_g2_princess_cuts.cjs
~~~

The three recent Fraction regressions (weighted sweeps, fixed-start response, global sweep stability) were run successfully in the available working container. The last checks 1,050 completed polygonal Monsters and exact continuum-offset integrations. This is **not** a native full-tree replay, Lean compilation or CI result. Historical V8 checks have the precise provenance recorded in their corresponding research files.

**Upper certificate audit resolved:** the dedicated
`verify_upper_warp_tight.cjs` command above has now replayed the current
then-best U about 1.4261297228. The historical `verify_upper_warp.cjs` still
reads only `upper_warp_exact.json`, with its weaker value about
1.4261297443; the two commands intentionally certify different files.

## 16-knot common-warp lower-family exclusion

The following is an exact **whole-strategy-class exclusion** for warps
of the archived 338-path Princess law, not a new bound on unrestricted V:

```sh
node packages/interval_global_closure/verify_lower_warp16.cjs
```

The reference V8 replay checked all 5,408 first captures and sixteen
exact coefficient inequalities; the Node file is provided for independent
local replay and was not separately executed here. See
[the mathematical certificate](research/12-global-closure/LOWER_WARP_16_EXCLUSION.md).


## Effective response and global selector checkpoint (2026-11-12)

The computational bodies below passed exact root V8 replay. Native commands
are listed for portability; native execution, Lean compilation, and CI were
not run in this continuation.

```sh
node packages/interval_turn_sheet/verify_effective_fan_response_bound.cjs
node packages/interval_global_closure/verify_selector_plane_oracle.mjs \
  packages/interval_global_closure/snapshots/selector_global_26_input.json \
  /tmp/selector_global_26_replay.json
node packages/interval_global_closure/verify_selector_plane_physical.cjs
node packages/interval_finite_reduction_audit/verify_selector_compiler_independent.cjs
node packages/interval_finite_reduction_audit/verify_selector_realization_audit.cjs
```

The effective-count helper takes a supplied complete arrangement census; it
does not build that arrangement. The global selector value is a linear-plane
supremum, and strict rational physical witnesses remain distinct from their
zero-scale inspection polygons. See the full scope in
[the checkpoint](research/12-global-closure/EFFECTIVE_RESPONSES_AND_GLOBAL_SELECTOR_ORACLE.md).

## Local prefix and ordered-fan checkpoint (2026-11-12)

The exact cores and inputs for this checkpoint were replayed in V8 while
the native executor was unavailable. The commands below are portable local
reproduction commands; a native run of them in this continuation is not
claimed. No Lean compilation or CI is needed.

Local first-capture and initial-interface checks:

```sh
node packages/interval_turn_sheet/verify_affine_record_prefix.cjs
node packages/interval_turn_sheet/verify_affine_interface_excursion.cjs
node packages/interval_turn_sheet/verify_initial_density_interface.cjs
node packages/interval_turn_sheet/verify_interface_return_block.cjs
node packages/interval_turn_sheet/verify_affine_half_cell_bridge.cjs
node packages/interval_turn_sheet/verify_fan_center_partition.cjs
```

Exact fan cost and continuous-start arrangements:

```sh
node packages/interval_global_closure/verify_ordered_fan_cost.mjs ORDERED_COST_REPORT.json
node packages/interval_global_closure/verify_reflected_fan.mjs REFLECTED_FAN_REPORT.json
node packages/interval_global_closure/verify_fan_m1_separator.mjs RAW_M1_REPORT.json
node packages/interval_global_closure/verify_fan_fixed_tail_separator.mjs RAW_TAIL_REPORT.json
node packages/interval_global_closure/verify_ordered_fan_m1_separator.mjs ORDERED_M1_REPORT.json
node packages/interval_global_closure/verify_ordered_fan_fixed_tail_separator.mjs ORDERED_TAIL_REPORT.json
```

Complete fixed-basis exclusion and its unrestricted response diagnostic:

```sh
node packages/interval_global_closure/verify_reflected_fan_basis_exclusion.mjs BASIS_EXCLUSION_REPORT.json
node packages/interval_global_closure/upper_oracle_worker.mjs packages/interval_global_closure/snapshots/reflected_fan_basis_attacker_response.json ATTACKER_RESPONSE_REPLAY.json
```

The exclusion verifier checks the archived source packet identity, exact
profile enclosures, all causal selector coefficients and the final strict
comparison with the existing lower bound. It excludes only its stated
fixed reflected-fan simplex. The upper-worker command separately computes
the 26-pair mixture's unrestricted Princess response, whose larger value
demonstrates why the basis ceiling is not a full-game upper bound.

See [the proof checkpoint](research/12-global-closure/LOCAL_PREFIX_CLOSURE_AND_FAN_ORACLES.md)
for the mathematical scopes and remaining global obligations.



## Current frozen coordinate update and exact continuation checks

The current upper law is the strict common-coordinate update:

~~~sh
node packages/interval_common_warp/verify_upper_warp.cjs
~~~

Its exported verifier was executed and independently replayed, including
all integer graph equations and 560 physical captures. The exact response is
57045189772271291487410009/40000000000000000000000000.
The older unwarped law and its pair-regret calculation below retain their
original scopes.

The exact center-chain, all-count front solution and last-crossing checks are:

~~~sh
node packages/interval_turn_sheet/verify_center_chain_energy.cjs
node packages/interval_turn_sheet/verify_front_chain_quadratic.cjs
node packages/interval_turn_sheet/verify_center_last_crossing.cjs
node packages/interval_turn_sheet/verify_center_reachable_bases.cjs
~~~

The complete declared-family warp minimizers, early exclusion and exact
rational-function adapter have the following entry points:

~~~sh
node packages/interval_cdf_discovery/verify_warp_quadratics.mjs packages/interval_cdf_discovery/snapshots/endpoint_joint_i1_field.json packages/interval_cdf_discovery/snapshots/original_field_warp_family_quadratics.json packages/interval_cdf_discovery/snapshots/original_field_warp_late_quadratics.json packages/interval_cdf_discovery/snapshots/original_field_warp_five_family_solution.json /tmp/warp_quadratics.json --rebuild
node packages/interval_cdf_discovery/verify_warp_early_phase.mjs packages/interval_cdf_discovery/snapshots/endpoint_joint_i1_field.json packages/interval_cdf_discovery/snapshots/original_field_warp_five_family_solution.json /tmp/warp_early.json
node packages/interval_global_closure/verify_germ_v8.mjs packages/interval_global_closure/germ_v8_fixture_inputs.json /tmp/germ_v8.json
node packages/interval_global_closure/verify_avoided_center_bounce.mjs --output /tmp/avoided_bounce.json --face packages/interval_common_warp/upper_warp_face_geometry.json --upper packages/interval_common_warp/upper_warp_exact.json --source packages/interval_global_closure/upper_dyadic_exact.json
~~~

The computational bodies were executed in V8, including independent tensor
rebuilds, physical capture replay and rational specializations. The Node
file-I/O wrappers were not invoked during the native executor outage.
The objective-only asymptotic verifier exports a callable CommonJS function;
its 14 regression cases were also independently replayed. See
[its exact scope and proof](packages/interval_global_closure/ASYMPTOTIC_CAPTURE_SEARCH.md).

No new finite-law computation is represented as the missing unrestricted
saddle. See [the detailed checkpoint](research/12-global-closure/CHAINS_AND_AVOIDED_BOUNCES.md).

## Previous unwarped global strategy checks

The current rational 280-pair monster strategy has a replayable integer
flow/cut certificate and an independently intersected rational princess
best-response approximation:

```sh
node --stack-size=16384 packages/interval_global_closure/certify_upper_candidate.cjs --verify packages/interval_global_closure/upper_dyadic_exact.json
python packages/interval_global_closure/verify_upper_candidate.py packages/interval_global_closure/upper_dyadic_exact.json /tmp/upper_dyadic_princess_response.json
```

Both commands were executed. The response supremum is exactly
`957063215727541539/671088640000000000`; this certifies the supplied upper law,
not an unrestricted equilibrium.

The new whole-strategy workflow and its exact/discovery separation are in
[the global package README](packages/interval_global_closure/README.md).
It includes exact fixed-bank reconstruction, unrestricted rational-function
capture-order search, generic unit-route checks, and the uniform corridor
exclusion. Those new Python checks were executed in this continuation.
NumPy/SciPy and SymPy are used where stated; no Lean or CI was run.

The full strategy exchange, continuous-CDF response searches and their
verification commands are documented separately in
[the upper solver method](packages/interval_global_closure/efficient_method.md),
[the CDF exchange](research/12-global-closure/CONTINUUM_EXCHANGE.md), and
[the physical response method](research/12-global-closure/CONTINUOUS_RESPONSE.md).
These distinguish exact certificates from numerical discovery and retain
both successful responses and the explicit attacks on rejected candidates.

## Exact play between the two certified strategies

```sh
node packages/interval_global_closure/paired_strategy_regret.cjs /tmp/paired_strategy_regret.json
```

The exported calculation was executed in V8 after the general
executor interruption. The Node filesystem wrapper itself was not invoked
during the outage. It checks 94,640 cross encounters by two independent
methods, replays the 338 captures against the old optimal Monster, and
writes the exact cross payoff and both unilateral improvement bounds.
It imports the separate unrestricted-response certificates. Input/source
hashes and the complete result are saved beside the script.
See [the explicit pair](research/12-global-closure/EXPLICIT_STRATEGY_PAIR.md).

## Faster unrestricted finite-law response

The recovered C++ source is byte-identical to the version checked before the
execution interruption. It uses exact aggregate inverse-hit sums and a
reviewed paired-block lower bound. The independent verifier was executed:

```sh
python packages/interval_global_closure/verify_continuous_fast_search.py
```

This needs a C++17 compiler and GMP. It tests contact equalities, weighted
center fixtures, fixed starts, unfinished frontiers and the archived exact
32-path response. It does not establish a new game lower bound. See
[the full scope](research/12-global-closure/FAST_CAPTURE_ORDER.md).

## Historical checks

Each original `packages/interval_*/` directory is a historical snapshot. They intentionally retain their original relative imports and compressed flow files. Do not move scripts away from their folders. Run the following commands from the repository root.

Python 3 standard library only for these core checks:

```sh
(cd packages/interval_pm_proof && python verify.py && python counterexample.py)
(cd packages/interval_exact_reduction && python verify_exact.py)
(cd packages/interval_exact_response_result && python tests.py)
(cd packages/interval_target_exclusion && python verify_target.py)   # potentially expensive
(cd packages/interval_equilibrium_check && python verify.py)
(cd packages/interval_uniform_reduction && python tests.py)
(cd packages/interval_uniform_reduction && python verify.py)         # potentially expensive
python packages/interval_structural_obstructions/verify.py
python packages/interval_characteristic_response/verify.py
python packages/interval_wait_in_out_exclusion/verify.py
python packages/interval_post_sweeper_detour/verify.py
python packages/interval_refined_upper/verify.py
python packages/interval_candidate_densities/verify.py
python packages/interval_central_concentration/verify.py
python packages/interval_continuous_rank/verify.py
python packages/interval_turn_curve_discovery/verify_characteristics.py
python packages/interval_signed_densities/verify.py
python packages/interval_signed_densities/verify_dual.py
python packages/interval_signed_densities/verify_trace_cap.py
python packages/interval_signed_densities/verify_local_gap.py
python packages/interval_signed_densities/verify_local_capture.py
python packages/interval_continuous_rank/research/audit_two_turn_formulas.py
python packages/interval_continuous_rank/research/audit_last_wave_stationarity.py
python packages/interval_no_extra_family/verify.py
python packages/interval_turn_sheet/verify_general_response.py
python packages/interval_turn_sheet/verify_uncrossing.py
python packages/interval_turn_sheet/verify_initial_wave.py
python packages/interval_turn_sheet/verify_terminal_integrals.py
python packages/interval_turn_sheet/verify_center_bellman.py
python packages/interval_turn_sheet/verify_general_center.py
python packages/interval_turn_sheet/verify_signed_bellman.py
python packages/interval_turn_sheet/verify_center_memory.py
python packages/interval_turn_sheet/verify_prefix_compression.py
python packages/interval_turn_sheet/verify_uniform_inward.py
python packages/interval_turn_sheet/verify_localized_inward.py
python packages/interval_turn_sheet/verify_initial_inward_cdf.py
python packages/interval_turn_sheet/verify_initial_inward_start.py
python packages/interval_turn_sheet/verify_inward_dominance.py
python packages/interval_turn_density/verify_terminal_sources.py
python packages/interval_turn_density/verify_curved_terminal_sources.py
python packages/interval_turn_density/verify_general_inward_adjoint.py
python packages/interval_turn_density/verify_free_second_inward.py
python packages/interval_turn_sheet/verify_free_second_inward_field.py
python packages/interval_turn_density/verify_free_inward_comparison.py
python packages/interval_turn_sheet/verify_free_inward_support_gate.py
python packages/interval_turn_density/verify_detached_inward_corner.py
python packages/interval_turn_density/verify_double_corner_inward.py
python packages/interval_turn_density/verify_first_corner_inward.py
python packages/interval_turn_density/verify_repeated_same_half.py
python packages/interval_turn_density/verify_terminal_inward_c.py
python packages/interval_turn_density/verify_endpoint_inward_comparison.py
python packages/interval_turn_density/verify_endpoint_inward_adjoint.py
python packages/interval_turn_density/verify_endpoint_inward_two_wave.py
python packages/interval_turn_sheet/verify_postone_first_hit_moments.py
python packages/interval_turn_density/verify_postone_same_half_delay.py
python packages/interval_turn_density/verify_postone_same_half_gate.py
python packages/interval_turn_density/verify_repeated_inward_uncrossing.py
python packages/interval_turn_density/monotone_cut.py
python packages/interval_turn_density/verify_endpoint_paired_cut.py
python packages/interval_turn_density/verify_endpoint_unary_families.py
python packages/interval_turn_density/verify_initial_center_wait_removal.py
python packages/interval_turn_density/verify_incoming_warp_preservation.py
python packages/interval_cdf_discovery/verify_warp_outer_column.py
python packages/interval_turn_density/verify_corridor.py
python packages/interval_turn_density/verify_curved_outgoing_layer.py
python packages/interval_turn_density/verify_positive_sheet.py
python packages/interval_turn_density/verify_positive_cdf_sheet.py
python packages/interval_turn_density/verify_two_interior_cdf.py
python packages/interval_turn_density/verify_wait_two_triangles.py
python packages/interval_turn_density/verify_m3_early.py
python packages/interval_turn_density/verify_signed_prefix_compression.py
python packages/interval_turn_density/verify_negative_pava.py
python packages/interval_turn_density/negative_exit_phase.py
python packages/interval_cdf_discovery/verify_frozen_attack.py
python packages/interval_cdf_discovery/audit_snapshot.py packages/interval_cdf_discovery/snapshots/constant_half_wait_candidate.json
python packages/interval_cdf_discovery/audit_snapshot.py packages/interval_cdf_discovery/snapshots/constant_half_wait_repaired.json
```

Some C++ files are optional independent cross-checks; no native compilation is necessary for standard-library Python verifiers. Exclude research logs from assertions of proof; consult each package's `PROOF.md` and `README.md` for its exact scope. No CI or Lean proof is promised by this snapshot.

The no-extra-family verifier explicitly reports that its exclusion target
was not achieved. Its exact ceiling applies only to the displayed
two-parameter princess family; it is not an upper bound on the full game.
The optional signed-density discovery-feature comparison needs NumPy,
SciPy, and Numba and is documented in that package's README.

The turning-density package distinguishes its exact capture checks from
numerical discovery. Its optional `verify_separated.py` compares analytic
features with independent numerical integration of actual captures;
`endpoint_tail.py` and `fit_endpoint_tail.py` check a local analytic basis
and stationarity residuals. Those programs need the experiment dependencies
described in that package's README. Small numerical residuals are not
existence proofs or matching game certificates.

The signed Bellman verifier checks 1,189 exact action, record, terminal,
and concavity cases; the curved-center verifier checks 1,056. They include
incoming coincidence atoms, center waits, endpoint starts, and positive
mass absorbed exactly at time two. The two positive-sheet verifiers check
4,284 upper-envelope identities and 4,895 lower-CDF identities, including
independent direct intersections and the endpoint first-contact jump.
They verify the stated formulas, not the existence of a globally matched
strategy or Bellman potential.

The center-memory verifier checks 3,987 exact comparisons with direct
polygonal first intersections. It includes slow outward motion, endpoint
departures, and characteristic atoms. The two-interior-turn verifier checks
4,512 exact identities for both initial signs and same-half turns. The signed-early prefix
verifier checks 2,112 isotonic comparisons, including lower-edge derivative
jumps. The source-resolved exit verifier checks 4,400 rational identities.
These tests have their stated local and specified-law scopes.

The early-M3 verifier checks 15,906 exact capture, endpoint-envelope, and
density identities. The independent normalized whole-law capture check
requires the experiment dependencies and is run with:

```sh
python packages/interval_turn_density/verify_m3_attached.py m3_attached_settled.json
python packages/interval_turn_density/m3_face_features.py
```

It compares actual physical captures with analytic feature rows, including
noncanonical sloped prefix contours. It does not certify a maximum over
all scalar responses or produce a matching lower law.

The ordered-negative-prefix extension has 3,960 exact comparisons with
an independent complete dynamic program. Its separate physical capture
check and the analytic-tail checks require the experiment dependencies:

```sh
python packages/interval_turn_density/negative_prefix_oracle.py
python packages/interval_turn_density/verify_singular_tail_basis.py
python packages/interval_turn_density/verify_singular_tail_negative.py
python packages/interval_turn_density/verify_singular_tail_law.py
```

The prefix-compression verifier checks ordinary capped laws against
arbitrary-speed initial routes. It passes 9,759 reported checks, including
7,800 exact coordinatewise capture comparisons and two atomic
counterexamples enforcing the theorem's separation hypothesis. This
does not establish ordinary-wave membership for the curved CDF candidates.

The full analytic-tail law and its failed outer attachment are documented
in `packages/interval_turn_density/SINGULAR_TAIL_ATTACHMENT.md`. The
moment and physical-feature checks use floating quadrature; the saved
numerical scalar maximum is not an exact game ceiling.

The initial-inward CDF verifier checks 639 exact complete-route identities,
10 initial/characteristic-atom fixtures, 47 exact directional identities,
and 47 strict finite attacks on ordinary initial prefixes. These include
the additional first-contact correction when an inward turn touches a
center atom. The finite attack excludes the proposed ordinary tail at
active positive-M2 starts; it does not provide a replacement equilibrium.

The free-start derivative audit has 1,079 exact checks, and the independent
turn-deletion verifier has 12,513. The latter checks individual first
captures on both signs, including strict attacks that move a second turn
earlier along an outgoing CDF plateau. The curved terminal-source verifier
retains the initial corrections and also checks fully curved incoming
paths. The general upper inward adjoint has 693 exact physical integral
and derivative checks, including a nonzero terminal edge correction.
The free-second-turn contact checker has 1,576 exact checks, including
physical integration over an actual second-turn surface and strict finite
variations at its incompatible ordinary-cap junction.
These establish identities and finite comparisons, not simultaneous
solvability or an unrestricted saddle.

The source-free free-second-turn identity has two independent physical
audits, with 1,036 and 720 exact checks. Its first-inverse active-support
gate has 282 exact checks, including turns outside the separated future-row
region. The detached-corner equations and conditional terminal-I reduction
have 1,260 checks. The singular double-corner upper law and its diffuse
second-turn replacement fail independent finite princess variations,
verified in 1,631 and 3,312 exact checks. The repeated same-half-return
kernel has 1,322 checks and a rational example beating all three elementary
turn deletions. These results distinguish feasible field identities from
the separate upper-response and unrestricted-response obligations.

The final-characteristic derivative for a pre-one inward phase has 7,104
exact physical checks, including curved incoming endpoint variations and
both edge signs. Its conditional support-deletion consequence does not
apply to an additional phase beyond `U=1` or to an unexamined contact atom.

The endpoint-inward comparison has 1,056 exact checks, including initial
atoms, the true post-one inverse, the scalar barrier, and the endpoint/
fixed-turn cross identity. The endpoint adjoint has 1,198 physical checks;
its separate two-wave audit has 624. The full first-hit-moment verifier
has 1,139 checks. These retain actual first inverses rather than replacing
them by the final outgoing characteristics.

The continuous post-one return theorem has 672 exact delay fixtures and
3,620 exact gate/merge checks. Its whole-field gate certificate can be
reproduced without optional dependencies:

```sh
python packages/interval_cdf_discovery/audit_postone_branch_gates.py \
  packages/interval_cdf_discovery/snapshots/endpoint_joint_i1_field.json \
  --output /tmp/endpoint_return_gates.json
```

This verifies all 6,936 transport triangles, 68 post-boundary cells, and
477 vertices in 144 split terminal triangles. It proves the supplied
branch geometry, not the remaining free-I cost inequalities or a game
bound. The chained-inward uncrossing identity has 442 separate exact
checks.

The generic attractive-cut optimizer checks capacities, conservation,
and equality of its flow and cut. Its 92 exact fixtures compare 5,020
feasible assignments exhaustively. The endpoint physical suite has
4,748 checks, and the extended unary-family suite has 6,544, including
the joint one-sided `U=1` limit. These certify the finite arrangements
and formulas; no finite cut by itself covers the continuum or the outer
start/cutoff parameters.

The initial-center-wait replacement has 342 exact physical checks. Its
upper-response conclusion uses a separate lower-semicontinuity argument.
The verifier deliberately retains the failure of pointwise domination
at a princess path that stays at the center.

The incoming-warp preservation verifier has 3,362 exact checks, including
monster waits, repeated center crossings, and a fixture where lower
quantiles reorder. The construction's two inverse-range certificates
are checked over 47 and 52 exact quadratic pieces:

```sh
python packages/interval_cdf_discovery/terminal_band_warp.py \
  --repair-end 255/256 --output /tmp/endpoint_low_band_warp.json
python packages/interval_cdf_discovery/terminal_band_warp.py \
  --qlo 17/20 --qhi 113/125 --repair-start 255/256 \
  --bridge-start 127/128 --output /tmp/endpoint_high_band_warp.json
```

The algebraic field is defined by the exact inverse envelopes and the
initial-front cap. Its optional outer-column audit uses NumPy/SciPy:

```sh
python packages/interval_cdf_discovery/audit_band_warp_columns.py \
  --output /tmp/endpoint_two_band_columns_audit.json
```

This last audit integrates the actual unmeshed field, with estimated
numerical quadrature errors. A separate standard-library verifier,
`verify_warp_outer_column.py`, proves the strict outer incompatibility
using a rational inverse bracket and a positive integral lower bound;
its conclusion needs no numerical quadrature. The construction and its
fixed-coordinate front solver are documented in
`JOINT_ENDPOINT_COMPONENT.md`. Neither supplies a matching certificate.

The local golden-ratio calculation uses `mpmath` and independent curved
path intersection/quadrature at 45 digits:

```sh
python packages/interval_turn_sheet/verify_curved_initial_power.py --quick
python packages/interval_turn_sheet/verify_endpoint_curved_power.py --quick
```

The quick audit has 27 capture integrations/difference checks, including
an actual mixture with exactly flat positive-M2 cost. The default audit
uses seven scales per case. These high-precision checks are not rational
or interval certificates and do not certify an endpoint asymptotic.
The endpoint variant has 42 quick comparisons and requires no flat
positive-M2 baseline. Its fixed-start power balance is not a global
initial-motion or active-support theorem.

The uniform and localized inward-sheet physical features have 483 and
260 exact checks. Their complete prefix optimizers and the full tied-ramp
law use the optional experiment dependencies:

```sh
python packages/interval_turn_density/verify_inward_prefix.py
python packages/interval_turn_density/verify_inward_positive.py
python packages/interval_turn_density/verify_localized_ramp.py
python packages/interval_turn_density/verify_localized_law.py
python packages/interval_turn_density/verify_localized_prefix.py
python packages/interval_turn_density/verify_independent_prefix.py
```

The last verifier includes affine negative-inverse competitors, integrating
their signed-M3 terms independently of the production constant-block API.
The saved density fits are structural experiments on the existing knots,
not exact scalar-response certificates or new game bounds.

The frozen CDF attack verifier uses exact rational arithmetic for the
complete field and checks an improving initial-inward route, not a
sampled quantile law. `audit_m1.py` in the same package separately checks
every M1 start by exact quadratic-cell minimization. See that package's
README for the frozen finite pool, rational late-inequality repair, and
new discovery options; none is labelled an unrestricted game bound.

The independent floating CDF attack probe needs NumPy; polishing also needs
SciPy. Its regression against exact reference costs can be run with:

```sh
PYTHONPATH=/workspace/scratch/f5595f62cf06/experiment_deps python -B packages/interval_turn_sheet/verify_cdf_probe.py
```

This checks 300 whole-field payoffs against independent exact costs,
including center and endpoint atoms and a near-endpoint interior turn.
It validates a discovery implementation, not an unrestricted optimum.

All six original package snapshots are also preserved in the archive file at `archive/monster_princess_progress_2026-11-10.zip` (see package directory list), including larger exploration checkpoints that may not be checked out individually.

## Center renewal, full-record boundaries, and common geometry

The following computational bodies were executed with exact rational
arithmetic, with independent parent replays. The new file-I/O wrappers
were not rerun after the second native executor outage.

~~~sh
node packages/interval_turn_sheet/verify_center_factorization.cjs
node packages/interval_turn_sheet/verify_center_affine_renewal.cjs
node packages/interval_cdf_discovery/verify_record_bellman_boundary.cjs --expected packages/interval_cdf_discovery/snapshots/record_bellman_boundary.json
node packages/interval_cdf_discovery/verify_late_negative_m2_edges.cjs --expected packages/interval_cdf_discovery/snapshots/late_negative_m2_full_exact.json
node packages/interval_turn_density/verify_center_wait.cjs
node packages/interval_turn_density/verify_projected_cut.cjs
python packages/interval_turn_density/project_order.py --verify-only
node packages/interval_cdf_discovery/verify_common_warp.mjs packages/interval_cdf_discovery/snapshots/endpoint_joint_i1_field.json packages/interval_cdf_discovery/snapshots/original_field_warp_features.json packages/interval_cdf_discovery/snapshots/original_field_warp_finite_solution.json /tmp/common_warp_replay.json
~~~

The center theorem, local affine recurrence, supplied-field boundary, and
complete late-M2 family have distinct scopes. The common-warp replay
rejects the saved finite-bank update by an exact off-bank M2 route.
No finite-bank score in these reports is an unrestricted lower guarantee.


## Exact center attachment and frozen physical exchange (2026-11-12)

The latest scope and linked certificates are in
[the checkpoint](research/12-global-closure/EXACT_CENTER_AND_FROZEN_EXCHANGE.md).
The complete algebraic center verifier is intentionally substantial; its
independent replay took about 525 seconds. No Lean command is required.

```sh
node packages/interval_turn_sheet/verify_affine_center_zeno_attachment.cjs > /tmp/center_zeno.json
node packages/interval_turn_sheet/verify_affine_center_offfront_transfer.cjs > /tmp/center_offfront.json
python packages/interval_global_closure/solve_frozen_master.py
```

The Python probability master requires NumPy and SciPy and checks both
normalized payoff inequalities after optimization. It is discovery data,
not a substitute for unrestricted strategy response certificates. Its input
rows are immutable physical paths; adding a Monster must not re-realize an
old row at a different subordinate scale.

The germ realization, frozen-pair, and complete M1 verifiers have native
Node entry points documented in their package notes. Their fixture source
hashes are retained in the included manifest and reports. The independent
root replay of the generalized realizer passed all 48 geometry, 24 upper
maximizer, and four legacy cases.


## Terminal-center regions and frozen exchange checkpoints

The latest complete gates and scope are documented in
[TERMINAL_CENTER_AND_FIXED_TAILS.md](research/12-global-closure/TERMINAL_CENTER_AND_FIXED_TAILS.md).

```sh
node packages/interval_turn_sheet/verify_center_rank_removal.cjs > /tmp/center_rank.json
node packages/interval_turn_sheet/verify_center_late_exterior.cjs > /tmp/center_late.json
python packages/interval_global_closure/rebuild_frozen_checkpoint.py \
  packages/interval_global_closure/snapshots/frozen349_checkpoint_delta.json.gz.b64 \
  . /tmp/frozen349
```

The restore script checks exact geometry hashes, all row identities, probability
dimensions and complete-M1 row coverage. It produces literal rows.json, bank.json
and master.json for the native workers. This is a recoverable discovery state,
not an unrestricted response certificate. The larger pinned rejection inputs
are listed in packages/interval_global_closure/fixed_tail_artifacts_manifest.json.

### Arbitrary low-record first-center prefixes

Run `node packages/interval_turn_sheet/verify_shared_prefix_budget.cjs`.
The saved exact certificate covers every first-center time in [7/8,t_L]
and every feasible low captured rank, with arbitrary same-side prefix
speed and turn count. It is a supplied-field local exclusion at 7131/5000;
it is not a game lower bound. See the complete dependency and scope statement
in `research/10-turn-density/SAME_SIDE_PREFIX_SHARED_BUDGET.md`.


## Finite ordered-fan center continuations and exact stationary tails

Run the standalone exact center partition and merge regressions:

    node packages/interval_turn_sheet/verify_fan_center_partition.cjs

Replay the early/middle gates for the older frozen field:

    node packages/interval_turn_sheet/verify_center_early_middle.cjs \
      packages/interval_cdf_discovery/snapshots/endpoint_joint_i1_field.json

The exact static-tail theorem and evaluator have separate independent checks:

    node packages/interval_global_closure/verify_static_tail_turns.mjs /tmp/static_turns.json
    node packages/interval_global_closure/verify_static_tail_dp.mjs /tmp/static_dp.json

The interval-fan provider and its physical verification are described in
research/12-global-closure/UNIFORM_TRANSLATION_FANS.md and the accompanying
translation_fan_artifacts_manifest.json. Symmetric trial archives retain
their stated scope even though the exact provider also supports outward
and asymmetric intervals. The native ordered-weight controller was not
written before the runtime outage, and has no claimed optimization result.

These commands verify supplied-law structural components. They do not
claim the unrestricted game value or replace the remaining initial-prefix
and matching-strategy obligations. No Lean compilation or CI is requested.

