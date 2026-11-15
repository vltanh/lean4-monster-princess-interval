# Effective fan responses and a global selector-plane oracle

Date: 2026-11-12 UTC.

The unrestricted interval game remains open. This checkpoint closes two response-analysis gates: a computable all-path Monster response class for each fixed ordinary finite fan, and the global Princess supremum of every fixed causal-selector linear CDF functional. It also proves the first stationary-contact reduction used in the former. These results supply tools for constructing a saddle strategy; they do not identify one. The established game-value bounds are unchanged.

## 1. A computable response class for each fixed fan

Let a common-quantile Princess law have an interior continuous piecewise affine CDF with finitely many stationary and unit characteristic edges, bounded density, and a final static piecewise constant density with finitely many atoms. Fixed positive-width unit/wait translation fans, including endpoint clipping and reflection, satisfy these hypotheses. Interior atoms and zero-width limits are outside the theorem.

The exact static-tail reduction gives a uniform completion horizon H for this law. Form the full time arrangement, including moving/stationary edge intersections. Let S be its number of time slabs, E the number of characteristic edge segments, Delta the smallest positive separation between stationary positions and physical endpoints, and M an interior density bound. The local interface formulas define positive constants Gamma and kappa_min over the nondegenerate interface types. Put

```text
K = ceil((4 M Gamma / kappa_min) max(H / Delta, 1)),
N = (S + 2 E + 1) (40 + 3 K) + 3 floor(H / Delta) + 2.
```

If there are no nondegenerate interfaces, take K=0.

An optimal unrestricted Monster response exists with at most N unit or waiting pieces. The arrangement is finite, and all constants are exactly computable from rational or algebraic fan data. This yields a terminating semialgebraic response procedure in principle. The bound can be very large; the helper computes it from a supplied complete arrangement census and does not construct that census itself.

The proof has four essential steps:

- Every legal bridge preserves characteristic half-plane constraints through its endpoints. Each characteristic contact set is connected, so the initial coarse decomposition needs at most S+2E+1 intervals.
- In an affine cell, the capture moment has a strictly negative definite Hessian in intermediate record levels. Freezing the FIRST stationary contact, both prefix records, and the later continuation leaves at most one clock constraint. This gives at most three productive legs and seven unit pieces before that contact.
- A nondegenerate stationary source has a local replacement with at most seventeen unit pieces and an immediate captured-width gain w >= kappa d. The source window is chosen so that its duration shrinks proportionally to the remaining coarse time. The ratio cancels in the subsequent record-switch estimate.
- Degenerate interfaces allow only one growing record direction until the next distinct stationary position. Transfers between distinct positions consume at least Delta units of disjoint chronological time. After the first nondegenerate source, a global record-width argument handles the whole remaining coarse interval.

The [full theorem](EFFECTIVE_FAN_RESPONSE_BOUND.md) includes the source-window proof, endpoint atoms, flat and one-front cases, and the precise count. The [first stationary-contact proof](AFFINE_FIRST_STATIONARY_CONTACT.md) supplies the variational step.

This closes the fixed-fan charging gap left in FAN_INTERFACE_EPOCH_BOUND.md. It does not prove a uniformly sufficient family of equilibrium Princess laws, and N need not remain bounded when widths shrink.

## 2. A global Princess oracle for causal-selector planes

On a completed unit Monster route, choose causal past lower/upper CDF records and a cut time on each leg. Running minima and maxima give an affine upper bound on ordered capture cost. Negative coefficients use closed CDF values; positive coefficients use strict values.

The new oracle maximizes any finite positive mixture of these linear functionals over every legal Princess marginal. Linearity and fair reflection reduce this to one deterministic radial path. Its light-coordinate graph U=P(V) is nondecreasing in the physical cone. After inserting every point/ray threshold and closing under the physical boundary translations, one query variable and one fill variable per open cell suffice.

Within a threshold chamber, the objective is linear on an ordered polytope. Moving entire tied blocks to threshold faces gives a finite signed-label problem. A closure solver computes its exact supremum, while an independent prefix-max dynamic program checks the same value.

The result is a supremum. Exact contacts have adverse signs and may lose payoff. The realizer replaces side labels by actual rational offsets and connects query and fill values inside the physical cone. Its explicit horizontal-shift and short-bridge error is checked against direct physical CDF integration. Cancelled terms retain their contact geometry.

See [the global oracle theorem](GLOBAL_SELECTOR_PLANE_ORACLE.md) and [the independent physical audit](SELECTOR_REALIZATION_AUDIT.md). A plane is tight only when its selectors agree with the actual record history. Optimizing an arbitrary fixed plane does not alone optimize the original Monster mixture.

## 3. Exact selector minimax for a fixed Monster bank

For any finite bank of completed unit routes, minimizing over causal past-vertex
selectors and their continuous leg cuts recovers each route's exact ordered
capture cost, including atoms. The resulting linear selector game has exactly
the same value as the original game restricted only on the Monster side.

The compact object in the proof is the uniform closure of convex combinations
of selector payoff profiles. Those profiles are uniformly Lipschitz in the
leg cuts even though contact payoffs need not be upper semicontinuous in the
Princess path. This distinction permits a valid minimax argument without
claiming an attained physical Princess optimizer.

The theorem supplies a two-oracle construction: solve an actual physical
path/selector matrix, add tight record selectors for the current ordered law,
and add a new path from the global plane oracle with its proved realization
error. For every positive fixed-bank tolerance, separated-profile packing
proves finite termination. Exact zero-tolerance termination and full-game
sufficiency of the bank are not inferred.

See [the selector synthesis theorem](SELECTOR_MINIMAX_SYNTHESIS.md). The root's
initial floating prototype confirms tight selector equality on the supplied
routes, but its first candidate has a cheap legal Monster attack and is
retained only as discovery work.

## 4. A full supplied-law replay

For the earlier 26-pair basis attacker, the compiled problem has 275 query rows, 274 fill rows, 664 labels, and 114,942 threshold nodes. Its global selector supremum is

```text
7483120787388344786724063 / 4835703274095654559809536.
```

The distinct actual capture-response supremum of that Monster law is

```text
7483097521803449565333963 / 4835703274095654559809536.
```

Both actual rational extremal realizations approach the selector optimum within the proved error. Their independently computed chronological capture payoffs also approach the second quantity. The minimum realization has 51 radial vertices. Its zero-scale inspection polygon has a substantially smaller literal capture payoff, so the exact path is retained without collapsing its small margins.

This is a supplied-law oracle test. Its values do not replace the existing unrestricted game bounds.

## 5. Verification and remaining obligation

The root replay independently rebuilt the full selector problem, checked its exact equality with the independent DP, and rescored 156 chronological captures, 138 retained point queries, and 760 ray subintervals. It also replayed all 47 independent physical packets, eight separate compiler games, the cancelled-contact fixture, and the realization audit.

The effective-bound replay checked 2,176 width inequalities, 680 degenerate cases, 48,000 characteristic inequalities, 1,920 scale identities, 1,920 episode bounds, 2,114 transfer charges, and eight invalid inputs. The arbitrary-path theorem is analytic; these fixtures check its arithmetic ingredients.

All these computational bodies ran in V8. Native CLI commands are supplied for reproduction, but native execution was unavailable in this continuation. No Lean compilation or CI was run.

What remains is a single constant and matching unrestricted strategies, allowing an approaching Princess family if attainment fails. Neither a finite candidate master nor an exact response theorem for a fixed law supplies that missing saddle. The next construction uses the global plane oracle to generate paths and the Monster response analysis to reject or certify the resulting law.
