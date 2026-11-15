# Exact normalized physical-bank pricing

`normalized_record_pricing.cjs` independently verifies rational dual lower bounds on the grid bank after the exact physical normalization: branch until the first endpoint or time 2, then take the prescribed opposite sweep or either direct two-endpoint tour. The equality with the full bank depends on [NORMALIZED_GRID_BANK_PRICING.md](../../research/12-global-closure/NORMALIZED_GRID_BANK_PRICING.md).

The verifier accepts either the existing exact atomic certificates or a rational nodal field produced by the native sparse master:

```sh
node packages/interval_clock_grid/normalized_record_pricing.cjs packages/interval_clock_grid/grid_n6_certificate.json
node packages/interval_clock_grid/normalized_record_pricing.cjs path/to/field.dual.json
node --max-old-space-size=8192 packages/interval_clock_grid/normalized_record_pricing.cjs packages/interval_clock_grid/lower_n256_field.json --target-bound
```

Nodal inputs have `n`, `field_denominator`, and `radial_nodes` containing `[j,k,numerator]` at every positive-radius parity node through time 6. Time and radius are measured in units of 1/(2n). A native `minimum_units`, `objective_denominator`, `normalized_bank_dual_value`, or `global_lower` claim is checked against the independent exact result.

The CLI also accepts the lossless compact representation decoded by `qout_field_codec.cjs`, and gzip files. It records the SHA256 of the exact input file bytes. The decoder does not certify field legality: the same complete nodal checks follow expansion.

## Acceptance and scope

All nodal values and inequalities are checked with BigInt. The verifier checks range and adjacent interval-containment order, constructs the covering discounts, and checks every causal cone inequality through a quadratic-time suffix-minimum computation. It then prices all normalized physical paths using exact record costs.

A verified normalized-bank dual price c gives the unrestricted game-value lower bound `c - 1/(2n)`. Optimality of c is unnecessary. The verifier does not infer a Princess security bound from an arbitrary normalized-bank profile.

If the nodal field also has a nonincreasing endpoint trace and the exact outward-after-two characteristic identities, the verifier reports `qout_verified: true`. In that case the proved fixed-profile normalization extends its dual inequality to the full bank, so the constructive Princess extraction theorem applies. A claimed `normalized_profile: true` is rejected when those exact identities fail. The extension after time 6 is chosen consistently with this stronger scope.

For full primal/dual input certificates, physical paths, causal calendars, and matching capacities are replayed independently through the existing primal verifier. The report states whether the normalized dual equals the exact physical upper objective. A dual larger than that physical upper is rejected.

## Exact state reduction

At a fixed time, position, and center-visit flag, a state is dominated when another state has no larger accumulated cost and no larger running minimum for either clock. Future costs are nondecreasing in those two records. A sorted Fenwick-tree pass performs this Pareto reduction exactly. `--no-pareto` disables it for independent comparison.

Deterministic tails are scanned directly. For each active clock the cached tail is the sum of `min(entry_record, suffix_record)` terms. Binary search and exact partial sums evaluate this concave tail function. The time-2 node is included before its first future interval is charged. Endpoint clocks become inactive on their first arrival; no own-endpoint atom is selected.

The implementation retains no ancestor pointers in ordinary value-only verification. `--witness` additionally returns an attaining physical route and integer clock calendar.

## Exact pursuit bounds and target verification

For an exactly verified Qout field, the verifier additionally uses the independent pursuit relaxation proved in [PURSUIT_PRUNING.md](PURSUIT_PRUNING.md). Each clock separately follows the fastest route to its own endpoint until time 2. Diagonal suffix sums and a binary search compute its exact lower cost. A weighted two-endpoint tour, minimized over the exact center-compatible interval of reachable positions at time 2, bounds the remaining cost. No floating comparisons are used. `--no-pursuit` disables this reduction.

In ordinary mode this bound is compared only with the value of an actually evaluated physical route. The returned value is the exact minimum. In `--target-bound` mode, `minimum_units` is instead a proposed lower bound. A branch is removed only if its proved lower bound is at least that target; any complete path below the target causes rejection. Exhausting the remaining branches therefore proves the target without assuming that it is attainable. The report distinguishes these modes using `verification_mode`, `verified_lower_units`, and `attainment_checked`. Target mode cannot be combined with `--witness`.

The API is `verifyNormalizedDual(input, { targetUnits: BigInt(input.minimum_units) })`. Its `normalized_bank_lower` and `global_lower` are certified inequalities even when `attainment_checked` is false. This is sufficient for both the global value bound and, when `qout_verified` is true, constructive Princess extraction.

## Cross-checks

The normalized verifier reproduced every exact optimum already checked on the full bank:

| Grid | Exact value | Pareto states | States without Pareto pruning |
|---|---:|---:|---:|
| 1 | 47/32 | 19 | 19 |
| 2 | 4893/3376 | 165 | 253 |
| 3 | 3153038167/2187120435 | 555 | 1,379 |
| 4 | 232810938448419/161887841831168 | 1,389 | 3,141 |
| 6 | 290632881989129783194425025/202628114404287702771503547 | 4,771 | 18,315 |

It also matched the independent C++ oracle exactly on repaired rational n=6 and n=32 nodal profiles. Those profiles are feasible duals; their numerical discovery masters are not treated as exact certificates.
