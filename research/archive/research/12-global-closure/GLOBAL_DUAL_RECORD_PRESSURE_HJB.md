# G2: Global record-occupation dual, Princess HJB, and free-flow balance

Date: 2026-11-12. **New constructive verification principle and one fully
solved unrestricted-path *restricted Monster subgame*.** The exact value
of the original unrestricted two-player game remains UNKNOWN. No
improvement to the branch's certified numerical interval is claimed.

**Subsequent global closure:** the general causal-selector upper certificate
below has now been proved to be an **exact attained dual** for the
actual unrestricted game after symmetry, lower-record absorption
at the Monster's first -1 visit, and deterministic monotone
causal-clock compression. See
[GLOBAL_INFINITE_HORIZON_ACTIVE_DUAL.md](GLOBAL_INFINITE_HORIZON_ACTIVE_DUAL.md).
The singular one-sided contact-germ transmission theorem is in
[GLOBAL_RADIAL_CONTACT_GERMS.md](GLOBAL_RADIAL_CONTACT_GERMS.md).
The original note's conditional wording is retained as historical
provenance, not as the latest state of the duality question.


## 1. Why a new dual variable is needed

GLOBAL_CDF_TRANSPORT_LP.md replaces a frozen Princess path bank with all
speed-one-transport-compatible CDF fields. However its payoff inequalities
still quantify over every possible Monster history. The appropriate
dual is a **law of complete Monster paths, together with two causal
record-selector kernels**, not a probability distribution over their
positions at one time.

This note gives an exact global upper certificate for *arbitrary*
completed Monster path laws, including diffuse supports, waits,
infinitely many turns and terminal Zeno paths. It turns the Princess
side of the coupled problem into **one scalar global optimal-control
oracle**. It also derives the local pressure-balance equation that
any smooth unsaturated part of an attained equilibrium must satisfy.

The older GLOBAL_SELECTOR_PLANE_ORACLE.md and
SELECTOR_MINIMAX_SYNTHESIS.md use finite supported Monster banks.
The theorem here does not make that support assumption, does not
replace the pure-path supremum with a sampled Princess list, and
uses no prior finite-turn bound.

## 2. Physical strict/closed CDF records attain their extrema

Fix an arbitrary legal Princess law \(\mu\) on continuous speed-one
paths, with time-dependent strict and closed CDFs \(F^-,F^+\).
For a continuous Monster path \(m\) and any finite \(t\),
\[
s\mapsto F^-(s,m(s))=\Pr_\mu(P(s)<m(s))
\]
is **lower semicontinuous**, and
\[
s\mapsto F^+(s,m(s))=\Pr_\mu(P(s)\le m(s))
\]
is **upper semicontinuous**.

Indeed for every deterministic continuous \(p\), the strict-contact
comparison indicator \({\bf1}_{p(s)<m(s)}\) is lower
semicontinuous in \(s\); the closed-comparison indicator is
upper semicontinuous. Fatou's lemma, applied also to
complements, preserves these statements under expectation.
Therefore the chronological strict minimum and closed maximum
over the compact interval \([0,t]\) **are attained**:
\[
 A_m(t)=\min_{0\le s\le t}F^-(s,m(s)),\qquad
 B_m(t)=\max_{0\le s\le t}F^+(s,m(s)).
\]
This is true despite atoms, coincidences and infinite Monster turns.
Both record values are bounded and measurable functions of \(t\).

**Important distinction:** exact record values are attained for
physical path laws, but this does NOT make the CDF's directional
derivative depend only on values at the currently attaining
record positions. The directional perturbation can be discontinuous
there, and arbitrarily near-active record germs still matter.
GLOBAL_CDF_VARIATIONAL_STATIONARITY.md handles that derivative
correctly.

## 3. Arbitrary Monster-law causal record occupation

Choose a completion horizon \(D<\infty\).
Let \(\nu\) be **any** Borel probability law on continuous Monster
trajectories which have all visited both endpoints by \(D\).
It need not have finite support or any common turn bound.

For each Monster trajectory \(m\) and each scoring time
\(t\in[0,D]\), choose measurable probability kernels
\(\kappa^-_{m,t}\) and \(\kappa^+_{m,t}\) on past times
\(s\in[0,t]\). They need not be active for a particular CDF.

