# Conditional density equations for an M1/M2 candidate

## Scope and outcome

This note records exact payoff and derivative calculations used to investigate
a continuum monster law. They are conditional equations for that family,
not an equilibrium proof. In particular, a sampled princess law obtained
from the restricted equations failed an unrestricted-monster response check.
Matching a collection of M1/M2 payoff curves does not supply the missing
lower guarantee against every monster.

There are two separate corrections to a tempting three-parameter response
ansatz:

1. For a nonnegative transition parameter, an additional inward leg just
   after `U=1` strictly improves the ansatz whenever the relevant M1 tail has
   positive mass.
2. For a negative transition parameter, that additional leg also has a cost.
   It can capture some M1 paths earlier. Its endpoint cannot be selected by
   the positive-parameter formula.

All equations below retain this distinction. The accompanying standard-
library verifier checks the derivative identities using exact rational
automatic differentiation, including both signs of the transition parameter.

## 1. Candidate monster law

Use the M1 and M2 paths defined in `CHARACTERISTIC_RESPONSE.md`. Consider a
symmetric law consisting of:

* mass `w0` on the reflected pair M1(-1);
* pair-density `f(x)` on M1(x), for `0<x<1`;
* pair-density `g(x)` on M2(x), for `0<x<1`;
* pair-density `h(z)` on M2(-z), for `0<z<1`.

The pair mass is divided equally between a path and its reflection. Thus

    w0 + integral_0^1 (f+g+h) = 1.

Write `F,G,H` for the cumulative integrals from zero and use a bar for the
tail, for example `Fbar(a)=F(1)-F(a)`. Here `f,g,h` are parameter densities;
they are not the threshold-tail functions called `f,g` in
`M1_M2_CONTROL.md`.

The formulas require integrable densities. Pointwise derivative statements
hold at continuity points of the densities; stronger smoothness is stated
where it is needed.

## 2. Three parameters and a fourth suffix parameter

Let

    0 <= a <= u < 1,       -a <= c < 1.

The original path starts at `a`, moves right until `U=u`, then moves left
until `V=min(u,c)`. If `c>=u`, it reaches zero and waits there until time c.
It then moves right to the endpoint and stays there. Its reflection is
handled by the symmetric monster law. Away from initial-equality and
turning thresholds, its characteristic inverses are

    A(z)=0                         if z<=a,
         (z-a)/2                   if a<z<=u,
         z                         if u<z<=c and c>=u,
         (z+c)/2                   if max(u,c)<z<=c+2,
         z-1                       if z>c+2;

    B(z)=0                         if z<=-a,
         (z+u)/2                   if -a<z<=min(u,c),
         z                         if u<z<=c and c>=u,
         z+1                       if z>c.

At the last case of B, the preceding cases take priority. These are first
inverse conventions: for example, the value at `z=u` in A is the earlier
value. Atomless integration ignores the finitely many such thresholds.

The formulas at `u=1` or `c=1` below mean one-sided limits from below. In
particular, `B(1)` tends to two as `c` tends to one from below. Substituting
the path that actually waits at zero until time one instead would give
`B(1)=1`; those two operations do not commute. Consequently a limiting
formula by itself is not an admissible princess lower certificate.

Let `J(a,u,c)` be the payoff of the original path. A modified path follows
the same prefix until just after U crosses one, then moves inward on
`U=1+epsilon` until `V=y`, before moving outward again. Here

    c <= y < 1.

Let `K(a,u,c,y)` denote the limit as epsilon decreases to zero. The limit
exists for the law above by bounded convergence away from the finite
thresholds. The case `y=1` is itself a limit from below. There is no claim
that these payoff limits are uniform over all other monster paths.

## 3. Exact payoff formulas

The following formulas give `4J`. The factor four combines the reflection
probability and the factor two in the characteristic-time coordinates.
Put `k=max(0,-c)`.

The endpoint pair contributes

    w0*(5+c).

The positive M1 density contributes

    integral_0^k (8-4x) f(x) dx
      + integral_k^a (u+6-3x) f(x) dx
      + integral_a^1 (8+c-3x) f(x) dx.

