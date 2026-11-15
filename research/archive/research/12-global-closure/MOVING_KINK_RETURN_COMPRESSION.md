# Moving spatial kink: finite compression between interface contacts

Research proof independently reviewed by the verification agent, 2026-11-14.

This note concerns a continuous field with one stationary spatial interface,
but a nonzero common time derivative. It proves a finite bound for a segment
whose physical endpoints both lie on that interface. It does not yet bound
the initial or final segment of a general light square when an endpoint is
away from the interface.

Translate the interface to `x=0`. On an interior light-coordinate square whose full physical coordinate box
stays inside the arena, write

\[
 F(t,x)=c+at+\begin{cases}b_-x,&x\le0,\\b_+x,&x\ge0,\end{cases}
 \qquad b_-,b_+\ge |a|.
\]

Reflection of space together with replacement of the CDF by its complement
reduces to `a>=0`. Incoming records satisfy `L<=F(t,0)<=H`. The running cost,
up to an irrelevant constant, is the integral of `L(t)-H(t)`. A fixed future
physical continuation contributes a continuous concave function `g(L,H)`,
nondecreasing in `L` and nonincreasing in `H`.

## 1. A negative return excursion has an immediate triangular replacement

Consider a path with `x(0)=x(T)=0` and `x(t)<=0` throughout. Subtract its
starting interface value from all scalar ranks, so the field is
`Y(t,x)=at+bx`, with `b=b_-`, and the incoming records are `l<=0<=h`.
Its exit upper record is fixed:

\[
 H_T=\max(h,aT).
\]

If no new lower record is made, the interface hold dominates pointwise in
upper record and preserves the lower record. Otherwise let the final lower
record be `-B<l`, and first assume `b>a`. Put `beta=b-a` and `d=B/beta`.
The replacement moves with velocity `-1` for time `d`, with velocity `+1`
for time `d`, and then holds at the interface until `T`.

### Feasibility and lower records

At any old event `(v,-D)` where the global lower record is reached,

\[
 -B=av-bD,
 \qquad D=\frac{av+B}{b}.
\]

The initial speed bound gives `v>=B/beta`. The terminal speed bound gives
`T>=v+D>=2B/beta=2d`, so the replacement fits. Since every original scalar
trajectory has derivative at least `-beta`, its running lower record is
bounded below by

\[
 \min\{l,\max(-B,-\beta t)\}.
\]

The replacement attains this bound at every time. It has the same final
lower record and a pointwise no larger running lower record.

### Upper record deficit

For a required event `(v,-D)`, the speed bound and `x<=0` imply

\[
 x(t)\le q(t):=\min\{0,-D+|t-v|\}.
\]

Here `u=v-D>=0`, and `v+D<=T`. Thus `q` is a negative triangle, with
interface holds before and after it. Its depth satisfies

\[
 D=\frac{au+B}{\beta}.
\]

Spatial monotonicity implies that the original path's upper record is at
most the upper record of `q` at every time. It suffices to compare these
triangles with the immediate triangle `u=0`.

Let the boundary reference upper record be `max(h,at)`. For `a>0`, the
integral of its excess over the triangular path's upper record is exactly

\[
 I(u,B;h)
 =\frac{b}{2a(a+b)}
   \left[a(u+2D)-\max(h,au)\right]_+^2,
 \qquad D=\frac{au+B}{\beta}.
 \tag{1}
\]

Indeed, an upper rank `y` between `max(h,au)` and `a(u+2D)` is first
reached at

\[
 \tau_y=\frac{b}{a+b}(u+2D)+\frac{y}{a+b},
\]

whereas the interface reaches it at `y/a`. Integrating the difference gives
(1). The bracket in (1) equals the positive part of

\[
 \min\{2aD,\ a(u+2D)-h\}.
\]

Both quantities inside this minimum are nondecreasing in `u`. Consequently
`I(u,B;h)>=I(0,B;h)`. The immediate triangle has no larger integrated upper
deficit than the original path. Together with the lower-record comparison,
it weakly decreases the integrated survival cost and preserves both exit
records. Every common future continuation therefore remains valid.

