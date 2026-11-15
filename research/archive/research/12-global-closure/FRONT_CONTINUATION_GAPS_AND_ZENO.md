# Front continuation: an exact boundary, a finite-count gate, and its degeneration

This is a fixed-field research checkpoint. It does not prove that an optimal
Princess has a particular front, a uniform density bound, or a positive record
gap. Its purpose is to distinguish a useful finite outer gate from a genuine
obstruction to obtaining that gate from front completion alone.

Use the signed symmetric ordered interior CDF `F`, actual endpoint capture
resets, and light coordinates `U=t+x`, `W=t-x`. Assume a continuous interior
field with no center atom, sticky endpoints, and maximal outward completion
on `t+|x|=C`, where `1<=C<=2`. On the positive postfront region,

\[
 \mathcal F(U,W)=K(W),\quad U\ge C,
 \qquad K(C)=\tfrac12.
\tag{1}
\]

Both light coordinates at least `C` give the interior CDF one-half. After
time `C`, a center state with records `(l,r)<=1/2` therefore has exact tour
value `min(3l+r,l+3r)`. The established triangle normalization, front
shortening, and heavier-first balance rules are used with their physical
endpoint conventions. These arguments do not replace an endpoint atom by
an interior trace.

## 1. An exact precenter terminal on the incoming front

Consider an interior positive precenter state on `U=C`:

\[
 W=w,\qquad x=(C-w)/2\in(0,1),\qquad
 \tfrac12\le l\le K(w),\quad 0\le r\le1-K(w).
\]

The negative half has not been caught. The record `l` can additionally
contain positive ranks below the Monster. Set

\[
 J_w(l)=\frac12\int_w^C\min\{l,K(v)\}\,dv,
 \quad l_z=\min\{l,K(z)\},\quad d_z=\frac{2-C+z}{2}.
\tag{2}
\]

Then the complete remaining value is

\[
\boxed{
 V_{\rm front}(w,l,r)=J_w(l)+\frac12+(3+x)r
 +\min\left\{0,\ \inf_{w\le z\le C}
 \big[d_z(l_z+\tfrac12)-(C+2-z)r\big]\right\}.}
\tag{3}
\]

The zero branch is direct leftward motion through the center to the negative
endpoint, then the positive endpoint. The parameter `z` describes a left
valley from `(C,w)` to `(C,z)`, then rightward motion to the positive
endpoint, followed by the opposite sweep. Thus this terminal is a complete
one-parameter optimization with both records. It is not in general the
minimum of only the two immediate direct tours.

### Proof

Until a first center or positive-endpoint visit, `W` is nondecreasing and
the CDF is `K(W)`. Hence the lower record is `min(l,K(W))` and the upper
survivor record remains `r`.

If the next exit is the center, its time is at least `C`. The speed bound
`dW/dt<=2` gives an accumulated cost at least
`J_w(l)+xr`. Its updated center records are `(1/2,r)`, and their exact
remaining value is `1/2+3r`. Direct leftward motion attains their sum.

If the positive endpoint is reached first at time `z+1`, its endpoint
light coordinate is `W=z`. For `z<C`, the left-then-right valley with
this same endpoint time maximizes `W` pointwise among all paths with
the specified entry and exit. It stays positive, inside the arena,
and on `U>=C`. It therefore captures every lower rank no later and
does not change the upper record before the actual endpoint reset.
After that endpoint the direct opposite sweep is optimal.

The valley contributes
`(1/2) integral_w^z min(l,K) + r(z-w)/2`.
Its right leg has duration `d_z` and constant records `(l_z,r)`.
The ensuing sweep contributes
`(1/2) integral_z^C min(l_z,K) + (4+z-C)/4`.
Monotonicity of `K` joins the two integrals to `J_w(l)`. Their sum
minus the negative-first branch is exactly the bracket in (3).

