# Interval Princess–Monster — Unrestricted research

**Status: OPEN.** The exact minimax value is unknown. This PR contains analytical reductions and reproducible rational certificates, not a completed Lean proof.

Both players choose hidden 1-Lipschitz paths in [-1,1] from freely chosen initial positions. Capture is first coincidence, including time zero. The Princess maximizes expected capture time; Monster minimizes.

## Certified value bounds

\[
\frac{36409808231}{25600000000}
\le V\le
\frac{291849329389899}{204800000000000}.
\]

Numerically, **1.4222581340234375 ≤ V ≤ 1.4250455536616162109375**.

The [current certificates](research/12-global-closure/NORMALIZED_GLOBAL_BOUND_CERTIFICATES.md) combine a complete n=512 feasible Qout dual with a law on 752 reflected physical Monster pairs. The refined lower passed the unchanged complete C++ oracle, the compressed center oracle and independent BigInt target pricing. The upper has an exact flow-and-cut certificate independently reconstructed in Python and replayed in Node. The remaining exact interval width is **0.0027874196381787109375**. The earlier n256 and B=1536 lower certificates remain preserved.

The [saved n512 Princess quantile law](packages/interval_discovery_certificates/princess_front_n512/princess.json), using positive interpolation width 1/1024, guarantees **582556541071/409600000000 = 1.42225718034912109375** against every legal Monster. Letting that width tend to zero proves the slightly larger value lower above. The full replay and exact extraction passed in [run 43546803161](https://github.com/vltanh/lean4-monster-princess/actions/runs/43546803161). This new narrow-width law is distinct from the previous n256 law and the full-width CDF used to prepare the refined nodes.

The [finite-initial-support obstruction](research/12-global-closure/FINITE_INITIAL_SUPPORT_NONATTAINMENT.md) rules out an attained finite-start Princess equilibrium, including any finite path mixture. The earlier 588-path strict-improvement fixture and 338-path seed remain exact regressions, both below the new lower. Finite formulas for a continuous starting distribution and uniformly certified approaching families remain eligible.

## Discovery and structural progress

The intermediate width target below **1e-4** remains unmet. The new lower passed [independent BigInt replay and exact Princess extraction](https://github.com/vltanh/lean4-monster-princess/actions/runs/43546803161), with 893,765,461 generated transitions. Its inputs and reports are [retained in the repository](packages/interval_discovery_certificates/princess_front_n512/README.md), bound to the original CI artifact hashes.

A new [refinement ceiling](research/12-global-closure/FROZEN_FIELD_REFINEMENT_CEILING.md) proves that increasing the mesh alone for the saved full-width front-two field cannot produce a standard lower above **1.42290944208984375**. Holding the current upper fixed, this leaves a gap above 0.00213. Discovery therefore changes the CDF geometry and the physical Monster distribution; this obstruction is not an upper bound on the unrestricted value.

The [boundary discovery run](https://github.com/vltanh/lean4-monster-princess/actions/runs/43541622377) supplied the current upper after one completed n=256 iteration. Its [retained certificate](packages/interval_discovery_certificates/README.md) includes exact provenance and a portable independent verifier; both implementations passed in [run 43544245486](https://github.com/vltanh/lean4-monster-princess/actions/runs/43544245486). The previous n=128 law and the original discovery campaign remain preserved.

The [CDF shape workflow](.github/workflows/shape-discovery.yml) tests whether variation and curvature can be removed at a fixed security floor. Its [fixtures](packages/interval_cdf_shape/README.md) show both successful removal of many nodal oscillations and a concrete physical attack against naive cached-bank smoothing. The [heavier-first center theorem](research/12-global-closure/CENTER_HEAVIER_FIRST_BALANCE.md) supplies an exact alternating, rank-balanced continuation recurrence. These results narrow the structural search; they do not identify the unrestricted equilibrium.

The [exact center implementation](packages/interval_center_pricing/README.md) now uses the returning-triangle, rank-balance and incoming-front reductions in the complete integer response bank. Its phase-separated dominance proof and independent regressions preserve the original minimum. The initial phase before the first center remains unrestricted.

## Start here

- [HANDOFF.md](HANDOFF.md) — authoritative current theorem inventory, blockers and proof strategy
- [NEXT_WORK.md](NEXT_WORK.md) — standalone instruction for the next research continuation
- [ROADMAP.md](ROADMAP.md), [STATUS.md](STATUS.md) — brief gated plan and current status
- [REPRODUCE.md](REPRODUCE.md) — exact native replay commands
- [Core research index](research/12-global-closure/README.md) — full-game mathematics
- [Clock-grid LPs](packages/interval_clock_grid/README.md) — exact finite programs and dual extraction
- [Archive guide](archive/README.md) — historical proofs, failed experiments, handoffs and logs
- [Backed-up complete history](https://github.com/vltanh/lean4-monster-princess/tree/archive/pr1-pre-squash-2026-11-13)

## Global results and limitations

The [global incoming-front theorem](research/12-global-closure/GLOBAL_INCOMING_FRONT_COMPLETION.md) allows every Princess rank to be forced outward at its first hit of **t+|p|=C**, preserving its unrestricted security when **C=2U−1=1.850091107323232421875**. The grid-aligned choice C=2 is also sufficient. This restricts the whole characteristic region, beyond the earlier clock-time cutoff. A law-independent Monster normalization retains each prefix until the first endpoint or the first post-center hit of the same front, then takes a direct endpoint tour. It preserves the all-Princess upper of any symmetric center-by-C law. Consequently some globally optimal Monster law completes by **2V+2**, and hence by **4.850091107323232421875** using the current upper.

The [projected n=256 Princess law](packages/interval_global_closure/lower_n256_front2_princess.json) enforces the front-two identities while preserving the existing explicit security **1.42160610141845703125**. Its exact nodal projection inherits the already certified bank lower; no new exhaustive pricing or equality with the projected field's minimum is claimed. Independent Python and Node checks bind the old and new sources, all transport constraints and the unchanged guarantee. The front determines 65,536 stored nodes and leaves 196,864 in the synthesis domain.

Full-game minimax and an optimal symmetric Monster law, a separate physical Monster/clock model with fully matched pressure and completion by time 8, and an explicit rational finite LP approximation satisfying **U_n − 1/(2n) ≤ V ≤ U_n** have analytical manuscripts. The new shorter Monster normalization does not assert preservation of that earlier particular full-matching certificate. Exact common left-floor clock atomization and physical-bank normalization make the finite programs operational; exact small-grid certificates now include n=1,2,3,4,6.

The [full fixed-field response theorem](research/12-global-closure/COMMON_THRESHOLD_FIXED_CDF_RESPONSE.md) now covers supplied rational positive-width common-threshold Princess CDFs, including their off-center spatial diagonals. An exact Monster best response needs at most **248n+94 physical affine pieces** at full width, or **744n+218** at positive narrow width. Free initial positions, actual endpoint contacts, and originally infinite-turn paths are included. A finite collection of rational quadratic programs computes the exact response value and a rational attaining route. The proof uses the newly completed moving-floor and moving-ceiling half-cell lemmas; it has passed two independent mathematical reviews.

The sharper [post-center theorem](research/12-global-closure/FINITE_POSTCENTER_RESPONSE.md) gives **8n+4 unit-speed legs** at full width and **24n+4** at positive narrow width. Its exact quadratic envelope is operational for the n=1 fixture. **No theorem identifies a finite Princess mesh sufficient for the unrestricted equilibrium. No matching lower and upper certificates at one exact c are known.** Fixed-field exact response and finite-grid approximation do not by themselves close the game.

The [complete continuous n=1 response](research/12-global-closure/EXACT_N1_CONTINUOUS_RESPONSE.md) now includes every free starting position, the physical boundary cells, and the exact center continuation. Two rational quadratic formulas give the response at each initial radius; their global minimum is **39/32**. Complete candidate regeneration and independent chronological integration validate this supplied test field. It is not a new game-value bound.

The new [transport obstruction](research/12-global-closure/STRICT_TRANSPORT_FINITE_SUPPORT_OBSTRUCTION.md) and [initial-contact obstruction](research/12-global-closure/FINITE_P1_INITIAL_CONTACT_OBSTRUCTION.md) constrain proposed equilibrium phases without asserting that all optimal laws have a particular form. A [boundary-loop kernel](research/12-global-closure/BOUNDARY_LAYER_KERNEL_AND_GAP.md) explains the retained n=64 law's endpoint gap. An independent [common-warp certificate](research/12-global-closure/N64_UPPER_COMMON_WARP_OBSTRUCTION.md), with 57,646 exact symbolic captures, shows that deforming that law's whole geometry while retaining its probabilities can improve the current n=256 upper by less than **0.000005545424**. Further progress needs more than that fixed deformation family.

The [seed geometry audit](research/12-global-closure/PRINCESS_SEED_SUPPORT_AND_CONTACT_OBSTRUCTIONS.md) also proves an exact ceiling for every reweighting of the original 338 paths and shows why small uniform path perturbations can destroy its strict-contact geometry. A finite description of a CDF with infinite initial support remains a viable target.

The [bulk contact equations](research/12-global-closure/BULK_CONTACT_AND_CUSP_EQUATIONS.md) retain the endpoint survivor term and isolate the correction from a curved initial phase. The extended [boundary kernel](research/12-global-closure/BOUNDARY_LAYER_KERNEL_AND_GAP.md) includes outward/inward/outward shadow paths; these invalidate a loop-only boundary repair. Their strict supermodularity gives a conditional monotone contact relation. These equations constrain a continuum construction but do not yet close its active regions or certify all Monster responses.

The [initial-inward block](research/12-global-closure/INITIAL_INWARD_SHEET_CONTACT.md) makes its response constraints and complementary density equation explicit. The [moving-front and endpoint-return equations](research/12-global-closure/MOVING_FRONT_INITIAL_CONTACT.md) add an upper obstacle and a second lower obstacle on the same initial field, including endpoint atoms. Their synthesis is jointly convex, with legal extension and omitted-family constraints still required. A separate [central-return criterion](research/12-global-closure/SUPERADDITIVE_CENTRAL_RETURN_COMPRESSION.md) strictly compresses two opposite record-setting excursions when the field's central excess is superadditive, preserving their final time and later contacts. This provides a uniform reduction within a proved phase, while equilibrium sufficiency of that phase structure remains open.

The [curved initial-phase theorem](research/12-global-closure/CURVED_INITIAL_PHASE_RESPONSE.md) now reduces arbitrary initial responses to at most **three directional runs** within a phase satisfying explicit curvature inequalities, including an exact class of nonlinear incoming power layers. It retains both records and a certified concave outer continuation. A finite global phase cover has not been proved.

The [outer continuation theorem](research/12-global-closure/FRONT_CONTINUATION_GAPS_AND_ZENO.md) gives an exact one-parameter precenter continuation on the incoming front and a finite center-return count from a spatial density cap and a surviving-record gap. A strict center-start slack supplies that gap for all relevant responses. Adding a small stationary endpoint-pair component can create slack above the global upper, producing a value-dense class with a finite postcenter count for each member. The count can diverge in the limit. An explicit power-law field, and CDF blends arbitrarily close to global security, show why near-optimality alone cannot guarantee a finite response from the balanced center. The inner precenter triangle and sufficient initial phase geometry remain unresolved.

The [front-one contact analysis](research/12-global-closure/FRONT_ONE_CONTACT_NONALGEBRAICITY.md) gives two further constraints. An all-positive-start common principal/endpoint contact model is excluded by an exact sweep upper below the current lower; even a full common tail interval `(1/3,1)` is excluded. A common phase confined near the endpoint instead forces a **nonalgebraic initial trace**: attempting a fixed-denominator Puiseux expansion forces the incompatible exponents `1/2,3/4,7/8,...`. These conclusions assume front-one completion and their stated contact pattern; front-one global sufficiency is not established.

The active directories preserve verifier and input paths. Historical research is archived, never discarded.
