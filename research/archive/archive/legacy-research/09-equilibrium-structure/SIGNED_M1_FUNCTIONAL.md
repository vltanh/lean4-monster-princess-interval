# Exact functional and indifference equations with signed M1 support

## 1. The enlarged law

Use the symmetric monster law from `SIGNED_M1_SUFFIX_REDUCTION.md`:

    mu_1 = w0 delta_(-1) + f(x) dx at x>0
                           + ell(z) dz at x=-z<0,
    mu_2 = g(x) dx at x>0 + h(z) dz at x=-z<0.

All four densities are nonnegative on [0,1], and

    w0 + integral_0^1 (f+g+h+ell) = 1.

Write F,G,H,L for their cumulative integrals from zero, use a bar for
the complementary tail, and set

    k=h+ell,    K0=H+L.

The symbol K0 denotes a cumulative density, not a capture payoff.
The global four-parameter response theorem assumes separately that
f, f+g, and k have nondecreasing versions. The integral identities below
do not require those monotonicity hypotheses.

Take an interior princess parameter tuple

    0<=a<=u<1,    -a<=c<=y<1.

Let J(a,u,c) be the original outward-suffix payoff and K(a,u,c,y) the
limiting payoff after the additional inward segment just after U=1.
The precise paths and all boundary conventions are in the suffix note.
As before, the factor four combines reflection probability and the
conversion from characteristic coordinates to time.

## 2. The exact additional negative-M1 contribution

The existing formulas for 4J in `../08-continuum/CANDIDATE_DENSITIES.md`
remain unchanged for w0,f,g,h. Add the following two expressions for ell.

The reflected negative-M1 contribution is

    integral_0^a (6+2z)ell(z) dz
      + integral_a^u (z-a)ell(z) dz
      + 2 integral_u^c z ell(z) dz       [only when c>=u]
      + integral_max(u,c)^1 (z+c)ell(z) dz.              (1)

The unreflected contribution is

    2 integral_0^1 (z+1)ell(z) dz                       if c<0;

    integral_0^min(u,c) (z+u)ell(z) dz
      + 2 integral_u^c z ell(z) dz       [only when c>=u]
      + 2 integral_c^1 (z+1)ell(z) dz                   if c>=0. (2)

These terms follow directly from the M1 first-capture formulas. For
parameter -z, the unreflected capture is B(z). The reflected capture is
A(z) when z>a and B(2+z) when z<a. On the stated path,
B(2+z)=3+z; multiplying by two gives the coefficient 6+2z in (1).
The case z=a is initial capture and has zero density measure.

The additional inward segment has the exact limiting gain

    4(K-J)
      = (y-c)Fbar(a)
        - integral_max(0,-y)^max(0,-c) (1-x)f(x) dx
        - integral_max(0,c)^max(0,y) (1+z)ell(z) dz.     (3)

Every M2 capture is unchanged. The negative-M1 loss in (3) comes from
crossing positive B thresholds: B(z) advances from z+1 to (1+z)/2.
The endpoint atom's B(1) is unchanged because y<1.

## 3. Derivatives on the nonnegative-c branch

Suppose c>=0, and put r=min(u,c), q=max(u,c). At continuity points of
the densities and away from the branch interfaces,

    4 K_a
      = (u-2-y)f(a) + (u-1-a-c)g(a)
        + 4h(a) + (6+2a)ell(a) - K0(u)+K0(a),

    4 K_u
      = F(a)+G(a)+K0(r) - (a+r)k(u),

    4 K_c
      = w0+Gbar(a)+K0bar(q)
        - (8-c-q)h(c) - (1-q)ell(c),

    4 K_y = Fbar(a)-(1+y)ell(y).                        (4)

For comparison, the new contributions to the derivatives of 4J are

    J_a: (6+2a)ell(a)-L(u)+L(a),
    J_u: L(r)-(a+r)ell(u),
    J_c: Lbar(q)-(2+c-q)ell(c).                         (5)

Adding (3) changes the last coefficient in (5) from -(2+c-q) to
-(1-q), and changes the positive-M1 a coefficient from u-2-c to
u-2-y. These changes matter when differentiating an active suffix.

## 4. Negative c and the sign of y

