# Finite-law response engine and exact seed face

This package computes the unrestricted princess response to a supplied finite symmetric law of unit-speed monster routes on `[-1,1]`. The frozen certificate reproduces the existing 67-pair law exactly:

```text
36563170811 / 25600000000
```

It also preserves that law's complete finite event residual face. This is an exact response certificate for the supplied law. The unrestricted interval-game equilibrium remains open.

## Files and replay

- `atomic_survival_v8.cjs` is a dependency-free CommonJS module.
- `atomic_seed_integer_certificate.json` contains the exact geometry, masses, sparse feasible flow, matching cut, and residual SCC data.
- `verify_atomic_seed_integer.cjs` is the independent replay audit.
- `ATOMIC_SURVIVAL_RESPONSE.md` gives the event/lexicographic reduction.

With a Node runtime, a minimal replay is:

```js
const fs = require("node:fs");
const E = require("./atomic_survival_v8.cjs");
const certificate = JSON.parse(
  fs.readFileSync("./atomic_seed_integer_certificate.json", "utf8")
);
const model = new E.Rational.Model(certificate.atoms);
const result = E.Integer.verifyIntegerFlow(
  E.Cut,
  E.Physical,
  E.BigFlow.BigFlow,
  model,
  certificate.atoms.map(a => a.weight_numerator),
  certificate.weight_denominator,
  certificate.flow_certificate
);
console.log(result);
```

The replay builds the capacities and checks the supplied flow. It does not rerun the 171 augmentation phases. Keep the atom order unchanged: sparse flow edge identifiers refer to the deterministic insertion order of the compiled network.

The module also works in a pure V8 isolate by evaluating its CommonJS source with an object `{exports: {}}` supplied as `module`. It needs no filesystem, network, WebAssembly, or third-party package.

## Exact input convention

An atom has `exact_light`, an array of vertices `[U,V]`. Each coordinate is an integer or rational string. Physical coordinates are

```text
t = (U + V) / 2
x = (U - V) / 2.
```

Routes start at time zero, remain in the physical strip, have positive horizontal or vertical light-coordinate legs, and finish after visiting both endpoints. The route and its reflection `(U,V) -> (V,U)` each receive half the atom's probability. The engine validates unit legs and physical vertices; callers must also retain the time-zero and completed-sweep input convention.

The frozen data contains 465 routes because zero-mass routes supply additional event coordinates. Exactly 67 pairs have positive mass, and their integer numerators sum to `1000000000`. The positive law is exactly the archived strategy in `packages/interval_refined_upper/strategy.json`. Extra zero-mass events change the representation of the response face, not the law.

All capture predicates in `Rational` use exact rational comparisons. Endpoint normalization is therefore performed before compiling any contact chamber. This avoids treating a rounded endpoint or coincident turn as a distinct physical event.

## What the response reduction covers

The response theorem first folds arbitrary signed princess paths into nonnegative paths for a symmetric monster law. A dense strict-interior, strict-speed class then has one shared monotone light-coordinate inverse `U=P(V)`. The time-zero crossing of that graph is free; there is no prescribed initial position, number of turns, first-crossing characteristic, or absorption-by-two condition.

At a fixed monster vertex, survival above or below the route is a conjunction of strict threshold tests. Horizontal survival lengths are ramp rewards. Lowering the unpriced parts of `P` maximizes the relevant vertical survival integrals. The resulting finite event problem has positive conjunction rewards and order implications, so maximum closure gives the response supremum.

Labels are lexicographic: `(base,-)`, `(base,0)`, and `(base,+)`. Lengths use the rational base; contact predicates retain the side. Physical boundary labels are restricted explicitly. The realization theorem uses ordered small perturbations and connectors, rather than assigning independent first and last values at the same query.

The exact residual face is a face of these limiting controls. It is not, by itself, an attained lower strategy. A proposed lower law still needs a joint legal realization and an unrestricted monster check. Shared characteristic atoms in a finite common-epsilon mixture have already produced genuine attacking routes; continuous freedom inside unpriced intervals must be retained.

## The frozen integer certificate

For the seed law, all capacities were scaled to integers. The common geometric denominator is `10000000000000000`, and the probability denominator is `1000000000`.

The saved network has:

| Quantity | Count |
|---|---:|
| Nodes, including source and sink | 80,892 |
| Directed capacity arcs | 176,922 |
| Nonzero supplied edge flows | 38,427 |
| Distinct stored flow values | 7,406 |
| Free residual SCCs | 10,125 |
| SCC condensation edges | 19,729 |

The exact flow is

```text
19296189851562500000000000.
```

The supplied cut has exactly the same capacity. The engine's replay checks nonnegative flow, every capacity bound, conservation at every internal node, source and sink balances, and cut equality. Both extremal response rows independently have exact expected capture time `36563170811/25600000000`.

The parent audit separately checked all 465 physical routes, exact agreement of the positive law with the archived 67-pair strategy, source reachability in the reconstructed residual graph, and all SCC and condensation-edge data. No Lean compilation or CI was used.

## Exported APIs and numerical scope

The module exports:

| API | Role |
|---|---|
| `Rational.Model`, `pack`, `restore` | Exact geometry and capture predicates |
| `Rational.sparseSolve` | Full response using only positive-mass atoms, then evaluation on the whole pool |
| `Cut.Flow` | Numerical maximum flow |
| `BigFlow.BigFlow` | Integer maximum flow |
| `Integer.solveIntegerLaw` | Exact integer law response and sparse witness |
| `Integer.verifyIntegerFlow` | Capacity/conservation/cut replay without augmentation |
| `FaceOpt.compress`, `optimize` | Residual SCC face and secondary nonnegative-law optimization |
| `Exact` | Reduced-basis Bareiss and exact primal/dual master repair |
| `Physical.Q`, `realize`, `capture` | Rational legal-path construction and direct capture checks |

The legacy floating geometry helpers and the absorption-by-two diagnostic remain exported separately. Prefer `Rational` for new work.

General discovery runs use numerical cut capacities. Their response controls and geometry are exact in their comparisons, but a numerical max-flow result is not automatically an integer certificate. Likewise, `Exact` certifies the exact dyadic matrix represented by the Float64 payoff entries supplied to it. It does not silently turn those entries into unrounded physical probabilities or costs.

The discovery master retains the full continuous CDF strategy as one named response component. Its dual coefficient must not be mistaken for a single pure princess path. The physical mixed-law evaluator and the ordered mixed-CDF evaluator are separate checks.

## Checks retained with the implementation

The integer flow routine passed 60 independent exhaustive small-network comparisons. Reduced-basis repair passed 60 small packing-game checks with exact primal and dual inequalities. Residual-face projection was compared with all 27,993 feasible label assignments in three small laws. The full normalized seed law then passed the exact flow/cut replay and the independent physical-law comparison above.

These checks support the response engine and the frozen seed certificate. They do not assert a new game value or a matching unrestricted equilibrium.
