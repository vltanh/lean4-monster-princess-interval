# G2: Exact monotone causal-clock compression and bounded active occupation

Date: 2026-11-12. This continues
[GLOBAL_STRONG_RECORD_DUALITY.md](GLOBAL_STRONG_RECORD_DUALITY.md).

**New global result:** the attained two-kernel causal-record dual can
be written with only ONE pathwise nondecreasing backward clock. The
clock is an exact deterministic realization of every admissible
causal selector measure, not a finite-trajectory approximation.
The symmetric Princess upper oracle is then an unrestricted
one-radius path problem with a nonnegative **active occupation
measure of total mass at most the game's completed-horizon value**,
uniformly bounded as the horizon tends to infinity.

Neither player's exact optimal strategy, nor the original game
value, is identified here.

## 1. Replace all causal selector kernels by a time-marginal order

Let \(D\ge2\), \({\cal M}_D\) and \(\Gamma_D\) be as in
GLOBAL_STRONG_RECORD_DUALITY.md, with a symmetric
Monster law \(\nu\). Take a lower-record causal measure
\(\gamma^-(dm,dt,ds)=\nu(dm)\,dt\,\kappa_{m,t}(ds)\)
supported on \(0\le s\le t\le D\).

Disintegrate its \((m,s)\) marginal as
\[
 (\pi_{m,s})_\#\gamma^-(dm,ds)
   =\nu(dm)\,\eta_m(ds),                              \tag{1}
\]
where for \(\nu\)-almost every \(m\), \(\eta_m\)
is a finite positive Borel measure on \([0,D]\)
of total mass \(D\). The selector cost depends
on \(\gamma^-\) **only through** (1), since
\(F^-(s,m(s))\) and the Princess pure-path
strict comparison do not involve the later
scoring time \(t\).

**Theorem 1 (exact causal prefix characterization).**
A measurable conditional family \(\eta_m\)
is induced by a causal history-selector law
with \(t\)-marginal \(dt\) **if and only if**
\[
\boxed{
 \eta_m([0,u])\ge u\quad
 \text{for all }u\in[0,D],
 \quad\eta_m([0,D])=D,
 \qquad\nu\text{-a.e. }m.}                           \tag{2}
\]

**Proof.** Necessity: all scoring times
\(0\le t\le u\) must select past times
\(s\le t\le u\). Their total mass is u,
so the selected-time marginal gives
\(\eta_m([0,u])\ge u\).

Sufficiency: put \(G_m(u)=\eta_m([0,u])/D\)
and define the generalized quantile time warp
\[
 \boxed{
  s_m(t)=\inf\{u\in[0,D]:G_m(u)\ge t/D\}.
 }                                                     \tag{3}
\]
The map \(t\mapsto s_m(t)\) is nondecreasing,
and (2) gives \(s_m(t)\le t\) for
Lebesgue-almost every t. The quantile
pushforward of \(dt\) under \(s_m\) is
exactly \(\eta_m\). Conditional measure
disintegration and countable-rational
approximations to the quantile in (3)
make \((m,t)\mapsto s_m(t)\) jointly
measurable (up to standard null
completions). Therefore
\[
 \kappa_{m,t}=\delta_{s_m(t)}
\]
is a legitimate **deterministic** causal
selector with precisely the same
\((m,s)\) marginal as the starting
arbitrary randomized kernel.
Every causal selector payoff is unchanged.
QED.

This result is a first-order stochastic
dominance/quantile-coupling theorem applied
to history time. **The nondecreasing
clock is without loss of generality**:
it is not a conjectured property of a
special optimal Monster response.

