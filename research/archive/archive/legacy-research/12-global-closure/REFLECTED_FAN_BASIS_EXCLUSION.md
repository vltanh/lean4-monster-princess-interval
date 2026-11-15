# Exact rejection of a reflected-fan basis

## Result and scope

Let \(p_1,\ldots,p_{342}\) be the **ordinary collapsed profiles** in the preserved `translation_fan_float349.json.gz.b64` packet. These are fixed new physical paths, with their exact rational vertices supplied by `profile_exact_vertices`; they are not silently substituted for their earlier infinitesimal source paths.

For each profile, choose \(z\) uniformly from \([0,\delta]\), where
\[
\delta=1/1024,
\qquad p_{i,z}(t)=1-\lvert1-p_i(t)-z\rvert.
\]
Give the reflected negative path equal probability, and combine the time marginals with arbitrary nonnegative weights \(w_i\) summing to one. Realize the combined marginals by their common ordered quantiles.

**No choice of these weights can give a matching lower strategy for the full game.** A fixed mixture of 26 legal Monster reflection pairs gives, for every weight vector,
\[
\inf_m \mathbb E T(m,P_w)
\le
\frac{1711141066194169545376440}
     {1208925818523913639952384}
\approx1.415422716576155
<
\frac{36290299773897097}{25600000000000000}.
\]
The last fraction is the repository's already established unrestricted lower bound.

This is a **whole-basis exclusion**, not a new upper bound on the full game. Its scope fixes both the 342 ordinary profiles and the width \(1/1024\). It does not exclude other profiles, other widths, or reflected fan laws in general. No numerical solver accuracy is assumed in the proof.

## 1. Legal paths and their marginals

Each original \(p_i\) stays in \([0,1]\) and is 1-Lipschitz. The folding map \(y\mapsto1-|1-y|\) is 1-Lipschitz; on \(y\in[0,1+\delta]\) its image stays in \([0,1]\). Thus each reflected fan is a legal Princess law.

For \(0\le x\le1\), its radial CDF is
\[
R_i(t,x)=
\left[\frac{x-p_i(t)}{\delta}\right]_0^1+
\left[\frac{x+p_i(t)+\delta-2}{\delta}\right]_0^1,
\]
where brackets mean clipping to \([0,1]\). The two underlying offset intervals are disjoint before \(x=1\). There are no center or endpoint atoms for positive width. Its signed CDF is
\[
F_i(t,x)=\frac12+
\frac{\operatorname{sgn}(x)}2R_i(t,|x|),
\]
with \(F_i(t,0)=1/2\). The mixed signed CDF is \(F_w=\sum_iw_iF_i\).

The usual common-quantile construction is legal because the marginals come from a law of 1-Lipschitz paths. It is this ordered law whose capture cost is being bounded; raw folded trajectories can cross each other.

## 2. Any causal history selectors give an upper plane

Fix a legal Monster route \(m\). For the continuous CDF above, its captured rank band at time \(t\) has endpoints
\[
L(t)=\min_{s\le t}F_w(s,m(s)),\qquad
H(t)=\max_{s\le t}F_w(s,m(s)).
\]
Choose any two times \(\sigma_L(t),\sigma_H(t)\in[0,t]\). They need not attain these extrema. Then
\[
1-H(t)+L(t)
\le 1-F_w(\sigma_H(t),m(\sigma_H(t)))
       +F_w(\sigma_L(t),m(\sigma_L(t))).
\]
Integrating until a completed endpoint sweep gives
\[
C_m(w)\le\sum_iw_i g_{mi}.
\]
The right side is linear in the Princess weights.

The saved selectors are particularly simple. On a right-going leg, retain one past lower-record vertex throughout; use a past upper vertex before a fixed activation time and the current position afterward. On a left-going leg, exchange the roles. Thus, for a right leg of duration \(d\), with activation delay \(a\),
\[
g_{\text{leg},i}
=d(1+F_i(\text{old lower}))
-aF_i(\text{old upper})
-\int_{\text{activation}}^{\text{end}}F_i(t,m(t))\,dt.
\]
For a left leg the expression is
\[
d(1-F_i(\text{old upper}))
+aF_i(\text{old lower})
+\int_{\text{activation}}^{\text{end}}F_i(t,m(t))\,dt.
\]

The construction used numerical record information to choose useful selectors. The verifier checks only the exact conditions required by the inequality: each stored vertex is in the past, and each activation time lies inside its current leg. Incorrect numerical active-set choices would merely produce a weaker valid upper plane.

Each listed Monster route represents a fair reflection pair; the symmetric fan CDF gives the same cost to either orientation. The routes in the certificate are new dyadic physical routes. Their times are reconstructed from the distances between consecutive dyadic positions. The verifier checks every unit leg, the initial time, and both endpoint visits. It does not assume that rounded coordinates retained the geometry of an earlier germ route.

