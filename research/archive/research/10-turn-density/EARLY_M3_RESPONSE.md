# Early two-turn sheets with a fixed second characteristic

This extends the upper response construction by a genuine two-interior-turn
monster family. It supplies an explicit nonnegative density, linear payoff
features, and the conditions under which the existing four-scalar princess
response still applies. No matching normalized law is asserted.

The new route is `M3(x;s,1)` from `TWO_INTERIOR_TURN_CDF.md`:

\[
(0,x),\quad ((s-x)/2,(s+x)/2),\quad
((s+1)/2,(s-1)/2),\quad(2,1),\quad(4,-1),
\]

with `|x|<=s<1`. Its second interior turn has characteristic `V=1`.
The two starting signs must be distinguished, even though each route is
itself paired fairly with its reflection.

## 1. Exact first-capture formulas

For a nonnegative princess path with initial position a, write

\[
\alpha(u)=\inf\{t:t+p(t)\ge u\},\qquad
\beta(v)=\inf\{t:t-p(t)\ge v\},\qquad
\phi(v)=2\beta(v)-v.
\]

Let

\[
T_s=\begin{cases}\beta(s),&\phi(s)\le1,\\
\beta(3),&\phi(s)>1.
\end{cases}
\]

Then the sum of the two reflected capture times is

\[
2C_3(+z;s,1)=
\begin{cases}
\alpha(s)+T_s,&a<z,\\
\beta(-z)\mathbf1_{\phi(-z)\le s}
+\beta(1)\mathbf1_{\phi(-z)>s}+T_s,&a\ge z,
\end{cases}                                                    \tag{1}
\]

and

\[
2C_3(-z;s,1)=
\mathbf1_{a\le z}\alpha(z)+\mathbf1_{a>z}T_s
+\beta(z)\mathbf1_{\phi(z)\le s}
+\beta(1)\mathbf1_{\phi(z)>s}.                                  \tag{2}
\]

Every turn equality uses its first contact. For `a=z=0`, both captures
are immediate and that case is handled separately. In particular,
`beta(1)` is not automatically two: a center-wait path can first attain
`V=1` at time one.

For an upper envelope use `beta(1)<=2` and `beta(3)<=4`. The canonical
epsilon paths with final exit `y<1` attain these two endpoint values.
The usual one-sided limits cover `y=1`; actual contact at the boundary
can only decrease the capture payoff. This is an envelope convention,
not an identification of a first inverse with the end of a plateau.

## 2. Replacement of the one-turn line

Keep `g` as the total positive-start M2/M3 marginal and `k` as the total
negative alpha marginal. Replace some of each corresponding `U=1` M2
line by densities `mP(z,s)` and `mN(z,s)` of (1) and (2).

For a positive start and a negative prefix threshold `V=-z`, set
`U=phi(-z)<1`. Relative to the old line, the local four-payoff correction
is

\[
(4+z-U)\int_{s<U}m_P(z,s)\,ds.                              \tag{3}
\]

After that threshold has passed the `U=1` cutoff it becomes
`-4 integral mP`. For a negative start and the positive threshold `V=z`,
the same formulas hold with `4-z-U` and `mN`.

The reflected correction for a turn threshold s is

\[
\begin{cases}
s+\phi(s)-4,&\phi(s)<1,\\
4,&\phi(s)>1.
\end{cases}                                                   \tag{4}
\]

It is present for every positive start and only for `z<a` among negative
starts. Positive starts `z>a` also contribute the alpha correction
`2[alpha(s)-alpha(1)]`, just as the positive early M2 sheet does.

Equation (4) is the useful distinction from early M2. Below `U=1`, the
new routes add a reflected beta price. Above `U=1`, their contribution
is constant in the suffix inverse. They change the first cutoff c, but
add no post-one beta slope.

## 3. An explicit flat-corridor density

Use `sigma=+1` for positive starts and `sigma=-1` for negative starts,
and put

\[
W_3(z,U)=4+\sigma z-U.
\]

For a lower turn r, a nonnegative generator coefficient C(z) gives

