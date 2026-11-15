# Candidate exclusion, not a full-game solution

Run `python verify_target.py` with Python 3.9 or newer.

`PROOF.md` states exactly what is and is not proved. The verifier performs an
exhaustive exact search retaining all minimizers, with strict lower-bound pruning
and no dominance pruning. It proves that the previously reported value
56305800187/40000000000 is strictly below the full-game value.

Files:
- `princess_strategy.json`: the unchanged 60-path princess distribution.
- `enumerate_all.py`: integer all-minimizer response search.
- `verify_target.py`: path, endpoint, lattice and perturbation checks.
- `enumeration_result.json`: the earlier saved all-minimizer run.
- `verified_result.json`: output of the complete new verifier.

The unrestricted exact value is not established by this package.
