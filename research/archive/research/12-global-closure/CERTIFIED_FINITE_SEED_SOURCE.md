# A certified finite source for the frozen-path exchange

## Scope

This component imports the existing lower strategy in
`packages/interval_uniform_reduction/princess_strategy.json`. It does not alter
its physical paths, infer a new unrestricted game value, or reinterpret its
microscopic coordinates as limits.

The input has 169 nonnegative paths. Coordinates are integers divided by
256,000,000. Positive integer pair weights sum to 100,000,000; each pair selects
the listed path or its negative reflection with equal probability. All legs
have speed 0 or 1, and every listed path has a constant final tail at +1.

The archived exact unrestricted Monster response is

\[
c=\frac{36290299773897097}{25600000000000000}
 =1.4175898349178553515625.
\]

The existing `exact_response.py` was independently replayed on the unchanged
input: 48,228 states, 7 completed routes, 21,262 exact dominance eliminations,
and 2,904 lower-bound eliminations. Its separate Fraction segment-intersection
check reproduced the supplied attaining route. This is an existing source
certificate, not a certificate for subsequently optimized weights.

## Why the full quantile-family oracle is finite

Let the positive paths be \(p_1\le\cdots\le p_n\) pointwise, with positive
weights \(w_i\). On each interval between consecutive cumulative weights, the
radial quantile path is exactly one listed \(p_i\). At a cumulative boundary,
either one-sided quantile convention again selects a listed path. Thus every
quantile path of this fixed source is already in its 169-row library.

For a fixed finite Monster mixture \(\mu\), the exact source oracle is

\[
\max_i\frac12\sum_j\mu_j
  \bigl(T_{m_j}(p_i)+T_{m_j}(-p_i)\bigr).
\]

There is no quantile discretization here. The maximum is over the complete
quantile family of the supplied source. It remains a restricted Princess
oracle, since other legal paths can do better.

The source weights give an exact convex combination of these rows. Hence a
probability master retaining all 169 rows also retains the known certified
strategy as an available mixture. Against any finite germ Monster law with
constant limiting probabilities, its expected limiting payoff is at least
\(c\), by the original pointwise-in-epsilon certificate and finite bounded
capture times. This implication does not certify a new master dual mixture.

## Immutable interface and checks

`certified_seed_source.cjs` exports `createCertifiedSeedSource(G,F)`. Its
`prepare` method checks positive weights, exact normalization, physical
unit/wait paths, nonnegative positions, endpoint tails, and adjacent pointwise
ordering at the union of every pair's vertices. Since path differences are
affine between those vertices, the last check proves ordering everywhere.
It returns frozen row IDs, physical paths, normalized pair weights, and the
implicit ordered-law interface.

`column(seed,monster)` computes literal pure-pair payoffs using the reviewed
first-inverse scorer. `bestResponse(seed,columns,weights)` returns the exact
maximum over the source family and every maximizing row ID. Coordinates from
the source are constant rational germs; no query profile is re-realized.

The first exported matrix contains all 169 rows against the archived 1,086
Monster atoms and the additional inward M1 at \(15/16-\epsilon\). It passed
724 independent chronological segment comparisons. The source's weighted
payoff is at least its archived certificate in every column. The minimum in
this finite bank is

\[
\frac{36290299931533693}{25600000000000000}
 =1.417589841075535\ldots.
\]

Against the new germ M1, the exact source score is

\[
\frac{7746196340152363}{5120000000000000}
 -\frac{36905259}{50000000}\epsilon,
\]

with limit 1.5129289726860085. This comparison explains why the certified
source is useful after the former 159-row candidate was rejected. It does not
suggest that its present weights match the upper law.

## Replay

From the bundle root:

```sh
node packages/interval_global_closure/prepare_certified_seed.mjs \
  SOURCE/princess_strategy.json \
  inputs/efficient_checkpoint.json \
  certified_seed
```

The output records input SHA-256 and Git blob hashes, exact and floating
matrices, normalized source weights, all immutable row IDs, the full source
oracle response to the archived upper weights, and the common eventual-sign
radius. Floating matrix entries are convenience copies of exact fractions.

The companion lower worker `separate_frozen_law.mjs` accepts any appended
immutable row array and a separate weight vector. It first runs the complete
all-start M1 reduction from `FINITE_INITIAL_M1_SEPARATION.md`, then uses the
unchanged capture-order search if that family does not already supply a
violating attack. Collapsed companions are separate columns, never a
replacement for the actual germ Monster.
