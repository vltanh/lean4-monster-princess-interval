# G2: Strong causal-record duality and exact one-radius Princess oracle

Date: 2026-11-12. **New unrestricted structural theorem: the causal
record-occupation dual has ZERO gap and ATTAINS its minimum on every
finite completed horizon.** It does not compute the full-game constant
or construct the global minimizer explicitly.

## 0. Summary and role in the global attack

The previous GLOBAL_DUAL_RECORD_PRESSURE_HJB.md proved only
\[
 V\le \sup_{p\ {\rm legal}} {\cal R}_{\gamma}(p)
\]
for a supplied completed Monster law with causal record selectors;
that result did **not** show that minimizing this upper bound over
all such selectors recovers the game. The current theorem closes this
exact strong-duality/existence gate, without a finite Monster bank,
finite turn cutoff, atomlessness, Princess attainment or a smooth
PDE assumption.

Three new conclusions are particularly useful:

1. The completed-horizon full game is **exactly** the infimum over
   causal history measures of the unrestricted pure Princess path
   oracle, and an optimal causal measure exists.
2. A symmetric optimal causal measure exists. Its Princess oracle
   **reduces to a single nonnegative radius trajectory** and one
   signed/strict threshold reward measure, not two independent
   space-time pressures.
3. Every near-optimal Princess CDF and optimal causal dual satisfy
   quantitative record-activity, Monster-response and Princess
   path-calibration inequalities, even if the Princess supremum
   is not attained. These are the required global KKT conditions.

This is mathematical progress toward G2, but G2 explicit construction
and the unrestricted numerical value still remain OPEN.

## 1. A monotone completed-horizon hierarchy

Let \({\cal A}_D\) be all continuous 1-Lipschitz paths on \([0,D]\)
taking values in \([-1,1]\). For \(D\ge 2\), let
\[
 {\cal M}_D=\{m\in{\cal A}_D:
    m\text{ visits }-1\text{ and }+1\text{ by time }D\}.
\]
It is a nonempty **compact** subset in the uniform topology:
existence of endpoint-visit times is closed by compactness of
\([0,D]\). Every \(m\in{\cal M}_D\) meets every legal Princess
path by time \(D\), by the intermediate-value theorem.

Define the completed-horizon security
\[
 W_D=\sup_{\mu\in{\cal P}({\cal A}_D)}
          \inf_{m\in{\cal M}_D}\mathbb E_\mu T(m,P).
                                                               \tag{1}
\]
For \(D_2\ge D_1\ge2\), the class of Monster paths completing
by \(D_1\) embeds into \({\cal M}_{D_2}\) by constant extension.
Against any Princess on the longer horizon its payoff depends
only on the shorter Princess prefix. Hence
\[
 \boxed{W_{D_2}\le W_{D_1}.}                              \tag{2}
\]
This is a **monotone hierarchy**, unlike the previous
"must visit both endpoints in [H,H+3]" auxiliary classes.

Let \(V\) be the truly unrestricted infinite-horizon game.
Preserve any Monster prefix through \(H=D-3>0\); then visit
the nearest endpoint and immediately sweep to the other,
within three more time units. This creates a Monster in
\({\cal M}_D\) and satisfies the pointwise bound
\[
 T(\widetilde m,p)\le T(m,p)+3\,{\bf1}_{T(m,p)>H}.
\]
The universal near-best-response proof of
GLOBAL_MINIMAX_AND_CDF_DUALITY.md (Markov inequality)
therefore gives
\[
\boxed{
 V\le W_D\le(1+3/(D-3))V,\quad D>3;
 \qquad V=\lim_{D\to\infty}W_D=\inf_{D>3}W_D.
}                                                           \tag{3}
\]
The value \(W_D\) still optimizes *continuous paths*: it is NOT
a finite-dimensional LP and does NOT impose a turn bound.

## 2. Compact convex space of joint causal record measures

