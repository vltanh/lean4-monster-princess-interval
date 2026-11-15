# Faster exact responses to ordered finite Princess laws

This is an implementation of the existing unrestricted finite capture-order
reduction, with exact GMP rational arithmetic. It is not a turn-limited spatial
grid search. The added lower bound is a relaxation of the entire remaining
capture problem, not an assertion that an optimal route belongs to a new local
family.

## Aggregate earliest-hit functions

For a target path p and pursuit direction d in {-1,1}, put
z(t)=t-d*p(t). Speed at most one makes z nondecreasing. From a state (s,x)
with that uncaptured target strictly ahead, the earliest unit-speed hit is
the first time z reaches q=s-d*x.

The inverse is piecewise affine but can have jumps when the target follows a
unit-speed leg in the pursuit direction. Its intervals must be right-closed:
at a repeated characteristic value, capture occurs at its first attainment.
Replacing that value by the inverse's right limit would be incorrect.

Each target's weighted inverse is stored as affine pieces and exact rational
breakpoints. An interval tree over target ranks stores sums of these
functions. A prefix or suffix sum is obtained from logarithmically many tree
nodes. This replaces the previous scan over every surviving target when
computing the independent earliest-hit lower bound. It changes no payoff.

Adjacent equal affine pieces are merged only when both their slope and
intercept agree. The engine checks every leaf inverse at its exact
breakpoints and interposed midpoints against a separate scalar scan.

## Disjoint paired-block bound

A normalized capture-order state has a captured rank interval [l,r], current
time s and position x. Every remaining left target is strictly left of x,
and every remaining right target is strictly right; simultaneous contacts
have already been collected.

Partition the remaining left ranks into blocks and each right tail into
blocks. Replace each left block by its largest rank, with the block's total
probability weight. Replace each right block by its smallest rank.

For a left block, if a continuous Monster first meets any member, its
position at that time is at most the representative's position. It started
strictly to the representative's right. Continuity therefore forces contact
with the representative no later. The right-block argument is symmetric.
Thus the weighted sum of representative capture times is a lower bound for
the original remaining weighted capture cost.

Pair the blocks disjointly and allow a separate virtual Monster for each
pair, always starting at the same fixed current (s,x). A pair's exact optimum
is the minimum of two orders: earliest left hit followed by earliest right
hit, or earliest right hit followed by earliest left hit. Earlier first
capture cannot hurt: the Monster can follow that target until any proposed
later first contact and then reproduce the continuation. After that first
contact, direct unit pursuit meets the other target no later than any
continuation.

There is no hidden free-start optimization inside this bound. Sunk absolute
capture costs are added unchanged. The sum of the pair minima is a relaxation,
because each pair has been allowed an independent continuation. Taking the
maximum of this and the previous single-target lower bound is safe.

The archived implementation's inverse-hit preconditions also hold at the
second virtual pursuit. Along a unit left ray, an initially-right target's
distance from the Monster is nondecreasing, so it is still strictly ahead
at the first left capture. The symmetric statement holds for right-first
pursuit. This excludes a premature flat-characteristic inverse in that call.

The default is eight paired blocks. Set
`CONTINUOUS_RESPONSE_PAIR_BLOCKS=0` to use only aggregate single-target
bounds. This setting changes pruning, not the exact problem.

## Additional implementation changes

Queued states that have subsequently become strictly dominated at the same
captured interval and anchor are skipped. Dominance still requires both
earlier time and no greater sunk cost. Consecutive collinear route links
are compressed without changing the route or capture times.

An interrupted search retains a certified unfinished-frontier lower bound
and an actual complete-route upper bound when it exits normally at its
node limit. A forcibly lost process does not supply that final bracket.

## Executed checks and exact source recovery

The verified C++ source has SHA256

    a33c316ea27c37310f75da7c777efb7457594a873bfaab0ed7221cd98c28649a

It was recovered from the committed baseline and the recorded edits after
the executor became unavailable. Its recovered bytes were checked against
the SHA256 emitted by the successfully executed verifier. The last untested
defensive edit is deliberately not included.

The executed report, `continuous_response_fast_verification.json`, contains:

- three small independent unrestricted-response comparisons, including
  weighted center coalescence and a later center split;
- fixed-center comparisons with an independent unpruned mask search;
- stopped-frontier inclusion checks;
- independent exact first intersections for all fixture routes;
- the exact archived 32-quantile optimum and all 32 physical captures;
- exact scalar inverse checks, including capture-side equalities.

Before adding the paired-block bound, the aggregate engine also reproduced
the archived 128-target optimum exactly. That run processed 102,318 states
in approximately 9.55 seconds, compared with the earlier engine's 102,672
states in 44.09 seconds. These are measurements from this environment, not
a general performance guarantee. The later paired-block version's
128-target benchmark was interrupted before it started.

Run from the repository root:

```sh
python packages/interval_global_closure/verify_continuous_fast_search.py
```

This compiles and checks the C++ engine using GMP; it does not run Lean or CI.

## The larger search did not finish

A separate 512-path law was extracted exactly from the final H5 CDF candidate,
with 37,574 path vertices, symmetric weights 1/512 and endpoint absorption
by time five. Its capture-order search was still running when the environment
failed. The last reported incumbent was about 1.41756, below the established
game lower bound, so that finite law cannot improve the lower certificate.
Its last live frontier was far below the incumbent; no exact optimum or new
lower bound is claimed.

That uncompleted search used the aggregate engine before the paired-block
bound. Its input and partial artifacts were local after the last durable
checkpoint and cannot presently be retrieved. The source and executed small
verifier above are durable and can be used for a fresh, fully recorded run.
