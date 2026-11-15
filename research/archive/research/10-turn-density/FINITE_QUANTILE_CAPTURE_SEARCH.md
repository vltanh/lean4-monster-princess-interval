# Exact capture-order search for an implicitly sorted finite law

## Scope

This is an unrestricted monster-response algorithm for a **specified finite**
princess law with rational polygonal paths and constant tails. The default
search uses the law's comonotone quantile coupling, which weakly improves its
payoff against every monster. It does not assume a turn bound or an upper
candidate's listed monster support.

It is not an unrestricted game-value certificate. A continuous CDF component
with positive mass is outside the exact finite-law search theorem. Sampling
that component may discover a route, but only a separate full-field evaluation
can certify the route's attack; a completed sampled search is not a lower
certificate for the continuous component.

The canonical capture-order and dominance arguments are reused from
[CAPTURE_ORDER](../07-structural-audit/CAPTURE_ORDER.md) and
[the exact response package](../../packages/interval_exact_response_result/PROOF.md).
The full-law quantile ordering theorem is already proved in
[the uniform reduction](../06-uniform-finite-reduction/PROOF.md), Section 2.

## 1. Why no expanded quantile support is needed

Write the input weights as positive integers w_i, with sum W. Sorting the
original paths pointwise produces an ordered law with the same marginals.
This sorted law still has finite polygonal support: subdivide time at original
vertices and pairwise crossings, then subdivide rank at all cumulative weights
occurring in these finitely many order regions. Between subdivisions every
quantile path follows one original path.

Explicit expansion can be large. Instead retain the captured rank interval
[l,h] in [0,W]. At an event (t,x), its update is

    l_new = min(l, sum_{p_i(t)<x} w_i),
    h_new = max(h, sum_{p_i(t)<=x} w_i).

At time zero the captured interval is initialized directly from those two
CDF traces. At later events, newly captured mass is
(l-l_new)+(h_new-h), and its contribution is that mass times t.

The strict lower and closed upper traces include initial atoms, coincident
paths, characteristic flats, and tangential contacts.

## 2. The next capture and the independent-target bound

On a unit right ray, p_i(s)-m(s) is nonincreasing. Each original path initially
above the ray has at most one first crossing. The closed CDF increases by its
weight at that first crossing. Group equal crossing times before updating the
rank count. The next new sorted capture is the first grouped event at which
the closed CDF exceeds h.

On a unit left ray, p_i(s)-m(s) is nondecreasing. The strict CDF decreases at
first crossings, and the next new capture is the first event below l.

This exactly follows the neighboring uncaptured quantile path, even when its
identity changes among the original paths before capture. No interpolation
of a time or rank is performed. Partial overlap with a weight block is retained.

The same event list gives the earliest independently achievable meeting time
for every remaining rank: integrate each event time over the part of its
rank block outside [l,h]. Adding the left and right integrals to the cost
already incurred is a rigorous continuation lower bound. It does not assume
that all those individual meetings can be realized together.

For arbitrary rational segment slopes, ray intersections use the first
generalized inverse of t-d*p_i(t), with d in {-1,+1}. The independent verifier
instead intersects line segments directly.

## 3. Exhaustiveness and dominance

The existing capture-order theorem applied to the finite expanded quantile
law supplies an optimal response starting at an original initial position,
travelling at unit speed, and turning only at a new capture. The implicit
events above enumerate exactly that tree.

Every event lies on at least one original input path. This original path may
be used as a dominance anchor even when it changes quantile identity. If two
states have the same captured rank interval and anchor, with t_1<=t_2 and
cost_1<=cost_2, the earlier monster can shadow that original admissible path
until the later event. All incidental new captures occur earlier and help.
It then follows the later continuation. Thus the same time/cost Pareto
dominance used in the existing solver remains valid.

Raw-law mode instead keeps a captured bit mask. It uses the same ray
intersection primitive, but does not replace the original path coupling.

A completed search is an exact finite-law minimum. A search stopped at an
attack or node limit reports complete=false. Its stored route is still
admissible and is independently scored, but its cost is not reported as the
minimum.

## 4. Executed exact checks

The V8 core and verifier body were executed during the executor outage.
The Node file-I/O wrappers were not executed.

* All 40 archived raw-law exact values are reproduced.
* On those 40 cases, implicit quantile search agrees with explicit weighted
  quantile expansion followed by raw-law search.
* On 24 additional rational subunit-speed inputs, pruned and unpruned searches
  agree, and implicit/explicit quantile searches agree.
* 1,920 arbitrary-slope ray queries agree with independent segment intersections.
* The 60-path archived certificate is reproduced exactly:
  56305800187/40000000000, with 25,776 visited states.
* The nine-point stationary-shell example returns 381/2633 and its route with
  three interior turns.
* A crossing-path fixture has raw cost 1/2 and sorted cost 9/4 against the
  same fixed monster, checking a strict rearrangement improvement.

Every returned route is independently checked: raw mode by first segment
intersections, sorted mode by the running strict/closed CDF records at all
actual contacts.

## 5. Interim optimal-face dual: an attained attack

The supplied interim lower dual has 37 radial paths, paired with reflections,
with epsilon=2^-40 and strict contraction eta=2^-240. Its exact physical input
is Git blob d40f7ca8d2cc4a32e3111745ea118e0d29975835; its realizer is blob
4bc138092297d46cbebf2d730fe674d37d6b3c17.

The implicit sorted search finds a route of cost approximately
1.2982771065183971 after 43 states. It stops at that strict attack, so this is
not a claim of minimum. The independent record evaluator agrees exactly.
The unsorted physical mixture costs approximately 1.2978297434815238 on the
same route.

An especially simple rational attack starts at 511/512, moves right to first
characteristic U=1-epsilon, then sweeps both endpoints. Its sorted payoff is
approximately 1.3592086268636998, below the interim finite-master objective
1.4176592478028027.

Regenerating the physical laws at epsilon=2^-32, 2^-36, 2^-40, and 2^-44
retains this attack, with costs approaching 1.359208626864. Moving the first
turn by plus or minus epsilon^2 gives different one-sided values. Thus a
shared incoming capture layer, not just an initial atom, is involved.

These computations reject the stated physical lower realization. They do
not reject the upper law's residual optimal face: spreading paths within
unpriced inverse intervals remains a different lower construction.
All exact route coordinates, payoffs, source references, and epsilon checks
are in the accompanying attack JSON.

## Reproduction

    node packages/interval_cdf_discovery/verify_finite_quantile_response.mjs
    node packages/interval_cdf_discovery/finite_quantile_response.mjs INPUT.json --target 1417/1000

The second command discovers an attack if one is found; without --target it
continues toward the finite-law optimum. --raw disables quantile sorting.
A node limit is reported as an incomplete search.
