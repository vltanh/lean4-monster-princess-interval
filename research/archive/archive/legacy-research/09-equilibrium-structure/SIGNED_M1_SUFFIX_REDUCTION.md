# A four-parameter princess response theorem with signed M1 support

## 1. The monster law and sufficient hypotheses

Use the M1 and M2 families and first-inverse conventions of
`../08-continuum/CHARACTERISTIC_RESPONSE.md`. Consider the symmetric law

    mu_1 = w0 delta_(-1)
           + f(x) dx at parameter x in (0,1)
           + ell(z) dz at parameter x=-z, z in (0,1),

    mu_2 = g(x) dx at parameter x in (0,1)
           + h(z) dz at parameter x=-z, z in (0,1),

where all densities are bounded and nonnegative and the total mass is one.
The mass of every reflected pair is divided equally between its two paths.

Assume that the following functions have nondecreasing versions:

    f,    f+g,    k=h+ell.                                (H)

There is no separate monotonicity assumption on ell or h. In particular,
the signed M1 density is not required to make the suffix threshold tail
convex. The proof below handles an arbitrary suffix tail.

**Theorem.** Under (H), the response ceiling over all admissible princess
paths equals the supremum over the same four scalar parameters

    0<=a<=u<=1,    -a<=c<=y<=1

used in the corrected conditional response family. Interior representatives
have `a<1`, `u<1`, `c<1`, and `y<1`; the remaining parameter values mean
one-sided payoff limits.

The characteristic prefix is

    (a,-a) -> (u,-a) -> (u,min(u,c)),

followed by the diagonal to `(c,c)` when c>=u, and then by the horizontal
leg to `(1,c)`. After crossing U=1, the path makes at most one additional
inward leg: it first reaches `(1+epsilon,c)`, raises V to y at that U
level, then moves outward to the endpoint and stays there. Let epsilon
decrease to zero. The parameter inequalities and a sufficiently small
epsilon make the construction legal.

This theorem controls princess responses to a specified monster law. It
does not assert that the hypotheses hold for an optimal law or that a
matching unrestricted princess lower strategy has been found.

## 2. The prefix reduction with k=h+ell

By the reflected-pair absolute-value comparison it suffices to consider
nonnegative princess paths. Put

    a=p(0),  U=t+p,  V=t-p,
    e=inf{t:U(t)>1},  c=2e-1.

For the moment take a<1 and c<1. Fixing a and c freezes the M2 cutoff.
Before U=1, the absolutely continuous alpha-threshold density is k(U).
The beta-threshold density is

    (f+g)(-V)        for negative V,
    k(V)             for positive V up to c.

All other terms are constants for this optimization or nonnegative atoms
at U=1. The latter are bounded by replacing their first inverse by e,
and that upper relaxation is approached with U<1 until the prefix ends.

The graph formulation has integrand

    L(U,V)=G(V)+k(U)V,

with `-a<=V<=b(U)=min(c,U)`. On the negative V interval its derivative is

    k(U)-(f+g)(-V).

Since f+g is nondecreasing, this derivative is nondecreasing in V.
Consequently the score is convex on that interval, so its maximum lies
at an endpoint. On the positive V interval its derivative is

    k(U)-k(V)>=0,

because V<=U and k is nondecreasing. The maximum on the full allowed
interval therefore occurs at V=-a or V=b(U).

The score difference between these alternatives is

    D(U)=G(b(U))-G(-a)+k(U)(b(U)+a).

Its Stieltjes differential is

    dD(U)=(b(U)+a) dk(U)>=0.

Where b(U)=U, the derivative of G cancels the k(U) term; where b is
constant there is no such term. A maximizing endpoint can therefore be
chosen with a single switch at U=u. This gives exactly the prefix in
Section 1. The proof does not require the older density-gap condition.

## 3. Suffix reduction by opposite Chebyshev monotonicity

Fix an arbitrary legal prefix with the same a and cutoff c. After U=1
the only alpha-threshold density is

    A(U)=f(2-U)    for 1<U<L=2-a,
    A(U)=0        for U>L.                               (1)

In particular A is nonincreasing on [1,L]. Let G be the beta-threshold
tail for this fixed prefix. It is nonnegative and nonincreasing, but need
not be convex or concave.

Up to terms independent of the suffix, four times its payoff is

    integral_1^infinity [G(V(U))+A(U)V(U)] dU.             (2)

This is the graph integration-by-parts identity from the characteristic
control formulation. Vertical graph segments are allowed; their values
at individual U levels do not affect the ordinary integral. First-inverse
values and threshold atoms are still retained in the original payoff.

### First keep V below one while A is active

For `1<=V<=U<L`,

    G(1-)-G(V)
      >= B0 + integral_1^V f(2-s) ds
      >= f(2-U)(V-1),

where B0>=0 is any beta mass at one. The second inequality uses the
monotonicity of f and V<=U. Interior negative M1 parameters add beta
density below one and above two, so they do not weaken this comparison
on (1,2).

