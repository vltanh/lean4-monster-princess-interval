# A finite response bound for stationary spatial kinks

Research proof for independent review, 2026-11-13.

This settles the stationary case of the merged main-diagonal cell problem.
It does not settle a kink with nonzero common time derivative.

## Statement

On one light-coordinate rectangle, suppose the supplied continuous CDF is

\[
F(t,x)=\psi(x),
\]

where `psi` is continuous, nondecreasing, and piecewise affine, with `K`
spatial breakpoints. Constants and a common positive affine rescaling of
the CDF are immaterial. Fix physical entry and exit times and positions,
and the incoming and outgoing scalar record intervals.

Every admissible segment is weakly dominated for integrated captured rank
range by a segment with those same physical endpoints, duration, and scalar
exit records, using at most

\[
\boxed{K+4\text{ unit-speed directional legs and one final hold}.}
\tag{1}
\]

For one stationary kink, this is five directional legs and one hold.
Preserving both exit records makes the conclusion valid with every common
future physical continuation. No concavity assumption about that continuation
is needed.

The new argument differs from the affine-cell proof: the relevant weighted
first-visit quadratic need not be jointly concave. Concavity along carefully
chosen duration-preserving directions is enough.

## 1. Weighted first-visit coordinates

Translate the initial physical position to zero. Write the final physical
position as `f`, and the global negative and positive physical extrema as
`-B` and `H`. If both scalar exit records are new, the path must visit those
record levels. Let `a,b` be the physical frontier distances corresponding to
the old scalar records, so that the newly discovered left and right levels
lie beyond `-a` and `b`.

If `psi` is flat at an old record level, choose any physical old frontier
having that scalar value; the intervening flat interval has zero rank mass.
If an old scalar bound lies outside the segment's visited scalar range, that
side has no new record and belongs to the one-sided cases below.

The rank mass at a physical position has the piecewise constant density
`w(x)=psi'(x)`. With the notation

\[
w_+(z)=w(z),\qquad w_-(z)=w(-z),
\]

the first-visit objective, after removing a constant independent of the
path, is

\[
\int_b^H w_+(z)\tau_z\,dz+
\int_a^B w_-(z)\tau_{-z}\,dz.
\tag{2}
\]

This is the complement of integrated captured range by Fubini, exactly as
in the uniform-density affine-cell argument. Flat density intervals cause
no problem: they have zero contribution to (2).

Accelerate each monotone movement to unit speed and move unused time to a
final hold. Removing an excursion to an old opposite frontier and back
cannot delay any newly visited level. After the first global extreme, travel
directly to the other global extreme and then to `f`. Consequently it is
enough to consider tours whose earlier turns alternate between expanding
positive and negative records, followed by the two fixed global extremes.

Write the positive turn levels as `R_i` and negative turn depths as `L_i`.
Each of the two chains is nondecreasing. Set

\[
M_+(r)=\int_r^H w_+(z)\,dz,
\qquad M_-(l)=\int_l^B w_-(z)\,dz.
\]

For a right-first tour, the exact first-visit cost is a fixed direct-travel
term plus twice

\[
E=R_1M_-(a)
 +\sum_{R_i\to-L_i}(R_i+L_i)M_+(R_i)
 +\sum_{-L_{i-1}\to R_i,\ i\ge2}
       (L_{i-1}+R_i)M_-(L_{i-1}).
\tag{3}
\]

The proof is direct: a leftward travel distance delays every still-unvisited
positive level by twice that distance, and a rightward distance delays every
still-unvisited negative level by twice that distance. Integrating the
remaining target density gives (3). Reflection gives the left-first formula.

## 2. A piecewise quadratic objective on a turn polytope

List the genuinely partial turns, before the two fixed global records, as
`z_1,...,z_m` in chronological order. Each is a positive level or a negative
depth according to parity. Partition their feasible set according to which
spatial density interval contains each coordinate. There are finitely many
such branches for any fixed `m`.

On one branch, write `w_i` for the density at partial turn `z_i`. Expanding
(3), the entire quadratic part in partial turns is

\[
\boxed{-\sum_{i=1}^m w_i z_i^2
       -\sum_{i=1}^{m-1}w_i z_i z_{i+1}.}
\tag{4}
\]

The remaining terms are affine or constant. The coefficient of an adjacent
product is the density on the side of the earlier turn. The global final
turns are fixed, so their products with partial turns are only affine.

Each branch is a compact polytope: the two ordered-chain constraints, old
and global bounds, the chosen density-interval bounds, and one duration
inequality. If the last global extreme is `H`, the fastest tour duration is

\[
2\left(B+H+\sum_i z_i\right)-f;
\]

if it is `-B`, the final term is `+f`. Thus the extra constraint is exactly
`sum z_i <= S` for a fixed `S`. Any unused duration is a final physical hold.

## 3. Reduce to at most one free equal-value block

