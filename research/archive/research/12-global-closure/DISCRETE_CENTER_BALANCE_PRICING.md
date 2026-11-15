# Exact center phases for normalized integer record pricing

This is an exact restriction of the **complete normalized physical lattice
bank**, for a supplied feasible `Qout` profile. It is not a beam search,
turn-budget approximation, or new continuum transfer estimate. It permits
the existing unrestricted lower transfer after the bank minimum has been
proved with this restriction.

The implementation must retain the original unrestricted precenter phase,
actual endpoint clocks, and both legal time-two endpoint tours. Distinct
outward and inward phases must have distinct Pareto frontiers. The last
section proves the additional value-function fact needed to retain ordinary
componentwise record dominance when the balance guard is enabled.

## 1. Record and charging conventions

Put

\[
 \Delta=\frac1{2n},\qquad R=2n,\qquad C=4n.
\]

Physical grid nodes are `(j Delta,k Delta)`, with matching parity. Write
`f(j,k)` for the signed interior nodal CDF. At a nonendpoint node the
two surviving records are first updated by

\[
 L\leftarrow\min(L,f(j,k)),\qquad
 R_s\leftarrow\min(R_s,1-f(j,k)),
\]

then `Delta*(L+R_s)` is charged for the next step. At its own first
endpoint a side stops charging immediately. The endpoint's interior trace
is not substituted for that actual stopping rule.

After a center update, both records are at most `1/2`. While the path is
on the positive side, its left record stays constant. Along an outward
positive ray, the right sample `1-f` is nonincreasing; along the return
ray it is nondecreasing. These follow directly from the nodal transport
inequalities. Reflection gives the negative-side statements.

The conditional center value includes every future lattice path, followed
by the usual first-endpoint/time-two normalization. The finite normalized
bank attains this minimum. The assertions below also apply to arbitrary
incoming center records in `[0,1/2]^2`.

## 2. Exact discrete triangle cost

Consider a positive returning center triangle starting at node time `j`,
with integer height `1<=h<R`. Let `l` be the opposite record, `r` the
attacked record, and put

\[
 S_a=1-f(j+a,a),\qquad
 q=\min(r,S_h),\qquad
 I_h(r)=\sum_{a=0}^{h-1}\min(r,S_a).
\]

Its exact left-clock cost is

\[
                \Delta\bigl(2hl+I_h(r)+hq\bigr).          \tag{1}
\]

The outbound sum stops at `h-1`. The peak node is updated before the
first returning step and is therefore included in the `h*q` term.
The return-center node belongs to the continuation and is not charged
twice. This is the required off-by-one convention.

At `h=R`, an actual endpoint has been reached. Formula (1) must not be
used with an interior-trace peak record. The direct endpoint tour instead
has exact cost

\[
                    \Delta\bigl(3Rl+I_R(r)\bigr).          \tag{2}
\]

The opposite record stays constant until the opposite endpoint: the
tour crosses the center on its sweep at absolute time at least two,
when outward forcing prevents any interior capture of those survivors.

## 3. Triangles, heavier-first, and balance

A one-sided center-to-center lattice segment of duration `2h` is
pointwise no farther outward than its maximal unit-speed triangle.
When `h<R`, replacing it by that triangle decreases its affected
running record at every charged node and leaves the opposite record
unchanged. Every common physical continuation remains valid.

When `h>=R`, replace the segment and its future by the direct tour
toward that side. This is a legal tour, not an out-of-arena tent.
The same-side survivors are caught no later by immediate outward
travel. The old path cannot depart toward the opposite side until
absolute time at least two; its opposite survivors then cannot be
caught before an endpoint arrival at least three units after this
starting center. The direct tour reaches that endpoint in three units.
The comparison holds node by node with the actual endpoint stopping.

Thus a best center continuation consists of returning triangles and
one final direct tour. The same argument replaces a final one-sided
center-to-first-endpoint prefix by its direct tour.

For `l<=r`, compare triangles of the same height attacking the heavier
and lighter records. Let `p=min(l,S_h)` and `q=min(r,S_h)`. Then

\[
 I_h(r)-I_h(l)\le h(r-l),\qquad q-p\le r-l,
\]

so (1) is no greater for the heavier-first choice. Moreover,

\[
                 \operatorname{sort}(l,q)
                    =(p,\max(l,q))\le(p,r).                \tag{3}
\]

For a fixed physical continuation, the record cost is nondecreasing
in both incoming records. Either that continuation or its reflection
therefore costs no more from the heavier-first exit state. This uses
the actual old continuation and preserves its triangle count.
For the final tour, (2) gives

\[
                    D_r-D_l\le-2R\Delta(r-l).              \tag{4}
\]

Choose an optimal center continuation with the fewest triangles and
apply these orientation exchanges chronologically. It remains optimal
with the same minimum count. Consecutive same-side triangles merge by
the preceding pointwise argument; if their combined height is at
least `R`, use the direct tour. A final triangle followed by a tour
toward the same side is likewise removed. Minimum count therefore
forces alternating outward directions, including the final tour.

At every return, the opposite side is consequently the next heavier
side. Thus a returned triangle can be required to satisfy

