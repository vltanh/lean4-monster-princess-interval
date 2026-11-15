# Moving-front upper and endpoint-return lower obstacles

The exact initial-inward equation in `INITIAL_INWARD_SHEET_CONTACT.md`
provides a lower constraint on an initial field value. It does not
control a Monster that moves the later turning front away from `U=1`.
This note supplies the complementary upper constraint, and a second
lower constraint from an initial inward turn followed by the positive
endpoint. All formulas concern continuous physical capture in the
ordered Princess law. They do not assert that these Monster families
are sufficient for the unrestricted game.

## 1. Common field and trace conventions

Let `F` be a symmetric ordered Princess CDF, continuous in the open
arena with continuous interior endpoint traces, with sticky endpoints
and maximal outward motion after time two. Write

\[
 \mathcal F(U,W)=F((U+W)/2,(U-W)/2),\qquad
 L(a,z)=\mathcal F(1-a,z-1),\quad
 \phi(a)=L(a,a),\qquad 0\le a\le z\le1.
\tag{1}
\]

Then `L` is nonincreasing in both coordinates, and

\[
 \phi(z)\le L(a,z)\le\phi(a).
\tag{2}
\]

The diagonal describes the initial positive-side CDF. Values on the
other two edges must match the prescribed front and outer field. In
particular these are traces of one legal field, not independent
functions.

Endpoint hits reset the corresponding actual survivor record. Integrals
below use interior traces on a boundary; their values at a single time
do not alter an integral. An initial endpoint hit is different and is
kept separate where indicated. Initial endpoint atoms are allowed.

For a descending light ray use the bulk note's moment

\[
 H_b(s)=\int_0^{b+1}\min\{s,F(t,b-t)\}\,dt.
\tag{3}
\]

If `b>1`, the initial part of this auxiliary line is outside the arena;
set `F=1` there. It contributes exactly `(b-1)s`. This is an algebraic
term used in the formula, not additional physical capture time.

## 2. Moving the positive turning front below one

Choose `0<=alpha<=z<=1` with `z>0`. The physical Monster starts at
`1-z`, moves right until

\[
 h=\frac{z-\alpha}{2},\qquad
 m(h)=1-\frac{\alpha+z}{2},
\]

then moves left to `-1` at time `2-alpha`, and right to `+1` at
time `4-alpha`. Its turning light coordinate is `b=1-alpha`. This is
`P(1-z,1-alpha)` in `BULK_CONTACT_AND_CUSP_EQUATIONS.md`.

Separate the part of its descending moment outside the initial patch:

\[
 H^{\rm out}_{\alpha}(s)
   =\frac12\int_0^{3-\alpha}
       \min\{s,\mathcal F(1-\alpha,W)\}\,dW.
\tag{4}
\]

When the outer field is held fixed, (4) is a fixed concave function of
its scalar argument. It remains jointly concave if the outer field is
also a variable.

The exact complete capture cost is

\[
\begin{aligned}
 C_P(\alpha,z)={}&4-\alpha
       -\frac12\int_{\alpha}^{z}L(u,z)\,du
       -\left(4-\frac{\alpha+z}{2}\right)L(\alpha,z)\\
 &+\frac{z-\alpha}{2}\phi(z)
       +\frac12\int_z^1\min\{\phi(z),L(\alpha,s)\}\,ds
       +H^{\rm out}_{\alpha}(\phi(z)).
\end{aligned}
\tag{5}
\]

To verify (5), the outward first leg has lower record `phi(z)` and
upper-survivor record `1-current field`. Its field integral is
`(1/2) integral_alpha^z L(u,z) du`. At the turn the upper record freezes
at `1-L(alpha,z)`. After the negative endpoint, the return reaches the
center at `3-alpha>=2`; maximal outward Princess motion after two
therefore makes the positive survivors wait until the positive endpoint.
The bulk moment identity gives

\[
 4-\alpha-\frac12\int_{\alpha}^zL(u,z)\,du
 -\left(4-\frac{\alpha+z}{2}\right)L(\alpha,z)
 +H_{1-\alpha}(\phi(z)).
\]

On the first portion of this auxiliary descending line, the coordinate
`s` runs from `alpha` to `z`. Monotonicity gives
`L(alpha,s)>=phi(s)>=phi(z)`, so its capped integral is exactly
`((z-alpha)/2)phi(z)`. Splitting the rest at `W=0` gives the final two
terms of (5).

For an interior parameter point `alpha<z`, the requirement `C_P>=V`
is the explicit upper obstacle

\[
\begin{aligned}
 \left(4-\frac{\alpha+z}{2}\right)L(\alpha,z)
 \le{}&4-\alpha-V-\frac12\int_{\alpha}^zL(u,z)\,du
       +\frac{z-\alpha}{2}\phi(z)\\
 &+\frac12\int_z^1\min\{\phi(z),L(\alpha,s)\}\,ds
       +H^{\rm out}_{\alpha}(\phi(z)).
\end{aligned}
\tag{6}
\]

The coefficient on the left is positive. Apart from the prescribed
diagonal and outer field, its right side uses larger first-coordinate
values in the same column, and later second-coordinate values in the
same row. The single integration endpoints have zero measure; (6) is
an algebraic way to isolate the local value, not permission to change
one point while disregarding continuity.

