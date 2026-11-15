# An effective finite response bound for a fixed ordered finite fan

## Result and scope

Fix one ordinary finite fan law. Its base profiles have finitely many
affine pieces of slopes −1, 0, and +1, become stationary after a finite
time, and have fixed positive translation widths. Endpoint clipping and
fair reflection are allowed. Realize the resulting signed marginals by
one common ordered quantile.

More generally, the proof uses exactly these marginal properties:

- the signed CDF is continuous and piecewise affine in the open arena;
- its finite arrangement has characteristic edges of slope ±1 and
  stationary edges;
- in every interior cell, \(0\le F_x\le M\) and \(|F_t|\le F_x\);
- the final marginal is a static piecewise constant density with finitely
  many atoms.

Endpoint atoms are retained with their strict/closed capture traces.
Interior atoms and zero-width limiting fans are outside this statement.

There is a computable integer \(N\), defined below from this fixed
arrangement, such that the unrestricted minimum expected capture time is
attained by a Monster path with at most \(N\) unit-speed or waiting pieces.
Thus optimization over that finite class is globally sufficient for this
one law. The count is deliberately conservative.

For rational fan data, every constant and ceiling in the displayed bound
is exactly computable. Together with the usual semialgebraic capture
formula, it gives a terminating, although potentially very expensive,
exact response procedure. For algebraic data the same statement holds
using exact real-algebraic comparisons.

This does not prove that an optimal Princess law belongs to a fixed finite
fan family. It proves no game value or saddle, and the bound is not uniform
as fan widths tend to zero.

## 1. Records, horizon, and finite input geometry

Write the ordered signed quantile as \(p_q(t)\), \(0<q<1\). For a Monster
path \(m\), the captured ranks are bounded by

\[
 L(t)=\inf_{s\le t}F^-(s,m(s)),\qquad
 U(t)=\sup_{s\le t}F^+(s,m(s)).
\]

The uncaught mass is \(1+L-U\). Before the first physical endpoint contact,
the trace \(F(t,m(t))\) is continuous and \(2M\)-Lipschitz. Previously caught
ranks remain caught under every subsequent replacement.

Let \(h\) be a time after which the marginal is stationary, and let \(K_0\)
be the number of distinct density boundaries, atom positions, and arena
endpoints of that final marginal. The proved static-tail reduction gives
the completion horizon

\[
 H=h+2(K_0+3).
\]

An ordered history removes one rank interval; its two surviving spatial
tails introduce at most two new static cut positions. The static theorem
allows multiple reversals and retains atoms. No direct-tour or one-turn
assumption is being made.

The previously proved finite-existence theorem supplies an optimal
finite-piece path on this horizon. We start from that path only to make
the following chronological construction immediate; none of the bounds
below uses its unknown original number of pieces.

Construct a finite time grid on \([0,H]\) containing:

1. all fan-profile vertices and all starts/ends of CDF edges;
2. every intersection time of active characteristic and stationary edges,
   as well as intersections of characteristic edges;
3. \(0,h,H\), omitting repetitions and points outside the horizon.

Let \(S\ge1\) be the number of open time slabs. Subdivide every active
characteristic edge at this grid, and let \(E\) be their total number of
segments. Redundant coincident segments may be merged but need not be.

Let \(\mathcal C\) be all stationary edge positions occurring in these
slabs, together with \(-1,+1\). Set

