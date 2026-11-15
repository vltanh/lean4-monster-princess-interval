# A certificate for an unrestricted interval Princess--Monster upper bound

## Status

This is a partial result, not a solution of the minimax game. It proves an upper bound against every continuous princess trajectory:

\[
V\le \frac{229233}{160000}=1.43270625.
\]

The princess is not restricted to a discretized path class, a prescribed number of turns, or a prescribed speed. In particular, the certificate applies to the equal-unit-speed game. The monster mixture is explicitly specified below. This work does not supply a matching lower bound. The earlier proposed lower bound 1.37 and the restricted numerical value near 1.3727 are not promoted to unrestricted equilibrium results here.

The mathematical reduction and exact flow checks were developed and checked in this session. No Lean formalization or independent external review has been performed.

## 1. Model and notation

A monster path m is a 1-Lipschitz function from nonnegative time to [-1,1]. A princess path p is any continuous function with the same range. Starting points are chosen independently as part of the players' strategies. Capture is at the first exact meeting:

\[
T(m,p)=\inf\{t\ge0:m(t)=p(t)\}.
\]

The monster minimizes expected capture time and the princess maximizes it. Let V denote the minimax value. For an upper bound it is enough to exhibit one monster distribution nu and prove E_nu[T(m,p)] <= U for every p. No reduction of the full monster strategy space is needed for this implication.

## 2. The explicit monster distribution

Let H=4. For -1 <= x < 1 define two paths:

\[
M_1(x;t)=\begin{cases}
x+t,&0\le t\le1-x,\\
2-x-t,&1-x\le t\le3-x,\\
-1,&3-x\le t\le4,
\end{cases}
\]

and

\[
M_2(x;t)=\begin{cases}
x+t,&0\le t\le(1-x)/2,\\
1-t,&(1-x)/2\le t\le2,\\
t-3,&2\le t\le4.
\end{cases}
\]

The monster selects a row with probability equal to its listed integer divided by 10000. Within that row it selects the displayed path or its reflection with equal probability. There are 16 rows, hence 32 actual paths.

| Family | Starting point x | Integer mass |
|---|---:|---:|
| M1 | -1 | 7507 |
| M1 | 5/8 | 149 |
| M1 | 3/4 | 171 |
| M1 | 7/8 | 188 |
| M2 | -7/8 | 153 |
| M2 | -3/4 | 150 |
| M2 | -5/8 | 147 |
| M2 | -1/2 | 143 |
| M2 | -3/8 | 143 |
| M2 | -1/4 | 122 |
| M2 | 1/4 | 228 |
| M2 | 3/8 | 271 |
| M2 | 1/2 | 280 |
| M2 | 5/8 | 116 |
| M2 | 3/4 | 116 |
| M2 | 7/8 | 116 |

The masses sum to 10000. Every actual path moves at speed at most one. Every path completes a traversal from one endpoint to the other by H=4. By the intermediate value theorem it captures every continuous princess path by time 4. Its continuation after time 4 is irrelevant.

The two path families are used in the classical numerical literature. Their use here does not assume that an optimal unrestricted monster must belong to those families.

## 3. Capture-deadline lemma

Fix a princess p and write T_i=T(m_i,p), where the actual monster paths have probabilities w_i, summing to one.

Initially place every monster below p(0) in B, and every monster above p(0) in A. A monster at exactly p(0) has T_i=0 and can be assigned to either side for the following inequalities.

**Opposite-side deadline.** If i is in B, j is in A, and the two monster paths first meet at time tau_ij, then

\[
\min(T_i,T_j)\le\tau_{ij}.
\]

Indeed, if both survived beyond tau_ij, continuity and absence of capture would imply

\[
m_i(t)<p(t)<m_j(t)
\]

up to and including tau_ij. This is impossible when m_i(tau_ij)=m_j(tau_ij). Monsters caught at time zero already satisfy the inequality.

**Endpoint deadline.** If i is in B, then T_i is no larger than the first time m_i reaches +1. If j is in A, then T_j is no larger than the first time m_j reaches -1. This follows from the same intermediate-value argument.

These conclusions require no bound on princess speed and no restriction on her reversals, waiting, or crossings of zero.

## 4. A finite relaxation, without discretizing princess trajectories

For a fixed initial-position chamber, form the finite ordered set

\[
0=t_0<t_1<\cdots<t_K=4
\]

