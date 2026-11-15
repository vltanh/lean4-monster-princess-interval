# Interval Princess–Monster: a uniform finite approximation theorem and exact response certificates

## Status and scope

**The exact unrestricted minimax value has not been identified. This document is not a full-game saddle-point proof.**

The main mathematical result below differs from the earlier fixed-support response reductions: it constructs finite games that approximate the **entire unrestricted game**, with an explicit error uniform over all opposing paths. It does not prove that any one finite game already has the unrestricted value.

The computational work also supplies (i) an exact all-monster response calculation for a specified 338-path princess distribution, and (ii) a completely enumerated, rational saddle certificate for a small finite grid game. Neither number is asserted to be the unrestricted value. Larger flow-network equilibrium searches remained unmatched on the unrestricted princess side.

The analytic arguments are written proofs, not Lean formalizations. The exact verifiers check arithmetic and finite response cases; they do not mechanically certify the continuous-to-finite theorems. No independent review or literature-priority claim is made.

## 1. Rules and notation

The arena is I=[-1,1]. Each player independently selects a hidden path, including its starting position. Both paths have Lipschitz constant at most one. Capture includes time zero and occurs at the first equality:

    T(m,p) = inf {t >= 0 : m(t)=p(t)}.

The monster minimizes and the princess maximizes expected capture time. Write V for the unrestricted value. For H>0, write

    tau_H(m,p) = min(T(m,p),H),

and V_H for the finite-horizon value. Pure paths are extended constantly when a finite description ends.

All finite computational strategies in this package obey these rules. No speed advantage, prescribed start, observation, or positive detection radius is introduced.

## 2. Ordered quantiles give an exact description of hiding by its time marginals

Let a princess distribution have time-marginal cumulative distribution function

    F(t,x) = Pr(P(t) <= x).

Let F(t,x-) denote its left limit in x. Its quantile coupling is

    Q(t,q) = inf{x : F(t,x) >= q},   0<q<1,

with one uniform random q selected at time zero and retained for the entire path.

### Lemma 1: quantile paths remain admissible

If the original random paths have speed at most one, then, with d=|t-s|,

    F(s,x-d) <= F(t,x) <= F(s,x+d).

Indeed, P(s)<=x-d implies P(t)<=x, and P(t)<=x implies P(s)<=x+d. The corresponding quantile inequalities give

    |Q(t,q)-Q(s,q)| <= |t-s|.

Thus every quantile path is admissible. Quantile paths are ordered: q<r implies Q(t,q)<=Q(t,r) for every t.

### Lemma 2: the quantile coupling weakly improves hiding against every monster

Fix m and t. A continuous princess path not captured by t must remain strictly below m throughout [0,t], or remain strictly above it throughout that interval. The probabilities of these two events are respectively at most

    L_F(m,t) = inf_{0<=s<=t} F(s,m(s)-),
    1-R_F(m,t), where R_F(m,t)=sup_{0<=s<=t}F(s,m(s)).

For the quantile coupling these bounds hold with equality in probability. The quantiles below m at every time form an initial interval of q-values of length L_F; those above m at every time form a final interval of length 1-R_F. Endpoint conventions affect at most one q at each of the two resulting interval boundaries, hence do not affect their probabilities.

Consequently, the quantile coupling has survival probability

    Pr(T(m,Q)>t) = 1-R_F(m,t)+L_F(m,t),

at least as large as that of the original coupling. In particular,

    J_H(F,m) := E tau_H(m,Q)
              = integral_0^H [1-R_F(m,t)+L_F(m,t)] dt.        (1)

This argument allows atoms and tangential contacts. The left limit in L_F is essential: an atom lying exactly on the monster is captured.

### Consequences

The princess can be represented by a family of marginal CDFs satisfying the speed inequalities, rather than a probability measure on an unrestricted collection of paths. Conversely, such a family is realized by the admissible quantile coupling.

For a fixed m, (1) is concave in F: a running supremum is convex and a running infimum is concave. The feasible marginal families form a convex set. The unrestricted princess problem therefore becomes a concave maximization with monster paths providing separation constraints.

