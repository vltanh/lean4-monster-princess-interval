# A two-state all-monster certificate for an ordinary ordered wave

This gives an exhaustive lower-response certificate for the ordinary
three-leg princess family. Its center continuation inequality has only
three scalar arguments: the current time, one surviving frontier, and the
next return time. It does not assume a bound on the monster's turn count.

No function satisfying the initial inequalities at the proposed game value
has yet been supplied. Thus this is a positive certificate format, not a
matching equilibrium or an evaluation of the game.

## 1. Family, inverses, and the center peak

Let the positive princess paths be

    p_q(t)=min(1,max(0,min(a(q)+t,u(q)-t),t-c(q))),

with equal reflected mass, and with q uniform on (0,1). Assume a and u are
continuous and strictly increasing, c is continuous and strictly decreasing,
and

    0 <= a(q) <= u(q) <= 2-a(q),    -a(q) <= c(q) <= 1.

The last upper bound on u makes the first outward turn occur no later than
the endpoint. Since a+u is strictly increasing, equality can occur at at
most one rank and does not create a positive-mass early endpoint plateau.
This allows u>1; it does not replace the bound by u<=1. All
paths are fixed at their signed endpoints by time two. The strictness
assumptions exclude interior coalescence; center and endpoint waiting are
allowed. Atomic variants require their exact first-touch traces and are not
inferred by a limit from this statement.

Use

    A(z)=Pr(a<=z),    I(z)=Pr(u<=z),    C(z)=Pr(c>=z),
    alpha_q(s)=inf{t>=0:t+p_q(t)>=s},
    B_q(s)=inf{t>=0:t-p_q(t)>=s}.

Extend A and I by zero to negative arguments and by one above their
supports; extend C by zero above one. For interior radius, write

    R(U,V)=Pr(p_q((U+V)/2)<=(U-V)/2)
          =min(max(A(-V),I(U)),C(V)).                       (1)

In particular, in the reachable cone following a center visit,

    R(U,V)=min(I(U),C(V)),    0<=V<=U.                     (2)

Choose tau in [0,1] at the crossing of the increasing I and decreasing C:

    I(t)<=C(t) for t<=tau,    I(t)>=C(t) for t>=tau.

Write Q=I(tau)=C(tau), with the usual choice inside an equality interval.
Every zero-to-zero path on [t,e] has t<=V<=U<=e. Therefore its entire
reachable cone has R=I(U) when e<=tau. If t>=tau, its entire future cone
has R<=C(t). At that center visit, both signs through rank C(t) have already
been captured. Hence no later interior excursion can acquire a new rank.

The endpoint completion cost, when the monster is at center time e>=tau
and the two captured radial frontiers are r and n, is

    E(e,r,n)
      =(e+2)*(1-(r+n)/2)-abs(r-n)/2.                     (3)

It visits the side with the smaller captured frontier first. Formula (3)
is an absolute-time contribution from the still uncaught paths; it excludes
all paths captured before the center visit.

## 2. Exact center states and actions

At any center visit t<=tau, after a same-half prefix and any number of
earlier center excursions, the two captured frontiers have the form

    (I(t),M),    I(t)<=M<=1.                              (4)

The side with frontier I(t) is called the lagging side. The other frontier
is the initial asymmetry, until I catches it. A center wait or an early
return triangle cannot create another independent frontier.

For t<=e<=tau, a triangle into the lagging side captures q in
(I(t),I(e)] on its outward leg at time (u(q)+t)/2. On return, the opposite
copies with q>M are captured at time e. Thus its immediate absolute capture
contribution is exactly

    K(t,e;M)
      =1/4 integral_{I(t)}^{I(e)} (u(q)+t)dq
        +e/2*(I(e)-M)_+.                                (5)

It returns to

    (e,max(M,I(e))).                                     (6)

A triangle into the other side has the same final state and is no better:
for q<=M only the lagging copy is still uncaught, while for q>M the two
copies have equal weight. This proves that the sign choice disappears from
the center Bellman problem.

A wait at center from t to e has immediate contribution

    W(t,e;M)
      =1/2 integral_{I(t)}^{I(e)} u(q)dq
       +1/2 integral_M^{max(M,I(e))} u(q)dq,              (7)

and the same final state (6). Empty integrals are zero.

### Terminal actions

