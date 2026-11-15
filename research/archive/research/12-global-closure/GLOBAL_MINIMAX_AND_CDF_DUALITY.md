# Full-game G1: minimax equality, attained Monster law, and uniform rank/horizon reduction

Date: 2026-11-12.

**Global mathematical theorems for the unrestricted interval Princess–Monster game,
with no prescribed Princess endpoint-absorption horizon, no finite Monster turn cap,
and no assumed equilibrium CDF.** These close the abstract minimax/existence and
uniform approximation parts of G1. They do **not** identify the constant, an
optimal Monster path distribution, or an optimal Princess CDF; G2–G5 remain open.

## 0. Game and important asymmetry

Let \(\mathcal A\) be all continuous \(1\)-Lipschitz paths
\(p:[0,\infty)\to[-1,1]\), including arbitrary initial positions. The
Princess and Monster choose independent Borel probability distributions
\(\mu,\nu\) over \(\mathcal A\) before playing. Their payoff is the
first-contact time
\[
T(m,p)=\inf\{t\ge0:m(t)=p(t)\}\in[0,\infty].
\]
Define the Princess security value
\[
V=\sup_{\mu\in\mathcal P(\mathcal A)}
      \inf_{m\in\mathcal A}\int T(m,p)\,d\mu(p).
\]
The unit sweep \(m(t)=1-t\) for \(0\le t\le2\) catches every
Princess by time \(2\), by the intermediate-value theorem. Thus
\(0\le V\le2\). Later constant continuation keeps the route legal.

For the Princess, the time-marginal CDF \(F(t,x)\) suffices to select an
ordered-quantile law dominating any original law with the same marginals
against **each** Monster route. In contrast, the Monster's time-marginal
CDF alone is insufficient to determine expected first contact: see the
exact counterexample in Section 6. The correct Monster dual variable is
a **law on entire trajectories**, not merely a one-time spatial CDF.

## 1. Global minimax equality and attained Monster optimizer

**Theorem 1 (unrestricted lopsided minimax).**
For the actual infinite-horizon first-contact payoff,
\[
\boxed{
 V=\min_{\nu\in\mathcal P(\mathcal A)}
      \sup_{p\in\mathcal A}\int T(m,p)\,d\nu(m).
}                                                        \tag{1}
\]
There exists an optimal **symmetric** Monster mixed law \(\nu_*\).
No Princess maximizing law is assumed to exist; the left side remains a
supremum. In particular, (1) is **not** an assertion that both players
have attained equilibrium strategies or that their optimal laws are
known explicitly.

**Proof.** Give \(\mathcal A\) the topology of uniform convergence on
every bounded time interval, metrized for example by
\[
d(f,g)=\sum_{j\ge1}2^{-j}
           \min(1,\|f-g\|_{[0,j]}).
\]
Arzelà–Ascoli and a diagonal argument make \(\mathcal A\) a compact
metric space; the \(1\)-Lipschitz and arena constraints are closed.
Hence probability laws on \(\mathcal A\), with weak convergence, also
form a compact space.

For fixed \(p\), the function \(m\mapsto T(m,p)\) is **lower
semicontinuous**, including \(T=\infty\). Indeed, if \(m_j\to m\) locally
uniformly and \(T(m_j,p)\) had a bounded subsequence with limit
\(s<T(m,p)\), a subsequence of their hit times would converge to
\(s\), forcing \(m(s)=p(s)\), a contradiction. Portmanteau gives
lower semicontinuity of
\[
 f_p(\nu)=\int T(m,p)\,d\nu(m)
\]
on the compact space of Monster laws; extended nonnegative integrals
are legitimate.

Fix \(c>V\) and any finite list of Princess paths \(p_1,\ldots,p_s\).
There exists a Monster law \(\nu\) with
\(f_{p_i}(\nu)\le c\) simultaneously. To see this, define the
finite-dimensional **upper set**
\[
C=\{z\in\mathbb R^s:
 \exists\nu,\quad f_{p_i}(\nu)\le z_i\text{ for all }i\}.
\]
It is nonempty (the sweep makes every coordinate at most \(2\)),
convex (mix Monster laws), upward closed, and closed: bounded
coordinate witnesses have weakly converging subsequences, and
Portmanteau preserves the upper coordinate bounds.

