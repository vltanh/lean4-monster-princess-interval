# Global Princess CDF first variation and an exact coupled saddle test

Date: 2026-11-12.

**Theorem:** For the actual ordered-quantile Princess game against
an arbitrary law of Monster trajectories that all complete capture
by a fixed horizon \(D\), the exact right directional derivative in
every legal CDF direction is an integral of **near-active strict
minimum and closed maximum records**. There is no finite-turn cap,
unique-record assumption, atomlessness, or differentiability
assumption. Together with a global Monster response lower bound it
gives a necessary-and-sufficient equilibrium certificate for a
specified completed Monster law and Princess field.

This is a complete **variational formulation**, not an explicit
solution of its inequalities and not a new numerical game bound.

## 1. Convex admissible fields and exact ordered capture cost

Let \(\mathfrak F\) be the class of time-dependent signed spatial
marginal CDFs of arbitrary legal Princess distributions on
\([-1,1]\). This class is convex, including atoms, because path-law
mixtures preserve legal speed-one marginal transport. Let
\(F^\uparrow\) denote the **common quantile coupling** of the
marginals. It is a legal Princess law, and against every legal
Monster route \(m\) its capture cost is
\[
C_m(F)=\int_0^D
       [1+a_F(m,t)-b_F(m,t)]\,dt,                       \tag{1}
\]
where
\[
a_F(m,t)=\inf_{0\le s\le t}F^-(s,m(s)),\qquad
b_F(m,t)=\sup_{0\le s\le t}F^+(s,m(s)).
\]
Here \(F^-\) is the strict CDF and \(F^+\) the closed CDF.
The horizon \(D\) is such that \(m\) has visited both endpoints
by \(D\), so survival vanishes thereafter for every legal Princess
path. This includes the compact completed class
\(\mathcal M_H\) from GLOBAL_MINIMAX_AND_CDF_DUALITY.md
with \(D=H+3\).

For \(F,G\in\mathfrak F\), define
\(F_\lambda=(1-\lambda)F+\lambda G\), \(0\le\lambda\le1\).
Both strict and closed CDF values interpolate linearly.
For each \(m,t\), a running infimum of affine functions is concave
in \(\lambda\), and the negative running supremum is concave.
Therefore
\[
C_m(F_\lambda)\text{ is concave in }\lambda,\qquad
\mathcal C_\nu(F):=\int C_m(F)\,d\nu(m)
\text{ is concave in }F                              \tag{2}
\]
for every Monster path law \(\nu\) completing by \(D\).

## 2. No-regularity Danskin formula for a running record

For fixed \(m,t,F,G\), write
\[
 f_s^-=F^-(s,m(s)),\quad g_s^-=G^-(s,m(s))-f_s^-,
 \quad a=\inf_{s\le t} f_s^-,
\]
\[
 f_s^+=F^+(s,m(s)),\quad g_s^+=G^+(s,m(s))-f_s^+,
 \quad b=\sup_{s\le t} f_s^+.
\]
All \(f_s^\pm\in[0,1]\) and \(g_s^\pm\in[-1,1]\).
No extrema need be attained, and no first-contact continuity is assumed.

Define the two **near-record selectors**
\[
\begin{split}
 \mathcal D^-(F;G-F;m,t)
 &=\lim_{\eta\downarrow0}
    \inf_{\substack{0\le s\le t\\ f_s^-\le a+\eta}}
          g_s^-,\\
 \mathcal D^+(F;G-F;m,t)
 &=\lim_{\eta\downarrow0}
    \sup_{\substack{0\le s\le t\\ f_s^+\ge b-\eta}}
          g_s^+ .
\end{split}                                            \tag{3}
\]
The admissible sets are nonempty for every \(\eta>0\),
and the limits exist because the sets shrink monotonically.
When unique strict/closed records are genuinely attained with
a separation gap, (3) reduces to evaluating \(G-F\) at those
active history points; ties select respectively the **minimum**
and **maximum** directional perturbations. For genuinely
unattained records the near-active formulation is indispensable.

**Lemma (bounded-family envelope).** For arbitrary bounded functions
\(f,g\) on any nonempty index set \(S\), with \(a=\inf_S f\),
\[
 \frac{d}{d\lambda^+}\biggr|_{\lambda=0}
      \inf_{s\in S}(f(s)+\lambda g(s))
 =
 \lim_{\eta\downarrow0}
       \inf_{\{s:f(s)\le a+\eta\}}g(s).                 \tag{4}
\]
For a supremum, replace both infima by suprema and reverse the
near-record comparison.

**Proof.** Let \(|g|\le K\) and denote the right side \(d\).
For each \(\lambda>0\), choose a point with
\(f\le a+\lambda^2\) and \(g\le d+\lambda\);
this is possible because the near-record infimum is at most \(d\).
It shows the upper right difference quotient is at most
\(d+2\lambda\).

