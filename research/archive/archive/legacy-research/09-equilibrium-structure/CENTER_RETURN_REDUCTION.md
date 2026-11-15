# A finite all-monster response reduction with central waiting mass

## 1. Princess class and finite density hypothesis

Let q be uniform in `(0,1)`. Assume `a(q),u(q)` are strictly increasing and
continuous, C(q) is strictly decreasing and continuous, and

    0 <= a(q) <= 1,      u(q) >= a(q),
    -a(q) <= C(q) <= 1.

Use the positive paths

    p_q(t)=min{1,max{min{a(q)+t,u(q)-t},t-C(q),0}},         (1)

and their reflections with equal probability. Unlike
`FINITE_MONSTER_RESPONSE.md`, this theorem permits `u(q)<C(q)` and hence
positive mass waiting at the center. Paths are strictly ordered at every
interior positive position; the only coalescence points are zero and the
endpoints. Every path is fixed at its signed endpoint from time two onward.

Define

    A(z)=Pr(a(q)<=z),   B(z)=Pr(u(q)<=z),   D(z)=Pr(C(q)>=z).

Assume B is absolutely continuous on `[0,1]`, with density b. Suppose a
fixed partition

    0=t_0<t_1<...<t_J<t_(J+1)=1

has the following property: on each open piece, every subinterval `[s,e]`
satisfies

    integral_s^e (s+2e-3v) b(v) dv >= 0.                 (K)

This is a condition on the specified princess law, independent of the
monster. Useful finite sufficient checks for a piece are:

* b is zero almost everywhere;
* `0<m<=b<=M<=4m` almost everywhere for fixed m,M;
* b is nonnegative and nonincreasing;
* b is nonnegative and concave.

For the density-ratio check, scale the interval to `[0,1]`. The coefficient
`2-3x` is positive on `[0,2/3]` and negative afterward, so

    integral_0^1 (2-3x)b(x) dx
      >= (2/3)m-(1/6)M >= 0.

For a nonincreasing density, its mean on any interval is at most the
midpoint, which is no farther right than `(s+2e)/3`. This proves (K).

For the concavity check, the centroid of a nonnegative concave function on
`[s,e]` lies no farther right than `(s+2e)/3`. One elementary proof decomposes
a piecewise-linear concave function into nonnegative endpoint-affine terms
and nonnegative tent functions. Each tent with vertex at r has centroid
`(s+r+e)/3<=(s+2e)/3`; the endpoint-affine terms have the same bound.
Piecewise-linear approximation proves the general concave case.

**Theorem.** For this law, the unrestricted monster-response infimum equals
the infimum over a finite-dimensional class consisting of:

1. an initial same-half unit-speed prefix, with at most two useful capture
   turns and, if needed, one terminal joining turn, ending either at zero
   or at an endpoint;
2. if it ends at zero, at most `J+3` zero-to-zero unit-speed triangles,
   separated by waits at zero;
3. a direct sweep from zero to one endpoint and then to the other, or a
   direct sweep from the already visited endpoint to the other.

Each triangle may choose either sign. Its two time parameters determine its
height. All these paths can be taken to finish by time six. Thus the theorem
gives finitely many direction words and finitely many real parameters; it
does not enumerate an infinite set of capture orders.

No equilibrium claim follows merely from membership in this class. A
proposed law must still attain the same constant as an unrestricted upper
strategy. The theorem makes its lower response check exhaustive.

## 2. Rank and the center peak

For `0<=x<1`, direct inversion of (1) gives the radial CDF

    R(t,x)=min{max{A(x-t),B(x+t)},D(t-x)}.                (2)

The inequality `C(q)>=-a(q)` implies `A(-v)<=D(v)`. Along any monster, the
characteristics `U=t+abs(m)` and `V=t-abs(m)` are nondecreasing. Therefore
the clamp in (2) has at most the three radial monotonicity phases

    decreasing -> increasing -> decreasing.

