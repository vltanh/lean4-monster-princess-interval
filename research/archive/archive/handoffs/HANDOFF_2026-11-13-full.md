# Handoff — unrestricted interval Princess–Monster game

## Constructive finite strategies and exact grid optima — 2026-11-13

The [constructive dual theorem](research/12-global-closure/CONSTRUCTIVE_PRINCESS_GRID_DUAL.md)
turns a rational finite-grid dual into a legal symmetric Princess law with
a finite rational piecewise affine CDF, sticky endpoints, and outward motion
after time 2. For rational \(0<\varepsilon\le1/2\), its security is at least

\[
U_n-\frac1{2n}-\frac{\varepsilon}{2n}.
\]

One shared random threshold preserves the physical light-coordinate order;
a positive threshold width removes capture atoms introduced by deterministic
rounding. The proof fixes the old minimizing clocks before sampling the
threshold. It does not assume unbiased rounding. Together with the finite
Monster primal, this gives explicit strategies for both players with a
certified gap tending to zero.

The [executable clock-grid package](packages/interval_clock_grid/README.md)
now contains exact witnesses for

| Grid | Exact \(U_n\) | Complete credit DAG nodes | Independent record states |
|---|---:|---:|---:|
| 1 | \(47/32\) | 3,221 | 261 |
| 2 | \(4893/3376\) | 64,271 | 2,522 |
| 3 | \(3153038167/2187120435\) | 321,175 | 9,651 |

For every row, both the complete credit graph and a separate physical-path
running-minimum algorithm replay the exact primal/dual equality using integer
arithmetic. The package also extracts actual Princess fields, evaluates their
CDFs exactly, and regenerates the saved fields from the verified duals.
The independent interpolation regression passes 6,060 map checks, 8,460
physical-coordinate checks, 12 buffer integrals, 2,472 CDF checks, and
1,800 affine-patch checks.

These coarse enclosures and example Princess strategies do not improve the
retained numerical interval. **They do not identify the exact unrestricted
value or prove finite exact termination.** The remaining task is a sharp
global pair of certificates with the same constant.

### Runtime recovery and remaining implementation checks

The local compute environment remains unavailable. The complete new finite
reduction, constructive proof, exact grid witnesses and portable source files
have been preserved directly in this branch. A focused CI workflow is included
to perform native Python, Node and C++ checks. Until the first CI result is
inspected, the new integer-lattice verifier and exact sampler retain their
explicit draft status. The sampler is separate from the standard-library
exhaustive C++ regression.

The [off-grid recovery note](research/12-global-closure/OFFGRID_RESPONSE_RECOVERY_NOTE.md)
preserves the two previously checked counterexample payoffs and routes.
Their complete nodal arrays and original executables were not recovered; that
note is a historical recovery aid, not a self-contained certificate.

## Effective global finite reduction — 2026-11-13

For every integer \(n\ge1\), an explicitly specified rational linear program
has value \(U_n\) satisfying

\[
\boxed{U_n-\frac1{2n}\le V\le U_n.}
\]

The [common-quantization proof](research/12-global-closure/EFFECTIVE_FINITE_UPPER_REDUCTION.md)
applies one odd, monotone, translation-compatible nearest-grid map to
every physical event and every pressure-matching edge. A symmetric clock
buffer of mass \(1/(2n)\), followed by chronological truncation, restores
causality. This gives an explicit global error estimate; it does not
assume continuity of the worst capture payoff under independent path rounding.

The [two-clock occupancy construction](research/12-global-closure/POLYNOMIAL_CLOCK_GRID_LP.md)
compresses the complete path bank to \(O(n^4)\) states, control arcs and
matching variables. Integer clock calendars are attached jointly to the
same physical path, and acyclic flow decomposition reconstructs a genuine
finite rational Monster law. Every exact LP optimum therefore gives an
unrestricted enclosure of width \(1/(2n)\). Dyadic refinement satisfies
\(U_{2n}\le U_n\).

The independent exact quantization regression passed 3,615 map identities,
32 clock repairs, 18 early endpoint cases, 56 simultaneous-jump fills,
11 cases requiring the full buffer, 400 matching containments, 15 collapsed
targets, and four joint two-clock calendar examples. This is an effective
finite approximation theorem. A fixed finite instance with value exactly
\(V\), matching optimal strategies, and a Lean proof remain unresolved.
The retained portable numerical interval is unchanged.

### Unpublished numerical checkpoint and interrupted computation

Before the compute environment became unavailable, an adaptive 248-pair
Monster law and a common light-coordinate warp passed exact unrestricted
upper-response recomputation and standalone integer-flow replay. The best
checked fraction was

\[
\frac{3737996014967678948542039107069869967977571}
 {2621440000000000000000000000000000000000000}
=1.4259323177214351\ldots.
\]

Its complete witness was left at
`global_cdf_work/upper_multiturn/cert_warp_round3.json.gz` in the
unavailable scratch workspace (1,199,002 bytes; SHA256
`7951c31dc21ee373ccf1007f35ef9f8b7872372fc90b7636e8eb8dfed1bc403a`).
The separate replay checked 86,503 nodes, 218,944 arcs and 94,863 positive
flow entries, with 496 orientations, 1,020 vertices and 772 physical legs.
The full atoms and witness were not uploaded before the outage.
**This is a pending recovery/reproduction checkpoint, not the published
portable upper certificate.** The headline interval continues to use
the reproducible committed upper \(1.4259991274612613\ldots\).

