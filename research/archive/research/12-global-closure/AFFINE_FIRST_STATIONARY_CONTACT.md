# First stationary contact inside one affine CDF cell

## Statement and scope

Let a closed space-time cell be bounded by finitely many characteristic
half-planes of slopes +1 and -1, a time slab, and two stationary walls
ell<=x<=r. The signed CDF on the cell is

\[
 F(t,x)=c+\alpha t+\beta x,\qquad \beta\ge|\alpha|.
\]

Physical endpoints may be treated as walls, with their atomic first contact
handled separately; the argument below concerns the continuous interior
CDF up to that contact. An old captured rank interval contains the entry
rank.

Fix the entry point and time, an exit point and time T, and a later
continuation. For every finite legal prefix inside the cell there is a
prefix with no greater expected first-capture cost, the same exit and
continuation, such that one of the following holds:

1. It reaches a stationary wall after at most seven unit-speed affine
   pieces, and all later motion is left available to the next phase.
2. It reaches the prescribed exit without a stationary contact and has
   at most seven such pieces in the entire prefix.

The statement counts only through the first stationary contact. It does
not claim that the entire continuation after that contact has seven pieces.
An initial point already on a stationary wall has a zero-piece prefix.

The same conclusion follows for arbitrary prefixes on a bounded horizon
by the limiting argument in Section 7. The constant does not depend on the
original number of turns. This is a local ingredient for a coarse global
decomposition; that decomposition and its subsequent phase count remain
separate obligations.

## 1. Characteristic constraints need no extra record faces

Along every legal Monster path, x-t is nonincreasing and x+t is
nondecreasing. Consequently, if two endpoints lie in a specified
characteristic half-plane, every legal bridge between the same endpoints
lies in that half-plane as well. This applies to either side of either
characteristic line.

Thus any replacement with the same entry and exit remains in all of the
cell's characteristic half-planes. Fixed endpoint times similarly retain
the time slab. Only stationary-wall confinement needs to be imposed on
the record variables.

The statement concerns each affine time piece of a characteristic edge.
A coarse decomposition must retain its vertices before applying this
observation across a change of edge velocity.

## 2. Constrained earliest rank travel

Reflect spatial and rank coordinates if necessary so alpha>=0. First take
the nondegenerate case beta>alpha, and put

\[
 c_+=\beta+\alpha,\qquad c_-=\beta-\alpha.
\]

From a state (s,x) with current rank q=F(s,x), the earliest unconstrained
upper and lower target times are

\[
 s+\frac{q'-q}{c_+}\quad(q'>q),\qquad
 s+\frac{q-q'}{c_-}\quad(q'<q).
\]

For an upper target, travel unit right. If the upper wall is reached
before the target, remain at that wall until its increasing rank reaches
the target. This is the earliest feasible upper capture. Before the hit,
its attained rank is the largest allowed by the unit-speed ray and the
upper wall.

A feasible lower target cannot be blocked by the lower wall. The unit-left
ray has the smallest possible rank until reaching that wall. If it has
not reached the target there, the wall rank is already above the target
and only rises thereafter. No later legal motion can reach that lower
target. This would contradict the assumed feasibility of the old target
itinerary.

For a fixed rank q, the times at which its quantile lies between the
stationary walls form an interval:

\[
 \frac{q-c-\beta r}{\alpha}\le t\le
 \frac{q-c-\beta\ell}{\alpha}
 \qquad(\alpha>0).
\]

An earlier feasible arrival can follow that rank's legal quantile to the
old arrival time; the whole intervening time interval is still available.
For alpha=0, feasible ranks are stationary and the same assertion is
immediate.

Applying the constrained earliest rule successively to an old finite
sequence of record targets catches every requested rank no later. Any
upper-wall wait exposes a stationary contact. Stop at the first such
contact if it occurs. Before it, productive capture travel consists only
of unit legs. The new first contact may be earlier than the old first
contact; this is allowed and starts the same next boundary phase.

