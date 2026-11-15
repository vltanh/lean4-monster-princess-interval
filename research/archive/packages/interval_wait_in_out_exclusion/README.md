# Exact wait-in-out response exclusion

Run `python verify.py`. Only Python's standard library is required.

The verifier exactly maximizes the three-parameter princess family that
waits at its starting point, travels inward at speed one, then travels
outward at speed one and stays at the endpoint. A complete hyperplane
arrangement certificate checks every limiting branch, including branches
adjacent to capture-time discontinuities.

For a specified symmetric six-row M1/M2 monster mixture, this family's
response supremum is `2641/1600`. A separately intersected rational
princess path obtains `100559/60000`, strictly more by `3043/120000`.

See `../../research/08-continuum/WAIT_IN_OUT_COUNTEREXAMPLE.md` for the
finite-completeness proof and the exact scope. This excludes the specified
response-shape reduction; it does not determine the unrestricted game value.
