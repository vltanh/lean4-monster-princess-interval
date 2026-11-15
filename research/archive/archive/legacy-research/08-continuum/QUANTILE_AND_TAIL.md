# Uniform quantile support bounds, an exact continuation game, and a continuum certificate

## Scope

These are structural results for the unrestricted interval game, not an identification of its value. They strengthen the finite approximation argument in `research/06-uniform-finite-reduction/PROOF.md`. In particular, they do not prove a fixed finite support or a fixed finite time horizon sufficient for exact equilibrium.

The arena is `[-1,1]`; both players choose hidden 1-Lipschitz paths and their initial positions; capture includes time zero. Write `T` for first equality, `tau_H = min(T,H)`, `V_H` for the truncated value, and `V` for the unrestricted value. Finite-horizon minimax and the ordered-quantile construction are as proved in the preceding manuscript.

## 1. The continuation game from a fixed monster position has exact value 2

**Theorem 1.** If the monster is required to start at a specified position `x`, while the princess can choose her starting position and path, the value is exactly `2`, for every `x` in `[-1,1]`.

### Upper guarantee

Independently choose with probability `1/2` each:

* go right at unit speed to `+1`, then left to `-1`;
* go left at unit speed to `-1`, then right to `+1`.

If the princess starts above `x`, the right-first path captures by time `1-x`, since a continuous princess cannot remain strictly above it when it reaches `+1`. The left-first path captures by time `(1+x)+2 = 3+x`. Their average is at most `2`.

If she starts below `x`, the corresponding bounds are `3-x` and `1+x`, also averaging to `2`. A princess starting exactly at `x` is captured immediately. No restriction on her subsequent number of turns is used; the upper proof even permits arbitrary continuous princess motion.

### Matching lower guarantee

First suppose `-1 < x < 1`. Choose any `0 < epsilon < min(1-x,1+x)`. Let `p_+` start at `x+epsilon`, run right at unit speed to `+1`, and remain there. Let `p_-` start at `x-epsilon`, run left at unit speed to `-1`, and remain there. Give these two paths probabilities

    w_+ = (1-x)/2,       w_- = (1+x)/2.

Before `p_+` reaches its endpoint, a monster starting at `x` remains strictly behind it: `m(t) <= x+t < x+epsilon+t`. Hence the monster captures `p_+` only by visiting `+1`. Similarly it captures `p_-` only by visiting `-1`.

If the monster visits `+1` first, the two capture times are at least `1-x` and `3-x`. Its expected payoff is therefore at least

    (1-x) + 2 w_- = 2.

If it visits `-1` first, the analogous lower bound is

    (1+x) + 2 w_+ = 2.

If it never visits one of the two endpoints, its expected payoff is infinite. These pointwise inequalities also hold against mixed monster strategies.

For `x=+1`, one princess starting at `1-epsilon` and running left to `-1` has first capture time at least `2`; for `x=-1`, reflect this construction. This proves the theorem, including the endpoints. The interior construction is an actual two-path strategy for any allowed positive `epsilon`, not just a limiting strategy.

## 2. Improved truncation inequality

**Corollary 2.** For every `H>0`,

    V_H <= V <= (1+2/H) V_H.

Take any truncated monster strategy, use it through time `H`, then independently apply the equiprobable two-sweep continuation in Theorem 1 from its current position. For each fixed princess path, condition on the realized monster prefix. If capture has not occurred, its conditional expected remaining time is at most `2`. Thus

    E T(extended M,p)
      <= E min(T(M,p),H) + 2 Pr(T(M,p)>H)
      <= (1+2/H) E min(T(M,p),H).

Taking infima gives the upper inequality. This improves the preceding manuscript's factor `1+3/H`; all its arguments that use that factor remain valid with the sharper one.

The number `2` is the optimal uniform continuation constant when one knows only the current monster position. The lower strategy in Theorem 1 shows that no smaller bound can hold uniformly for such continuation games. This statement does **not** assert sharpness of the multiplicative inequality for `V_H`.

For reference, `V <= 3/2`: equiprobable full sweeps starting at the two endpoints each finish by time `2`; because the two monster paths meet at time `1`, at least one has captured any continuous princess by that time. Their two capture times sum to at most `3`. Consequently

    0 <= V - V_H <= 2V/(H+2) <= 3/(H+2).

