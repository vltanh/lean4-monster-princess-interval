# A global CDF transport linear program: no finite path bank

Date: 2026-11-12. Status: **exact structural reformulation, not a solution
of the unrestricted game**.

## 1. The replacement for finite trajectory mixing

The current G2 search tried reweighting an archived finite Monster
trajectory bank. Two whole reweighting rays are now excluded above the
best certified upper bound; nothing shows that a fixed finite bank can
contain a true saddle. Conversely, nothing proves that an optimal Monster
law has infinite support. The correct shift is **from frozen trajectories
to an unrestricted CDF field and its coupled Monster record process**.

The relevant existing inputs are GLOBAL_MINIMAX_AND_CDF_DUALITY.md
(global minimax, ordered Princess dominance, and horizon approximation),
GLOBAL_CDF_VARIATIONAL_STATIONARITY.md (exact near-active CDF variation),
and GLOBAL_CDF_BELLMAN.md (unrestricted Monster verification for supplied
endpoint-absorbed fields). The additional result below makes the full
Princess feasible set and the entire finite-horizon game an explicit
**linear** optimization problem, with neither a Princess path basis nor
a Monster turn-count assumption.

## 2. Exact local-speed feasibility of arbitrary time-dependent CDFs

Fix a finite horizon D>0. Let F(t,x), 0<=t<=D and x in R, satisfy:

* For each t, x -> F(t,x) is a right-continuous probability CDF
  supported on [-1,1]. Put F^+(t,x)=F(t,x) and
  F^-(t,x)=lim_{y upward to x}F(t,y).
* For every 0<=s<=t<=D and every real x, writing d=t-s,
  
      F(s,x-d) <= F(t,x) <= F(s,x+d).                (TC)

These are linear inequalities on the entire field, including its atoms.
No differentiability, prescribed absorption time, or parametrization by
a finite path bank is needed.

**Theorem 1 (exact transport-cone representation).**
(TC) is necessary and sufficient for F to be the one-time marginal
CDF of a probability law on all continuous speed-at-most-one Princess
paths [0,D] -> [-1,1]. Moreover F admits the *common-quantile*
realization

    Q(t,r)=inf {x: F(t,x)>=r},     0<r<1,

whose paths are 1-Lipschitz for **every** r in (0,1) and nondecreasing
in r at every t. Symmetry can, without loss for security optimization,
be imposed by the additional linear equations

    F(t,x)=1-F^-(t,-x).                              (SYM)

**Proof.**
For a speed-one law P, the inclusions

    {P(s)<=x-d} subset {P(t)<=x}
                  subset {P(s)<=x+d}

prove (TC). Conversely let Q_s(r) denote its generalized inverse.
By the left inequality in (TC), for every r,

    F(t,Q_s(r)+d)>=F(s,Q_s(r))>=r,

so Q_t(r)<=Q_s(r)+d. By the right inequality, for every epsilon>0,

    F(t,Q_s(r)-d-epsilon)
      <=F(s,Q_s(r)-epsilon)<r.

Hence Q_t(r)>=Q_s(r)-d. Interchanging s,t as appropriate gives
|Q_t(r)-Q_s(r)|<=|t-s| for all r. Each Q(.,r) is a legal continuous
path. Its dependence on r is monotone and measurable, so the
pushforward of uniform Lebesgue rank measure has precisely the CDF F.
Reflection of the Princess law gives (SYM); symmetrization does not
decrease its security payoff, by the concavity of an infimum of linear
payoff functionals. QED.

For regular F, (TC) is equivalently the characteristic inequalities

    F_x+F_t >= 0,      F_x-F_t >= 0.                 (CH)

For an arbitrary atomic/irregular legal F, these remain **necessary
nonnegative-measure inequalities in space-time distributions**, not
a smooth-density assumption. Indeed, differentiating the quantile
representation in distributions gives

    F_x = integral_0^1 delta_(x=Q(t,r)) dr,
    F_t = -integral_0^1 Q_t(t,r) delta_(x=Q(t,r)) dr,