The central rank is `R(t,0)=min{B(t),D(t)}`. A is zero at nonpositive
arguments, up to irrelevant endpoint quantiles. Because B increases and D
decreases, choose a center-peak time `tau in [0,1]` such that

    B(t)<=D(t) for t<=tau,      B(t)>=D(t) for t>=tau.

Such a time exists since `B(0)=0` and `D(1)=0`. A flat equality interval
causes no difficulty; choose any point in it.

Here is the useful reachable-state fact. Any zero-to-zero path on `[s,e]`
satisfies

    s <= V(t) <= U(t) <= e.

If `e<=tau`, then `A(-V)=0` and

    D(V)>=D(e)>=B(e)>=B(U),

so its **entire reachable cone** has radial rank `R=B(U)`. This is not just
a property of the original path: it holds for every replacement bridge
between the same zero endpoints.

If `s>=tau`, the reverse comparison gives `R=D(V)<=D(s)`. At the initial
zero visit, both reflected prefixes through rank D(s) have already been
captured. Such a return excursion captures nothing new and may be replaced
by a wait at zero. At most one disjoint return excursion can straddle tau.

## 3. Canonical finite responses and triangular excursions

First take a finite even midpoint-quantile sample of (1) and its reflection.
The capture-order domination theorem supplies a unit-speed canonical
monster starting at a sampled path and turning only at new captures.

Before the first zero or endpoint visit, the monster remains in one open
half-interval. There the full signed CDF is either `(1+R)/2` or `(1-R)/2`.
Strict ordering at positive interior positions makes each new capture's
quantile label unambiguous. As the radial trace has at most two reversals,
the useful canonical prefix has at most two interior turns.

After a zero visit, the captured quantiles on each sign form an initial
radial interval. During an excursion into the positive side, all uncaptured
positive paths lie above the monster's captured frontier. A leftward
unit-speed leg cannot newly capture them: relative to each such 1-Lipschitz
path its displacement is nonincreasing. Negative paths cannot be captured
while the monster is positive. Thus after turning inward the canonical
monster cannot turn outward again before zero; no new capture would justify
that turn. Every complete zero-return excursion is therefore one triangle.
Reflect the argument for negative excursions.

There is also a direct normalization independent of canonical turn counting.
For a single same-half zero-return excursion on `[s,e]`, strictly away
from zero in its interior, the maximal capped tent
`min(t-s,e-t,1)` dominates its radius pointwise, so it catches every target
in that half no later. Opposite-side captures can occur only at the zero
junctions. If `e-s>=2`, the capped tent visits an endpoint, after which the
direct opposite sweep dominates the continuation. Thus any retained return
triangle before the first endpoint has length less than two. This covers
the possible triangle straddling the center peak as well.

After its last zero visit, direct outward travel to the endpoint of the
chosen side captures every princess met by the old same-half prefix no
later. The other side cannot be captured on that prefix. A subsequent
direct endpoint-to-endpoint sweep captures all survivors. Thus the final
part may be taken to be this straight completion.

Once either endpoint is reached, the straight sweep to the other is the
pointwise earliest possible capture of every remaining target. Accordingly
only excursions before the first endpoint need consideration.

## 4. Initial asymmetry costs only two exceptional triangles

At the first zero visit s, write `r_+,r_-` for the captured radial frontiers
on the two sides, and put `M=max(r_+,r_-)`. Both frontiers are at least
the current central rank. Suppose initially `r_+>=r_-`; reflect otherwise.

Consider all complete return triangles ending before tau and satisfying
`B(e)<=M`. Their reachable cones have `R=B(U)<=B(e)<=M`. They cannot capture
a new positive path, because that whole positive prefix was already
captured. A single maximal negative triangle spanning these excursions,

    m(t)=-min(t-s,e-t),

pointwise dominates every visit to the negative side and hence captures
every newly caught negative path no later. It reaches the same final zero
at time e. Its radius is at most one half, since `e<=tau<=1`, so it remains
inside the arena. Consequently all these pre-balance excursions merge into
at most one triangle. Earlier captured paths are unaffected.

At most one further return triangle has

    B(s)<M<B(e).

