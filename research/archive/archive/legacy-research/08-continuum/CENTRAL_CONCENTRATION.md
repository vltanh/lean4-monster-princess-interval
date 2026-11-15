# A marginal sweep obstruction to centrally concentrated princess laws

## Scope

This is an unrestricted monster response theorem and an exact rejection of one
explicit rational princess law suggested by restricted numerical discovery. It
also rejects the ordered quantile rearrangement of that law. It does not reject
every continuum candidate, determine the game value, or establish a best
response to the rejected law.

In particular, the negative-`c` paths below retain their original outward suffix.
The additional inward detour is applied only when `c >= 0`; applying the proposed
detour formula indiscriminately to negative `c` would be an error.

## 1. An upper bound depending on only two time marginals

Let `P` be any random admissible princess path. Fix `0 < eta < 1` and use the
single monster path with successive vertices

    (0, -1+eta), (1, eta), (2+eta, -1), (4+eta, 1).

Define

    alpha = Pr(P(0) < -1+eta),
    beta  = Pr(P(1) > eta).

Then

    E T <= 1 + (1+eta) alpha + (3+eta) beta.                 (1)

The bound holds for every coupling of the given time marginals, including the
ordered quantile coupling.

### Proof

A princess not captured by time `1` has remained strictly on one side of the
monster throughout `[0,1]`; changing sides would give equality by continuity.
The uncaptured mass on its left is therefore at most `alpha`, by looking at
time zero. The uncaptured mass on its right is at most `beta`, by looking at
time one. Equality at either displayed threshold is already a capture and is
correctly excluded by the strict inequalities.

Every left survivor is captured by the visit to `-1` at time `2+eta`, and every
right survivor by the subsequent visit to `+1` at time `4+eta`. The contribution
through time one is at most `1`. The additional contributions are at most
`(1+eta) alpha` and `(3+eta) beta`, proving (1).

This proof uses only continuity of princess paths; it does not impose a turn
bound, a prescribed initial position, or a restricted monster family. The
monster itself has unit-speed segments and stays inside the arena.

## 2. Consequences for concentration near the center

If all princess paths lie in `[-delta,delta]` at time one, with `delta < eta`,
then `beta=0`, so

    E T <= 1 + (1+eta) Pr(P(0) < -1+eta).                  (2)

Thus a proposed limiting law that concentrates at the center at time one cannot
be justified merely by checking its payoffs against monster paths with an exact
turn on `t+x=1`. A nearby legal monster path can pass above the concentration
before turning.

For a sequence of such laws with `delta -> 0`, suppose the initial marginals
converge weakly to `rho`. Applying (2) first at a fixed continuity point
`-1+eta` of `rho`, and then letting `eta` decrease to zero, gives the necessary
upper obstruction

    limsup (best-response payoff) <= 1 + rho({-1}).         (3)

For symmetric initial marginals with total limiting endpoint mass `A`, the
right side is `1+A/2`. If there is no limiting endpoint atom, it is `1`. This is
an upper obstruction for the specified concentrating sequence, not a statement
that general admissible princess laws have payoff at most one.

### A mixture with endpoint paths

Suppose a symmetric princess law is divided into a central component of mass
`1-R` and another symmetric component of mass `R`. Assume:

* central-component initial positions lie strictly between `-1+eta` and
  `1-eta`;
* central-component positions at time one lie in `[-delta,delta]`, where
  `delta < eta`.

Symmetry gives `alpha <= R/2` and `beta <= R/2`, independently of how the other
component moves. Consequently (1) implies

    E T <= 1 + (2+eta) R.                                 (4)

If the other component is at the endpoints at time one, its positive half
makes `beta=R/2`. These statements also follow solely from the marginals and
are preserved by ordered quantile rearrangement, even if rearrangement changes
which original path supplies a quantile's position.

For a converging family in which the central component acquires total initial
endpoint mass `A_c`, the same limiting argument gives the corresponding
necessary upper obstruction `1+2R+A_c/2`. Any proposed strategy with a larger
guarantee must avoid these concentration and marginal conditions.

## 3. An explicit rational law excluded by (4)

The data file
`packages/interval_central_concentration/candidate.json` specifies 62 reflected
pairs, hence 124 explicit paths. Its integer weights are normalized by their
exact sum `9999999997`; the two paths in each pair receive half the normalized
pair weight. Parameter triples `(a,u,c)` have denominator `10000000`, and

    delta = 1/1000000000,       eta = 1/64.

The numbers originate in floating-point discovery but the law below, the
normalization, and the verification are entirely rational. The floating-point
objective is not used in the proof.

### Exact positive-half path construction

For each listed `(a,u,c)`, start at `a`, move right to

    ((u-a)/2, (u+a)/2),

and then move inward. If `c >= u-2 delta`, reach `delta` at time `u-delta`,
wait there until time `c+delta`, and begin moving outward. Otherwise turn
outward at

    ((u+c)/2, (u-c)/2).

For `c < 0`, continue directly to `+1` at time `c+1` and stay there. For
`c >= 0`, continue only until

    ((1+delta+c)/2, (1+delta-c)/2),

then move inward to `(1,delta)`, and finally outward to `(2-delta,1)` and stay
there. The negative-half path is its spatial reflection. Delete repeated
vertices and redundant collinear vertices.

The verifier checks all time and position bounds, nondecreasing vertex times,
and all segment speeds exactly. In particular, these are actual admissible
paths with a strictly positive central margin, rather than formal limiting
paths that touch zero.

Every `c >= 0` pair starts strictly inside `(-63/64,63/64)` and is at
`+/-delta` at time one. Every `c < 0` pair is at the endpoints at time one.
The total noncentral pair mass is exactly

    R = 1388665985 / 9999999997 < 7/50.

Therefore the unrestricted sweep in Section 1 gives

    E T <= 1 + (129/64) R
        < 1 + (129/64)(7/50)
        = 4103/3200
        = 1.2821875.                                      (5)

The same inequality holds against the ordered quantile rearrangement.
Using the exact initial marginal rather than `alpha <= R/2` sharpens the
certificate to

    alpha = 48509926/9999999997,
    beta  = 1388665985/19999999994,

    E T <= 1554318825101/1279999999616
         = 1.2143115824744497... .                         (6)

Both bounds are strictly below the existing exact lower bound for the full game,

    36290299773897097/25600000000000000
      = 1.4175898349178553515625.

Accordingly this explicit positive-margin law, including its ordered quantile
rearrangement, cannot be an equilibrium princess strategy. The assertion is
not that (6) is its optimal response value; one sufficiently strong response is
all that is needed for exclusion.

## 4. What this changes in the proof search

Equalizing the restricted `M1/M2` payoffs and adding a local detour does not by
itself construct a valid unrestricted lower certificate. A construction in
which most hiders funnel near the center at one common time can be defeated by
a monster whose first turn is shifted beyond that time-characteristic line.
The response is legal and depends only on two marginals, so uncrossing or
quantile rearrangement cannot repair this example.

A future continuum candidate must be tested against (1), as well as against
the unrestricted capture-order or Bellman conditions. The missing matching
lower certificate remains open.
