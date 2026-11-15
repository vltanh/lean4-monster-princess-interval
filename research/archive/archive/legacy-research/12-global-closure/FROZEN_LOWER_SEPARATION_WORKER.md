# Reusable separation of frozen Princess rows

## Objects that remain fixed

The worker takes an array `[{id,path,provenance}]`. Each path is a physical
polygonal path over rational germs; its negative reflection has equal
conditional probability. A new query realization must have a new row ID.
The worker never changes a subordinate scale or rebuilds an old path from
labels. It only removes consecutive identical vertices, which does not change
the physical path, and caches exact coordinates, edges, and first inverses.

The separate weight input is interpreted as exact constant rational numbers:
every decimal is converted literally to a rational, zeros are omitted from
the active mixture, and the result is normalized. There is no thresholding.
Pointwise quantile coupling defines the ordered law through the weighted
strict and closed marginals. Pure row payoffs remain the literal paired
payoffs of the input paths; an ordered-law payoff must not be substituted for
their linear matrix average.

## A universal finite M1 bank

Let \(S\) be the union of initial positions of all supplied signed paths,
including rows whose current weight is zero. By
`FINITE_INITIAL_M1_SEPARATION.md`, for every probability vector on these paths
the complete M1 infimum occurs at a start in \(S\cup\{-1,1\}\), in one of
the two endpoint-sweep orientations. The proof uses monotonicity of first
inverses in every support gap and exact time-zero capture at a support atom.
It applies to the raw mixture and to its common-quantile coupling.

Thus the optional `allInitialColumns:true` bank is a complete universal M1
bank for every subsequent choice of weights on the fixed rows. It is not
limited to the eight current worst starts. Reflection identifies two Monster
routes only because every input row is a reflected pair. Distinct germs with
the same limiting initial position remain distinct columns.

The worker also adds each distinct ordinary collapsed companion as a
separate column. Collapsing is not asserted to preserve payoffs against
varying Princess germs. Both routes are physically rescored, and the germ
route is retained.

For the first 332-row library, the union has 378 signed initial germs. The
756 oriented candidates reduce to 378 reflected classes; 40 additional
collapsed routes give 418 exact columns. Every column includes all 332 pure
row payoffs. The then-current ordered mixture is rejected by inward M1 from
\(119/128\), whose limiting cost is

\[
\frac{3529103878977573469185350187}
     {2559999999999999573555200000}
=1.3785562027256149\ldots.
\]

These numbers describe that named input mixture. No lower bound for the
unrestricted game follows from passing a finite Monster bank.

## All-capture-order search

The complete M1 scan runs first. If it already supplies a strict limiting
attack below the requested target, the default worker returns its attacks
without a further unrestricted search.

Otherwise the worker enters the already reviewed `G.CaptureSearch` sorted
core. Its constructor state is initialized from the validated prepared
paths, rather than parsing the same vertices again. The initial incumbent is
the exactly scored best M1 route. No transition, geometric comparison,
arrival comparison, dominance rule, or lower bound in the search core is
changed.

A completed search has the original finite-law all-Monster scope. A stopped
search supplies only an attained physical attack. Its result explicitly
records `complete`, `stopReason`, state counts, and remaining stack size.
An endpoint tour is appended to a returned attack after all active ranks have
already been captured; this leaves its current-law score unchanged and makes
the column capture every zero-weight row too. The result is independently
rescored by the unit-route rank-record engine.

Six independent fixtures compare the prepared constructor with the original
constructor through completed searches. Their optimum germs agree exactly.
Six further comparisons use the reviewed limit-objective wrapper; its
finite uniform lower/upper germ sandwich and limiting optimum agree.
All universal/companion columns in those fixtures are checked by 394 signed
chronological segment intersections. Removing weights does not remove
zero-weight initial positions from the universal bank.

## Replay and integration

```sh
node packages/interval_global_closure/separate_frozen_law.mjs \
  FROZEN_ROWS.json MASTER.json OUTPUT_PREFIX \
  --all-initial-columns --no-search
```

For ordinary subsequent separation, omit the two last flags. Optional
`--target`, `--top`, `--nodes`, and `--milliseconds` control the requested
target, returned leading attacks, and the explicit search budget. A target
from a floating probability master is a diagnostic target, not an exact
value certificate. Optional `--limit-objective` uses the reviewed
`asymptotic_germ_search.cjs` gate: only the objective lower-bound comparison
uses limits; geometry, capture order, arrival times, and Pareto comparisons
remain exact germs. A completed run then certifies the limiting response
with a retained finite germ sandwich. It does not automatically certify the
upper incumbent as the exact full-germ optimum; that status is separately
reported by `exact_germ_optimum`.

`OUTPUT_PREFIX.report.json` gives normalized weights, input SHA-256 hashes,
the complete current-law M1 scan, universal support if requested, candidate
scores, and eventual-sign radius. `OUTPUT_PREFIX.columns.json` gives
`row_ids`, Monster `atom` objects in the exact `PATH` light-coordinate schema,
physical routes, and row-major `exact_limits`, `exact_costs`, and `decimals`.
Germ costs and raw versus ordered means are separately labeled.

For a persistent process, use
`createFrozenSeparator(rows).separate(weights,options)`. It retains inverse
caches. Do not reset its arithmetic radius while keeping those caches:
previously used comparisons remain part of the common certificate. Append
rows under new immutable IDs, and rebuild or explicitly extend the geometry
context. Pin each pair of row/weight inputs before launching a worker to
avoid mixing two iterations of a mutable file.

Verification:

```sh
node packages/interval_global_closure/verify_frozen_separator.mjs \
  inputs/germ_v8_fixture_inputs.json reports/frozen_separator.json
```
