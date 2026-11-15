# Global closure attempt: optimize and test whole strategies

**Exact global reductions (2026-11-13):**
[the horizon theorem](GLOBAL_EXACT_HORIZON_REDUCTION.md) fixes the
original game at Princess cutoff 3 and Monster completion 7, with an
almost-sure center deadline `2V` for every Monster optimum.
[The seven-state physical-clock lift](FINITE_STATE_PHYSICAL_CLOCK_LIFT.md)
makes the compact continuity-equation model sufficient as well as
necessary; its seven controls run for graph time 24.
[Finite certificate synthesis](FINITE_GLOBAL_CERTIFICATE_SYNTHESIS.md)
gives a full-game algebraic verifier for each supplied polynomial
template. **The optimal template's finite complexity and a matching
certificate pair remain unproved.** The continuous-measure LP is exact
but is not a finite LP. Both new exact-rational regressions passed.

**Latest audit:** [the bare Eulerian relaxation has exact value 1](EULERIAN_RELAXATION_GAP.md),
so its conservation laws cannot replace the common Monster/clock
trajectory lift. A second fake score of 5/4 survives the explicitly
listed scalar support and effort cuts. The physical pressure-matching
theorem is unchanged. The tight upper certificate and original lower
response have both been replayed natively; reflected quantile ties and
the Hall inequality have been repaired. See the
[updated handoff](../../HANDOFF_2026-11-13.md). **Exact equilibrium remains open.**

**New global pressure-matching result (2026-11-13):** [GLOBAL_CAUSAL_PRESSURE_MATCHING.md](GLOBAL_CAUSAL_PRESSURE_MATCHING.md) converts the complete unrestricted single-radius Princess oracle for any physically causal Monster/record-clock law into a **maximal partial transport** between positive and negative record-pressure measures. The matching relation is \((t,u)\preceq(s,v)\iff v\ge u+|s-t|\). The exact value is **baseline active mass + unmatched positive mass**; one can bound every Princess path by exhibiting a partial matching, with no Princess trajectory enumeration. For symmetric Monster laws this yields the exact all-game variational identity
\[
V=1+\min_{\nu,s}\bigl[\mathbb E_\nu(\sigma+B+I/2)+\mu_+(X)-\operatorname{Match}_\preceq(\mu_+,\mu_-)\bigr].
\]
The same note derives pathwise causal-clock backlog conservation \(\alpha=\sigma_{\rm occ}+\partial_t\beta+\partial_x k\), with explicit proof that these Eulerian equations are **necessary and, by the follow-up counterexamples, insufficient without further trajectory coupling** for a physical Monster/clock lift. Strict contact atoms are handled via an outward-germ supremum and the closed-order Strassen theorem. A byte-matched exact Fraction verifier passed 200 finite matching/closure instances, 1,875 queue identities and 27 two-sweep germ tests. **New global tradeoff:** let \(e=\mathbb E(\sigma+B+I/2)\) be Monster search effort and \(D\) the unmatched pressure mass. Every physical symmetric causal law satisfies
\[
D\ge\max\left(0,\frac12-\sqrt{2e}-\frac32e\right).
\]
In particular, exact pressure matching \(D=0\) requires \(e\ge(7-2\sqrt{10})/9\approx0.0750494\). This uses the previously established unrestricted sweep-stability inequality and does not impose any turn or mixing ansatz.

**No new numerical game bound or explicit equilibrium**; this is a new no-ansatz proof interface, not a claim that unmatched pressure vanishes or that timewise balance is optimal.

**Authoritative global handoff:** [root HANDOFF_2026-11-13.md](../../HANDOFF_2026-11-13.md) is the reviewed inventory of unrestricted results, exact current bounds, negative directions, all-count local theorems, verification provenance, and next coupled Bellman/CDF closure gates. The material below is a historical research narrative; in particular **abstract duality is established but explicit global equilibrium construction remains OPEN**.

