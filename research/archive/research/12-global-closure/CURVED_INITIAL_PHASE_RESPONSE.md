# Three directional runs in a curved initial phase

This is a conditional response theorem for a supplied Princess field. It
allows nonpolynomial incoming phases and an arbitrary fixed outer
continuation depending on **both** survivor records. It does not prove
that an unrestricted optimal Princess has finitely many such phases, or
that an arbitrary legal initial field can be replaced by one satisfying
these conditions without lowering its security.

## 1. Phase and record conventions

Use physical light coordinates

\[
 U=t+x,\qquad W=t-x,
\]

and write the signed Princess CDF as `F(U,W)`. It is continuous on the
phase closure, has values in `[0,1]`, and obeys transport

\[
 F_U\ge0,\qquad F_W\le0.
\]

A unit rightward Monster movement increases only `U`, at rate two; call
it `R`. A unit leftward movement increases only `W`, at rate two; call it
`L`. Both coordinates are nondecreasing for every legal Monster path.

An incoming scalar record interval is `[ell,h]`, with
`0<=ell<=F(U_0,W_0)<=h<=1`. The two surviving rank masses are
`(ell,1-h)`. The running cost rate is

\[
                         1+\ell(t)-h(t).                 \tag{1}
\]

All arguments use the actual current records, including any earlier
capture. A common future contributes a continuous, coordinatewise
nondecreasing, concave function `Q(ell,1-h)` of the two survivor masses.
Every fixed bounded physical future has this property, since its two
clock costs are integrals of minima of the incoming record and a fixed
future record. The exact outer value has the property too: an infimum of
concave functions is concave. No symmetry of that future is required.

The phase must have the following geometric property: the coordinate
box between any two comparable points used in a replacement is contained
in the phase closure and in the open physical arena. In particular, this holds
in the initial triangle

\[
 \mathcal T=\{0\le U\le1,\ -1\le W\le0,\ U+W\ge0\},       \tag{2}
\]

and in any intersection of characteristic coordinate strips and time
strips contained in it, for paths whose initial position is strictly
inside the arena. Their coordinate boxes cannot reach the sole arena
endpoint corner of (2). All compared segments therefore avoid physical
endpoint hits. Actual endpoint starts, including their capture resets,
are separate boundary cases; no endpoint atom is replaced by its interior
trace, and the local theorem is not applied across an endpoint reset.

## 2. A curvature condition and the theorem

Assume on the smooth interior of the phase that

\[
 \boxed{
 F_U>0,\qquad F_{UU}\ge0,\qquad F_{UW}\ge0,\qquad
             (\log F_U)_{UW}\le0.}                       \tag{3}
\]

It is enough that the following equivalent transition-map conditions
hold on every relevant coordinate box. For a bottom edge `W=W_0`, let

\[
 s=F(u,W_0),\qquad u=\chi(s),\qquad
 H_W(s)=F(\chi(s),W),\quad W_0\le W\le W_1.
\]

The inverse `chi` is increasing and concave; each `H_W` is increasing
and concave; and `H_W'(s)>=1` wherever the derivative exists. The
transition-map statement also makes sense with weak derivatives. We
require horizontal strict increase on the intervals that are inverted;
a constant first horizontal leg is unproductive and is treated directly
below. Singular endpoint derivatives are permitted when these maps have
continuous traces.

Indeed, (3) implies

\[
 H_W'(s)=\frac{F_U(u,W)}{F_U(u,W_0)}\ge1,
\]

and

\[
 \operatorname{sign} H_W''
 =\operatorname{sign}\left[
    (\log F_U)_U(u,W)-(\log F_U)_U(u,W_0)\right]\le0.       \tag{4}
\]

The convexity of the bottom-edge field gives the concavity of its
inverse. Thus the differential conditions are a sufficient analytic
criterion; differentiating a merely undifferentiated asymptotic formula
is not part of this theorem.

