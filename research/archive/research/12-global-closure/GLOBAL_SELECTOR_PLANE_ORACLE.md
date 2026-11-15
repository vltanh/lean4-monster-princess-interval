# A global oracle for causal-history selector planes

## Statement and scope

A completed unit-speed Monster route and causal history selectors give an affine upper bound on its cost against an ordered symmetric Princess law. The upper bound is a finite sum of a constant, signed CDF point evaluations, and signed CDF integrals on unit rays. A negative coefficient always multiplies a **closed** CDF and a positive coefficient a **strict** CDF.

For any finite positive mixture of these planes, `selector_plane_oracle.cjs` computes the **global supremum over every legal symmetric Princess marginal**, not merely over a supplied basis. It also constructs ordinary rational, legal, fairly reflected Princess paths whose plane scores approach that supremum with an explicit error. No claim of a matching game strategy is made.

The implementation accepts either completed unit routes with causal selectors or the resulting point/ray terms. The latter interface verifies the contact signs and physical domains; causality of independently supplied terms is the caller's separate obligation. The route interface verifies unit geometry, endpoint completion, and each selector's use of a past vertex.

## 1. Causal upper planes and contact conventions

Let \(F_{\le}\) and \(F_<\) be the closed and strict signed marginal CDFs. On a right-going Monster leg \([a,b]\), choose a past lower-record point \(L\), a past upper-record point \(H\), and an activation time \(\tau\in[a,b]\). The plane contribution is
\[
 (b-a)(1+F_<(L))-(\tau-a)F_{\le}(H)
   -\int_\tau^b F_{\le}(t,m(t))\,dt.
\]
On a left-going leg it is
\[
 (b-a)(1-F_{\le}(H))+(\tau-a)F_<(L)
   +\int_\tau^b F_<(t,m(t))\,dt.
\]
A running maximum dominates every selected past upper value and a running minimum is no larger than every selected past lower value. These formulas therefore upper-bound the ordered capture cost even when the selected records or activation times are not the true ones.

The signs are essential. At a contact, a contribution
\(-aF_{\le}+bF_<\), \(a,b\ge0\), is no larger than either adjacent noncontact value. This also holds at the physical endpoints. At a center query a radial path at zero has \(F_{\le}=1,F_<=0\); a positive radial path has both CDFs \(1/2\). Avoidance increases the score by \((a+b)/2\). The code never applies a sign-of-zero convention to an actual center atom when physically scoring a path.

Consequently the supremum can be approached by paths strictly inside the arena, with strictly subunit speed and no retained point contacts. One proof contracts any radial path toward radius \(1/2\), chooses a generic contraction parameter to avoid the finitely many point equalities, and applies the adverse-contact inequalities and bounded Fatou to the finitely many ray integrals. This is a supremum reduction, not a claim of payoff continuity at literal contacts.

A symmetric signed Princess path can first be folded to its absolute value: fair reflection of \(p\) and of \(|p|\) has exactly the same one-time marginal. The affine functional is linear in the path law, so its global supremum reduces to one deterministic nonnegative radial path with fair reflection.

## 2. Unary light-coordinate rewards

Write \(U=t+p(t)\), \(V=t-p(t)\). A strict radial path has a continuous nondecreasing inverse graph \(U=P(V)\) in the cone
\[
 \max(V,0)\le P(V)\le V+2.
\]
Extend it virtually from \((V,U)=(-1,0)\) and trim the negative-time prefix after realization.

At a noncontact query \((t,x)\), put
\(u=t+|x|\), \(v=t-|x|\), and \(A=\mathbf1\{P(v)>u\}\).
Then
\[
 F(t,x)=
 \begin{cases}1-A/2,&x\ge0,\\ A/2,&x<0.\end{cases}
\]
At \(x=0\) this is used only after the proved avoidance reduction. The returned physical path is checked at every retained point.

Thus a point coefficient \(c\) contributes a constant \(c\) when \(x\ge0\), plus the unary coefficient \(-\operatorname{sign}(x)c/2\).
Split each Monster unit ray at its center crossing. A radial outward part has fixed \(V\) and contributes a horizontal ramp in \(P(V)\); a radial inward part has fixed \(U\) and contributes a vertical threshold integral. The unary coefficient is \(-\operatorname{sign}(x)c/4\), because \(dt=dU/2\) or \(dV/2\).

All objective terms are unary. Exact contacts are evaluated separately by the physical scorer.

**Cancelled terms retain their geometry.** For example, \(-F_{\le}+F_<\) is zero off a contact but negative at a contact. The compiler may cancel its objective coefficients, but keeps its query and ray thresholds so the realization cannot create that omitted adverse contact.

## 3. Finite arrangement for arbitrary signed rewards

Let \(H\) be the largest priced time. Seed the \(V\) grid with all point/horizontal-query coordinates and vertical-ray endpoints; seed the \(U\) grid with point/vertical thresholds and horizontal-ray endpoints. Include \(V=-1,0,H\), \(U=0\), and close the bounded ranges
\[
 V\in[-1,H],\qquad U\in[0,H+2]
\]
under the cone boundaries and their inverses:
\(U=\max(V,0)\), \(U=V+2\), \(V=U\), \(V=U-2\).
Only finitely many bounded translates by multiples of two are introduced.

