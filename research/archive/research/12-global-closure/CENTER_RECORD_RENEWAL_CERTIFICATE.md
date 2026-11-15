# Exact center renewal and a finite quadratic lower certificate

This reduction absorbs arbitrarily many postcenter excursions into a Bellman inequality on three state variables. It applies to a fixed symmetric ordered Princess field with continuous interior CDF, sticky endpoints, and maximal outward motion after time 2. It does not assume a finite number of Monster turns and does not assert that a particular finite potential attains the game value.

Write `F(t,x)` for the signed interior CDF and use survival records `L=min F` and `R=min(1-F)`. At every center state, `0<=L,R<=1/2`.

## 1. One-sided excursions are dominated by triangles

Consider an excursion from the center at time `t` back to the center at time `t+2h`, with the Monster positive throughout the open excursion. Lipschitz legality gives

\[
 0\le m(t+s)\le\min(s,2h-s),\qquad 0\le s\le2h.
\]

If `h<1`, the upper triangle is a legal path in the arena. It captures same-sign survivors no later: at every physical time its position and therefore its CDF value are at least those of the original excursion. Its right survival record is consequently no larger throughout. The left record remains `L` for both paths because `F>=1/2` on the positive half and `L<=1/2`.

Define

\[
 \begin{aligned}
 S(t,s)&=1-F(t+s,s)=F(t+s,-s),\\
 I(t,h,r)&=\int_0^h\min\{r,S(t,s)\}\,ds,\\
 r'&=\min\{r,S(t,h)\}.
 \end{aligned} \tag{1.1}
\]

Transport makes `S(t,s)` nonincreasing in `s`. During the outward leg the right record is `min(R,S(t,s))`. During the return leg it stays equal to its peak value `R'`: moving left makes `F` nonincreasing and therefore cannot lower `1-F`.

The exact positive-triangle cost is

\[
 C_+(t,h,L,R)=2hL+I(t,h,R)+hR',
 \quad R'=\min\{R,S(t,h)\}. \tag{1.2}
\]

Its exit center state is `(t+2h,L,R')`. The negative triangle has the reflected formula

\[
 C_-(t,h,L,R)=2hR+I(t,h,L)+hL',
 \quad L'=\min\{L,S(t,h)\}, \tag{1.3}
\]

and exits at `(t+2h,L',R)`.

These comparisons are recordwise and hold also when the original excursion has arbitrarily many internal reversals. A center continuation potential must be nondecreasing in both records so that the improved triangle's smaller exit record is harmless.

## 2. Final tours and long excursions

From a center state at time `t`, the direct positive-endpoint tour goes right for one unit of time and then left for two. The positive survivors contribute `I(t,1,R)` on the first leg and are all captured by its endpoint. The left record contributes `L` on that first leg.

The first endpoint is reached at time `t+1>=1`. Its remaining opposite sweep has cost exactly `2L`: the sweep reaches the center at `t+2>=2`, and outward-after-two survivors cannot be captured in the interior before their endpoint. Thus the exact tour costs are

\[
 E_+(t,L,R)=3L+I(t,1,R),
 \qquad
 E_-(t,L,R)=3R+I(t,1,L). \tag{2.1}
\]

A final one-sided path from the center to its first endpoint is dominated by this direct tour. The direct outward leg lies at least as far toward its side until time 1 and has captured that whole side by time 1. The original path cannot reach that endpoint earlier. Its opposite-side survivors cannot be captured during the one-sided portion; after a first endpoint at time at least `t+1`, their earliest opposite endpoint is at least `t+3`. Outward forcing prevents an intervening interior capture after the necessary center return at time at least `t+2>=2`.

Likewise, an entire one-sided returning excursion with `h>=1` is dominated, together with its future, by the direct tour toward that side. The original cannot return to the center before `t+2`; opposite-side survivors then cannot be captured before the opposite endpoint, at time at least `t+3`. The direct tour captures the same side no later and reaches that opposite endpoint at `t+3`.