**New 2026-11-13 whole-game G2 cut: nonzero macroscopic Monster completion lateness.**
The global dual minimizing Monster law must satisfy
\(\mathbb E[\tau_{\pm\,\mathrm{both}}-2]
 \ge 0.0090511656481067\ldots>181/20000\),
uniformly over ANY number of Monster reversals.
The proof uses fastest-sweep rigidity plus an entire continuum
of legal Princess runner offsets; its physical-response
lower envelope is convex, so Jensen closes the constraint for
arbitrary Monster probability measures. This eliminates
a global neighborhood of infinitesimal sweep-geometry
updates, NOT a finite turn family. Every optimum also obeys
\(0.00452558\ldots\le
 \mathbb E[\sigma+B+I/2]\le0.42612972\ldots\).
[Complete proof](GLOBAL_SWEEP_STABILITY_ENERGY_BARRIER.md) |
[Exact regression](../../packages/interval_global_closure/verify_global_sweep_stability.py).

**Do not confuse this with constructive closure.** The actual G2
task is still a matching explicit transport CDF and legal
Monster/clock occupation whose global radial HJB upper
and unrestricted Monster Bellman lower coincide.
Neither an exact value nor a finite phase classification is known.

**Current global proof handoff — attained INFINITE-HORIZON one-clock dual and singular contact-germ gate (2026-11-12):**
The actual unrestricted value has an exact **attained** strong dual over
a symmetric Monster law on entire paths and ONE nondecreasing backward
record clock per path, with finite active occupation of mass at most V.
No finite turn, path support, or time horizon is assumed. Symmetry
reduces the Princess upper oracle to a single legal radius trajectory.
An optimal dual can be normalized to two fastest endpoint sweeps plus
genuinely precompletion-reversing trajectories. The sweep occupation
is an explicit characteristic measure; only the reversing-history
pressure remains unknown.

- [Global unrestricted active-record dual and proof](GLOBAL_INFINITE_HORIZON_ACTIVE_DUAL.md)
- [Finite-horizon strong duality and exact radial oracle](GLOBAL_STRONG_RECORD_DUALITY.md)
- [Causal stochastic time-order equals monotone backward clock](GLOBAL_MONOTONE_CAUSAL_CLOCK.md)
- [Exact order-one strict contact germs and free-flow singular-pressure exclusion](GLOBAL_RADIAL_CONTACT_GERMS.md)
- [Exact causal-selector LP regression](../../packages/interval_global_closure/verify_global_strong_record_duality.py)
- [Exact monotone-clock / continuous sweep regression](../../packages/interval_global_closure/verify_global_monotone_clock.py)

**A matching optimal Princess CDF, explicit Monster/clock law, and the
exact numerical game value remain OPEN. The old unrestricted value
interval is unchanged.** No Lean compilation/CI.

**Latest G2 handoff — two complete bad Monster update rays eliminated:**
[rigorous near-active Princess germ and continuum ray theorem](G2_NEAR_ACTIVE_GERM_SEPARATION.md).
A four-column exact physical Princess bank has 2,248 certified
oriented first contacts, and the source-file-based independent
[cut verifier](../../packages/interval_global_closure/verify_g2_princess_cuts.cjs)
and [all-ray verifier](../../packages/interval_global_closure/verify_g2_ray_exclusions.cjs)
pass in V8. Both (i) every mix of the old 280-pair Monster law
with its archived Princess-best-response Monster route and (ii)
every transfer from original atom 0 to atom 120 are rigorously
ruled out as ways to beat the existing best exact global upper
\(1.426129722845311...\).
The [fast exact rejection screen](../../packages/interval_global_closure/g2_princess_cut_screen.cjs)
is reusable for other weights on the fixed 281-route bank.
This is **not** an equilibrium result; G2–G5 remain open.