There is no priced threshold inside either boundary-swept band of an open \(V\) cell \((v_i,v_{i+1})\). Use alternating variables
\[
 q_i\le c_i\le q_{i+1},
\]
where \(q_i=P(v_i)\) and \(c_i\) represents the cell's threshold pattern. The clipped constant fill
\[
 P(V)=\min(V+2,\max(V,0,c_i))
\]
preserves that pattern throughout the open cell. For fixed endpoint query values, the integral of an arbitrary signed step reward is no larger than the cell length times its best admissible pattern. Choosing the corresponding \(c_i\) attains that bound in the limiting fill. This is an arbitrary-sign fill argument; the old positive-reward minimal-fill theorem is not assumed.

Horizontal query rewards are continuous piecewise affine ramps. Within each threshold chamber the remaining problem is a linear objective on an order polytope. Push an entire equal-level block, rather than individual constrained variables, to a chamber/boundary endpoint. Consequently only the two sides \(u_j-\), \(u_j+\) of each common threshold are needed. The virtual first row has the special exact label zero.

Physical query bounds are the interior sides
\[
 q_i\in[\max(v_i,0)+,(v_i+2)-].
\]
A fill row has bounds
\[
 c_i\in[\max(v_i,0)+,(v_{i+1}+2)-].
\]
Every adjacent row is ordered. The resulting finite exact signed-label problem is solved by the retained maximum-closure backend. Its returned minimum and maximum label witnesses are independently rescored. A prefix-maximum dynamic program gives an independent \(O(\text{rows}\times\text{labels})\) solution because this particular unary model has one total row chain. Conjunction rewards in a future extension would require a separate argument.

## 4. Actual rational approximation

Replace every selected side label by \(u_j\pm\delta\). Choose
\[
 0<\delta<\min(1/4,\mathrm{gridgap}/4),\qquad \eta=\delta^2.
\]
On each \(V\) cell, join the left query value linearly to the clipped fill at \(v_i+\eta\), follow the clipped constant fill until \(v_{i+1}-\eta\), then join linearly to the right query value. The fill scalar lies between the two query scalars. The physical cone is convex, so these bridges stay legal and nondecreasing. Their widths do not overlap.

Convert every light vertex by \(t=(U+V)/2\), \(p=(U-V)/2\), trim at the exact time-zero crossing, and compress collinear vertices. The final light row covers all priced physical times, after which constant continuation is legal.

No retained point is a contact. A flat light segment is off every priced vertical threshold; diagonal boundary pieces meet such a threshold only at isolated values of \(V\). The explicit objective error is
\[
 \delta\sum_{\rm horizontal}|c_h|
 +2\eta\sum_{\rm cells}\sum_{\rm active\ vertical}|c_v|.
\]
The point-side values and the middle fill values are exact. Only horizontal shifts and the two short bridges can lose score. The code checks this error against a direct physical signed-CDF scorer, which uses chronological segment geometry rather than inverse-label rewards.

The physical scorer retains closed and strict contacts exactly. The zero-scale polygon is useful for inspecting phases but may have a much smaller literal payoff. It is never substituted for the actual rational witness.

## 5. The full 26-pair test

The reproducible input contains 138 signed CDF point terms and 71 signed unit-ray terms from the exact 26-reflection-pair basis attacker, plus its original routes and causal selectors. The finite arrangement has 275 query rows, 274 fill rows, 664 labels, 114,942 threshold nodes, and 231,592 graph arcs.

The exact global selector supremum is
\[
 \frac{7483120787388344786724063}{4835703274095654559809536}
 \approx1.5474731105762056.
\]
The independently certified actual capture supremum of that same Monster law is the distinct quantity
\[
 \frac{7483097521803449565333963}{4835703274095654559809536}
 \approx1.5474682993660103.
\]
Their difference is about \(4.81\times10^{-6}\).

Actual minimum/maximum cut realizations have 51/587 radial vertices. Both plane scores are within \(2.21\times10^{-15}\) of the selector supremum, inside the explicit \(2.86\times10^{-15}\) error. Direct chronological first contacts against all 52 Monster orientations give capture scores about 1.547468299366008.

The minimum witness starts just above \(117/128\). Its smallest retained physical point margin is
\[
 1/2548034363503987214413749060589817855737856.
\]
Its zero-scale polygon has 50 vertices and literal capture score about 1.3686626207. This discontinuity is recorded, not hidden by rounding its initial position or replacing the actual path.

The standalone full replay checks 156 chronological captures (including the inspection polygon), 138 retained point contacts, and 760 signed ray subintervals. Separate independent packets provide:
- 47 physical cases, 4,747 exact score comparisons, 4,183 sampled legal-path upper checks, 564 optimal/arbitrary-label realizations, and 890 selector-versus-capture comparisons;
- eight exact prefix-DP compiler games, 89 point checks, 133 physical ray pieces, and 40 tight selector identities;
- the independent rational query/fill realization proof and its 84-assignment regression.

These checks validate the oracle and this supplied affine functional. They do not establish a lower game guarantee, an equilibrium, or a complete best-response-face extension.

## Replay

From the repository root:
```sh
node packages/interval_global_closure/verify_selector_plane_oracle.mjs \
  packages/interval_global_closure/snapshots/selector_global_26_input.json \
  /tmp/selector_global_26_replay.json
node packages/interval_global_closure/verify_selector_plane_physical.cjs
node packages/interval_finite_reduction_audit/verify_selector_compiler_independent.cjs
```

The first command rebuilds the exact graph and actual rational paths. The independent verifiers use different dynamic programming and physical integration implementations. All dependencies are repository-relative; the atomic engine is the sibling `interval_turn_density/atomic_survival_v8.cjs`.
