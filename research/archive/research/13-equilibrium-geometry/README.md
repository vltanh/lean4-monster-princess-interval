> **Exact center-wait subgame solved (2026-11-15):** [a restricted infinite-dimensional saddle](CENTER_WAIT_PRINCIPAL_ONE_TURN_EXACT.md) has value `3/2 - e^(-1/2)/2 = 1.1967346701...`, with an explicit exponential/atomic Monster law and a continuously approaching Princess law. It applies when **every** Princess path enters the exact center and the Monster uses only the principal one-turn front `t+x=1` with nonnegative oriented starts. The same Monster law proves an upper of 1.196735 on the **full** one-interior-turn Monster class against this Princess restriction; it does not give a full one-turn exact minimax value. [Fraction regression](../../packages/interval_center_wait_principal/verify.py).

# Equilibrium geometry — active research index

**One-turn comparison: closed negatively.** The [exact countercertificate](ONE_TURN_SEPARATION_COUNTERCERTIFICATE.md) supplies a physical one-turn Monster law with an all-Princess upper

\[
 V\le W_1\le
 C=\frac{142472349375511}{100000000000003}
 =1.4247234937550672\ldots
 <U_*=\frac{291849329389899}{204800000000000}.
\]

This disproves the frozen target \(W_1>U_*\) in the [separation directive](ONE_TURN_SEPARATION_DIRECTIVE.md). The exact restricted value \(W_1\), the exact unrestricted value \(V\), and equality \(V=W_1\) remain open. The [continuum potential certificate](ONE_TURN_CONTINUUM_POTENTIAL_CERTIFICATE.md) gives the physical functional, the all-Princess reduction, and the finite rational verification theorem.

**Newer bounds (2026-11-15):** 1.4225745 ≤ V ≤ 1.4240199 from the light-cone program; see [its summary](../14-light-cone-lattice/README.md).

**Research target:** derive and prove the global transport-compatible **contact atlas**, rather than guess a finite set of trajectories and optimize their weights. No exact equilibrium, finite phase classification or unique free-boundary solution is presently established.

The game is the first-coincidence pursuit game on [-1,1], with independently hidden arbitrary initial positions and 1-Lipschitz paths. The natural object on the Princess side is a symmetric ordered time-dependent CDF F(t,x); on the Monster side it is a physical trajectory with **two surviving capture records**. Initial location, later turns, center crossings and endpoint contact all matter.

## The geometric dependency chain

1. **Admissible fields and global reductions:** [legal CDF transport](../12-global-closure/GLOBAL_CDF_TRANSPORT_LP.md), [global minimax](../12-global-closure/GLOBAL_MINIMAX_AND_CDF_DUALITY.md), [first variation](../12-global-closure/GLOBAL_CDF_VARIATIONAL_STATIONARITY.md), [incoming-front completion](../12-global-closure/GLOBAL_INCOMING_FRONT_COMPLETION.md). These concern the entire game.
2. **Physical initial interfaces:** [bulk P/S contacts](../12-global-closure/BULK_CONTACT_AND_CUSP_EQUATIONS.md), [initial inward I](../12-global-closure/INITIAL_INWARD_SHEET_CONTACT.md), [moving-front P and endpoint-return J](../12-global-closure/MOVING_FRONT_INITIAL_CONTACT.md), [boundary shadow/inward layer](../12-global-closure/BOUNDARY_LAYER_KERNEL_AND_GAP.md). Their identities are exact for named paths; completeness is not known.
3. **Initial phase geometry:** [conditional curved three-run response](../12-global-closure/CURVED_INITIAL_PHASE_RESPONSE.md), [conditional square-root endpoint interface](../12-global-closure/ENDPOINT_SQUARE_ROOT_CONTACT.md), [conditional nonalgebraic near-endpoint trace](../12-global-closure/FRONT_ONE_CONTACT_NONALGEBRAICITY.md), and [strict transport/contact obstruction](../12-global-closure/STRICT_TRANSPORT_FINITE_SUPPORT_OBSTRUCTION.md).
4. **Global continuation:** [front terminal, record gaps and Zeno obstruction](../12-global-closure/FRONT_CONTINUATION_GAPS_AND_ZENO.md), [whole-region first exit and center modulus](../12-global-closure/POSITIVE_PREFRONT_RESPONSE_AND_MODULUS.md), [center heavier-first balance](../12-global-closure/CENTER_HEAVIER_FIRST_BALANCE.md), [center record renewal](../12-global-closure/CENTER_RECORD_RENEWAL_CERTIFICATE.md), [precenter record Bellman](../12-global-closure/FINITE_RECORD_BELLMAN_LIFT.md). The **W=0 precenter exit is not a center state**. The whole-region exchange is conditional, and its unchanged inner curvature is excluded through U=41/40; matching a competitive additional phase is open.
5. **Falsification and certification:** [contact atlas](CONTACT_ATLAS.md), [proof gates](PROOF_GATES.md), [working hypotheses and decisions](WORKING_NOTE.md). The exact game bounds are held fixed as controls, not optimization targets.

