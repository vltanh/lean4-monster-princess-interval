# CDF shape discovery and a certified smoothing counterexample

This package asks whether the temporal oscillations in numerically optimized
Princess CDFs are necessary. It contains a successful finite-bank
regularization experiment, a separate **global counterexample to one naive
smoothing attempt**, and a short CI workflow that searches for new shapes.
It does not prove a finite equilibrium-sufficient phase classification.

The comparison game lower used here is

\[
L=\frac{582291421641}{409600000000}
=1.42160991611572265625.
\]

The shape experiments below do not improve that bound. See
[the authoritative handoff](../../HANDOFF.md) for the current whole-game status.

## The optimization problem and acceptance gate

Write \(g(t,r)=2F(t,r)-1\) on the positive half interval. A coarse profile with
grid parameter \(m\) has nodal variables \(g_{j,k}\), with \(j+k\) even,
\(t=j/(2m)\), and \(r=k/(2m)\). The default objective is the exact discrete
functional

\[
\mathcal T(g)=\frac1{2m}\sum_k\sum_j
|g_{j+2,k}-g_{j,k}|.
\]

The `curvature` objective instead sums
\(\lvert g_{j+4,k}-2g_{j+2,k}+g_{j,k}\rvert/(2m)\).
These are nodal functionals, not a proved continuous equilibrium energy.

The LP retains the cone transport inequalities and sticky endpoint
constraints. Every discovered physical causal calendar gives a linear
security inequality at a fixed rational floor. Cached paths find additional
violations cheaply. Clearing that cache is insufficient: a candidate is
accepted only after the **complete integer physical-bank oracle** verifies
its repaired profile at the requested floor. Floating optimality of the
variation objective is never promoted to an exact theorem.

The `--fixed-initial` variant fixes all initial nodal values. Exact integer
upper and lower constraints are propagated through the order graph before
repair, preventing a rounding error from changing these values.

## An accepted simplification