\[
m_{r,C}(z,s)=
\frac{C(z)(4+\sigma z-r)}{(4+\sigma z-s)^2},
\qquad r<s<1.                                                \tag{5}
\]

Its cumulative turn mass and full start marginal are

\[
\int_r^U m_{r,C}(z,s)\,ds
=\frac{C(z)(U-r)}{4+\sigma z-U},\qquad
\int_r^1m_{r,C}(z,s)\,ds
=\frac{C(z)(1-r)}{3+\sigma z}.                              \tag{6}
\]

In particular,

\[
W_3(z,U)m_{r,C}(z,U)-\int_r^U m_{r,C}(z,s)\,ds=C(z).       \tag{7}
\]

Suppose k is nondecreasing and `k(r)>=b(z)`, where b is the local
baseline price. Choose `C(z)=k(r)-b(z)` for the lower-edge generator and
add (5) with coefficient `dk(t)` and lower turn t for every `r<t<s`.
Equivalently,

\[
m(z,s)=\frac{(4+\sigma z-r)[k(r)-b(z)]
 +\int_r^s(4+\sigma z-t)\,dk(t)}{(4+\sigma z-s)^2}.          \tag{8}
\]

This is nonnegative and nondecreasing in s. Its exact cancellation is

\[
W_3m-\int_r^Um=k(U)-b(z),\qquad
W_3\partial_Um-2m=k'(U)                                  \tag{9}
\]

on differentiability intervals. The denominator is at least two on the
legal early domain. Integrable unbounded k is allowed: the total start
marginal equals

\[
\frac1{3+\sigma z}\int_r^1[k(s)-b(z)]\,ds,                \tag{10}
\]

and is finite. This follows directly from nonnegative Stieltjes Fubini;
no cancellation of two infinite endpoint values is needed.

For positive starts use `b(z)=p(z)=f(z)+g(z)`. For negative starts use
`b(z)=k(z)+betaP_pre(z)`, where `betaP_pre` includes both positive early
families. As in the signed-early construction, negative starts must lie
below all their own early turn coordinates, so their own reflected
price vanishes on their start band.

## 4. Mixing early M2 and M3 without changing the prefix comparison

On a positive start band, give the M2 construction from
`SIGNED_EARLY_RESPONSE.md` a fraction `1-lambda(z)` of its generator
coefficients and give (8) the fraction `lambda(z)`, with
`0<=lambda(z)<=1`. Use the same baseline p and lower edge for both.
Their local corrections add to `k(U)-p(z)`, independently of lambda.
The same allocation applies to the negative sheets with their corrected
baseline. This allocation is a condition of the construction; two
arbitrary unrelated sheet profiles do not inherit the theorem.

There are two useful lower-edge choices.

* A common fixed edge `r>bP` with `k(r)>=p(z)` uses the lower-edge jump
  comparison already proved in `SIGNED_EARLY_RESPONSE.md`.
* A moving zero edge `r(z)=k^{-1}(p(z))` on one finite start band uses
  `p(z)>=k(z)` to keep every turn legal. Its local derivative is
  `[p(z)-k(U)]_+`, before subtracting the common alpha price. For fixed
  edge geometry, all generators remain linear in the density unknowns.

For step k the crossing jump is allocated only above p(z), as before.
A finite upper start endpoint below the ordinary terminal threshold is
needed when retaining the old terminal tail; the all-the-way-to-one
early-sheet balance has different incoming asymptotics.

Write

\[
J_a(U)=\int_{z>a}[j_P(z,U)+m_P(z,U)]\,dz,
\]

\[
\beta_{P,pre}(V)=\int[j_P(z,V)+m_P(z,V)]\,dz,
\quad
\beta_{N,pre,a}(V)=\int_{z<a}[h_N(z,V)+m_N(z,V)]\,dz.       \tag{11}
\]

All these functions are nondecreasing in their turning coordinate.
The negative-prefix derivative is precisely the previously proved one,
with this enlarged J. The fixed-edge cap/Jensen comparison, or the
moving-zero-edge comparison, therefore still gives one constant
negative-prefix inverse u.