\[
 \Delta=\min\{|c-c'|:c,c'\in\mathcal C,\ c\ne c'\}>0.
\]

Positions are merged before taking this minimum. In particular,
\(\Delta=2\) if only the two arena endpoints occur. A valid \(M\) is the
maximum of all interior cell densities \(F_x\); any independently
verified larger bound is also allowed.

These are properties of the complete fixed CDF arrangement, not of a
sampled response path.

## 2. Characteristic confinement is automatic

For every legal path, \(m(t)-t\) is nonincreasing and \(m(t)+t\) is
nondecreasing. Therefore every legal bridge between two endpoints in a
specified half-plane bounded by \(x=t+c\) or \(x=-t+c\) stays in that
half-plane.

A characteristic segment has a connected contact set along any legal
path. Partition the original finite optimal path at the time grid and at
both ends of every characteristic contact interval. The number of coarse
intervals is at most

\[
 Q=S+2E+1.
\]

An interval lying on a characteristic is already one unit piece. On every
other coarse interval \([a,e]\), all later same-endpoint replacements
remain in the original characteristic half-planes. A new contact with
one of those faces can only create an initial or terminal unit boundary
arc: if the controlling endpoint is strict, contact is impossible; if it
is an equality, monotonicity forces the whole intervening boundary arc.

Consequently there is no repeated characteristic-face charge during the
later normalization. Only stationary positions require additional
attention.

## 3. First stationary contact: the explicit seven-piece lemma

Consider the initial affine cell of a coarse interval, before its first
stationary contact. It is confined by stationary walls, the fixed time
interval, and characteristic half-planes. The latter constraints are
automatic by Section 2.

Write \(F=c+\alpha t+\beta x\). If \(\beta=|\alpha|\), only one record
direction can grow, so a pointwise extremal bridge handles the piece
directly. If \(\beta=0\), it is rank-flat. Otherwise, after reflecting
directions when necessary, put

\[
 c_+=\beta+\alpha>0,\qquad c_-=\beta-\alpha>0.
\]

Build the sequential earliest feasible itinerary through the old record
targets. Upper targets use unit right travel, with a wall wait only if the
upper wall is reached first. Lower targets use unit left travel. For
\(\alpha\ge0\), a lower target that is still below the rank at the lower
wall cannot become feasible later, because that wall rank only increases.

A rank's available times between the stationary walls form an interval.
An earlier feasible arrival can follow that rank's quantile, at speed
\(-\alpha/\beta\), to its old arrival time. Thus the earliest itinerary
catches every requested rank no later. Any required wall wait exposes a
stationary contact. Before the first such contact, productive travel is
unit speed.

For alternating new record magnitudes \(x_1,x_2,\ldots,x_n\), the two
parity sequences are nondecreasing. Fix the last two records and one
last-record time budget. The exact affine capture moment has, on the
\(m=n-2\) intermediate variables, Hessian

\[
 v^\top D^2\mathcal M\,v
 =-k\left(v_1^2+v_m^2+
          \sum_{j=1}^{m-1}(v_j+v_{j+1})^2\right)<0,
 \qquad k=c_+^{-1}+c_-^{-1}.
\]

Old captured rank bands change only constant and linear terms. For example,
the right-first old-band correction is

\[
 \frac{a_0^2}{2c_+}+\frac{b_0^2}{2c_-}
 +\frac{2\beta b_0}{c_+c_-}\,x_1.
\]

Stationary-wall constraints at record vertices and hold endpoints are
linear. The record-order chains, bounded levels, and one clock budget
form a compact finite polytope after adding these wall inequalities.
Duplicate levels and old-record equalities are nonproductive: constrained
earliest travel removes them, possibly revealing an earlier wall.

Take the minimum over the finite union of feasible itinerary polytopes
with at most the original productive-level count (and either first direction),
and choose a least-length minimizer. This makes the preceding deletion of
duplicate and nonproductive levels part of the minimization, rather than
an unproved strictness assumption.

At this minimizing representative, take the FIRST active stationary face
and freeze its time, position, BOTH captured prefix records, and all later
variables and history. If the contact is productive, its time fixes one
linear clock equality. If it lies on the final rank hold or nonproductive
connector, retain the old last-record point/time as one upper budget and
hold to that time. There is no second independent spatial budget after
the rank and time are fixed.

Every earlier stationary inequality is strict. More than three productive
levels would leave at least two intermediate variables and at most one
clock condition. After deleting duplicate levels, a nonzero two-sided
local variation preserves the strict inequalities. The negative Hessian
makes one side strictly improve the prefix moment, while the frozen
records and state leave later cost unchanged. This contradicts minimality.

Thus there are at most three productive unit legs, one nonproductive
constant-rank hold, and one nonproductive connector before the first wall,
or through the exit if no wall occurs. Unitize each nonproductive piece
by a legal extremal bridge. If that bridge hits a wall, stop at its first
contact; otherwise it has at most two unit legs. Therefore the prefix
count is at most

\[
 3+2+2=7.
\]

If the first wall is a physical endpoint, retain its closed atomic contact
and use the dominating endpoint sweep; no interface density is assigned
outside the arena.

The counted wall may be earlier than the old wall, or the opposite
stationary wall. That is permitted. It starts the next phase at an actual
frozen contact. The detailed availability, collision, and limiting
arguments are in AFFINE_FIRST_STATIONARY_CONTACT.md.

## 4. Local interface constants and unitization

At a stationary interface \(c\) in one time slab, continuity gives a common
time coefficient:

\[
 F(s+t,c+x)-F(s,c)=
 \begin{cases}
  \alpha t+\beta_-x,&x\le0,\\
  \alpha t+\beta_+x,&x\ge0,
 \end{cases}
 \qquad \beta_\pm\ge|\alpha|.
\]

For \(\alpha<0\), reflect spatial and rank directions and exchange the two
densities. It suffices to define the constants for \(\alpha\ge0\).

If \(\alpha>0\) and \(C=\beta_--\alpha>0\), set

\[
 \gamma=\frac{\beta_-}{C}+\frac12,\qquad
 \kappa=\frac{\alpha C}{17\alpha+C}.
\]

If \(\alpha=0\) and both densities are positive, use

\[
 \gamma=\frac32,\qquad
 \kappa=\frac{\min(\beta_-,\beta_+)}{17}.
\]

Call these the nondegenerate, two-front interface types. There are only
finitely many types in the arrangement. Let

\[
 \Gamma=\max\gamma,\qquad \kappa_{\min}=\min\kappa>0
\]

over those types. If there are none, the later quantity \(K\) is defined
as zero, and neither \(\Gamma\) nor \(\kappa_{\min}\) is divided by.

The proved local return-block and partial-excursion reductions apply with
arbitrary old captured records. In a common forward cone persisting to
time \(\gamma d\), they replace a prefix of duration \(d\), with its later
continuation fixed, by at most five return tents, three productive unit
legs, one rank hold, and one nonproductive connector. The all-wait return
block is an alternative, not an additional wait beside five tents.

A nonproductive hold or connector may be replaced by a two-leg unit bridge.
It loses no old capture, and extra captures only help. A pure interface
wait is dominated by a maximal right tent when \(\alpha\ge0\); the reflected
case is analogous. Consequently at most

\[
 10+3+2+2=17
\]

unit pieces suffice in the local source block. The cone chosen below
stays strictly inside the arena, so no endpoint wait is needed in this
unitization.

## 5. Quantitative captured-width gain

Let \(w\) be the final captured rank width of that local \(d\)-block.
The interval contains its source rank and every current rank.

First suppose \(\alpha>0\), \(C>0\). Whenever the path is on or right of
the interface at relative time \(t\),

\[
 F(s+t,m(s+t))-F(s,c)\ge\alpha t,
\]

and hence \(t\le w/\alpha\). If \(w\ge\alpha d\), then \(w\ge\kappa d\)
already. Otherwise the entire terminal time interval of length
\(d-w/\alpha\) lies strictly left of the interface.

At most seventeen unit pieces meet this terminal interval. On the left,
each unit piece has rank-speed magnitude at least \(C\). One piece
therefore changes rank by at least \(C(d-w/\alpha)/17\), and that change
cannot exceed \(w\). Rearranging gives

\[
 w\ge \frac C{17}\left(d-\frac w\alpha\right)
 \quad\Longrightarrow\quad w\ge\kappa d.
\]

This argument allows a zero rank speed on the right-hand unit direction.

For \(\alpha=0\) with both densities positive, rank changes monotonically
along every unit leg, even when it crosses the interface, at speed at
least \(\min(\beta_-,\beta_+)\). A longest unit leg gives the same conclusion
\(w\ge\kappa d\).

The estimate is immediate at the end of the local block. It does not wait
for another interface return, and is valid with arbitrary old records.

## 6. A source window uniform up to a coarse interval's end

Let \((s,c)\) be an interior stationary contact in a coarse interval
ending at \(e\). Put \(R=e-s>0\) and

\[
 h_*=\min\{\Delta/2,R/2\},\qquad d=h_*/\gamma.
\]

The time grid includes every active moving/stationary edge intersection.
An approaching characteristic line cannot meet \(c\) before the end of
the containing time slab, which is at least \(e\). Its distance from the
source is therefore at least \(R\), and it cannot enter the source's
forward cone before \(R/2\). A receding characteristic cannot enter that
cone at all. A line through the source lies on the cone boundary.
Other stationary positions and physical endpoints are at distance at
least \(\Delta\).

It follows that the full required two-half-cell cone persists through
\(h_*=\gamma d\). This is why stationary/moving intersection times must
be included in \(S\); profile vertices alone would not suffice.

The exact scale cancellation is

\[
 \frac R d=2\gamma\max\{R/\Delta,1\}
 \le 2\Gamma\max\{H/\Delta,1\}.
\]

Keep \(R\), rather than prematurely replacing it by \(H\), until this
cancellation is taken. The estimate remains uniform as \(s\) approaches
the coarse interval's end.

## 7. All remaining record episodes after a nondegenerate contact

After the local block, the captured width is at least \(\kappa d\).
Upper- and lower-record growth times have trace values separated by this
width. Since the trace is \(2M\)-Lipschitz before an endpoint contact,
opposite productive episodes are separated by at least
\(\kappa d/(2M)\).

Thus all remaining record-direction switches before \(e\), even across
other CDF cells and interfaces, are bounded by

\[
 \frac{2MR}{\kappa d}
 \le \frac{4M\Gamma}{\kappa_{\min}}
       \max\{H/\Delta,1\}.
\]

Set

\[
 K=\left\lceil
 \frac{4M\Gamma}{\kappa_{\min}}\max\{H/\Delta,1\}
 \right\rceil .
\]

There are at most \(K+2\) one-sign episodes, allowing an initial or terminal
nonproductive gap. This is a statement about the supports of the two
continuous record-variation measures, not an assumption of isolated
capture events.

For an upper-only episode, the pointwise maximal legal bridge

\[
 \min\{1,m(s)+t-s,m(e)+e-t\}
\]

catches every old newly caught upper rank no later. There is no old new
lower capture to lose. A lower-only episode uses the pointwise minimum.
Each bridge has at most three unit/waiting pieces. Extra captures help.
No cell-confinement hypothesis is needed for this replacement.

The episode partition is taken before these bridge replacements; it need
not remain the record partition afterward. Its piece count is already
fixed, and each replacement is independently dominating.

From the first physical endpoint contact, one unit sweep toward the other
endpoint dominates all remaining targets. Any zero-mass tail beyond \(H\)
can be truncated. Endpoint atoms therefore do not enter the interior
Lipschitz estimate.

## 8. Degenerate interfaces and chronological transfer charges

If \(\alpha>0\) and \(\beta_-=\alpha\), every legal path in the left cell
has nondecreasing rank, and every point in the right cell lies above the
source rank. No new lower record can be created before leaving these two
cells. If \(\alpha=0\) and one density vanishes, only the record toward the
nonflat side can grow. If both vanish, no record grows. The reflected
statements cover \(\alpha<0\).

Until the next DISTINCT stationary position or the coarse exit, the path
therefore has one record direction. A single extremal bridge compresses
that whole block. If this bridge reaches a different stationary position
earlier than the old block did, freeze its prefix at that first new contact
and restart there. The remaining bridge and old continuation remain an
actual legal suffix. A contact with the same stationary position does not
start a new charge.

Every frozen distinct-position transfer has time length at least
\(\Delta\). They are disjoint pieces of the single evolving chronological
path, so there are at most \(\lfloor H/\Delta\rfloor\) in total. This is
not a sum of contacts from unrelated deformations. A terminal degenerate
block with no transfer costs at most three pieces per coarse interval.

Once a nondegenerate contact occurs, Section 7 handles the entire remaining
coarse interval; no further stationary charging is needed there.

## 9. The explicit global count

One nondegenerate coarse interval needs at most:

- seven unit pieces through its first stationary contact;
- seventeen unit pieces for the local width-producing block;
- \(3(K+2)\) pieces for all later record episodes.

This is \(30+3K\). Characteristic boundary arcs and the alternative terminal
degenerate block fit within an additional five pieces; use the more
conservative allowance \(40+3K\). A coarse interval consisting of one
characteristic arc, or one affine prefix reaching its exit without a wall,
also fits this allowance.

Charge at most three pieces for each distinct degenerate stationary
transfer, and reserve two for endpoint completion or horizon truncation.
A valid uniform count is therefore

\[
 \boxed{\displaystyle
 N=(S+2E+1)(40+3K)
      +3\lfloor H/\Delta\rfloor+2 .}
\]

If no nondegenerate interface type occurs, use \(K=0\). All degenerate
passes are then handled by the seven-piece affine prefix and the
chronological one-front transfer construction.

Starting from the fixed finite optimizer, every replacement has no greater
cost and preserves all old final captured ranks. It is therefore still
optimal and completes by \(H\). Its resulting number of pieces is bounded
by \(N\), independently of the original finite optimizer's complexity.
This establishes the unrestricted fixed-law sufficiency assertion.

## 10. Exact implementation and verification

The helper effective_fan_response_bound.cjs computes the displayed
constants and integer bound from a supplied complete arrangement census.
It validates transport inequalities, interface density bounds, and
degenerate cases. It does not itself construct the fan arrangement:
completeness of the supplied census and validity of \(M\) remain explicit
inputs to the theorem.

The companion exact verifier checks:

- 2,176 local unit-path and old-band width inequalities;
- 680 degenerate one-front fixtures;
- 48,000 characteristic half-plane inequalities for independent extremal
  bridges;
- 1,920 exact window-ratio identities and 1,920 episode-bound comparisons;
- 2,114 distinct-position transfer charges;
- eight invalid-input rejections.

The full global theorem, first-face variational argument, and record-support
decomposition are analytic. These finite fixtures check their local
algebra and count arithmetic, not a sampled substitute for arbitrary paths.

## Dependencies

- FINITE_FAN_RESPONSE_EXISTENCE.md, proof blob
  1f70cba151b28b30de9305bb82216088005e5647:
  attainment, a finite optimal starting representative, and the fixed
  static-tail horizon.
- Static tail proof blob e78d8a40669357968709ce9a5c4be8c76237e1fa:
  productive turns at static density/atom boundaries and the multi-turn
  completion bound.
- AFFINE_FIRST_STATIONARY_CONTACT.md, proof blob
  305413236b794a074dd438b049061df7e59044a4:
  both-record freezing, the first-face clock constraint, availability,
  collision deletion, and seven-piece unitization.
- AFFINE_RECORD_PREFIX.md, proof blob
  25e05857eea4505d87730829b3ce455d5d77d265:
  the exact single-cell quadratic and negative Hessian.
- INITIAL_INTERFACE_RETURN_BLOCK.md, proof blob
  d10fa2df15cb767f11fb5cb4b92cf990e3a046ce:
  the at-most-five-tent block, including arbitrary old records.
- AFFINE_HALF_CELL_BRIDGE.md, corrected proof blob
  a7f977451db98b0b00bdd4e5b3f1f4fd3974cf3a:
  the fifteen-affine-piece local source theorem and center-source handling.
- AFFINE_INTERFACE_EXCURSION.md, proof blob
  2ad880d9ab22b8b96217f29410c02c82bfbcb628:
  arbitrary-left normalization and its precise future persistence gate.

The earlier FAN_INTERFACE_EPOCH_BOUND.md deliberately left a global
charging gate open. Sections 2, 3, 5, and 8 above supply the characteristic
confinement, first stationary contact, immediate width, and chronological
transfer steps needed to close that gate for a fixed ordinary fan.