## 3. Equally weighted quantiles approximate all monsters simultaneously

Let an admissible princess law have time-marginal CDF `F(t,x)`, and replace it by its ordered quantile coupling `Q(t,q)`. This can only increase its capture payoff against every monster. For integer `n>=1`, select the fixed quantile levels

    q_i = (i-1/2)/n,       i=1,...,n,

and give the `n` admissible paths `Q(t,q_i)` equal weights `1/n`. Repeated paths are permitted.

**Theorem 3.** For every monster path `m`, uniformly over its starting position, speed-bounded motion, and number of turns,

    | E_q tau_H(m,Q(.,q))
      - (1/n) sum_i tau_H(m,Q(.,q_i)) | <= H/n.

### Proof, including atoms and touching

At a fixed time `t`, the quantiles that have been captured by `m` form an interval of quantile levels, possibly with either endpoint included or excluded. Indeed, a surviving ordered continuous path stays strictly below `m` throughout `[0,t]`, or stays strictly above it. The first set is an initial interval in `q`, and the second set is a final interval. Their complement is the captured interval.

For every interval `A` in `[0,1]`, with arbitrary endpoint conventions,

    | length(A) - #(i : q_i in A)/n | <= 1/n.

This follows by subtracting the two one-sided empirical-CDF discrepancies, each of which is at most `1/(2n)` for midpoint quantiles. A singleton interval containing a midpoint is included in this estimate, so atoms and an exact touching quantile cause no exception.

Apply this inequality to the captured interval for each `t`, or equivalently to its surviving complement, and integrate from `0` to `H`. The layer-cake identity for `tau_H` gives the asserted bound. No continuity assumption for capture time as a function of paths is used.

Define

    A_n(H) = sup over n admissible paths p_1,...,p_n
             inf over monsters m of (1/n) sum_i tau_H(m,p_i).

Using arbitrarily near-optimal truncated princess laws gives

    V_H - H/n <= A_n(H) <= V_H.

The approximating support size is `n`, independent of spatial or temporal mesh size. The paths themselves still belong to an infinite-dimensional Lipschitz class.

## 4. An explicit full-game finite-support bound

Let

    L_n = sup over n admissible paths p_1,...,p_n
          inf over monsters m of (1/n) sum_i T(m,p_i).

Since `T >= tau_H`, Theorems 2 and 3 give, for every `H>0`,

    0 <= V-L_n <= 3/(H+2) + H/n.

For `n>=2`, choose `H=sqrt(3n)-2>0`. Then

    0 <= V-L_n <= 2 sqrt(3/n) - 2/n.

In particular, `n >= 12/epsilon^2` suffices for an equally weighted `n`-path princess family whose guarantee approaches within `epsilon` of `V` (with an arbitrarily small additional error if the supremum is not attained).

This is an approximation theorem, not an exact support cutoff. Even for fixed `n`, arbitrary Lipschitz path shapes remain to be optimized. It does not discharge the roadmap's request for a finite terminating exact certificate.

## 5. A finite-control continuum lower-certificate theorem

The CDF formulation also supplies a way to verify a proposed continuum princess law without an unsupported turn bound. The following smooth version states the certificate explicitly; constructing a matching certificate remains open.

Suppose `F` is a continuously differentiable family of atom-free CDFs on `[0,H] x [-1,1]`, with

    F_x >= 0,        |F_t| <= F_x,
    F(t,-1)=0,      F(t,1)=1.

Its quantile paths are admissible. For a monster path define

    a(t) = min_{0<=s<=t} F(s,m(s)),
    b(t) = max_{0<=s<=t} F(s,m(s)).

The survival probability is `1-b(t)+a(t)`. Let `U(t,x,a,b)` be continuously differentiable on a neighborhood of the feasible domain `0<=a<=F(t,x)<=b<=1`. Assume:

1. `U(H,x,a,b) <= 0` on the feasible terminal domain.
2. `U(0,x,F(0,x),F(0,x)) >= c` for every initial point `x`.
3. For every feasible state and every velocity `v` in `[-1,1]` (restricted to inward velocities at arena endpoints), put

       g = F_t(t,x) + v F_x(t,x),
       alpha = min(g,0) if a=F(t,x), and 0 otherwise,
       beta  = max(g,0) if b=F(t,x), and 0 otherwise.

   Require

       U_t + v U_x + alpha U_a + beta U_b + 1-b+a >= 0.

