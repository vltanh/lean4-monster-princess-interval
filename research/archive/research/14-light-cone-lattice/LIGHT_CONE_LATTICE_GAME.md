# The lattice game in light coordinates: a validated solver and what it shows

Date: 2026-11-14. Status: **numerical results from floating-point linear programs. No new
certificate, no change to the certified bracket, no Lean result.** The exact value \(V\) is still
open. Code: [packages/interval_lightcone](../../packages/interval_lightcone/README.md).

Update 2026-11-15: atomic versions of the laws of Section 6 now have exact upper bounds,
\(V\le1.4241299\) and \(W_1\le1.4245197\), proved in
[ATOMIC_TWO_TURN_UPPER.md](ATOMIC_TWO_TURN_UPPER.md), and the retained field refined to \(n=1024\) gives
the lower bound \(V\ge1.4225745\) ([REFINED_N1024_LOWER.md](REFINED_N1024_LOWER.md)). Where this note says
"certified bracket" it means the earlier \([1.42226,\,1.42472]\). Everything else in this note is numerical.

## Summary

1. A new solver for the lattice game reproduces the five exact clock-grid optima \(U_n\),
   \(n=1,2,3,4,6\), to within \(2\cdot10^{-15}\), and gives \(U_8\), \(U_{16}\), \(U_{24}\),
   \(U_{32}\).
2. On these grids the Monster needs very little beyond one interior turn. Allowing more turns
   lowers the value by \(1.7\cdot10^{-4}\) at \(n=4\), \(7.9\cdot10^{-5}\) at \(n=8\),
   \(5.2\cdot10^{-5}\) at \(n=16\) and \(2.2\cdot10^{-4}\) at \(n=24\) and \(n=32\). The gap does not shrink
   steadily, so the data do not support \(W_1=V\); they bound the difference on these grids.
3. Within the one-turn class, turn levels close to but different from \(b=1\) matter. With only
   \(b=1\) and \(b=2-a\) the value at \(n=16\) is \(7.7\cdot10^{-4}\) higher; adding the two levels
   \(b=1\pm1/n\) recovers the full one-turn value.
4. The repository's exact integer pricing engine returns, for the optimal fields found here at
   \(n=8\) and \(n=16\), the solver's value plus \(1/(4n)\) to rounding. The lattice optimum has
   the same phase structure as the retained \(n=512\) field, but it is not a usable input for the
   lower-bound pipeline: interpolated to finer grids it prices near 1.412.
5. A continuum linear program with piecewise-constant start densities gives explicit Monster laws
   on 16 bins whose computed Princess response is 1.42449 with one-turn paths and 1.42410 when
   two-turn paths that join a one-turn trajectory are added. Both are below the certified upper
   bound 1.424723, but they are floating-point values with the response taken on a mesh, not
   certificates. Placed on a fine grid as atoms, the same laws have the exact bounds of
   [ATOMIC_TWO_TURN_UPPER.md](ATOMIC_TWO_TURN_UPPER.md).
6. Extrapolating the grid values puts \(V\) near \(1.424\), in the upper part of the certified
   bracket \([1.42226,\,1.42472]\). This is an estimate with an uncertainty of about
   \(5\cdot10^{-4}\), not a bound.

The indifference equations behind the densities are in
[ONE_TURN_INDIFFERENCE_EQUATIONS.md](ONE_TURN_INDIFFERENCE_EQUATIONS.md).

## 1. Paths as staircases

Put \(U=t+x\), \(W=t-x\). A 1-Lipschitz path is a curve in the strip \(|U-W|\le2\) along which
\(U\) and \(W\) are both nondecreasing, starting on \(U+W=0\). A unit-speed path is a staircase:
moving right raises \(U\), moving left raises \(W\). Two paths meet exactly where their curves
meet, at time \((U+W)/2\), so the capture time is the time of the first common point.

