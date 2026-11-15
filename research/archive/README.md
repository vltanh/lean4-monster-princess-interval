> **Archive.** This folder is a snapshot of our research repository as it stood on 2026-11-15, when
> that repository was retired. It covers the work from 2026-11-10 to 2026-11-15. Nothing here is
> maintained, and some notes are superseded by later ones. Links inside the folder are relative
> to it, and the workflows in `.github/` no longer run. The current account of the bounds and the
> maintained copies of the programs they need are in [`research/`](../README.md). Status labels in
> these notes, such as "certified" or "proved", are the notes' own, and only the results restated
> in `research/` have been rechecked.

# Princess–Monster on the interval: equilibrium geometry

**One-turn comparison CLOSED negatively; unrestricted exact game OPEN.** Two hidden players choose arbitrary initial positions and 1-Lipschitz paths in [-1,1]; capture occurs at first coincidence, including time zero. The Princess maximizes expected capture time and the Monster minimizes.

The independently checked enclosure is

\[
\frac{36409808231}{25600000000} \le V \le
\frac{142472349375511}{100000000000003}.
\]

That is **1.4222581340234375 ≤ V ≤ 1.424723493755067…**, width **0.002465359731629758…**. These are certified inequalities, **not** an exact value or an equilibrium. The saved explicit positive-width Princess law guarantees **1.42225718034912109375**, not the larger limiting value lower.

**Newer bounds (2026-11-15), with less checking than the enclosure above:**

\[
\frac{9322984150699}{6553600000000} \le V \le \frac{1603303881142469}{1125899906842624},
\]

that is **1.4225745 ≤ V ≤ 1.4240199**, width 0.0014454. The lower bound has the same minimum from both native pricing engines but no independent BigInt replay; the upper bound is a written proof with an exact integer computation in two implementations, not yet independently reviewed. Results, strategies and next steps: [the light-cone summary](research/14-light-cone-lattice/README.md). Interactive pictures of both strategies: [strategies.html](research/14-light-cone-lattice/strategies.html) (open the file in a browser).

## One-turn comparison closed

The [physical continuum countercertificate](research/13-equilibrium-geometry/ONE_TURN_SEPARATION_COUNTERCERTIFICATE.md) proves **V ≤ W_1 ≤ 142472349375511/100000000000003 < 57/40 < U_***, where U_* remains the frozen earlier upper. Its Monster law uses an endpoint-sweep pair and seven piecewise constant start densities, each supported on legal canonical one-turn paths. The standard-library verifier checks all 730,146 exact rational potential inequalities with **zero residual repair**. This defeats the proposed strict separation W_1 > U_*. The exact restricted value, W_1 = V, and an unrestricted saddle remain open.

## Read first: geometry program

- **[Geometry index](research/13-equilibrium-geometry/README.md)** — active research program and reading order
- **[Contact atlas](research/13-equilibrium-geometry/CONTACT_ATLAS.md)** — physical attack families and missing interfaces
- **[Proof gates](research/13-equilibrium-geometry/PROOF_GATES.md)** — what would constitute an actual global solution
- **[Geometry notebook](research/13-equilibrium-geometry/WORKING_NOTE.md)** — hypotheses to test or disprove, with explicit scope
- [NEXT_WORK.md](NEXT_WORK.md) — one focused continuation instruction
- [HANDOFF.md](HANDOFF.md) and [STATUS.md](STATUS.md) — condensed authoritative checkpoint and result ledger

The critical obstacle is **global geometric sufficiency**: existing equations price important path families, and existing Bellman/center certificates give conditional all-path tests, but no theorem identifies the equilibrium's active CDF phases and Monster contacts. An optimal Princess law cannot have finite support in its **initial positions**. A conditional near-endpoint contact model may require a nonalgebraic initial trace. Neither observation rules out an exact functional or variational characterization.

**New geometric exclusion:** [the positive-prefront and modulus theorem](research/12-global-closure/POSITIVE_PREFRONT_RESPONSE_AND_MODULUS.md) extends the three-run exchange to first center/front/endpoint exit, but also proves that its curvature cannot persist throughout the inner region: monotonicity of `F_U` in both light coordinates through `U=41/40` gives an endpoint-sweep cost below **1137/800 = 1.42125**, below the certified game lower. A competitive construction must change that inner phase. Joint continuity and a positive record gap also suffice for a finite postcenter count; no density bound is needed.

A separate [static counterexample](research/12-global-closure/GLOBAL_FREE_START_ZENO_COUNTEREXAMPLE.md) proves that every optimal **free-start** Monster response can require infinitely many initial reversals. Its Princess law has a center atom and security at most one-third, so it excludes a universal finite-turn theorem for all legal fields, without excluding a finite equilibrium-sufficient class.

For the distinct **atom-free front-one power cusp**, a [compensated curvature exchange](research/12-global-closure/COMPENSATED_CURVATURE_AND_CUSP_RESPONSE.md) now proves an attained finite-turn global free-start response, using the earlier strict comparison with the centered infinite-turn optimum. The broader curvature condition still cannot cover the whole inner region competitively: through U=21/16 its sweep upper is 91/64, below the certified game lower.

## New global reduction and projection obstruction

The [synchronized physical-pressure theorem](research/12-global-closure/SYNCHRONIZED_PRESSURE_AND_FINITE_SUPPORT.md) moves every matched pair to a common history time and then to its first antipodal encounter. Positive-time matches can cancel at exactly the same radius; only time-zero matches need radial dominance. Physical paths and causal clocks remain coupled. For a fully matched law with N oriented paths, this yields finitely many clock events and a polygonal physical realization with at most N+2 knots per path. **Finite optimal support remains unproved**, so this is a conditional finite reduction, not the requested game solution.

The [direct front-one projection counterexample](research/12-global-closure/FRONT_ONE_PROJECTION_SECURITY_LOSS.md) has exact source security 47/40 and projected security 469/400, a strict loss of 1/400. Exhausting all 720 capture orders for each six-target law proves the free-start optima. The loss also persists for some regular bounded-density laws. These low-security examples exclude universal projection preservation; they do not exclude value-level front-one sufficiency.

## Preserved proof and computation

- [Core mathematical manuscripts](research/12-global-closure/README.md) — minimax, transport, incoming fronts, actual two-record response, contact equations, conditional phase reductions
- [Current one-turn and unrestricted upper](research/13-equilibrium-geometry/ONE_TURN_SEPARATION_COUNTERCERTIFICATE.md), [retained lower and earlier upper certificates](research/12-global-closure/NORMALIZED_GLOBAL_BOUND_CERTIFICATES.md), and [retained data](packages/interval_discovery_certificates/README.md)
- [Reproduction commands](REPRODUCE.md) — independent full and compact checks, with expensive searches opt-in
- [Code / certificate package map](packages/README.md) — active geometry checks, frozen exact certification, archived discovery machinery
- [Historical handoffs and numerical phase](archive/README.md) — immutable snapshots; full pre-squash branch also preserved

**CI policy:** the old parameter searches are manual-only, while exact regression and certificate workflows remain available. Do not reinterpret a sampled path bank, fixed-field optimizer, conditional contact law, or successful CI fixture as proof of the unrestricted saddle.

This is a research manuscript and computational-certificate repository, **not a complete Lean proof**.