The all-turn CDF discovery and exact integer-lattice lower-verifier work
were also interrupted. Recent finite-bank scores are not global lower
bounds. Earlier checks found both one-turn and two-turn attacks on high
bank-scoring fields. No improved Princess lower bound is claimed.

## Two-run interior response and sticky endpoint density — 2026-11-13

The [two-run continuation theorem](research/12-global-closure/TWO_RUN_AFFINE_CELL_WITH_CONTINUATION.md)
strengthens the fixed-field reduction. When the entire future path is
included, its cost is concave and nonincreasing in the two captured rank
extents. In an affine interior cell, one of the two unit-speed orders
(right then left, or left then right) is therefore at least as good as
any local path with the same physical entry and exit. Boundary half-cells
retain the proved five-piece rule. The rigorous combined response bound
is `2 K_int + 5 K_bd + 1`; the finite rational quadratic-program
reduction remains valid. A uniform two-piece boundary rule and a grid-only
response theorem are not assumed.

[First-endpoint stopping](research/12-global-closure/STICKY_CDF_DENSITY.md)
weakly increases every Princess capture time. The added constraint that
the positive endpoint CDF trace never increases is globally value-preserving.
A stopped radial dither gives regular sticky CDFs that are still value-dense;
characteristic interpolation and rational quantization preserve this order.
It is compatible with forcing outward motion at time 2 and absorption at 3.

The new exact standard-library regression checks 4,840 directional words,
1,200 concave continuation costs, 26 polytope vertices, 12 Hessian entries,
and 12 terminal-excursion identities. The unrestricted numerical bounds
remain unchanged. These results do not yet specify the global equilibrium
or a finite mesh containing an optimal Princess field.

## Sharper horizons and an exact finite response reduction — 2026-11-13

The [sharp outward-time theorem](research/12-global-closure/SHARP_OUTWARD_HORIZON_REDUCTION.md)
proves `S(outward_T(mu)) >= min(S(mu),(T+1)/2)`. If the Monster has not
visited the center by T, the opposite fair half cannot be caught before
the opposite endpoint, at time at least `T+1+abs(m(T))`. Thus forcing
Princesses outward after **2** preserves unrestricted security, and every
optimal Monster law satisfies `tau_center <= 2V-1` almost surely.
Some global optimal Monster completes both endpoints by **6**. The
protected-turn full-matching normal form consequently completes by **8**
while retaining center visitation by 2. The absorbed-by-3 potential
hierarchy is now globally complete; its statewise future-credit bound
remains 7, which is a different normalization.

For each supplied rational characteristic P1 CDF, the
[four-leg affine-cell theorem](research/12-global-closure/FOUR_LEG_AFFINE_RECORD_RESPONSE.md)
and [boundary projection corollary](research/12-global-closure/BOUNDARY_CELL_RECORD_PROJECTION.md)
prove an exact finite Monster response reduction. In a cell, at most four
speed-one legs and one constant-CDF leg suffice, preserving both exit
records. Concavity in partial record turns gives just four explicit local
candidate tours. If K counts the affine cells through absorption time+2,
some unrestricted best response uses at most `5K+1` pieces. Its value is
the minimum of finitely many rational quadratic programs and is rational.
Strict endpoint contact is included through both CDF traces.

The exact horizon regression passes 72 physical cases; the affine-cell
regression checks chronological first visits, the full negative-definite
quadratic form, 23 rational polytope vertices, and a counterexample showing
three directional legs are insufficient. These are fixed-field finite
response and global time-reduction theorems. **They do not bound the mesh
of an optimal Princess CDF or evaluate the game value.** The current
rigorous numerical interval is unchanged.

## Complete finite lower-certificate hierarchy — 2026-11-13

The [analytic-exit potential theorem](research/12-global-closure/ANALYTIC_EXIT_POTENTIAL.md)
reduces a supplied Princess CDF to one potential on four state coordinates:
physical time, position, and the two actual clock credits. First-endpoint,
queue-cap, and endpoint-absorption continuations have explicit exact formulas.
On rational characteristic and queue meshes, every control and boundary
condition is a finite rational linear inequality.

The [completeness proof](research/12-global-closure/FINITE_POTENTIAL_HIERARCHY_COMPLETENESS.md)
establishes that, with absorption horizon 3, **every rational c<V has a
finite rational certificate of this form**, and the supremum of the
hierarchy is V. It proves statewise Lipschitz continuity, smooth strict
subsolution approximation, exact legal CDF approximation, and density at
the unrestricted value. This is approximation completeness; it supplies
neither a finite termination bound nor an exact equilibrium certificate.

A standalone standard-library verifier independently rebuilds the exact
geometry and checks 105,733 analytic inequalities and 804 direct tail
integrals for a coarse certificate at `2677462523/2000000000 = 1.3387312615`.
It does not trust floating LP rows or a reconstructed coefficient lattice.
Closed-form fixtures and an intentionally invalid endpoint potential also
pass their acceptance/rejection checks. This validates the operational
certificate method; the retained stronger lower and upper bounds are unchanged.


## Current numerical checkpoint — full ordered-CDF upper

The strongest exact upper is now
`1140799301969009059644426513/800000000000000000000000000`
(`1.4259991274612613...`), with the previous lower unchanged.
[Complete statement and verifier](research/12-global-closure/FULL_ORDER_CDF_UPPER_CERTIFICATE.md).
The rational law has 241 reflected pairs. Its exact unrestricted response
was recomputed and replayed successfully; its discovery CDF has no claimed
unrestricted lower guarantee. The earlier checkpoint paragraphs below
retain their historical bounds. The finite horizon and physical-lifting
theorems remain applicable. The game is still open.

