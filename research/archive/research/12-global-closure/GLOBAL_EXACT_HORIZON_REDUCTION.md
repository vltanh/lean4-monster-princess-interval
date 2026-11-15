# Exact global finite-horizon reduction by center crossing and outward completion

Date: 2026-11-13. **This is an exact reduction of the unrestricted
infinite-horizon game, not a truncation with an error term.** It removes
the unbounded-time part of the closure problem. It does not bound the
number of turns or CDF pieces on the remaining compact time interval.

## 1. Main theorem

Let V be the unrestricted first-contact value on [-1,1], with both players
moving at speed at most one and arbitrary initial positions. The global
minimax theorem supplies an optimal Monster probability law; Princess
attainment is not assumed.

Fix any constant H with `H >= 2V`. The already proved fair fastest-sweep
upper bound `V <= 3/2` permits the explicit choice **H=3**.
For completeness, both opposite unit sweeps catch every Princess by time
2, and at least one catches her by time 1: at time 1 both sweeps are at
zero, and the intermediate value theorem supplies the earlier contact
on one of their two sides. Their equally weighted mean is therefore at
most `(1+2)/2=3/2` against every pure Princess path.

The following conclusions hold.

1. **Every optimal Monster law**, symmetric or otherwise, is supported
   almost surely on paths that visit the center by time `2V`.
2. The Princess security supremum is unchanged if she is required to
   choose a fair reflection of a nonnegative radius path and, after H,
   move outwards at full speed until reaching her endpoint. In particular,
   all these Princess paths are endpoint-absorbed by `H+1`.
3. Against every such outward-completed Princess law, the unrestricted
   Monster response has an optimizer that visits the center by H and both
   endpoints by `H+4`.
4. Some symmetric **globally optimal Monster law for the original game**
   is supported on those same bounded-horizon Monster paths. An explicit
   normalization of an existing optimal law produces it.

Consequently the full game has the exact representation

\[
\boxed{
V=
\sup_{\mu\in\mathcal P_H^{\rm out}}
\min_{m\in\mathcal M_H}\mathbb E_\mu T(m,P)
=
\min_{\nu\in\mathcal P(\mathcal M_H)}
\sup_{p\ {\rm arbitrary\ legal}}\mathbb E_\nu T(M,p),
}
\tag{1}
\]

where `P_H^out` is the class of symmetric laws on sign-preserving paths
that move maximally outward after H, and `M_H` consists of all legal
Monster paths visiting 0 by H and both endpoints by `H+4`. The second
minimum is attained by a symmetric law. The Princess supremum in (1)
need not be attained.

With the simple rational constants:

\[
\boxed{
H=3,\qquad
\text{Princess outward after 3 and absorbed by 4},\qquad
\text{Monster completed by 7}.
}
\tag{2}
\]

If U is any independently established numerical upper bound, `H=2U`
also works, giving absorption by `2U+1` and completion by `2U+4`.
No numerical certificate is needed for the explicit 3/4/7 version.

## 2. The sign-preserving Princess class is globally sufficient

Start with any Princess law. Symmetrization cannot decrease its security
payoff. Apply the common ordered-quantile coupling to its symmetric
time marginals, which cannot decrease first-contact survival against any
Monster. Use the reflection-compatible two-trace quantile representatives
from [GLOBAL_MINIMAX_AND_CDF_DUALITY.md](GLOBAL_MINIMAX_AND_CDF_DUALITY.md),
Section 3, so the exact pointwise identities include exceptional ranks.

For ranks above 1/2, the ordered quantile is nonnegative at every time;
the reflected lower-half ranks are nonpositive. Thus an arbitrarily
near-optimal Princess law can be realized by choosing a legal radius
`r(t) in [0,1]`, choosing an independent fair sign, and following `+r`
or `-r` forever. This conclusion concerns the ordered coupling, not an
unjustified claim about every original Princess trajectory.

Mass at radius zero is harmless: its positive and negative sign labels
may coincide physically for a while. The labels still partition the
law into two pieces of probability exactly 1/2.

Write

\[
J_\mu(m)=\mathbb E_\mu T(m,P),\qquad
B(\mu)=\inf_m J_\mu(m),\qquad
\tau_0(m)=\inf\{t\ge0:m(t)=0\}.
\]

For every such sign-preserving symmetric Princess law and every Monster,

\[
\boxed{J_\mu(m)\ge\tfrac12\tau_0(m).}\tag{3}
\]

