# A two-dimensional turn law with a global princess-response reduction

## 1. Result and purpose

An increasing graph of negative-M2 turn characteristics can make optimal
princesses follow one common spacetime arc. That is unsuitable as a lower
strategy unless the common-arc capture issue is resolved. A two-dimensional
turn distribution has a different possibility: its density can make the
princess payoff exactly flat across a whole characteristic corridor.

This note gives an explicit construction and proves its unrestricted
princess-response theorem. It is not merely an Euler equation. Under the
checkable hypotheses below, **every admissible princess path is bounded by a
four-parameter limiting response**, and a continuum of other paths has the
same suffix payoff. The remaining equilibrium problem is to select a
matching lower law and solve its boundary conditions.

The construction retains the following reflected-pair monster components:

* endpoint M1 mass `w0`;
* positive M1 density `f` and positive M2 density `g`, with M2 turn `b=1`;
* negative M1 density `ell`;
* an optional negative M2 density `h0` with turn `b=1`;
* a new negative M2 joint density `h(z,s) dz ds`, with start `-z` and
  turning characteristic `s`.

All pair masses are divided equally between the two reflections. Common
positive scaling of all components does not affect the conditions below;
the law is normalized after construction. The shifted M2 paths are those
of `../09-equilibrium-structure/SHIFTED_CHARACTERISTIC_RESPONSE.md`.

## 2. Explicit construction of the turn sheet

Let `F(x)=integral_0^x f(r) dr`. Initially suppose `f` is nondecreasing,
bounded, and absolutely continuous. Choose a measurable upper boundary

    1 <= v(z) <= 2,             0 <= z <= 1,

and a bounded nonnegative `ell` satisfying, wherever `v(z)>1`,

    f(2-v(z)) >= ell(z).                                      (1)

The nonnegative joint density on `1<s<v(z)` is

    h(z,s)
      = [f(2-v(z))-ell(z)]/[v(z)+6-z]
        + integral_s^v(z) f'(2-r)/(r+6-z) dr.                  (2)

Set it to zero outside that strip. This is a legal M2 law, since
`z<=1<=s<=2<=2+z`. The boundary `v=1` contributes no sheet mass;
condition (1) is unnecessary there.

Define its zeroth and excess-turn moments

    H(z) = integral_1^v(z) h(z,s) ds,
    M(z) = integral_1^v(z) (s-1) h(z,s) ds,

and put

    k(z) = h0(z)+H(z)+ell(z),
    Gamma(z) = F(2-v(z))-ell(z)(z+2-v(z)).                      (3)

The global response theorem assumes

    f, f+g, and k are nondecreasing;
    Gamma is nonincreasing.                                  (4)

A convenient sufficient condition for the last assertion is that both
`v` and `ell` are nondecreasing, in addition to (1). At differentiability
points,

    Gamma'
      = -[f(2-v)-ell]v' - ell - ell'(z+2-v) <= 0.             (5)

Neither `v` nor `ell` has to be monotone if (4) is checked directly.
In particular, `v` can be piecewise constant, and can return to one
outside the sheet support. A downward jump in `v` must be paid for by
the corresponding `ell` jump so that `Gamma` does not increase; the
separate jump of `k` must also have the stated sign. With constant
`v,ell,h0` on a z interval, `Gamma'=-ell` and `k'>=0`, so the remaining
checks are at the interval boundaries.

The construction also works for bounded monotone `f` with jumps. Write
`P(s)=f(2-s)` and replace the integral in (2) by the Stieltjes integral
`integral_(s,v] [-dP(r)]/(r+6-z)`, with consistent one-sided versions.
Jumps of `P` produce jumps in the ordinary joint density `h`, not atoms
of the monster measure in `s`. The identities below hold almost
everywhere and then after integration. Absolute continuity suffices for
the first implementation.

For step densities there is an especially convenient finite formula.
Write `f(x)=f0+sum_i Delta_f_i 1_(x>=x_i)`, where all increments are
nonnegative, and put `r_i=2-x_i`. At fixed `v>1`, write
`W_v=v+6-z`, `W_i=r_i+6-z`, and `p=f(2-v)-ell(z)`. Then

    h(z,s)=p/W_v+sum_(s<r_i<v) Delta_f_i/W_i,

    H(z)=(v-1)p/W_v
           +sum_(r_i<v) Delta_f_i(r_i-1)/W_i,

    M(z)=(v-1)^2 p/(2W_v)
           +sum_(r_i<v) Delta_f_i(r_i-1)^2/(2W_i).            (5a)