with dt understood in each measure. Since |Q_t|<=1 almost everywhere,
F_x +/- F_t are nonnegative measures. The all-time (TC) formulation
above is used in the exact LP and avoids any converse regularity
subtlety at moving atoms or endpoint traces.

## 3. Reordering is STRICTLY better than raw path mixing

Let mu be any law of continuous Princess paths with marginals F.
For any continuous Monster path m, a Princess path that has not met m
by time t must have stayed strictly on one side of m for the entire
history. Thus

    Pr_mu[T(m,P)>t]
      <= 1 + inf_{s<=t} F^-(s,m(s))
             - sup_{s<=t} F^+(s,m(s)).              (SR)

For the common-quantile realization Q, the two surviving rank sets
are precisely the lower and upper tails, and equality holds in (SR),
up to rank-boundaries of Lebesgue measure zero. This holds
simultaneously against **every** Monster route.

In particular, given two legal fields F_0,F_1 and 0<=lambda<=1,

    C_m((1-lambda)F_0+lambda F_1)
       >= (1-lambda)C_m(F_0)+lambda C_m(F_1),       (CONC)

where C_m is the ordered first-contact expected time. Raw mixing of
the two already-ordered path laws gives only the right-hand
side. Globally reordering their mixed CDF can strictly improve it.

Here is an exact and elementary strict witness. Define, for 0<=t<=2,

    p_1(t)=t-1,    p_2(t)=1-t,

and hold each path at its attained endpoint afterwards. Take
equal Princess weights. For 0<=t<=2 the ordered rank paths are

    q_low(t)=-|1-t|,    q_high(t)=|1-t|,

again held at their endpoints for t>=2. All four paths are legal.
Choose a legal Monster m that remains at x=1/2 until t=2,
then runs left at speed one to x=-1 at t=7/2, and finally
sweeps to +1 at t=11/2 (so m is endpoint-completed).

The exact chronological first captures are

    T(m,p_1)=3/2,   T(m,p_2)=1/2,
    T(m,q_low)=7/2, T(m,q_high)=1/2.

Therefore the **raw half-mixture** has mean capture time 1,
whereas the **ordered law with exactly the same one-time CDFs**
has mean capture time 2. Indeed *every* raw mixture supported on
the fixed two-path bank {p_1,p_2} has mean at most 3/2 against
this m, strictly below the reordered half-mixture's 2.

This does not prove an increase in the unrestricted Princess
maximin value; it proves why the fixed-path mixing objective
is not the correct global Princess design space.

## 4. An exact full-field infinite linear program

Let H>0, D=H+3. Let M_H be the set of all continuous 1-Lipschitz
Monster paths on [0,D] visiting **both** distinct endpoints during
[H,D]. This class permits waits, resets, non-unit speeds,
arbitrarily many reversals, and Zeno accumulation. Its paths
capture every legal Princess by D.

For each m in M_H introduce measurable history variables
a_m(t),b_m(t) in [0,1], 0<=t<=D. The following is one
**infinite-dimensional linear program**, not an optimization over
a finite list of Princess or Monster trajectories:

    maximize c over F, all a_m,b_m, and c

subject to the CDF normalization/monotonicity/right-traces and (TC),
and, simultaneously for every m in M_H and 0<=s<=t<=D,

    a_m(t) <= F^-(s,m(s)),
    b_m(t) >= F^+(s,m(s)),                            (REC)

plus the linear payoff inequalities for every m in M_H,

    c <= integral_0^D [1+a_m(t)-b_m(t)] dt.           (PAY)

Optionally enforce (SYM). Denote its **supremum** by L_H; Princess
attainment is not assumed.

**Theorem 2 (exact LP equivalence and unrestricted limit).**
The LP has precisely the completed-horizon Princess security value:

    L_H = sup_mu inf_{m in M_H} E_mu T(m,P).