For the reverse bound, take a \(\lambda^2\)-minimizer of
\(f+\lambda g\). Since some point has \(f\le a+\lambda^2\)
and \(g\le K\), its \(f\)-value is at most
\(a+2K\lambda+2\lambda^2\), while its difference
quotient is bounded below by \(g-\lambda\).
That near-active \(g\) is at least the infimum in (3) with
\(\eta=2K\lambda+2\lambda^2\), which tends to \(d\).
Thus the lower quotient tends to at least \(d\).
Apply the result to \(-f,-g\) for the supremum case.
\(\square\)

## 3. Exact full trajectory/CDF directional derivative

**Theorem 1 (global CDF first variation).** For every legal
completed Monster route \(m\), any legal CDFs \(F,G\), and
the fixed completing horizon \(D\),
\[
\boxed{
 D^+ C_m(F;G-F)
 =\int_0^D
 [\mathcal D^-(F;G-F;m,t)-
  \mathcal D^+(F;G-F;m,t)]\,dt.}                        \tag{5}
\]
For every probability law \(\nu\) supported on completed
routes with a common horizon \(D\),
\[
\boxed{
 D^+\mathcal C_\nu(F;G-F)
 =\int_{\mathcal M}\int_0^D
 [\mathcal D^--\mathcal D^+]\,dt\,d\nu(m).}           \tag{6}
\]

**Proof.** Apply Lemma (4) separately to the running minimum
of strict CDF forms and running maximum of closed CDF forms.
For every \(\lambda>0\), each record changes by no more than
\(\lambda\), because \(|g_s^\pm|\le1\). Thus the payoff's
difference quotient is bounded in absolute value by \(2D\).
Pointwise right derivatives exist by Lemma (4); dominated
convergence exchanges the derivative with the time integral
and, again, with the Monster mixture. Measurability of the
limiting integrand follows as a pointwise limit of the
measurable difference quotients. The argument remains valid
for countably many turn times, terminal Zeno accumulation,
and characteristic point contacts. \(\square\)

The directional derivative uses **true active history
records**. A fixed selector that was not tight at \(F\)
does not give (5); and replacing its strict CDF by the
closed CDF changes the answer at atoms.

## 4. An exact saddle certificate with no Princess basis restriction

**Theorem 2 (global complementary variational inequality).**
Fix a legal Monster distribution \(\nu\) supported on
paths completing by a common \(D\), a legal ordered Princess
CDF \(F\), and \(c=\mathcal C_\nu(F)\).
Suppose:

1. (**Monster lower verification**) For every legal Monster
   path \(m\), without any time or turn restriction,
   \[
     C_m(F)\ge c.                                     \tag{7}
   \]
2. (**Princess global CDF stationarity**) For every admissible
   Princess CDF \(G\in\mathfrak F\),
   \[
     \boxed{D^+\mathcal C_\nu(F;G-F)\le0.}              \tag{8}
   \]

Then the original unrestricted game has **exact value \(c\)**;
the ordered law of \(F\) and the Monster law \(\nu\)
are an attained saddle pair.

Conversely, any attained ordered/symmetric Princess saddle
and any completed Monster saddle must satisfy (7)-(8)
with \(c\) equal to their common value.

**Proof.** Concavity (2) implies for every \(G\)
\[
\mathcal C_\nu(G)-\mathcal C_\nu(F)
\le D^+\mathcal C_\nu(F;G-F)\le0.
\]
Thus \(F\) maximizes the payoff against \(\nu\) over
**all legal marginal CDFs**, not just a finite path family.
For any arbitrary original Princess law, its common-quantile
reordering dominates it against each Monster path. Hence
its expected capture under \(\nu\) is at most
\(\mathcal C_\nu(G)\le c\). This proves the unrestricted
Monster upper guarantee. Hypothesis (7) supplies the
unrestricted Princess lower guarantee. Both meet at
\(\mathcal C_\nu(F)=c\).

For necessity, at an attained saddle \(F\) maximizes
the concave functional \(\mathcal C_\nu\); all feasible
one-sided derivatives are nonpositive, and (7) holds
by the other saddle inequality. \(\square\)

The complementary **quantile support** form is described
in GLOBAL_MINIMAX_AND_CDF_DUALITY.md: under an attained
Princess optimum, \(\nu\)-almost every Monster trajectory
has cost \(c\) against \(F\), and almost every Princess
quantile path has cost \(c\) against \(\nu\).

### Approximate certificate