An endpoint-first path with `z>=C` cannot improve the negative-first
branch. At its first `W=C` state, say `U=C+2y`, the records have become
`(1/2,r)`. Its prefix cost is at least
`J_w(l)+xr+y(1/2+r)`: the required increase of `W` supplies the first
two terms, and its extra increase of `U` supplies the last term.
There are no further interior captures. Either endpoint order from
position `y` adds at least the corresponding direct tour cost. After
adding the displayed extra term, the positive-first order costs at
least `3/2+r`, and the negative-first order at least `1/2+3r`.
Since `r<=1/2`, both are at least the center negative-first value.
The same argument covers a nonexiting infinite path with positive
survivors; if no survivors remain its cost cannot be smaller either.

At `z=C`, the bracket in (3) is `1-2r>=0`, consistently with this
comparison. At an actual initial endpoint apply its reset separately;
at an actual center first clip `l` to one-half. Formula (3) is stated
for updated interior precenter states, not arbitrary abstract records.
For continuous `K`, its compact one-dimensional infimum is attained.

## 2. A record gap and central density give a finite return bound

Suppose that throughout the central decision region the signed spatial
CDF obeys

\[
 0\le F(s,y)-\tfrac12\le M y
       \qquad(0\le y\le r_0),
\tag{4}
\]

where `0<r_0<1` and `0<M<infinity`. A bounded signed spatial density
on this strip is sufficient; differentiability is unnecessary. Fix a
center state at time `t<C` with

\[
 \min(l,r)\le\tfrac12-\delta,\qquad \delta>0.
\tag{5}
\]

Then an exact minimizing center continuation exists with at most

\[
\boxed{
 N=\left\lfloor\frac{C-t}{2h_0}\right\rfloor,
 \qquad h_0=\min\{r_0,\delta/M\},
}
\tag{6}
\]

proper returning triangles, followed by a direct endpoint tour.
If `(4)` has `M=0`, take `h_0=r_0`. Actual endpoint-touching triangles
belong to the tour branch rather than to the interior-trace recurrence.

The lighter incoming record is enough in (5); both records need not
already have the gap. A minimum-count representative has no unproductive
proper triangle: absorb such a triangle into the next triangle's side
over their combined duration, where the larger tent dominates pointwise
and the old first triangle captured nothing. If that tent reaches an
endpoint, or if the next action is the final tour, use the direct-tour
comparison. This strictly removes a return without increasing cost.
Thus the following rank test is applied to productive returns; a balanced
no-update return is not incorrectly inferred to satisfy it merely from
the weak balance inequality.

In heavier-first balanced normal form, the first
affected record after a return is at most its opposite incoming record.
That opposite record is at most `1/2-delta`. Thereafter both records
are at most this threshold. Thus every proper return, including the
first, has a peak satisfying

\[
 F(s+h,h)\ge\tfrac12+\delta.
\tag{7}
\]

If `h<r_0`, (4) gives `h>=delta/M`; otherwise `h>=r_0` directly.
Every return consequently lasts at least `2h_0`. Front shortening
keeps all returned triangles before time `C`, proving the count.

There is no assumption here that an unrestricted optimum was finite.
First minimize in each finite triangle budget. The fixed-budget
heavier-first/balance argument uses the actual old future, preserves
that budget, and permits a minimum-count representative within it.
Compactness of its finitely many height parameters, with zero-height
merging and the separate physical endpoint branch, gives an attained
minimum by lower semicontinuity. Full continuity at an endpoint-touching
limit is unnecessary: its actual capture reset is a favorable lower
jump. The bound just proved reduces every such minimum to budget
`N`. A center hold before a triangle is absorbed into the outward
tent over their combined duration, which dominates pointwise on that
side; if the tent reaches an endpoint, or if the hold precedes the
final tour, use the direct-tour comparison instead. Finite path
approximations of an arbitrary center response, including one whose
center zero set has positive measure,
preserving its first actual endpoint visits and approximating the
adjacent controls in shrinking time windows, converge in record cost
for a continuous fixed field. Their common front normalization has a
bounded completion horizon. Hence the finite-budget infima have the
unrestricted value, and they already stabilize at `N`.

For a positive initial start `a`, its first-center upper survivor
record is at most `1-f(a)`, where `f(a)=F(0,a)`. Consequently any
start range `a>=a_*>0` with `f(a_*)>1/2` has the common gap

\[
                   \delta=f(a_*)-\tfrac12.
\tag{8}
\]

