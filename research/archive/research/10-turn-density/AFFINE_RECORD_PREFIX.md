# Local record compression in one affine CDF corridor

## Status and scope

This is a local all-count prefix theorem. It does not certify a Princess law, an unrestricted game value, or a finite turn bound across an arbitrary piecewise affine CDF arrangement.

Let a continuous signed CDF be
\[
F(t,x)=q_0+\alpha(t-t_0)+\beta(x-x_0),\qquad \beta>|\alpha|,
\]
on a region containing the entire rank-time rectangle used below. Define the rank coordinate \(y=F-q_0\). A legal Monster path has
\[
-c_-\le \dot y\le c_+,\qquad c_+=\beta+\alpha,\quad c_-=\beta-\alpha.
\]
Conversely every path satisfying these inequalities is a legal physical path in this region. Holding \(y\) constant is the legal physical motion \(\dot x=-\alpha/\beta\).

The confinement hypothesis is substantive. If the specified final records are \([-L,H]\), and the local interval is \([t_0,t_0+T]\), require
\[
\{(t,x):t_0\le t\le t_0+T,\ -L\le F(t,x)-q_0\le H\}
\]
to lie in the affine CDF region and in the allowed physical domain. A sufficiently short neighborhood of an interior affine-cell accumulation point has this property. A general polygonal cell, and in particular a stationary density interface, need not have it.

## 1. The local theorem

Fix an entry point of rank \(0\), an already captured rank band \([-b,a]\), final records \([-L,H]\) containing that band, an exit rank \(y_e\in[-L,H]\), and an exit time \(T\). Suppose the confinement hypothesis holds.

Among all legal paths with these data, including paths with infinitely many turns, there is a path with no larger first-capture moment of the newly captured ranks consisting of:

1. at most three productive unit-speed legs;
2. one possible nonproductive unit-speed connector to the exit rank; and
3. a constant-rank hold after that connector to reach the prescribed exit time.

Zero-length pieces are omitted. A productive leg here may first cross ranks already captured before extending one record. Consecutive legs with the same direction are combined. The two possible first directions are both allowed.

Any absolute entry-time contribution is fixed by the final newly captured mass, so the assertion concerns either absolute or entry-relative capture moments. The old history and every continuation after the common exit point and time are unchanged.

If a rank direction has zero speed, it cannot create new records in that direction. The alternating argument is unnecessary in that degenerate case.

## 2. Exact finite-itinerary formula

Take the first direction to be positive. Write alternating record extrema as
\[
r_i=(-1)^{i+1}x_i,\qquad x_i\ge x_{i-2},\quad
x_{-1}=x_0=0,
\]
with indices in this display starting at \(i=1\). The last two extrema are fixed by \(H,L\) and by the final direction.

For the initially uncaptured case \(a=b=0\), a fastest itinerary has
\[
\tau_i=\tau_{i-1}+\frac{x_i+x_{i-1}}{c_i},\qquad
c_i=\begin{cases}c_+,&i\text{ odd},\\c_-,&i\text{ even}.\end{cases}
\]
Its unweighted first-capture rank moment is
\[
M_N=\sum_{i=1}^N\left[
 (x_i-x_{i-2})\tau_{i-1}
 +\frac{x_i^2-x_{i-2}^2}{2c_i}
 +\frac{x_{i-1}(x_i-x_{i-2})}{c_i}
 \right].
\]
Put \(k=c_+^{-1}+c_-^{-1}\). Direct telescoping gives
\[
\tau_N=\frac{x_N}{c_N}+k\sum_{i=1}^{N-1}x_i
\]
and
\[
\begin{aligned}
M_N={}&\frac{x_N^2}{2c_N}+\frac{x_{N-1}^2}{2c_{N-1}}+kS,\\
S={}&(x_{N-1}+x_N)\sum_{j=1}^{N-2}x_j+x_Nx_{N-1}\\
 &-\sum_{j=1}^{N-2}x_j^2-\sum_{j=1}^{N-2}x_jx_{j+1}.
\end{aligned}
\]

For an already captured band \([-b,a]\), assuming the first two turns reach the respective old frontiers, subtract
\[
\frac{a^2}{2c_+}+\frac{b^2}{2c_-}+bkx_1.
\]
This is exactly the first-capture moment assigned by the zero-band itinerary to those already captured ranks. It changes only a constant and a linear term. Directions are exchanged for a negative first leg.

## 3. Concavity and the one-budget vertex argument