Push the measures
\(\nu(dm)\,dt\,\kappa^\pm_{m,t}(ds)\)
through \((m,t,s)\mapsto(s,m(s))\), obtaining nonnegative
Borel record-occupation measures \(\alpha^-,\alpha^+\) on
\([0,D]\times[-1,1]\). Each has mass exactly \(D\).
Causality is encoded by the existence of the above kernels;
a generic pair of equal-mass spatial measures is NOT sufficient.

Define the linear Princess-field functional
\[
 {\cal L}_\alpha(F)
  = D+\int F^-(s,x)\,\alpha^-(ds,dx)
       -\int F^+(s,x)\,\alpha^+(ds,dx).                \tag{1}
\]
The exact ordered quantile capture cost of \(m\) is
\[
 C_m(F)
  =\int_0^D [1+A_m(t)-B_m(t)]\,dt.                     \tag{2}
\]

**Theorem 1 (unrestricted global causal-selector upper bound).**
For every legal Princess CDF \(F\),
\[
 \int C_m(F)\,\nu(dm)\le{\cal L}_\alpha(F).             \tag{3}
\]
Moreover put, for every legal pure Princess path \(p\),
\[
 {\cal R}_\alpha(p)
 =D+\int{\bf1}_{p(s)<x}\,\alpha^-(ds,dx)
      -\int{\bf1}_{p(s)\le x}\,\alpha^+(ds,dx).         \tag{4}
\]
Then
\[
 \sup_{F\ {\rm legal}}{\cal L}_\alpha(F)
   =\sup_{p\ {\rm legal}}{\cal R}_\alpha(p).           \tag{5}
\]
Consequently the original unrestricted game's security value \(V\)
obeys the **globally valid** upper bound
\[
 \boxed{V\le {\cal U}_\alpha:=
                 \sup_{p\ {\rm any\ legal\ path}}
                        {\cal R}_\alpha(p).}          \tag{6}
\]
No finite path bank is present in this upper bound.

**Proof.** The average of any strict CDF trace over past-selector
times is at least its historical minimum; the average of any
closed trace is at most its historical maximum. Integrate this
pair of pointwise bounds over \(dt\,d\nu\) to get (3).
For an arbitrary Princess path law \(\mu\), Fubini yields
\[
 {\cal L}_\alpha(F_\mu)
 =\int {\cal R}_\alpha(p)\,\mu(dp).
\]
The right-hand side cannot exceed the supremum over pure paths,
and every pure-path CDF is itself feasible. This proves (5).
The common-quantile Princess law dominates all other laws with
the same time marginals against every Monster path; thus for
any physical Princess law \(\mu\), its payoff against \(\nu\) is at
most \(\int C_m(F_\mu)d\nu\), which by (3)--(5) is at most
\({\cal U}_\alpha\). Since \(\nu\) is a legal Monster mixed
strategy, weak duality proves (6). QED.

This is a *sufficient* upper certificate. We do not claim that
optimizing jointly over all \(\nu,\kappa^\pm\) has attained a
minimizer or yet proved a new global strong-duality theorem
for the selector-kernel class.

### Coupled exact saddle verification

Suppose a legal CDF \(F_*\), any completed Monster law
\(\nu\) and causal selectors yield
\[
 \inf_{m\ {\rm legal}} C_m(F_*)\ge c,\qquad
 \sup_{p\ {\rm legal}}{\cal R}_\alpha(p)\le c.          \tag{7}
\]
Then **the unrestricted game is solved: \(V=c\)**.
The first is a global Monster Bellman lower certificate, the
second a global Princess control/HJB upper certificate.
No separate finite-bank restriction is needed.

Indeed
\[
c\le\inf_m C_m(F_*)\le
\int C_m(F_*)d\nu\le{\cal L}_\alpha(F_*)
\le{\cal U}_\alpha\le c.
\]
Every inequality is an equality, so the selector kernels
are automatically active almost everywhere under
\(\nu(dm)\,dt\), and \(\nu\) is concentrated on optimal
Monster responses to \(F_*\). Similarly almost every
quantile path of \(F_*\) is optimal for (4).