**Theorem.** Fix the physical entry and exit states and times in one
such phase, the incoming records, and a common concave monotone future
cost `Q`. Every admissible Monster segment is weakly dominated by one
with at most three unit-speed directional runs. If three remain, their
order is `L-R-L`. Zero-duration runs are allowed. The replacement has
exactly the same physical exit state and time, and its integrated cost
plus `Q` is no larger. It need not preserve the two exit records.

The reflected-complement version applies if
`1-F(W,U)` satisfies (3); it leaves at most `R-L-R`.

## 3. The exact cost of an R-L-R triple

It suffices first to consider a finite axis path. Isolate an `R-L-R`
triple in the coordinate rectangle

\[
 U_0\le U\le U_1,\qquad W_0\le W\le W_1,
 \qquad D=W_1-W_0>0.
\]

Its variable middle coordinate is `u`:

\[
 (U_0,W_0)\to(u,W_0)\to(u,W_1)\to(U_1,W_1).              \tag{5}
\]

The duration `T=(U_1-U_0+D)/2` is fixed. Put

\[
 s=F(u,W_0),\quad u=\chi(s),\quad
 g(s)=F(u,W_1),\quad F_e=F(U_1,W_1).
\]

Only the **productive interval**

\[
                         s>h,\qquad g(s)<\ell             \tag{6}
\]

requires an exchange. Because both `s` and `g(s)` increase, its closure
is an interval. On it the first right leg improves the upper record and
the left leg improves the lower record. The final right leg may or may
not improve the upper record again.

Define

\[
 \begin{aligned}
 C(s)&=\int_{W_0}^{W_1}\min\{\ell,F(\chi(s),W)\}\,dW,\\
 I_0(s)&=\int_{U_0}^{\chi(s)}\max\{h,F(U,W_0)\}\,dU,\\
 I_1(s)&=\int_{\chi(s)}^{U_1}\max\{s,F(U,W_1)\}\,dU.
 \end{aligned}
\]

Twice the prefix cost, after removing the fixed term `2T`, is exactly

\[
 S(s)=(\chi-U_0)\ell-I_0+C-Ds
                  +(U_1-\chi)g-I_1.                    \tag{7}
\]

This formula includes every running-record crossing. In particular it
does not approximate a record by its value at a vertex.

Let

\[
 v(s)=\min\{U_1,\ F(\,\cdot\,,W_1)^{-1}(s)\}.
\]

When the requested level is above the whole final edge, define `v=U_1`.
On the productive interval, `g(s)<s`, so the crossing is after `chi`.
The final edge contributes the derivatives

\[
 I_0'(s)=s\chi'(s),\qquad
 I_1'(s)=-s\chi'(s)+v(s)-\chi(s).
\]

Differentiating (7) therefore gives the particularly useful identity