\[
                         q\le l.                          \tag{5}
\]

The current peak-node update must be applied before testing (5).
Equal records permit both directions. No such guard is applied before
the first genuine center visit.

## 4. The operational phase restriction and time-two boundary

Use the following state phases before the existing terminal boundary:

* **Precenter:** retain both unit directions without the new restrictions.
* **Center:** after capping both records at `1/2`, start toward a heavier
  side; permit either direction on a tie.
* **Outward:** continue away from the last center, or turn inward.
  With the balance policy enabled, the latter requires (5).
* **Inward:** continue toward the center without another turn.

The phase changes only restrict the pre-time-two prefix. Retain both
original legal endpoint-tour choices at time two, as well as the direct
opposite sweep after an earlier endpoint. Such retained tails are actual
bank paths, so allowing both cannot introduce an inadmissible low value.

A normal-form continuation crossing time two remains representable.
On an outward ray its affected record is constant after time two,
by the Qout identity. A prospective peak later than two can be
shortened to time two without changing that record. Its continuation
after the return uses the time-independent endpoint-only center value.
Alternatively, apply the original time-two endpoint-tour normalization
directly. Both operations retain a legal normalized bank path and do
not increase its clock cost. Endpoint-time and parity boundaries are
integer grid boundaries, so no rounded duration is introduced.

Every original bank path is dominated by a path in the stated phase
class. Conversely every retained phase path and tail is in the original
bank. Therefore the complete minimum is unchanged, including free
initial positions, endpoint starts, and the original late-center rule.

## 5. Why phase-separated full Pareto dominance is valid

There is a genuine trap here. Componentwise smaller records alone do
not preserve an individual balance-guarded path. For example,
`A_l<=B_l`, `A_r<=B_r` can hold while `B_r<=B_l` but `A_r>A_l`.
A return permitted for B is then forbidden for A. Merely grouping by
the current balance comparison does not repair this: the comparison
can change after further outward capture.

The repair is an exact conditional-value lemma, not a claim that
the same guarded continuation remains available.

### Outward-phase value lemma

Fix an outward state `(t,x)` after a center visit. Its last-center time
is fixed by its geometry: `t-|x|>=0`. Initially ignore the balance guard:
allow any further outward peak, then the fixed unit return, then the
exact center value `Q`; also allow the direct tour toward the current
side. This unguarded phase value is nondecreasing in both records,
since every fixed prefix has monotone cost and outgoing records and
`Q` is monotone.

Suppose an unguarded first return has attacked record `q>l`. At that
center, an optimal continuation starts toward the **same** side,
by the heavier-first result. If it starts with a triangle, its next
return has affected record at most `l`, by (5). Merge the original
triangle from the last center with this next same-side triangle.
The enlarged maximal triangle agrees with the entire old outward
ray through the current state: its new peak is no earlier than the
old peak, and the current state lies before that old peak. Thus the
replacement does not change the fixed past. Its remaining path is
pointwise farther outward, and its return record is at most the next
triangle's old record, hence at most `l`. Its first return is now
balanced. One merge suffices; no repeated reoptimization is needed.

If the enlarged height reaches an endpoint, or if the center
continuation starts with a same-side final tour, use the direct tour
from that last center. It too agrees with the past through the
current outward state and dominates the remaining cost.

Hence the guarded and unguarded outward-phase values are identical.
The guarded value is therefore nondecreasing in both records.

If an attempted unbalanced return encounters the time-two cutoff
before reaching the center, the same argument applies to its legal
tail. A tail that first goes to the old side remains in a one-sided
prefix and is dominated by the immediate old-side tour. A tail that
first goes to the opposite side passes through a center with `q>l`;
there its opposite-first order is dominated by the heavier old-side
order, and the resulting one-sided prefix collapses to that same
direct tour. Thus keeping both time-two tours does not invalidate
the phase-value lemma.

### Other phases

The inward phase has a fixed return to the center followed by `Q`,
or reaches the time-two boundary first. Both the center value and
the retained tail minimum are record-monotone. The precenter phase
uses unrestricted physical prefixes followed by those same monotone
boundary values. At the center, heavier-first restriction preserves
the full value `Q`, which is monotone by its original all-path
definition.

Consequently, at the same time, position, and phase, a state with
componentwise no larger records and no larger accumulated cost
dominates another state in value. Standard full two-record Pareto
pruning is sound **within each phase**. Inward and outward states
must not share a frontier. The implementation should not justify
this rule by the false individual-path argument at the start of
this section.

## 6. Collapsing a deterministic return

After the allowed inward turn, no further choice remains before the
center or the time-two boundary. Moreover, the **updated** records are
constant throughout this inward segment. On the positive side the
affected right sample is nondecreasing along the unit inward ray, so
its running minimum stays at its peak value. The opposite left sample
is at least `1/2`, whereas its record is already at most `1/2` after
the previous center visit. Reflection proves the other case. This
argument applies from an interior peak as well as from an already
inward state; it does not apply before the first center visit.

At an interior node `(j,k)` after updating its records to `(l,r)`, put

