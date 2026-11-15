# A global paired-control response for endpoint inward rows

This note gives an unrestricted princess-response formulation for a
specified symmetric monster-law class. Every coupling between its two
monotone controls is attractive after reversing one control. The
remaining terms give unary potentials. Consequently a finite control
arrangement has an exact minimum-cut optimizer, and bounded-density
continuum controls admit a uniform approximation estimate.

This is a response theorem for a supplied law. No matched law, new game
value, or finite continuum certificate is asserted by the accompanying
finite fixtures. In particular, the outer start/cutoff variables and
the continuum approximation error must be covered before a finite cut
can be used as a game certificate.

## 1. The physical law and universal folding

Every route below is chosen together with its reflection, with equal
probabilities. The unnormalized component masses are nonnegative.
The class consists of:

* the endpoint sweeper pair, with mass `w0`;
* signed M1 starts, with densities `f(z)` at `+z` and `ell(z)` at `-z`,
  for `0<z<1`;
* fixed M2 turns `U=1`, with start densities `g(z)` and `h0(z)` at
  `+z` and `-z`;
* fixed-second inward rows `I(z,v,1)`, with density `j(z,v)` on
  `0<z<1, -z<v<z`;
* late M2 rows `M2(+z,s)` on `1<s<2-z`, and `M2(-z,s)` on
  `1<s<2+z`, with joint densities `hplus(z,s)` and `hminus(z,s)`;
* center-reaching early M2 rows `M2(x,s)`, with joint density
  `hearly(x,s)` on `|x|<s<1`;
* early M3 rows starting at x, turning first at U=s and next at V=1,
  then visiting +1 and -1, with density `mearly(x,s)` on `|x|<s<1`;
* endpoint-second inward rows `E(z,v)=I(z,v,2+v)`, with density
  `i(z,v)` on `0<z<1, -z<v<z`.

All densities may be merely integrable. Bounded densities are used for
the explicit estimate in Section 8. No density monotonicity is imposed.
The excluded center boundary `v=z`, and additional atoms at arbitrary
first-turn curves, require their closed capture formulas separately.
Finite M1 and late-M2 atoms are supported by the implementation, but the
bounded-density estimate below does not silently treat their jumps as
Lipschitz terms.

The nonnegative-princess restriction is removable for every one of
these components, and indeed for every reflected monster pair. For a
continuous princess p, set `r=abs(p)`. The earlier capture in each pair
is the first radial contact `abs(m)=r`, and is identical for p and r.
If that contact is at zero, both orientations capture there. Otherwise
rename the monster so that `m(t1)=r(t1)>0`, and put
`sigma=sign(p(t1))`. The original first capture is against `sigma*m`.
At the later r capture t2 against `-m`, the continuous difference
`p+sigma*m` changes from sign sigma at t1 to the opposite weak sign at
t2. Thus the other original capture occurs by t2. Therefore

    T(m,p)+T(-m,p) <= T(m,abs(p))+T(-m,abs(p)).        (1)

Absolute value preserves the Lipschitz bound. This argument is
independent of the number or location of monster turns. It is the same
universal comparison proved in
`research/08-continuum/CHARACTERISTIC_RESPONSE.md`, Section 3.

## 2. The last-U=1 cutoff and endpoint completion

For a nonnegative princess, write `U=t+p(t), V=t-p(t)`, and let

    a=p(0),  c=last V on U=1,  L=2+c.

Initially `0<=a<=1` and `-a<=c<=1`. For now take interior values
`a<1,c<1`. Both characteristic coordinates are nondecreasing, and
`0<=U-V<=2`.

All alpha thresholds that still matter after fixing the prefix are at
most L:

* a missed E first leg has `v<psi(z)<=c`, hence second threshold
  `2+v<=L`;
* a positive M1 start above a has threshold `2-z<=2-a<=L`;
* a late positive-M2 start above a has `s<=2-z<=2-a<=L`;
* all other alpha thresholds of the stated class, including both early
  families, are at most one.

After U=L, replace the continuation by the least feasible V,

    V(U)=max(V(L),U-2).                              (2)

This changes no relevant alpha inverse and weakly increases every
remaining beta inverse. A late-M2 early/final capture is also
nondecreasing as its beta inverse increases, including its upward
capture jump. Thus (2) weakly improves the entire law's response.