Thus the score in (2) cannot decrease when V>=1 is clamped to its
left-hand limiting value at one. After U=L, A is zero and decreasing V
can only increase G. Using V<1 and then taking a limit therefore suffices.
The lower spatial obstacle `V>=U-2` is inactive on [1,L], since
`U-2<=-a<=c`.

### Then replace any increasing graph by one constant level

Let I=[1,L], of length L-1>0, and let V be any nondecreasing graph with
values between c and some y<1. Opposite Chebyshev monotonicity gives

    integral_I A(U)V(U) dU
      <= (integral_I A)/(L-1) * integral_I V.             (3)

For completeness, subtracting the right side from the left side equals

    1/[2(L-1)] * integral_I integral_I
      (A(s)-A(t))(V(s)-V(t)) ds dt,

which is nonpositive because A decreases and V increases.

Set `Abar=(integral_I A)/(L-1)`. Combining (3) with the unchanged G
term yields

    integral_I [G(V(U))+A(U)V(U)] dU
      <= integral_I [G(V(U))+Abar V(U)] dU
      <= (L-1) sup_(c<=v<=y) [G(v)+Abar v].              (4)

The last quantity is the supremum of the scores of constant graphs
V(U)=v on I. Choose such a v, or a sequence approaching the supremum.
It is no larger than the old terminal value y. For U>L, the smallest
feasible continuation is

    V_new(U)=max(v,U-2).

The old continuation has V>=y and V>=U-2, so V_new<=V_old. Since A=0
there, this continuation is at least as good as the old one.

We have proved that an immediate jump from c to one freely chosen v,
followed by an outward leg and endpoint wait, controls every suffix.
Rename v as y. The formal jump at U=1 is approached by placing it at
U=1+epsilon; this preserves the original M2 cutoff. The bounded-density
capture formulas justify the payoff limit. Values y approaching one are
handled from below, so atoms at B=1 are not silently crossed early.

The argument used no convexity of G and therefore no monotonicity of ell.
This is why the suffix reduction survives the signed M1 repair.

## 4. Exact scalar gain and the new interior suffix equation

Let J(a,u,c) be the original outward-suffix payoff, and K(a,u,c,y) the
limit after adding the immediate inward leg. Write

    Fbar(a)=integral_a^1 f(x) dx.

Direct first-inverse comparison gives

    4(K-J)
      = (y-c) Fbar(a)
        - integral_(max(0,-y))^(max(0,-c)) (1-x)f(x) dx
        - integral_(max(0,c))^(max(0,y)) (1+z)ell(z) dz.  (5)

The first term delays positive-parameter unreflected M1 captures with
x>a. The second term is the previously identified cost of crossing
negative B thresholds. The new third term comes from negative-parameter
unreflected M1 captures B(z): for c<z<=y, their capture changes from
z+1 to the limiting time (1+z)/2. Every M2 capture is unchanged.

For c>=0, an interior positive optimum y satisfies

    (1+y)ell(y)=Fbar(a).                                 (6)

This equation can distribute the time-one princess positions, since the
limiting post-transition path has `p(1)=1-y`. The old positive-M1-only
law has ell=0 and forces y toward one whenever Fbar(a)>0; the new term
is exactly the missing cost of that inward movement.

If `S_ell(y)=(1+y)ell(y)` is continuous and strictly increasing, the
global optimum on the positive interval is obtained by clipping its
inverse to [c,1]:

* y=c when Fbar(a)<=S_ell(c);
* S_ell(y)=Fbar(a) when the inverse lies in (c,1);
* y tends to one when Fbar(a)>=S_ell(1-).

In the interior differentiable case,

    y'(a)=-f(a)/S_ell'(y(a))<=0.                          (7)

Thus increasing starting quantiles can have decreasing suffix parameters,
which is compatible with the ordered multi-leg lower-law construction.
For c<0, the negative-y possibilities must also be compared using the
full formula (5); (6) alone does not optimize that branch.

## 5. Quantitative stability on a positive suffix strip

The proof gives a useful equality-case estimate. Suppose c>=0 and a
suffix graph remains in `[c,y]` on `[1,L]`, where `y<1` is its terminal
level. Put

    Abar=Fbar(a)/(1-a),
    m=Abar-ess_sup_(c<z<y) ell(z).

If m>0, then replacing the graph by the constant level y and the minimal
continuation improves the total payoff by at least

    m/4 * integral_1^L [y-V(U)] dU.                    (8)

Indeed, on this strip G'(v)=-ell(v), so
`H(v)=G(v)+Abar*v` satisfies `H(y)-H(v)>=m(y-v)`. Combine this with
the nonnegative opposite-Chebyshev deficit in (3). The continuation
comparison is also nonnegative. The same assertion follows from the
stronger sufficient condition `inf_[a,1] f>ess_sup_[c,y] ell`.

Let S be the global response ceiling of the specified monster law and
let `epsilon=S-J_M(p)`. Under the preceding strip hypotheses, (8) gives

    integral_1^L [y-V(U)] dU <= 4 epsilon/m.

For `0<eta<L-1`, monotonicity then implies

    y-V(1+eta) <= 4 epsilon/(m eta).                    (9)

