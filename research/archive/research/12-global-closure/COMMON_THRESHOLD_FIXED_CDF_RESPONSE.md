# Exact finite response to a supplied common-threshold Princess field

Research theorem independently reviewed by the root, audit, and verification
agents, 2026-11-14. Frozen after the final reviews.

The moving spatial diagonals in a common-threshold P1 field do admit a
finite response reduction. The reduction concerns each **supplied fixed
Princess field**. It does not assert that some finite field mesh is
equilibrium-sufficient for the unrestricted game.

For a full-width rational common-threshold field on light mesh `1/n`, an
exact best response can be chosen with at most

\[
 \boxed{31(8n+3)+1=248n+94}
 \tag{1}
\]

physical affine pieces. For a rational positive narrow width, a safe bound
is

\[
 \boxed{31(24n+7)+1=744n+218.}
 \tag{2}
\]

Both statements allow a free initial Monster position and actual endpoint
starts. The fixed-field value and an attaining response can be computed by
a finite collection of rational quadratic programs over bounded rational
polytopes. In particular, a rational attaining response exists.

## 1. Supplied field and geometric assumptions

Let `F(t,x)` denote the continuous interior CDF, including its continuous
interior traces at `x=±1`, of a legal symmetric ordered Princess law. It has
no interior atoms, stops each Princess at her endpoint, and forces every
surviving radius maximally outward after time two. The actual endpoint
traces are

\[
 F^-(t,-1)=0,\quad F^+(t,-1)=F(t,-1),
 \qquad
 F^-(t,1)=F(t,1),\quad F^+(t,1)=1.
 \tag{3}
\]

Use light coordinates `U=t+x`, `W=t-x`. The field is obtained from a
rational nodal common-threshold construction with positive threshold
width. On every affine piece its transport inequalities imply

\[
 F(t,x)=at+bx+c,\qquad b\ge |a|.
 \tag{4}
\]

For full width, the light grid has knots `i/n`. A light square is either
affine, split along a time diagonal, or split along a spatial diagonal.
Across a spatial diagonal `x=x_0`, continuity forces the same time
coefficient on both sides:

\[
 F(t,x)=at+c+
 \begin{cases}
   b_-(x-x_0),&x\le x_0,\\
   b_+(x-x_0),&x\ge x_0,
 \end{cases}
 \qquad b_\pm\ge |a|.
 \tag{5}
\]

The interface in (5) is stationary in physical space; the common time
coefficient `a` need not vanish.

For narrow width, write

\[
 A=\tfrac12-\varepsilon,\qquad
 B=\tfrac12+\varepsilon,\qquad 0<\varepsilon<\tfrac12,
\]

and refine each light axis by

\[
 \frac in,\qquad\frac{i+A}{n},\qquad\frac{i+B}{n}.
 \tag{6}
\]

On each refined coordinate band, the scalar threshold probability is
either clamped or affine. If at least one coordinate is clamped, the
field is affine on the refined rectangle. When both are active, both
bands have the same width `2ε/n`, so the crossing rectangle is a square.
The shared threshold gives a spatial diagonal for equal orientations and
a time diagonal for opposite orientations. Thus the same local cell
types apply. The full-width endpoint case `ε=1/2` uses the coarser grid.

For the validated outward nodal profiles used by the extraction, the raw
interpolated field is already outward after two, as proved in
`NORMALIZED_GRID_BANK_PRICING.md`. Describing the same normalization as an
outward overwrite at time two does not add an unclassified cut. On the
positive half of `t=2`, the light bands have opposite orientations and
coarse indices `i+j=4n-1`, so this line is precisely their existing time
diagonal. In the narrow construction, the local fractions sum to one:
either both lie in the central active bands, where the same time diagonal
applies, or both are in complementary clamped bands, where the field is
constant across the cut. The negative side follows by reflection. The
outward footpoint depends on one light coordinate and uses the same knot
set; its absorption front is a coarse coordinate line. More explicitly,
the common odd periodic rounding map satisfies `T(4-W)=4-T(W)`. Thus
`U+W>=4` implies `T(U)>=4-T(W)`, so the rounded node is also after time
two. On the positive side its Qout nodal value depends only on `T(W)`,
which proves equality with the outward extension directly. The narrow
knot set is likewise invariant under `z -> 4-z` because `A+B=1`.

At a physical boundary `U-W=±2`, periodicity aligns the corresponding
coordinate bands. A boundary-cut cell has a single affine interior half;
its dividing spatial diagonal is the physical boundary itself. All field
values used below remain in that physical half-cell. No affine extension
outside the arena is used.

These facts are also sufficient hypotheses for the theorem without
referring to the threshold construction: a supplied rational field with
these cell types, endpoint traces, and outward normalization has the same
finite response conclusion.

## 2. Compact response horizon and actual first endpoint

A direct unit-speed sweep from one endpoint to the other has expected
capture time at most `3/2`: the Princess on the starting side is caught by
time one and the other signed half by time two.