In characteristic coordinates u=t+x, v=t-x, the speed inequalities say that F is nondecreasing in u and nonincreasing in v. Where derivatives exist, they read |F_t|<=F_x. These are alternative descriptions, not assumptions of differentiability.

This extends the usual finite uncrossing observation to arbitrary path distributions and retains the exact capture payoff. The finite uncrossing and capture-order principles appear in Alpern–Fokkink–Lindelauf–Olsder, Propositions 7 and 5 respectively; the formula and approximation argument here are proved directly.

## 3. A uniform bound for truncating time

### Lemma 3: finite-horizon minimax

The finite-horizon monster path space is compact under uniform convergence, by the speed bound and the bounded arena. The payoff tau_H is bounded and lower semicontinuous: if capture has not occurred by some r<H, the absolute separation on the compact interval [0,r] has a positive minimum, and sufficiently small uniform perturbations preserve noncapture through r.

For any finite collection of princess paths, minimax follows by the finite-dimensional mixed-hider simplex and the compact convex space of monster probability measures; expected payoffs are lower semicontinuous in the latter and affine in both mixed strategies. Equivalently one can separate the convex upper payoff set.

For each princess path p, the set of monster measures satisfying E tau_H(M,p)<=a is closed. If a exceeds the supremum of the finite-hider lower values, these sets have the finite intersection property. Compactness gives a monster measure satisfying every such inequality. Letting a decrease proves minimax for the full truncated game and shows that finite princess distributions approach V_H.

This supplies the minimax property used below without assuming an optimal finite princess support.

### Lemma 4: truncation error

For every H>0,

    V_H <= V <= (1+3/H) V_H.                              (2)

To obtain the upper inequality, use an optimal (or arbitrarily near-optimal) truncated monster distribution until H. At time H, each monster goes to its nearer endpoint and then traverses the entire interval. This takes at most 1+2=3 additional time units and guarantees capture of every continuous princess still uncaptured.

For every p,

    E T(extended M,p)
      <= E min(T(M,p),H) + 3 Pr(T(M,p)>H)
      <= (1+3/H) E min(T(M,p),H).

The second inequality uses H Pr(T>H)<=E min(T,H). The lower inequality in (2) follows by truncating the payoff.

There is no need to assume in advance that the unrestricted game has a value: its lower value is at least V_H and its upper value is at most the right side of (2). Since V_H<=2 (one endpoint-to-endpoint sweep suffices), their difference tends to zero. Thus the common unrestricted value exists and satisfies (2).

## 4. Regularizing without assuming continuity of capture times

A small perturbation of a path can cause a large capture-time jump. Ordinary uniform path approximation alone is therefore insufficient. The following random spatial translation controls the CDF instead.

Fix 0<delta<1 and put s=1-delta. From any princess path p form

    p_Z(t) = s p(t/s) + Z,

where Z is independently uniform on [-delta,delta]. The path stays in [-1,1] and has speed at most one.

### Lemma 5: the regularization loses at most the scale factor

For a fixed monster m and fixed Z, define

    mhat_Z(u) = projection_to_[-1,1]((m(su)-Z)/s).

This is an admissible monster path. Any actual meeting of m with p_Z at time t produces a meeting of mhat_Z with p at time t/s. Projection might cause an earlier meeting, but cannot invalidate this implication. Hence

    T(m,p_Z) >= s T(mhat_Z,p),

and therefore

    min(T(m,p_Z),H) >= s min(T(mhat_Z,p),H).

Starting with an eta-optimal truncated princess distribution gives a regularized distribution guaranteeing at least s(V_H-eta), uniformly against every monster.

At every time its spatial marginal is a convolution with the uniform law on [-delta,delta]. Thus its CDF is Lipschitz in x with constant at most

    1/(2 delta).                                         (3)

Apply the quantile coupling of Section 2. This preserves all marginal CDFs, preserves (3), and can only improve the hiding guarantee.

