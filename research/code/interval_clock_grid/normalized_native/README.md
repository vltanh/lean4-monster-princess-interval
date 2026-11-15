> This folder holds only the files that the bounds in [`research/`](../../../README.md) need. The description below is the original one; files it mentions that are not here are in [the archive](../../../archive/packages/interval_clock_grid/normalized_native).

# Native exact pricing of the normalized physical grid bank

`price_normalized.cpp` prices a supplied integer radial dual profile exactly.
It branches only until the first endpoint or time 2, and then evaluates the
deterministic endpoint suffixes. A Fenwick prefix-minimum structure removes
states dominated in both running records and accumulated cost. All prices,
comparisons, tail sums, and dominance decisions use unsigned integers. There
is no beam width, path-count cutoff, or floating-point pruning.

The mathematical dependencies are
[left-floor clock atomization](../../../archive/research/12-global-closure/LEFT_FLOOR_CLOCK_ATOMIZATION.md),
[exact physical-bank normalization](../../../archive/research/12-global-closure/NORMALIZED_GRID_BANK_PRICING.md),
and [common quantization](../../../archive/research/12-global-closure/EFFECTIVE_FINITE_UPPER_REDUCTION.md).
The exhaustive search verifies the finite computation; those proofs establish
its relation to the unrestricted game.

## Input and output

Compile with a C++17 compiler. The binary input is little-endian:

1. `uint32` version, currently 1;
2. `uint32` grid parameter `n`;
3. `uint64` radial-profile denominator `D`;
4. row-major `uint64` values `g[j][k]` for `0 <= j <= 12n` and
   `0 <= k <= 2n`.

Only nodes with matching parity are used. Their values must be in `[0,D]`,
the center must be zero, and every adjacent interval-containment inequality
must hold. The executable validates these conditions before searching.
It also checks dimensions and integer bounds before computing costs.

```sh
g++ -O3 -std=c++17 price_normalized.cpp -o /tmp/price_normalized
/tmp/price_normalized input.bin 32
```

The optional final argument is the number of attaining or near-attaining
routes to retain. Setting it to zero disables all path-history storage and
returns the exact minimum alone. This saves memory when checking a finer
dual. Witness mode stores packed move prefixes only for the current and next
Pareto layers, plus the winning complete routes. It does not retain the
unbounded ancestor tree of earlier versions. All route tie ordering and
integer search decisions are preserved. The minimum `K` is in units of
`1/(4nD)`. Therefore

\[
 V\ge\frac{K-2D}{4nD}.
\]

This is a game-value lower bound. An arbitrary nodal profile checked only
on the normalized bank is not automatically an explicit Princess security
certificate. The separate optional sticky/outward dual conditions in the
normalization theorem supply the stronger full-bank nodal inequality.

## Sparse numerical discovery

`solve_normalized.py` uses NumPy and SciPy to maximize a restricted nodal
master, generates new physical-path/calendar constraints with the exact
integer oracle, and repeats. It can seed the master with a coarser grid's
physical plans when the new grid parameter is an integer multiple.
When the bundled native HiGHS interface is available, it retains separate
master and bundle-level simplex bases and appends new cuts. `--fresh-lp`
selects the independent fresh SciPy implementation. This changes discovery
speed only; both paths use the same exact integer certification gate. Each warm solve resets its deadline relative to the cumulative HiGHS run clock, so the configured time budget applies to that solve. A real native time-limit regression verifies recovery without discarding the warm basis.

```sh
python3 solve_normalized.py 6 --output /tmp/normalized_n6
node ../normalized_record_pricing.cjs /tmp/normalized_n6.dual.json
```

The numerical profile is clipped, quantized to integer values, and repaired
by exact isotone closure before pricing. The saved `.dual.json` contains the
complete rational profile and exact minimum. The separately saved checkpoint
contains floating LP values and mixture weights; those are discovery data
and are not claimed as exact upper certificates.

`cached_path_pricing.py` evaluates the exact current running-record cost of
already known physical paths in vectorized integer batches. If one violates
the current LP level, its new minimizing clock calendar is added immediately.
These cached minima are **upper** bounds on the complete dual minimum; they
never update the certified lower. The complete native oracle is called when
the cache has no new separating calendar. `--no-cached-separation` disables
this acceleration. `save()` rejects witness-only answers.

By default the master imposes sticky endpoint and outward-after-two nodal
constraints, whose value-preserving property is proved separately. The
`--unrestricted-profile` option retains arbitrary isotone profiles instead.
The oracle itself supports both classes and always scans its deterministic
tails exactly, including record crossings.

`refine_dual.py` interpolates a saved profile to a finer grid and repeats
exact integer pricing without optimizing a new master. Its lower is certified
by the final feasible integer field and search, independently of the quality
of the interpolation heuristic.

`--profile-grid k` optimizes a coarse full-width characteristic field while
pricing every physical path on the finer grid `n`, where `k` divides `n`.
`interpolated_master.py` keeps each interpolation coefficient as an integer
over `2*(n/k)` and constructs the exact fine field from repaired coarse
integers. It projects the physical clock columns onto the coarse variables.
The resulting LP upper is an upper for this **restricted Princess profile
class**, not an unrestricted game upper. Complete fine-bank pricing still
gives a globally valid feasible-dual lower after subtracting `1/(2n)`.

```sh
python3 solve_normalized.py 256 --profile-grid 64 --denominator 100000000 \
  --seed /path/to/n64.checkpoint.json --profile-seed /path/to/n64.dual.json \
  --output /tmp/coarse64_fine256
```

The portable current lower can be replayed without NumPy or SciPy:

```sh
python3 verify_native_field.py ../lower_n256_field.json
node --max-old-space-size=8192 ../normalized_record_pricing.cjs ../lower_n256_field.json --target-bound
```

The Python and JavaScript readers independently decode the compact exact
field. The native checker computes its minimum; BigInt target mode proves
the claimed lower without asserting target attainment. See the
[global certificate note](../../../archive/research/12-global-closure/NORMALIZED_GLOBAL_BOUND_CERTIFICATES.md)
for the value bound and distinct explicit Princess security.

## Independent verification

`test_price_normalized.py` uses exhaustive Fraction path enumeration on small
grids, without the native dominance pruning, and a separate integer DP on
known certificate profiles through n=6. It checks returned routes by direct
chronological pricing. The saved replay records 72 small fields, 29,448
enumerated normalized paths, 2,016 late-center rejections, 144 endpoint-start
paths, 34,290 tail record decreases, and 1,006 checked output routes. Reflection
symmetry removes duplicate starting orientations in the native search; the
independent exhaustive reference still checks both orientations. Value-only
mode is checked against route mode on four additional cases.

`../normalized_record_pricing.cjs` is a separate BigInt implementation that
accepts the saved rational fields and reconstructs the exact normalized
minimum. It verifies the input order constraints and compares its result to
the claimed native integer minimum. Neither implementation establishes finite
exact termination of the unrestricted game.

The native search also uses proved [independent-pursuit lower bounds](../../../archive/research/12-global-closure/NORMALIZED_PURSUIT_LOWER_BOUND.md). For exact outward profiles, it combines a relaxed pre-two pursuit with lower bounds on both time-two records and the weighted endpoint-tour formula. Otherwise it uses only the basic independent-pursuit relaxation. These bounds prune a state only after comparison with a complete legal-path incumbent.
