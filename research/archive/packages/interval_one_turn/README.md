# Canonical one-turn analysis

This package **closes the strict separation test negatively**: a physical
continuous one-turn Monster law has an exact all-Princess upper below the frozen
comparison target. The exact restricted minimax value remains open.

The Monster class starts anywhere, uses unit-speed straight legs with at most
one interior reversal before its first endpoint, then sweeps directly to the
opposite endpoint. The Princess has no path restriction. The endpoint reversal
does not count as an interior reversal. Arbitrary waiting or variable-speed
one-reversal paths are not silently included in this canonical class.

## Complete response formula

The [complete-domain theorem](../../research/13-equilibrium-geometry/ONE_TURN_COMPLETE_DOMAIN.md)
includes negative turns, late returns, endpoint starts, exact endpoint faces,
time-zero capture, atoms and contact ties. For a fixed rational piecewise-affine
CDF it gives a finite quadratic partition of the two-parameter response domain.

```sh
python3 packages/interval_one_turn/verify_domain.py
```

The independent direct-capture fixtures check 2,432 oriented formula cases,
152 contact-tie cases and 1,887 endpoint-face domination cases. The universal
theorems are proved in the manuscript, not established by these finite tests.

## Closed comparison: continuum physical upper

The [countercertificate](../../research/13-equilibrium-geometry/ONE_TURN_SEPARATION_COUNTERCERTIFICATE.md) proves

\[
V\le W_1\le\frac{142472349375511}{100000000000003}
=1.424723493755067\ldots<\frac{57}{40}<U_*.
\]

Thus the target W_1>U_* is false. The law combines an endpoint-sweep atom,
an S(a) density, and six P_b(a) densities at b=15/16,31/32,1,65/64,33/32,17/16.
Every physical path belongs to the canonical class. The initial-radius and
light-coordinate potential theorem bounds **every** legal Princess path,
including arbitrary turns, waits, endpoint/center contacts and time-zero ties.
It does not determine exact W_1, exact V, or whether W_1=V.

```sh
python3 packages/interval_one_turn/verify_continuum_upper.py \
  packages/interval_one_turn/one_turn_continuum_upper.json.gz \
  --output /tmp/one_turn_continuum_replay.json --require-counterexample
python3 packages/interval_one_turn/verify_continuum_upper.py --self-test
python3 packages/interval_one_turn/verify_continuum_functional.py
python3 packages/interval_one_turn/verify_continuum_physical.py
```

All four commands require only Python's standard library. The frozen input
contains exact integer masses and quadratic potential numerators, rational
mesh data, and one exact normalization denominator. Replay reconstructs the
physical coefficients and verifies 691,200 HJB vertex inequalities, 19,050
U-interface inequalities, 18,000 W-interface inequalities, 1,800 terminal
inequalities and 96 initial cubic inequalities: **730,146 checks, zero
residual repair**. The benchmark comparison uses exact fractions.

The [potential proof](../../research/13-equilibrium-geometry/ONE_TURN_CONTINUUM_POTENTIAL_CERTIFICATE.md)
proves continuous coverage between mesh points and handles both initially
crossed b<1 boundaries and late b>1 terminal captures. Optimizer objectives,
floating residuals and numerical CDF auxiliary columns are absent from the
frozen replay. Its SHA256 is
`c87c7b902382396bce06e4265b6140077b50e336af48de5ff6d2f301af9dc482`.
The retained report is `one_turn_continuum_upper_replay.json`.

The independent chronological functional checks pass 77 full-support and
308 density-subinterval cases. A separate physical checker, independent
of the potential/HJB implementation, passes 238 P-bin, 136 S-bin and 34
endpoint fixtures; its report is `continuum_physical_replay.json`.
The analytic endpoint-only certificate gives exactly 3/2 with zero repair;
self-tests also exercise two residual repairs and reject four malformed inputs.

## Earlier projected atomic upper

The [projected physical certificate](../../research/13-equilibrium-geometry/ONE_TURN_PROJECTED_PHYSICAL_UPPER.md)
proves

\[
W_1\le\frac{478205958821456999}{335544320000000000}
=1.425164815251401\ldots.
\]

The saved law contains 375 fair-reflected rational physical path pairs with
integer weights of denominator 10^10. It improves the earlier upper below
by exactly `1165888329615857/8388608000000000000`, but remains above the frozen
benchmark by `200087745232387/1677721600000000000`. It is superseded by the
continuum law above.

```sh
python3 packages/interval_one_turn/rebuild_projected_upper.py --output /tmp/one-turn-projected
python3 packages/interval_one_turn/verify_projected_upper.py \
  /tmp/one-turn-projected/one_turn_projected_upper.certificate.json
python3 packages/interval_one_turn/verify_projected_upper.py --self-test
```

The [independent reconstruction note](PROJECTED_UPPER_VERIFICATION.md) explains
the exact rational physical clauses, sound projection implications, and
integer flow. The Python verifier does not trust supplied geometry, reward
coefficients, labels, or floating scores. It rebuilds 112,604 graph nodes and
328,157 arcs, checks every integer capacity and node balance, and checks exact
flow/cut equality. Missing sound projection edges may weaken this upper and
are deliberately permitted. No finite-width Princess witness is claimed.

