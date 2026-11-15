# Exact finite-state physical-clock lift

Date: 2026-11-13. **The physical Monster/history-clock lift is exactly
representable by a continuity equation on a fixed-dimensional compact
state space.** This closes the sufficiency gap of the bare Eulerian
pressure equations. It does **not** turn the game into a finite LP or a
finite list of algebraic cases: the unknowns below are measures on a
continuous state space, and no degree, support or partition bound is
proved.

The core lift has four state coordinates and four constant control
velocities. Three additional registration coordinates enforce the
center/endpoint visit requirements using three more constant controls.
The latter construction is an ordinary continuity equation in seven
coordinates; it needs no unproved hybrid-boundary gluing rule.

## 1. Inputs and scope

[GLOBAL_EXACT_HORIZON_REDUCTION.md](GLOBAL_EXACT_HORIZON_REDUCTION.md)
proves that some symmetric original-game Monster optimum visits the
center by `H=3` and both endpoints by `D=H+4=7`. Denote this compact
Monster path class by `M_H`. Its guarantee is against **every** legal
Princess, not only outward-completed Princess paths.

The finite-horizon strong record dual in
[GLOBAL_STRONG_RECORD_DUALITY.md](GLOBAL_STRONG_RECORD_DUALITY.md) and
the clock theorem in
[GLOBAL_MONOTONE_CAUSAL_CLOCK.md](GLOBAL_MONOTONE_CAUSAL_CLOCK.md)
therefore apply at the one fixed horizon `D=7`.

We deliberately use **full-horizon clocks** of total mass D. Their
occupation can have mass at `x=-1`, which is inert because
`Phi(r,-1)=0`. We do not impose the active-clock condition
`alpha{x=-1}=0` on the full occupation. This avoids introducing a
first-hitting-time reset into the clock dynamics.

For one base Monster path `m:[0,D] -> [-1,1]`, use two selected-time
measures `eta_-,eta_+`. The minus clock prices m; the plus clock prices
the reflected path -m. Each satisfies

\[
 \eta_\pm\ge0,\quad\eta_\pm([0,D])=D,\quad
 \eta_\pm([0,u])\ge u\quad(0\le u\le D).
 \tag{1}
\]

These conditions are equivalent to a deterministic nondecreasing
backward clock, by the existing generalized-quantile construction.
In particular `eta_+({D})=eta_-({D})=0`: an atom of mass a at D would
contradict the prefix inequality for `u>D-a`.

An arbitrary probability law over such triples `(m,eta_-,eta_+)`,
followed by fair reflection of m, gives a symmetric physical Monster
law and legitimate possibly randomized clocks. Conditional averaging
of clocks on identical Monster paths, followed by the same quantile
construction, recovers a deterministic clock if desired. Conversely,
every symmetric Monster law and its full-horizon lower clock has this
representation: pair the clock on m with the clock on -m.

Its full occupation is

