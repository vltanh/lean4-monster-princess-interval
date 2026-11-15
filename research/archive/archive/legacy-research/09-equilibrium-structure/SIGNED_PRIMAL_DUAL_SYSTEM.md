# A conditional primal-dual boundary system for signed M1/M2 support

## 1. Purpose and hypotheses that are not yet proved

The exact signed functional identifies a concrete system to solve, rather
than another parameter grid. The system below combines both sides of
complementary slackness. Upper-response stationarity alone leaves an
undetermined density function; monster indifference under the proposed
lower law supplies additional transport equations.

This is a conditional candidate system. Its branch assumptions are guided
by `packages/interval_signed_densities/discovery.json`, not established as
a support theorem. In particular, that discovery optimized under three
monotonicity constraints. Its linear-program dual is not automatically a
princess law for the unrestricted game.

The explicit rationalization of that discovery is now ruled out by
[`LOCAL_SCALAR_GAP.md`](LOCAL_SCALAR_GAP.md): a rational mixture using a
shifted negative-M2 characteristic has a strictly smaller response
ceiling against arbitrary princess paths. The equations below remain
useful as conditional branch and transport identities. They are not a
proposal to complete that excluded candidate by choosing a different
lower mixture, and they do not exclude every signed-M1/M2 law.

Use w0,f,g,h,ell,F,G,H,L,k,K0 as in `SIGNED_M1_FUNCTIONAL.md`. A proposed
nonendpoint lower branch has

    u=a,    c=c(a)>=0,    y=y(a)>=c(a),

with c and y nonincreasing in the increasing initial position a. Give
these paths an initial radial CDF A(a), density rho(a)=A'(a). Permit an
additional endpoint-start component at a=1. For its negative-c branch
assume y=c, and write

    E(z)=Pr(endpoint-start component has c<-z).

These are unconditioned masses. Thus A(1-) plus the total endpoint-start
mass is one, and E is nonincreasing. E(1-) need not be zero: it may
include a stationary endpoint component with limiting c=-1.

The formulas describe the controlled one-sided payoff limits used in the
four-parameter response theorem. In particular c,y approaching one retain
the limits B(1)=2 and B(3)=4, rather than substituting an exact central
plateau. They are not a uniform lower-limit theorem against all monsters.
Within an interior parameter interval, assume no initial-position atom;
endpoint atoms and branch-end atoms need separate boundary conditions.

## 2. Upper stationarity on the diagonal u=a

Put r=min(a,c), q=max(a,c). Along an active initial-inward branch the
tangent derivative in a is K_a+K_u. Hence

    0=(a-2-y)f(a)-(1+c)g(a)
       +(4-a-r)h(a)+(6+a-r)ell(a)
       +F(a)+G(a)+K0(r).                               (P1)

For a free c<y, the c equation is

    (8-c-q)h(c)+(1-q)ell(c)
      =w0+Gbar(a)+K0bar(q).                             (P2)

For a free positive y,

    (1+y)ell(y)=Fbar(a).                                (P3)

When c=y, replace (P2) by the tangent condition

    (8-c-q)h(c)+(2+c-q)ell(c)
      =w0+Fbar(a)+Gbar(a)+K0bar(q),                     (P2b)

and require the one-sided suffix condition

    Fbar(a)<=(1+c)ell(c).                               (P3b)

At c=y=1 the c condition is a boundary inequality instead. At u=a the
remaining prefix condition is K_u<=0, because increasing u is feasible.
These inequalities cannot be replaced by extra stationarity equations.

Endpoint-start negative-c indifference, when active on an interval, gives

    (1-z)f(z)+(7+z)g(z)=w0.                             (P4)

The positive endpoint-start relation is

    (7-z)h(z)+(1+z)ell(z)=w0,                           (P5)

but only where those positive-c endpoint responses are active. In the
numerical terminal region h=0 and ell is large, (P5) is slack. It must
not be imposed there merely because h and ell are unknown densities.

## 3. The dual initial-density and endpoint-tail equations

Let C_f(z), C_g(z) be the lower law's payoffs against the reflected
positive-parameter M1(z), M2(z) pairs. On the stated branches, direct
first-inverse integration gives

    4 C_f(z)
      =2(3-z)
       + integral_(a<z) (2-z+y(a)) dA(a)
       + integral_(z<a<1) (a-z) dA(a)
       +(1-z) Pr(endpoint start)+(1-z)E(z),

    4 C_g(z)
      = integral_(a<z) (5+c(a)) dA(a)
       + integral_(z<a<1) (4+a-z) dA(a)
       +(5-z) Pr(endpoint start)+(7+z)E(z).             (D0)

The additional E terms distinguish endpoint paths that turn outward
before crossing the negative B threshold. Their M1 capture is at 1-z,
whereas their M2 capture is at four.