**Exact G1b first-variation closure, 2026-11-12:** the full
strict/closed history-record CDF payoff has an exact direction
derivative given by near-active record slopes even with atoms,
ties, or Zeno routes. The resulting variational inequality plus
a global Monster response lower bound is an exact two-sided
saddle criterion. See
[GLOBAL_CDF_VARIATIONAL_STATIONARITY.md](GLOBAL_CDF_VARIATIONAL_STATIONARITY.md)
and [the exact fixture](../../packages/interval_global_closure/verify_cdf_record_variation.py).
This is an analytical characterization, *not* an explicit equilibrium.


**New global theorem, 2026-11-12:** the unrestricted Princess
security supremum equals the Monster mixed minimax, and the optimal
Monster law is attained on the compact trajectory space. The
uniform horizon/rank theorem also gives an explicit global
\(6/H+(H+3)/(2n)\) game-value approximation width, without
assuming endpoint-absorbed Princess laws or any finite Monster
turn cutoff. See
[GLOBAL_MINIMAX_AND_CDF_DUALITY.md](GLOBAL_MINIMAX_AND_CDF_DUALITY.md).
This closes the **abstract G1 minimax/existence gate**, not any
numerical value or the constructive G2–G5 equilibrium gates.
The Princess optimizer may not be attained and no explicit
optimal Monster trajectory distribution is presently known.


Date: 2026-11-11.

**The unrestricted proof remains open. No global minimax gate G5-G8 is
closed.** The later [constructive upper checkpoint](EXACT_UPPER_CHECKPOINT.md)
resolves the finite-bank solver bottleneck and supplies a normalized
280-pair law with exact unrestricted response
`957063215727541539/671088640000000000`, together with an actual princess
response within `1.91e-8` of that supremum. The older experiments below
retain their original scope and completion status.

The continued [whole-CDF exchange](CONTINUUM_EXCHANGE.md) now includes
complete native M2 and initial-inward families and a physical response
search without a turn-count cutoff. [Adaptive record refinement](CONTINUOUS_RESPONSE.md)
resolves the remaining record-interpolation error on a supplied node graph;
the continuum response certificate remains a separate obligation.
[Center waits can be replaced by unit excursions](CENTER_WAIT_UNITIZATION.md)
for the upper law. These general constructions are used in both strategy
searches rather than adding isolated local response constraints.

The current direction is to construct and verify a matching pair, using
computer assistance, rather than accumulate increasingly local response
lemmas. This checkpoint solves complete finite upper-support optimizations
and tests their actual lower counterparts globally. Two natural lower
constructions fail by large, exact margins. They are stopped here.

## What is completed

### 1. One optimization for an entire finite monster bank

For any supplied finite bank of symmetric unit-leg monster routes completing
both endpoint visits, the common survival-query order polytope gives one LP
for the exact minimax against **every princess path**. It optimizes normalized
monster probabilities and a mixed query response together. No sampled
princess-response list is assumed exhaustive.

The proof is a common-threshold decomposition of the implication polytope;
completing conjunction auxiliaries increases every monster-row payoff.
See [the minimax theorem](../../packages/interval_global_closure/SURVIVAL_MINIMAX.md).
The implementation also accepts arbitrary complete unit-leg paths, without
requiring a named M1/M2/M3/I template.

The 472-pair coarse fixture has an exactly reconstructed primal/dual value

    219625051/152700512 = 1.4382731801187412...

with eight positive monster pairs and nine positive princess query
components. All 472 rational lower rows and the separate global rational
cut agree. This is a test of the complete method, not a proposed full-game
value or an improvement of the existing game bounds.

Adding the archived 67-pair support yields a 531-pair bank. Its floating
optimum, independently checked by the global cut, is approximately
1.42824885534557; only the old 67 M1/M2 pairs receive mass. The broad coarse
extensions therefore do not repair the missing geometry.

### 2. A uniform exact test of approaching lower strategies

For a specified finite ordered princess family with rational-function
coordinates in epsilon, the unrestricted monster-response minimum is a
rational function on a sufficiently small positive epsilon interval.
Exact capture-order search supplies the function, an attaining route, and
a common rational validity radius. Monsters may themselves depend on
epsilon. This avoids substituting epsilon=0 into discontinuous capture
times or confusing a fixed-epsilon test with a uniform limiting guarantee.

