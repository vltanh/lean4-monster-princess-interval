# Exact atomic survival response by one closure cut

## Status and scope

This note gives an exact response theorem for a supplied finite symmetric
monster law. Each monster route is continuous, has finitely many unit
right/left legs, remains in [-1,1], and has completed a sweep of both
endpoints by a common finite time T. Zero-duration legs are deleted.
The M1, center-reaching M2/M3, and general initial-inward I atoms used by
the implementation satisfy these conditions. Arbitrary initial princess
position, arbitrary subsequent turns, center crossings, and absorption
after time two are included.

The theorem does not construct a matching lower law or identify the
unrestricted game's value. Optimizing weights on a fixed finite set of
monster atoms is a separate finite-support minimax problem.

Implementation: atom_survival_cut.py.
Verifier: verify_atom_survival_cut.py.

Before the executor disconnected, the non-lexicographic implementation
passed 1,335 exact/physical checks:
416 exhaustive reward/capture identities; 5 exact exhaustive global cuts
including both lattice extrema; 456 mixed-family exact reward/capture
identities; 456 legal strict-speed physical capture comparisons; and
2 complete-law realizations of the cut extrema.

The lexicographic implementation and its expanded verifier were written,
but that verifier had not returned when the environment disconnected.
Do not mark that expanded suite as passed.

## 1. Folding and a dense strict-speed class

For every reflected monster pair and every continuous princess p,

    T(m,p)+T(-m,p) <= T(m,|p|)+T(-m,|p|).

At the first radial contact, one original orientation captures. At the
later folded capture, continuity forces the remaining original
orientation to have captured already. Absolute value preserves the
Lipschitz bound. It therefore suffices to maximize over 0<=p<=1.

Capture time is lower semicontinuous for uniform path convergence on
[0,T]. Indeed, before any time strictly below the limiting first
capture, the continuous distance from the monster has a strictly
positive minimum.

For eta>0 put

    p_eta=(1-2 eta)p+eta.

Then eta<=p_eta<=1-eta and Lip(p_eta)<=1-2 eta. Fatou and lower
semicontinuity imply that the supremum is unchanged by restricting to
strict-interior, strictly subunit-speed paths. Both light coordinates

    U=t+p(t),  V=t-p(t)

are strictly increasing for these paths. Thus U=P(V) is a continuous
strictly increasing graph, and the same value P(V) governs both sides
of any queried contact. No independent first/last choice is made at a
shared monster corner.

Extend this graph virtually to (U,V)=(0,-1), before t=0. If p(0)=a in
(0,1), a strictly increasing segment joins (0,-1) to (a,-a) inside the
strip 0<U-V<2. The curve crosses U+V=0 freely, so the initial a is not an
outer optimization variable.

After all captures, extend the graph to a sufficiently large final V.
These extensions do not change any payoff.

## 2. Finite event data and survival

In light coordinates every unit-right monster leg is horizontal and
every unit-left leg is vertical. Include in the event set

    v_0=-1 < v_1 < ... < v_n

every V coordinate of every vertex of every route and its reflection.
Take v_n at least the largest such coordinate. Because both
orientations complete endpoint sweeps, this lies beyond the time range
in which a capture can remain outstanding.

Write x_j=P(v_j). Feasibility is

    max(0,v_j) <= x_j <= v_j+2,
    x_j <= x_(j+1).

The virtual first value can be fixed to x_0=0; the last value can be
fixed to x_n=v_n+2 after all captures.

At a monster point (u,v), with t=(u+v)/2,

    p(t)>m(t) iff P(v)>u,
    p(t)<m(t) iff P(v)<u.

Survival through time t is the disjoint sum of the events that the
princess has remained strictly above, or strictly below, the entire
monster prefix. Equality is capture and belongs to neither event.

Let A and B denote the conjunctions of all preceding above and below
vertex tests. A horizontal leg from (u0,v) to (u1,v) contributes

    A * clamp(P(v)-u0, 0, u1-u0)
      + B * (u1-u0)

to twice that orientation's capture-time integral.

A vertical leg from (u,v0) to (u,v1) contributes

    A * (v1-v0)
      + B * integral_[v0,v1] 1[P(v)<u] dv.

After each leg, append the strict above/below tests at its endpoint.
The initial tests are at the actual monster start, so initial
coincidences are handled exactly.

For an atom of pair mass w, sum these expressions for both orientations
and multiply by w. The result is the atom's four-score, 4 w J_pair.

## 3. Exact exchange between event queries

Hold all query values x_j fixed. No horizontal monster leg occurs at an
unqueried V. On (v_j,v_(j+1)), lower P to

    P_min(v)=max(x_j,v,0).

This weakly increases every below-survival integrand and leaves every
queried above/below test and every horizontal-leg term unchanged.

The endpoint value x_(j+1) is realized by a connector in a V interval
immediately BEFORE v_(j+1). If the connector meets the upper physical
edge, follow U=V+2 for its final part. If it meets the lower edge, follow
U=V. Its V width can be made arbitrarily small. Its physical duration
need not be small, but all affected vertical-leg integrals change by at
most that V width, while queried values are retained.

