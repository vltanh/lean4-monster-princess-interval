# A finite continuous Bellman certificate in actual survival records

This note gives a sufficient certificate for a **fixed rational P1 Princess field**. Its inequalities cover continuous starts, arbitrary legal Monster velocities, and record-switch faces. They are not restricted to physical grid paths. A successful certificate at the value of an independently verified physical Monster upper would give an exact saddle certificate.

No such equality is asserted here. The discovery implementation is separate from exact acceptance. In particular, simply interpolating a discrete Bellman value is not justified: the exact diagnostic `check_record_dp_lift.py` finds failed interior and record-face inequalities even for a coarse test field.

## 1. Field assumptions and the stopped physical problem

Let `F(t,x)` be the signed interior CDF of a symmetric ordered Princess law. Assume it is continuous and rational P1 on a finite characteristic triangulation, including continuous endpoint interior traces. It has no interior atoms, is sticky at its first endpoint, and moves maximally outward after time 2. Endpoint atoms are allowed.

On each affine field cell, write light coordinates

\[
 U=t+x,\qquad W=t-x,
 \qquad F=a+bU-cW,
 \quad b,c\ge0.
\]

For a Monster prefix before its first endpoint, its two survival records are

\[
 L(t)=\min_{s\le t}F(s,m(s)),\qquad
 R(t)=\min_{s\le t}\bigl(1-F(s,m(s))\bigr).
\]

The survival probability is `L+R`. At its corresponding endpoint, a record is set to zero; the other record is unchanged. The endpoint jump uses actual capture, whereas all pre-exit formulas below use the continuous interior trace.

By symmetry it suffices to test Monster starts in `[0,1]`. Before the first center visit the Monster stays positive, so `L>=1/2`; after the center visit both records are at most `1/2`.

The outward-after-two reduction permits the following stopping rule: stop at the first endpoint or at time 2, and use the exact continuation guards below. Any path that has not visited the center by time 2 already has expected capture time greater than `3/2`. Thus a certificate of value at most `3/2` for the center-by-two class is a global lower certificate.

This argument does not use a bound on the number of visits to a field triangle. Full-width common-threshold fields can have off-center main diagonals, so the earlier no-reentry response argument for time-diagonal triangles does not automatically apply to them. Local Bellman inequalities remain valid through any number of cell crossings.

## 2. Two compact state domains

The precenter-positive domain is

\[
 \begin{aligned}
 &0\le U\le2,\quad U+W\ge0,\quad0\le U-W\le2,\\
 &\tfrac12\le L\le F(U,W),\quad
 0\le R\le1-F(U,W).
 \end{aligned} \tag{2.1}
\]

The inequality `U<=2` is exactly the requirement that a positive current position can still reach the center by time 2. A path first hitting the positive endpoint in this mode necessarily does so by time 1.

The postcenter domain is

\[
 \begin{aligned}
 &U,W\ge0,\quad U+W\le4,\quad |U-W|\le2,\\
 &0\le L,R\le\tfrac12,\quad
 L\le F(U,W),\quad R\le1-F(U,W).
 \end{aligned} \tag{2.2}
\]

On a fixed affine field triangle, intersecting these conditions with any rational record rectangle gives a rational polytope in four dimensions. Both domains satisfy `L+R<=1`.

Let `P_pre` and `P_post` be continuous potentials on these domains, piecewise quadratic on a finite rational polyhedral subdivision. Their restrictions from adjacent cells must agree exactly on shared faces.

## 3. Complete local control inequalities

All derivatives below refer to the polynomial for the current closed cell. Require

\[
 P_L\ge0,\qquad P_R\ge0. \tag{3.1}
\]

In the interior of the record constraints, the two unit-speed conditions are

\[
 2P_U+L+R\ge0,
 \qquad
 2P_W+L+R\ge0. \tag{3.2}
\]

On the left-record face `L=F`, require

\[
 2\bigl(P_W+F_WP_L\bigr)+L+R\ge0. \tag{3.3}
\]

