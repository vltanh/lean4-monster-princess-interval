> **Research navigation (2026-11-14 UTC):** the active question is now the *equilibrium contact geometry*. Start with [research/13-equilibrium-geometry](../13-equilibrium-geometry/README.md), its [contact atlas](../13-equilibrium-geometry/CONTACT_ATLAS.md) and [proof gates](../13-equilibrium-geometry/PROOF_GATES.md). This directory remains the preserved reference index of mathematical manuscripts; conditional contact identities and fixed-field response reductions do not establish global equilibrium sufficiency.

# Core unrestricted game proofs — current reading order

[Canonical handoff](../../HANDOFF.md) · [Next research instruction](../../NEXT_WORK.md) · [Reproduction](../../REPRODUCE.md) · [Archive](../../archive/README.md)

1. **Global minimax and legal Princess CDF:** [minimax/quantiles](GLOBAL_MINIMAX_AND_CDF_DUALITY.md), [transport](GLOBAL_CDF_TRANSPORT_LP.md), [CDF stationarity](GLOBAL_CDF_VARIATIONAL_STATIONARITY.md).
   **New global obstruction:** [finite initial Princess support cannot attain V; every such law is strictly improvable](FINITE_INITIAL_SUPPORT_NONATTAINMENT.md). The [338-path support/contact audit](PRINCESS_SEED_SUPPORT_AND_CONTACT_OBSTRUCTIONS.md) closes useful reweighting of that seed and isolates its two contact fronts.
2. **Global characteristic-front reduction:** [incoming-front Princess completion and Monster decision-front normalization](GLOBAL_INCOMING_FRONT_COMPLETION.md). Security-preserving C=2U−1; an optimal Monster completes by 2V+2. The grid-aligned C=2 projection also preserves every normalized-bank lower. Earlier inputs: [outward time 2](SHARP_OUTWARD_HORIZON_REDUCTION.md), [sticky endpoint density](STICKY_CDF_DENSITY.md).
3. **Physical dual:** [one-clock dual](GLOBAL_INFINITE_HORIZON_ACTIVE_DUAL.md), [causal pressure matching](GLOBAL_CAUSAL_PRESSURE_MATCHING.md), [physical lift](FINITE_STATE_PHYSICAL_CLOCK_LIFT.md).
4. **Synchronized physical matching and conditional finite support:** [equal-time/first-antipodal retiming and finite polygonal realization](SYNCHRONIZED_PRESSURE_AND_FINITE_SUPPORT.md). This fixes trajectory complexity once the fully matched support size N is supplied; it does not prove finite optimal support.
   **Attained full matching:** [localization](POST_FIRST_ENDPOINT_PRESSURE_LOCALIZATION.md), [physical correction](GLOBAL_ZERO_DEFICIENCY_REDUCTION.md), [attainment](GLOBAL_ZERO_DEFICIENCY_ATTAINMENT.md); [nonphysical Eulerian gap](EULERIAN_RELAXATION_GAP.md) rules out a false shortcut.
5. **Effective global finite LP:** [quantitative approximation](EFFECTIVE_FINITE_UPPER_REDUCTION.md), [O(n^4) clock graph](POLYNOMIAL_CLOCK_GRID_LP.md), [Princess dual extraction](CONSTRUCTIVE_PRINCESS_GRID_DUAL.md).
   **Current strongest value lower:** [complete n512 refined certificate](NORMALIZED_GLOBAL_BOUND_CERTIFICATES.md), checked by the original integer oracle, compressed center engine and independent BigInt. The [exhaustive B=1536 lattice response and exact time-one exit](INTEGER_LATTICE_VALUE_LOWER_CERTIFICATE.md) remain a separate weaker certificate.