Suppose a Monster has not visited the center by time two. By reflection
assume its position at time two is positive. The negative fair half has
not yet been caught. After time two, those Princesses move outward at
speed one, so they can be caught only at their negative endpoint. The
Monster cannot reach it before `3+m(2)>3`. Its expected capture time is
therefore strictly greater than `3/2`. Such a path is unnecessary for a
best response.

For a path that has visited the center by two, the established outward
normalization replaces its suffix after time two by a direct endpoint
tour in its chosen endpoint order. If it reaches an endpoint earlier,
the universal direct sweep to the opposite endpoint dominates its entire
remaining path. These are the physical arguments in
`NORMALIZED_GRID_BANK_PRICING.md`; they apply equally to continuous paths.

Consequently a best response may be sought among paths whose first
endpoint time is at most four and which complete both endpoints by six.
Let `σ<=4` denote that first endpoint time. Once it is reached, only one
unit-speed opposite sweep is needed.

The bounded class of 1-Lipschitz paths with a center visit by two, a first
endpoint visit by four, and both endpoint visits by six is compact in the
uniform topology. For each
Princess path, first capture time is lower semicontinuous in the Monster
path. Its expectation is lower semicontinuous by Fatou's lemma. Capture is
bounded by six on this class. Hence a minimizing path exists.

Later cell replacements retain their physical endpoint states and times,
or encounter an actual endpoint earlier. They therefore retain the bound
`σ<=4` and completion by six. It is unnecessary to impose a new center-time
constraint on every intermediate replacement.

## 3. Local bounds and the complete fixed continuation

For a fixed later physical path, including its actual endpoint contacts,
the remaining capture cost as a function of incoming scalar records is

\[
 g(L,H)=\int\left[
    \min\{L,A(s)\}+1-\max\{H,B(s)\}\right]ds.
 \tag{7}
\]

It is continuous and jointly concave, nondecreasing in `L` and
nonincreasing in `H`. This is the continuation required by the local
two-record exchange arguments.

### Affine cells and time diagonals

On an affine coordinate rectangle, the record-preserving four-leg theorem
gives at most four unit-speed legs and one constant-CDF leg. The latter has
velocity `-a/b` when `b>0`; constant fields use the separate two-run case.

A time-diagonal triangle contains the coordinatewise box between any
comparable entry and exit points. Since `U,W` are nondecreasing, a path
cannot reenter it. The affine theorem therefore applies to each of its
two halves separately. A full time-split rectangle needs at most ten
physical pieces.

### Spatially split interior squares: thirty-one pieces

Take the first and last contact of the old path segment with the spatial
interface in (5). Its prefix before the first contact and suffix after the
last contact each lie in one affine half-square.

`AFFINE_MOVING_FLOOR_HALF_CELL.md` and
`AFFINE_MOVING_CEILING_HALF_CELL.md`, after reflection if `a<0`, give
record-preserving bounds of five and thirteen pieces for the two
orientations. Use the conservative thirteen-piece bound for each exterior.
These replacements retain the old split times, positions, and records.
They may create additional interface contacts, which does not invalidate
the old split points or their piece counts.

Next apply `MOVING_KINK_RETURN_COMPRESSION.md` to the middle between the
old interface contacts, with the entire now-fixed later physical path in
(7). It gives at most two triangles and one interface hold, hence five
pieces. This middle exchange may change its exit records, but it weakly
decreases its local cost plus the whole fixed continuation.

Thus the complete square needs at most

\[
                  13+5+13=31
\]

pieces. If the path never meets the interface, a single half-cell bound
already suffices. Degenerate first/last contacts have zero duration.
The full coordinate box of an interior square lies in the arena, as
required by the return theorem.

### Physical boundary affine half-cells

Apply the affine half-cell theorem on the legal side of the physical
boundary, using its continuous interior trace as a nominal scalar field.
The containment needed for that theorem is

\[
 \text{entry/exit coordinate box}\ \cap\ \text{legal boundary half-plane}
 \ \subseteq\ [-1,1]\text{ arena}.
 \tag{8}
\]

This holds for the boundary cells described in Section 1. Every nominal
replacement stays in the legal half-cell, so its trace values remain
between zero and one. The conservative bound is thirteen pieces.

If a segment ends at the old first actual endpoint, feed the half-cell
lemma its nominal interior-trace exit records, then apply the actual
endpoint reset at that fixed exit. The reset value zero or one need not
be attained by the interior affine field and is not imposed as one of
that scalar lemma's prescribed attained records.

If the replacement touches the actual endpoint before the nominated old
first endpoint time, the actual strict/inclusive traces (3) enlarge its
captured rank interval. Its actual capture cost is no larger than the
nominal trace cost that ignored this early reset. The direct opposite
sweep then dominates its actual remaining path. This argument uses no
possibly negative nominal survival outside the arena: the replacement
never leaves the legal half-cell.

All local replacements retain the physical entry/exit states, so their
light coordinates remain in the same coordinatewise box. Earlier endpoint
contact can only terminate the cell processing and shorten the remaining
response to its final sweep.

## 4. No rectangle reentry and the explicit global counts

Along every legal Monster path, `U,W` are nondecreasing. A coordinate
rectangle cannot be left and later reentered: every intervening point
would have to remain in the coordinatewise box of two points of that
rectangle. Motion along a shared coordinate edge is already a unit-speed
physical leg and can be assigned consistently to one incident cell.