The original source was discovered in actual Actions run
[43532597339](https://github.com/vltanh/lean4-monster-princess/actions/runs/43532597339),
artifact `discovery-princess-proximal`. Its n=64/profile32 candidate has SHA-256
`00d9fe3974395829b1ce85bdb94b788b499a36b54e75d355daa86cc7c319469a`.

At profile32/bank64, a fully separated fixed-initial regularization gave:

| Quantity | Original CI field | Regularized field |
|---|---:|---:|
| Discrete temporal variation | 1.505730642609375 | 1.434103325859375 |
| Discrete temporal curvature | 1.60579751425 | 1.484449780453125 |
| Nodal temporal direction changes | 181 | 86 |
| Tight-order equality components | 378 | 408 |
| Certified finite-bank floor | 1.4243494815625 | 1.42433951333984375 |

The temporal variation falls by about **4.76%**, and 95 of the 181 nodal
direction changes disappear while the initial nodal distribution stays
exactly unchanged. These direction changes count the signs of successive
time differences at fixed radii; they are **not** counts of turns in an
individual Princess trajectory.

The admitted bank allowance was exactly \(1/100000\). The accepted field's
complete native minimum is

\[
\frac{72926183083}{51200000000}.
\]

An independent BigInt target replay passed. Further complete n=256 native
pricing of the same full-width profile gave the transferred game-value lower
\(145439300377/102400000000=1.420305667744140625\). This is slightly above the
corresponding unsmoothed n=256 result, but below the current game lower stated
at the top of this note. Neither transfer is a same-CDF continuum security
claim; explicit-law extraction is a separate construction.

The frozen `regularized_seed_field.json` and
`regularized_response_bank.json.gz` total about 131 KB. The latter contains
causal physical calendar constraints, not Monster mixture weights.
`regularization_checkpoint.json` binds their hashes and records the exact
metrics and source provenance. It also records the optimizer's repaired
starting profile separately: numerical import changes a few later-time
probability values, shifting the variation and curvature by exactly
\(1/32000000000\). Every initial value agrees exactly with the original CI
field. The table above uses the original CI field's metrics.

This result shows that part of the apparent oscillation is optional. It does
not bound the number of equilibrium phases: the tight-order component count
actually increases.

## A naive smoother is globally suboptimal

An earlier TV candidate reduced the discrete variation to
1.431821450625 and cleared the then-cached 1,238 physical response paths.
Complete pricing found a missing physical attack. The rejected field and its
attacker are retained as `naive_tv_rejected.dual.json.gz` and
`naive_tv_attack.json`.

Use the full-width common-threshold interpolated CDF defined by that field.
The Monster follows the unit-speed path through these vertices:

| Time | Position |
|---:|---:|
| 0 | 1/32 |
| 13/64 | 15/64 |
| 23/32 | −9/32 |
| 2 | 1 |
| 4 | −1 |

For this particular Princess law, the path gives

\[
\mathbb E[T]\le
\frac{726854769333}{512000000000}
=1.419638221353515625
< L.
\]

The exact gap below the known game lower is
\(4038030873/2048000000000\), about 0.00197169.

The certificate is a direct causal upper, not an assertion that the
finite-bank oracle evaluated every continuous response. At the physical
path's grid vertices, full-width interpolation fixes the light coordinates,
so its CDF values equal the stored nodal values. For each surviving side,
keep the running minimum of these samples and sum left rectangles until the
corresponding endpoint is reached. Continuous survival is at most those
running records. Thus the rectangle sum bounds the actual capture
expectation from above. Endpoint clocks stop at their first endpoint hits;
capture at time zero is included.

`verify_shape_attack.py` independently checks 98,304 cone inequalities, all
512 sampled CDF values through the rational JavaScript interpolator, physical
legality, and the complete rectangle sum with Python `Fraction` arithmetic.
The saved replay is `naive_tv_attack_replay.json`. The unit regression also
checks an endpoint-start path whose exact payoff is one, exercising capture
at time zero.

This excludes **that smoother**, not all low-variation fields. The later
accepted regularization demonstrates why those two claims must be kept
separate.

## Reproduction and CI discovery

```bash
python packages/interval_cdf_shape/test_shape_search.py
python packages/interval_cdf_shape/verify_shape_attack.py \
  packages/interval_cdf_shape/naive_tv_rejected.dual.json.gz \
  packages/interval_cdf_shape/naive_tv_attack.json
node packages/interval_clock_grid/normalized_record_pricing.cjs \
  packages/interval_cdf_shape/regularized_seed_field.json --target-bound
```

New optimization from the compact seed, with an additional declared allowance:

```bash
python packages/interval_cdf_shape/shape_search.py \
  --seed-field packages/interval_cdf_shape/regularized_seed_field.json \
  --response-checkpoint packages/interval_cdf_shape/regularized_response_bank.json.gz \
  --n 64 --profile-grid 32 --fixed-initial --objective variation \
  --loss 1/100000 --seconds 300 --iterations 100 --output results/shape
python packages/interval_cdf_shape/certify_shape.py results/shape \
  --refine 256 --refine-seconds 240
```

The separate `.github/workflows/shape-discovery.yml` starts three independent
new searches: fixed-initial variation, free-initial curvature, and
fixed-initial variation using the currently retained stronger n=256 geometry.
The first two verify the original observed CI artifact hashes and then
optimize from the compact regularized seed. The current-geometry family
generates valid causal calendars from the retained physical Monster law.

Each family has 300 seconds for optimization and, after acceptance, at most
240 seconds for n=256 native pricing. Coarse acceptance must pass an
independent BigInt replay. A prospective new global improvement from fine
pricing is flagged for independent high-resolution replay; this workflow
does not silently promote it. A budget stop preserving only the starting
field is explicitly reported as `NO_NEW_ACCEPTED_SHAPE`. Artifacts include
rejected fields and physical attacks, candidates, exact fractions, hashes,
solver logs, and resumable calendar constraints.

The actual [shape discovery run 43535423731](https://github.com/vltanh/lean4-monster-princess/actions/runs/43535423731)
completed all four jobs successfully, including the exact regression job.
All three new searches nevertheless reported `NO_NEW_ACCEPTED_SHAPE`:
current-field variation and free curvature stopped at an LP time limit;
fixed variation stopped with an inconclusive solver status after an exact
response rejected a trial. No further shape or game-bound improvement is
claimed. The earlier successful regularization and the global smoothing
counterexample were independently replayed in that run. The next structural
target is the coupled transport and rank-balance system described in the
handoff, rather than larger budgets for the same objective.