This supplies a finite nonpolynomial outer continuation for such an
initial phase. It does not settle starts approaching the center,
fields without (4), or whether an optimal field admits uniform
constants. Those are the remaining gluing hypotheses.

## 3. An explicit front-one law with an initial infinite-return optimum

Fix `0<p<1`. Let the initial radial CDF be

\[
                         G(r)=r^p,\quad0\le r\le1.
\tag{9}
\]

A rank starting at radius `r` stays there until time `1-r`, then
moves outward at unit speed and stops at the endpoint. Its reflected
copy has equal probability. This is one globally legal ordered sticky
front-one law, with no initial center or endpoint atom. Its signed
interior field on the positive side is

\[
 F(t,x)=\frac12+\frac12
 \begin{cases}
 x^p,&t+x\le1,\\
 ((1-t+x)/2)^p,&t+x\ge1,\ t-x\le1,\\
 0,&t-x\ge1.
 \end{cases}
\tag{10}
\]

Consider its center response from `(t,l,r)=(0,1/2,1/2)`.
Every finite normalized response is strictly improvable. Therefore
no finite-turn center response is optimal for this one field.

### A first returning triangle

By the front-one shortening rule, a first proper triangle has some
height `0<a<=1/2`. By reflection take it positive. Its entire
triangle is in the stationary region of (10). With

\[
                      A_p=\frac{p+2}{2(p+1)},
\]

its prefix cost and exit records are

\[
 C_{\rm old}=2a-A_pa^{p+1},\qquad
                  (\tfrac12,\tfrac12-\tfrac12a^p).
\tag{11}
\]

For `0<epsilon<a`, replace it by a negative triangle of height
`epsilon` and a positive triangle of height `b=a-epsilon`.
They have exactly the old final center time `2a`; both remain in
the stationary region because their largest incoming light coordinate
is `2a<=1`. Their cost and records are

\[
 C_{\rm new}=2a-b\epsilon^p
                    -A_p(\epsilon^{p+1}+b^{p+1}),
\]
\[
 (\tfrac12-\tfrac12\epsilon^p,
                         \tfrac12-\tfrac12b^p).
\tag{12}
\]

Thus the exact prefix saving is

\[
 C_{\rm old}-C_{\rm new}
 =b\epsilon^p+A_p(\epsilon^{p+1}+b^{p+1}-a^{p+1})
 =a\epsilon^p-O(\epsilon).
\tag{13}
\]

Retain the complete old physical suffix at the unchanged center time.
If it completes within a further time `H`, its cost is nondecreasing
in both records and is `H`-Lipschitz in either one. The lower record
has improved. The only possible suffix loss is at most

\[
                 \frac H2[a^p-(a-\epsilon)^p]=O(\epsilon).
\tag{14}
\]

Since `epsilon^p/epsilon` diverges, (13) strictly exceeds (14) for
sufficiently small `epsilon`. This comparison works for a bounded
suffix with any number of later turns, not only a finite suffix.

### A direct tour or initial hold

Let `c=1/2`, `b=c-epsilon`, and

\[
 B(s)=\frac{s^{p+1}}{p+1}+(1-s)s^p.
\]

The direct positive-first tour has cost `2-B(c)/2`.
Insert a negative `epsilon`-triangle, then take the positive-first
tour at center time `2epsilon`. The exact saving is

\[
 \frac32\epsilon^p-2\epsilon+A_p\epsilon^{p+1}
                      +\frac{B(b)-B(c)}2
 =\frac32\epsilon^p-O(\epsilon)>0.
\tag{15}
\]

An initial positive-duration center hold is likewise strictly improved
by placing a sufficiently small triangle inside it. This captures
positive mass earlier, preserves the hold's center exit time, and
weakly improves the exit records. The stationary formula applies
when its height is small enough.

Every response with finitely many center excursions has a finite
triangle-and-tour representative of no greater cost. Equations
(13)--(15) improve that representative. More strongly, an optimal
response cannot have a first positive-duration excursion or initial
hold. It must have infinitely many excursions accumulating at time
zero. This is an initial Zeno phenomenon in an explicit physical law,
not a statement about sampled high-turn paths or an auxiliary
renewal model.

