# The bare Eulerian clock relaxation has exact value 1

Date: 2026-11-13. **A decisive obstruction to the proposed Eulerian construction route, not a new game-value bound.**

The conservation laws (12)--(13) in
[GLOBAL_CAUSAL_PRESSURE_MATCHING.md](GLOBAL_CAUSAL_PRESSURE_MATCHING.md)
are necessary for a physical Monster/history clock. They were explicitly
not asserted to be sufficient. This note proves a large, exact failure of
sufficiency: **even when the chronological Monster occupation and flux are
those of an actual symmetric Monster law, the remaining bare Eulerian
constraints admit an attained relaxed value of 1.** The original game has
the previously certified lower bound
`36290299773897097/25600000000000000 > 1.4175898`.

Thus optimizing only these conservation laws and the exact pressure
matching cannot produce a valid unrestricted upper strategy. The missing
pathwise lift is an essential constraint, not a numerical precision issue.
The pressure-matching theorem itself is unchanged: it evaluates the
Princess oracle of a supplied occupation correctly; the fake occupation
below is not the record occupation of the supplied physical Monster law.

## 1. Precisely which relaxation fails

Retain an **actual symmetric complete Monster trajectory law** and its
killed chronological occupation `sigma`, velocity flux `j`, initial law
`mu_0`, and first-arrival law `xi_-` at -1. In particular,

\[
 \partial_t\sigma+\partial_x j
   =\delta_0\otimes\mu_0-\xi_-\otimes\delta_{-1},
 \qquad |j|\le\sigma.
\]

Allow an arbitrary finite nonnegative measure `alpha`, a locally finite
nonnegative measure `beta`, and a locally finite signed flux `k`, subject
to the proposed necessary clock constraints

\[
 \alpha=\sigma+\partial_t\beta+\partial_x k,
 \qquad |k|\le\beta,
 \qquad \alpha\{x=-1\}=0,
 \qquad \alpha(X)=\sigma(X)=M.
 \tag{1}
\]

Also impose all the causal-test inequalities

\[
 \int\phi\,d\alpha\le\int\phi\,d\sigma
 \quad\text{when}\quad \partial_t\phi\ge|\partial_x\phi|.
 \tag{2}
\]

All measures have the same time/space domain as the original note. One
can use smooth compactly supported tests in the distributional formulas;
the construction below has compact support, so there is no condition at
infinite time to check.

The relaxed objective is the exact full radial oracle

\[
 C_{\rm rel}=M+D(\alpha),\qquad
 D(\alpha)=\mu_+(X)-\operatorname{Match}_{\preceq}(\mu_+,\mu_-),
 \tag{3}
\]

with the positive/negative pressure split and the cone order from the
pressure-matching note. This is a relaxation even though the
chronological `sigma,j` still have a genuine physical Monster lift.
The witness below also has finite total backlog mass, interval support,
and all aggregate prefix inequalities. In general physical backlogs
need only be locally finite when the endpoint time has finite mean but
infinite second moment.

## 2. Fix the physical Monster law to the two fastest sweeps

Let the Monster choose each fastest endpoint sweep with probability 1/2.
The sweep from +1 has position `m(t)=1-t` for `0<=t<=2`; its reflection
starts at -1 and is killed at time zero in the one-sided active measure.
Consequently

\[
 \sigma(dt,dx)=\tfrac12\mathbf1_{0<t<2}\,dt\,
                  \delta_{1-t}(dx),\qquad j=-\sigma,
 \qquad M=1.
 \tag{4}
\]

The full initial law is
`mu_0=(delta_{-1}+delta_1)/2`, and the first -1 arrival-time law is
`xi_-=(delta_0+delta_2)/2`. The source and instantaneous sink at `(0,-1)`
cancel, leaving exactly the source `(0,1)/2` and sink `(2,-1)/2` in (4).
Thus the chronological Monster component is physically valid and
symmetric, with zero extra endpoint effort.

Its actual unrestricted Princess response is 3/2; see
[ALL_MONOTONE_SUBGAME_EXACT.md](ALL_MONOTONE_SUBGAME_EXACT.md).
For the lower direction alone, the legal Princess path

\[
 p_\varepsilon(t)=\min(-1+\varepsilon+t,1),\quad0<\varepsilon<1,
\]

has capture times `1-epsilon/2` and `2` against the two sweeps, giving
`3/2-epsilon/4`. This already rules out every asserted physical upper
certificate of value 1 for this Monster law.

## 3. A fake history occupation with exact score 1

For every `0<t<2`, set

\[
 a(t)=
 \begin{cases}
  1-2t,&0<t\le1,\\
  -\tfrac12,&1<t<2.
 \end{cases}
 \tag{5}
\]

Join `(0,a(t))` to the chronological point `(t,1-t)` by the straight
segment

