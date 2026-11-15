# Exact payoffs for continuous ordered multi-leg laws

`continuous_rank.py` evaluates the expected capture time of a polygonal
monster against a continuous symmetric ordered princess law. It does not
discretize the princess distribution or use the finite-hider response
oracle. Rational input is evaluated using `fractions.Fraction` throughout.

For uniform `q` in `[0,1]`, the positive princess follows

```text
p_q(t) = min(1, max(min(a(q)+t, u(q)-t), t-C(q), 0)).
```

The parameters are continuous and piecewise affine on a shared quantile
partition. Both `a,u` are strictly increasing; `C` is strictly decreasing.
The constructor checks `0 <= a <= 1`, `u >= a`, and `-a <= C <= 1` at every
knot, which implies these inequalities throughout every affine piece.
The law chooses this path or its reflection with equal probability.
An optional `endpoint_mass` is split equally between stationary endpoints.

The formula uses clipping at one. It does not silently replace an earlier
endpoint visit by permanent absorption. Every path is permanently at its
signed endpoint by time two because `C <= 1`. If permanent absorption at
the *first* endpoint visit is desired, an additional absorption cap is
needed; the current engine makes no such claim.

## Five legs and additional waves

`FiveLegLaw(q,a,u1,c1,u2,c2,endpoint_mass=0,exact=True)` implements

```text
z1 = max(min(a+t,u1-t),t-c1)
z2 = max(min(z1,u2-t),t-c2)
p  = min(1,max(0,z2)).
```

It checks strict increase of `a,u1,u2` in rank, strict decrease of `c1,c2`,
and the pointwise inequalities

```text
a <= u1 <= u2,    -a <= c1 <= c2 <= 1,
a+u1 <= 2,       u2-c1 <= 2.
```

The last two inequalities exclude early endpoint peaks at every interior
rank. Their left sides increase strictly, so equality can occur only at the
top rank `q=1`, which has zero probability. Thus the clipped formula agrees
almost surely with permanent absorption at the first endpoint visit;
no extra absorption CDF is needed for this class. A separate stationary
endpoint-pair atom is still supported.

With `I_j(z)=Pr(u_j<=z)` and `D_j(z)=Pr(c_j>=z)`, its radial CDF is

```text
R(t,r) = max(A(r-t), min(I1(t+r),D1(t-r)),
                       min(I2(t+r),D2(t-r))).
```

The integration algorithm is unchanged: it includes every component knot
and every affine branch crossing before selecting the active radial branch.
`MultiLegRankLaw(q,a,incoming,outgoing,...)` supports any finite number of
such incoming/outgoing pairs. It checks the analogous peak inequality
`incoming[j]-outgoing[j-1]<=2` for each later outward peak.

## Exact integration

Set `A(z)=Pr(a<=z)`, `B(z)=Pr(u<=z)`, and `D(z)=Pr(C>=z)`. These are continuous
piecewise-affine functions. The interior radial CDF is

```text
R(t,r) = min(max(A(r-t), B(t+r)), D(t-r)).
```

At radius one, this expression is the limit from the interior. It excludes
the endpoint atom. At radius zero it includes the central atom.

Let `F_left(t,x)=Pr(p(t)<x)` and `F_right(t,x)=Pr(p(t)<=x)` be the full signed
CDF limits. For a continuous monster path `m`, the captured rank interval
has endpoints

```text
L(t) = inf_{s<=t} F_left(s,m(s)),
U(t) = sup_{s<=t} F_right(s,m(s)).
```

Ordering and continuity of the individual paths give this identity: a rank
outside the interval stays strictly on one side of the monster; a rank
strictly between the two records must intersect it by continuity. Boundary
rank exceptions have zero probability unless several princesses coalesce,
in which case the left/right CDF limits include the entire captured atom.
The survival probability is therefore `1-U(t)+L(t)`.

On each monster leg the program splits time at spatial zero crossings,
parameter-CDF knots, clamp branch changes, and crossings of the running
CDF records. Every surviving expression is affine in time, so its integral
is rational and exact. Exact left/right limits at zero and at both endpoints
are evaluated at every boundary, including waits. This is necessary when
center or endpoint atoms are present.

```python
from fractions import Fraction as F
from continuous_rank import RankLaw

law = RankLaw([0, 1], [0, 1], [0, 1], [1, 0])
monster = [(0, 0), (F(1, 2), 0),
           (F(3, 2), 1), (F(7, 2), -1)]
answer = law.payoff(monster)
assert answer.value == F(11, 8)
assert answer.survival == 0
```

`exact=False` enables floating arithmetic for bounded structural experiments.
It does not create a certificate. `require_complete=False` returns the
truncated payoff at the final vertex and the surviving mass. The default
rejects an unfinished response.

## Verification and scope

Run `python verify.py` in this directory. Seven analytically calculated
fixtures cover outward motion, delayed sweeps, center arrivals, central
waiting atoms, and stationary endpoint atoms. Six further routes compare
rational and floating evaluation, and compare with an independent explicit
segment-intersection calculation on midpoint quantiles. That latter check
uses the uniform quantile discrepancy bound; it is a sanity check, not the
source of the exact engine's result.

Additional exact fixtures check a two-parameter quadratic response, the
downward payoff jump caused by an exact center wait, and degeneration of
five legs to three. A genuine five-leg example has two distinct central
arrival waves; its truncated center-wait payoff and residual mass `3/7`
are calculated analytically. Six independent polygonal capture comparisons
also check that five-leg example.

This evaluator computes a fixed monster payoff. It does not itself optimize
over all monsters, assert that three princess legs suffice at equilibrium,
or certify a new interval for the game value. The finite response theorems
in `research/09-equilibrium-structure/` explain when a finite collection of
continuous monster words is exhaustive.

For a fixed rational law and a fixed direction word with affine vertex
parameters, exact payoff is piecewise quadratic on a finite rational
polyhedral subdivision of the word's parameter domain. Collision candidates
are affine in the quantile and monster parameters, their validity and order
comparisons are linear, and integrating over the resulting affine quantile
endpoints is quadratic. Coincident legs and other equality cases must be
included as separate faces. This establishes a finite algebraic route to an
all-monster check; this package currently evaluates points, not the full
subdivision or its quadratic minimization problems.
