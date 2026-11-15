# Light-cone staircase solvers

Numerical solvers for the interval Princess–Monster game written in the light coordinates
`U = t + x`, `W = t - x`. The LP solvers are **floating point and are not certificates**. They
reproduce the five exact clock-grid optima already in the repository and extend the same quantity
to finer grids.

The exception is the **atomic upper bound**: `atomic_upper.cpp` is an exact integer program. With the
proof in
[ATOMIC_TWO_TURN_UPPER.md](../../UPPER_BOUND.md) it gives
`V <= 1603303881142469/1125899906842624 = 1.4240199075...` and
`W_1 <= 25661865897887875/18014398509481984 = 1.4245197187...`.

The mathematics, the results and their scope are in
[research/LATTICE_GAME.md](../../LATTICE_GAME.md).

## Files

| File | What it solves |
| --- | --- |
| `lattice_game.py` | Unrestricted lattice game: Princess nodal field LP, exact Monster best response by a frontier dynamic program |
| `lattice_game_turns.py` | The same game with the Monster limited to `k` interior turns before its first endpoint, then a direct sweep |
| `one_turn_lattice.py` | One-turn family `P_b(a)`, `|a| <= b <= 2 - a`, as a Monster LP with a Princess dynamic program over `(r0, U, W)` |
| `one_turn_continuum.py` | Continuum one-turn game with piecewise-constant start densities and exact integration, turn levels `b = 1` and `b = 2 - a` only |
| `continuum_turn_levels.py` | Continuum LP with piecewise-constant densities: one-turn paths with turn levels spread around `b = 1`, and two-turn paths that join a one-turn trajectory |
| `validate_small_grids.py` | Regression against the exact optima `U_n`, `n = 1, 2, 3, 4, 6`, of `research/code/interval_clock_grid` |
| `price_lattice_optimum.py` | Prices a lattice optimum with the exact integer engine `price_normalized.cpp`, on its own grid and, after the common-threshold interpolation, on finer grids |
| `princess_family_lattice.py` | The lattice game with the Princess restricted to the three-parameter family "out, in, (wait at the center), out, stay"; within 4e-5 of the unrestricted optimum on `N = 8, 16, 24` |
| `capture_order_pricing.py`, `capture_order_pricing.cpp` | Exact Monster best response against a finite ordered Princess law in continuous time, by a shortest-path program over (captured interval, side). The Python file is tested against an exhaustive search; the C++ file is the same program in integers (a 1000-path law in 22 s); `capture_order_pricing_samples.cpp` takes paths given by integer samples |
| `atomic_upper.cpp` | Exact all-Princess upper bound for an atomic law of one-turn pairs `P_b(a)` and two-turn pairs `T2(c, U1)`: integer dynamic program over cell staircases, one start cell per thread |
| `atomic_response.py` | Independent NumPy version of the same dynamic program, and the reader that places a compact law on the grid `1/N` |
| `check_atomic_upper.py` | Checks: capture-time table against physical trajectories in exact fractions, dynamic program against exhaustive enumeration, C++ against Python |
| `optimize_atomic_law.py` | Cutting-plane optimization of a binned law for one grid, with `atomic_upper.cpp` as the exact response oracle |
| `atomic_law_32bins_grid2048.txt`, `atomic_law_32bins_grid1024.txt` | Laws optimized for the grids `1/2048` and `1/1024`: `V <= 1.4240199075` and `V <= 1.4240686613` |
| `atomic_law_16bins.txt`, `atomic_law_16bins_one_turn.txt` | Laws taken from the continuum LP: integer bin masses over `2^24` on the mesh `1/16` |
| `atomic_upper_replay.json` | Output of `atomic_upper.cpp` for the four laws |
| `strategy_page_data.py`, `build_strategy_page.py`, `strategy_page_template.html` | Build the playground `research/strategies.html` (not committed; the same page is at [vltanh.me/princess-monster-interval](https://vltanh.me/princess-monster-interval/)) from the committed law, field and programs (about 20 s). Its averages are exact for the Monster's law placed on the grid 1/512, whose proved bound (1.4242096) the page quotes |
| `refine_retained_field.py`, `refined_n1024_lower_replay.json` | Exact factor-2 refinement of the retained `n = 512` Princess field by the repository's common-threshold rule, and its pricing at `n = 1024` with `price_normalized.cpp` (5 hours, 16 GB): `V >= 9322984150699/6553600000000 = 1.4225744859` |

Requirements: Python 3 with NumPy and SciPy (HiGHS through `scipy.optimize.linprog`).

## Commands

Run from the repository root.

```sh
python3 research/code/interval_lightcone/validate_small_grids.py        # about 5 s, prints PASS
python3 research/code/interval_lightcone/lattice_game.py 16 --quiet     # about 80 s
python3 research/code/interval_lightcone/lattice_game_turns.py 8 1      # at most one interior turn
python3 research/code/interval_lightcone/one_turn_lattice.py 16
python3 research/code/interval_lightcone/one_turn_lattice.py 16 --only-main-levels
python3 research/code/interval_lightcone/one_turn_continuum.py 32
python3 research/code/interval_lightcone/continuum_turn_levels.py 16 2 0         # one turn: 1.4244766
python3 research/code/interval_lightcone/continuum_turn_levels.py 16 2 3 --check 4 8   # with two-turn paths
python3 research/code/interval_lightcone/price_lattice_optimum.py 16 32 64 128   # needs g++
python3 research/code/interval_lightcone/princess_family_lattice.py 16 3 --quiet        # about 1 min
python3 research/code/interval_lightcone/check_atomic_upper.py --grids 16 32 64 128 256   # about 45 s, prints PASS
g++ -O3 -fopenmp -std=c++17 research/code/interval_lightcone/atomic_upper.cpp -o /tmp/atomic_upper
/tmp/atomic_upper research/code/interval_lightcone/atomic_law_32bins_grid2048.txt 2048   # 15 s: V <= 1.4240199075
/tmp/atomic_upper research/code/interval_lightcone/atomic_law_32bins_grid1024.txt 1024   # 3 s: V <= 1.4240686613
/tmp/atomic_upper research/code/interval_lightcone/atomic_law_16bins.txt 4096            # 140 s on 20 threads, 3.2 GB
/tmp/atomic_upper research/code/interval_lightcone/atomic_law_16bins_one_turn.txt 4096
```

`atomic_upper` prints the maximum `K`, the total weight `W` and the bound `K / (8 N W)`.

`lattice_game.py N` prints the half-offset lattice value `L_N` and `L_N + 1/(4N)`. The second
number is the clock-grid optimum `U_N` ([LOWER_BOUND.md](../../LOWER_BOUND.md)) for `N = 1, 2, 3, 4, 6`
to within `2e-15`. `price_lattice_optimum.py` checks the same
identity on the optimal fields themselves: the exact engine returns `45838149486/32000000000` at
`N = 8` and `91427061649/64000000000` at `N = 16`. The interpolated optimum prices much lower on
finer grids (1.4170, 1.4141, 1.4122 on 32, 64, 128 from `N = 16`), so these fields are not seeds
for a better certified lower bound.

## Conventions

- `delta = 1/(2N)`. Monster nodes are `(U, W) = (2i, 2j) delta`; a move adds `2 delta` to `U`
  (right) or to `W` (left). Starts are the multiples of `1/N`.
- The Princess moves on the odd points `(2m+1, 2k+1) delta`, so the two players never tie. Her
  mixed strategy is a radial nodal field `G(s, d)` on the Monster nodes, the mass of radial paths
  strictly inside the node, with `G(s+1, d+1) >= G(s, d) >= G(s+1, d-1)`.
- A Monster edge captures, at its midpoint time, the mass by which the signed field leaves the
  interval between its running minimum and maximum.
- Every best-response path is continued to both endpoints before it is turned into an LP cut. A
  path that stops when everything is caught under the current field gives a cut that is false for
  other fields; an early version of the solver had this defect and returned values that were too
  low.
