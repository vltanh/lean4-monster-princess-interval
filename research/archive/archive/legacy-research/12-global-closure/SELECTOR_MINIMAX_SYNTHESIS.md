# Exact selector game for a finite completed Monster bank

## Main statement

Fix a finite bank B of completed unit-speed Monster routes, all contained
in a common horizon H. Routes may be treated as fair reflection pairs;
then Princess laws may be symmetrized without changing their payoffs.
The statements below use symmetric legal Princess marginals and their
common ordered-quantile realization.

For each route, allow all causal **past-vertex** lower/upper record
selectors and one cut time in each unit leg. Let S be their finite union
of compact cut boxes, with the route index and vertex choices discrete.
Write L_s(F) for the corresponding linear selector plane.

Then

\[
 \boxed{
 \sup_{F\ {\rm legal}}\min_{m\in B}C_m(F)
 =
 \inf_{\nu\in{\cal P}(S)}
       \sup_{p\ {\rm legal\ radial}}
          \int_S L_s(F_{\pm p})\,d\nu(s).
 }
\]

The infimum over selector distributions is attained, although its
minimizer need not have finite support. Restricting that infimum to
finite selector mixtures does not change its value. On the Princess
side, actual finite mixtures of legal radial pairs approximate the
left-hand supremum arbitrarily closely after common-quantile ordering.

These are supremum/approximation statements for physical Princess laws.
An attained physical Princess optimizer, a finite-support selector
optimizer, or a saddle for the full infinite Monster family is not
claimed.

The proof does not assume a finite Princess basis, endpoint-by-two motion,
a prescribed incoming wave, absence of atoms, or a finite Princess turn
count. The compiler's global path oracle is precisely the best-response
oracle required for a finite selector mixture.

## 1. Why ordered marginals give the correct primal

For any legal target law, a path surviving against a Monster must remain
strictly below it for the entire elapsed history or strictly above it for
the entire history. Thus its survival probability is at most

\[
 1+\inf_{s\le t}F^-(s,m(s))
   -\sup_{s\le t}F^+(s,m(s)).
\]

The common ordered-quantile law realizes this bound exactly. Its two
survivor events are the lower and upper rank tails. The strict lower and
closed upper CDF traces retain initial, center and endpoint contacts.

Legal marginal transport implies that the common quantile paths are
1-Lipschitz. Therefore this ordering is an admissible Princess law and
simultaneously maximizes survival against every Monster with those
marginals. For a reflection-paired bank, symmetrization and then ordering
lose nothing.

Consequently the primal in the displayed formula is an exact optimization
over legal Princess laws for this finite bank, expressed through marginals.
It is not the raw finite-path capture matrix. A raw mixture and its
ordered realization can have different costs.

For each route,

\[
 C_m(F)=\int_0^{T_m}
 \left[1+\min_{s\le t}F^-(s,m(s))
          -\max_{s\le t}F^+(s,m(s))\right]dt .
\]

Completion at both physical endpoints makes the terminal records 0 and 1
for every legal law; there is no omitted later survival term.

## 2. Exact causal selector representation, including atoms

Along a right-moving unit leg, both strict and closed CDF traces are
nondecreasing. Along a left-moving unit leg, both are nonincreasing.
This follows pathwise from the speed bound and remains true at atoms and
characteristic coincidences.

It follows that every old lower or upper record is attained at an earlier
route vertex, using its appropriate strict or closed trace. No continuous
past-time selector is needed.

On a right leg [a,b], choose earlier vertices l,h and a cut c in [a,b].
The plane contribution is

\[
 (b-a)[1+F^-(l)]
 -(c-a)F^+(h)
 -\int_c^b F^+(t,m(t))\,dt .
\]

On a left leg it is

\[
 (b-a)[1-F^+(h)]
 +(c-a)F^-(l)
 +\int_c^b F^-(t,m(t))\,dt .
\]

Every such expression is a majorant of the actual record cost, because
each chosen quantity is an available operand of the corresponding
minimum or maximum.

Choose l,h to be the actual old records. Monotonicity of the current
trace then gives a threshold cut where the current CDF replaces the old
record. A jump through the threshold causes no difficulty: the cut point
itself has zero time measure, while its capture effect is retained in
the old vertex traces for later legs. A plateau at equality admits any
cut in that plateau.

Hence, exactly,

\[
 C_m(F)=\min_{\sigma\in S_m}L_{m,\sigma}(F),\qquad
 \min_{m\in B}C_m(F)=\min_{s\in S}L_s(F).
\]

