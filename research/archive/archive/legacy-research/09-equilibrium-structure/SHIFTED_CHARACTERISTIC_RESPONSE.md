# Exact response formulas for a shifted sweeper characteristic

## 1. The two-parameter monster family

For

    -1<=x<=1,    |x|<=b<=2-x,

define M2(x,b) by

    x+t          until t=(b-x)/2,
    b-t          until t=b+1,
    t-(b+2)      until t=b+3,
    1            afterward.

Its first turn is at `((b-x)/2,(b+x)/2)`, followed by visits to -1
and +1. The parameter restrictions are exactly the nonnegative-time and
nonnegative-turn-position restrictions, with that turn inside [0,1].
They imply 0<=b<=3. The family used previously is b=1.

Let p be a nonnegative admissible princess path and put

    a=p(0), U=t+p(t), V=t-p(t),
    A(z)=inf{t:U(t)>=z}, B(z)=inf{t:V(t)>=z}.

Define the right endpoint of the U=b plateau by

    e_b=inf{t:U(t)>b},    x_b=b-2e_b.

When a<=b, continuity gives U(e_b)=b and the speed bound gives x_b<=a.
When a>b, one instead has e_b=0 and U(e_b)>b; this case must be kept
separate. The first-inverse convention and the right-end plateau convention
are both essential below.

## 2. Individual first-capture times

If a<=b, the unreflected capture is

    T(M2(x,b),p) = B(b+2)    if x<x_b,
                    B(-x)     if x_b<=x<a,
                    0         if x=a,
                    A(b)      if x>a.                   (1)

For every a, the reflected capture is

    T(-M2(x,b),p) = A(-x)    if x<-a,
                     0        if x=-a,
                     B(b)     if x>-a.                 (2)

If a>b, every feasible x satisfies `-a<x<a`, and the captures are instead

    T(M2(x,b),p)=B(b+2),
    T(-M2(x,b),p)=B(b).                                (3)

Indeed U(t)>=a>b, so no first-leg or descending-leg unreflected capture
is possible. In particular, x=b<a has a zero-length first leg and must
not be put into the early equality branch of (1). Using e_b=0 blindly
would make exactly that mistake.

To prove (1) when x<a and a<=b, let tau=(b-x)/2 be the first turning time.
Capture on the first leg occurs exactly when

    B(-x)<=tau,                                        (4)

equivalently `U(tau)<=b`, or `tau<=e_b`, or `x>=x_b`.
Equality belongs to this early branch. If that condition fails, U>b
after the turn, so the descending leg b-t cannot capture p. The final
ascending leg gives B(b+2).

If x>a, the monster starts above p and its first outward leg cannot
capture it. At the turn,

    U(tau)<=a+b-x<b,

so the descending leg first captures at A(b). For (2), the reflected
first turn is nonpositive because b+x>=0. A princess starting below
the reflected monster is therefore caught on its initial leftward leg
at A(-x); otherwise the middle rightward leg catches at B(b).

The primitive early test (4) is valid even when a>b; it then always fails.
The formulas remain valid for parameter atoms and starting coincidences.
They can be integrated directly against a joint measure in (x,b). The
cutoff x_b depends on the princess path at each b, so a continuum of b
values does not reduce to one frozen scalar cutoff.

## 3. The common-time-one turn curve Q_eta

Set `b=1+eta`, `x=-1+eta`, with `0<eta<1`. Then M2(x,b) has
successive vertices

    (0,-1+eta), (1,eta), (2+eta,-1), (4+eta,1).

Write Q_eta for its reflected pair and d=p(1). Its unreflected capture
is determined solely by the time-one position:

    B(1-eta)    if d<=eta,
    B(3+eta)    if d>eta.                               (5)

The first case includes capture exactly at the turn. Its reflected
capture is

    A(1-eta)    if a<1-eta,
    0           if a=1-eta,
    B(1+eta)    if a>1-eta.                             (6)

These exact identities strengthen a bound using only the two marginals.
They also show which early inverse is shared with a near-endpoint M1
attacker, without discarding initial or turning equality cases.

## 4. An exact separable functional for a Q density

Suppose the Q pair parameter has density w(eta) on (0,1). For fixed
a=p(0) and d=p(1), equations (5)-(6) give

    2 J_Q(p)
      = integral_d^1 B(1-eta) w(eta) deta
        + integral_0^d B(3+eta) w(eta) deta
        + integral_0^(1-a) A(1-eta) w(eta) deta
        + integral_(1-a)^1 B(1+eta) w(eta) deta.         (7)

For an atomic Q measure, the first integral includes eta=d, the second
excludes it, and both reflected integrals exclude eta=1-a, whose capture
is zero. Formula (7) is written for a density so these endpoints have
zero measure.

After changing variables, the added alpha-threshold density is

    w(1-U)       on a<U<1,

and the added beta-threshold densities are

    w(1-V)       on 0<V<1-d,
    w(V-1)       on 2-a<V<2,
    w(V-3)       on 3<V<3+d.                            (8)

Thus, with a and d fixed, this is again a separable characteristic
functional. The constraints fixing those parameters must still be kept,
especially the time-one point

    (U,V)=(1+d,1-d).

If a common M2 cutoff c is also fixed, then c<=1-d. Removing this
time-one constraint while retaining the density cutoffs in (8) would
optimize a different problem.

## 5. How the Q curve can distribute a later inward characteristic

In a law with positive M1 density f, a common b=1 M2 component, and a
Q component but no interior negative M1 component, fix a,c,d. After
time one, all early Q beta thresholds in (8) have been crossed. The
remaining threshold strip

    1-d < V < 1

has no beta mass. In comparison with the outward suffix starting at time
one, an inward leg just after time one, on
`U=1+d+epsilon`, can raise V from 1-d toward one without advancing
any supporting beta capture. It delays the positive M1 alpha thresholds
above 1+d.

The limiting gain from raising V to one from below is

    d/4 * integral_a^(1-d) f(x) dx                      (9)

when a<1-d; the integral is zero otherwise. This follows directly from
the capture delay d/2 and reflection probability one half.

Consequently the Q extension naturally permits a later incoming
characteristic `A_2=1+d`, varying with the time-one rank. This differs
from filling the original positive beta strip with negative M1 density,
which instead prices the endpoint y of an inward leg near U=1 through
`(1+y)ell(y)=Fbar(a)`. Both mechanisms have exact response formulas;
neither formula alone proves that its support contains an equilibrium.