The original paths can be extended constantly beyond H before the contraction; the comparison above only uses their original guarantee up to H.

## 5. A uniform spatial and temporal grid approximation

Take integers K,N>=1 and define

    h=2/K,      H=N h,
    spatial grid = {-1+jh : j=0,...,K}.

A grid princess chooses one grid position at each time kh, k=0,...,N, with successive positions differing by -h,0,or h, and interpolates linearly. Thus there are at most (K+1)3^N grid paths.

For a quantile path Q from the regularized law, round its sampled positions downward to this spatial grid, then interpolate. Call the resulting path Q_h.

Adjacent samples of Q differ by at most h. Their grid indices consequently differ by at most one, so Q_h is admissible. Downward rounding is monotone in Q, so the quantile paths remain ordered.

The chord of a 1-Lipschitz path on an interval of length h differs from it by at most h/2; rounding its two endpoints contributes less than h. In particular, the convenient uniform bound

    |Q_h(t,q)-Q(t,q)| <= 2h                               (4)

holds for every q and t in [0,H].

Combining (3) and (4), both the right and left grid CDF limits obey

    |F_h(t,x)-F(t,x)| <= h/delta,
    |F_h(t,x-)-F(t,x)| <= h/delta.                        (5)

For example, F(t,x-2h)<=F_h(t,x-)<=F_h(t,x)<=F(t,x+2h); continuity and (3) give (5).

The running supremum and infimum in (1) each change by at most h/delta. Thus, **uniformly over every admissible monster path**,

    |J_H(F_h,m)-J_H(F,m)| <= 2Hh/delta.                   (6)

Let W_{K,N} be the maximum guarantee of all grid princess mixtures against unrestricted monsters for the truncated payoff. Let eta tend to zero in Lemma 5. Then

    (1-delta)V_H - 2Hh/delta <= W_{K,N} <= V_H.           (7)

This is the key uniform statement absent from a fixed-support response calculation.

## 6. The grid-hider game is itself an exact finite matrix game

There is no additional approximation on the monster side.

Against any mixture on a finite set of unit-speed-bounded hider paths, a best monster response can start at a hider starting position and then move at speed +1 or -1, turning only at a new capture. One way to see the reduction is to start on the first captured hider at time zero, shadow her if needed, and successively replace each segment to the next captured path by direct speed-one pursuit. Direct pursuit cannot arrive later; any incidental captures only help. The same argument works for the truncated payoff by ignoring events after H.

For grid princess paths, the line intercepts t+x and t-x of moving pieces, and the stationary spatial coordinates, lie in the common coset -1+h Z. (The two intercept signs give the same coset because 2=K h.) A canonical monster starts on the spatial grid and hence has its initial line intercept in that coset. At a meeting of opposite-moving pieces, the time is half the sum of two such intercepts, and is therefore a multiple of h/2. At a stationary-hider meeting the same conclusion holds. After a turn the monster's new line intercept is again in -1+h Z: it either equals the moving hider's intercept or differs from the previous intercept by twice a grid position, with the appropriate sign. Coincident pieces first meet at the current event or a piece endpoint, with the same lattice property. This argument covers odd as well as even K; it does not assume that -1 is an integer multiple of h.

It follows inductively that every useful monster turn occurs on the half-time lattice:

    t in (h/2) Z,   x in (h/2) Z.

Thus the following finite family contains a best response to **every weighting** of the grid hiders:

* start at one of the K+1 h-grid positions;
* take 2N steps of duration h/2;
* move at speed +1 or -1 on each step and remain in [-1,1].

There are at most (K+1)2^(2N) such paths. A canonical response finishing its useful captures early can be extended by harmless bounded half-grid motion. The finite game's payoffs are multiples of h/2, capped at H. Its minimax value W_{K,N} is therefore rational and admits an exact finite primal–dual certificate.

The large upper bounds on the family sizes are not efficiency claims. Capture-order search, CDF flow variables, and constraint generation can avoid enumerating most of these paths in practice.

