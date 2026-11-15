# Local prefix normal forms, ordered fan oracles, and a whole-basis exclusion

Date: 2026-11-12 UTC.

**The unrestricted interval game remains open.** This checkpoint closes local initial-prefix reductions, implements exact continuous-start separators for fixed laws, and rejects one entire candidate basis. It does not identify a matching saddle pair, and the existing unrestricted value bounds are unchanged.

## 1. Initial turns: the local obstruction and its repair

Inside one affine CDF corridor
\[
F(t,x)=q_0+\alpha t+\beta x,\qquad\beta>|\alpha|,
\]
the rank coordinate has constant one-sided speeds \(\beta+\alpha\) and \(\beta-\alpha\). With fixed final records and an exit state/time, the capture moment is a strictly concave quadratic in intermediate record levels. The two parity order chains and one travel budget have vertices with at most one partial intermediate level. Removing nonproductive repeats gives at most three productive legs, a connector, and a constant-rank hold.

The **whole rank-time corridor must stay in that affine cell**. This condition cannot be dropped at a stationary density interface.

At such an interface the two densities differ:
\[
F(t,a+x)=q_0+\alpha t+\beta_\pm x.
\]
A direct concavity extension is false. The saved exact 49-leg example has positive normalized curvature \(1504/441\). It is preserved as a failed-proof audit, not discarded after finding a replacement.

The repair has two physical steps. An arbitrary same-side excursion, with any number of internal turns, can be normalized to its maximal unit tent or an interface wait. For excursions opposing a positive CDF flux, the extra lower ranks captured by the maximal tent pay for its possible delay of upper ranks. This comparison needs the affine earliest-future-hit region through
\[
\gamma T,\qquad
\gamma=\frac{B}{B-\alpha}+\frac12.
\]
Next, when interface flow overtakes a previous right excursion, an exact two-target comparison deletes the right-left pair. It covers the positive crossover term that broke the earlier concavity argument.

After these steps, fixed-time parity variations have the sum-of-squares identity
\[
Q(v)=-\frac{K+1}{2}\sum_j(z_j-z_{j-1})^2.
\]
Every active order, amplitude, and flow face either removes a nonproductive excursion or permits the physical deletion. This gives **at most five complete interface tents** for a sufficiently small return block. The separately labelled old-record extension subtracts only a constant and a linear term; it does not assume that resetting at a left return erases a pre-existing upper record.

The last partial one-half excursion is handled by constrained earliest rank travel and the last active interface face. The resulting initial-source normal form has **at most 15 affine pieces**: five complete tents, three productive unit legs, a constant-rank hold, and a connector. The uniform finite-sequence bound precedes the compact limiting argument, so initial accumulations of infinitely many turns are included.

These are local theorems with a real persistence hypothesis. A global computable turn count cannot be inferred from local finiteness or compactness alone.

Proofs and exact implementations:

- [Single affine corridor](../10-turn-density/AFFINE_RECORD_PREFIX.md)
- [The failed concavity extension and exact crossover deletion](../10-turn-density/INITIAL_DENSITY_INTERFACE_AUDIT.md)
- [Arbitrary same-side excursions](../10-turn-density/AFFINE_INTERFACE_EXCURSION.md)
- [Finite interface-return block](../10-turn-density/INITIAL_INTERFACE_RETURN_BLOCK.md)
- [Final one-half bridge](../10-turn-density/AFFINE_HALF_CELL_BRIDGE.md)

### A finite optimal response exists for each fixed fan

These local results now imply an unrestricted **existence theorem** for a fixed finite positive-width fan law. The stationary-tail reduction gives a common finite response horizon. Compactness and lower semicontinuity give an optimum within that horizon. After any positive captured rank width \(w\), the bounded interior density \(C\) separates opposite productive record events by at least \(w/(2C)\). Each resulting one-sign episode has a pointwise dominating bridge with at most three affine pieces. The local 15-piece theorem removes the only possible initial accumulation, and a first endpoint contact permits a dominating opposite sweep.

Consequently some optimal response has finitely many affine pieces. For ordinary rational fan data, its value and some optimal vertex coordinates are real algebraic: for the finite number of pieces furnished by existence, the exact capture-cost arrangement is semialgebraic over the rationals.

Neither argument supplies an effective piece count or proves algebraicity of the unrestricted game's value. See [finite response existence and its algebraicity corollary](FINITE_FAN_RESPONSE_EXISTENCE.md).