Set
\[
 K_D=\{(m,t,s):m\in{\cal M}_D,\quad0\le s\le t\le D\},
\]
a compact metric space. Let \(\Gamma_D\) be the set of pairs
of nonnegative Borel finite measures
\(\gamma^- ,\gamma^+\) on \(K_D\) for which there exists a
probability law \(\nu\in{\cal P}({\cal M}_D)\) satisfying
\[
(\pi_{m,t})_\#\gamma^-=
(\pi_{m,t})_\#\gamma^+
=\nu(dm)\,dt .                                          \tag{4}
\]
Each \(\gamma^\pm\) has mass \(D\), and disintegration supplies
causal probability kernels over \(0\le s\le t\), with the
SAME underlying Monster law \(\nu\).

**Lemma 1.** \(\Gamma_D\) is nonempty, convex and weakly
compact, with no finite-support or bounded-turn restriction.

**Proof.** The set of finite measures of mass \(D\) on
compact \(K_D\) is weakly compact. The common-marginal
condition is closed: its \(\nu\) is recovered as the
\(m\)-marginal divided by \(D\), and the map
\(\nu\mapsto\nu\otimes dt\) is weakly continuous.
It is linear in the measures, hence convex. Nonemptiness
follows by taking any \(\nu\) and the kernel \(s=0\).
QED.

For any legal Princess CDF \(F\) on \([0,D]\), write
\(F^-(t,x)=\Pr(P(t)<x)\) and
\(F^+(t,x)=\Pr(P(t)\le x)\), with arbitrary atoms.
Define the affine causal majorant
\[
 {\cal L}_{\gamma}(F)
  =D+\int_{K_D}F^-(s,m(s))\,d\gamma^-
      -\int_{K_D}F^+(s,m(s))\,d\gamma^+.              \tag{5}
\]

**Lemma 2 (correct semicontinuity direction).**
For every fixed legal \(F\), the map
\(\gamma\mapsto{\cal L}_{\gamma}(F)\) is
**lower semicontinuous** and affine on \(\Gamma_D\).
For a fixed \((m,t,s)\), the functions
\[
 (m,s)\mapsto F^-(s,m(s)),\qquad
 (m,s)\mapsto -F^+(s,m(s))
\]
are both bounded and lower semicontinuous.
Indeed each is the expectation over continuous Princess
paths \(p\) of the corresponding bounded **open-set**
indicator
\({\bf1}_{p(s)<m(s)}\) or
\(-{\bf1}_{p(s)\le m(s)}\). The latter is lower
semicontinuous because it is \({\bf1}_{p(s)>m(s)}-1\).
Fatou and Portmanteau prove the claim.
Consequently every sublevel set
\(\{\gamma:{\cal L}_{\gamma}(F)\le c\}\)
is weakly closed.

## 3. Exact recovery of the first-contact running records

For any Monster path \(m\) and legal CDF \(F\), define
\[
 A_m(t)=\min_{0\le s\le t}F^-(s,m(s)),\qquad
 B_m(t)=\max_{0\le s\le t}F^+(s,m(s)).
\]
The minimum/maximum ARE attained, including at contact
atoms, by the lsc/usc argument above. The common-quantile
Princess law \(F^\uparrow\) is 1-Lipschitz legal and has
\[
 C_m(F)=\mathbb E_{F^\uparrow}T(m,P)
 =\int_0^D[1+A_m(t)-B_m(t)]\,dt.                     \tag{6}
\]

For every \(\gamma\in\Gamma_D\) with Monster marginal
\(\nu\),
\[
{\cal L}_\gamma(F)\ge\int C_m(F)\,\nu(dm)
                    \ge\inf_{m\in{\cal M}_D} C_m(F). \tag{7}
\]
Conversely, choose a minimizing \(m\in{\cal M}_D\)
(the chronological capture cost is lsc in m),
set \(\nu=\delta_m\), and for almost all \(t\)
choose minimizers of the strict record and maximizers
of the closed record as the two selectors.
The compact-valued, Borel past argextrema admit
universally measurable selection, by the measurable
minimum/selection theorem; completing the kernels
on a null set suffices. This yields equality in (7).