Since `V(L)<=L<3`, the completed path has exactly

    beta(3)=4,  beta(s+2)=s+3 for every s>1.          (3)

These are consequences of completion, not substitutions made for the
original arbitrary path. The reflected `beta(s)` terms are retained
exactly. The absorption time is `1+V(L)`, which may exceed two. Neither
V nor the final level is clamped at one.

The route horizon of this class is at most six. This gives a uniform
bound of 24 for its unnormalized four-score per unit mass.

## 3. The two controls and trace convention

Use the prefix inverse P and the post graph Z:

    P(v),  -a<=v<=c,      P nondecreasing,
                         max(a,v)<=P(v)<=1;
    Z(U),   1<=U<=L,      Z nondecreasing,
                         c<=Z(U)<=U.                (4)

P is the last/right beta-inverse trace where it occurs in a first-miss
indicator. At regular levels it equals the first inverse. A density
in v does not charge its countably many outgoing-plateau exceptions.
The physical alpha inverse uses the first/left Z trace. A closed early
test at a turn `U=s` instead uses the last/right Z trace. These
distinctions are retained explicitly for atomic rows in the code.

An original U=1 plateau is represented in P up to its last level c.
Every positive alpha(1) price is relaxed upward to `(1+c)/2`. This
relaxation is jointly approachable with all the stated diffuse
components. Scale the prefix coordinates by `1-epsilon`; join its
endpoint `(1-epsilon,(1-epsilon)c)` outward to
`(1+epsilon,(1-epsilon)c)`; and map the post graph by

    Unew=2epsilon+(1-epsilon)U,
    Vnew=(1-epsilon)V.                              (5)

The post spatial gap remains in `[2epsilon,2]`, and its new cutoff is
`Lnew=2+(1-epsilon)c`. Complete outward afterward. This is a legal
path whose first U=1 crossing approaches c and whose next inward
motion is strictly after U=1. Thus an initial jump of Z at U=1 in the
relaxed control is not mistakenly declared an exact physical fixed-I1
capture plateau. Diffuse first-turn boundaries have zero mass. The
remaining fixed beta(1) atom is delayed, rather than advanced, by this
one-sided approximation. Dominated convergence, or its lower-limit
version at that beta atom, proves approach from at least the declared
relaxed score.

This proves equality of the unrestricted response supremum and the
supremum of the functional below over a,c,P,Z. It does not assert that
one maximizing physical path exists, or that equality holds in each
fixed-a,c stratum without the limiting convention. Boundary values
`a=1` and `c=1` are included by their one-sided limits as well as their
actual first-capture values.

## 4. The endpoint component: one attractive pair

Put, with physical-triangle restrictions understood,

    T_z(v)=integral_v^z i(z,w)dw,
    j_a(v)=integral_|v|^a i(z,v)dz,
    C(P,v)=integral_P^1 i(z,v)dz.

The endpoint component's only nonseparable term is

    integral_-a^c Z(2+v) C(P(v),v)dv.                (6)

Its prefix unary is

    qE(v,P)=j_a(v)P
       -integral_max(a,|v|)^P [T_z(v)+(2-z)i(z,v)]dz. (7)

The lower limit in (7) matters when c>a: values z<v lie outside the
physical triangle and must not be assigned the polynomial's formal
extension. On `1<U<2-a` the missed-alpha source is independent of P,
so it gives the post unary

    Z(U) integral_|U-2|^1 i(z,U-2)dz.                (8)

For beta prices define the finite positive measure

    nu_a(dB)=j_a(B)dB on [-a,a]
          +[integral_|B-2|^1 i(z,B-2)dz]dB on [1,3].

Write `G_a(Z)=nu_a((Z,infinity))`. The post beta unary is `G_a(Z(U))`,
and the outward-completion unary at `z=Z(L)` is

    (2+z-L)G_a(z)+integral_z^3 G_a(t)dt.             (9)

The first part of nu is direct low-start capture; the second is the
reflected capture. In particular, (9) includes reflected thresholds
above one, without a beta ceiling.

For completeness, the absolute endpoint constant used by the code is

    CE = integral_a^1 (z+c)T_z(c)dz
       + integral_-1^c (2+v)[j_1(v)-j_a(v)]dv
       + integral_-a^a v j_a(v)dv + integral_c^a j_a(v)dv
       + integral_1^3 (B+1)j_1(B-2)dB,              (10)

