# Directive — separate the one-interior-turn Monster subgame

**CLOSED NEGATIVELY, 2026-11-14.** Alternative (M) is proved by the [physical continuum countercertificate](ONE_TURN_SEPARATION_COUNTERCERTIFICATE.md):
\[
 W_1\le\frac{142472349375511}{100000000000003}
 =1.424723493755067\ldots<\frac{57}{40}<U_*.
\]
All 730,146 exact rational potential inequalities pass with zero residual repair. The target (P), and therefore W_1>U_*, is false. The exact value of W_1, the unrestricted V, and whether W_1=V remain open. The original target, gates and hygiene rules below are retained as the resolved research specification; they are no longer instructions to continue the separation search.

## Objective, baseline and definitions

In the unrestricted Princess–Monster first-coincidence game on [-1,1], the players choose independent hidden 1-Lipschitz paths with free initial positions. Let
\[
U_*=\frac{291849329389899}{204800000000000}
=1.4250455536616162109375
\]
be the already certified **all-Princess physical Monster upper** on the unrestricted value \(V\).

Let \(\mathcal B_1\) be exactly the class defined in [ONE_TURN_SUBGAME_BRACKET.md](ONE_TURN_SUBGAME_BRACKET.md): the Monster starts anywhere, follows unit-speed straight legs with **at most one interior reversal before its first endpoint**, and then sweeps directly to the opposite endpoint. The first-endpoint reversal is not counted as interior. The Princess is **unrestricted**. Define
\[
 W_1=\inf_{\nu\in\mathcal P(\mathcal B_1)}
            \sup_{\text{legal }p}\mathbb E_{\nu}T(m,p).
\]
The proven bracket is
\[
1.4222581340234375 \le W_1 \le 1.424723493755067\ldots.
\]
**W_1<U_* is proved.** The new continuous physical law and its exact all-Princess potential certificate are in [ONE_TURN_SEPARATION_COUNTERCERTIFICATE.md](ONE_TURN_SEPARATION_COUNTERCERTIFICATE.md). The older projected atomic upper remains a reproducible, weaker result.

**Original desired theorem, now excluded:** produce a legal Princess law \(\mu\), preferably a symmetric ordered continuous CDF or a controlled approaching family, and a **strict rational margin** \(\delta>0\) such that
\[
\boxed{\inf_{m\in\mathcal B_1}\mathbb E_{p\sim\mu}T(m,p)\ge U_*+\delta.}\tag{P}
\]
Since \(\sup_\mu\inf_{m\in\mathcal B_1}\le W_1\) by weak duality, (P) proves \(W_1>U_*\ge V\). It shows that the precise **canonical bang-bang/direct-tour class** \(\mathcal B_1\) is insufficient to attain the unrestricted optimum. **It does not by itself exclude one-reversal paths with arbitrary waiting/variable speed or a different endpoint continuation.** State any further normalization theorem separately.

**Competing falsification, now proved:** find a probability law \(\nu\) supported on \(\mathcal B_1\) with an independently certified, universal all-Princess inequality
\[
\boxed{\sup_{\text{legal }p}\mathbb E_{m\sim\nu}T(m,p)\le U_*.}\tag{M}
\]
The new certificate proves (M), hence W_1<U_*, decisively defeating objective (P). An LP objective against a finite Princess bank is not such a certificate; use the legal physical-clock/Qout construction or another complete all-Princess argument.

These are **alternative outcomes**. Do not continue optimizing one side after the other has been proved.

**New complete foundation:** [restricted minimax and the exact grid hierarchy](ONE_TURN_MINIMAX_AND_EXACT_GRID_HIERARCHY.md)
now prove an attained optimal Monster measure and
\(W_1=\sup_{\mu\text{ finite actual}}\inf_{m\in\mathcal B_1}J(\mu,m)\).
The [finite-Princess response theorem](ONE_TURN_FINITE_PRINCESS_ATTACK_SET.md)
prices any actual rational polygonal Princess law on a complete finite
arrangement, including subunit velocities and waits. Dyadic unit-path
finite LP lower values increase to W_1 with no continuum-transfer
subtraction; there is no claimed convergence rate. Consequently a strict
separation, if true, has an actual finite rational certificate and a
continuous piecewise-affine approaching-law certificate. This does not
assert that a particular finite bank or field has achieved it.