## 2. Ordered fan costs and complete continuous-start families

The fixed interval-fan provider now has an exact common-quantile cost evaluator. It computes captured running CDF records and integrates \(1-H+L\), with strict/closed endpoint traces. It also supplies exact supergradients in the weights of fixed physical fan rows.

For a specified Monster route, the ordered cost is concave in the marginal weights. Its supporting upper planes are useful for complete weight optimization and for rejecting a whole fixed basis. They are not unrestricted Monster-response certificates by themselves.

Two exact continuous-start separators have been completed for both raw interval mixtures and their ordered realization:

1. the complete first-sweep/return M1 family;
2. every legal initial start for a supplied complete fixed unit tail.

The ordered separators add rank-equality cuts to the raw geometric arrangement. In the moving M1 family, intersections of event lines from different fan components are also necessary. On each complete arrangement cell the cost is quadratic; the separator checks cell endpoints and any interior stationary point. It retains closed endpoint atoms and germ distinctions.

The independent ordered checks integrate first-capture quantile bands directly; they do not reuse the survival-area computation that is being tested. These separators remove continuous initial positions as a sampling issue for their stated route families. They do not make those families exhaustive over all future Monster turns.

- [Ordered fan costs and weight planes](ORDERED_FAN_COST_AND_WEIGHTS.md)
- [Raw continuous-start arrangements](CONTINUOUS_FAN_INITIAL_STARTS.md)
- [Ordered continuous-start arrangements](ORDERED_FAN_INITIAL_STARTS.md)

## 3. Reflected endpoint fans

A separate new family folds an outward translation at the endpoint:
\[
p_z(t)=1-|1-p(t)-z|,\qquad z\in[\ell,h]\subseteq[0,1].
\]
For nonnegative base paths, this preserves legal speed and avoids center/endpoint atoms for positive interval width. The exact provider uses the folded CDF directly. It includes arbitrary causal constant/current history selectors, so the resulting upper planes do not depend on guessing the correct numerical record activation.

The existing finite center-return reduction extends to these folded marginals: their density edges still have slopes \(0,\pm1\), and the local center diamonds retain the same stationary form. This extension does not give a uniform count when a family of source paths or widths itself tends to a singular limit.

The old clipped-fan rows and the new folded-fan rows remain distinct physical strategies.

## 4. An exact exclusion of all weights in one proposed basis

The ordinary collapsed 342-profile basis was tested with folded outward width \(1/1024\). It is now rejected for **every probability vector**, using 26 legal Monster reflection pairs and exact linear history-selector inequalities:
\[
\sup_{w\in\Delta_{342}}\inf_m C_m(w)
\le
\frac{1711141066194169545376440}
     {1208925818523913639952384}
\approx1.415422716576155.
\]
This is strictly below the repository's existing unrestricted lower bound.

The certificate makes no numerical LP optimality assumption. It checks 87,070 exact profile-enclosure comparisons, 269,119 clipped-affine integral cells, and all 8,892 upper-plane coefficients, then verifies the final inequality by integer arithmetic.

The attacking Monster mixture itself has an unrestricted Princess response supremum about \(1.5474683\), with two separately realized physical approaching witnesses. Therefore the \(1.4154\) number is explicitly a restriction-of-basis statement, not a game upper bound.

See [the complete basis-exclusion proof and replay](REFLECTED_FAN_BASIS_EXCLUSION.md). Weight refinement within this fixed basis is stopped.

## 5. Verification and current next obligation

The mathematical arguments have independent internal audits and exact BigInt rational replays. The native executor was unavailable during these checks; no native replay, Lean compilation, or CI is claimed. The upper-worker's default dependency path now points to the actual committed atomic response engine, so its documented CLI does not depend on a scratch-only copy.

The outstanding global construction still needs an exact constant and matching unrestricted inequalities. The local prefix theorem, finite center theorem, stationary-tail dynamic program, and continuous-start arrangements provide useful components. A global finite response certificate for a specified law and a globally sufficient equilibrium construction remain separate obligations.

The current constructive direction is a global oracle for the linear history-selector functional over all legal Princess paths. Unlike reweighting a fixed basis, that oracle can introduce the missing marginal shapes while preserving exact certificate inequalities. It must include strict/closed contact predicates and the full legal trajectory geometry before being used to support a closure claim.