Use the right-continuous value of `f(2-v)` and exclude `r_i=v` from
the sums. Equivalently, use the lower one-sided value and include that
jump; both give the same density almost everywhere and the same
moments. Formula (5a) is linear in the density heights and `ell`, so
fixed choices of `v` admit a density linear program.

The corresponding exact primitives in z need only logarithms. On a
bin with fixed `v,ell`, each moment is a sum of terms `C/(A-z)`.
Use

    integral_l^r dz/(A-z) = log((A-l)/(A-r)),
    integral_l^r z dz/(A-z) = A log((A-l)/(A-r))-(r-l).       (5b)

The scalar capture integrands are affine in z after splitting at their
capture-regime boundaries, so (5b) integrates all features analytically.

### Integrable terminal growth is allowed

Boundedness of `f` is a convenient initial presentation, not an essential
restriction. A nondecreasing integrable `f` can diverge at one. Formula
(2) remains locally finite for `s>1` and defines an integrable sheet.
The following derivative-free moment formulas make this explicit. Put
`Lz=7-z`, `P(r)=f(2-r)`. Then

    H(z)=Lz integral_1^v [P(r)-ell(z)]/(r+6-z)^2 dr,

    2M(z)=integral_1^v [P(r)-ell(z)]
                     [1-Lz^2/(r+6-z)^2] dr.                 (5c)

They follow by Stieltjes integration by parts; the lower boundary term
vanishes because integrability and monotonicity imply
`(r-1)f(2-r) -> 0` as `r` decreases to one. Both moments are finite,
and the sheet mass in `1<s<1+epsilon` tends to zero. The cap comparison
pays for alpha changes using total mass, and the suffix proof below uses
integrals of `f`; neither needs its endpoint value to be finite. Thus
the response theorem also covers this extension, with locally absolutely
continuous or Stieltjes versions of (2).

## 3. Exact suffix functional before optimization

By the reflected-pair absolute-value comparison, nonnegative princess
paths suffice. Write

    a=p(0), U=t+p(t), V=t-p(t),
    A(r)=inf{t:U(t)>=r}, B(r)=inf{t:V(t)>=r},
    e=inf{t:U(t)>1}, c=V(e), L=2-a.

As in the signed-density response theorem, `e` is the right endpoint of
the `U=1` plateau, whereas `A` and `B` are first inverses.

The cap argument from `NEGATIVE_M2_SHIFT.md` extends to this law. Lowering
the characteristic graph `V(U)` can only delay each reflected `B(s)`
capture. For an unreflected negative M2, an early capture either moves
later or becomes a late capture; an already late capture remains late.
The only potentially unfavorable changes are the same alpha-threshold
changes as in the old proof. Thresholds at most one cost `O(delta)`, and
the positive-M1 component is controlled by monotonicity of `f`.

Consequently, for an upper supremum we may keep `V<1` until the endpoint
and use

    B(s)=s+1, B(s+2)=s+3       for every s>=1.                 (6)

These are approached by legal capped paths, not imposed on a limiting
path with an early `V=1` plateau. The capture horizon is at most five.

Fix the prefix ending at `(U,V)=(1,c)`. At a suffix beta threshold `z`
let

    phi(z)=U(B(z)),       B(z)=[z+phi(z)]/2.

The inverse graph is nondecreasing and obeys

    1<=phi(z)<=z+2,           c<z<1.                          (7)

For `z>0`, M2 with parameters `(-z,s)` captures early exactly when
`phi(z)<=s`. Its late capture is `s+3`. Equality belongs to the early
branch; it has zero mass in the `s` integral.

Put

    R_a(u)=integral_u^L f(2-r) dr      if 1<=u<L,
           0                         if u>=L.

Relative to the outward suffix, the exact gain multiplied by four is

    integral_c^0 q_a^-(z,phi(z)) dz       [when c<0]
      + integral_max(c,0)^1 q_a^+(z,phi(z)) dz,                (8)

where

    q_a^-(z,u)=R_a(u)-f(-z)(z+2-u),                           (9)

    q_a^+(z,u)
      =R_a(u)-ell(z)(z+2-u)
       -integral_u^v(z) (2s+6-z-u)h(z,s) ds.                 (10)

The last integral is zero for `u>=v(z)`. Formula (8) is an integration
by parts of the positive-M1 alpha contribution, together with the exact
capture gains of the M1 and shifted M2 components. It does not freeze
the shifted-M2 cutoff at one.

## 4. Why the whole corridor has the same payoff

For `u<L` and `1<u<v(z)`, differentiation gives

    partial_u q_a^+
      =-f(2-u)+ell(z)+integral_u^v h(z,s) ds
                         +(u+6-z)h(z,u),                    (11)

    partial_uu q_a^+
      =f'(2-u)+(u+6-z)partial_s h(z,u).                      (12)