**Theorem 4.** These conditions imply that this princess law guarantees `E tau_H >= c` against every admissible monster, and therefore `V >= c`.

### Proof

Along any absolutely continuous monster path, `f(t)=F(t,m(t))`, its running minimum `a`, and its running maximum `b` are absolutely continuous. Almost everywhere,

    f'=F_t+m'F_x,
    a'=min(f',0) on {a=f}, and a'=0 elsewhere,
    b'=max(f',0) on {b=f}, and b'=0 elsewhere.

The chain rule and condition 3 give

    d/dt U(t,m(t),a(t),b(t)) >= -(1-b(t)+a(t)).

Integrating, then using conditions 1 and 2, yields

    E tau_H = integral_0^H (1-b+a) dt
             >= U(0,m(0),F(0,m(0)),F(0,m(0)))
                - U(H,m(H),a(H),b(H))
             >= c.

### Why only finitely many control velocities need checking

At a fixed feasible state, the left side in condition 3 is piecewise affine in `v`. Let `I_x` be the admissible velocity interval: `[-1,1]` when `-1<x<1`, `[0,1]` at `x=-1`, and `[-1,0]` at `x=+1`. Its only possible interior breakpoint is

    v_0 = -F_t/F_x,

when `F_x>0`. The speed inequality ensures `v_0` lies in `[-1,1]`. Therefore it is enough to check both endpoints of `I_x`, together with `v=v_0` if it is defined and belongs to `I_x`. If `F_x=0`, then `F_t=0`, so the expression is affine and the endpoints of `I_x` suffice. In particular, `v=0` must be checked at an arena endpoint even when `F_x=0` and the formula for `v_0` is undefined.

The state domain is still continuous; these are not three exhaustive game cases. A specified piecewise algebraic `F,U`, with correct interface conditions, could in principle reduce these inequalities to finite exact sign certificates. This theorem provides a certificate format; it does not assert existence of such a finite algebraic equilibrium or supply an exact constant.

## 6. Exact terminal cost for a full-payoff continuum certificate

The preceding smooth certificate uses a zero terminal bound and therefore certifies a truncated payoff. There is a stronger version for a princess law whose paths have all reached fixed endpoints by time `H`. It certifies the **full** expected capture time and does not require an identity such as `V=V_H`.

### 6.1 The exact two-endpoint continuation cost

Suppose the current monster position is `x`, the total probability mass of uncaptured princess paths fixed at `-1` is `a`, and the total uncaptured mass fixed at `+1` is `1-b`. These are unconditioned masses, so their sum may be less than one. The minimum additional contribution to the expected capture time is exactly

    W(x,a,b) = min{
        (a+1-b)(1+x) + 2(1-b),
        (a+1-b)(1-x) + 2a
    }.

The first expression visits `-1` first; the second visits `+1` first. Each is attained by direct unit-speed travel to the first endpoint and then to the other. Every other route visits one endpoint first, so the speed bound gives at least the corresponding expression. If an endpoint has no uncaptured mass, direct travel to the other endpoint gives the same minimum. If positive uncaptured mass is never visited, the remaining expected payoff is infinite and the lower bound still holds.

### 6.2 Capture at time H must be applied before evaluating W

Let `pi` be the probability of a terminal princess location at `-1`. Ordered quantiles with labels below `pi` end at `-1`, and those above `pi` end at `+1`, apart from an irrelevant single label. Let `a_-` and `b_-` be the limits of the running surviving-left and captured-upper bounds as time increases to `H`, before the final-time capture is applied. The post-capture state `(a_H,b_H)` is

| Monster position `x_H` | `a_H` | `b_H` |
|---|---:|---:|
| `-1 < x_H < 1` | `a_-` | `b_-` |
| `x_H = -1` | `0` | `max(b_-,pi)` |
| `x_H = +1` | `min(a_-,pi)` | `1` |

