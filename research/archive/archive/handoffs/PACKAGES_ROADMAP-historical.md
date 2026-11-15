# Finite-gate roadmap toward an exact unrestricted game solution

The exact value is unknown. Do not claim completion by improving decimal bounds or growing strategy supports indefinitely. A final proof needs one explicit constant c and an unrestricted saddle pair (or epsilon-approaching lower family):

    E_{M ~ nu}(T(M,p)) <= c       for every princess p,
    E_{P ~ mu_eps}(T(m,P)) >= c - o(1)   for every monster m.

## Auditable gates

- [x] **G0 — Preserve research state.** Archive all proof packages and source verifiers, isolate speculative work, mark unproved lemmas. (This PR.)
- [x] **G1 — A finite-support princess-response oracle.** Event deadlines and min-cut certificates against arbitrary princess trajectories; closed for finite piecewise-linear monster mixtures, subject to proof audit.
- [x] **G2 — A finite-support monster-response oracle.** Capture-order enumeration against a fixed finite mixture of piecewise-linear princess paths; implemented and validated on individual instances, subject to structural-lemma audit.
- [x] **G3 — Exact optimization of an initial finite monster support.** 32-path support LP solved with matching rational primal/dual certificates, then excluded globally. This gate is a *negative result*, not a step toward proving its candidate value.
- [ ] **G4 — Audit both continuous reduction lemmas.** Check the envelope converse, boundary starting positions, overlapping moving paths, first encounter vs tangencies, and capture-order normalization. Seek adversarial counterexamples and an independently readable proof. Do not expand experiments before this audit.
- [ ] **G5 — Obtain a globally sufficient finite equilibrium-support theorem OR a closed-form continuum equilibrium.** This is the key currently missing structural theorem. A uniform approximation theorem alone does not satisfy G5.
- [ ] **G6 — Identify exact candidate c and a pair of strategies/approximating families.** Derive from analytic optimal-control or exact finite LP duality; avoid inferring c from a numerical decimal.
- [ ] **G7 — Verify upper inequality for every princess path.** Use finite deadlines if finite monster support, or a continuum proof otherwise; include boundary conditions and capture-time discontinuities.
- [ ] **G8 — Verify matching lower inequality for every monster path.** Use capture-order reduction if finite princess mixtures, or an epsilon/continuum limit with uniform global control.
- [ ] **G9 — Produce a standalone hand proof and mechanically check critical finite arithmetic.** Reduce computational steps to exact certificates. Optionally formalize in Lean; no formalization currently included.

## Immediate next experiment with a stopping rule

Use the two exact best-response oracles in a double-oracle primal/dual search. For each support expansion, retain a rational monster upper certificate and princess lower certificate; only declare a case closed if both are unrestricted and match exactly (or via a rigorous limiting argument). If new counterexamples continue to appear, stop growing the support and prioritize G5, a genuine global structure theorem. Maintain distinct ledgers for finite supports versus a fully exhaustive reduction.

## Notes on finite approximation

`interval_uniform_reduction/PROOF.md` proposes an error-controlled limit of finite games. This supplies a potential computable characterization of V, but neither a simple exact constant nor a finite terminating certificate. Its CDF quantile-coupling and regularization proof should be independently audited before relying on it for any theorem beyond this research draft.
