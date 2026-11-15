# A conditional response reduction for monotone candidate densities

## Scope and hypotheses

This note gives a globally sufficient response-shape theorem for a
**specified class** of M1/M2 laws. It does not establish that an optimal
monster law has these hypotheses, solve the resulting scalar optimization,
or provide an unrestricted princess lower guarantee.

The symmetric monster law has unreflected parameter measures

    mu_1 = w0 delta_(-1) + f(x) dx on [0,1],
    mu_2 = g(x) dx on [0,1] + h(z) dz at parameter x=-z,

where the masses sum to one. Suppose f, g, h are bounded, nonnegative
densities, f and h are nondecreasing, and there is an alpha in [0,1] such
that, almost everywhere,

    f(x)+g(x)=0                  on [0,alpha),
    f(x)+g(x)>=h(1)              on (alpha,1].             (H)

Changing a density on a null set has no effect; nondecreasing versions
are used. The endpoint atom is allowed, but additional atoms are not part
of this theorem.

Fix a princess start `0<=a<1` and frozen transition parameter

    -a <= c < 1,
    e=(1+c)/2=inf{t:U(t)>1},       U=t+p, V=t-p.

The path therefore exits the `U=1` characteristic at `(1,c)`. We first
give separate prefix and suffix results for these fixed parameters.
Section 4 handles `a=1` and `c=1` by an explicit lower-semicontinuity
argument; it does not silently assign a limiting capture formula to
a boundary path.

## 1. Prefix: one switch is sufficient under (H)

Up to `U=1`, the absolutely continuous alpha-threshold density in the
notation of `M1_M2_CONTROL.md` is `h(U)`. The beta-threshold density is

    f(-V)+g(-V)       for negative V up to c,
    h(V)             for 0<V<c, if c>0.

All other terms are constants for this optimization or nonnegative atoms
at `U=1`. The latter have first-capture time at most e. Replacing that
time by e gives an upper relaxation; it is approached by keeping `U<1`
until the end of the prefix.

After the integration-by-parts identity in `M1_M2_CONTROL.md`, the
path-dependent integrand for a graph `V=z(U)` is

    L(U,V)=G(V)+h(U)V,                                      (1)

where G is the beta tail. Its allowed interval is

    -a <= V <= b(U),        b(U)=min(c,U).

For fixed U, the derivative in V on the negative half-line is
`h(U)-f(-V)-g(-V)`. Under (H), this is nonpositive for `V<-alpha`
and nonnegative for `V>-alpha`. Thus the score has a valley there, and
its maximum on any negative interval is at an endpoint. On the positive
half-line its derivative is `h(U)-h(V)>=0`, because `V<=U`. Consequently
the maximum of (1) on the entire allowed interval is at `V=-a` or
`V=b(U)`.

The difference between those endpoint scores is

    D(U)=G(b(U))-G(-a)+h(U)(b(U)+a).

It is nondecreasing in U. Where `b(U)=U`, the G derivative `-h(U)`
cancels the derivative from `h(U)U`; where b is constant, there is no
such term. In Stieltjes form,

    dD(U)=(b(U)+a) dh(U) >= 0.                             (2)

The coefficient is nonnegative since `c>=-a`. Thus the pointwise
maximizing endpoint can be selected by a single switch, which is also
a legal nondecreasing graph. For some `u in [a,1]`, the maximizing
prefix is therefore, in characteristic coordinates,

    (a,-a) -> (u,-a) -> (u,min(u,c)),

followed, if `c>=u`, by the diagonal to `(c,c)`, and then a horizontal
leg to `(1,c)`. This is exactly the prefix of `P(a,u,c)` defined in
`POST_SWEEPER_DETOUR.md`. If `u=1`, use a sequence `u<1` approaching
one. This preserves the claimed upper supremum and avoids treating an
early `U=1` plateau as if its first capture occurred at the plateau's
right endpoint.

The argument handles negative c as well: then `b(U)=c` is constant,
the two alternatives are `V=-a` and `V=c`, and (2) still applies.

## 2. Suffix: a single extra inward leg with a free endpoint

This part requires only that f be nondecreasing. Fix any prefix and its
cutoff c. After crossing `U=1`, the alpha density is

    A(U)=f(2-U) for 1<U<2-a, and zero afterward.           (3)

Write `L=2-a`. The beta tail G has density `f(-V)` on `[c,0]` if
c is negative, no density on `[max(c,0),1)`, an atom of nonnegative
mass B0 at one, density `f(2-V)` on `(1,2)`, and a nonnegative atom
at three. In particular, G is convex on `[c,1)`: on its negative
part its derivative `-f(-V)` is nondecreasing, and at zero that
derivative increases to zero.

**Suffix theorem.** The supremum over all legal suffixes with this
fixed cutoff equals the supremum obtained by one additional inward leg
immediately after crossing `U=1`, ending at a freely chosen
`y in [c,1)`, followed by an outward leg to `p=1` and then a wait.
The case `y=c` is the original outward suffix. The limit `y->1-` is
included in the supremum.

Here "immediately after" means first reaching `U=1+epsilon` and then
raising V from c to y, with epsilon tending to zero. At exactly `U=1`
that inward leg would change the cutoff; it is not an admissible
substitute with the same capture formula.

