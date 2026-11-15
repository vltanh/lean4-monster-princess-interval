# Exact interval-game response certificate

This package does **not** solve the full Princess and Monster game.

It verifies the exact unrestricted monster response to the explicit princess mixture in `princess_strategy.json`:

    56305800187 / 40000000000 = 1.407645004675.

Thus the unrestricted game's value is strictly greater than 11/8; the previously suggested values near 1.373 are excluded as well. No matching monster guarantee is claimed.

Read `PROOF.md` for the full mathematical reduction, the thirty-row symmetric strategy, the pruning proofs, and the exact scope of the result.

Run with Python 3 (standard library only):

    python verify.py princess_strategy.json --expect 56305800187/40000000000
    python tests.py

No optimizer is invoked. Optional independent GMP rational implementation: `verify_gmp.cpp`.