In either ordered chain, group equal coordinates into maximal blocks. A
block is free if its value is strictly between the fixed old/global/density
boundaries and strictly between neighboring distinct block values. All
coordinates of a free block have the same density.

If the duration inequality is inactive, vary one free block as a unit. Its
quadratic coefficient is `-r*w <= 0`, where `r` is its size. The objective is
concave on the full feasible interval of this variation. At an endpoint with
no larger cost, either a block merges or reaches a fixed bound, or the duration
constraint becomes active.

Now suppose the duration constraint is active and there are two free blocks.
Let their sizes be `r,s`. Shift the first block by `delta` and the second by
`-(r/s)*delta`, preserving total duration.

If they belong to the same ordered chain, there are no quadratic cross terms
between them in (4), because adjacent turns have opposite parity. The
quadratic coefficient is nonpositive.

If they belong to opposite chains, let their constant densities be `u,v`.
Let `e_1` count adjacent turn pairs directed from the first block to the
second, and `e_2` those directed from the second to the first. Each turn has
at most one successor and one predecessor, so

\[
0\le e_1,e_2\le\min(r,s).
\]

The quadratic coefficient along the duration-preserving variation is

\[
Q=-ru-\frac{r^2}{s}v+
       \frac rs(e_1u+e_2v).
\tag{5}
\]

For `r <= s`, the displayed edge bounds give

\[
Q\le-r\left(1-\frac rs\right)u\le0.
\]

For `r >= s`, they give

\[
Q\le-r\left(\frac rs-1\right)v\le0.
\]

Thus this line restriction is concave as well, even though the full Hessian
in (4) can be indefinite. Move to a feasible interval endpoint with no larger
cost. At least one pair of blocks merges or one block reaches a fixed bound.
The number of free blocks strictly decreases. Repeating this finite procedure
leaves at most one free block in the two chains together.

## 4. Count the remaining turns

Every partial-turn coordinate now equals an old record bound, a global
record bound, a fixed spatial density breakpoint, or the one free-block
value. Remove nonexpanding turns. Old-record turns discover no new rank;
repeated visits to the same fixed level or the same free level discover
nothing after their first visit; global-record revisits are unnecessary.
Removal advances first visits and cannot increase duration. Put the freed
time into the final hold.

Each spatial density breakpoint belongs to at most one of the two outward
frontier chains. It therefore contributes at most one genuine partial record
turn. There are at most `K` such turns, at most one further free partial turn,
and the two global record turns. Including travel to the final position gives
at most `K+4` directional legs, proving (1) for finite polygonal paths.

For arbitrary Lipschitz paths, take polygonal interpolants retaining the
endpoint states and global physical extrema. Their running scalar records
and integrated ranges converge uniformly because `psi` is Lipschitz. Apply
the finite-tour construction and pass to a convergent subsequence of its
bounded finite duration parameters. This gives the same exact domination
and record preservation for the original path.

If only one scalar exit record is new, the direct tour to that record and
then to the endpoint, followed by a hold, suffices. If neither record is new,
one direct leg and a hold suffice. Zero density and zero-duration branches
are included by the non-strict inequalities above.

## 5. Physical square containment

Every replacement has speed at most one, the original physical endpoints,
and the original duration. Its two light coordinates are nondecreasing and
have the original total increments. It therefore stays in the coordinatewise
box between entry and exit, which is contained in the merged light square.
The final physical hold has constant CDF because this theorem assumes `a=0`.

## 6. Why a two-run extension is not automatic

For the abstract concave-continuation version, take a stationary spatial
function with slopes one on the left of zero and four on the right. Start
and end at `x=1/5`, use duration one, and take incoming scalar records equal
to the starting scalar value. Add a continuation reward of `23/20` times the
new lower-record extension. Equivalently, its continuation cost is an affine
nonincreasing function of that extension.

The three-run path through `7/20`, then `-3/20`, then `1/5` has integrated
captured range `879/800` and continuation reward `437/400`, totaling

\[
\frac{1753}{800}=2.19125.
\]

The negative-first pure order through `-3/10` has total `109/50=2.18`; the
positive-first pure order through `7/10` has total `3/2`. Both are strictly
worse. A common positive scaling and shift put the CDF in `[0,1]`, and a
physical rescaling puts the example in an interior light square. This is a
counterexample to the abstract two-run lemma with arbitrary concave
continuation; it is not by itself a construction of a complete global
Princess law realizing that prescribed continuation.

## Remaining gap

For `F(t,x)=a*t+psi(x)` with `a != 0`, first-visit targets move and record
turn locations need not be ordered spatially. In particular, the static
two-chain density partition used above cannot simply be reused. Interface
crossing values are monotone, and first-hit/return times are affine on fixed
spatial branches, but a uniform bound on productive crossings remains to be
proved. Nothing in this note supplies that missing bound or a finite exact
equilibrium mesh.