**Proof.** The graph integrand is

    G(V)+A(U)V.                                            (4)

For `1<U<L`, any `1<=V<=U` is no better than the left-hand limit
`V->1-`. Indeed the score difference is

    B0 + integral_(2-V)^1 f(x) dx - f(2-U)(V-1) >= 0,       (5)

since `2-V>=2-U` and f is nondecreasing. For U after L, A is zero
and reducing V increases G. Thus, by clamping and taking a limit,
it suffices to consider `V<1` until the strip's lower boundary forces
larger V.

Fix the value `y<1` reached at U=L. On `[1,L]` the strip's lower
obstacle is inactive: `U-2<=-a<=c`. Hence the graph is any
nondecreasing function with values in `[c,y]`. Convexity of (4) in V
gives its chord bound between c and y. Writing

    V(U)=c+(y-c)lambda(U)

with nondecreasing lambda, layer cake represents that chord bound as
an average of graphs that make a single jump from c to y at some
`s in [1,L]`. Every such graph has the same terminal y, and therefore
the same best continuation after L. That continuation is simply the
smallest feasible `V=max(y,U-2)`; it maximizes the decreasing beta tail.

For a single jump, the difference between the y-score and the c-score is

    D_y(U)=G(y)-G(c)+(y-c)f(2-U),

which is nonincreasing in U. The payoff as a function of its jump
location s therefore has nondecreasing derivative `-D_y(s)` and is
convex. Its maximum is at `s=1` or `s=L`. A jump at L brings no
remaining alpha benefit and can only accelerate beta captures; omitting
it and using the original outward suffix is at least as good. A jump
at one is the claimed additional inward leg. Taking limits from
`U>1` and `y<1` proves the statement, including the possible failure
of attainment.

## 3. Exact scalar cost of the extra leg

Let

    Fbar(a)=integral_a^1 f(x) dx.

Relative to the original outward suffix, the limiting gain from the
additional leg to y is

    4 Delta(a,c,y)
      = (y-c) Fbar(a)
        - integral_(max(0,-y))^(max(0,-c)) (1-x) f(x) dx.  (6)

The first term delays unreflected M1 paths starting above a. The integral
is the loss from earlier unreflected M1 captures with B thresholds
crossed by the extra inward leg. Every M2 capture and the remaining
M1 captures are unchanged. Formula (6) can also be obtained directly
from the first-inverse formulas.

If `c>=0`, the integral is zero, so `y->1-` is optimal and (6)
reduces to the gain proved in `POST_SWEEPER_DETOUR.md`. For negative c,
one must optimize y; monotonicity of f does **not** justify retaining
only `y=c` and `y=1`.

For example, take `a=99/100`, `c=-99/100`, f equal to one below a
and eleven above a. This is a nondecreasing density, and can be scaled
to fit a probability law. It has `Fbar(a)=11/100`. At `y=-9/10`,

    4 Delta = 99/20000 > 0,

whereas at `y=1`,

    4 Delta = -5621/20000 < 0.

Thus a partial inward leg beats both endpoint choices in this example.
Multiplying f by `10/11` makes it a probability density; with
`w0=g=h=0` and `alpha=0`, it satisfies the hypotheses above. It is not
asserted to be an equilibrium law. The example rules out the
endpoint-only suffix shortcut even within the conditional class.

## 4. Boundary responses are bounded by interior responses

Let p be any nonnegative legal princess path, including one with `a=1`
or `c=1`. For `0<epsilon<1/2`, set

    p_epsilon(t)=epsilon+(1-2epsilon)p(t).

This path is legal, takes values in `[epsilon,1-epsilon]`, and has speed
at most `1-2epsilon`. In particular its initial point is strictly less
than one, and `U_epsilon=t+p_epsilon` is strictly increasing. Its exit
time from `U=1` is at most `1-epsilon`, so its parameter c is strictly
less than one. The paths converge uniformly to p.

For any fixed continuous monster path, first capture is lower
semicontinuous under this convergence. Indeed, if a subsequence had
capture times bounded a fixed amount below the capture time against p,
a further convergent subsequence of those times would give an earlier
zero of the limiting difference, a contradiction. Every monster in the
present support captures by time four. Fatou's lemma consequently gives

    J(p) <= liminf_(epsilon->0+) J(p_epsilon).

Thus the supremum over the interior cases already bounds all boundary
responses. This is an upper-response argument; it is not a justification
for taking a singular limit in a claimed princess lower strategy.

## 5. What the conditional theorem supplies

Under the stated density assumptions, every nonnegative princess response
is bounded by the supremum of an explicit family with four scalar
parameters `(a,u,c,y)`. Its prefix has one switch; its suffix has at most
one additional inward leg after the sweeper characteristic. The family
includes limits at `u=1` and `y=1`, with the capture conventions explained
above. The symmetry and uncrossing reduction in
`CHARACTERISTIC_RESPONSE.md` then bounds arbitrary princess responses.

This is a candidate-specific sufficient reduction, not a universal
bounded-turn theorem. Before it can close an upper bound, one must
construct a law satisfying its hypotheses and optimize this full family.
A matching lower guarantee against every monster remains an independent
requirement.
