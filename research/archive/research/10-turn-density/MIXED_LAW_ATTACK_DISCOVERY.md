# Mixed-law attack discovery

This is a reproducible counterexample search for the frozen round-41 ordered marginal mixture, not a lower certificate or a new value bound. The input field is blob `5c45d042ee9948faebc03354c3e1e2ee3cbec1a5`; the physical mixture is blob `aca3c181205ea4b5fb676e45ab2d9956f3b8173e`. The actual law is obtained by quantile ordering the mixed marginals. Its score must not be replaced by an average of component capture costs.

## Discovery and validation

The script samples 48 radial quantiles at 257 times, forms a legal piecewise linear interpolant, and runs the capture-order search on its 96 reflected paths. This finite search exhausted 591,483 states. It supplies candidate monster curves only. Every reported attack is instead scored on the complete continuous-plus-finite law by `mixed_cdf_payoff.mjs`, using exact rational first-contact traces and affine survival integrals.

A naive floating implementation misclassified the shared epsilon capture layers by as much as 0.000735. The replacement discovery evaluator keeps finite-path contacts exact while evaluating only the continuous field in floating arithmetic. Its five benchmark errors are at most 9.16e-12. That hybrid evaluator is still not the final proof.

## Exact counterexamples

| Route | Ordered mixed score | Continuous component alone |
|---|---:|---:|
| Late negative M2, reflected | 1.4224439541715264 | 1.4236839844663458 |
| Center wait, then two excursions | 1.4230983662178944 | 1.423552839230389 |
| Five interior turns, all unit legs | 1.4233615819193206 | 1.4238169341464137 |

The complete rational vertices and exact score fractions are in the snapshot. The first route starts at 434153572919/500000000000, moves left to its first turn with reflected characteristic 6457057227/6250000000, then sweeps both endpoints. Exact perturbations of that characteristic by plus or minus 1e-6 and 1e-9 retain the attack. It therefore persists over an interval and is not merely an isolated first-contact jump.

The waiting curve starts at zero, waits until 3/20, then visits (69/160,9/32), (2197/2560,-373/2560), (513/256,1), and (1025/256,-1). Replacing its waiting prefix by a single straight incoming leg is more expensive; one cannot keep its old cost after that replacement. A valid unit-leg approximation instead starts with the three vertices (1/40,-1/40), (3/40,1/40), and (1/8,-1/40), then follows the same remaining curve. This is the five-interior-turn counterexample in the table. More small alternating excursions approach the waiting score, but the three-lobe realization already suffices as a concrete physical atom below the round-41 finite master.

Both principal attacks cost more on the continuous component alone. The new finite response-face mass therefore causes the failures. This does not exclude a better continuous interpolation of that face or prove anything about the unrestricted optimum.

## Reproduction

Run from the repository after saving the input mixture JSON:

```sh
node packages/interval_cdf_discovery/discover_mixed_response.mjs \
  packages/interval_cdf_discovery/snapshots/endpoint_joint_i1_field.json \
  packages/interval_cdf_discovery/snapshots/mixed_cdf_round41.json --search
```

Without `--search`, the script evaluates the three fixed rational witnesses. The exact scoring engine is a separate dependency. During recovery, the computational bodies and every reported score were executed in V8; the reconstructed Node file and CLI wrapper were not run because the executor was unavailable.