An optimal response does exist. The front-one terminal normalization
restricts it to paths completed by time four. This is a compact set
of 1-Lipschitz paths. First capture is lower semicontinuous in a
uniformly convergent Monster path; Fatou therefore makes expected
capture cost lower semicontinuous. The infimum is attained. The
pointwise front normalization used here needs the explicit continuous
field (10), not a bounded derivative at the center.

## 4. No turn bound uniform over bounded-density front-one laws

The density of (9) diverges at the center. This is exactly the
degeneration excluded by (4). Nevertheless its consequence for a
uniform class bound persists under regular approximation.

For `eta>0`, take

\[
 G_\eta(r)=\frac{(r+\eta)^p-\eta^p}{(1+\eta)^p-\eta^p}
\tag{16}
\]

and use the same stationary-to-front-one path construction. Each
initial radial density is bounded; all interior spatial densities
remain bounded too. These are continuous ordered front-one fields,
and `G_eta` converges uniformly to `G`.

The path construction composes the initial CDF with the same radial
footpoint in (10), so the complete signed fields converge uniformly
in their interior traces. For every physical path completed by time
four, each running record changes by at most the uniform CDF error.
Its payoff changes by at most eight times that error, uniformly over
all such paths, with actual endpoint resets shared by both fields.

For every fixed finite triangle budget `N`, the compact normalized
`N`-triangle class attains its minimum for (10). Section 3 makes
this minimum strictly larger than the unrestricted center value.
Uniform payoff convergence preserves the strict gap for all
sufficiently small `eta`. Hence some bounded-density front-one
fields require more than `N` returns in every optimal response.

This does not contradict a bound depending on the density and record
gap, a finite response theorem for each supplied P1 field, or the
possibility of a special finite-phase equilibrium. It rules out a
uniform outer turn cutoff based only on front-one completion and
qualitative regularity. The initial state in this obstruction is
fixed at the center; no claim is made that it is the unrestricted
free-start worst response to (9), or that (9) is near an equilibrium.

## 5. The obstruction can occur arbitrarily close to global security

This statement concerns the fixed-center response, not the free-start
worst response. Let `F_reg` be a regular symmetric ordered front-two
field with bounded interior spatial density and security close to the
unrestricted game value. Such regular approaching fields are available
from the established approximation and front-two completion results.
Transport gives a joint Lipschitz bound on their interior traces.
Let `F_cusp` be (10), and define the **CDF** blend

\[
                  F_\eta=(1-\eta)F_{\rm reg}+\eta F_{\rm cusp},
                  \qquad0<\eta<1.
\tag{17}
\]

This is a legal ordered field after common-quantile reconstruction.
It is still front-two and has no center atom. For each fixed Monster,
its two running-record integrals are concave in the field, including
the separate actual endpoint resets. Taking their infimum preserves
concavity. Thus, for any valid game upper `U_*`,

\[
 S(F_\eta)\ge(1-\eta)S(F_{\rm reg})+\eta S(F_{\rm cusp})
             \ge S(F_{\rm reg})-\eta U_*.
\tag{18}
\]

This uses concavity of ordered-CDF security. It is not an assertion that
the ordered law's payoff is linear in the two component laws.

Nevertheless no finite response from center `(0,1/2,1/2)` is optimal
for `F_eta`. For a first proper positive triangle of height `a<1`,
use the same opposite `epsilon` triangle and shortened old triangle.
The new lower record improves by at least `eta epsilon^p/2`. It stays
improved throughout the remaining `2a-2epsilon` prefix time. This
supplies a saving of at least

\[
                         (a-\epsilon)\eta\epsilon^p.
\tag{19}
\]

For the combined field, compare the same physical events. Every old
outbound event at time `u<=a-epsilon` maps to the new event at time
`u+2epsilon` and the identical positive position. The regular field
changes by `O(epsilon)`. The cusp footpoints at these two events are
`min(u,1/2)` and `min(u,1/2-epsilon)`; their powered values differ
uniformly by `O(epsilon)`, since any nonzero difference is near radius
one-half. The remaining old peak window maps to the new peak. Its
cusp rank is bounded away from zero for this fixed `a>0`, so its
change is also `O(epsilon)`. Later return events coincide physically.
This same-event map bounds the new combined upper survivor record
by the old combined record delayed by `2epsilon`, plus `O(epsilon)`.
It does not interchange a running maximum with a sum of fields.