The positive M2 density contributes

    12G(k) + integral_k^a (u+4-x) g(x) dx
      + (5+c)*Gbar(a).

For the negative M2 density, the reflected contribution is always

    4H(a) + integral_a^u (z-a) h(z) dz
      + 2 integral_u^c z h(z) dz       [this term only when c>=u]
      + integral_max(u,c)^1 (z+c) h(z) dz.

Its unreflected contribution is

    8H(1)                                        if c<0;

    integral_0^min(u,c) (z+u) h(z) dz
      + 2 integral_u^c z h(z) dz                  [only when c>=u]
      + 8Hbar(c)                                 if c>=0.

For `c<0`, the maximum in the reflected expression is u and the optional
integral is absent.

### Exact effect of an additional inward leg

The modified payoff satisfies

    4(K-J) = (y-c)*Fbar(a)
      - integral_max(0,-y)^max(0,-c) (1-x) f(x) dx.       (1)

Indeed, M1 paths with `x>a` are captured at `A(2-x)` and their capture times
increase by `(y-c)/2`. M1 paths with `-y<x<-c` instead have their capture
times `B(-x)` reduced from `1-x` to `(1-x)/2`. Every other term is unchanged
in the limit. The integration bounds in (1) are therefore essential.

For `c>=0`, the integral vanishes, so `y=1` gives the largest payoff within
this suffix family and

    K(a,u,c,1) = J(a,u,c) + (1-c)*Fbar(a)/4.             (2)

For `c<0`, an interior negative y satisfies the stationarity condition

    Fbar(a) = (1+y) f(-y).                              (3)

Monotonicity of f alone does not justify restricting y to c or one. For
example take `a=99/100`, `c=-99/100`, and f equal to one below 99/100 and
eleven above 99/100. A detour ending at `y=-9/10` gives

    4(K-J)=99/20000 > 0,

whereas the full detour to `y=1` gives

    4(K-J)=-5621/20000 < 0.

Scaling f and adding any remaining probability mass makes this a normalized
law without changing the comparison. This is an obstruction to the proposed
two-choice suffix shortcut, not a claim about an equilibrium density.

## 4. Derivatives for the nonnegative-transition branch

Set `K_+(a,u,c)=K(a,u,c,1)` for `c>=0`, and put

    r=min(u,c),       q=max(u,c).

Differentiating the preceding integrals gives

    4 (K_+)_a = (u-3) f(a) + (u-1-a-c) g(a)
                  + 4h(a) - H(u) + H(a),

    4 (K_+)_u = F(a) + G(a) + H(r) - (a+r) h(u),

    4 (K_+)_c = w0 + Gbar(a) + Hbar(q)
                  - (8-c-q) h(c).                     (4)

The corresponding derivative of J in a has `(u-2-c)f(a)` in place of
`(u-3)f(a)`, and its derivative in c has an additional `Fbar(a)`.

For `c<0`, the derivatives of the original J are

    4J_a = (u-2-c) f(a) + (u-1-a-c) g(a)
              + 4h(a)-H(u)+H(a),

    4J_u = F(a)-F(-c)+G(a)-G(-c)-(a+c)h(u),

    4J_c = w0+Fbar(a)+Gbar(a)+Hbar(u)
              -(2+c-u)f(-c)-(8-c-u)g(-c).              (5)

Equations (1), (4), and (5) cover the extra suffix parameter without
silently changing the negative-c branch.

## 5. Conditional indifference equations

These equations apply only if the indicated paths are active responses to
the same proposed monster law. They are necessary local conditions; they
neither establish global maximality nor produce a princess lower strategy.
The companion `CONDITIONAL_RESPONSE_REDUCTION.md` gives sufficient density
hypotheses under which the full four-parameter family controls every
princess response. Those hypotheses and the full scalar optimization must
still be checked for any particular law.

### Central-wait branch: c tends to one

The equations in the interior `a<u<1` are

    (3-u) f(a)+(2+a-u) g(a)
      = 4h(a)-H(u)+H(a),

    F(a)+G(a)+H(u) = (u+a)h(u).                         (6)

