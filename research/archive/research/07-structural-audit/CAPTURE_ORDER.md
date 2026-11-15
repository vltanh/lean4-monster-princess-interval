# Capture-order audit and an obstruction to a uniform turn or horizon bound

## Status and scope

This note establishes two different results.

1. The finite-support monster-response reduction used in the earlier packages is valid. A precise induction strengthens it to **coordinatewise domination**, independent of the hider probabilities. The argument requires neither constant tails nor piecewise linearity.
2. Symmetry and noncrossing order do **not** imply a fixed bound on the number of monster turns, or a fixed horizon for an optimal response. Explicit stationary, symmetric hider distributions force arbitrarily many interior turns and arbitrarily late last captures. A nine-point rational example already rules out a universal bound of two interior turns.

These results concern responses to specified hider distributions. They do not identify the unrestricted game value and do not rule out a simpler equilibrium-specific strategy family. They do rule out attempting to justify such a family from symmetry and ordering alone.

## 1. A weight-independent finite-response theorem

Let `p_1,...,p_n : [0,infinity) -> [-1,1]` be 1-Lipschitz hider paths. For a monster `m`, write `T_i(m)` for its first encounter with `p_i`, including time zero and allowing infinity.

**Theorem 1.** For every admissible monster `m`, there is an admissible monster `m*` with

    T_i(m*) <= T_i(m)  for every i,

such that `m*` starts at one of the hider starting positions and travels at speed one between successive new capture events. It changes direction only at a new capture event. It captures every hider by time `2(n-1)`.

Consequently, one finite family of canonical monsters contains a best response for **every** nonnegative weighting of the specified hider paths. It has at most `n * 2^(n-1)` terminal direction cases. For hiders with finitely many rational linear pieces on every bounded time interval, all the relevant meeting times and payoffs are rational.

The numerical horizon `2(n-1)` depends on support size. Section 4 proves that its dependence cannot be replaced by any universal constant for all hider distributions.

### 1.1 Earliest pursuit lemma

Suppose the monster is at `(s,x)` and a target satisfies `p(s)>x`. Move along the ray

    q(t) = x + t - s.

Before that ray first meets the target, every admissible monster starting at `(s,x)` lies at or below the ray and hence strictly below the target. No admissible route can meet the target earlier. The first meeting occurs no later than the ray reaches `+1`: at its starting time the target is strictly above the ray, and at that endpoint time it is at or below the ray. Continuity supplies a meeting.

The leftward version is identical. In particular, a direct pursuit takes at most two time units. The argument permits tangencies and intervals of coincidence: the first equality is the event.

If another target starts strictly behind a speed-one ray, its 1-Lipschitz property prevents it from catching that ray from behind. Any new encounter during the leg is therefore with a target ahead, and is a legitimate new-capture event.

### 1.2 The induction that eliminates shadowing

The earlier manuscripts correctly used shadowing as a comparison argument, but did not spell out why the final path contains no shadowing segments. The following invariant supplies that step.

First suppose the original monster has at least one finite capture. Order its finite capture times, breaking ties arbitrarily. Let `i` be the first target in this order. Start the new monster at `p_i(0)`, thereby capturing `i` at time zero and possibly capturing other coincident targets as well.

Maintain the following data:

* the new monster is at `p_i(s)` for a designated, already captured target `i`;
* `s <= T_i(m)`;
* every target preceding `i` in the original ordering has already been captured no later than its original time.

Choose the earliest target `j` in the original order that is still uncaptured. There is an admissible comparison route from the current event to `p_j(T_j(m))`: shadow `p_i` from `s` until `T_i(m)`, then follow the original monster until `T_j(m)`. The earliest pursuit lemma therefore shows that direct speed-one pursuit of `j` reaches it at some `s' <= T_j(m)`.

Use this direct pursuit in the constructed path; **do not use the shadowing comparison route**. Any target captured incidentally during this leg has original capture time at least `T_j(m)`, because `j` was the earliest remaining target. Its new capture time is at most `s'`, so its capture also improves. Designate `j` as the new anchor and repeat.