On the right-record face `R=1-F`, require

\[
 2\bigl(P_U-F_UP_R\bigr)+L+R\ge0. \tag{3.4}
\]

Impose both applicable conditions when the two record faces meet. Imposing (3.2) on closed cells as well is harmless; on an active face the corresponding clamped condition is stronger because of (3.1) and the transport signs.

These inequalities also handle every velocity `v in [-1,1]`. Indeed, `dot U=1+v`, `dot W=1-v`, and the field derivative is affine in `v`. On an active record face its contribution to `dot P` is a nonnegative multiple of either `min(dot F,0)` or `min(-dot F,0)`. Consequently `dot P+L+R` is concave in `v`. Nonnegativity at the two endpoints `v=-1,+1` implies nonnegativity throughout the interval.

For a quadratic potential and affine `F`, all expressions in (3.1)–(3.4) are affine in the four state coordinates. Therefore they are checked exactly at the vertices of their respective rational polytopes or faces. A record-switch face must not be omitted merely because its interior has zero four-dimensional volume.

At a field or potential seam, continuity identifies the tangential derivatives. Checking the closed pieces permits any admissible crossing or motion along a seam. The resulting potential is Lipschitz on each compact mode, so the inequalities integrate along arbitrary absolutely continuous legal paths.

## 4. Exact mode and exit guards

### Center registration

At the first center visit the state is `U=W=t`, `L=1/2`. Require

\[
 P_{\rm pre}(t,t,1/2,R)
 \le P_{\rm post}(t,t,1/2,R). \tag{4.1}
\]

Identifying the two potential traces is an allowed stronger implementation. The discovery mesh uses this exact identification.

### First endpoint

Define the exact one-clock continuation

\[
 B(t,L)=\int_0^2\min\{L,F(t+u,1-u)\}\,du. \tag{4.2}
\]

The descending sweep minimizes the remaining record at every later time. Thus after a first positive-endpoint contact the exact continuation cost is `B(t,L)`, irrespective of the record captured at that endpoint. Require

\[
 P(U,W,L,R)\le B\bigl((U+W)/2,L\bigr)
 \quad\text{when }U-W=2. \tag{4.3}
\]

At the negative endpoint, by reflection require

\[
 P(U,W,L,R)\le B\bigl((U+W)/2,R\bigr)
 \quad\text{when }W-U=2. \tag{4.4}
\]

The precenter-positive mode only has the first of these endpoint exits. Its remaining record can exceed `1/2`, so the tail builder must cover `0<=L<=1`; restricting it to postcenter records would omit initial endpoint starts.

### Time 2

In the postcenter mode at time 2, all surviving records are constant until their own endpoint. Set `x=(U-W)/2`. The exact remaining cost is

\[
 G(x,L,R)=\min\{
 (1+x)L+(3+x)R,
 (3-x)L+(1-x)R\}. \tag{4.5}
\]

Require `P_post<=` each of the two expressions. The time-2 record is already updated: it is part of the state constraint `L<=F`, `R<=1-F`. It is not an additional scoring interval before this guard.

### Initial states, including endpoint atoms

For `0<=x<1`, require

\[
 P_{\rm pre}\bigl(x,-x,F(0,x),1-F(0,x)\bigr)\ge c. \tag{4.6}
\]

There is no interior atom, so these two records sum to one. Requiring the continuous limiting trace at `x=1` as well is a permissible stronger condition.

An actual endpoint start has already captured the endpoint atom. It must be handled separately by

\[
 c\le B\bigl(0,F(0,1)\bigr). \tag{4.7}
\]

This avoids assigning the positive endpoint's uncaptured interior-limit record to an endpoint-start path. Negative endpoint starts are its reflection.

## 5. Global lower-certificate theorem

If the potentials satisfy Sections 2–4 and `c<=3/2`, then the Princess law has security at least `c` against every legal Monster path.

