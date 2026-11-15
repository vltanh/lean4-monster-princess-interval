# The free-second-turn inward field and its support surface

The fixed-`U=1` inward obstacle is only one response component. The strict
plateau deletion in `INWARD_TURN_DOMINANCE.md` requires the second turn
to be optimized. This note gives a source-free field comparison for that
optimization, a local restriction on its active support, and a concrete
transport-legal curved incoming saturation. No complete matching law is
asserted.

## 1. Exact cost with a free second turn

Use the route `I_s(a,v)` and trace conventions of
`INWARD_TURN_DOMINANCE.md`. Suppose the ordered nonnegative paths stay
at the positive endpoint after time two. For

    0<a<1, -a<=v<a, a<=s<=1,

write

    A=Pr(p(0)<=a),       L=R_<(a,v),
    B=R(s,v),           M=max(A,B),
    N=integral_-a^v R_<(a,w)dw,
    F_s(L)=integral_v^s(L-R_<(s,w))_+dw,
    H(s)=integral_s^(s+2)R(U,s)dU.

The exact identity already checked in `TWO_INTERIOR_TURN_CDF.md` is

    4CI_s=4s+8-2(s+3)A+N+(2s-a-v)L-F_s(L)-H(s)
          -(s+6-v)(B-A)_+
          -integral_a^s(R(U,v)-A)_+dU.                 (1)

It includes first-contact atoms with the displayed strict initial row and
closed middle column. The boundary `v=a` has the separate reflected
center-contact correction and is not included here.

## 2. A source-free comparison to negative M1

Put

    x=1-a, y=1+v, z=1-s,       0<=z<=x<=y,
    r(t)=1-A(1-t),             d=D(x,y),
    D(t,w)=1-R(1-t,-1+w).

For the initial row and d, use the strict CDF; for middle columns use the
closed CDF. A continuous field needs no distinction. Define the first
row-inverse moment

    w_z(q)=z+2 alpha_(1-q)(1-z),
    W_z(d)=integral_0^d w_z(q)dq.                      (2)

In particular, `w_z(q)=z` for initial ranks already above `1-z`. It is
safer to use this first-inverse definition than select an arbitrary point
inside a characteristic plateau. Directly from the strict row,

    W_z(d)=z d+integral_(-(1-z))^(1-z)
                       (R_<(1-z,V)-(1-d))_+dV.       (3)

Let `Cell(s)` denote the reflected pair starting at `+s`, sweeping left
to `-1`, then right to `+1`. Then

    4[CI_(1-z)(1-x,-1+y)-Cell(1-z)]
      =(8-2z)[r(x)-r(z)]
       -{W_z(d)+(x-y-z)d}
       -integral_x^y D(x,w)dw
       -(8-z-y)[r(x)-D(z,y)]_+
       -integral_z^x[r(x)-D(t,y)]_+dt.                (4)

All low-rank alpha and beta contributions have canceled. To derive (4),
split the initially lower ranks at L. Their first-inverse sum is
`N(s)-W_z(d)+zd`, while the initial inward contribution is
`-integral_x^yD+(y-x)d`. Subtract the negative-M1 identity at s; its
remaining initial mass is `(8-2z)r(z)`. This gives (4).

At `z=x`, the route is direct negative M1, so (4) is identically zero.
Indeed, row integration by parts gives

    W_x(D(x,y))=y D(x,y)-integral_x^yD(x,w)dw.

At `z=0`, (4) recovers the fixed-second-turn obstacle relative to its
endpoint negative-M1 value. Thus, wherever negative M1 is active, every
free second turn is one member of an exact one-parameter family of field
obstacles. If `Cell(1-z)` has positive slack above the proposed value, that
slack must be retained; requiring `CI>=Cell` would be unnecessarily strong.

The derivative with respect to d of the inverse term is

    w_z(d)+x-y-z
       =2 alpha_(1-d)(1-z)-a-v>=s-a=x-z.              (5)

Unlike the fixed-`U=1` inverse, this lower bound degenerates when `s=a`.
That endpoint is the redundant M1 comparison. A uniform contraction for
all free turns cannot simply reuse the fixed-turn square-root denominator
without separating this degeneracy and its inactive responses.

### A first-inverse support gate

The exact comparison also controls earlier turns for which the useful
future-row condition `A(s)>=R(1,v)` fails. It does not presume an ordinary
incoming cap. On the branch `B>A`, put

    W=8-z-y,
    Afirst=W_z(d)-z d=2 integral_0^d alpha_(1-q)(1-z)dq.