A direct sweep from the lagging side to its endpoint and then to the other
endpoint contributes

    S(t,M)
      =1/4 integral_{I(t)}^{C(t)} (u(q)+t)dq
       +(t+1)/2*(1-C(t))+(t+3)/2*(1-M).                 (8)

The first integral is the interior incoming capture; ranks above C(t) on
that side are caught at the first endpoint. Since u<=2 and t>=0, no
incoming rank is missed merely because the first endpoint is reached.

The remaining terminal action is a triangle returning at e>=tau, followed
by endpoint completion. It suffices to take

    tau<=e<=2,    e-t<2.                                 (9)

Indeed, after e=2 the outgoing capture frontier is constant and a later
return only delays the remaining captures. The boundary e-t=2 is an actual
endpoint visit and is already covered by (8); its first-touch gain must not
be discarded by treating it as an interior turn.

Put

    r=min(I(e),C(t)),    n=C(e).

The terminal triangle's contribution is

    T(t,e;M)
      =1/4 integral_{I(t)}^r (u(q)+t)dq
       +e/2*(n-M)_+ + E(e,r,max(M,n)).                   (10)

It too may be taken into the lagging side. If r<=M, this captures more of
the only uncaught low-rank side no later, and leaves identical high-rank
endpoint times. If r>M, the pairs with q>M have identical costs under
reflection of the whole terminal route, while every remaining q<=M is
caught earlier by the lagging-side route. This also proves the sign claim
when the optimal endpoint order changes after the triangle.

## 3. The two-state Bellman certificate

Let P(t,M) be a bounded continuous function on

    D={(t,M):0<=t<=tau, I(t)<=M<=1}.

It represents a lower bound for the absolute-time contribution of paths
still uncaught at that center state. Require all of the following:

    P(t,M) <= S(t,M),                                    (B1)
    P(t,M) <= T(t,e;M)                 for (9),           (B2)
    P(t,M) <= K(t,e;M)+P(e,max(M,I(e))) for t<=e<=tau,    (B3)
    P(t,M) <= W(t,e;M)+P(e,max(M,I(e))) for t<=e<=tau.    (B4)

These are explicit integral inequalities in at most (t,M,e). In
particular, (B3) checks every possible next return, rather than checking a
presumed finite list of return times. The common boundary e=t is harmless.

If I has a density, (B4) may instead be verified by its differential form
and continuity across M=I(t). For M>I(t), it is

    partial_t P(t,M) >= -t*I'(t)/2.                       (11)

Along the diagonal it is

    d/dt P(t,I(t)) >= -t*I'(t).                          (12)

For nonsmooth P, retain the integral form (B4).

**Center theorem.** Under (B1)-(B4), every monster continuation from the
state (4) has expected remaining absolute contribution at least P(t,M).

For a finite sequence of waits and early triangles, apply (B3) or (B4)
at every step and telescope the immediate capture contributions. The first
endpoint action or first return crossing tau is bounded by (B1) or (B2).
At and after tau, (3) is exact. This proves the result for finite canonical
continuations.

To cover arbitrary Lipschitz continuations, use the finite ordered-quantile
capture-order domination and uniform truncated-payoff approximation from
`../09-equilibrium-structure/CENTER_RETURN_REDUCTION.md`, Sections 3 and 6.
The chosen canonical paths finish by time six. Their center excursions can
be replaced by maximal tents between the same zero endpoints: targets in
that half are caught no later, while opposite-side captures can only occur
at a zero junction. The Bellman argument applies to the resulting finite
sequence under the original continuum law. Uniform quantile discrepancy
then transfers its lower bound to the original monster. No density
partition, compactness claim for singular capture times, or turn bound is
used in this step.

## 4. Explicit initial-prefix attachment

The center theorem must be attached to the monster's free initial
position. It does not by itself certify a game value.

By reflection it suffices to start at +z. Before the first center or
endpoint visit, new captures relative to the initial rank split have the
order: early lower ranks, higher ranks, late lower ranks. The raw radial
trace itself may oscillate. `ORDINARY_PREFIX_COMPRESSION.md` proves that
these record phases permit two useful capture turns and, for an endpoint
prefix, one final joining turn. It gives a pointwise comparison for
arbitrary-speed prefixes and explains why cross-initial-rank characteristic
atoms require separate treatment. The following two finite families contain
the resulting prefixes; any earlier center visit uses the center theorem.