\[
 z_t(s)=a(t)+\frac{s}{t}(1-t-a(t)),\qquad0\le s\le t,
 \qquad v_t=\frac{1-t-a(t)}t.
 \tag{6}
\]

Each segment is a legal path in the physical interval:

* For `0<t<=1`, its speed is exactly `v_t=1`.
* For `1<t<2`, its speed is `v_t=3/(2t)-1`, which lies between
  `-1/4` and `1/2`.
* Both endpoints lie in `[-1,1]`; the intervening segment therefore does
  too. The value `a(1)=-1` occurs at a single integration parameter and
  carries zero measure.

Define

\[
 \begin{split}
 \alpha&=\tfrac12\int_0^2\delta_{(0,a(t))}\,dt,\\
 \beta&=\tfrac12\int_0^2\int_0^t
                         \delta_{(s,z_t(s))}\,ds\,dt,\\
 k&=\tfrac12\int_0^2\int_0^t
                     v_t\,\delta_{(s,z_t(s))}\,ds\,dt.
 \end{split}
 \tag{7}
\]

The measures `alpha,beta` are nonnegative, `|k|<=beta`, and both total
masses are finite (`alpha(X)=beta(X)=1`). For any smooth test `phi`,
the fundamental theorem of calculus on each segment gives

\[
 \begin{split}
 \langle\partial_t\beta+\partial_xk,\phi\rangle
 &=-\tfrac12\int_0^2\int_0^t
   [\phi_t(s,z_t(s))+v_t\phi_x(s,z_t(s))]\,ds\,dt\\
 &=\tfrac12\int_0^2
             [\phi(0,a(t))-\phi(t,1-t)]\,dt\\
 &=\langle\alpha-\sigma,\phi\rangle.
 \end{split}
 \tag{8}
\]

Thus (1) holds, with the correct signs and the time-zero source included.
If `phi_t>=|phi_x|`, then `phi` is nondecreasing along every segment in
(6), so the same construction proves (2) for **every** such test, not
just a finite test list.

The fake active occupation has the explicit form

\[
 \boxed{
 \alpha(dt,dx)=\delta_0(dt)
   \left[\tfrac14\mathbf1_{[-1,1]}(x)\,dx
                         +\tfrac12\delta_{-1/2}(dx)\right].
 }
 \tag{9}
\]

It has mass 1 and **no mass at x=-1**. All its mass is at historical
time zero; this also satisfies every aggregate prefix inequality
`alpha([0,u] x [-1,1]) >= sigma([0,u] x [-1,1])`.

The positive pressure is `du/4` on `0<u<1`, at time zero. The negative
pressure is precisely the same `du/4` plus an extra mass `1/2` at
radius `u=1/2`. Match the continuous positive pressure diagonally to
the continuous negative pressure:

\[
 \pi=\tfrac14\int_0^1
            \delta_{((0,u),(0,u))}\,du.
 \tag{10}
\]

Every pair satisfies the closed cone relation, the plan has mass 1/4,
and it matches **all** positive pressure. Hence

\[
 \boxed{D(\alpha)=0,\qquad C_{\rm rel}=1.}
 \tag{11}
\]

There is no hidden contact convention in this computation. Directly,
for every legal radius path `r`, only its initial value matters, and

\[
 \boxed{
 \int\Phi(r(t),x)\,d\alpha
       =\tfrac12+\tfrac12\mathbf1_{\{r(0)>1/2\}}.
 }
 \tag{12}
\]

The uniform component contributes 1/2 for every initial radius; the
negative atom contributes 1/2 precisely with the displayed strict
inequality. The supremum is exactly 1 and is attained, for example, by
`r(t)=1`. The exact pressure-matching theorem is working correctly.

## 4. The relaxed optimum is exactly 1, and why it is not physical

For any complete physical Monster path, its first and second endpoint
times `sigma_0,tau` satisfy `tau>=sigma_0+2`. Thus
`tau_-+tau_+ >= 2`. For a symmetric Monster law,

\[
 M=\mathbb E\tau_-=
       \tfrac12\mathbb E(\tau_-+\tau_+)\ge1.
\]

Because the unmatched positive pressure `D` is nonnegative, every
instance of the relaxation in Section 1 has objective at least 1.
The feasible construction above attains 1. Therefore

\[
 \boxed{\inf C_{\rm rel}=\min C_{\rm rel}=1.}
 \tag{13}
\]

By contrast, a physical clock on the Monster law (4) can select only
points on the single active worldline

\[
 \{(s,1-s):0\le s<2\}.
\]

At selected time zero it can select **only x=1**. The occupation (9)
puts positive mass at time zero throughout the interval, including
mass 1/2 at x=-1/2. No clock on that Monster law can produce it.
The segments (6) are individually legal, but they are **different
histories from the Monster history being priced**. Equations (1)--(2)
fail to enforce that identity of histories.

