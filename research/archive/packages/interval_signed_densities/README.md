# Signed-M1 functional and exclusion checks

Run from the repository root:

    python packages/interval_signed_densities/verify.py
    python packages/interval_signed_densities/verify_dual.py
    python packages/interval_signed_densities/verify_trace_cap.py
    python -B packages/interval_signed_densities/verify_local_gap.py
    python packages/interval_signed_densities/verify_local_capture.py

This standard-library-only checker verifies the derivative formulas in
`research/09-equilibrium-structure/SIGNED_M1_FUNCTIONAL.md` by differentiating
the exact rational capture integrals. It reuses the rational automatic-
differentiation arithmetic from `interval_candidate_densities/verify.py`,
but assembles the enlarged signed-M1 capture functional independently.

The checks cover positive and negative transition parameters, both signs of
the final inward endpoint, the two prefix ordering branches, the endpoint-
start tangent y=c, and the central-wait diagonal u=a. This checks algebra;
it does not certify an equilibrium, a proposed density, or a new game bound.

`verify_dual.py` checks the dual capture-payoff derivatives in
`SIGNED_PRIMAL_DUAL_SYSTEM.md` against the independent continuous-rank
engine. Its rational example has a genuine central waiting mass and covers
both orderings of the initial-position and outgoing-characteristic fronts.
The 16 fixtures also include distinct c and y fronts, checking the
additional derivative terms in the extra-leg case.
An additional five-leg example separates the two outgoing fronts and
checks the limiting payoff derivatives by exact affine extrapolation in
the positive second-inward-leg offset. Together these give 16 exact
dual derivative checks.

`verify_trace_cap.py` independently integrates direct segment-intersection
capture times over constant and linear monster densities. Its 28 exact cap
inequalities and 28 exact negative-M2 shift identities cover endpoint and
center starts, initial coincidences, U/V plateaus, and repeated turns.
They check the boundary bookkeeping in `NEGATIVE_M2_SHIFT.md` without
assuming that the princess has a canonical scalar response shape. These
additional checkers also use only Python's standard library.

## Fixed-bin structural discovery

`discover.py` integrates continuous piecewise constant monster densities
analytically in the starting position. It imposes the three sufficient
monotonicity conditions from `SIGNED_M1_SUFFIX_REDUCTION.md`, and searches
the four-parameter limiting princess response family. The bins remain
fixed throughout, with at most five rounds of numerical response separation.
The saved `discovery.json` and `discovery.log` record the run and its
stopping rule.

The active response shapes suggested a coupled boundary system, recorded
in `SIGNED_PRIMAL_DUAL_SYSTEM.md`. The extra inward legs in that system
fail an unrestricted support check under a shifted M2 response. Neither
the fitted densities nor their constrained LP dual constitute a saddle
certificate. In particular, the density-monotonicity constraints prevent
interpreting the LP dual as a lower law against arbitrary pure monsters.

`verify_discovery_features.py` independently compares the numerical bin
integrals with the exact rational capture integrals in `verify.py`, on
27 fixtures spanning both signs of the transition and suffix endpoints.
This optional comparison and the discovery script use NumPy, SciPy, and
Numba; the exact derivative checker above does not.

## Exact exclusion of the rationalized candidate

`local_gap_certificate.json` contains one exact normalization of the
rounded discovery densities. `verify_local_gap.py` checks nonnegativity,
total mass, and all three monotonicity conditions. It then proves a
strict scalar response gap on the full closed domain with
`31/32 <= a <= 63/64` and either `c <= 0` or `y-c <= 1/16`.
Affine and convex reductions leave five two-dimensional slices; 946
closed rational quadratic cells, including their faces, are maximized
exactly. A legal scalar response outside the bad set exceeds its exact
ceiling by `947831/2048001504`.

Combined with the arbitrary-path theorem in `NEGATIVE_M2_SHIFT.md`,
these exact data give a concrete four-law monster mixture whose response
ceiling is strictly smaller than that of the rationalized law. The
checker verifies the rational mixture coefficients and a positive
guaranteed decrease. The proof and the scope are explained in
[`LOCAL_SCALAR_GAP.md`](../../research/09-equilibrium-structure/LOCAL_SCALAR_GAP.md).
This is a candidate exclusion, not an equilibrium or a new game-value
interval. The checker uses only Python's standard library.

`verify_local_capture.py` checks the actual rational candidate independently
of the scalar integral assembly. It integrates direct segment-intersection
times for 20 legal epsilon paths over the continuous monster densities,
then verifies five exact one-sided payoff limits. These include the
comparison response and both bad-region maximizers, as well as positive
central waiting and a negative suffix. All agree exactly with the scalar
functional used by the certificate. This checker also needs only the
standard library.
