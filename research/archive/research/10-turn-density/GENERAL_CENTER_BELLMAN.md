# Center verification for curved ordered princess laws

The ordinary-wave center state loses information when a low-rank path
leaves the center slowly. At a later center visit, that path may be absent
from the center but still available for a new interior capture. This note
retains both captured frontiers and gives exact Bellman inequalities for
that case. Concavity reduces their frontier verification to finitely many
vertices of a polyhedral potential.

The result certifies arbitrary continuations after a center visit. A
potential satisfying the required initial-prefix inequalities for the
proposed equilibrium has not yet been constructed. This is not a claim
that the unrestricted game has been solved.

## 1. Ordered law and the safe terminal time

Let q be uniform on (0,1), let p_q(t) in [0,1] be ordered nondecreasingly
in q, and give p_q and -p_q equal probability. Every path is 1-Lipschitz.
Assume each p_q is fixed at +1 from some absorption time sigma_q<=2.
For the candidate-focused horizon-one statement, assume additionally

    Pr(sigma_q=2)=0.                                      (H)

For a family whose final outward characteristic is c(q), with a final
unit-speed leg, (H) is exactly the no-mass condition c(q)<1 almost surely.
Stationary endpoint atoms are permitted; they have sigma=0.

Write the closed radial CDF in characteristics as

    R(U,V)=Pr(p_q((U+V)/2)<=(U-V)/2),
    Z(t)=R(t,t).

At the endpoint use the actual closed value

    R(t+2,t)=1,                                           (1)

not its interior limit. Interior transport gives R increasing in U and
decreasing in V.

**Terminal lemma.** Under (H), after any center visit e>=1, no previously
uncaught path can be captured in the interior. Only the two endpoint
visits matter.

Indeed, for sigma_q<2 and s<=sigma_q, Lipschitz speed gives

    p_q(s)>=1-(sigma_q-s)>s-1.

A monster departing the center at e>=1 has radius at most s-e<=s-1.
After sigma_q the princess is at the endpoint. This proves the claim up to
a null set of ranks. It does not require ordinary center waiting or any
post-return saturation of the curved CDF.

With captured radial frontiers r_+,r_-, the remaining absolute capture
contribution is therefore

    E(e,r_+,r_-)
      =(e+2)*(1-(r_++r_-)/2)-abs(r_+-r_-)/2.              (2)

The smaller captured frontier is visited first.

Without (H), the claim is universally true for e>1 but can fail at e=1.
A path may join the ray p(s)=s-1 after time one without having been at
center at time one. A completely general atomic version can use center
horizon two and terminal cost (2) there; all action and concavity formulas
below remain unchanged. The horizon-one version does not silently discard
an exact-time-two absorption atom.

## 2. The complete center state

After a center visit, the captured ranks on each sign are prefixes. Write
their endpoints as r_+,r_-. The state is

    (t,r_+,r_-),    r_+,r_->=Z(t).                         (3)

The two frontiers can be different and neither is replaced by Z(t) later.
In particular, an outward capture need not reach the center before the
monster returns. Its rank remains in the appropriate captured frontier.

For a fixed departing time t, define the row inverse

    kappa_t(q)=inf{U in [t,t+2]:R(U,t)>=q}.                (4)

It exists by the endpoint convention (1). A unit-speed outward monster
captures rank q at time (t+kappa_t(q))/2. Closed traces in (4) retain
incoming coalescence and exact endpoint captures.

For an outward leg ending at characteristic U=e, put rho=R(e,t). The
absolute contribution of newly caught ranks above an old frontier r is

    O(t,e;r)
      =1/4 integral_r^{max(r,rho)} (t+kappa_t(q))dq
      =[(t+e)*(rho-r)_+
         -integral_t^e (R(U,t)-r)_+ dU]/4.                (5)

The second equality is the layer-cake identity for the monotone row
inverse. It is often preferable for exact CDF computations. It remains
valid at jumps: the first term uses the closed value rho, while the
integral has no artificial endpoint mass.

## 3. Exact triangle and wait actions

Take a triangle into the positive half, leaving center at t and returning
at e, with

    t<=e<=t+2.