For an interior terminal position, admissibility and path continuity ensure `a_- <= pi <= b_-`. At `x_H=-1`, all remaining terminal-left paths are captured at `H`, including any that were above the monster immediately before `H`; similarly at `+1`. The maximum and minimum in the endpoint rows therefore cannot be omitted.

For example, a monster approaching `-1` while remaining below all left-ending princesses may have `b_-<pi`; simply using `W(-1,a_-,b_-)` would wrongly charge future search time for princesses captured at `H`.

### 6.3 A rigorous smooth-to-terminal limiting theorem

Assume `F` satisfies the smooth hypotheses of Section 5 on every compact subinterval `[0,h]` with `h<H`, rather than necessarily at `H`. Assume its ordered quantile paths extend continuously to `H` and are then fixed at `-1` or `+1`. In particular, terminal atoms are allowed even though the preterminal marginals are atom-free.

Let `U` satisfy the initial inequality and the differential inequality of Theorem 4 for `t<H`. Replace the zero terminal condition by the following upper-trace condition. Whenever feasible preterminal states converge to `(H,x,a_-,b_-)`, require

    limsup U(t,x_t,a_t,b_t) <= W(x,a_H,b_H),

where `(a_H,b_H)` is the post-capture state in the table. Only compatible terminal tuples need be checked. A sufficient implementation is an upper boundary extension of `U` bounded by the displayed endpoint-adjusted formula.

**Theorem 5.** These conditions imply `E T(m,Q) >= c` for every unrestricted monster path `m`.

**Proof.** Integrate the differential inequality to each `h<H` as in Theorem 4. Let `h` increase to `H`. The prefix survival integral converges, and the running minimum and maximum have limits by monotonicity. The upper-trace condition gives

    E min(T(m,Q),H) + W(m(H),a_H,b_H) >= c.

Conditional on a particular surviving quantile, the princess is fixed at the appropriate endpoint from time `H` onward. Section 6.1 therefore gives

    E T(m,Q)
      >= E min(T(m,Q),H) + W(m(H),a_H,b_H)
      >= c.

This proves a full-payoff lower bound without bounding the monster's capture horizon. The terminal cost is the exact best continuation value, not a truncation-error estimate.

### 6.4 Finite atoms and capture interfaces

A candidate may have endpoint atoms or other moving atoms before `H`, so the purely smooth hypotheses can be too restrictive. At the initial time, capture of an atom at the monster's starting point must already be applied: the initial condition is

    U(0,x,F(0,x-),F(0,x)) >= c,

rather than putting both bounds equal to `F(0,x)`. Here the running bounds throughout the path use `F(t,m(t)-)` for the lower bound and `F(t,m(t))` for the upper bound, as in the exact quantile survival formula.

The certificate extends whenever, along every admissible monster path, the composite potential

    u(t)=U(t,m(t),a(t),b(t))

is absolutely continuous between its finitely many jumps, satisfies

    u'(t) >= -(1-b(t)+a(t))

almost everywhere between jumps, and obeys the interface inequality

    u(t+) >= u(t-)

at every jump, including any formula-interface jump. An atom captured at time `t` contributes no additional elapsed time at that instant, which explains this direction of the inequality. For finitely many atomic trajectories there are only finitely many such first-capture jumps. Piecewise smooth candidate formulas must separately justify the stated absolute continuity and the interface inequalities; an almost-everywhere differential check alone is insufficient if a singular continuous variation is possible.

Integrating on the intervening intervals and adding the jump inequalities gives exactly the same bound. At `H`, apply the post-capture update before using `W`, or impose the corresponding upper-trace condition directly. This is a precise extension criterion, not a claim that every nonsmooth CDF automatically meets it.

## 7. What remains open

Symmetry and quantile ordering do not imply a fixed bound on the number of useful monster turns or the time of its last capture. The independent stationary-shell construction in the structural audit gives symmetric ordered laws whose optimal responses have arbitrarily large values of both quantities. It does not prove that an equilibrium of the full game needs an unbounded horizon; it rules out deriving a cutoff from symmetry and ordering alone.

The missing exact-value step remains a matching unrestricted upper/lower certificate, or a structural theorem specific enough to imply one. The improved tail estimate and quantile support bound give controlled approximation. The Bellman inequality gives another possible verification route once an exact continuum candidate is known.