For `a=0`, the upper record is constant and the lower-record argument alone
suffices. For `b=a`, the scalar derivative on the entire left half is
nonnegative, so a new lower record is impossible and the interface hold
dominates.

## 2. Positive return excursions and interface holds

On a nonnegative return excursion, the lower record is constant because
`F(t,x)>=F(0,0)>=L`. The pointwise maximal positive triangle

\[
 x_*(t)=\min(t,T-t)
\]

therefore dominates: it preserves the lower record and has a pointwise no
smaller upper record.

For a finite polygonal interface-to-interface path, apply these two lemmas
to its sign components. Consecutive same-sign pieces can first be grouped.
Every negative component becomes an immediate triangle followed by an
interface hold; every positive component becomes one full triangle.

Push any interface hold to the right. A hold followed by a negative
triangle is a nonpositive return segment, so Section 1 replaces it by one
negative triangle and a final hold. A hold followed by a positive triangle
is dominated by one positive triangle occupying their combined duration.
This process creates no new sign excursion. The result is an alternating
finite sequence of positive and negative triangles, followed by at most one
interface hold. Remove any triangle which makes no new relevant record,
using the same one-sided lemmas.

## 3. The cost of a negative-positive pair is concave when `b_-<=b_+`

Assume temporarily `b_-,b_+>a>=0`, and define

\[
 \alpha_\pm=b_\pm+a,\qquad \beta_\pm=b_\pm-a.
\]

Fix an interface-to-interface pair of total duration `2K`, consisting of a
negative triangle of depth `p`, then a positive triangle of depth `K-p`.
Subtract the starting boundary rank, and let incoming records be `l<=0<=h`.
On the interval where both excursions make a new record, the exit records
are affine in `p`:

\[
 L=-\beta_-p,
 \qquad H=\alpha_+K-\beta_+p.
 \tag{2}
\]

The inequalities selecting this interval are `L<=l` and `H>=h`, along with
`0<=p<=K`. It is a closed interval, possibly empty.

For any newly captured lower rank `y`, its first-visit time is `-y/beta_-`.
For a newly captured upper rank, its first-visit time is

\[
 \tau_y=\begin{cases}
 \dfrac{2b_-p+y}{\alpha_-},&h\le y\le2ap,\\[4pt]
 \dfrac{2b_+p+y}{\alpha_+},&\max(h,2ap)\le y\le H.
 \end{cases}
\]

The local cost is `2K(1+L-H)` plus the integrals of these first-visit times,
up to constants independent of `p`. Its quadratic coefficient is

\[
 q_{NP}^{(1)}
 =\frac{\beta_-}{2}
  -\frac{\beta_+(3b_++a)}{2\alpha_+}
 \qquad\text{when }h\ge2ap,
 \tag{3}
\]

and

\[
 q_{NP}^{(2)}
 =\frac{\beta_-}{2}
  +\frac{2a(2b_-+a)}{\alpha_-}
  -\frac{3\alpha_+}{2}
 \qquad\text{when }h\le2ap.
 \tag{4}
\]

The two cost polynomials join with equal value and first derivative at
`h=2ap`. Moreover,

\[
 q_{NP}^{(2)}-q_{NP}^{(1)}
 =\frac{2a^2(b_--b_+)}{\alpha_-\alpha_+}.
\]

If `b_-<=b_+`, then `q_NP^(1)<=0` and `q_NP^(2)<=q_NP^(1)`. The complete
local cost is therefore concave on the productive interval. Adding the
concave continuation `g(L,H)`, with the affine records (2), preserves this
concavity.

A minimum is attained at an endpoint of that interval. Such an endpoint
has `p=0`, `p=K`, `L=l`, or `H=h`. The first two already have only one
excursion. If `L=l`, the negative triangle makes no new lower record;
replacing it by an interface hold and then enlarging the positive triangle
dominates. If `H=h`, the positive triangle makes no new upper record;
replace it by a hold and use Section 1 on the resulting nonpositive path.
In all cases the pair becomes at most one excursion and one final hold,
with no greater complete cost.

