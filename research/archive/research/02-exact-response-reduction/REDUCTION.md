# Exact finite-response reductions for the interval Princess--Monster game

## Status and scope

This note proves an exact finite reduction of the princess's best response to **any specified finite family of piecewise-linear monster paths that each guarantee capture by a common horizon**. It also implements the known finite capture-order reduction of the monster's best response to a specified finite hider mixture.

The princess-side result upgrades the earlier deadline-network **relaxation** to an **equality of suprema**. It is not a spatial or temporal discretization of the princess.

All seven initial-position chambers of the previously supplied 32-path monster mixture have been closed, with exact matching flow/deadline certificates and explicit rational approaching paths. This establishes the exact worst-case performance of that particular mixture, not the unrestricted game's value.

**Not established:** a theorem restricting an unrestricted optimal monster to a fixed finite support; a pair of matching saddle-point certificates; the exact value of the unrestricted game. The number of supports must not be silently increased while calling the process a completed finite reduction.

The new converse argument is given below in full. It has not been independently reviewed or formalized in Lean. The code checks exact rational certificates rather than certifying the written argument mechanically.

## 1. Definitions

The arena is [-1,1]. Both paths have speed at most one; the upper-bound argument also permits an arbitrary continuous princess. Capture occurs at the first equality of positions.

Fix monster paths m_1,...,m_N, probabilities w_i >= 0 with sum 1, and a horizon H such that each m_i captures every continuous princess by time H. A sufficient condition is that every monster completes an endpoint-to-endpoint traversal by H. Each m_i is 1-Lipschitz.

An open initial chamber is a component of (-1,1) after deleting all monster starting positions. Fix such a chamber C. Its partition is

    B = {i: m_i(0) < x}, A = {j: m_j(0) > x}, for any x in C.

For i in B let d_i be the first time m_i reaches +1. For j in A let d_j be the first time m_j reaches -1. These deadlines are at most H.

For i in B and j in A let a_ij be their first meeting time, or infinity if they never meet.

Define the compact set of deadline vectors

    R_C = {r in [0,H]^N:
             r_i <= d_i for all i,
             min(r_i,r_j) <= a_ij for every i in B, j in A}.

## 2. Exact deadline theorem

**Theorem 1.** For the specified mixture and chamber,

    sup_{p(0) in C, Lip(p)<=1} sum_i w_i T(m_i,p)
       = max_{r in R_C} sum_i w_i r_i.

The left side is unchanged if the princess is permitted arbitrary continuous paths instead of 1-Lipschitz paths. A maximizing deadline vector need not be realized exactly by one princess path; the assertion is about its supremum.

### 2.1 Necessity

Before capture, the sign of p(t)-m_i(t) cannot change. Thus any surviving monster in B stays below p, and any surviving monster in A stays above p.

If i in B and j in A meet at a_ij, both cannot survive past that time: otherwise

    m_i(a_ij) < p(a_ij) < m_j(a_ij)

would hold while the outside quantities are equal. Therefore min(T_i,T_j) <= a_ij.

A surviving B-monster cannot reach +1 while remaining strictly below the princess. An A-monster cannot reach -1 while remaining above her. Therefore T_i <= d_i.

Every actual capture vector belongs to R_C. This gives the upper inequality, even for arbitrary continuous princess paths.

### 2.2 Constructive converse

Take r in R_C and delta > 0, and put

    e_i = max(0, r_i-delta).

For a B-monster define its downward continuation

    l_i(t) = m_i(t)                         if 0 <= t <= e_i,
             m_i(e_i) - (t-e_i)            if t >= e_i.

For an A-monster define its upward continuation

    u_j(t) = m_j(t)                         if 0 <= t <= e_j,
             m_j(e_j) + (t-e_j)            if t >= e_j.

Set

    L(t) = max(-1, max_{i in B} l_i(t)),
    U(t) = min(+1, min_{j in A} u_j(t)).

Empty maxima/minima leave the corresponding wall. Keep the time-zero constraints even when r_i=0. This ensures that the constructed princess starts in the prescribed chamber.

Each continuation is 1-Lipschitz, and a finite maximum or minimum of 1-Lipschitz functions is 1-Lipschitz.

We claim L(t)<U(t) for every t in [0,H]. Fix i in B and j in A and put e=min(e_i,e_j).