6. **Complete finite response for a supplied common-threshold CDF:** [full theorem and exact rational computation](COMMON_THRESHOLD_FIXED_CDF_RESPONSE.md), [moving floor](AFFINE_MOVING_FLOOR_HALF_CELL.md), [moving ceiling](AFFINE_MOVING_CEILING_HALF_CELL.md), [moving-interface returns](MOVING_KINK_RETURN_COMPRESSION.md). Earlier inputs: [two-run continuation](TWO_RUN_AFFINE_CELL_WITH_CONTINUATION.md), [boundary cases](BOUNDARY_CELL_RECORD_PROJECTION.md). Separate lower certificates: [analytic exit potential](ANALYTIC_EXIT_POTENTIAL.md), [completeness](FINITE_POTENTIAL_HIERARCHY_COMPLETENESS.md).
7. **Current explicit upper:** [CI-discovered 752-pair law and independent replay](../../packages/interval_discovery_certificates/README.md). Earlier inputs:  [241-pair exact certificate](FULL_ORDER_CDF_UPPER_CERTIFICATE.md), [clock homogenization](FINITE_BANK_CLOCK_HOMOGENIZATION.md), [continuum residual correction](ENDPOINT_FRONT_DEFICIENCY_COMPLETION.md).
8. **Subtle strict contacts:** [radial germs](GLOBAL_RADIAL_CONTACT_GERMS.md), [finite support response](GERM_RESPONSE.md), [realization](GENERALIZED_GERM_REALIZATION.md).

The foundational signed Monster Bellman theorem remains at [research/10-turn-density/GLOBAL_CDF_BELLMAN.md](../10-turn-density/GLOBAL_CDF_BELLMAN.md). Historical failed candidates, restricted-phase papers, and old multi-page status handoffs have been archived under [archive/legacy-research](../../archive/legacy-research/).

**Missing theorem:** fixed equilibrium complexity or a matching unrestricted Princess lower/physical Monster upper at one exact c. Older historical relative links may require the [relocation map](../../archive/RELOCATION_MAP.md); original blobs are backed up.

## Exact normalized-bank continuation

- [Common left-floor clock atomization](LEFT_FLOOR_CLOCK_ATOMIZATION.md): exact finite physical-bank value, without restricting continuous clock laws.
- [Normalized grid-bank pricing](NORMALIZED_GRID_BANK_PRICING.md): first-endpoint/time-two physical normalization, Qout dual equivalence, and law-specific global primal upper.
- [Equivalent uniform-leg clock LP](POLYNOMIAL_UNIFORM_LEG_CLOCK_LP.md): independent finite refinement; no improvement over the atomized bank value.
- [Exact compressed center pricing](DISCRETE_CENTER_BALANCE_PRICING.md) and [implementation](../../packages/interval_center_pricing/README.md): phase-specific dominance, straight returns and the front guard preserve the complete integer minimum.
- [Exact pursuit pruning](NORMALIZED_PURSUIT_LOWER_BOUND.md): complete pricing acceleration with no heuristic state deletion.
- [Current unrestricted rational bounds](NORMALIZED_GLOBAL_BOUND_CERTIFICATES.md) and [explicit feasible-dual Princess extraction](NORMALIZED_PRINCESS_EXTRACTION.md).
- [Full-width refinement identity](FULL_WIDTH_INTERPOLATION_REFINEMENT.md), [sharp narrow-width loss](SHARP_NARROW_INTERPOLATION_LOSS.md), and [full-width quarter-mesh counterexample](FULL_WIDTH_TRANSFER_COUNTEREXAMPLE.md).

The current exact interval is **1.4222581340234375 ≤ V ≤ 1.4250455536616162109375**. Exact value, matching strategies and finite equilibrium sufficiency remain open. The two new interpolation counterexamples rule out universal quarter-mesh transfer for arbitrary feasible Qout profiles.

## Discovery with exact separation

- [Continuous-record hypographs](CONTINUOUS_RECORD_HYPOGRAPHS.md): exact convex constraints for admitted unit-speed routes and conservative secant-LP error; known-path optimization remains distinct from unrestricted certification.
- [Frozen-field refinement ceiling](FROZEN_FIELD_REFINEMENT_CEILING.md): a verified continuous attack and monotone edge quadrature cap every compatible standard refinement certificate. The current field cannot reach width below 1e-4 with the physical upper held fixed.
- [Retained n512 Princess certificate](../../packages/interval_discovery_certificates/princess_front_n512/README.md): complete original/center native search, independent BigInt verification and explicit strategy extraction.
- [Record-hypograph geometry search](../../packages/interval_continuous_lower/README.md) and [joint physical Monster search](../../packages/interval_mixture_cut/README.md): discovery models with exact acceptance gates and resumable CI artifacts.
- [Fixed-law n512 clock obstruction](../../packages/interval_fixed_marginal/ci_n512_obstruction/README.md): all-calendar nodal-family exclusion, with a separately evaluated continuous response and explicit scope.