The same U now has an independent actual-clock certificate and an explicit
continuum Monster realization with zero matching deficiency. See
[finite bank homogenization](research/12-global-closure/FINITE_BANK_CLOCK_HOMOGENIZATION.md)
and [front completion](research/12-global-closure/ENDPOINT_FRONT_DEFICIENCY_COMPLETION.md).
The standalone replay passed 85,268 causal-prefix checks and 12,214 exact
order-flow edges. The finite seed's entire deficiency D lies on the sweep
front; replacing sweep probability D/2 by the specified uniform B_h family
raises its endpoint baseline by exactly D and matches all positive
pressure. Its exact worst-case value is U, attained by stationary
endpoints. Neither those endpoints nor the discovered finite-bank CDF
have a matching unrestricted Princess lower guarantee.

## Attained global reduction to fully matched physical pressure — 2026-11-13

The [attained global normal form](research/12-global-closure/GLOBAL_ZERO_DEFICIENCY_ATTAINMENT.md)
proves

\[
V=\min\{\mathbb E_\nu\tau_-:
\nu\text{ has physical causal clocks with every positive pressure matched},
\ \tau_0\le3,\ \tau_\pm\le9\}.
\]

This applies to arbitrary physical path laws, including infinite supports
and arbitrarily many turns. A fractional alternating-resource argument
first [localizes all unmatched pressure](research/12-global-closure/POST_FIRST_ENDPOINT_PRESSURE_LOCALIZATION.md)
to the initial front `t+x=1`. A physical boundary turn reduces its mass
geometrically without raising the certified upper value. Each turned
copy then has a permanently negative unpaired tail, so it is never turned
again. The resulting coupled paths stabilize exactly after at most one
change per sample, preserving center time 3 and completion time 9.
This closes the attainment gap without requiring positive fast-sweep mass.

The exact rational replay checks fractional rerouting, arbitrary atomic
front completion, physical turn accounting, and the protected negative
tail. **This removes the matching-deficiency term from the global attained
optimization. It does not supply the minimizing law, a matching Princess
lower law, a finite support bound for an optimum, the exact game value,
or a Lean proof.** The numerical interval remains
`1.4175898349178553515625 <= V <= 1.4259991274612613...`.

## Current reduction checkpoint — exact horizon and physical lift

**The unrestricted value and matching equilibrium remain OPEN.** Two
previously missing global reductions are now proved, without a strategy
bank or an assumption about optimal turn counts:

- [Exact horizon theorem](research/12-global-closure/GLOBAL_EXACT_HORIZON_REDUCTION.md):
  every optimal Monster law has `tau_center <= 2V` almost surely.
  The fair-sweep bound `V <= 3/2` gives the explicit normalization:
  Princess outward after 3 and endpoint-absorbed by 4; some globally
  optimal Monster law center-crossed by 3 and endpoint-completed by 7.
  Its upper guarantee still covers every original Princess path.
  Completed-horizon values stabilize exactly at 7. Reflected `2n`-rank
  approximation now loses at most `7/(2n)`, with no horizon error.
- [Sufficient physical-clock lift](research/12-global-closure/FINITE_STATE_PHYSICAL_CLOCK_LIFT.md):
  seven coordinates retain physical time, position, both actual clock
  backlogs and three visit registrations. Seven constant control
  directions and graph horizon 24 give an exact compact flow model.
  The ordinary superposition principle reconstructs a physical path law
  and both causal clocks from every feasible flow. This closes the
  lifting gap of the older aggregate conservation equations; it does
  not make those older equations sufficient.
- [Finite certificate synthesis](research/12-global-closure/FINITE_GLOBAL_CERTIFICATE_SYNTHESIS.md):
  on the fixed Princess slab `[0,3]`, a supplied polynomial CDF and
  Bellman potential can be checked against all Monsters by finitely many
  real-algebraic conditions. The exact terminal condition is the minimum
  of two weighted endpoint tours. Supplied finite polyhedral-polynomial
  state fluxes and a cone matching likewise give a finitely checkable
  all-Princess upper certificate, without a separate path-lifting guess.

**Precise remaining finite-reduction gate:** either exhibit matching
lower and upper certificates in a finite syntax, or prove an
equilibrium-specific finite bound on the required pieces/degrees/charts.
The seven-state flow and its matching are continuous measures. The
fixed-template verifier is not a theorem that an optimum fits a fixed
template. Neither compactness nor seven controls bounds the number of
coupled charge events along a physical history.

Both new Fraction regressions passed natively; see `REPRODUCE.md`.
The horizon and superposition proofs have been internally cross-reviewed,
but are not Lean-checked. The retained exact interval is unchanged:
`1.4175898349178553515625 <= V <= 1.426129722845311109685250225`.

## Proof audit and native replay — 2026-11-13

**The unrestricted proof is still OPEN.** This audit does not supply a
matching Princess CDF and Monster law. It completes the missing native
replay of the tight upper certificate, reruns the archived exact lower
response, repairs two proof details, and establishes a concrete failure
of the proposed aggregate-flow construction.

- **Both retained bounds replayed:** the original 338-path lower response
  returns exactly `36290299773897097/25600000000000000`; the dedicated
  [tight upper verifier](packages/interval_common_warp/verify_upper_warp_tight.cjs)
  returns exactly
  `57045188913812444387410009/40000000000000000000000000`.
  The upper replay additionally matches all 53,588 rational reward
  coefficients against the actual warped physical routes. The numerical
  interval is unchanged.
