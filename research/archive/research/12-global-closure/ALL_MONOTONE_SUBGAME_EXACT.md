# Exact closure of the entire nonreversing Monster subgame

Date: 2026-11-13. **Exact infinite-dimensional subgame solved**, with
all continuous monotone Monster paths, arbitrary speeds, waiting,
arbitrary starts, and arbitrary legal Princess paths and mixtures.
This is NOT the unrestricted interval Princess–Monster value.

## 1. Exact upper envelope for every weighted pair of sweeps

Define the two fastest endpoint-to-endpoint Monster sweeps
\[
 m_+(t)=\min(-1+t,1),\qquad
 m_-(t)=\max(1-t,-1).
\]
For \(0\le w\le1\) let \(\nu_w=w\delta_{m_+}+
(1-w)\delta_{m_-}\).

**Theorem 1.** Over ALL legal continuous speed-one Princess paths,
\[
\boxed{
 \sup_{p\in\mathcal A}
 \left[wT(m_+,p)+(1-w)T(m_-,p)\right]
 =1+\max(w,1-w).}                                    \tag{1}
\]
For \(0<w<1\), the supremum is **not attained by any pure or
randomized Princess law**. At \(w=0\) or \(w=1\) it is attained
by the stationary Princess at the selected sweep's destination endpoint.

**Proof.** Both sweeps catch every Princess by time two.
At time one they occupy the same position zero. If
\(p(1)\ge0\), the rightward sweep, which starts below
the Princess and is at zero at time one, has met her by
time one. If \(p(1)\le0\), the leftward sweep has met
her by time one. Thus
\(\min(T_+,T_-)\le1\) and \(\max(T_+,T_-)\le2\).
For any weights, the largest possible weighted sum
subject to these two inequalities is
\(1+\max(w,1-w)\).

If \(w\ge1/2\), choose
\(p_\epsilon(t)=\min(-1+\epsilon+t,1)\) with
\(0<\epsilon<1\). Its exact first contacts are
\((T_+,T_-)=(2,1-\epsilon/2)\), so its weighted
payoff is \(1+w-(1-w)\epsilon/2\), approaching
\(1+w\). If \(w\le1/2\), reflect this path,
giving the approaching value \(2-w\).
This proves (1).

For \(0<w<1\), equality would require
\((T_+,T_-)=(2,1)\) or \((1,2)\) when
\(w\ne1/2\), or the same two possibilities when
\(w=1/2\). But a first hit of either sweep
at time one requires \(p(1)=0\), when both
sweeps are simultaneously at zero, forcing
both capture times to be at most one. Thus
equality is impossible.

At \(w=0\) or \(w=1\), equality would require
the single selected sweep to have capture
time exactly two. The rightward sweep is at
\(+1\) at time two. For every Princess path,
\(m_+(0)=-1\le p(0)\) and \(m_+(2)=+1\ge p(2)\).
If its first contact were exactly at time two,
then necessarily \(p(2)=1\). Speed-one
Lipschitzness gives \(p(t)\ge t-1=m_+(t)\)
for every \(t\le2\). Since \(p(2)=1\) and
\(p(0)\ge-1\), a strict inequality may hold
before time two; for example \(p(t)=1\)
constant gives capture at time two. Therefore
**the supremum IS attained at w=0 or w=1**,
by the Princess stationary at the sweep's
destination endpoint. The nonattainment claim
above applies only to \(0<w<1\). QED.

## 2. All monotone Monster strategies

Let \(\mathcal M_{\rm mono}\) be all continuous
nondecreasing or nonincreasing 1-Lipschitz
Monster paths, including slow movement,
waiting and arbitrary initial positions.
A path not visiting both endpoints has
infinite first-contact payoff against at
least one stationary endpoint Princess.
Consequently any Monster law with finite
worst-case payoff must almost surely
visit both endpoints (by testing the two
stationary endpoint Princess laws).
A nondecreasing completed Monster must
start at -1 and is pointwise dominated
in capture time against every Princess
by \(m_+\); similarly for nonincreasing
completed Monsters and \(m_-\).
The pointwise domination is proved in
GLOBAL_DUAL_RECORD_PRESSURE_HJB.md.