At `alpha=0,z>0`, (5) reduces to the principal-front cost. At
`alpha=z>0`, the first leg vanishes and (5) is the direct-inward
`D_z` cost. The latter is a boundary identity, not an independent local
inversion: `L(z,z)=phi(z)` also occurs in its other terms. At
`alpha=z=0`, the actual physical route is the endpoint sweep. If
`phi(0)<1`, the interior formula's trace exceeds that actual sweep by
`4[1-phi(0)]`; the actual endpoint row must be retained separately.

## 3. An initial inward turn followed by the positive endpoint

There is another family outside (5). For `0<a<=z<1`, let `J_(a,z)`
have vertices

\[
 (0,1-a),\quad
 \left(d,1-\frac{a+z}{2}\right),\quad
 (z,1),\quad(z+2,-1),\qquad d=\frac{z-a}{2}.
\tag{7}
\]

The first turn is a positive valley. Put `f=phi(a)`, `l=L(a,z)`, and

\[
 O_z(f)=\frac12\int_1^{1+z}
              \max\{f,\mathcal F(U,z-1)\}\,dU.
\tag{8}
\]

Its exact physical cost is

\[
\begin{aligned}
 C_J(a,z)={}&z+H_{1+z}(l)
       +\frac12\int_a^zL(a,s)\,ds
       -\frac12\int_0^a\max\{f,L(b,z)\}\,db\\
 &-O_z(f)-\frac{z-a}{2}(f+l).
\end{aligned}
\tag{9}
\]

The first left leg has lower record equal to the current field and
upper-survivor record `1-f`. On the right leg, the lower record is
`l`, and the upper-survivor record is `1-max(f,current field)`.
The right leg's maximum integral splits at `U=1` into the two negative
integrals in (9). At time `z`, the actual positive endpoint hit resets
the upper-survivor record to zero. The remaining descending sweep
contributes `H_{1+z}(l)-z*l`: the removed term is precisely the
exterior portion of (3). Summing these terms proves (9). In particular,
there is no assumption that this last sweep reaches the center after
two; the full moment in (3) prices it at its actual times.

Since the exterior portion has length `z`, for `0<=l_1<l_2<=1` one has

\[
 H_{1+z}(l_2)-H_{1+z}(l_1)\ge z(l_2-l_1).
\]

Consequently the local scalar function in (9) satisfies

\[
\begin{aligned}
 &[H_{1+z}(l_2)-d l_2]-[H_{1+z}(l_1)-d l_1]\\
 &\hspace{25mm}\ge\frac{z+a}{2}(l_2-l_1).
\end{aligned}
\tag{10}
\]

Thus for `a<z`, fixed preceding data and fixed outer field, `C_J>=V`
is a strictly monotone lower obstacle on `L(a,z)`. This bound works at
front plateaus and does not require differentiation. At `a=z>0`,
(9) reduces to the actual endpoint-first row `S(1-z)`, again as a
boundary identity rather than an independent local inversion.

At `a=0,z>0`, the physical route starts at `+1`, goes inward, returns
to `+1` at time `z`, then sweeps to `-1`. It is not the fast endpoint
sweep. If the initial positive endpoint atom has mass
`p_+=1-phi(0)`, formula (9)'s interior trace exceeds this actual route's
cost by exactly `z*p_+`: the trace charges that atom until the return
to `+1`, whereas actual capture occurs at time zero.

## 4. What the coupled obstacles do and do not establish

The principal initial-inward row `I_(a,z)` in
`INITIAL_INWARD_SHEET_CONTACT.md` supplies its earlier-data lower
obstacle, with local inversion slope at least `a/2`. Formula (6)
supplies an opposite-direction upper obstacle. Formula (9) adds a
different lower obstacle that includes a positive endpoint reset.
They are constraints on the same two-dimensional field.

Each cost is concave in its consistent field variables: positive
integrals of `min` are concave, negative integrals of `max` are concave,
and the remaining terms are linear. Therefore their superlevel
constraints, together with the transport inequalities and linear trace
consistency, form a convex feasibility problem. Fixing the outer field
is a useful attachment problem; jointly varying it preserves this
convexity. The partial traces must extend to the same global legal,
symmetric, sticky CDF; equivalently, one can take that full field as the
variable. The displayed local transport and trace constraints alone are
not asserted to characterize global extendibility. The set of such
global extensions is convex.

This statement supplies neither a pointwise least field nor a
uniqueness theorem. The integral terms have mixed signs, and an active
region is not specified in advance. In particular, it does not reduce
all physical Monster responses to these rows. Negative-start turning
families, turns with `b>1`, valleys outside this initial patch, and
additional center excursions remain distinct constraints unless a
separate theorem disposes of them. No finite equilibrium-sufficient
Princess mesh or exact global value follows from this block alone.

## 5. Exact physical regression for the endpoint-return identity

The standalone standard-library replay is

```sh
python -B packages/interval_global_closure/verify_inward_endpoint_obstacle.py \
  packages/interval_global_closure/inward_endpoint_obstacle_replay.json
```

It compares (9) to chronological physical capture for mixtures of
uniform radial Princess laws that remain stationary until time `0`,
`1`, or `2` and then move outward, including genuine stationary endpoint
mass. It checks 81 physical rows, 27 initial-endpoint trace jumps,
27 diagonal endpoint-first reductions and 243 lower-obstacle chords,
using 414 actual contact branches. The saved receipt is
`inward_endpoint_obstacle_replay.json` beside the script. These checks
exercise both endpoint atoms and the earlier center times of the final
sweep; they are a regression for the identity, not an equilibrium
certificate.
