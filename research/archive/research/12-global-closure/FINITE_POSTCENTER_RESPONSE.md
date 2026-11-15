# A finite response after the first center visit

This theorem gives an explicit finite bound for the part of a Monster
response **after its first visit to the center**. For a full-width common
threshold Princess field on light mesh \(1/n\), the bound is

\[
                         \boxed{8n+4}
\]

unit-speed physical legs. A positive narrow threshold width gives the
bound \(24n+4\). The initial portion before the first center visit is not
bounded by this result.

The proof uses the established two-run affine-cell theorem with the
entire fixed later continuation included. That theorem may change the
two exit records. We therefore make the finitely many replacements
backwards in time. We do not apply its record-preserving four-leg
variant and then silently count only two legs.

## 1. Assumptions and the general band theorem

Let \(F(t,x)\) be the signed interior CDF of a symmetric ordered
Princess law on \([-1,1]\). Assume:

* \(F\) is continuous up to its interior endpoint traces, and
  \(F(t,0)=1/2\).
* Princess paths stop at their first endpoint and move maximally
  outward after time \(2\).
* There is a partition
  \[
                0=a_0<a_1<\cdots<a_m=2
  \]
  with \(a_{i+1}-a_i\le1\), such that on each central light square
  \[
                a_i\le U,W\le a_{i+1},
  \qquad U=t+x,\quad W=t-x,
  \]
  the field has the stationary affine form
  \[
        F(t,x)=\frac12+\beta_i(U-W),\qquad \beta_i\ge0.       \tag{1.1}
  \]

The light squares lie strictly inside the arena: their maximal
\(|x|\) is at most \(1/2\). There is therefore no physical-endpoint
clipping issue in the local affine replacement.

**Theorem.** For every center state
\[
          (t_0,L_0,R_0),\qquad
          0\le t_0\le2,\quad 0\le L_0,R_0\le\frac12,
\]
and every admissible continuation, there is a continuation of no
greater remaining capture cost which:

1. completes both endpoints by time \(6\);
2. after that center state has at most \(4m+4\) physical legs, each of
   velocity \(+1\) or \(-1\);
3. consists of returning center triangles followed by one direct
   two-endpoint tour.

Zero-duration legs may be deleted, and adjacent equal-velocity legs
may be merged. The assertion remains true for original continuations
with infinitely many turns, infinitely many center excursions, or a
center zero set of positive measure.

Here \(L\) and \(R\) are the two surviving rank masses. Before endpoint
capture their updates are the running minima of \(F\) and \(1-F\);
the appropriate record is reset to zero at an actual endpoint.

For the unrestricted fixed-field response, the existing outward-after-
two reduction allows a best response to visit the center by time \(2\).
Indeed, a route which has not visited it by then pays more than
\(3/2\) on the opposite fair half alone, whereas a direct endpoint sweep
has total cost at most \(3/2\). The theorem consequently supplies the
same \(4m+4\) bound after the first center of a best response.

If an endpoint was visited before that first center, the already
normalized opposite sweep has only one remaining physical leg, so this
case is immediate.

## 2. Fixed future paths give concave record continuations

Fix a physical continuation from a given time and position, completed
within a finite horizon. For each later time \(s\), let \(A(s),B(s)\)
be the left and right record bounds imposed by that future path alone,
including its actual endpoint resets.

Its remaining cost as a function of the incoming records is

\[
 H(L,R)=\int
       \left(\min\{L,A(s)\}+\min\{R,B(s)\}\right)\,ds.         \tag{2.1}
\]

This function is finite, continuous, jointly concave, and
nondecreasing in each variable. The concavity follows term by term
from the minimum of a variable and a constant. Endpoint jumps merely
make one of the future bounds zero and cause no exception.

The two-run theorem in
**TWO_RUN_AFFINE_CELL_WITH_CONTINUATION.md** applies to an affine field
on the coordinatewise box between fixed entry and exit points, when
this whole future cost is included. Its scalar record variables
measure captured rather than surviving ranks; changing conventions
turns the nondecreasing concavity in (2.1) into exactly the
nonincreasing concavity used there.

In particular, if both entry and exit are at the center, at times
\(s\le t\), its two pure light-coordinate orders are

\[
 \begin{array}{ll}
 \text{positive triangle:}&
       m(s+u)=\min\{u,t-s-u\},\\[2mm]
 \text{negative triangle:}&
       m(s+u)=-\min\{u,t-s-u\},
 \end{array}
 \qquad 0\le u\le t-s.                                    \tag{2.2}
\]