**Theorem 2 (exact all-monotone minimax).**
The unrestricted Princess law versus the
entire monotone Monster class has security
value
\[
 \boxed{
 V_{\rm mono}
 =\sup_\mu\inf_{m\in\mathcal M_{\rm mono}}
  \mathbb E_\mu T(m,P)
 =\min_\nu\sup_{p\in\mathcal A}\mathbb E_\nu T(M,p)
 =\frac32.}                                         \tag{2}
\]
The Monster minimax is attained by the
**fair pair of fastest sweeps**. Every optimal
monotone law has exactly half of its mass
on each orientation, although uniqueness
of the entire path law is not established. The
Princess security supremum is **not
attained**.

**Proof.** For the upper bound, the fair
sweep mixture has global pure-Path
supremum \(3/2\) by Theorem 1.
For the lower bound, use the symmetric
fair-reflected Princess runner pair
\(\mu_\epsilon=(\delta_{p_\epsilon}+
\delta_{-p_\epsilon})/2\). It scores
\(3/2-\epsilon/4\) against EACH fast sweep.
Any completed monotone Monster is
pointwise dominated by the corresponding
fast sweep, so it scores at least that
against \(\mu_\epsilon\). Incomplete
monotone paths may have infinite payoff
against an endpoint Princess but might
capture the runner pair quickly. To
exclude them from the lower proof, add
\(\eta\) mass to each stationary endpoint
Princess, forming
\[
 \mu_{\epsilon,\eta}
 =(1-2\eta)\mu_\epsilon+
 \eta\delta_{p\equiv-1}+
 \eta\delta_{p\equiv+1}.
\]
Any incomplete monotone Monster has
infinite expectation against this law,
whereas every completed monotone
Monster has expected payoff at least
\((1-2\eta)(3/2-\epsilon/4)\).
Let \(\epsilon,\eta\downarrow0\) to
obtain \(V_{\rm mono}\ge3/2\).

For Monster uniqueness, let \(\nu\) be
a finite-cost law on monotone paths.
Almost every path completes both endpoints;
replace each by its dominant fast sweep.
The resulting mixture is \(\nu_w\) with
\(w\) the total nondecreasing mass.
For the original law's worst Princess
payoff we have
\[
 \sup_p\mathbb E_\nu T
 \ge\sup_p\mathbb E_{\nu_w}T
 =1+\max(w,1-w).
\]
To attain \(3/2\) requires \(w=1/2\).
Furthermore, any completed nondecreasing
path \(m\ne m_+\) must lag strictly behind
\(m_+\) at some time. A Princess
trajectory can be chosen so its first
contact with \(m_+\) occurs before
its first contact with \(m\), but this
does not by itself show that the **global
supremum** strictly increases under
positive slow-route mass: the extra
loss may vanish along near-maximizing
Princess contact germs. Therefore
the preceding argument proves the
unique **optimal direction weight**
\(w=1/2\) and existence of a canonical
optimal law, but **does not prove
uniqueness of the full monotone path
distribution**. We make no such claim.

Princess nonattainment: if a Princess
law \(\mu\) achieved security \(3/2\),
its expected payoff against both fast
sweeps would be at least \(3/2\).
Averaging them would give at least
\(3/2\), contradicting Theorem 1's
strict inequality for every pure path,
which persists after integrating any
probability law. QED.

## 3. Exact global dual and support implications

The exact weighted-sweep envelope is
a globally valid causal-selector dual
with no Princess path bank:
\[
 \mathcal U(\nu_w)=1+\max(w,1-w).
\]
It is V-shaped, with unique minimizing
sweep weight \(w=1/2\) and one-sided
derivatives \(-1,+1\). The maximizing
Princess path does not exist for interior
weights, so an active-path-only Danskin
derivative is invalid; the two
approaching runner germs provide the
correct opposing derivatives.

