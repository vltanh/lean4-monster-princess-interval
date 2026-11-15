# Free-turn variation and a late-wave support equation

## 1. Scope

This note derives an exact variation identity for monster turning points.
It gives necessary support equations for an equilibrium candidate, beyond
indifference within the old M1/M2 parameter families. It does not identify
an equilibrium or assume that a one-turn monster family is globally sufficient.

Let a princess law choose a random path p in [0,1], then choose its sign
fairly. Every p is 1-Lipschitz and is fixed at 1 from time two onward.
Ordering of the paths is not required for Sections 2-4.

Write

    a=p(0),  A(z)=Pr(a<z),
    alpha_p(z)=inf{t:t+p(t)>=z},
    beta_p(z)=inf{t:t-p(t)>=z}.

Fix 0<z<1 and assume Pr(a=z)=0. This removes only an initial-capture
atom from the formulas; a candidate with such an atom must retain its
zero capture contribution separately.

For 1<s<2+z, define the monster M(s,-z) by the vertices

    (0,-z), ((s+z)/2,(s-z)/2), (s+1,-1), (s+3,1).

It moves right, turns at the displayed positive interior point, and
then visits both endpoints. Put

    tau=(s+z)/2,  y=(s-z)/2,
    R(s,z)=Pr(p(tau)<=y)=Pr(beta_p(z)<=tau).

For a fixed z, R is the distribution function of twice beta_p(z) minus
z. In particular, it is nondecreasing and right-continuous in s, including
any atoms. The old negative-start M2 path is the boundary choice s=1.

## 2. Exact payoff formula

Let C(s,z) be the expected capture time of M(s,-z) against the symmetric
princess law. Then

    2 C(s,z)
      = (s+1)(1-A(z))
        + E[alpha_p(z) 1_{a<z}]
        + E[beta_p(z) 1_{beta_p(z)<=tau}]
        + (s+3)(1-R(s,z)).                              (1)

To verify the four terms, first consider a reflected princess -p.
If a<z, the monster starts to her left and catches her on its first
rightward leg at alpha_p(z)<=z<tau. If a>z, it starts to her right and
cannot meet her on that leg. Its leftward leg has characteristic t+m=s.
The endpoint assumption and the speed bound give p(t)>=t-1 for t<=2.
Thus t-p(t)<=1 before time two. For s>1, the first meeting with -p
is therefore the left endpoint at time s+1.

An unreflected p starts to the right of the monster. It is captured on
the first leg exactly when beta_p(z)<=tau. If that capture fails, the
following leftward leg cannot catch it: after the turn the monster is
below p, and its relative position cannot increase while moving left
at unit speed. On the last rightward leg p is already fixed at 1, so
capture is at s+3. These observations prove (1), including capture at
the first turning point.

The possible s=1 boundary is substantive. A princess with a final
outward segment t-p(t)=1 can be caught before time two when s=1, whereas
every s>1 catches its negative reflection at s+1. Formula (1) applies
at s=1 only when the negative paths in question have no such earlier
first-inverse plateau. It always describes the right-hand limit at one.

## 3. An exact Stieltjes variation identity

For fixed z, the payoff in (1) has bounded variation in s and satisfies

    dC(s,z)
      = (2-A(z)-R(s,z))/2 ds
        - (6+s-z)/4 dR(s,z).                            (2)

Equivalently, for 1<s0<s1<2+z,

    C(s1,z)-C(s0,z)
      = (1/2) integral_s0^s1 (2-A(z)-R(u,z)) du
        - (1/4) integral_(s0,s1] (6+u-z) dR(u,z).       (3)

Here the Stieltjes integral includes atoms. At a jump of R, exactly
the newly captured positive mass changes from the late endpoint time
s+3 to the first-turn time tau. Its contribution to the pair payoff
jumps by -(6+s-z) Delta R/4, agreeing with (2).

For the continuous part, differentiate (1): increasing s delays each
negative late capture and each positive late capture at unit rate. A
new positive early capture has beta_p(z)=tau, so the boundary term is
`(tau-(s+3)) dR/2`. This gives (2). Alternatively, integration by parts
in the distribution function of beta_p(z) proves (3) directly and
does not require a density.

