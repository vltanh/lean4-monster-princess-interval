> This folder holds only the files that the bounds in [`research/`](../../README.md) need. The description below is the original one; files it mentions that are not here are in [the archive](../../archive/packages/interval_clock_grid).

# Exact polynomial clock-grid LPs

This package makes the finite approximation theorem operational. It contains exact rational primal and dual certificates for n=1,2,3,4,6, independent complete pricing implementations, and the current unrestricted bound certificates.

## Current whole-game certificates

The exact n=256 feasible Qout dual and the new n=128 physical Monster law in [interval_discovery_certificates](../interval_discovery_certificates/README.md) give

\[
\frac{582291421641}{409600000000}\le V\le
\frac{145925593551091}{102400000000000}.
\]

An explicit legal Princess quantile law has security at least
`582289859141/409600000000 = 1.42160610141845703125`.
The slightly larger value lower above uses vanishing interpolation width.
See [the full certificate note](../../archive/research/12-global-closure/NORMALIZED_GLOBAL_BOUND_CERTIFICATES.md),
[the compact strategy construction](../../archive/research/12-global-closure/NORMALIZED_PRINCESS_EXTRACTION.md),
and [the physical Qout upper](../../archive/packages/interval_clock_grid/QOUT_PRIMAL_CERTIFICATES.md).

```sh
python packages/interval_clock_grid/normalized_native/verify_native_field.py packages/interval_clock_grid/lower_n256_field.json
node --max-old-space-size=8192 packages/interval_clock_grid/extract_normalized_princess.cjs verify packages/interval_clock_grid/lower_n256_field.json packages/interval_clock_grid/lower_n256_princess.json
python packages/interval_discovery_certificates/verify_manifest.py
```

The second command performs the large independent BigInt lower replay and
regenerates the strategy. Cheap strategy evaluation does not replace that
check. The former 703-pair `upper_n64_physical.json.gz` remains here as the exactly verified discovery seed. The exact game is still open.

## Finite approximation theorem

The model is the complete integer-credit LP in [POLYNOMIAL_CLOCK_GRID_LP.md](../../archive/research/12-global-closure/POLYNOMIAL_CLOCK_GRID_LP.md). The global interpretation depends on [EFFECTIVE_FINITE_UPPER_REDUCTION.md](../../archive/research/12-global-closure/EFFECTIVE_FINITE_UPPER_REDUCTION.md):

\[
U_n-\frac1{2n}\le V\le U_n.
\]

Here \(U_n\) is the exact optimum of the finite clock-grid LP, and \(V\) is the unrestricted game's value. These first grids demonstrate the reduction and exact verification. Their enclosures do not improve the sharper separately certified numerical bounds already recorded in the repository. An exact finite-grid optimum is not an exact formula for \(V\).

## Reproduce the exact certificates

No third-party packages are required.

```sh
node packages/interval_clock_grid/verify_grid.cjs packages/interval_clock_grid/grid_n1_certificate.json
node packages/interval_clock_grid/record_pricing.cjs packages/interval_clock_grid/grid_n1_certificate.json
node packages/interval_clock_grid/verify_grid.cjs packages/interval_clock_grid/grid_n2_certificate.json
node packages/interval_clock_grid/record_pricing.cjs packages/interval_clock_grid/grid_n2_certificate.json
```

The same commands apply to `grid_n3_certificate.json`.

Both verifiers reject a nonzero exact duality gap. The first additionally reconstructs every physical path and clock, checks the supplied cone matching, and prices the entire credit-state DAG. The second reuses the physical primal checks and prices physical paths directly through their running historical clock minima. It does not build or traverse the credit-state DAG.

| Grid | Exact finite optimum \(U_n\) | Global lower \(U_n-1/(2n)\) | Physical/calendar plans | Full DAG nodes | Full DAG arcs |
|---|---:|---:|---:|---:|---:|
| \(n=1\) | \(47/32\) | \(31/32\) | 2 | 3,221 | 9,215 |
| \(n=2\) | \(4893/3376\) | \(4049/3376\) | 4 | 64,271 | 218,923 |
| \(n=3\) | \(3153038167/2187120435\) | \(1859012063/1458080290\) | 10 | 321,175 | 1,156,127 |

The independent record verifier visits 261 states for \(n=1\), 2,522 for \(n=2\), and 9,651 for \(n=3\). These are states with a physical position, visit flags, and two historical minima. They are not sampled paths or a truncated search.

## Discover the certificates again

```sh
node packages/interval_clock_grid/solve_grid.cjs 1 /tmp/grid_n1
node packages/interval_clock_grid/solve_grid.cjs 2 /tmp/grid_n2
```

