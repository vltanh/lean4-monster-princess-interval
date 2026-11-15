# Unrestricted interval Princess--Monster: partial proof package

**Not a full minimax solution.** The completed result is a computer-assisted upper-bound certificate:

    V <= 229233/160000 = 1.43270625.

The certificate covers every continuous princess path, including unrestricted turning and waiting. The monster is a specified mixture of 32 unit-speed piecewise-linear paths.

## Verify

No third-party packages are required for the checks:

    python verify.py
    python counterexample.py

`verify.py` reconstructs rational event times and integer network capacities, then checks saved feasible flows. It does not call an optimizer. `counterexample.py` checks an exact counterexample to the fixed-infinitesimal response reduction from the earlier discussion; it is not a full-game lower-bound certificate.

## Files

- `PROOF.md`: the mathematical reduction, explicit strategy, certificate interpretation, and limitations.
- `strategy.json`: rational monster mixture.
- `flows.json.gz`: positive integer flow arcs, compressed with gzip.
- `verify.py`: standard-library-only certificate verifier.
- `verification.json`: a convenient summary; the verifier does not trust this summary.
- `counterexample.py`: rational intersection checks for the four-path counterexample.

The exact unrestricted minimax value and a matching princess distribution remain unproved in this work.
