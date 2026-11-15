# Reproduce the available exact checks

Each `interval_*/` directory is an independently generated historical snapshot. They intentionally retain their original relative imports and compressed flow files. Do not move scripts away from their folders.

Python 3 standard library only for these core checks:

```sh
(cd interval_pm_proof && python verify.py && python counterexample.py)
(cd interval_exact_reduction && python verify_exact.py)
(cd interval_exact_response_result && python tests.py)
(cd interval_target_exclusion && python verify_target.py)   # potentially expensive
(cd interval_equilibrium_check && python verify.py)
(cd interval_uniform_reduction && python tests.py)
(cd interval_uniform_reduction && python verify.py)         # potentially expensive
```

Some C++ files are optional independent cross-checks; no native compilation is necessary for standard-library Python verifiers. Exclude research logs from assertions of proof; consult each package's `PROOF.md` and `README.md` for its exact scope. No CI or Lean proof is promised by this snapshot.

All six original package snapshots are also preserved in the archive file at `archive/monster_princess_progress_2026-11-10.zip` (see package directory list), including larger exploration checkpoints that may not be checked out individually.
