# One exact common-coordinate update of the upper law

## Tight certificate: native replay completed 2026-11-13

The strongest stored common-warp certificate has now been independently
replayed in native Node, using the **tight** JSON rather than the earlier file:

```text
57045188913812444387410009 / 40000000000000000000000000
= 1.426129722845311109685250225.
```

Run from the repository root:

```sh
node --stack-size=16384 packages/interval_common_warp/verify_upper_warp_tight.cjs
```

The dedicated entry point pins both input Git blob hashes and checks positive
normalized probabilities, completion of both endpoints, the exact stored
flow/cut witness, all physical Monster vertices and unit legs, both extremal
response rows, and the actual approaching Princess first contacts. It also
recompiles every reward directly from the **warped physical routes** and
compares all 53,588 exact coefficients with the common-map interval basis;
this checks the actual tight nonidentity warp, not just the identity map.

The reproducible output is `upper_warp_tight_replay.json`. Its 59,593-node,
177,126-arc certificate has 104,598 positive flows. The physical check uses
560 oriented first contacts against a 211-vertex legal Princess path, whose
payoff lies below the supremum by approximately 9.68033796855e-16.

This closes the tight-certificate replay item in the handoff. It does not
improve the stored bound, construct a matching lower strategy, or provide a
Lean check. The historical CLI below intentionally continues to read the
earlier certificate.

## Earlier certificate and construction

This package freezes one geometric update of the already certified 280-pair monster law. Its unrestricted first-capture response is

```text
57045189772271291487410009 / 40000000000000000000000000
= 1.426129744306782287185250225
```

The probabilities are unchanged: the 280 nonnegative integer numerators sum to 10^10, and each pair is split equally between a path and its reflection. The only change is a common strictly increasing map of light coordinates. This is an upper strategy and an exact response certificate. It is not a matched equilibrium or a lower guarantee.

## Geometry and exact coefficients

Let 0=k_0<...<k_68=1 be the stored knots. The stored positive integer increments n_i, divided by 10^15, sum to one. They define a piecewise affine map psi on [0,1], extended by oddness and psi(x+2)=psi(x)+2. Apply (U,V) -> (psi(U),psi(V)) to every path.

Strict monotonicity preserves light-coordinate order, the strip |U-V|<=2, the time-zero line, reflection, and the endpoint lines U-V=+/-2. Unit legs remain unit legs. The same transformation is a bijection on unrestricted legal princess paths, so the response can be computed on the reference event arrangement.

For a first contact with reference light coordinates (U_c,V_c), its new time is (psi(U_c)+psi(V_c))/2. Each survival reward in the complete atomic event compiler is a positive coordinate interval. Splitting that interval at integers and folding by oddness and two-periodicity expresses the reward as a nonnegative integer combination of the 68 increments. No positive rewards are discarded.

The stored compiler audit checks all 53,588 identity reward coefficients and two nonidentity strict rational maps, for 160,764 exact interval/reward comparisons. Five independent capture-coordinate feature rows also pass. These audits concern the common-map coefficient construction; the candidate certificate below is replayed separately.

## Certificate and replay

Files:

- `upper_warp.cjs`: common-map interval compiler, capture-coordinate feature rows, numerical discovery cut, and exact physical map.
- `upper_warp_integer.cjs`: integer graph construction, optional exact solve, and flow/cut replay.
- `upper_warp_exact.json`: exact increments, all 280 mapped physical pairs, both extremal response labels, and the integer flow certificate.
- `verify_upper_warp.cjs`: rebuilds the interval basis from the source law and verifies the stored result without rerunning max flow.
- `upper_warp_basis_verification.json`: coefficient checks.
- `upper_warp_replay.json`: reproducible replay report.

The source law is `../interval_global_closure/upper_dyadic_exact.json`. The compiler uses the existing complete atomic survival oracle and exact priced-order projection in `../interval_turn_density/`.

Run:

```sh
node packages/interval_common_warp/verify_upper_warp.cjs
```

The exact projected graph has 59,593 nodes and 177,126 directed arcs. The stored 104,598 positive flow entries obey every integer capacity and every node conservation equation. Their value equals the stored cut capacity. Both extremal exact capture-coordinate rows agree with the resulting fraction.

The verifier also checks all 1,165 physical vertices and 885 unit legs, probability normalization, and 560 oriented segment-capture calculations against one common legal epsilon princess. At epsilon=2^-48 its score is below the exact supremum by approximately 9.68034e-16. That path only witnesses approach to this upper law's response; it is not a minimax lower strategy.

## Scope of the discovery machinery

The numerical warp minimax used only the same finite coordinate knots. It did not refine a path mesh, alter probabilities, or establish a continuum saddle. This one strict update is now frozen; further value iterations are not part of this checkpoint.

The numerical reward compiler also permits zero increments for an auxiliary limiting optimization. Such an output must not be interpreted as the actual response to a collapsed physical law. If psi_0 is nondecreasing, use psi_epsilon=(1-epsilon)psi_0+epsilon*identity. The strict maps preserve contact order, and their capture-time errors relative to the limiting reference expression are uniformly bounded by ||psi_epsilon-psi_0||_infinity. The saved physical law itself has strictly positive increments and needs no such limiting qualification.

The gap to an unrestricted lower construction remains open. The active response/capture geometry, rather than further decimal refinement, is the intended next input to the coupled phase analysis.

