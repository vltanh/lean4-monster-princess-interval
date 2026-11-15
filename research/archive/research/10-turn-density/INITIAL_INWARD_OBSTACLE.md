# A contractive initial-inward obstacle equation

This note turns the exact initial-inward response into an inverse-integral
map. It establishes a local fixed-point construction under explicit box,
exterior, and projection hypotheses. The prescribed outer traces and the
joint terminal moments have not yet been instantiated in a matching law.

**The second-turn coordinate in this note is fixed at U=1.** The exact
finite comparison in `INWARD_TURN_DOMINANCE.md` shows that an active such
route is strictly beaten whenever its last middle-capturable rank has
already entered a positive-length outgoing column plateau before U=1.
In particular, appending an ordinary incoming cap followed by a final
outward leg does not turn this construction into a matching lower law.
The cap estimates below remain valid conditional components; a complete
construction must include free second turns, or a genuinely different
incoming/turn attachment. A small fixed-turn residual is not a substitute
for that missing inequality.

## 1. Exact derivative-free cost

Use the hypotheses and first-contact conventions of
`INITIAL_INWARD_CDF.md`. In a continuous initial phase put

    x=1-a,       y=1+v,       0<x<=y,
    r(x)=1-A(1-x),
    e(y)=1-R(1,-1+y),
    D(x,y)=1-R(1-x,-1+y),
    w=e^{-1},     W(z)=integral_0^z w(s)ds.

The inverse is used only on a strictly increasing branch of e. Let

    V4=5+integral_0^1 c_1(q)dq,
    c_1(q)=2 alpha_q(1)-1.

Then the exact inward score is

    4CI(1-x,-1+y)-V4
      =8r(x)-Phi_xy(D(x,y))
       -integral_x^y D(x,z)dz
       -(8-y)(r(x)-e(y))_+
       -integral_0^x(r(x)-D(t,y))_+dt,                  (1)

where

    Phi_xy(z)=W(z)+(x-y)z.                             (2)

Indeed, the row part of the original formula contributes
`y-x-integral D`, and

    J(1)-J(1-D)=integral_0^D[-1+w(s)]ds=-D+W(D).

The constants and the remaining linear D terms give (1).

Here D is the **full** radial deficit. A high-rank submeasure deficit may
replace it only where the retained low ranks have full mass below every
point used in the row and column integrals. For a tail separated from all
low initial positions, this holds throughout a sufficiently small negative-V
initial patch. Otherwise the fixed low contribution must be retained in
(1); it must not be silently dropped.

Write the right-hand side of (1), before subtracting Phi, as S_D(x,y).
Then

    CI>=V4/4  if and only if  Phi_xy(D)<=S_D.           (3)

On the branch `r(x)>e(y)`, the nominally large term `8r` cancels:

    S_D=y r(x)+(8-y)e(y)
        -integral_x^yD(x,z)dz
        -integral_0^x(r(x)-D(t,y))_+dt.                (4)

This cancellation is the source of the small local contraction constant.

## 2. An explicit invariant inverse box

First hold r, e, and the exterior field fixed. Let all unknown points lie
in a prescribed patch

    P subset {0<x<=y<=Y, e(y)<r(x)}.

Assume the following bounds hold for every input field being considered:

    0<=r(x)<=R sqrt(x),
    0<=D(t,z)<=M sqrt(z),
    alpha s<=e(s)<=beta s  for 0<=s<=Z,                (5)

where `0<alpha<=beta`, and e is continuous strictly increasing. Choose
positive inverse-box constants L,H with

    H sqrt(Y)<=e(Z).                                  (6)

A sufficient condition for (6) is `H sqrt(Y)<=alpha Z`. The interval
`[0,Z]` is an **inverse horizon**: a bound on e only up to Y is not enough,
because `w(H sqrt(Y))` is generally of order `sqrt(Y)`.

The scalar bounds in (5) imply, for `0<=z<=H sqrt(Y)`,

    z^2/(2beta)<=W(z)<=z^2/(2alpha).                   (7)