The solver writes a checkpoint after each column-generation iteration, then writes the exact certificate and replay report. Its initial columns are two explicit physical strategies. It solves a numerical restricted path master, prices all complete physical calendars in the full DAG, and adds improving columns. Convergence of floating-point column generation only triggers rational reconstruction. The solver returns success only after the reconstructed primal and dual pass the exact verifier.

The portable solver was evaluated with the same module bodies in a JavaScript isolate. It reproduced both exact values from the two initial columns. The supplied certificate files were also checked on the full graph after removing the geometric deadline pruning used in an earlier discovery implementation.

## Physical model and scaling

Put \(\Delta=1/(2n)\), with 16n time steps through time 8. Initial positions are on the coarser grid \(n^{-1}\mathbb Z\cap[-1,1]\). Every move changes time by \(\Delta\) and position by \(\pm\Delta\).

A state records time, position, the two active clock credits, the first-visit flags for the endpoints, and the center-visit flag. Both credits begin at zero. A charge adds one unit to an active credit. A move requires one unit from every active credit and consumes it. On first reaching an endpoint, its corresponding credit must be exactly zero and that clock becomes inactive. The center must have been visited by time 2, and both endpoints by time 8. The progress quantity \(3j+q_-+q_+\) strictly increases, so the flow graph is acyclic.

Every path is used with its reflection with equal probabilities. A minus-clock charge at position \(x\) emits at \((t,x)\); a plus-clock charge emits at \((t,-x)\). Each charge has physical mass \(\Delta/2=1/(4n)\). In these scaled units:

- Every charge has baseline cost 1.
- A positive emitted event has an additional cost 1.
- Every matched positive/negative unit subtracts 1.
- The final LP objective is divided by \(4n\).

A positive event \((t,x)\), \(x>0\), may match a negative event \((s,y)\), \(y<0\), exactly when \(-y\ge x+|s-t|\), with time and position expressed in the same grid units. Center events have baseline cost 1 and no matching vertex.

## What the exact certificates prove

Each certificate lists rational path weights, integer physical moves, integer causal clock calendars, integer matching amounts under a common denominator, and rational nonnegative event discounts.

The primal replay checks every unit-speed move, initial position, deadline, clock support before its endpoint visit, left-limit causal prefix, exact active-clock mass, probability normalization, matching cone condition, and matching capacity. It then computes the exact strategy objective.

For every admissible positive/negative pair, the discounts satisfy

\[
d_p+d_q\ge1.
\]

Consequently, subtracting the event discount from each charge cost gives a lower bound on the matched objective of every physical strategy. An exact shortest-path calculation finds the minimum modified charge cost across the entire credit DAG. Equality with the primal proves the finite LP optimum.

The second verifier obtains the same dual minimum differently. Along a fixed physical path, if the active clock ends after K moves and its event costs are \(c_0,\ldots,c_{K-1}\), then its best causal calendar has cost

\[
\sum_{j=0}^{K-1}\min_{0\le i\le j}c_i.
\]

Each unit of active time selects a cheapest available past event. This produces a valid integer calendar and realizes the lower bound imposed by the causal prefixes. The verifier therefore enumerates all reachable physical states while retaining the two running minima and the cheapest cost for each identical state. No beam limit or approximate dominance rule is used.

Acceptance calculations use integers and BigInt, including the primal/dual equality. Floating-point rational reconstruction is only a proposal mechanism. Changes to the physical-step metadata, an underfunded clock, an overcapacity matching entry, and an infeasible discount cover were each rejected during validation.

## A small explicit optimum

For \(n=1\), the pair law assigns weight \(7/8\) to the fastest sweep from +1 to -1 and weight \(1/8\) to

\[
(0,0)\to(1/2,1/2)\to(2,-1)\to(4,1).
\]

Each pair includes its reflected orientation. The baseline is \(5/4\), and the unmatched positive pressure is \(7/32\), giving \(47/32\). The exact discount dual proves that no other allowed grid path or causal calendar improves this value.

For \(n=2\), the four exact pair weights are \(349,3,21,49\), divided by 422. The baseline is \(284/211\), and the unmatched pressure is \(349/3376\). Their sum is \(4893/3376\). Complete routes, calendars, and dual discounts are in the certificate file.

## Files

