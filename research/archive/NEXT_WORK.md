# Next work — find the equilibrium geometry

## One-turn separation comparison: closed negatively (2026-11-14)

The [physical continuum countercertificate](research/13-equilibrium-geometry/ONE_TURN_SEPARATION_COUNTERCERTIFICATE.md) proves

\[
 V\le W_1\le\frac{142472349375511}{100000000000003}
 =1.424723493755067\ldots<\frac{57}{40}<U_*.
\]

The target W_1>U_* is therefore false. Alternative (M) of the [directive](research/13-equilibrium-geometry/ONE_TURN_SEPARATION_DIRECTIVE.md) is complete: a legal physical one-turn law has a universal all-Princess upper below the frozen benchmark. The exact integer potential certificate passes 730,146 rational inequalities with zero repair. Both the frozen-file replay and a separate fresh replay passed; independent physical capture and support audits also passed.

**Do not continue either side of this resolved comparison search.** The complete-domain theorem, restricted minimax and attained Monster measure, exact finite-Princess response, and convergent lower hierarchy remain available. The current exact values W_1 and V, their equality or strict inequality, and equilibrium support are still open. The remainder of this file is the unrestricted equilibrium-geometry plan.

---

**Light-cone program (2026-11-14/15).** Current bounds 1.4225745 ≤ V ≤ 1.4240199; the prioritized list is Section 4 of [research/14-light-cone-lattice/README.md](research/14-light-cone-lattice/README.md). The main points:

1. **Lower bound, the larger part of the gap.** The retained field cannot give more than about 1.4229 on any grid (n = 2048 would give about 1.42273, 4.5 hours and 42 GB with `price_center.cpp`). A finer profile is the concrete route: `solve_normalized.py n --profile-grid k`, seeded with `--seed` and `--profile-seed` from the next coarser solution, reaches k = 64 in about 20 minutes, and the best grid-k profiles fall about 0.078/k short of the value, so a grid-128 profile should certify about 1.4231 at n = 1024. The k = 128 stage at n = 256 needs the LP time limit in `persistent_highs.py` raised above 120 s; with 3600 s it ran an hour without improving its seed and was stopped. [REFINED_N1024_LOWER.md](research/14-light-cone-lattice/REFINED_N1024_LOWER.md), Section 4, has the measurements.
2. **Independent replay of the n = 1024 lower bound** with `packages/interval_center_pricing/verify_bigint.cjs` (17 minutes at n = 512, expected several hours at n = 1024).
3. **Upper bound.** `optimize_atomic_law.py` optimizes a law for one grid with the exact program as its oracle; the optimum on the grid 1/N is about V + 0.08/N, so a law for 1/4096 gains at most about 5e-5. Adding the Monster's loitering paths to the families is the change that could matter more. A proof of W_1 > V needs a Princess law that guarantees more than 1.42402 against every one-turn Monster.
4. **Exact solution.** Complete [the indifference equations](research/14-light-cone-lattice/ONE_TURN_INDIFFERENCE_EQUATIONS.md) with the layer before time 1, the two-turn paths and the thresholds.
5. **Pricing without a lattice.** `packages/interval_lightcone/capture_order_pricing.cpp` prices a finite ordered Princess law exactly against every continuous Monster, as a shortest path over (captured interval, side), with no 1/(2n) transfer loss. The engine is fast enough (1000 paths in 22 s); the obstacle is a finite law close enough to the optimum: the best so far is worth 1.4137, and laws drawn from a lattice field lose about 0.04/M on M shifted copies. Numbers and tests are in `capture_order_pricing.py`.

**Main question:** What are the **global transport-compatible contact phases and free boundaries** of an optimal (or uniformly approaching) Princess CDF, and which Monster paths actually support the associated saddle?

**Do not** restart the resolved one-turn separation test or repeat mesh refinement on the frozen Princess field. The remaining milestone is a globally sufficient equilibrium geometry and a matching strategy pair.

## Start with these files

