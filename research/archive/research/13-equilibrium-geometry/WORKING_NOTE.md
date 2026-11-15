# Working note: candidate equilibrium geometry

**This is a hypothesis register, not a proof.** Append new results with exact assumptions, chronological capture interpretation, and counterexamples. Avoid growing another numerical log. Confirmed mathematical statements belong in their own manuscript under the core research directory.

| Candidate statement | Current evidence | Decisive test | Status |
| --- | --- | --- | --- |
| \(W_1>U_*\) for the frozen one-turn separation target | Exact continuum Monster law with all-Princess upper \(C=142472349375511/100000000000003<U_*\) | Full rational potential replay, including every initial-radius phase and zero repair | **DISPROVED; comparison closed negatively** |
| The one-turn restriction is sufficient for the unrestricted value, \(W_1=V\) | The new law proves \(V\le W_1\le C\), without a matching Princess lower. Numerically, on the lattice the one-turn value exceeds the unrestricted value by 1.7e-4, 7.9e-5, 5.2e-5, 2.2e-4 at n = 4, 8, 16, 24 ([light-cone note](../14-light-cone-lattice/LIGHT_CONE_LATTICE_GAME.md)): small, not decreasing | Prove equality or strict separation at the actual values | **OPEN** |
| Initial P/S/I/J/shadow sheets admit one globally transport-compatible contact system | Individual exact family formulas and convex inequalities | Solve jointly with endpoint atoms; test moving-front and negative-start responses | **OPEN** |
| Curved initial patch has a finite LRL response normal form at equilibrium | Conditional curvature-sign theorem and exact local fixtures | Prove curvature signs on every active patch and a globally sufficient phase cover | **OPEN** |
| The same curvature can extend throughout the inner region to front two | Exact sweep bound using only monotonicity of F_U in both coordinates | At U=41/40 the sweep is already below 1137/800 | **DISPROVED**; a different inner phase is needed |
| W=0 initial exits can be priced by the incoming-front terminal | Front terminal only proves its stated boundary continuation | Give separate inner triangle/exit Bellman certificate or explicit counterexample | **OPEN**; no substitution allowed |
| Center return count is uniformly bounded at equilibrium | Continuity-modulus/slack gate gives a finite count for each supplied field | Prove a uniform global gap/modulus or find all-count potential; account for balanced-state Zeno | **OPEN**; no uniform bound from near-optimality |
| Every legal Princess law has a finite-turn free-start Monster minimizer | Explicit static majority-center-atom law with a continuous power cusp | Off-center join and opposite-triangle insertion strictly improve every proposed exception | **DISPROVED**; not an equilibrium-class exclusion |
| The atom-free front-one cusp requires infinite turns globally | Strict centered/free-start gap plus the compensated RLR exchange | Three-run prefront prefix and finite positive-gap continuation | **DISPROVED**; an attained finite-turn global response exists |
| Direct front-one projection preserves every Princess security | Exact six-target capture-order exhaustion; regularization proof | Source47/40 versus projected 469/400 | **DISPROVED**; low-security example leaves value-level sufficiency open |
| Full matching needs genuinely different selected times | Resource-level causal retiming and first antipodal encounters | Retain physical slots and reorient swapped signs | **DISPROVED**; equal-time exact positive-time cancellation suffices |
| Finite optimal fully matched Monster support exists | Each supplied N has a finite polygonal/atomic-clock realization | Prove a finite N or a matching continuum construction | **OPEN** |
| Simple algebraic endpoint trace | Conditional incompatible Puiseux exponent cascade | Verify proposed active-contact hypotheses before applying obstruction | **NOT ASSUMED** |
| Finite start support is exact | Global nonattainment theorem | None — this class is excluded | **DISPROVED** |

## Closed one-turn comparison — 2026-11-14

The [one-turn countercertificate](ONE_TURN_SEPARATION_COUNTERCERTIFICATE.md) closes the frozen target in the negative direction:

\[
 V\le W_1\le
 \frac{142472349375511}{100000000000003}
 <\frac{291849329389899}{204800000000000}=U_*.
\]

The law has a fair endpoint-sweep atom and piecewise constant start densities on endpoint-first `S(a)` routes and canonical one-turn `P_b(a)` routes. Its turn levels are `15/16`, `31/32`, `1`, `65/64`, `33/32`, and `17/16`. Every component is physically in the declared one-turn class. The [continuum certificate theorem](ONE_TURN_CONTINUUM_POTENTIAL_CERTIFICATE.md) covers arbitrary Princess paths, including initial phase crossings for levels below one. The frozen rational nodal witness satisfies all sufficient potential inequalities with zero residual repair; its upper is `1.4247234937550672...`.

This is a comparison counterexample and an improved unrestricted upper, not an identification of either exact value. Both \(W_1\) and \(V\), as well as equality between them, remain unresolved.

The independently rebuilt [806-pair obstruction](../../packages/interval_one_turn/opposing_finite_bank_obstruction.md) also records a useful scope boundary. A rational inverse-CDF witness gives minimum `1167495935793/819200000000>U_*` on that finite bank, so changing only its probability weights could never have met the target. Its finite rank decomposition has approaching physical realizations uniformly on the specified bank. That uniformity does not extend to new continuous Monster starts or turns. The successful continuum law uses geometries beyond the finite bank.

## First concrete task

### Reviewed results from this continuation

