# From a rational ordered law to finitely many exact quadratic programs

## 1. Statement and scope

Fix a symmetric ordered multi-leg princess law satisfying the hypotheses of
`MULTI_LEG_FINITE_RESPONSE.md`. Suppose its parameter functions

    a(q), A_1(q),...,A_k(q), C_1(q),...,C_k(q)

are continuous, rational piecewise-affine functions of the uniform quantile
`q in [0,1]`, on a finite rational partition. Their slopes satisfy the strict
ordering conditions of that theorem. The inequalities between parameter
functions hold on every piece and can be checked at its endpoints.

The incoming CDF I_j is then piecewise affine, with piecewise-constant
density. A finite density partition satisfying the return-triangle condition
is obtained by taking its constant-density pieces and its zero-density
pieces separately. Thus the all-monster response theorem supplies an
explicit finite bound on the necessary triangle count.

**Theorem.** The unrestricted best monster response to this specified law
reduces to finitely many quadratic minimizations on compact rational
polytopes. Every resulting quadratic has rational coefficients. The exact
best-response value is rational and is attained by a monster whose vertex
times and positions are rational.

The reduction includes starting coincidences, tangencies, coincident
segments, waits at zero, zero-length legs, and capture at endpoints. It
does not discard parameter-boundary strata or infer their capture payoffs
from generic limits.

This is a finiteness theorem and a certificate construction, not an efficiency
claim. The hyperplane arrangement and the face enumeration may be very large.
It also does not assert that a rational piecewise-affine law is optimal for
the original game. A matching unrestricted upper strategy is still needed
to close that game.

## 2. A finite rational parameterization of all required monsters

The response theorem gives finitely many direction words. Fix one word and
write theta for its real parameters. For its initial prefix, use its starting
position and the bounded number of turn positions. Once the direction of
each leg is fixed, its duration is the signed difference of its endpoint
positions, with a nonnegative-duration constraint. Thus all vertex times
are affine functions of theta with rational coefficients.

For each zero-return triangle use its start and end times s,e and its sign.
Its peak has time `(s+e)/2` and position `+/- (e-s)/2`. The intervening waits
are at zero. Impose ordered disjoint time intervals, the arena bound
`e-s<=2`, and the common completion horizon six. The final endpoint visits
have times given by the last zero time plus one and plus three, or by the
first endpoint time plus two in the no-zero case.

All these constraints are linear with rational coefficients. The resulting
parameter set is a compact rational polytope P_theta. Different counts and
sign words give a finite union of such polytopes. Allowing zero-length legs
closes the domains. A limiting direction word that visits an endpoint earlier
than its designated final visit still describes a legal monster; inclusion
of these boundary paths cannot invalidate a best-response reduction.

On every segment the monster has a fixed slope `v_m in {-1,0,1}` and formula

    m(t;theta)=v_m*t+b_m(theta),

where b_m and the segment's time endpoints are rational affine functions.
No division by a variable leg duration is required, including on zero-length
legs: the slope belongs to the direction word and its endpoint identity
continues to hold when the duration is zero.

## 3. The princess path has a finite rational affine description

On each input quantile piece, all initial positions and leg characteristics
are affine in q. The raw path is obtained by finitely many minimum and
maximum operations applied to affine functions of `(t,q)`, followed by the
zero floor and endpoint absorption. Before absorption its graph therefore
has a finite rational polyhedral subdivision, on each cell of which

    p(t,q)=v_p*t+b_p(q),       v_p in {-1,0,1},

with b_p rational affine. Segment switch times are rational affine in q
after subdividing q at the finitely many points where switch orders change.

Endpoint absorption also has a finite affine description. Enumerate the
outward segments and their possible first intersections with position one.
Each candidate hitting time is affine in q, with affine conditions saying
that the time lies in its segment. Their earliest valid value is piecewise
affine on a finite rational quantile subdivision. From that time onward the
path is the constant one. Reflecting the path simply negates its positions
and slopes. At zero and at the endpoints, whole intervals of quantiles may
coincide; these are retained as actual constant segments.

## 4. Every first-capture regime is affine in (q,theta)

Consider a monster segment and a princess segment whose closed time intervals
overlap.

### Different slopes

If `v_m != v_p`, their only possible meeting is

    t = (b_p(q)-b_m(theta))/(v_m-v_p).                  (1)

The denominator is a fixed nonzero integer. The candidate time is rational
affine in `(q,theta)`. Its validity is determined by affine inequalities:
q lies in its quantile piece, t is nonnegative, and t lies in both segments'
closed time intervals. Equality is included because first contact captures.

### Parallel and coincident segments

If `v_m=v_p`, the segments meet exactly when

    b_p(q)=b_m(theta).                                 (2)

When (2) holds, their first meeting on this segment pair is the later of
the two starting times, provided this is no later than either ending time.
Split into the two affine cases selecting the later starting time. This
again gives affine candidates and affine validity conditions, including
coincident waiting segments at zero or an endpoint.

Zero-length segments and isolated common vertices can either be included
using the same closed-interval rules or enumerated as vertex candidates.
They do not require a generic-position assumption. Initial capture is the
candidate time zero and is treated in exactly the same way.

### Selecting the earliest valid meeting

There are finitely many segment pairs. Subdivide `(q,theta)` space by their
validity hyperplanes and by all pairwise comparisons between candidate
times. Include every lower-dimensional equality stratum. On each stratum
the valid candidate list and its earliest value are fixed, so

    T(q,theta)=alpha*q+ell(theta)+gamma                 (3)

