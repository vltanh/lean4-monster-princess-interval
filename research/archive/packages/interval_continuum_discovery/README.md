# Bounded continuum discovery experiments

These scripts and saved outputs preserve the numerical investigation that
led to the exact results in `research/08-continuum/`. **None of the floating
objectives in this directory is a certificate for the unrestricted game.**
The exact verifiers live in the separate packages named below.

The scripts use NumPy, SciPy, and Numba, plus existing exploratory modules
in this repository. They were run with NumPy 2.3.5, SciPy 1.17.0, Numba
0.68.1, and llvmlite 0.50.0. They are optional discovery tools; these
dependencies are unnecessary for the new exact verifiers. Paths have been
made relative to the repository so that the saved work is portable.

## Completed and stopped investigations

| Files | Experiment and outcome | Mathematical scope |
| --- | --- | --- |
| `direct_support.py`, `direct_support_4.*` | Direct flow LP over all quarter-grid two-turn monster paths; floating objective approximately 1.43827318 | A finite monster-support search; no unrestricted equilibrium |
| `direct_support_8.log` | Eighth-grid version built a 636,730-variable LP and was deliberately interrupted before an answer | **Incomplete; no value or certificate** |
| `near_sweeper_support.py`, `near_sweeper_8.*` | Added nearby first-turn characteristics to the eighth-grid M1/M2 support; the floating optimum stayed at approximately 1.432522325 | Did not improve the already solved original support; no exclusion of all nearby continuum turns |
| `center_return_support.py`, `center_return_8.*` | Added paths returning to the center before their next sweep; extra paths received zero weight in this sampled LP | A sampled family check only |
| `full_two_turn.py`, `full_two_turn_4.*` | Cut-generation version stopped at its 160-iteration cap with a large response gap | **Not converged; its restricted objective is not a game bound** |
| `full_half_network.py`, `full_half_network_16.*` | Optimized a half-interval hider-flow network against M1/M2 samples | The resulting hider law was defeated by an omitted monster |
| `full_half_separate.py`, `full_half_separation_16.*` | Added unrestricted monster responses for a fixed limit of 24 iterations | Persistent support changes; no equilibrium or closure |
| `central_wait_candidate.py`, `central_wait_candidate_32*` | Sampled the initial-outward / inward / central-wait / outward princess family | Omits the exact improving inward leg proved in `POST_SWEEPER_DETOUR.md` |
| `corrected_central_candidate.py`, `corrected_central_candidate_32_monotone.*` | Added that inward leg for nonnegative transition parameters; bounded run converged within its sampled family | Still omits partial negative-transition detours; its princess dual fails the exact unrestricted response check in `interval_central_concentration` |
| `central_wait_exploit.py`, `offset_response_search.py`, `offset_response_*` | Discovered explicit monster responses to the sampled hider laws, including positive-margin constructions and ordered quantile payoffs | Floating discovery; the final rational exclusion uses the simpler marginal theorem, not these numerical response values |
| `witnesses.py`, `witnesses32.json` | Constructed paths approaching archived deadline responses | Witness exploration only; small margins and singular limits do not yield a uniform all-monster lower guarantee |

## Reproduction examples

From this directory, with the optional numerical dependencies installed:

```sh
python direct_support.py 4
python near_sweeper_support.py 8
python center_return_support.py 8
python central_wait_candidate.py 32 monotone
python corrected_central_candidate.py 32 monotone
python offset_response_search.py corrected_central_candidate_32_monotone.json
```

The half-network continuation uses the saved `response` field in
`full_half_network_16.json` as its seed. A fresh base-network run overwrites
that file without a response field; in that case first supply an actual
monster response before running the continuation. The saved files preserve
the original completed bounded experiment and its seed.

The corrected candidate script now enforces its supported monster family in
every mode: M1(-1), M1 with nonnegative parameter, and M2. Applying its detour
payoff formula to other negative M1 parameters would omit an earlier-capture
loss. The saved `monotone` run used the supported family and is unaffected
by that mode restriction. Its additional weight-order inequalities also
matter: the reported dual is a lower strategy only against those constrained
monster mixtures, not against every sampled pure M1/M2 path. In particular,
its payoff against the sampled M2(-11/32) is below the reported restricted
objective. Neither dual interpretation supplies an unrestricted lower bound.

The stopped larger LP and the nonconverged cut-generation loop need not be
rerun. Their purpose here is to record the stopping conditions and prevent
their intermediate objectives from being mistaken for a completed proof.

## Exact results extracted from this work

- `../interval_refined_upper/`: rational 134-path upper guarantee, with full
  integer-flow verification.
- `../interval_post_sweeper_detour/`: exact gain from a missing response leg.
- `../interval_candidate_densities/`: exact checks of the corrected payoff
  derivatives, conditional ODE, and negative-transition counterexample.
- `../interval_central_concentration/`: exact unrestricted response excluding
  the corrected sampled princess law and its ordered rearrangement.

The global conditional four-parameter response theorem is a hand proof in
`research/08-continuum/CONDITIONAL_RESPONSE_REDUCTION.md`; no experiment
establishes that an optimal monster law satisfies its density hypotheses.
