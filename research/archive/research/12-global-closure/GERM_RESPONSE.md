# Exact response to an approaching finite princess law

This is a global test of a supplied finite family. It does **not** establish the
unrestricted game's value or a sufficient finite equilibrium class. In the
executed example it rejects the canonical lower counterpart of an exactly
solved finite monster bank by a large, explicit gap.

## 1. Uniform rational-germ response theorem

Let a finite princess family have positive rational weights summing to one.
Assume every time and position coordinate of every vertex is a rational
function of a parameter epsilon. After its last vertex, each path remains
constant. Suppose that for all sufficiently small positive epsilon the paths
are legal and ordered, including ties:

    p_1(t) <= ... <= p_n(t).

Leg slopes may themselves be rational functions of epsilon. The paths need
not reach an endpoint. Distinct paths that have the same epsilon-zero limit
must remain distinct unless their full rational germs agree.

**Theorem.** The unrestricted monster-response value is a rational function
of epsilon on some common positive interval. A completed finite symbolic
capture-order computation determines that function, an attaining monster
route, and an explicit positive rational radius on which the result holds.
The infimum here includes monsters whose initial position, turn positions,
number of turns and entire trajectory depend on epsilon.

### Proof

For each fixed epsilon, the capture-order domination theorem in
`research/07-structural-audit/CAPTURE_ORDER.md` permits a monster starting on
one of the princess initial locations and running directly at unit speed
between successive new captures. For ordered paths, the captured labels form
an interval. At each state, the next new capture comes from its left or right
neighbor, with coincident labels captured simultaneously. Each genuine step
increases the captured set, so the complete tree is finite for this supplied
family. This bound depends on its support size; it is not a turn bound for
arbitrary hiding laws or for equilibrium.

On any fixed hider leg, solving a direct unit-speed intersection uses only
rational arithmetic in its vertex coordinates. Leg selection, simultaneous
capture, ordering, and objective comparisons require only signs or identities
of rational functions. There are finitely many branches and comparisons.
Their eventual signs are fixed on a common positive interval. Therefore the
same symbolic branching computation is valid for every epsilon in that
interval and returns one rational-function minimum.

This argument is uniform over the monster. It is **not** an interchange of
an infimum and a limit and does not infer capture behavior by substituting
epsilon=0 into the paths. The actual capture times are determined first;
their rational limits are taken only afterward.

### Exact comparison radius

Write a nonzero polynomial as

    p(epsilon) = epsilon^k (a_k + a_(k+1) epsilon + ... + a_d epsilon^(d-k)),

where a_k is nonzero. Put S=sum_(j>k)|a_j|. For

    0 < epsilon < min(1, |a_k|/(2 S)),

the bracket has the sign of a_k. When S=0 there is no extra restriction.
Apply this separately to the numerator and denominator of each rational
comparison, and take the minimum of the resulting positive radii. Divisions
also certify that their divisors remain nonzero.

An equality test that returns **false** must record the root-free interval of
its difference. Otherwise an isolated positive root could change an initial
tie, a simultaneous capture, or a collinearity decision inside the reported
radius. `Germ.__eq__` includes this check; the regression suite specifically
tests this issue. Identity equalities need no sign test.

### Pruning does not change the theorem

The implementation uses the same exact comparisons as the existing rational
capture-order oracle:

* For the same captured interval and anchor princess, a state with an earlier
  time and no larger accumulated cost dominates a later state. It can shadow
  the anchor until the later time and then imitate the later continuation.
  Incidental extra captures can only help.
* The sum of the independently earliest possible capture times of all remaining
  targets is a lower bound on any common continuation. A branch whose bound is
  at least the already attained best cost can be discarded.

Every comparison used by these rules is a protected rational-germ comparison.
The node limit raises an error if reached; an interrupted search is not a
completed response certificate.

## 2. How the supplied paths are constructed

`packages/interval_global_closure/germ_response.py` follows the existing
lexicographic survival-cut realization exactly. It displaces contact labels by
epsilon, puts connectors epsilon squared before the next query, and applies
the strict spatial shrink

    x -> (1-2 epsilon^6) x + epsilon^6

to positive paths. Reflection gives the negative paths. The nested threshold
components produce ordered physical paths; the code also checks their order
at every relevant vertex time and checks all speed and arena inequalities.

These shrunk positive paths end at 1-epsilon^6, not at the arena endpoint.
The oracle uses their actual constant tails. It does not apply an
endpoint-absorption completion formula to them.