* If e>0, then e<min(r_i,r_j)<=a_ij. Consequently m_i(s)<m_j(s) for 0<=s<=e.
* If e=0, strict ordering holds at time zero because C is an open chamber.
* If the lower constraint expires first, its continuation thereafter falls with speed one. The upper path cannot fall faster than one, so their positive separation cannot vanish before the upper constraint expires.
* If the upper constraint expires first, it rises with speed one; the lower path cannot rise faster. Their separation again persists.
* After both expire, the separation increases.

Likewise l_i(t)<1: before e_i the monster has not reached its upper-wall deadline; after e_i its continuation decreases. Also u_j(t)>-1.

Since there are finitely many curves, these strict pairwise inequalities imply L(t)<U(t). For any prescribed starting point x in C, choose the constant

    lambda = (x-L(0))/(U(0)-L(0)),   0<lambda<1.

The function

    p_delta(t) = (1-lambda)L(t)+lambda U(t)

is a 1-Lipschitz path in [-1,1], starts at x, and satisfies

    p_delta(t)>m_i(t) for i in B, 0<=t<=e_i,
    p_delta(t)<m_j(t) for j in A, 0<=t<=e_j.

Hence T(m_i,p_delta)>=r_i-delta for every i. Extend p_delta constantly after H; all monsters have already captured it by H.

It follows that

    sum_i w_i T(m_i,p_delta) >= sum_i w_i r_i - delta.

Let delta decrease to zero. This proves the converse and the theorem.

This proof is the essential step absent from the earlier relaxation. No proposed turn pattern or grid approximation for the princess is needed.

## 3. Why the optimization is finite

Let E_C consist of 0,H, all finite opposite-side first-meeting times in [0,H], and all wall deadlines. Write its distinct elements as

    0=t_0<t_1<...<t_K=H.

For any r in R_C, round each coordinate upward to the next event time. Every defining inequality is preserved: its right-hand side is itself an event time. The objective cannot decrease.

Therefore the maximum is attained by a vector in the **finite** set

    R_C intersect E_C^N.

For rational piecewise-linear monster paths every event time is rational. This is an exact finite reduction of the specified response problem.

Exhaustive enumeration is unnecessary. Write s_i(k)=1 if r_i>t_k. The survivor labels are nonincreasing in k. For B use the label y_i(k)=s_i(k), and for A use z_j(k)=1-s_j(k). A meeting constraint at t_k becomes

    y_i(k)<=z_j(k).

Together with the time monotonicity and wall constraints these are directed implications. Maximizing the weighted survival durations is a minimum-cut problem. The ordinary weight arcs encode

    H - sum_i w_i r_i.

An implication capacity H+1 is sufficient to force every minimizing cut to respect the implications; the earlier certificates used H, and their correctness here follows directly from a feasible flow plus a feasible matching deadline vector.

An exact certificate consists of:

1. a feasible deadline vector r;
2. a feasible source-to-sink flow F;
3. the exact equality sum_i w_i r_i=H-F.

Weak flow-cut duality gives the upper inequality. The constructive converse gives an approaching princess family attaining the lower inequality in the limit. No claim from a floating-point optimizer is needed.

### Chamber boundaries

At a monster starting position, the corresponding paths capture the princess at time zero. Their time-zero captures satisfy the inequalities of either neighboring chamber after assigning them to that side. Thus neighboring upper certificates cover boundary points. For the global supremum of a fixed mixture, matching approaching paths from the open chambers suffice.

## 4. The seven completed cases

For the earlier 32-path mixture, reflection reduces the initial-position analysis to the following chambers. All the values below are **exact response suprema for that fixed mixture**.

| Chamber | Exact response supremum | Status |
|---|---:|---|
| (0,1/4) | 458409/320000 | Closed |
| (1/4,3/8) | 91681/64000 | Closed |
| (3/8,1/2) | 57301/40000 | Closed |
| (1/2,5/8) | 114601/80000 | Closed |
| (5/8,3/4) | 458403/320000 | Closed |
| (3/4,7/8) | 229201/160000 | Closed |
| (7/8,1) | 229233/160000 | Closed |

The verifier checks the old feasible flows, checks all inequalities of each matching deadline vector, and checks exact equality of objectives. In addition, the package contains constructed rational princess witnesses for delta=1/1000, 1/10000, and 1/1000000 in every chamber. It verifies all their speeds, starting chambers, and all 32 capture times. The all-delta conclusion follows from Theorem 1, not from these three examples alone.

Thus the old strategy's worst-case value really is 229233/160000. A sharper analysis of the same strategy cannot turn it into the solution of the full game.

