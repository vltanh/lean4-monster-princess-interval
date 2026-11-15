# The value of the game: our attempt

The paper proves $15/11\le V\le 13/9$, that is $1.3636\le V\le 1.4444$, and conjectures $V=1.4$. This
folder records our attempt to find $V$. It does not find it. It narrows the bracket to

$$
\frac{9322984150699}{6553600000000}=1.4225745\ldots\ \le\ V\ \le\ \frac{1603303881142469}{1125899906842624}=1.4240199\ldots,
$$

a width of $0.0014454$, against $0.0808$ in the paper. Both bounds are above $1.4$, so if they hold,
the conjecture $V=1.4$ is false. This needs only the lower bound. Even our older lower bound
$1.4222581$, which has the most checking of all (Section 1), is enough.

**Nothing in this folder is formalized in Lean, and no one outside the project has reviewed it.** Each bound is a written argument
that reduces it to one exact integer computation. The programs and certificates of those
computations are in [`code/`](code). The table in Section 1 says how far each bound has been
checked. The Lean formalization of the paper is the rest of this repository and does not depend on
anything here. The dependence goes the other way at one point, below.

The game is the one of the paper. Both players choose hidden paths in $[-1,1]$ with free starts: the
Monster with speed at most 1, the Princess with continuous paths. The payoff is the first time they
coincide. By the paper's Proposition 3, every Princess path is dominated by one of speed at most 1:
each Monster path meets the original no later than the faster path. The formalization proves this
for every continuous path
([`proposition3_of_continuous`](../PrincessMonsterInterval/AlpernEtAl2008/Section2/Dominance.lean#L512)).
So the notes below take both players' paths to be 1-Lipschitz. Throughout, $U=t+x$ and $W=t-x$ are light
coordinates. In them a 1-Lipschitz path is a monotone curve, a unit-speed path is a staircase, and
two players meet where their curves cross. That change of coordinates is what makes the
computations below exact.

An interactive page shows both strategies. You can hide from the Monster's law in a live round, hunt
the Princess's field, and see how each nearly equalizes the other's options:
[vltanh.me/princess-monster-interval](https://vltanh.me/princess-monster-interval/). To build it
locally, run `python3 research/code/interval_lightcone/build_strategy_page.py`, which writes
`research/strategies.html`.

## 1. Bounds

| Bound | Value | How it is verified | Not done |
| --- | --- | --- | --- |
| Lower | $V\ge 36409808231/25600000000 = 1.4222581340$ | written proof plus an exact integer computation: a Princess field on the grid $n=512$, priced by two native engines and by an independent BigInt replay ([LOWER_BOUND.md](LOWER_BOUND.md)) | review, Lean |
| **Lower** | $V\ge 9322984150699/6553600000000 = 1.4225744859$ | the same proof; the field refined to $n=1024$, where the two native engines return the same minimum ([LOWER_BOUND.md](LOWER_BOUND.md)) | independent BigInt replay (expected to take several hours), review, Lean |
| **Upper** | $V\le 1603303881142469/1125899906842624 = 1.4240199075$ | written proof plus an exact integer dynamic program. C++ and NumPy programs return the same integer. Small cases are checked by exhaustive enumeration and by exact-fraction trajectories ([UPPER_BOUND.md](UPPER_BOUND.md)) | independent review, Lean |
| Upper, one-turn class | $W_1\le 25661865897887875/18014398509481984 = 1.4245197187$ | same proof; C++ program at $N=4096$, both programs agree up to $N=2048$ | as above |

$W_1\ge V$ is the value when the Monster may turn at most once before it first reaches an endpoint and
then sweeps. Our earlier bounds, $1.4222581\le V$ and $V\le W_1\le 1.4247235$, came from the first row
and from an exact potential certificate for a continuous one-turn law
([archived](archive/research/13-equilibrium-geometry/ONE_TURN_SEPARATION_COUNTERCERTIFICATE.md)).

**Estimates, not bounds.** From the Monster's side, the best laws of the two families below on the
grids $1/1024$ and $1/2048$ extrapolate to about $1.42397$. From the Princess's side, the best
profiles on the grids $1/16$, $1/32$ and $1/64$ have limits $1.41908$, $1.42156$ and $1.42274$, about
$0.078/k$ below the same number. Both point to $V\approx1.4240$, close to the upper bound and about
$1.4\cdot10^{-3}$ above the lower bound.

## 2. The strategies

### Monster

The law behind the upper bound,
[atomic_law_32bins_grid2048.txt](code/interval_lightcone/atomic_law_32bins_grid2048.txt), is
symmetric: each path is played together with its mirror image. Masses:

| Family | Path | Mass |
| --- | --- | ---: |
| sweep | from one endpoint straight to the other | 0.6228 |
| $S(a)$, $a>0$ | to the near endpoint $+1$, then across to $-1$ | 0.1728 |
| $P_1(a)$, $a>0$ | right until $t+x=1$, left to $-1$, right to $+1$ | 0.0962 |
| $P_1(-c)$, $c>0$ | the same, started on the far side | 0.0664 |
| $S(-c)$, $c>0$ | through the centre to $+1$, then to $-1$ | 0.0297 |
| $P_b(\pm a)$, $b$ near 1 | one turn at a level $t+x=b$ just off 1 | 0.0072 |
| $T_2(c,U_1)$ | out to $t+x=U_1$, back until $t-x=1$, then the sweep from $-1$ | 0.0050 |

Start positions are spread over 32 bins of width $1/32$ with piecewise-constant densities. The
two-turn paths start mostly near the centre and join the sweep that left $-1$ at time 0. They are
worth about $3.9\cdot10^{-4}$: with one-turn paths alone the best law of the same form has limit
1.42449.

On the lattice the unrestricted Monster also uses paths that loiter near the centre for a while
before sweeping (0.2% of the weight at $n=16$). They are not in the two families, and they are why
a Princess law optimized only against one-turn and two-turn Monsters loses $7\cdot10^{-3}$
([LATTICE_GAME.md](LATTICE_GAME.md), Section 7).

### Princess

The Princess plays an **ordered** law: a symmetric radial CDF $G(t,r)$, each radial rank $q$
following the level curve $G=q$ on a random side. The field behind both lower bounds is the
full-width interpolant of a profile on the grid $1/64$
([princess_front_n512](code/interval_discovery_certificates/princess_front_n512/README.md)), refined
to $n=1024$ for the second. Read off its rank curves:

- the innermost ranks, $q\lesssim0.2$, reach the centre and wait there until time 1;
- ranks up to $q\approx0.7$ pass within 0.005 to 0.03 of the centre at about $t=0.9$;
- ranks from 0.75 to 0.85 turn back at radius 0.1 to 0.2, just before time 0.9;
- the top ranks come in only to about radius 0.64;
- most ranks first run **outward**, by up to 0.04, and after time 1 every rank runs out to the
  endpoint.

On the lattice the Princess's optimum is reached to within $4\cdot10^{-5}$ by a three-parameter
family: "out for a time $\sigma$, in, wait at the centre if reached, out, stay". Dropping the
outward run costs $2.8\cdot10^{-3}$ ([LATTICE_GAME.md](LATTICE_GAME.md), Section 7).

### Indifference

The two laws were found separately, so they are not an exact saddle pair, but each nearly equalizes
the other's options:

- Against the Monster law, the Princess's best payoff (computed by `atomic_upper.cpp` on the grid
  $1/2048$) is within $10^{-4}$ of its maximum from 99.3% of starting radii. It is within
  $1.2\cdot10^{-4}$ from all of them. Her best-response paths go through the same phases as her
  own field.
- Against the Princess field (lattice cost on the time grid $1/1024$), 96% of the Monster law's
  probability is on paths within $2\cdot10^{-4}$ of the cheapest path, and 99% within $10^{-3}$. The
  mass-weighted mean excess is $1.7\cdot10^{-4}$. The rest sits at the edges of a few start bins.
  Paths the law never uses cost $10^{-3}$ to 0.4 more.

The linear relations behind this, such as $\rho(c)=e/(7-c)$ and $(7+a)p(a)+(1-a)s(a)=e$, are
derived in [INDIFFERENCE.md](INDIFFERENCE.md) for the support seen numerically. They do not yet
cover the layer before time 1 or fix the thresholds.

## 3. Structural findings (numerical)

- One interior turn is nearly enough for the Monster. On the lattice the restriction costs
  $1.7\cdot10^{-4}$, $7.9\cdot10^{-5}$, $5.2\cdot10^{-5}$, $2.2\cdot10^{-4}$ and $2.2\cdot10^{-4}$ at
  $n=4,8,16,24,32$. The gap does not shrink, so there is no evidence for $W_1=V$.
- Turn levels just off $b=1$ matter. With only $b=1$ and $b=2-a$, the continuum one-turn value stays
  near 1.4254.
- An upper-bound law is tied to the grid it was optimized for and gets worse on finer grids. A law
  taken from the continuum improves with the grid. A lower-bound field behaves the same way: the bank
  minimum of a fixed field exceeds its limit by about $0.18/n$.
- The lattice optimum of one grid is a poor seed for the lower-bound computation. Its interpolant
  prices near 1.412, because the optimum uses the lattice to stay one step ahead of a sweep.

## 4. What did not close the gap

- **Refining the Princess field.** A fixed field gains less at each doubling of the grid. The
  field behind the lower bound is worth at most about 1.4229 on any grid: $n=2048$ would give about
  1.42273. Going higher needs a better field.
- **Finer profiles.** The profile optimizer reaches the grid $1/64$ in about 20 minutes when it is
  seeded from the next coarser solution. At $1/128$ its first linear program takes 6.5 minutes, and an
  hour-long run did not improve its seed ([LOWER_BOUND.md](LOWER_BOUND.md)).
- **Better Monster laws in the same families.** On the grid $1/N$ the optimum is about $V+0.08/N$,
  so a law optimized for $1/4096$ would gain at most about $5\cdot10^{-5}$.
- **Pricing without a lattice.** `capture_order_pricing.cpp` prices a finite ordered Princess law
  exactly against every continuous Monster, with no $1/(2n)$ transfer loss. The best finite law
  found so far is worth only 1.4137, and laws drawn from a lattice field lose about $0.04/M$ on $M$
  shifted copies.
- **An analytic description of the equilibrium.** The archive's notes contain partial results.
  They have not been rechecked for this summary:
  - an optimal Princess law cannot have finitely many starting positions
    ([note](archive/research/12-global-closure/FINITE_INITIAL_SUPPORT_NONATTAINMENT.md));
  - a Princess CDF that is convex in both light coordinates throughout the inner region up to
    $U=41/40$ lets the sweep cost less than $1137/800=1.42125$, so a competitive field must change
    shape earlier ([note](archive/research/12-global-closure/POSITIVE_PREFRONT_RESPONSE_AND_MODULUS.md));
  - against some Princess laws every optimal Monster response must reverse infinitely often (a
    low-value example, not an equilibrium;
    [note](archive/research/12-global-closure/GLOBAL_FREE_START_ZENO_COUNTEREXAMPLE.md));
  - pushing a Princess law onto a simpler "front-one" form can lose value, from $47/40$ to $469/400$
    ([note](archive/research/12-global-closure/FRONT_ONE_PROJECTION_SECURITY_LOSS.md)).

  None of them identifies the phases of an optimal Princess CDF or the Monster paths that support
  it, and that is the missing step.

## 5. Open problems

1. **The lower bound, the larger part of the gap.** A profile on a grid finer than $1/64$. By the
   $0.078/k$ law, a grid-128 profile should certify about 1.4231 at $n=1024$.
2. **An independent replay of the $n=1024$ lower bound** with `verify_bigint.cjs`. It takes 17
   minutes at $n=512$ and is expected to take several hours at $n=1024$.
3. **The upper bound.** Add the loitering paths of Section 2 to the Monster's families.
4. **Is $W_1>V$?** A Princess law that guarantees more than 1.42402 against every one-turn Monster
   would prove it.
5. **The exact solution.** Complete the indifference equations with the layer before time 1, the
   two-turn paths and the thresholds.

## 6. Files

| File | Content | Status |
| --- | --- | --- |
| [UPPER_BOUND.md](UPPER_BOUND.md) | the upper bounds: laws, proof, computation, checks | proof plus exact computation |
| [LOWER_BOUND.md](LOWER_BOUND.md) | the lower bounds: the Princess field, why its price bounds $V$, the computation, how far refinement and finer profiles can go | proof plus exact computation |
| [LATTICE_GAME.md](LATTICE_GAME.md) | the lattice game, its solver, the equilibria at $n\le32$, the Princess family | numerical, plus the proof of $U_n=L_n+1/(4n)$ |
| [INDIFFERENCE.md](INDIFFERENCE.md) | indifference equations of the one-turn game | derived for a stated support |
| [code/interval_lightcone](code/interval_lightcone/README.md) | the exact upper-bound program and its checks, the laws, the lattice solvers, the strategy page | |
| [code/interval_discovery_certificates](code/interval_discovery_certificates) | the Princess fields at $n=512$ and $n=1024$ and the engine records | |
| [code/interval_clock_grid](code/interval_clock_grid), [code/interval_center_pricing](code/interval_center_pricing) | the two native pricing engines and the BigInt replay | |
| [archive/](archive/README.md) | the whole research repository as it stood on 2026-11-15: every note from 2026-11-10 on (`archive/research/01-…` to `14-…`), every package and certificate, and the earlier handoffs | archive, not maintained |

Requirements: Python 3 with NumPy and SciPy, a C++17 compiler with OpenMP, and Node.js for the
BigInt replay.

## Credits

As for the formalization, the computations, the proofs and the write-ups were done by Claude
(Anthropic) agents at the maintainer's direction, from 2026-11-10 to 2026-11-15. The maintainer is
The-Anh Vu-Le.