\[
 \boxed{
 S'(s)=(\ell-g)\chi'+C'
       +(U_1-\chi)(g'-1)+U_1-D-v(s).}                    \tag{8}
\]

These identities hold almost everywhere, including fields with flat
vertical portions. Equivalently they follow by differentiating the
integrals of maxima and minima and using their one-sided derivatives.

## 4. Every term in the derivative decreases

On (6), the factors `ell-g` and `chi'` are nonnegative and nonincreasing,
so their product is nonincreasing. Each transition map `H_W` is concave;
therefore `min(ell,H_W)` and its integral `C` are concave, and `C'` is
nonincreasing. The factors `U_1-chi` and `g'-1` are likewise nonnegative
and nonincreasing. Finally, `v(s)` is nondecreasing.

Thus the right side of (8) is nonincreasing. The whole prefix cost is
concave in the peak-rank parameter `s`. This proof uses neither spatial
affinity nor a polynomial field.

The exit survivor records are

\[
                         (g(s),\ 1-\max\{s,F_e\}).        \tag{9}
\]

Both components are concave functions of `s`. Composing them with the
concave coordinatewise nondecreasing future `Q` preserves concavity.
Consequently the entire prefix-plus-future cost is concave on the
productive interval and attains a minimum at an endpoint of its closure.
Continuous limits cover a crossing exactly at an old record or at `F_e`.
The minimum of a concave function on the compact interval need not be
unique; existence of an endpoint choice is all that is used.

## 5. Productive endpoints and clipping cases

An endpoint of the feasible productive interval has one of four forms.

* `u=U_0`: the first right leg has zero duration.
* `u=U_1`: the last right leg has zero duration.
* `s=h`: the first right leg sets no new upper record.
* `g=ell`: the middle left leg sets no new lower record.

In the first two cases there are already at most two directional runs.
For `s<=h`, including the third boundary case, replace (5) by left then
right on the same rectangle. Every new lower rank is reached no later:
the left leg now has the smaller fixed coordinate `U_0`. All its field
values are below the incoming upper record. On the final right edge,
queries after `U=u` occur at exactly their old absolute times, and before
that point their values are at most `g<=s<=h`. Thus no upper capture is
delayed, and both records and their integrated cost weakly improve.

For `g>=ell`, including the fourth boundary case, replace (5) by right
then left. The old middle and final legs captured no lower rank. The
new right-first upper captures occur no later along the bottom edge,
where the field is no smaller than on the top edge. The subsequent
left leg ends at `F_e>=g>=ell`, so it captures no lower rank either.
Again all cost and future comparisons have the required direction.

These direct arguments also cover an initially unproductive triple.
If a horizontal edge is constant, its corresponding productive upper
case is absent and the same direct deletion applies. Zero vertical
length is removed by merging adjacent right runs. There is no division
by a zero field slope in any of these cases.

It follows that every `R-L-R` triple can be replaced by at most two
runs, with the same physical endpoints and duration and no greater
complete cost. Use the **entire fixed later physical path** for `Q`
whenever applying this exchange. The two records may change, but the
comparison already accounts for that fixed later path. If the terminal
`Q` is an abstract concave monotone function, prepending a fixed physical
segment preserves these properties: its running cost is an integral of
record minima, and its exit records are componentwise minima of the
incoming records and fixed history records. Composition with `Q` is
therefore still concave and monotone. Repeated deletion is justified for
the full stated class of terminal functions.

## 6. Finite words, arbitrary paths, and first exits

Merge consecutive equal directions in a finite axis word and repeatedly
remove an `R-L-R` triple. The number of runs strictly decreases. An
alternating word with no `R-L-R` has at most three runs; its only
three-run form is `L-R-L`.

An arbitrary Lipschitz path admits monotone axis-staircase approximations
with the same endpoint states and times. On each small time interval,
use its exact increments of `U` and `W` in either axis order. The
coordinate-box hypothesis keeps every approximation in the phase.
Uniform continuity of `F` gives convergence of both running records and
integrated costs. The fixed future cost is continuous on the compact
record domain. Apply the finite-word result and take a subsequence of
the at most three nonnegative run durations. This proves the theorem
without a finite-switch or non-Zeno assumption.

For the initial triangle (2), preserve the old exit point and time.
A replacement may touch a characteristic exit boundary earlier and
then move along it to that old exit. This is a legal physical path:
the initial and outer fields share the same trace. Keeping that boundary
portion and the old outer suffix proves the required comparison. If one
instead attaches an optimal outer continuation at the **first** exit,
its cost can only improve. Thus the theorem genuinely reduces the
initial first-exit problem and does not assume the two records are
summarized by one number.

If one whole initial triangle satisfies (3), its unknown prefix can
therefore be optimized over the finite directional list `L-R-L`, with
zero runs covering all shorter cases, plus the separate actual endpoint
and center starts. Entry position, exit point and the split of the two
left runs remain continuous variables. The result is an exact
finite-dimensional response optimization for this **given phase and
outer continuation**, not a finite-dimensional parametrization of all
optimal Princess laws.

There is also a direct sufficient lower-certificate form. Let `P` be any
already certified lower bound for the outer continuation, continuous and
increasing concave in the two records at every fixed exit state. If
`prefix cost + P(exit state, exit records) >= c` for every at-most-three-run
prefix in the **phase closure** ending at the chosen boundary exit, and
for the separate initial boundary starts, then every unrestricted Monster
response has cost at least `c`. These checks include prefixes that touch
the exit boundary earlier and then travel along it to the chosen exit.
One cannot truncate them at their first boundary touch for an arbitrary
`P` unless a boundary subsolution inequality is also known; the earlier
first-touch argument used the exact outer value. Apply the exchange with
`Q=P` to the original prefix; its actual outer cost is at least `P`.
This uses a finite list of continuous parameter families and a verified
outer lower bound. It does not require guessing the exact outer optimizer
or fitting a new unknown potential throughout the initial patch.

## 7. Nonpolynomial sufficient classes

A useful subclass is

\[
             F(U,W)=A(U)R(W)+B(W),                       \tag{10}
\]

where `A` is increasing and convex, `R` is positive and nondecreasing,
and the whole field satisfies transport `A R'+B'<=0` and the CDF range
bounds. Here `F_U=A'R`, so the logarithmic mixed derivative is zero.
The inverse-and-transition-map proof applies with no need to make
`B` affine. This includes genuinely curved rank-one characteristic
families.

For the additive class `F=A(U)+B(W)`, convex `A` suffices to eliminate
`R-L-R`. If `-B` is also increasing convex, the reflected theorem
eliminates `L-R-L` as well, leaving at most two directional runs.
Endpoint square-root traces are not excluded by these shape conditions:
`A(U)=A(1)-c sqrt(1-U)` is increasing and convex and has a continuous
endpoint value. All global compatibility, range and attachment
conditions still have to be checked for an actual field.

For smooth initial coordinates

\[
 L(a,z)=F(1-a,z-1),
\]

a sufficient form of (3) is

\[
 \boxed{-L_a>0,\quad L_{aa}\ge0,\quad L_{az}\le0,
                   (\log(-L_a))_{az}\ge0.}              \tag{11}
\]

The logarithmic condition is substantive; neither the transport signs
nor one mixed-derivative sign alone supplies this proof.

## 8. Exact incoming power layers satisfy the criterion locally

This section concerns an **exact** power phase, not a formal germ with
an undifferentiated remainder. Fix an interior compact interval of
initial positive positions, enlarged slightly on both sides. Suppose
on that enlarged band the Princess paths are

\[
 r_\xi(t)=\xi+t-\kappa(\xi)t^\gamma,
              \qquad \gamma>1,                         \tag{12}
\]

for sufficiently small `t>=0`. Assume `kappa` is positive `C^3` and the
initial signed density `rho=f'` is positive `C^2`, both bounded away
from zero on the enlarged band, with their displayed derivatives
bounded. Take time small enough that

\[
 1-\kappa'(\xi)t^\gamma>0,\qquad
                    \gamma\kappa(\xi)t^{\gamma-1}<2.
\]

These inequalities ensure ordering and the unit speed bound in this
phase. Its signed CDF is `F(U,W)=f(xi)`, where, with
`t=(U+W)/2`, the initial label solves

\[
 \xi-\kappa(\xi)t^\gamma=-W.
\]

Set `p=gamma-1>0`, `D=1-kappa'(xi)t^gamma`, and
`c(xi)=gamma rho(xi)kappa(xi)/2`. Implicit differentiation gives

\[
 \xi_U=\frac{\gamma\kappa(\xi)t^p}{2D},\qquad
 \xi_W=-\frac1D+\xi_U,\qquad
                     F_U=\frac{c(\xi)t^p}{D}.            \tag{13}
\]

All estimates below are uniform on a smaller compact band of `-W`.
Since `xi=-W+O(t^(p+1))`, direct differentiation of (13) yields

\[
 \begin{aligned}
 F_{UU}
   &=\frac p2c(-W)t^{p-1}+O(t^{2p}),\\
 F_{UW}
   &=\frac p2c(-W)t^{p-1}+O(t^p+t^{2p}),\\
 (\log F_U)_{UW}
   &=-\frac{p}{4t^2}+O(t^{p-1}).
 \end{aligned}                                           \tag{14}
\]

For the last line, write
`log F_U=log c(xi)+p log t-log D`. The first and third terms have mixed
second derivatives `O(t^(p-1))`; the middle term supplies the displayed
negative leading term. Bounded coefficient derivatives and `D` bounded
away from zero justify these differentiated estimates directly.

Because `c` is uniformly positive, every sign in (3) holds for some
uniform `0<t<=delta` on that compact band. This includes the golden
power `gamma=(1+sqrt(5))/2`; it does not rely on `gamma` being rational.

For a geometrically admissible phase, choose `0<a<b<1` in the smaller
band and take

\[
 -W\in[a,b],\qquad 0\le U+W\le2\delta,                  \tag{15}
\]

with `delta` small enough to remain in (2) and in the enlarged label
band. This region has the coordinate-box property. Monotone light
coordinates and increasing physical time give a single visit to it.
The trace at `t=0` is continuous, although `F_U=0` there; productive
horizontal variations lie at `t>0`, and the boundary cases follow by
continuous limits. Therefore the entire visit has the three-run
replacement proved above. No artificial initial unit outward segment
has been inserted into the Princess path.

The constant `delta` can shrink as the label band approaches an
endpoint or a singular coefficient. Nothing here makes it uniform as
`xi` approaches one. Consequently this local power-layer result does
not imply a finite global phase cover.

## 9. Coupling and the remaining global gate

If a supplied initial field is covered by finitely many such
coordinate-box phases with a one-way transition order, apply the theorem
backwards, always retaining the actual later continuation. A bound of
three directional runs per visited phase follows. The fields and
continuations must be those of the same legal ordered Princess law.
A matching upper law and all outer response constraints remain part of
an equilibrium certificate.

For clarity, a useful exact outer terminal is available independently
of any early-center pruning. Maximal outward motion after time two puts
all Princesses at endpoints by time three. At an admissible state
`(3,x,ell,r)`, the exact remaining cost is

\[
 \min\{(1-x)(\ell+r)+2\ell,
        (1+x)(\ell+r)+2r\}.                              \tag{16}
\]

At an abstract interior state, first update both records against the
current half-CDF value; actual endpoint resets are also applied. Thus a
future completed by time seven suffices for the statewise outer problem.
At first center contact, its record guard is the exact center value at
`(min(ell,1/2),min(r,1/2))`. Positive precenter histories have the simpler
pair `(1/2,r)`. These facts make the two-record continuation in this note
a concrete exact object, rather than a guessed one-record boundary term.

The remaining global step is **phase existence or a security-preserving
replacement into such a phase class**. This note proves neither. The
conditional square-root boundary law and active-valley estimates must
still be imposed on any proposed phase construction; admitting a
square-root trace alone does not establish their compatibility. The
published finite upper laws contain broad initial-inward support, but
those sampled rows are not an asymptotic sequence of proved exact
unrestricted-equilibrium contacts.

## 10. Exact local regression

The independent standard-library Fraction replay is

```sh
python -B packages/interval_global_closure/verify_curved_initial_phase.py \
  packages/interval_global_closure/curved_initial_phase_replay.json
```

It integrates the chronological running records directly on three
polynomial transport patches: a bilinear field with a final upper-record
recapture, a curved rank-one field, and a genuinely non-rank-one field
with strictly negative logarithmic mixed derivative. The replay checks
27 physical RLR integrals, nine bilinear formula identities, 24 ordered
peak-derivative comparisons, 756 exact concavity chords with three
monotone concave suffixes, 18 clipping-boundary dominations and 81
endpoint-minimum comparisons. It does not establish phase existence or
an unrestricted game value. Both the proof and this replay were
independently reviewed; the analytic argument above supplies the
continuous and arbitrary-path scope that finitely many fixtures cannot.

## 11. An explicit three-parameter initial guard

For an ordinary interior start, the surviving `L-R-L` list has an exact
integral form in the same initial field `L(a,z)=F(1-a,z-1)`. Choose

\[
 0<a<1,\qquad 0\le\alpha\le a\le z\le e\le1,
                 \qquad \alpha=0\ \text{or}\ e=1.
\tag{17}
\]

The three light-coordinate legs are

\[
 (1-a,a-1)\to(1-a,z-1)
       \to(1-\alpha,z-1)\to(1-\alpha,e-1).
\tag{18}
\]

Their directions are left, right, left, with zero lengths allowed.
The first point is the free initial position `1-a` at time zero. The
last point lies on one of the two characteristic exit edges. On the
edge `alpha=0`, the free parameters are `(a,z,e)`; on the edge `e=1`,
they are `(alpha,a,z)`. Thus (17) describes two families with three
continuous parameters, including the initial position.

Put

\[
 f=\phi(a)=L(a,a),\qquad \ell=L(a,z),\qquad
                      k=\max\{f,L(\alpha,z)\}.
\]

The exact prefix cost is

\[
\begin{aligned}
2C_{\rm pre}(\alpha,a,z,e)={}&e-\alpha
       +\int_a^z L(a,s)\,ds-(z-a)f+(a-\alpha)\ell\\
 &-\int_\alpha^a\max\{f,L(b,z)\}\,db
       +\int_z^e\min\{\ell,L(\alpha,s)\}\,ds
       -(e-z)k.
\end{aligned}
\tag{19}
\]

Indeed, the first left leg contributes
`(1/2) integral_a^z L(a,s) ds + (z-a)(1-f)/2`. The middle right leg
contributes `(a-alpha)(ell+1)/2` minus its clipped upper-record
integral. The last left leg contributes its capped lower-record
integral plus `(e-z)(1-k)/2`. Their constant durations sum to
`(e-alpha)/2`, giving (19). Both clips remain necessary: the middle
peak can lie below the initial upper record, and the last leg may
fail to improve the valley record.

The physical exit and its actual survivor records are

\[
 t_e=\frac{e-\alpha}{2},\quad
 x_e=1-\frac{\alpha+e}{2},\qquad
 (\ell_e,r_e)
   =\bigl(\min\{\ell,L(\alpha,e)\},\ 1-k\bigr).
\tag{20}
\]

Consequently the sufficient lower guard against the entire initial
phase is the explicit inequality

\[
       C_{\rm pre}(\alpha,a,z,e)
           +P(t_e,x_e,\ell_e,r_e)\ge c
\tag{21}
\]

for every tuple in (17), with a certified continuous monotone concave
outer lower bound `P` as in Section 6. The original phase curvature
hypotheses are required for completeness of this list. Formula (19)
itself is simply the physical record integral and does not require
those hypotheses.

The parameter domain deliberately retains phase-closure travel.
For `alpha=0` and `e>z`, the last left leg travels along the front
after reaching it earlier. For `z=e=1` and `alpha<a`, the middle
right leg travels along the other exit edge. These cases must remain
in (21) when `P` is an arbitrary certified lower bound, rather than
the exact dynamically consistent outer value.

The ordinary formula is not used at `a=0`: that start is the actual
positive endpoint, with its time-zero endpoint capture reset; the
fast endpoint sweep handles it separately. The start `a=1` is the
separate center state. Under the regular center convention its
zero-duration trace is consistent, but no endpoint trace is silently
substituted for actual capture.

For a **fixed** outer field, a **fixed** certified `P`, and a fixed
parameter tuple, the left side of (21) is concave in the consistent
initial field values. In (19), positive minima and negative maxima
are concave and the remaining terms are linear. Each exit record in
(20) is concave, so composition with the fixed monotone concave `P`
preserves concavity. Its superlevel constraint is therefore convex
in those field variables. This statement asserts neither concavity
in the three path parameters nor convexity of the phase curvature
conditions (3); those are separate nonlinear restrictions. The outer
and initial traces must still belong to one legal field.

The Fraction replay in Section 10 also checks six instances of (19)
against direct chronological record integration. They include both
exit edges, a peak on each side of the old upper record, each
zero-leg degeneration, and the two forms of exit-boundary travel.