Monotonicity of the first row and the elementary hinge bound give

    integral_x^y D(x,w)dw <= (y-x)d,
    integral_z^x[r(x)-D(t,y)]_+dt <= (x-z)r(x).

Substituting these two upper bounds into (4), and retaining the favorable
initial-mass term, proves the exact inequality

    4[CI_(1-z)-Cell(1-z)]
      >= W[D(z,y)-r(z)]-(y-z)r(z)+(y-x)r(x)-Afirst.   (5a)

Consequently any inward response no more expensive than `Cell(1-z)`
must satisfy

    W[D(z,y)-r(z)]
      <= Afirst+(y-z)r(z)-(y-x)r(x).                  (5b)

This is also necessary for an active inward response in a proposed lower
certificate, even if that particular negative-M1 response has slack.
It uses the strict first-row inverse and closed middle-turn CDF, so it
does not replace a first contact by a later point on a coincident leg.

For example, if all ranks in the displayed first-inverse moment reach
`U=1-z` by time `C y`, then `Afirst<=2 C y d`. Under `d=O(sqrt(y))`
and `z=O(y^2)`, (5b) forces

    D(z,y)-r(z)=O(y^(3/2)).

Thus a genuinely earlier active second turn must already capture almost
all ranks initially below `1-z`, or its first-inverse moment must be
larger than that initial-arc estimate. A typical incoming row with
`D(z,y)` of order `sqrt(y)` and `r(z)` only of order `y` fails this gate
by an entire order. These are conditional scale consequences of (5b),
not a claim that every unrestricted law has those scales.

## 3. Second-turn stationarity and support compression

At a smooth point define

    Z(s)=R(s,s),
    J_L(s,v)=integral_v^s 1_(R(s,w)<L) R_U(s,w)dw.

Differentiating (1) gives

    4 partial_s CI
      =4+L+min(L,Z(s))-2M+J_L(s,v)-H'(s)
                    -(s+6-v)partial_s M.             (6)

For `s>1`, `Z=H=0` under the endpoint hypothesis, recovering the earlier
post-one formula. For `s<1`, dropping the center and H terms would change
the stationary surface.

On the nondegenerate active branch `B>A`, write

    E(s,v)=(s+6-v)R_U(s,v)+2R(s,v)+H'(s)-4,
    K_(s,v)(L)=L+min(L,Z(s))+J_L(s,v).

Stationarity is

    E(s,v)=K_(s,v)(R(a,v)).                            (7)

Transport makes J nondecreasing in L. The explicit first term makes K
**strictly increasing**, even if the other terms have flat pieces.
Therefore, on a region where `R_U(a,v)>0`, at most one initial start a
can satisfy (7) for a fixed pair `(v,s)`. A smooth active inward law there
cannot have positive density on an open three-dimensional `(a,v,s)` box.
Its natural nondegenerate support is a surface `a=a(v,s)`, or equivalently
`s=S(a,v)`. Plateaus in the initial CDF and nonsmooth first-contact faces
are expressly outside this injectivity conclusion.

At a strict local second-turn minimum, `CI_ss>0`. Differentiating (6) in a
while keeping v,s fixed gives

    CI_sa=R_U(a,v) K'_(s,v)(L)/4>0,

so the implicit surface has the orientation

    S_a=-CI_sa/CI_ss<0.                               (8)

An initial-start-independent ridge is therefore not the generic smooth
minimum surface. This is consistent with the independently checked upper
junction issue for a graph depending only on v.

If the minimized response envelope is constant on an open `(a,v)` patch,
its tangent second derivatives vanish. The resulting Hessian identities
are

    Caa Css=Cas^2,
    Cav Css=Cas Csv,
    Cvv Css=Cvs^2.                                    (9)

Thus its full Hessian has rank one in the normal direction to the active
surface, under the stated strict-minimum and smoothness assumptions.

### The necessary curvature sign

Let `W=s+6-v`, and keep a,v (hence L) fixed when differentiating in s.
A local minimum requires

    W R_UU(s,v)+3R_U(s,v)+H''(s)
       <=partial_s[min(L,Z(s))+J_L(s,v)].              (10)

In the outgoing-gap subcase where `Z=H=0` and all high ranks below L have
already completed their incoming phase, `J_L=Omega'(1-s)`. If that low
source is convex, the right side is nonpositive. An ordinary incoming
density increasing toward U=1 then produces local maxima, not minima.
This argument is conditional on the stated separation; it is not a sign
claim for every curved incoming field.

## 4. A rounded incoming saturation with legal transport