1. [Geometry overview](research/13-equilibrium-geometry/README.md), [contact atlas](research/13-equilibrium-geometry/CONTACT_ATLAS.md), [proof gates](research/13-equilibrium-geometry/PROOF_GATES.md), [working note](research/13-equilibrium-geometry/WORKING_NOTE.md).
2. [Global CDF first variation](research/12-global-closure/GLOBAL_CDF_VARIATIONAL_STATIONARITY.md), [transport](research/12-global-closure/GLOBAL_CDF_TRANSPORT_LP.md) and [incoming-front completion](research/12-global-closure/GLOBAL_INCOMING_FRONT_COMPLETION.md).
3. [Initial-inward exact block](research/12-global-closure/INITIAL_INWARD_SHEET_CONTACT.md), [moving-front P/J obstacles](research/12-global-closure/MOVING_FRONT_INITIAL_CONTACT.md), [bulk moments](research/12-global-closure/BULK_CONTACT_AND_CUSP_EQUATIONS.md) and [shadow contacts](research/12-global-closure/BOUNDARY_LAYER_KERNEL_AND_GAP.md).
4. [Curved precenter phase](research/12-global-closure/CURVED_INITIAL_PHASE_RESPONSE.md), [positive-prefront extension and inner class exclusion](research/12-global-closure/POSITIVE_PREFRONT_RESPONSE_AND_MODULUS.md), [outer gap/Zeno obstruction](research/12-global-closure/FRONT_CONTINUATION_GAPS_AND_ZENO.md) and [two-record center renewal](research/12-global-closure/CENTER_RECORD_RENEWAL_CERTIFICATE.md).

## Specific first attack: the initial contact atlas

Use coordinates U=t+x, W=t−x and an ordered signed CDF F with F_x≥|F_t| wherever smooth. Put all proposed precenter P, S, I, J and shadow contacts on **one field**, retaining endpoint atoms and the negative-start / late-turn branches. Record which equations are exact consequences of physical first capture and which equal-cost or active-set assumptions remain hypotheses.

Prove **one** of the following substantive outcomes:

- an all-Monster-sufficient reduction covering the inner precenter triangle and both W=0 and incoming-front exits, with a continuation that depends on both surviving records;
- a legal continuous, potentially nonalgebraic CDF phase satisfying transport and a global set of complementary contact inequalities, plus a full-path certificate; or
- an exact physical counterexample to a specific proposed phase/contact pattern, strong enough to eliminate that pattern instead of just adding another test path.

A sampled optimal profile and numerical coincidence of contact costs are not such outcomes.

**Use the newly proved obstruction:** do not maintain `F_UU>=0` and `F_UW>=0` throughout the inner triangle through `U=41/40`. That class has sweep cost below 1137/800, so cannot approach the current game lower. Determine a changed inner phase or prove a separate front-one restriction sufficient. The whole-region first-exit theorem is valid conditionally but cannot justify the excluded front-two class. Center continuity plus record slack supplies a finite count for each fixed field; an all-count potential remains an alternative. The [global static Zeno example](research/12-global-closure/GLOBAL_FREE_START_ZENO_COUNTEREXAMPLE.md) prevents an unconditional finite-turn shortcut, while leaving the near-optimal regular case open.

## Validation and handoff

Use [geometry structural regressions](.github/workflows/geometry-structural-checks.yml) to audit *identities on test fixtures*; these are not universal proofs. Use [REPRODUCE.md](REPRODUCE.md) only when a change affects the certified inequalities. Add tested conjectures, disproofs and open interfaces to [WORKING_NOTE.md](research/13-equilibrium-geometry/WORKING_NOTE.md); update [STATUS.md](STATUS.md). Every new theorem must state its assumptions, all endpoint/center cases, proof of arbitrary-path sufficiency, and whether a physical dual has been constructed.

**Stop criteria:** if a proposed family is not proved exhaustive, state the exact missing family/phase instead of silently optimizing the restricted game. A functional/integral-equation characterization is a legitimate exact solution; an elementary constant is not a prerequisite.

The complete pre-reorganization research plan is archived at [archive/handoffs/NEXT_WORK-2026-11-14-numerical.md](archive/handoffs/NEXT_WORK-2026-11-14-numerical.md). The game remains OPEN.