For a Princess on the positive side with curve \(\Gamma\), write \(w_\Gamma(c)\) for the height at
which \(\Gamma\) crosses the line \(U=c\) and \(u_\Gamma(c)\) for the abscissa at which it crosses
\(W=c\). A Monster leg on \(U=c\) catches her at time \((c+w_\Gamma(c))/2\) and a leg on \(W=c\)
at time \((c+u_\Gamma(c))/2\), provided the crossing lies on the leg and is her first meeting with
that Monster. Her first meeting is a crossing of a vertical leg if she starts to the Monster's
left and of a horizontal leg if she starts to its right.

For the one-turn path \(P_b(a)\) (start \(a\), right until \(t+x=b\), left to \(-1\), right to
\(+1\)) this gives, for a radial Princess with start \(r_0\):

| Path | Condition | Capture time |
| --- | --- | --- |
| \(P_b(a)\) | \(a>r_0\) | \((b+w_\Gamma(b))/2\) |
| \(P_b(a)\) | \(a<r_0\), \(u_\Gamma(-a)\le b\) | \((u_\Gamma(-a)-a)/2\) |
| \(P_b(a)\) | \(a<r_0\), \(u_\Gamma(-a)>b\) | \(b+3\) |
| mirror of \(P_b(a)\) | \(-a>r_0\) | \((-a+w_\Gamma(-a))/2\) |
| mirror of \(P_b(a)\) | \(-a<r_0\) | \((b+u_\Gamma(b))/2\) |

The table assumes \(|a|\le b\le2-a\), and that the Princess is at her endpoint from time 3 on,
which loses nothing by the incoming-front theorem. Her response to a one-turn law is therefore a
Markov problem in \((r_0;U,W)\).

## 2. The lattice game

Let \(\delta=1/(2n)\). The Monster moves on the nodes \((U,W)=(2i,2j)\delta\), one step raising
\(U\) or \(W\) by \(2\delta\), from a start in \(n^{-1}\mathbb Z\). The Princess moves on the odd
points \((2m+1,2k+1)\delta\), so the players never tie. Write \(s=i+j\) (time \(s\delta\)) and
\(d=i-j\) (position \(d\delta\)).

A symmetric ordered Princess law is a radial nodal field \(G(s,d)\), \(0\le d\le 2n\): the mass of
radial paths strictly inside the node. The legal fields are exactly those with

\[
 G(s+1,d-1)\le G(s,d)\le G(s+1,d+1),\qquad G(s,0)=0,\quad G(s,2n)=1,
\]

and the level sets of such a field are odd-lattice staircases. Beyond \(U=2\) the field is fixed
by the front rule of
[GLOBAL_INCOMING_FRONT_COMPLETION.md](../12-global-closure/GLOBAL_INCOMING_FRONT_COMPLETION.md).
The signed field is \(F=(1+G)/2\) on the positive side and \((1-G)/2\) reflected.

A Monster edge captures, at its midpoint time, the mass by which \(F\) leaves the interval between
its running minimum and maximum. The lattice value is

\[
 L_n=\max_G\ \min_{\text{lattice paths}}\ \sum_{\text{edges}} t_{\rm mid}\,(\text{mass captured}).
\]

**Master problem.** Maximize \(c\) subject to the monotonicity constraints and one cut per
generated path. For a path with nodes \(P_0,\dots,P_K\) that visits both endpoints, and for any
choice of record nodes \(P^B_k,P^A_k\in\{P_0,\dots,P_k\}\),

\[
 c\le\frac\delta2+\delta\sum_{k=1}^{K-1}\bigl(1-F(P^B_k)+F(P^A_k)\bigr).
\]

The right side is at least the path's true cost for every legal field, with equality when the
record nodes are the actual ones for the current field. The path must reach both endpoints: if it
is cut off when everything has been caught under the current field, the inequality is false for
other fields. An early version of the solver did this and returned values that were too low.

**Oracle.** The exact minimum over all lattice paths is found by a dynamic program over frontier
states: a node, the side whose record the Monster is currently extending, and the level of the
other record. Two lattice facts make these states sufficient. From a node strictly inside the
visited rank interval, running straight to a frontier dominates any other way of reaching it. At
the right frontier, "right then left" reaches the same node as "left then right" at the same time
with at least as much captured. The state count is (nodes) × (distinct field levels), a few
hundred levels at an LP vertex.

## 3. Agreement with the exact clock-grid optima

