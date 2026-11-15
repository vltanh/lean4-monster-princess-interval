# Terminal sources and an incoming-front fixed point

This note concerns an ordered terminal attachment to a specified lower
field. It proves source identities and a conditional contraction for one
front. It does **not** prove existence of a complete matched tail, an
unrestricted response certificate, or a game value. In particular, a
formal fractional history or a fitted pair of logarithmic modes is not
silently treated as an exact solution.

**The ordinary initial segment used in this note cannot be part of a
matched unrestricted law wherever its positive-M2 response is active.**
The exact finite attack in
[INWARD_INITIAL_OBSTRUCTION.md](INWARD_INITIAL_OBSTRUCTION.md) improves
that response whenever a positive-rank band has a nonzero initial
unit-speed outward run. This obstruction applies even if all three
terminal equations below and their outer matching conditions are solved.
The identities and conditional contraction remain valid for their stated
path class. A viable replacement must also change the initial phase;
[INITIAL_INWARD_CDF.md](INITIAL_INWARD_CDF.md) gives the corresponding
curved-field equation and moving support boundary.

## 1. Retained low ranks and ordinary high ranks

Retain ranks of total mass `q0=1-rT` from an ordered radial field `R_old`:

\[
 L(U,V)=\min\{R_{\rm old}(U,V),q_0\}.
\]

Choose `xT>0` so that every retained initial position is at most
`aT=1-xT`. Assume that the retained field is zero on outgoing rows
`V>=1-xT`. This is an actual outgoing gap, not a replacement of a narrow
positive layer by an atom at `V=1`.

Parameterize the new high ranks by their initial deficit `x`. Write

\[
 a=1-x,\qquad u=1-h(x),\qquad c=-1+d(x),\qquad
 r(x)=\Pr(\hbox{high initial deficit}\le x).
\]

Thus `r(0)=0`, `r(xT)=rT`, and the mass element is `dr(x)`. The ordinary
path first moves outward, then inward, then outward to its endpoint.
Its first and second turn times are `(x-h)/2` and `(d-h)/2`, and its
endpoint arrival time is `d`. Sufficient within-tail conditions are
positive increasing `r,d,h`, `0<h<x<d`, and `h+d<2`.

The boundary high path dominates every retained low path if it starts
at or above the largest retained initial position and its valley lies
at or above that low quantile. The single corner condition is

\[
 R_{\rm old}(1-h_T,-1+d_T)\ge q_0.                 \tag{1}
\]

Indeed, the initial outward segment dominates by the common speed bound.
Before the valley, the high incoming segment has speed `-1`; after the
valley its outgoing segment has speed `+1`. The low path's Lipschitz
bound and the valley comparison therefore give domination on both
segments. This argument also allows a small initial support gap.

## 2. The two source functions

Use the common integration domain `-1<=V<=1`. Extend the low CDF by `q0`
below the full physical lower boundary, including the spatial endpoint
edge for `U>1`, and by zero above the upper boundary. Define

\[
 Q(x)=\int_{-1}^1[L(1+x,V)-L(1,V)]\,dV,
 \qquad
 \Omega(\eta)=\int_{-1}^1[L(1,V)-L(1-\eta,V)]\,dV. \tag{2}
\]

Both are nonnegative. `Q` is post-one incoming flux; `Omega` records
retained low mass still moving inward just before `U=1`. The negative-M1
four-cost contains `-Omega`. This sign convention is fixed throughout
this note.

For a triangular affine field these sources are piecewise quadratic.
`packages/interval_cdf_discovery/terminal_low_sources.py` finds the full
slice arrangement, including intersections of triangle edges with
`R=q0`, and checks the quadratic on each resulting interval exactly.
It also checks the outgoing gap and extracts the affine order gate (1).

## 3. Exact endpoint-normalized equations

Put `tau=d^{-1}(x)` and `E(x)=r(tau)`. In the continuous setting, equality
of positive M1 and M2 costs gives

\[
 (8-2x)E(x)=x[3-r(x)]+Q(x).                       \tag{3}
\]

Positive M1 indifference with the endpoint sweep gives

