# Handoff — equilibrium geometry of the unrestricted interval game

**2026-11-14 UTC | one-turn comparison CLOSED negatively | exact game OPEN.**
This replaces the 52 KB numerical handoff; the complete previous text is at [archive/handoffs/HANDOFF-2026-11-14-numerical.md](archive/handoffs/HANDOFF-2026-11-14-numerical.md). No certificates or mathematical manuscripts were deleted.

## Precise objective

Let Princess and Monster independently choose hidden 1-Lipschitz paths in [-1,1], with unrestricted starting positions. Payoff is their first coincidence, including time zero. Establish an **unrestricted saddle characterization**: an admissible continuous Princess CDF (or uniformly approaching sequence), a physical Monster law, and matching all-path inequalities at one value. A closed-form elementary constant is not required. Our first obstacle is the **global contact/phase geometry**, not numerical precision.

## Frozen, certified facts

| Item | Exact scope |
| --- | --- |
| Game-value lower | **36409808231/25600000000 = 1.4222581340234375**; n512 front refinement, complete original/center native pricing, independent BigInt target search, proved 1/1024 transfer |
| Saved fixed Princess law | **582556541071/409600000000 = 1.42225718034912109375** against every Monster at interpolation width 1/1024; do not assign the larger limiting lower to this file |
| Game-value upper | **142472349375511/100000000000003 = 1.424723493755067…**; physical continuous one-turn law, 730,146 exact potential inequalities, zero repair |
| Remaining width | **6311320912972370575307/2560000000000076800000000 = 0.002465359731629758…**; no claimed sub-1e-4 width or exact value |
| Attainment | Symmetric optimal Monster law exists by the analytical minimax manuscripts; no finite-initial-support Princess law attains V |
| Finite algorithms | Rational LP hierarchy and fixed positive-width piecewise-linear CDF exact Monster response are valid, but **not equilibrium-sufficient** |

[Current upper theorem](research/13-equilibrium-geometry/ONE_TURN_SEPARATION_COUNTERCERTIFICATE.md) · [retained lower and historical upper theorem](research/12-global-closure/NORMALIZED_GLOBAL_BOUND_CERTIFICATES.md) · [retained proof files](packages/interval_discovery_certificates/) · [exact replay](REPRODUCE.md). These are mathematical arguments and exact computational certificates, not a completed Lean formalization.

## Light-cone program (2026-11-14/15): new bounds and the two strategies

[research/14-light-cone-lattice/README.md](research/14-light-cone-lattice/README.md) is the summary; [strategies.html](research/14-light-cone-lattice/strategies.html) draws both strategies. In short:

| Bound | Value | Checking | Missing |
| --- | --- | --- | --- |
| Lower | **V ≥ 9322984150699/6553600000000 = 1.4225744858854674** | retained n512 field refined exactly to n = 1024 ([package](packages/interval_discovery_certificates/princess_front_n1024/README.md)); `price_normalized.cpp` and `price_center.cpp` return the same bank minimum 18652368301398/13107200000000 | independent BigInt replay (started, stopped after 15 minutes) |
| Upper | **V ≤ 1603303881142469/1125899906842624 = 1.4240199075…** | atomic Monster law of one-turn and two-turn paths on the grid 1/2048; written proof and exact integer program, C++ and NumPy versions agree ([note](research/14-light-cone-lattice/ATOMIC_TWO_TURN_UPPER.md)) | independent review, Lean |
| One-turn class | **W_1 ≤ 25661865897887875/18014398509481984 = 1.4245197187…** | same proof; C++ program on the grid 1/4096 | as above |

The frozen table above is unchanged because these bounds have less checking. With them the width is 0.0014454.

What was learned about the strategies (numerical unless stated):

