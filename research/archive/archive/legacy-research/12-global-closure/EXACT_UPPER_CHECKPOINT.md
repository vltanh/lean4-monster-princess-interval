# A constructed monster law and its unrestricted best response

Date: 2026-11-11. This is a supplied-law certificate, not an equilibrium.

The continued whole-strategy optimization produced an actual monster law
with 280 distinct reflected pairs and integer probabilities of denominator
10,000,000,000. Its unrestricted princess-response supremum is exactly

    957063215727541539/671088640000000000
      = 1.426135325025828985869...

Thus this number is a valid upper bound for the full interval game. The
matching lower construction is still missing. G5-G8 remain open.

## The strategy is explicit

The `atoms` array in
[`upper_dyadic_exact.json`](../../packages/interval_global_closure/upper_dyadic_exact.json)
is the complete law. For each entry, select it with probability
`weight_numerator / weight_denominator`, then independently choose its
displayed route or its spatial reflection with probability one half.

The route is supplied in exact light coordinates `(U,V)`. Convert each
vertex to `(time,position)=((U+V)/2,(U-V)/2)` and interpolate linearly.
Every leg has unit speed and every route visits both endpoints. The
certificate checks nonnegative times, the arena constraint, normalization,
and every leg. Identical reflected physical routes were combined before
rounding. The rational law is explicitly a new law selected from numerical
discovery, not an assertion that floating LP multipliers were exact.

The candidate came from joint reweighting of an expanded 1,086-pair
monster bank. The expansion combines the original 909-pair bank, physical
CDF-dual routes, and attacks found by the whole-field response search. A small normalized master and the unrestricted survival-cut separator
replace the large order-polytope LP that previously timed out. A finite
master value is never substituted for the response of its proposed law.

## Preserve the geometry when making the law rational

The discovery checkpoint contains arbitrary rational light coordinates.
A single strictly increasing dyadic map is applied to every coordinate,
commuting with spatial reflection and integer translation. It retains all
shared characteristics, their strict order, initial times, endpoint contacts,
and unit-speed legs. Its maximum physical vertex change is `3/41943040`.
The new law is then globally certified in its own right; no continuity
assumption substitutes for recomputing its response.

This distinction matters: independently rounding physical turning positions
and reconstructing elapsed times changed a trial law's unrestricted response
from about `1.426135` to `1.434503`, although every vertex moved by at most
`1/8388608`. It destroyed common light-coordinate contacts. That trial law
was discarded. `efficient_dyadic_law.py` implements the common-map rule.

The frozen discovery checkpoint and full matching bank are
`efficient_checkpoint.json` and `efficient_checkpoint_bank.json`. The exact
certificate is self-contained and does not need the discovery optimizer.

## Exact unrestricted response check

The previously proved survival-query reduction represents every princess
path by a legal monotone query profile, including strict-contact approach
sides. The positive support alone gives 240 query coordinates and 308
rational base levels. Its integer maximum-flow network has 105,783 nodes
and 268,928 arcs. The saved flow has the same value as its cut:

    maximum flow = cut capacity = 329041605759107475.

After the documented probability and geometric scaling, the residual
reward is the exact response value above. Independent replay checks all
capacity inequalities, flow conservation at every internal vertex, the
source/sink balance, and equality of the feasible flow and cut. These
provide an upper ceiling without assuming a sampled princess list is
exhaustive.

Both extremal monotone response profiles also give exactly this value.
Their rational physical-pair payoffs were recomputed by the separate
Python `SurvivalCut` implementation and agree with the JavaScript rational
model. The response reduction's epsilon realization theorem makes this
ceiling the supremum, rather than merely a potentially loose ceiling.

## An actual princess best-response approximation

[`upper_dyadic_princess_response.json`](../../packages/interval_global_closure/upper_dyadic_princess_response.json)
contains an actual legal rational princess path, constructed with
`epsilon=1/16777216`. The independent piecewise-linear first-intersection
routine checks its capture against all 560 oriented monster routes. Its
exact expected payoff is within

    1.907889187625e-8

of the unrestricted supremum. The JSON stores the exact payoff, exact
gap, every path vertex, and every first capture time. This is a best
response to the supplied monster law; it is not asserted to be a
maximin princess strategy against other monsters.

## Reproduction

No Lean compilation or CI is needed. Run from the repository root:

```sh
node --stack-size=16384 packages/interval_global_closure/certify_upper_candidate.cjs --verify packages/interval_global_closure/upper_dyadic_exact.json
python packages/interval_global_closure/verify_upper_candidate.py packages/interval_global_closure/upper_dyadic_exact.json /tmp/upper_dyadic_princess_response.json
```

The first command only replays the saved certificate; it does not trust an
optimizer's success flag. The second uses Python `Fraction` throughout.
Both were executed. They establish the stated law and its response, not
optimality of the supplied bank or of any full-game strategy.

## Earlier checkpoint retained

The preceding 162-pair law remains in `upper_candidate_exact.json`, with
exact response `4674200578946657/3276800000000000`. It is superseded by
the 280-pair law above. Both certificates and both physical response
witnesses remain replayable; neither is claimed to be a saddle point.