Formula (3) is a global comparison for any two turn characteristics
with the same starting point. It can be checked without differentiating
the princess trajectories or making a generic-position assumption.

## 4. Necessary local and interval indifference equations

Where R is differentiable in s,

    C_s = (2-A-R)/2 - (6+s-z) R_s/4.                    (4)

An interior locally optimal monster turn must have C_s=0. Therefore

    (6+s-z) R_s(s,z)=2(2-A(z)-R(s,z)).                  (5)

If all s in an interval are indifferent for this fixed z, the equation
integrates explicitly:

    R(s,z)=2-A(z)-K(z)/(6+s-z)^2.                        (6)

In particular, the corresponding incoming density is proportional to
the inverse cube of 6+s-z. This is a necessary equation for such an
indifference interval, not a prescription that every active support
contains an interval at a fixed start.

## 5. A single incoming wave

For the ordered multi-leg laws, there are regions of characteristic
space on which the radial CDF is exactly one incoming CDF B(s),
independent of z. On such a region put b=B'. Equations (4)-(5) become

    C_s=(2-A(z)-B(s))/2-(6+s-z)b(s)/4,
    (6+s-z)b(s)=2(2-A(z)-B(s)).                         (7)

Where b is differentiable,

    C_ss=-(3b(s)+(6+s-z)b'(s))/4.                       (8)

Consequently a positive constant incoming density makes the payoff
strictly concave as a function of the turn characteristic. A minimizing
monster cannot have an interior turn optimum in such a region. It must
use a region boundary or a different CDF branch. More generally, an
interior local minimum requires

    b'(s)<=-3b(s)/(6+s-z).                              (9)

This explains why a narrow uniform late-arrival layer is vulnerable at
one of its edges. A genuine smooth interior turn support requires a
sufficiently decreasing incoming density.

If a straight characteristic s=s0 is active for a whole open interval
of starting parameters z, (7) forces

    A'(z)=b(s0)/2.                                     (10)

Thus the initial radial distribution must be uniform on that interval.
A nontrivial open two-dimensional region of indifferent turns is
impossible inside one incoming branch. Indeed, (10) throughout such a
region first forces b to be constant; differentiating (7) in s then
forces b=0 and A+B=2, the degenerate case with no relevant remaining
mass. Any nontrivial continuum support inside the branch must therefore
be confined to lower-dimensional sets, such as curves.

## 6. The fixed-time-one turning curve

The additional family Q_eta has vertices

    (0,-1+eta), (1,eta), (2+eta,-1), (4+eta,1).

It corresponds to z=1-eta and s=1+eta=2-z. If this curve is an active
interior monster support inside one incoming branch, free-s stationarity
gives

    (s+2)B'(s)+B(s)=2-A(2-s),
    d[(s+2)B(s)]/ds=2-A(2-s).                          (11)

Thus its necessary late-wave profile is determined by the initial
radial CDF, up to one integration constant. For example, if

    A(z)=alpha+beta*z,

on the relevant start interval, then

    B(s)=[K+(2-alpha-2 beta)s+(beta/2)s^2]/(s+2).        (12)

The density must also be nonnegative and satisfy the CDF range and
branch conditions. Local minimum curvature imposes a further check.
Differentiate (11), or differentiate C_s along s=2-z, to obtain

    C_ss=(b(2-z)-2A'(z))/4.

Hence a necessary condition is

    b(2-z)>=2A'(z).                                    (13)

Equations (11)-(13) test a fixed-time turning support against nearby
unrestricted turn locations. Indifference only along the Q_eta curve
would not imply these equations: the monster must also resist a turn
perturbation transverse to the curve.

## 7. What remains to form a saddle

The free-turn identities provide a concrete candidate-shape constraint:
late incoming densities, initial radial densities, and active monster
turn curves cannot be chosen independently. They do not supply the
princess best-response conditions against a proposed monster mixture,
the other monster start variations, or the global all-monster lower
inequality. Those obligations remain in addition to (3) and (11).