Keep this possible balance-crossing triangle. At its return, both captured
frontiers equal B(e), since the incoming reachable cone has no larger rank.
Every later zero visit before tau then has equal frontiers B(t). Equality
or flat intervals of B merely remove one of these exceptional cases.

## 5. Balanced returns and density breakpoints

Take a remaining return triangle `[s,e]` with equal captured frontiers B(s)
at its start and `e<=tau`. Each new radial label corresponds to an incoming
characteristic `v in (s,e]`. In the triangle's chosen half its capture time
is `(v+s)/2`; its reflection is caught at the return to zero at time e.
The paired average is therefore

    (v+s)/4+e/2.

Waiting at zero instead catches both paths at time v. The difference in
expected cost is exactly

    (1/4) integral_s^e (s+2e-3v)b(v)dv.                 (3)

Both choices have the same captured frontiers B(e) at the end, so there
is no unaccounted continuation cost. All older labels were already captured,
and the reachable cone contains no newer label above B(e).

If the triangle lies within one density piece, (K) permits replacing it
by waiting at zero. Every retained balanced triangle must therefore contain
one of the J fixed partition breakpoints in its half-open interval `(s,e]`.
These intervals are disjoint, so at most J such triangles remain.

Adding the at most one pre-balance triangle, one balance-crossing triangle,
and one triangle straddling tau gives the asserted bound `J+3`. Excursions
after tau capture nothing new and have already been removed.

## 6. Continuum transfer and the finite parameter domain

The preceding canonical argument is applied to finite quantile samples,
but the replacements in Sections 4-5 are evaluated under the original
continuum law and its density b. They do not require a density condition
for the atomic empirical approximation.

Every selected princess is fixed at an endpoint by time two. A canonical
monster can have no new interior capture after time two; hence its next
endpoint visit is by time four, and the final opposite sweep finishes by
six. If all selected paths were captured earlier, append the endpoint
sweeps. Its last zero visit is by time three. The replacements above keep
zero-visit times or complete earlier, so their endpoint completion is also
by six.

For any original monster m, extend it after time six if necessary to capture
every sampled path. Canonical domination then supplies a completed m_n whose
empirical full payoff is at most the empirical payoff of m truncated at six.
Indeed, each sampled capture time of m_n is at most its capture time against
the extended monster, and the preceding endpoint argument separately makes
it at most six. If the original capture is before six it is unchanged by
extension; otherwise the second bound applies. Thus, pointwise on every
sampled path,

    T(m_n,p_i) <= min{T(m,p_i),6}.

The midpoint-quantile discrepancy is uniformly at most `6/n`. The
continuum-law replacements produce a path b_n in the stated finite class
with `J(b_n)<=J(m_n)`. Therefore

    inf_b J(b) <= J(b_n) <= J(m_n)
      <= J_{6,n}(m_n)+6/n
      <= J_{6,n}(m)+6/n
      <= J_6(m)+12/n
      <= J(m)+12/n.

Let even n tend to infinity. Inclusion gives the opposite inequality, so
the finite-class and unrestricted response infima coincide.

For a concrete finite parameterization, use the starting position and up to
three initial turn positions (two capture turns and an optional terminal
joining turn), then the `J+3` disjoint triangle intervals in
`[0,3]`, their finitely many sign choices, the intervening waits at zero,
and the final endpoint choice. Include the no-zero case separately. Zero
length triangles and coincident turns can be included to close the domains.
Every trajectory is explicit and has a common capture horizon of six.

## 7. Exact scope

This theorem allows central waiting atoms; it does not infer a turn bound
from the number of radial rank phases alone. Atomic incoming shells can
make arbitrarily many return triangles useful, so the finite density
partition is essential. It must be proved for the proposed law, with all
breakpoints stated. Incoming parameter atoms can be regularized in a
candidate family, but no passage to a singular lower limit is justified by
this theorem alone.

The next equilibrium step is to choose an actual law satisfying these
hypotheses and prove that its finite-dimensional monster minimum matches
an unrestricted upper guarantee. A failure of that matching step must not
be described as a closed proof of the original game.