Consequently one may use only returning excursions with `h<1`, followed eventually by a direct endpoint tour. This is a normalization of the response, not a bound on how many shorter excursions occur.

At `h=1`, the physical triangle touches an endpoint and its same-sign record actually resets to zero. Formula (1.2) at `h=1` is only the **closed interior-trace limit** of `h<1`; it is not the physical endpoint formula. The separate tour guard (2.1) covers the endpoint-touching path.

## 3. Outward forcing truncates the excursion parameter

For a center start `t<=2`, the outward ray after its physical time 2 has fixed radial footpoint `2-t`. Hence `S(t,s)` and the resulting running record are constant for `s>=2-t`, until the endpoint.

If `h>h0=2-t` and `h<1`, shorten the triangle to half-duration `h0`. Both return times are at least 2. The exit record is unchanged and the removed cost is exactly

\[
 2(h-h_0)(L+R')\ge0
\]

for the positive excursion, with the reflected expression for a negative excursion. Once back at the center after time 2, there is no useful delay: the exact remaining cost is

\[
 G_0(L,R)=\min\{3L+R,L+3R\}. \tag{3.1}
\]

It is therefore enough to impose renewal inequalities for

\[
 0\le t\le2,\qquad
 0\le h\le\min\{1,2-t\}. \tag{3.2}
\]

The `h=1` boundary in (3.2) is interpreted as the interior-trace limit described above.

## 4. A center-state potential

Let `Q(t,L,R)` be continuous and Lipschitz on

\[
 [0,2]\times[0,1/2]^2.
\]

Require record monotonicity and the center-hold inequality

\[
 Q_L\ge0,\qquad Q_R\ge0,
 \qquad Q_t+L+R\ge0. \tag{4.1}
\]

Define its continuation symbol by

\[
 \overline Q(t,L,R)=\begin{cases}
 Q(t,L,R),&t\le2,\\
 G_0(L,R),&t\ge2,
 \end{cases}
\]

with the time-2 guard `Q(2,L,R)<=G0(L,R)`. At time 2 the exact continuation may jump upward from the potential; that is a favorable exit jump, not a continuity assumption.

For every parameter choice (3.2), require the two renewals

\[
 \begin{aligned}
 Q(t,L,R)&\le C_+(t,h,L,R)
      +\overline Q(t+2h,L,R'),\\
 Q(t,L,R)&\le C_-(t,h,L,R)
      +\overline Q(t+2h,L',R).
 \end{aligned} \tag{4.2}
\]

Also require the two final-tour guards

\[
 Q(t,L,R)\le E_+(t,L,R),\qquad
 Q(t,L,R)\le E_-(t,L,R). \tag{4.3}
\]

Then `Q` is a valid lower bound on the remaining expected capture cost from every center state. This statement includes paths with infinitely many center excursions and positive-measure center zero sets.

## 5. Countable-excursion proof

The existing outward normalization permits restricting a centered response to a finite completion horizon. Normalize a long excursion or the final one-sided portion as in Section 2. Before the terminal tour, the nonzero set of a continuous Monster path is a countable disjoint union of positive or negative open excursions with endpoints in the closed center zero set.

For each returning excursion, the triangle has no greater accumulated cost and no greater affected exit record. Apply (4.2) to the triangle and then use record monotonicity to obtain the corresponding endpoint inequality for the original excursion. Excursions crossing time 2 use the exact `G0` continuation; there is at most one such excursion. After time 2 all surviving records stay fixed until their own endpoints, so additional returning excursions only add nonnegative cost.

For the zero set, no interval decomposition assumption is needed. The two records are absolutely continuous before an endpoint. On `{m=0}`, their derivatives are zero almost everywhere, since `F(t,0)=1/2` and the records are already at most `1/2`. Therefore the derivative of

\[
 \int_{t_0}^s(L(u)+R(u))\,du+Q(s,L(s),R(s))
\]

is nonnegative almost everywhere on that zero set by (4.1).

The same expression is absolutely continuous before time 2. Its increment over each completed excursion is nonnegative by the endpoint inequality. Countable additivity of its integrable derivative sums the excursion increments and the zero-set contribution. Limits at accumulation times follow from continuity; no minimum excursion duration is used. The time-2 guard permits an upward exit jump. Finally apply (4.3) to the terminal tour. This proves the claimed lower bound.

## 6. One oriented potential is sufficient

To avoid fitting both endpoint orders in every polynomial piece, use one potential `Q_plus`. Impose (4.1), both renewal inequalities with the **same branch on both sides**, the single direct-tour guard

\[
 Q_+(t,L,R)\le3L+I(t,1,R), \tag{6.1}
\]

and the single terminal guard

\[
 Q_+(2,L,R)\le3L+R. \tag{6.2}
\]

For renewals returning after time 2, use `3L+R` as this oriented branch's continuation. Define

\[
 Q(t,L,R)=\min\{Q_+(t,L,R),Q_+(t,R,L)\}. \tag{6.3}
\]

The reflected branch obeys the reflected inequalities. Taking a minimum preserves each renewal:

\[
 \min_i Q_i(z)\le C(z,a)+\min_i Q_i(T(z,a)).
\]

Both branches use the same physical excursion cost and state update for a fixed action. The minimum also preserves the center-hold path inequality and record monotonicity. The first branch supplies the positive final-tour guard; the reflected branch supplies the negative one. Thus Section 4 applies without explicitly partitioning the curved set where the two branches agree.

The precenter certificate from `FINITE_RECORD_BELLMAN_LIFT.md` couples to this potential only through its center trace. One may use a single precenter potential below both `Q_plus(t,1/2,R)` and `Q_plus(t,R,1/2)`, or two precenter branches `A_plus,A_minus` with the respective componentwise center comparisons. In the latter case both initial traces must be at least the desired security, and only `A_plus` needs the positive precenter endpoint guard. Taking minima at each phase gives the required center registration and endpoint exits.

## 7. Finite rational quadratic checks

For a fixed rational P1 field, the outward ray in (1.1) has one fixed light coordinate. Its intersection with the field mesh has finitely many affine pieces. Partition `(t,h,r)` by the piece containing the upper limit `h` and the piece containing the unique crossing of the nonincreasing ray through level `r`.

Each crossing time is affine in `(t,r)` divided by a fixed nonzero field slope. Integrating before and after it shows that `I(t,h,r)` is a rational quadratic polynomial on each chart. The chart inequalities are affine in `(t,h,r)`. A flat field piece is handled without division. Each chart also records the affine update `r'=r` or `r'=S(t,h)`.

Let `Q_plus` be P2 on a finite rational polyhedral subdivision of `(t,L,R)`. On a fixed start piece, integral chart, and continuation piece, the maps

\[
 (t,h,L,R)\mapsto(t+2h,L,R')
 \quad\text{or}\quad(t+2h,L',R)
\]

are affine. Therefore every renewal difference in (4.2) is quadratic in the four variables `(t,h,L,R)`, on an explicitly bounded rational polytope. Returning after time 2 simply substitutes the affine oriented tour continuation. Final-tour and center-registration differences have degree at most two in three and two variables, respectively.

All conditions consequently admit a finite exact replay using `exact_quadratic_polytope.py`, including interior stationary minima and singular cases. LP discovery can instead impose sufficient rational quadratic polar inequalities, or use the exact minimizer to separate violated continuum inequalities. For a fixed field, each pointwise certificate constraint is linear in the potential coefficients.

This gives a finite certificate covering all postcenter turn counts. It does not assert finite termination of a discovery algorithm, nor prove that the unrestricted game's optimum has an exact finite P2 potential.