For an exact reconstruction input, rational weights are preserved unchanged.
For a floating discovery input, the reconstructed rational weights and their
normalizing sum are recorded explicitly. The latter reconstruction is a
specified legal law, not an exact solution of the discovery LP.

## 3. Exact rejection of the coarse canonical lower law

`global_minimax_grid4_exact.json` gives an exactly solved bank of 472 monster
pairs. Its finite-bank value is

    c_bank = 219625051 / 152700512 = 1.4382731801187412... .

The exact reconstruction selects nine positive nested princess components,
with their nine reflections. The germ oracle exhausts their unrestricted
monster response. For

    0 < epsilon < 1700401 / 21043007044,

the exact response is

    J_epsilon =
      (108090289 - 38175128 epsilon + 38175128 epsilon^2
       - 139830322 epsilon^6 + 76350256 epsilon^7 - 76350256 epsilon^8)
      / (152700512 (1-epsilon^6)).

It is attained by a monster starting at

    x_epsilon = 3/4 + epsilon^2 - epsilon^6/2 - 2 epsilon^8

and running left at unit speed. It may continue directly to -1 after the last
listed capture; that extension changes none of the capture times. In
particular,

    lim_(epsilon->0+) J_epsilon
      = 108090289 / 152700512
      = 0.7078580653351051... .

The completed search visited 171 states, including four completed leaves, with
40 exact dominance eliminations and 40 exact lower-bound eliminations.
Separate exact segment intersections reproduce the entire response function.

The positive initial mass concentrates, in the limit, as follows:

| Initial position | Positive-family mass |
|---|---:|
| 1/4 | 1714833 / 9543782 |
| 1/2 | 2972753 / 9543782 |
| 3/4 | 2428098 / 4771891 |

The approaching start just beyond the top cohort is absent from the fixed
bank. It defeats the whole canonical lower law without any interior reversal.
This failure cannot be repaired by treating epsilon as a smaller numerical
tolerance.

These numbers are response values for a rejected supplied princess law. They
are **not** bounds on the full game's value. The exactly verified finite-bank
upper law remains an upper guarantee; its particular canonical lower
counterpart fails to match it.

## 4. The larger canonical law has the same obstruction

The enriched discovery bank contains the existing 67-pair upper support and
additional coarse M1/M2/M3/I paths. Its nested decomposition has 76 positive
components. After the explicit rational reconstruction recorded in
`global_minimax_enriched_germ_attack.json`, the legal straight-left monster
starting at

    31/32 + epsilon^2 - (15/16) epsilon^6 - 2 epsilon^8

has a payoff whose exact rational limit is approximately
`0.7976998218727116`. Its protected radius is `1/25348`.

This is a verified **specified attack**, not an exhaustive minimization of the
152-path family. The value and reconstructed weights are stored as exact
rationals in that JSON. It does not identify the unrestricted response of the
original floating weights or an exact enriched finite-bank equilibrium.

## 5. Executed checks and the next global obligation

Run from the repository root:

    python packages/interval_global_closure/verify_germ_response.py
    python packages/interval_global_closure/germ_response.py \
      packages/interval_global_closure/global_minimax_grid4_exact.json

The larger specified attack can be regenerated without exhaustively searching
the 152-path response tree:

    python packages/interval_global_closure/germ_response.py \
      packages/interval_global_closure/global_minimax_enriched.json \
      --rightmost-left-attack \
      --output packages/interval_global_closure/global_minimax_enriched_germ_attack.json

Executed validation includes six small germ fixtures, pruned versus unpruned
search, 108 independent rational target-order permutations, the pre-existing
`exact_oracles.monster_best_response` implementation, moving coalescence,
initial ties, distinct equal-limit paths, nonconstant rational speeds,
constant tails, and the equality-root regression. Independently evaluated
`exact_oracles.first_meeting` checks all 18 coarse-certificate paths at a valid
rational epsilon against the displayed straight-left attack. Root reruns
passed these checks.

The finite upper response theorem is complete for its fixed monster support.
That does not make one canonical representative of every maximizing query
graph a sufficient lower-law class. In particular, the deadline theorem allows
responses to start throughout an open initial chamber, while the current
canonical realization concentrates near chamber boundaries. The next proposed
construction therefore retains the whole legal deadline corridor and its
continuum of initial positions. That construction still needs an unrestricted
monster lower certificate at the same constant as the upper law. No matching
saddle, Lean check, or full-game closure is asserted here.