For the positive prefix the first-crossing rule is

\[
k(U)+J_a(U)\ge
k(V)+\beta_{P,pre}(V)+\beta_{N,pre,a}(V),                  \tag{12}
\]

clipped to `max(u,V)<=U<=1`. On a negative start band its corrected
local density cancels to `-J_a(U)` above the lower edge. The same
first-crossing choice remains globally maximizing there. The target is
ordered in V, so these choices form a legal monotone inverse.

For the suffix, use only the M2 parts

\[
\beta_{P,post}=\int j_P,\qquad
\beta_{N,post,a}=\int_{z<a}h_N.                            \tag{13}
\]

Thus the negative late sheet uses `ell+betaP_post`, while the negative
early edge uses `k(z)+betaP_pre`. With the corresponding effective
Gamma nonincreasing, the old one-exit suffix comparison applies
unchanged. The M3 terms in (4) are already fixed once a,u,c and the
prefix are fixed. They contribute no remaining suffix inverse choice.

Under these explicit common-edge, separation, monotonicity, residual
nonnegativity, and Gamma conditions, the unrestricted princess ceiling
is again the four-scalar supremum over

\[
0\le a\le u\le1,\qquad -a\le c\le y\le1,
\]

with (12) as its prefix. The absolute-value reflection comparison and
the legal epsilon realization carry over. All M3 routes capture by
time four, so they preserve the earlier time-five domination used for
integrable density approximation.

The total normalization is still `w0+integral(p+k)=1`. Require the
positive line residual `g-H_jP-H_mP-H_jL>=0` and the negative line
residual `k-ell-H_hN-H_mN-H_hL>=0`. Treating a prefix beta price as
additional mass would double count it.

## 5. The terminal phase and a curved-prefix CDF condition

If a exceeds both M3 start bands and c is below their negative endpoint,
the complete M3 correction relative to the `U=1` M2 lines is zero.
For positive starts, (3)'s post-cutoff value is `-4H`, and (4) contributes
`+4H`. The same cancellation holds for negative starts because every
such z is below a. This remains true for every final exit `y<1`.

Consequently small-start M3 sheets can change the early prefix and its
center excursions without changing the high negative-c stationarity
equations in `NEGATIVE_EXIT_PHASE.md`. This is a precise support
condition, not a claim that every terminal attachment is unaffected.

There is also a direct test of a proposed ordered lower prefix. On a
regular unique-crossing portion of (12), let `a_*(U,V)` solve equality.
If the incoming and first-outgoing rank cutoffs are I(U) and C(V), then

\[
R(U,V)=\min\{I(U),C(V),A(a_*(U,V))\}.                     \tag{14}
\]

The derivative denominator is
`hN(a,V)+mN(a,V)+jP(a,U)+mP(a,U)`. Its U numerator is
`k'(U)+partial_U J_a(U)`, and its negative V numerator is
`k'(V)+betaP_pre'(V)+partial_V betaN_pre,a(V)`.
They are nonnegative. The transport cone therefore follows locally
from the same density signs. Flat equality regions need their own
allowed lower contours; (14) must not select one arbitrary representative
and then exclude the others.

On the diagonal `U=V=t`, equation (12) reduces to

\[
\int_0^a[h_N+m_N+j_P+m_P](z,t)\,dz=0.                    \tag{15}
\]

Before any turn density is active, strict k recovers the ordinary
`min(I,C)` prefix. When a turn band becomes active, (15) restricts the
center mass to initial ranks below its lowest active start. This gives
a checkable source condition for the observed early outgoing waves.
It does not by itself merge arbitrary monster excursions or certify
the unrestricted monster response.

## 6. Computable features and independent checks

`packages/interval_turn_density/m3_early_oracle.py` integrates a unit
generator (5) over a start interval exactly through logarithmic
primitives. The cumulative turn-start mass is

\[
H(t)=(t-r)_+\int_{lo}^{hi}\frac{dz}{4+\sigma z-t}.
\]