Before the first endpoint,

\[
 (U(\sigma)-U(0))+(W(\sigma)-W(0))=2\sigma\le8.
\]

A uniform `1/n` grid has at most `n` times the coordinate increase plus
one crossed knot on each axis. Thus at most `8n+3` rectangles are visited,
with a safe allowance for boundary ties. Since every full rectangle or
legal boundary half-rectangle costs at most thirty-one pieces, and the
final sweep is one piece, this proves (1).

The narrow grid (6) is the union of three translated `1/n` grids on each
axis. Each contributes at most `n` times the coordinate increase plus one
crossed knot. The resulting safe count is `24n+7` rectangles. The same
argument gives (2). One may instead use the finite actual count of
visited rectangles if a particular refined mesh has coincident knots.

These counts include zero-duration and edge ties by allowing unused pieces
and assigning shared-edge motion to an incident rectangle. Adjacent
equal-velocity pieces may be merged afterward.

## 5. A finite family of rational quadratic programs

Assume the supplied nodal data, mesh, and positive threshold width are
rational. All affine coefficients are rational. The finite permitted
velocities in each cell are

\[
       -1,\quad+1,\quad0,\quad-a/b_-,\quad-a/b_+,
\]

with only positive denominators used and constant-field cases treated
separately. There are finitely many cell sequences, piece words within
the above bounds, endpoint orders, and record-comparison branches.

For each word, use the initial Monster position and the nonnegative piece
durations as variables. Initial position is allowed throughout `[-1,1]`.
Physical time, position, light coordinates, and affine CDF values at every
piece endpoint are affine rational functions of these variables.
Endpoint constraints, speed-word constraints, cell membership, record
winners, and the chosen order of crossings are linear. Total time is at
most six, so the resulting closed parameter polytope is bounded.

Within one affine field piece the CDF has a fixed rational slope along
the chosen physical velocity. A crossing with an old record therefore
occurs at an affine rational time once its branch is chosen. Integrating
the two running record masses gives a rational quadratic polynomial.
Zero slopes are handled by the corresponding constant-record branch.

For evaluation, subdivide every physical leg at any field-cell and record
crossings; in particular, subdivide the final direct sweep. This adds
finitely many analytic subpieces without adding a physical control change
to (1) or (2). Actual endpoint resets are included in the subsequent
record state.

Endpoint starts are separate allowed branches with `σ=0`, followed by the
opposite sweep. Thus no free-start or endpoint case is omitted.

### Closed contact faces

A closed parameter branch may develop an endpoint contact earlier than
the nominated first contact. If its nominal formula ignores that early
reset, it overestimates the actual capture payoff by (3); it never
underestimates it. Every parameter point still represents a legal physical
path, because all cell and half-plane membership inequalities are closed.

Let `v_F` be the true fixed-field minimum. Every branch quadratic value is
at least the actual payoff of its represented path, hence at least `v_F`.
Conversely, the bounded attaining response constructed above is represented
by a branch with its actual first endpoint and correct record comparisons,
whose quadratic value is exactly `v_F`. Therefore

\[
 \boxed{v_F=\min\{\text{the finitely many rational quadratic programs}\}.}
 \tag{9}
\]

At a minimizing closed-branch parameter, an ignored earlier endpoint reset
cannot lower the actual payoff strictly below `v_F`; otherwise `v_F` would
not be the minimum. The represented path is consequently an attaining
response, and may be shortened to the direct sweep after that endpoint.

## 6. Exact rational attainment and an explicit finite algorithm

A rational quadratic polynomial on a nonempty compact rational polytope
has a rational minimizer. To see this, take the smallest face containing
some global minimizer in its relative interior. The gradient restricted
to that face's affine hull is zero. These stationary equations are linear
with rational coefficients. Their feasible solution set has a rational
point in the same relative interior. The quadratic is constant on this
stationary affine set, so that rational point has the same minimum value.

Equivalently, enumerate all faces of each branch polytope, solve the
rational restricted stationary equations, and retain a rational feasible
point whenever such a point exists in that face. The objective is constant
on each stationary solution set. A global minimizer is included among
these finitely many candidates, including zero-dimensional vertex faces.
This is an exact finite procedure; no convexity or numerical solver
termination is assumed.

Applying this to (9) gives a rational `v_F` and a rational initial position
and duration vector for an attaining response. This is an existence and
exact computation result, not a claim that the naive enumeration is
computationally small.

## 7. What this theorem does and does not close

The previous affine/time-diagonal reduction did not cover repeated
crossings of an off-center spatial diagonal. Sections 3 and 4 now cover
those crossings, actual boundary half-cells, narrow clamping strips,
arbitrary legal turn counts, and free initial positions.

The theorem certifies exact response reducibility for every supplied
rational positive-width common-threshold field, including the explicit
extracted Princess laws in this project. It does not prove that the
unrestricted optimal Princess law lies in a finite mesh or that any finite
clock-grid value equals the game value. Those are separate global
equilibrium questions.