At least one has no greater cost on this interval plus the fixed
future path. Both preserve the physical exit time and position, but
they need not preserve the exit records.

If the affine slope is zero, neither record changes in the square.
Either triangle then has the same local and future cost; no division
by the field slope is needed.

## 3. Normalize the horizon and the final tour

Once the first endpoint has been reached, direct motion to the other
endpoint weakly dominates every other continuation. At time \(2\),
all uncaptured Princess paths move outward at speed one until their
endpoint. From the Monster's current position they cannot be caught
in the interior. Therefore the remaining cost depends only on the
times at which the two endpoints are next visited.

For endpoint weights \(L,R\), one of the two direct endpoint orders
minimizes this weighted arrival-time sum. Thus a continuation can be
normalized after time \(2\), or after its first endpoint if earlier,
to direct endpoint travel. This gives completion by time \(6\).
It also shows that the last center visit before the first endpoint
of this continuation is no later than time \(3\): any such visit
after time \(2\) occurs on a straight leg from a position in
\([-1,1]\).

A final one-sided segment from the center at time \(t\) to its first
endpoint is dominated, together with its subsequent sweep, by the
direct tour toward that endpoint. The unit outward leg captures
same-side survivors no later and reaches that endpoint by time
\(t+1\). The original one-sided segment cannot reach it earlier.
Opposite-side survivors remain uncaptured until a center return,
which follows that endpoint no earlier than \(t+2\ge2\); they then
cannot be caught before the opposite endpoint. The direct tour
reaches that endpoint at \(t+3\).

The same argument handles a returning one-sided center excursion
of duration \(2h\ge2\). Replace the entire excursion and its future
by the direct tour toward its sign. The original cannot return to
the center before \(t+2\), so it cannot catch opposite-side
survivors before time \(t+3\). The direct tour does at least as well
on both sides.

We may therefore assume that every returning excursion before the
final tour has duration less than \(2\), and that the final tour
has exactly two unit-speed legs. If a long excursion is present,
one such replacement discards the whole later path; no iteration
over infinitely many long excursions is needed.

## 4. A finite decomposition of a closed center zero set

Append the interval \([2,3]\) to the \(m\) central bands. On its
central square \(U,W\in[2,3]\), outward forcing gives
\[
                            F(t,x)=\frac12.                 \tag{4.1}
\]
For example, on the positive side the time-two radial footpoint is
\(2-W\le0\); the negative side follows by symmetry. Thus the appended
band is another stationary affine band of length \(1\).

Let \(Z\) be the set of center times between the starting center
\(t_0\) and the last center before the final tour. This is compact,
contains both end times, and lies in \([0,3]\).

For each of the \(m+1\) closed bands \(I_i=[a_i,a_{i+1}]\)
(including the appended band), if \(Z\cap I_i\ne\varnothing\), set
\[
          s_i=\min(Z\cap I_i),\qquad
          t_i=\max(Z\cap I_i),
\]
and retain the block \([s_i,t_i]\). Degenerate blocks are allowed
for this decomposition and will later contribute no legs.

The blocks are chronologically ordered and can overlap only at a
shared band endpoint. Their union contains all of \(Z\). Every
positive-length gap between consecutive nonempty blocks therefore
has no center time in its interior and is a single one-sided
excursion.

There are at most \(m\) such gaps. Equivalently, every gap strictly
straddles an internal band knot: if both endpoints belonged to a
single closed band, that band's block would contain the gap.
Distinct gaps have disjoint interiors, so no knot can be strictly
inside two of them. Using closed bands resolves excursions whose
endpoints coincide with knots without any generic-position
assumption.

For a block \([s_i,t_i]\), legality from both center endpoints gives
\[
       |m(u)|\le\min\{u-s_i,t_i-u\},
       \qquad s_i\le u\le t_i.
\]
Consequently
\[
                 s_i\le U(u),W(u)\le t_i.
\]
The **whole block**, including all its infinitely many possible
excursions and center holding sets, lies inside the one central
affine square \(I_i^2\).

We have therefore partitioned the path before its terminal tour
into at most \(m+1\) affine-square blocks and at most \(m\)
one-sided gap excursions. No decomposition of a center Cantor set
into intervals has been asserted or used.

## 5. Replace the finite pieces backwards

Start with the normalized final two-leg tour and work backwards
through the finite ordered list of blocks and gaps. At each step
the entire later physical route is already fixed. Its cost is
the concave nondecreasing function (2.1) of the current exit
records.

