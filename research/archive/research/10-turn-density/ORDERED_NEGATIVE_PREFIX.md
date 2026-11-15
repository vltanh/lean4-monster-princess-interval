# An ordered-block response without monotonicity of the positive marginal

This removes the assumption that `p=f+g` is nondecreasing from the concrete
signed-M3 attachment in `EARLY_M3_RESPONSE.md`. The negative part of the
princess inverse can have several ordered constant blocks. Those blocks
are determined by exact pooling, so the four remaining scalar parameters
are unchanged. This is a response theorem for the specified density law;
it does not construct a matching lower strategy or determine the game value.

## 1. Scope and the negative-prefix score

Keep the signed M3 start band `[0,b]`, common turn floor r, and fixed
second turn `V=1`, with `0<b<r<1`. The checked implementation uses
`b=1/8` and `r=1/4`. Keep the attached negative early-M2 and both late
sheets, their separation conditions, nonnegative residual line densities,
nondecreasing f and k, the corrected negative-early edge, and the suffix
Gamma conditions. The positive M3 lower edge must remain nonnegative:

    p(z)<=k(r),                       0<z<b.               (1)

Only monotonicity of p is removed. For the finite implementation, p and
k are step densities on the existing partition; arbitrary nonnegative
step p is permitted. No further density bins are introduced.

For a princess starting at a, let `phi(V)` be its incoming inverse on

    -a<V<min(c,0),     a<=phi(V)<=u<=1.                   (2)

Here u is an upper bound on the negative inverse and a lower bound on
the positive inverse. A jump at `V=0` is legal: the two one-sided
inverse values need not coincide. When c is negative, u only bounds
the negative prefix. The whole scalar domain remains

    0<=a<=u<=1,          -a<=c<=y<=1.

Let K be a primitive of k. Outside the small positive-M3 start band,
the variable part of four times the threshold score is

    p(-V)*phi-K(phi).                                     (3)

For a below b there is also an alpha price

    J_a(U)=integral_a^b mP(z,U) dz,

which vanishes below r and is nonnegative above it. For a at or above b
this price is zero. On the small band the flat-corridor identity gives
the exact derivative

    q_U(V,U)=p(-V)-k(U),                 U<r,
    q_U(V,U)=-J_a(U),                    U>r.              (4)

In particular the score is constant above r whenever a>=b. It need not
be globally concave at r. The two-case comparison below retains this
upward derivative jump instead of applying Jensen across it.

## 2. Ordinary ordered pooling

First consider a negative interval without the modification in (4).
Write its consecutive constant coefficient intervals as lengths w_i
and coefficients p_i, in increasing V order. Pool adjacent intervals
whenever their weighted mean coefficients decrease. Continue until the
pooled means `p_hat_i` are nondecreasing. Within each pooled block, the
prefix integral

    D(v)=integral_(block left)^v [p(-s)-p_hat] ds

is nonnegative and is zero at the two block endpoints. This is the
usual cumulative property of adjacent-violator pooling and follows
directly by induction when two violating blocks are joined.

For every nondecreasing legal inverse phi, Stieltjes integration by
parts therefore gives, on each block,

    integral (p-p_hat)*phi = -integral D dphi <=0.          (5)

Consequently its score is bounded by

    integral [p_hat(V)*phi(V)-K(phi(V))] dV
      <=sum_blocks w * max_(a<=U<=u) [p_hat*U-K(U)].      (6)

Choose the smallest maximizing U on every block. Since K is convex,
this is the first crossing `k(U)>=p_hat`, clipped to `[a,u]` with the
appropriate one-sided convention at a step. The selected U values are
nondecreasing because the pooled means are nondecreasing. The resulting
constant inverse blocks satisfy equality in (5) and (6), so they give
the global optimum over all monotone inverses, including nonconstant
and singular ones.

For step k the chosen inverse lies at a density knot or at a clipping
endpoint. Thus this is a finite exact response calculation, not a
sampling of the inverse graph. Pooling the coefficients depends on p
and the interval lengths; the subsequent common convex potential may
be changed without recomputing that ordering argument.

## 3. The two cases at the small M3 band

The small band comes last in increasing V order. If the negative interval
ends before it, apply Section 2 to the entire interval with upper bound u.
Otherwise the following cases are exhaustive.