## Restricted switching-time problem

The [one-interior-turn restricted game bracket](ONE_TURN_SUBGAME_BRACKET.md) now has the exact upper \(C\) above against a completely unrestricted Princess. The certified law mixes immediate endpoint sweeps with continuous start densities on endpoint-first routes and one-turn routes at six rational turn levels. Its frozen rational potential passes all HJB, interface, terminal, and initial-radius inequalities with **zero repair**. Because every route belongs to the one-turn class, the same certificate improves the unrestricted upper.

The earlier one-turn upper `1.432964907524812...` and two-turn upper `1.425178547805600...` are historical bounds, superseded for this comparison by \(C\). The reflected-start encounter lemma remains a general, sharp pathwise ingredient.

A separate [finite-bank obstruction](../../packages/interval_one_turn/opposing_finite_bank_obstruction.md) proves that reweighting the previously tested 806 reflected pairs cannot reach \(U_*\). Its exact lower applies only to that specified bank, which includes the complete `1/8` one-turn triangle. It explains a limitation of the atomic search and does not provide an all-one-turn Princess lower.

## Latest decisive results

The [physical matching normal form](../12-global-closure/SYNCHRONIZED_PRESSURE_AND_FINITE_SUPPORT.md) eliminates time displacement from matched pressure, and then reduces positive-time matches to exact antipodal encounters. It gives a finite polygonal and atomic-clock representation for any supplied finite fully matched support. The unknown support size is now an explicit remaining gate; it is not bounded by the state dimension or by compactness.

The [front-one projection counterexample](../12-global-closure/FRONT_ONE_PROJECTION_SECURITY_LOSS.md) rules out a universal security-preserving projection, including for some bounded-density laws. The [compensated curvature theorem](../12-global-closure/COMPENSATED_CURVATURE_AND_CUSP_RESPONSE.md) proves finite global response for the particular atom-free power cusp and excludes extending its broadened inner class through U=21/16. Neither result supplies an equilibrium phase cover.

## Key structural constraints

- At smooth interior points legal ordered CDF transport requires F_x≥|F_t|; the globally admissible description also includes monotonicity, symmetry, correct endpoint traces/atoms and sticky/endward completion.
- Finite initial Princess support **cannot attain the unrestricted value**. Search for an infinite-support continuous CDF, perhaps nonalgebraic, or a uniformly certified approximating family.
- Do not infer that a finite active contact list is sufficient. The current physical attack with negative start a=-7/8 and later turn b=67/64 defeats simplistic positive-start/early-turn models.
- A phase theorem requiring curvature, record slack or a common equal-cost trace must prove those assumptions for its candidate. A central continuity modulus replaces the earlier density cap. Transport alone supplies no positive record gap.
- A [global free-start infinite-turn example](../12-global-closure/GLOBAL_FREE_START_ZENO_COUNTEREXAMPLE.md) rules out a universal finite-turn response theorem. Its center atom and low security leave a suitable equilibrium class possible.
- A global analytic characterization may use functional equations or variational inequalities; an elementary closed form is unnecessary. However a closed system **without proven equivalence to the unrestricted game** is still an ansatz.

The current certified interval is **1.4222581340234375 ≤ V ≤ 1.4247234937550672...**, with the exact upper \(C\) displayed above. The [historical frozen upper](../12-global-closure/NORMALIZED_GLOBAL_BOUND_CERTIFICATES.md) remains the benchmark \(U_*\) for the now-closed comparison; the inherited lower remains valid. See the [countercertificate](ONE_TURN_SEPARATION_COUNTERCERTIFICATE.md) and [independent checks](../../REPRODUCE.md) for current scope and reproduction.

## Workflow

Formulate a geometric conjecture with its exact physical tests, prove or falsify a phase boundary, and only then consider computation to distinguish models. Record the result in [WORKING_NOTE.md](WORKING_NOTE.md), with a link to full mathematical arguments under the core research index. The dedicated [geometry regression workflow](../../.github/workflows/geometry-structural-checks.yml) audits exact *fixtures*, not universal statements; the old discovery jobs require explicit manual dispatch.