## Gate 1 — a complete two-parameter Monster domain and exact response formulas

**CLOSED:** [The complete-domain theorem](ONE_TURN_COMPLETE_DOMAIN.md) exhausts the full closed parameter triangle, proves domination of its extra endpoint face, and supplies a three-integral physical response formula with exact strict/closed traces. It also proves finite quadratic certification for a fixed rational piecewise-affine CDF. The independent rational fixture checker passes 2,432 reflected formula comparisons, 152 contact-tie cases and 1,887 endpoint-face comparisons. The positive-separation Gates 2 and 3 are closed by the opposing countercertificate: their target is impossible.

Orient the first nondegenerate Monster leg to the right, using fair reflection separately. An interior-turn candidate has vertices
\[
(0,a)\to(h,a+h)\to(H,-1)\to(H+2,1),\quad
H=1+a+2h,
\]
where \(-1<a<1\) and \(0<h<1-a\). On this domain the first rightward leg does not hit \(+1\), the reversed leftward leg first hits \(-1\), and the post-endpoint tour is legal. Also include **the degeneracies** \(h=0\) (straight to \(-1\)), \(h=1-a\) (actual first hit at \(+1\), an \(S(a)\) endpoint-first path), true endpoint starts, and their reflections. These boundary classes have their **own chronological first-hit and endpoint-atom conventions**. Before promoting this parameterization, prove it really exhausts \(\mathcal B_1\), including possible turns on the negative side \(a+h<0\) and time-zero contacts.

The existing [bulk P/S formula](../12-global-closure/BULK_CONTACT_AND_CUSP_EQUATIONS.md) uses \(b=a+2h\) and, for \(P(a,b)\), assumes \(b\ge0\) and \(a+h\ge0\). **Do not identify it with the entire rectangle/triangle**: supply the missing negative-side and contact-degenerate formulas or a genuine pathwise domination theorem excluding them. Keep \(-1<a<1\), late \(b>1\), and endpoint trace jumps. The saved physical witness with start \(a=-7/8\), late turn \(b=67/64\), is a required regression.

**Pass:** a theorem specifying every parameter region and codimension-one boundary, with exact physical first-capture payoff for any admissible candidate CDF; independent rational checks of representative interior, boundary, and tied-contact paths. **Fail:** "checked a dense mesh" or a formula covering only \(b=1\)/positive starts.

## Historical Gate 2 — positive separation, now excluded

Work on admissible Princess continuous distributions or actual finite laws followed by the proved regularization argument. A finite actual rational polygonal law is now a complete alternative certificate route: price its full attack arrangement exactly, prove a strict margin, then invoke the compactness/joint-lower-semicontinuity regularization theorem to obtain continuous approaching laws. Formal contact labels and sampled-clock profiles are not actual finite laws. Transport, symmetry, endpoint atoms, trace matching and legal ordered quantile motion remain non-negotiable.

Optimize a small number of *qualitatively distinct* piecewise-affine CDF geometries against all the Gate-1 response families. For each proposal:

1. use the exact \(C_E,C_S(a),C_P(a,b)\) identities where their hypotheses hold, and chronological formulas elsewhere;
2. minimize the **actual continuum capture expectation** over all continuous \((a,h)\), including open boundaries and one-sided limits; do not accept a sampled-clock/clock-grid minimum;
3. require a **buffer** \(>U_*+\delta\) large enough to survive exact rounding and any interpolation losses; emit the minimizing physical attack if the test fails;
4. reject the candidate immediately if an actual legal one-turn attack scores \(\le U_*\).

A previous attempt had sampled-clock score \(1.428599525640625\) but was defeated by an actual one-turn route with continuous cost \(1.4106390267557076\ldots\). This is a **failed candidate, not evidence for (P)**. Retain this example as an adversarial fixture, and ensure exact physical contact follows the agreed interpretation.