If one excursion was unproductive initially, the same endpoint replacement
applies directly, so it is not necessary to enter the productive interval.

## 4. The positive-negative pair when `b_->=b_+`

Now consider a positive triangle of depth `p` followed by a negative
triangle of depth `K-p`. On the productive interval,

\[
 P=\alpha_+p>h,
 \qquad L=\alpha_-p-\beta_-K<l,
 \qquad H=\max(P,2aK).
 \tag{5}
\]

The upper ranks captured during the first triangle have first-visit time
`y/alpha_+`. New lower ranks have first-visit time

\[
 \tau_y=\frac{2b_-p-y}{\beta_-}.
\]

When `P<2aK`, the additional upper ranks between `P` and `2aK` are first
reached on the returning negative leg, at

\[
 \tau_y=\frac{2b_-K+y}{\alpha_-}.
\]

Consequently the local cost's quadratic coefficient is

\[
 q_{PN}^{(1)}
 =\frac{\alpha_+}{2}
  -\frac{\alpha_-(3b_--a)}{2\beta_-}
 \qquad\text{when }P\ge2aK,
 \tag{6}
\]

and

\[
 q_{PN}^{(2)}
 =q_{PN}^{(1)}-\frac{\alpha_+^2}{2\alpha_-}
 \qquad\text{when }P\le2aK.
 \tag{7}
\]

Again the cost is continuously differentiable at the joining point. If
`b_->=b_+`, then both coefficients are nonpositive. The continuation in (5)
is concave as well: `L` is affine, `H` is a convex maximum of affine
functions, and `g` is concave, nondecreasing in `L`, and nonincreasing in
`H`.

An endpoint minimum has zero duration for one triangle, an old lower
record, or an old positive peak `P=h`. An old lower record allows the
nonnegative replacement from Section 2. If `P=h`, replace the positive
triangle by a boundary hold without affecting any records; Section 1 then
compresses the entire nonpositive segment. Thus a positive-negative pair
also becomes at most one excursion and one final hold in this slope order.

## 5. Bound for an interface-to-interface segment

Use the entire fixed later physical continuation whenever applying Sections
3 or 4. Push any newly created hold to the right as in Section 2. Each pair
replacement removes at least one sign excursion, so the finite procedure
terminates.

When `b_-<=b_+`, no negative-positive adjacency remains; the only possible
alternating sequence is positive then negative. When `b_->=b_+`, no
positive-negative adjacency remains; the sequence is negative then
positive. In either case there are at most two triangles and one final
interface hold:

\[
 \boxed{\text{At most four unit-speed directional legs and one interface hold.}}
 \tag{8}
\]

The first one-sided replacements preserved both exit records or improved
them. The pair exchanges use concavity of the fixed future and may change
the exit records; do not claim record preservation for (8).

All replacements keep the physical endpoint states and times. Their light
coordinates are nondecreasing and remain in the entry/exit coordinate box,
so they stay in the original light square.

For arbitrary Lipschitz paths, polygonal approximation gives convergence
of both running records and integrated cost. Apply the finite polygonal
result and take a convergent subsequence of the at most five duration
parameters. The same compactness argument covers the degenerate slope
limits `b_-=a` or `b_+=a`. The fixed physical continuation has its natural continuous concave extension
to nearby scalar records, so the inequality passes to the limit. This
establishes (8) for general interface-to-interface segments.

The stated application is restricted to interior merged light squares whose
entry/exit coordinate box stays inside the physical arena. This note does
not extend a scalar affine field outside the arena or justify clipping such
an extension; physical boundary half-cells require their separate boundary
argument.

## 6. Remaining scope

This is a return-segment theorem. A general visit to a merged square may
start or end off the spatial interface. Its prefix before first interface
contact and suffix after last contact still require a finite half-cell
argument. Neither this theorem nor the previous stationary theorem proves
a finite exact equilibrium mesh for the unrestricted game.