The same contradiction can be read from the full physical effort
inequality in the pressure-matching note. The actual chronological
Monster has effort `e=0`, so every physical clock must have deficiency
at least 1/2. Our relaxed object has deficiency zero. Adding that one
inequality excludes this example, but no claim is made that it or any
finite list of moments supplies a complete physical lift.

## 5. A second fake passes the listed global scalar restrictions

The zero-effort witness is excluded by the already proved physical
effort/deficiency inequality. The failure of lifting persists after
adding that inequality and the recorded scalar reversal, start-position,
and completion-delay tests. Here is an explicit second witness, with
`delta=1/4` and relaxed score `5/4`, still strictly below the certified
original-game lower bound. The claim in this section concerns precisely
the inequalities checked below, not every possible physical constraint.

For `0<delta<1`, consider the actual Monster path

\[
 m_\delta(t)=
 \begin{cases}
  1-\delta/2-t,&0\le t\le\delta/4,\\
  1-\delta+t,&\delta/4\le t\le\delta,\\
  1+\delta-t,&\delta\le t\le\delta+2,
 \end{cases}
 \tag{14}
\]

held at -1 thereafter, and its fair reflection. Both paths start strictly
inside the interval and reverse before the first endpoint. The first
endpoint is reached at time `delta`, after which the path immediately
sweeps to the other endpoint. Thus

\[
 M=1+\delta,\qquad e=\delta,\qquad
 \overline\Delta=\delta,\qquad
 \mathbb E|M(0)|=1-\delta/2,
 \qquad\Pr(\text{precompletion reversal})=1.
\]

Let `x_0=1-delta/2`. Each prefix point `(t,+/-m_delta(t))`,
`0<t<delta`, is joined to the fake historical source `(0,+/-x_0)`
by a straight legal segment: the original path itself proves
`|m_delta(t)-x_0|<=t`. For each point on the positive path's terminal
sweep, use the fake historical source

\[
 a_\delta(t)=
 \begin{cases}
  1+\delta-2t,&\delta\le t\le1,\\
  \delta-1,&1<t<\delta+2.
 \end{cases}
\]

The first segment family has speed +1. The second has speed
`(2-t)/t`, of absolute value at most one for `t>=1`. Define `beta,k`
by these bridges exactly as in (7), with the physical path probabilities.
The same fundamental-theorem proof establishes (1)--(2), with `sigma,j`
now those of this actual symmetric reversing Monster law.

The resulting fake occupation is

\[
 \begin{split}
 \alpha_\delta={}&\tfrac\delta2
       [\delta_{(0,x_0)}+\delta_{(0,-x_0)}]\\
 &+\delta_0(dt)\left[
       \tfrac14\mathbf1_{[-(1-\delta),1-\delta]}(x)\,dx
       +\tfrac{1+\delta}{2}\delta_{-(1-\delta)}(dx)\right].
 \end{split}
 \tag{15}
\]

Match the equal-radius continuous positive/negative parts diagonally,
and also match the two equal prefix atoms at radius `x_0`. This matches
all positive pressure, leaving only the extra negative atom. Hence

\[
 \boxed{D(\alpha_\delta)=0,\qquad C_{\rm rel}=1+\delta.}
\]

The exact strict radial score, writing `r=r(0)`, is

\[
 \int\Phi\,d\alpha_\delta
   =\tfrac{1+\delta}{2}
          [1+\mathbf1_{\{r>1-\delta\}}]
      -\tfrac\delta2\mathbf1_{\{r=x_0\}}.
 \tag{16}
\]

Its maximum is `1+delta`, attained at `r=1`.

Now fix **delta=1/4**, so `x_0=7/8`, `M=5/4` and `D=0`.
The following recorded necessary scalar tests all hold:

| Test | Exact check for the fake lifted candidate |
| --- | --- |
| Positive reversal mass, including the canonical interior-start restriction | Both physical paths start at `+/-7/8` and reverse before endpoint completion. The reversal probability is 1. |
| Initial-position budget `E abs(M(0)) >= 2-U` | `7/8 >= 2-U`, using the retained rational upper certificate `U`. |
| Endpoint effort upper budget `e <= U-1` and recorded positive lower budget | `e=1/4 < U-1`; its completion delay `1/4` exceeds `181/20000` and the sharper algebraic delay threshold. |
| Weakened effort/deficiency test `D >= max(0,1/2-sqrt(2e)-3e/2)` | Its right side is zero. |
| Unweakened sweep-stability test `M+D >= 3/2-sqrt(Delta_bar)-Delta_bar/4` | The right side is `15/16 < 5/4`. |
| Every uniform-offset convex envelope `M+D >= L_A(Delta_bar)`, `0<A<1` | Verified for the entire continuous parameter range below. |