### Prefix ending at center

Start at +z, move left with U=z until V=v, then right with V=v until U=b,
then left to the center at time b. Use

    0<z<=1,    -z<=v<z,    z<=b<v+2.                     (13)

Zero-duration legs are allowed. Direct motion to center is included by
b=z. The boundary v=z with b>z is already a center visit at time z and
belongs to the Bellman continuation, not to a prefix with first visit b.

Put

    a0=A(z),    r0=R(z,v),    r1=R(b,v),
    Z(b)=min(I(b),C(b)),    M=max(a0,r1).

The exact contribution captured by the first center visit is

    L(z,v,b)=1/2 [
       integral_0^{r0} alpha_q(b)dq
      +integral_{r0}^{a0} alpha_q(z)dq
      +integral_{a0}^{M} B_q(v)dq ]
      +b*Z(b)/2.                                        (14)

All initially lower positive ranks are caught by the last inward leg;
initially higher positive ranks are caught only on the outward leg. No
negative copy is caught before the center, where its captured frontier is
Z(b). This proves (14) directly, rather than by a smooth derivative rule.

If b<=tau, then r1=max(A(-v),I(b)) and consequently

    M=max(A(z),I(b)),    Z(b)=I(b).                       (15)

For a proposed lower value h, require

    L(z,v,b)+P(b,M) >= h                if b<=tau,       (I1)
    L(z,v,b)+E(b,M,Z(b)) >= h           if b>=tau.       (I2)

Starting at the center additionally requires

    P(0,I(0)) >= h.                                      (I0)

### Prefix reaching an endpoint first

Use the four legs

    inward U=z; outward V=v; inward U=b; outward V=w,

followed by the direct opposite-endpoint sweep. The successive interior
turns have characteristics (z,v), (b,v), and (b,w), with

    -z<=v<z,    z<=b<v+2,    v<=w<b.                     (16)

The first endpoint is reached at time w+1 and the other at time w+3.
Padding by zero-duration legs includes a direct initial endpoint sweep
and prefixes with fewer useful turns. An actual earlier endpoint or center
visit is treated by its own completion rather than by continuing the
interior formula through it.

Put

    r0=R(z,v),    r1=R(b,v),    r2=R(b,w),
    l=min(r0,r2),    H=max(A(z),r1).

Its complete expected capture cost is

    J_end(z,v,b,w)=1/2 [
       integral_{r0}^{A(z)} alpha_q(z)dq
      +integral_l^{r0} alpha_q(b)dq
      +integral_0^l alpha_q(w+2)dq
      +integral_{A(z)}^H B_q(v)dq
      +integral_H^1 B_q(w)dq
      +integral_0^1 B_q(w+2)dq ].                       (17)

The first three integrals are the successive first captures of positive
paths initially below the monster. The next two are positive paths
initially above it. The last is the negative half, caught on the final
leftward sweep. Formula (17) includes captures on the endpoint itself via
the exact inverses; no limiting interior trace is substituted.

Require

    J_end(z,v,b,w) >= h                                  (I3)

on (16), and include direct starting-endpoint sweeps. This last initial
family has four scalar parameters. The center Bellman problem remains
two-dimensional; there is no hidden additional center frontier in (I3).

**All-monster criterion.** If (B1)-(B4) and (I0)-(I3) hold, the specified
princess law guarantees h against every unrestricted Lipschitz monster.
The proof is the initial-prefix normalization, the center theorem, and the
same uniform finite-quantile transfer. A matching unrestricted upper law
would then close the game at h. Neither a matching P nor such an h has yet
been established for the candidate under construction.

## 5. An optional convex-density compression

There is a useful strengthening of the finite-density-partition result.
Suppose the incoming density i=I' is nonnegative and convex on [0,tau].
For balanced center states, the excess cost of a triangle over waiting is

    D(s,e)=1/4 integral_s^e (s+2e-3v)i(v)dv.              (18)

Every sequence of balanced pre-tau triangles is then dominated by one
triangle and center waits, even if (18) is negative on some intervals.

Here is an elementary proof. For a convex function f on [0,1], integration
against its nonnegative distributional second derivative gives

    integral_0^1 (3x-2)f(x)dx
      <= f(1)/2-integral_0^1 f(x)dx.                    (19)