- [Physical lattice-to-explicit-Princess bridge](PHYSICAL_LATTICE_PRINCESS_EXTRACTION.md): produces a new legal law; does not assign continuum security to the frozen source.
- [Parallel CDF and Monster discovery](../../packages/interval_discovery/README.md), [retained exact upper](../../packages/interval_discovery_certificates/README.md), and [shape regularization with a physical counterexample](../../packages/interval_cdf_shape/README.md).

## Continuous response closure components

- [Complete common-threshold response](COMMON_THRESHOLD_FIXED_CDF_RESPONSE.md): 248n+94 physical affine pieces at full width; 744n+218 at positive narrow width. Finite rational quadratic programs give the exact fixed-field value and a rational attaining response, with free starts and actual endpoint contacts.
- [Finite post-center response](FINITE_POSTCENTER_RESPONSE.md): sharper bounds of 8n+4 legs at full width and 24n+4 at positive narrow width.
- [Heavier-first rank-balance recurrence](CENTER_HEAVIER_FIRST_BALANCE.md): alternate excursions toward the heavier surviving side; returned records interlace.
- [Incoming-front terminal guard](GLOBAL_INCOMING_FRONT_COMPLETION.md): proper returns from center time t have height at most (C−t)/2, and the post-center front has an exact two-tour terminal cost. Regularity and center-record hypotheses are explicit.
- [Curved initial-phase response reduction](CURVED_INITIAL_PHASE_RESPONSE.md): at most three directional runs in a qualified nonpolynomial phase, with an explicit two-record outer certificate and arbitrary-path closure. A finite global phase cover is still required.
- [Front continuation, record gaps and initial Zeno](FRONT_CONTINUATION_GAPS_AND_ZENO.md): exact one-parameter front terminal, density/slack return count, endpoint mixing for a value-dense finite-postcenter class, and the explicit obstruction to a uniform fixed-center cutoff.
- [Positive prefront response and center modulus](POSITIVE_PREFRONT_RESPONSE_AND_MODULUS.md): continuity replaces the density hypothesis; the whole-region exchange gives at most three runs, but its inner monotonicity class is excluded below the game lower once it extends through U=41/40.
- [Global free-start Zeno counterexample](GLOBAL_FREE_START_ZENO_COUNTEREXAMPLE.md): a static majority-center-atom law has an attained optimum and every optimal Monster reverses infinitely often near time zero; this low-security example excludes a universal finite-turn theorem, not an equilibrium class.
- [Compensated curvature and finite global cusp response](COMPENSATED_CURVATURE_AND_CUSP_RESPONSE.md): a weaker invariant RLR exchange resolves the atom-free cusp's free-start finite attainment; its whole-inner extension is still excluded by the sweep bound at U=21/16.
- [Superadditive central-return compression](SUPERADDITIVE_CENTRAL_RETURN_COMPRESSION.md): a uniform strict pair-compression rule preserving the final center time and complete continuation, for fields satisfying the additional interval-excess inequality. Additive and concave-density fields are sufficient examples.
- [Prefix-compression diagnostic](INITIAL_PREFIX_COMPRESSION_DIAGNOSTIC.md): a later contact front defeats global time advance; actual fixed-front compression can depend on future record sensitivities. Exact chronological replay is available.
- [Exact parametric center value](PARAMETRIC_CENTER_VALUE_QUADRATICS.md): finite quadratic envelope with rational attainment and bounded-depth scalar elimination.
- [Actual-record Bellman lift](FINITE_RECORD_BELLMAN_LIFT.md) and [three-state center renewal](CENTER_RECORD_RENEWAL_CERTIFICATE.md): sufficient finite quadratic certificate conditions covering arbitrary controls and countable excursions.
- [Exact rational polytope minima](EXACT_QUADRATIC_POLYTOPE_MINIMA.md) and [bounded scalar elimination](EXACT_SCALAR_QUADRATIC_ELIMINATION.md).
- [Exact endpoint-tail charts](ENDPOINT_TAIL_QUADRATIC_CHARTS.md) and [partial center-outward charts](CENTER_EXCURSION_QUADRATIC_CHARTS.md).
- [Stationary spatial-kink response bound](STATIONARY_KINK_RECORD_RESPONSE.md).