Before its first center visit a Monster starting strictly on one side
cannot meet any Princess path carrying the opposite sign label. This
half of the mass survives until at least `tau_0`. If the Monster starts
at the center the bound is zero; if it never reaches the center the
expected payoff is infinite. Contact at time zero is included.

## 3. A hard center-crossing support theorem for every Monster optimum

Let `mu_n` be sign-preserving symmetric Princess laws with
`B(mu_n) >= V-epsilon_n`, where `epsilon_n` decreases to zero. Such laws
exist by Section 2; no maximizing Princess law is needed. For every m,

\[
J_{\mu_n}(m)\ge
\max\{V-\epsilon_n,\tau_0(m)/2\}.
\]

If nu is any optimal Monster law, its payoff against every legal Princess
law is at most V. Hence

\[
\int\max\{V-\epsilon_n,\tau_0(m)/2\}\,\nu(dm)\le V.
\]

Monotone convergence gives

\[
\int\max\{V,\tau_0(m)/2\}\,\nu(dm)\le V.
\]

The integrand is at least V everywhere, so its positive excess must
vanish almost surely:

\[
\boxed{\tau_0(M)\le2V\quad\nu\text{-almost surely}.}\tag{4}
\]

This is a support bound, not merely an expected-time bound, and applies
to arbitrary starts, waits, infinitely many reversals and Zeno paths.

The same argument yields a useful quantitative version. If a Monster
law has unrestricted upper guarantee at most `V+delta`, then

\[
\boxed{\mathbb E_\nu[(\tau_0-2V)_+]\le2\delta.}\tag{5}
\]

More generally, if a specific sign-preserving symmetric Princess law
guarantees L and a Monster law has unrestricted upper guarantee U, then

\[
\boxed{\mathbb E_\nu[(\tau_0-2L)_+]\le2(U-L).}\tag{6}
\]

The zero-gap case of this estimate is exactly (4). A positive gap gives
tail control, not a hard support bound.

## 4. Outward completion never lowers Princess security

For a nonnegative radius path r, define

\[
r^H(t)=
\begin{cases}
r(t),&0\le t\le H,\\
\min\{1,r(H)+t-H\},&t\ge H.
\end{cases}
\tag{7}
\]

It remains 1-Lipschitz, dominates r pointwise after H, and equals 1 by
`H+1`. Preserve the original fair sign labels and apply (7) to every
radius, obtaining a legal symmetric law `mu^H`.

**Lemma 1 (pointwise comparison after a center visit).** If
`tau_0(m) <= H`, then for every sign-labelled original Princess path p,

\[
\boxed{T(m,p^H)\ge T(m,p).}\tag{8}
\]

**Proof.** The paths agree through H, so already captured paths retain
their exact capture time. Consider an uncaptured positive-sign path.
At the Monster's center visit, it must be strictly above the Monster:
equality would already be capture. It stays strictly above through H
by continuity and absence of contact. After H the new Princess position
is at least the old position. If the new path meets the Monster at a
finite time t, then `m(H)<p(H)` and `m(t)=p^H(t)>=p(t)`. The intermediate
value theorem forces an old contact by t. The negative-sign case uses
the reversed inequalities. An infinite new capture time is immediate.
No continuity of the first-contact functional is assumed. QED.

If `tau_0(m)>H`, the Monster stays strictly on one side throughout
[0,H]. The opposite sign-labelled half survives at least to H, so

\[
J_{\mu^H}(m)\ge H/2.
\]

Combining both cases gives, for every sign-preserving symmetric mu,

\[
\boxed{B(\mu^H)\ge\min\{B(\mu),H/2\}.}\tag{9}
\]

Because `B(mu)<=V<=H/2`, outward completion does not decrease its
security. Taking arbitrarily near-optimal mu proves

\[
\boxed{\sup_{\mu\in\mathcal P_H^{\rm out}}B(\mu)=V.}\tag{10}
\]

This is an exact domination argument for the game value, not a Markov
tail estimate. The forced Princess endpoint horizon is uniform over
all original Princess laws after the preceding symmetrization and
ordering steps.

## 5. After H, surviving targets can only be caught at their endpoints

Suppose the Monster has visited the center by H and the Princess uses
an outward-completed law. Let `x=m(H)`. Every surviving positive target
has `p(H)>x`. While it is still moving outward,

\[
m(t)\le x+t-H<p(H)+t-H=p^H(t).
\]

Thus it cannot be captured before reaching +1. Once there it stays,
so its future capture is exactly the Monster's first visit to +1 after
H. Every surviving negative target has the reflected property.