It is equality for affine functions; for the hinge (x-r)_+, the difference
between the left side and right side is -r^2(1-r)/2. Therefore D(s,e)<=0
implies

    i(e) >= 2*(I(e)-I(s))/(e-s).                         (20)

For fixed s, let

    H(e)=(e-s)i(e)-2*(I(e)-I(s)).

Then H(s)=0 and H''=(e-s)i''>=0 distributionally. Once H(e)>=0, convexity
implies H stays nonnegative to its right. Since partial_e D=-H/4, extending
that profitable triangle to the right cannot worsen its cost. It also
implies i is nondecreasing beyond e.

For adjacent intervals,

    4[D(s,w)-D(s,e)-D(e,w)]
      =2(w-e)(I(e)-I(s))-(e-s)(I(w)-I(e)).               (21)

By (20) and the subsequent monotonicity of i, (21) is nonpositive. Drop
every triangle with positive excess cost. Extend the first remaining one
across each intervening wait and merge each later one by (21). This proves
the claim. Singular convex endpoint densities are allowed by restriction
to compact subintervals and the finite-horizon approximation already used
above.

The two exceptional pre-balance triangles in the earlier reduction can
also be merged whenever a balance-crossing triangle actually occurs:
start a lagging-side triangle at the beginning of the pre-balance sequence
and end it at that crossing return. For q<=M its only uncaught copy is
caught no later by the larger lagging-side tent. For q>M no earlier
pre-balance triangle captured either copy; reflecting the crossing
triangle if necessary and moving its start earlier decreases their paired
capture times. A center wait that itself crosses the balance level is a
separate case and is already covered by (B4).

These compression facts may simplify an eventual P or initial-prefix
verification. They do not imply that checking only M1, M2, and M3 is
sufficient without the remaining inequalities above.

## 6. Concavity removes the continuous frontier check

For a fixed continuation route starting at center time t, first future
capture times on either sign are nondecreasing in radial rank. Indeed, a
route beginning below two ordered nonnegative paths must meet the lower
path before it can meet the higher one. Thus the part of the route's cost
depending on M is

    1/2 integral_M^1 T_q dq,

which is concave in M, with slopes at most -t/2. The infimum over routes is
also concave. Hence the true optimal center continuation has this shape.

Suppose a proposed P(t,.) is concave and piecewise affine, and every one of
its slopes is at most -t/2. Each right side in (B1)-(B4) is then concave as
a function of M:

* In (B3), below I(e) its slope is -e/2; above I(e) it is a slope of
  P(e,.), which is no greater and subsequently nonincreasing.
* In (B4), below I(e) its slope is -u(M)/2, which decreases with M. At
  I(e), its left trace is at least -e/2 and the right slope is at most
  -e/2. Above that point, concavity follows from P(e,.).
* S is affine in M. For T, put n=C(e) and r=min(I(e),C(t)), so n<=r.
  Its successive slopes on M<n, n<M<r, and M>r are respectively
  -e/2, -(e+1)/2, and -(e+3)/2. Empty pieces are simply omitted.

Consequently, on each affine M interval of P(t,.), checking a Bellman
inequality at both endpoints proves it throughout that interval: the
concave right side lies above its chord, while P equals its chord.

It therefore suffices to check (B1)-(B4) at the finitely many frontier
knots of P, including its moving lower boundary M=I(t) and M=1. The
remaining continuous variables are t and e. This is a finite sufficient
certificate scheme independent of a guessed monster turn count. It
interpolates a verification potential, not the princess law.

## 7. Independent exact checks and the response probe

`../../packages/interval_turn_sheet/verify_center_bellman.py` compares the
inverse-characteristic formulas with the independent exact running-CDF
capture engine. Its fixtures include independent a and u, negative c,
central waiting, incoming characteristics above one, and terminal returns
above one. The complete initial-endpoint formula and the lagging-side
dominance are checked separately.

`../../packages/interval_turn_sheet/probe_center_bellman.py` optimizes
continuous monster parameters for a piecewise-affine RankLaw. Its fixed
incoming-density breakpoints supply an exhaustive triangle count through
the earlier finite-response theorem and the merging argument in Section 5.
It searches that full class by default and independently recomputes every
reported route with the capture-record engine. The optimizer itself is
heuristic: a reported response is an actual adverse route, while its
reported minimum is not a certified global minimum. It cannot be used as
a substitute for (B1)-(B4) and (I0)-(I3).