The clock-grid optimum \(U_n\) of
[POLYNOMIAL_CLOCK_GRID_LP.md](../12-global-closure/POLYNOMIAL_CLOCK_GRID_LP.md) is the value when
the Monster is on the lattice and the Princess is unrestricted. Against lattice Monsters a
continuous Princess can stay just below and to the left of each grid line. That is the odd-lattice
path with every crossing coordinate raised by \(\delta\), so every capture is later by
\(\delta/2\). This gives

\[
 U_n=L_n+\frac1{4n}.
\]

*Proof for the game "Monster on unit-speed lattice paths, Princess unrestricted".* By symmetry the
Monster's law can be taken symmetric, and then Lemmas 1 and 2 of
[ATOMIC_TWO_TURN_UPPER.md](ATOMIC_TWO_TURN_UPPER.md) reduce the Princess to radial curves that avoid
the lattice points. A lattice Monster path is a union of lattice edges in the \((U,W)\) plane, so
such a curve first meets it in the interior of an edge. The edges she crosses, and their order,
are those of her staircase of cells (Lemma 3 there): the right side of the cell on a right move
and the top side on an up move. So which Monster paths are caught at each move depends on the
staircase alone. The crossing time is below its value at the far corner of the cell, and a curve
that runs just inside the top and right sides of its cells brings all crossings arbitrarily close
to their far corners at once. The odd-lattice path through the centres of the same cells crosses
the same edges at their midpoints, exactly \(\delta/2\) earlier. Hence, for every symmetric
lattice law, the supremum over Princess paths is the maximum over odd-lattice paths plus
\(\delta/2\), and minimizing over laws gives the identity. ∎

That this game is the clock-grid optimum of the repository is the content of
[POLYNOMIAL_CLOCK_GRID_LP.md](../12-global-closure/POLYNOMIAL_CLOCK_GRID_LP.md). The solver confirms
it to rounding error on every grid with an exact certificate:

| \(n\) | exact \(U_n\) | \(L_n+1/(4n)\) from the solver | difference |
| --- | --- | --- | --- |
| 1 | 47/32 = 1.468750000000000 | 1.468750000000000 | 0 |
| 2 | 4893/3376 = 1.449348341232227 | 1.449348341232227 | 0 |
| 3 | 1.441639022955771 | 1.441639022955770 | 7e-16 |
| 4 | 1.438100204530593 | 1.438100204530593 | 0 |
| 6 | 1.434316668462172 | 1.434316668462174 | 2e-15 |

`python3 packages/interval_lightcone/validate_small_grids.py` repeats the comparison.

## 4. New grid values

Floating-point LP values, duality gap below \(10^{-9}\):

| \(n\) | \(L_n\) | \(L_n+1/(4n)\) | \(L_n-1/(4n)\) |
| --- | --- | --- | --- |
| 8 | 1.401192171854722 | 1.432442171854722 | 1.369942171854722 |
| 16 | 1.412922838700238 | 1.428547838700238 | 1.397297838700238 |
| 24 | 1.416604365926588 | 1.427021032592654 | 1.406187699259921 |
| 32 | 1.418473089382883 | 1.426285589382883 | 1.410660589382883 |

By the identity of Section 3, the third column is \(U_n\) and the fourth is the established
lower bound \(U_n-1/(2n)\). Neither improves the certified bracket: the upper column would need
\(n\) of the order of 100 to pass below \(1.424723\). The \(n=32\) run took 91 minutes and ended
with a duality gap of \(10^{-10}\).

## 5. How many interior turns the Monster needs

`lattice_game_turns.py` limits the Monster to \(k\) interior turns before its first endpoint,
followed by the direct sweep, which is the class \(\mathcal B_k\) of
[ONE_TURN_SUBGAME_BRACKET.md](../13-equilibrium-geometry/ONE_TURN_SUBGAME_BRACKET.md) on the
lattice.