This proves the invariant by induction. It covers simultaneous original captures: all those times are equal and the same weak inequalities apply. If a target has already been captured incidentally, skip it when choosing the next designated target.

After all targets with finite original capture times have been handled, pursue the remaining targets in any order. Their original times were infinite, so any finite captures dominate them. If the original monster captures no target at all, simply start at any hider and use this last construction immediately.

Every direction change occurs at a designated new capture. Subdivide straight legs at incidental new captures; this makes every positive-duration leg end at a new capture event while adding no turns. At least one target is captured at time zero, so there are at most `n-1` subsequent legs. Each leg takes at most two time units by the pursuit lemma. This proves the theorem, including the horizon claim.

### 1.3 Finite enumeration

At any canonical capture event, the next segment has one of two directions. Its end is the first encounter with a previously uncaptured hider in that direction. If there is no uncaptured hider ahead, the direction is unnecessary: it cannot acquire a new capture before the endpoint, and an uncaptured hider cannot overtake it from behind. Every retained branch acquires at least one new capture.

Thus there are finitely many canonical paths, independently of the weights. The theorem proves their sufficiency by pointwise capture-time comparison, rather than by assuming existence of an optimizer over the original infinite-dimensional monster path space.

For ordered hiders, a captured set is a contiguous interval of indices. Indeed, to encounter two ordered outer paths, continuity forces an encounter with every path between them. The current event therefore has at most two uncaptured neighboring targets. This justifies the interval-state search in `packages/interval_uniform_reduction/exact_response.py`.

With distinct initial positions and no simultaneous acquisitions, the number of complete interval-expansion orders across **all** starting indices is `2^(n-1)`: read a capture order backwards, successively removing its leftmost or rightmost remaining index. Coincident acquisitions only remove branches after a deterministic refinement of the tied order. This sharper count is still exponential in support size and is not a uniform finite reduction of the full game.

## 2. The pruning rules are justified

### Independent-target lower bound

At a state with current event `(t,x)`, captured set `S`, and accumulated weighted capture cost `C`, let `h_j` be the earliest meeting time of uncaptured target `j`. The pursuit lemma computes this time exactly. Every continuation has cost at least

    C + sum_{j not in S} w_j h_j.

The individual earliest meetings need not be jointly realizable. That does not compromise a lower bound. Comparing this bound with an attained full-route cost is valid branch-and-bound pruning, provided equality is retained whenever all minimizers rather than just the minimum value are sought.

### Earlier-anchor dominance

Consider states with the same captured set `S` and anchor target `i`, at times `t'<=t`, and costs `C'<=C`. From the earlier state, shadow `p_i` until time `t`, then follow a continuation of the later state. The already captured targets cost no more in aggregate. Any additional captures during shadowing occur no later than they would in the later-state continuation. Hence the earlier state has no larger continuation optimum.

The comparison requires both inequalities. Keeping only the earliest arrival or only the cheapest arrival would not suffice. The implementation retains the nondominated `(time,cost)` pairs.

### Implementation conditions checked in this audit

The ordered integer solver validates the following before using its specializations:

* positive integer weights, ordered times, and slopes in `{-1,0,1}`;
* noncrossing order, checked at the union of the piecewise-linear vertex times;
* reflection symmetry of both weights and complete paths before omitting negative starting positions;
* exact divisibility at intersections, rather than rounding to its integer scale;
* acquisition of every coincident neighboring target before further branching.

The generalized-inverse calculation uses the **first** occurrence of a characteristic value at a flat portion. This is the appropriate convention for first capture. The state normalization removes targets coinciding at the current event before a future-meeting calculation is used for an adjacent target.

This is a mathematical and source-level audit, not a Lean proof or an independent rerun of every archived certificate. No error in these two pruning principles or the structural normalization was found.

## 3. A nine-point counterexample to a two-interior-turn theorem

Let all hiders remain stationary. Give the following unnormalized weights to their starting positions; the total weight is `5266`.