The [prefront/modulus manuscript](../12-global-closure/POSITIVE_PREFRONT_RESPONSE_AND_MODULUS.md) resolves a specific G1/G3 proposal. Under the whole-region curvature criterion, the earliest RLR exchange has feasible peak interval `[max(U0,W1),min(U1,W0+2)]` and produces at most three runs before the first center, physical endpoint or front contact. The proof retains both records, actual endpoint resets and arbitrary-path limits. Any certified remaining-cost lower bound may be attached after first exit; the exchange itself uses the actual concave physical suffix.

That class cannot contain competitive front-two geometry. If F_U is nondecreasing in both coordinates on the inner triangle through C, the endpoint sweep satisfies `E<=3/2-sqrt((C-1)*(5-C))/4` for `1<C<=3-sqrt(3)`, and `E<=5/4` above that threshold. At C=41/40 this is strictly below 1137/800. Only inner monotonicity, transport, symmetry and the CDF range are used; front completion and the logarithmic curvature inequality are unnecessary. Thus an additional inner phase is a proved requirement for this construction, not another optional test row.

For the center recurrence, joint continuity gives `omega(h)->0`. A lighter-record gap delta forces each productive balanced return to have height greater than any `h_delta` with `omega(h_delta)<delta`, so at most `floor((C-t)/(2*h_delta))` returns suffice. Endpoint mixing can produce the required slack in a value-dense family, but the count may diverge along that family. This advances G3 without proving an equilibrium phase cover.

The separate [global free-start Zeno proof](../12-global-closure/GLOBAL_FREE_START_ZENO_COUNTEREXAMPLE.md) uses a static law with probability 3/4 at zero and residual radial CDF sqrt(r). Every off-center response is strictly improved by starting at zero and joining it. Every one-sided initial segment is improved by a small opposite triangle followed by the delayed old path. A minimum is attained, so all minimizers have infinitely many initial reversals. The law has security below 1/3 and a center atom; it excludes the universal finite-turn assertion, not the remaining near-optimal continuous case.

Section 6 settles the different atom-free front-one law with radial CDF r^p, 0<p<1. If Q_p is its centered optimum and S_p permits a free start, it proves S_p<Q_p. One early completed excursion is enlarged to a maximal triangle of height a, then the positive-gap theorem supplies a finite productive balanced tail. Starting at its peak at time zero advances every initially outer capture by at least tau, while all inner mass a^p is swept by time 2a. The exact change is at most `2*a^(p+1)-tau*(1-a^p)<=a*(3*a^p-1)<0`. The new competitor is finite. No assertion that S_p has a finite optimal response follows.

Both manuscripts passed two independent full analytic reviews. The [new boundary replay](../../packages/interval_global_closure/verify_positive_prefront_boundary.py) independently integrates actual physical first contacts and chronological records: 135 exact agreements, 1,263 contact branches, 27 early-boundary run checks and six endpoint-atom resets. These fixtures audit the construction; the universal reductions and exclusions are analytic proofs. No matching physical dual or new unrestricted value is claimed.

### Further reviewed structural results

The [synchronized physical-pressure theorem](../12-global-closure/SYNCHRONIZED_PRESSURE_AND_FINITE_SUPPORT.md) first retimes the later side of each cone match, then moves both resource selections to their first antipodal encounter. All changes are earlier and preserve causal physical clocks; sign-swapped pairs are reoriented. Positive-time pairs cancel at one identical time/radius. With finite fully matched support, each path needs only finitely many selected events and a polygonal interpolation preserving the certificate. The remaining finite-support assumption is explicit, rather than hidden in a turn-count ansatz.

The [direct front-one counterexample](../12-global-closure/FRONT_ONE_PROJECTION_SECURITY_LOSS.md) has exact source security 47/40 and projected security 469/400. A finite-target theorem makes 720 rational capture orders per law exhaustive. One late-center endpoint route attains both values, and regular bounded-density approximations preserve strict loss for sufficiently small smoothing widths. This defeats the universal projection route; neither the whole front-one value class nor a high-security projection theorem is excluded.

The [compensated curvature manuscript](../12-global-closure/COMPENSATED_CURVATURE_AND_CUSP_RESPONSE.md) replaces horizontal CDF convexity by B*A_U+A*A_W>=0, with A=F_U and B=-F_W. Its exact cancellation gives a finite global response for the atom-free power cusp. In a whole inner region attached to the center, the same condition forces F_t>=0 and the sweep bound E<=3/2-(C-1)/4. At C=21/16 this is 91/64, below the certified game lower. The broadened phase therefore still needs a different inner attachment.

### Next unresolved construction

Try to combine the exact I/P/J inequalities with the shadow-contact relation for a common F, rather than optimize each branch separately. Write down the candidate active curve(s), the induced boundary traces, free constants and endpoint masses. Then seek **one missing physical path family** that either falsifies the candidate or can be proved dominated. Do not force the equal-cost equations throughout a region unless complementary slackness proves it.

Watch the sign and record conventions: F_x≥|F_t| in smooth interior pieces, actual endpoint capture has a jump, and outer continuation depends on both residual records. The actual negative-start late-turn attack **a=-7/8**, **b=67/64** is a mandatory adversarial fixture.

## Result protocol

For a meaningful result, record: (i) theorem or precise conjecture, (ii) assumed field class, (iii) exact family score and contact chronology, (iv) new obstruction or sufficiency argument, (v) counterexample attempt, (vi) reproducible exact test, and (vii) which gate in [PROOF_GATES.md](PROOF_GATES.md) changes.

**Historical frozen comparison:** `1.4222581340234375 ≤ V ≤ U*=1.4250455536616162109375`. The exact countercertificate now strengthens the upper to \(C=142472349375511/100000000000003\), while preserving the inherited lower. The frozen claim \(W_1>U_*\) is closed negatively; exact one-turn and unrestricted values remain open.