Let `w_+` and `w_-` be the two surviving sign masses at H. The exact
optimal additional cost from that state is therefore

\[
\boxed{
\min\left\{
 w_-(x+1)+w_+(x+3),\quad
 w_+(1-x)+w_-(3-x)
\right\}.
}\tag{11}
\]

The first expression visits -1 then +1 at full speed; the second visits
+1 then -1. From the first chosen endpoint onward the opposite sweep
is pointwise fastest. Zero survivor masses, an endpoint initial position,
and zero-duration first legs are all included. Either tour visits both
endpoints within four additional time units. The nearer endpoint need
not be optimal when the two weights differ, which is why replacing
four by three here would be incorrect.

The prefix cost to add to (11) is `E[min(T,H)]`, with the same original
prefix. Already captured paths do not contribute a new tail cost.

### A uniform normalization, independent of the Princess law

There is a stronger fact than optimizing (11) for one supplied law.
Given any Monster path with `tau_0<=H`, preserve its prefix through H.
Let e be the **first endpoint visited by its old continuation at or
after H**. Replace the continuation by the direct unit-speed trip
from x to e, then the unit-speed sweep to -e, and hold there.

The new first arrival at e is no later than the old one. Its arrival
at -e is also no later than the old first post-H arrival there, because
the old route must traverse distance two after first reaching e.
Section 5 therefore proves

\[
\boxed{
T(N_Hm,p^H)\le T(m,p^H)
\quad\text{for every outward-completed sign-labelled path }p^H.
}\tag{12}
\]

All paths already caught by H are unchanged. The new Monster still
visits the center by H and completes both endpoints by `H+4`.
The same normalization works for **every** outward-completed Princess
law simultaneously; it does not choose a tail using unknown optimal
Princess weights.

## 6. Every supplied outward law has an attained response by H+4

Fix any `mu in P_H^out`. It is static at the endpoints after `S=H+1`.
From time S, replace any Monster continuation by its first future
endpoint followed by the opposite endpoint, at full speed. This
cannot delay any still-uncaught stationary target. If no future
endpoint is visited, either the old cost is infinite or there are
no surviving positive-mass targets; any endpoint tour then suffices.
This proves that the unrestricted response infimum is unchanged by
requiring both endpoint visits by `S+4=H+5`.

The corresponding bounded-horizon path set is compact. First-contact
time is lower semicontinuous in the Monster path, so its expectation
is lower semicontinuous and a response optimizer exists on that set.

Such an optimizer must visit the center by H. Otherwise `x=m(H)` is
nonzero, and its first possible center visit is at least `H+|x|`.
The opposite sign-labelled half of the Princess law survives at least
that long. Consequently

\[
J_\mu(m)\ge\frac{H+|x|}{2}>\frac H2\ge V\ge B(\mu),
\]

contradicting optimality. Apply the uniform normalization (12) to this
optimizer. Its payoff cannot increase, so it remains an optimizer and
belongs to `M_H`. This proves the fixed-law exact response assertion.
The temporary `H+5` compactness argument also handles the boundary
case `H/2=V`; no strict upper-gap assumption is hidden in the theorem.

## 7. A bounded-horizon Monster optimizer for the original game

Take a symmetric globally optimal Monster law nu supplied by the global
minimax theorem. The stationary endpoint Princess challenges imply
`E_nu tau_+ <= V` and `E_nu tau_- <= V`, so both endpoint visits occur
almost surely at finite times. Stop each path at its second endpoint
visit. This changes no first contact against any legal Princess and
commutes with reflection.

By (4), these paths visit the center by H almost surely. Apply the
uniform normalization `N_H` from Section 5. Stopping first ensures a
first post-H endpoint visit always exists, including when the old path
completed before H and is holding at that endpoint. Hitting times and
the unique first endpoint choice are Borel functions of the full
continuous path. The normalization commutes with reflection. Hence
its pushforward `nu_H` is a legal symmetric probability law on `M_H`.

For any sign-preserving symmetric Princess law mu, let `mu^H` denote
its outward completion. Equations (8) and (12) give

\[
\begin{aligned}
\mathbb E_{\nu_H,\mu}T
&\le\mathbb E_{\nu_H,\mu^H}T\\
&\le\mathbb E_{\nu,\mu^H}T\\
&\le V.
\end{aligned}
\tag{13}
\]