At the final target, unused time may be taken as a constant-rank hold,
followed by the old nonproductive exit connector. A straight connector
between the same two endpoints is legal, remains in the cell, and has
affine rank between its endpoint ranks. Thus it is nonproductive when
those ranks already lie in the captured interval.

## 3. The exact single-cell quadratic

Translate the entry time and rank to zero. Write the alternating productive
record levels as

\[
 +x_1,-x_2,+x_3,\ldots
\]

after choosing the first sign, with x_i>=x_(i-2). Both old rank boundaries
are retained as lower bounds on the corresponding first new records.
The arrival clocks satisfy

\[
 \tau_1=x_1/c_1,\qquad
 \tau_i-\tau_{i-1}=(x_i+x_{i-1})/c_i.
\]

Here c_i alternates between c_+ and c_-. The opposite first sign simply
interchanges the two rates. With the last two records fixed, put
k=1/c_++1/c_->0. The capture moment is the known affine-cell quadratic

\[
 \begin{split}
 M={}&\frac{x_N^2}{2c_N}+\frac{x_{N-1}^2}{2c_{N-1}}\\
 &+k\left[
 (x_{N-1}+x_N)\sum_{j\le N-2}x_j+x_Nx_{N-1}
 -\sum_{j\le N-2}x_j^2
 -\sum_{j\le N-2}x_jx_{j+1}\right].
 \end{split}
\]

Only the Hessian is needed. For an intermediate variation v with m=N-2
coordinates,

\[
 v^\top D^2M v
 =-k\left[v_1^2+v_m^2+
          \sum_{j=1}^{m-1}(v_j+v_{j+1})^2\right]<0
 \quad(v\ne0).
\]

For m=1 the first and last terms are both v_1^2. This is strict
negative definiteness, with no parity-only or two-density assertion.

Old captured ranks change only a constant and a linear term. For example,
with old offsets [-b0,a0] and a right-first productive chain, the omitted
old-rank moment is

\[
 \frac{a_0^2}{2c_+}+\frac{b_0^2}{2c_-}
 +\frac{2\beta b_0}{c_+c_-}\,x_1.
\]

Hence the Hessian is unchanged. If one side never exceeds its old record,
it is a one-sign episode and needs no quadratic argument.

## 4. Compact record polytope and nonproductive collisions

Fix the final two records and the original last-record time as an upper
time budget. Earlier completion can be held at the last rank until that
time, preserving its physical point and the later connector exactly.

The remaining constraints are linear:

- the two parity record-order chains and old-record lower bounds;
- the one last-record clock budget;
- stationary-wall bounds at unit-record vertices and hold endpoints.

Checking the wall bounds at segment endpoints suffices because both
physical motion and the walls are affine. Characteristic bounds are
automatic by Section 1. Record magnitudes are bounded by the fixed time
budget and the finite rates, so this is a compact polytope.

A duplicate same-side record is nonproductive. Its out-and-back portion
can be removed, holding the previous record until the old return time
if necessary. That quantile stays available throughout the intervening
interval. Reapplying constrained earliest travel consolidates the holds
at the end, unless it reveals an earlier stationary contact. In either
case no new productive level is introduced.

The same argument handles a first candidate record equal to an already
captured boundary and zero-duration legs. A genuine terminal wall contact
inside an old captured band is retained as a nonproductive connector, not
counted as a productive record level.

These collision reductions are made before the free-dimension count;
one must not count a long chain of repeated tight record levels as
independent productive turns.

## 5. The first active wall face

Minimize over the finite union of feasible record polytopes with at most
the original productive-level count and either first direction. Each
polytope is compact. Choose a least-length minimizing representative;
the preceding collision reductions then remove duplicate and nonproductive
levels before the strict-face dimension count. If it has a
stationary contact, take its first one and freeze:

- its time and position;
- both captured prefix records there;
- every later record variable and the complete later continuation.

All stationary-wall constraints strictly before this first contact are
strict. The contact's physical position adds no new independent constraint
once its rank and time are fixed. If the contact is a productive vertex,
fixing its time is one linear clock equality.