The cut minimum is attained because the plane is continuous in each cut.
Arbitrary other causal past points also yield valid majorants, but the
vertex subclass already gives equality. The compactness proof below
uses this exact subclass: moving an arbitrary past evaluation time
would not have the same uniform continuity at contacts.

## 3. Uniform continuity is in selectors, not in Princess paths

For fixed route and vertex choices, changing one right-leg cut from c to
c' changes its plane by

\[
 \int_c^{c'}[F^+(t,m(t))-F^+(h)]\,dt.
\]

The corresponding left-leg difference is the integral of
F^-(l)-F^-(t,m(t)). In either case its absolute value is at most |c-c'|.
Therefore, uniformly over every legal target law,

\[
 |L_\sigma(F)-L_{\sigma'}(F)|
 \le \sum_j|c_j-c'_j|
\]

within a fixed discrete selector component. Also 0<=L_s(F)<=2H.

For a pure radial path p, define its selector payoff profile

\[
 f_p:S\longrightarrow[0,2H],\qquad f_p(s)=L_s(F_{\pm p}).
\]

Every f_p is continuous on S, and these profiles are uniformly bounded
and equicontinuous. This remains true when p has initial atoms, endpoint
waits, center waits, or characteristic unit segments.

By contrast, point contact rewards are generally only lower
semicontinuous in the maximizing Princess path. One must not invoke a
maximizing-player weak-compactness theorem that requires upper
semicontinuity there. The next section avoids that error.

## 4. Compact payoff-profile closure and minimax

Let

\[
 K=\overline{\operatorname{co}\{f_p:p\ {\rm legal\ radial}\}}
 ^{\|\cdot\|_\infty}\subset C(S).
\]

Uniform boundedness and equicontinuity make K compact; it is convex by
construction. A finite convex combination of profiles is the actual
linear selector profile of the corresponding finite mixture of radial
pairs.

Every legal symmetric marginal profile belongs to K. For example,
represent its ordered law by radial quantiles, integrate their pure
profiles, and approximate this bounded equicontinuous family uniformly
by finite mixtures. One can first approximate the expectations at a
finite selector net and then use the common Lipschitz estimate to extend
the approximation to all selectors.

Conversely every finite convex combination is an actual legal marginal.
The function

\[
 f\longmapsto\min_{s\in S}f(s)
\]

is 1-Lipschitz in the uniform norm. Thus the primal value is

\[
 \max_{f\in K}\min_{\nu\in{\cal P}(S)}\int_S f\,d\nu .
\]

The probability measures on the compact selector space are weakly
compact. The pairing is jointly continuous for the uniform topology on
K and the weak topology on measures: changing f costs at most its
uniform norm difference, and a fixed continuous f integrates
continuously. The continuous compact convex minimax theorem applies:

\[
 \max_{f\in K}\min_\nu\int f\,d\nu
 =
 \min_\nu\max_{f\in K}\int f\,d\nu
 =
 \min_\nu\sup_p\int f_p\,d\nu .
\]

This proves the stated equality, with selector-side attainment.
The compact maximizing object is a payoff-profile closure, not a claim
that its maximizing profile is realized by one physical Princess law.

Finite selector mixtures are sufficient for arbitrary approximation.
Quantize each cut box while retaining its discrete vertex choices. The
uniform cut Lipschitz estimate bounds the approximation error
simultaneously for every p. Rational weights may then be used when an
ordinary rational input packet is desired.

Adding other valid causal selector planes does not change the value:
weak duality still bounds every such mixed plane from below by the
primal, while the exact vertex-selector subclass already attains the
same infimum.

## 5. Relation to an actual Monster mixture

A selector distribution nu has a marginal distribution w over the
finite route bank. Since each selector plane majorizes its route cost,

\[
 \sum_{m\in B}w_m C_m(F)
 \le \int_S L_s(F)\,d\nu(s)
\]

for every legal marginal F. Thus the globally optimized plane reward is
a valid response upper certificate for that actual Monster mixture.

The selector auxiliary variables are a way to certify and synthesize
the marginal optimization. They are not additional physical Monster
controls.

Conversely, a finite mixture of actual oracle-generated Princess paths
has a legal marginal CDF. Its common-quantile ordered realization is
the candidate to score. Its guarantee

\[
 \min_{m\in B}C_m(F)
\]

is a guarantee against the stated bank only. An all-Monster lower
certificate or separator is still required before calling it a full
game lower strategy.

## 6. A genuine candidate-synthesis exchange

Maintain finite actual Princess paths P_n and finite vertex selectors S_n.
Use the matrix entries

\[
 A_{p,s}=L_s(F_{\pm p})
\]

and solve the finite zero-sum game. Let mu_n,nu_n be its equilibrium
mixtures and v_n its value. Form the actual marginal F_n of mu_n and
score its ordered realization.

The two global separations are:

1. **Selector separation.** For every route in the bank, extract its
   actual strict/closed old records and threshold cuts under F_n. This
   produces a tight selector and the exact value
   \[
   L_n=\min_{m\in B}C_m(F_n)\le v_n.
   \]

2. **Princess separation.** Apply the global selector-plane oracle to
   the finite mixture nu_n. It gives the exact supremum
   \[
   U_n=\sup_p L_{\nu_n}(F_{\pm p})\ge v_n.
   \]
   Use its ordinary physical realization with a stated error tolerance
   to add a real legal path, not a formal label column.

Always recompute matrix entries for the actual realized path with the
physical strict/closed scorer. The label supremum is the upper
certificate; it is not silently substituted for a path's attained score.

These provide

\[
 L_n\le V_B\le U_n.
\]

When their difference is small, F_n is an actual legal candidate with the
corresponding bank guarantee. The procedure searches new marginal shapes
globally and has no fixed Princess basis restriction.

## 7. Finite termination for any positive bank tolerance

This exchange has a rigorous finite-accuracy stopping property, despite
possible nonattainment by an exact physical maximizer.

Fix epsilon>0, and realize every Princess oracle response to error at
most epsilon/4. If U_n-L_n>epsilon, then either

\[
 U_n-v_n>\epsilon/2
 \quad\hbox{or}\quad
 v_n-L_n>\epsilon/2 .
\]

In the first case the realized new path scores more than v_n+epsilon/4
against nu_n, whereas every old path scores at most v_n. Its profile is
therefore at uniform distance greater than epsilon/4 from every old
path profile. Only finitely many such insertions are possible because
the pure-profile family is totally bounded in C(S).

In the second case the tight new selector scores below
v_n-epsilon/2 against mu_n, whereas every old selector scores at least
v_n. In the pseudometric

\[
 d(s,s')=\sup_p|L_s(F_{\pm p})-L_{s'}(F_{\pm p})|,
\]

it is farther than epsilon/2 from every old selector. The selector space
is totally bounded in this metric by its finite component structure and
the uniform cut Lipschitz estimate. Only finitely many such insertions
are possible.

Every nonterminating iteration would make at least one of these separated
insertions. This contradiction proves finite epsilon termination for the
fixed bank when the finite master and both separators are solved as
specified. The argument is independent of tie choices and allows adding
both response types at each iteration.

This is a finite-bank approximation result. It is not a proof that a
fixed finite bank contains a full-game optimal Monster law, nor that an
exact zero-tolerance exchange terminates.

## 8. Atomic and implementation safeguards

The proof retains the following distinctions.

- Lower records use strict CDF values; upper records use closed values.
  Endpoint, center and time-zero atoms are not averaged away.
- The causal past-vertex restriction is exact for unit routes.
- Current-ray integrals are evaluated with their specified trace, even
  when a Princess travels along a characteristic.
- The oracle's two-sided labels describe a supremum. Its explicit
  continuous rational bridges produce actual paths within a certified
  score error.
- Cancelled off-contact point or ray coefficients can still encode an
  adverse exact contact. Their geometry must remain in the realization
  grid.
- The ordered marginal candidate is scored by running records, not by
  averaging raw capture costs of its generating paths.

The current global compiler and independent audit satisfy these local
interfaces. Its arbitrary-sign query/fill theorem supplies the exact
finite-selector Princess supremum used in Section 6.

## Dependencies and verification scope

- Global selector compiler audited source:
  8a6926549004f5739b207e41ddd9167f6784584f.
- Independent physical realization/compilation proof:
  SELECTOR_REALIZATION_AUDIT.md, blob
  76d2f058ed62f0ec7b12bcb517d229b4774e64a7.
- Independent end-to-end verifier, with callable prefix-DP and native
  CLI entry:
  d6275602572ab3feca3c3d122af3029555f44345.
- Its unchanged exact report:
  e5b82482065fcd1172d22d24facebf78fcc6f5e0.

Forty independent tight-selector comparisons already equal chronological
pair first capture exactly in that report. Those fixtures support the
physical interfaces; the uniform-profile minimax and finite-tolerance
termination claims are the analytic arguments above, not conclusions
drawn from sampled games.