Thus near-best suffixes in any region with a uniform positive m collapse
to the immediate inward characteristic in a quantitative sense. This
controls arbitrary paths in that region, not just chosen extreme
representatives. If the original graph reaches V>=1, the clamping step
must first be handled; (8) does not silently assume that its deficit is
zero.

There is a separate unconditional prefix estimate when w0>0, a<1, and
c<1. Writing `s=A(1)` and `e=inf{t:U(t)>1}`, the prefix upper relaxation
loses at least `w0(e-s)/2` from its endpoint M1 atom. Every remaining
relaxation in the proof is nonnegative. Consequently,

    e-A(1) <= 2 [S-J_M(p)]/w0.                         (10)

These estimates can help validate a shifted-turn attack against all
near-best responses after the active scalar parameter regions have been
enclosed. They do not by themselves exclude the full signed-M1 class:
flat score regions and boundary branches still need their own analysis.

## 6. Boundary conventions and the scope of the reduction

The parameters u=1, y=1, a=1, and c=1 mean payoff suprema from legal
interior paths. In particular, an inward leg at exactly U=1 can change
the M2 cutoff and is not a substitute for the U=1+epsilon construction.

All boundary princess paths are bounded by interior ones using

    p_epsilon(t)=epsilon+(1-2epsilon)p(t).

These paths are legal, have initial positions below one, and have strictly
increasing U. They converge uniformly to p. First capture against each
fixed continuous monster is lower semicontinuous, and every supporting
monster captures by time four. Fatou's lemma gives the needed upper
comparison. This is an upper-response argument, not a license to use a
singular limiting path as a lower strategy.

When a tends to one, Fbar(a) tends to zero. Formula (5) then makes y=c
optimal unless the crossed M1 threshold measures vanish. In particular,
one must differentiate an endpoint-start branch tangent to the boundary
y=c, rather than holding y fixed. If a=u=1 and c>0 are approached on
this branch, its positive-c stationarity equation is

    (7-c)h(c)+(1+c)ell(c)=w0.                            (11)

The old relation `(7-c)h(c)=w0` omits the new M1 cost. For an interior
extra-suffix branch y>c with u=1, the partial c equation can instead be

    (7-c)h(c)=w0+Gbar(a),

where Gbar is the positive M2 tail. These equations concern different
active constraints and must not be conflated.

The result supplies a finite-dimensional global upper-response problem
for a plausible larger support class. A complete game proof still needs
an actual law satisfying (H), a proof of its scalar response ceiling,
and a matching princess law with an unrestricted lower certificate.

## 7. A common shifted-M2 attack on positive extra-leg representatives

There is a necessary unrestricted-monster check beyond the scalar upper
optimization. Fix an interior representative with `0<=c<y<1`, and
realize its extra inward leg on U=1+epsilon. Shift the M2 component from
its descending characteristic U=1 to U=1+delta, keeping the starting
parameter x fixed. The shifted paths and exact capture formulas are in
`SHIFTED_CHARACTERISTIC_RESPONSE.md`.

For legality, shift only positive starts x<=1-delta; the omitted g mass
tends to zero. All negative starts are legal for small delta. Keep the
M1 component unchanged. First let epsilon tend to zero with delta fixed,
and only then let delta decrease to zero. Direct capture comparison gives

    4 Delta_shift(a,c,y)
      = (y-c)Gbar(a) - integral_c^y (7-z)h(z) dz.       (12)

The first term is the delay of positive M2 captures A(1). The second is
the loss when negative M2 starts -z, c<z<y, switch from the late capture
time four to the early time (1+z)/2 on the added inward leg. All remaining changes
vanish in this order of limits. Formula (12) concerns these explicit
representatives; it does not silently transfer them to arbitrary paths
with the same payoff against the unshifted law.

The global scalar maximizer condition makes (12) strictly negative for
every positive extra leg when w0>0. Put q=max(u,c) and write K0=H+L
for the cumulative integral of k=h+ell. The exact derivative in
`SIGNED_M1_FUNCTIONAL.md` can be rewritten as

    4 K_c(a,u,c,y)
      = w0 + [Gbar(a)-(7-c)h(c)] + E(c),

    E(c)=K0bar(q)-(1-q)k(c)>=0.                         (13)

The last inequality follows from q>=c and k nondecreasing. Integrate
(13) from c to y while holding a,u,y fixed. If the starting tuple is a
global scalar maximizer, then

    K(a,u,y,y) <= K(a,u,c,y).

Consequently,

    4 Delta_shift(a,c,y)
      <= -w0(y-c)-integral_c^y E(z) dz
      <= -w0(y-c).                                     (14)

No monotonicity of h alone is used. In particular, a decrease of h near
the endpoint does not invalidate this integrated comparison.

This rules out a matching lower certificate made only from such extra-leg
representatives whenever their positive lengths have positive average
and no other supported representatives offset the same shift. It is not
an exclusion of the entire signed-M1 class. To reach that stronger claim
one would need equality-case control for every near-best response and
a proof that no matching law can be supported on y=c branches. The
quantitative estimates in Section 5 address part of the first issue on
regions with m>0; they do not settle either issue in full.
