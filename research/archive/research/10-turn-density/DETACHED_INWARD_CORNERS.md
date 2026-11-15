# Detached inward corners: exact costs and a conditional response reduction

**Subsequent endpoint test:** `ENDPOINT_INWARD_OBSTACLE.md` proves that an
active positive M1 start with no initial atom at that start forbids a
positive-length initial unit-outward run on a positive-mass band above
it (including an atom at the replacement's upper start). Thus making positive M2 inactive
does not rescue an ordinary-initial matching tail. The identities and
pre-one response reduction below remain valid conditional calculations;
the omitted endpoint-I face is essential to the unrestricted game.

An ordinary initial unit-speed segment is incompatible with an **active**
positive M2 at the corresponding start; see
`INWARD_INITIAL_OBSTRUCTION.md`. That obstruction does not assume that
positive M2 must be active in every equilibrium. This note analyzes a
different support: positive M1 and negative M1 remain active, while a
monster starts at an ordinary princess's first incoming corner, makes an
initial inward excursion, and turns outward again at a second outgoing
corner. No positive-M2 equality is imposed.

The cost identities below are exact. The response reduction is conditional
on stated concavity and source conditions. They do **not** construct a
matching law. In particular, the simplest upper measure supported only on
the resulting one-dimensional corner curve has a separate outgoing-cutoff
kink obstruction. A lower response reduction cannot resolve that upper
stationarity problem by itself.

## 1. Fronts and the ordinary terminal field

Use initial deficit `xi=1-a`, incoming defect `h(xi)=1-u(a)`, and outgoing
deficit `d(xi)=1+c(a)`. Let `r(xi)` be the mass of initial positions above
`1-xi`. All three fronts are increasing, and the terminal ordinary paths
have

    0<h(xi)<xi<d(xi).

Write

    e(y)=r(d^{-1}(y)),       i(x)=r(h^{-1}(x)).

In the negative-V terminal cone, the full CDF deficit is

    D(x,y)=max(e(y),min(r(y),i(x))),       0<=x<=y,
    x=1-U, y=1+V.                                      (1)

The retained lower ranks lie below every first turn considered. Their
pre-one incoming source is `Omega`, and their post-one source is `Q`,
with the definitions and strict/closed trace conventions in
`CURVED_TERMINAL_SOURCES.md`. Assume an outgoing gap throughout the
terminal interval, so `H(s)=0` there. Assume continuous front laws when
differentiating; the identities also have the corresponding Stieltjes and
one-sided versions.

Let `V0` denote the endpoint-sweep payoff. It is a reference payoff, not
an asserted game value. Set

    W(xi)=integral_0^xi d(t)dr(t).

## 2. The detached double-corner route

Choose `xi`, and define

    x=h(xi), tau=d^{-1}(xi), k=h(tau),
    E=e(xi), R=r(xi), rx=r(x).

Require the useful-capture gap

    tau<x, equivalently E<rx.                         (2)

The monster starts at `a=1-x`, turns inward at `V=-1+xi`, turns outward
until `U=1-k`, and then sweeps the two endpoints. Its first turn is the
initial/incoming corner of rank `1-r(xi)`; its second is the
incoming/outgoing corner of rank `1-e(xi)`.

Deleting the final part of the outward leg, from `U=1-k` to `U=1`, saves
exactly

    T(xi)=k[3-R+2E]+Omega(k)                          (3)

in four times expected capture time. The retained low ranks are **below**
the first inward turn, and enter this formula through their later first
inverse; they are not assumed captured on the initial inward leg.

The exact comparison to negative M1 starting at the same `a=1-x` is

    4[CI_corner-Cell(1-x)]
      =x[3+2rx-R]+Omega(x)
       -(8-xi)(rx-E)-integral_tau^x h(t)dr(t)-T(xi).   (4)

No equality of any monster cost was used in (4). In particular, this
formula remains meaningful when positive M2 has slack.

Combining the exact positive-M1 and negative-M1 moment identities gives
the independent comparison

    4[CI_corner-Cf(1-xi)]
      =(8-2xi)E-3xi-Q(xi)+xi r(h(xi))
       +integral_{h(xi)}^xi[t-h(xi)+h(t)]dr(t)-T(xi). (5)

The coefficient is **`8-2xi`**, not `8`. Exact physical capture fixtures
with nonzero E distinguish them. Hence simultaneous positive-M1 and
corner equality requires

    (8-2xi)E
      =3xi+Q(xi)-xi r(h(xi))
       -integral_{h(xi)}^xi[t-h(xi)+h(t)]dr(t)+T(xi).  (6)

This is a replacement for the earlier active-positive-M2 equation. It
must be solved jointly with the positive-M1 and negative-M1 moments, the
quantile relation `e=r o d^{-1}`, the ordering gap (2), and the outer
attachment. The old active-g tail history cannot simply be reused.

## 3. A general outgoing-ridge route

For arbitrary first-turn parameters `0<x<=y`, put

    tau=d^{-1}(y), k=h(tau), m=min(y,h^{-1}(x)),
    E=e(y), D0=r(m), rx=r(x).

Consider the useful branch `E<rx`, or `tau<x`. The first turn has deficit
rank D0. Its optimal second turn has not yet been assumed; the route
below specifically uses the outgoing ridge `U=1-k`.

Its exact four-cost relative to the endpoint reference is

    J(x,y)=4[CI_ridge(1-x,-1+y)-V0]
      =y rx+(8-y)E-W(m)
       +integral_x^m(t-x)dr(t)
       -integral_tau^x h(t)dr(t)
       -k[3-r(m)+2E]-Omega(k).                       (7)

To derive (7), insert (1) into the source-free fixed-second comparison.
The first-turn row splits at `m`; its integration-by-parts term is
`W(m)-integral_x^m(t-x)dr`. The initial-rank hinge in the middle column is
exactly `integral_tau^x h dr`. Finally apply the deletion (3), with R
replaced by r(m). This also explains why Q does not appear directly in
(7): it enters the positive-M1 matching equation, not this comparison.

## 4. Reducing every second turn to two endpoints

Fix x,y and allow every second turn `a<=s<=1`, where `a=1-x`. Write
`z=1-s`. The outward leg is redundant if its capture frontier never
exceeds the initial frontier. Such a route is pointwise dominated by
negative M1 starting at a; this is the `B<=A` dominance of
`INWARD_TURN_DOMINANCE.md`.

On the useful ordinary incoming segment,

    k<z<h(x),  D(z,y)=i(z)<r(x)<=D0.

All high ranks below the first turn have already completed their
incoming motion. The only remaining first-inverse derivative is the low
source `Omega'(z)`. The exact second-turn derivative becomes

    4 CI_s=3-D0+2i(z)+Omega'(z)-(8-y-z)i'(z).          (8)

Assume

    i'>0, i''<=0, Omega'>=0, Omega''>=0.              (9)

Then throughout this useful segment

    4 CI_ss=-3i'(z)-Omega''(z)+(8-y-z)i''(z)<0.       (10)

Thus the cost is strictly concave as a function of the second-turn U.
Its minimum is at an endpoint. The earlier endpoint has `B=A` and is
dominated by the collapsed negative-M1 route. At the later endpoint the
turn reaches the outgoing ridge. After that ridge, `D=e(y)` is constant
in U and

    4 CI_s=3-D0+2e(y)+Omega'(z)>0.                    (11)

Consequently every second turn is dominated in expected cost by either
the collapsed outward leg or the outgoing ridge. Under (9), a positive
measure of nondegenerate interior second turns cannot consist of
minimizers. This includes a quarter-root incoming deficit, which is
strictly concave.

## 5. Reducing the remaining first turn to its corner

Assume in addition that r is increasing and concave. On the initial side
`x>=h(y)`, so `m=y`, differentiation of (7) gives

    J_x=(y-h(x))r'(x)+r(x)-r(y)
       >=(x-h(x))r'(x)>0.                            (12)

The inequality uses only concavity of r. Hence for fixed y, every such
route has cost at least that of its first-corner route `x=h(y)`.

On the other side, `y>=h^{-1}(x)` and `m=h^{-1}(x)` stays fixed as y
varies. Differentiation gives

    J_y=r(x)-E+(8-y-k)e'(y)
        -k'(y)[3-i(x)+2E+Omega'(k)].                 (13)