Hence
\[
 \boxed{\min_{\gamma\in\Gamma_D}{\cal L}_\gamma(F)
      =\inf_{m\in{\cal M}_D} C_m(F).}                 \tag{8}
\]
The common-quantile coupling **simultaneously dominates**
all raw Princess laws with the same one-time CDF against
every Monster. Therefore
\[
 W_D=\sup_{F\ {\rm transport\!-\!legal}}
                    \min_{\gamma\in\Gamma_D}{\cal L}_\gamma(F).
                                                               \tag{9}
\]
Legal CDFs are exactly the transport-cone fields in
GLOBAL_CDF_TRANSPORT_LP.md. In particular, their set
is convex, and (5) is affine in F.

## 4. NEW strong duality, with attainment and no Princess compactness

**Theorem 1 (exact global finite-horizon strong record duality).**
\[
\boxed{
 W_D=\min_{\gamma\in\Gamma_D}
           \sup_{\substack{p\in{\cal A}_D}}
           {\cal R}_{\gamma}(p),\qquad
 {\cal R}_{\gamma}(p)
 =D+\int {\bf1}_{p(s)<m(s)}\,d\gamma^-
       -\int {\bf1}_{p(s)\le m(s)}\,d\gamma^+ .
}                                                           \tag{10}
\]
The minimum over ALL joint causal selector measures
\(\gamma\) **exists**. No optimal Princess path or
CDF is assumed, and each Monster law may have uncountable
support and trajectories with infinitely many reversals.

**Proof (finite-dimensional separation, no topology error).**
For any fixed \(\gamma\), writing a legal CDF as the
one-time marginals of a Princess path law \(\mu\),
Fubini and linearity imply
\[
 {\cal L}_\gamma(F)=\int{\cal R}_\gamma(p)\,\mu(dp),
\]
so
\[
 \sup_{F\ {\rm legal}}{\cal L}_{\gamma}(F)
   =\sup_{p\in{\cal A}_D}{\cal R}_{\gamma}(p).        \tag{11}
\]
Put \(w=\sup_F\min_\gamma{\cal L}_\gamma(F)=W_D\).
Weak duality immediately gives
\(\inf_\gamma\sup_F{\cal L}_\gamma(F)\ge w\).

Fix \(c>w\) and any finite list \(F_1,\ldots,F_n\)
of **actual transport-legal CDFs**. Consider the upper set
\[
 C=\{z\in{\mathbb R}^n:
      \exists\gamma\in\Gamma_D,\ 
      {\cal L}_\gamma(F_i)\le z_i\ (1\le i\le n)\}.
\]
It is nonempty, convex, upward closed, and **closed**:
if \(z^{(j)}\to z\), weak compactness gives a
subsequence of corresponding \(\gamma_j\)
converging to \(\gamma\), while Lemma 2 yields
\({\cal L}_\gamma(F_i)\le z_i\).

If \((c,\ldots,c)\notin C\), strict separation of
a point from a closed convex upward set gives
nonnegative coefficients \(\lambda_i\) with
\(\sum_i\lambda_i=1\) and
\[
 \min_{\gamma\in\Gamma_D}\sum_i\lambda_i
   {\cal L}_\gamma(F_i)>c.
\]
But \(F=\sum_i\lambda_iF_i\) is again a legal CDF,
and linearity of (5) makes its minimum equal
the left side; this contradicts \(w<c\).

Thus for each finite collection \(F_i\), a single
\(\gamma\) satisfies \({\cal L}_{\gamma}(F_i)\le c\)
for all of them. Since all these sublevel sets
are closed and \(\Gamma_D\) is compact, their
finite-intersection property provides a
\(\gamma_c\in\Gamma_D\) such that
\[
 {\cal L}_{\gamma_c}(F)\le c\quad
 \text{for EVERY legal CDF }F.
\]
Now let \(c\downarrow w\). Compactness of
the nested closed solution sets gives a
\(\gamma_*\) with
\(\sup_F{\cal L}_{\gamma_*}(F)\le w\).
Weak duality and (11) give equality and
attainment in (10). QED.