On P, elementary integral bounds give

    [8alpha-alpha Y-(2M/3+R)sqrt(Y)]y
       <=S_D(x,y)<=[8beta+R sqrt(Y)]y.                (8)

The lower estimate deliberately allows the column its full upper bound
`x r(x)`. Combining that column with `y r(x)` improves its error term from
`2M/3+R` to `2M/3`; either estimate is valid.

Consequently the inverse root lies in

    L sqrt(y)<=T[D](x,y)<=H sqrt(y)                    (9)

whenever

    L^2/(2alpha)
       <=8alpha-alpha Y-(2M/3+R)sqrt(Y),
    H^2/(2beta)-H sqrt(Y)>=8beta+R sqrt(Y).             (10)

This follows by evaluating Phi at the two endpoints. In this box,

    partial_z Phi=w(z)+x-y
       >=[L/beta-sqrt(Y)]sqrt(y)=c sqrt(y).            (11)

Require `c>0`. The root is therefore unique. Conditions (6), (10), and
(11) prove actual inverse-box invariance; they do not appeal to a lower
clamp which could violate (3).

For example, the purely scalar constants

    alpha=2/5, beta=1/2, R=M=2,
    L=6/5, H=5/2, Y=1/64

satisfy (10). They give `c=91/40` and a fixed-front contraction factor
`sqrt(Y)/c=5/91`. However they require the e comparison through at least
`Z=25/32` if (6) is checked by `alpha Z`; they are **not** a verified
small endpoint attachment. A shorter known inverse horizon requires a
correspondingly smaller Y.

## 3. Fixed-front contraction

For two fields with the same exterior, r, and e,

    |S_D-S_E|<=y ||D-E||_infinity.                     (12)

The row length is `y-x`, the column length is x, and the positive-part
map is 1-Lipschitz. The inverse bound (11) gives

    ||T[D]-T[E]||_infinity
       <=sqrt(Y)/c ||D-E||_infinity.                  (13)

Thus the inverse map is a strict contraction when `sqrt(Y)<c`.
An upper cap is safe for the response inequality: if a prescribed physical
cap H0 obeys `H0>=L sqrt(y)`, then

    min(H0,T[D])<=T[D]

still satisfies (3) at a fixed point, since Phi is increasing in the box.
A lower cap is not automatically safe. It requires the separate gate

    S_D(x,y)>=Phi_xy(L0(x,y))                          (14)

for the actual lower obstacle L0. The inverse box supplies (14) for
`L0=L sqrt(y)`, but not for an arbitrary initial or exterior boundary.

### Precise local existence statement

Let K be a nonempty closed set of bounded fields with the prescribed fixed
exterior and the box (9) on P. Suppose:

1. The inverse-horizon, scalar box, and strict contraction conditions above
   hold for every member of K.
2. A chosen nonexpansive projection P0 and fixed upper cap produce a field
   in K, preserve the fixed exterior, and only lower the uncapped root on P.
3. Every lower obstacle imposed by that projection satisfies (14). Any
   response requirements outside P are separately verified against the
   changing interior integrals.

Then `D -> P0(min(H0,T[D]))` has a unique fixed point in K. Uniform Picard
iteration converges to it; after an iteration with successive difference
epsilon, its remaining supnorm error is at most
`epsilon kappa/(1-kappa)`, where `kappa=sqrt(Y)/c`. The fixed point obeys
the inward inequality (3) throughout P. Where neither the cap nor the
projection lowers the root, the inward cost is exactly `V4/4`.

This is a genuine local existence statement once its exterior and
projection gates are supplied. It is not an assertion that every proposed
attachment supplies them. In particular, it does not assume an active
inward sheet fills the whole wedge `e(y)<r(x)`.

## 4. Transport and slope projections

The legal transport cone is

    D_x>=0,       D_y>=0.

On a rectangular extension of the domain, its greatest minorant is

    M f(x,y)=inf_{s>=x,t>=y} f(s,t).                   (15)