## 7. Uniform finite approximation theorem for the full game

Combining (2) and (7) proves:

> **Theorem.** For h=2/K, H=Nh and every 0<delta<1,
>
>     W_{K,N} <= V <= (1+3/H) (W_{K,N}+2Hh/delta)/(1-delta).    (8)
>
> Here W_{K,N} is the exact value of the finite matrix game described in Section 6. The inequality applies to the unrestricted interval game, not merely a fixed proposed support.

For an entirely explicit sequence, take an integer n>=2 and set

    H=n,  h=1/n^3,  K=2n^3,  N=n^4,  delta=1/n.

Write W_n for the associated finite-game value. Then

    W_n <= V <= ((n+3)/(n-1)) (W_n+2/n),                  (9)

and, using W_n<=2,

    0 <= V-W_n <= (10n+6)/(n(n-1)) <= 26/n.              (10)

Thus the unrestricted value is a computable real with explicit finite rational enclosures. No unexplained discretization-convergence assumption is needed.

**What (8)-(10) do not establish:** a fixed finite K,N with W_{K,N}=V; a closed-form or evaluated exact constant; a full-game saddle point; finite termination of the earlier double-oracle loop. An unevaluated convergent sequence is not being presented as the exact-value answer requested in the conversation.

## 8. The stronger path-network computation used in the search

The experimental implementation does not merely reweight the listed princess paths. It constructs their planar spacetime graph, subdividing every intersection and permitting every path obtained by switching at intersections.

Assign a CDF potential to each open face. The difference between potentials immediately to the right and left of a directed path edge is its probability mass. Nonnegative edge masses impose order inequalities; flow conservation follows by telescoping the face potentials around each vertex. Conversely, the ordered quantile construction decomposes any feasible potential assignment into admissible paths on the graph.

For a fixed monster path, its visits to faces and edges determine the CDF values in (1). Auxiliary running-upper and running-lower variables make the survival objective a finite linear program. To separate a proposed flow, its quantile decomposition is sent to an unrestricted finite-hider monster-response search. All relevant geometry was retained as integers or exact polynomial coefficients; exploratory LP objectives and their comparisons were floating point.

This includes many more trajectories than the basis list, but it remains a restricted graph until one applies a uniform mesh theorem or verifies matching unrestricted responses. A numerical equilibrium on one graph alone is not a solution of the full game.

The adaptive graph experiments generated stronger strategies but their dual monster mixtures still had substantially larger unrestricted princess responses. The final search logs are included as research data, not proof certificates.

## 9. Exact unrestricted response check produced by the computation

`princess_strategy.json` specifies 169 nonnegative paths and positive integer weights summing to 100,000,000. Select a listed path according to these weights, then select it or its reflection with equal probability. Coordinates are integers divided by 256,000,000. All paths have slopes 0,+1,-1 and stay in [0,1] before reflection; their final constant tails lie at +1.

The exact unrestricted monster-response value of this particular 338-path distribution is

    c = 36290299773897097 / 25600000000000000
      = 1.4175898349178553515625.

One attaining monster route has vertices

    (0, 11/16),
    (107999999/128000000, -19999999/128000000),
    (127999999/64000000, 1),
    (255999999/64000000, -1).

The first coordinate is time. Direct Fraction-based intersections with all 338 hider paths give exactly c.

The complete response search has:

    visited states:                 48,228
    completed terminal routes:           7
    exact dominance eliminations:   21,262
    exact lower-bound eliminations:   2,904.

These counts are not an assertion that there are only seven possible monster routes. Every other branch is eliminated by a proved comparison. The node cap was not reached.

### Why the response search is exhaustive

For ordered hiders, the set captured by a continuous monster is a contiguous interval of hider indices. At a state the monster chooses left or right and captures the next uncaptured adjacent path, possibly capturing several coincident paths together. Every segment expands the captured interval, so the tree is finite.

A state with accumulated weighted capture cost C has the rigorous continuation lower bound

    C + sum_{uncaptured j} w_j * earliest_possible_meeting_time(j).

