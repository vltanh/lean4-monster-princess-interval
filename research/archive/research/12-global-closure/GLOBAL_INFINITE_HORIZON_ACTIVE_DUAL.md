# G2 CLOSED ABSTRACT GLOBAL DUAL: attained infinite-horizon one-clock minimax

Date: 2026-11-12. **This theorem applies to the ACTUAL unrestricted
infinite-horizon Princess–Monster game; there is no auxiliary common
completion horizon, path-support cutoff, turn-count bound or optimal
Princess attainment assumption.** It constructs an exact, ATTAINED
global causal-clock minimax representation with a finite active
occupation measure. The numerical value and both explicit equilibrium
strategies are still UNKNOWN: G2 constructive completion is OPEN.

Earlier steps:
- GLOBAL_MINIMAX_AND_CDF_DUALITY.md: existence of a symmetric
  optimal full Monster law and exact unrestricted lopsided minimax;
- GLOBAL_CDF_TRANSPORT_LP.md: all Princess CDFs as transport fields;
- GLOBAL_STRONG_RECORD_DUALITY.md: compact finite-completion
  causal-occupation strong duality;
- GLOBAL_MONOTONE_CAUSAL_CLOCK.md: causal time selection equals
  a monotone backward clock, and an endpoint sink is inert.

The result here removes the finite horizon completely **without**
claiming that finite-horizon active measures are automatically tight.

## 1. Global symmetric survival becomes a ONE-record functional

Let \({\cal A}\) be all continuous 1-Lipschitz paths
\([0,\infty)\to[-1,1]\), with arbitrary initial positions, and
\(T(m,p)\) the first equality/contact time. Let \(\nu\)
be a **symmetric** probability law on complete Monster trajectories
with
\[
 \tau_-(m)=\inf\{t\ge0:m(t)=-1\},\qquad
 \mathbb E_\nu\tau_-(M)<\infty.                       \tag{1}
\]
Here symmetry is invariance under reflection \(m\mapsto-m\).
It implies \(\mathbb E_\nu\tau_+(M)
           =\mathbb E_\nu\tau_-(M)<\infty\);
both endpoint visits occur almost surely, though their times
need not have a common deterministic bound.

For a symmetric transport-legal Princess CDF F, write
\(F^-(t,x)=\Pr(P(t)<x)\),
\(F^+(t,x)=\Pr(P(t)\le x)\).
Let
\[
 A_m(t)=\min_{0\le s\le t}F^-(s,m(s)),
\quad
 B_m(t)=\max_{0\le s\le t}F^+(s,m(s)).
\]
The extrema are actually attained, even with atoms and
infinitely many Monster reversals, because strict CDF
along a continuous path is lower semicontinuous,
and closed CDF is upper semicontinuous.

Symmetry of F gives the **exact pointwise identity**
\[
 F^+(s,x)=1-F^-(s,-x),
\quad B_m(t)=1-A_{-m}(t).
\]
Thus the ordered-quantile Princess law's survival
probability against m equals \(A_m(t)+A_{-m}(t)\).
Average over symmetric \(\nu\) and use Tonelli:
\[
 \boxed{
 {\cal C}_\nu(F):=\mathbb E_{\nu,F^\uparrow}T(M,P)
       =2\mathbb E_\nu\int_0^\infty A_m(t)\,dt
       =2\mathbb E_\nu\int_0^{\tau_-(m)}A_m(t)\,dt .
 }                                                   \tag{2}
\]
The last equality uses \(F^-(\tau_-,-1)=0\),
so the lower record is identically zero after the
Monster first visits -1. No finite completion time is assumed.
All integrals are finite because \(0\le A\le1\) and (1).

**This is the key global simplification:** in the symmetric
full game the independent closed upper-record process is
redundant. Both records are represented by just ONE
causal strict lower-record process, and that process has
finite total scoring mass \(\mathbb E_\nu\tau_-\).