Where f(z)>0 and g(z)>0 in a matching saddle, both C_f and C_g must be
constant. Differentiating (D0) gives

    (2-z+y(z))rho(z)=3+E(z)-(1-z)E'(z),
    (1+c(z))rho(z)=1-A(z)-E(z)-(7+z)E'(z).              (D1)

Define

    D(z)=(7+z)(2-z+y(z))-(1-z)(1+c(z)).

For 0<z<1 and 0<=c<=y<=1 this denominator is positive. The two
equations solve explicitly as the two-state differential system

    A'=[20+4z+(1-z)A+8E]/D,

    E'=[(2-z+y)(1-A-E)-(1+c)(3+E)]/D.                  (D2)

This determines the lower initial density and negative endpoint-tail
density once the active branch maps are supplied. In particular A'>0
on every such interval. A proposed lower law cannot assign zero mass to
the corresponding initial-position interval while retaining positive f
and g there in a saddle.

Where either f or g vanishes, only its active partner's equality remains;
the other monster payoff must satisfy the global lower inequality. Thus
(D2) is not an equation to extend through support gaps by convention.

## 4. Negative M2 indifference determines the c-front

Let

    C(z)=Pr(c>=z),    alpha(z)=the initial a at the c=z front.

On a smooth nonendpoint front, C(z)=A(alpha(z)). Where C>A, one has
alpha(z)>z. The negative M2 pair's exact cost is

    2 C_h(z)
      =2z A(z)
        + integral_z^alpha(z) [(a+z)/2+2] dA(a)
        +6(1-C(z)).                                    (D3)

Indeed, a<=z is captured on both reflected paths at the center time z;
z<a<=alpha has first-leg capture on one side and capture at time two
on the other; a>alpha has the two late captures at times four and two.

Consequently, on an active h interval with C>A,

    (4-2z)rho(z)
      =3A(z)+C(z)+(alpha(z)+z-8)C'(z).                  (D4)

Equivalently, along a high-initial branch with z=c(a),

    c'(a)
      =(a+c(a)-8)rho(a)
        /[(4-2c(a))rho(c(a))-3A(c(a))-A(a)].             (D5)

This supplies the c-map equation missing from upper-response stationarity.
Its denominator and sign must be checked; a negative c' is required by
the ordered candidate.

If C<A, the front lies below the initial threshold. Directly partitioning
the same capture cases instead gives

    4 C_h'
      =A+3C+(z+c(z)-4)rho+2(z-4)C'.                    (D6)

An active h interval in this second region requires the right side to
vanish. The two formulas agree at a regular front-crossing point C=A.

## 5. Negative M1 indifference supplies the y-front equation

Put Y(z)=Pr(y>=z), so C(z)<=Y(z). On a smooth c front, the initial
coordinate is alpha(z)=A^{-1}(C(z)). The unreflected negative-M1 capture
B(z) has three cases:

* c>=z: it is z when a<=z, and (a+z)/2 when a>z;
* c<z<=y: it is (1+z)/2, on the post-U=1 inward segment;
* y<z: it is 1+z, at the endpoint.

The reflected capture is z or (z+c)/2 when a<z, according as c>=z or
c<z, and is 3+z when a>z. Differentiating these exact capture integrals
gives

    4 C_ell'
      =4+A-Y-6rho+(alpha-1)C'-(1+z)Y'       if C>A,    (D7)

    4 C_ell'
      =4-A+2C-Y-(6+z-c(z))rho
        +(z-1)C'-(1+z)Y'                  if C<A.       (D8)

Where ell>0, the relevant right side must vanish. Together with the
active h equation, this determines both outgoing-front derivatives C'
and Y'. The maps c,y are recovered through the ordered identities

    C(c(a))=A(a),    Y(y(a))=A(a),                      (D9)

on strictly monotone nonendpoint pieces. On an endpoint-start component
these identities are replaced by its explicit endpoint parameter
distribution. Flat maps require their atomic front conditions instead
of dividing by a zero derivative.

As an independent check, the exact continuous-rank engine was applied
to the simple law a(q)=q, c(q)=y(q)=1-q. It agrees with all four dual
payoff derivatives on both sides of C=A, using rational arithmetic.
This validates those capture-regime formulas on a nontrivial center-
waiting example; it does not prove a candidate solves the system.

## 6. A concrete free boundary and its coupled density jump

The discovery suggests a possible terminal region

    h=0, ell=d>0 on [b,1].

Suppose a lower initial branch just below b has u=a and c=y=Gamma(a)
with Gamma(a)>=max(a,b). Since K0bar(Gamma)=d(1-Gamma), equation
(P2b) simplifies to

    Gamma(a)=[w0+Fbar(a)+Gbar(a)]/d-1.                 (B1)

The preceding central-wait branch has Gamma=1. Its departure point a0
and the proposed triple point a=c=y=b therefore satisfy

    w0+Fbar(a0)+Gbar(a0)=2d,
    w0+Fbar(b)+Gbar(b)=d(1+b).                          (B2)