\[
 d=\min(|k|,C-j),\qquad
 j'=j+d,\qquad k'=k-d\operatorname{sign}(k).
\]

Every allowed return has the exact same successor records `(l,r)`
and charges exactly

\[
                         d\Delta(l+r).                    \tag{6}
\]

There are `d` charged nodes, starting with the present peak/inward
node and ending just before the destination. If `j'<C`, then
`k'=0`; schedule the resulting state directly into that later center
layer. The center update does not reduce either record, and its
outgoing charge belongs to the subsequent decision. If `j'=C`,
retain the same two original legal endpoint tails at `(C,k')`.
This includes the equality case of reaching the center exactly at
time two. No endpoint is crossed by the collapsed inward segment.

This substitution is an exact evaluation of a deterministic subpath,
not an additional pruning rule. It preserves the minimum under any
of the established balance policies that already force straight
returns. Destination states can use the same phase-separated Pareto
test. A minimum-only implementation may omit the intermediate history;
a witness-producing implementation must expand the `d` unit steps
when reconstructing a path.

## 7. Earlier grid-aligned incoming fronts

`GLOBAL_INCOMING_FRONT_COMPLETION.md` proves the globally sufficient
incoming-front restriction and its exact nodal monotonicity for front
two. The following discrete extension permits an earlier aligned front,
while accounting explicitly for the previously retained late-center
paths.

Choose `1<=c<=2` with `n*c` an integer, and write `J=2*n*c`. Thus
`J` is an even physical-grid time index. In radial light coordinates set

\[
 (\Gamma_c g)(U,W)=
 \begin{cases}
   g(\min(U,c),W),&W<c,\\
   0,&W\ge c.
 \end{cases}                                             \tag{7}
\]

Every projected query is a legal lattice node. For a changed node,
`W>=U-2>c-2` guarantees radius at most one at `U=c`, while `c>=1`
guarantees nonnegative time. The projection preserves both transport
orders, center value zero, and endpoint stopping. It gives outward
motion after `c`, hence also the existing outward-after-two condition.
At node indices it uses

\[
 j'=(J+j-k)/2,\qquad k'=(J-j+k)/2
\]

when `j+k>J` and `j-k<J`; otherwise retain the old node or set it
to zero according to (7). Alignment makes both new indices integral
with the required matching parity.

Let `v(g)` be the complete normalized-bank minimum in capture-time
units, still allowing all original center-by-two paths. Then

\[
 \boxed{v(\Gamma_c g)\ge
              \min\{v(g),(c+1)/2\}.}                     \tag{8}
\]

For a path whose first center visit is by `c`, every precenter node has
`t+|x|<=c` and is unchanged. Changed nodes are postcenter. There each
record has already seen the center price `D`: decreasing the radial
field raises the own-side price and leaves the opposite price at least
`D`. Thus neither optimal running clock improves under projection.
The path's endpoint resets occur at exactly the same nodes, and its
total price cannot decrease.

For a path whose first center visit is later than `c`, reflect so that
its node at time `J` has position `k_J>0`. The negative endpoint clock
has stayed at least `D` before that visit. After the first center, the
negative-side light coordinate `W=t-|x|` is already greater than `c`
and is nondecreasing until any subsequent crossing. Formula (7) gives
radial value zero there, so this clock cannot decrease below `D` in
the interior. On the positive side its price is again at least `D`.
Only the actual first negative-endpoint visit deactivates it. That
visit cannot occur before node `J+R+k_J`, so this one active clock
already costs at least

\[
 \frac{D(J+R+k_J)}{2RD}
       =\frac{c+1}{2}+\frac{k_J}{2R}
       >\frac{c+1}{2}.                                  \tag{9}
\]

The charge count starts at time zero and ends just before the endpoint
reset; no endpoint interior trace or fractional time rounding appears.
Combining the two path classes proves (8).

This also supplies a conditional exact search guard. At a precenter
state with `j+|k|>J`, no continuation can visit the center by `c`.
If an attained incumbent has raw integer cost at most `D*(J+R)`, all
such states can be discarded. The equality case `j+|k|=J` remains:
it can reach the center exactly at `c`. A source bank lower `b` is
preserved by projection whenever `b<=(c+1)/2`; a reused proof must bind
the original certified field and the exact projection, rather than
attaching its old replay to different input bytes.

For example, `c=474/256=237/128` is aligned on the retained `n=256`
grid and has floor `(c+1)/2=365/256=1.42578125`. This is a valid earlier
search front for any attained incumbent at most that floor. It is also
above `2U-1` for the currently certified unrestricted upper, so the
global Princess-class sufficiency theorem applies at this rational
front. These are mathematical permissions for an exact search, not a
claim that a new search has been run.

## 8. Verification scope

An implementation should compare the unrestricted native minimum
with each intermediate policy on exact small fixtures, including
endpoint starts, record ties, time-two exits and opposite surviving
records equal to zero. The retained large field is a further exact
regression target. These comparisons test implementation; the
universal bank equivalence and Pareto justification are the proofs
above. The continuum lower remains the existing transfer applied
to the resulting exact bank minimum.
