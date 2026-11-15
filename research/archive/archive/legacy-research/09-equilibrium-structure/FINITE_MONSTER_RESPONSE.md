# A finite monster-response theorem for separated ordered three-leg laws

## Scope

This is an exact all-monster response reduction for a specified princess
class. It is not a proof that an optimal princess law belongs to that class,
and no matching equilibrium is asserted. Its separation hypothesis is
substantive: it excludes the central waiting atom in the previous failed
candidate, as well as the stationary-shell counterexamples.

Write `q` for a uniform parameter in `(0,1)`. Let `a(q),u(q)` be strictly
increasing continuous functions and let `C(q)` be strictly decreasing and
continuous. Assume

    0 <= a(q) <= 1,
    u(q) >= a(q),
    -a(q) <= C(q) <= 1,
    u(q) >= C(r) for every q,r in (0,1).                 (S)

Define the positive princess paths by

    p_q(t) = min{1, max{min{a(q)+t,u(q)-t},t-C(q),0}}.    (1)

Choose `p_q` or `-p_q` with equal probability. Formula (1) is 1-Lipschitz,
has initial value a(q), and reaches the signed endpoint by time two.
The strict parameter monotonicity implies that the positive paths are
strictly ordered whenever their positions lie strictly between zero and
one. Condition (S) implies that there is no positive-mass atom at zero:
an interior quantile could be at zero only if `u(q)<=t<=C(q)`.

If equality in (S) occurs at the extreme parameter values, a single limiting
quantile can touch zero. It has measure zero and is not used in the finite
midpoint-quantile approximation below.

**Theorem.** The best monster response to this law can be found among
unit-speed paths with at most two useful interior turns before their first
endpoint visit, followed by a direct sweep to the opposite endpoint. In
particular, its exact response is a finite-dimensional optimization over
the starting position, at most two turn positions, and the choice of first
endpoint. The first endpoint need not be prescribed in advance.

This is a statement about the infimum against every legal monster path,
including paths with arbitrarily many turns. It does not restrict the
monster by assumption.

## 1. The radial rank has at most two reversals

For `0<=x<1`, let `R(t,x)=Pr(p_q(t)<=x)`. Set

    A(z)=Pr(a(q)<=z),
    B(z)=Pr(u(q)<=z),
    D(z)=Pr(C(q)>=z).

The prefix sets in q are nested, because a and u increase and C decreases.
Directly from (1),

    R(t,x)=min{max{A(x-t),B(x+t)},D(t-x)}.               (2)

The inequality `C(q)>=-a(q)` gives `A(-v)<=D(v)` for every v. Thus (2)
is a clamp of B between A and D.

For any 1-Lipschitz monster m, its absolute-value path is also 1-Lipschitz.
Both characteristics

    U(t)=t+abs(m(t)),     V(t)=t-abs(m(t))

are nondecreasing. Hence `A(-V)` and `D(V)` are nonincreasing, while B(U)
is nondecreasing. B(U) crosses each decreasing bound at most once; because
the lower bound A is no larger than the upper bound D, the crossings occur
in that order. Consequently

    r(t)=R(t,abs(m(t)))

has at most three consecutive monotone phases:

    nonincreasing -> nondecreasing -> nonincreasing.     (3)

This holds on the whole prefix before the first endpoint, even if the
monster changes sign. It is not a separate assertion for each excursion.

## 2. Passing from radial rank to signed quantile rank

Away from the endpoints, the full symmetric CDF at the monster is

    F(t,m(t)) = (1 + sign(m(t))*r(t))/2,                 (4)

with value one half at m=0. Condition (S) is used here: `R(t,0)=0`, so
there is no missing central atom or interval of quantile labels in (4).

On an interval where r is monotone and nonnegative, its nonzero set is an
interval. The sign of m is constant on that nonzero set, since changing sign
requires passing through m=0, where r=0. Thus `sign(m)*r` is monotone on each
of the at most three phases in (3). It may have a different direction from
r, but it acquires no extra monotone phase. Therefore the full quantile
rank in (4) has at most two reversals before the first endpoint.