- [Operational exact n=1 center envelope](EXACT_CENTER_ENVELOPE_N1.md): complete five-layer regeneration, 48 candidates, exact center value 79/64 and independent physical-route integration.
- [Moving-interface return compression](MOVING_KINK_RETURN_COMPRESSION.md): four unit-speed legs and an interface hold in an interior square.
- [Moving-floor affine half-cell](AFFINE_MOVING_FLOOR_HALF_CELL.md) and [moving-ceiling affine half-cell](AFFINE_MOVING_CEILING_HALF_CELL.md): record-preserving five- and 13-piece bounds; no affine extension outside the legal half-cell.

- [Complete continuous n=1 response](EXACT_N1_CONTINUOUS_RESPONSE.md): exact free-start security 39/32, two-quadratic initial-position value, full pre-center enumeration and independent physical replay.

## Equilibrium phase and fixed-family obstructions

- [Strict transport and finite Monster support](STRICT_TRANSPORT_FINITE_SUPPORT_OBSTRUCTION.md): active record capture cannot occur inside a strict transport patch in the stated best-response pair; saturated regions and interfaces remain possible.
- [Finite P1 initial-contact obstruction](FINITE_P1_INITIAL_CONTACT_OBSTRUCTION.md): an affine positive-density initial cell forces a short inactive inward layer; the excluded contact pattern is conditional, not a classification of every equilibrium.
- [Two-parameter endpoint-layer kernel](BOUNDARY_LAYER_KERNEL_AND_GAP.md): exact start/loop payoff with all ties; the retained n64 upper is explained almost exactly by its endpoint gap.
- [Bulk contact and cusp equations](BULK_CONTACT_AND_CUSP_EQUATIONS.md): exact principal/endpoint moments and transport pressure; a nonnegative initial correction prevents an unjustified three-trace closure.
- [Direct front-one projection security loss](FRONT_ONE_PROJECTION_SECURITY_LOSS.md): complete six-target all-path values 47/40 and 469/400, exact 1/400 loss, and a bounded-density regularization extension. Universal projection preservation fails; value-level sufficiency remains open.
- [Front-one contact exclusions and nonalgebraicity](FRONT_ONE_CONTACT_NONALGEBRAICITY.md): rational near-center support exclusions, a forbidden broad common P/S tail phase, and an incompatible formal Puiseux cascade for near-endpoint E/P/S contacts. These are conditional on the front-one model.
- [Endpoint square-root contact](ENDPOINT_SQUARE_ROOT_CONTACT.md): conditional flat sweep/principal costs force a square-root initial tail and universal first-front time, with no derivative or ordinary-path ansatz; finite P1 fields are excluded under those same hypotheses.
- [Exact initial-inward contact and adjoint block](INITIAL_INWARD_SHEET_CONTACT.md): actual-capture moments, an inactive-branch dominance test, scalar inversion, joint convex legal-trace synthesis, and the complementary backward density equation. General endpoint and earlier-center rows remain outside this block.
- [Moving-front and endpoint-return obstacles](MOVING_FRONT_INITIAL_CONTACT.md): positive-P upper and inward-valley J lower constraints, endpoint atom corrections and joint convexity on a common legal global extension.
- [Boundary shadow and inward-sheet extensions](BOUNDARY_LAYER_KERNEL_AND_GAP.md): exact chronological contacts, the missed loop-only attack, and a conditional monotone outer contact relation. The current n128 initial gap has a separate exact diagnostic receipt.
- [Law-specific outward completion](LAW_SPECIFIC_OUTWARD_COMPLETION.md): a fixed-opponent ordered cutoff; no automatic preservation of an unrestricted Princess guarantee.
- [Retained n64 common-warp obstruction](N64_UPPER_COMMON_WARP_OBSTRUCTION.md): 41 profiles and 57,646 exact symbolic captures prove a class lower of 1.4250400082376236269997635 for fixed probabilities under every strict common warp. This is not an unrestricted lower on V.
