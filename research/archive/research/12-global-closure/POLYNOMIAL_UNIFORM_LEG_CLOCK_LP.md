# Polynomial grid LP with exact vertex and uniform-leg clocks

Research proof, 2026-11-13.

The polynomial clock-grid construction can include continuous selected
mass on each physical grid leg without increasing its asymptotic size.
The resulting rational LP has \(O(n^4)\) states, arcs, and variables
and computes the **exact unrestricted Princess-response minimax value
on the finite physical grid-path bank**.

This is an equivalent refinement of the vertex-clock model. The common
left-floor theorem in LEFT_FLOOR_CLOCK_ATOMIZATION.md shows that its
value is exactly the vertex-clock value. Both models still restrict
the Monster's physical paths; neither asserts that a finite grid is
sufficient for the unrestricted game.

Write \(h=1/n\), \(\Delta=h/2\), and \(N=16n\). Let
\(\widehat U_n\) denote the new value and \(U_n\) the previously defined
vertex-clock value. Then

\[
 \boxed{
 V\le\widehat U_n=U_n\le V+\frac1{2n}.}                       \tag{1}
\]

In particular \(\widehat U_n-1/(2n)\le V\le\widehat U_n\).
The refinement cannot improve the exact objective value. It supplies
an alternative physical realization and exact pricing oracle, with
no stronger uniform error constant asserted here.

The construction uses the proved
FINITE_BANK_CLOCK_HOMOGENIZATION.md; equality with the vertex model
additionally follows from LEFT_FLOOR_CLOCK_ATOMIZATION.md. The new work is the integral
calendar decomposition, its polynomial planning-state realization,
and the exact two-record pricing rule.

## 1. Physical bank and exact clock templates

The physical bank is unchanged. Its paths start at
\(x\in\{-1,-1+h,\ldots,1\}\), use unit-speed moves of duration
\(\Delta\), visit zero by time \(2\), and complete both endpoints by
time \(8\). Reflection is included. Paths can stop being scored as
soon as both endpoints have been visited.

For each oriented active clock, allow selected mass at the vertices
strictly before its first active endpoint and selected mass uniformly
distributed on each open physical leg before that endpoint. There
are no positive-duration stationary physical legs.

These templates are exact for the full clock-and-matching minimax
on this bank. To recall why, fix every common light-coordinate knot
and send each whole intervening open band to one uniformly selected
interior point. Apply the same nondecreasing map to:

* the selected and scoring events of each clock on each physical path;
* both ends of every pressure-matching pair.

A unit-speed grid leg has one fixed light coordinate and one free
coordinate in one such band. Every transformed event therefore remains
on the identical physical path and leg. Coordinatewise order preserves
selected-before-scoring causality. Averaging the transformed scoring
measure restores exactly physical Lebesgue time on each leg.
Selected marginal mass becomes uniform on each open leg; vertex
atoms stay fixed. The same map preserves interval containment,
selected-event signs, active lifetimes, and matching mass.

This is a statement about the joint minimax/matching certificate. It
does not assert that a fixed Princess field's minimizing clock is
uniform on a whole leg. A fixed field may have an interior record
crossing; the common transformation changes its selected/scoring
kernel while preserving the all-Princess matching certificate.

By the existing fixed-bank strong record duality, minimizing the
resulting clock-and-matching objective is exactly the bank's
unrestricted Princess-response minimax. Princess attainment is not
needed.

## 2. Exact causal inequalities for one calendar

Fix a physical path and an active endpoint at grid index \(k\).
Divide all selected masses by \(\Delta\). Let

\[
 a_j\ge0,\qquad b_j\ge0\qquad(0\le j<k)
\]

be the node mass at time \(j\Delta\) and the uniform mass on
\((j\Delta,(j+1)\Delta)\), respectively.

Define the cumulative masses immediately after the node atom and
after the open leg by

\[
 A_j=\sum_{i<j}(a_i+b_i)+a_j,\qquad B_j=A_j+b_j.
\]

Causality and exact active mass are equivalent to

\[
 B_j\ge j+1\quad(0\le j<k),\qquad B_{k-1}=k.                 \tag{2}
\]