for rational alpha,gamma and rational affine ell. Every monster in the
finite family visits both endpoints by time six, so some candidate is
valid and first capture is always finite.

## 5. Integrating a uniform quantile gives a quadratic

Every hyperplane just used has the form

    c*q+L(theta)=0

with rational constant c and rational affine L. If c is nonzero, its
intersection with the q fiber is a rational affine function
`q=-L(theta)/c`. If c is zero, it is a hyperplane entirely in parameter
space. Add the quantile bounds zero, one, and all fixed quantile-piece
endpoints to this finite list of fiber cuts.

Subdivide P_theta by all parameter-only hyperplanes and all comparisons
between these affine fiber cuts. On each relatively open parameter stratum
C their order is fixed. Thus each positive-length quantile interval has
affine endpoints `L_C(theta),U_C(theta)` and one fixed affine first-capture
formula (3). Its integral is

    alpha/2 * (U_C(theta)^2-L_C(theta)^2)
      + (ell(theta)+gamma)*(U_C(theta)-L_C(theta)),       (4)

a rational quadratic in theta. Sum over the intervals and both reflection
choices, with the factor one half. This gives a rational quadratic Q_C
equal to the actual expected capture payoff on that stratum.

Quantile endpoints of individual intervals have measure zero. A capture
coincidence holding for a positive-length quantile interval is not discarded:
its equality is independent of q after subdivision, so it is a parameter
stratum on which the corresponding coincident-segment rule is recomputed.
This is why parameter boundary strata cannot simply be omitted.

## 6. Boundary jumps do not invalidate the finite quadratic reduction

The actual expected capture payoff J(theta) can jump downward at a parameter
boundary. For example, exact overlap with a central waiting atom can capture
positive mass earlier. We therefore retain the separate quadratic Q_C for
every stratum C, including all equality strata.

Let P_C be the closure of C inside its affine hull. This is a compact
rational polytope. The trajectory m_theta depends continuously on theta in
the uniform topology, including zero-length legs. First capture against
any fixed continuous princess path is lower semicontinuous under this
convergence: any purportedly earlier subsequence of capture times has a
convergent subsequence giving an earlier limiting intersection. Fatou's
lemma then gives lower semicontinuity of J.

Consequently, for every `theta_0 in P_C`,

    J(theta_0) <= Q_C(theta_0).                          (5)

Indeed, approach theta_0 through C; Q_C is continuous and agrees with J
there. On the other hand, every actual theta belongs to a stratum C and
has `J(theta)=Q_C(theta)`. These two observations imply

    min_theta J(theta) = min_C min_(theta in P_C) Q_C(theta).  (6)

Thus closing a stratum for its quadratic optimization introduces only
boundary extension values that are no smaller than the actual boundary
payoff. The true boundary formulas remain among the other strata. No
unproved continuity of capture time is being used.

## 7. Rational quadratic minima have rational attaining points

Let P be a nonempty compact rational polytope and Q a rational quadratic.
Choose a minimizer x*. Let F be the smallest face of P containing x*, so
x* lies in the relative interior of F. The affine hull of F has a rational
parameterization

    x=x_0+Zy,

with rational x_0 and Z. In these coordinates write

    Q(x_0+Zy)= (1/2)y^T H y + c^T y+d,

with rational symmetric H,c,d. Since y* is an interior minimizer relative
to this affine hull,

    H y* + c = 0.                                      (7)

This consistent rational linear system has a rational particular solution
and a rational basis of its nullspace. Rational solutions are dense in its
real solution set. Choose a rational solution y_r sufficiently close to y*
that its corresponding point remains in the relative interior of F.

All solutions of (7) give the same quadratic value. If y and y+z both solve
it, then H z=0 and

    Q(y+z)-Q(y)=z^T(Hy+c)+(1/2)z^T H z=0.

Thus x_r is a rational point of P attaining its global minimum, and the
minimum value is rational. A vertex face is the zero-dimensional instance
of the same argument.

This also gives a finite exact procedure. Enumerate the faces of P; on each
face solve its tangential stationary linear system and test whether its
solution space meets the relative interior of the face. These are rational
linear feasibility problems, including strict inequalities for nonincident
facets. Evaluate Q at one rational feasible stationary point from every
successful face and take the smallest value. A global minimizer appears
on its smallest face, and every retained candidate is an actual feasible
point. No convexity assumption on the quadratic is needed.

Applying this procedure to (6) proves the theorem. If a minimizing quadratic
extension point lies on a lower-dimensional boundary, (5) and global
minimality force its actual payoff to equal the same minimum. Its rational
monster parameters therefore provide an attaining unrestricted response.

## 8. The resulting proof obligation is finite, but still candidate-specific

For one specified rational piecewise-affine ordered law, a complete exact
lower-response certificate can therefore consist of:

* the finite sign words and rational parameter polytopes;
* the affine capture-regime arrangement, including equality strata;
* the resulting rational quadratics;
* the finite face/stationarity comparisons establishing their minimum;
* one rational monster attaining that minimum.

The mathematical reduction does not require a time grid or an asymptotic
truncation error. The common six-time bound is justified by the endpoint
behavior of this particular law and by the response-normalization theorem.

The final game proof remains a different obligation: construct a law whose
exact lower response equals an unrestricted upper guarantee. This note
supplies a finite certificate format once such a law is proposed; it does
not prove that a rational law with a matching value exists.
