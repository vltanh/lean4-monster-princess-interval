# Continuum response and certificate work

The unrestricted exact value remains **open**. These notes supply exact
response formulas, verified exclusions of overly narrow strategy families,
and sufficient certificate conditions. They do not supply a matching saddle
pair.

| Note | Established result | What is still needed |
| --- | --- | --- |
| [Characteristic response](CHARACTERISTIC_RESPONSE.md) | Exact M1/M2 capture formulas and a separable monotone-path functional, including atoms and the end of a characteristic plateau | A candidate measure and a global optimization of its response |
| [M1/M2 control](M1_M2_CONTROL.md) | A two-dimensional potential test sufficient for an unrestricted princess upper guarantee | Explicit measures and potentials attaining the desired constant |
| [Wait-in-out counterexample](WAIT_IN_OUT_COUNTEREXAMPLE.md) | A complete rational exclusion of the three-parameter wait/inward/outward response family for arbitrary M1/M2 mixtures | Any proposed simpler response family needs additional candidate-specific hypotheses |
| [Missing post-transition inward leg](POST_SWEEPER_DETOUR.md) | An exact gain formula for adding another inward leg after crossing `U=1`; the proposed continuum family omits it | Including the leg does not by itself prove an exhaustive response family |
| [Refined exact upper bound](REFINED_UPPER_BOUND.md) | A rational 134-path strategy gives `V <= 36563170811/25600000000`, certified in all 27 full-interval starting chambers | A matching unrestricted lower guarantee |
| [Conditional response reduction](CONDITIONAL_RESPONSE_REDUCTION.md) | All princess responses to a specified monotone-density class reduce to a four-parameter supremum, with boundaries included | An optimal law satisfying the hypotheses and an exact optimization of that supremum |
| [Corrected density equations](CANDIDATE_DENSITIES.md) | Exact payoff derivatives, negative-transition detour cost, and a conditional local ODE | Global support boundaries, normalization, response inequalities, and a valid lower strategy |
| [Central concentration obstruction](CENTRAL_CONCENTRATION.md) | A two-marginal sweep inequality excludes the corrected rational 124-path candidate, including its ordered rearrangement | A lower family that avoids this explicit unrestricted response |
| [Quantiles, continuation, and lower certificates](QUANTILE_AND_TAIL.md) | Exact fixed-monster-start continuation value 2, uniform finite-support approximation, and Bellman tests for truncated or full-payoff lower guarantees | An explicit princess law and potential matching an unrestricted upper guarantee |

The two unrestricted inequalities still have to meet at the **same** exact
constant. Neither the number of local control velocities in a Bellman test
nor the two characteristic coordinates constitute a finite enumeration of
all equilibria.

Bounded discovery programs and logs are preserved separately in
`packages/interval_continuum_discovery/`. In particular, the sampled value
near 1.42804 is not a game value or a lower certificate; its sampled
princess law is excluded by the concentration theorem.

The preceding [structural audit](../07-structural-audit/) explains why the
finite-response calculations are valid and why no universal turn or time
cutoff follows from symmetry and ordering alone.
