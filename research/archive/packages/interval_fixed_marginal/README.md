# Fixed physical law: clock refinement and a quadrature obstruction

This package isolates a different physical Monster law from the first CI
discovery campaign. It optimizes the causal clocks used to certify that law,
while preserving **every physical path and its exact rational probability**.
The new law has 676 reflected physical path pairs. It is a search seed, not
the best retained global upper bound.

## What is certified

The seed came from the last completed checkpoint of `princess-plain` in
[run 43532597339](https://github.com/vltanh/lean4-monster-princess/actions/runs/43532597339).
The source job later failed on the old cumulative HiGHS timer. Its floating
objective is not a certificate. A fresh exact sparse Qout replay establishes
the following facts independently of that job's status:

| Quantity | Exact value | Approximation |
| --- | --- | --- |
| Seed all-Princess upper | `729770894042503/512000000000000` | 1.425333777426764 |
| Actual endpoint-loop response supremum lower for this fixed law | `364744584499177/256000000000000` | 1.424783533199910 |
| All-calendar **n128 Qout certificate-family** lower | `45606479434184872583171/32000000000000000000000` | 1.425202482318277 |
| Actual continuous payoff of that blocking field against this law | a rigorous rational interval in `blocking_field_report.json` | 1.424183121174385 |

The third row prevents **any** choice of n128 nodal causal calendars, including
unlisted calendars, from certifying this fixed law below the then-current
global upper `291849329389899/204800000000000`. It does not exclude the actual
physical law. The fourth row shows why: about 0.00101936 of that obstruction
comes from the left-rectangle clock quadrature. Refining the clock grid can
therefore matter even though the physical paths are unchanged.

None of the last three rows is a lower bound for the unrestricted game.
The first row is an unrestricted game upper, but it is weaker than the
retained global upper. No equilibrium or unrestricted saddle is claimed.

## Reproduce the exact checks

From the repository root:

```sh
python packages/interval_fixed_marginal/verify_seed.py
python packages/interval_fixed_marginal/verify_obstruction.py
python packages/interval_fixed_marginal/test_search.py
```

`verify_seed.py` checks the compressed and uncompressed seed hashes, decodes
the compact physical marginals, independently checks 4,056 chronological
endpoint-loop contacts, and reruns the exact sparse Node certificate verifier.
The seed contains all 947 causal calendars and a maximum-flow/minimum-cut
witness. Source run, head, random seed, and checkpoint hash are recorded in
`seed_manifest.json`.

`verify_obstruction.py` uses only Python integer arithmetic. It verifies every
Qout order inequality of the blocking field and minimizes the causal clocks
for every physical route by taking running prefix minima. Every admissible
calendar charges at least elapsed time to the past, so this prefix-minimum
formula is the minimum over all causal calendars, not just the search bank.
Evaluating any candidate clock certificate on this one feasible Qout field
then proves the stated family lower bound.

The same script integrates the actual full-width common-threshold field
along every physical route. Each lattice edge is an affine field segment.
If its survival values are `a,b` and the preceding record is `M <= a`, the
unit-interval integral is `M` when `b >= M`, and otherwise
`M - (M-b)^2/(2*(a-b))`. Exact integer division gives an outward-rounded
rational enclosure. Actual initial endpoint capture gives an empty clock;
the interior endpoint trace is used only before first arrival. Thus endpoint
atoms are not replaced by limiting traces. The analytic interpolation and
clock interpretations remain manuscript arguments, not Lean formalizations.

## Discovery

The driver uses one LP equality for each physical pair and a variable for
each admitted causal calendar. Its probability LP has only the observed
Qout-cut rows. An exact integer sparse closure oracle separates every
proposal. Every physical route is repriced under the dual field to discover
new causal calendars before each expensive closure query. Only strict
calendar improvements are admitted. Largest-remainder rationalization is performed
separately within each physical group, retaining its exact numerator.

Example of a refined clock search:

```sh
python -u packages/interval_fixed_marginal/search.py \
  --native-flow --n 256 --iterations 100 --seconds 1200 --lp-seconds 60 \
  --price-every 3 --alternative-cuts 4 --level-fraction 0.8 \
  --seed 223606 --output results/fixed-plain-256
```

`--n` must be an integer multiple of the source grid. Refinement repeats
physical unit steps and scales clock times; it does not round or move the
physical paths. Use `--n 512` for a separate finer-clock experiment. Resume
with the same grid and input:

```sh
python -u packages/interval_fixed_marginal/search.py \
  --native-flow --n 256 --iterations 100 --seconds 1200 --lp-seconds 60 \
  --price-every 3 --alternative-cuts 4 --level-fraction 0.8 \
  --seed 223606 --output results/fixed-plain-256 \
  --resume results/fixed-plain-256/checkpoint.json
```

Outputs include exact seed and best certificates, independent replay results,
all physical marginals, a reusable calendar checkpoint, a hashed cut archive,
source hashes, parameters and seeds, and iteration logs. The restricted LP
objective is exploratory. A `BUDGET_STOPPED` result preserves the best
completed exact certificate and does not assert optimization convergence.
An exact all-calendar family floor at or above `--target-upper` stops that
grid and saves `blocking.field.json.gz` and `blocking.report.json`. Replay
the obstruction, including a separate actual continuous-payoff diagnostic,
with `python packages/interval_fixed_marginal/verify_obstruction.py
--result-directory results/fixed-plain-256`.

A local n128 pilot completed 15 iterations in about 183 seconds and improved
this seed's certified upper to `364863178953333/256000000000000`
(1.425246793067707). This remained above the retained global upper, and the
all-calendar obstruction above explains why merely continuing that same
grid family cannot reach a new global result. The next experiment should
refine clocks or change physical probabilities/geometry.

For an accepted candidate, independently replay its exact physical law on the
full Qout graph without rerounding its probabilities:

```sh
node packages/interval_mixture_cut/dense_replay.cjs \
  results/fixed-plain-256/best.sparse.json \
  results/fixed-plain-256/best.dense
```