The exact limiting below integral on a subinterval is therefore

    [min(v_(j+1),u)-v_j]_+ * 1[x_j<u].

The resulting finite query functional is an upper envelope of every
continuous graph with the same query values.

Conversely, any feasible nondecreasing query array has legal connector
realizations. Perturb it toward a strictly increasing interior reference
and use a smaller connector width. Strict query predicates survive;
equality predicates contribute no post-contact reward and can only
gain in the limiting perturbation. Fatou applied to the nonnegative
survival integrals proves that the finite array's score is approached
from at least that value by legal paths. A final strict-speed spatial
shrink handles center and endpoint contacts.

Thus the unrestricted princess-response supremum equals the supremum of
this finite, piecewise-affine query functional. There is no special U=1
relaxation, no wave-count restriction, and no final V<=1 clamp.

## 4. Lexicographic event labels close the supremum exactly

Let B contain:
* every nonnegative U coordinate of every monster vertex;
* 0;
* every physical query bound max(0,v_j) and v_j+2.

All ramps break at points of B. All strict survival predicates compare a
query value to a point of B.

Partition the ordered feasible polytope into its strict/equality
comparison faces relative to B. On each face the score is affine.
Every vertex of a face's closure uses values from B: otherwise a maximal
block of equal unanchored coordinates can be moved in both directions,
contradicting extremality.

A face supremum may lie on a boundary where closed capture loses
future reward. Retain its approach side with labels

    (b,-), (b,0), (b,+),   b in B,

ordered lexicographically. Evaluate every ramp LENGTH at b. Evaluate
every strict predicate by comparing the label with (u,0). At physical
bounds, exclude the outward labels (lower,-) and (upper,+).

The order-polytope face argument proves that every continuous response
has score at most the maximum over these finitely many lexicographic
arrays.

Conversely, an ordered lexicographic array is realized by replacing
(b,side) with b+side*epsilon and then making an ordered epsilon^2
perturbation inside the physical bounds. Connectors use a still smaller
scale. Labels with exact side zero may move to either side; their
closed-contact score is no larger than the available limiting score.
This proves approachability of every lexicographic array's score.

Therefore the exact unrestricted response supremum of the supplied
finite law is the finite lexicographic maximum.

Rational atom parameters and rational pair masses produce rational
capacities and a rational response supremum. No endpoint mesh limit,
initial-position search, or trace-offset error interval is required.

## 5. Positive AND rewards and one maximum-closure graph

Each above term is a nonnegative conjunction of increasing threshold
bits [x_j>=label_k]. Each below term is a nonnegative conjunction of
their complements. An increasing ramp is expanded into its
nonnegative adjacent label increments.

For w>=0:

* w times an AND of positive bits is represented by an auxiliary z
  with reward w z and implications z=>each bit.
* w times an AND of negative bits is represented by an auxiliary z
  with reward w(1-z) and implications each bit=>z.

One-bit terms are unary. Order of labels within a variable and
monotonicity between successive V events are hard implications.
Physical bounds fix the corresponding threshold sides.

The resulting maximum-closure problem is one source/sink minimum cut.
Its hard capacity can be 1 plus the sum of absolute unary coefficients.
A feasible path never needs to cut a hard implication.

The code independently checks the cut value against a first-contact
scan on the same limiting query graph. Above paths can first capture
only on a horizontal leg, at U=P(V). Below paths can first capture only
on a vertical leg, at the next query whose value reaches U, or at the
center diagonal V=U, whichever comes first.

## 6. The full optimal face

After a maximum flow:
* residual-source-reachable threshold nodes are forced true;
* nodes that can reach the residual sink are forced false;
* the remaining positive-residual implications describe every optimal
  closure choice.

The implementation retains this entire residual face, together with
its minimum and maximum query arrays. It does not declare that every
limiting maximizer is attained by a physical path. The realization
above gives the corresponding epsilon-optimal legal paths.

A lower law assembled inside the full equality face must still satisfy
all pure-monster inequalities, including monster paths outside the
finite supplied support. Those are the remaining saddle obligations.

## 7. Current diagnostic

The earlier 423-atom probability fit used a coarse fixed paired-control
set and was dominated in its dual by one supplied complete CDF response.
It was not a global upper certificate.

The new survival cut attacked its 73-positive-atom law at approximately
1.46019594034. Independent legal rational paths gave approximately
1.46019594035. This is an attack on that specific fitted law, not a new
game-value interval.

The main response starts near a=13/16, uses additional pre-U1 turns,
then a genuine incoming phase just after U1. It can complete its useful
outward continuation before time two; arbitrary later zero-price
motions are not evidence that absorption after two is necessary.

The next authorized computation is a normalized probability-law solve
using this global event cut, retaining all physical atoms and the
discovered continuous-start attacking routes. It must report the
actual response face and support, not present the old coarse fit's
objective as an equilibrium.