This proof explicitly avoids Sion arguments that would
incorrectly require upper semicontinuity of physical
first-contact reward in the maximizing Princess path.
The only compactness used is on the MINIMIZING
causal-selector side, with the correct lsc sign.

### Monster minimax follows as a byproduct

Let \(\nu_*\) be the Monster marginal of a
minimizing \(\gamma_*\).
For every pure Princess path p,
\[
 \mathbb E_{\nu_*}T(M,p)
 \le{\cal R}_{\gamma_*}(p)\le W_D.
\]
The first inequality follows from the record
majorant applied to the one-path Princess CDF.
Conversely \(W_D\le\sup_p\mathbb E_\nu T(M,p)\)
for every Monster law \(\nu\), by weak duality
against the completed-horizon Princess security.
Thus
\[
\boxed{
 W_D=\min_{\nu\in{\cal P}({\cal M}_D)}
       \sup_{p\in{\cal A}_D}\mathbb E_\nu T(M,p),
}                                                           \tag{12}
\]
and \(\nu_*\) is an **attained** Monster minimizer.
This independently recovers the completed-horizon
lopsided minimax theorem from the selector dual.

By (3),
\[
\boxed{
 V=\lim_{D\to\infty}\min_{\gamma\in\Gamma_D}
            \sup_{p\in{\cal A}_D}{\cal R}_\gamma(p).
}                                                           \tag{13}
\]
The hierarchy is monotone in D, not necessarily in
a fixed number of turns or a path-support size.

## 5. NEW exact symmetric single-radius reduction

