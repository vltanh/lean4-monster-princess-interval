# Arbitrary-path preservation under an outward rank-band correction

**Recovery status.** Reconstructed from the retained theorem and audit summary during the 2026-11-11 executor outage. The original physical verifier completed 3,396 exact Fraction checks before the outage. Its source is not reconstructed here.

## 1. Low-start comparison

Let \(p_q,\widetilde p_q\), \(0<q<1\), be ordered nonnegative legal path families, each reflected with probability one half. Suppose they have the same initial quantiles and
\[
\widetilde p_q(t)\ge p_q(t)\quad\hbox{for all }t
\]
for almost every rank. Assume no rank \(q<q_{\rm lo}\) changes. Let \(a_{\rm lo}\) satisfy
\[
A(a_{\rm lo})\le q_{\rm lo},
\]
where \(A\) is the common closed initial radial CDF.

For every legal monster with \(|m(0)|\le a_{\rm lo}\), its expected capture time under the new law is at least its expected capture time under the old law. The assertion covers arbitrary speeds, waits, reversals, and contact atoms.

### Proof

Any changed positive rank starts at \(p_q(0)\ge a_{\rm lo}\ge m(0)\), except for null quantile endpoints. Before its old first contact, continuity gives \(p_q(t)>m(t)\); otherwise a previous equality would already have occurred. Since \(\widetilde p_q\ge p_q\), the new positive path cannot meet the monster earlier. A changed reflected path starts at \(-p_q(0)\le-a_{\rm lo}\le m(0)\). Before its old first contact it remains strictly below the monster, and \(-\widetilde p_q\le-p_q\) cannot meet the monster earlier either. An equality at time zero already has old capture time zero and causes no difficulty. Unchanged ranks have identical costs. Integrating the two pointwise inequalities proves the claim.

The comparison uses the ordered quantiles of the complete new CDF. A sum of shifted rank-band CDFs can reorder paths; one must not simply assert that the physical paths outside the named source band are unchanged. The correct lower-rank gate is that the complete new and old CDFs agree below the band level, which preserves all ranks \(q<q_{\rm lo}\).

## 2. High-start causal equality

Suppose, separately, that the complete strict and closed radial CDF fields agree throughout the incoming cone
\[
U\ge U_{\rm cut}.
\]
Then every legal monster with \(|m(0)|\ge U_{\rm cut}\) has exactly the same capture-time law under the two princess laws.

Indeed the monster speed bound gives
\[
t+|m(t)|\ge |m(0)|.
\]
Every possible positive or reflected contact therefore lies in the unchanged incoming cone. Both strict and closed traces agree there, so the two running signed records, including every contact atom, agree at every time. This proves equality for all histories and all turn counts.

This is an incoming-cone statement. An outgoing-cone hypothesis is neither required nor interchangeable with it.

## 3. Application to the localized source correction

The earlier outward correction in the localized construction changes a CDF band beginning at \(q_{\rm lo}=1/2\), preserves the complete initial CDF, and decreases the radial CDF, hence moves its ordered quantiles outward. Its incoming support lies in
\[
7/8\le U\le29/32.
\]
Consequently it preserves every monster cost starting at \(|m(0)|\ge15/16\), and it does not decrease any monster cost starting at
\[
|m(0)|\le A^{-1}(1/2)
=\frac{1158285233139}{1513364115088}
\approx0.7653711500035452
\]
for the stated endpoint_joint_i1 base.

These comparisons concern this outward source correction relative to its preceding law. A different, later inward warp can affect the low-start band; its effects must be combined with their own exact column or response comparison. One must not infer low-start protection for a composite construction merely from this theorem for one component.

The causal high-start equality concerns the entire changed field, not just its named rank band. Incoming jumps require both strict and closed traces; the localized provider retains the left/right control traces for this purpose.

## 4. Prior exact checks and scope

The original verify_outward_warp_preservation.py completed 3,396 exact Fraction checks before the outage. They included 810 low-start cost comparisons, 486 high-start causal equalities, 162 initial-equality atom cases, 1,170 waits, and 768 strict cost increases. Its fixtures included an actual reordering of higher ranks.

These tests check physical capture comparisons, not a global game value. The proof above supplies the unrestricted path statement once its order, initial-law, unchanged-rank, and incoming-cone hypotheses are established for the full proposed law.
