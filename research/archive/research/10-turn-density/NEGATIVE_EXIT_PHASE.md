# A continuous negative-exit phase and its coupled boundary equations

This is a constructive replacement for an ordinary negative-outgoing
branch that was supposed to jump directly to a positive final exit.
The positive-start late sheet can be solved row by row, including flux
from the other post-incoming field. What remains is a boundary-value
problem coupling those rows to the initial and first-outgoing quantiles
and the upper densities. No globally matched law is claimed here.

## 1. Why a finite final-exit jump is not a smooth interface

For high initial a, above all M2 start supports, take c<0. First suppose
the positive early start band is disjoint from `[-c,a]`. With `p=f+g`,

    4 K_u = integral_(-c)^a p(x)dx-(a+c)k(u),
    4 K_au = p(a)-k(u).                                  (1)

The maximizing u values form an interval. On an interior plateau their
common k value is the average of p on `[-c,a]`, hence is at most p(a).
Suppose an ordinary branch with y=c and an extra branch with y>c have
common limiting a,c. Ordering of the lower paths requires
`u_extra<=u_ordinary`. If the upper densities are continuous there,

    4[K_a(extra)-K_a(ordinary)]
      =-(y-c)f(a)
          +(u_extra-u_ordinary)[p(a)-k_plateau] < 0.       (2)

Thus both cannot be active with free interior a when f(a)>0. Strict
increase of k is not needed. With a positive early equality band, its
contribution is removed from the integral in (1); the remaining average
is still at most p(a), so the same argument applies when a lies above
that band. An initial or first-outgoing gap, an upper-density jump, or
an intermediate phase with y tending to c is a different interface and
is not excluded by (2).

The continuous intermediate phase has

    c=-x(z),   y=-z,   0<z<=x(z)<a(z)<u(z)<1.             (3)

Here z parameterizes the final negative outgoing characteristic. Its
rank is `q(z)=1-d(z)`, where d is the mass with final outgoing coordinate
less than -z. The first-outgoing deficit is
`E(x)=Pr(first c<-x)`. Exact quantile matching is

    E(x(z))=d(z),     A(a(z))=1-d(z).                    (4)

The ordered direction has `d'<=0`, `a'>=0`, and `x'>=0`. A constant
cap d across a whole start interval is not imposed.

## 2. Solve the entire positive late row, including its source

Fix a monster start z. Write

    J(s,z)=integral_(-z)^s 1_{R(s,V)<A(z)} R_U(s,V)dV,
    W=6+s+z,  L0=7+z,  T=A(z)+2+2d(z),  L=T/2,
    TJ(s,z)=integral_1^s (6+r+z)J(r,z)dr.                (5)

All traces here are the continuous interior traces. The source J is
nonnegative and is computed from the **same** lower field; it cannot
be prescribed independently of that field. It involves ranks below
A(z), whereas the negative-row sheet has ranks at least `1-E(z)>=A(z)`.

Positive-turn indifference gives the exact equation

    W B_s+2B=4+A(z)+J(s,z),     B(s,z)=R(s,-z).

Anchoring at `B(1,z)=1-E(z)` yields

    B(s,z)=2+A(z)/2
      -[(1+A(z)/2+E(z))L0^2-TJ(s,z)]/W^2.              (6)

Suppose it reaches its cap `1-d(z)` at s=v(z), then stays at that cap
until the endpoint turn `s*=2-z`. The endpoint contact is the closed
jump to one. Its four-cost gain is exactly 8d. Beyond the cap the
four-cost derivative is `T+J(s,z)`. Hence endpoint/line indifference is

    T(2-z-v)+integral_v^(2-z) J(r,z)dr=8d.              (7)

The left side is strictly decreasing in v, with derivative
`-T-J(v,z)<0`. A legal exit exists uniquely precisely when

    T(1-z)+integral_1^(2-z) J(r,z)dr>=8d.               (8)

