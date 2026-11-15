# One global minimax LP for a fixed monster bank

## Scope

This replaces princess-response sampling by one complete finite optimization
for a supplied finite bank of symmetric, finitely turning, unit-speed monster
pairs. Every pair completes an endpoint sweep. The princess remains
unrestricted. It does not prove that the finite monster bank is sufficient
for the unrestricted game's value.

The geometric input and legal limiting realizations are those of
`../interval_turn_density/ATOMIC_SURVIVAL_RESPONSE.md`. That theorem supplies
a finite lexicographic query array and nonnegative conjunction rewards for
every monster pair. `survival_minimax.py` optimizes the monster probabilities
and a complete mixed query response simultaneously.

## 1. A common order polytope

Let `b_(i,k)` be the bit saying that query value `P(V_i)` is at least label
`k`. Legal arrays satisfy the threshold-chain and time-order implications

    b_(i,k) <= b_(i,k-1),
    b_(i,k) <= b_(i+1,k),

together with fixed zero/one bits at physical bounds. Every above-survival
term is a nonnegative coefficient times an AND of positive bits. Every
below-survival term is a nonnegative coefficient times an AND of their
complements. Introduce one shared auxiliary per distinct conjunction:

* For a positive AND, `a <= b_j` for every constituent bit, and use reward
  `coefficient*a`.
* For a negative AND, `b_j <= a` for every constituent bit, and use reward
  `coefficient*(1-a)`.

Single-bit terms need no auxiliary. Empty conjunctions are constant.
All variables lie in `[0,1]`. Consequently the entire constraint set
consists of order inequalities and fixed bounds.

For each monster pair `m`, let `J_m(z)` be the resulting affine payoff.
Solve the linear program

    maximize c
    subject to c <= J_m(z) for every bank member m,
               z lies in the common order polytope.

This includes all lexicographic princess query arrays at once. It neither
samples princess trajectories nor alternates through selected response rows.

## 2. Exactness of the relaxation

For any feasible fractional point `z`, choose one common uniform random
number `r` in `(0,1)` and set every bit or auxiliary to `1[z_j >= r]`.
Every implication survives this thresholding. The expected value of each
Boolean coordinate is its original fractional coordinate, so the expected
affine reward in every monster row is exactly `J_m(z)`.

For each thresholded array, complete auxiliary bits to their actual
conjunction values. A positive auxiliary can only increase, and a negative
auxiliary can only decrease. Because every conjunction coefficient is
nonnegative, this raises every monster-row payoff simultaneously. Thus the
fractional solution is dominated by a finite distribution over genuine
lexicographic query arrays. At most one array is needed between consecutive
distinct coordinate values of `z`.

Conversely, any distribution over legal query arrays gives a feasible
fractional point by taking coordinate expectations, with auxiliaries equal
to the genuine conjunction bits. Its row payoffs are represented exactly.
The LP therefore equals the finite-bank maximin game.

Finite minimax duality supplies normalized nonnegative monster weights.
For these weights the original global survival cut independently computes
the supremum over every princess path. An exact feasible primal mixture
and exact dual law with equal value certify the finite-bank minimax.
The legal path realization theorem transfers every finite mixed query
response to an epsilon-approaching princess mixture against all members of
the fixed bank simultaneously.

## 3. What an exported lower strategy does and does not establish

The common-threshold decomposition is nested in query space. It is a
convenient complete representation for the *restricted* minimax LP. Its
canonical physical realization is not a proof that the same mixture is a
lower strategy against arbitrary monsters.

The event-query reduction lowers `P(V)` between queries to maximize the
supplied upper-law functional. When that interval carries no relevant
price, many other physical fills have the same upper payoff. Concentrating
on the canonical fill can concentrate the princess starting law near a few
chamber boundaries. A new monster can exploit those concentrations.

Accordingly:

* A matching LP primal/dual proves the value only for the supplied monster
  bank, with an unrestricted princess.
* An omitted-monster attack on one decomposed mixture rejects that mixture.
  It does not reject every point of the LP optimal face or every physical
  fill of the corresponding deadline corridors.
* Even the entire residual optimal cut face records query arrays. Its
  geometric continuum of zero-price fills remains relevant when seeking
  an unrestricted lower law.

The symbolic all-monster check in `germ_response.py` makes this distinction
concrete. The exact coarse fixture has restricted value
`219625051/152700512`, while its supplied canonical lower realization has
unrestricted response limit `108090289/152700512`. The latter is not a
bound on the full game's value.

## 4. Fixed experiments

The first executable fixture is a specified grid-four bank, deduplicated
after completed endpoint sweeps: 472 reflection pairs. It contains every
legal grid-four M1/M2 parameter, but its coarse M3 second turns and I first
inward turns are restricted to the nonnegative half. It is not an exhaustive
monster grid game. The targeting run separately adds broader signed M3/I
routes from the existing field data after checking their exact legality.
It has 7,438 variables and 15,923 order implications. The floating LP,
exact rational reconstruction, and independent rational global cut agree.

The next fixed bank adds the entire archived 67-pair upper support, for
531 pairs. Its complete floating minimax is approximately
`1.42824885534557`, independently matching the global cut. Only the old
67 M1/M2 pairs receive positive weights. Hundreds of coarse additional
M3 and I routes therefore do not resolve the missing geometry. This is
a structural diagnostic, not a new value-interval claim.

The targeted field-bank run additionally takes the named active routes
from `initial_inward_duals.json`, discards all old cost and structural
multipliers, and attempts to optimize actual normalized probabilities anew.
It contains 909 pairs, 254,755 variables, and 526,228 implications. The
default HiGHS attempt was stopped after approximately 8.8 minutes without
returning a solution. The same-bank interior-point fallback reached its
180-second LP time limit with no primal solution reported. No candidate
value or strategy is available from this attempted solve. The complete
status is `fieldbank_run_status.json`. No mesh refinement or game-completion
claim follows from this run.

## 5. Reproduction

Run from the repository root:

    python packages/interval_global_closure/survival_minimax.py --grid 4
    python packages/interval_global_closure/survival_minimax.py --grid 4 --archived-upper --output global_minimax_enriched.json
    python packages/interval_global_closure/survival_minimax.py --grid 4 --archived-upper --field-support --output global_minimax_field.json

The solver requires NumPy and SciPy. Its numerical outputs are discovery
artifacts. Exact reconstruction and global rational-cut verification are
separate executed checks; no Lean compilation or CI is invoked.