The density (2) makes (12) zero. At the upper boundary, (11) is zero
by the first term of (2). Thus throughout the active part of the strip,

    q_a^+(z,u)=Gamma(z)-F(a)       for 1<=u<=v(z), u<L.       (13)

If `u>=L`, both loss terms in (10) are nonnegative and `R_a=0`, so
`q_a^+<=0`. Above the strip, `q_a^+` is convex in `u` until `L`,
and remains bounded by zero thereafter. Therefore, on the entire legal
interval (7),

    q_a^+(z,u) <= max{Gamma(z)-F(a),0}.                       (14)

This is a global pointwise inequality, including exits outside the sheet.
If `Gamma(z)>F(a)`, then (1) and (3) imply `v(z)<L`, so the entire
closed interval `[1,v(z)]` is an equality corridor. The endpoint value
`u=z+2` gives zero, corresponding to remaining at the endpoint when the
threshold is crossed.

Since `Gamma` is nonincreasing, its positive-payoff region is an initial
interval in `z`. For `c>=0`, choose its exit `y>=c`, use any nondecreasing
`phi(z)` in `[1,v(z)]` for `c<z<y`, and then use `phi(z)=z+2` for
`z>y`. The choice `phi=1` is always available as a one-sided limit.
Thus (14) is attained in the upper supremum, and **every positive-c
suffix reduces to one scalar exit y**.

If an interior exit is regular, its equation is

    Gamma(y)=F(a).                                          (15)

The equality corridor is essential: (15) fixes an exit, but it does not
force all ranks onto one common incoming characteristic.

## 5. Negative c does not leave an uncontrolled suffix

For `c<=z<0` and `u<L`, monotonicity of `f` gives

    partial_u q_a^-(z,u)=-f(2-u)+f(-z)<=0,                   (16)

because `-z<=-c<=a<2-u`.

Suppose a suffix receives a strictly positive contribution at some
positive threshold. By (10), its inverse there must be below `L`.
Monotonicity of `phi` then puts every preceding negative threshold below
`L`; (16) bounds its negative-threshold contribution by setting `phi=1`.
Equation (14) bounds all positive contributions by the positive initial
interval of `Gamma-F(a)`, and bounds all other contributions by zero.
This gives the response that jumps across every negative threshold at
`U=1+`, follows the positive corridor, and exits once.

If there is no positive contribution from positive thresholds, those
terms can be discarded for an upper bound. Restrict the graph to `V<=0`
and then use the minimal endpoint continuation. The negative-threshold
functional is exactly the old signed-M1 suffix functional on this
restricted range. The opposite-Chebyshev argument in
`SIGNED_M1_SUFFIX_REDUCTION.md`, Section 3, reduces it to one immediate
jump ending at some `y in [c,0]`.

Taking the larger of these two cases proves the same one-exit reduction
for every `-a<=c<0`. It does not require the negative-threshold pointwise
scores to have a single sign change.

## 6. Prefix reduction and the finite response formula

Fix `a,c`. All shifted M2 paths with `z<=c` have already captured on
their first leg before the suffix. For `z>c`, their capture optimization
is exactly the suffix problem above. The reflected shifted capture is
`A(z)` for `z>a` and the fixed value `s+1` for `z<a`.

The prefix therefore has alpha density `k`, negative-beta density
`f+g`, and positive-beta density `k`. Its additional turn-moment terms
are constant when `a,c` are fixed. The monotone one-switch argument of
the signed response theorem applies unchanged. Its characteristic
vertices are

    (a,-a) -> (u,-a) -> (u,min(u,c)),

then the diagonal to `(c,c)` if `c>=u`, and then the horizontal leg to
`(1,c)`, with `a<=u<=1`.

Let `K_old(a,u,c,y)` denote the signed-M1 limiting scalar functional,
using negative M2 density `h0+H`. The exact new scalar functional is

    4 K_new
      =4 K_old
       +2 integral_0^a M(z) dz
       +2 integral_max(0,y)^1 M(z) dz
       -integral_max(0,c)^max(0,y) (7-z)H(z) dz.              (17)

For example, on `c<z<y`, the sheet's first capture changes from the
old value four to `(1+z)/2`; for `z>y`, its late value changes from four
to `s+3`. Its reflected late value changes from two to `s+1` when
`z<a`. These three differences give (17) directly.

**Global response theorem.** Under (1)-(4), after normalization, the
supremum payoff of the specified monster law over every admissible
princess path equals

    sup K_new(a,u,c,y),
    0<=a<=u<=1,       -a<=c<=y<=1.                            (18)