The compact input is `one_turn_projected_upper.json.gz`; its hash and the
executed counts appear in `one_turn_projected_upper_replay.json`. Rebuilding
needs Python's standard library, Node, and a C++17 compiler. Replay alone uses
only the Python standard library. Both commands accept
`--require-counterexample`, which deliberately rejects this law because its
exact upper exceeds the benchmark.

## Earlier causal-clock certificate

The earlier exact saved law proves

\[
W_1\le\frac{1459511091170171}{1024000000000000}
=1.4253037999708701171875.
\]

It uses 413 physical/calendar plans on 326 distinct reflected path pairs.
Every path belongs to the stated canonical class, visits the center by time
two and completes its endpoint tour by time 65/16. The bound is above the
frozen unrestricted benchmark by exactly
`66111055169/256000000000000`; it does not close the separation test.

The [physical upper manuscript](../../research/13-equilibrium-geometry/ONE_TURN_PHYSICAL_UPPER.md)
explains the all-Princess normalization, causal upper planes and sound order
inequalities. Neither a finite Princess bank nor the floating optimizer is
used as proof of the upper.

```sh
python3 packages/interval_one_turn/rebuild_upper.py --output /tmp/one-turn-upper
python3 packages/interval_one_turn/verify_upper.py \
  /tmp/one-turn-upper/one_turn_upper.sparse.json
```

Rebuilding uses the repository's existing graph generator and C++ integer
maximum-flow proposal helper, then the unchanged JavaScript BigInt physical
verifier and a separate Python integer/Fraction replay. It needs Python with
the repository's NumPy/SciPy dependencies, Node and a C++17 compiler; it runs
no floating-point LP. Replaying the generated certificate with `verify_upper.py`
uses only the Python standard library.

The saved `one_turn_upper.json.gz` is the full exact law, compacted using runs
of identical physical moves and runs of identical consecutive clock charges.
It contains integer probabilities, all physical paths, both causal calendars
and the expected rational upper. `rebuild_upper.py` expands these without
rounding. The generated integral flow and cut are independently checked, so
the optimizer and graph generator need not be trusted. The saved
`one_turn_upper_replay.json` records hashes, exact counts, flow/cut equality
and the comparison with the frozen benchmark.

`--require-counterexample` makes either rebuild or replay reject a certificate
unless its one-turn upper is at most the frozen benchmark. It deliberately
rejects this earlier checkpoint. The continuum checker above now passes the
corresponding gate, disproving `W1 > U*` without proving `W1 = V` or identifying
either exact minimax value.

## Exact finite-law pricing and the complete lower hierarchy

The [finite-Princess attack theorem](../../research/13-equilibrium-geometry/ONE_TURN_FINITE_PRINCESS_ATTACK_SET.md)
reduces the full continuous one-turn response to a finite exact arrangement
for each supplied actual rational polygonal Princess law. The general mode
includes subunit velocities and interior waits; initial and turn ties use
actual first coincidence.

```sh
python3 packages/interval_one_turn/verify_finite_princess.py
python3 packages/interval_one_turn/verify_finite_princess.py --general --law actual_princess_law.json
```

The [minimax and hierarchy proof](../../research/13-equilibrium-geometry/ONE_TURN_MINIMAX_AND_EXACT_GRID_HIERARCHY.md)
establishes an attained optimal Monster probability law and equality with
the supremum of actual finite Princess securities. Unit-step Princess paths
on the parity clock have exact continuous one-turn pricing on a finite
parameter grid. Their dyadic finite LP lower values increase to W_1 without
a continuum-transfer subtraction. This is a convergence theorem with no
claimed rate, finite optimal support, or finite attaining grid. A successful
strict finite-law certificate also yields continuous rational piecewise-affine
approaching laws by the proved uniform-security regularization argument.

The checker independently audits 896 integer/Fraction physical intersections,
1,440 general inverse/chronological intersections, third-leg jump and initial
contact cases, and 1,296 exact parity-clock contacts. The proofs establish
the continuum claims; these fixtures audit the implementations.

## Endpoint-only repair obstruction

The [endpoint repair theorem](../../research/13-equilibrium-geometry/ONE_TURN_ENDPOINT_REPAIR_OBSTRUCTION.md)
rules out a particular tempting continuation: keeping the saved interior law
fixed and replacing its endpoint mass by any one-turn distribution, with
arbitrary starts. Every such law has worst
Princess response at least `62211501887219437/43648000000000000`, still above
the benchmark. Its proof covers both first-endpoint choices and arbitrary
legal turn locations. It does not rule out coupled changes to the bulk law.

```sh
python3 packages/interval_one_turn/verify_endpoint_repair.py
```

The checker reconstructs the saved law's endpoint baseline and gap, verifies
the exact endpoint-layer capture kernels and their tie faces, and recomputes
the obstruction. Its 1,443 kernel/domination checks, 144 outside-gap checks,
and 1,239 saved-plan
capture comparisons audit the arbitrary-measure proof in the manuscript.

## Why one finite atomic bank could not close the target

The [806-bank obstruction](opposing_finite_bank_obstruction.md) proves that
every probability reweighting on its specified 806 physical geometries has
worst Princess response at least 1167495935793/819200000000>U_*.
This is a finite-bank exclusion, not an all-B_1 lower; the successful
continuous law above has starts outside that finite bank.

```sh
node packages/interval_one_turn/opposing_verify_finite_bank.cjs
```

No Lean compilation or CI run is claimed.