It is nonexpansive in supnorm and is no greater than f. If a lower barrier
L0 is itself transport monotone and satisfies `L0<=f`, then `L0<=Mf`:
every point in the infimum has `L0(s,t)>=L0(x,y)`. The same observation
retains a fixed exterior encoded by compatible equal lower and upper
obstacles there. Compatibility must be checked; arbitrary frozen boundary
values need not admit any monotone extension.

Diagonal slope restrictions are also difference inequalities. For example,

    r(y)-r(x)<=C(sqrt(y)-sqrt(x)),       x<y,           (16)

can be added to the transport inequalities. The greatest function below f
satisfying all these inequalities is the min-plus minorant

    P f(z)=inf_w [f(w)+d(z,w)],                        (17)

where d is the infimum of the costs of finite constraint chains. Each
constraint `g(z)<=g(w)+cost` is an edge in the chain. Infima of admissible
minorants, or equivalently this constraint closure, show that P is
nonexpansive and no greater than f. A lower barrier satisfying all the
same difference inequalities is preserved. The zero-cost coordinate
edges alone give (15).

One must test the lower barrier against **every** added slope constraint;
transport monotonicity alone is insufficient. A construction of the form

    max(e(y), min(L0 sqrt(y), C0 x^(1/4)))

can separate an initial `sqrt(y)` region from a smaller incoming corner,
but its diagonal value, its exterior compatibility, and the requested
slope bounds still require explicit checks. No projection is permitted to
repair a failed lower cost gate by increasing D.

## 5. The diagonal and the positive-response moments

For a transport-monotone field with its true initial diagonal,

    r(x)<=D(x,y)<=r(y),       D(x,x)=r(x).              (18)

The exact positive-response coupling derived in
`CURVED_TERMINAL_SOURCES.md` is

    (8-2x)e(x)=x[3-r(x)]+Q(x),
    W(r(x))=(8-x)e(x)+integral_0^xD(t,x)dt.            (19)

Here Q is the retained low-rank post-one source, under that note's
separation and trace hypotheses. The second identity is the diagonal
`CI=Cg=V4/4` condition. It must not be replaced by a fixed ordinary-tail
history. Transport also gives the useful necessary moment bounds

    8e(x)<=W(r(x))<=(8-x)e(x)+x r(x).                 (20)

### A useful lower-bound gate

For a field already satisfying the second identity in (19), the root
cannot pass below the physical lower obstacle r(x) on an active-rank
branch if

    (8-y)e'(y)>=e(y)+r(y).                            (21)

To see this, put `G(y)=S_D(x,y)-Phi_xy(r(x))`. At y=x,
the diagonal moment gives G=0. On `e(y)<r(x)`,

    G'(y)=2r(x)-e(y)+(8-y)e'(y)-D(x,y)
                +integral_(D(t,y)<r(x))D_y(t,y)dt>=0.

The same argument holds with Stieltjes differences. This is a gate for a
moment-consistent field, not by itself a uniform invariant-box proof for
an iteration which does not retain those moments.

### When projection preserves diagonal equality

There is a separate noncircular diagonal-preservation test. Suppose the
unprojected proposed field f has increasing diagonal `g(x)=f(x,x)`,
satisfies `f(x,y)>=g(x)` for `y>=x`, and its diagonal obeys (16).
Extend below the diagonal by `g(min(x,y))`. Then

    b(x,y)=g(min(x,y))

is an admissible minorant with the same diagonal. Therefore both the
transport minorant and the stronger constraint minorant (17) retain that
diagonal exactly. The exterior and any incoming upper cap must also
dominate this barrier.

For the raw I root on `e(y)<r(x)`, these properties have direct sufficient
conditions. Its implicit y derivative has numerator

    (8-y)e'(y)-e(y)+r(x)-D_input(x,y)
       +integral_(D_input(t,y)<r(x))D_input,y(t,y)dt
       +D_root(x,y).                                  (22)

It is positive under the small-tail bounds, for example if
`(8-y)e'(y)>e(y)+M sqrt(y)`. On the diagonal the right-hand side is

    (8-x)e(x)+integral_0^xD_input(t,x)dt,