Direct speed-one travel toward a hider gives that earliest time. Branches whose exact bound is at least an already attained complete value cannot improve the minimum.

For dominance, states with the same captured interval and current anchor hider are compared. An earlier state with no greater accumulated cost can shadow its anchor until the later time and then imitate the later continuation. Incidental captures only help. Hence the later state cannot have a smaller optimum.

All weights, event coordinates, costs, and pruning comparisons in `exact_response.py` are integers. A factor of two clears the slopes of inverse characteristic functions. The cached lower-bound sums are piecewise affine generalized inverses, evaluated exactly. The optional naive implementation sums every individual earliest-meeting bound instead.

Python and C++ exact implementations return the same value, route cost, and search counts. Cached and naive integer bounds also agree. Forty small generated cases agree with unpruned exhaustive search, and forty CDF survival identities agree with direct Fraction-based capture-time integration.

This is a lower certificate for the full game, not a proposed exact value. No monster mixture attaining this same unrestricted upper guarantee has been supplied.

### Exact rejection of the proposed monster counterpart

`rejected_dual.json` gives a rationalized version of the graph LP's dual monster candidate: 164 reflected pairs, with positive pair-weight numerators summing to 1,000,000,000. It also gives one admissible princess path. Direct exact intersections give its expected capture time

    1674493271312017851 / 1024000000000000000
      = 1.6352473352656424...,

strictly above both 8/5 and c. `check_rejected_dual.py` checks every path's admissibility, every capture time, and this equality using only exact fractions. Thus this particular monster candidate does not match the princess guarantee. This rejects a specified weighting, not all reweightings of its support; the displayed payoff is not a lower bound for the unrestricted game.

## 10. A fully enumerated finite-grid regression

For K=4, N=4, the mesh is h=1/2 and the truncated horizon is H=2. `grid_case.json` contains exact rational mixed strategies with

    W_{4,4} = 227/196.

The verifier enumerates all 259 admissible grid princess paths and all 720 admissible half-grid monster paths. It checks every inequality against the supplied rational strategies, obtaining matching lower and upper values. There is no floating-point tolerance in this check.

This small value is a test of the finite construction and certificate machinery. It is not V, and its coarse parameters do not give a useful numerical approximation to V through the conservative general error estimate.

## 11. What remains to close the requested problem

The earlier missing justification for finite discretization is now replaced by the explicit uniform estimate (8). That supports a guaranteed approximation procedure for the full game.

Exact closure still needs one of the following mathematical results:

* matching unrestricted monster and princess guarantees at a specified constant; or
* a structural theorem reducing the continuum optimization to a sufficient finite collection of parameterized cases, followed by exact solution of those cases.

Neither was established by this run. The finite-grid regression, the 338-path exact response, and the larger numerical graph equilibria must not be confused with those missing statements.

## 12. Reproduction and file roles

Run, using only Python's standard library:

    python verify.py
    python tests.py

To repeat the main exact response using uncached lower bounds:

    python exact_response.py princess_strategy.json --naive

`finite_grid.py --discover` reconstructs the small-grid certificate with SciPy and then checks it exactly. SciPy is not required by `verify.py` or `tests.py`.

An optional second implementation is `exact_ordered.cpp` (C++17 and Boost multiprecision headers). The Python verifier does not depend on it.

The `research/` directory contains discovery scripts, numerical logs, and selected checkpoints. These are not part of the exact verification claim. Their LP solutions and response objectives must not be promoted to exact statements without separate certification.

### Attribution

S. Alpern, R. Fokkink, R. Lindelauf, G. J. Olsder, “The ‘Princess and Monster’ Game on an Interval,” SIAM Journal on Control and Optimization 47(3), 1178–1190 (2008), DOI 10.1137/060672054. The 2006 preprint contains the capture-order result as Proposition 5 and the finite uncrossing result as Proposition 7. The arguments needed for the uniform estimate are provided above rather than inferred from a numerical discretization.