The alpha feature is `-integral_r^1 H(t)dt-integral_prefix H(phi(V))dV`.
For a piecewise affine prefix, the reflected feature uses integration
by parts on each segment and the post-cutoff value four. The stable
implementation evaluates its log primitive by a uniformly convergent
series whose argument is at most one third. The feature row is linear
in the original density coefficients.

Verification completed:

* `verify_m3_early.py`: **15,906 exact Fraction checks**, comprising
  3,886 direct signed first-capture identities, 3,886 endpoint ceiling
  inequalities, 3,598 equalities without time-one contact, and 4,536
  flat-density identities and sign checks.
* `m3_early_oracle.py`: **12 independent signed first-capture epsilon
  limits**, with maximum extrapolated feature error `4.12e-18`.

These establish the extension's formulas and feature implementation.
They do not establish that the conditional adjoint has a nonnegative
solution matching a complete lower field, or that every arbitrary
monster path is controlled by that field.

## 7. A complete normalized fixed-geometry attachment

`m3_attached_oracle.py` and `discover_m3_attached.py` apply these formulas
to one full upper law on the existing eleven density bins. Both M3 start
bands are `[0,1/8]`, with first-turn floor `1/4`. The negative early M2
band remains `[1/8,1/2]`, with turn floor `15/16`. Both old late-sheet
bands remain present. This adds no density knots.

Here the small negative-M3 turning band overlaps the later negative-M2
start band. Its correction must therefore be included explicitly. Put

\[
\beta_{3,full}(V)=\int[m_P(z,V)+m_N(z,V)]\,dz
\]

and use the negative-M2 edge numerator

\[
k(15/16)-k(z)-\beta_{3,full}(z).                           \tag{16}
\]

This subtracts the full negative-M3 price, even for initial ranks that
would see only its `z<a` part. Above the negative-M2 edge, its actual
threshold derivative becomes

\[
-J_{P,a}(U)-\int_{z>a}m_N(z,V)\,dz\le0.                  \tag{17}
\]

Below the edge it is the common target-minus-alpha derivative. The edge
condition (16) ensures that its first crossing occurs no later than the
edge. Hence (17) preserves the global maximizing first-crossing rule.
For `a>=1/8`, both terms in (17) vanish and the equality corridor is
genuine. This over-subtraction changes an ordinary density and releases
the removed mass onto the negative line; it is not an extra monster
component. The source is used only in the early sheet. The late Gamma
contains no M3 beta price, by (4).

The saved `m3_attached_discovery.json` is normalized to floating error
below `2e-16`. Its positive-start and negative-start M3 masses are
approximately `0.00290641` and `0.00307835`. Every labelled density and
shape inequality has slack at least `-6.6e-14`. The negative-line tests
retain some deliberately conservative pre-correction inequalities;
those are labelled in the output, and all their multipliers are saved.

The five-round scalar search finds response `1.425201429339405`, versus
its restricted finite-row objective `1.425185256101158`. These are
floating structural diagnostics, not a certified interval for the game.
The law's structural inequality multiplier mass is about `0.00280433`,
and its structural equality multiplier mass is about `0.0153310`.
Neither is silently folded into a princess distribution. In particular,
nonzero monotonicity multipliers do not by themselves exclude all
alternative responses on a flat equality face.

The canonical finite-row dual puts substantial mass at the limiting
`c=y=1` face and has no negative-c extra branch. It has not recovered the
joint continuous interfaces or the singular endpoint tail. A literal
time-one center atom cannot be substituted for those limiting paths:
(1)-(2) would capture that atom early.

`verify_m3_attached.py` checks the entire law by independent segment
intersections, including the cross-price edge subtraction and both late
sheets. Its three cases have maximum extrapolated error `6.0e-15`.
Reducing the curved-prefix interpolation tolerance by a factor of one
hundred changed none of the twenty checked active scores at floating
precision. This is a reproducible admissible-law attachment and an
implementation check, not a matched lower construction.