| \(n\) | \(k=0\) | \(k=1\) | \(k=2\) | \(k=3\) | unrestricted |
| --- | --- | --- | --- | --- | --- |
| 4 | 1.426136364 | 1.375773180 | 1.375603421 | 1.375600205 | 1.375600205 |
| 8 | 1.445766316 | 1.401270850 | 1.401192862 | 1.401192172 | 1.401192172 |
| 16 | | 1.412974526 | 1.412923484 | | 1.412922839 |
| 24 | | 1.416823 (one-turn family) | | | 1.416604366 |
| 32 | | 1.418695 (one-turn family) | | | 1.418473089 |

The Monster's equilibrium mixture puts mass 0.9966 at \(n=16\) and 0.9941 at \(n=24\) on paths with
at most one interior turn. The remaining paths start near the center or next to another support
path and run to meet the trajectory of a one-turn path head-on, then follow it. Against the
Princess strategy that is optimal for the one-turn game they are strongly profitable: at \(n=16\)
the best two-turn path costs 1.306968 against a value of 1.412975. In the unrestricted optimum
each inward run of the Princess begins with a short outward run; a hand estimate on the retained
field shows that this is what cancels the gain, and the value falls only by the amounts below.

The gap between \(k=1\) and unrestricted play is \(1.7\cdot10^{-4}\), \(7.9\cdot10^{-5}\),
\(5.2\cdot10^{-5}\), \(2.2\cdot10^{-4}\) at \(n=4,8,16,24\). It is small and it is not decreasing.
The \(n=24\) entry for \(k=1\) is from `one_turn_lattice.py`, whose family excludes a turn before
the center from a negative start; at \(n=8\) and \(n=16\) the two one-turn values differ by
\(1.5\cdot10^{-6}\) and \(5\cdot10^{-7}\).

## 6. Turn levels in the one-turn class

`one_turn_lattice.py` solves the family \(P_b(a)\), \(|a|\le b\le2-a\):

| \(n\) | all levels | \(b=1\) and \(b=2-a\) only |
| --- | --- | --- |
| 4 | 1.375773180 | |
| 8 | 1.401272325 | 1.401272325 |
| 16 | 1.412975004 | 1.413742729 |
| 24 | 1.416823264 | |
| 32 | 1.418695442 | |

At \(n=16\), allowing \(b=1\pm1/16\) in addition recovers the full value. In the equilibrium the
levels other than \(1\) and \(2-a\) carry little mass, but removing them costs \(7.7\cdot10^{-4}\).
These paths join a sweep that is slightly ahead of or behind the endpoint sweep, so they reach the
center just before time 1.

`one_turn_continuum.py` solves the continuum game with piecewise-constant start densities and only
the levels \(b=1\) and \(b=2-a\), integrating exactly. Its values are 1.427158, 1.426370,
1.425486, 1.425413 for 4, 8, 16, 32 uniform bins. The response program was checked against the
lattice response for the same law, which converges to it (1.433449, 1.429513, 1.427516, 1.426523
at \(n=16,32,64,128\) against 1.425486). So these two levels cannot reach the certified one-turn
upper \(1.424723\), which uses six levels.

### Continuum laws with a spread of levels and with two-turn paths

`continuum_turn_levels.py` adds densities that are uniform on rectangles of \((a,b)\) with \(b\)
in the mesh columns next to \(b=1\), and the two-turn family

\[
 T_2(c,U_1):\quad\text{start }c,\ \text{right until }t+x=U_1,\ \text{left until }t-x=1,\
 \text{then with the sweep from }-1,
\]

which is the mirror image of \(P_1(-U_1)\) with the start of its run replaced by a run from \(c\).
The law lives on a coarse mesh; the Princess's response is a dynamic program over
\((r_0;U,W)\) on that mesh refined twice, and is then recomputed on finer meshes. With 16 bins and
two level bins on each side of \(b=1\):

| Monster class | LP value | response on meshes refined 4 and 8 times |
| --- | --- | --- |
| one turn | 1.4244766 | 1.4244888 |
| one turn, four level bins | 1.4244698 | 1.4244820 |
| + \(T_2\) with \(|c|<1/16\) | 1.4241368 | 1.4241523 |
| + \(T_2\) with \(|c|<3/16\) | 1.4240983 | 1.4241136 |
| + \(T_2\) with all \(c\) | 1.4240833 | 1.4240990 |