### A. All negative inverse values are at most r

When `a<=r`, apply ordinary pooling to the entire negative interval,
with upper bound `min(u,r)`. In this range the score is exactly (3),
including the small band; J_a is zero there.

### B. The small-band inverse is at least r

This case is needed only when `a>=b` and `u>=r`. Pool the left interval
`V<-b` with its full upper bound u. On the small-band suffix set phi
to the larger of r, a, and the last chosen left inverse. The small-band
score is constant on this range by (4), so this realizes its optimal
score among paths in this case.

To prove exhaustiveness, suppose first that `a>=b`. If the left interval's
terminal inverse exceeds r, monotonicity forces all small-band inverses
above r, giving Case B. If that terminal inverse is at most r, cap all
subsequent inverses at r. Their scores do not change above r, and the
left interval is unaffected; the result belongs to Case A. This includes
a path which first crosses r in the middle of the small band.

If `a<b`, the entire negative interval lies in the small band. Capping
at r is feasible since `a<b<r`, and (4) shows that it improves or
preserves every score above r. Hence Case A alone suffices. If `a>r`,
Case A is empty and Case B applies automatically.

The optimum is therefore the better of at most two explicitly constructed
block inverses. No monotonicity of p is used.

## 4. Attachment to the positive prefix and suffix

For any original legal inverse, choose u equal to its terminal negative
inverse (or the initial positive value when there is no negative interval).
The replacement above has all negative values at most u. The previous
positive-prefix first-crossing construction has all its values at least u
and remains valid: its monotone alpha and beta prices depend on the
nonnegative generators, monotone k, and (1), not on the order of p outside
the positive-M3 start band.

The corrected negative-early equality corridor is unchanged. The post-one
proof uses nondecreasing f, its decreasing reflected alpha reward, and the
Gamma conditions. It does not require monotonicity of p. Thus the old
suffix comparison and boundary-limit conventions still apply.

Under the retained hypotheses, the unrestricted princess response is the
same four-scalar supremum, now with the two-case ordered negative prefix
and the earlier optimized positive prefix. It is not in general correct
to keep the old constant negative inverse after dropping p monotonicity.

## 5. Exact fixed-path feature correction

For an arbitrary saved negative block inverse, its change from the old
constant-u inverse in the baseline law is

    4 Delta_base = integral_negative [
       p(-V)*(phi(V)-u) + integral_phi(V)^u k(U)dU] dV.    (7)

For a positive-M3 unit generator with lower turn r0 and start band Z,
define its cumulative mass

    M_(r0,Z)(U)=integral_Z integral_(r0)^U m_(r0,1)(z,s) ds dz.

Its additional four-payoff change is

    integral_(z in Z and -z in prefix)
         [(phi(-z)-r0)_+-(u-r0)_+] dz
      -integral_negative [M_(r0,Z intersect (a,1))(phi(V))
                           -M_(r0,Z intersect (a,1))(u)] dV.       (8)

Apply (8) to the edge coefficient `k(r)-p(z)` and each subsequent k
jump. The first term is the local cancellation; the second is the
positive-start alpha price. Both are linear in the density unknowns
for a frozen block path. No other attached-sheet feature changes.

`negative_prefix_oracle.py` implements (5)-(8), stores negative blocks
alongside the existing positive inverse pieces, and constructs physical
epsilon paths for independent capture integration.

## 6. Checks and discovery scope

`verify_negative_pava.py` compares the pooling prescription with an
independent complete dynamic program over every allowed nondecreasing
inverse sequence. All 3,960 exact rational comparisons pass, including
the flat-band cases and the additional nonnegative low-start alpha cost.
An explicit two-interval example has optimized ordered score 3/2 and
best constant score 1, so the extension can be strict.

Three complete physical-path checks cover a negative cutoff, a start
inside the M3 band, and an inverse crossing its turn floor. The largest
extrapolated difference from the analytic whole-law feature is
`4.44e-16`. Those floating checks verify the implementation independently
of the pooling score calculation.

`discover_negative_prefix.py` removes only the p-monotonicity rows from
the existing eleven-bin density problem. It preserves every other
structural row and records the remaining multipliers. Its scalar
separation is numerical. A converged finite-bin discovery objective is
not an exact response ceiling, a lower law, or a completed saddle proof.