whose derivative is `(8-x)e'-e+r+integral D_y>0` under the same bounds.
Hence the raw root increases in y and its diagonal increases in x. If an
input y modulus gives `D_y<=C/(2sqrt(y))`, then (22) yields

    D_root,y <=[8beta+(R+H+C/2)sqrt(Y)]/[c sqrt(y)].    (23)

The analogous diagonal bound omits the `-sqrt(Y)` part of c. These are
checkable sufficient conditions for a loose slope constraint not to bind
the raw diagonal. They are not a substitute for checking the incoming
corner and fixed exterior, where the `sqrt(y)` inverse box may end.

## 6. Coupling fronts and the incoming cap

The fixed-front theorem does not yet solve (19). There is nevertheless a
small-variation mechanism for a joint map. Read r from the input diagonal
and define e by the first equation in (19). With Q fixed,

    delta e(s)=-s delta r(s)/(8-2s).                   (24)

If `e'>=alpha` on the complete inverse horizon and the extension of r
beyond the unknown patch is supnorm nonexpansive, then

    |delta W(z)|
       <=z^2 ||delta r||/[2alpha^2(8-2Z)].             (25)

Indeed, inverse stability gives
`|delta w(q)|<=q||delta r||/[alpha^2(8-2Z)]`; integrate in q.
Using (4), variation of r, e, and both integrals contributes at most

    [3+(8-Y)/(8-2Y)]y ||delta D||

to S. Thus the joint raw root has the explicit bound

    kappa_joint <= sqrt(Y)/c *
      [3+(8-Y)/(8-2Y)+H^2/(2alpha^2(8-2Z))].           (26)

This is small for a sufficiently small patch. It is conditional on the
same inverse horizon, on the branch/rank separation, and on preserving
the e slope bounds. Equation (16) and the exact formula (19) can supply
those slope bounds, but they must be checked with Q and the exterior.

Finally the incoming cap should be applied **after** the transport
projection if its row moment is to remain exact. For a monotone uncapped
initial field Z, the cap has the form

    D_i(x,y)=max(e(y),min(i(x),Z(x,y))).                (27)

`CURVED_TERMINAL_SOURCES.md` gives the scalar negative-M1 row equation
which determines i. Its derivative in i is the incoming plateau width;
under a positive plateau-width gate, the scalar cap is stable. If
`Z>=e`, the cap only lowers Z, so at a fixed point it preserves the
inward inequality. If i is increasing and dominates the new diagonal,
it preserves transport and that diagonal as well.

The safe order is therefore: raw I root, transport/slope minorant, update
the diagonal fronts, then solve the incoming cap. A full contraction for
this joint composition still needs the cap's front-dependence bound and
the exterior gates. The fixed-front result above must not be promoted to
such a theorem before those obligations are discharged. No unrestricted
game value or matching strategy is claimed here.

### Weighted front norm and a composition test

The incoming cap is better conditioned in the norm

    ||delta D||_* = sup_(x,y) |delta D(x,y)|/sqrt(y).   (28)

Then `|delta r(s)|<=epsilon sqrt(s)` and (24) gives
`|delta e(s)|<=epsilon s^(3/2)/(8-2s)`. Repeating the inverse calculation
on the complete inverse horizon gives

    |delta W(z)|
      <=2 epsilon z^(5/2)/[5alpha^(5/2)(8-2Z)].        (29)

The row, column, and front terms in (4) are bounded by

    [11/3+(8-Y)/(8-2Y)] epsilon y^(3/2).

Thus a joint raw-root constant in (28) is

    kappa_* <= (1/c)[
       (11/3+(8-Y)/(8-2Y))sqrt(Y)
       +2(H/alpha)^(5/2)Y^(1/4)/(5(8-2Z)) ].          (30)

Here the extension of the front beyond Y must also be nonexpansive in
the weighted norm through the inverse horizon. The branch separation
must be uniform for the two inputs being compared; a moving switch to
an unrelated exterior formula is not covered by (30).

