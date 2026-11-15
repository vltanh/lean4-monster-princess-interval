> **2026-11-14 UTC — exact certificates.** The one-turn comparison is closed by the new continuous physical law below; historical lower and upper receipts remain intact. The broader [equilibrium geometry program](research/13-equilibrium-geometry/README.md) remains open. Run routine exact structural checks in [geometry-structural-checks.yml](.github/workflows/geometry-structural-checks.yml); manual-only discovery workflows are preserved for hypothesis-driven tests. The full certificate commands below remain valid, but do not repeat billion-transition pricing without a changed proof dependency.

# Reproduce current exact certificates

## Current unrestricted bracket and explicit Princess law

The current n512 game-value lower is **36409808231/25600000000**;
the saved explicit Princess law separately guarantees
**582556541071/409600000000**. The new physical one-turn upper is
**142472349375511/100000000000003 = 1.424723493755067…**, leaving exact width
**6311320912972370575307/2560000000000076800000000 = 0.002465359731629758…**.
The historical upper **291849329389899/204800000000000** remains the frozen
comparison target U_*. The new certificate proves V≤W_1≤C<U_*.
See [the countercertificate](research/13-equilibrium-geometry/ONE_TURN_SEPARATION_COUNTERCERTIFICATE.md),
[retained lower and historical upper proof](research/12-global-closure/NORMALIZED_GLOBAL_BOUND_CERTIFICATES.md)
and [retained lower package](packages/interval_discovery_certificates/princess_front_n512/README.md).

The complete current upper replay is inexpensive and needs only Python's standard library:

```sh
python3 packages/interval_one_turn/verify_continuum_upper.py \
  packages/interval_one_turn/one_turn_continuum_upper.json.gz \
  --output /tmp/one_turn_continuum_replay.json --require-counterexample
```

This passes all 730,146 rational inequalities with zero residual repair.
The saved replay and compressed-input hash are in
`packages/interval_one_turn/one_turn_continuum_upper_replay.json`.
It does not rerun the large historical lower computations below.

From the repository root, this inexpensive command verifies the retained
files and completed report bindings, exact rational arithmetic, every nodal
transport condition and deterministic extraction of the saved strategy:

```bash
node packages/interval_discovery_certificates/princess_front_n512/check.cjs
```

It **does not repeat the response search**. The substantial independent
complete-bank replay, including exact regeneration and comparison of the
saved continuous Princess law, is:

```bash
node --max-old-space-size=6000 packages/interval_center_pricing/verify_strategy.cjs \
  packages/interval_discovery_certificates/princess_front_n512/field.json \
  packages/interval_discovery_certificates/princess_front_n512/princess.json --progress 128
```