where empty integrals vanish and every column is zero outside its
physical support. Equations (6)-(10) are the complete four-score.

Set `W=-Z`. The pair reward becomes `-W C(P,v)`. Its threshold mixed
difference is

    (W1-W0) integral_P0^P1 i(z,v)dz >=0.             (11)

Thus the pair is attractive for arbitrary nonnegative i; neither a
factorization nor density monotonicity is needed. P increases in v,
whereas W decreases in U. Both are directed order constraints.

For the useful special case `i(z,v)=h(z)`, if `H'=h`, (7) reduces to

    [H(a)-H(|v|)]_+ P
       -(2-v)[H(P)-H(max(a,|v|))].                  (12)

This formula, and not a frozen-prefix suffix optimization, is what
allows both controls to be optimized simultaneously.

## 5. Unary components and the additional attractive early families

For a fixed a, signed M1 gives a positive measure of alpha and beta
thresholds. The exact signed atom formula is

    unreflected: beta(-x) if x<a; alpha(2-x) if x>a;
    reflected:   alpha(-x) if x<-a; beta(2-x) if x>-a,

with zero on each corresponding initial equality. All thresholds
before one are prefix unaries; those above one are post unaries.
The endpoint pair contributes `w0*(1+c)+2w0*beta(1)` to the
four-score. The beta(1) term is not replaced by two.

For a fixed-second inward density j, define its row and low-start
column in the same way as for i, and let its total mass be M. Its
four-score is

    (1+c) integral_a^1 m(z)dz +8 integral_0^a m(z)dz
    +integral_a^1 (z-1)T_z(c)dz +2M beta(1)
    +integral_-a^c {
        (v+P-8)j_a(v)
        -integral_max(a,|v|)^P
              [T_z(v)+(1+c-z-v)j(z,v)]dz }dv.       (13)

Only (3), and the joint alpha(1) convention, are used here. Formula
(13) does not make the old simultaneous beta(1)<=2 relaxation.
The fixed positive/negative M2 turn lines are the corresponding
one-dimensional first-turn boundary formulas, and remain unary.

For a late M2 atom `(x,s)`, the reflected term is `alpha(-x)` if
`x<-a`, zero if `x=-a`, and `beta(s)` otherwise. The unreflected term
is `alpha(s)` if `x>a`, zero if `x=a`, and, for `v=-x`,

    beta(v) if phi(v)<=s;  s+3 otherwise.            (14)

When v<=c this is a prefix unary. When v>c, its twice-capture score is

    v+1 + integral_1^s 1_{Zext(U)<v}dU
        +(s+6-v)1_{Zext(s+)<v},                    (15)

where `Zext(U)=max(Z(L),U-2)` after L. The last indicator is zero on
the endpoint face `s=v+2`, by the closed physical bound `phi(v)<=v+2`.
The right trace at s in (15), versus the left trace in alpha(s), is
essential at an atom. Integrating (15) against either signed joint
density leaves unary potentials. In density notation the corresponding
local beta price has derivative

    integral_(s>=U) h(z,s)ds +(U+6-v)h(z,U),         (16)

as obtained independently by differentiating the early/final branch.
The high positive-start alpha marginal is supported in
`1<U<=2-a<=L` and is also unary.

All these unary potentials may be nonconvex, discontinuous at retained
atoms, and nonmonotone. Minimum-cut optimization does not require a
convexity or first-crossing hypothesis for a unary table.

### Early M2: keep its missed beta inverse

For `|x|<=s<1`, the shifted M2 first-contact formula still applies,
but its missed capture is `beta(s+2)`, which must not be replaced by
`s+3`. If `x<a`, put v=-x. When v<=c the unreflected twice-capture is

    (v+P(v))1_{P(v)<=s} +[2beta(s+2)]1_{P(v)>s}.    (16a)

When v>c it is simply `2beta(s+2)`. If x>a the capture is alpha(s);
the reflected capture is alpha(-x) for x<-a and beta(s) for x>-a.
Each corresponding initial equality contributes zero. These formulas
also handle a>s: the legal P>=a makes every early test fail.

The missed indicator in (16a) increases with P, while every post
unary composing `2beta(s+2)` increases with W=-Z. Their product is
attractive. Thus early M2 adds positive prefix/post pairs, not an
arbitrary isotonic functional. Its reflected beta(s) term is unary
even when s<1.