\[
 \int_0^x[d(t)+h(t)]\,dr(t)
 =3x+Q(x)+xE(x)+\int_0^{\tau}h(t)\,dr(t).         \tag{4}
\]

The endpoint sweep's four-cost is

\[
 4C_{\rm end}=4+\int_{-1}^1L(1,V)\,dV
                     +\int_0^{x_T}d(t)\,dr(t).   \tag{5}
\]

For negative M1, define

\[
 H_r(\eta)=(8-2\eta)r(\eta)+\int_0^\eta r(t)\,dt-3\eta,
 \qquad J(x)=\int_0^x[d(t)-t]\,dr(t).
\]

Its exact endpoint difference is

\[
 4[C_\ell(1-\eta)-C_{\rm end}]
 =H_r(\eta)-\Omega(\eta)
       -J\bigl(\min\{h^{-1}(\eta),x_T\}\bigr).    \tag{6}
\]

Consequently incoming-front indifference is

\[
 J(x)=H_r(h(x))-\Omega(h(x)).                     \tag{7}
\]

One direct derivation of (6) splits high ranks according to whether
`h(t)<eta`. If `eta=h(x)`, their contribution to `N(1)-N(1-eta)` is

\[
 J(x)+\eta r_T-\int_0^\eta r(t)\,dt.
\]

The retained low contribution is `eta*q0+Omega(eta)`. Substitution in
the full-field negative-M1 identity yields (6). For larger `eta`, the
high-rank integral stops at `xT`; it must not be extrapolated to a
nonexistent high branch.

The source identities have both an independent analytic audit and
1,875 Fraction checks in
`packages/interval_turn_density/verify_terminal_sources.py`. The checks
compare with direct first intersections and include nonzero `Q`, nonzero
`Omega`, and both sides of the incoming cutoff. Atomic fixtures avoid
ambiguous incoming rows; applications with atoms require the strict
horizontal and closed spatial traces from the full-CDF identities.

## 4. An exact contraction when r and w=d+h are supplied

This part does not presume an exact asymptotic history. Suppose
`0<xT<=10^-5`, `r(0)=0`, and, throughout the relevant interval,

\[
 \frac{4}{5\sqrt x}\le r'(x)\le\frac1{\sqrt x},
 \qquad 3\sqrt x\le w(x)\le5\sqrt x.
\]

Assume `Omega(0)=0` and `0<=Omega'<=8000` on
`0<=eta<=(4/25)xT^2`. Define

\[
 A_r(\eta)=H_r(\eta)-\Omega(\eta),\qquad
 W(x)=\int_0^x[w(t)-t]\,dr(t).
\]

Consider the closed set of continuous functions

\[
 \frac{x^2}{50}\le h(x)\le\frac{4x^2}{25},
 \qquad \|h\|_* =\sup_{0<x\le x_T}\frac{|h(x)|}{x^2}.
\]

On this set define

\[
 T[h](x)=A_r^{-1}\!\left(W(x)-\int_0^x h(t)\,dr(t)\right). \tag{8}
\]

The derivative assumptions imply `1.6*sqrt(x)<=r(x)<=2*sqrt(x)` and

\[
 A_r'(\eta)=(8-2\eta)r'(\eta)-r(\eta)-3-\Omega'(\eta)
 \ge\frac6{\sqrt\eta}.                            \tag{9}
\]

They also give

\[
 \frac{12}{5}x-\frac8{15}x^{3/2}\le W(x)\le5x,
 \qquad
 0\le\int_0^xh\,dr\le\frac8{125}x^{5/2}.
\]

At the lower trial value `eta=x^2/50`, `A_r(eta)` is less than
`2.264*x`; the argument in (8) is greater than `2.398*x`.
At the upper trial value `eta=4x^2/25`, `A_r(eta)` exceeds
`5.107*x`, while that argument is at most `5*x`. Thus (8) is defined
and preserves the stated interval.

For two candidate fronts, (9) bounds the inverse derivative by
`(2/5)x/6`. Moreover,

\[
 \left|\int_0^x(h_1-h_2)\,dr\right|
 \le\frac25x^{5/2}\|h_1-h_2\|_*.
\]