Once v is found, there is no further row shooting parameter:

    E=d+L[((6+v+z)/L0)^2-1]+TJ(v,z)/L0^2.             (9)

Require `d<=E<=1-A`. The whole row (6), its cap, and its endpoint
comparison are then explicit. This solves its turn comparison, not its
start comparison or transport between different rows.

For an independent derivation, set D=1+A/2+E and Wv=6+v+z. Direct
integration gives the negative-row flux moment

    Qneg=2L Wv-2D L0+8(D-L)+integral_1^v J(r,z)dr.

Substitution in

    4(Cf-Cg)=(1-z)(A+2)-(6+2z)E+integral_1^(2-z)J-Qneg

gives (7). The executable construction is
`packages/interval_turn_density/negative_exit_phase.py`. Its independent
rational verifier checks **4,400 identities** over 400 rows, including
300 with nonzero affine source J. It verifies the row construction and
endpoint comparison; it does not manufacture a globally consistent J.

### Source-free special case

If all relevant post-incoming ranks lie above A(z), J is zero. Then

    S=(1-z)(A+2+d)/(7+z),
    E=S+(S-d)^2/[4(1+A/2+d)],
    v=2-z-8d/(A+2+2d).                                (10)

For variable d, the upper-edge transport condition reduces to

    d(A'+d') <= (A+2+2d)^2/8.                           (11)

The interior cone still requires `B_z>=0` and `B_s>=0` throughout the
sheet. In the general-source case these are tested directly from (6),
including the derivative of J; they cannot be replaced by (11).

## 3. Upper stationarity along the same ranked phase

Let `Fbar,Gbar,Lbar` be the tail primitives of f,g,ell. Assume all initial
positions a(z) in this phase lie above the monster start bands, so
`k=ell` on `[a,1]`, and the initial-dependent late alpha source vanishes.
For now suppose the first negative prefix is the ordinary constant u.
Let Hplus be the positive late-sheet marginal, and retain g as the total
positive M2 marginal. The four free stationarity equations are

    integral_x^a p(r)dr = (a-x)ell(u),                   (12)

    w0+Gbar(a)+Lbar(u)
       =(1-u)p(x)+(7+x)[g(x)-Hplus(x)],                 (13)

    (6+2a)ell(a)-integral_a^u ell(r)dr
       =(2-z-u)f(a)+(1+a-x-u)g(a),                     (14)

    F(2-v(z))-F(a)=[2-z-v(z)]f(z).                     (15)

Equation (15) is the final-exit condition; it is linear in f for supplied
a,v. Its capacity condition is `a<=2-v(z)`. The positive late density is

    jL(z,s)=[f(2-v(z))-f(z)]/[v(z)+6+z]
                    +integral_s^v(z) f'(2-r)/(r+6+z)dr.

For fixed fronts all four equations are linear in the upper densities
and w0. Their common payoff is constant along a smooth phase satisfying
them. A separate equality anchors that constant to the other phases.

### When the positive early sheet meets the negative prefix

It is incorrect to retain (12)-(13) unchanged across that start band.
Define the two linear corrections from the actual positive early density:

    CU(a,u,x)=integral_x^a [ (u+6+r)jE(r,u)
                                  -integral_(s<u) jE(r,s)ds ]dr,

    DE(x,u)=(8+x-u)integral_(s<u)jE(x,s)ds
                           +2integral_(s>=u)(1-s)jE(x,s)ds.

Use zero density off its legal support. Then replace (12) by

    integral_x^a p-(a-x)ell(u)+CU=0,                    (16)

and add DE to the left-minus-right residual of (13). For the rectangular
flat corridor with u>sP, (16) is just the integral of `p-ell(u)` over
the negative prefix **outside** the positive early start band. Within
that band the correction cancels the old incoming price exactly.