Every boundary value means its legal one-sided payoff limit. The proof
uses the cap, the global suffix inequalities, and the monotone prefix
argument just given. Interior representatives use `U=1+epsilon` for
the final immediate inward leg. The sheet mass in `1<s<1+epsilon`
vanishes as epsilon decreases, while the optional `h0` line retains the
old late-capture convention. Endpoint and central-boundary paths are
covered by the same shrinking-path/Fatou argument as in the signed
response theorem, now with capture horizon five.

This is an all-princess upper response result. No unrestricted lower
monster-response claim is hidden in (18).

## 7. Effective suffix price and usable primal equations

Define

    W(z)=(1+z)ell(z)+(7-z)H(z)+2M(z).

Flatness gives the exact identity

    W(z)=F(1)-F(2-v(z))+ell(z)(z+2-v(z))
        =F(1)-Gamma(z).                                     (19)

Thus the positive suffix equation is `Fbar(a)=W(y)`, and the old scalar
gain formula is reused by replacing `(1+z)ell(z)` with `W(z)` on the
positive threshold interval. The negative-threshold price is unchanged.

For `c>0`, put `q=max(u,c)`, and let `K0` be the cumulative integral of
`k=h0+H+ell`. The scalar derivatives are

    4 K_new,a = 4 K_old,a + 2M(a),
    4 K_new,u = 4 K_old,u,

    4 K_new,c
      =w0+Gbar(a)+K0bar(q)
       -(8-c-q)h0(c)-(1-q)[H(c)+ell(c)],

    4 K_new,y = Fbar(a)-W(y).                                (20)

They are useful matching equations, but the global inequality (18), not
their stationarity alone, is the result supplied here.

There is a substantive support consequence. Monotonicity of `k` gives

    K0bar(q)>=(1-q)k(c),

so a free interior positive cutoff `c<y` satisfies

    (7-c)h0(c) >= w0+Gbar(a).                               (20a)

In particular, if `w0>0`, the turn sheet alone cannot support such a
branch: a nonzero density on the line `s=1` is required there. This is
why the optional `h0` component should not be removed from a candidate
merely because the sheet has been added.

For an endpoint-start branch, vary along `a=u=1, y=c`. The positive-c
indifference condition is

    (7-c)h0(c)+W(c)=w0,                                     (20b)

while the negative-c condition remains

    (1-z)f(z)+(7+z)g(z)=w0.                                 (20c)

Consequently an endpoint-positive active range cannot coincide with a
free extra-suffix c range having `Gbar(a)>0`.

## 8. An explicit nonempty example

Before normalization, take

    w0=1, f=1, g=0, h0=1/16, ell=1/4,
    v(z)=1+z/4.

Then

    h(z,s)=3/(28-3z)       for 1<s<1+z/4,
    H(z)=3z/[4(28-3z)],
    M(z)=3z^2/[32(28-3z)],
    Gamma(z)=3/4-7z/16,   W(z)=1/4+7z/16.

Every hypothesis is immediate: `k=5/16+H` increases, `f` and `f+g` are
constant, and `Gamma` decreases. Divide all masses and densities by

    Z=33/16+(7/3)log(28/25)

to obtain a probability law. This is an example of the globally
controlled class, not a proposed saddle or improved game bound.

The interior suffix exit is `y=(12-16a)/7`, clipped to the applicable
feasible interval. Every nondecreasing inverse graph inside
`1<=phi(z)<=1+z/4` before that exit has the same positive-suffix payoff.
In particular, the construction admits genuinely distinct smooth
princess trajectories instead of enforcing a common curve.

## 9. Matching target for the lower construction

For an ordered lower law, let `A(z)` be its initial-position CDF and
`R(s,z)` its radial CDF in characteristic coordinates. In a sheet where
both monster start and turn vary through indifferent interior choices,
turn indifference integrates exactly to

    R(s,z)=2-A(z)-K(z)/(6+s-z)^2.                             (21)

If `C(z)=R(1,z)` and `Y(z)=R(v(z),z)`, the two boundaries obey

    K(z)=[2-A(z)-C(z)](7-z)^2
        =[2-A(z)-Y(z)](v(z)+6-z)^2.                         (22)

The upper corridor provides precisely the freedom required to realize
these distributed ranks. Their inverse trajectories are

    s(z,q)=z-6+sqrt(K(z)/[2-A(z)-q]).                         (23)

The lower law still must obey the transport cone, the prefix matching,
the exit relation (15), normalization, common payoff, and the global
monster Bellman inequality. Equations (21)-(23) are recorded to identify
the concrete matching target, not to assert those obligations have
already been solved.
