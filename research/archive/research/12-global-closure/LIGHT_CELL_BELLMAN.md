# A global light-cell lower certificate

This is a conservative, executable lower certificate for a **specified**
ordered princess CDF absorbed at the two endpoints by a declared time H.
It covers every monster path and every start, without a turn cutoff. It
does not claim that the current numerical CDF is a minimax strategy. The
first coarse run is weak; its purpose is a genuine global verification
route rather than another response-family exclusion.

## 1. A finite graph covering all monster paths

Use signed light coordinates U=t+x and V=t-x. Along every 1-Lipschitz
monster, both coordinates are nondecreasing. Choose any finite rectangular
grid covering 0<=t<=H, -1<=x<=1. Retain every closed rectangle intersecting
this physical region, and connect neighboring rectangles in the increasing
U or increasing V direction.

Every monster traces a finite chain in this graph. Its arbitrarily many
turns inside one rectangle do not create more graph transitions. At a
simultaneous crossing of two grid lines, insert a rectangle touching the
same grid vertex; closed-cell inclusion makes this legitimate. Additional
graph chains are allowed: this is a relaxation, not a restriction on the
monster.

For evaluations outside the physical rectangle, extend every princess
path constantly to negative times and constantly after endpoint absorption.
For x outside [-1,1], use the usual CDF values zero or one. The extension
preserves the transport order F_U>=0, F_V<=0, including the strict and
closed traces.

For cell C=[u0,u1] x [v0,v1], every visited point satisfies

    F^-(u0,v1) <= F^-(U,V) <= F^+(U,V) <= F^+(u1,v0).

Grant the relaxed monster capture of this entire rank interval when it
enters the cell, at the artificial timestamp

    t_C=max(0,(u0+v0)/2).

This timestamp is no later than any real visit to the cell. The relaxed
capture interval contains every actual capture made in that cell.

The integer implementation uses a declared probability denominator D and
rounds the surviving lower and upper masses **down**:

    A_C=floor(D*F^-(u0,v1)),
    B_C=floor(D*(1-F^+(u1,v0))).

This grants additional captures. It therefore remains a lower relaxation.
CDF evaluations and this rounding use exact fractions.

## 2. Initial states and endpoint completion

Every cell meeting U+V=0 is an allowed starting cell. Its entire central
rank interval is granted capture at zero. The remaining state is
`(a,b)=(A_C,B_C)`, where a and b are D times the uncaptured masses below
and above the monster.

A cell meeting U+V=2H has an optional terminal action. Intersect it with
that line and the arena to obtain the possible time-H positions
`[xmin,xmax]`. All surviving princesses are then at the endpoints. The
terminal absolute capture contribution is

    min(a*(H+1+xmin)+b*(H+3+xmin),
        a*(H+3-xmax)+b*(H+1-xmax))/D.

The first option visits the left endpoint first and chooses its best
possible starting position in the cell; the second does the same on the
right. Allowing this position choice only lowers the true continuation
cost. Actual monsters with arbitrarily slow or incomplete continuation
cannot beat this endpoint-tour lower bound.

## 3. Backward Bellman calculation

At a cell whose current surviving masses are `(a,b)`, moving to successor
cell C' updates them to

    a'=min(a,A_C'),  b'=min(b,B_C').

The new absolute capture contribution is

    t_C' * ((a-a')+(b-b')) / D.

Add the successor value and minimize over successors and any terminal
action. The graph is acyclic, so backward evaluation is finite. Minimizing
the initial values over all initial cells gives a lower bound for **every
unrestricted monster** against the supplied CDF. It is not merely the
value against graph-constrained real monsters: the artificial early
captures are what make the direction of the bound correct.

## 4. Concave record interpolation

For a fixed future cell chain and fixed endpoint-tour order, the first
capture timestamp of a remaining lower rank is nonincreasing with rank.
The same statement holds for the upper tail when it is parametrized from
the upper endpoint inward. Integrating these timestamps over initial
surviving masses gives a jointly concave function of `(a,b)`.
The minimum over complete chains and terminal orders remains concave.

It is therefore sufficient for a conservative computation to retain a
rectangular grid of mass records in each cell, including zero and both
exact cell bounds. At a nongrid successor state, interpolate the four
surrounding lower nodal values with nonnegative bilinear weights. True
concavity puts this interpolant below the true relaxed value. Backward
induction preserves the lower-bound direction even if the interpolated
numerical surface is not itself concave.

The implementation stores all values in integer units `1/(D*time_den)`.
Both one-dimensional interpolation stages round downward. Products use
128-bit intermediate integers, and the input checks exclude overflow of
stored 64-bit values. This avoids assigning an exact-certificate status to
an unchecked floating dynamic program.

## 5. What was checked and what remains

`light_bellman.py` constructs the graph and audits every affine CDF
triangle with exact rationals. `light_bellman.cpp` performs the integer
calculation. The companion verifier compares complete small cases with an
independent individual-rank-mask search, checks coarse interpolation is a
lower bound, and exercises the overflow guard.

This theorem and its trace conventions received independent internal
review. It is not a Lean formalization. The first native-mesh run on the
old `initial_inward_repaired` field gives only approximately 1.18261,
far below the candidate's tested route scores. It is therefore not used
to improve the game's lower bound or to claim near-optimality. Cell-wide
early captures explain why the coarse relaxation can be loose.

The separate physical light-**node** search uses actual unit-leg routes
and exact capture moments to discover attacks. That search is useful for
strategy construction, but its restricted spatial graph and floating
record interpolation do not provide the unrestricted lower guarantee
proved here. Its output routes are independently rescored before use.
