# Finite-reduction gate audit

The full minimax finite reduction is NOT proved. Read `research/11-finite-reduction/FINITE_REDUCTION_GATE.md` for the hand proofs, exact scope, and missing equilibrium-specific obligation.

From this directory, run Python 3 with the standard library only:

```sh
python endpoint_absorbed_turns.py --max-k 9 --output endpoint_absorbed_turns.json
python exact_quadratic.py
python verify_finite_bellman.py --output finite_bellman_results.json
```

The first calculation is an exact specified-law counterfamily, not a sampled monster grid. The second and third implement finite certificate-verification components and complete endpoint-law fixtures, not a general automatic certificate search. No Lean compilation or CI is required or claimed.