With 8 bins the one-turn value is 1.4249220 (response 1.4250714) and the two-turn family gains
only \(1.4\cdot10^{-5}\). The response rises on the finer mesh because the payoff is quadratic in
a corner position inside a bin; after the first further refinement it is stable to \(10^{-8}\).

Three points about scope. The values are floating-point. The response is taken over staircases
with corners on a mesh, with no bound yet for corners off the mesh. A Princess who has passed the
turning point of \(T_2\) is credited with the largest time that path can still give, which can
only raise the response. So 1.42410 is numerical evidence for \(V\le1.4241\), not a proof.

The proof is supplied for atomic versions of the first and last law of the table in
[ATOMIC_TWO_TURN_UPPER.md](ATOMIC_TWO_TURN_UPPER.md). With the bin masses placed on the grid
\(1/4096\) the exact bounds are \(W_1\le1.4245197\) and \(V\le1.4241299\); the excess over the
continuum responses is \(0.127/N\).

In the optimum the two-turn mass is 0.0055. Most of it starts within \(1/16\) of the center, runs
out, and comes back along \(t+x=U_1\) with \(U_1\) in \((7/8,15/16)\), the last line used by the
mirror images of \(P_1(-c)\). The Princess answers with a short outward run before each inward
run, as on the lattice.

## 7. The equilibrium at \(n=16\) and \(n=24\)

**Monster** (unrestricted game, \(n=16\); mirror images merged): endpoint sweep 0.665; start at
\(15/16\), go to the endpoint and sweep back 0.087; start at \(15/16\) and sweep away from the
near endpoint 0.021; \(P_1(a)\) for \(a\in[1/4,1/2]\) about 0.012 per start; \(S(a)\) for
\(a\in[9/16,7/8]\) 0.006 to 0.010 per start; \(P_1(a)\) for \(a\in[9/16,15/16]\) 0.005 per start;
\(P_1(a)\) for \(a\in[-7/8,-1/4]\) 0.006 per start; starts with \(|a|<3/16\) carry 0.003 in total.

**Princess** (unrestricted game, \(n=16\)): each rank \(q\) runs inward along a line
\(t+r=u(q)\) and outward along a line \(t-r=w(q)\), with \(u\) nondecreasing and \(w\)
nonincreasing in \(q\). Ranks up to about 0.7 reach the center and wait; ranks from about 0.7 to
0.86 run just ahead of the sweep line \(t+r=1\) and turn back before the center, the higher the
rank the earlier; the top 0.14 stay near the endpoint, come in once and return.

**Comparison with the retained field.** On the 767 nodes before the front that the \(n=16\) grid
shares with the retained \(n=512\) field of
[princess_front_n512](../../packages/interval_discovery_certificates/princess_front_n512/README.md),
the two fields differ by a median of \(5.4\cdot10^{-4}\) and by less than 0.01 on 89 % of the
nodes. The large differences (up to 0.35) are confined to the center at \(t\approx0.7\) and to the
late excursion of the endpoint group, where the optimum is not unique. So the two solutions have
the same phase structure. They are not the same kind of object: the retained field is a
full-width profile on grid 64, optimized for the price of its interpolant on the \(n=256\) bank
and then refined.

**Exact pricing of the lattice optima.** `price_normalized.cpp` of
[normalized_native](../../packages/interval_clock_grid/normalized_native/README.md), run on the
optimal fields found here (floored to denominator \(10^9\), with endpoint trace 1), returns the
bank minima

\[
 \frac{45838149486}{32000000000}=1.4324421714375\ (n=8),\qquad
 \frac{91427061649}{64000000000}=1.428547838265625\ (n=16).
\]

These are the solver's \(L_n+1/(4n)\) to within \(5\cdot10^{-10}\), the rounding of the field.
They are exact feasible-dual lower bounds on \(U_8\) and \(U_{16}\) and they confirm the identity
of Section 3 for these two fields. They give no new bound on \(V\).