Now take an arbitrary original Princess law. Symmetrizing it leaves its
payoff against the symmetric `nu_H` unchanged. Its common ordered-quantile
coupling dominates its payoff and belongs to the sign-preserving class.
Thus (13) controls **every** legal Princess strategy, not merely those
forced outward after H. It follows that

\[
\sup_{p\ {\rm arbitrary\ legal}}\mathbb E_{\nu_H}T(M,p)\le V.
\]

Weak duality forces equality. Therefore `nu_H` is globally optimal for
the original unrestricted game. This also proves both directions and
attainment on the Monster side of (1).

The class `M_H` itself is compact in the uniform topology on [0,H+4]:
the speed and arena constraints are closed, as are a center visit by H
and visits to both endpoints by H+4. No finite turn count is used.

## 8. Exact stabilization and fixed-horizon rank approximation

Let W_D be the completed-horizon game from
[GLOBAL_STRONG_RECORD_DUALITY.md](GLOBAL_STRONG_RECORD_DUALITY.md): the
Monster must visit both endpoints by D, while the Princess may use every
legal path on [0,D]. Restricting Monster paths gives `W_D>=V`. Section 7
provides a globally optimal Monster law completed by `H+4`, so the reverse
inequality holds for every `D>=H+4`. Thus

\[
\boxed{W_D=V\quad\text{for every }D\ge7.}\tag{14}
\]

The earlier decreasing completed-horizon hierarchy therefore stabilizes
exactly. The finite-completion causal-record strong dual at D=7 is an
exact dual of the original game; taking an unbounded horizon limit is
unnecessary. The additional center-by-3 restriction is also valid.

There is a corresponding improvement to the uniform rank approximation.
Let `V_{H,n}^out` be the supremum of unrestricted Princess security over
equal-weight `2n` reflected ordered paths that move maximally outward
after H. Then

\[
\boxed{
V-\frac{H+4}{2n}\le V_{H,n}^{\rm out}\le V,
\qquad
V-\frac7{2n}\le V_{3,n}^{\rm out}\le V.
}\tag{15}
\]

To prove this, start with an arbitrarily near-optimal ordered symmetric
law and force its sign-labelled quantile paths outward after H. Sample
these paths at the `2n` midpoint ranks. Use the symmetric two-trace
representatives on [0,H], then **apply the outward completion to those
same representatives**. This order of operations matters at exceptional
plateau ranks: taking a fresh midpoint of inverse traces after clipping
need not commute with the nonlinear outward clipping map. The resulting
sampled paths are exactly reflected, ordered, legal and outward-completed.

For each Monster history, the survivor ranks are an initial and a final
interval. Midpoint counting changes their total probability by at most
`1/(2n)`, including either endpoint convention. Every Monster in `M_H`
captures all paths by `H+4`, so integrating survival changes its expected
cost by at most `(H+4)/(2n)`. Section 6 identifies the sampled law's
unrestricted response with its response over `M_H`. Taking the infimum
over those Monsters, then the Princess supremum, proves (15).

There is still no proved finite n for which equality holds. The quantity
`V_{H,n}^out` retains continuous-path optimization on [0,H], so (15) is
not itself a finite LP or a finite equilibrium-support theorem.

## 9. What this closes, and what it does not

**Closed:** the unbounded-horizon gate in the full unrestricted game.
The original exact game can be studied on the single compact interval
[0,7], with Princess forced-outward boundary data after time 3 and an
exact two-choice endpoint continuation formula. The center-crossing
bound (4) holds for every Monster optimizer, without Princess attainment.

**Still open:** a uniform finite number of interior phases, CDF pieces,
turns, support types or algebraic cases on [0,3]; an explicit equilibrium;
and the exact value V. Arbitrarily many turns or Zeno behavior before
the cutoff remain admissible. A compact time interval does not by itself
make a path optimization finite-dimensional, and this theorem does not
assert an equilibrium-specific turn bound.

This exact theorem supersedes the need to increase a completion horizon
indefinitely when searching for the unrestricted equilibrium. It does
not supersede approximation theorems for other restricted strategy
classes, nor convert finite-bank values into exact game values.

## 10. Reproduction

The companion exact-rational regression
`packages/interval_global_closure/verify_exact_horizon_reduction.py`
checks the physical first-contact comparisons, the center barrier,
outward legality, and the two endpoint-tail formulas on legal polygonal
paths with waits, reversals, initial contacts and center-contact ties.
These are independent finite physical-contact audits of the main
domination steps. The universal quantile, minimax, almost-sure support
and compactness statements are analytic proofs, not Lean-checked claims.
