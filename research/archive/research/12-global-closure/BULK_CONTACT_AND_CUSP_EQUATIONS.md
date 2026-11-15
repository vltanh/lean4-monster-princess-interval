# Bulk contact equations at the principal turning front

This note derives exact contact identities for the dominant one-turn and
endpoint-first Monster families. It gives a functional system for a
candidate phase construction; it does not assert that these families
exhaust an unrestricted optimal Monster law. In particular, the small
multiturn sheet in the current physical laws must not be discarded.

## 1. Conventions and two physical families

Let `F(t,x)` be the signed CDF of a symmetric ordered Princess law,
continuous in the open arena, with continuous endpoint interior traces,
sticky endpoints, and maximal outward motion after time two. Write

\[
 \mathcal F(U,W)=F((U+W)/2,(U-W)/2),\qquad
 f(a)=F(0,a).
\]

Thus `F_x>=|F_t|`, or `mathcal F_U>=0` and `mathcal F_W<=0`.
There is no extra factor one-half in the signed-CDF record cost: the fair
Princess reflection is already included in `F`. Interior initial and turn
atoms are excluded where a derivative is used; endpoint atoms are retained.

The interior-turn family `P(a,b)` has vertices

\[
 (0,a),\quad(h,(a+b)/2),\quad(b+1,-1),\quad(b+3,1),
       \qquad h=(b-a)/2.
\tag{1}
\]

Its parameter domain here is `-1<a<1`, `b>=0`, `h>=0`, and
`0<=(a+b)/2<1`. Its first leg moves right, its second left, and its final
leg right. The principal family is `P(a,1)`; negative `a` covers the
reflected initial-inward one-turn routes.

The geometry implies `b<2-a<3`. When `a>=0`, it also gives `b<2`,
so the first center visit is before two; when `a<0`, the first center
visit is `-a<1`, even if the later return time `b` exceeds two.

The endpoint-first family `S(a)`, `-1<a<1`, has vertices

\[
             (0,a),\quad(1-a,1),\quad(3-a,-1).
\tag{2}
\]

A negative `a` becomes the familiar positive-start initial-inward route
after reflection. The endpoint sweep is the separate limiting physical
route `E:(0,1)->(2,-1)`.

For (1), put

\[
 \sigma=b+1,\quad
 k=\mathcal F(b,-a),\quad
 I(a,b)=\frac12\int_a^b\mathcal F(U,-a)\,dU.
\tag{3}
\]

Define a concave front moment

\[
 H_b(s)=\int_0^{b+1}\min\{s,F(t,b-t)\}\,dt.
\tag{4}
\]

When `b>1`, the initial portion of this auxiliary line lies outside the
arena; use the ordinary exterior CDF value `F(t,x)=1` for `x>1`.
That portion contributes `(b-1)s`. It is an algebraic moment, not extra
physical scoring time. Actual endpoint values do not affect the integral;
interior endpoint traces are used in its derivatives.

## 2. Exact contact costs, with no endpoint-inverse assumptions

The two exact costs are

\[
 \boxed{C_P(a,b)=b+3-I(a,b)-(b+3-h)k+H_b(f(a)).}
\tag{5}
\]

\[
 \boxed{C_S(a)=1-a-I(a,2-a)+H_{2-a}(f(a)).}
\tag{6}
\]

For the endpoint sweep,

\[
                  C_E=H_1(1)=\int_0^2F(t,1-t)\,dt.
\tag{7}
\]

These identities do not assume that every Princess has already absorbed
by two, or the historical identities `beta(1)=2`, `beta(3)=4`.

To prove (5), the right first leg makes `F` nondecreasing, so its lower
record stays `f(a)` and its upper-survivor record is `1-F`. Its cost is
`h f(a)+h-I`. At the turn the latter record becomes `1-k`. During the left
leg the lower record is `min(f(a),F(t,b-t))`. The front values before `h`
are at least `k>=f(a)`, hence this lower-record integral is
`H_b(f(a))-h f(a)`. After the first negative endpoint the Monster next
reaches the center at time `b+2>=2`; its positive survivors cannot be
caught before the positive endpoint because they are moving maximally
outward. Thus the upper-survivor contribution from the turn onward is
`(b+3-h)(1-k)`. Adding proves (5).

For (6), the same first-leg calculation runs until `sigma=1-a`.
At the positive endpoint the upper record resets to one. The auxiliary
front for `b=2-a` has its exterior portion exactly before that time;
its contribution `sigma f(a)` cancels the first-leg lower record. This
leaves (6). The direct endpoint sweep has a nonincreasing lower field and
an already complete upper record, which gives (7).

### A necessary endpoint jump

