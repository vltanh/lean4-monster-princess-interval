# Complete negative-prefix optimization with an initial-inward sheet

The added monster family and its independently checked upper feature are
in `UNIFORM_INWARD_UPPER.md`. This note closes its negative-prefix
optimization for step densities, including interaction with the small
signed-M3 sheet. It replaces a potentially misleading finite sampling of
princess paths by a complete finite arrangement. The remaining scalar
optimization and a matched unrestricted equilibrium are not certified.

## 1. The local score

Use the attached signed-M3 law, with its small positive-M3 start band
`0<z<b0=1/8` and turn floor `r=1/4`. Add the actual density

    i(a,v)=h(a),                 -a<v<a,

where h is nonnegative and nondecreasing on the same finite density
partition as the other coefficients. It is additional mass, so
normalization adds `integral_0^1 2a*h(a)da`. There is no need to tie h
to k or to introduce a new density partition.

Write b for the princess's initial coordinate, c for the last V at its
`U=1` cutoff, and u for the upper bound on its negative inverse. On

    -b<V<min(c,0),             b<=phi(V)<=u,

put

    K(U)=integral_0^U k(s)ds,
    H(U)=integral_0^U h(s)ds,
    j_b(V)=H(b)-H(-V),
    w(V)=1+c-2V.

The part of four times the score which varies with U is, outside the
small positive-M3 band,

    q(V,U)=[p(-V)+j_b(V)]U-K(U)-w(V)H(U).              (1)

The omitted terms depend on V,b,c but not U, so they do not affect this
optimization. In the small band `V>-b0`, for `U>r`, add

    K(U)-K(r)-p(-V)(U-r).                              (2)

This is the exact integrated M3 cancellation. For `b>=b0`, the extra
positive-start alpha price J_b is zero, so (1)-(2) give the complete
variable score throughout the negative prefix.

### Low initial coordinates

If `b<b0`, all negative thresholds lie in the small band. Above r the
old M3 score derivative is `-J_b(U)<=0`. The new inward contribution is

    j_b(V)-w(V)h(U)<=0.                                (3)

Indeed `j_b(V)<= (b+V)h(U)` because `U>=b` and h is nondecreasing,
while `b+V<=1+c-2V` follows from `b<=1` and `V<=min(c,0)`.
Thus capping every negative inverse at r improves or preserves the score.
On the retained range `U<=min(u,r)`, J_b vanishes and (1) applies.
This cap is feasible since `b<b0<r`.

Equation (3) also explains why the old flat small-band suffix cannot
simply be ignored after adding h. For higher starts it is generally
decreasing above r, and its cost depends on the preceding block level.
The arrangement below keeps that cost rather than optimizing the left
and small-band pieces separately.

## 2. A finite set of inverse levels is sufficient

Take all k/h density knots in the legal inverse interval, add b and its
upper endpoint, and add r when it lies in that interval. The p partition
can be included too; in the implementation all densities share one
partition. Call the sorted set `U_0<...<U_m`.

For each fixed V away from a density boundary, (1)-(2) are affine in U
between consecutive members of this set. For a legal monotone inverse
with an intermediate value U, randomly round it to the two enclosing
levels with their linear interpolation probabilities. Use one common
uniform variable for the entire graph. Every resulting rounded graph
is nondecreasing: within one level interval, the upper-rounding event
increases with U, and distinct level intervals are already ordered.

The expected score of these rounded graphs equals the original score,
pointwise and after integration. At least one therefore scores no less
than the original. It suffices to optimize nondecreasing graphs taking
only the finite levels U_j. This argument needs piecewise affinity,
not concavity across the M3 turn-floor jump.

## 3. Every relevant V crossing is also finite

Split the negative V interval at the reflected density knots and at
`-b0`. On each resulting open cell, p(-V) and h(-V) are constant,
`j_b(V)` is affine, and w(V) is affine. Therefore the score for each
fixed inverse level has the form

    q(V,U_j)=A_j V+B_j.                                (4)

Insert every crossing of two such affine functions which lies inside
the cell. On an open interval between consecutive inserted points,
their relative order is constant.

Any nondecreasing finite-level graph can be made constant on that
interval without losing score: among the levels it uses there, choose
the one with greatest score. It dominates every other used level
throughout the interval. Make any preceding upward jumps at the left
edge and any following upward jumps at the right edge. Because the
chosen level lies between the incoming and outgoing levels, the whole
graph remains nondecreasing.

Thus every optimizing switch may be placed at a density boundary or a
pairwise score crossing. This proves completeness of the finite
arrangement, including zero-score ties and clipped interval endpoints.

## 4. Ordered dynamic programming

For consecutive arrangement intervals I_l and inverse levels U_j, compute

    W_lj=integral_(I_l) q(V,U_j)dV.

The complete recurrence is

    D_l(j)=W_lj+max_(i<=j) D_(l-1)(i).                  (5)

Retain predecessor indices and recover an optimal graph by tracing the
maximizing final state backward. Merge adjacent intervals having the
same level. The result has at most one block per inverse level, even
though the verification arrangement can contain many crossings.

For rational density data and rational b,u,c, all levels, crossing
coordinates, integrals, and comparisons in this negative-prefix
calculation are rational. The discovery implementation uses floating
arithmetic; it is not presented as a certified scalar supremum.

## 5. Positive prefix and interfaces

The added inward first variation at any prefix threshold is

    qI_U(V,U)=j_b(V)-(1+c-2V)h(U),

with `j_b(V)=integral_|V|^b h` when `|V|<b`, and zero otherwise.
On positive thresholds its V derivative is

    2h(U)-h(V)*1_(V<b)>=0,                             (6)

because `U>=max(b,V)` and h is nondecreasing. Its U derivative is
nonpositive. Consequently the existing ordered first-crossing response
uses the modified alpha price

    old_alpha_b(U)+(1+c-2V)h(U)

and target `old_target_b(V)+j_b(V)`. Its orderedness and clipped lower
bound are preserved. On the old early-M2 start band, the added derivative
is nonpositive, so the existing minimum-inverse comparison remains valid.
No post-one suffix inverse term is added by the inward family.

The negative replacement ends at an inverse no larger than u and the
positive replacement begins at one no smaller than u. They therefore
join legally, including a possible outward jump at V=0. The separately
verified full feature must integrate both parts; using u in place of the
new negative blocks would evaluate a different path.

## 6. Implementation and checks

`uniform_inward_prefix.py` implements the finite-level arrangement and
recurrence (5). `inward_attached_oracle.py` joins its blocks to the new
positive prefix and the independently derived additional h feature.

With h zero, 120 comparisons against the separate exact-pooling
construction agree to `2.71e-20` in score. With nonzero monotone h,
2,560 independently evaluated whole-law prefix routes do not beat the
arrangement optimum. These are implementation checks; completeness is
the argument in Sections 2-4, not the sampled comparisons.

The underlying inward-family verifier independently checks 172 exact
pure-route identities, 16 complete physical two-dimensional density
integrals on 247 affine capture cells, and 16 exact first-touch ceiling
losses. Its six attaining cases and ten strictly relaxed cases are
recorded separately. No sampled prefix or upper LP dual is claimed to
be a matching unrestricted princess law.