For c<0 the a derivative in (4) is still valid, while

    4 K_u
      = F(a)-F(-c)+G(a)-G(-c) - (a+c)k(u),

    4 K_c
      = w0+Gbar(a)+K0bar(u)
        - (1-u)f(-c) - (8-c-u)g(-c).                    (6)

The y derivative is

    4 K_y = Fbar(a)-(1+y)f(-y)       if y<0,
    4 K_y = Fbar(a)-(1+y)ell(y)      if y>0.             (7)

At y=0, use the appropriate one-sided derivatives. At y=c, maximize
over the one-sided feasible direction y>=c rather than imposing K_y=0.
The values c=0 and c=u likewise require their own one-sided conditions.

The accompanying exact automatic-differentiation check differentiates
the integral formulas independently of (4)-(7), over every smooth sign
and ordering branch. It checks these algebraic identities, not global
optimality of a proposed strategy.

## 5. Endpoint-start and central-wait branches

### Endpoint start

When a and u tend to one, Fbar(a) tends to zero. The optimal suffix is
y=c unless the intervening M1 threshold measure vanishes. Thus one must
differentiate tangent to y=c. For a positive interior c, the equation is

    (7-c)h(c)+(1+c)ell(c)=w0.                            (8)

For a negative transition c=-x, the corresponding equation remains

    (1-x)f(x)+(7+x)g(x)=w0.                             (9)

An additional signed-M1 density changes (8) but not (9). In particular,
using the old relation h(c)=w0/(7-c) simultaneously with a positive ell(c)
on an endpoint-active interval would violate indifference.

### Central wait with a<u

For a central-wait branch c,y tending to one and an interior prefix
a<u<1, the necessary equations are

    (3-u)f(a)+(2+a-u)g(a)
      =4h(a)+(6+2a)ell(a)-K0(u)+K0(a),

    F(a)+G(a)+K0(u)=(a+u)k(u).                          (10)

### Central wait on the diagonal u=a

If u=a is active over an interval and its payoff is constant as a
varies, use K_a+K_u. The equation becomes

    (3-a)f(a)+2g(a)
      =(4-2a)h(a)+6ell(a)+F(a)+G(a)+H(a)+L(a).          (11)

The coefficient of ell in this diagonal equation is six. It is not
obtained by simply replacing h by h+ell in the old equation.

## 6. An interior extra-suffix branch

For an active branch with u=1, c>=0, and c<y<1, the free a,c,y
conditions are

    (1+y)f(a)+(a+c)g(a)
      =4h(a)+(6+2a)ell(a)-K0bar(a),

    (7-c)h(c)=w0+Gbar(a),

    (1+y)ell(y)=Fbar(a).                                (12)

The remaining u condition is a boundary inequality, not an additional
stationarity equation. The middle relation in (12) and the endpoint
relation (8) concern different active constraints. If they held at the
same c with Gbar(a)>0 or ell(c)>0, they would contradict one another.
Their active c regions must therefore be separated, or the candidate
must use a different prefix boundary.

Put W(y)=(1+y)ell(y). If W is differentiable and strictly increasing,
the last equation in (12), or the corresponding equation for any free
positive y, gives

    y'(a)=-f(a)/W'(y(a))<=0.                            (13)

The limiting time-one location is d(a)=1-y(a), so it increases with the
starting position. If a proposed lower mixture gives this branch an
initial radial density rho0(a), its time-one density is therefore

    rho1(d(a))=rho0(a) W'(y(a))/f(a),                    (14)

where f and W' are positive. This connects the monster suffix price
to an ordered lower-law marginal, rather than leaving the time-one
locations as arbitrary free choices.

Equations (8)-(14) are conditional indifference and transport equations.
They still require normalization, branch selection, nonnegativity, the
three monotonicity conditions, and all global response inequalities.
They do not by themselves give an equilibrium or a new game bound.
The rational law suggested by the subsequent fixed-bin discovery is
strictly improvable, as proved in
[`LOCAL_SCALAR_GAP.md`](LOCAL_SCALAR_GAP.md). That candidate exclusion
uses these exact formulas together with arbitrary-path estimates; it
does not settle the entire signed-M1/M2 class or the unrestricted game.