If \((c,\ldots,c)\notin C\), strict finite-dimensional separation from
this closed convex upper set supplies nonnegative weights
\(w_i\), \(\sum_iw_i=1\), satisfying
\[
\inf_\nu\sum_iw_i f_{p_i}(\nu)>c.
\]
The infimum over Monster mixed laws equals the infimum over pure
Monster paths, by linearity. **There is a minor extended-payoff
issue when some \(w_i=0\):** the finite upper set \(C\) retains only
laws with finite costs against *every* listed path, whereas a pure
Monster minimizing the weighted sum might fail to catch an unused
zero-weight path. This is harmless: the nonnegative weighted sum
has a finite minimizer on compact \(\mathcal A\), by lower
semicontinuity and the universal sweep. All its positive-weight
targets are captured at finite times. Complete that minimizing
Monster trajectory by a full endpoint tour *after* the latest of
those finitely many capture times. This leaves its weighted score
unchanged and makes every listed cost finite. Hence the infimum
of \(w\cdot z\) over \(z\in C\) equals the unrestricted pure
weighted-response infimum, even when some coefficients vanish.
The Princess law \(\sum_iw_i\delta_{p_i}\) would therefore have
security payoff \(>c>V\), a contradiction.

Therefore the closed subsets
\(\{\nu:f_p(\nu)\le c\}\) have the finite-intersection property.
Compactness gives a \(\nu_c\) satisfying the inequalities
**simultaneously for every Princess path**. Apply this for
\(c\downarrow V\), and use nested compactness once more to obtain
\(\nu_*\) with \(\sup_p f_p(\nu_*)\le V\).
Weak duality gives the opposite inequality, proving (1).

Reflecting \(m\mapsto-m\) preserves the set of Princess paths.
Both \(\nu_*\) and its reflection are optimal; so is their average.
Thus an optimal symmetric Monster law exists. \(\square\)

The proof **does not use** a continuous hitting-time payoff, or invoke
compactness in the wrong maximization direction. Exact contacts are
the reason lower, not upper, semicontinuity is available.

## 2. Uniform finite-horizon completion, without Princess absorption

For \(H>0\) let \(D=H+3\). Let \(\mathcal M_H\) be all legal
Monster paths on \([0,D]\) which visit **both** endpoints during
\([H,D]\), with arbitrary lawful movement before and between visits.
This is a nonempty compact subset of the 1-Lipschitz path space on
\([0,D]\). Each \(m\in\mathcal M_H\) catches every legal Princess by \(D\):
at its two opposite endpoint visits, \(m-p\) has opposite weak signs.

**Theorem 2 (universal horizon error).** For every Princess law \(\mu\),
without assuming endpoint absorption or finite Princess turns, put
\[
B(\mu)=\inf_{m\in\mathcal A}\mathbb E_\mu T(m,P),\quad
B_H(\mu)=\inf_{m\in\mathcal M_H}\mathbb E_\mu T(m,P).
\]
Then the stronger **multiplicative** estimate is
\[
\boxed{
 B(\mu)\le B_H(\mu)\le(1+3/H)B(\mu)
                         \le B(\mu)+6/H.}            \tag{2}
\]
Moreover the optimal full-game Monster law can be transformed to a
law \(\nu_H\) on \(\mathcal M_H\) with
\[
\boxed{\sup_p\mathbb E_{\nu_H}T(M,p)
                   \le(1+3/H)V\le V+6/H.}             \tag{3}
\]

**Proof.** Preserve an arbitrary legal Monster prefix through time \(H\).
From its position \(x=m(H)\), travel at unit speed to the *nearest*
endpoint (distance at most \(1\)), then sweep directly to the opposite
endpoint (distance \(2\)), and hold position. This makes a physically
legal \(\widetilde m\in\mathcal M_H\). A tie at \(x=0\) may be resolved
deterministically (a Borel choice), so the construction also pushes
forward Monster probability laws.

Every Princess encountered by \(m\) by time \(H\) is caught at the same
time by \(\widetilde m\). Every other Princess is caught by
\(\widetilde m\) no later than \(H+3\). Pointwise,
\[
\boxed{
T(\widetilde m,p)
 \le T(m,p)+3\,\mathbf1_{\{T(m,p)>H\}}.}                \tag{4}
\]
For a near-optimal pure response to \(\mu\), Markov's inequality and
the universal bound \(B(\mu)\le2\) imply (2) on letting the pure-response
error vanish.

Apply the *same pathwise completion map* to the optimal Monster law
\(\nu_*\) from Theorem 1. For every pure Princess path \(p\),
\[
\Pr_{\nu_*}(T(M,p)>H)
 \le \mathbb E_{\nu_*}T(M,p)/H\le V/H\le2/H.
\]
Average (4) and take the supremum over all \(p\), proving (3).
No interchange of an infimum with a hitting-time limit is needed.
\(\square\)

