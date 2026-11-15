# The local power at an active initial-inward boundary

## 1. What the calculation establishes

The strict ordinary-prefix attack in `INWARD_INITIAL_OBSTRUCTION.md`
requires a positive-length initial unit outward run. An immediately curved
initial path can avoid that argument. Its curvature is nevertheless
constrained if the positive M2 response is flat and an active initial-inward
sheet reaches the no-inward-turn boundary.

Under the local regularity hypotheses below, an initial power law

    p_b(t)=b+t-kappa(b)t^gamma+o(t^gamma),  gamma>1,

has the following alternatives.

* If `gamma>(1+sqrt(5))/2`, a sufficiently short inward turn decreases the
  cost below a flat positive-M2 value.
* If `1<gamma<(1+sqrt(5))/2`, the leading inward cost change is positive.
  An inactive gap next to that boundary is possible.
* If the inward cost is flat right up to the boundary, the exponent must be
  `phi=(1+sqrt(5))/2`, and the leading coefficient must satisfy

      kappa(b)^phi=2^(phi+1)/(phi[1+c_1(A(b))]).        (1)

In particular, finite nonzero quadratic initial curvature does not repair
the ordinary initial segment under these hypotheses. The balanced power
has initial velocity one and an unbounded initial acceleration. This is a
fixed-initial-position local result. It does not justify extending the
same power to the first incoming turn, choosing the whole inward support
wedge, or changing the endpoint tail exponents.

## 2. Hypotheses and traces

Fix an interior initial position `a` with `rho=A'(a)>0`. Use the exact
response and strict/closed trace conventions in `INITIAL_INWARD_CDF.md`.
Assume `beta(1)=2`, `beta(3)=4`, and set

    d=1+c_1(A(a))>0.

The initial paths in a neighborhood of `a` obey the displayed expansion,
uniformly in their initial position, together with its first time
derivative. More explicitly, the remainders in

    partial_t p_b(t)=1-gamma kappa(b)t^(gamma-1)
                       +o(t^(gamma-1))

are uniform there. The initial CDF and `kappa` are locally smooth enough
that changing the initial position by `O(delta)` changes their density
coefficients by `O(delta)`; `partial_b p_b(t)=1+O(t^gamma)` suffices.
The first `U=1` inverse moment is smooth at the relevant rank.

There is also a necessary off-diagonal regularity assumption. The changes
in `R(1,-a+delta)`, its V derivative, and the **uncut** column integral

    integral_a^1 R_V(U,-a+delta)dU

are `O(delta)`. This rules out another caustic or singular attachment
contributing at one of the powers being balanced. The initial power itself
satisfies this column condition: its potentially singular second
derivative is integrable in U when `gamma>1`. A full candidate must check
its other interfaces separately.

The initial path has no positive-length unit run. Thus the right-hand
first contact of the initial rank tends to time zero. This is different
from the jump used in the ordinary-prefix exclusion.

## 3. Two terms in the exact inward derivative

Put `v=-a+delta`, with `delta>0`. At the first monster turn the time is
`delta/2`. Its radial rank comes from the initial position

    b_delta=a-delta+kappa(a)(delta/2)^gamma
                      +o(delta^gamma).

Consequently

    R_V(a,-a+delta)
      =-rho+rho kappa gamma delta^(gamma-1)/2^gamma
                +o(delta^(gamma-1))+O(delta).          (2)

The coefficient of this derivative in the exact I formula tends to `d`.
This produces the positive first term below.

The column integral in that formula begins where rank `A(a)` first reaches
the outgoing characteristic `V=-a+delta`. On the curved initial segment,

    delta=kappa(a)t^gamma+o(t^gamma),

so its U coordinate is

    alpha_delta=a+2 kappa^(-1/gamma)delta^(1/gamma)
                    -delta+o(delta^(1/gamma)).         (3)

Moving the lower column limit from `a` to `alpha_delta` removes a negative
integral. Since `R_V=-rho+o(1)` on that shrinking interval, its contribution
to the inward derivative is

    -2rho kappa^(-1/gamma)delta^(1/gamma)
                    +o(delta^(1/gamma)).               (4)