- **A proposed relaxation is decisively insufficient:**
  [EULERIAN_RELAXATION_GAP.md](research/12-global-closure/EULERIAN_RELAXATION_GAP.md)
  proves that the bare clock conservation equations and pressure
  matching have attained relaxed optimum **1**, even when chronological
  Monster occupation comes from a genuine symmetric law. A second
  reversing example passes the explicitly listed existing scalar cuts
  but has fake score **5/4**, while an actual legal Princess scores
  **13/8** against that same Monster law. The missing condition is that
  the record clock and chronological motion use the same trajectories.
  The exact physical pressure-matching theorem is not contradicted.
- **Proof repairs:** reflected finite-rank sampling now uses the midpoint
  of the lower and upper quantile traces, which gives exact symmetry even
  at CDF plateau ranks. The Hall-deficiency proof's reversed inequality
  is corrected. Their theorem statements and approximation constants
  are unchanged; see the amended global minimax and matching notes.

These are verification and obstruction results. They do not close the
constructive saddle gate, give a finite equilibrium classification, or
constitute a Lean check. The current complete-game interval remains
`1.4175898349178553515625 <= V <= 1.426129722845311109685250225`.

**New global pressure-matching result (2026-11-13):** [GLOBAL_CAUSAL_PRESSURE_MATCHING.md](research/12-global-closure/GLOBAL_CAUSAL_PRESSURE_MATCHING.md) converts the complete unrestricted single-radius Princess oracle for any physically causal Monster/record-clock law into a **maximal partial transport** between positive and negative record-pressure measures. The matching relation is \((t,u)\preceq(s,v)\iff v\ge u+|s-t|\). The exact value is **baseline active mass + unmatched positive mass**; one can bound every Princess path by exhibiting a partial matching, with no Princess trajectory enumeration. For symmetric Monster laws this yields the exact all-game variational identity
\[
V=1+\min_{\nu,s}\bigl[\mathbb E_\nu(\sigma+B+I/2)+\mu_+(X)-\operatorname{Match}_\preceq(\mu_+,\mu_-)\bigr].
\]
The same note derives pathwise causal-clock backlog conservation \(\alpha=\sigma_{\rm occ}+\partial_t\beta+\partial_x k\), with explicit proof that these Eulerian equations are **necessary and, by the follow-up counterexamples, insufficient without further trajectory coupling** for a physical Monster/clock lift. Strict contact atoms are handled via an outward-germ supremum and the closed-order Strassen theorem. A byte-matched exact Fraction verifier passed 200 finite matching/closure instances, 1,875 queue identities and 27 two-sweep germ tests. **New global tradeoff:** let \(e=\mathbb E(\sigma+B+I/2)\) be Monster search effort and \(D\) the unmatched pressure mass. Every physical symmetric causal law satisfies
\[
D\ge\max\left(0,\frac12-\sqrt{2e}-\frac32e\right).
\]
In particular, exact pressure matching \(D=0\) requires \(e\ge(7-2\sqrt{10})/9\approx0.0750494\). This uses the previously established unrestricted sweep-stability inequality and does not impose any turn or mixing ansatz.

**No new numerical game bound or explicit equilibrium**; this is a new no-ansatz proof interface, not a claim that unmatched pressure vanishes or that timewise balance is optimal.

**Correction to later survivor-halving work (2026-11-13):**
[GLOBAL_SURVIVOR_HALVING_RECURRENCE.md](research/12-global-closure/GLOBAL_SURVIVOR_HALVING_RECURRENCE.md)
is a *dynamic-programming decomposition for the response to a
given fixed Princess CDF*, NOT a recurrence identifying the
unknown equilibrium or a law requiring the Monster to turn
when half of the survivor mass has been caught. The same
mathematical splitting works at **every** threshold
\(0<\rho<1\), and for **every** fixed elapsed time h
one has the ordinary threshold-free Bellman semigroup.
Its contraction controls the number of bookkeeping
phases, but an individual phase still optimizes over
ALL Lipschitz Monster paths. An exact three-stationary-
target response crosses half surviving mass during
an uninterrupted optimal sweep. Therefore this result
does **not** constitute a reduced strategy class,
an equilibrium-specific phase recurrence, or a finite
roadmap. This is an explicit research correction
in response to scrutiny; do not elevate it to
a newly solved game gate.