Reflection of full paths induces the involution
\[
 R(m,t,s)=(-m,t,s),\qquad
 (\gamma^-,\gamma^+)\longmapsto
 (R_\#\gamma^+,R_\#\gamma^-).
\]
The set \(\Gamma_D\) is convex and invariant
under this involution. For a reflected Princess law
\(F^R\), strict and closed traces exchange under
reflection:
\[
 (F^R)^-(t,x)=1-F^+(t,-x),\qquad
 (F^R)^+(t,x)=1-F^-(t,-x).
\]
Hence \({\cal R}_{R\gamma}(p)={\cal R}_\gamma(-p)\).
If \(\gamma_*\) minimizes (10), its reflection
does too, and their arithmetic average also
minimizes (10), because the pure-path supremum
is convex in \(\gamma\).

It follows that **some** optimal \(\gamma_*\)
satisfies \(\gamma^+_*=R_\#\gamma^-_*\), and its
underlying Monster law \(\nu_*\) is symmetric.

Let \(\alpha\) be the pushforward of just
\(\gamma^-_*\) under
\((m,t,s)\mapsto(s,m(s))\), a nonnegative
measure of total mass D on spacetime.
Then for EVERY legal Princess path p,
\[
 {\cal R}_{\gamma_*}(p)
  =\int [\,{\bf1}_{p(s)<x}
          +{\bf1}_{p(s)>-x}\,]\,\alpha(ds,dx).
                                                               \tag{14}
\]
The integrand is an exact function only of
\(r(s)=|p(s)|\):
\[
\Phi(r,x)=
\begin{cases}
1+{\bf1}_{r<x}, & x>0,\\
{\bf1}_{r>0},   & x=0,\\
{\bf1}_{r>-x},  & x<0.
\end{cases}                                                   \tag{15}
\]
Strict inequalities at both thresholds are
ESSENTIAL; equality atoms have distinct costs.

Since the absolute value of any legal signed
Princess trajectory is a legal radial trajectory,
and every 1-Lipschitz \(r:[0,D]\to[0,1]\)
is realized by p=r, equation (14) gives the
**single-radius exact full-game dual**:
\[
\boxed{
 W_D=\min_{\substack{\nu\ {\rm symmetric}\\
           \gamma^-\ {\rm causal\ over\ }\nu\otimes dt}}
        \ \sup_{\substack{r:[0,D]\to[0,1]\\
                     |r'|\le1}}
         \int_{[0,D]\times[-1,1]}
                 \Phi(r(s),x)\,\alpha_{\gamma^-}(ds,dx).
}                                                           \tag{16}
\]
Here \(\gamma^+=R_\#\gamma^-\) by definition,
so no independent upper selector remains.
**The causal lift to complete Monster histories
is part of the constraint**: (16) cannot
be replaced by an arbitrary spatial measure.

The optimization over \(r\) still permits
center waits, moving atoms, arbitrarily many
radial reversals and Zeno. It is a global
scalar optimal-control problem, not a
finite wave/template hypothesis.

### Smooth-zone radial HJB and record-pressure balance

If \(\alpha(ds,dx)=h(s,x)\,ds\,dx\)
with locally continuous h in an open zone,
write
\[
 g(s,r)=\int_{-1}^{1}\Phi(r,x)h(s,x)\,dx.
\]
At \(0<r<1\) the derivative exists there and is
\[
 \boxed{\partial_rg(s,r)=h(s,-r)-h(s,r).}             \tag{17}
\]
The scalar future-value oracle obeys in smooth
interior regions
\[
 U_s+|U_r|+g(s,r)=0,\quad U(D,r)=0,
                                                               \tag{18}
\]
with inward-pointing state-constrained velocity
sets at \(r=0,1\), and additional jump/atomic
rules when \(\alpha\) is singular. If an optimal
radial path is uniformly strictly unsaturated
\((0<r<1,\,|r'|<1)\) on a compact interval,
two-sided calculus of variations gives
\[
 \boxed{h(s,-r(s))=h(s,r(s))\text{ a.e.}}             \tag{19}
\]
A positive-density family of calibrated,
unsaturated optimal rank paths propagates
(19) to the corresponding open flow strip
by the quantile change of variables.

This makes the free-boundary condition more
explicit than the earlier two-pressure notation:
**the negative/positive spatial traces of ONE
causal lower-record occupation density must match
where optimal Princess transport is unsaturated.**
At singular sources or on characteristics
\(|r'|=1\), the correct condition is the
exact threshold oracle (15), not the PDE alone.

### Canonical optimal Monster support survives strong duality

**Corollary.** The minimum in (16) is attained even after restricting
the underlying symmetric Monster law to the canonical form
\[
 \nu=\frac q2(\delta_{m_+}+\delta_{m_-})
          +(1-q)\nu_{\mathrm{rev}},
\]
where \(m_\pm\) are the fastest endpoint-to-endpoint sweeps and
\(\nu_{\mathrm{rev}}\) is symmetric and supported on paths
with at least one genuine direction reversal. No arbitrary
slow monotone paths are necessary in an optimal dual witness.

**Proof.** By (12), choose a symmetric optimal Monster law on
\({\cal M}_D\). All its paths have visited both endpoints by D;
a monotone nondecreasing such path starts at -1, and the
unit rightward sweep pointwise captures each Princess no
later than it. The reflected dominance holds for
nonincreasing paths. Replace the two monotone components
by the corresponding fast sweeps. Since D>=2 these
routes remain in \({\cal M}_D\), and replacement
cannot worsen the worst-Princess score. Weak duality
forces equality, so the modified canonical law
\(\nu_{\rm can}\) is also optimal.

Now **hold this Monster law fixed**. The compact convex
subset \(\Gamma_D(\nu_{\rm can})\) with prescribed
\((m,t)\)-marginal \(\nu_{\rm can}\otimes dt\)
has the same lsc/affine properties. Repeating Section 4's
finite-dimensional separation proves
\[
\min_{\gamma\in\Gamma_D(\nu_{\rm can})}
     \sup_p {\cal R}_\gamma(p)
 =\sup_F \int C_m(F)\,\nu_{\rm can}(dm)
 =\sup_p\mathbb E_{\nu_{\rm can}}T(M,p)=W_D.
\]
Thus selectors exist at **exactly** the global value
with the prescribed canonical underlying Monster law.
Symmetrizing them does not change that law, and gives
the one-radius representation (16). QED.

This is stronger than just canonicalizing an optimal
Monster distribution: an **attaining dual record selector
law can be made canonical simultaneously**. The
quantity q and the reversing-history occupation measure
remain unknown, and no finite turn bound follows.

## 6. NEW quantitative complementarity without Princess attainment

Let \(\gamma_*\in\Gamma_D\) be any optimal dual from
Theorem 1, with Monster marginal \(\nu_*\) and
optimal value \(w=W_D\).
Take a legal Princess CDF \(F_\epsilon\)
whose unrestricted completed-horizon
Monster security obeys
\(\inf_{m\in{\cal M}_D} C_m(F_\epsilon)
      \ge w-\epsilon\).
Then
\[
 w-\epsilon
 \le \int C_m(F_\epsilon)\,\nu_*(dm)
 \le {\cal L}_{\gamma_*}(F_\epsilon)
 \le w.                                             \tag{20}
\]
The **dual selector activity slack**
\[
 \begin{aligned}
 {\rm gap}_{\rm record}
 &=\int [F^-_\epsilon(s,m(s))-A_m^\epsilon(t)]\,d\gamma_*^-\\
 &\quad+\int[B_m^\epsilon(t)
              -F^+_\epsilon(s,m(s))]\,d\gamma_*^+
 \end{aligned}
\]
is nonnegative and at most \(\epsilon\).
Consequently for any \(\delta>0\),
\[
\boxed{
\gamma_*^-\{F^-_\epsilon(s,m(s))-A^\epsilon_m(t)>\delta\}
\le\epsilon/\delta
}                                                     \tag{21}
\]
and an identical estimate holds for upper records.

Let \(\mu^\uparrow_\epsilon\) be the ordered
Princess realization of \(F_\epsilon\).
Because \(\int{\cal R}_{\gamma_*}(p)
             d\mu^\uparrow_\epsilon(p)
       ={\cal L}_{\gamma_*}(F_\epsilon)\),
and \({\cal R}_{\gamma_*}(p)\le w\)
for EVERY pure Princess path,
\[
\boxed{
\mu^\uparrow_\epsilon
 \{p:{\cal R}_{\gamma_*}(p)\le w-\delta\}
       \le\epsilon/\delta.}                         \tag{22}
\]
The Monster marginal also obeys
\[
\boxed{
\nu_*\{m:C_m(F_\epsilon)\ge w-\epsilon+\delta\}
 \le\epsilon/\delta.}                               \tag{23}
\]
These are simultaneous global primal-dual
calibrations. They survive near-contact germs,
unattained Princess suprema, arbitrary atoms,
and continuous or terminal-Zeno Monster support.
An attained Princess solution would make
all three slacks zero; **attainment is NOT
required for the approximate statements**.

## 7. Exact tests, limitations, next constructive gate

The independently executed
\`packages/interval_global_closure/verify_global_strong_record_duality.py\`
regresses (15) against all signed strict/closed
indicator cases in 441 rational (p,x) pairs, including
the equality/collision boundaries. A finite synthetic
transport/selector primal-dual LP with 21 legal
Princess input paths, two/four completed Monster
routes, nine time knots and up to 176 causal
past-selector positions gives matching primal
and dual objectives under HiGHS. This fixture is
a finite *diagnostic*, not a computational proof
of (10) for all paths or a numerical game bound.
The theorem itself is the separation argument
in Section 4.

**Immediate substantive G2 target:** explicitly construct
the symmetric causal lower-record law \(\gamma^-\)
on full Monster histories and jointly calibrate
a global Princess CDF \(F\), using the exact radial
threshold functional (15) and quantitative
complementarity (20)-(23). The upper certificate
must solve the **global radial path oracle**, and
the lower certificate must cover every Monster
path via the unrestricted record Bellman
inequality. Do not return to a fixed number
of Monster turn templates or raw mixing
of frozen Princess trajectories.

**Not proved here:** the original exact constant,
a matching global saddle, a finite support or
finite turn cutoff, or an improved unrestricted
numerical bound. No Lean compilation/CI.