Combining (2)-(4) with the exact CDF response gives

    4[CI_v(a,-a+delta)+Cg'(a)]
      =rho[d kappa gamma delta^(gamma-1)/2^gamma
                 -2 kappa^(-1/gamma)delta^(1/gamma)]
         +o(delta^(gamma-1)+delta^(1/gamma))+O(delta).  (5)

The baseline `CI_v(a,-a+)=-Cg'(a)` uses the unit initial tangent and the
absence of a positive-length initial run. If `Cg` is flat, it vanishes.
The two displayed powers agree exactly when `gamma-1=1/gamma`, giving
`gamma=phi`. Their coefficients then agree exactly at (1), because
`1+1/phi=phi`. If `gamma>phi`, the negative term has the smaller exponent;
if `gamma<phi`, the positive term does.

When the leading powers cancel, the assumptions in this section give only
a smaller-order remainder. They do **not** determine its sign or prove an
active patch exists. A higher initial expansion and the global row/column
attachments are still needed.

## 4. An independently computable legal fixture

The test family starts with `b` uniform on `[L,H]=[1/5,2/5]`. For
`T0=1/32` and `c0=9/10`, define

    p_b(t)=b+t-kappa t^gamma,             0<=t<=T0,
    u(b)=b+2T0-kappa T0^gamma,
    c(b)=c0-b.

After `T0`, the path runs inward at unit speed to zero, waits there until
`c(b)`, runs outward at unit speed to one, and stays there. The tested
coefficients satisfy the speed bound and `u(b)<c(b)`. The family is ordered,
has no first-contact atoms in the initial band, and absorbs at the endpoint
before time two.

For `a=3/10`, let `rho=1/(H-L)` and `d=1+c0-a`. Direct integration of the
capture groups yields the exact remainder

    4[CI(a,-a+delta)-Cg(a)+delta Cg'(a)]
      =rho[ d kappa delta^gamma/2^gamma
          -2gamma kappa^(-1/gamma)delta^(1+1/gamma)/(gamma+1)
          +delta^2/2
          +kappa delta^(gamma+1)/((gamma+1)2^gamma)
          -kappa^2 delta^(2gamma)/2^(2gamma+1) ].        (6)

The verifier does not use (6) to obtain the compared cost. It intersects
each actual curved or straight princess piece with the actual unit-speed
monster legs, takes the first equality, and integrates those capture times
over the initial rank. It then compares the result and finite-difference
derivatives with (6).

The linear subtraction in (6) can also be realized by an ordered physical
mixture. Give this continuum mass `m=1/20`; give the ordinary path
`(a,u,c)=(4/5,9/10,2/5)` mass `n=4m Cg'_wave`; give the remaining mass to
the path initially at zero which leaves center at `c=19/20`. The high path
lies above the continuum, the center path lies below it, and all weights
are positive. Their positive-M2 derivatives are respectively `-1/4` and
zero, so the mixture has **exactly constant** `Cg` on the tested initial
band. Their inward-minus-M2 costs cancel the linear term exactly. Thus its
actual four-score inward gain is `m` times (6).

For `gamma=2`, this actual gain is negative with leading order
`delta^(3/2)`. For `gamma=3/2` it is positive at sufficiently small delta.
For `gamma=phi` and coefficient (1), the two leading terms in (6) cancel
exactly, leaving the positive term `rho delta^2/2` at next order. This last
fixture demonstrates the leading balance; it is not a flat-I solution.

Run the high-precision audit with

```sh
python -B packages/interval_turn_sheet/verify_curved_initial_power.py
```

`--quick` uses two scales per case. The complete audit halves delta across
seven scales. These are high-precision analytic-curve fixtures, not Fraction
certificates, interval enclosures, or a new game bound.

## 5. Relation to the construction problem

`INITIAL_INWARD_CDF.md` gives the full derivative-free response and the
conditional Volterra equation for an active initial patch. The present
balance supplies a local boundary germ for that equation. It does not fix
the active set. In particular, an active curved germ may end before the
first incoming turn and be followed by a later unit-outward segment; the
ordinary exclusion applies to the initial run, not every later such
segment. Transport, the incoming attachment, the exact endpoint moments,
and all other monster responses remain separate matching obligations.