If the first contact lies on the final constant-rank hold or nonproductive
connector, instead retain the old last-record point and time as the single
upper budget. A nearby earlier completion can still be held to that time,
and the same fixed connector reaches the contact. Before contact the hold
and connector remain confined because their endpoints do. No second
independent time or spatial budget is introduced.

If there are more than three productive levels before this event, fixing
the last two leaves at least two intermediate variables and at most one
clock constraint. After the collision reductions all their record-order
and old-record inequalities are strict. There is therefore a nonzero
two-sided feasible local variation. It preserves all earlier strict wall
constraints for a sufficiently small displacement.

The strictly negative Hessian in Section 3 implies that at least one side
of this variation has smaller capture moment. The frozen records and
contact state make every later cost unchanged. This contradicts
minimality.

Thus at most three productive unit legs precede the first stationary
contact. If no wall is touched, the identical argument applies through the
prescribed exit, using its fixed final records and single time budget.

This is a first-face argument. Taking a later active face without freezing
earlier confinement constraints would not justify the dimension count.

## 6. Unitization and degenerate cells

The compressed prefix has at most three productive unit legs, one
constant-rank hold, and one nonproductive affine connector.

A nonproductive interval between fixed endpoints may be replaced by its
pointwise maximal or minimal legal bridge. It loses no previously captured
rank, and any extra capture only helps the unchanged continuation. Inside
the stationary walls, such a bridge has two unit legs unless it hits a
wall. If it hits one, the first contact occurs on its initial unit leg;
the rest belongs to the next phase and is not charged to this prefix.

Consequently the count through the first stationary wall, or through the
exit when there is no contact, is at most

\[
 3+2+2=7
\]

unit pieces. No boundary wait is charged as a pre-contact unit piece.

If beta=alpha>0, the CDF rank along every legal path is nondecreasing:
F'=alpha+beta*m'>=0. Only an upper record can grow. The clipped pointwise
maximal bridge gives the required bound directly. The beta=-alpha case is
its reflection. If beta=alpha=0 the cell is rank-flat and an extremal
bridge is again sufficient. Thus vanishing inverse speeds do not require
division by zero or a nonexistent quantitative two-front width gain.

This degenerate reduction alone does not create a positive captured width
when endpoint constraints force a constant-rank characteristic. A global
count must charge its passage through the finite coarse geometry rather
than inserting a false positive-width estimate.

## 7. Arbitrary prefixes and what remains global

For a bounded-horizon arbitrary prefix in the closed affine cell, use
piecewise-linear interpolation retaining the final record extrema and the
exit. The local CDF is Lipschitz, so the running records and original-band
capture moments converge. No old final captured rank is lost, and extra
captures can only help the fixed continuation.

Apply the finite reduction. Full paths remain equi-Lipschitz with fixed
exit and later continuation. Along a subsequence, their first-contact
times converge; the at-most-seven-piece prefixes are compact after
zero-duration pieces are permitted. A limiting contact can occur earlier,
which only shortens the counted prefix. First-capture lower
semicontinuity and Fatou preserve the no-greater-cost conclusion.

This gives the local lemma for arbitrary prefixes. It still does not by
itself provide a global number of cells, interface epochs, or post-contact
record switches. In particular, the quantitative width bound of a
nondegenerate interface block requires its full future persistence
hypothesis. The coarse construction must state separately how degenerate
one-front passages and critical time faces are charged.

## Dependencies

The affine quadratic and strict Hessian are the single-density result in
AFFINE_RECORD_PREFIX.md (proof blob
25e05857eea4505d87730829b3ce455d5d77d265).
The constrained target travel and old-band conventions agree with
AFFINE_HALF_CELL_BRIDGE.md (corrected proof blob
a7f977451db98b0b00bdd4e5b3f1f4fd3974cf3a).
The arbitrary-old-record interface return theorem is
INITIAL_INTERFACE_RETURN_BLOCK.md (blob
d10fa2df15cb767f11fb5cb4b92cf990e3a046ce).

This note is a symbolic proof audit. It introduces no sampled numerical
turn cap and claims no new native execution.