| Position | Weight at each listed position |
|---|---:|
| `0` | `4096` |
| `-1/4`, `1/4` | `512` |
| `-1/2`, `1/2` | `64` |
| `-3/4`, `3/4` | `8` |
| `-1`, `1` | `1` |

This distribution is symmetric, its hider paths are ordered, and every nonnegative hider stays in the nonnegative half-interval.

An optimal route, up to reflection, has turning vertices

    (time,position):
    (0,0), (1/4,1/4), (1,-1/2), (9/4,3/4), (4,-1), (6,1).

It has **three interior turns** and one endpoint turn. The sums of the two capture times in successive shells are `1,3,6,10`. Its expected capture time is therefore

    (512*1 + 64*3 + 8*6 + 1*10)/5266
      = 381/2633.

Exact enumeration of all 256 interval-expansion orders gives the following restricted response values:

| Maximum number of interior turns | Minimum expected capture time |
|---:|---:|
| 0 | `752/2633` |
| 1 | `809/5266` |
| 2 | `763/5266` |
| 3 or more | `762/5266 = 381/2633` |

In particular, the best route with at most two interior turns is worse by exactly `1/5266`. Only the displayed route and its reflection attain the unrestricted minimum, up to continuing straight through intermediate captures and irrelevant motion after the final capture.

### Why the restricted enumeration covers arbitrary monster paths

For stationary hiders, delete excursions that obtain no new capture, start at the first captured hider, and travel directly between successive new captures. This cannot delay any capture. Its new-capture order expands a contiguous interval, so the enumeration below covers it.

It also cannot increase the number of interior reversals in this example. A reversal of the direct route at an interior newly captured position corresponds to a reversal of the original route before its next new capture. Such an original reversal cannot instead occur at an endpoint: both endpoints contain uncaptured positive-weight hiders whenever that would alter the new-capture order. Distinct reversals occur between distinct consecutive capture events. Thus a route with at most two interior turns is dominated by an enumerated route with at most two interior turns.

The following complete Python standard-library calculation reproduces the table with integer arithmetic. Positions and times are multiplied by four, so the integer weighted costs are divided by `4*5266` only at the end.

```python
from fractions import Fraction

positions = list(range(-4, 5))
weights = [8 ** (4 - abs(x)) for x in positions]
records = []

def visit(left, right, current, time, cost, direction, inner_turns):
    if left == 0 and right == 8:
        records.append((cost, inner_turns))
        return
    for nxt in (left - 1, right + 1):
        if not 0 <= nxt < 9:
            continue
        new_direction = 1 if nxt > current else -1
        new_time = time + abs(positions[nxt] - positions[current])
        new_turn = (direction != 0 and direction != new_direction
                    and abs(positions[current]) < 4)
        visit(min(left, nxt), max(right, nxt), nxt, new_time,
              cost + weights[nxt] * new_time, new_direction,
              inner_turns + int(new_turn))

for start in range(9):
    visit(start, start, start, 0, 0, 0, 0)

assert len(records) == 256
assert sum(weights) == 5266
assert [min(c for c, k in records if k <= cap)
        for cap in range(4)] == [6016, 3236, 3052, 3048]
for cap in range(4):
    cost = min(c for c, turns in records if turns <= cap)
    print(cap, Fraction(cost, 4 * sum(weights)))
```

The counterexample is a response problem, not a good hiding strategy for the full game. Its purpose is to invalidate a proposed universal structural implication.

## 4. Arbitrarily many interior turns and no universal response horizon

The preceding phenomenon is not confined to one extra turn. The following family has a direct hand proof.

For any integer `k>=1`, put

    r_i = i/k  (1 <= i <= k),
    epsilon = 1/(16*k^2 + 1).

Place stationary hiders at `0` and at every `+r_i,-r_i`. Give the center unnormalized weight one and each member of shell `i` unnormalized weight `epsilon^i`, then normalize by `1+2*sum_i epsilon^i`.