Integrating the monotone delay costs only `O(epsilon)`, and the
terminal upper record changes by `O(epsilon)` as well. To see explicitly
why the cusp at zero causes no larger integrated loss, put
`c=min(a,1/2)>0`. Its old and new histories use
`min(s,c)^p` and `min((s-2epsilon)_+,c-epsilon)^p`. For example,

\[
 \int_0^T[\min(s,c)^p-\min((s-2\epsilon)_+,c)^p]ds
                      \le2\epsilon c^p,
\]

and changing the cap from `c` to `c-epsilon` contributes at most
`T[c^p-(c-epsilon)^p]=O(epsilon)`. No pointwise Lipschitz bound at
zero is assumed. The fixed bounded suffix is Lipschitz in its records.
Hence (19) gives a strict total improvement for small `epsilon`.
The same argument applies when `a>1/2`: the cusp's peak cap is then
already `c=1/2`.

If the first action is the direct positive-first endpoint tour,
the inserted opposite triangle improves its negative survivor record
by at least `eta epsilon^p/2`. That record then persists for three
units until its negative endpoint: the opposite sweep crosses the
center after time two. The adverse regular contribution and the
cusp cap/clock shifts are `O(epsilon)`, whereas the saving is
`(3eta/2)epsilon^p-O(epsilon)>0`. An initial center hold is again
strictly improved by a sufficiently small triangle within it.

Front-two normalization completes a center response by time five,
so compactness and lower semicontinuity give attainment just as above.
Every attaining center response therefore has infinitely many initial
excursions. By (18), this behavior is compatible with security
arbitrarily close to the unrestricted value.

Consequently near-optimal security alone cannot force bounded center
density or a finite fixed-center response. This does not exclude a
canonical regular approaching family, a regular optimal representative,
or a finite **free-start** best response to these blended laws. The
center may be a nondangerous state. A global reduction may legitimately
control that corner by a lower potential rather than an attaining
finite physical response.

## 6. Center slack and endpoint doping close the dangerous balanced corner

Write `Q(t,l,r)` for the exact center continuation of the same front-C
field, and suppose a separate certificate proves

\[
                       Q(0,\tfrac12,\tfrac12)\ge b>c,
\tag{20}
\]

where `c` is the security level to be certified. This scalar center
bound need not have a finite attaining response; an all-count lower
potential is sufficient.

Take a positive precenter prefix with first center time `tau<C` and
updated center records `(1/2,1/2-d)`. Throughout that prefix its lower
record is at least one-half and its upper surviving record is at
least `1/2-d`, so its cost is at least `tau(1-d)`.
All center futures in the normalized class complete by absolute time
`C+3`; zero-cost visits for inactive clocks can be appended so that
the same physical class visits both endpoints for either record vector.
Their record costs are consequently Lipschitz with constant
`C+3-tau` in each record. Taking infima gives

\[
 Q(\tau,\tfrac12,\tfrac12-d)
 \ge Q(\tau,\tfrac12,\tfrac12)-(C+3-\tau)d.
\]

The legal policy that holds at the center until `tau` gives
`Q(0,1/2,1/2)<=tau+Q(tau,1/2,1/2)`. Adding these inequalities proves

\[
\boxed{\quad J(\hbox{complete response})\ge b-(C+3)d.\quad}
\tag{21}
\]

Thus every response with cost below `c` must have

\[
                         d>\delta_*:=\frac{b-c}{C+3}>0.
\tag{22}
\]

Under (4), Section 2 gives a uniform finite number of postcenter
returns for all these potentially violating responses. It is safe
to use `C` instead of `C-tau` in the numerator of (6). A response
whose first center is at or after `C` already has endpoint-only
continuation, so it needs no record-gap gate. It is not silently
discarded. Actual endpoint-first branches likewise retain their
separate direct-sweep normalization.