- **Monster.** 62 % sweeps, 20 % endpoint-first paths S(±a), 16 % one-turn paths P_1(±a), 0.7 % one-turn paths at levels just off t + x = 1, 0.5 % two-turn paths T_2 that join the sweep from −1. The two-turn paths are worth about 3.9e-4; turn levels just off 1 are needed. On the lattice the unrestricted Monster also loiters near the centre (0.2 %), which these families do not contain.
- **Princess.** An ordered law: inner ranks wait at the centre until time 1, middle ranks pass just outside it at about t = 0.9, outer ranks turn back early; most first run outward by up to 0.04. On the lattice a three-parameter family of such paths is within 4e-5 of her optimum.
- **Indifference.** Against the Monster law the Princess's best payoff is within 1e-4 of its maximum from 99.3 % of starts; against the Princess field 96 % of the Monster law's probability is on paths within 2e-4 of the cheapest one, and 99 % within 1e-3. One-turn play is within about 2e-4 of unrestricted play on lattices up to n = 32, with no sign of W_1 = V.
- **Value.** Best laws on successive grids extrapolate to about 1.42397 from both sides. This is an estimate, not a bound; the lower bound is now the larger part of the gap.
- **Proved along the way:** U_n = L_n + 1/(4n) between the repository's clock-grid optimum and the half-offset lattice value.

## One-turn comparison: closed

The [countercertificate](research/13-equilibrium-geometry/ONE_TURN_SEPARATION_COUNTERCERTIFICATE.md) proves V ≤ W_1 ≤ C < 57/40 < U_*. Here C=142472349375511/100000000000003, and U_*=291849329389899/204800000000000 is the frozen historical comparison upper. The law combines endpoint sweeps with continuous S(a) and P_b(a) start densities at b=15/16,31/32,1,65/64,33/32,17/16. Its complete all-Princess proof includes initially crossed turn levels, late endpoint captures, arbitrary Princess turns and initial ties. The frozen integer/P2 potential replay needs only Python’s standard library, takes about ten seconds, and has zero exact residual repair.

This proves alternative (M) and makes the former search for W_1>U_* impossible. Do not restart that comparison search. It does not identify exact W_1 or V, show W_1=V, or classify optimal support. The earlier complete-domain, finite-Princess response and minimax/hierarchy proofs remain valid. The previous 752-pair upper remains a historical benchmark with unchanged provenance. No new CI or Lean result is claimed.

## Structural inventory

**Globally justified:** ordered-quantile transport; symmetry/minimax; global Princess incoming-front completion at t+|x|=C (C=2U−1 or C=2); law-independent Monster decision-front normalization and an optimal Monster completed by 2V+2; finite-initial-support nonattainment; actual-record variational derivative and saddle inequalities; causal physical matching/clock dual; center heavier-first rank balance and the available all-count renewal lower-certificate conditions. Read [the core index](research/12-global-closure/README.md).

**Conditional but useful:** bulk P/S moment/contact equations; initial-inward I, moving-front P and endpoint-return J obstacles; shadowing and endpoint boundary contacts; curved-phase three-run first-exit response under curvature signs; superadditive central return compression under an extra field inequality; finite postcenter excursions under joint continuity and a positive record gap; conditional square-root endpoint tail; conditional non-Puiseux near-endpoint model. These do **not** classify the unrestricted equilibrium.

**Disproved shortcuts:** attained finite Princess start support; reweighting the original finite seed into an exact equilibrium; a universal quarter-mesh interpolation gain; unlifted Eulerian flow (spurious value 1); deducing a uniform center-turn cutoff from front completion or near-optimality; loop-only boundary tests without shadow/inward routes. See the [contact atlas](research/13-equilibrium-geometry/CONTACT_ATLAS.md).

## Latest exact reductions

- [Synchronized pressure and finite support](research/12-global-closure/SYNCHRONIZED_PRESSURE_AND_FINITE_SUPPORT.md): causal retiming replaces cone matches by equal-time matches and positive-time exact antipodal cancellation. A fully matched law with N oriented support paths has a finite atomic-clock and polygonal realization with at most N+2 knots per path. No finite optimal N is established; arbitrary finite optimal support is not silently identified with finite support in the fully matched class.
- [Front-one projection failure](research/12-global-closure/FRONT_ONE_PROJECTION_SECURITY_LOSS.md): exact all-path securities 47/40 and 469/400, proved by a complete finite-target capture-order reduction and 720 rational orders per law. Bounded-density regularizations retain a strict loss for sufficiently small, existential smoothing widths. The example is below the game lower and does not decide value-level front-one sufficiency.
- [Compensated curvature](research/12-global-closure/COMPENSATED_CURVATURE_AND_CUSP_RESPONSE.md): a weaker invariant exchange gives a finite global response for the specific atom-free power cusp. Its whole-inner version still forces inward motion and gives a sweep upper 91/64 at U=21/16, below the game lower.