\[
 \bar\alpha=
 \frac12\mathbb E\bigl[(t,m(t))_\#\eta_-
                       +(t,-m(t))_\#\eta_+\bigr],
 \qquad\bar\alpha(X)=D.
 \tag{2}
\]

The exact upper oracle is

\[
 \sup_{r:[0,D]\to[0,1],\ |r'|\le1}
       \int\Phi(r(t),x)\,d\bar\alpha(t,x),
 \quad\Phi(r,x)=\mathbf1_{\{r<x\}}+\mathbf1_{\{r>-x\}}.
 \tag{3}
\]

All strict contacts remain exactly as in the existing dual.

## 2. Four-coordinate graph completion

Define right-continuous backlogs

\[
 q_\pm(t)=\eta_\pm([0,t])-t,
 \qquad0\le q_\pm(t)\le D-t.
 \tag{4}
\]

Use the pre-atom initial convention `q_+(0-)=q_-(0-)=0`.
Atoms at time zero are then upward jumps from zero. At D both queues
are zero. Continuous singular clock measures and countably many atoms
are allowed.

Define graph length

\[
 \lambda(t)=t+\eta_+([0,t])+\eta_-([0,t])
            =3t+q_+(t)+q_-(t).
 \tag{5}
\]

It is strictly increasing between its upward jumps. Complete each
jump by holding physical time and Monster position fixed and filling
the two queue jumps monotonically. The resulting curve has common
graph-parameter interval `0<=lambda<=3D`, with state

\[
 z=(t,x,q_+,q_-)\in
 K_D:=\{0\le t\le D,\ -1\le x\le1,
                  \ 0\le q_+,q_-\le D-t\}.
\]

Its derivatives almost everywhere satisfy

\[
 \boxed{
 t'=\theta,\quad x'=u,\quad
 q_+'=\xi_+-\theta,\quad q_-'=\xi_--\theta,
 \quad\theta,\xi_+,\xi_-\ge0,\quad
 \theta+\xi_++\xi_-=1,\quad |u|\le\theta.
 }
 \tag{6}
\]

Here `theta=dt/dlambda`, while `xi_+,xi_-` are the densities of the
two selected-time charges relative to graph length. All are bounded.
The physical speed bound gives `|x'|<=t'`, including `x'=0` during
vertical clock jumps. This argument uses Radon--Nikodym derivatives
with respect to `dt+deta_++deta_-`, so it includes singular measures.

Equivalently, `z'` lies in the convex hull of just four constant
velocities, in coordinate order `(t,x,q_+,q_-)`:

| Control | Velocity |
| --- | --- |
| Move left | `(1,-1,-1,-1)` |
| Move right | `(1,1,-1,-1)` |
| Charge plus clock | `(0,0,1,0)` |
| Charge minus clock | `(0,0,0,1)` |

The weights are `(theta-u)/2`, `(theta+u)/2`, `xi_+`, `xi_-`.
This is a convex control set, not a claim that optimal Monster
velocities have a finite switching word. Waiting and slower movement
are admitted exactly as convex controls; no approximation is needed.

Every velocity increases `ell(z)=3t+q_++q_-` at unit rate. Thus
`ell(z(lambda))=lambda`. The initial state is `(0,m(0),0,0)` and the
terminal state is `(D,m(D),0,0)`. With D=7, the core graph horizon is
exactly **21**, regardless of how many clock atoms or Monster turns
occur.

### Converse: every admissible extended path gives physical clocks

Take any absolutely continuous curve in `K_D` satisfying (6), starting
with `t=q_+=q_-=0`, and running to graph time `3D`. The invariant
`ell=lambda` and `q_++q_-<=2(D-t)` imply at the terminal time

\[
 3D=3t+q_++q_-\le2D+t\le3D.
\]

Hence `t=D` and both queues are zero. The function t is continuous,
nondecreasing and covers [0,D]. Since `|x'|<=t'`, x is constant on
every interval where t is constant. Therefore it defines one
unambiguous physical path `m(t)=x`, and

\[
 |m(t_2)-m(t_1)|\le t_2-t_1.
\]

Push `xi_+(lambda)dlambda` and `xi_-(lambda)dlambda` forward by t to
obtain `eta_+,eta_-`. Integrating the queue equations gives total
mass D for each. Evaluating at the last graph point with physical
time u gives

\[
 \eta_\pm([0,u])-u=q_\pm\ge0.
\]

Thus (1) holds. Generalized quantiles supply causal backward clocks.
This reconstruction preserves the selected-time measures exactly,
including their atoms and ties. It is not merely an approximation of
the clock or a realization of its first moment.

**Theorem 1.** Full-horizon physical Monster paths with the two causal
clocks are exactly the projections of the admissible four-coordinate
extended paths above, up to irrelevant choices of how simultaneous
clock jumps are filled.

## 3. Exact Eulerian sufficiency for the core lift

Let `L=3D`. Introduce a narrowly continuous probability curve
`rho_lambda` on `K_D` and four nonnegative control flux measures `F_i`
on `[0,L] x K_D`. Require

\[
 \sum_iF_i=d\lambda\,\rho_\lambda(dz),\qquad
 \partial_\lambda\rho+
      \operatorname{div}_z\left(\sum_i v_iF_i\right)=0,
 \tag{7}
\]

with initial probability supported on `{t=q_+=q_-=0}`. The equation
is an equality of distributions on the ambient Euclidean space, with
the initial and terminal traces; it is not an equation tested only
inside the state polytope. This excludes unrecorded boundary sources.

**Theorem 2.** Every flow satisfying (7) has a probability-law lift to
admissible extended paths, and hence to genuine Monster paths and
causal clocks with exactly the prescribed pressure occupation.

**Proof.** Write `a_i=dF_i/d(dlambda rho_lambda)`. These are Borel,
nonnegative, and sum to one almost everywhere. The barycentric field

\[
 b(\lambda,z)=\sum_i a_i(\lambda,z)v_i
\]

is bounded and Borel after arbitrary definition off the occupation
measure. Equation (7) becomes the ordinary nonnegative continuity
equation `partial_lambda rho + div(b rho)=0`.

Apply the standard superposition principle: a narrowly continuous
positive measure solution with an integrable Borel velocity is the
time-marginal family of a measure on absolutely continuous integral
curves. A primary statement is Luigi Ambrosio, *Lecture notes on
transport equation and Cauchy problem for BV vector fields and
applications*, **Theorem 3.4**, [author's lecture notes hosted at
CMU](https://www.math.cmu.edu/cna/LectureNotesFiles/Ambrosiolec.pdf).
The present field is bounded, the interval is finite, and the measures
are probabilities; its integrability hypothesis is therefore automatic.
No BV regularity or uniqueness of b is required for this superposition
step.

The resulting curves stay in `K_D`: their marginals are supported
there at every rational graph time, and continuity plus closedness of
`K_D` give the assertion at all times. They start on the prescribed
initial face and satisfy (6). Apply Theorem 1 curve by curve.

Moreover the selected-time charges are preserved, not just the total
state flux. The four velocity vectors are linearly independent, and
their control weights can be recovered from b:

\[
 \theta=b_t,\quad u=b_x,\quad
 \xi_+=b_{q_+}+b_t,\quad\xi_-=b_{q_-}+b_t.
\]

Integrating these same Borel weights along the superposed curves
reproduces every `F_i`, by their time marginals. Consequently their
pressure projection is exactly the prescribed one. QED.

Conversely any law of admissible extended paths gives (7) by the
chain rule. Thus the core Eulerian representation is both necessary
and sufficient. This differs from the bare `(sigma,j,beta,k)` system:
`rho_lambda` retains the **joint distribution of both backlogs and
the Monster position**, so queue mass cannot be transferred between
different Monster histories merely by balancing its mean.

## 4. Enforcing center and endpoint visits without a first-hit reset

To represent the exact class `M_H`, add three registration variables

\[
 0\le r_-,r_0,r_+\le1.
\]

They start at zero and increase only through three new controls.
Register-minus increases only `r_-`, at unit speed; register-center
only `r_0`; register-plus only `r_+`. Their fluxes have the closed
support guards

\[
 G_-:=\{x=-1\},\quad
 G_0:=\{x=0,\ t\le H\},\quad
 G_+:=\{x=1\}.
 \tag{8}
\]

All three freeze physical time, Monster position and both queues.
The original four velocity vectors are extended by three zeros.
The full state is now the seven-coordinate compact polytope

\[
 Z_D=K_D\times[0,1]^3.
\]

There are **seven constant control velocities**. Their nonnegative
weights sum to one. The linear function

\[
 \ell(z)=3t+q_++q_-+r_-+r_0+r_+
 \tag{9}
\]

increases at unit rate under every control. Run the flow for

\[
 \boxed{\Lambda=3D+3=24\quad\text{when }D=7.}\tag{10}
\]

The initial support is `{t=q_+=q_-=r_-=r_0=r_+=0}`. At graph time
Lambda, the state inequalities give

\[
 \Lambda=\ell(z)\le2D+t+3\le3D+3.
\]

Equality forces `t=D`, both queues zero, and all registrations equal
to one. Thus each registration has accumulated positive mass on its
guard. The projected physical Monster has visited -1 and +1 by D,
and 0 by H.

Conversely, any Monster in `M_H` can register each visit during a
unit graph-length interval at any corresponding hitting time,
holding t, x and the queues fixed. This adds exactly three to graph
length and preserves both clock measures. It works for instantaneous
or tangential physical contacts, visits at physical time zero, and
endpoint visits at D. There is no requirement to register the **first**
visit. Partial registrations interleaved with other controls are also
harmless: the positive registration still proves that the physical
path visited the guard.

Theorem 2 applies without any hybrid extension: use the ordinary
continuity equation in `R^7`, with seven nonnegative fluxes summing
to `dlambda rho_lambda`, the same initial face, and the three support
conditions (8). The seven constant velocities are linearly
independent. Superposition therefore preserves the registration
fluxes as well as both clock fluxes. Positive registration mass on a
closed guard implies an actual physical visit on almost every lifted
path. This proves exact necessity and sufficiency for `M_H`.

The continuous registration variables are proof devices for visiting
three specified sets. They are not a proposed Monster strategy, a
partition of the optimal trajectory, or a restriction on its turns.

## 5. Exact full-game measure program

Let `F_+^charge,F_-^charge` be the two charge flux measures in the
seven-coordinate flow. Their physical pressure projection is

\[
 \boxed{
 \bar\alpha=
   \tfrac12(t,x)_\#F_-^{\rm charge}
       +\tfrac12(t,-x)_\#F_+^{\rm charge}.
 }
 \tag{11}
\]

The registration and movement controls create no pressure directly.
Each charge flux has total D, by the integrated queue equations, so
the full pressure mass is D. All pressure is evaluated at the same
physical `(t,x)` as the Monster history carried by that state.

The exact horizon theorem and finite-horizon record dual now give

\[
 \boxed{
 V=\min_{\text{seven-coordinate feasible flows}}
      \ \sup_{r:[0,D]\to[0,1],\ |r'|\le1}
                      \int\Phi(r(t),x)\,d\bar\alpha.
 }
 \tag{12}
\]

For the upper direction, Theorem 2 reconstructs a symmetric legal
Monster law and causal clocks from every feasible flow, so its
objective is a genuine all-Princess upper bound. For equality, take
the bounded-horizon optimal Monster law supplied by the exact
horizon theorem and an attaining full-horizon record selector;
the graph-completion construction gives a feasible flow with value
V. No Princess attainment is assumed.

To use causal pressure matching, first remove only the inert part:

\[
 \alpha=\bar\alpha|_{\{x>-1\}}.
\]

Now, and only now, `alpha{x=-1}=0`. Apply
[GLOBAL_CAUSAL_PRESSURE_MATCHING.md](GLOBAL_CAUSAL_PRESSURE_MATCHING.md)
to this active pressure. With `M=alpha(X)` and its positive/negative
radius split `mu_+,mu_-`, (12) becomes

\[
 \boxed{
 V=\min_{\text{feasible state flows and partial matches }\pi}
       \left[M+\mu_+(X)-\pi(X\times X)\right],
 }
 \tag{13}
\]

where the matching marginals are dominated by `mu_+,mu_-` and
`pi` is supported on
`(t,u) precedes (s,v) iff v>=u+abs(s-t)`.
This is an **exact linear program over continuous measures**, with
fixed state dimension and finitely many flux types. It is not a
finite-dimensional LP: the measure supports have not been discretized
or proved finite.

For a full-horizon selector, its active mass M need not equal
`E tau_-`: a suboptimal selector might continue pricing older active
positions after the first -1 visit. That equality belongs to the
normalized active-clock representation. Equation (13) needs only
the exact radial oracle for alpha and does not assert it here.

## 6. What has and has not become finite

The following quantities are now fixed for the original unrestricted
game: physical horizon 7; core state dimension 4; core control count
4; visit-enforced state dimension 7; total control count 7; and a
common graph horizon 24. No entire Monster history has to be stored
as a state variable in the exact flow system.

The distribution on that state space is still unknown. There is no
bound here on the number of control switches, support atoms, CDF
pieces, algebraic degrees, or cells needed for an optimal solution.
In particular, Caratheodory's theorem cannot be applied as if the
continuity equation and pressure-matching conditions were finitely
many scalar constraints; they are continuum conditions.

Thus this result repairs a specific fatal feasibility gap and gives
a fixed-dimensional constructive optimization interface. To obtain
the requested finite-case proof, one still needs an equilibrium-
specific finite-complexity theorem or an explicit matching pair of
global certificates. Neither is claimed in this note.

## 7. Verification

`packages/interval_global_closure/verify_finite_state_clock_lift.py`
checks exact rational clock graph completions, generalized-quantile
causality, both pressure projections with strict contacts, the four
and seven velocity identities, compact-state constraints, and
registration of actual center/endpoint contacts. It also checks the
inert endpoint removal on the two-sweep example.

The executed standard-library Fraction regression passed **120**
four-/seven-state clock fixtures, **6,298** compact-state/control
segments, **1,200** independent strict-pressure projection comparisons,
and **40** continuous two-sweep inert-mass/contact-germ checks. Every
fixture checks the causal selected-time quantiles, both total clock
masses, and the exact graph horizons 21 and 24.

These finite fixtures audit the formulas and implementation. The
continuum sufficiency is the analytic superposition proof in Section
3, with its hypotheses explicitly verified. No Lean kernel check,
finite optimal support theorem, or exact numerical V is claimed.