### Early M3: the same positive missed-capture product

For `|x|<=s<1`, define the route by

    (0,x), ((s-x)/2,(s+x)/2),
    ((s+1)/2,(s-1)/2), (2,1), (4,-1).

Its unreflected capture has the same first two cases as early M2,
except that the missed capture in (16a) is beta(1). Its reflected
capture is

    alpha(-x) if x<-a;
    beta(s) if x>-a and s<=c;
    beta(3)=4 if x>-a and s>c,

with zero at x=-a. Hence its only mixed term is again an increasing
prefix missed indicator times an increasing post beta score. For a
density in s, the missed mass `K(P)=integral_(s<P) m(x,s)ds` increases
with P. The product `K(P)*2beta(1)` gives attractive edges from that
prefix level to all post beta(1) threshold variables.

The center-reaching condition `s>=|x|` is essential for the simple
reflected alpha(-x) branch. For negative x=-z and a same-half first
turn `-z<=s<z`, the reflected M2 route is exactly E(z,s). The analogous
reflected M3 route with second V=1 is exactly I(z,s,1). Thus the E
and fixed-I1 components already cover these same-half families, with
their correct first-miss alpha branch. They are not put through the
incorrect center-reaching formula.

## 6. Exact finite cuts and the continuum cut formulation

On a finite arrangement, use ordered labels for P and for W=-Z.
Domain-cell integrals of (11) give nonnegative mixed threshold
differences. A positive binary reward `b*X*Y` can be written as
`b*X-b*X*(1-Y)`, so it is one unary plus a directed edge of capacity b.
Threshold nesting and the P/W order constraints are hard directed
implications. Arbitrary unary increments go to the source or sink.

This is exactly the finite problem solved by `monotone_cut.py`.
Its returned flow is checked for capacities and conservation, and its
cut capacity equals the flow. Thus a returned exact rational cut is a
global certificate for that finite arrangement, not a local best reply.

The same threshold expansion is valid in the continuum. Use
`X(v,z)=1_{P(v)>=z}` and `Y(U,w)=1_{W(U)>=w}`. The positive cross
measure is `i(z,v) dz dv dw`, joining X(v,z) to Y(2+v,w).
Nesting and monotonicity are directed order constraints. This is an
exact continuum attractive-cut variational formulation. Calling a
finite graph cut does not, by itself, certify the continuum cut.

## 7. The outer variables and the actual response theorem

Let M be the total monster mass, and let `F(a,c,P,Z)` be the complete
four-score above. Then the stated law's unrestricted response is

    sup_p E[T] = (1/(4M)) sup_(a,c,P,Z) F(a,c,P,Z).   (17)

The outer region is `0<=a<=1,-a<=c<=1`, with the boundary and
one-sided trace conventions of Section 3. No initial-start atom or
ordinary-wave ansatz for a lower law appears in (17).

A finite control cut at one a,c is insufficient for an upper bound.
A proposed certificate must cover the entire outer region, including
`a->1-`, `c->1-`, and the degenerate prefix face `c=-a`.
In particular, `c=1-` is not interchangeable with exact c=1 at the
beta(1) atom: a late first beta(1) inverse may be approached from below.
An implementation must retain that one-sided trace state or separately
bound the boundary limit. The actual endpoint initial-capture value
likewise must not replace the `a->1-` supremum.

For bounded densities, a useful one-sided outer comparison is obtained
by choosing `a'<=a`, `c' >= max(c,-a')`, `c'<1`. Retain P on the
common interval, extend it by P=1 up to c', and replace the post graph
by `max(c',Zext)`. Apart from starts in `[a',a]` and direct first-beta
thresholds in `[c,c']`, the raw capture formulas show only unchanged
or delayed captures. Consequently the four-score loss is at most 24
times the law mass in those two parameter strips. This gives an
explicit outer modulus on compact regions below c=1; the one-sided
beta atom at the last face remains a separate trace calculation.

Completion does not prove `Z(L)<=1`. A lower construction that assumes
absorption by time two must establish that the selected upper response
face has this additional property, or allow the later absorption time
`1+Z(L)` in the lower law.

## 8. A uniform continuum approximation estimate