Keep \(x_{N-1},x_N\) fixed. The Hessian in \(x_1,\dots,x_{N-2}\) has diagonal \(-2k\), adjacent entries \(-k\), and all other entries zero. For a variation \(v\),
\[
v^\mathsf THv
=-k\left[v_1^2+v_m^2+\sum_{j=1}^{m-1}(v_j+v_{j+1})^2\right]<0
\]
unless \(v=0\).

The odd record levels form one ordered chain between their initial and final positive records; the even levels form a second such chain. Their feasible set before imposing time is the product of two simplices. The final connector has fixed duration because its initial final extremum and its target rank are fixed. The travel-time formula therefore imposes just one extra linear upper budget on the sum of the intermediate levels.

A concave function has a minimum at a vertex of this cut polytope. Every vertex is either an original product vertex or the intersection of the time-budget hyperplane with a product edge. Each chain simplex has vertices using only its two endpoint levels. A product edge varies a contiguous block of one parity together. Therefore a cut vertex has at most one partial level in total, in addition to the two final record levels.

Repeated endpoint or partial levels do not capture new ranks. Delete the corresponding unproductive detours and visit the remaining productive extrema directly, in their retained order. Every retained record is reached no later. There are at most three productive levels. Complete the fixed exit connector, then hold the exit rank until time \(T\). The rank-time rectangle makes all these replacements legal in the same affine region.

Additional cell-confinement inequalities would be additional linear constraints. The single-budget vertex conclusion cannot be used after silently adding them.

## 4. Arbitrary paths and an initial accumulation of turns

A finite piecewise linear rank path can be accelerated along its finite sequence of productive record extrema. Traveling to each next extremum at the appropriate maximal rank speed reaches it no later; subsequent connector and hold pieces recover the prescribed exit state and time. This cannot increase the first-capture moment.

For an arbitrary legal rank path, approximate it uniformly by piecewise linear interpolation, including the first attainment times of its final upper and lower extrema and the exit time among the interpolation nodes. The interpolants retain the speed constraints, final records, and exit data. Their first-capture moment is continuous under this uniform approximation because
\[
M=T(H+L-a-b)-\int_0^T\{\text{newly captured rank width by }s\}\,ds
\]
and both running extrema are uniformly Lipschitz with respect to the path in the supremum norm.

Compress each finite approximant as above. The family with at most three productive legs, one connector, and one hold is compact after zero-duration pieces are allowed. A convergent subsequence yields the asserted compressed path, with moment no greater than the original. This step covers infinitely many turns accumulating at the entry time or at an interior time; it does not assume a minimum productive excursion size.

## 5. The remaining two-cell exception

For a positive-width translation-fan CDF, a local initial cone can be split by a stationary density edge:
\[
F(t,x)=q_0+\alpha t+\beta_\pm(x-a),\qquad x\gtrless a.
\]
The two cells share \(\alpha\), but their densities can differ. The single affine rank transform does not apply across that edge.

For \(\alpha>0\), newly captured lower records lie on the negative side. A newly captured upper band can begin before its positive-going leg crosses the edge. Relative to the inverse using only the positive-side speed, its exact correction is
\[
\frac12\left(\frac1{\alpha+\beta_+}-\frac1{\alpha+\beta_-}\right)
(\alpha S-H_{\rm old})_+^2,
\]
where \(S\) is the edge-crossing time. The correction is positive when \(\beta_->\beta_+\). Exact examples show that the full hinged objective need not retain the conditional concavity of the single-cell problem.

Consequently this note rules out a necessary infinite productive-turn accumulation strictly inside one affine cell. It does not rule out an accumulation at a stationary density interface. An interface deletion argument or a separate all-count solution is still required.

## 6. Exact implementation and verification

Files:

- \`packages/interval_turn_sheet/affine_record_prefix.cjs\`
- \`packages/interval_turn_sheet/verify_affine_record_prefix.cjs\`
- \`packages/interval_turn_sheet/affine_record_prefix_checks.json\`

The verifier compares the telescoped expression with chronological physical first-contact integration against uniformly distributed affine quantile trajectories. It also checks the Hessian by exact rational differences and enumerates product-chain vertices and their time-budget edge intersections.

The saved replay passes:

- 264 moment/travel identities;
- 132 independent physical rank integrals, inspecting 4,356 physical segments;
- 308 exact unit-leg identities;
- 880 exact Hessian entries;
- 3,239 feasible budget vertices and 3,239 three-productive-level checks;
- 440 comparisons with feasible interior points.

These are implementation checks of the stated formulas. The all-count theorem is the symbolic concavity, vertex, and compactness argument above; the fixtures do not stand in for that argument.