If (7) is relaxed to \(C_m(F)\ge c-\epsilon_M\)
and (8) to \(D^+\mathcal C_\nu(F;G-F)\le\epsilon_P\)
for all legal \(m,G\), the same concavity argument gives
\[
\boxed{
c-\epsilon_M\le V\le c+\epsilon_P.}                   \tag{9}
\]
The \(\epsilon_P\) bound needs **all legal CDF directions**
and cannot be estimated solely from a sampled Princess basis.

## 5. From this formula to a solvable candidate

The exact forward equation to attack is (8), not a list of
finite Monster turn templates. It is a variational inequality
with two active-record fields (strict lower, closed upper).
On a polygonal Monster path and piecewise-affine legal CDF,
the old vertex/leg selector oracle is a computable
supergradient separator. Its global signed-label routine can
test a sufficient upper certificate after one chooses
support trajectories and tight selectors.

For continuous Monster support, (6) identifies the correct
limiting **record-occupation measure**: each Monster trajectory
and elapsed time carries (possibly multiple) near-active
historical contact locations. The Princess CDF's transport
constraints and this measure must satisfy the variational
inequality simultaneously.

No finite-support assertion is required, and no optimal
Monster time-marginal CDF is substituted for its full
trajectory/record measure. The next gate G2 is to find a
nontrivial explicit pair satisfying (7)-(8), perhaps first in
a restricted analytic density family and then against the
unrestricted oracles.

## 6. Verification and limitations

The pure-Fraction
\`packages/interval_global_closure/verify_cdf_record_variation.py\`
checks the bounded-family envelope formula on exhaustive finite
rational examples with both tied and untied records, and checks
near-record behavior on a family whose infimum is not attained.
The universal lemma and integral interchange are the above
mathematical arguments, not consequences of these fixtures.

**Full-game numerical bounds remain unchanged.**
No value \(c\), explicit equilibrium CDF, optimal Monster
path distribution, Lean proof or CI completion is claimed.


## 7. Exact nonstationarity witness for the archived 338-path/280-pair candidate

This global variational test is not merely formal. Take the existing
archived ordered symmetric 338-path Princess marginal \(F_0\) and
the certified 280-reflection-pair Monster law \(\nu_0\) in
\`packages/interval_uniform_reduction/princess_strategy.json\`
and \`packages/interval_global_closure/upper_dyadic_exact.json\`.
The independently exact chronological cross-score from
\`paired_strategy_regret.json\` is
\[
 J_0=\mathcal C_{\nu_0}(F_0)
 =\frac{74616624991393892648392565953}
        {52428800000000000000000000000}.
\]
The saved exact 158-vertex legal Princess response \(p_{\rm resp}\),
from \`upper_dyadic_princess_response.json\`, has actual score
\[
 P_{\rm resp}=
 \frac{25577132582444953823400565374247721487193868293686855005813644646669}
 {17934576386819087896673684066307618331721014751397308006400000000000}.
\]
Because \(\nu_0\) is spatially reflection-symmetric, its payoff
against \(p_{\rm resp}\) equals the payoff against the fair
reflection-pair law of \(p_{\rm resp}\). Let \(G_{\rm resp}\)
be the legal signed time-marginal CDF of that pair. Reordering
its quantiles cannot decrease the payoff against any Monster
route, so
\[
 \mathcal C_{\nu_0}(G_{\rm resp})\ge P_{\rm resp}.
\]
By concavity along the **actual legal full-CDF direction**
\(G_{\rm resp}-F_0\), and the derivative theorem,
\[
\boxed{
D^+\mathcal C_{\nu_0}(F_0;G_{\rm resp}-F_0)
 \ge P_{\rm resp}-J_0
 \approx 0.0029361293227555024>0.}                 \tag{17}
\]
The exact positive defect is
\[
\frac{12856014555795398907425695656626138444357081196696780105608081781108993821}
     {4378558688188253881023848649000883381767825867040358400000000000000000000000}.
\]
In particular, the archived field **strictly fails the
global Princess stationarity condition** for that Monster law.
For every \(0<\lambda\le1\), the re-ordered mixed marginal
\(F_\lambda=(1-\lambda)F_0+\lambda G_{\rm resp}\)
has payoff against this **fixed** Monster law at least
\(J_0+\lambda(P_{\rm resp}-J_0)\).

The same archived pair has Monster deviation gain
\(J_0-L\approx0.0056093417063262557\), by its existing exact
unrestricted response certificate. Thus it violates **both**
saddle inequalities. Neither unilateral improvement is a new
full-game value bound, and mixing the Princess CDF toward
\(G_{\rm resp}\) may introduce other Monster attacks.

To reproduce (17) from the exact saved source certificates, run
\`python packages/interval_global_closure/verify_archived_variational_witness.py\`.
This is the first concrete full-CDF directional separation
recorded under the new exact first-variation theorem; it does
not supply a replacement equilibrium.