A sufficient condition for strict positivity on the useful branch is

    (8-y-k)r'(tau)
       >=h'(tau)[3+2e(y)+Omega'(k)],  tau=d^{-1}(y).  (14)

Indeed, `e'=r'(tau)/d'(tau)` and `k'=h'(tau)/d'(tau)`;
the omitted `-i(x)` term helps, and `r(x)-E>0`. Thus every point on this
side has cost at least the first-corner route obtained by reducing y to
`h^{-1}(x)`.

Suppose all relevant corners satisfy (2), all negative-M1 costs in the
terminal interval equal V0, and (6) is solved together with positive-M1
equality. Equations (10)--(14) then prove **every terminal I(a,v,s)
inequality**, not merely equality at the selected double-corner curve.
All domain paths used in the comparison must remain inside the interval
where the displayed fronts and source gates hold. This is a response
certificate for that terminal component, not for the entire game.

## 6. Why a distributed ordinary incoming equality strip is obstructed

Without concavity of i, (10) alone does not exclude an interior minimum.
However, an open equality strip in `(y,z)` along first corners would
require

    (8-y-z)i'(z)=3-r(y)+2i(z)+Omega'(z).              (15)

Differentiating in y yields `r'(y)=i'(z)`. On an open rectangular subset
both derivatives must therefore be the same constant lambda. Then
differentiating (15) in z gives

    Omega''(z)=-3lambda<0.                           (16)

So a convex low source also rules out such an open two-dimensional
ordinary incoming equality strip, even without first assuming i is
concave. This statement concerns an open smooth strip; it does not rule
out singular support, varying first-turn ranks away from the corner,
source concavity, or genuinely curved incoming paths.

## 7. Independent exact checks

Run

```sh
python -B packages/interval_turn_density/verify_detached_inward_corner.py
```

The comparison side uses only piecewise-affine front moments. The payoff
side is the independent continuous-rank engine, which integrates running
signed CDF records along physical monster routes. The fixtures check
(3)--(5), general ridge costs (7), and the second-turn endpoint/ridge
dominance for concave initial and incoming deficits. They deliberately
do not impose g equality. They have `Q=Omega=0`; the source terms in the
general formulas are separately checked by
`verify_curved_terminal_sources.py`.

No numerical field, asymptotic series, or finite collection of checks in
this note is asserted to be a matching law.