## 3. Exact enclosures without large-denominator accumulation

Set \(S=2^{44}\). Round each exact Princess profile's time and position vertices to the dyadic grid \(S^{-1}\mathbb Z\), coalescing equal rounded times. Call the resulting interpolant \(\widetilde p_i\). The interpolant is used only for integration; the actual strategy remains the exact original \(p_i\).

The verifier checks
\[
\|p_i-\widetilde p_i\|_\infty\le4/S
\]
at **every original and rounded breakpoint**, using exact rational arithmetic. Between consecutive points of that union the difference is affine, and after both final vertices it is constant. These checks therefore prove the uniform enclosure, including all 772 coalesced vertices.

The two clipped CDF terms imply
\[
|F_i(t,x)-\widetilde F_i(t,x)|
\le\frac{\|p_i-\widetilde p_i\|_\infty}{\delta}
\le\frac4{S\delta}.
\]
A history-selector integrand contains two signed CDF evaluations. For a route completed by time \(T\), replacing the profile by its interpolant changes its coefficient by at most
\[
\frac{8T}{S\delta}.
\]
The certificate adds this error with upward integer rounding.

To enclose each interpolant integral, split at its own time vertices and at the Monster's center crossing. Each CDF term is a clipped affine function there. If its endpoint numerators are \(u,v\), the clipping width is \(W\), and the duration is \(d\), its integral uses the exact primitive
\[
\Phi(r)=
\begin{cases}
0,&r\le0,\\
r^2/(2W),&0\le r\le W,\\
r-W/2,&r\ge W.
\end{cases}
\]
For \(u\ne v\) the integral is \(d(\Phi(v)-\Phi(u))/(v-u)\); for equal endpoints it is \(d[u/W]_0^1\). All stored integration values are integer floor/ceiling enclosures at scale \(S\). The final signs are chosen conservatively: subtract lower bounds and add upper bounds. This avoids reliance on floating-point quadrature.

## 4. From the 26 planes to the basis exclusion

The certificate assigns positive integer weights \(q_m\) to its 26 reflection pairs, and normalizes by \(Q=\sum_mq_m\). If \(\overline g_{mi}\) is a verified upper coefficient, then
\[
\begin{aligned}
\inf_m C_m(w)
&\le\sum_m\frac{q_m}{Q}C_m(w)\\
&\le\sum_iw_i\sum_m\frac{q_m}{Q}\overline g_{mi}\\
&\le\max_i\sum_m\frac{q_m}{Q}\overline g_{mi}.
\end{aligned}
\]
The last maximum is exactly the rational bound at the top of this note. The maximum occurs at profile 341. The comparison with the existing game lower bound is an integer cross-multiplication.

A floating simplex solve suggested the 26 planes and their mixture. Its residual gap was about \(7.1\times10^{-6}\); it was not accepted as an optimality certificate. Positive integer weights, causal selectors, exact integration enclosures, and the last displayed inequality are sufficient for the final proof.

## 5. Replay and completed checks

Run from the repository root:
```sh
node packages/interval_global_closure/verify_reflected_fan_basis_exclusion.mjs REPORT.json
```

Files:

- `packages/interval_global_closure/fan_selector_upper_bound.cjs`
- `packages/interval_global_closure/verify_reflected_fan_basis_exclusion.mjs`
- `packages/interval_global_closure/snapshots/reflected_fan_basis_exclusion.json`
- `packages/interval_global_closure/snapshots/reflected_fan_basis_exclusion_checks.json`

The input packet is the previously committed `snapshots/translation_fan_float349.json.gz.b64`. The Node wrapper checks its uncompressed SHA-256 before replaying. The exact core and all input data were replayed in V8 after native execution became unavailable; no native replay, Lean compilation, or CI is claimed.

The completed exact replay checks:

- all 43,921 original profile vertices and their legal speed/domain constraints;
- 87,070 uniform profile-enclosure breakpoint comparisons;
- 269,119 clipped-affine integration cells;
- 8,892 coefficient enclosures, covering all 342 profiles and all 26 planes;
- exact physical-route legality, selector causality, weight normalization, and the final rational exclusion.

The selector proof and every enclosure formula received an independent agent audit. This does not constitute Lean-kernel verification or external peer review.

## 6. What the attacking mixture reveals

The 26-pair mixture is highly exploitable outside this basis. A separate exact unrestricted Princess-response cut gives
\[
\sup_p\mathbb E T(M,p)=
\frac{7483097521803449565333963}{4835703274095654559809536}
\approx1.5474682993660103.
\]
Its minimum and maximum optimal query profiles have legal approaching physical realizations. Their actual weighted capture limits agree with this fraction.

This is why the certificate must not be called a global upper strategy at \(1.4154\): the family restriction is essential. The result directs construction toward new marginal geometry and a global linear-selector response oracle. Continuing to optimize weights within the rejected fixed basis cannot close the game proof.