For the last row, use the exact `L_A` in
[GLOBAL_SWEEP_STABILITY_ENERGY_BARRIER.md](GLOBAL_SWEEP_STABILITY_ENERGY_BARRIER.md),
equation (14). If `0<A<=1/4`, then `L_A(1/4)=1/2-A/4<5/4`.
If `1/4<=A<1`, then

\[
 \frac54-L_A(1/4)
 =\frac{16A^2-8A+27}{128A}
 =\frac{16(A-1/4)^2+26}{128A}>0.
 \tag{17}
\]

Thus this is an all-parameter check, not sampling the Princess offset
distribution. The second witness passes these stronger existing
constraints, although it still lacks the pathwise clock lift.

Its physically false upper score is exposed even without the archived
lower certificate: the legal runner `p(t)=min(-1+delta+t,1)` has first
capture times `1` and `2+delta` against the two actual Monster paths,
so its expected capture is

\[
 \frac32+\frac\delta2=\frac{13}{8}>\frac54.
\]

The true clock can select historical time zero only at `+/-x_0`, whereas
(15) has an additional continuous initial-position component. Once
again, individually legal backwards bridges have substituted other
histories for the priced Monster histories.

## 6. Necessary coupling constraints omitted by the bare equations

For an actual clock, write its selected-time measure on a Monster path
as `eta_m`, and its nonnegative backlog as

\[
 \kappa_m(t)=\eta_m([0,t])-t,\qquad0\le t<\tau_-(m).
\]

The physical definitions in the original note imply

\[
 \boxed{\beta\ll\sigma.}\tag{18}
\]

Indeed `sigma(A)=0` says that for almost every Monster path, its
chronological occupation of `A` is zero. Multiplying that occupation
by the finite nonnegative pathwise backlog cannot give `beta(A)>0`.
The fake construction violates (18): most of its `beta` lies off the
chronological sweep worldline.

There are also **joint** directional constraints, stronger than the
two separate inequalities `|j|<=sigma` and `|k|<=beta`. If all endpoint
times are bounded by `H`, then `0<=kappa_m(t)<=H-t` before the active
endpoint. Put `R(t)=H-t` on the active domain. Pointwise weighting of
the same path velocity gives the measure inequalities

\[
 \boxed{
 0\le\beta\le R\sigma,\qquad
 |Rj-k|\le R\sigma-\beta.
 }
 \tag{19}
\]

The second follows by integrating
`(R-kappa_m(t))*m'(t)`, whose absolute value is at most
`R-kappa_m(t)`. In particular, wherever all chronological flow has
speed +1, the backlog flux must satisfy `k=beta`; wherever it has
speed -1, it must satisfy `k=-beta`. For (4), genuine clocks satisfy
`k=-beta` everywhere.

Neither (18) nor (19), separately or together, is proved sufficient
here. They specify additional necessary constraints and exclude the
displayed fake; they do not solve the general physical-lifting
problem. Tracking the distribution of the pathwise backlog, together
with the common Monster position and the two endpoint-visit flags,
is a potential exact formulation. Its feasibility and its usefulness
for constructing an equilibrium must be proved before treating it as
a solution method.

## 7. Reproduction and impact on the proof plan

[verify_eulerian_relaxation_gap.py](../../packages/interval_global_closure/verify_eulerian_relaxation_gap.py)
uses only standard-library exact rational arithmetic. It independently
integrates the two transport regions in (7) against polynomial tests,
checks the source/flux signs in (8), evaluates the strict radial
payoff (12), verifies finite atomic analogues of the complete diagonal
matching, and computes actual physical first contacts for the
Princess runner against the two real sweeps.

The continuum proof is the calculation above. The finite regression
is an arithmetic and contact-convention audit, not a replacement for
the analytical proof or a Lean kernel check.

The executed regression passed **45** clock-conservation moments,
**45** chronological source/sink moments, **1,599** legal backward
segments, **1,890** strict radial integrals, **4,416** atomic
threshold/germ checks, and **100** actual two-sweep Princess responses.
For the second reversing-path witness it also passed **45** additional
conservation moments, **1,890** strict radial integrals, **3,160** exact
checks of the continuum-envelope factorization, the displayed scalar
restrictions, and the physical first-contact payoff `13/8`. The
all-parameter envelope result is proved by the polynomial factorization
(17); those finite substitutions audit the arithmetic only.

**Decision for the constructive attack:** the raw Eulerian cone has
now failed a decisive exact test. Its best objective is 1, below the
known full-game lower bound, even with a fixed physically valid
chronological Monster. Do not optimize this cone and interpret the
result as a physical upper strategy. A usable next construction must
retain a pathwise clock lift or establish a stronger sufficient
feasibility theorem. No original-game bound, equilibrium, finite
phase reduction, or completed proof is claimed by this result.
