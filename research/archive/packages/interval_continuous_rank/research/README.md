# Bounded three-piece structural test

`continuous_candidate.py` preserves a four-round local fitting experiment.
It fits three affine pieces in rank, with fixed knots `[0,.35,.75,1]`, to
the archived 169 positive princess paths, then varies the ordered a,u,C
knot values and an endpoint-pair mass. All tested payoffs use the continuous
rank engine in the parent directory.

The response searches include ordinary endpoint sweeps, up to three
interior turns, center waits, and one or two zero-return triangles. These
are actual admissible monster paths, but the floating optimization of their
parameters is not exhaustive. The initial finite constraint set included
only the inward-first half of the usual M2 family; later responses exposed
the omitted outward-first branch. The final two local princess optimizations
also did not converge fully. The output is therefore **not a lower bound,
an upper bound, a saddle point, or evidence excluding all three-leg laws**.

The test did not identify a stable candidate. Its final local law formed a
large genuine center atom before time one, and its strongest discovered
attack simplified to an ordinary outward-first M2 route. This was useful
for diagnosing the inadequacy of the initial constraints, but gives no
reason to increase the number of affine pieces. The experiment stops after
four rounds; its historical JSON and log are retained for reproducibility.

Run with NumPy and SciPy available. The script reconstructs its fit inputs
from the existing `princess_strategy.json`; it does not use an external
array cache. Running it overwrites the local experiment JSON and log only
if standard output is explicitly redirected to the latter.

## Fixed late-wave five-leg tests

`five_leg_fixed_wave.py` and `five_leg_negative_branch.py` preserve two
subsequent bounded tests with the same four rank knots and
`A2(q)=1.001+0.000001q`. The first uses two seeds and three exchange
rounds; the second uses one negative-outer-C1 seed and a 100-iteration cap.
Both include signed M1/M2 starts and the specified F/L/Q attackers. The
second additionally includes explicit moving two-turn attacks and searches
on the incoming-characteristic boundary faces.

Neither test found a stable candidate. The local optimizers reached their
iteration caps, so their sampled objectives are not certificates. The first
test's generic floating monster search also missed a thin but decisive
two-turn family; its exact geometry was derived afterward. The negative-C1
seed escapes that first-wave attack, but a corresponding last-wave attack
with `s=sup A2` defeats its final fitted law. Both formulas and their exact
capture proofs are in `FIRST_WAVE_TWO_TURN_RESPONSE.md` and
`LAST_WAVE_TWO_TURN_RESPONSE.md` under `research/09-equilibrium-structure/`.

The negative-branch JSON also includes explicit F/L/Q probes at the fixed
late-wave boundary values and their midpoint. These expose the steep
dependence inside that fixed strip; they do not change epsilon or refine
the candidate's rank partition. The historical logs and JSON contain the
actual stopping status and all discovered routes. Their purpose is to
preserve structural failures, not to report a new interval for the game.