Equivalently, first apply Section 1 at a precenter incoming-front
hit. It leaves either a first-center branch at time `C` or an
endpoint-first valley branch with no proper postcenter returns.
Only the remaining first-center-before-first-endpoint branches with
`tau<C` need (21). This uses no assertion that every raw low-cost
path has first center by `C`; that assertion would in particular
be unjustified for arbitrary front-one targets above one.

### A nonvacuous value-dense class with finite dangerous continuations

Let `F_base` be a regular front-C field satisfying (4) and having
certified global security at least `c_0`. Let `U_*<2` be a valid upper
on the unrestricted game, with `c_0<=U_*`. The symmetric stationary
endpoint Princess law has signed interior CDF `F_end=1/2`. Its
free-start security is one, whereas its center-start value is two:
the two endpoint arrival times from the center have sum at least four.
For `0<eta<1`, use the ordered CDF blend

\[
              F_\eta=(1-\eta)F_{\rm base}+\eta F_{\rm end}.
\tag{23}
\]

The same fixed-row concavity used in (18) gives

\[
 S(F_\eta)\ge(1-\eta)c_0+\eta,
 \qquad
 Q_\eta(0,\tfrac12,\tfrac12)
                   \ge b_\eta:=(1-\eta)c_0+2\eta.
\tag{24}
\]

In this special endpoint blend the physical row payoff is in fact
affine: before a clock's own endpoint its minimum commutes with
`eta/2+(1-eta)F_base`, and its actual endpoint reset is shared.
Thus `J_eta=(1-eta)J_base+eta(tau_-+tau_+)/2`. Taking infima gives
the two inequalities in (24).

Choose

\[
                    \eta>\frac{U_*-c_0}{2-c_0}.
\tag{25}
\]

The right side is less than one, and this makes `b_eta>U_*>=S(F_eta)`.
Consequently (21), now with target `U_*`, supplies the positive gap
`(b_eta-U_*)/(C+3)` for every early-center response of cost at most
`U_*`. This includes every actual worst response, rather than merely
hypothetical paths violating an already known lower floor. Equation
(6) therefore gives a finite postcenter restriction containing the
true minimizing response values of this field. Its central density
cap is at most `(1-eta)M`; if this cap vanishes, use the zero-density
case already stated.

The construction preserves front completion, transport, symmetry,
sticky endpoints, and interior regularity. Its endpoint atoms are
actual stationary targets, with the usual endpoint capture resets.
It also preserves any curved initial-phase criterion stated through
the signs of `F_U`, `F_UU`, `F_UW` and `(log F_U)_UW`: the first
three derivatives scale by `1-eta`, and the logarithmic mixed
derivative does not change. This observation is conditional on the
base field having that criterion; it does not create the criterion.

For the globally value-dense assertion take `C=2`, where front
completion is already known to preserve the unrestricted value.
Take regular base fields with certified `c_n` tending to the game
value `V`, and certified uppers `U_n` tending to `V`. The complete
approximation hierarchy supplies such sequences. Since `V<2`, one
can choose `eta_n` satisfying (25) and tending to zero. The endpoint-
doped fields are value-dense by (24), and each has a finite postcenter
restriction for its true worst responses. The bound can diverge with
`n`; no uniform turn count or finite-dimensional equilibrium class
is obtained.

This gives a useful sufficient gluing procedure for nonpolynomial
candidate phases: certify or create center slack, control the central
density, and check only finitely many postcenter return parameters
in the dangerous region. The unknown initial phase and the inner
precenter triangle `0<=W<=U<C` still need their own valid response
reduction or lower certificate. In particular, the `W=0` exit of the
initial three-run guard is not a center state, and Section 1 alone
does not price that exit.

## 7. Relation to the retained work

The archived `INFINITE_TURN_RENEWAL.md` studies a conditional affine
renewal cell and its all-count Green formulas. The example here instead
specifies the entire legal Princess law and proves a center-response
obstruction directly by physical triangles. It does not rely on that
cell's realization or hinge closure. The archived microscopic connector
example addresses a different failure: fixed inverse trace data do not
determine a robust unrestricted response limit.

For the game, the useful positive task is to certify a central density
bound and a record gap on all dangerous first-center states, or to
construct an all-count center potential covering the remaining balanced
corner. Neither front completion nor the curved initial three-run
criterion alone supplies that last corner.