Indeed \(A_j\ge B_{j-1}\ge j\), with the usual empty prefix at
\(j=0\). During leg \(j\), at fractional progress \(0\le s\le1\),
the physical credit in units of \(\Delta\) is

\[
 (1-s)(A_j-j)+s(B_j-j-1).                                  \tag{3}
\]

It is nonnegative if and only if the endpoint credits are
nonnegative. Node atoms only increase credit. The final equality
excludes selected mass at the active endpoint.

For \(k=0\), the unique calendar is empty and the clock is inactive
from the start.

## 3. Integral calendars preserve both selected marginals

Apply one common stochastic rounding to all the ordered cumulative
values

\[
 0,\ A_0,\ B_0,\ A_1,\ B_1,\ldots,A_{k-1},B_{k-1}=k.
\]

For \(Z\) uniform on \([0,1)\), replace each cumulative value \(C\) by
\(\lfloor C+Z\rfloor\). Monotonicity, every integer lower bound in
(2), and the final value \(k\) are preserved. Taking differences
gives nonnegative integer masses \(a'_j,b'_j\). Their expectations
are \(a_j,b_j\), respectively.

Only finitely many fractional-part thresholds occur, so this is a
finite mixture of integral calendars. It preserves every node atom
and every uniform-leg mass, not just the total mass.

Apply the decomposition independently to the two active clocks,
conditional on the same physical path. This preserves their joint
physical support and both aggregate selected-event marginals.
Consequently it preserves any matching built from those marginals.
No symmetry shortcut is being used to decouple physical trajectories.

## 4. Polynomial planning-state graph

An ordinary state is

\[
 (j,k,q_-,q_+,e_-,e_+,c),
\]

where \(t=j\Delta\), \(x=k\Delta\), \(0\le j\le N\),
\(|k|\le2n\), and \(j\equiv k\pmod2\). The endpoint flags indicate
whether the two active clocks have been deactivated, and \(c\)
records whether zero has been visited. An inactive queue is zero.
An alive queue is an integer between zero and \(N-j\).

Initialize the endpoint and center flags at time zero. Initial
positions have even physical index \(k\). Exclude uncentered states
at or after time \(2\). A state with both endpoints visited is
terminal. These are the same physical conditions as in the original
polynomial grid LP.

There are also two *planning copies* of each nonterminal ordinary
state, labeled by the next legal physical direction \(d\in\{-1,1\}\).

The arcs are as follows.

1. **Ordinary node charge.** Increase an alive queue by one and emit
   one unit of selected mass at the present physical vertex (or its
   reflected vertex for the other clock).

2. **Choose the next direction.** Move from the ordinary state to
   the planning copy for a legal adjacent physical leg. This emits
   no mass and changes no queue.

3. **Uniform-leg charge in a planning copy.** Increase an alive
   queue by one and emit one unit of selected mass uniformly on
   the chosen open physical leg (or its reflection for the other
   clock).

4. **Execute the planned move.** This is the only way to leave
   a planning copy. Require every alive planned queue to be at
   least one, consume one from each, and move to
   \((j+1,k+d)\). Update the center and endpoint flags there.
   If an endpoint is reached for the first time, its corresponding
   post-move queue must be exactly zero before deactivation.

There is no arc back from planning to ordinary at the same physical
time and no arc that changes the selected direction. All charges
stay within \(q_\pm\le N-j\).

### Why the planning credit is physically legitimate

The credit accumulated during planning is virtual bookkeeping.
It is not claimed that selected mass from the open future leg has
already appeared at its left endpoint.

For a decomposed graph path, let \(q_0\) be the real credit after
ordinary node charges and before entering planning. If \(b\)
planning charge units are selected for one clock, its post-move
credit is \(q_1=q_0+b-1\). Both are nonnegative by the state bounds
and move guard. The actual selected measure is uniform on the leg,
so its real intermediate credit is

\[
 q(s)=(1-s)q_0+s q_1,\qquad 0\le s\le1.
\]

Thus it is causal throughout. It is also bounded by the remaining
time: this upper bound holds at both endpoints and is affine.
No memory of \(q_0\) is needed in the graph state; each flow
decomposition determines it along its own planning segment.