The outward turn occurs at time (t+e)/2 and radius (e-t)/2. Put

    rho=R(e,t),    z=Z(e).

Its immediate absolute capture contribution and new state are

    K_+(t,e;r_+,r_-)=O(t,e;r_+)+e/2*(z-r_-)_+,           (6)
    r_+'=max(r_+,rho),    r_-'=max(r_-,z).                (7)

For a negative triangle interchange the two signs. Formula (7) is the
essential correction to an ordinary-wave collapse: the opposite sign
acquires only the center rank z, not the entire outgoing rank rho.
Transport gives rho>=z, so every center capture on the outgoing side was
already included in its outward leg.

At e=t+2 the turn is an actual endpoint visit. Because rho=1, (6)-(7)
followed by (2) give exactly the direct endpoint sweep. No separate
limiting interpretation is needed. Its cost can also be written

    S_+(t;r_+,r_-)
      =O(t,t+2;r_+)+(t+3)/2*(1-r_-).                    (8)

The other sign is obtained by reflection. Unlike the ordinary two-state
case, both signs must be checked in the general Bellman inequality.

### Waiting at center

For a wait on [t,e], define the running center record

    Z_t^*(s)=sup_{v in [t,s]} Z(v).

The supremum includes exact center contacts. It cannot be replaced by
Z(s), which may decrease after a center peak. For either old frontier r,
put d=max(r,Z_t^*(e)). Its newly captured contribution is

    W_side(t,e;r)
      =[e*(d-r)-integral_t^e (Z_t^*(s)-r)_+ ds]/2.        (9)

The total wait contribution is the sum of (9) for the two signs, and the
new frontiers are max(r_+,Z_t^*(e)) and max(r_-,Z_t^*(e)). This handles
several incoming waves and center atoms without assuming a single peak.

## 4. Three-state center Bellman theorem

Let P(t,r_+,r_-) be a bounded verification potential on

    0<=t<=1,    Z(t)<=r_+,r_-<=1.

It is a lower bound for the absolute contribution of paths still uncaught
in the state (3). Require:

1. For each sign and t<=e<=1,

       P(t,r_+,r_-) <= K_sign(t,e;r_+,r_-)
                       +P(e,r_+',r_-').                 (B1)

2. For each sign and 1<=e<=t+2,

       P(t,r_+,r_-) <= K_sign(t,e;r_+,r_-)
                       +E(e,r_+',r_-').                 (B2)

3. For every center wait t<=e<=1,

       P(t,r_+,r_-) <= W(t,e;r_+,r_-)
                       +P(e,d_+,d_-).                  (B3)

4. At the terminal center time,

       P(1,r_+,r_-) <= E(1,r_+,r_-).                    (B4)

Here the updates and immediate costs are exactly (6)-(9). Direct endpoint
completion is already present in (B2) through e=t+2.

**Theorem.** Under (H) and (B1)-(B4), every unrestricted Lipschitz monster
continuation from the center state (3) has remaining expected absolute
capture contribution at least P(t,r_+,r_-).

For a finite canonical continuation, every same-half excursion between
zero visits can be replaced by the maximal tent between those visits.
It catches every target in that half no later; targets of the opposite
sign can be caught only at center junctions. A tent touching an endpoint
ends the need for further interior excursions, since the direct opposite
sweep is the earliest possible capture of all remaining targets. Thus
the continuation consists of waits and the triangles above. Apply (B1)
and (B3) successively and telescope the immediate captured contributions;
use (B2) or (B4) for its completion.

For an arbitrary continuation, take finite ordered quantile samples of the
remaining tails. The fixed-start version of capture-order domination is
obtained by chasing each next uncaught target at maximum speed. Earlier
arrival cannot invalidate the original capture deadline: the monster
could follow that target to the old arrival time and then resume the old
route. Canonical paths therefore capture each sampled target no later.
The endpoint-by-two completion gives the same finite horizon used in the
existing quantile-discrepancy argument. Apply the continuum action
inequalities to these finite canonical routes, then let the uniform
quantile discrepancy tend to zero. This proves the unrestricted result
without taking a favorable limit of singular capture times and without
postulating a monster turn bound.

## 5. Joint concavity and finite frontier vertices