**The lattice optimum is a poor seed for the lower-bound pipeline.** The common-threshold
(full-width) interpolant of the \(n=16\) optimum has exact bank minima 1.4170340, 1.4141311,
1.4122022 on \(n=32,64,128\), far below the 1.4232347 of the retained field at \(n=512\). A
field that is optimal for the lattice game uses the lattice itself, for example to stay one step
ahead of a sweep, and loses that once it is interpolated. A better certified lower bound needs a
field optimized as a continuous object, as the retained one was, on a finer profile grid, or a
different transfer.

### A three-parameter family for the Princess

`princess_family_lattice.py` restricts the Princess to the ordered law of a mixture of paths

\[
 G(\rho_0,\sigma,\tau):\quad\text{start at radius }\rho_0,\ \text{run outward for a time }\sigma,\
 \text{run inward until time }\tau,\ \text{run outward to the endpoint and stay,}
\]

where a path that reaches the center waits there until \(\tau\). In light coordinates this is a
leg on \(W=-\rho_0\), a leg on \(U=\rho_0+2\sigma\), an optional stretch on the diagonal and a leg
on \(W=\) const. The Monster is unrestricted.

| \(n\) | outward run, lattice steps | paths | family value | \(L_n\) | loss |
| --- | --- | --- | --- | --- | --- |
| 8 | 0 | 116 | 1.398253578 | 1.401192172 | \(2.9\cdot10^{-3}\) |
| 8 | up to 2 | 315 | 1.401183987 | 1.401192172 | \(8.2\cdot10^{-6}\) |
| 16 | 0 | 472 | 1.410241635 | 1.412922839 | \(2.7\cdot10^{-3}\) |
| 16 | up to 3 | 1768 | 1.412877563 | 1.412922839 | \(4.5\cdot10^{-5}\) |
| 16 | up to 8 | 3558 | 1.412892780 | 1.412922839 | \(3.0\cdot10^{-5}\) |
| 24 | up to 6 | 6683 | 1.416567551 | 1.416604366 | \(3.7\cdot10^{-5}\) |

So the Princess needs the short outward run, and with it this family is within \(4\cdot10^{-5}\)
of her unrestricted optimum on these grids. At \(n=16\) the mass by run length is 0.457, 0.423,
0.075, 0.021 for 0, 1, 2, 3 steps and 0.024 beyond; by type, 0.70 reaches the center, 0.28 turns
back before it and 0.02 stays at the endpoint. The mean run is 0.35 steps at \(n=8\) and 0.7 steps
at \(n=16\), the same physical length, about 0.02, on both grids, so the run is a feature of the
continuum game and not a lattice effect.

Together with Section 5 this gives a compact picture of the equilibrium support, up to effects
below \(10^{-4}\) on these grids: the Monster uses \(P_b(a)\) and \(T_2(c,U_1)\), two parameters
each; the Princess uses \(G(\rho_0,\sigma,\tau)\), three parameters.

**The Monster paths that constrain her.** In the solution with the family Princess and the
unrestricted Monster at \(n=16\), the Monster's weight on the active paths is 0.686 on sweeps,
0.135 on endpoint-first paths, 0.176 on one-turn paths, 0.0015 on two-turn paths, and 0.002 on
paths that loiter within about 0.1 of the center for a time of about 0.4, with several short
reversals, and then sweep. The last group is small but it cannot be dropped on the Princess's
side. A family law optimized against one-turn and two-turn Monsters only reaches 1.412883527
against them, and the exact engine then finds a Monster that waits at the center for the arriving
Princesses and holds it to 1.405654829 (the engine's bank minimum 1.421279829 minus \(1/(4n)\);
the Python frontier program gives the same number). So the times at which her paths reach the
center are fixed by the Monster's option to wait there, and any fast surrogate for the Monster's
best response has to contain such paths. Adding only paths that wait in place and then make one
turn is not enough: at \(n=8\) the law that is optimal against those three families (1.401190787)
is held to 1.395093415 by the exact Monster, which moves around near the center while it waits.

**Binned laws lose more for her than for the Monster.** With the exact Monster program at
\(n=16\), the family value is 1.412877424 with one variable per path, 1.410034877 when the paths
are grouped in bins of two cells (start) by two steps (turn time), and 1.407874759 with bins of
four by four. For the Monster, 16 bins already come within about \(10^{-4}\).