The actual lower incoming contour may curve in the equality corridor.
Its inverse at a particular first-outgoing threshold is then not
automatically the scalar u of a canonical representative. The contour
must agree with u outside the corridor and remain in the permitted
flat region inside it. The lower start equations below use its actual
first inverses. On a flat early band, the corrected c residual is
independent of the chosen inverse inside the corridor, as required.

## 4. Lower start equations and cross-phase sources

Let `u_low(z),c_low(z)` be the incoming and first-outgoing characteristics
of the rank whose initial position is z. Let `uT(z)` be the actual
incoming first inverse at the first-outgoing threshold -z. On a regular
positive-line active interval,

    [1+z+c_low(z)-u_low(z)] A'(z)
       +(8+z-uT(z))E'(z)=1-A(z)-E(z).                 (17)

These functions come from the same prefix field, including either early
corridor. They are shared unknowns of the joint system, not values to
borrow from an obsolete ordinary-wave continuation. One absolute Cg
value anchors (17); (7) then anchors Cf at the same value.

The high initial coordinates a(z) must also satisfy the active positive
M1/M2 comparison. If their negative rows lie beyond the positive late
start support, it is

    (1-a)[A(a)+2]-(6+2a)E(a)+Qlow(a)=0,                (18)

where Qlow is the integral of the actual lower-rank post-incoming flux
on both signs of V. If such a row still has post-negative flux, retain
the additional `-Qneg(a)` term. The high-start analogue of (17), together
with `A(a(z))=1-d(z)`, determines its initial density. Negative M1
activity must also be imposed using the actual prefix first inverses;
the curved-prefix Omega term cannot be omitted or counted twice.

This is why a local fit of (12)-(15) alone is insufficient: (4),
(17)-(18), the negative-M1 response, and the common absolute value
must hold for one field. Conversely, (6)-(9) remove the two-dimensional
post-negative row as an independent fitting object once these shared
fronts and source moments are supplied.

## 5. Interfaces, selection, and feasibility

At a smooth ordinary-to-extra onset, use a free threshold beta and
terminal rank mass dT, not the old numerical values. The conditions are

    z=x=beta,  a=aT,  u=uT,  d=E(beta)=dT,  v(beta)=1,
    Fbar(aT)=(1-beta)f(beta).                            (19)

The second line is Ky=0. The ordinary tangential c equation then
becomes the free-extra c equation, and (14) agrees continuously because
y tends to c. The lower zero-width condition is

    (1-beta)[A(beta)+2]-(6+2beta)dT+Qlow(beta)=0.        (20)

If the ordinary first-outgoing threshold remains above all positive
early starts, its analytic singular history and linear tail adjoint may
be attached here. Otherwise their incoming/c equations need the early
corrections (16); no old tail may be inserted merely because u is close
to one.

Continue until an actual active-set boundary is reached: final z=0;
the first cutoff x reaches an early start band; a source rank crosses
A(z); a line residual reaches zero; a cap or cone inequality becomes
an equality; or an upper parameter reaches its legal boundary. The
corresponding new phase must match the rank, characteristic, cumulative
primitive, and payoff traces. A jump in an upper density is allowed only
if its one-sided stationarity conditions and the lower contact traces
are checked; it is not silently smoothed into (19).

For the complete candidate require nonnegative f,g,ell and both signed
sheet densities, nonnegative line residuals, monotone f,p,k, the effective
Gamma condition, `0<=A<=1`, `d<=E<=1-A`, monotone quantiles, and the full
transport cone. Normalize once by `w0+integral(p+k)=1`. Finally verify
the global four-scalar princess envelope and the unrestricted monster
response. Neither a finite route pool nor the local source-resolved
cap supplies that last verification.

The selection problem is therefore a joint boundary-value/collocation
problem with free interfaces and a linear upper adjoint conditional on
the lower fronts. The source-resolved cap (7)-(9) is a constructive
subproblem with a unique solution. The remaining coupled system has
not yet been solved into a normalized matching law.