In particular, integral_a0^b(f+g)=d(1-b). A branch immediately above b
may have c<a and y=b pinned to a jump of W(y)=(1+y)ell(y). Its suffix
condition is the pair of one-sided inequalities

    (1+b)ell(b-) <= Fbar(a) <= (1+b)d.                 (B3)

The pinned branch can leave the interface when its first inequality
becomes equality. If it then has a free y<b, equation (P3) applies.

Assume both one-sided branches satisfy diagonal a-stationarity at the
triple point, and assume the negative endpoint relation (P4) is active
on both sides. The continuous cumulative integrals cancel in the jump
conditions, giving

    Delta f
      =(b+7)[(4-2b)Delta h+6 Delta ell]/(b^2+2b+13),
    Delta g=-(1-b)Delta f/(7+b).                         (B4)

This is the jump rule appropriate to c=y=a=b. It does not assume that
the central-wait relation or the positive endpoint relation continues
through the terminal interface. Those would be different active sets.

For an interior c branch on the right, taking its c equation to b from
below supplies the additional trace condition

    (8-2b)h(b-)+(1-b)ell(b-)
      =w0+Gbar(b)+(1-b)d.                               (B5)

The proposed constants b,d,a0, support endpoints, initial CDF masses,
and endpoint-tail masses must be fixed by these matching equations,
normalization, common payoff values, and the inequalities at every
inactive branch. None of them is determined by the sampled decimal.

## 7. A different conditional jump must not be confused with (B4)

If both endpoint equations (P4)-(P5) and the central-wait diagonal
continue on one common parameter interval, eliminating g,h gives

    f'=A0(a)f+B0(a)w0+E0(a)ell+D0(a)ell',

where, with Z=19-2a-a^2,

    A0=(a+3)(3a+25)/[(a+7)Z],
    B0=2(147-84a-11a^2)/[(7-a)^2(a+7)Z],
    E0=8(a+3)(a+7)/[(7-a)^2 Z],
    D0=2(a+7)(a^2-4a+19)/[(7-a)Z].                     (B6)

Its jump relation would be Delta f=D0 Delta ell. This follows under
that active-set hypothesis, but the current numerical terminal branch
does not satisfy it. In particular, imposing (P5) where h=0 and
(1+a)ell>w0 would manufacture an inconsistent candidate.

## 8. What makes this a boundary system, and what is still missing

The equations above specify a finite collection of branch regimes,
primal density equations, dual density/front equations, and interface
conditions. They also specify which equality is replaced by which
inequality at c=y, u=a, c=1, a=1, and at density support gaps.

They are not yet a solved ordinary finite-state shooting problem:
(D9) couples inverse fronts evaluated on different parameter intervals.
To obtain such a shooting formulation, one must select a consistent
finite branch ordering, parameterize the simultaneously moving fronts,
and verify their range matches at every interface. Treating ell or the
jump location as an arbitrary fitted function would leave the original
equilibrium problem unresolved. Equations (D7)-(D9), not another upper
stationarity identity, supply the missing dual restrictions.

There is also an immediate unrestricted support check. The common-M2
shift identity in `SIGNED_M1_SUFFIX_REDUCTION.md` improves every controlled
extremal response with c<y and c>=0 by an amount proportional to its
extra-leg length when w0>0. The dual system forces A'>0 on intervals
where both f,g are positive. Thus a canonical lower mixture cannot
simultaneously fill such an interval with a positive-length extra-leg
branch and satisfy a matching unrestricted certificate. A proposed
solution must change its monster support, use a no-extra branch, or
justify different lower paths in a genuine equality corridor.

For the fixed rational discovery law this support objection has been
upgraded to an arbitrary-path exclusion. Section 6 of
[`NEGATIVE_M2_SHIFT.md`](NEGATIVE_M2_SHIFT.md) combines a trace cap, a
quantitative suffix comparison, and an initial-mass estimate. The exact
local scalar gap in `LOCAL_SCALAR_GAP.md` verifies its hypotheses and
supplies a concrete improving four-law mixture. No choice of lower
paths, including paths in equality corridors, can make that particular
monster law optimal. The broader signed-M1/M2 class remains open unless
the same hypotheses or another exclusion argument are verified.

The no-extra contact alternative is y=c with

    Fbar(a)=(1+c(a))ell(c(a)).                           (B7)

It avoids that particular shift loss while retaining an equation for
the suffix price. Whether this alternative survives every monster is
an independent question; the initial-inward restriction u=a itself
has not been justified for a full-game lower equilibrium.

Finally, any candidate must pass the global four-parameter upper
inequality and the unrestricted lower-response verification, including
the free-turn identities and the multi-turn witnesses. The present
system provides explicit equations and falsifiable support conditions;
it is not a claim that those final inequalities have been closed.