For a fixed future route starting at center, first future capture times on
either sign are nondecreasing in radial rank. The route's remaining cost
is therefore jointly concave in (r_+,r_-): it is the sum of two terms

    1/2 integral_r^1 T_q dq.

Every partial slope is at most -t/2. Taking the infimum over routes
preserves joint concavity. This motivates a concave polyhedral P in the
two frontier coordinates.

Assume that, for each t, P(t,.,.) is concave and polyhedral, and each
partial slope is at most -t/2. Then every right side of (B1)-(B3) is jointly
concave in the current frontiers. The following elementary extension
lemma proves this, including all clipping boundaries.

Write a future concave polyhedral function as the minimum of its affine
planes. A plane has coefficients a_+,a_-<=-e/2. For one coordinate clipped
upward at a captured rank b, the plane plus its immediate capture
contribution becomes

    a*max(r,b)+1/2 integral_r^{max(r,b)} h(q)dq,           (10)

where h(q) is the absolute capture time of the newly acquired rank. The
function h is nondecreasing and at most e. Below b, the derivative of
(10) is -h(r)/2; above b it is a. Thus the derivative is nonincreasing,
including its downward jump at b. Formula (10) is concave. Sum the two
coordinate terms and take the minimum over affine planes to obtain joint
concavity.

For a triangle, h is the outward first-hit time on its chosen side and the
constant e on the other side. For a center wait, h is the first time the
running center record reaches q. All are at most e. The endpoint function
E is itself the minimum of two affine planes with coefficients
-(e+1)/2 and -(e+3)/2, so the same lemma proves the assertion for (B2).

Consequently, on every convex polygonal cell where the current P is
affine, it is sufficient to check a Bellman inequality at the cell's
vertices. For any convex combination of those vertices, the concave right
side is at least the same combination of its vertex values, while the
left side equals that combination exactly.

This leaves finitely many vertex families, the two continuous variables
t,e, and the two discrete triangle signs. The vertices include the moving
domain boundaries r_+=Z(t) and r_-=Z(t). Concavity and the partial-slope
bounds are additional finite conditions on the potential's planes.
These checks interpolate a verification potential; they do not replace
the princess continuum by finitely many paths.

## 6. Initial attachment and remaining work

Let an initial monster prefix first reach center at time t, let G be its
absolute contribution from paths already captured, and let r_+,r_- be
the two actual captured frontiers. To obtain a global lower guarantee h,
the remaining initial obligation is

    G+P(t,r_+,r_-)>=h       for t<=1,
    G+E(t,r_+,r_-)>=h       for t>=1,

together with prefixes reaching an endpoint first. For an ordinary wave,
`CENTER_BELLMAN_CERTIFICATE.md` reduces this to explicit finite initial
families. For a curved ordered field, that initial-prefix reduction must
be proved separately or replaced by a verification potential before the
first center visit. It is not supplied by the center theorem.

The intended use for the separated curved candidate is to construct a
polyhedral frontier potential with a finite set of contact vertices,
prove the two-variable inequalities above, and attach its free initial
starts. No such completed potential has yet been instantiated.

## 7. Exact independent fixtures

Run from the repository root:

```sh
python packages/interval_turn_sheet/verify_general_center.py
```

The verifier performs **1,056 exact Fraction checks** against the
independent continuous capture-record engine:

| Check | Count |
|---|---:|
| Direct endpoint sweeps | 64 |
| Terminal triangles | 256 |
| Early triangle followed by another triangle | 128 |
| Center waits with the running center record | 64 |
| Both updated captured frontiers | 448 |
| Joint-concavity comparisons across clipping boundaries | 96 |

Fixtures include inward and outward speeds 1/2, 2/3, and 3/4, multiple
incoming waves, and stationary endpoint atoms. One explicit slow-outward
fixture has

    R(3/5,3/5)=0 < R(4/5,3/5),

so it has a new interior capture after a center return with no center
mass. This is precisely the case that invalidates an ordinary-wave
post-return saturation argument. Terminal endpoint turns use the closed
CDF value one and are checked against direct capture, not an interior
limit. The tests establish the implemented action identities and
concavity comparisons; they are not an instantiated equilibrium
certificate.
