# An exact obstruction to reweighting the 806-route bank

This result concerns a specified finite Monster bank. It is not a Princess lower certificate against the complete one-turn class. The later [continuum countercertificate](../../research/13-equilibrium-geometry/ONE_TURN_SEPARATION_COUNTERCERTIFICATE.md) uses new continuous starting positions and closes the full comparison negatively.

The bank contains 806 fair reflected pairs of canonical physical one-turn routes. It consists of the retained 598 geometries and every canonical pair with both light parameters `a,b` on the `1/8` lattice in

\[
 -1\le a\le1,\qquad a\le b\le2-a.
\]

Endpoint starts use the immediate opposite sweep, zero-length legs are removed, and the route is recorded through its first completed visit to both endpoints. Reflection duplicates are merged. The complete lattice contributes 241 distinct pairs, including all 21 pairs whose first center visit is later than time two. The global finite-event inverse-curve oracle, which imposes no center deadline, is used throughout this note.

## Exact statement

For every probability vector on these 806 reflected pairs, the supremum of the expected capture time over all physical Princess paths is at least

\[
 L_{806}=\frac{1167495935793}{819200000000}
       =1.4251659372473144\ldots.
\]

In particular,

\[
 L_{806}-U_*
 =\frac{24654558351}{204800000000000}>0,
 \qquad
 U_*=\frac{291849329389899}{204800000000000}.
\]

Consequently no reweighting of this bank can supply an all-Princess Monster upper at or below the frozen target. New physical geometries or a different law class are necessary for that route to comparison closure.

The statement also excludes arbitrary unequal weights on the individually oriented routes represented by the bank: symmetrizing such a Monster law cannot increase its worst Princess payoff, and produces a probability law on the listed fair pairs. The certificate itself stores and evaluates the fair pairs.

## Files and reproduction

The compact witness `opposing_complete8_witness.json.gz` is approximately 115 kB. It contains the rational physical routes and integer threshold marginals of denominator `100000000`; it contains no LP matrix, optimizer state, reward-unit table, or floating solution.

When the files are placed in `packages/interval_one_turn`, run from the repository root:

```sh
node packages/interval_one_turn/opposing_verify_finite_bank.cjs
```

The verifier also accepts explicit witness and engine-directory arguments:

```sh
node opposing_verify_finite_bank.cjs WITNESS.json.gz ENGINE_DIRECTORY
```

`ENGINE_DIRECTORY` contains the existing audited `atomic_survival_v8.cjs` and `projected_cut.cjs` modules. The physical interpretation uses their established finite-event inverse-curve response theorem. This is an exact computational replay and a mathematical certificate argument, not a Lean kernel proof.

The verifier:

1. Checks every rational route for time-zero start, arena containment, unit speed, at most one interior reversal before the first endpoint, no subsequent interior reversal, and completion at both endpoints. It checks reflected-pair uniqueness and reconstructs the entire `1/8` lattice to confirm coverage.
2. Rebuilds all inverse-query coordinates, level coordinates, forced bounds, reward clauses, and projected order edges directly from those routes.
3. Verifies every threshold numerator lies between zero and its denominator and every order implication holds with integer arithmetic.
4. Independently completes the marginal field on all original inverse thresholds, checking monotonicity both across query rows and within each row, as well as exact agreement at all priced thresholds.
5. Recompiles every physical row using the rational engine's exact coefficients. With geometry scale `65536`, every reward coefficient becomes an integer. It evaluates conjunctions as integer minima and negative conjunctions as the denominator minus an integer maximum. It checks the minimum payoff and its strict comparison with the target by integer arithmetic.

The successful replay rebuilt 2,352 unit-speed legs, 108,732 projected thresholds from 539,166 original thresholds, 216,015 order edges, 411,434 reward clauses, and 702,816 exact row coefficients. The maximum route completion time is `23/4`. No supplied reward units or saved solver residuals are trusted.

## Why a fractional threshold field proves the statement

Write the certified threshold marginals as `x_j=n_j/D`. A common uniform rank `z` on `[0,1]` gives Boolean thresholds

\[
 Z_j(z)=\mathbf1_{z\le x_j}.
\]

Every order implication `x_u<=x_v` therefore holds for the Boolean thresholds as well. The verified full inverse-CDF completion extends each rank to a legal ordered inverse-label profile.

For a positive reward conjunction, its expectation is the minimum of its marginals. For a conjunction of negative literals, its expectation is one minus their maximum. Thus the integer row calculation is exactly the common-rank expectation of the finite-event capture scores. It gives a value at least `L_806` against each bank pair individually.

There are finitely many distinct marginal values. Partitioning `[0,1]` at those values produces a finite rational decomposition into 20,662 rank intervals; a constant label profile is used on each interval. Zero-weight intervals are absent. The code does not have to enumerate these profiles to evaluate their expected row scores.

For any fixed probability vector `w` on the bank,

\[
 \int\sum_iw_i R_i(Z(z))\,dz
   =\sum_iw_i R_i(x)\ge L_{806}.
\]

At least one legal label profile therefore has weighted score at least `L_806`. The exact finite-event response theorem identifies the physical response supremum with the maximum legal closure score, proving the claimed exclusion for every `w`.

## A common approaching physical Princess law

The same finite decomposition also yields a common approaching Princess mixture for this bank, rather than a separate limiting argument for every weight vector.

Use the late/minimal inverse fill for each label profile. Displace nonzero side labels by `epsilon`, place the inverse connectors on the subordinate `epsilon^2` scale, and, if necessary, use the radial shrink on the subordinate `epsilon^6` scale. The finite-event realization argument gives, for each fixed profile and each fixed bank route,

\[
 \liminf_{\epsilon\downarrow0}
 T(m,p_{\epsilon})\ge R(m,Z).
\]

The direction is a lower limit, not exact equality at a chosen positive epsilon. Every encoded strict survival-side comparison remains strict for sufficiently small epsilon because the bank's geometric events are fixed and finite. Perturbed level intervals lose only vanishing length, and the late connectors and subordinate shrink cannot reverse a separated comparison. Equal-side contacts can move or be delayed; they cannot produce a new earlier contact separated from the encoded one by a fixed positive time gap. This is the fixed-event realization argument used by the inverse-curve oracle, not a generic assertion of continuity of capture times.

Reflect each realized radial path fairly and retain the rational rank-interval weights. There are only finitely many components and 806 bank pairs. A single sufficiently small epsilon therefore makes every pair's expected payoff at least `L_806-eta`, for any prescribed positive `eta`. The choice of epsilon is independent of the Monster probabilities. Taking

\[
 \eta=\tfrac12(L_{806}-U_*)
\]

already gives a single actual Princess mixture that exceeds `U_*` against every reweighting of this finite bank.

This finite common choice does not extend to newly chosen Monster starts or turn coordinates. In particular, a Monster outside the bank may depend on epsilon and intercept an approaching initial atom. No uniform lower bound against all continuous one-turn routes follows from this witness.