For the coarse canonical lower realization, the completed search gives

    lim_(epsilon -> 0+) inf_m E T(m,P_epsilon)
        = 108090289/152700512 = 0.7078580653351051...

An attaining monster starts just above 3/4 and runs left, with no interior
turn. The full formula and radius are in [the germ response proof](GERM_RESPONSE.md).
The larger canonical realization has a separately verified straight-sweep
attack with limit about 0.7976998219. Neither number is a bound on V.

### 3. A diffuse replacement also fails as a whole

Replacing each extreme coarse response by a uniform blend of its lower and
upper deadline envelopes removes the initial atoms and preserves its
active-upper-support deadlines. A fixed monster starting at -15/16 and
sweeping right then left nevertheless yields

    limsup_(delta -> 0+) E T
       <= 34192713983279/29347816802304 < 7/6.

The inequality holds for **every legal coupling of these time marginals**,
including their ordered quantile coupling. The proof uses a
coupling-independent first-sweep CDF integral and a two-unit completion
bound, with exact rational logarithm bounds. The limiting argument checks
all collapsed first-sweep envelope pieces and does not assume continuity
of full first-capture time.

See [the uniform corridor exclusion](UNIFORM_CORRIDOR_EXCLUSION.md).
This excludes that entire supplied construction, not every possible
nonuniform or time-dependent filling of the same corridors.

### Bounded computation that did not finish

One fixed targeted bank combined the prior named active field routes with
the earlier bank: 909 pairs, 254,755 LP variables, and 526,228 order
implications. Default HiGHS was stopped after approximately 8.8 minutes
without a solution. The same-bank interior-point fallback reached its
180-second LP limit with no primal solution. There is no candidate value,
normalized strategy, or certificate from this run. Its complete status is
saved in
[`fieldbank_run_status.json`](../../packages/interval_global_closure/fieldbank_run_status.json).
No further banks or parameter grids were added.

## What these results do not establish

The exact response face of a finite upper law is a face of query profiles.
It is not already the full space of useful physical lower realizations.
Equilibrium construction must choose the distribution within the available
trajectory corridors and the dependence between positions at different
times. A canonical query realization, or a uniform constant blend, can
perform well against the upper support and very poorly against a missing
monster.

The LP does not prove that a fixed finite monster bank contains an optimal
law. The germ theorem does not prove that a matching finite approaching
princess family exists. The corridor exclusion does not prove that finite
support is impossible. None of those missing existence statements is
silently assumed.

## Closing condition and stopping rule

The only full-game closing condition remains one exact constant c and
actual laws satisfying

    sup_p E T(M,p) <= c,
    inf_m E T(m,P_epsilon) >= c-o(1), uniformly in m.

The next mathematical result must supply a globally compatible lower
construction and its matching upper law, or a proved sufficient equilibrium
class. Do not resume either rejected lower construction by repairing a
sequence of local starts or turns. A larger list of checked response
families, a better decimal, or a fixed-bank saddle alone is not this result.

## Executed verification

- Exact finite-bank primal/dual reconstruction and separate rational
  global-cut equality.
- Six symbolic response fixtures, pruned/unpruned agreement, 108 independent
  rational capture-order permutations, comparison with the pre-existing
  exact oracle, and 18 independent physical captures for the coarse law.
- 283 exact generic unit-route checks, including named-template embeddings,
  physical limiting realizations, and invalid-route rejection.
- Exact corridor deadline equalities and logarithm bounds, 74 collapsed
  first-sweep pieces, two independent integration methods, and 1,152 exact
  physical midpoint captures.

The new Python checks were executed in this continuation. Earlier V8
certificates and their historical outage qualifications remain preserved.
No Lean compilation or CI was run. The numerical optimization and exact
certificate stages remain explicitly distinguished.