With certified residuals \(c-\epsilon_M\) and
\(c+\epsilon_P\) on the two sides of (7), the sound
unrestricted interval is
\[
c-\epsilon_M\le V\le c+\epsilon_P.                    \tag{8}
\]
This is an *unconditional* certificate format, not an
assertion that a matching \(F_*,\nu,\kappa,c\) has been found.

## 4. One scalar Princess HJB for regular record occupation

The general pure-path problem (6) allows arbitrary Borel
record-occupation measures, including contact atoms and
mass concentrated at a past record time. In that generality
(4), with its strict/closed inequalities, is the exact
definition: do not erase singular impulses by writing a
spurious smooth PDE.

On a region where both occupation measures have bounded,
continuous densities \(k^\pm(t,x)\) with respect to
\(dt\,dx\), define
\[
 w(t,x)=k^-(t,x)-k^+(t,x),\qquad
 r(t,y)=\int_y^1 w(t,x)\,dx.                          \tag{9}
\]
If the occupations are absolutely continuous throughout
the scored spacetime domain, the strict and closed
comparisons coincide \(\alpha^\pm\)-a.e., and
\[
 {\cal R}_\alpha(p)
   =D+\int_0^D r(t,p(t))\,dt.                         \tag{10}
\]

Set
\[
 U(t,x)=\sup_{\substack{p(t)=x\\|p'|\le1,\;|p|\le1}}
                  \int_t^D r(s,p(s))\,ds.
\]
The deterministic dynamic-programming principle yields,
where differentiable (or in the standard viscosity sense),
\[
 \boxed{U_t+|U_x|+r(t,x)=0,\qquad U(D,x)=0}            \tag{11}
\]
in the open physical interval, and
\[
 {\cal U}_\alpha=D+\max_{x\in[-1,1]}U(0,x).            \tag{12}
\]
At \(x=-1\), the admissible velocities are \([0,1]\),
so the boundary Hamiltonian is \(\max(0,U_x)\);
at \(x=+1\), they are \([-1,0]\), giving
\(\max(0,-U_x)\). Equivalently use state-constrained
dynamic programming at the endpoints.

The Princess HJB (11) is a **single global one-particle
control problem** even when \(\nu\) has continuum support
and individual Monster paths reverse infinitely many times.
Causal contact atoms require jump/payoff conditions in
addition to its smooth-region PDE; the exact equation (4)
is the fallback.

This is a useful inversion of the original search: after
constructing a candidate global record-occupation law,
one verifies an upper bound by solving a scalar HJB over
ALL Princess paths, not by extending a finite Princess
response list.

## 5. A new free-flow pressure-balance necessary condition

**Theorem 2 (source cancellation on unsaturated optimal
Princess trajectories).** Assume the occupation measures
are absolutely continuous with a continuous difference density
\(w\) on an open spacetime strip \(O\). Suppose a legal pure
path \(p\) **maximizes** (10) among all legal Princess paths
and, on a compact interval \(I\) contained in that strip,
\[
 |p(t)|\le1-\eta,\qquad |p'(t)|\le1-\eta
 \quad\text{a.e. on }I                                \tag{13}
\]
for some \(\eta>0\).
Then
\[
 \boxed{w(t,p(t))=0\quad\text{for almost every }t\in I.} \tag{14}
\]

**Proof.** For every smooth \(\varphi\) supported in the
interior of \(I\), \(p_\epsilon=p+\epsilon\varphi\)
remains in the arena and remains speed-one legal when
\(|\epsilon|\) is sufficiently small, by (13).
The two-sided first variation of (10) at this maximizing
path must vanish:
\[
 0=\int_I r_x(t,p(t))\varphi(t)\,dt
   =-\int_I w(t,p(t))\varphi(t)\,dt.
\]
The fundamental lemma of the calculus of variations gives
(14). QED.

For a **calibrated coupled certificate** (7), almost every
Princess quantile path is a maximizing pure path in (4).
If these quantile paths fill an open positive-density CDF
strip and have a common strict speed margin there, then
(14) implies
\[
 \boxed{k^-(t,x)=k^+(t,x)
       \quad\text{for a.e. }(t,x)\text{ in that strip}.} \tag{15}
\]
To justify the last implication, integrate (14) over ranks
and use the quantile change of variables
\(dq=\rho(t,x)\,dx\) in a positive-density strip. This is
a **conditional necessary free-boundary balance equation**,
not a claim that the unknown equilibrium has a smooth patch
or that its dual occupation lacks atoms.

The structural consequence is sharp: an optimal Princess
family may have unsaturated interior transport only where
its two opposing Monster record prices balance. An
unbalanced nonzero regular record source must be supported
on saturated characteristics \(|p'|=1\), on state/contact
interfaces, or outside the actual optimal Princess support.

### Approximate calibration / no-attainment version

If \({\cal U}_\alpha-{\cal L}_\alpha(F)\le\epsilon\)
for an ordered Princess field \(F\), then for every
\(\delta>0\),
\[
 \mathrm{Leb}\{q:
 {\cal R}_\alpha(Q(\cdot,q))\le{\cal U}_\alpha-\delta\}
 \le\epsilon/\delta.                                \tag{16}
\]
Indeed every pure path has score at most \({\cal U}_\alpha\),
and the mean deficit over quantile ranks is at most
\(\epsilon\). Thus near-saddle fields constrain the
**full rank distribution** of path-optimality defects even
when no exact Princess maximizer exists.

## 6. Exact two-sweep regression: solved subgame, nonattainment

This is a genuine exact infinite-path response calculation,
not a numerical sample and **not** the original full game's value.

Let
\[
m_+(t)=t-1,\qquad m_-(t)=1-t,\quad 0\le t\le2,
\]
extended constantly from their endpoints thereafter.
Both are legal, visit both endpoints by 2, and have **no
restrictions on the Princess's path**.
Let \(\nu=(\delta_{m_+}+\delta_{m_-})/2\).

The causal record selectors are exact for EVERY legal CDF:
for the rightward sweep, the lower strict record is the
initial endpoint \((0,-1)\), and the upper closed record
is the current position \((t,m_+(t))\). For the leftward
sweep, the lower strict record is current and upper closed
record is the initial endpoint \((0,+1)\). Consequently
\[
 {\cal L}_\alpha(F)=\int C_m(F)d\nu
 =\frac12\int_0^2
 [1+F^-(t,1-t)-F^+(t,t-1)]\,dt.                     \tag{17}
\]
The path oracle (4) equals the **actual** fair-sweep
expected first-contact time for every pure Princess path.

Write its capture times \(T_+,T_-\), both at most 2.
At time 1 the two Monsters occupy the same location 0.
Every Princess has met at least one of them by time 1,
so \(\min(T_+,T_-)\le1\), while
\(\max(T_+,T_-)\le2\). Thus
\[
 \frac{T_++T_-}{2}\le\frac32.                         \tag{18}
\]
Equality is **impossible for any legal pure Princess
path**: it would require capture by one Monster exactly
at time 1 and by the other at time 2; but a first capture
at time 1 forces \(p(1)=0\), so BOTH Monsters contact
that Princess at time 1.

For every \(0<\epsilon<1\), take the legal Princess path
\[
 p_\epsilon(t)=\min(-1+\epsilon+t,1).
\]
It meets \(m_+\) at time 2 and \(m_-\) at
\(1-\epsilon/2\). Therefore
\[
 \mathbb E_\nu T(M,p_\epsilon)
   =\frac32-\frac{\epsilon}{4}
   \underset{\epsilon\downarrow0}{\longrightarrow}\frac32. \tag{19}
\]
A fair law on \(p_\epsilon\) and its reflection
guarantees the same \(3/2-\epsilon/4\) against EACH
of the two available Monster sweeps. Hence the **entire
restricted two-sweep subgame** is solved exactly:
\[
 \boxed{
 \sup_\mu\min\{\mathbb E_\mu T(m_+,P),
              \mathbb E_\mu T(m_-,P)\}
 =\frac32.}                                         \tag{20}
\]
The Princess supremum is **not attained**, even by an
arbitrary randomized legal law: for each pure Princess
path the fair-sweep score is strictly below \(3/2\),
so every probability-law average is strictly below it.

This example has three consequences for G2:
1. The dual path oracle genuinely needs a **supremum**
   and must retain one-sided near-contact germs.
2. Symmetry and common-ordered-quantile representations
   do NOT by themselves imply a maximizing physical
   Princess law exists.
3. A valid global record-occupation upper certificate
   can be **exact for every Princess path** without any
   finite Princess response bank; here its optimum is
   \(3/2\), substantially weaker than the known full-game
   upper \(1.4261297228\ldots\).

The last point is a regression, not an improvement to V.

## 7. NEW unrestricted optimal-Monster reversal-mass theorem

The solved two-sweep game forces a quantitative **whole-game support
condition**, not merely a statement about the restricted game.

Call a Monster path **nonreversing** when it is globally monotone
(nondecreasing or nonincreasing); pauses and arbitrarily slow
monotone motion are allowed. Let \(\nu_*\) be ANY optimal Monster
trajectory law for the original unrestricted game; its existence
was proved in GLOBAL_MINIMAX_AND_CDF_DUALITY.md.

**Lemma (optimal laws complete individually).** Almost every
path under \(\nu_*\) visits BOTH endpoints in finite time.
Indeed the Princess has two legal stationary paths
\(p_-(t)\equiv-1\) and \(p_+(t)\equiv+1\). The optimal
Monster law has finite expected capture time against each.
A positive mass of Monster paths that never visits either
specified endpoint would give infinite expectation against
that stationary Princess. Discard the union of these two
null events.

**Lemma (fast monotone sweep dominates all nonreversing paths).**
A globally nondecreasing, individually completed Monster path
must start at \(-1\); by speed one it satisfies
\(m(t)\le m_+(t)=\min(-1+t,1)\) for every \(t\).
For any continuous legal Princess \(p\), the difference
\(m_+(0)-p(0)\le0\), and at the time \(T(m,p)\) of a
finite encounter, \(m_+(T)\ge m(T)=p(T)\).
The intermediate value theorem forces
\(T(m_+,p)\le T(m,p)\). Reflection gives
\(T(m_-,p)\le T(m,p)\) for every nonincreasing completed
Monster. The pointwise dominance includes slow segments,
pauses, and any continuous monotone trajectory.

**Theorem (canonical fast-sweep plus reversing decomposition).**
There exists a **symmetric globally optimal** Monster
trajectory law of the form
\[
 \boxed{\nu_*=
 \frac{q_*}{2}\delta_{m_+}
 +\frac{q_*}{2}\delta_{m_-}
 +(1-q_*)\,\nu_{\rm rev}},                            \tag{21a}
\]
where \(\nu_{\rm rev}\) is a reflection-symmetric law
supported on paths that reverse direction at least once,
and \(0\le q_*\le1\). In particular, no continuously
distributed *slower nonreversing* histories are needed in
the support of **some** globally optimal Monster law.

**Proof.** Start with a symmetric optimal Monster law
whose existence is proved in
GLOBAL_MINIMAX_AND_CDF_DUALITY.md. By the completion lemma
above, its trajectories visit both endpoints almost surely.
On its nondecreasing subset replace each path by the
fast rightward endpoint sweep \(m_+\); on its nonincreasing
subset replace it by \(m_-\); leave all reversing
trajectories unchanged. This is a Borel path-law
pushforward: monotonicity is a Borel (in fact closed)
property in the path topology, and the replacement is
piecewise constant/identity. The pointwise sweep-dominance
lemma guarantees that the replacement cannot **increase**
the Monster's expected capture time against any pure
Princess path. Thus its worst Princess payoff is at most
the original optimal value \(V\). Full-game weak duality
forces the new law's worst payoff to be at least \(V\),
so it is also optimal. Reflection commutes with this map,
preserving symmetry. The two sweep masses must agree by
symmetry, giving (21a). QED.

This is an existence of a canonical optimal representative,
**not** a proof that every optimum is free of slow monotone
paths. The quantitative result below in fact bounds
\(q_*\) uniformly for ALL optimal laws.

For a symmetric ordered Princess field \(F\), the
canonical decomposition makes the coupled Monster
functional completely explicit on its monotone sector:
\[
 \mathcal C_{\nu_*}(F)
 =\frac{q_*}{2}\int_0^2
   [1+F^-(t,1-t)-F^+(t,t-1)]\,dt
   +(1-q_*)\mathcal C_{\nu_{\rm rev}}(F).              \tag{21b}
\]
Consequently the unknown signed pressure can be split
into an exact **characteristic sweep source** and a
reversing-history record-occupation source. Equation
(21b) is a global identity, not a finite route-bank
assumption. It isolates the genuinely unsolved part of
the Monster support.

**Lemma (exact unrestricted response to the two-runner Princess law).**
Let \(\mu_\epsilon\) be the fair-reflected Princess law on
\(p_\epsilon(t)=\min(-1+\epsilon+t,1)\)
and \(p_\epsilon^{\rm ref}(t)=-p_\epsilon(t)\).
Write \(a=1-\epsilon\).
Then for **every** legal Monster trajectory \(m\),
\[
\mathbb E_{\mu_\epsilon}T(m,P)\ge \frac{a}{2}
 =\frac{1-\epsilon}{2},                              \tag{21}
\]
and this lower bound is **attained** by the Monster that starts
at \(p_\epsilon(0)\) and follows \(p_\epsilon\) up to time \(a\).

**Proof.** Until time \(a\) the two Princess paths are at
\(p_\epsilon(t)=-a+t\) and
\(p_\epsilon^{\rm ref}(t)=a-t\); they meet at the
center at time \(a\).
Suppose a Monster could capture both at times
\(t_1\le t_2<a\). Whether the left runner or right
runner is hit first, the distance between the two
captured positions at their respective contact times
is \(2a-t_1-t_2\). The Monster's speed bound gives
\[
 t_2-t_1\ge2a-t_1-t_2,
\]
which forces \(t_2\ge a\), a contradiction. Hence
\(\max(T(m,p_\epsilon),T(m,p_\epsilon^{\rm ref}))
\ge a\), so their average is at least \(a/2\).
If the Monster starts at the left runner and follows
it to the center at time \(a\), it captures the left
runner at time zero and the right runner at time \(a\).
The mean is exactly \(a/2\). QED.

**Theorem 3 (positive reversing mass in EVERY full-game optimum).**
Let \(q_*=\nu_*\{m:m\text{ is nonreversing}\}\).
Using the branch's certified full-game upper bound
\[
U_{\rm best}=
\frac{57045188913812444387410009}
{40000000000000000000000000}
\simeq1.426129722845311,
\]
the stronger **exact rational support inequality** is
\[
 \boxed{
 1-q_*\ \ge\ \frac32-U_{\rm best}
  =\frac{2954811086187555612589991}
         {40000000000000000000000000}
  \simeq0.07387027715468888.}                        \tag{22}
\]

**Proof.** The fair-reflected \(\mu_\epsilon\) scores
exactly \(3/2-\epsilon/4\) against each fast sweep.
By the monotone dominance lemma, against EVERY
completed nonreversing Monster its expected capture
time is at least \(3/2-\epsilon/4\).
Against every *other* Monster its expected capture
time is at least \((1-\epsilon)/2\), by the new
unrestricted-response lemma above.
Thus, using almost-sure completion of optimal
Monster laws and Tonelli,
\[
 \mathbb E_{\nu_*,\mu_\epsilon}T
 \ge q_*(3/2-\epsilon/4)
        +(1-q_*)(1-\epsilon)/2.
\]
But the globally optimal Monster law guarantees
expected capture at most \(V\le U_{\rm best}\)
against EVERY Princess law. Letting
\(\epsilon\downarrow0\) yields
\(1/2+q_*\le U_{\rm best}\). Rearrange. QED.

In particular every unrestricted optimal Monster law,
whether finitely or diffusely supported, must assign
at least about **7.39% mass to genuinely reversing
trajectories**. This does not prove that infinitely
many reversals occur at equilibrium or that the
estimate is sharp. The mass conclusion combines an
unrestricted **two-trajectory Princess response
certificate** and the branch's independently
established global upper certificate; it does not
improve the original game's numerical bounds.

### Strengthening: genuinely productive reversals BEFORE completion

The word "reversal" must not be interpreted as
a **gratuitous reversal after both endpoints
have already been visited**. Such a tail
cannot affect any first capture and could
make an uninformative support statement
appear stronger than it is. The exact
support theorem admits the following
more meaningful strengthening.

For a completed Monster m write
\[
 \tau_{\rm comp}(m)=
   \max(\tau_-(m),\tau_+(m)).
\]
Call m **precompletion monotone** if its
restriction to \([0,\tau_{\rm comp}(m)]\)
is nondecreasing or nonincreasing.
Otherwise it has at least one
**productive direction reversal
before visiting the second endpoint**.

The fast-sweep dominance lemma applies
to every precompletion-monotone path:
all Princess targets are caught by
\(\tau_{\rm comp}\), so only the prefix
matters. A monotone completed prefix
must start at one endpoint, and the
corresponding fastest sweep weakly
dominates every one of its captures.
The exact two-runner unrestricted
response lemma still applies to
all remaining Monster paths, with
no restriction on their movement.

Repeating the proof of Theorem 3
therefore gives the strictly stronger
whole-game support requirement
\[
 \boxed{
 \nu_*\{m:
   m|_{[0,\tau_{\rm comp}(m)]}
   \text{ is nonmonotone}\}
       \ge3/2-U_{\rm best}
       \simeq0.07387027715468888.}                  \tag{22a}
\]
This holds for EVERY global optimal
Monster law, regardless of its
irrelevant postcompletion continuation.
The condition is Borel because endpoint
first-visit times are Borel and
monotonicity on a random closed prefix
can be checked on rational time pairs.

Further, every Monster path can be
replaced by its **stopped-at-completion**
version
\(m^{\rm stop}(t)=m(\min(t,\tau_{\rm comp}(m)))\),
without changing its first-contact
payoff against any Princess. This
is a Borel payoff-preserving legal
transformation. Therefore the
canonical symmetric optimal law can
be chosen with:
- its monotone component equal to
  the two fastest sweeps, stopped
  after completion;
- its other trajectories stopped
  after completion and genuinely
  nonmonotone BEFORE completion.

The lower 7.39% support restriction
is thus not an artifact of extra
turns appended after capture.

### Exact diagnostic on the archived Princess lower strategy

For context, exact rational physical first contacts with the
two fast endpoint sweeps of the archived 338-path Princess law give
\[
 b_{\rm old}=
 \frac{18145150023847037}{12800000000000000}
 =1.4175898456130498\ldots
\]
against each symmetric sweep. This exceeds the same
law's certified unrestricted lower guarantee
\(L=36290299773897097/25600000000000000\)
by **exactly**
\[
 b_{\rm old}-L
   =\frac{273796977}{25600000000000000}
   =1.06951944140625\times10^{-8}.
\]
Thus the archived near-optimal lower CDF almost
equalizes the *monotone sweeps* already, making
a monotone-only perturbation a poor route to improving
its full-game maximin value. This is a genuine exact
cross-score, not a new game bound.

## 8. Constructive next gate

The missing substantive step is to **construct a competitive
causal record-occupation law \(\alpha^\pm\)**, arising from
legal whole Monster histories \(\nu\), and solve its
Princess pure-path oracle \({\cal U}_\alpha\) at a value
matching a full Monster Bellman lower certificate for a
Princess CDF \(F\).

Priority:
- Solve global free-boundary pressure balance (15) and
  its characteristic/singular matching conditions **jointly**
  with Monster record dynamics.
- Determine whether an attaining continuous field exists
  or a boundary-germ Princess sequence is necessary;
  never infer attainment from compactness alone.
- Test any candidate by **both** unrestricted inequalities
  (7); do not promote a finite-path master or a smooth
  patch equation alone into a game-value claim.

Current full-game bounds, exact optimal Princess CDF,
and exact optimal Monster law remain unchanged/OPEN.
**Independent exact regression:** run

    python packages/interval_global_closure/verify_global_dual_two_sweep.py

The standard-library Fraction verifier checks physical first-contact
times against independently integrated strict/closed causal-selector
price on **429** legal two-leg Princess paths and 29 approaching
\(\epsilon\)-families with reflections; it additionally tests
**259** distinct arbitrary legal Monster prefixes with endpoint-tour
completions against four \(\epsilon\) runner pairs, and tests
14 explicit attaining Monster routes. All local Fraction fixtures
passed. The script also checks the archived 169 weighted reflected
Princess path pairs against both sweeps from their source JSON,
asserting the exact cross fraction above; this latter archived-source
test was independently calculated using exact V8 BigInt arithmetic,
but the native Python script was not run with a mounted full repository
copy in the working container. These finite fixtures audit formulas,
not the unrestricted global theorem or its mass-bound analytic proof.

No Lean compilation or CI in this checkpoint.