**Checkpoint:** 2026-11-13. **Source branch:** `research/interval-progress-2026-11-10`, [PR #1](https://github.com/vltanh/lean4-monster-princess/pull/1). This handoff consolidates work through commit `325345fa935ad9005f1db47162c3e629b2e12d12` (subsequent handoff-document commits are administrative). The PR was a draft with **172 commits and 1,058 changed files** when surveyed. The complete unrestricted game remains **OPEN**; no exact value, matching two-sided saddle, finite phase reduction or checked Lean proof is claimed.

**Reading order:** this file → [exact horizon reduction](research/12-global-closure/GLOBAL_EXACT_HORIZON_REDUCTION.md) → [physical-clock lift](research/12-global-closure/FINITE_STATE_PHYSICAL_CLOCK_LIFT.md) → [finite certificate synthesis](research/12-global-closure/FINITE_GLOBAL_CERTIFICATE_SYNTHESIS.md) → [global pressure matching](research/12-global-closure/GLOBAL_CAUSAL_PRESSURE_MATCHING.md) → [verification commands](REPRODUCE.md). The synthesis note links the Bellman and duality foundations. [STATUS.md](STATUS.md) contains the full chronological ledger, not a concise statement of which gates are closed.

## 1. Problem, exact proven bracket and direction of inequalities

For independent laws over all continuous 1-Lipschitz paths in [-1,1], let \(T(m,p)\) be the **first** time \(m(t)=p(t)\), including \(t=0\) and coincident segments. The Princess maximizes and the Monster minimizes expected first-contact time:
\[
V=\sup_\mu\inf_m\mathbb E_\mu T(m,P)
=\min_\nu\sup_p\mathbb E_\nu T(M,p).
\]
The minimax equality and Monster attainment have an unrestricted analytic proof, but **no explicit maximizing Princess law is known or assumed to exist**.

The strongest retained certified bounds are:
\[
\boxed{
L=\frac{36290299773897097}{25600000000000000}
=1.4175898349178553515625
\le V\le
U=\frac{1140799301969009059644426513}
{800000000000000000000000000}
=1.42599912746126\ldots
}
\]
The exact gap is
\[
\boxed{U-L=
\frac{6727434034724778394426513}
{800000000000000000000000000}
=0.00840929254340597\ldots .}
\]

- **Lower certificate:** the archived symmetric, ordered 338-path Princess law (169 reflected path pairs), [source JSON](packages/interval_uniform_reduction/princess_strategy.json). Its Monster best response gives exactly L. The certificate is **against all legal Monsters**, not a finite tested list; see [explicit strategy-pair analysis](research/12-global-closure/EXPLICIT_STRATEGY_PAIR.md) and [uniform reduction](packages/interval_uniform_reduction/PROOF.md).
- **Upper certificate:** the rational 241-pair law in [full_order_upper_exact.json](packages/interval_global_closure/full_order_upper_exact.json) supplies U against **all legal Princess paths**. Its [standalone verifier](packages/interval_global_closure/verify_full_order_upper.cjs) validates all physical routes, recomputes the exact 75,268-node response graph, and replays its flow on a separately rebuilt graph. The previous [tight common-warp certificate](packages/interval_common_warp/upper_warp_tight_exact.json), about 1.42612972284531, remains valid but is weaker.
- An earlier 280-reflected-pair unwarped upper law and the 338-path lower law have exact cross payoff \(J=74616624991393892648392565953/52428800000000000000000000000=1.42319917662418\ldots\). Their opposite unilateral defects are approximately \(0.00560934170633\) (Monster) and \(0.00293614840165\) (Princess). This **is not** a saddle. [Exact pair](research/12-global-closure/EXPLICIT_STRATEGY_PAIR.md).

**Do not claim a bound improvement** from any of the structural, restricted-family, near-sweep, or fixed-bank experiments below. The numerical bracket above is unchanged.

## 2. Global results covering the actual unrestricted path space

The following are analytical theorem claims in the linked repository manuscripts, not a statement that Lean has checked their proofs. They **do not** assume a finite turn count or a finite Monster path bank.

| Result and precise scope | Primary proof |
| --- | --- |
| **G1: unrestricted lopsided minimax; attained symmetric Monster law** on full continuous trajectories; Princess attainment not proved. | [GLOBAL_MINIMAX_AND_CDF_DUALITY.md](research/12-global-closure/GLOBAL_MINIMAX_AND_CDF_DUALITY.md) |
| **Horizon/rank approximation:** \(V_{H,n}-6/H\le V\le V_{H,n}+(H+3)/(2n)\), with 2n ordered Princess quantiles and bounded completion time, **but no finite-turn/LP reduction**. | [GLOBAL_MINIMAX_AND_CDF_DUALITY.md](research/12-global-closure/GLOBAL_MINIMAX_AND_CDF_DUALITY.md) |
| **Complete Princess CDF transport cone:** \(F(s,x-(t-s))\le F(t,x)\le F(s,x+(t-s))\); common-quantile realization is legal and dominates raw couplings with the same marginals. Strict/closed CDF records yield an exact infinite LP. | [GLOBAL_CDF_TRANSPORT_LP.md](research/12-global-closure/GLOBAL_CDF_TRANSPORT_LP.md) |
| **Full CDF directional variation:** first derivative uses *near-active* strict lower and closed upper history records, including ties, atoms, and Zeno. Together with an all-Monster lower certificate it is a conditional global saddle test. | [GLOBAL_CDF_VARIATIONAL_STATIONARITY.md](research/12-global-closure/GLOBAL_CDF_VARIATIONAL_STATIONARITY.md) |
| **Finite-completion strong record duality** with minimizing causal selectors (not a finite route family). | [GLOBAL_STRONG_RECORD_DUALITY.md](research/12-global-closure/GLOBAL_STRONG_RECORD_DUALITY.md) |
| **Deterministic monotone causal clock:** stochastic history selectors can be pushed forward to a nondecreasing past-time clock on each Monster path. | [GLOBAL_MONOTONE_CAUSAL_CLOCK.md](research/12-global-closure/GLOBAL_MONOTONE_CAUSAL_CLOCK.md) |
| **Horizon-free attained one-clock minimax:** a symmetric complete Monster law plus one active causal lower-record clock suffices. The active record occupation has finite mass at most V. This is an **abstract exact duality, not an explicit minimizer**. | [GLOBAL_INFINITE_HORIZON_ACTIVE_DUAL.md](research/12-global-closure/GLOBAL_INFINITE_HORIZON_ACTIVE_DUAL.md) |
| **Singular contact-germ transmission:** a vanishing Princess perturbation can change the radial dual payoff by *order one* on exact contact graphs; calibrated free-flow interior paths exclude such singular contact pressure. | [GLOBAL_RADIAL_CONTACT_GERMS.md](research/12-global-closure/GLOBAL_RADIAL_CONTACT_GERMS.md) |
| **Global Monster Bellman sufficient certificate:** CDF history records and an inequality covering every legal Monster transition, including endpoint resets, waits, atoms and arbitrary turns; **a matching potential has not been constructed**. | [GLOBAL_CDF_BELLMAN.md](research/10-turn-density/GLOBAL_CDF_BELLMAN.md) and [FINITE_REDUCTION_GATE.md](research/11-finite-reduction/FINITE_REDUCTION_GATE.md) |
| **Global Princess radial upper oracle:** occupation measure induces a scalar threshold optimal-control problem; smooth interior form is an HJB and interior unsaturated flow has balanced opposing record pressure. Actual contact atoms require strict germ conditions, not just a smooth PDE. | [GLOBAL_DUAL_RECORD_PRESSURE_HJB.md](research/12-global-closure/GLOBAL_DUAL_RECORD_PRESSURE_HJB.md) |

### Exact, still-unevaluated full-game target

After symmetry, let \(\nu\) be a law on **complete Monster histories**, \(\tau_-(m)\) its first arrival at -1, and \(s_m(t)\) a nondecreasing Borel **backward clock** satisfying \(0\le s_m(t)\le t\). Define a positive spacetime measure \(\alpha\) by pushing forward
\[
\nu(dm)\mathbf1_{t<\tau_-(m)}dt
\quad\text{under}\quad (m,t)\mapsto(s_m(t),m(s_m(t))).
\]
It must retain its causal **lift to legal full Monster trajectories**. Writing
\(\Phi(r,x)=\mathbf1_{\{r<x\}}+\mathbf1_{\{r>-x\}}\),
the manuscript proves the attained exact global dual
\[
\boxed{
V=\min_{\nu,s}\;\sup_{\substack{r:[0,\infty)\to[0,1]\\
|r'|\le1}}\int\Phi(r(t),x)\,\alpha(dt,dx).
}
\]
Neither the minimizing \((\nu,s)\) nor the maximizing/approaching radius law is explicit. **Do not replace \(\alpha\) by an arbitrary positive density**: without its Monster-path/clock causal lift the variational problem is different. **Do not discard strict inequalities:** contact-germ jumps can change the score by O(1).

On the Princess side, a legal CDF F with strict and closed traces has ordered-quantile Monster response
\[
C_m(F)=\int_0^\infty
\left[1+\inf_{s\le t}F^-(s,m(s))
        -\sup_{s\le t}F^+(s,m(s))\right]dt .
\]
For symmetry, the dual may be written using a single lower record. These are two interfaces to the **same full game**, not an interchangeable replacement for the physical first-hit definition.

**Closing conditions at one constant \(c\):** construct (i) a legal F (or a uniform approaching F_\(\epsilon\) family) and certify \(C_m(F)\ge c\) for **every** legal Monster m, including free initial position, waiting, arbitrary turns, resets and Zeno, and (ii) a physical Monster law \(\nu\) with an admissible monotone clock s and certify \(\sup_r\int\Phi(r,x)d\alpha\le c\) against **every** legal radial Princess path, with singular/contact-germ conventions exact. Only BOTH sides yield V=c. An \(\epsilon_M,\epsilon_P\) pair gives a valid \(c-\epsilon_M\le V\le c+\epsilon_P\).

## 3. Global structural restrictions (unrestricted, but NOT equality)

- **All monotone Monster paths are controlled:** the two opposite fastest endpoint sweeps form a fully solved restricted Monster game of value \(3/2\). More generally a weighted fastest-sweep law has unrestricted Princess response \(1+\max(w,1-w)\); the Princess supremum is typically **unattained**. [All monotone theorem](research/12-global-closure/ALL_MONOTONE_SUBGAME_EXACT.md).
- **Canonical full-game support:** some symmetric optimal Monster law can be taken to consist of the two fastest endpoint sweeps plus a symmetric law on paths that **start in the interior and reverse before completing both endpoints**. This is not a finite-turn support claim. The original derivation and endpoint-start dominance are in [ALL_MONOTONE_SUBGAME_EXACT.md](research/12-global-closure/ALL_MONOTONE_SUBGAME_EXACT.md).
- **Mandatory reversing mass:** every Monster optimum assigns at least \(3/2-U=0.07387027715468\ldots\) probability to reversing paths, using the exact two-runner unrestricted response. [Dual/reversal theorem](research/12-global-closure/GLOBAL_DUAL_RECORD_PRESSURE_HJB.md).
- **Endpoint budget and geometry:** if \(\sigma\) and \(\tau\) denote first and second endpoint arrival times, then \(\mathcal E=(\tau_++\tau_-)/2-1=\sigma+B+I/2\) exactly, where B is wrong-way variation and I is slower/idle time between endpoints. Every optimal Monster law has \(\mathbb E|M(0)|\ge 2-U\approx0.57387027715\) and \(\mathbb E\mathcal E\le U-1\approx0.42612972285\). No turn-count assumption.
- **NEW continuum-offset global coercivity:** every optimal Monster law satisfies
\[
\boxed{
\mathbb E(\tau-2)\ge
\frac27(1+3a-\sqrt{1+6a-5a^2})
=0.0090511656481067\ldots>\frac{181}{20000},
\quad a=\frac32-U.
}
\]
This follows from all-path uniform fastest-sweep rigidity, a continuum of Princess runner offsets and a convex/Jensen response envelope. It also forces \(\mathbb E\mathcal E\ge0.00452558282\ldots\). [Complete proof + rational certificate](research/12-global-closure/GLOBAL_SWEEP_STABILITY_ENERGY_BARRIER.md). It excludes an **infinite-dimensional neighborhood** of near-sweep Monster laws, not all reversing histories and not the actual equilibrium search.

These support restrictions are simultaneously valid tests for a proposed optimal \(\nu\) in the causal-clock dual. They are not sufficient to construct or characterize \(\nu_*\).

## 4. Restricted/candidate results — retain, but do NOT conflate with V

| Component | Certified scope / result | Evidence |
| --- | --- | --- |
| Archived 338-path versus 280-pair approximate pair | Exact cross score J and both unilateral defects; strict failure of saddle stationarity. | [EXPLICIT_STRATEGY_PAIR.md](research/12-global-closure/EXPLICIT_STRATEGY_PAIR.md), [GLOBAL_CDF_VARIATIONAL_STATIONARITY.md](research/12-global-closure/GLOBAL_CDF_VARIATIONAL_STATIONARITY.md) |
| Failed Monster reweightings | Two **whole continuous weight rays** rigorously excluded from improving U: adding the archived Princess-best-response Monster path; moving mass from old atom 0 to 120. Four physical Princess cuts, 2,248 exact oriented first contacts. | [G2_NEAR_ACTIVE_GERM_SEPARATION.md](research/12-global-closure/G2_NEAR_ACTIVE_GERM_SEPARATION.md), [cuts](packages/interval_global_closure/g2_near_active_princess_cuts.json), [verifiers](packages/interval_global_closure/verify_g2_ray_exclusions.cjs) |
| All continuous common-coordinate warps of archived Princess law | The supplied **restricted family** has upper ceiling \(1.417638883192751\ldots\) from a 35-route rational Monster law, very close to archived L; **not a lower bound for all Princess laws nor a new global upper**. | [LOWER_WARP_ALL_TIGHTENED.md](research/12-global-closure/LOWER_WARP_ALL_TIGHTENED.md) |
| Fixed finite translated/reflected fans | Effective finite-piece Monster responses for a **fixed** positive-width law, plus finite-bank selector oracle. No uniform complexity as widths vanish; not an equilibrium-support theorem. | [FINITE_FAN_RESPONSE_EXISTENCE.md](research/12-global-closure/FINITE_FAN_RESPONSE_EXISTENCE.md), [EFFECTIVE_RESPONSES_AND_GLOBAL_SELECTOR_ORACLE.md](research/12-global-closure/EFFECTIVE_RESPONSES_AND_GLOBAL_SELECTOR_ORACLE.md) |
| All-count center-return/Green/Zeno formulas | Exact algebraic count-uniform optimization for prescribed saved affine terminal wedge; short hinges eliminated and phases partly classified. May require infinitely many turns. **No assertion about arbitrary first starts, earlier exits or initial waits.** | [TWO_SOURCE_GREEN_ZENO_ENVELOPE.md](research/12-global-closure/TWO_SOURCE_GREEN_ZENO_ENVELOPE.md), [LOW_SURPLUS_ALL_HINGES_EXCLUSION.md](research/12-global-closure/LOW_SURPLUS_ALL_HINGES_EXCLUSION.md), [HIGH_SURPLUS_SINGLE_RETURN.md](research/12-global-closure/HIGH_SURPLUS_SINGLE_RETURN.md), [INFINITE_TURN_RENEWAL.md](research/12-global-closure/INFINITE_TURN_RENEWAL.md) |
| Finite-turn reduction obstruction | For arbitrarily large k there are symmetric ordered endpoint-absorbed Princess laws requiring k Monster reversals; hence endpoint absorption and smooth CDF **do not themselves** give a uniform finite-turn bound. This does not rule out an equilibrium-specific simplification. | [FINITE_REDUCTION_GATE.md](research/11-finite-reduction/FINITE_REDUCTION_GATE.md) |

Full older computational and local-geometry steps are preserved under [research/08-continuum](research/08-continuum), [research/09-equilibrium-structure](research/09-equilibrium-structure), [research/10-turn-density](research/10-turn-density), [research/12-global-closure](research/12-global-closure), and their associated packages. [STATUS.md](STATUS.md) is the chronological index.

## 5. Verification manifest and provenance

**Fast primary replay from the repository root** (full checkout, ordinary Python / Node installed):

```bash
python packages/interval_global_closure/verify_global_minimax_reduction.py
python packages/interval_global_closure/verify_cdf_record_variation.py
python packages/interval_global_closure/verify_global_strong_record_duality.py
python packages/interval_global_closure/verify_global_monotone_clock.py
python packages/interval_global_closure/verify_global_dual_two_sweep.py
python packages/interval_global_closure/verify_weighted_sweep_envelope.py
python packages/interval_global_closure/verify_fixed_start_runner_response.py
python packages/interval_global_closure/verify_global_sweep_stability.py
node packages/interval_global_closure/verify_g2_ray_exclusions.cjs
node packages/interval_global_closure/verify_g2_princess_cuts.cjs
```

**Certified original numerical strategies** (some checks are resource intensive):

```bash
python packages/interval_uniform_reduction/exact_response.py \
  packages/interval_uniform_reduction/princess_strategy.json
# Checks the historical warped certificate, not the tight upper file:
node packages/interval_common_warp/verify_upper_warp.cjs
# Checks the current tight upper certificate:
node --stack-size=16384 packages/interval_common_warp/verify_upper_warp_tight.cjs
node --stack-size=16384 \
  packages/interval_global_closure/certify_upper_candidate.cjs \
  --verify packages/interval_global_closure/upper_dyadic_exact.json
python packages/interval_turn_sheet/verify_two_source_outer_envelope.py
python packages/interval_turn_sheet/verify_short_source_mergers.py
```

**Current handoff audit:** three recent exact-Fraction scripts (weighted sweeps, fixed-start response, global sweep stability) were executed successfully in the available working container; the newest stability script checks 1,050 legal polygonal Monster routes, seven offsets, and symbolic-Fraction integrations/strict upper comparison. The repository's corresponding source was also inspected via GitHub. This does **not** mean the entire 1,058-file branch, every historical V8 verifier, native Node, Lean or CI was rerun. Much earlier exact certificates were reported as run in the V8 connector or local Python, with separate caveats in the respective proof files. Treat every quoted executable result as a **fixture/certificate audit**, not as a substitute for the analytical continuum proofs.

**Tight-upper verification item CLOSED:** the dedicated native Node replay
above passed, with both input JSONs pinned to their exact Git blob hashes.
The original lower verifier also passed natively after its source and
strategy JSON were matched to the current Git blobs; it completed all
48,228 search nodes. The new quantile-tie and Eulerian-relaxation
regressions were executed with exact Fraction arithmetic. These targeted
replays do not assert a full-tree replay, Lean compilation or CI.

**Known caveats:** strict first contacts are discontinuous; use actual positive-epsilon paths rather than their zero-scale label limits. A finite Monster master value is not an unrestricted Princess lower bound. A sampled spatial graph is not an unrestricted Monster response certificate. A stationary-monotone subgame equality is not the full-game equality. Even an exact causal dual representation does not reveal its minimizer. The many local affine-terminal theorems are conditional on their stipulated cell and terminal geometry.

## 6. Focused next-work gates — no indefinite case queue

**Use the exact fixed domain:** Princess data on `[0,3]`, the two-tour
terminal boundary, and Monster completion by 7. Increasing a completion
horizon is no longer a missing global step. The seven-state lift is an
alternative sufficient way to represent all physical Monster/clock
laws on this domain; no path-history lift needs to be guessed after
solving its full continuity equation. A finite polynomial template is
globally verifiable, but no completeness bound for such templates is
known.

**Gate A — construct the global dual occupation, not another path-bank mixture.** Parameterize an actual symmetric Monster history law \(\nu\) and its measurable nondecreasing past clock \(s_m\); explicitly carry its causal lift (a mere spacetime density is insufficient). Use the canonical sweep source plus genuinely interior-start reversing histories, allowing arbitrary turn counts and Zeno. Impose the whole-game endpoint moment, reversal probability, and **completion-delay** constraints from §3. The output must be an explicit feasible \(\alpha\), not just a signed numerical pressure.

**Failed shortcut at Gate A:** optimizing only the displayed Eulerian
clock equations is now ruled out by the exact value-1 relaxation
counterexample. The reversing value-5/4 example also survives the named
scalar effort and delay cuts. Any replacement of the trajectory/clock
variables therefore needs a proved sufficient lifting theorem. The
necessary conditions `beta << sigma` and the joint directional moment
bounds in the old note are not asserted sufficient. The new full
seven-state flow retains the joint queue distribution and **does** have
a sufficient lifting theorem. Constructing its optimum remains open.

**Gate B — solve the *whole* radial Princess adversary to that \(\alpha\).** Evaluate \(\sup_{r:|r'|\le1}\int\Phi(r,x)d\alpha\) with both strict comparisons and all nonattained near-contact germs. For absolutely continuous interior components derive the HJB/calibration; for characteristic/singular mass use exact threshold jump/transmission conditions. Stop if a legal pure radius or near-contact family disproves the claimed upper value. Do not treat a finite grid optimum as global.

**Gate C — construct/verify a matching full Princess CDF.** Supply F satisfying transport inequalities, with correct endpoint atoms, and a global Bellman/potential certificate for every Monster: arbitrary free start, any speed \(|m'|\le1\), center/endpoint waits and resets, and infinitely many turns. For piecewise polynomial candidate potentials the existing finite arithmetic verifier reduces **verification**, not existence, to critical controls and exact face-stationarity checks. A local center-Zeno envelope is not sufficient.

**Gate D — close exactly or decisively falsify the candidate.** Put both unrestricted inequalities at the **same** c, or report a rigorously controlled \(\epsilon\)-gap. Any counterexample should be reproducible as a physical Monster route or Princess path with strict contact sides. A failed candidate goes in a single negative-result section; do not spawn an unbounded M4/M5/... or extra local-cell proof queue.

**Stop/go:** progress means a feasible *global* candidate with both certified residuals, a theorem implying a finite equilibrium-specific phase class, or an unconditional nontrivial whole-game restriction such as §3. Merely changing a third decimal of an old finite bank or adding another conditional local inequality does not advance the closure gate.

## 7. Exact unresolved claims

1. A constructive minimizing \((\nu_*,s_*)\) / occupation measure \(\alpha_*\), including its reversing-history geometry and singular thresholds.
2. A full Princess CDF \(F_*\) (or approaching family) calibrated to that dual, with **unrestricted** Monster response.
3. Matching upper and lower global Bellman/HJB/record inequalities at the same explicit c; a finite certificate format may exist without an attaining finite analytic solution.
4. The exact constant V, equilibrium-specific finite-phase theorem (if true), and Lean formalization/CI.

**No completion of the unrestricted proof is claimed.** This file is the authoritative review checkpoint; future work should update it and the numerical ledger **only when a claim's scope or certificate changes**.

