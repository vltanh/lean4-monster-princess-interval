# Realizing light-coordinate query profiles over rational germs

This component turns a finite query profile over \(\mathbb Q(\epsilon)\) into an actual legal family of radial paths. It keeps the microscopic interpolation as explicit candidate data. It does not assert that two realizations with the same limiting labels have the same adaptive-monster value.

## Input and subordinate scale

The input is a strictly increasing list of query coordinates \(v_j\), an ordered list of base levels \(b_k\), and labels \(3k+\sigma+1\), with \(\sigma\in\{-1,0,1\}\). The virtual first query is \((U,V)=(0,-1)\). All coordinates have finite limits. The perturbed query value is
\[
P(v_j)=b_{k_j}+\sigma_j\delta.
\]

The scale is chosen once for the whole model, so every response row uses the same perturbation. Form the ordered union of the base levels, \(v_j,-v_j,v_j+2\), physical constants, and any extra supplied geometry. If \(m\) is the largest vanishing order of a positive adjacent gap, choose
\[
K>\max(0,m),\qquad
\delta=\epsilon^K,\qquad
\rho=\epsilon^{K+1},\qquad
\eta=\epsilon^{K+5}.
\]
The implementation verifies every adjacent gap is larger than \(8\delta\) for sufficiently small positive \(\epsilon\), with a common explicit sign radius. A supplied cached scale must come from the same complete geometry. Query monotonicity and the strip \(0\le U-V\le2\) are independently checked after applying the side labels.

This distinction is essential when two coordinates have the same limit but differ by, for example, \(\epsilon^3\). Such a difference remains part of the Monster geometry; it cannot be silently replaced by a side label or by equality.

## Four interpolation choices

Between two queries, choose a jump coordinate strictly inside their V interval, then use horizontal or vertical light segments, with the boundary diagonals \(U=V\) and \(U=V+2\) when needed.

- **Late/minimal:** put the jump just before the next query.
- **Early/maximal:** put the jump just after the previous query.
- **Isolated avoided:** if the previous base is exactly the next query V, and the next base is larger, move the jump below the incoming characteristic by at least \(\delta\).
- **Common wave:** in that same exact-equality case, use the shared outgoing coordinate \(V=b-4\delta\).

The isolated rule tests equality of rational germs, not equality of limits. The report records intervals with merely equal limits and every center wait introduced by the selected fill. A center interval produced by late fill is not automatically unavoidable: early fill may remove it while changing other first-inverse moments. Its provenance therefore remains explicit.

The connector consists of four monotone moves: advance V at fixed previous U; follow the center boundary if necessary; advance U at the chosen V and then along the endpoint boundary if necessary; finally advance V at fixed target U. The two queried points lie in the strip and are ordered, so every move stays in the strip. Its first and last U values at each query both equal the intended perturbed value.

Under \(t=(U+V)/2,\ p=(U-V)/2\), monotone U and V give \(|p'|\le1\). Trimming the virtual negative-time part at \(t=0\) gives a legal radial path in \([0,1]\).

## Strictification is a separate choice

The module supports the raw graph, affine radial shrink
\[
p\mapsto(1-2\eta)p+\eta,
\]
and clipping
\[
p\mapsto\max(\eta,\min(1-\eta,p)).
\]
Both strict variants are legal. Every nonzero queried side is checked after the change. Changed side-zero first/last traces are reported, rather than treated as equivalent.

Clipping preserves unit-speed legs and waits. Threshold intersections on a unit radial leg are computed directly in light coordinates, without creating rational-function slopes. If the input query and base coordinates are polynomials of degree at most D, then K can be chosen at most D+1, and the clipped output coordinates have degree at most D+6. This avoids the exponential degree growth caused by repeatedly substituting \(\delta^6\). The degree statement concerns the output geometry; intermediate sign comparisons may have larger degree.

A fixed upper-cut score must still be checked by physical first capture. In particular, zero-side changes are not covered by the nonzero-side trace audit.

## Family-level one-sign gate

Avoiding a center separately on each path is weaker than ordering a whole coincident band. A useful sufficient gate on a declared wave is
\[
U_p(t)\ge b+\delta u_{\min},\qquad
V_p(t)\le b+\delta v_{\max},\qquad u_{\min}>v_{\max}
\]
for every participating radial path during that wave. A monster cannot capture both reflected signs during it: after a positive contact its U would have to decrease at a negative contact, or after a negative contact its V would have to decrease at a positive contact.

Incoming offsets in \(\{-1,0,1\}\) and the common outgoing offset \(-4\) provide a strict local gap. Endpoint waits and later phases must be excluded from, or separately checked against, the declared wave bounds. This is a construction option, not an automatic global improvement theorem.

## Exact tests

The portable verifier checks:

- 48 synthetic combinations: four geometries, four fills, and three strictification choices;
- 24 independent physical signed-pair recaptures: six upper-germ fixtures, both extremal label profiles, and affine/clip variants;
- exact agreement with the previously verified clipped connector on four controls from the actual159-row checkpoint.

The nested initial-layer fixture has Monster coordinates separated at order \(\epsilon^3\). It selects \(K=4\). Its clipped minimum-profile score is exactly
\[
2-\epsilon/8+\epsilon^2/4+\epsilon^3/8-3\epsilon^4/8-\epsilon^5/8,
\]
so its limiting response is 2. Collapsing the Monster geometry first would instead give \(3/2\).

These tests establish the reported realizations and captures, not a minimax lower strategy. The retained159-row law is independently rejected by complete M1 separation.

## Replay

```sh
node packages/interval_global_closure/verify_generalized_realizer.mjs \
  packages/interval_global_closure/germ_atomic_fixture_labels.json \
  generalized_realizer_report.json \
  efficient_checkpoint.json
```

The optional checkpoint argument enables the four compatibility tests. The fixture input is blob 1a8f947ccba776b900a9d628ebf27ddd3dc1176c; the checkpoint is blob 6cac47a4b2227fa1469bb463d35ed37ffb3af1b6.