- `grid_model.cjs`: complete physical-credit DAG and numerical shortest-path pricing.
- `small_lp.cjs`: numerical simplex for restricted column masters.
- `solve_grid.cjs`: discovery, checkpointing, rational reconstruction, and mandatory exact replay.
- `exact_certificate.cjs`: exact primal matching and full-DAG dual verification.
- `verify_grid.cjs`: command-line exact certificate replay.
- `record_pricing.cjs`: independent exact physical-record dual replay.
- `grid_n1_certificate.json`, `grid_n2_certificate.json`: exact witnesses.
- The corresponding `_replay.json` and `_record_replay.json` files: recorded exact results.


## Extract an actual Princess law

The [constructive extraction theorem](../../archive/research/12-global-closure/CONSTRUCTIVE_PRINCESS_GRID_DUAL.md)
turns the exact nodal dual into a continuous rational P1 field. The implementation
includes the full isotone profile, one-parameter threshold integration, endpoint
stopping, and maximal outward continuation after time 2.

~~~sh
node packages/interval_clock_grid/extract_princess.cjs packages/interval_clock_grid/grid_n2_certificate.json 1/100 /tmp/grid_n2_princess.json
node packages/interval_clock_grid/verify_princess_extraction.cjs packages/interval_clock_grid/grid_n2_certificate.json /tmp/grid_n2_princess.json
~~~

For positive rational width \(\varepsilon\le1/2\), the returned law guarantees
\(U_n-1/(2n)-\varepsilon/(2n)\) against every Monster. Its finite description
contains the nodal radial CDF and exact interpolation rule; uniform quantiles
and an independent fair sign specify the actual paths. The module exposes exact
rational `radialCDF`, `interiorTrace`, and `strictCDF` evaluators. Negative-endpoint
strict contact is distinguished from the interior trace.

The included `grid_n1_princess.json`, `grid_n2_princess.json`, and
`grid_n3_princess.json` use \(\varepsilon=1/(2n)\). Their coarse guarantees
are examples of the construction, not improvements on the separately certified
Princess lower bound. `verify_princess_extraction.cjs` first verifies the finite
dual and regenerates the entire field. It then checks isotone closure against
full interval containment, all nodal values, and exact sampled CDF symmetry,
transport and outward equalities. The analytic proof establishes legality
between sample points.

The first two certificates can be rediscovered by the small solver above.
The third required a physical-record column solver and exact integer
reconstruction with larger denominators; its complete certificate is portable
and independently replayable by both existing verifiers.


## Larger grids with the nodal master

```sh
node packages/interval_clock_grid/solve_nodal_grid.cjs 4 /tmp/grid_n4
node packages/interval_clock_grid/record_pricing.cjs packages/interval_clock_grid/grid_n4_certificate.json
node packages/interval_clock_grid/record_pricing.cjs packages/interval_clock_grid/grid_n6_certificate.json
```

The nodal solver replaces explicit matching variables in the restricted master
by radial CDF values and adjacent containment inequalities. It prices all
physical paths through the two historical minima, then reconstructs the active
rational system with exact elimination. Acceptance still requires equality
with the independent BigInt primal/dual replay.

| Grid | Exact finite optimum | Physical/calendar plans | Record states |
|---|---:|---:|---:|
| 4 | `232810938448419/161887841831168` | 13 | 25,081 |
| 6 | `290632881989129783194425025/202628114404287702771503547` | 25 | 132,141 |

These are exact atomic-clock LP optima. Their bounds remain weaker than the
separately certified numerical game interval. The
[uniform-leg extension](../../archive/research/12-global-closure/POLYNOMIAL_UNIFORM_LEG_CLOCK_LP.md)
defines a stronger polynomial LP that removes the vertex-only clock restriction;
the filenames above retain their original atomic-clock meaning.

## Exact physical-bank normalization and native scaling

The [left-floor theorem](../../archive/research/12-global-closure/LEFT_FLOOR_CLOCK_ATOMIZATION.md) proves that the atomic-clock LP already equals the true unrestricted Princess-response minimax on its complete finite physical bank. [Uniform clocks](../../archive/packages/interval_clock_grid/UNIFORM_CLOCKS.md) are an equivalent independently implemented refinement; exact n=1,2,3 values agree.

The [normalized pricing theorem](../../archive/research/12-global-closure/NORMALIZED_GRID_BANK_PRICING.md) permits branching only until first endpoint or time 2, followed by deterministic endpoint tours. [Independent BigInt pricing](../../archive/packages/interval_clock_grid/NORMALIZED_PRICING.md) reproduces every supplied n=1,2,3,4,6 optimum. The [native implementation](normalized_native/README.md) combines exact integer pricing, independent exhaustive tests, and a sparse numerical master with persistent LP bases. Finer feasible duals give rigorous game-value lower bounds after subtraction of 1/(2n); numerical master values alone are not unrestricted certificates.