This is the key distinction from an arbitrary ordered flow: spatial
ordering alone does not bound rank reversals along a monster.

## 3. Finite quantile laws and canonical capture order

First choose finitely many positive quantile levels strictly inside `(0,1)`
and include their reflected paths. The capture-order domination theorem in
`research/07-structural-audit/CAPTURE_ORDER.md` permits a canonical monster
starting at one of these paths and moving at unit speed, turning only at a
new capture. It captures every selected path no later than any proposed
monster. Consecutive legs in the same direction are combined.

Before the first endpoint visit, the selected paths are strictly ordered
whenever they meet the monster. A rightward unit-speed leg captures increasing
quantile labels: relative to every 1-Lipschitz princess, the monster's signed
displacement is nondecreasing. A leftward leg captures decreasing labels.
Every useful turn therefore produces a reversal in the sequence of newly
captured quantile ranks. Since the rank trace has at most two reversals, the
canonical monster has at most two useful interior turns before an endpoint.

Once the monster reaches either endpoint, all remaining princesses are on
its opposite side. A direct unit-speed sweep to the other endpoint captures
them no later than any continuation: every remaining first capture requires
the corresponding change of side. Equivalently, starting from an endpoint,
the straight sweep is the pointwise earliest intersection with every
1-Lipschitz target. Thus no further interior turn is needed.

If all selected paths are captured before an endpoint is visited, append
a visit to an endpoint in the current direction and then sweep to the other.
The added motion changes none of their capture times. At most two prior
interior turns are still sufficient.

## 4. Transfer to the continuum law

Let B be the class just described, allowing zero-length legs and using no
more than two interior turn positions before the final endpoint sweep.
Every path in B visits both endpoints by time eight: at most three
pre-endpoint legs each have length at most two, followed by a length-two
sweep. Consequently it captures every continuous princess by time eight.

Approximate the full symmetric law by its equal-weight midpoint quantile
law with an even number n of paths. This avoids the single label one half
at the gap between the positive and negative supports. The quantile
discrepancy theorem gives, uniformly for
every monster,

    |J_8(m)-J_{8,n}(m)| <= 8/n,                         (5)

where the subscript eight denotes capture time truncated at eight. For any
unrestricted monster m, first extend it after time eight to capture all
sampled paths if necessary. Apply finite capture-order domination and the
preceding shape reduction to this completed path. The resulting `m_n in B`
captures each sampled path no later than the completion and also by time
eight. Hence `J_{8,n}(m_n)<=J_{8,n}(m)`. Since m_n visits both endpoints by eight,
its full payoff equals its truncated payoff. Therefore

    inf_{b in B} J(b) <= J(m_n)
      <= J_{8,n}(m_n)+8/n
      <= J_{8,n}(m)+8/n
      <= J_8(m)+16/n
      <= J(m)+16/n.

Let n tend to infinity and then take the infimum over m. The reverse
inequality follows from inclusion of B in the legal monster class. This
proves equality of the unrestricted and finite-parameter response infima.

One can also obtain attainment within B: its finitely many direction words
are parameterized by closed bounded position domains, the associated paths
depend continuously on those parameters, and first capture is lower
semicontinuous. Fatou then makes the expected payoff lower semicontinuous.
The compact parameter domains therefore contain a minimizer. Attainment
is not needed for the preceding equality argument.

## 5. What remains to make this an equilibrium theorem

The theorem controls every monster against a member of the specified class.
It does not show that the class has an optimal unrestricted princess law.
The separation condition `inf u >= sup C` and strict ordering must be
checked for any proposed application; a positive central waiting atom
invalidates the rank-zero argument in Section 2.

To close the original game by this route one still needs a law of this class
whose finite-parameter minimum agrees exactly with a verified unrestricted
monster upper guarantee. The role of the theorem is to make that matching
lower check globally exhaustive once such a law is proposed.