This is also a route to a better certified lower bound. A law with binned densities in
\((\rho_0,\sigma,\tau)\) is a legal Princess strategy, its nodal field on any grid is a sum over
its paths, and `price_normalized.cpp` prices that field against every Monster. Two cautions from
the Monster side apply. The law has to be optimized on a grid close to the one on which it is
priced: the 16-bin Monster law that is optimal for atoms on the grid \(1/128\) (response 1.42467
there) has response 1.42658 on the grid \(1/2048\). And the lattice transfer costs \(1/(2n)\), so a
field at \(n=512\) can certify at most about \(V-8\cdot10^{-4}\) and one at \(n=1024\) about
\(V-4\cdot10^{-4}\); the engine takes 16 minutes at \(n=512\) for the retained field and scales
roughly like \(n^4\). The open step is a Monster response program that is exact, or at least
contains the loitering paths, and is fast enough to be called a few hundred times at
\(n\ge512\). With it, a column-generation scheme with one variable per path is feasible: the
reduced costs of all paths come from one pass over the nodes of the active Monster paths.

## 8. Where the value probably lies

The half-offset values converge slowly and not as a clean power series. Three-point fits
\(V-c/n-d/n^2\) give 1.42394 from \(n=4,8,16\) for the unrestricted game, and 1.42398, 1.42433,
1.42411 for the one-turn family from \((4,8,16)\), \((8,16,32)\), \((16,24,32)\). With the gap of
Section 5 this puts \(V\) near 1.424 with an uncertainty of about \(5\cdot10^{-4}\). The
continuum values of Section 6, 1.42449 for one turn and 1.42410 with two-turn paths at 16 bins,
are consistent with this, and their atomic versions give the proved bounds \(V\le1.42413\) and
\(W_1\le1.42452\). With \(n=32\) the unrestricted three-point fits are 1.42381 from \((8,16,32)\)
and 1.42419 from \((16,24,32)\); the second is above the proved upper bound, which shows the size
of the fitting error. The certified
lower bound \(1.42226\) is the price of one profile-grid-64 field minus the transfer loss
\(1/1024\); it does not locate \(V\) inside the bracket.

## 9. Relations seen in the one-turn optimum

Write \(e\) for the mass of the endpoint-sweep pair and \(p\), \(s\), \(\rho\), \(\alpha\) for the
start densities of \(P_1(a)\), \(S(a)\) (\(a>0\)), \(P_1(-c)\), \(S(-c)\) (\(c>0\)). Indifference
of a Princess who runs just ahead of the sweep line about where she turns back gives

\[
 (7+a)\,p(a)+(1-a)\,s(a)=e,\qquad \rho(c)\,(7-c)=e,\qquad \alpha(c)\,(1+c)=e,
\]

on the parts of the support where such Princess paths are used, and inequalities elsewhere. In
the \(n=32\) one-turn optimum the first ratio is 1.0000 for \(a\ge27/32\) and between 1.003 and
1.017 for \(a\in[9/16,13/16]\); the second is 1.0000 at six starts and within 2 % on
\([7/32,21/32]\), but 1.08 on \([11/16,7/8]\); the third is 1.02 to 1.04. These are leading-order
relations on a grid that resolves the layer near \(b=1\) with two or three steps. They are
recorded as a guide to the continuum equations, not as results.

## 10. What to do next

- Refine the continuum program of Section 6 (finer bins in the layer before time 1, more
  two-turn and three-turn families) and pass its best law through the exact atomic bound of
  [ATOMIC_TWO_TURN_UPPER.md](ATOMIC_TWO_TURN_UPPER.md). The present 16-bin law cannot go below
  1.42410 on any grid.
- For the certified lower bound, optimize a full-width profile on a grid finer than 64 with the
  existing pipeline, or find a transfer that loses less than \(1/(2n)\). Lattice optima are not
  usable seeds (Section 7).
- Complete [the indifference equations](ONE_TURN_INDIFFERENCE_EQUATIONS.md) with the layer near
  the center at time 1 and the two-turn paths, and solve them for the thresholds.