In the original unrestricted game,
the Monster's nonreversing sector may
be canonicalized to fair fast sweeps
by reflection, but the remaining
reversing-history measure must balance
their dual characteristic pressures.
The previously proved whole-game
reversal-mass bound
\(\Pr_{\nu_*}(\mathrm{reversal})\ge
3/2-U_{\rm best}\simeq7.39\%\)
therefore measures a **necessary
deviation from this fully solved
monotone subgame**.

This is a rigorous closure of an
infinite-dimensional subgame, not
the unknown full-game saddle.

## 4. Regression

Run
\`python packages/interval_global_closure/verify_weighted_sweep_envelope.py\`.
The exact Fraction checker verifies the
global inequality on 429 legal quarter-grid
Princess polylines and seven rational
sweep weights, and verifies the approaching
runner germs for 19 epsilon values at
each weight. The global theorems are
analytic, not inferred from the fixtures.

## 4. Stronger global endpoint-start dominance (not just monotonicity)

**Theorem 3 (all endpoint-start Monster routes are dominated).**
For EVERY continuous speed-one Monster trajectory \(m\)
with \(m(0)=-1\), including arbitrarily many reversals,
pauses, and infinite-turn/Zeno behavior, and EVERY legal
Princess path \(p\),
\[
 \boxed{T(m_+,p)\le T(m,p).}                           \tag{3}
\]
Symmetrically, if \(m(0)=+1\), then
\(T(m_-,p)\le T(m,p)\).

**Proof.** If \(m(0)=-1\), speed-one Lipschitzness and the
arena constraint imply
\[
 m(t)\le \min(-1+t,1)=m_+(t)
\]
for EVERY \(t\ge0\), without any monotonicity hypothesis.
For any Princess, initially \(m_+(0)=-1\le p(0)\).
If \(m\) meets \(p\) at finite time \(t\), then
\(m_+(t)\ge m(t)=p(t)\).
Continuity forces \(m_+\) to have met \(p\) by time \(t\).
If \(T(m,p)=\infty\), the inequality is trivial.
The reflection case is identical. QED.

**Corollary (stronger canonical unrestricted optimum).**
There exists a symmetric optimal Monster law
\[
 \boxed{\nu_*=
 (q/2)(\delta_{m_+}+\delta_{m_-})
 +(1-q)\nu_{\mathrm{int,rev}},}                       \tag{4}
\]
where \(\nu_{\mathrm{int,rev}}\) is supported on
**reversing Monster paths with strictly interior
initial positions** \(m(0)\in(-1,1)\).

Start with any symmetric optimal law. Its paths
complete both endpoint visits almost surely, as
proved in GLOBAL_DUAL_RECORD_PRESSURE_HJB.md.
Map every endpoint-start trajectory, regardless of
its reversals, to the corresponding fast sweep.
Map every remaining nonreversing completed trajectory
to its fast sweep as before (necessarily it starts
at an endpoint), and retain only interior-start
reversing trajectories. The map is Borel and
commutes with spatial reflection. Pointwise
dominance guarantees the pushed-forward law is
still globally optimal. Symmetry makes its two
sweep weights equal.

Combining (4) with the previously proved
all-optima reversal-mass bound gives
\[
 \boxed{
 \nu_{\mathrm{int,rev}}\text{ has total mass }
 1-q\ge 3/2-U_{\mathrm{best}}
 \simeq 0.07387027715468888.}                        \tag{5}
\]
In particular, **at least 7.39% of the mass of this
canonical optimal law must lie on interior-start
reversing trajectories**. This excludes *all*
endpoint-start reversing policies from the
unknown portion of the global support; it is a
strictly stronger structural reduction than merely
eliminating slow monotone trajectories.

It does not imply that every optimal Monster law
has this support form; the result is existence
of an optimal canonical representative.

## 5. Exact fixed-start Monster response to the approaching two-runner law

This is a further **unrestricted control result**, not a
finite-turn assumption. Fix \(0<\epsilon<1\), let
\(a=1-\epsilon\), and take the symmetric Princess
law on the two inward runners
\[
 p_L(t)=\min(-a+t,1),\qquad
 p_R(t)=\max(a-t,-1).
\]
The two runners meet at the center at time \(a\).

**Theorem 4 (exact fixed-start response).**
For every fixed Monster initial position \(x\in[-a,a]\),
\[
 \boxed{
 \inf_{\substack{m(0)=x\\|m'|\le1}}
 \frac{T(m,p_L)+T(m,p_R)}2
 =\frac{3a-|x|}{4}.}                                 \tag{6}
\]
For \(|x|>a\), the universal lower bound
\[
 \frac{T(m,p_L)+T(m,p_R)}2
 \ge\frac a2+\frac{(a-|x|)_+}{4}                      \tag{7}
\]
still holds (without an attainment claim).

**Proof.** Before time \(a\), the two runners are
at \(-a+t\) and \(a-t\). If the Monster starts
at \(x\in[-a,a]\), its earliest possible
capture of either runner is at least
\[
 t_{\min}\ge\frac{a-|x|}{2},
\]
by the speed-one separation inequality.
Regardless of its start, it cannot capture
**both** runners strictly before time \(a\):
if it captured them at \(t_1\le t_2<a\),
the distance between the two contact
positions is \(2a-t_1-t_2\), forcing
\(t_2-t_1\ge2a-t_1-t_2\) and \(t_2\ge a\).
Thus the later capture is at least \(a\).
Averaging proves the lower bound (6)
and the global bound (7).

For \(x\ge0\), move right at unit speed
until meeting the right runner at
\[
 t_1=(a-x)/2,\qquad
 m(t_1)=(a+x)/2.
\]
Immediately reverse left at unit speed.
The resulting Monster position is
\(m(t)=a-t\) until time \(a\), when it
meets the left runner at the center.
Both contact times are exactly \(t_1,a\),
so the mean is \((3a-x)/4\).
For \(x\le0\), reflect the construction.
This is a legal one-reversal Monster
response, proving exact attainment.
QED.

**Corollary (a global initial-position moment restriction).**
For the canonical symmetric unrestricted
optimal Monster law from Theorem 3,
\[
 \nu_*=\frac q2(\delta_{m_+}+\delta_{m_-})
       +(1-q)\rho,
\]
where \(\rho\) is supported on interior-start
reversing paths, put
\(r=\int|m(0)|\,\rho(dm)\in[0,1]\).
Then the existing certified full-game
upper bound \(U_{\rm best}\) forces
\[
 \boxed{
 1-q\ge
 \frac{6-4U_{\rm best}}{3+r}
 =\frac{4(3/2-U_{\rm best})}{3+r}.}                   \tag{8}
\]
**Proof.** Score the symmetric runner Princess
law against the canonical optimal Monster
distribution. Each fast sweep has score
\(3/2-\epsilon/4\). Every other path
has score at least (7). As
\(\epsilon\downarrow0\), the latter lower
bound converges uniformly for all
\(|x|\le1\) to \((3-|x|)/4\). Hence
\[
 V\ge\limsup_{\epsilon\downarrow0}
 \mathbb E_{\nu_*,\mu_\epsilon}T
 \ge\frac32q+\frac{1-q}{4}(3-r).
\]
Since \(V\le U_{\rm best}\), rearrange
to obtain (8). QED.

The previous universal bound
\(1-q\ge3/2-U_{\rm best}\simeq7.387\%\)
is recovered from \(r\le1\).
The new inequality is **strictly stronger
when the reversing component starts
away from the endpoints**. For example,
if its mean initial absolute position
were \(r=0\), the lower bound would
be \((4/3)(3/2-U_{\rm best})
\simeq9.849\%\).
No assertion that \(r=0\), or even that
\(r\) is bounded away from 1, is made.
This is a genuine two-parameter
whole-game support constraint, not
a new game-value interval.
