# Pull request 1: Unrestricted interval Princess–Monster: one-turn comparison closed, exact game OPEN

> Archived from the retired research repository. This was its only pull request, from
> `research/interval-progress-2026-11-10` into `main`, opened 2026-11-11 and still open when the repository was
> retired. Links to `vltanh/lean4-monster-princess` no longer work; the files they point to are
> in this folder at the same paths. The commit messages are in [HISTORY.md](HISTORY.md).

## Description

## Update 2026-11-15: new bounds 1.4225745 ≤ V ≤ 1.4240199, structure of both players' optimal paths

Base for links: `research/interval-progress-2026-11-10`. Nothing below is a Lean proof, and no CI was run for these commits.

**Start here:** [research/14-light-cone-lattice/README.md](https://github.com/vltanh/lean4-monster-princess/blob/research/interval-progress-2026-11-10/research/14-light-cone-lattice/README.md) summarizes the bounds, both strategies, what is proved and what to do next. `research/14-light-cone-lattice/strategies.html` draws both strategies interactively (download the file and open it in a browser; rebuild with `python3 packages/interval_lightcone/build_strategy_page.py`).

**New upper bound (written proof and exact integer computation; not independently reviewed).**

\[
 V\le\frac{1603303881142469}{1125899906842624}=1.4240199075\ldots,\qquad
 W_1\le\frac{25661865897887875}{18014398509481984}=1.4245197187\ldots
\]

The Monster law is atomic: one-turn paths `P_b(a)` and two-turn paths `T_2(c,U_1)` on the grid 1/2048, 0.5 % of the mass on two-turn paths. Every Princess path is reduced to a staircase of grid cells in light coordinates and the maximum over staircases is an integer dynamic program. The C++ and NumPy programs return the same integer; small grids are checked against exhaustive enumeration and against physical trajectories in exact fractions. The enclosure stated below, which had an independent replay, is left as it was. Note: [ATOMIC_TWO_TURN_UPPER.md](https://github.com/vltanh/lean4-monster-princess/blob/research/interval-progress-2026-11-10/research/14-light-cone-lattice/ATOMIC_TWO_TURN_UPPER.md).

**New lower bound (both native engines agree; no independent BigInt replay).**

\[
 V\ge\frac{9322984150699}{6553600000000}=1.4225744858854674
\]

The retained n512 Princess field is refined to n = 1024 by the common-threshold rule (exact over twice the denominator) and priced by the unchanged `price_normalized.cpp`: complete normalized-bank minimum 18652368301398/13107200000000, then the 1/(2n) transfer. `price_normalized.cpp` took 4.96 hours; `price_center.cpp` (policies 3 and 4) returns the same minimum in 25 minutes each. Files: [princess_front_n1024](https://github.com/vltanh/lean4-monster-princess/tree/research/interval-progress-2026-11-10/packages/interval_discovery_certificates/princess_front_n1024), written by the repository's own `refine.py`. Note: [REFINED_N1024_LOWER.md](https://github.com/vltanh/lean4-monster-princess/blob/research/interval-progress-2026-11-10/research/14-light-cone-lattice/REFINED_N1024_LOWER.md).

With both new bounds the bracket is **1.4225745 ≤ V ≤ 1.4240199**, width 0.0014454 (was 0.0024654).

**Numerical findings** ([LIGHT_CONE_LATTICE_GAME.md](https://github.com/vltanh/lean4-monster-princess/blob/research/interval-progress-2026-11-10/research/14-light-cone-lattice/LIGHT_CONE_LATTICE_GAME.md), floating-point LPs unless stated):

- A lattice solver in light coordinates reproduces the five exact clock-grid optima and extends them to n = 8, 16, 24, 32. The identity `U_n = L_n + 1/(4n)` between the clock-grid optimum and the half-offset lattice value is proved.
- One interior turn is not enough for the Monster: two-turn paths that join a sweep are worth about 4e-4 in the continuum laws. The best bounds found on the grids 1/128, 1/256, 1/1024 extrapolate to about **1.4240** for the game with these two Monster families. This is an estimate, not a bound.
- The Princess's lattice optimum is reached to within 4e-5 by a three-parameter family: run outward for a short time, run inward, wait at the center if reached, run outward and stay. Her arrival times at the center are constrained by Monster paths that loiter near the center (0.2 % of the Monster's weight at n = 16).
- The lower bound is the larger part of the gap. The retained field cannot give more than about 1.4229 on any grid; a better bound needs a better field. An exact continuous-time pricing program for finite Princess laws (`capture_order_pricing`) avoids the lattice transfer loss, but the best law fed to it so far is worth 1.4137.

Code: [packages/interval_lightcone](https://github.com/vltanh/lean4-monster-princess/tree/research/interval-progress-2026-11-10/packages/interval_lightcone).

```sh
python3 packages/interval_lightcone/check_atomic_upper.py --grids 16 32 64 128 256
g++ -O3 -fopenmp -std=c++17 packages/interval_lightcone/atomic_upper.cpp -o /tmp/atomic_upper
/tmp/atomic_upper packages/interval_lightcone/atomic_law_32bins_grid2048.txt 2048
```

---

## One-turn comparison closed negatively; exact game OPEN

The proposed separation `W1 > U*` is false. This update retains a physical one-turn Monster law and an exact certificate proving its upper against **every legal Princess path**:

\[
\frac{36409808231}{25600000000}\le V\le W_1\le
C:=\frac{142472349375511}{100000000000003}
<\frac{57}{40}<U_*:=\frac{291849329389899}{204800000000000}.
\]

The current unrestricted enclosure is **1.4222581340234375 ≤ V ≤ 1.424723493755067…**, with width **0.002465359731629758…**. The saved explicit positive-width Princess law separately guarantees **1.42225718034912109375**; the larger limiting lower must not be attributed to that fixed law.

The exact restricted value `W1`, the unrestricted value `V`, and whether `W1 = V` remain open. This is a research manuscript and computational-certificate PR, **not a completed Lean proof**.

### What the new certificate establishes

The canonical Monster class consists of free-start unit-speed paths with at most one **interior reversal before the first endpoint**, followed by a direct sweep to the opposite endpoint. The endpoint reversal is not counted as interior. The Princess has arbitrary starts, turns, waits and endpoint/center contacts.

The law combines an endpoint-sweep pair with seven piecewise constant start densities: endpoint-first `S(a)` and one-turn `P_b(a)` at `b = 15/16, 31/32, 1, 65/64, 33/32, 17/16`, all paired fairly with their reflections. Every component is physically in the declared class. This supplies alternative (M) of the separation directive and excludes alternative (P); do not continue the resolved search for `W1 > U*`.

- [Countercertificate and complete physical law](https://github.com/vltanh/lean4-monster-princess/blob/research/interval-progress-2026-11-10/research/13-equilibrium-geometry/ONE_TURN_SEPARATION_COUNTERCERTIFICATE.md)
- [Continuum potential theorem](https://github.com/vltanh/lean4-monster-princess/blob/research/interval-progress-2026-11-10/research/13-equilibrium-geometry/ONE_TURN_CONTINUUM_POTENTIAL_CERTIFICATE.md): physical capture functional, initially crossed turn levels, late endpoint captures, radius interpolation, and arbitrary-path coverage
- [Retained certificate and verifier package](https://github.com/vltanh/lean4-monster-princess/tree/research/interval-progress-2026-11-10/packages/interval_one_turn)

### Exact validation

The standard-library Python replay reconstructs the physical coefficients and verifies **730,146 rational inequalities**: 691,200 interior HJB, 19,050 U-interface, 18,000 W-interface, 1,800 terminal and 96 initial cubic checks. Every positive residual is exactly zero, so **no residual repair is needed**. Floating optimizer objectives and feasibility tolerances are not proof inputs.

```sh
python3 packages/interval_one_turn/verify_continuum_upper.py \
  packages/interval_one_turn/one_turn_continuum_upper.json.gz \
  --output /tmp/one_turn_continuum_replay.json --require-counterexample
python3 packages/interval_one_turn/verify_continuum_upper.py --self-test
python3 packages/interval_one_turn/verify_continuum_functional.py
python3 packages/interval_one_turn/verify_continuum_physical.py
```

The independent chronological checks cover 77 full-support and 308 density-subinterval cases, plus a separate 238 P-bin, 136 S-bin and 34 endpoint audit. The analytic endpoint-only control gives exactly 3/2; self-tests exercise residual repair and reject malformed inputs. These fixtures audit the formulas; the manuscript proves universal coverage. **No new CI run or Lean formalization is claimed.**

Compressed certificate SHA256: `c87c7b902382396bce06e4265b6140077b50e336af48de5ff6d2f301af9dc482`. [Full replay and reproduction scope](https://github.com/vltanh/lean4-monster-princess/blob/research/interval-progress-2026-11-10/REPRODUCE.md).

### Preserved findings and provenance

- The inherited n512 lower retains its original complete pricing and transfer proof: [certificate](https://github.com/vltanh/lean4-monster-princess/blob/research/interval-progress-2026-11-10/research/12-global-closure/NORMALIZED_GLOBAL_BOUND_CERTIFICATES.md), [saved field and explicit law](https://github.com/vltanh/lean4-monster-princess/tree/research/interval-progress-2026-11-10/packages/interval_discovery_certificates/princess_front_n512), and [historical independent CI](https://github.com/vltanh/lean4-monster-princess/actions/runs/43546803161).
- The earlier 752-pair upper is the frozen benchmark `U*`: [retained provenance](https://github.com/vltanh/lean4-monster-princess/blob/research/interval-progress-2026-11-10/packages/interval_discovery_certificates/README.md) and [historical independent CI](https://github.com/vltanh/lean4-monster-princess/actions/runs/43544245486).
- The [complete one-turn domain](https://github.com/vltanh/lean4-monster-princess/blob/research/interval-progress-2026-11-10/research/13-equilibrium-geometry/ONE_TURN_COMPLETE_DOMAIN.md), [restricted minimax and convergent exact lower hierarchy](https://github.com/vltanh/lean4-monster-princess/blob/research/interval-progress-2026-11-10/research/13-equilibrium-geometry/ONE_TURN_MINIMAX_AND_EXACT_GRID_HIERARCHY.md), and [finite-Princess attack arrangement](https://github.com/vltanh/lean4-monster-princess/blob/research/interval-progress-2026-11-10/research/13-equilibrium-geometry/ONE_TURN_FINITE_PRINCESS_ATTACK_SET.md) remain valid. No convergence rate or finite attaining grid is asserted.
- The [earlier projected atomic upper](https://github.com/vltanh/lean4-monster-princess/blob/research/interval-progress-2026-11-10/research/13-equilibrium-geometry/ONE_TURN_PROJECTED_PHYSICAL_UPPER.md) is retained at `478205958821456999/335544320000000000` on 375 reflected pairs, with independent reconstruction and replay. The new [common-warp/flow reduction](https://github.com/vltanh/lean4-monster-princess/blob/research/interval-progress-2026-11-10/research/13-equilibrium-geometry/ONE_TURN_COMMON_WARP_FLOW.md) documents its synthesis. Both it and the older causal-clock certificate are superseded upper bounds.
- The [806-bank obstruction](https://github.com/vltanh/lean4-monster-princess/blob/research/interval-progress-2026-11-10/packages/interval_one_turn/opposing_finite_bank_obstruction.md) excludes every reweighting of that specified finite bank from reaching `U*`. Its scope is the finite bank; the successful continuous law uses additional starts. The earlier [endpoint-only repair obstruction](https://github.com/vltanh/lean4-monster-princess/blob/research/interval-progress-2026-11-10/research/13-equilibrium-geometry/ONE_TURN_ENDPOINT_REPAIR_OBSTRUCTION.md) likewise remains valid for its fixed interior law.
- Prior global results remain intact in the [core mathematical index](https://github.com/vltanh/lean4-monster-princess/blob/research/interval-progress-2026-11-10/research/12-global-closure/README.md), including synchronized physical matching and conditional finite-support reduction, the front-one projection counterexample, compensated-curvature cusp response, and distinct Zeno obstructions. [Structural-results commit](https://github.com/vltanh/lean4-monster-princess/commit/878d526ccb97dcf75a3ee150c04ff617782825cc).

### Remaining research objective

A matching all-Monster Princess lower and all-Princess physical Monster upper are still required to determine an exact value. The next structural target is a globally sufficient, transport-compatible contact/phase description, including both surviving records, free starts, arbitrary turns, and boundary contacts. Existing conditional contact equations and approximation hierarchies do not establish that sufficiency. A complete functional or variational characterization would count as an analytic solution without an elementary closed form.

Start with [HANDOFF](https://github.com/vltanh/lean4-monster-princess/blob/research/interval-progress-2026-11-10/HANDOFF.md), [NEXT_WORK](https://github.com/vltanh/lean4-monster-princess/blob/research/interval-progress-2026-11-10/NEXT_WORK.md), [STATUS](https://github.com/vltanh/lean4-monster-princess/blob/research/interval-progress-2026-11-10/STATUS.md), and the [geometry index](https://github.com/vltanh/lean4-monster-princess/blob/research/interval-progress-2026-11-10/research/13-equilibrium-geometry/README.md).

Historical handoffs and the [pre-squash branch](https://github.com/vltanh/lean4-monster-princess/tree/archive/pr1-pre-squash-2026-11-13) remain preserved. Heavy discovery workflows remain manual-only. Exact regression fixtures are available, with their scope distinguished from universal mathematical proofs.



🤖 Generated with [Claude Code](https://claude.com/claude-code)

## Comment 1 (2026-11-11)

## Finite reduction first — checkpoint 0e951c0

The requested full minimax finite reduction is **not established; G5 remains open**. This continuation did not refine the value interval or continue endpoint fitting.

Exact computation and a general hand argument show that symmetry, ordered paths, endpoint absorption by time two, and even an atomless piecewise-affine interior CDF do **not** imply a universal monster-turn bound. The construction forces k interior reversals for every k. Exhaustive rational checks covered k=1,...,9 plus a compact fixture: 349,780 canonical orders. These are specified-law counterexamples, not equilibrium exclusions.

A separate finite verification theorem now makes the local Bellman route explicit for supplied continuous piecewise-affine CDFs and continuous piecewise-quadratic potentials: four record-contact cases, at most three critical speeds (including rank tracking), endpoint reset/waiting cases, initial checks, and exact face-stationary quadratic minimization. The prototype passed 5,280 derivative identities, 5,280 critical-speed comparisons, seven quadratic fixtures, and five complete endpoint-law certificates. It is not an automatic solver for the repository candidate, nor a proof that an optimal finite certificate exists.

Read `research/11-finite-reduction/FINITE_REDUCTION_GATE.md` and run `packages/interval_finite_reduction_audit/`. The outstanding issue is an equilibrium-specific bounded certificate/phase-complexity theorem, or an explicit finite matching certificate pair. A finite verification format or an accuracy-dependent hierarchy does not close that issue. No Lean compilation or CI was run; the commit includes `[skip ci]`.

## Comment 2 (2026-11-13)

## Recurrence-first reassessment — 2026-11-13

The next direction is a generative response policy, not more complete-path mixtures or necessary support inequalities.

[GLOBAL_SURVIVOR_HALVING_RECURRENCE.md](https://github.com/vltanh/lean4-monster-princess/blob/research/interval-progress-2026-11-10/research/12-global-closure/GLOBAL_SURVIVOR_HALVING_RECURRENCE.md) derives an exact unrestricted Monster-response recurrence for every fixed legal ordered Princess field:

- State is (time, position, lower surviving rank cutoff, upper surviving rank cutoff). The whole past is replaced by two surviving rank tails, with an explicit normalized conditional-CDF restart.
- At any such state the conditional optimal remaining mean time is at most 2, by a pointwise two-endpoint-tour comparison.
- A phase is any legal prefix of duration at most 4 reducing remaining probability by at least half. It may contain arbitrarily many turns or Zeno accumulation; it is not a restricted trajectory template.
- The exact operator is T g = inf_phase [integrated survival cost + surviving fraction * g(next state)]. It has W=T W and contracts by at most 1/2. Iterating lower/upper continuations 0 and 2 brackets the full response within 2^(1-n) after n phases. A globally verified Bellman residual eta implies response error at most 2 eta.

**What is still unsolved:** computing the continuum phase operator, identifying an invariant analytic posterior family, and coupling its policy to a matching all-Princess dual certificate. A phase is NOT a finite-turn reduction. No equilibrium CDF, game value, or improved numerical bound is claimed.

Executed exact Fraction tests: 2,145 physical two-tour inequalities; 31 stationary/moving ordered-target models with 155 starting states; independent all-order and physical response comparisons; 1,085 iteration brackets; 28,334 strict/closed posterior identities. A counterexample shows that time/position/total surviving mass alone is insufficient: equal survivor mass can have conditional remaining values 2 and 3/4.

[Verifier](https://github.com/vltanh/lean4-monster-princess/blob/research/interval-progress-2026-11-10/packages/interval_global_closure/verify_survivor_halving.py) · [Executed report](https://github.com/vltanh/lean4-monster-princess/blob/research/interval-progress-2026-11-10/packages/interval_global_closure/verify_survivor_halving.report.json). Executed source was byte-matched to Git blob `6d04ae3bd7129909142cf24e9f51bccbf6e0f80a`. No Lean/CI run.

This is a recurrence description of the unrestricted response, not yet a closed-form recurrence for equilibrium turning times. The four-state record representation was already in the earlier Bellman notes; the new step is the conditional restart, uniform half-survival phase horizon, and contractive error-controlled recursion.

## Comment 3 (2026-11-13)

### Correction: the survivor-halving recurrence is not a strategic phase description

The user's objection is correct. The last result must NOT be interpreted as claiming that an optimal Monster reverses direction, resets, or switches physical policy when one-half of the remaining Princess probability has been caught.

For **every** fixed ordered Princess CDF F and **every** threshold 0<rho<1, the same exact response DPP can be split at the first point where surviving probability reaches rho times its starting value. With an artificial horizon max(4,2/rho), it contracts by rho and provides numerical *recursion-depth* control. Thus rho=1/2 has no privileged equilibrium meaning.

A transparent fixed-start optimal-response counterexample: stationary equally weighted Princess targets at {-1,0,1}, Monster starts at -1 and optimally goes straight right. After immediate capture at -1, the two survivors are {0,1}; at t=1 the survivor mass halves as the route passes x=0, but the optimal control has NO turn, wait or speed change.

The genuine **assumption-free**, fixed-F dynamic programming identity is for arbitrary elapsed h>0:

    R_F(z) = inf_{all speed<=1 prefixes gamma of duration h}
                [ integral_0^h S_u du + R_F(z_h) ].

Here R_F(z)=S(z) W_F(z), z=(t,x,a,b) is the exact two-rank record state. This is a tautologically valid semigroup identity, NOT a discovered structure for the game's equilibrium. The phase optimization still contains all Lipschitz paths, and the unknown Princess CDF is not determined.

**Status corrected, not solved:** The repository note [GLOBAL_SURVIVOR_HALVING_RECURRENCE.md](research/12-global-closure/GLOBAL_SURVIVOR_HALVING_RECURRENCE.md) now proves the every-rho statement and gives this physical counterexample. The [handoff](HANDOFF_2026-11-13.md) flags it explicitly. Future work must derive any nontrivial recurrence/invariant class from the coupled global saddle and calibrate both unrestricted responses, rather than assume a convenient threshold or family.
