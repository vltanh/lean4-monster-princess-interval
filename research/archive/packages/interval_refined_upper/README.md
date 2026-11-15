# Exact refined unrestricted upper bound

Run `python verify.py` using the Python standard library. The verifier
checks the explicit rational 134-path monster law in `strategy.json`,
builds all 27 full-interval deadline networks, computes integer flows,
and independently verifies capacity, conservation, and matching cuts.

The resulting bound is

    V <= 36563170811/25600000000 = 1.4282488598046875.

It improves the previous exact upper bound by
`28681989/25600000000`. It is **not** the exact unrestricted game value.

The proof is in `research/08-continuum/REFINED_UPPER_BOUND.md`, relative to
the repository root. `verification_output.txt` records a full passing run.
No floating-point optimizer, third-party library, compiler, or Lean build
is needed. The decimal printed by Python is only a display of the exact
rational result.