## The missing theorem

We do not know how to assemble the initial field, moving contacts, endpoint atoms and two surviving records into **one legal, globally sufficient phase decomposition**. The [whole-positive-region exchange](research/12-global-closure/POSITIVE_PREFRONT_RESPONSE_AND_MODULUS.md) now gives at most three runs before first center/front/endpoint exit when its curvature holds throughout that region. Any valid outer lower bound may be attached at first exit, since the exchanges themselves use an actual concave physical suffix. But the same note excludes extending the inner monotonicity unchanged through U=41/40: the endpoint sweep then costs less than 1137/800, below the certified lower. Competitive geometry needs a different inner phase before that level, or a separately justified front-one model. W=0 is still not a center state.

The modulus strengthening makes every nonfully-uncaught center state admit a finite optimal continuation for each fixed continuous field. Center slack and endpoint mixing give a value-dense class with finite postcenter complexity member by member; no uniform count or precenter phase sufficiency follows. The [static free-start Zeno counterexample](research/12-global-closure/GLOBAL_FREE_START_ZENO_COUNTEREXAMPLE.md) additionally rules out a universal finite-turn response theorem for arbitrary legal fields. Its center atom and low security are explicit limitations; it does not decide the equilibrium's response topology.

Section 6 of the same note proves that the atom-free front-one cusp has free-start value strictly below its centered optimum. The compensated exchange above now closes that particular response problem: a global optimizer can be chosen with finitely many turns. This is a fixed-law result, not an equilibrium-sufficient Princess class.

A candidate CDF must satisfy transport, endpoint jumps, symmetry, and genuine chronological first captures. Its companion Monster law must be a distribution on legal **physical** paths, not a clock-only optimizer. Equilibrium requires the two universal inequalities in [PROOF_GATES.md](research/13-equilibrium-geometry/PROOF_GATES.md); fitting finitely many contact families establishes neither.

## What numerical discovery actually ruled out

Compatible refinements of the current frozen full-width front-two field cannot yield a standard transferred lower larger than **1.42290944208984375**; with the historical U_* this left width >0.00213. With the new upper C, the remaining difference from that ceiling is 0.001814051665223508… . This is **not** an upper bound on V or on other Princess laws. The retained earlier reference Monster clocks have an endpoint-loop supremum within ~1.12e-11 of the fixed-law upper, so changing clock assignments alone is unpromising. Record-CDF campaigns (29 proposed profiles) and joint-physical campaigns (111 proposals, 22 exact upper checks, 19 full native pricing calls) yielded no new unrestricted bound. These failures justify stopping the old optimization loop, not inferring an impossibility theorem.

The critical negative-start later-turn witness uses start **a=-7/8** and turn **b=67/64>1**. A geometry model restricted to positive starts or early turns will miss it.

## First research deliverable

Construct a **contact atlas that is sufficient or has a concrete adversarial counterexample**, starting with the joint precenter initial-inward / moving-front / endpoint-return / shadow constraints. Track the outer continuation as a function of **both surviving records**, and preserve all endpoint/center exit faces. Identify a global transport-compatible candidate or prove a specific contact ansatz impossible.

Update [WORKING_NOTE.md](research/13-equilibrium-geometry/WORKING_NOTE.md) with the theorem/counterexample and exact test. Then either:
- prove a full-phase cover and all-path Bellman/renewal certificate, followed by the physical dual; or
- give a rigorous impossibility/obstruction for the proposed geometry and revise it.

Do not start another high-resolution numerical campaign without a new structural hypothesis and a falsifiable test. The old programs, certificates and commands remain intact: [package map](packages/README.md), [REPRODUCE.md](REPRODUCE.md).

## Provenance

The previous full handoff, roadmap, status and PR narrative are frozen as files under [archive/handoffs](archive/handoffs/). The historical [pre-squash branch](https://github.com/vltanh/lean4-monster-princess/tree/archive/pr1-pre-squash-2026-11-13) retains the original commit timeline. Existing exact artifact hashes and paths have not been altered by this editorial reorganization.