For an affine-square block, apply Section 2. One of the two
triangles (2.2) has no greater block-plus-future cost. It stays
inside that same square, preserves the two physical endpoint
states, and uses at most two legs.

For a gap excursion of duration \(2h<2\), its sign is constant.
If positive, legality gives
\[
                  0\le m(s+u)\le\min\{u,2h-u\}.
\]
The positive triangle is legal because \(h<1\). It is pointwise
farther toward the positive side, so it decreases the right
survival record at least as quickly. The left record remains
unchanged, because it is at most \(1/2\) and \(F\ge1/2\) on the
positive side. Thus this triangle has no greater local cost and
no greater exit records. Monotonicity of the fixed continuation
preserves the comparison. The negative gap is its reflection.

Each replacement weakly decreases the cost of the **current
entire route**, with its current incoming records. A later
replacement need not remain optimal under the record change
produced by an earlier one: the earlier comparison already
includes that later route as its fixed continuation. This is
why the backwards construction is sufficient.

At most \(m+1+m=2m+1\) triangles remain, followed by the two-leg
tour. Their total number of unit-speed physical legs is at most
\[
               2(m+1)+2m+2=\boxed{4m+4}.                    \tag{5.1}
\]

All replacements preserve their time intervals except the
initially normalized terminal tour or a long-excursion
replacement, which can only shorten completion. The time-six
completion bound is retained.

## 6. Application to common-threshold interpolation

Let the light-grid spacing be \(h=1/n\), and suppose a legal
normalized radial nodal profile is interpolated by the common
threshold construction. Write the threshold interval as
\[
       [A,B]=[1/2-\varepsilon,1/2+\varepsilon],
       \qquad 0<\varepsilon\le1/2.
\]
The signed center nodal values are \(1/2\), and symmetry makes
the two off-diagonal nodal values in any centered light square
sum to \(1\).

In the square \(U,W\in[kh,(k+1)h]\), let those off-diagonal
values be \(1/2+d_k\) and \(1/2-d_k\), with \(d_k\ge0\).
Both coordinates use the same threshold within this square.
Writing
\[
 p_k(z)=
 \max\!\left\{0,\min\!\left\{1,
       \frac{(z-kh)/h-A}{B-A}\right\}\right\},
\]
the interpolated field is exactly
\[
       F(U,W)=\frac12+d_k\bigl(p_k(U)-p_k(W)\bigr).           \tag{6.1}
\]
This identity uses only the center and symmetry identities;
it is unaffected by which reflected orientation is chosen
for the cell's common threshold.

For full width \(\varepsilon=1/2\), \(p_k\) is affine
throughout the cell. The \(2n\) intervals of length \(h\)
partitioning \([0,2]\) are therefore central affine bands:
\[
                m=2n,\qquad 4m+4=\boxed{8n+4}.              \tag{6.2}
\]

For a positive narrower width, split each interval at
\((k+A)h\) and \((k+B)h\). On each resulting interval
\(p_k\) is affine, possibly constant. There are at most
\(6n\) central affine bands on \([0,2]\), so
\[
                         4m+4\le\boxed{24n+4}.              \tag{6.3}
\]

In both cases the field is already sticky and outward after
time \(2\), by the normalized-profile interpolation theorem.
For rational nodal data and rational \(\varepsilon>0\), all
band endpoints and affine coefficients are rational.

The deterministic limit \(\varepsilon=0\) is excluded: it
can create capture atoms, and the continuous interior-field
argument above must not be applied to that limit as an
attained Princess strategy.

## 7. What is and is not made finite

The theorem bounds the complete centered continuation for a
fixed interpolated field. In particular, the exact center
value can be represented by finitely many response words
with continuous turn-time parameters. For rational P1 data,
splitting the field and record order branches gives rational
quadratic objectives on rational polyhedral feasibility
domains. The parametric active-face argument then gives a
finite lower envelope of rational quadratic candidate
functions on rational polyhedral parameter domains; the
[exact parametric center-value note](PARAMETRIC_CENTER_VALUE_QUADRATICS.md) supplies its precise
endpoint and singular-face treatment.

This does not say that the regions on which individual
candidates win are polyhedra: comparisons of two quadratic
candidates can have curved boundaries. It also does not
restrict turns to lattice vertices.

Most importantly, this theorem leaves the **precenter**
part of the unrestricted response untouched. It neither
proves an exact finite description of the globally optimal
Princess field nor closes the remaining game-value gap.
