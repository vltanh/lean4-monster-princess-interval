# Exact scoring of the ordered continuous/finite mixture

## What is scored

The input is a specified affine radial CDF, its mixture mass lambda, and a
finite rational polygonal radial law with fair reflections. The scorer forms
the full signed marginal CDF

    F = lambda F_continuous + (1-lambda) F_finite

and uses its ordered quantile coupling. It does **not** average the components'
capture-time payoffs. The latter is the raw mixture, which can be weaker.

The implementation reuses the exact field geometry and trace conventions of
exact_response_audit.mjs and the rational path primitives of
finite_quantile_response.mjs. The current continuous component is the complete
endpoint_joint_i1_field.json, Git blob
5c45d042ee9948faebc03354c3e1e2ee3cbec1a5.

For any supplied admissible polygonal monster, the result is its exact expected
capture time if complete=true. Otherwise it is the prefix survival integral
with explicit remaining lower/upper records. No finite-quantile or sampled
response search is a lower certificate for the continuous component.

## Integration and atoms

Split a monster leg at the center, every intersected affine-field triangle
edge, finite-path vertices, and actual finite-path contacts. On each open
subinterval both signed CDF traces are affine. Values at its one-third and
two-third points recover the two endpoint limits exactly; an additional
midpoint check detects a missed affine boundary.

Let l,h be the preceding running lower and upper records. Apply strict/closed
CDF updates at the interval's left endpoint and its right limit. If the open
interval traces are f_minus and f_plus, its survival integral is

    length*(1-h+l)
      - integral (f_plus-h)_+
      - integral (l-f_minus)_+.

Each hinge integral is the exact area of a trapezoid or triangle. Update the
records at the right limits and then at the actual endpoint, including
center/endpoint atoms. Instantaneous capture contributes no elapsed time.

This formula works because each trace is affine on the interval. After the
left-limit record update, an increasing trace can only establish upper
records and a decreasing trace can only establish lower records. On a unit
right leg the closed trace is nondecreasing; on a unit left leg the strict
trace is nonincreasing.

The implementation also supports waits and subunit polygonal legs by the same
affine-interval calculation. All predicates and areas use BigInt fractions.

## Independent positive-M1 moment check

For an interior start a without an initial atom, put s=2-a and
A=Pr(p(0)<=a). With the full radial marginal field R, including the finite
component after time two, the capture partition gives

    4 C_f(a) = 8-4a+2s A-I-F-H,
    I = integral_a^s R_closed(U,-a) dU,
    F = integral_-a^s (A-R_strict(s,V))_+ dV,
    H = integral_s^(s+2) R_closed(U,s) dU.

The alpha row is strict and beta columns are closed. The H term is retained:
the strict epsilon paths finish inside the endpoints, so endpoint-by-two
cannot be silently assumed for their component. This independent first-
inverse calculation agrees exactly with the record integral at a=3/5.

## Round-41 diagnosis

The interim payload is Git blob
aca3c181205ea4b5fb676e45ab2d9956f3b8173e. It assigns exact mass approximately
.9966708386047582 to the continuous field and the remaining mass to 32 actual
epsilon paths and their reflections.

The positive M1 route

    (0,3/5), (2/5,1), (12/5,-1)

has exact ordered-mixture payoff approximately 1.4233830592878158. It is
strictly below the rational number 7117/5000=1.4234, and below the reported
interim finite-master objective 1.4234295428517187.

For comparison on this same route:

| Coupling | Payoff, display only |
|---|---:|
| Raw mixture | 1.4233817786868812 |
| Mixture of separately ordered components | 1.4233830223123949 |
| Full ordered marginal mixture | 1.4233830592878158 |

The inequalities hold exactly. The continuous component alone costs
5040505530693409424763651796467/3541254481809244160000000000000.

Several other old attacks are repaired by this mixture; their full exact
scores are preserved in the report. This diagnoses an off-support response
of a particular interim candidate, not the game's value or failure of every
law in an upper optimal face.

## Checks and reproduction

Executed in pure V8:

* 64 pure-finite cases agree with the independent discrete record evaluator.
* 28 pure-field M1/M2 routes agree with the previous unitRoutePayoff evaluator.
* The round-41 M1 score agrees with the independent first-inverse moment.
* Exact mixture-concavity inequalities and the threshold 7117/5000 pass.

The Node wrappers were not executed during the executor outage.

    node packages/interval_cdf_discovery/verify_mixed_cdf_payoff.mjs MIXTURE.json
    node packages/interval_cdf_discovery/mixed_cdf_payoff.mjs FIELD.json MIXTURE.json ROUTE.json

The reproduction inputs must be the identified complete field and the
physical mixed-law payload, not only the dyadic payoff matrix.