Consequently, with
\(V_H=\sup_\mu B_H(\mu)\), the truncated full-game values satisfy
\[
\boxed{ V\le V_H\le(1+3/H)V\le V+6/H.}               \tag{5}
\]
The minimax argument of Theorem 1 also applies *within*
\(\mathcal M_H\), yielding an attained Monster mixed optimizer of the
finite-horizon game. The legal target paths only need to be specified
through \(D\).

## 3. Universal finite-rank Princess approximation with explicit error

A Princess law can first be symmetrized under \(p\mapsto-p\):
its security payoff does not decrease, because it is the infimum
of linear functionals in the Princess law and the Monster response
class is reflection-invariant. The same holds for \(B_H\).

Next replace the symmetric law by its **common ordered quantile
coupling** of its signed one-time CDF \(F(t,\cdot)\). Every quantile
path is 1-Lipschitz because each original path was 1-Lipschitz.
The ordered coupling has at least as large survival probability
against every Monster trajectory: the surviving target paths must be
strictly below the Monster throughout the past or strictly above it;
their probabilities are bounded respectively by the lowest strict-CDF
record and the complementary highest closed-CDF record. The ordered
quantiles attain both bounds simultaneously. This is the same
ordered-CDF domination already established in the repository's
SELECTOR_MINIMAX_SYNTHESIS.md, now used without a terminal assumption.

**Quantile convention at plateau ranks (audit correction, 2026-11-13).**
An ordinary lower generalized inverse need not give exactly reflected
samples at exceptional ranks. For example, the symmetric stationary law
with masses \(1/4,1/2,1/4\) at \(-1,0,1\) has lower quantiles
\(Q_-(1/4)=-1\) and \(Q_-(3/4)=0\), which are not reflections.
For every \(0<q<1\), use instead
\[
\begin{aligned}
Q_-(t,q)&=\inf\{x\in[-1,1]:F(t,x)\ge q\},\\
Q_+(t,q)&=\inf\{x\in[-1,1]:F(t,x)>q\},\\
Q_{\rm sym}(t,q)&=\tfrac12\bigl(Q_-(t,q)+Q_+(t,q)\bigr).
\end{aligned}
\]
Both generalized inverses are nondecreasing in q and 1-Lipschitz in
t, by the same transport inequalities. Their midpoint therefore has
these properties too. At each fixed t the two traces differ only at
the at-most-countably-many CDF plateau ranks, so the law of
\(Q_{\rm sym}(t,U)\), for U uniform on (0,1), still has CDF F.
Reflection exchanges the traces exactly:
\(Q_-(t,1-q)=-Q_+(t,q)\). Consequently
\(Q_{\rm sym}(t,1-q)=-Q_{\rm sym}(t,q)\), including every
exceptional rank, and \(Q_{\rm sym}(t,1/2)=0\).
Thus this convention preserves the ordered-CDF domination theorem
and supplies genuinely symmetric representatives before sampling.

For any integer \(n\ge1\), sample \(N=2n\) equally weighted
paths \(Q_{\rm sym}(\cdot,q_j)\) at midpoint ranks
\(q_j=(j-\frac12)/N\), \(1\le j\le N\).
The exact reflection identity gives \(n\) **fairly reflected radial
pairs**; all paths remain legal and ordered. Denote the resulting
law \(\mu_N\).

For each fixed Monster history and each time \(t\), the uncaptured
ranks of the ordered law form an initial and a final interval in
\(q\). Midpoint counting on one interval has discrepancy at most
\(1/(2N)\), including the strict/closed endpoint conventions.
The two survivor tails therefore differ in total mass by at most
\(1/N\), uniformly in the Monster path, time, and source Princess law.
For a Monster in \(\mathcal M_H\), integrate survival to time \(D\):
\[
\boxed{
\left|\mathbb E_{\mu_N}T(m,P)-
       \mathbb E_{\mu^\uparrow}T(m,P)\right|
 \le \frac{D}{N}=\frac{H+3}{2n},
 \qquad m\in\mathcal M_H.}                             \tag{6}
\]
No weak convergence of first-hit times or assumption of atomlessness
has been used. In particular, fixed path-contact ties are harmless.

