# Proof gates for an exact geometric solution

Let F denote an admissible ordered Princess CDF (possibly representing a continuous distribution of paths), m any legal deterministic Monster path, and J(F,m) its **actual chronological first-capture expectation**. Let μ be a probability law on legal physical Monster paths. An exact saddle value c is established by the pair of universal inequalities

\[
(\forall m)\quad J(F,m)\ge c,\qquad
(\forall p)\quad \mathbb E_{m\sim\mu}T(m,p)\le c,
\]

where p ranges over **all** legal deterministic Princess paths. A family F_k with security tending to c can replace an attaining F. The joint probability and support conventions must match the original hidden-path game, including free starts and capture at time zero. The full minimax manuscript gives the precise quantile representation.

## G1. Contact completeness

From the global first-variation and physical capture record, identify supported phases and complementary slackness. Prove that every optimal Monster physical response lies in those phases, or prove all omitted phases have no lower payoff. Existing P/S/I/J/shadow cost identities are **necessary test rows** only. Do not infer completeness from numerical activeness or regularity of a trial field.

The [direct P1 projection counterexample](../12-global-closure/FRONT_ONE_PROJECTION_SECURITY_LOSS.md) excludes universal front-one preservation, even for some regular bounded-density laws. A value-level front-one reduction therefore needs a different or stronger argument. The [compensated curvature variant](../12-global-closure/COMPENSATED_CURVATURE_AND_CUSP_RESPONSE.md) resolves one cusp response but still excludes whole-inner coverage through U=21/16.

## G2. Legal field construction

Solve the free-boundary/Volterra/transport system with interior monotonicity, F_x≥|F_t| on smooth patches, symmetry, correct initial distribution, endpoint atoms, all interface/trace matching and valid ordered-path representation. Include the initial-inward column correction; do not impose a flat principal front or a Puiseux ansatz without verifying it. Produce either one admissible F or a rigorously specified approaching sequence F_k.

## G3. Lower against every Monster

Use the full two-record precenter/center Bellman certificate, or prove an equilibrium-sufficient response normal form that includes arbitrary starts, endpoint hits, long turns and infinite center excursions. Handle the W=0 precenter exit as its own interface. If invoking curved-phase or central compression lemmas, prove their field-side assumptions, not just the local algebra. Reject any fixed finite sampled bank as a global lower proof.

The [whole-region first-exit theorem](../12-global-closure/POSITIVE_PREFRONT_RESPONSE_AND_MODULUS.md) is now available, but the same note excludes maintaining its inner monotonicity through U=41/40. A competitive application needs an additional phase. The continuity-modulus center bound applies to positive record gaps; the [static free-start Zeno counterexample](../12-global-closure/GLOBAL_FREE_START_ZENO_COUNTEREXAMPLE.md) rules out a universal finite-turn assertion for all legal fields. These results refine G1/G3 without discharging them.

## G4. Matching physical Monster upper

Exhibit a legal path law μ and its causal capture/clock coupling with upper ≤c against **every Princess path**. The existing 752-pair rational law yields a nonmatching upper; its clock optimality for its own support does not prove global optimality. A physical law cannot be replaced by an unlifted clock flow.

The [synchronized pressure theorem](../12-global-closure/SYNCHRONIZED_PRESSURE_AND_FINITE_SUPPORT.md) is a new global restriction on this dual: matched resources can select equal times, with exact antipodal cancellation at positive times. For a fully matched law on N oriented paths, clocks and paths have an explicit finite normal form. This discharges a trajectory-complexity assumption **conditional on N**. It supplies no support-size bound or matching value; finite support in this fully matched representation must itself be proved.

## G5. Characterization and validation

A unique solution to a **complete necessary-and-sufficient** functional system would be an analytic solution even without elementary c. Existence, admissibility, boundary conditions, and all-path equivalence must be justified. A system written only for guessed active sheets is not such a characterization. State whether c is attained on either side; finite Princess initial support is ruled out for attainment.

## Evidence standard

For any proposed interface/phase:
1. State the complete parameter and endpoint domains.
2. Derive its actual capture cost, including ties and endpoint atoms.
3. Check transport and chronological consistency on adjoining phases.
4. Supply a uniform proof of all-path domination, or a precise disproof witness.
5. Separate mathematical argument from finite Fraction/Python/CI regression.
6. Preserve any claimed rational certificate with an independently checked implementation.

Known rational bounds and verification commands remain at [the certificate note](../12-global-closure/NORMALIZED_GLOBAL_BOUND_CERTIFICATES.md) and [REPRODUCE.md](../../REPRODUCE.md). No new theorem is claimed by this agenda.