**Theorem 2.** Every optimal pure monster response, up to reflection and irrelevant post-capture motion, starts at zero and makes successive alternating sweeps of the nested shells. It has `k-1` interior turns and one final endpoint turn. Its last capture occurs at time `k+2`. An optimal mixed response can randomize between the two reflected pure routes.

### 4.1 The weights impose lexicographic minimization

Set

    G_0 = T(0),
    G_i = T(+r_i) + T(-r_i),  i>=1.

By Theorem 1 it suffices to compare canonical responses. Their event coordinates are multiples of `1/k`; their travel times and each `G_i` are therefore multiples of `1/k`. With `n=2k+1`, every canonical response finishes by `4k`, and hence `0<=G_i<=8k` for `i>=1`.

Consider two canonical responses. Suppose their first unequal coordinate in `(G_0,G_1,...,G_k)` is `j`, with the first response smaller there. Its advantage at that coordinate is at least `epsilon^j/k`. Every possible disadvantage at later coordinates has total magnitude at most

    8k * sum_{i=j+1}^k epsilon^i
      < epsilon^j * 8k*epsilon/(1-epsilon)
      = epsilon^j/(2k).

Thus the first response has strictly smaller weighted objective. Minimizing expected capture time is exactly lexicographic minimization of `(G_0,G_1,...,G_k)` on the finite canonical family.

### 4.2 Lexicographic minimization forces the sweeps

Minimizing `G_0` forces the monster to start at zero. To minimize `G_1`, it must first reach one of `+r_1,-r_1` at time `r_1`, then traverse directly to the other at time `3r_1`. The two choices are reflections. There is no time for an additional excursion if these capture times are attained.

Suppose shells through `i-1` have been completed in the forced way, at time `s_{i-1}`, with the monster at one of `+r_{i-1},-r_{i-1}`. It has not visited either member of shell `i` yet: the forced earlier part stayed within the inner shells.

From this event, the two possible first-visit orders for shell `i` have capture-time sums

    2*s_{i-1} + 4*r_i - 2*r_{i-1},
    2*s_{i-1} + 4*r_i + 2*r_{i-1}.

The first is strictly smaller. It is attained only by continuing to the nearer member of shell `i`, reversing there, and crossing directly to its other member. Therefore this behavior is forced when `G_i` is minimized subject to the earlier coordinates.

Inductively,

    G_i = 4 * sum_{j=1}^i r_j,
    s_i = 2 * sum_{j=1}^i r_j + r_i.

The first visited member of every shell is a reversal point. For shells `1,...,k-1` those points lie strictly inside the arena; the final shell is the pair of endpoints. Since `r_i=i/k`,

    s_k = 2 * (k+1)/2 + 1 = k+2.

The speed bound and equality in these travel-time inequalities force the same actual route for any unrestricted optimizer: if its canonical improvement has equal weighted cost, positivity of every weight forces equality of every capture time. This proves the theorem beyond just the finite enumerated family.

### Consequences and limitation

There is no constant `B` such that every symmetric ordered hider distribution has an optimal monster response with at most `B` interior turns. There is likewise no constant `H` such that every such distribution has an optimal response completing all its captures by `H`. These failures already occur for stationary hiders, so allowing more general princess motion cannot repair the proposed universal statements.

This does **not** prove that the unrestricted interval game has no equilibrium with a small number of turn types or a short horizon. A correct reduction of that kind would need extra properties specific to an optimal or near-optimal hiding law, rather than just symmetry, order, or confinement of reflected paths to their respective half-intervals.

## 5. Result for the proof roadmap

The finite-response part of the project has a sound structural foundation after the induction in Section 1 is made explicit. In particular, the search is not assuming a universal turn bound when it verifies a **fixed** finite hider distribution.

The next global structural claim must avoid the counterexamples in Sections 3 and 4. Promising claims would have to derive additional conditions from optimality in the full game, or supply a matching global strategy certificate directly. A bare assertion that optimal responses to all ordered symmetric hiders use only one or two interior reversals, or finish by a universal time such as four, is false.
