# Light-cone program: bounds, strategies and open problems

Summary of the work of 2026-11-14 and 2026-11-15 on the interval Princess–Monster game. Both players
choose hidden 1-Lipschitz paths in \([-1,1]\) with free starts; the payoff is the first coincidence
time. The exact value \(V\) and a matching pair of optimal strategies are **still open**.

Throughout, \(U=t+x\) and \(W=t-x\) are light coordinates. A 1-Lipschitz path is a monotone curve in
the \((U,W)\) plane, a unit-speed path is a staircase, and two players meet where their curves cross.
That change of coordinates is what made the computations below exact.

## 1. Bounds

| Bound | Value | How it is verified | Not done |
| --- | --- | --- | --- |
| Lower, retained before this work | \(V\ge 36409808231/25600000000 = 1.4222581340\) | two native engines and an independent BigInt replay ([princess_front_n512](../../packages/interval_discovery_certificates/princess_front_n512/README.md)) | |
| **Lower, new** | \(V\ge 9322984150699/6553600000000 = 1.4225744859\) | the same field refined to \(n=1024\); the repository's two native engines return the same bank minimum ([REFINED_N1024_LOWER.md](REFINED_N1024_LOWER.md), [princess_front_n1024](../../packages/interval_discovery_certificates/princess_front_n1024/README.md)) | independent BigInt replay (started, stopped after about 15 minutes) |
| Upper, retained before this work | \(V\le W_1\le 142472349375511/100000000000003 = 1.4247234938\) | 730,146 exact potential inequalities, independent replays ([countercertificate](../13-equilibrium-geometry/ONE_TURN_SEPARATION_COUNTERCERTIFICATE.md)) | |
| **Upper, new** | \(V\le 1603303881142469/1125899906842624 = 1.4240199075\) | written proof plus an exact integer dynamic program; C++ and NumPy programs return the same integer; small cases checked by exhaustive enumeration and by exact-fraction trajectories ([ATOMIC_TWO_TURN_UPPER.md](ATOMIC_TWO_TURN_UPPER.md)) | independent review, Lean |
| **Upper on the one-turn class, new** | \(W_1\le 25661865897887875/18014398509481984 = 1.4245197187\) | same proof; C++ program at \(N=4096\), both programs agree up to \(N=2048\) | as above |

With the two new bounds, \(1.4225745\le V\le 1.4240199\), width \(0.0014454\) (from \(0.0024654\)).

**Estimates, not bounds.** From the Monster's side, the best laws of the two families below on the
grids \(1/1024\) and \(1/2048\) extrapolate to about \(1.42397\). From the Princess's side, the best
profiles on the grids \(1/16, 1/32, 1/64\) have limits \(1.41908, 1.42156, 1.42274\), about
\(0.078/k\) below the same number. Both point to \(V\approx1.4240\), close to the new upper bound and
about \(1.4\cdot10^{-3}\) above the lower bound.

Also proved here: the clock-grid identity \(U_n=L_n+1/(4n)\) between the repository's clock-grid
optimum and the half-offset lattice value
([LIGHT_CONE_LATTICE_GAME.md](LIGHT_CONE_LATTICE_GAME.md), Section 3).

## 2. The strategies

### Monster

The law behind the new upper bound, [atomic_law_32bins_grid2048.txt](../../packages/interval_lightcone/atomic_law_32bins_grid2048.txt),
is a symmetric mixture: each path is played together with its mirror image. Masses:

| Family | Path | Mass |
| --- | --- | ---: |
| sweep | from one endpoint straight to the other | 0.6228 |
| \(S(a)\), \(a>0\) | to the near endpoint \(+1\), then across to \(-1\) | 0.1728 |
| \(P_1(a)\), \(a>0\) | right until \(t+x=1\), left to \(-1\), right to \(+1\) | 0.0962 |
| \(P_1(-c)\), \(c>0\) | the same, started on the far side | 0.0664 |
| \(S(-c)\), \(c>0\) | through the centre to \(+1\), then to \(-1\) | 0.0297 |
| \(P_b(\pm a)\), \(b\) near 1 | one turn at a level \(t+x=b\) just off 1 | 0.0072 |
| \(T_2(c,U_1)\) | out to \(t+x=U_1\), back until \(t-x=1\), then the sweep from \(-1\) | 0.0050 |

Start positions are spread over 32 bins of width \(1/32\) with piecewise-constant densities. The
two-turn paths start mostly near the centre and join the sweep that left \(-1\) at time 0. They are
worth about \(3.9\cdot10^{-4}\): with one-turn paths alone the best law of the same form has limit
1.42449.

On the lattice the unrestricted Monster also uses paths that loiter near the centre for a while
before sweeping (0.2 % of the weight at \(n=16\)). They are not in the two families, and they are the
reason a Princess law optimized only against one- and two-turn Monsters loses \(7\cdot10^{-3}\)
([LIGHT_CONE_LATTICE_GAME.md](LIGHT_CONE_LATTICE_GAME.md), Section 7).

### Princess

The Princess plays an **ordered** law: a symmetric radial CDF \(G(t,r)\), each radial rank \(q\)
following the level curve \(G=q\) on a random side. The field behind the lower bound is the retained
grid-64 profile ([princess_front_n512](../../packages/interval_discovery_certificates/princess_front_n512/README.md)),
refined to \(n=1024\). Read off its rank curves:

- the innermost ranks, \(q\lesssim0.2\), reach the centre and wait there until time 1;
- ranks up to \(q\approx0.7\) pass within 0.005 to 0.03 of the centre at about \(t=0.9\);
- ranks from 0.75 to 0.85 turn back at radius 0.1 to 0.2, just before time 0.9;
- the top ranks come in only to about radius 0.64;
- most ranks first run **outward**, by up to 0.04, and after time 1 every rank runs out to the endpoint.

