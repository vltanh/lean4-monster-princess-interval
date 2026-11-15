# Unrestricted-bound attack: substantive-improvement gate (2026-11-12)

**Outcome: no meaningful certified improvement to the unrestricted game bound in this continuation.** This is a negative experiment/handoff, not a new value certificate or a solved game.

## Verified baseline and the improvement threshold

The existing exact 338-path Princess law guarantees
\[
L=\frac{36290299773897097}{25600000000000000}
=1.4175898349178553515625.
\]
The exact warped 280-pair Monster certificate on this branch gives
\[
U=\frac{57045188913812444387410009}
        {40000000000000000000000000}
\approx1.426129722845310,
\]
through \`packages/interval_common_warp/upper_warp_tight_exact.json\`. Its correction to the preceding certificate is only \(2.1461\times10^{-8}\), **not** a substantive step toward the requested closure.

The full-game gap is still about \(0.00854\). For the next **meaningful** upper-side checkpoint, require a rigorous all-Princess upper certificate below **1.4255** (over \(0.00063\) improvement, about 7% of the gap); do not repeat the old 68-knot weight nudges.

## Global-oracle diagnostics: isolated changes to the existing upper law fail

The following were actually evaluated by the global rational-geometry maximum-cut Princess oracle \`E.Rational.Model.solve\`, not by a list of sampled Princess paths. Its capacities are floating-point: these are **diagnostics and rejected candidates**, not exact new bounds.

| New normalized Monster law | Global Princess response |
| --- | ---: |
| Original warped 280-pair law | 1.4261297443 |
| Mix 0.05% of reflected right-first sweep from \(-1/2\) | 1.4266625026 (worse) |
| Mix 5% of the same reflected sweep | 1.4798192871 (worse) |
| Mix 1% of twelve signed early M3 routes at \(z\in\{1/32,1/16,1/8\}\), \(s\in\{3/4,7/8\}\) | 1.4418643098 (worse) |
| Apply a non-odd tent-based causal coordinate deformation with parameter \(+1/16\) to the route representatives, then reflect | 1.4316742932 (worse) |
| Same deformation with parameter \(-1/16\) | 1.4324961398 (worse) |

The non-odd deformation was \(F(U)=U+\epsilon h(U)\), \(G(V)=V-\epsilon h(V)\), where \(h\) is even on \([-1,1]\), equal to \(1-|u|\), and extended by \(h(u+2)=-h(u)\). For \(|\epsilon|<1\), both transformed light coordinates remain monotone; the endpoint and time-zero boundaries are preserved. Its reflected Monster law is legal. These counterproductive trials show that a local initial-strategy payoff gradient is not a reliable global response criterion.

## Lower-side diagnostic: the same 169 Princess-path shapes, new weights

An exact first-hit pair matrix was generated for 163 legal Monster route controls (the sixteen archived warp attackers, endpoint sweeps, the archived best response, and a 64th-grid sweep bank). The free-weight Princess LP had a **restricted** value about 1.42376060545. Critically, the signed reflected pair for path index \(i\) is given by event indices \((168-i,169+i)\); an initial reversed-index trial was discarded. The corrected matrix independently reproduced each route's base-law score.

The LP concentrates mass on 25 original positive-half profiles. An unrestricted canonical Monster response to that candidate costs **about 1.23018071**, far below the finite-bank value. An exchange with 24 added unrestricted attacks decreased the 187-route restricted LP value to about **1.41962536**, but the candidate still suffered a Monster response around **1.3647**. None of these LP values is a lower bound for the original game.

Adding the reweighted distribution back to the archived law also failed a full canonical-response check:

| New-path mass \(\theta\) | Unrestricted Monster response |
| --- | ---: |
| 0 (original law) | 1.4175898349 |
| 0.01 | 1.4157157517 |
| 0.03 | 1.4119675692 |
| 0.05 | 1.4082193864 |
| 0.10 | 1.3988489296 |

The canonical search checked all starts and capture-order branches under its stated pruning rules with no node cap hit; the displayed decimal candidate responses use floating-weight scoring, **not** a new rational lower certificate. Increasing the bank objective while losing to off-support attacks does not tighten \(L\).

## The actual promising upper-side target

The *existing* normalized M3 density law in
\`packages/interval_turn_density/m3_attached_settled.json\` gives a numerical response approximately **1.425185838159153** (about **0.000944** below the old certified upper). Its analytical representation and conditional all-Princess four-scalar reduction appear in \`research/10-turn-density/EARLY_M3_RESPONSE.md\`. This is already a stronger discovery direction than further common-clock optimization.

The remaining **concrete certification gates** are:

1. **Exact legal Monster law.** Reconstruct rational or rigorously interval-enclosed, normalized density coefficients, including both signed early M3 sheets, the corrected negative early edge, and both late sheets. Check every sign, residual, edge, and Gamma condition required by the conditional four-scalar response theorem. Zero-slack constraints need exact matching, not rounded floating inequalities.
2. **Exact global four-scalar bound.** Verify a conservative ceiling below \(1.4255\) for every \(0\le a\le u\le1\), \(-a\le c\le y\le1\), with curved prefix determined by the true first-crossing equations. Include c=y=1 limits, negative c, flat equality corridors, characteristic coincidences, and exact-contact adverse conventions. Numerical optimizer convergence, sampled parameter rows, and a small primal/dual discrepancy cannot replace this proof.
3. **Unrestricted conclusion.** Only after steps 1-2 and the previously proved reduction hypotheses are verified, declare \(V\le1.4255\), replay the normalization and interval-arithmetic certificate, and update STATUS.md with the rational bound.

This is **not** a claim that the M3 numerical law already meets these gates. The exact full-game value and global saddle remain open. Next session should focus on closing the M3 certificate rather than more isolated route additions, common warp nudges, or finite-bank values.