Let \(V_{H,n}\) denote the Princess security supremum against
\(\mathcal M_H\) **restricted to symmetric, common-ordered,
equal-weight \(2n\)-path Princess laws**. Then
\[
 V_H-\frac{H+3}{2n}\le V_{H,n}\le V_H .
\]
Combining this with (5) gives the explicit unrestricted value bracket
\[
\boxed{
 \frac{V_{H,n}}{1+3/H}
 \le V
 \le V_{H,n}+\frac{H+3}{2n}.}                           \tag{7}
\]
The weaker but purely additive form
\(V_{H,n}-6/H\le V\) also follows because \(V\le2\).
Using the multiplicative lower endpoint may considerably sharpen
a computed certificate without any extra Monster routes.
Its width is at most \(6/H+(H+3)/(2n)\). Choosing
\(H=\sqrt{12n}\) gives
\[
\boxed{\text{width}\le2\sqrt{3/n}+\frac3{2n}.}         \tag{8}
\]

**Scope of finiteness:** This reduces the Princess's *number of
weighted paths* to \(2n\), and the Monster's *time horizon* to
\(H+3\), with a uniform certified error. It does **not** impose a finite
number of corners or turns on those paths, so \(V_{H,n}\) is still a
continuous-path optimization, not a finite LP or a solved exact game.

### Explicit approximate global saddle

For any \(\epsilon>0\), choose a Princess law with security at least
\(V-\epsilon\), symmetrize, order, and sample its \(N=2n\) midpoint
quantiles as above. From (2) and (6),
\[
\inf_m\mathbb E_{\mu_N}T(m,P)
\ge V-\epsilon-\frac6H-\frac{H+3}{2n}.                 \tag{9}
\]
The Monster law \(\nu_H\) in (3) satisfies the **simultaneous**
all-Princess upper guarantee \(V+6/H\). Therefore this finite-rank
Princess law and bounded-horizon Monster law form an approximate
unrestricted saddle with total security gap
\[
\boxed{
\epsilon+\frac{12}{H}+\frac{H+3}{2n}.}                \tag{10}
\]
With \(H=\sqrt{24n}\), the error becomes
\(\epsilon+2\sqrt{6/n}+3/(2n)\).
These are existence/approximation guarantees; we have not constructed
the maximizing \(2n\) quantiles or the optimizing Monster measure.

## 4. Exact coupled complementarity (G1 optimality conditions)

Let \(\nu_*\) be the optimal symmetric Monster law in Theorem 1.
For every pure Princess \(p\),
\[
\Psi_{\nu_*}(p):=\mathbb E_{\nu_*}T(M,p)\le V.            \tag{11}
\]
Let \(\mu_\epsilon\) be any Princess law with
\(B(\mu_\epsilon)\ge V-\epsilon\).
Then
\[
0\le
\int (V-\Psi_{\nu_*}(p))\,d\mu_\epsilon(p)
\le\epsilon,                                          \tag{12}
\]
and
\[
0\le\int
 \bigl(\mathbb E_{\mu_\epsilon}T(m,P)
                -(V-\epsilon)\bigr)\,d\nu_*(m)
\le\epsilon.                                          \tag{13}
\]
Indeed every Monster cost against \(\mu_\epsilon\) is at least
\(V-\epsilon\); the average of these costs under \(\nu_*\) is at
most \(V\), because (11) bounds every Princess pure path.
Markov's inequality gives the quantitative support restrictions
\[
\mu_\epsilon\{p:\Psi_{\nu_*}(p)\le V-\delta\}
   \le\epsilon/\delta,\qquad
\nu_*\{m:\mathbb E_{\mu_\epsilon}T(m,P)
              \ge V-\epsilon+\delta\}
   \le\epsilon/\delta                               \tag{14}
\]
for every \(\delta>0\).

If a Princess optimizer \(\mu_*\) happens to exist, let
\(\epsilon=0\). The integrands in (12)-(13) are nonnegative
and have mean zero. Thus
\[
\boxed{
\Psi_{\nu_*}(p)=V\quad\mu_*\text{-almost surely},
\qquad
\mathbb E_{\mu_*}T(m,P)=V\quad\nu_*\text{-almost surely}.
}                                                     \tag{15}
\]
After symmetrizing and ordering \(\mu_*\), (15) is a genuine
coupled support condition on the optimal Princess quantile paths
and the optimal Monster trajectories. In terms of the ordered
Princess signed CDF \(F\), its Monster-side equality is
\[
\boxed{
\int_0^\infty\!
 \biggl[
 1+\inf_{0\le s\le t}F^-(s,m(s))
  -\sup_{0\le s\le t}F^+(s,m(s))
 \biggr]\,dt=V
 \quad\text{for }\nu_*\text{-a.e. }m.}                 \tag{16}
\]
There is no assertion of a finite optimal turn support or a
smooth Euler–Lagrange density. Both remain to be derived.