On the lattice the Princess's optimum is reached to within \(4\cdot10^{-5}\) by the three-parameter
family "out for a time \(\sigma\), in, wait at the centre if reached, out, stay", and dropping the
outward run costs \(2.8\cdot10^{-3}\) ([LIGHT_CONE_LATTICE_GAME.md](LIGHT_CONE_LATTICE_GAME.md),
Section 7).

### Indifference

The two laws were found separately, so they are not an exact saddle pair, but each nearly equalizes
the other's options:

- against the Monster law, the Princess's best payoff (computed by `atomic_upper.cpp` on the grid
  \(1/2048\)) is within \(10^{-4}\) of its maximum from 99.3 % of starting radii, and within
  \(1.2\cdot10^{-4}\) from all of them; her best-response paths have the phases of her own field;
- against the Princess field (lattice cost on the time grid \(1/1024\)), 96 % of the Monster law's
  probability is on paths within \(2\cdot10^{-4}\) of the cheapest path and 99 % within \(10^{-3}\); the
  mass-weighted mean excess is \(1.7\cdot10^{-4}\). The rest sits at the edges of a few start bins.
  Paths it never uses cost \(10^{-3}\) to 0.4 more.

The linear relations behind this, such as \(\rho(c)=e/(7-c)\) and
\((7+a)p(a)+(1-a)s(a)=e\), are derived in
[ONE_TURN_INDIFFERENCE_EQUATIONS.md](ONE_TURN_INDIFFERENCE_EQUATIONS.md) for the support seen
numerically. They do not yet cover the layer before time 1 or fix the thresholds.

## 3. Structural findings (numerical)

- One interior turn is nearly enough for the Monster: on the lattice the restriction costs
  \(1.7\cdot10^{-4}\), \(7.9\cdot10^{-5}\), \(5.2\cdot10^{-5}\), \(2.2\cdot10^{-4}\), \(2.2\cdot10^{-4}\) at
  \(n=4,8,16,24,32\). The gap does not shrink, so there is no evidence for \(W_1=V\).
- Turn levels just off \(b=1\) matter: with \(b=1\) and \(b=2-a\) only, the continuum one-turn value
  stays near 1.4254.
- An upper-bound law is tied to the grid it was optimized for and gets worse on finer grids; a law
  taken from the continuum improves with the grid. A lower-bound field behaves the same way: the bank
  minimum of a fixed field exceeds its limit by about \(0.18/n\).
- The lattice optimum of one grid is a poor seed for the lower-bound pipeline (its interpolant prices
  near 1.412), because it uses the lattice to stay one step ahead of a sweep.

## 4. What to do next

1. **Lower bound — the larger part of the gap.** A profile on a grid finer than 64. The repository's
   `solve_normalized.py --profile-grid k`, seeded from the next coarser solution, reaches \(k=64\) in
   about 20 minutes; \(k=48\) at \(n=96\) gave bank 1.4242268. The \(k=128\) stage at \(n=256\) needs a
   longer LP time limit than the built-in 120 s and had not improved its seed after an hour. By the
   \(0.078/k\) law a grid-128 profile should certify about 1.4231 at \(n=1024\). Refining the retained
   field to \(n=2048\) instead gives at most about 1.42273 (4.5 hours, 42 GB with `price_center.cpp`).
2. **Independent replay of the new lower bound** with `verify_bigint.cjs` (17 minutes at \(n=512\),
   expected several hours at \(n=1024\)).
3. **Upper bound.** A law optimized on \(1/4096\) gains at most about \(5\cdot10^{-5}\); adding loitering
   paths to the Monster's families is the structural change that could matter.
4. **Exact solution.** Complete the indifference equations with the layer before time 1, the two-turn
   paths and the thresholds; decide \(W_1>V\) with a Princess law that guarantees more than 1.42402
   against every one-turn Monster.
5. **Pricing without a lattice.** `capture_order_pricing.cpp` prices finite ordered Princess laws
   exactly in continuous time, with no \(1/(2n)\) loss, but the best finite law found so far is worth
   only 1.4137 ([NEXT_WORK.md](../../NEXT_WORK.md)).

## 5. Files

| File | Content | Status |
| --- | --- | --- |
| [ATOMIC_TWO_TURN_UPPER.md](ATOMIC_TWO_TURN_UPPER.md) | the upper bounds: laws, proof, computation, checks | proof plus exact computation |
| [REFINED_N1024_LOWER.md](REFINED_N1024_LOWER.md) | the lower bound and how far refinement and finer profiles can go | exact computation |
| [LIGHT_CONE_LATTICE_GAME.md](LIGHT_CONE_LATTICE_GAME.md) | the lattice game, its solver, the equilibria at \(n\le32\), the Princess family | numerical, plus the proof of \(U_n=L_n+1/(4n)\) |
| [ONE_TURN_INDIFFERENCE_EQUATIONS.md](ONE_TURN_INDIFFERENCE_EQUATIONS.md) | indifference equations of the one-turn game | derived for a stated support |
| [strategies.html](strategies.html) | a playground in the style of the vltanh.me playgrounds: hide from the Monster's plan in a live round, hunt the Princess's plan, explore both plans, and see the indifference above; open the file in a browser. `build_strategy_page.py --site DIR` writes the same page as the folder for vltanh.me/princess-monster-interval/ | illustration, rebuilt from the files above by `packages/interval_lightcone/build_strategy_page.py` |
| [packages/interval_lightcone](../../packages/interval_lightcone/README.md) | solvers, the exact upper-bound program, checks, laws | |
| [princess_front_n1024](../../packages/interval_discovery_certificates/princess_front_n1024/README.md) | the refined field and the engine records | |