## 2. Compact infinite-horizon ACTIVE causal selectors

Write
\(\lambda_\nu(dm,dt)
  ={\bf1}_{0\le t<\tau_-(m)}\,\nu(dm)\,dt\)
on \({\cal A}\times[0,\infty)\). It is a finite
Borel measure of total mass
\[
 M_\nu=\lambda_\nu(\mathrm{all})
     =\mathbb E_\nu\tau_-(M)<\infty.
\]

Define the Polish path/time space
\[
 K_\infty=\{(m,t,s):
     m\in{\cal A},\quad0\le s\le t<\infty\}.
\]
Let \(\Gamma^-(\nu)\) be the nonnegative finite
measures \(\gamma\) on \(K_\infty\) with
\[
 (\pi_{m,t})_\#\gamma=\lambda_\nu.                    \tag{3}
\]
Disintegration yields causal probability kernels
\(\kappa_{m,t}(ds)\), supported on the past interval
\(0\le s\le t\), for \(\lambda_\nu\)-almost all
\((m,t)\).

**Lemma 1.** \(\Gamma^-(\nu)\) is nonempty,
convex and **weakly compact**, even though the time
axis and Monster turn counts are unbounded.

**Proof.** The full path space \({\cal A}\) is compact
in the local-uniform topology. The fixed finite
marginal \(\lambda_\nu\) is tight; moreover any
measure \(\gamma\) satisfying (3) has
\[
 \gamma\{t>R\ \mathrm{or}\ s>R\}
 \le\lambda_\nu\{t>R\}
 =\mathbb E_\nu[(\tau_-(M)-R)_+]\longrightarrow0.
                                                               \tag{4}
\]
Here \(s\le t\) and integrability of \(\tau_-\)
give uniform tail control. Hence the entire set
is uniformly tight and of fixed finite mass
\(M_\nu\). Prokhorov yields relative compactness.
The support condition \(s\le t\) is closed,
and the \((m,t)\)-marginal remains \(\lambda_\nu\)
under weak convergence. Thus the set is closed,
hence compact. The choice \(s=0\) makes it
nonempty; convexity is immediate. QED.

This proves the missing tightness DIRECTLY for a
**fixed optimal infinite-horizon Monster law**.
A bounded active mass alone, with Monster laws
varying across horizon D, would not imply (4).

## 3. Exact symmetric radial reward and one-selector minimax