If a whole diagonal segment `u=a` is active and its payoff is constant as a
varies, the tangential condition is instead

    (3-a) f(a)+2g(a)
      = (4-2a)h(a)+F(a)+G(a)+H(a).                    (7)

Equation (7) uses `J_a+J_u`, not `J_a` alone. On a subinterval where f is zero
and h is constant, differentiation yields

    g'=(g-h)/2,

so `g=h+C exp(a/2)` there. This is conditional on the active diagonal and
the density assumptions.

### Endpoint-start branch: a and u tend to one

For a nonnegative active c, (4) gives

    h(c)=w0/(7-c).                                    (8)

For `c=-x<0`, using the original suffix `y=c`, (5) gives

    (1-x)f(x)+(7+x)g(x)=w0.                           (9)

If an interval of the c-parameter is skipped and h is a constant h0 on the
corresponding interval `[r,s]`, equality of the two endpoint payoffs requires

    h0=w0/[7-(r+s)/2].                               (10)

This follows by integrating `4J_c=w0-(7-c)h0`. It is not a reason to assume
such a plateau exists.

### Connecting branch: u tends to one, a remains below one

For an active nonnegative c with the corrected suffix, the two free
derivatives in (4) yield

    (7-c)h(c)=w0+Gbar(a),

    2f(a)+(a+c)g(a)=4h(a)-Hbar(a).                    (11)

The uncorrected three-parameter family would incorrectly retain
`Fbar(a)` in the first equation and `(1+c)f(a)` in the second. Whenever
`Fbar(a)>0` and `c<1`, that uncorrected family omits a strict improvement.

On a smooth branch `c=c(a)`, differentiation of the first equation in (11)
gives

    c'(a) = -g(a) / [(7-c)h'(c)-h(c)]                 (12)

when the denominator is nonzero. An additional boundary optimality condition
is needed for the constrained parameter `u<=1`.

## 6. An audited differential equation on one proposed region

Suppose (7), (8), and (9) all hold on an open interval. Eliminating g and h
and differentiating gives

    f'(a) = A(a) f(a) + B(a) w0,

    A(a) = (a+3)(3a+25) / [(a+7)(19-2a-a^2)],

    B(a) = 2(147-84a-11a^2)
             / [(7-a)^2 (a+7)(19-2a-a^2)].            (13)

One way to check the elimination is to differentiate (7) and (9):

    (3-a)f'+2g' = 2f+g-h+(4-2a)h',

    (1-a)f'+(7+a)g' = f-g.

Substitute `h=w0/(7-a)` and `g=[w0-(1-a)f]/(7+a)` and solve this two-by-two
system. The exact verifier checks these identities at rational arguments.
The homogeneous factor for (13) is

    L(a) = (a+7) / [20-(a+1)^2]^2
      * [(2 sqrt(5)+a+1)/(2 sqrt(5)-a-1)]^(1/sqrt(5)).

Its logarithmic derivative is

    1/(a+7) + 4(a+2)/[20-(a+1)^2] = A(a).

Consequently the local solution can be written by quadrature as

    f(a)=L(a) [C+w0 integral^a B(t)/L(t) dt].

This solves only that conditional region. The endpoints of the region,
other branches, normalization, and all global response inequalities remain
to be supplied; none is fixed by (13) alone.

## 7. What the numerical investigation does and does not establish

A bounded floating-point run at 32 parameter subdivisions optimized a
sampled princess family against a finite M1/M2 monster family, with discrete
monotonicity constraints on f and h. It suggested the branch geometry used
above. The corrected script adds the post-transition inward leg only when
`c>=0`; its output is exploratory and is not a rational upper certificate.

The sampled princess dual is not a lower certificate for the unrestricted
game. A separate monster path outside the sampled family exploits the
concentration of its nonnegative-c paths near the center at time one. This
failure remains after retaining the original suffix for negative c. The
exact response obstruction is recorded separately with its verifier.

Thus the useful output here is the corrected exact functional and the
conditional equations, not a value or a matching saddle point. A solution
would still need a law satisfying the global upper inequalities and an
independently valid lower guarantee against all monster paths.