At the boundary `b=2-a`, evaluate the *interior-turn limit* of (5), using
`k=F(1-a,1-)`. Comparing with the actual endpoint route gives

\[
 \boxed{\lim_{b\uparrow2-a}C_P(a,b)-C_S(a)
                   =4[1-F(1-a,1-)].}
\tag{8}
\]

The positive endpoint atom is captured four units earlier by the actual
endpoint hit. Therefore the endpoint family cannot be identified with a
closed interior-turn equation unless that atom is absent. A continuous
phase construction must keep this trace jump explicitly.

## 3. Start and turning-front variations

For a point where the relevant derivatives exist and no time interval is
a tie between the fixed lower record and the descending field, set

\[
 A_b(t)=F(t,b-t),\qquad E_b=F(b+1,-1+),
\]

\[
 \tau=h+\bigl|\{t\in[h,b+1]:A_b(t)>f(a)\}\bigr|,
\quad
 B_o=\int_0^h F_x(t,a+t)\,dt,
\]

\[
 B_i=\int_h^{b+1}1_{\{A_b(t)<f(a)\}}F_x(t,b-t)\,dt,
\qquad L_e=\min(f(a),E_b).
\tag{9}
\]

Then differentiation of the physical record integrals yields

\[
 \boxed{\partial_a C_P
       =\tau f'(a)-B_o+(b+3-h)\mathcal F_W(b,-a),}
\tag{10}
\]

\[
 \boxed{\partial_b C_P
       =1-k+L_e+B_i-(b+3-h)\mathcal F_U(b,-a).}
\tag{11}
\]

The term `L_e` is essential. It is the survivor mass that remains just
before the negative endpoint, and may be positive. Replacing it by zero
would incorrectly remove endpoint atoms. If the lower field crosses the
initial record in the interior, `tau` is that crossing time; otherwise it
can equal `b+1`. Formula (11) remains valid in the latter case because it
uses `min(f,E_b)`, not `E_b` unconditionally.

At a kink of the turning front, use the two one-sided versions of (11),
including the corresponding one-sided spatial derivatives on the active
descending ray. A local minimizing turn must satisfy

\[
                       \partial_b^-C_P\le0\le\partial_b^+C_P.
\tag{12}
\]

It need not satisfy one smooth equality. The current full-width
coarse-64/fine-256 field illustrates this: on much of `U=1`, the left
`mathcal F_U` is large while the right derivative is zero or almost zero.
The turn is pinned by a genuine cusp between incoming and outgoing
transport phases.

For `S(a)`, use `sigma=1-a`, `b=2-a`, and the analogous definitions with
the right leg ending at `sigma`, and the descending active integral
running from `sigma` to `sigma+2`. Then

\[
 \boxed{C_S'(a)=\tau_S f'(a)
       -[1-k_S+L_{e,S}+B_{o,S}+B_{i,S}].}
\tag{13}
\]

Positive-time record ties require directional minimum derivatives, not
arbitrary selection of one branch. For example, in (11) increasing `b`
gives zero derivative on a tied interval, whereas decreasing it includes
the corresponding spatial derivative. The original formulas (5)-(6)
remain exact at all ties and can be used directly.

## 4. Flat supported families become scalar moment equations

If a principal interval of starts is active at cost `V`, put

\[
 k(a)=\mathcal F(1,-a),\qquad H=H_1.
\]

Equation (5) is the exact column condition

\[
 \boxed{I(a,1)+\frac{7+a}{2}k(a)-H(f(a))=4-V.}
\tag{14}
\]

If the endpoint-first family is active as well, (6) gives

\[
 \boxed{H_{2-a}(f(a))-I(a,2-a)=V-1+a.}
\tag{15}
\]

A positive endpoint-sweep component in an actual saddle also requires
`H(1)=V`. For an approaching Princess sequence against a fixed optimal
Monster law with positive sweep mass, this is the corresponding limiting
equality, rather than an automatic Princess-attainment assertion.

The derivative `H'(s)` is the front waiting time at level `s`, wherever
that derivative is unique. Thus (14) has only an initial CDF, a principal
front trace, a one-dimensional concave front moment, and an outward-column
integral. It does not require a full response oracle to evaluate or
separate this family.

## 5. The bulk pressure of the actual main family types

Consider a continuum main Monster law with fast-sweep probability `q`,
principal-family density `g(a) da`, and endpoint-family density `h(a) da`,
where `-1<a<1`. Fair reflection is understood. Assume absolute continuity
of these parameter measures for the density formulas in this section;
the corresponding pushforward-measure statements also make sense before
taking any continuum limit of a finite bank.

In the positive initial light triangle

\[
                \mathcal T=\{0<U<1,\ -U<W<U\},
\]

only their initial unit-speed legs produce bulk field variation. Returns
from `S` have `U>1` or reflected `W>1`; principal returns and turns lie on
the principal fronts. Put `G=g+h`. For an antisymmetric field variation
supported away from the initial and principal boundaries, the exact bulk
first variation is

\[
 \boxed{\delta J_{\rm main}
   =\int_{\mathcal T}\frac{G(-U)-G(-W)}2\,
                                  \delta\mathcal F(U,W)\,dU\,dW.}
\tag{16}
\]

Indeed, a right initial leg has `W=-a`, `dt=dU/2`, and coefficient `-1`
in its CDF cost. Its negative-position portion, reflected into the positive
triangle, has `U=-a`, `dt=dW/2`, and the opposite sign. This proves (16)
without differentiating the CDF or approximating its paths.

Consequently a strict two-direction transport region of a saddle must
obey

\[
                  G(-U)-G(-W)+2\rho_{\rm rest}(U,W)=0,
\tag{17}
\]

where `rho_rest` is the actual pressure of the remaining Monster families.
The small initial-inward/multiturn sheet cannot be dropped from (17)
because its role may be precisely to support the curved initial phase.
Where that sheet is absent and `G` is not locally constant, (17) rules
out a freely varying two-direction phase; one of the characteristic
transport constraints must be active.

On the positive principal front `U=1`, `-1<W<1`, write
`K(W)=mathcal F(1,W)`. For trace variations, the main law's singular
coefficient is

\[
 \boxed{\Lambda(W)=\frac12\left[
 q+\int_{\{a:f(a)>K(W)\}}g(a)\,da-(7-W)g(-W)\right].}
\tag{18}
\]

The three terms are the fast sweep, current lower-record pressure from
principal returns, and the long-lived upper-record charge at each turn.
If the trace can be varied freely, this coefficient must cancel the
remaining families' front pressure. When the incoming or outgoing
transport constraint is saturated, it instead supplies the boundary data
for the corresponding constrained phase; setting it to zero without
checking admissible variations would be wrong.

In a region where there is no extra front pressure and the trace is free,
strictly increasing `f` turns (18) into the one-dimensional equation

\[
             (7+a)g(a)
                 =q+\int_{f^{-1}(k(a))}^{1}g(s)\,ds.
\tag{19}
\]

This is a conditional interface equation, not a claim that the measured
finite-bank densities already solve it.

### An exact attachment boundary on the negative-start branch

For `a<0`, the route `P(a,b)` first reaches the center at time `-a`.
Its positive excursion returns at time `b` with survivor records
`(f(a),1-k(a,b))`. If `d=1-k-f(a)>0`, its prescribed negative-first final
tour attacks the lighter side. The heavier-first direct-tour comparison
in `CENTER_HEAVIER_FIRST_BALANCE.md` saves at least `2d` by reversing that
tour. The remaining positive excursion followed by a positive-first
tour is dominated by deleting the excursion. The resulting whole route
is precisely `S(a)`. Consequently

\[
 \boxed{C_P(a,b)-C_S(a)\ge2[1-k(a,b)-f(a)]
                 \quad\hbox{if }1-k(a,b)-f(a)>0.}
\tag{19a}
\]

Thus every active negative-start principal row necessarily satisfies
`k(a)+f(a)>=1`. Both terms are nondecreasing in `a`, so this defines a
single initial cutoff for that branch, rather than an arbitrary guessed
subset of starts. The equality `k(a)+f(a)=1` is a candidate attachment
between the returning family and the monotone endpoint family. It is
only a necessary contact boundary: equality there does not by itself
prove the two complete costs coincide. For a moving turn front, the same
inequality gives the exact lower feasible front `k(a,b)>=1-f(a)`.

## 6. A one-dimensional saturated-phase closure and its exact correction

A natural saturated submodel on an initial positive-start strip is

\[
 \mathcal F(U,-a)=\min\{k(a),\max\{f(a),B(U)\}\},
          \qquad a\le U\le1,
\tag{20}
\]

with increasing incoming trace `B`. The three pieces are respectively an
initial outward phase, an incoming phase, and a terminal outward phase.
Assume `B(a)<=f(a)<=k(a)<=B(1)` and let `u(r)` be the first inverse of
`B`. Layer cake gives

\[
 I(a,1)=\frac12\left[k(a)-a f(a)
                           -\int_{f(a)}^{k(a)}u(r)\,dr\right].
\tag{21}
\]

Thus the entire principal equal-cost condition closes in one-dimensional
functions:

\[
 \boxed{(8+a)k(a)-a f(a)-\int_{f(a)}^{k(a)}u(r)\,dr
                         =8-2V+2H(f(a)).}
\tag{22}
\]

Together with (15), the front-moment definition, the cusp inequalities,
and an appropriate front-pressure balance, this is a concrete functional
system for the saturated bulk. All its integrals are over one variable.
A physical construction still has to check its initial and terminal
attachments and all omitted Monster responses.

There is an exact way to expose, rather than hide, the curved-initial
correction. For a general legal field define `u_a(r)` as the first `U`
where the column `mathcal F(U,-a)` reaches level `r`. Monotonicity gives

\[
 I(a,1)=\frac12\left[k(a)-a f(a)
                          -\int_{f(a)}^{k(a)}u_a(r)\,dr\right].
\tag{23}
\]

If the common incoming characteristic of rank `r` is `u(r)`, but a
Monster catches that rank earlier on its curved initial phase, then
`u_a(r)<=u(r)`. Put

\[
             \Delta(a)=\int_{f(a)}^{k(a)}[u(r)-u_a(r)]\,dr.
\]

The correct replacement for (22) is therefore

\[
 (8+a)k(a)-a f(a)-\int_{f(a)}^{k(a)}u(r)\,dr+\Delta(a)
                            =8-2V+2H(f(a)).
\tag{24}
\]

Equivalently, early curved-phase captures reduce the ordinary principal
cost by exactly `Delta(a)/2`. The ordinary initial-outward/incoming model
sets this correction to zero. The separate initial-inward attack theorem
shows why a positive-length initial unit outward run can fail at an
active boundary. The initial sheet must determine `u_a` (or its integral
correction) through its own contact equations; a cusp at `U=1` alone does
not prove that the whole initial field is the three-trace clamp (20).

### A canonical nonnegative correction, without a phase assumption

For positive starts one may choose a canonical reference trace
`B(U)=mathcal F(U,0)` for `0<=U<1` and append the value `B(1)=1`.
This terminal jump is an algebraic device; it is not claimed to be an
actual new Princess field. Its generalized first inverse assigns `u(r)=1`
to all levels above `B(1-)`. Levels in a jump are assigned its coordinate. The usual lower and upper
generalized inverses can differ only at plateau levels, a rank-null set,
so the layer-cake integrals remain exact.

For every `a>=0` and `a<=U<1`, transport gives

\[
 \mathcal F(U,-a)\ge\max\{f(a),B(U)\},\qquad
 B(U)\le k(a),\quad f(a)\le k(a).
\]

Consequently the correction in (24) can be defined directly by

\[
 \boxed{\Delta(a)=\int_a^1
       [\mathcal F(U,-a)-\max\{f(a),B(U)\}]\,dU\ge0.}
\tag{24a}
\]

The artificial jump ensures the reference column reaches its prescribed
terminal level `k(a)` at `U=1`, with no change in its time integral.
Layer cake identifies (24a) exactly with the inverse-level correction in
(24). Thus the five one-dimensional objects `f`, `B`, `k`, `H`, and
`Delta` encode the whole positive principal-family payoff without
assuming ordinary Princess turns. They are constrained by a common
legal two-dimensional field; their independent realizability is not
being asserted. Determining the correction from the active initial sheet
is the remaining attachment problem.

Equations (14)-(19) and (23) are exact contact/pressure identities under
the stated regularity. Equations (20)-(22) are an explicit reduced phase
ansatz. Equations (23)-(24) specify exactly what must be added when that
ansatz has a curved initial attachment. No claim of an equilibrium or of
a closed global one-dimensional solution is made until that attachment,
the endpoint trace jumps, and the remaining support are all certified.

## 7. Exact physical checks

`verify_bulk_contact_equations.py` uses a legal radial law uniform on
`[0,1]`, stationary until `T` in `{0,1,2}`, then unit outward and
endpoint-sticky. Its independent oracle intersects individual affine
Princess and Monster pieces and integrates the lower envelope of first
capture times over the initial radius. It does not use capture records.

The regression passes 549 M2 costs, 51 endpoint-family costs, 45 nontrivial
endpoint-limit comparisons, 236 negative-start balance comparisons, and
exact start/turn derivatives on 49 smooth parameter fixtures. Fourteen
additional endpoint-route derivatives explicitly include the nonzero
endpoint survivor term and its cap by the incoming lower record. In the stationary-until-two subcase with `b<=1`, put
`f=(1+a)/2`, `h=(b-a)/2`. Direct physical integration gives

\[
 C_P=2-f^2+h(1-f)-3h^2/4,
\]

\[
 C_{P,a}=h/4-f/2-1/2,\qquad
 C_{P,b}=(1-f)/2-3h/4.
\]

For `S`, with `sigma=1-a`, the exact cost is
`1+sigma-sigma^2/4` for `a>=0`, and `2-sigma^2/4` for `a<=0`.
These checks include endpoint survivor mass and therefore detect its
omission from (11) or (13).