There is a concrete analytic way to supply the needed negative R_UU near
an outgoing edge. Let e(y) and I(x) be increasing, and fix `0<epsilon<1`.
For q>=0 define

    f_epsilon(q)=1,                         q<=1-epsilon,
                 1+(q-1+epsilon)^2/(4epsilon),
                                            |q-1|<=epsilon,
                 q,                         q>=1+epsilon.

Use the homogeneous rounded maximum

    M(x,y)=e(y) f_epsilon(I(x)/e(y)).                  (11)

It keeps an exact outgoing region `M=e` and an exact incoming region
`M=I`, but replaces their sharp corner by a C1 curved phase. On its middle
piece,

    M_I=(q-1+epsilon)/(2epsilon)>=0,
    M_e=[(1+epsilon)^2-q^2]/(4epsilon)>=0.             (12)

Thus (11) satisfies both transport inequalities. It can be combined with
an uncapped initial field Z as

    D=max(e,min(Z,M)),                                (13)

without losing transport when Z is itself legal. This is an analytic
candidate phase, not a claim that an arbitrary Z satisfies the game
inequalities after this operation.

For a linear outgoing trace `e=e0 y`, its exact area is

    integral_0^infinity [M(x,y)-e0 y]dy
       ={I(x)^2/e0} {atanh(epsilon)/(2epsilon)}.       (14)

To check it directly, put `u=e/I`. The incoming part contributes
`integral_0^(1/(1+epsilon))(1-u)du`; the transition contributes

    integral_(1/(1+epsilon))^(1/(1-epsilon))
             [1-(1-epsilon)u]^2/(4epsilon u)du.

The nonlogarithmic terms cancel, leaving (14).

If the leading positive moments give `r(x)~4e0 sqrt(x)` and the leading
negative-M1 row area is `8r(x)`, (14) gives

    I(x)~C_epsilon x^(1/4),
    C_epsilon=8e0 sqrt(epsilon/atanh(epsilon)).         (15)

The corresponding incoming characteristic defect for initial deficit xi
is

    h(xi)~[atanh(epsilon)/epsilon]^2 xi^2/16.          (16)

The square-root and squared scales survive, but their incoming coefficient
changes. At `epsilon=1/2` it is approximately `0.0754343`, rather than
`1/16`. These are leading balances with a fixed epsilon; low-source and
initial-arc corrections remain to be solved.

The outgoing edge is

    x_-(y)=[(1-epsilon)e0/C_epsilon]^4 y^4.            (17)

At a rounded-front free-turn minimum, under the same separation as in
the last paragraph of Section 3, (6) becomes the exact equation

    (8-y-x) M_x(x,y)
       =3-D_initial(a_deficit,y)+2M(x,y)+Omega'(x).    (18)

Here `a_deficit=1-a` is held fixed and x in (18) is the second-turn
deficit. Near (17),

    M_xx=I'^2/(2epsilon e)+f'_epsilon I'',

and the positive first term dominates when I has the scale (15). Hence
`R_UU=-M_xx<0`, supplying the local-minimum sign absent from an ordinary
incoming corner. With bounded low-source derivative, the optimal turn's
offset from (17) is `O(y^7)`. This is distinct from its variation over
initial starts: if the initial field has `D_initial,x=O(1)`, then
`S_a=O(y^7)`, and an `O(y)` interval of starts spans only `O(y^8)` in
second-turn coordinate. Those scales describe a thin but nonzero surface;
they must not be replaced by a start-independent graph.

## 5. Verification and remaining gates

Run

```sh
python -B packages/interval_turn_sheet/verify_free_second_inward_field.py
python -B packages/interval_turn_sheet/verify_free_inward_support_gate.py
```

The audit passes **1,036 exact Fraction checks**, including 480 comparisons
of (4) with independent physical first-capture integration, 96 direct-M1
endpoints of the turn interval, 220 initial-atom starts, and 120 strict
initial-turn trace witnesses. Formula (3) is used for the row moment, so
the test does not silently identify a first inverse with the end of a
coincidence interval.

The separate support-gate audit passes **282 exact Fraction checks**:
129 comparisons with direct physical capture costs, 92 strict response
exclusions, 35 necessary-support instances, 14 strict first-turn traces,
and 12 checks at turns where `A(s)>=R(1,v)` actually fails. These counts
include overlapping properties of the fixtures. The added two-path law
specifically tests that the gate does not depend on the future-row
condition.

The active support and rounded saturation still need joint construction:
the full free-turn inequality, initial and outgoing attachment, scalar or
field row moments, the upper law's nonnegative surface measure, and the
unrestricted monster/princess certificates are not supplied by these
identities alone. In particular, a local stationary surface is not yet a
globally minimizing second-turn rule.