**Pass:** a legal candidate with a uniform, mathematically justified *positive margin* on **all** continuous Monster parameters. **Fail:** any finite path-bank minimum, high-resolution plot, floating solver dual or unproved discretization-to-continuum transfer.

## Historical Gate 3 — positive-separation certificate, now excluded

For a rational piecewise-affine CDF candidate, use the complete-domain theorem's finite quadratic partition: include **all** CDF-cell crossings, strict/closed capture-record changes, first center/endpoint contacts, ties, initial endpoint atoms and switch-time jumps. Derive the exact objective separately on every piece and boundary; the cost is not one global quadratic. For other candidate geometries, establish the applicable function class and coverage before choosing a sign verifier.

Alternatively, for an actual finite rational polygonal Princess law, use the exact finite attack arrangement and chronological inverse oracle. The general checker explicitly includes interior waits and subunit slopes. Every actual arrangement vertex must meet a rational target strictly above U_*. A successful finite-law lower can be regularized by the proved theorem; no numerical smoothing width follows automatically.

Minimize exactly using analytic monotonicity/convexity, rational polytope stationary/face checks, quantifier elimination, or validated interval isolation **with a published coverage proof**. Prove a single explicit rational \(c>U_*\) and verify every piece/face using an independent implementation or hand-verifiable tables. If the Princess strategy is obtained as an approaching family, prove its security tends to \(c\) uniformly over the complete Monster class.

**Original pass criterion:** all-path certificate (P) with source, rational margin, independent verifier, exact replay commands and full assumptions. This gate is now **closed as impossible** by the opposing certificate (M).

## Historical competing search (M), now completed

In parallel with Gate 2—but with a hard budget—try a **reweighted continuous distribution** over all \(\mathcal B_1\) paths, particularly full \(P(a,b)\), not just principal \(P(a,1)\). The old ablation showing that **fixed** weights fail is not an exclusion of the entire one-turn class. If a physical candidate achieves a possible upper \(\le U_*\), promote it only with a global all-Princess causal-clock or complete response certificate. A restricted-master optimum or probability mass chart is diagnostic only.

## Historical stop rules and research hygiene

**Closed local alternative:** [the endpoint-only repair obstruction](ONE_TURN_ENDPOINT_REPAIR_OBSTRUCTION.md)
proves that no replacement of the earlier fixed endpoint component by any
one-turn distribution, with arbitrary new starts, can reach the target
while the interior law stays fixed. The exact response floor for that repair
family is `62211501887219437/43648000000000000 > U_*`. Finer clocks alone
cannot help the fixed law by more than `9803/1024000000000000`. Any new upper
attempt must change the interior law or leave the theorem's stated family.
This closes that modification family. The later continuous law changes the interior law and proves (M), excluding (P); the exact subgame is still open.

- Prioritize Gate 1 (finitely parameterized **exhaustion theorem**) before broad optimization. Avoid growing a sequence of new local contact lemmas without closing a global parameter region.
- Attempt a **small number of distinct CDF geometries** and both proof directions. If several fail on the same first-contact boundary, analyze that boundary as a structural obstruction instead of increasing grid size.
- Do **not** rerun the unchanged billion-transition original certificates merely to prove this restricted statement. Freeze the unrestricted \(L,U_*\) as benchmark inputs.
- If a universal sign or endpoint/clock continuity claim fails, preserve the counterexample and amend the model; never silently discard a response family.
- Every reported quantity must be labeled **candidate finite-bank value**, **actual physical response**, **verified all-\(\mathcal B_1\) lower**, or **all-Princess \(\mathcal B_1\) upper**. A successful CI fixture does not formalize a continuum theorem.
- Deliver a self-contained proof or a precise obstruction, update [STATUS.md](../../STATUS.md) and this directive, commit incremental verified results to PR #1, and include hashes/replay sources. If no strict separation exists yet, state exactly which gate is blocked instead of reporting numerical progress as closure.

The original unrestricted research program remains at [NEXT_WORK.md](../../NEXT_WORK.md). This was its finite-geometry comparison subproblem; the comparison is now resolved and the unrestricted exact game remains open.