containing all opposite-side first-meeting times and all endpoint deadlines. The monster paths are piecewise linear with rational vertices, so these times can be computed exactly.

Round each actual capture time T_i upward to the next event time, obtaining tau_i. Then tau_i >= T_i. Crucially, rounding preserves every deadline inequality: if T_i <= t_k, then its upward rounding is also <= t_k.

Let s_i(k)=1 when tau_i>t_k and zero otherwise. Thus s_i(k) is nonincreasing in k and

\[
\tau_i=\sum_{k=0}^{K-1}(t_{k+1}-t_k)s_i(k).
\]

For i in B use a node variable y_i(k)=s_i(k). For j in A use z_j(k)=1-s_j(k). Consequently y is nonincreasing in time and z is nondecreasing. At an opposite-side meeting deadline t_k the necessary condition is

\[
y_i(k)\le z_j(k).
\]

This is a relaxation of princess play: not every permissible binary assignment needs to be realizable by a princess. That cannot invalidate an upper bound, since every actual princess supplies a permissible assignment.

## 5. The network

Create a source s, sink t, and one node for each (i,k). A node on the source side of a cut has binary label one.

For each i in B, put an arc from s to (i,k), of capacity w_i(t_{k+1}-t_k). For each j in A, put an arc from (j,k) to t, with the same corresponding capacity.

Add implication arcs of capacity H=4:

* For i in B, an arc (i,k+1) -> (i,k), enforcing nonincreasing y.
* For j in A, an arc (j,k) -> (j,k+1), enforcing nondecreasing z.
* At a meeting deadline t_k, an arc (i,k) -> (j,k), enforcing y_i(k) <= z_j(k).
* At a B endpoint deadline t_k, an arc (i,k) -> t.
* At an A endpoint deadline t_k, an arc s -> (j,k).

An actual princess's rounded capture times define a cut crossing none of the implication arcs. The capacity of that cut is exactly

\[
\sum_i w_i(4-\tau_i)=4-\sum_iw_i\tau_i.
\]

Any feasible source-to-sink flow F is no larger than the capacity of any cut. Therefore

\[
F\le4-\sum_iw_i\tau_i\le4-\sum_iw_iT_i,
\]

and hence

\[
\boxed{\mathbb E_\nu T\le4-F.}
\]

Only flow feasibility is required. There is no need to trust an optimizer's claim of optimality or even to establish that the saved flow is maximal.

## 6. All initial positions are covered

Reflection symmetry of nu lets us assume p(0)>=0. This is only a statement about the initial point: the subsequent princess path may cross zero arbitrarily often.

The distinct positive monster starting positions partition [0,1] into the seven open chambers in the table below. Throughout one chamber the initial classification into A and B is constant, so the same network applies to every initial point in that chamber.

At a chamber boundary, monsters starting at that boundary are captured at time zero. Assigning those monsters to the side prescribed by either neighboring chamber satisfies all necessary inequalities. Thus the open-chamber certificates also cover their endpoints, including 0 and 1.

All capacities were scaled by 320000 to become integers. The independently checked feasible flow amounts are:

| Initial-position chamber | Integer flow | Upper bound 4 - flow/320000 |
|---|---:|---:|
| (0,1/4) | 821591 | 458409/320000 |
| (1/4,3/8) | 821595 | 91681/64000 |
| (3/8,1/2) | 821592 | 57301/40000 |
| (1/2,5/8) | 821596 | 114601/80000 |
| (5/8,3/4) | 821597 | 458403/320000 |
| (3/4,7/8) | 821598 | 229201/160000 |
| (7/8,1) | 821534 | 229233/160000 |

The largest upper bound is 229233/160000. Combining the seven certificates proves the claimed theorem for every continuous princess path, and therefore for every randomized princess strategy as well.

## 7. What the verifier checks

Run `python verify.py` with Python 3. The verifier uses only the standard library. It reconstructs every monster path and event time using `fractions.Fraction`, builds the capacity graph exactly, then reads the positive flow arcs from `flows.json.gz`.

It checks that the probabilities are nonnegative and sum to one, every saved arc has an integer flow within its integer capacity, every interior node has exactly zero net flow, and the source and sink balances match. It verifies all seven chambers and computes their maximum upper bound with exact rational arithmetic.

The optimizer used to discover the distribution and flows is not invoked during verification. The final result is not a floating-point assertion. As a separate sanity check, the same construction applied to the two endpoint sweepers gives the familiar upper bound 3/2.