Therefore

\[
 \|T[h_1]-T[h_2]\|_*
 \le\frac2{75}x_T^{3/2}\|h_1-h_2\|_*.             \tag{10}
\]

This proves a unique fixed point and geometric convergence in the
weighted norm. At `xT=2^-18`, the displayed contraction factor is less
than `1.987e-10`. It is a conditional existence theorem for `h`, with
the supplied `r,w,Omega`; it does not establish (3) or (4).

The fixed point is increasing because differentiating (7) gives
`h'=(w-h-x)r'/A_r'(h)>0`. In fact `h'<=x/3`. Thus `d=w-h` is also
increasing if, in addition, `w'>=1/sqrt(x)`. These extra hypotheses must
be checked for any specified outer representation.

## 5. Extending negative-M1 indifference through the whole last slab

The incoming equality only covers `eta<=hT`. For `hT<=eta<=xT`, (6)
requires the low source

\[
 \Omega_*(\eta)=H_r(\eta)-J(x_T).                 \tag{11}
\]

Suppose the old source is strictly increasing, the right side is
increasing, and their values agree at both ends of this interval. Then
the monotone change of the low incoming coordinate

\[
 \phi(1-\eta)=1-\Omega_{\rm old}^{-1}(\Omega_*(\eta)),
 \qquad L_{\rm new}(U,V)=L_{\rm old}(\phi(U),V)    \tag{12}
\]

is continuous at both slab edges and preserves the CDF cone. The common
domain extensions in Section 2 are essential here. The outgoing gap
makes the positive-side extension zero, and the retained initial support
makes the negative-side extension `q0`.

The map leaves `U=1`, the post-one field, and the low initial distribution
unchanged. For terminal positive starts, all retained low ranks already
lie inside their initial outward light line, so their columns
`V<=-aT` are identically `q0`. Thus (12) preserves the source and low
terms in (3) and (4). At `eta=hT`, it is the identity, retaining the
high-tail order gate. It enforces (6) throughout the remaining slab.

The outer endpoint condition in this construction is the scalar

\[
 \int_0^{x_T}d\,dr
 =(8-x_T)r_T-3x_T-\Omega_{\rm old}(x_T).          \tag{13}
\]

It is a genuine matching condition on outer data. It cannot be removed
by an assertion that a narrow incoming layer is negligible.

## 6. Current fixed-field data and unresolved obligations

For `initial_inward_candidate.json`, with `xT=2^-18` and
`q0=.996638896119`, exact extraction gives

\[
 Q(x)=.5508756406272x-195.1319606689792x^2.
\]

Near zero,
`Omega(eta)=7793.523194296427*eta+1.502765040705919e9*eta^2`.
The source is a different quadratic on later subintervals; the full
arrangement is retained by the extractor. Its early quadratic is valid
far beyond the approximately `9.10e-13` incoming scale of the diagnostic
tail.

A floating outer fit using the fractional correction series and one
antiperiodic logarithmic Fourier pair matches the saved tail mass and
the corner gate. It has positive sampled front derivatives. The pair
does not exhaust the infinite-dimensional endpoint freedom and is not
an exact asymptotic manifold. A tiny history join was corrected explicitly
before evaluating its costs.

For that diagnostic, terminal positive f/g costs differ from the endpoint
cost by at most about `1.04e-12`. The old negative-M1 dip is removed, but
negative-M1 has positive slack up to about `.00155` before applying (12).
The frozen-data scalar (13) misses by about `6.36e-9` in four-cost units.
Allowing a small retained-mass change moves its scalar root by roughly
`7.94634e-10`; this is an outer matching variable, not proof that the
coupled tail equations have an exact solution.

Even within this conditional path class, (3) and (4) still need an exact
endpoint solution compatible with the supplied outer profile, the
hypotheses of Section 4 must be certified for that solution, and (13),
the corner gate, and the source-warp range must all hold together.
Solving those obligations would not remove the ordinary-prefix attack
stated at the start of this note. The unrestricted construction now needs
a curved initial phase and its additional source terms; the ordinary
fixed-point calculation is preserved as a conditional component only.