For the upper-record selector, a symmetric
dual optimizer from GLOBAL_STRONG_RECORD_DUALITY.md
can be chosen with
\(\gamma^+=R_\#\gamma^-\), where R
reflects the entire Monster trajectory,
not the selected time. Thus the upper
selector needs no independent time clock.

## 2. One-clock exact global minimax

Define the strict-threshold radial score
for \(0\le r\le1\), \(-1\le x\le1\):
\[
 \Phi(r,x)=
 \begin{cases}
 1+\mathbf1_{\{r<x\}},&x>0,\\
 \mathbf1_{\{r>0\}},&x=0,\\
 \mathbf1_{\{r>-x\}},&x<0 .
 \end{cases}                                           \tag{4}
\]
It is exactly the symmetric upper
selector integrand, including boundary
contacts and atoms.

Let \(\mathfrak C_D\) denote the pairs
\((\nu,s)\) consisting of a symmetric
Borel probability law \(\nu\) on all
completed Monster paths \({\cal M}_D\)
and a jointly measurable backward clock
\(s_m(t)\) which, for \(\nu\)-a.e m,
is nondecreasing in t, lies in
\([0,D]\), and satisfies \(s_m(t)\le t\)
for almost all t.

**Theorem 2 (attained global one-clock dual).**
\[
\boxed{
 W_D=
 \min_{(\nu,s)\in\mathfrak C_D}
 \sup_{\substack{r:[0,D]\to[0,1]\\
                 r\ 1\text{-Lipschitz}}}
  \int_{{\cal M}_D}\int_0^D
   \Phi\bigl(r(s_m(t)),m(s_m(t))\bigr)
   \,dt\,\nu(dm).
 }                                                    \tag{5}
\]
The outer minimum EXISTS. A minimizing
Monster law can additionally be chosen
in the canonical support class
\[
 \nu=\frac q2(\delta_{m_+}+\delta_{m_-})
        +(1-q)\nu_{\rm rev},
\]
with \(\nu_{\rm rev}\) symmetric and
supported on reversing paths; fast
endpoint sweeps are sufficient for
its nonreversing component.

**Proof.** By the attained strong
duality theorem, a symmetric optimal
pair \(\gamma^\pm\) exists.
Reflecting the upper selector gives
\(\gamma^+=R_\#\gamma^-\).
Apply Theorem 1 pathwise to the
conditional selected-time marginal
of \(\gamma^-\). The resulting
nondecreasing \(s_m(t)\le t\) has
identical \((m,s)\) occupation and
therefore gives EXACTLY the same
linear Princess functional for
**every** signed Princess path.
Its symmetric dual upper bound
depends only on the absolute-value
radius by the strict identity (4).
Hence the right-hand side of (5)
equals \(W_D\).

Conversely each \((\nu,s)\in\mathfrak
C_D\) defines \(\gamma^-\) by pushing
\(\nu(dm)dt\) through
\((m,t)\mapsto(m,t,s_m(t))\), and
\(\gamma^+=R_\#\gamma^-\) has the
same \((m,t)\) marginal because \(\nu\)
is symmetric. It belongs to the
original compact causal-dual class,
so its radial oracle is at least
\(W_D\). Attainment and the
canonical-monotone-support corollary
are inherited from the stronger
compact-measure minimax theorem.
QED.

**Interpretation:** a whole Monster
trajectory carries one nondecreasing
causal record clock. At each physical
scoring time t it can price a past
position \(m(s_m(t))\). The Princess
then chooses ONE globally legal
radial trajectory. Randomizing
a finite set of routes, optimizing
a fixed turn word, or forcing the
Princess onto a finite path bank is
not part of (5).

## 3. Universal active-mass and simple dual-pressure constraints

For a candidate \((\nu,s)\), define
the single lower-record occupation
measure on spacetime
\[
 \alpha(A)=\int\!\!\int_0^D
   \mathbf1_{\{(s_m(t),m(s_m(t)))\in A\}}
         \,dt\,\nu(dm).
                                                               \tag{6}
\]
Its total mass is D. The causal
condition immediately forces a
time-prefix dominance constraint:
\[
 \boxed{\alpha([0,u]\times[-1,1])\ge u
 \quad(0\le u\le D).}                               \tag{7}
\]
This is necessary but NOT sufficient:
the entire pathwise causal lift is
still mandatory.

Observe the exact values at the
two constant Princess radii:
\[
 \Phi(1,x)=\mathbf1_{\{x>-1\}},\qquad
 \Phi(0,x)=2\mathbf1_{\{x>0\}}.                      \tag{8}
\]
Because the oracle is the supremum
over every legal radius, if its
certified value is at most c then
\[
 \boxed{
 \alpha(\{x>-1\})\le c,\qquad
 2\alpha(\{x>0\})\le c.}                            \tag{9}
\]

In particular for the **optimal**
one-clock dual (5),
\[
 \boxed{
 \beta_D:=\alpha|_{\{x>-1\}},\quad
 \beta_D([0,D]\times[-1,1])
 \le W_D\le 2,\quad
 \beta_D(\{x>0\})\le W_D/2.}                        \tag{10}
\]
The endpoint at \(x=-1\) is
**inert**: \(\Phi(r,-1)=0\) for
every legal r. All its mass
\(D-\beta_D(\mathrm{all})\) can
be omitted from evaluating the
Princess oracle. Thus
\[
 W_D=\sup_r\int\Phi(r(s),x)\,\beta_D(ds,dx)
\]
for a minimizing candidate.
Although the full causal measure
has mass D, **all payoff-relevant
occupation has mass at most W_D**.
By the monotone horizon theorem,
\[
 \lim_{D\to\infty}W_D=V,\qquad
 \limsup_{D\to\infty}\beta_D(\mathrm{all})
             \le V\le U_{\rm best}.
\]
The bounded-mass statement holds
without a finite horizon-independent
Monster turn cutoff.

This is a genuine **uniform
measure-mass reduction**, not yet
a proof of compactness of
the \(\beta_D\) over the unbounded
time axis: a bounded total mass
may escape to arbitrarily late s.
An infinite-horizon attaining
active occupation law is NOT
asserted.

### Pathwise endpoint absorption of inactive selector mass

Once a Monster has first visited
\(-1\) at time \(\tau_-(m)\),
choosing \(s=\tau_-(m)\)
thereafter gives
\(F^-(s,m(s))=0\) for
EVERY legal Princess CDF F.
It is therefore universally
no worse than any other
lower-record selector for all
later scoring times.
For any fixed completed
Monster law, this replacement
preserves the upper-certificate
direction and only decreases
its objective against every
Princess field. Hence there
is always an optimal selector
for that law which places
all lower-record mass after
\(\tau_-(m)\) at the inert
endpoint \(x=-1\).
The active measure is then
generated entirely by physical
scoring times \(t<\tau_-(m)\);
its total mass is at most
\(\mathbb E_\nu\tau_-(M)\).
In an optimal Monster law
\(\mathbb E_\nu\tau_-(M)\le W_D\),
because the stationary
Princess at -1 has first
contact time \(\tau_-\)
and is among the pure
Princess challenges.

This provides an independent
pathwise explanation for
the uniform active-mass
estimate (10), including
Monster trajectories with
infinite precompletion
turn sequences.

## 4. Consequences for constructing the equilibrium

The new global unknowns are exactly:

1. The distribution \(\nu\) of
   physically legal complete Monster
   trajectories, with its monotone
   sector normalized to two fast
   endpoint sweeps and its reversing
   sector unrestricted.
2. One nondecreasing causal
   record clock \(s_m(t)\le t\)
   along each trajectory, or
   equivalently a conditional
   selected-time measure \(\eta_m\)
   satisfying the linear prefix
   inequality (2).
3. A **single nonnegative active
   occupation measure \(\beta_D\)**
   of total mass at most about
   the game value, coupled to
   the Monster history law; no
   independent upper pressure is
   needed after reflection.
4. A global radius HJB/path
   certificate for the strict
   reward (4), matched to a
   transport-legal Princess
   CDF and a Monster Bellman
   lower certificate.

An attractive constructive
approach is to solve the
limiting free-boundary matching
of this **bounded active measure**
to the Princess's optimal
radial trajectories, rather
than to fit hundreds of
frozen Monster paths or
enumerate turn counts.

A fixed nonnegative spatial
measure \(\beta\) with total
mass at most two is *not*
enough to prove a Monster
upper bound: the pathwise
causal and endpoint-completion
constraints are essential.
Neither the exact value
nor the missing coupled
free-boundary law is
identified by this result.

## 5. Verification and scope

This note follows analytically
from the exact strong duality
and the quantile coupling
of time measures. The
strict-threshold identities
of (4) were checked in
441 rational atomic/contact
fixtures in
\`packages/interval_global_closure/verify_global_strong_record_duality.py\`.

**Unresolved:** construction
of the minimizing clock/history
law, the Princess CDF, the
global common saddle, and the
unrestricted numerical game value.
No Lean compilation or CI.