A generic projection (17) is not automatically nonexpansive in (28),
because a constraint chain may move to a larger y. There is a useful
special case which avoids that problem. If the proposed field is already
nondecreasing in y, its transport minorant is simply

    M_x f(x,y)=inf_(s>=x) f(s,y).                      (31)

It keeps y fixed and is nonexpansive in (28). An infimum of functions
sharing the modulus `C(sqrt(y2)-sqrt(y1))` shares that modulus. Hence
(22)-(23), together with the same property of the exterior and caps, can
make the diagonal slope gate invariant without adding slope edges.
The diagonal-preservation barrier above then applies.

The cap estimate in `CURVED_TERMINAL_SOURCES.md` supplies a finite
weighted constant under its initial-speed and plateau-separation gates.
For example, on its stated box `xi<=1e-5`, its front contribution is at
most `1.071+1.07 Y^(1/4)` and its additional field contribution to the cap
is at most `.631 sqrt(Y)`; the directly unclipped field has constant one.
Fixed low sources contribute no difference. Those estimates require the
same front norm through `s<=5sqrt(Y)` and a feasible unsaturated cap root.

Consequently, if all the following gates hold on a closed nonempty class,
the **joint** local composition is a Banach map:

* the explicit inverse box and full inverse horizon;
* a common active-rank patch containing every uncapped root, with compatible
  incoming/outgoing continuation outside it;
* the y monotonicity and common modulus used by (31), with the raw
  diagonal preserved;
* the exact front relation (19), its source and inverse-slope bounds;
* the cap's monotonicity, separation, feasibility, and weighted estimates;
* the strict numerical inequality `K_cap kappa_*<1`.

At such a fixed point the local positive-M1/M2 moments hold by the front
relation and diagonal equality, the negative-M1 row moment holds by the
final cap, and the inward inequality holds because every subsequent block
only lowers the root. These are the **fixed-second-turn** equations. If the
cap leaves the plateau described at the start of this note, the free-turn
comparison gives a strict attack despite all these equations. The common
exterior/active-set gates and the free-second-turn response remain
obligations; scalar smallness of (30) does not discharge them.

## 7. The inactive-rank region is already controlled by direct left travel

The region `B=R(s,v)<=A(a)` need not be solved by an inward equality
equation. For an initial-inward route which turns outward to characteristic
`U=s>=a`, direct left travel from the same start, followed by its right
endpoint sweep, captures every ordered princess no later.

Every initially lower positive path is captured earliest by direct left
travel: its monster position is the smallest one allowed by the speed
bound until the first crossing. Initially higher ranks are not captured
on the inward route's first segment or middle outward segment when closed
`B<=A`. Their positive gap cannot close on its subsequent unit-left leg.
The direct-left route begins its final right sweep at `1+a<=1+s`, so it
also captures those remaining ranks no later. The negative reflected
paths are initially lower and obey the same direct-left comparison. This
argument uses first contact and does not require endpoint absorption.

Under the additional standing assumptions `beta(1)=2` and absorption by
time two, there is a quantitative version for `s=1`. Write
`t1=(a+v)/2` and `Delta=(B-A)_+`. The negative reflected copy loses at
least `1-a` under I; each initially higher positive rank missed by the
middle segment also loses at least `1-a`, while each of the Delta ranks
caught on that segment can gain at most `3+a-t1`. Therefore

    CI-Cell >=[(1-a)(2-A)-(4-t1)Delta]/2.              (32)

In the deficit coordinates, an active equality `CI=Cell` requires

    r(x)-e(y)>=2x[1+r(x)]/(8+x-y).                    (33)

In particular there is a strictly inactive strip before `B=A`, not just
an absence of active points on that boundary. Once the negative-M1 cost
is controlled, all `B<=A` inward inequalities follow pointwise. Formula
(33) helps locate a nonsingular active patch for the inverse map. It does
not by itself guarantee that an arbitrary field formula glued across the
strip is continuous or transport monotone.