For any **finite supported** completed Monster candidate and tight
causal record selectors, the existing
GLOBAL_SELECTOR_PLANE_ORACLE.md supplies the complementary upper
certificate: if its linear selector-plane global path supremum
equals \(c\) and a Princess field has unrestricted Monster response
at least \(c\), it is a saddle. This is a sufficient *verification*
criterion, not proof that a finite-support equilibrium exists.

## 5. The precise next constructive gate

The exact **no-smoothness CDF first variation** of the coupled
strict/closed records is now separately proved in
[GLOBAL_CDF_VARIATIONAL_STATIONARITY.md](GLOBAL_CDF_VARIATIONAL_STATIONARITY.md).
It yields a necessary-and-sufficient variational inequality for
global Princess optimality against any completed Monster path law,
with a quantitative error version. Combining that inequality with
the unrestricted Monster response lower bound gives a complete
saddle *verification criterion*, still without a constructed candidate.



The abstract G1 minimax/existence question is closed, but the
**explicit equilibrium** is not. The remaining constructive task is to
find a pair \((F,\nu)\), potentially with continuum support and
infinitely many Monster reversals, for which both global support
equalities (15) hold and the CDF record inequality is tight on
the Monster support. The selector-plane oracle supplies a complete
Princess upper separator for a supplied *finite* Monster mixture;
the center-renewal Bellman machinery supplies local Monster response
certificates for a supplied ordered CDF.

Do **not** promote a finite-bank LP objective to a global bound.
Do **not** infer that because an optimal Monster mixed law exists, it
has a finite set of trajectories or a finitely supported time-marginal
CDF. Do **not** infer a Princess optimizer exists from the lower
semicontinuity used for the Monster minimizer.

## 6. Explicit obstruction: the Monster marginal CDF is insufficient

Construct these four legal polygonal path pieces in the interval:

- \(A:\ (0,-1)\to(2,0)\), and \(B:\ (0,1)\to(2,0)\);
- \(L:\ (2,0)\to(4,-1)\to(6,1)\);
- \(R:\ (2,0)\to(4,1)\to(6,-1)\).

Let \(\nu_{\rm cross}\) choose each of \(A\circ R\)
and \(B\circ L\) with probability \(1/2\), and let
\(\nu_{\rm bounce}\) choose each of \(A\circ L\)
and \(B\circ R\) with probability \(1/2\).
All four completed trajectories are 1-Lipschitz, stay inside
\([-1,1]\), and visit both endpoints by time six.

Their **time-marginal position distributions coincide identically
for every \(t\ge0\)**: before time two both laws have half mass at
\(A(t)\) and half at \(B(t)\); after time two both have half at
\(L(t)\) and half at \(R(t)\); after six hold their endpoint positions.

Against the stationary legal Princess \(p(t)\equiv-3/10\), the two
physical chronological first-hit lists are
\[
\nu_{\rm cross}: (7/5,13/5),\quad
\nu_{\rm bounce}:(7/5,53/10).
\]
Their expected capture times are therefore
\[
\boxed{
\mathbb E_{\nu_{\rm cross}}T=2,\qquad
\mathbb E_{\nu_{\rm bounce}}T=67/20=3.35.}
\]
The same Monster one-time CDF has different capture payoff.
A search for a single *Monster time-marginal CDF* cannot solve
this path-dependent game; its complete path-space coupling is
essential. The corresponding Princess CDF remains sufficient
because of the ordered-dominance theorem.

## 7. Reproduction and provenance

Run:

    python packages/interval_global_closure/verify_global_minimax_reduction.py

The standalone exact-Fraction verifier checks:
the four legal complete Monster counterexample paths, equality
of their position multisets on each affine time piece, their
exact first contacts and distinct expectations;
the two-tail midpoint discrepancy over 36,057 rational fixtures;
and an exact endpoint-completion capture inequality over seven
stationary-target fixtures. **These fixtures do not mechanically
verify the compactness/separation or all-\(H,n\) analytic proofs**.
No Lean formalization or CI run is claimed.

The separate audit regression
`packages/interval_global_closure/verify_symmetric_quantile_ties.py`
exhibits the failed ordinary-quantile reflection claim and checks the
repaired two-trace convention for moving symmetric atomic laws,
including exact plateau ranks, crossing quantile paths, and actual
continuous-time first contacts. It uses rational affine breakpoints,
not an approximate contact-time grid.

**Effect on game bounds:** NONE. The rigorous numerical
Princess/Monster bounds already in STATUS.md remain unchanged.
The new results are global structural facts and a uniform
approximation theorem, not an exact numerical equilibrium value.