Any symmetric Princess marginal CDF is generated by
a probability distribution \(\rho\) on legal radial
paths \(r:[0,\infty)\to[0,1]\), \(|r'|\le1\),
followed by a fair reflection \(\pm r\).
Indeed take the absolute values of any symmetric
Princess path law; fair-reflecting those absolute
paths reproduces the same time marginals.
The common-quantile coupling then weakly improves
first-contact survival against every Monster.

For \(0\le r\le1\) and \(-1\le x\le1\), define
\[
 \Phi(r,x)=\mathbf1_{\{r<x\}}+
           \mathbf1_{\{r>-x\}}
 =\begin{cases}
 1+\mathbf1_{\{r<x\}},&x>0,\\
 \mathbf1_{\{r>0\}},&x=0,\\
 \mathbf1_{\{r>-x\}},&x<0 .
 \end{cases}                                          \tag{5}
\]
Then \(2F^-(s,x)=\int\Phi(r(s),x)\,\rho(dr)\).
Both strict comparisons are deliberate: at
a Monster/Princess equality the score drops.

For any \(\gamma\in\Gamma^-(\nu)\) define
\[
 {\cal R}_\gamma(r)
 =\int_{K_\infty}
     \Phi(r(s),m(s))\,\gamma(dm,dt,ds).                \tag{6}
\]
For any radial law \(\rho\), its marginal F satisfies
\[
 {\cal C}_\nu(F)
 =\min_{\gamma\in\Gamma^-(\nu)}
       \int{\cal R}_\gamma(r)\,\rho(dr).              \tag{7}
\]
Indeed for every \((m,t)\), the minimum of
\(2F^-(s,m(s))\) over \(0\le s\le t\)
is exactly the lower record in (2);
the minimum is attained, and measurable
argmin selection makes (7) exact.

**Lemma 2 (correct lsc sign).**
For every fixed radial trajectory r, the map
\(\gamma\mapsto{\cal R}_\gamma(r)\)
is affine and lower semicontinuous on the
compact set \(\Gamma^-(\nu)\). This is because
\[
 (m,t,s)\mapsto
 \mathbf1_{\{r(s)<m(s)\}}+
 \mathbf1_{\{r(s)>-m(s)\}}
\]
is a bounded nonnegative **lower semicontinuous**
function: each strict inequality defines an
open set in the local-uniform path/time topology.
Portmanteau applies to finite weakly converging
occupation measures.

## 4. NEW THEOREM: attained global strong duality without a horizon

**Theorem 1 (fixed-law horizon-free one-record duality).**
For **every** symmetric Monster law \(\nu\)
satisfying (1),
\[
 \boxed{
 \sup_{p\in{\cal A}}\mathbb E_\nu T(M,p)
  =\min_{\gamma\in\Gamma^-(\nu)}
            \sup_{\substack{r:[0,\infty)\to[0,1]\\
                       r\ 1\text{-Lipschitz}}}
                  {\cal R}_\gamma(r).
 }                                                    \tag{8}
\]
The minimum is attained. A maximizing Princess
path (or distribution) is **NOT** assumed to exist.

**Proof.** Since \(\nu\) is symmetric,
symmetrizing an arbitrary Princess law leaves
its expectation against \(\nu\) unchanged.
Replacing that symmetric Princess law by the
common ordered-quantile coupling of its CDF
cannot decrease its payoff against any Monster.
Every symmetric legal CDF has a radial-law
representation from Section 3. Therefore
\[
 \sup_{p\in{\cal A}}\mathbb E_\nu T(M,p)
 =\sup_{\rho\in{\cal P}({\cal R})}
      \min_{\gamma\in\Gamma^-(\nu)}
           \int{\cal R}_\gamma(r)\,\rho(dr).          \tag{9}
\]
Here \(\mathcal R\) is the full space of legal
nonnegative radius trajectories, not a finite bank.

Apply the finite-dimensional convex upper-set
separation proof of
GLOBAL_STRONG_RECORD_DUALITY.md, section 4,
with the present compact **active** selector
space \(\Gamma^-(\nu)\):
for each fixed radial-law \(\rho\), its
payoff is affine and lsc in \(\gamma\);
for each fixed \(\gamma\), it is affine in
the radial law \(\rho\). There is no need
to assume compactness or upper semicontinuity
of the maximizing radial-law space.
The compact dual, lsc sublevels, convexity,
and the finite-intersection property give
\[
 \sup_\rho\min_\gamma\int{\cal R}_\gamma\,d\rho
 =\min_\gamma\sup_\rho\int{\cal R}_\gamma\,d\rho.
\]
For fixed \(\gamma\), a linear expectation
over radial laws has supremum equal to the
supremum over pure radial paths.
Together with (9), this proves (8).
The same nested compact-intersection
argument attains the minimizing \(\gamma\).
QED.

**Theorem 2 (EXACT ATTAINED UNRESTRICTED GAME DUAL).**
Let
\[
 V=\sup_{\mu\in{\cal P}({\cal A})}
       \inf_{m\in{\cal A}}\mathbb E_\mu T(m,P)
\]
be the ORIGINAL infinite-horizon game value.
Then
\[
 \boxed{
 V=
 \min_{\substack{\nu\ {\rm symmetric}\\
       \mathbb E_\nu\tau_-(M)<\infty}}
       \ \min_{\gamma\in\Gamma^-(\nu)}
        \sup_{r\in{\cal R}}{\cal R}_\gamma(r).
 }                                                   \tag{10}
\]
The JOINT minimum is attained, and an
optimal pair can be chosen with
\[
 \boxed{
 \gamma(\mathrm{all})=\mathbb E_\nu\tau_-(M)
                 \le V\le U_{\rm best}
                 \simeq1.426129722845311.
 }                                                   \tag{11}
\]
The underlying optimal symmetric Monster law may
also be chosen in the canonical
fast-sweep-plus-reversals support class.

**Proof.** The established unrestricted lopsided
minimax theorem in
GLOBAL_MINIMAX_AND_CDF_DUALITY.md supplies an
attained symmetric Monster law \(\nu_*\)
with
\[
 \sup_p\mathbb E_{\nu_*}T(M,p)=V.
\]
For the stationary Princess \(p(t)\equiv-1\),
\(T(M,p)=\tau_-(M)\), so
\(\mathbb E_{\nu_*}\tau_-\le V<\infty\).
Theorem 1 now supplies an attaining
active selector \(\gamma_*\) for
this SAME \(\nu_*\), with radial
oracle exactly V and mass equal
to \(\mathbb E_{\nu_*}\tau_-\).
Every other admissible symmetric
\(\nu,\gamma\) gives, by Theorem 1,
a radial upper oracle equal or above
\(\sup_p\mathbb E_\nu T(M,p)\ge V\).
Hence the joint minimum exists and
equals V. Canonicalization of the
underlying Monster law into two
fast endpoint sweeps plus reversing
histories preserves optimality;
applying Theorem 1 again gives an
attaining selector for that
canonical law. QED.

**The active measure has uniformly bounded
physical size in the ACTUAL unrestricted game,
not merely along finite-horizon approximations.**
The existence of the global minimizing
finite measure follows from compactness on
the minimizing side, without using an
unjustified Princess weak compactness.

## 5. Exact deterministic monotone-clock form

For fixed \(\nu\) in (10), disintegrate
\(\gamma(dm,dt,ds)
 =\nu(dm)\mathbf1_{t<\tau_-(m)}dt
             \kappa_{m,t}(ds)\).
The conditional selected-time
marginal \(\eta_m(ds)\) has mass
\(\tau_-(m)\) and satisfies
\[
 \eta_m([0,u])\ge\min(u,\tau_-(m))
 \quad(u\ge0).                                      \tag{12}
\]
The necessity proof is causal:
all scoring times \(t\le u\)
select \(s\le t\le u\).

Conversely define the conditional
time quantile
\[
 s_m(t)=\inf\{u:
        \eta_m([0,u])\ge t\},
       \qquad0<t<\tau_-(m).                          \tag{13}
\]
It is measurable, nondecreasing in t,
satisfies \(0\le s_m(t)\le t\)
by (12), and pushes Lebesgue measure
on \([0,\tau_-(m))\) exactly onto
\(\eta_m\). Thus every randomized
causal selector is payoff-equivalent
to **one deterministic monotone
backward clock**, separately along
each complete Monster trajectory.

Combining this with Theorem 2:
\[
\boxed{
 V=\min_{\substack{\nu\ {\rm symmetric}\\
             \mathbb E_\nu\tau_-<\infty\\
             s_m(t)\ {\rm nondecreasing},\
             0\le s_m(t)\le t}}
 \ \sup_{\substack{r:[0,\infty)\to[0,1]\\|r'|\le1}}
  \mathbb E_{m\sim\nu}
    \int_0^{\tau_-(m)}
     \Phi(r(s_m(t)),m(s_m(t)))\,dt.
}                                                    \tag{14}
\]
The minimum in (14) is ATTAINED.
No random choice of a *finite list*
of past contact times is required.

The upper value of ANY supplied
feasible pair (\(\nu,s_m\))
is a rigorous bound for the
unrestricted game when the
global radial oracle is solved.
A full saddle certificate additionally
needs a matching Princess lower law
(or an approaching family), certified
against ALL Monster paths by
the global record Bellman inequality.

### Explicit sweep source in the canonical global optimizer

The prior exact canonical Monster reduction gives an
optimal symmetric law of the form
\[
 \nu_*=\tfrac q2(\delta_{m_+}+\delta_{m_-})
            +(1-q)\nu_{\mathrm{rev}},
\]
where \(m_+(t)=\min(t-1,1)\) and
\(m_-(t)=\max(1-t,-1)\);
\(\nu_{\mathrm{rev}}\) is symmetric and supported
on trajectories whose prefix **BEFORE the second
endpoint visit** is nonmonotone. Every route
can be stopped at that second endpoint
without affecting any Princess first contact;
the precompletion qualification rules out
counting gratuitous postcapture turns.

For the rightward sweep \(m_+\),
\(\tau_-(m_+)=0\): **it contributes
zero active lower-record occupation**.
For the leftward sweep \(m_-\),
\(\tau_-(m_-)=2\).
Along this sweep every legal strict CDF trace
\(F^-(t,m_-(t))\) is nonincreasing in t,
by the speed-one transport inequality.
Therefore the exact historical lower
record is always its CURRENT value:
\[
 A_{m_-}(t)=F^-(t,1-t),\qquad0\le t\le2.
\]
For **every legal Princess CDF** the
selector clock \(s_{m_-}(t)=t\) is thus
at least as good for the minimizing
dual as any other causal selector.
It can be imposed without loss
on a joint optimal canonical clock.

Consequently the minimizing active
occupation admits the exact,
UNIVERSAL decomposition
\[
 \boxed{
 \alpha_*=\frac q2\,\mathbf1_{0\le t\le2}
                      dt\,\delta_{x=1-t}
              +\alpha_{\mathrm{rev}},
 }                                                    \tag{18}
\]
and the **full-game** radial oracle is
\[
 \boxed{
 V=\sup_{r\ {\rm legal}}
 \left\{\frac q2\int_0^2\Phi(r(t),1-t)\,dt
           +\int\Phi(r(s),x)\,
                        \alpha_{\mathrm{rev}}(ds,dx)
 \right\}                                             \tag{19}
\]
for at least one optimal canonical pair
\((q,\alpha_{\mathrm{rev}})\).
Here \(\alpha_{\mathrm{rev}}\) has a causal
lift to complete reversing trajectories;
it is NOT an arbitrary positive spacetime
measure. This is an exact identity
at the (unknown) global equilibrium,
not an assertion that we know its
parameters or that q must be positive.

The known sweep source is
\[
 \frac q2\int_0^1
       [1+\mathbf1_{\{r(t)<1-t\}}]dt
 +\frac q2\int_1^2
       \mathbf1_{\{r(t)>t-1\}}dt.                     \tag{20}
\]
The unresolved obstacle is therefore the
**reversing-history pressure needed to
calibrate the two open characteristic
threshold regions adjacent to (1,0)**.
This is much more specific than mixing
individual finite Monster routes.

As an exact fixed-law regression,
take \(q=1\), i.e. the fair pair of
sweeps with no reversing occupation.
The optimal clock above has
active occupation total mass one,
\(\alpha=(1/2)dt\,\delta_{x=1-t}\)
for \(0\le t\le2\), and the radial
oracle (20) has supremum EXACTLY \(3/2\).
For the legal one-sided radial
path \(r_\epsilon(t)=|\min(-1+\epsilon+t,1)|\),
the oracle score is
\(3/2-\epsilon/4\).
No legal radius attains \(3/2\):
a maximizer would require
\(r(t)<1-t\) almost everywhere
before t=1 and
\(r(t)>t-1\) almost everywhere
after t=1, forcing \(r(1)=0\)
and then violating the speed-one
bound on the second interval.
This matches the independent
physical first-contact theorem in
GLOBAL_DUAL_RECORD_PRESSURE_HJB.md.

This worked example verifies that
a finite **active** measure and an
attained **dual clock** are compatible
with an UNATTAINED Princess optimum.

## 6. Quantitative horizon-free KKT / calibration

Let \(\nu_*,\gamma_*\) attain (10),
and let \(F_\epsilon\) be a symmetric
legal Princess CDF that guarantees
\(V-\epsilon\) against every
unrestricted Monster.
Using (2), (7), and the global
dual value \(V\), we have
\[
V-\epsilon
 \le {\cal C}_{\nu_*}(F_\epsilon)
 \le 2\int F^-_\epsilon(s,m(s))\,d\gamma_*
 \le V.                                             \tag{15}
\]
The **actual record selector slack** is
\[
\int 2[F^-_\epsilon(s,m(s))
       -A^\epsilon_m(t)]\,d\gamma_*
  \le\epsilon.                                      \tag{16}
\]
The exact nonnegative integrand is
controlled despite arbitrary
first-contact germs, atoms and
infinite Monster reversals.

For the ordered quantile realization
of the symmetric CDF, let \(\rho_\epsilon\)
be the corresponding law of absolute
radial paths. Then
\[
 \int {\cal R}_{\gamma_*}(r)\,
             \rho_\epsilon(dr)
  =2\int F^-_\epsilon\,d\gamma_*
  \ge V-\epsilon.
\]
Since \({\cal R}_{\gamma_*}(r)\le V\)
for EVERY legal pure radius r,
\[
 \boxed{
 \rho_\epsilon
  \{r:{\cal R}_{\gamma_*}(r)\le V-\delta\}
  \le\epsilon/\delta.
 }                                                   \tag{17}
\]
And \(\gamma_*\)-mass of history
selectors whose strict rank price
exceeds the actual record by more
than \(\delta>0\) is at most
\(\epsilon/(2\delta)\).
These estimates remain true without
a Princess optimizer.

If a maximizing Princess CDF F*
exists, its positive-mass radial paths
saturate the dual oracle
and its Monster response Bellman
value saturates V on the support
of \(\nu_*\). If no maximizer
exists, the same statements hold
quantitatively along any
approaching sequence.

## 7. What is NOW solved versus what remains open

**Closed analytically:**
- Exact infinite-horizon two-player
  lopsided minimax and Monster
  attainment (earlier G1).
- Exact infinite-horizon **strong
  causal-record dual with
  attained active selector**,
  now additionally of finite
  total mass \(\le V\).
- Elimination of the independent
  upper-record occupation by
  symmetry and elimination of
  all stochastic history-selector
  kernels by a deterministic
  nondecreasing backward clock.
- Exact one-radius global Princess
  oracle and quantitative
  near-optimality / record
  complementarity.
- All without a Monster turn
  cutoff, finite path basis,
  common absorption horizon
  or Princess attainment.

**Still OPEN:**
- Explicit equations/functions
  identifying the minimizing
  *Monster path distribution*
  \(\nu_*\) and its causal clock.
- A matching explicit legal
  Princess CDF (or uniform
  approaching family).
- The exact numerical/rational/
  algebraic game value and a
  complete two-sided saddle
  certificate. The rigorous
  existing bounds are UNCHANGED:
  \(1.4175898349\ldots\le V
                  \le1.4261297228\ldots\).
- A Lean kernel formalization.
  No Lean compilation or CI was
  requested/run in this attack.

**Next constructive attack:** solve
the Euler–Lagrange/free-boundary
matching of the **finite-mass
global active lower-record
occupation** (14) to the
Princess's rank-transport CDF.
The monotone clock and canonical
Monster support give the exact
feasible class; the radial
oracle gives the global upper
separation; the existing
unrestricted Monster Bellman
gives the matching lower gate.
