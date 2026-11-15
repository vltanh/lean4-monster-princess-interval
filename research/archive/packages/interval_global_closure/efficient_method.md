# Global response-cut strategy exchange

This implementation optimizes actual probabilities on complete physical
Monster routes. Every supplied Monster column is present in every master.
An unrestricted Princess response oracle checks each proposed probability
law. The master and the oracle have different roles: the master value is a
lower bound for the game restricted to the supplied Monster bank, while the
oracle value of a normalized law is an upper bound for the full game.

No finite-bank lower mixture is called an unrestricted lower strategy.

## Global master and separation

For Monster columns `m_j`, let `A_ij` be the limiting capture payoff of a
legal Princess query profile `p_i`. The master minimizes `c` subject to

```
sum_j w_j = 1,  w_j >= 0,
sum_j A_ij w_j <= c  for every retained Princess row i.
```

The Monster bank remains complete when Princess rows are added or removed.
The negative inequality multipliers are a normalized Princess mixture for
this finite matrix. Its positive support is retained in result files.

The rational-geometry lexicographic survival-cut theorem in
`../interval_turn_density/ATOMIC_SURVIVAL_RESPONSE.md` supplies the separation
oracle. It includes all legal Princess paths, starts, speeds, and turns.
Both extremal maximum-cut profiles, and selected profiles of the residual
optimal face, become new master rows. Rational comparisons determine every
contact predicate; network capacities and the discovery master are floating
point. A small numerical separation gap is consequently discovery evidence,
not an exact certificate by itself.

The implementation retains the best globally checked law even when a new
master proposal is worse. L1 level stabilization chooses a feasible law
near that incumbent. A one-dimensional response-cut LP searches the segment
joining the incumbent and trial laws. Every segment point is still a
normalized physical Monster strategy. These are optimization choices, with
no effect on the strategy classes or the global oracle's scope.

## Common-quantile completion of the entire Princess mixture

Write a legal query profile as ordered threshold bits `b_(i,k)`. Suppose the
current master mixture has marginal bit probabilities `z_(i,k)`. For one
common uniform random number `r`, replace every bit by

```
b_(i,k)(r) = 1[z_(i,k) >= r].
```

The expected order inequalities survive, so every resulting thresholded
profile is legal. A positive survival conjunction has new expectation
`min z_(i,k)`, which is at least its expectation under the original joint
law. A conjunction of complemented bits has new expectation
`1 - max z_(i,k)`, with the same dominance property. Every Monster payoff is
a nonnegative sum of these conjunction expectations. Therefore this single
completion increases the payoff against **all Monster columns at once**.

There are finitely many distinct marginal probabilities. One nested profile
per consecutive probability interval realizes the completed law. Adding
all these profiles and reoptimizing can strictly increase the finite-bank
master even when the completed law itself has the same minimum payoff.
The active Monster constraint can remain unchanged while other constraints
gain slack that the new mixture then uses.

The stored 909-column experiment illustrates this global step. One
completion produced 1,728 profiles and raised the reoptimized matrix value
from approximately `1.42616406872` to `1.42623093111`. The retained 125-profile
basis and its exact query geometry are in `efficient_uncross_summary.json`.
That basis can be evaluated independently against all 909 columns. This is
a restricted-game statement; choosing canonical physical fills for those
profiles does not establish a full-game lower guarantee.

## Computation and independent checks

`efficient_separator.cjs` maintains a persistent Node oracle. It compiles
each unit-leg capture condition into integer query/label comparisons using
exact rational geometry. Only the final payoff arithmetic is numerical.
Initial compiled rows are checked against the independent rational contact
routine, and every lifted sparse-support response is checked against that
routine's weighted payoff. Active-support models are cached across repeated
bundle trials.

`efficient_numeric_model.cjs` can avoid repeated rational reward arithmetic
in discovery models. It first verifies that floating images of the complete
exact event-coordinate universe have strictly the same order. All branch
comparisons then preserve their exact meaning, while reward lengths remain
numerical. Physical bounds and profile lifting still use exact coordinates.
If the ordering check fails, the rational reference model is used. The
`--rational-oracle` flag also selects that reference implementation directly.
The two implementations agreed on both saved actual and trial laws used in
the verification run; final exact certification remains separate.