Conversely every integral atom/uniform calendar follows exactly these
arcs: make the prescribed node charges, choose the prescribed
physical direction, make the prescribed uniform charges, and move.
The cumulative constraints give all guards, including zero credit at
first endpoint arrival.

### Acyclicity and size

Let the phase be zero in ordinary states and one in planning states.
The integer rank

\[
 {\cal R}=4j+q_-+q_++\mathrm{phase}
\]

strictly increases on every arc. A charge increases it by one;
choosing a direction increases it by one; a physical move increases
it by \(3-\#\{\text{alive clocks}\}\ge1\).
Therefore the graph is a DAG.

It has \(O(n^4)\) states. The endpoint/center flags and the three
phases contribute only constant factors. Every state has a constant
number of outgoing arc types, so there are \(O(n^4)\) arcs as well.
This avoids enumerating all possible pairs of uniform densities as
separate physical-move arcs.

## 5. Exact finite matching of atom and open-leg types

Each selected-event type is either a physical node or a uniform
open unit leg. There are \(O(n^2)\) types. Open unit legs have a
constant nonzero spatial sign; center events are nodes.

Number each light-grid knot \(ih\) by \(2i\), and its following
open band by \(2i+1\). Represent a radial interval by the two
indices of its endpoints. A node has two even indices; an open
leg has one even index and one odd index.

A positive type and a negative type can be matched precisely when
their index intervals satisfy containment. Equivalently, their
physical midpoint representatives satisfy the causal cone
inequality. The midpoints are type indices, not point-mass
approximations.

For necessity, apply the deterministic common midpoint collapse to
any feasible pair of events. It preserves the order inequalities.
For sufficiency, use a shared uniform quantile \(0<\alpha<1\):
send every even index \(2i\) to \(ih\) and every odd index \(2i+1\)
to \(h(i+\alpha)\). This is nondecreasing in the index for every
\(\alpha\). Every indexed containment remains an actual interval
containment, and averaging \(\alpha\) gives exactly the uniform
marginal on each open leg.

Splitting each type proportionally among its finite matching edges
therefore realizes every feasible finite matching flow as an actual
continuous coupling. Same-band equality is handled by the common
quantile; independent uniforms would not suffice there.

Use a nonnegative matching variable for each feasible positive/
negative type pair, with source and target capacities equal to the
aggregate emitted type masses. There are \(O(n^4)\) such variables.
Alternatively, the expanding-interval order network from the
finite-bank homogenization theorem has only \(O(n^2)\) internal
order nodes and arcs; its capacities are linear in the emitted
type masses.

## 6. Objective and exact equivalence

A unit source-to-terminal flow on the planning graph decomposes into
physical paths with two integral calendars. Fair-reflect each such
path. A node or uniform charge arc carrying flow \(f\) contributes
physical selected mass \(\Delta f/2\) of its specified type.

Thus, with \(c_z\) denoting emitted type counts and matching counts
\(\gamma\), the objective is

\[
 \frac{\Delta}{2}\left[
  \sum_{\text{all charge arcs}}f
  +\sum_{\text{positive types }z}c_z
  -\sum_{\text{matching edges}}\gamma
 \right].                                                 \tag{4}
\]

The first term is the active endpoint baseline
\(\tfrac12\mathbb E(\tau_-+\tau_+)\). Every feasible point gives
actual physical paths, causal clocks, and a continuous matching,
so (4) is an unrestricted upper certificate.

Conversely, fixed-bank homogenization and Section 3 map every
fixed-bank clock-and-matching certificate to a flow in this graph
with exactly the same atom/leg type masses and objective. Section 3
preserves the homogenized selected marginals as well.
Consequently the LP value \(\widehat U_n\) is exactly

\[
 \min_{\nu\text{ on the finite grid physical bank}}
 \sup_{p\text{ legal}}\mathbb E_\nu T(M,p).
\]

The variables and all coefficients are rational. The finite feasible
polytope is bounded, and a rational optimal solution exists.
Flow decomposition gives a finite rational Monster law. The physical
common-trajectory condition is enforced by every graph path and is
preserved when the unit flow is mixed.

Setting all planning charge flows to zero recovers the old
vertex-clock model, giving \(\widehat U_n\le U_n\).
Conversely, the common left-floor theorem moves every selected
uniform-leg event to its chronological left vertex without changing
physical paths or scoring time and without increasing deficiency.
It gives \(U_n\le\widehat U_n\), hence equality. The remaining
inequalities in (1) follow from physical validity and the already
proved common-quantization approximation bound.

## 7. Exact two-record pricing with current uniform items

There is a useful dual pricing simplification. Fix a physical grid
path and assign an arbitrary scalar price to every node type and
uniform-leg type. For one active clock ending at step \(k\), let
the two items available at index \(j\) be:

* its node atom at \(j\);
* its uniform open leg from \(j\) to \(j+1\).

One unit of either item can serve any scoring interval \(i\ge j\).
For the current uniform item \(i=j\), couple selected time and
scoring time identically. For an earlier leg \(j<i\), every selected
time is earlier than every scoring time in interval \(i\).

The prefix constraints (2) are precisely the finite triangular
transport conditions for assigning the item masses to the \(k\)
scoring rows, each of mass one. A greedy assignment or the
one-dimensional Hall criterion gives such a transport. Conversely
every such assignment is causal. Fractional assignment to a current
uniform item uses the same fractional identity coupling; all remaining
row mass can be assigned to its earlier items.

It follows that the exact clock price for this physical path is

\[
 \sum_{j=0}^{k-1}
 \min\{\text{prices of all node and uniform-leg items of indices }
          0,\ldots,j\}.                                   \tag{5}
\]

In particular the current leg's uniform item is included before its
scoring interval is charged. A current-leg unit is feasible from
zero initial credit; it pays for its own interval causally.

The two clocks minimize independently conditional on the same physical
path. Therefore a full physical record DP remains valid: update
each alive record with the current node price and the proposed leg's
uniform price, charge that step using the updated records, then
perform the endpoint/center guard updates. Do not emit the newly
reached active endpoint as a node item for its deactivated clock.

This record formulation is an exact alternate dual pricing oracle.
It makes no assertion about a fixed arbitrary field's partial-leg
record crossings; the prices here belong to the finite homogenized
minimax model.

## 8. Constructive Princess extraction from this equivalent dual

The finite matching dual again admits one radial isotone profile,
now on both node and open-leg interval types. Let an optimal such
profile have objective \(\widehat U_n\), together with its exact
physical pricing certificate.

Restrict the profile to node types. Every feasible vertex-clock law
is also feasible in the new model, so its nodal plane against this
restricted profile is at least \(\widehat U_n\). This is precisely
the nodal minimax inequality needed by
CONSTRUCTIVE_PRINCESS_GRID_DUAL.md. Its common one-parameter
rounding construction, positive smoothing width, endpoint stopping,
and outward-after-two normalization therefore apply without change.

For every rational \(0<\varepsilon\le1/2\), the resulting explicit
legal Princess law has security at least

\[
 \boxed{\widehat U_n-\frac1{2n}-\frac{\varepsilon}{2n}.}
\]

The open-leg profile values can be ignored for this conservative
extraction; only the valid nodal lower inequality is used. More
generally, any rational feasible uniform-leg dual with objective
\(c\) gives the same construction with \(c\) replacing
\(\widehat U_n\). Exact optimality is unnecessary if a primal/dual
gap is retained in the final two-sided certificate.

## 9. What a zero-gap result would still require

The construction permits uniform-leg clocks, while the left-floor
theorem proves that they do not improve the finite-bank optimum.
It does not remove the finite physical-path restriction or imply
\(\widehat U_n=V\) at any finite \(n\).

For a true exact solution one would still need, for example, a legal
Princess field whose unrestricted response lower certificate equals
a feasible physical upper certificate. A finite exact continuous
potential, or the previously proved finite fixed-field response
quadratic-program enumeration, can supply a sufficient lower
verification. The planning graph itself supplies the upper side.

An optimal matching/flow dual on this graph is not automatically a
continuous global lower certificate. Its constraints price the finite
physical bank. Any claim of zero transfer loss must separately check
the physical interpolation, endpoint traces, and continuous control
inequalities.
