# G2 free-boundary attack: exact global radial contact-germ jump and singular-pressure exclusion

Date: 2026-11-12. This works with the
**actual attained unrestricted infinite-horizon active dual**
of GLOBAL_INFINITE_HORIZON_ACTIVE_DUAL.md, and with any finite
nonnegative active occupation measure \(\alpha\) over
\([0,\infty)\times[-1,1]\). No finite Monster path
bank, no smoothness assumption, no finite turn bound,
and no common horizon are used.

**New structural obstruction:** optimal Princess radial
paths with genuinely *unsaturated* interior speed cannot
have positive causal-record occupation on their exact
contact graph. The proof handles SINGULAR occupation
measures and atom-induced order-one jumps, where
ordinary smooth HJB/Euler--Lagrange derivatives fail.

## 1. The exact unrestricted radial functional

For a legal nonnegative 1-Lipschitz radius path
\(r:[0,\infty)\to[0,1]\) put
\[
 J_\alpha(r)=\int
    \Phi(r(t),x)\,\alpha(dt,dx),\qquad
 \Phi(r,x)=
    \mathbf1_{\{r<x\}}+\mathbf1_{\{r>-x\}}.          \tag{1}
\]
At an actual optimal unrestricted Monster/causal-clock dual
\(\alpha=\alpha_*\), Theorem 2 of
GLOBAL_INFINITE_HORIZON_ACTIVE_DUAL.md gives
\[
 \sup_{r\ {\rm legal}}J_{\alpha_*}(r)
 =V,\qquad
 \alpha_*(\mathrm{all})=
 \mathbb E_{\nu_*}\tau_-(M)\le V<\infty.             \tag{2}
\]
The strict comparisons in (1) retain exactly the
physical first-contact convention.

For any fixed legal \(r_0\), any bounded test
function \(\varphi(t)\) for which
\(r_\epsilon=r_0+\epsilon\varphi\) is legal
for all sufficiently small positive \(\epsilon\),
the pointwise strict threshold indicators have
one-sided limits. Finite total \(\alpha\)-mass
makes dominated convergence available,
**even if \(\alpha\) puts atoms or singular
curve mass exactly on a contact surface**.

## 2. Exact order-one contact-germ jump

**Theorem 1 (global strict-contact jump identity).**
Suppose \(r_0+\epsilon\varphi\) is legal for all
\(0<\epsilon<\epsilon_0\). Then
\[
 \boxed{
 \begin{aligned}
 &\lim_{\epsilon\downarrow0}
       J_\alpha(r_0+\epsilon\varphi)
       -J_\alpha(r_0)\\
 &=\alpha\{(t,x):r_0(t)=x,\ \varphi(t)<0\}\\
 &\qquad+
   \alpha\{(t,x):r_0(t)=-x,\ \varphi(t)>0\}
 \ \ge0 .
 \end{aligned}}                                        \tag{3}
\]
All sets in (3) are Borel, and the limit exists.
It is not divided by \(\epsilon\): an arbitrarily
small spatial change can produce an **order-one**
gain when occupation mass lies on a contact curve.

**Proof.** At each \((t,x)\), consider
\(\mathbf1_{\{r_0(t)+\epsilon\varphi(t)<x\}}\).
Away from equality \(r_0(t)=x\), this converges
to the original strict indicator. At equality
it is zero for all \(\epsilon>0\) if
\(\varphi\ge0\), and one if \(\varphi<0\).
The second strict indicator
\(\mathbf1_{\{r_0+\epsilon\varphi>-x\}}\)
has the complementary equality rule:
it gains one precisely when
\(r_0=-x,\ \varphi>0\). Each individual
comparison has a one-sided nonnegative
jump; both indicators are bounded by
one. Integrate their pointwise limits
by bounded dominated convergence
against the **finite nonnegative**
\(\alpha\), proving (3). QED.

This is a precise, global statement about
**one-sided physical contact germs**.
Replacing "<" or ">" by non-strict
comparison would invalidate (3).

## 3. NEW necessary condition: no singular contact pressure on free flow

**Theorem 2 (free-flow contact graph exclusion).**
Let r be a legal radius path attaining
\(J_\alpha(r)=\sup_{r'\ {\rm legal}}J_\alpha(r')\).
Suppose on an open time interval
\(I\subset(0,\infty)\) there exists
\(\eta>0\) such that
\[
 \eta\le r(t)\le1-\eta,\qquad
 |r'(t)|\le1-\eta\quad\text{a.e. }t\in I.             \tag{4}
\]
Then
\[
 \boxed{
  \alpha\{(t,x):t\in I,\ x=r(t)\}=0,\qquad
  \alpha\{(t,x):t\in I,\ x=-r(t)\}=0 .
 }                                                    \tag{5}
\]

**Proof.** Take any nonnegative smooth bump
\(\psi\in C_c^\infty(I)\). The two paths
\(r-\epsilon\psi\) and \(r+\epsilon\psi\)
remain in \([0,1]\) and obey the
1-Lipschitz constraint for small
\(\epsilon>0\), because of the uniform
strict margins (4). Apply Theorem 1
with \(\varphi=-\psi\): at a maximum,
the nonnegative limiting payoff
increase (3) must be zero, so
\(\alpha\{x=r(t),\psi(t)>0\}=0\).
Apply with \(\varphi=+\psi\) to get
\(\alpha\{x=-r(t),\psi(t)>0\}=0\).
A countable sequence of compactly
supported bumps positive on an
exhaustion of I proves (5). QED.