## 8. Exact failure of the fixed-infinitesimal response reduction

This section concerns the strong, fixed-infinitesimal interpretation of the response family used in the previous discussion. It does not claim that the unrestricted value cannot be near 1.3727, and it does not refute a differently formulated class that allows finite, independently optimized offsets.

Consider a symmetric monster mixture with total probability 3/7 on M1(-1) and its reflection, and total probability 4/7 on M1(-1/2) and its reflection.

For the special princess family, let P_a^epsilon start at a in [epsilon,1-epsilon], wait until 1-a-epsilon, run inward to epsilon, and then run to +1. Include reflections and stationary endpoint hiding. Here epsilon tends to zero.

The sweeper-pair limiting payoff against every interior P_a^epsilon is 3/2. Against the pair M1(-1/2), away from a=1/2 the limiting payoff is

\[
K(a)=\begin{cases}
1/2,&0<a\le1/4,\\
5/8-a/2,&1/4<a<1/2,\\
17/8,&1/2<a<1.
\end{cases}
\]

At a=1/2, immediate capture by one path lowers the payoff and does not change the maximum. Endpoint hiding gives sweeper payoff 1 and interior-pair payoff 5/2. Thus the supremum over this fixed-infinitesimal family, including its mixtures, is

\[
\max\left\{\frac37\frac32+\frac47\frac{17}{8},\;
\frac37+\frac47\frac52\right\}=\frac{13}{7}.
\]

There is also a uniform finite-epsilon check. For every 0 < epsilon < 1/6, the sweeper-pair payoff against an interior special path is exactly 3/2 - 3 epsilon/4. The M1(-1/2)-pair payoff is at most 17/8 - epsilon/4. Hence the mixture payoff for every such interior path is at most

\[
\frac{13}{7}-\frac{13}{28}\epsilon<\frac{13}{7}.
\]

Stationary endpoint hiding still gives exactly 13/7. Consequently even taking the union over all 0 < epsilon < 1/6, with a depending arbitrarily on epsilon, does not increase the supremum. This is a counterexample to the small-offset response reduction as precisely specified here; it is not a claim about a path class allowing arbitrary finite offsets.

Now take the following admissible unit-speed princess path, given by its vertices:

\[
(0,3/4),\quad(3/16,3/4),\quad(11/16,1/4),\quad(23/16,1).
\]

After the last vertex it remains at +1. Its capture times against the four monster paths are respectively

\[
2,\quad23/32,\quad3/2,\quad7/2.
\]

Therefore its expected capture time is

\[
\frac{3}{14}\left(2+\frac{23}{32}\right)
+\frac27\left(\frac32+\frac72\right)
=\frac{901}{448}>\frac{13}{7}.
\]

The difference is exactly 69/448. `counterexample.py` checks the path's speed bound and all four capture times with rational arithmetic.

This shows why an upper-bound proof cannot simply assume that a princess best response always waits, runs to an infinitesimal neighborhood of the center, and turns there. It does not constitute a lower bound of 901/448 for the full game: that payoff is against this particular, deliberately chosen monster mixture.

## 9. What remains unproved

The certificate supplies only one side of a minimax solution. It does not show that the displayed monster mixture is globally optimal. It does not furnish a princess distribution guaranteeing the same value against all monster paths.

Combining this result with the analytical lower bound in Alpern et al. gives

\[
\frac{15}{11}\le V\le\frac{229233}{160000}.
\]

An exact unrestricted value and matching optimal or epsilon-optimal strategies have not been established in this work.

## References

1. S. Alpern, R. Fokkink, R. Lindelauf and G. J. Olsder, “The ‘Princess and Monster’ Game on an Interval,” SIAM Journal on Control and Optimization 47(3), 1178–1190 (2008). DOI: 10.1137/060672054. Source of the published analytical bounds 15/11 and 13/9.
2. The same authors, “A Numerical Approach to the ‘Princess and Monster’ Game on an Interval,” Advances in Dynamic Games and Their Applications (2009). DOI: 10.1007/978-0-8176-4834-3_9. Source of the restricted path families; these are not assumed to be sufficient in the certificate above.
3. R. Fokkink, L. Geupel and K. Kikuta, “Open Problems on Search Games,” Search Theory: A Game Theoretic Perspective, pp. 75–81 (2013). DOI: 10.1007/978-1-4614-6825-7_5. Discussion of the structural conjecture and corrected restricted computations.