The completed independent CI [43546803161](https://github.com/vltanh/lean4-monster-princess/actions/runs/43546803161)
checked 893,765,461 transitions in 780.246 seconds. The archive and report
hashes bind the actual historical verifier source. The wrapper above performs
one full pricing replay; do not also run a separate BigInt pricing command
merely to duplicate it. The original native engine provides a second complete
implementation without the center/front compression:

```bash
python packages/interval_clock_grid/normalized_native/verify_native_field.py \
  packages/interval_discovery_certificates/princess_front_n512/field.json
```

That original computation has 5,117,238,127 transitions. Run it deliberately
when an input or proof dependency warrants verification, not during each
floating discovery step. Independent upper verification reconstructs the
physical paths, every causal clock prefix and the integer flow/cut:

```bash
python packages/interval_discovery_certificates/verify_manifest.py \
  packages/interval_discovery_certificates/monster_boundary_n256_manifest.json
```

The former `packages/interval_clock_grid/lower_n256_field.json` and
`lower_n256_princess.json` remain valid weaker regression inputs. Their original
native and BigInt extraction commands still work. Python 3, Node.js and g++
are required for the exact computations; no floating optimizer is used to
accept these certificates. A command listing is not a claim of a new CI or
Lean result.

The [compact replay workflow](.github/workflows/compact-fine-replay.yml)
now reads the retained repository inputs without an expiring download
requirement. Pushes run independent small regressions; manual dispatch with
`replay_complete_bank=true` requests the substantial replay. The separate
[retention workflow](.github/workflows/discovery-certificates.yml) checks the
saved data and strategy identity. These jobs have different scopes.

## Global incoming-front projection and contact equations

The [incoming-front theorem](research/12-global-closure/GLOBAL_INCOMING_FRONT_COMPLETION.md) is a global security-preserving reduction. Its projected field inherits the existing exact lower through a proved record comparison. These commands do not rerun n256 exhaustive pricing and do not claim that the projected minimum equals the old minimum.

```bash
python -B packages/interval_global_closure/verify_incoming_front_completion.py --report /tmp/incoming_front_completion_replay.json
node packages/interval_global_closure/project_front2_princess.cjs verify
python -B packages/interval_global_closure/verify_front2_projection_fraction.py --checkout . --report /tmp/front2_projection_independent_replay.json
python -B packages/interval_global_closure/verify_bulk_contact_equations.py /tmp/bulk_contact_equations_replay.json
python -B packages/interval_global_closure/verify_initial_inward_contact.py /tmp/initial_inward_contact_replay.json
python -B packages/interval_global_closure/verify_inward_endpoint_obstacle.py /tmp/inward_endpoint_obstacle_replay.json
python -B packages/interval_global_closure/verify_curved_initial_phase.py /tmp/curved_initial_phase_replay.json
python -B packages/interval_global_closure/verify_positive_prefront_boundary.py /tmp/positive_prefront_boundary_replay.json
python -B packages/interval_global_closure/verify_front_one_contact_moments.py /tmp/front_one_contact_moment_replay.json
python -B packages/interval_global_closure/verify_boundary_shadow_kernel.py
python -B packages/interval_global_closure/inspect_monster_start_profile.py --physical-certificate packages/interval_discovery_certificates/monster_mutations_n128.physical.json.gz --report /tmp/monster_mutations_n128_start_profile_replay.json
python -B packages/interval_global_closure/verify_prefix_compression_diagnostic.py --report /tmp/prefix_compression_diagnostic_replay.json
```

To regenerate the projected field and explicit law, use `node packages/interval_global_closure/project_front2_princess.cjs generate`. The source field and original strategy are SHA256-bound. The projected field is `a8e1d84d67e66e08d6d1eeb02f18c6e5121108cb4368ededd9db2e792a97189e`; the strategy is `73633ef3386a9712463280fe220e8d6898c197414fea61fa8c1bdf3f8e659a68`. Its explicit security remains `582289859141/409600000000`. The unchanged value lower belongs to the approaching-width family, not the one saved strategy.

Node checks all stored front/cone/sticky identities and reconstructs the quantile law. Independent Python decodes all four old/new field/strategy arrays, checks 1,050,881 full-horizon identities and each field's 2,097,152 transport inequalities, then exhausts six small physical banks. The contact scripts independently integrate affine first collisions; the boundary-shadow replay includes 9,075 inward cases, 1,650 direct cases and 165 sweeps. The n128 initial-profile diagnostic does not reprove the stored max-flow upper. The [separate CI workflow](.github/workflows/front-reduction.yml) runs these checks without repeating unchanged large searches.

The [endpoint square-root theorem](research/12-global-closure/ENDPOINT_SQUARE_ROOT_CONTACT.md) is a reviewed analytic consequence of its explicitly stated equal-cost and front-slope assumptions. It is not a numerical equilibrium certificate.

The inward replay covers both peak-record branches and exact physical derivatives. The prefix diagnostic independently replays all stored complete paths, small prefix deletions and two front-preserving compressions using the existing chronological affine-interval integrator. Its dimensionless interpolation epsilon is **1/2**, unlike the historical saved n256 strategy's **1/512** and the current n512 strategy's **1/1024**; its fixed-field costs do not evaluate either saved narrow strategy. The [superadditive central-return theorem](research/12-global-closure/SUPERADDITIVE_CENTRAL_RETURN_COMPRESSION.md) is an independently reviewed analytic proof, including two separate derivations of its concave-density case. CI fixtures do not constitute a Lean verification of the universal theorem.

The [curved-initial-phase theorem](research/12-global-closure/CURVED_INITIAL_PHASE_RESPONSE.md) reduces every initial response in a qualified phase to at most three directional runs, with both exit records and the full continuation. Its Fraction replay checks nonlinear phase fixtures. The [front-one contact note](research/12-global-closure/FRONT_ONE_CONTACT_NONALGEBRAICITY.md) proves exact response-family exclusions and a conditional nonalgebraic endpoint trace. Its physical replay checks 1,062 affine contact branches; the Puiseux contradiction remains an analytic proof, not a finite fixture claim. Neither note proves a global finite phase cover.

The [positive-prefront/modulus addendum](research/12-global-closure/POSITIVE_PREFRONT_RESPONSE_AND_MODULUS.md) proves a first-exit exchange, a continuity-only center count and an inner-curvature class exclusion through U=41/40. Its new Fraction replay independently compares actual first captures with chronological records in 135 cases, including all three outgoing boundaries and endpoint atoms. The [static global free-start Zeno theorem](research/12-global-closure/GLOBAL_FREE_START_ZENO_COUNTEREXAMPLE.md) is a separate analytical counterexample, not a numerical fixture. Both manuscripts have two independent full reviews; no Lean kernel check or unrestricted equilibrium is claimed.

The new boundary replay runs in [geometry structural CI](.github/workflows/geometry-structural-checks.yml); [run 43553779143](https://github.com/vltanh/lean4-monster-princess/actions/runs/43553779143) passed at commit 102b396. The Zeno note's additional atom-free front-one comparison proves a strict free-start improvement by chronological time ordering and the finite positive-gap theorem. That analytical proof has two independent reviews and needs no numerical fixture or repeated large bank search.

The [outer continuation and Zeno note](research/12-global-closure/FRONT_CONTINUATION_GAPS_AND_ZENO.md) is a reviewed analytical proof. It gives a front terminal, an explicit finite-return criterion, and endpoint mixing with controlled loss; it also explains the failure of a uniform fixed-center cutoff. No finite fixture or existing CI job is presented as a formal verification of its universal statements.

## Exact center compression

The [center engine](packages/interval_center_pricing/README.md) preserves the complete normalized integer minimum through phase-specific value monotonicity. Policies 0–4 successively compare unrestricted branching, center triangles, rank balance, collapsed returns and the front-two terminal guard. A front-two input is required for policy 4. The precenter branch remains unrestricted.

```bash
python packages/interval_center_pricing/test_center_pricing.py /tmp/center-regression.json
python packages/interval_center_pricing/verify.py packages/interval_clock_grid/lower_n256_field.json --output /tmp/center-retained-replay.json
```

These preserve the existing continuum transfer estimate. They accelerate the complete exact bank verification used by the stronger n512 certificate; they do not replace the transfer by a smaller unproved error.

## Discovery workflows and new structural fixtures

The geometry and joint physical discovery implementations are separate from
exact replay. The [record-hypograph workflow](.github/workflows/continuous-geometry-discovery.yml)
varies Princess CDF geometry; the [joint Monster workflow](.github/workflows/adaptive-bound-discovery.yml)
varies physical paths and probabilities, with coarse pricing, exact
one-turn-loop separation and independently checked integer flow/cut uppers.
Both upload exact candidates, floating histories, solver logs, seeds, source
hashes, and restart checkpoints. Read HANDOFF.md for completed outcomes.

To start another intentional campaign through the verified push mechanism,
set `run_on_push` to `true` in the corresponding package's `campaign.json`
and push that change on the research branch. Leave it `false` for routine
retention and implementation changes: exact regressions still run. Both
workflows also declare manual discovery inputs and optional artifact resume
IDs. The actual discovery runs linked here were observed after pushes;
a declared workflow is not evidence that a job ran. The old cached-rejection
artifacts did not include each rejected trial array; the corrected driver
now retains the exact compact trial before any screening decision.

The cheap structural regressions and retained fixed-law obstruction are:

```bash
python packages/interval_quantile_certificate/test_refinement_ceiling.py
python packages/interval_quantile_certificate/earlier_front_probe.py
python packages/interval_quantile_certificate/test_continuous_record_hypographs.py --report /tmp/continuous-record-hypographs.json
python packages/interval_continuous_lower/test_record_lp.py
python packages/interval_continuous_lower/test_trial_retention.py
python packages/interval_mixture_cut/test_search.py
python packages/interval_mixture_cut/test_princess_retention.py
python packages/interval_fixed_marginal/ci_n512_obstruction/verify.py
```

The refinement check establishes the route/edge identity behind the frozen
geometry ceiling. The earlier-front probe checks its exact projection,
transport, unchanged continuous attacks and a saved physical bank witness.
The continuous-record regression checks the exact cone integral, zero slopes,
endpoint atoms and conservative secant error for specified physical routes.
The nodal record-LP regression separately compares its hypographs with clocks. The mixture regression checks loop rectangles, chronological first
contacts and native/BigInt flow agreement; its retention regression checks
complete-priced field archives, exact best selection and restart integrity. The fixed-law verifier binds the
actual n512 CI data, reconstructs all 676 refined seed marginals, and replays
both nodal and continuous costs. None of these checks promotes a cached
response bank or a fixed-law obstruction into a new unrestricted lower.


The separate [main discovery workflow](.github/workflows/discovery.yml) is
push-triggered and manually dispatchable. Its validated `campaign.json`
selects experiments and can restore exact candidates, physical calendars,
random seeds and solver checkpoints from a previous Actions artifact.
[Run 43532597339](https://github.com/vltanh/lean4-monster-princess/actions/runs/43532597339)
performed the original five-family discovery. Its new physical upper is now
archived in the repository; floating objectives and cached path minima are
never promotion certificates.

The [shape workflow](.github/workflows/shape-discovery.yml) runs new variation
and curvature searches at explicit exact security floors, with complete
coarse separation, independent BigInt acceptance, and bounded finer pricing.
Its source, counterexamples and exact scope are in
[interval_cdf_shape](packages/interval_cdf_shape/README.md).

```bash
python packages/interval_discovery/test_princess_search.py
python packages/interval_discovery/test_monster_search.py
python packages/interval_discovery/test_configure_campaign.py
python packages/interval_cdf_shape/test_shape_search.py
python packages/interval_cdf_shape/verify_shape_attack.py packages/interval_cdf_shape/naive_tv_rejected.dual.json.gz packages/interval_cdf_shape/naive_tv_attack.json
python packages/interval_global_closure/verify_center_heavier_first.py
node packages/interval_princess_lift/test_native_princess_extraction.cjs
python packages/interval_princess_lift/extract_lattice_princess.py verify
```

The native-report extractor compacts and interpolates an already certified
field while binding the original field/report/C++ hashes. It independently
checks every Qout inequality and the transfer fractions; it does not itself
repeat native pricing or claim an independent BigInt run:

```bash
node packages/interval_princess_lift/extract_native_princess.cjs packages/interval_clock_grid/lower_n256_field.json packages/interval_clock_grid/lower_n256_native_replay.json --output /tmp/native_princess
```

For prospective new lower candidates, first run the complete exact native
verifier on the new bytes. `interval_discovery/summarize.py` independently
checks the field and fractions and can request a second full implementation
with `--bigint`. Existing saved certificates need not be replayed during every
floating experiment. See HANDOFF.md for observed CI outcomes rather than
inferring success from this command list.

## Preserved B=1536 lattice lower

~~~bash
python packages/interval_global_closure/lattice_lower/replay_h3_lattice.py
node packages/interval_clock_grid/qout_primal_certificate.cjs packages/interval_clock_grid/upper_n64_physical.json.gz
~~~

The first command losslessly expands the frozen integer CDF, checks all hashes
and CDF inequalities, compiles the C++17 verifier, exhausts its entire lattice
response class, compares the full saved result, and recomputes the global bound
with Fraction. Python's standard library and g++ are sufficient; no optimizer,
NumPy or floating discovery interpolation is used. The full replay can take
several minutes and expands a 226,590,752-byte table before working arrays.
Use `--work-dir /tmp/princess-lattice` to retain the expanded table and replay.

The exact result is K=18308527154, C=12884901888, B=1536. Thus

    V >= K/C - 1/B = 3050023091/2147483648
      = 1.4202776788733899593353271484375.

This is an unrestricted **game-value** lower bound via the proved quantization
transfer. It does not assert that the same CDF has that security against all
continuous Monsters. The upper verifier checks every Princess path for the
703-pair physical Monster law.

A fast independent input/arithmetic check and the small exhaustive regressions:

~~~bash
python packages/interval_global_closure/lattice_lower/replay_h3_lattice.py --check-only
python packages/interval_global_closure/lattice_lower/test_integer_lattice.py
python packages/interval_global_closure/lattice_lower/test_inward_lattice.py
python packages/interval_global_closure/lattice_lower/test_endpoint_release.py
python packages/interval_global_closure/lattice_lower/test_early_outward.py
~~~

`--check-only` does **not** replay or independently establish the large search
minimum. The Fraction regressions enumerate coarse banks without the C++
dominance or pursuit pruning; they cover inward movement, partial record
crossings, shrinking endpoint atoms, both probability/cost scales, and both
centered and uncentered early exits. See the [proof](research/12-global-closure/INTEGER_LATTICE_VALUE_LOWER_CERTIFICATE.md)
and [manifest](packages/interval_global_closure/lattice_lower/h3_lattice_certificate.json)
for the exact scope and source/input hashes.


## Earlier finite-path and Monster regressions

~~~bash
python packages/interval_princess_geometry/verify_prefix_split.py
python packages/interval_uniform_reduction/exact_response.py packages/interval_princess_geometry/prefix_split_princess.json
python packages/interval_uniform_reduction/exact_response.py packages/interval_uniform_reduction/princess_strategy.json
node --stack-size=16384 packages/interval_global_closure/verify_full_order_upper.cjs
~~~

The first command deterministically reconstructs the 588-path prefix fixture and checks its exact unrestricted response; the second independently reads it through the original response program. The third reproduces the 338-path reference seed. The last verifies the 241-pair Monster upper. All bounds cover every legal opposing path. The 588-path value is 9072574958621987/6400000000000000; its gain over the source is only 60590851/25600000000000000, a strict-improvement regression rather than meaningful numerical closure. The nonattainment theorem makes the lower inequality strict.

## Finite-initial-support and contact obstructions

~~~bash
python packages/interval_global_closure/verify_finite_initial_support_obstruction.py
python packages/interval_princess_geometry/verify_geometry.py
~~~

The first checks rational prefix-splicing/contact fixtures for the analytic nonattainment and strict-improvement theorem. The second independently checks the all-reweightings ceiling, all direct captures, source geometry and exact mesh-collapse example; it also replays both exhaustive all-Monster minima. These finite checks do not replace the continuum proof in research/12-global-closure/FINITE_INITIAL_SUPPORT_NONATTAINMENT.md.

## Physical pressure, finite approximation and Princess extraction

~~~bash
python packages/interval_global_closure/replay_continuum_clock_certificate.py packages/interval_global_closure/reweighted_physical_clock_certificate.json.gz
python packages/interval_global_closure/verify_global_pressure_localization.py
python packages/interval_global_closure/verify_common_quantization.py
node packages/interval_global_closure/verify_randomized_interpolation.cjs
node packages/interval_clock_grid/verify_grid.cjs packages/interval_clock_grid/grid_n1_certificate.json
node packages/interval_clock_grid/record_pricing.cjs packages/interval_clock_grid/grid_n1_certificate.json
node packages/interval_clock_grid/verify_grid.cjs packages/interval_clock_grid/grid_n2_certificate.json
node packages/interval_clock_grid/record_pricing.cjs packages/interval_clock_grid/grid_n2_certificate.json
node packages/interval_clock_grid/verify_grid.cjs packages/interval_clock_grid/grid_n3_certificate.json
node packages/interval_clock_grid/record_pricing.cjs packages/interval_clock_grid/grid_n3_certificate.json
node packages/interval_clock_grid/verify_princess_extraction.cjs packages/interval_clock_grid/grid_n3_certificate.json packages/interval_clock_grid/grid_n3_princess.json
python packages/interval_global_closure/lattice_lower/test_integer_lattice.py
~~~

See [packages/interval_clock_grid/README.md](packages/interval_clock_grid/README.md) for n=1,2 Princess extraction commands. These finite grids do not attain a proved exact unrestricted value.

## Lower certificate engine and cell response regression

~~~bash
python packages/interval_global_closure/analytic_exit/replay_certificate.py packages/interval_global_closure/analytic_exit/coarse_characteristic_certificate.json
python packages/interval_global_closure/analytic_exit/test_replay.py
python packages/interval_global_closure/verify_two_run_continuation.py
~~~

The coarse lower fixture c=1.3387312615 is below best L. Independent exact arithmetic tests do not by themselves kernel-check continuum proofs.

All historical commands are preserved at [archive/handoffs/REPRODUCE-historical.md](archive/handoffs/REPRODUCE-historical.md).

## New structural and implementation regressions

```bash
node packages/interval_global_closure/left_floor_atomization_regression.cjs
node packages/interval_global_closure/uniform_leg_regression.cjs
python packages/interval_global_closure/verify_sharp_interpolation_loss.py
python packages/interval_global_closure/verify_full_width_refinement.py
python packages/interval_global_closure/verify_fullwidth_transfer_counterexample.py
node packages/interval_clock_grid/test_pursuit_pruning.cjs
node packages/interval_clock_grid/test_normalized_princess.cjs
python packages/interval_clock_grid/normalized_native/test_price_normalized.py
python packages/interval_clock_grid/normalized_native/test_interpolated_master.py
python packages/interval_clock_grid/normalized_native/test_cached_path_pricing.py
```

Numerical discovery requires NumPy and SciPy; the committed exact native field replay needs Python, a C++17 compiler and the standard libraries only. The BigInt replay needs Node. See [native discovery and verification](packages/interval_clock_grid/normalized_native/README.md) for the separation of floating optimization from exact certificates.

## Physical pressure retiming and finite-support normal form

```sh
python3 -B packages/interval_global_closure/verify_synchronized_pressure.py /tmp/synchronized_pressure_replay.json
```

This exact structural replay checks six resource-pair retimings, including sign swaps and collapsed demand; a complete two-path fully matched law compressed from six to four knots; 40 physical capture comparisons for the rate-limited tracker; and six contraction comparisons. These fixtures audit the constructions. The general matching and fixed-N completeness statements are proved analytically in [the manuscript](research/12-global-closure/SYNCHRONIZED_PRESSURE_AND_FINITE_SUPPORT.md). No finite optimal N or new game value is claimed.

## Exact front-one projection counterexample

```sh
python3 -B packages/interval_global_closure/verify_front_one_projection_counterexample.py --output /tmp/front_one_projection_counterexample_replay.json
```

This exhausts all 720 capture orders for each of two six-target legal laws and independently intersects the attaining physical route. Their unrestricted fixed-law securities are 47/40 and 469/400, with loss 1/400 under direct front-one completion. The accompanying bounded-density extension is an analytic existence proof, not an exact security claim for a supplied smoothing width. The dedicated geometry workflow runs this small regression; it starts no numerical discovery campaign.

## Exact continuous-response algebra

```sh
python packages/interval_global_closure/record_bellman/test_exact_quadratic_polytope.py
python packages/interval_global_closure/record_bellman/test_eliminate_quadratic_interval.py
```

These replay exact algebraic components, including singular stationary faces and degenerate parameter fibers. They do not certify a global security value without a supplied complete Bellman certificate or an exhaustive response construction.

The exact tail and renewal chart components can also be regenerated and checked against independent chronological Fraction integration:

```sh
python packages/interval_global_closure/record_bellman/test_chart_field_parser.py
python packages/interval_global_closure/record_bellman/build_endpoint_tail_charts.py packages/interval_clock_grid/grid_n2_princess.json /tmp/endpoint_tail_n2.json --epsilon 1/4 --direct-replay
python packages/interval_global_closure/record_bellman/build_center_excursion_charts.py packages/interval_clock_grid/grid_n2_princess.json /tmp/center_excursion_n2.json --epsilon 1/4 --direct-replay
```

The interpolation width is an explicit argument. The field parser accepts old expanded Princess artifacts, compact fields, and the newer nested normalized Princess artifacts; changing width changes the law and carries no inherited guarantee from another width.

## Complete finite center-value replay

The [n=1 center computation note](research/12-global-closure/EXACT_CENTER_ENVELOPE_N1.md) gives the full sequence: regenerate and byte-compare the 19 exact integral charts, run all five renewal layers with `--verify --history-output`, then independently integrate the reconstructed physical routes. The dedicated `exact-center-replay` CI job runs that entire sequence. Its exact center value 79/64 describes one fixed field and state, not the unrestricted game value.

## Complete continuous n=1 response

The [full response note](research/12-global-closure/EXACT_N1_CONTINUOUS_RESPONSE.md) and
[component README](packages/interval_global_closure/record_bellman/README.md) give
the complete input-chart checks. After the complete center regeneration above,
run:

```sh
python packages/interval_global_closure/record_bellman/build_endpoint_tail_charts.py packages/interval_clock_grid/grid_n1_princess.json /tmp/endpoint_n1_charts.json --epsilon 1/2 --direct-replay
python -c "from pathlib import Path; assert Path('/tmp/endpoint_n1_charts.json').read_bytes() == Path('packages/interval_global_closure/record_bellman/endpoint_tail_n1_fullwidth.json').read_bytes()"
python packages/interval_global_closure/record_bellman/exact_n1_precenter.py --field packages/interval_clock_grid/grid_n1_princess.json --center packages/interval_global_closure/record_bellman/center_envelope_n1_exact.json.gz --center-charts packages/interval_global_closure/record_bellman/center_excursion_n1_fullwidth.json.gz --tail packages/interval_global_closure/record_bellman/endpoint_tail_n1_fullwidth.json --output packages/interval_global_closure/record_bellman/n1_precenter_complete.json.gz --complete --verify
python packages/interval_global_closure/record_bellman/replay_n1_precenter.py packages/interval_global_closure/record_bellman/n1_precenter_complete.json.gz packages/interval_global_closure/record_bellman/center_envelope_n1_exact.json.gz packages/interval_clock_grid/grid_n1_princess.json /tmp/n1_precenter_replay.json
```

The first command independently checks 68 endpoint integrals. Complete
pre-center regeneration repeats all candidate and pruning calculations;
the separate replay checks 67 initial routes, 97 edge states, 1,989 affine
intervals and 29 exact whole-interval comparisons. The fixed-field security
is 39/32. This is not a new bound near the unrestricted game value.

## Boundary contacts and a common-warp family obstruction

```sh
python packages/interval_global_closure/verify_boundary_layer_kernel.py --physical-certificate packages/interval_clock_grid/upper_n64_physical.json.gz --report /tmp/boundary_layer_kernel_replay.json
python packages/interval_global_closure/verify_common_warp_family.py --physical-certificate packages/interval_clock_grid/upper_n64_physical.json.gz --family-certificate packages/interval_global_closure/n64_upper_common_warp_obstruction.json.gz --report /tmp/common_warp_family_replay.json
```

These deliberately use the **retained n=64 law**, not the newer n=128 upper.
The first verifier checks the two-parameter contact formula, all boundary
ties and the source law's endpoint-gap diagnostic. The second independently
constructs 41 clipped polynomial-germ Princess paths, computes all 57,646
first contacts, and proves a rational column inequality for every continuous
strict common light-coordinate warp of the fixed n64 law. Both use only
Python's standard library. Neither changes the unrestricted value bounds.

## Complete one-turn domain and physical upper

The complete canonical one-turn domain and exact trace conventions are proved in
[ONE_TURN_COMPLETE_DOMAIN.md](research/13-equilibrium-geometry/ONE_TURN_COMPLETE_DOMAIN.md).
The current all-Princess upper and closed-negative comparison are in
[ONE_TURN_SEPARATION_COUNTERCERTIFICATE.md](research/13-equilibrium-geometry/ONE_TURN_SEPARATION_COUNTERCERTIFICATE.md).
The [potential theorem](research/13-equilibrium-geometry/ONE_TURN_CONTINUUM_POTENTIAL_CERTIFICATE.md)
proves continuous coverage, all Princess normalization, initial crossings and terminal traces.

```sh
python3 packages/interval_one_turn/verify_continuum_upper.py \
  packages/interval_one_turn/one_turn_continuum_upper.json.gz \
  --output /tmp/one_turn_continuum_replay.json --require-counterexample
python3 packages/interval_one_turn/verify_continuum_upper.py --self-test
python3 packages/interval_one_turn/verify_continuum_functional.py
python3 packages/interval_one_turn/verify_continuum_physical.py
node packages/interval_one_turn/opposing_verify_finite_bank.cjs
```

The first command passes exactly 730,146 inequalities with zero repair and
returns 142472349375511/100000000000003<U_*. The Python fixture checks cover
physical chronological captures and density-bin integration. The last command
checks a separate 806-bank obstruction; it is explicitly not a full-B_1 lower.
These commands use no floating LP and trigger no CI. The earlier projected
atomic and causal-clock certificates remain independently reproducible:

```sh
python3 packages/interval_one_turn/verify_domain.py
python3 packages/interval_one_turn/verify_endpoint_repair.py
python3 packages/interval_one_turn/verify_finite_princess.py
python3 packages/interval_one_turn/rebuild_projected_upper.py --output /tmp/one-turn-projected
python3 packages/interval_one_turn/verify_projected_upper.py /tmp/one-turn-projected/one_turn_projected_upper.certificate.json
python3 packages/interval_one_turn/verify_projected_upper.py --self-test
python3 packages/interval_one_turn/rebuild_upper.py --output /tmp/one-turn-upper
python3 packages/interval_one_turn/verify_upper.py /tmp/one-turn-upper/one_turn_upper.sparse.json
```

The physical replay uses exact saved probabilities, paths, clocks and integer
flow/cut checks; no floating LP or CI run is needed. The compact law and exact
replay hashes are retained in `packages/interval_one_turn/one_turn_upper_replay.json`.
The improved 375-pair projected certificate and independent reconstruction are
recorded in `packages/interval_one_turn/one_turn_projected_upper_replay.json`;
its exact upper is `478205958821456999/335544320000000000`, still above U*.
The projected rebuild and replay both accept `--require-counterexample`,
which rejects the saved law.
This earlier atomic upper remains above the frozen benchmark; the current
continuum upper at the start of this section passes the counterexample gate.