**Quantitative version.** If instead
\(J_\alpha(r)\ge\sup J_\alpha-\epsilon\)
under the same strict free-flow
margins, the identical argument gives
\[
 \boxed{
 \alpha\{t\in I,x=r(t)\}\le\epsilon,\quad
 \alpha\{t\in I,x=-r(t)\}\le\epsilon,
 \quad\alpha\{t\in I,|x|=r(t)\}\le2\epsilon.
 }                                                    \tag{6}
\]
The interval I may be unbounded:
apply the bump argument to compact
subintervals and exhaust I by
monotone convergence.

This necessary condition applies
to the **actual global optimal
active record measure** whenever
a maximizing pure radius exists
and has a free-flow interval.
If the Princess supremum is not
attained, apply (6) to any
near-maximizing radius with
a uniform free-flow strip.
Do not infer that such an optimizer
or strip exists without proof.

When \(\alpha\) also admits a smooth
density h, the regular first
variation on a zero-contact free
strip is
\[
 \partial_r g(t,r)=h(t,-r)-h(t,r),
\]
so ordinary unsaturated optimality
imposes \(h(t,-r)=h(t,r)\).
The singular exclusion (5) is
logically prior to that smooth
Euler--Lagrange condition; it
protects against losing entire
contact masses in a formal PDE
differentiation.

## 4. Explicit active-dual regression: the two endpoint sweeps

For the symmetric fair two-sweep
Monster law, the exact globally
optimal lower-record clock
concentrates its one unit of
active mass on the leftward sweep:
\[
 \alpha_{\mathrm{sw}}
  =\tfrac12\mathbf1_{0\le t\le2}
       dt\,\delta_{x=1-t}.
\]
Take the legal saturated-radius
path \(r_0(t)=|1-t|\) on \([0,2]\),
extended by constant 1. At EVERY
nonzero time in (0,2) its radius
lies on the dual contact threshold
\(|x|=|1-t|\). The exact score is
\[
 \boxed{J_{\alpha_{\mathrm{sw}}}(r_0)=1/2.}         \tag{7}
\]

For \(0<\epsilon<1\) choose the
legal physical runner radius
\[
 r_\epsilon(t)
   =|\min(-1+\epsilon+t,1)|.
\]
For fixed \(0\le t<1\),
\(r_\epsilon(t)\to r_0(t)\) from BELOW;
for fixed \(1\le t<2\), it
approaches from ABOVE. The exact
right and left threshold germ
limits therefore win both
characteristic strips:
\[
 \boxed{
 J_{\alpha_{\mathrm{sw}}}(r_\epsilon)
       =3/2-\epsilon/4,\qquad
 \lim_{\epsilon\downarrow0}J(r_\epsilon)-J(r_0)=1.
 }                                                    \tag{8}
\]
The saturated speed of r0 is
crucial: Theorem 2 does not
rule out such characteristic
contact occupation; the
one-sided supremum is
**unattained** here.

An independent Fraction physical
threshold engine tests (8) for
34 rational epsilons in
\`packages/interval_global_closure/verify_global_monotone_clock.py\`.
The jump is a full unit, not an
infinitesimal derivative.

## 5. Generalized physical germ constraints on the global unknown

For any legal family \(r_\epsilon\)
converging pointwise to \(r_0\),
the global dual upper bound
\(V=\sup_rJ_{\alpha_*}(r)\)
imposes
\[
 \boxed{
 \int \bigl[\lim_{\epsilon\downarrow0}
          \Phi(r_\epsilon(t),x)\bigr]
       \alpha_*(dt,dx)\le V
 }                                                    \tag{9}
\]
whenever the pointwise limit of
the two strict indicators exists;
bounded convergence justifies it.
This is an **exact continuum
near-contact germ cut**, not a
finite sampled Princess path column.

For the above runner family its
limit is explicit. Put
\(R(t)=|1-t|\) for \(t<2\) and
\(R(t)=1\) afterwards. Then
\[
\Phi_{\rm runner}(t,x)=
\begin{cases}
 \mathbf1_{\{R(t)\le x\}}
 +\mathbf1_{\{R(t)>-x\}},&0\le t<1,\\
 \mathbf1_{\{R(t)<x\}}
 +\mathbf1_{\{R(t)\ge-x\}},&1\le t<2,\\
 \mathbf1_{\{1<x\}}
 +\mathbf1_{\{1>-x\}},&t\ge2 .
\end{cases}                                           \tag{10}
\]
This differs at the exact
characteristic thresholds from
the value of \(\Phi(R(t),x)\).
For a canonical optimal decomposition
\(\alpha_*=(q/2)dt\,\delta_{x=1-t}
                      +\alpha_{\rm rev}\),
the global inequality (9) yields
\[
 \boxed{
  \int\Phi_{\rm runner}(t,x)\,
                 \alpha_{\rm rev}(dt,dx)
       \le V-\tfrac32 q .
 }                                                    \tag{11}
\]
This is a rigorous **whole-continuum
transmission inequality** on the
unknown reversing-history pressure.
It is compatible with the existing
unrestricted two-runner lower response
and its \(q\le V-1/2\) consequence,
but it carries the complete
strict-sided spacetime information
rather than only that scalar mass
bound.

**Remaining constructive gate:** solve
the coupled free/saturated/characteristic
occupation equations for a legal
\((\nu_*,s_m)\) and an optimal
(or approaching) Princess CDF.
The current note neither determines
q nor improves the existing full-game
numerical interval. No Lean compilation
or CI.