To prove this, take any centered-by-two path starting in the interior of the positive half. Integrating Section 3 up to its first center/endpoint/time-2 event gives the accumulated survival integral plus the new potential at least the old potential. Center registration cannot decrease the potential by (4.1). At the first endpoint or time 2, the exact continuation dominates the potential by (4.3)–(4.5). The total expected capture time is therefore at least the initial potential, hence at least `c` by (4.6).

Endpoint starts follow from (4.7), and negative starts follow by reflecting the entire path. Paths with a center visit after time 2 have cost greater than `3/2`, so they also satisfy the lower bound.

If an independent physical Monster certificate has unrestricted upper `c`, the two certificates prove the exact game value and a saddle pair. Nothing in this criterion assumes finite initial support of the Princess: a finite P1 CDF formula generally describes a continuum of initial positions.

## 6. Why the endpoint guard has finitely many quadratic charts

Along the endpoint sweep, `U=t+1` is fixed and `W=t-1+2u` increases. A finite characteristic mesh partitions the `(t,u)` parameter domain into finitely many rational polygons. Refining in `t` at their vertices gives bands on which the ordered sweep pieces have affine-in-`t` endpoints and

\[
 F(t+u,1-u)=a_i+b_i t+c_i u,
 \qquad c_i\le0.
\]

There is at most one record crossing of the level `L` along the whole sweep. If it occurs in a nonflat piece, its location is

\[
 u_*=(L-a_i-b_i t)/c_i.
\]

The condition that it belongs to the piece is a pair of affine inequalities in `(t,L)`. Integrating `L` before the crossing and the affine field afterward gives a rational quadratic polynomial in `(t,L)`. A flat piece needs no division: the adjacent closed charts or the all-constant/all-field branches cover it. Coincident formulas agree on their common seams.

Thus `B` is given by finitely many rational quadratic formulas on an explicitly checked rational polygon cover. This construction uses the fixed field, not an approximation to the tail integral.

## 7. A finite exact acceptance procedure

The field triangles, record rectangles, and potential pieces are provided with rational data. The checker reconstructs their intersections and verifies coverage and shared-face agreement; it does not trust a list of favorable sample states.

Control checks are affine vertex checks, as above. The remaining differences are quadratic:

- the initial trace is quadratic on each rational interval;
- the center comparison is quadratic on a rational polygon;
- an endpoint comparison is quadratic on a polytope of dimension at most three, after intersecting a tail chart;
- each time-2 comparison is quadratic on a polytope of dimension at most three.

A quadratic minimum on a compact rational polytope can be checked by enumerating its faces. On the affine hull of each face, solve the rational linear stationary system for the restricted quadratic. Retain solutions lying in that face, including singular stationary affine sets; a nonempty such intersection has a rational point and the quadratic is constant on that stationary affine set. Include the vertices. The global minimum occurs among these candidates. This also covers an interior minimum that all vertex samples would miss.

There are no irrational root assumptions hidden in this quadratic case. Higher-degree potential pieces would require a separate exact polynomial-positivity procedure; the P2 implementation does not use them.

For LP discovery, a stronger linear sufficient condition is convenient. For every pair of vertices `v,w` of a guard polytope, require the quadratic polar coefficient

\[
 2q((v+w)/2)-\tfrac12q(v)-\tfrac12q(w)\ge0,
\]

where `q` is the desired nonnegative guard difference. Include `v=w`. For any convex representation `z=sum lambda_i v_i`, the quadratic is the corresponding weighted sum of these polar coefficients. Their nonnegativity therefore implies `q>=0` on the entire polytope. These constraints are linear in the potential coefficients when the Princess field is fixed.

The exact face-minimum test can accept certificates that the stronger polar conditions would reject. In particular, a numerical certificate is not rejected merely because an irrelevant nonphysical extension has a negative coefficient.

## 8. Direct repair of rational rounding errors

A finite rational replay can account explicitly for rounding the potential coefficients. Let `eta` and `delta_v` be the nonnegative positive parts of its worst record-derivative and unit-control violations, respectively. Let

\[
 S=\max\{F_U,-F_W\}
\]