## 5. Finite unrestricted monster responses

The complementary reduction is based on Proposition 5 of Alpern, Fokkink, Lindelauf and Olsder (2008). Here is the version implemented by the verifier.

**Theorem 2.** Suppose a princess mixture is supported on n specified 1-Lipschitz piecewise-linear paths, with constant tails after their final vertices. An unrestricted monster best response can be found by a finite capture-order search:

* Start at one of the princess starting positions, capturing at least one path at time zero.
* Thereafter move at speed +1 or -1 until the next previously uncaptured princess path is met.
* At each such event, choose the next direction. Do not reverse between capture events.

Every segment captures at least one previously uncaptured path. There are at most n-1 positive-duration capture segments, and no more than n*2^(n-1) terminal direction cases. Coincidences and impossible directions reduce the count.

### Reason for the reduction

For any monster path, move its first capture to time zero by starting on the first captured princess path and, if necessary, shadowing her until the original capture time. This cannot delay any original capture and advances the first one.

At a capture event, consider the next not-yet-captured princess path in the original order. Move directly toward her at maximum speed until meeting her. Because she has speed at most one, the direct pursuit reaches her no later than the original monster did. The monster could then shadow her until the original meeting time and resume the original plan. Any extra intervening captures only improve the payoff.

Repeat the improvement. The same argument removes waiting or turns between successive new captures. At each event there are only two directions to consider. A direction with no remaining princess currently ahead is unnecessary: no such princess can overtake the outgoing speed-one monster from behind, and turning back before a capture is dominated by choosing the useful direction immediately.

For piecewise-linear rational inputs, the next meeting is found by solving linear equations on the finitely many input pieces. Every time and every payoff is rational. `monster_best_response` enumerates these cases using exact fractions, without numerical pruning.

The included four-hider regression has four starting positions, sixteen visited search states, and six terminal cases. All six are exhausted; its exact response value is 151/128. This is a regression problem, not a proposed solution of the full game.

## 6. What these reductions do and do not buy

For a proposed finite monster mixture, Theorem 1 verifies its guarantee against **all** princess paths. For a proposed finite princess mixture, Theorem 2 verifies its guarantee against **all** monster paths. Consequently a genuine matching candidate pair could be certified without proving that arbitrary paths globally have some fixed number of turns.

There is a useful extension for non-attainment. If a proposed n-path princess mixture depends on epsilon, with fixed combinatorial piece structure and rational-function vertices and weights, there are still only finitely many capture-order cases. Within each case, meeting times and payoffs are rational functions of epsilon. All relevant comparisons have eventually constant signs as epsilon tends to zero, except identities, which can be treated separately. Thus its limiting global guarantee can, in principle, be certified by finitely many polynomial sign checks. This is a conditional certificate format, not an assertion that the needed candidate exists.

What is still missing is a matching candidate, or a structural theorem proving that a sufficient bounded-complexity candidate family exists. Neither Theorem 1 nor Theorem 2 supplies a uniform bound on the number of support paths needed for the original minimax problem. Iterating finite best-response computations may generate more and more paths. It is not a completed finite reduction of the entire game until a matching certificate closes or a suitable support/structure theorem is proved.

## 7. Verification

Run:

    python verify_exact.py

Only Python's standard library is required. The default run checks the saved rational paths directly. To reconstruct all envelope paths as well, run `python verify_exact.py --rebuild-witnesses`. Files:

* `exact_oracles.py`: rational path operations, approaching-princess construction, exhaustive monster response.
* `old_strategy_best_responses.json`: seven matching deadline vectors.
* `prior_certificate/`: the earlier monster mixture, network builder and feasible flows.
* `witnesses.json`: the 21 explicitly checked approaching princess paths and their capture times.
* `monster_response_test.json`: exhaustive four-hider test result.
* `verification_output.txt`: saved successful verifier output.

## Sources

S. Alpern, R. Fokkink, R. Lindelauf, G. J. Olsder, "The 'Princess and Monster' Game on an Interval," SIAM Journal on Control and Optimization 47(3), 1178--1190 (2008), DOI 10.1137/060672054. Proposition 5 supplies the finite capture-order reduction underlying Theorem 2. The deadline converse in Theorem 1 is derived in this note; no novelty claim beyond that is made.

The previously generated `interval_pm_proof/PROOF.md` supplied the necessary deadline inequalities and one-sided flow certificate. Its explicit statement that the constraints were a relaxation is strengthened here only for a **specified finite-support monster mixture**.