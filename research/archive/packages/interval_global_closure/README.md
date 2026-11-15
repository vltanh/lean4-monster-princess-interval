# Global strategy optimization and exact rejection tests

This package targets complete strategy pairs. It has not solved the
unrestricted interval game. A subsequent constructive checkpoint supplies
a new exact upper law and its actual best-response approximation; the
matching princess minimax strategy remains missing.

## Exact horizon and physical-clock lifting regressions

```sh
python packages/interval_global_closure/verify_exact_horizon_reduction.py
python packages/interval_global_closure/verify_finite_state_clock_lift.py
```

The [horizon theorem](../../research/12-global-closure/GLOBAL_EXACT_HORIZON_REDUCTION.md)
reduces the unrestricted game exactly to Princess outward motion after
time 3 and a globally optimal Monster law completed by 7. The first
script independently checks its physical contact and endpoint-tour
comparisons. The [lifting theorem](../../research/12-global-closure/FINITE_STATE_PHYSICAL_CLOCK_LIFT.md)
gives a sufficient seven-coordinate, seven-control flow model with graph
horizon 24. The second script checks both clocks, all state/control
identities, visit registrations, causal reconstruction, and exact strict
pressure projection. Both passed natively with rational arithmetic.
The continuum proofs remain analytic. These are not a finite optimal
support theorem or a matching equilibrium certificate.

## Constructed upper law and best response

Read [the exact upper checkpoint](../../research/12-global-closure/EXACT_UPPER_CHECKPOINT.md).
The complete rational law and flow are in `upper_dyadic_exact.json`.
Its unrestricted response supremum is
`957063215727541539/671088640000000000`. The separate physical princess witness
in `upper_dyadic_princess_response.json` is within `1.91e-8` of this value.

```sh
node --stack-size=16384 packages/interval_global_closure/certify_upper_candidate.cjs --verify packages/interval_global_closure/upper_dyadic_exact.json
python packages/interval_global_closure/verify_upper_candidate.py packages/interval_global_closure/upper_dyadic_exact.json /tmp/upper_dyadic_princess_response.json
```

The first command replays exact integer capacities, conservation, and cut
equality. The second independently checks both rational response profiles
and all oriented physical captures. These checks were executed.

## Explicit pair and both response incentives

[The strategy-pair checkpoint](../../research/12-global-closure/EXPLICIT_STRATEGY_PAIR.md)
combines the upper law with the archived 338-path Princess law. Their exact
cross payoff is approximately `1.4231991766241816`. The Monster can gain
at most `0.00560934170633` by deviating; the Princess at most
`0.00293614840165`. The Monster bound is attained by the archived optimal
route, and the supplied Princess response is within `1.91e-8` of her
supremal improvement.

```sh
node packages/interval_global_closure/paired_strategy_regret.cjs /tmp/paired_strategy_regret.json
```

The exported calculation was executed in V8 and agrees across two exact
first-hit implementations on 94,640 representative encounters. The CLI
filesystem wrapper was not invoked after the executor outage.
This constructs an approximate saddle pair, not a matching equilibrium.

## Whole-strategy exchange

[The efficient upper master](efficient_method.md) keeps an entire physical
Monster bank and checks each proposed law against the unrestricted Princess
oracle. It uses whole-mixture quantile completion and persistent LP bases.
The frozen `efficient_checkpoint.json` and matching
`efficient_checkpoint_bank.json` give a self-contained 1,086-column restart.
`efficient_dyadic_law.py` preserves shared light-coordinate relations when
constructing a dyadic version; its response must still be recertified.

[The CDF exchange](../../research/12-global-closure/CONTINUUM_EXCHANGE.md)
optimizes every legal field value, with no optional shape restrictions.
[The physical response search](../../research/12-global-closure/CONTINUOUS_RESPONSE.md)
has no turn-count bound, exactly rescores decoded attacks against the full
CDF, and adaptively adds record levels to resolve interpolation error.
The remaining spatial graph restriction is explicit. The saved attacks
are not global lower certificates.

[Center-wait unitization](../../research/12-global-closure/CENTER_WAIT_UNITIZATION.md)
is a general upper-law reduction, with exact physical fixtures and a
retained counterexample to pointwise lower-law domination.

[The light-cell Bellman relaxation](../../research/12-global-closure/LIGHT_CELL_BELLMAN.md)
covers every Monster path, using downward-rounded integer arithmetic.
Its current instance is too weak to improve the established lower bound.
It is kept separate from the more effective, spatially restricted attack
finder rather than interpreting a discovery minimum as a certificate.

## Faster exact finite-law Monster responses

`continuous_response_fast_search.cpp` replaces per-target lower-bound scans
with interval-tree sums of exact inverse-hit functions. A disjoint paired-block
relaxation strengthens pruning without restricting the Monster. Its tested
source was recovered exactly after the execution interruption; the source
hash matches the executed independent verification report.

```sh
python packages/interval_global_closure/verify_continuous_fast_search.py
```

See [the mathematical bound and execution scope](../../research/12-global-closure/FAST_CAPTURE_ORDER.md).
The larger 512-path run was interrupted and supplies no new lower certificate.

## Earlier exact construction tests

Read the [checkpoint](../../research/12-global-closure/README.md), the
[finite-bank minimax theorem](SURVIVAL_MINIMAX.md), the
[uniform germ-response theorem](../../research/12-global-closure/GERM_RESPONSE.md),
and the [diffuse corridor exclusion](../../research/12-global-closure/UNIFORM_CORRIDOR_EXCLUSION.md).

Run from the repository root. NumPy and SciPy are used for discovery and
basis selection; SymPy supplies exact rational linear algebra and rational
function arithmetic. The corridor and generic-route checks use Python's
standard library, together with existing repository code. No Lean or CI
invocation is required.

```sh
python packages/interval_global_closure/reconstruct_minimax.py packages/interval_global_closure/global_minimax_grid4.json packages/interval_global_closure/global_minimax_grid4_exact.json
python packages/interval_global_closure/germ_response.py packages/interval_global_closure/global_minimax_grid4_exact.json
python packages/interval_global_closure/verify_germ_response.py
python packages/interval_global_closure/verify_generic_paths.py
python packages/interval_global_closure/verify_corridor_law.py
```

The reconstruction accepts an optimization basis only after exact
normalization, positivity, all-bank payoff inequalities, and independent
global-cut equality pass. The germ search fails explicitly on its node
limit; an interrupted run is not a certificate.

Optional discovery and the larger specified attack:

```sh
python packages/interval_global_closure/survival_minimax.py --grid 4
python packages/interval_global_closure/survival_minimax.py --grid 4 --archived-upper --output global_minimax_enriched.json
python packages/interval_global_closure/germ_response.py packages/interval_global_closure/global_minimax_enriched.json --rightmost-left-attack --output packages/interval_global_closure/global_minimax_enriched_germ_attack.json
```

The coarse bank is a particular documented set of 472 pairs; it is not all
possible grid routes. The named field-support run uses a fixed additional
set from an earlier whole-field computation. It must be reported according
to its saved completion status, never inferred complete from model setup.

The numerical JSON files retain the bank, weights, query geometry, and
nested response mixture. Large regenerable order vectors and residual
graphs are omitted by default; use `--full-output` when those are needed.
The exact JSON files state the scope of every certificate or attack.