over the field cells, and choose `gamma=delta_v+2S eta`. Let the nonnegative numbers `delta_g` and `delta_c` bound all upper-guard violations and the center-registration violation, respectively. These can be obtained by exact quadratic minimization, or conservatively by the exact polar coefficients.

Replace both potentials by

\[
 \widetilde P
 =P+\eta(L+R-1)+\gamma(t-2)-\delta_g,
 \qquad t=(U+W)/2,
\]

and subtract an additional `delta_c` from the precenter potential.

Record monotonicity is repaired by the `eta` term. The new unit-control contribution is at least `gamma-2S eta=delta_v`, repairing every control inequality. Since `L+R<=1` and `t<=2`, the added state-dependent terms are nonpositive, so all upper exit guards improve. The mode-specific constant repairs the center guard.

If the unrepaired initial trace is bounded below by `c0`, the repaired trace is bounded below by

\[
 c_0-2\gamma-\delta_g-\delta_c.
\]

Take the minimum with the exact endpoint-start value (4.7) and `3/2`. The resulting number is a rigorous lower bound once all stated residuals have been recomputed exactly. This repair is specific to the actual-record state and does not invoke an unquantified continuity argument.

## 9. Operational mesh construction

`solve_record_p2_lift.py` is the numerical discovery prototype. It uses characteristic physical triangles, a rational record grid, and the canonical staircase triangulation of each product `triangle × interval × interval`. P2 Lagrange nodes are shared on common faces. The state domain is obtained by the exact two additional cuts `L<=F` and `R<=1-F`.

The prototype's local geometry can be checked particularly simply. A vertex of a four-simplex cut by those two halfspaces is either an original vertex, an original edge meeting one cut, or an original triangle meeting both cuts. Enumerating those supports with rational linear systems reconstructs every clipped vertex. Each record-switch face is retained explicitly.

`check_record_dp_lift.py` is an exact diagnostic for one natural initializer: interpolate the grid remaining-cost value minus `Delta(L+R)/2`. It is not a successful certificate and is labeled accordingly. Its failed checks demonstrate why off-grid initial traces and record-switch faces must be part of the acceptance procedure. The optimization prototype frees the potential coefficients instead of assuming that this initializer is valid.


## 10. An oriented minimum avoids fitting both terminal orders in one piece

There is a useful variant with one precenter potential and one *oriented* postcenter potential `P_plus`. Require all postcenter controls and record monotonicity for `P_plus`, but impose only its positive-endpoint guard and the right-endpoint-first time-2 guard. Define

\[
 P_{\rm post}(U,W,L,R)
 =\min\{P_+(U,W,L,R),P_+(W,U,R,L)\}. \tag{10.1}
\]

Reflection preserves the control inequalities because the field is symmetric. Along any physical state path, both branches are absolutely continuous and satisfy the same running-cost subsolution inequality. Their minimum does as well: on the strict branch sets differentiate the active branch; on a positive-measure equality set the two derivatives agree almost everywhere.

At the positive endpoint the first branch supplies the required guard. At the negative endpoint the reflected branch supplies it. At time 2, the first branch is bounded by the right-first tour and the reflected branch by the left-first tour, so their minimum is bounded by the minimum of the two tour costs.

The precenter registration conditions become the two inequalities

\[
 \begin{aligned}
 P_{\rm pre}(t,t,1/2,R)&\le P_+(t,t,1/2,R),\\
 P_{\rm pre}(t,t,1/2,R)&\le P_+(t,t,R,1/2).
 \end{aligned} \tag{10.2}
\]

The initial and precenter endpoint guards are unchanged. Every check is still a finite affine or quadratic check. In particular, no explicit subdivision along the potentially curved set where the two postcenter branches are equal is needed.

This variant can be materially less restrictive than fitting a single quadratic piece below both terminal orders. It is implemented by the discovery solver's `--oriented` option. It is a sufficient certificate construction, not an assertion that either oriented branch alone is a global continuation lower bound.