For the fully unrestricted game V, the exact certified bound is

    L_H/(1+3/H) <= V <= L_H;                           (LIM)

in particular, V=lim_(H -> infinity) L_H=inf_(H>0)L_H
(the last infimum need not arise from monotonicity).

**Proof.**
For any feasible F, the pointwise record extrema

    A_m(t)=inf_{s<=t}F^-(s,m(s)),
    B_m(t)=sup_{s<=t}F^+(s,m(s))

are measurable: along a fixed continuous m, the strict trace
F^-(s,m(s)) is lower semicontinuous in s and the closed trace
F^+(s,m(s)) is upper semicontinuous, by Fatou applied to the
common-quantile paths. Consequently A_m and B_m are bounded
monotone functions of t. Choosing a_m=A_m, b_m=B_m satisfies
(REC), and (SR) with equality for the ordered quantile law yields

    E T(m,Q) = integral_0^D [1+A_m(t)-B_m(t)]dt.

Conversely any feasible (REC) has a_m<=A_m and b_m>=B_m,
so (PAY) cannot exceed this actual expected first-contact cost.
Theorem 1 identifies exactly all legal Princess marginals, and
ordering is simultaneously optimal for all m with the same
marginals. Therefore the LP supremum equals the claimed security
supremum, without a finite-support restriction.

The universal horizon completion theorem in
GLOBAL_MINIMAX_AND_CDF_DUALITY.md proves that the completed
security value is between V and (1+3/H)V, giving (LIM).
Let H grow. QED.

The LP is **linear**, despite the original running infimum and
supremum, because the causal record obstacles (REC) have been
lifted into independent linear variables. Its index set is
infinite and its exact solution is not supplied. In particular,
this is not a claim that a fixed spatial mesh or a finite route
bank can certify the optimum.

## 5. The coupled global free-boundary problem to attack

An actual solution must identify a field F_*, a constant c, and a
Monster law nu_* on **complete trajectories** (or a limiting
near-optimal Princess sequence) with both unrestricted inequalities:

    C_m(F_*) >= c                      for every legal m,
    E_{m~nu_*} T(m,p) <= c             for every legal p.

A matching pair certifies V=c. The global CDF variational theorem
provides an alternative second check using **all** legal CDF
perturbations, including near-active strict/closed record germs;
a Monster's one-time position CDF is not an adequate dual variable.
Complementarity requires nu_* to concentrate on Monster paths
attaining the first inequality, and active record selectors to
balance the Princess field's speed-cone constraints.

Operationally the variables are now:

1. A **whole CDF F** in the exact transport cone (TC), allowing moving
   atoms and free endpoint arrival times; no fixed 338 paths, knot set,
   or time-two absorption.
2. A **whole Monster record-value/Bellman potential** for each F,
   rather than a turn-template or finite-path response bank.
3. A **dual record-occupation law** on full Monster histories,
   rather than probabilities only on the archived 280 routes.
4. A genuinely coupled free-boundary/KKT verification, not another
   local reweighting or an infinitesimal improvement of the old bound.

An infinite-horizon renewal or Zeno layer may appear naturally in
the complementary Monster support; the existing local Green/Zeno
calculations are then useful as conditional parts of the *global*
Bellman solution, not a substitute for one.

**Concrete G2 closure criterion:** supply a nontrivial explicit
CDF field and companion global Bellman lower certificate at a
common c, plus a trajectory-law upper certificate at c (or
uniform approaching Princess lower laws if the supremum is
unattained). Failure to solve the unrestricted obstacle and
stationarity conditions means G2 remains open.

**Numerical full-game bounds:** unchanged. No optimal CDF, Monster
trajectory law, equality constant, Lean formalization, or CI result
is claimed. This note is an analytic pivot and a strict
two-path counterexample to the sufficiency of raw bank mixing.