Assume all displayed densities are bounded. Write their suprema as
`F,E,G,H0,J,I,Hplus,Hminus,Hearly,Mearly`, where E denotes ell here. Define

    CP=F+2E+G+2H0+6J+8I+Hplus+4Hminus
          +20Hearly+20Mearly,
    CZ=F+Hplus+I.                                  (18)

The prefix part, including its endpoint cross term for a fixed Z, is
CP-Lipschitz in P. The factor eight in its endpoint term uses
`|Z|<=3`. After separating positive alpha prices, every remaining
post term is nonincreasing in Z: lowering Z delays all beta captures,
including (15). The positive alpha coefficient is at most CZ.
For the early families, differentiating the turn-density integral in
(16a) gives a bounded tail plus a density times the capture jump.
The latter twice-capture is at most eight. Their other alpha/beta
marginals are also bounded by the turn interval length. The factor
20 is a common conservative bound for these contributions. Their
mixed beta terms improve when Z is rounded downward.

Fix interior a,c and take a domain partition of maximum length delta,
with a range net of maximum gap delta. Include the paired cuts
`U=2+v` and `U=2-a`. Suppose `delta<min(1-a,1-c)`.
First cap P at `1-delta`.
In each v cell, sample its left trace, round it downward, then clamp
it below by `max(a,v_right)`. The resulting monotone constant prefix
is legal and satisfies

    integral |Pdelta-P| <= 7delta.                 (19)

Indeed the cap costs at most `2delta`, left sampling costs at most
`delta*TV(P)<=delta`, range rounding costs at most `2delta`, and
the diagonal clamp costs at most `2delta`.

In each U cell, sample Z on the left, round downward, and clamp below
by c. This is a legal monotone constant post graph with `Zdelta<=Z`
and

    integral |Zdelta-Z| <=4delta.                  (20)

The range and total variation are each at most two. Any loss in the
terminal beta term is nonpositive under this rounding. Therefore the
finite-control supremum on an arrangement containing these choices
satisfies

    sup_cont F <= sup_finite F +(7CP+4CZ)delta.      (21)

The finite supremum is exact and can be certified by a cut. This bound
is deliberately coarse; it is an analytic control error, not an
instruction to refine the current experimental mesh. Different domain
and range gaps give the corresponding separate BV terms.

For merely integrable densities, truncate each component nonnegatively
at height K. All truncations remain physical laws. If the removed
total mass is epsilon_K, the four-score changes uniformly by at most
`24epsilon_K`. Apply (21) to the bounded truncation and then let
`K->infinity`. This proves convergence without assuming smooth optimal
controls. More generally a two-dimensional kernel error on an area-A
disagreement set is bounded by
`K*A+integral_(kernel>K) kernel`; this is its absolute-continuity
modulus and covers nonuniform density truncations.

Additional atomic alpha thresholds or first-turn curves need their
own exact trace states or brackets. They are not covered by (18).
The endpoint/fixed-turn beta(1) atom is already protected by downward
Z rounding and the separate outer-boundary convention.

## 9. Implementation and independent checks

`endpoint_paired_controls.py` builds the endpoint attractive pair,
exact reflected beta unaries, outward-completion term, and absolute
constant. Its signed M1 atom adapter retains both initial equalities.
`endpoint_unary_families.py` adds fixed-I1 polynomial densities,
closed early/late M2 and early-M3 atoms, and signed
piecewise-polynomial M1 and fixed-turn M2 start densities.
All features are linear in the physical monster masses.

`verify_endpoint_paired_cut.py` passes 4,748 exact checks, including
1,380 exhaustively compared feasible controls, two finite global cut
optima, 26 complete physical law scores, 3,328 independent capture
triangles, and 12 fixtures with V above one. The separate generic cut
self-test covers 5,020 exhaustive feasible assignments in 92 fixtures.
The extended-family verifier passes 6,544 exact checks: 784 exhaustive
controls, two global finite cuts, 16 absolute whole-law physical scores,
5,718 independent capture triangles, 14 joint-epsilon physical scores,
two exact epsilon limits, and eight positive-c clipping cases. It
includes signed early M2/M3 rows, physical-triangle clipping,
first/last turn traces, and endpoint-turn equalities.

These identities and approximation bounds complete the response
reduction for the specified law class. Constructing a normalized law
whose entire response face matches a legal unrestricted lower law,
and certifying its continuum and outer maxima, remain open.