`efficient_hotstart.py` retains HiGHS simplex bases when response rows are
appended or proximal right-hand sides change. The bundled SciPy HiGHS
binding supplies the solver; `--cold-master` uses ordinary stateless SciPy
LP calls. On the saved 1,018-column initial matrix, the persistent and
stateless solves agree at `1.4257143094377172`. Appending twenty response
rows took about 0.31 seconds, versus about 1.97 seconds for a cold full
solve; a changed proximal level took about 0.06 seconds after a 1.24-second
initial solve. These timings describe this execution environment only.

`efficient_geometry.py` rebuilds the exact saved query geometry for Python
Fraction checks. It is necessary because archived Princess profiles retain
additional event coordinates beyond the current Monster bank. Rebuilding
only the bank's natural event coordinates would misinterpret their labels.

`certify_upper_candidate.cjs` separately aggregates physical reflection
pairs, rounds weights to explicitly normalized integer probabilities,
computes an exact BigInt maximum flow, and replays the resulting flow/cut
certificate. Its rational law is an actual full-game upper strategy even
before a matching lower strategy has been found.

## Whole-route union and reproducible commands

`efficient_union.py` combines complete unit-route banks by exact physical
reflection equivalence. Collinear vertices and tails after both endpoints
have been swept are removed. Archived labels, CDF-derived unit routes, and
decoded physical node-DP attacks can all enter the same union. Source LP
multipliers are discarded when the probabilities are jointly optimized.

Center-wait attacks can enter through `--unitize-center-waits`. Each wait is
replaced by closed unit-speed excursions with the same start and end time.
For folded strictly positive Princess paths, the old center wait cannot
capture; each new orientation therefore captures no later than its old
orientation. Folding and strict-positive approximation extend this to a
global upper-law dominance result. See
`../../research/12-global-closure/CENTER_WAIT_UNITIZATION.md` for the proof
and exact physical fixtures. The representative is transformed once and
then reflected. The union stores the original and replacement separately.
The old attack payoff against a CDF with center atoms is **not** transferred
to its replacement; original waiting routes remain in the lower exchange.

The first expanded union included every old 909 column, every unit route
from the H2 CDF dual, and all eight initial physical DP attacks. It had
1,013 distinct reflection pairs. Incorporating all thirteen attacks in the
updated report gives 1,018 pairs.

The saved union bank contains its routes, normalized seed weights, and
required profile geometry. Earlier discovery-stage files are not needed to
run it. The following command continues the frozen global response-cut
problem:

```sh
python -u packages/interval_global_closure/efficient_master.py \
  --bank-input efficient_checkpoint_bank.json \
  --resume efficient_checkpoint.json \
  --rounds 500 --face-samples 6 --line-search 2 \
  --prox-level 0.5 --uncross-every 8 \
  --pool efficient_resume_pool.npz \
  --output efficient_resumed_result.json
```

Result files retain the actual Monster weights, the complete bank, the
best unrestricted Princess response value, the finite master value, the
positive Princess dual basis, and exact query coordinates. Large response
pools are restart caches, not proof certificates.

## A response to a reconstructed law

The law obtained by independently rationalizing the H2 dual's physical turn
positions and rebuilding unit-speed times has unrestricted Princess response
approximately `1.434887088574663`. This is a **new law**, and the value is not
a global response certificate for the source field dual. Even very small
turn-position changes can break shared contact alignments and change the
global supremum sharply. The source field master of about `1.4235550464`
therefore cannot be compared directly with this reconstructed law's value.
The analogous independently reconstructed H3 law has response about
`1.4350536067`, with exactly the same qualification.

The explicit rational realizations in
`efficient_h2.princess_paths.json` independently attain that numerical
response **against the reconstructed H2 law** under exact
segment-intersection recapture. They use epsilon
`2^-64`, below the smallest distinct event gap.

Both supplied paths reach the positive endpoint at time 2 to numerical
precision, return to position `0.45` at time 3, and reach the endpoint again
at time 4. They provide concrete legal path columns outside a class requiring
permanent endpoint absorption by time 3. This does not reject the original
field dual, prove that those columns improve its maximin, or establish that
every maximizing response has that property. Late capture times alone
would not suffice for that conclusion; the actual path excursion is the
relevant evidence.

The two canonical responses are pure witnesses against one upper law. Their
uniform mixture is not claimed to defend against arbitrary Monsters.
