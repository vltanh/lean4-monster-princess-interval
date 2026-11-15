# Status ledger — interval Princess–Monster research

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


## Stronger unrestricted upper certificate — 2026-11-13

The current certified interval is
`1.4175898349178553515625 <= V <= 1.4259991274612613...`.
The exact new upper is
`1140799301969009059644426513/800000000000000000000000000`.
[Proof and scope](research/12-global-closure/FULL_ORDER_CDF_UPPER_CERTIFICATE.md);
[standalone verifier](packages/interval_global_closure/verify_full_order_upper.cjs).

The whole ordered-CDF discovery problem on the old 280-pair event
geometry converged numerically. Its dual weights were rounded to a
rational 241-pair law and then independently recertified against all
Princess paths. The exact graph has 75,268 nodes and 191,435 arcs; the
rebuilt-graph replay checked 83,601 positive-flow entries. Its stationary
endpoint baseline is `1.4259967347889189...`, leaving deficiency
`0.000002392672342420767...`. This is a stronger upper certificate, not
an equilibrium or an unrestricted lower guarantee for the discovery CDF.
The lower bound and the open finite-equilibrium gate are unchanged.
The older entries below are chronological statements at their own dates.

**Independent physical realization completed:** the
[finite clock homogenization theorem](research/12-global-closure/FINITE_BANK_CLOCK_HOMOGENIZATION.md)
reduces every supplied finite unit-speed bank to an exact finite clock
and matching LP. For the new 241-pair law, an ordinary integer circulation
and a standalone physical replay verify the same exact upper, including
85,268 clock-prefix checks and 12,214 order-flow edges. All unmatched
pressure lies in three continuous sweep-front cells. The
[continuum completion theorem](research/12-global-closure/ENDPOINT_FRONT_DEFICIENCY_COMPLETION.md)
replaces `D/2` of sweep probability by an explicit uniform family and
produces a zero-deficiency law with exact worst-case payoff U. Each
stationary endpoint attains U against this supplied law. This does not
supply a matching full-game Princess lower strategy.

## Exact bounded horizon and sufficient physical-clock flow — 2026-11-13

Two global gates are now closed analytically:

1. [Exact horizon reduction](research/12-global-closure/GLOBAL_EXACT_HORIZON_REDUCTION.md):
   every optimal Monster law satisfies `tau_center <= 2V` almost surely.
   Princess security is unchanged by forcing ordered symmetric paths
   outward after time 3; they reach their endpoints by 4. Some globally
   optimal Monster law reaches the center by 3 and both endpoints by 7,
   while retaining its guarantee against every original Princess path.
   Consequently the completed-horizon value is exactly V for every
   horizon at least 7. The post-3 continuation has just two exact weighted
   endpoint tours. No truncation error or finite-turn assumption enters.
2. [Exact physical-clock lift](research/12-global-closure/FINITE_STATE_PHYSICAL_CLOCK_LIFT.md):
   keep the joint distribution of physical time, position, two clock
   backlogs, and three visit registrations. Seven constant controls on a
   compact seven-dimensional polytope, over graph time 24, give a
   necessary **and sufficient** continuity-equation representation.
   Superposition reconstructs physical Monster paths and both causal
   clocks, preserving the individual charge fluxes. Pressure matching
   then gives an exact linear program over continuous measures.

[Finite full-game certificate synthesis](research/12-global-closure/FINITE_GLOBAL_CERTIFICATE_SYNTHESIS.md)
combines these results with the Bellman verifier: each fixed polynomial
CDF/potential template and finite polyhedral-polynomial flux/matching
template has a finite real-algebraic check. A matching pair at one c would
prove V=c. **No finite bound on the required pieces, degrees, charts or
turns, and no matching pair, has been obtained.** The continuous-measure
program is not a finite-dimensional LP.

Both new exact-rational regressions passed natively. The horizon suite
checks 1,274 center bounds, 2,106 outward first-contact comparisons,
2,106 common tail normalizations and 162 weighted-tour formulas. The
clock suite checks 120 clock pairs, 6,298 state/control segments, 1,200
strict-pressure comparisons and 40 continuous two-sweep germ cases.
These audit the formulas; the continuum proofs are analytic. The exact
L/U interval is unchanged, and no Lean or CI result is claimed.

## Proof audit: native certificates, quantile repair, and failed flow relaxation — 2026-11-13

**Full game remains OPEN; no numerical bound improved.** Both recorded
ends of the interval have now been replayed in native runtimes. The
338-path lower response returned its exact stored rational after a
complete 48,228-node search. The new dedicated
`packages/interval_common_warp/verify_upper_warp_tight.cjs` replayed the
actual tight JSON and its 59,593-node exact flow/cut witness, and checked
all 53,588 reward coefficients directly from the warped physical routes.
The outstanding tight-upper replay item is closed.

The unrestricted finite-rank approximation proof now uses
`Q_sym=(Q_lower+Q_upper)/2`. Ordinary lower quantiles alone need not give
reflected midpoint samples at CDF plateau ranks. This repairs the stated
symmetry while preserving the original transport law and error bound.
The exact regression passed 4,212 reflected identities, 405 physical
first-contact/rank comparisons, and 4,455 strict-survival checks.
The pressure-matching Hall proof also has its reversed inequality fixed.

**Decisive negative construction:**
[EULERIAN_RELAXATION_GAP.md](research/12-global-closure/EULERIAN_RELAXATION_GAP.md)
proves that bare Eulerian clock conservation plus exact pressure
matching has attained relaxed value **1**, even with a genuinely
physical symmetric chronological Monster occupation. A reversing
example satisfying the explicitly checked scalar support/effort/delay
cuts has fake score **5/4**, while a single legal Princess scores
**13/8** against the same Monster. Aggregate causal transport can run
along different histories from the Monster being scored; the original
physical-clock dual does not permit this. Additional necessary coupling
conditions are recorded, without claiming they are sufficient.

The all-Princess reduction behind the tight upper was also audited for
strict contact, arbitrary starting positions and unlimited turn counts.
It uses finite Monster event geometry to bound every Princess; it is
not a finite Princess test bank. No matching lower CDF, finite
equilibrium classification, Lean compilation or CI is claimed.

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

**Authoritative 2026-11-13 checkpoint:** [HANDOFF_2026-11-13.md](HANDOFF_2026-11-13.md) gives the source-of-truth summary: current exact L/U certificates, global theorem dependencies, all-class structural restrictions, rigorous scope distinctions, reproducibility, and the still-open constructive saddle. The entries below remain a **chronological ledger** and include historical (weaker) bounds; consult the handoff before selecting a new proof direction.

## G2 global coercivity against ALL near-fast-sweep laws (2026-11-13)

**New genuine UNRESTRICTED support/dual feasibility theorem**, no finite
Monster support, turn cap, common time horizon or smoothing assumption.
For any Monster trajectory, let sigma be its first endpoint visit,
tau its second, B its total wrong-way motion between endpoints and
I its time not moving at full speed between endpoints. Then
\[
 \tau-\sigma=2+2B+I,\quad
 \mathcal E=\frac{\tau_-+\tau_+}{2}-1
           =\sigma+B+I/2,\quad
 \|m^{\rm stopped}-m^{\rm fastest\ sweep}\|_\infty
       \le\tau-2.
\]
Each of these holds with arbitrary waits, resets and Zeno turns.
The two stationary endpoint Princesses force **every optimal**
Monster law to satisfy
\[
 \mathbb E \mathcal E \le U_{\rm best}-1
         =0.426129722845311\ldots,\quad
 \mathbb E|M(0)|\ge2-U_{\rm best}=0.573870277154688\ldots.
\]

An exact **continuum-offset Princess law** gives a globally valid
**convex** lower response envelope \(L_A(\delta)\) as a function of
Monster endpoint-completion lateness
\(\delta=\tau-2\). Jensen applies to ANY Monster law.
Optimizing A produces the NEW whole-game necessary bound
\[
 \boxed{\mathbb E_{\nu_*}(\tau(M)-2)
 \ge\frac{2}{7}(1+3a-\sqrt{1+6a-5a^2})
 =0.0090511656481067386\ldots},\quad
 a=3/2-U_{\rm best}.
\]
An independently exact rational certificate with A=4/15 proves
\(\mathbb E(\tau-2)>181/20000=0.00905\):
the universal Princess payoff at mean delay
181/20000 is EXACTLY 2190541249/1536000000,
strictly exceeding U_best by an exact positive fraction.
Thus infinitesimal geometry changes and ALL mixtures supported
in a sufficiently near-sweep completion-time neighborhood
cannot achieve the known global upper. The equilibrium
endpoint-delay energy is bounded both ways, in particular
\(\mathbb E\mathcal E\ge0.00452558282405\ldots\).

[Full analytic proof and convex Jensen bound](research/12-global-closure/GLOBAL_SWEEP_STABILITY_ENERGY_BARRIER.md);
[exact Fraction test](packages/interval_global_closure/verify_global_sweep_stability.py).
The verifier passed 1,050 completed legal rational Monster paths,
seven exact runner offsets, independent physical-first-contact and
variation identities, and exact continuum-offset integral/strict
rational gap checks. The analytic claims do not rely on a finite
path test.

**Does NOT solve G2/G5:** no matching CDF/Monster clock, no exact
full-game constant, no finite turn/phase bound; certified value
interval is UNCHANGED. This supplies a new rigorous global
feasibility cut for the attained Monster causal-clock minimax.
No Lean compilation/CI.

## G2 exact infinite monotone subgame and stronger endpoint-start support exclusion (2026-11-13)

**Entire infinite-dimensional monotone Monster subgame closed.**
For the two fastest sweeps \(m_\pm\), the unrestricted
Princess pure-path supremum against weights \(w,1-w\) is
\[
 \sup_p[wT(m_+,p)+(1-w)T(m_-,p)]
 =1+\max(w,1-w).
\]
For \(0<w<1\) this supremum is not attained (at
\(w=0,1\) it is attained by a stationary endpoint Princess).
The Monster minimax over **every** monotone legal trajectory,
including arbitrary speeds, waits, and starts, is exactly
\(3/2\), achieved by the fair pair of fastest sweeps;
Princess security \(3/2\) is an unattained supremum.
A positive vanishing stationary-endpoint Princess mass
eliminates incomplete monotone Monster responses in
the lower-bound argument. The optimal Monster orientation
weights are necessarily \(1/2,1/2\), but uniqueness of
the entire monotone Monster path law is not claimed.

**Stronger unrestricted dominance theorem:** EVERY Monster
trajectory starting at -1, including reversing and Zeno
ones, is pointwise capture-dominated against ALL Princess
paths by the fastest rightward sweep; similarly for +1.
Thus a symmetric optimal full-game Monster law can be
canonicalized to
\[
 \nu_*=(q/2)(\delta_{m_+}+\delta_{m_-})
 +(1-q)\nu_{\rm int,rev},
\]
where the residual law is supported on trajectories
that both **start strictly inside (-1,1) and reverse**.
The previous all-optima bound implies the canonical
interior-start reversing component has mass at least
\(3/2-U_{\rm best}>7.38\%\).
This eliminates endpoint-start reversing policies from
the genuinely unknown global optimal-support search.
It does NOT prove a full-game equilibrium or improve
the unrestricted numerical interval.


**New exact fixed-start unrestricted Monster response:** against
the symmetric pair of inward Princess runners starting at
\(\pm a\), \(a=1-\epsilon\), the Monster's global best
response from ANY prescribed start \(x\in[-a,a]\)
has exact expected first capture
\[
 \inf_{m(0)=x}\frac{T(m,p_L)+T(m,p_R)}2
 =\frac{3a-|x|}{4}.
\]
A one-reversal route attains it; the lower bound covers
ALL legal Monster histories without a turn restriction.
This yields a stronger **joint initial-position/reversal
mass constraint** on a canonical globally optimal law:
if \(q\) is its fast-sweep mass and
\(r=\mathbb E_{\nu_{\rm int,rev}}|M(0)|\),
\[
 \boxed{1-q\ge\frac{4(3/2-U_{\rm best})}{3+r}.}
\]
For \(r=1\) this recovers the unconditional 7.387% bound;
for \(r=0\) it would force 9.849% reversing mass.
The latter is only a conditional illustration, NOT a
claim that the unknown equilibrium has \(r=0\).
[Exact 37-case Fraction physical response verifier](packages/interval_global_closure/verify_fixed_start_runner_response.py)
passed; full proof is in
[the monotone subgame and support note](research/12-global-closure/ALL_MONOTONE_SUBGAME_EXACT.md).

[Proof](research/12-global-closure/ALL_MONOTONE_SUBGAME_EXACT.md)
and [executed Fraction regression](packages/interval_global_closure/verify_weighted_sweep_envelope.py):
429 legal Princess polylines, seven rational sweep weights,
19 epsilon approaching families per weight; all passed.
No Lean compilation or CI. G2-G5 remain OPEN.

## G2 global STRICT contact-germ transmission and singular free-flow exclusion (2026-11-12)

From the **attained actual infinite-horizon** radial dual
\(J_\alpha(r)=\int[\mathbf1_{r(t)<x}+
\mathbf1_{r(t)>-x}]\,d\alpha(t,x)\), with
\(\alpha\ge0\), \(\alpha(\mathrm{all})\le V\),
we have a new exact theorem for any feasible
one-sided Princess perturbation \(r+\epsilon\varphi\):
\[
\lim_{\epsilon\downarrow0}
 [J_\alpha(r+\epsilon\varphi)-J_\alpha(r)]
 =
\alpha\{x=r(t),\varphi(t)<0\}
+\alpha\{x=-r(t),\varphi(t)>0\}.
\]
**The jump can be order ONE, not \(O(\epsilon)\)**,
so differentiating a smooth HJB without its strict
contact boundary germs is unsound.

**New necessary optimality condition even for singular
occupations:** if an optimal pure radius r is strictly
inside \((0,1)\) and has speed bounded uniformly below
one on an open interval I, then
\(\alpha\{t\in I,x=r(t)\}=
\alpha\{t\in I,x=-r(t)\}=0\).
A radius within \(\epsilon\) of optimal permits at
most \(\epsilon\) occupation on either graph, hence at
most \(2\epsilon\) on both. In regular zones the
remaining first variation recovers
\(h(t,-r)=h(t,r)\); on saturated
characteristics the strict germ jump remains essential.

For the exact two-sweep active source
\((1/2)dt\,\delta_{x=1-t}\), the contact path
\(r_0(t)=|1-t|\) has payoff \(1/2\),
whereas the arbitrarily close legal runner
\(r_\epsilon\) has \(3/2-\epsilon/4\):
the exact jump equals **one**.
The corresponding limiting runner-germ functional
is an explicit **continuum** linear inequality
on any candidate reversing-history occupation,
not a sampled finite Princess column.

[Global singular-occupation contact theorem](research/12-global-closure/GLOBAL_RADIAL_CONTACT_GERMS.md);
[34 Fraction integral fixtures](packages/interval_global_closure/verify_global_monotone_clock.py).

**This is a global optimality obstruction, not a new bound
on the numerical game value or a matched explicit saddle.**
G2 constructive and G3–G5 remain OPEN. No Lean/CI.

## G2 GLOBAL INFINITE-HORIZON STRONG DUAL CLOSED (abstract) — CONSTRUCTIVE SADDLE OPEN (2026-11-12)

**New theorem for the actual UNRESTRICTED full game, not merely an
accuracy-dependent horizon limit:** Let \(\nu\) be a symmetric
Monster law on complete 1-Lipschitz trajectories and
\(\tau_-(m)=\inf\{t:m(t)=-1\}\). For any such
\(\nu\) with \(\mathbb E_\nu\tau_-<\infty\),
the Princess pure-path best response is EXACTLY the
minimum over a compact space of **one** causal
strict lower-record kernel on the finite measure
\(\nu(dm)\mathbf1_{t<\tau_-(m)}dt\).
The history selector can be represented WITHOUT LOSS
by a measurable nondecreasing time clock
\(s_m(t)\le t\).

The resulting exact ATTAINED global minimax is
\[
\boxed{
 V=\min_{\substack{\nu\ {\rm symmetric},\
       \mathbb E_\nu\tau_-<\infty\\
       s_m(t)\uparrow,\ 0\le s_m(t)\le t}}
   \sup_{\substack{r:[0,\infty)\to[0,1]\\|r'|\le1}}
   \mathbb E_\nu\int_0^{\tau_-(m)}
   \Big[\mathbf1_{\{r(s_m(t))<m(s_m(t))\}}+
       \mathbf1_{\{r(s_m(t))>-m(s_m(t))\}}\Big]\,dt.
}
\]
Its minimum exists, although the Princess supremum
may not be attained. The fixed-\(\nu\) strong duality
uses compactness of **finite active causal measures**,
the correct lower semicontinuity of strict
comparisons, and finite-dimensional convex
upper-set separation. The full-game minimum follows
from the previously proved symmetric optimal Monster
law: stationary Princess at -1 forces
\(\mathbb E_{\nu_*}\tau_-\le V\le
U_{\rm best}=1.426129722845311\ldots\).
The active dual occupation measure thus has exact
total mass \(\mathbb E_{\nu_*}\tau_-\le V\),
independent of any terminal horizon.

**Canonical optimal support:** all Monster paths can be
stopped after first visiting both endpoints.
A symmetric optimal law can be chosen as
\((q/2)(\delta_{m_+}+\delta_{m_-})+
(1-q)\nu_{\mathrm{rev}}\), where the
remaining paths have genuinely **nonmonotone
PRECOMPLETION prefixes**. Every optimal law
(not only this canonical representative) assigns at least
\(3/2-U_{\rm best}\simeq7.387\%\) mass to
nonmonotone precompletion paths: postcapture
gratuitous reversals do NOT count.
In an optimal dual the entire straight-sweep
active occupation is the explicitly known
characteristic measure
\((q/2)\mathbf1_{0\le t\le2}dt\,\delta_{x=1-t}\);
only the reversing-history pressure is unknown.

**New exact complementary conditions:** a near-optimal
Princess CDF makes the dual record-time slack
at most \(\epsilon\), and all but
\(\epsilon/\delta\) of its radial quantile mass
lies within \(\delta\) of the maximal global
radius-control score. This works without Princess
attainment, smoothness, finite turn caps, or
artificial endpoint absorption.

[Complete infinite-horizon proof](research/12-global-closure/GLOBAL_INFINITE_HORIZON_ACTIVE_DUAL.md) |
[time-clock quantile and bounded-active-sector proof](research/12-global-closure/GLOBAL_MONOTONE_CAUSAL_CLOCK.md) |
[finite-horizon strong duality](research/12-global-closure/GLOBAL_STRONG_RECORD_DUALITY.md).

Independent exact regressions:
[Fraction causal clock and two-sweep continuous germ](packages/interval_global_closure/verify_global_monotone_clock.py)
(1,000 random past-selector reordering fixtures, 34 continuous
one-sided sweep integrals),
[Fraction causal-selector finite LP](packages/interval_global_closure/verify_global_strong_record_duality.py)
(441 atomic threshold pairs and exact rational matching finite
LP witnesses at \(3/2\) for 21 Princess path rows and four
Monster routes).
They audit identities, not the infinite-dimensional
separation proof. No Lean compilation or CI.

**The original game is NOT SOLVED:** no explicit optimal
Monster law/clock, no matching Princess CDF, and no exact
numerical V. Certified value interval unchanged
\(1.4175898349\ldots\le V\le1.4261297228\ldots\).
The *abstract* causal-duality gate is closed, while
explicit coupled free-boundary construction and G2-G5
completion remain OPEN.

## G2 global dual HJB and quantitative all-game reversal support (2026-11-12)

**New unrestricted saddle verification principle:** an arbitrary
completed Monster trajectory law (finite, diffuse, infinite-turn)
plus two causal strict/closed record-selector kernels generates
nonnegative occupation measures \(\alpha^\pm\) of equal mass \(D\).
They give a linear majorant
\[
{\cal L}(F)=D+\int F^-\,d\alpha^--\int F^+\,d\alpha^+
\]
and the **exact unrestricted pure Princess-path upper oracle**
\[
V\le\sup_{|p'|\le1}
\left[D+\int{\bf1}_{p(s)<x}\,d\alpha^-
          -\int{\bf1}_{p(s)\le x}\,d\alpha^+\right].
\]
When those measures have regular densities \(k^\pm\), this is
a single scalar state-constrained Princess HJB with source
\(r(t,y)=\int_y^1(k^--k^+)(t,x)dx\).
A matching unrestricted Monster Bellman lower certificate
closes the game. On strictly unsaturated smooth optimal
Princess-flow regions, **the signed record pressure must
balance**: \(k^-=k^+\). These are exact conditional
free-boundary necessary/sufficient conditions, not an
explicit equilibrium. [Full proof](research/12-global-closure/GLOBAL_DUAL_RECORD_PRESSURE_HJB.md).

**New full-game structural theorem (strengthened):** EVERY optimal
Monster trajectory law \(\nu_*\) assigns at least
\[
\frac{2954811086187555612589991}
{40000000000000000000000000}
\simeq0.07387027715468888
\]
of its mass to **reversing trajectories**. Every nonreversing
completed Monster path is pointwise dominated by a fast
endpoint-to-endpoint sweep. The two sweeps form an exactly
solved infinite-Princess-path subgame of value \(3/2\) with
**unattained** Princess supremum. More importantly, the
approaching fair-reflected Princess runner law also has an
**exact unrestricted Monster-response** of
\((1-\epsilon)/2\), proved by two-target speed-one
separation. The combined two-class response bound and
existing global upper \(U_{\rm best}\) force
\[
 \Pr_{\nu_*}(\text{reversal})\ge3/2-U_{\rm best}>7.38\%.
\]
This is a genuine whole-game restriction on every optimal
Monster law, not an additional upper/lower game-value bound.


**New canonical global support reduction:** there exists a
symmetric unrestricted optimal Monster law with the exact
decomposition
\(\nu_*=(q_*/2)(\delta_{m_+}+\delta_{m_-})
 +(1-q_*)\nu_{\mathrm{rev}}\),
where \(m_\pm\) are the two fastest endpoint-to-endpoint
sweeps and \(\nu_{\mathrm{rev}}\) is supported on genuine
reversing trajectories. The proof pointwise-dominates
EVERY slow nonreversing completed path by the corresponding
fast sweep and pushes any existing symmetric optimal law
forward. This identifies a canonical global support structure
without assuming an optimal finite-turn bound, and separates
the known characteristic sweep record pressure from the
unknown reversing-history record pressure.

An exact BigInt sweep cross-score for the archived 338-path
Princess strategy is
\(18145150023847037/12800000000000000
=1.4175898456130498\ldots\),
only \(1.06951944140625\times10^{-8}\) above that
law's unrestricted lower guarantee. Thus the old strategy
already nearly equalizes both monotone sweeps; merely
reweighting those routes is not a constructive closure.

[Executed exact Fraction physical/selector regression](packages/interval_global_closure/verify_global_dual_two_sweep.py):
429 legal rational Princess polylines plus 29 one-sided germ
families with reflections all passed independently scored
chronological captures and causal record-plane integrals.
A further 259 arbitrary completed Monster prefixes, four
runner epsilons each, and 14 explicit attaining responses
passed the exact physical first-contact regression.
No full-game numerical bound improvement, no explicit optimal
field or Monster law; G2–G5 OPEN. No Lean compilation or CI.

## G2 strategic pivot: exact global CDF transport LP, no finite strategy bank (2026-11-12)

A full-field **infinite linear program** now directly characterizes the
completed-horizon unrestricted Princess security problem, using only (i)
all-time CDF transport inequalities
\(\ F(s,x-(t-s))\le F(t,x)\le F(s,x+(t-s))\ \),
(ii) linear strict/closed first-contact record obstacles, and
(iii) linear integrated survival constraints against **all** completed
Monster trajectories. Every feasible CDF is realized by legal
noncrossing 1-Lipschitz quantile paths; no finite Princess basis,
finite Monster turn cap, prescribed endpoint absorption, or smooth
CDF assumption is used. For its supremum \(L_H\), the prior universal
completion theorem yields exactly
\[
L_H/(1+3/H)\le V\le L_H,\qquad
V=\lim_{H\to\infty}L_H=\inf_{H>0}L_H.
\]

An explicit two-crossing-path example demonstrates that globally
reordering the CDF of a raw finite Princess mixture **strictly beats
every mixture on that fixed two-path bank** against a single legal
completed Monster (mean first capture 2 vs at most 3/2). This is the
mechanism missing from frozen-path mixing; it is **not** an
unrestricted-game improvement.

The new formulation is a **reformulation**, not an evaluated LP or
optimal-strategy construction. The constructive G2 target is now a
joint CDF transport/free-boundary and Monster record-occupation
solution, with actual unrestricted Bellman and CDF stationarity
certificates. [Proof and strict witness](research/12-global-closure/GLOBAL_CDF_TRANSPORT_LP.md).

**No change to certified numerical game bounds. G2-G5 OPEN.**
No Lean compilation or CI.

## G2 two full Monster update rays EXCLUDED and exact four-cut exchange CLOSED (2026-11-12)

New **exact global negative theorem**: two promising one-parameter
Monster adjustments to the old certified 280-pair law have been
**excluded for every valid weight**, not only sampled perturbations.

1. Mixing any mass \(0\le\lambda\le1\) of the archived
   best-response Monster route into the old 280-pair law **cannot
   beat the best certified unrestricted game upper**
   \(U_{\rm best}=1.426129722845311...\). A legal 162-vertex
   Princess has old-law expected capture
   \(A=1.426135310893618...\), and added-route expected capture
   \(B=2.999999982512355...\), so
   \((1-\lambda)A+\lambda B\ge A>U_{\rm best}\).
   More strongly, every \(\lambda>8.97930481038\times10^{-9}\)
   worsens even the *unwarped* 280-pair law's own upper
   \(U_0=1.426135325025829...\).

2. Moving **any** probability mass \(\delta\ge0\) (within
   normalization) from original Monster atom 0 to atom 120
   cannot beat \(U_{\rm best}\). Two exact physical Princess
   payoff cuts have slopes of opposite sign. Their minimax
   intersection occurs at
   \(\delta_*=0.000004620208384168817...\) and forces the
   unrestricted Princess response to be at least
   **1.4261332895524503...**, strictly above
   \(U_{\rm best}\) by **0.000003566707139...**.
   This is a whole-continuum certificate.

[Complete proof and four-column exchange analysis](research/12-global-closure/G2_NEAR_ACTIVE_GERM_SEPARATION.md),
[exact ray verifier](packages/interval_global_closure/verify_g2_ray_exclusions.cjs).

A reusable bank of **four actual legal Princess trajectories**
has been scored against all 281 proposed Monster reflection pairs.
The [rational cut bank](packages/interval_global_closure/g2_near_active_princess_cuts.json)
contains **2,248 independent exact first contacts**.
[Physical replay verifier](packages/interval_global_closure/verify_g2_princess_cuts.cjs)
and [fast exact screening tool](packages/interval_global_closure/g2_princess_cut_screen.cjs)
were executed in the V8 tool environment and pass all four columns.
The screening value is a **lower bound on the Princess response**,
so it can *reject* a candidate Monster law but cannot certify its
global upper optimality.

The underlying reason is now formalized by an exact near-active
Monster-side Danskin derivative: Princess paths with payoffs
arbitrarily close to, but not necessarily attaining, the old
supremum can dominate the directional test. The former practice
of optimizing only saved optimal-face labels is insufficient.

**Unrestricted full-game value interval unchanged; G2 explicit
saddle OPEN.** The two excluded weight rays do not rule out
simultaneous new Monster route geometries, a richer path measure,
or a new Princess CDF. No Lean compilation/CI/native Node run.


## G2 near-active physical response-germ exclusion (2026-11-12)

**New exact global *negative* result, not a solved equilibrium:**
the natural Monster update mixing the old certified 280-reflection-pair
law \(\nu_0\) with the archived Monster best response to the 338-path
Princess law \(\nu_1\) is **provably worse** for every mix weight
\(\lambda>8.97930481037766\times10^{-9}\). The 280-pair law has
unrestricted Princess response
\(U_0=957063215727541539/671088640000000000\).
A concrete *legal 162-vertex Princess path*, reconstructed from the
saved exact light-coordinate label assignment and a rational
\(2^{-28}\) offset, scores \(A\simeq1.4261353108936183\)
against \(\nu_0\) and \(B\simeq2.999999982512355\)
against \(\nu_1\). Thus
\((1-\lambda)A+\lambda B>U_0\) on the entire stated ray.
All **562 individual physical first contacts** were replayed with
exact BigInt fractions; the 1% mixture scores
\(1.4418739576098056...\).

The exact rational exclusion threshold, full physical proof, and
important near-active Monster dual derivative lemma are in
[the G2 germ-exclusion theorem](research/12-global-closure/G2_NEAR_ACTIVE_GERM_SEPARATION.md).
The complete reproducible 243-label/162-vertex witness is in
[the JSON certificate](packages/interval_global_closure/g2_m1_injection_witness.json)
with [standalone exact verifier](packages/interval_global_closure/verify_g2_m1_injection.cjs).
The original exact zero-cost Princess label face shows a *beneficial*
\(1.421874515...\) score against \(\nu_1\); near-optimal
physical Princess paths instead score almost \(3\).
Hence exact face endpoints alone **do not control G2 directions**:
the correct derivative takes a supremum over *arbitrarily near-active*
Princess paths, preserving microscopic contact-side germs.

Further **numerical full Princess-oracle** experiments all failed:
1% dispersed Monster starts \(\to1.44186375\);
0.1% old sweep mass shifted to existing atom 120
\(\to1.42802090\); 0.5% shifted to atom 20
\(\to1.42659319\). These are diagnostic rejected candidates,
not bound certificates.

**G2 remains OPEN.** No new Princess CDF or Monster law
passes both unrestricted saddle inequalities. The best previously
certified unrestricted value interval is unchanged.
The numerical global oracle was executed in the connector's V8;
the 562 exact direct hits were independently replayed in V8.
The new standalone Node wrapper is committed but not separately run
with native Node, and Lean/CI were not run.


**Concrete coupled-candidate rejection:** applying the exact variational
theorem to the archived 338-path Princess / 280-pair Monster law yields
a legal global CDF direction with right derivative at least
**0.0029361293227555024**. The archived pair also has the already
certified Monster improvement **0.0056093417063262557**.
Both are strict positive defects. This establishes that the archived
pair is not a stationary saddle, without conflating a finite-bank
improvement with a new game bound.
[Exact witness](research/12-global-closure/GLOBAL_CDF_VARIATIONAL_STATIONARITY.md#7-exact-nonstationarity-witness-for-the-archived-338-path280-pair-candidate)
and [source arithmetic verifier](packages/interval_global_closure/verify_archived_variational_witness.py).


### G1 exact CDF stationarity: two near-active records (2026-11-12)

For any Monster law completing by a common horizon \(D\), the ordered
Princess capture functional \(\mathcal C_\nu(F)\) is concave in the legal
time-marginal CDF. Its **exact right first variation** against any legal
CDF perturbation \(G-F\) is the time/Monster integral of (i) the
minimum perturbation over arbitrarily near-active *strict lower*
history records, minus (ii) the maximum perturbation over
arbitrarily near-active *closed upper* records. This handles atoms,
record ties and Zeno without a differentiability or unique-selector
assumption.

It yields a **necessary-and-sufficient conditional saddle test**:
if every legal Monster path costs at least \(c=\mathcal C_\nu(F)\)
against \(F\), and every legal CDF direction has
\(D^+\mathcal C_\nu(F;G-F)\le0\), then the *full unrestricted*
game value is exactly \(c\). Directional residuals \(\epsilon_M\)
and \(\epsilon_P\) give the sound bracket
\(c-\epsilon_M\le V\le c+\epsilon_P\). This constructs **the
mathematical coupled free-boundary inequality**, but it does not
produce an explicit candidate \(F,\nu,c\).
[Hand proof](research/12-global-closure/GLOBAL_CDF_VARIATIONAL_STATIONARITY.md)
and [exact tie/nonattainment fixture](packages/interval_global_closure/verify_cdf_record_variation.py)
(3,375 finite algebraic cases, including 2,625 tied records, plus
six explicit nonattained-record enclosures). No Lean compilation or CI.


## GLOBAL G1 CLOSED: full-game minimax, Monster attainment, and uniform horizon/rank reduction (2026-11-12)

A new **unrestricted** theorem proves the Princess security supremum equals
the Monster mixed minimax and that an optimal **symmetric Monster
probability law on complete trajectories exists**. This is not just a
finite-bank statement: no assumption of an endpoint-absorbed Princess
law, Monster turn-count cap, or finite action horizon is used.
The minimizing Monster path space is compact in the local-uniform
topology, and first-contact time is lower semicontinuous in the
Monster path. A finite-dimensional upward-closed separation and
compactness argument proves the full lopsided minimax equality without
incorrectly assuming upper semicontinuity for the maximizing Princess.
An attained Princess optimizer is **not** claimed.

The unrestricted game also has an explicit **two-sided uniform
rank/horizon approximation**. Let \(V_{H,n}\) be the security value
when Monster must visit both endpoints between \(H\) and \(H+3\),
and Princess uses \(n\) equally weighted *reflected ordered-quantile
pairs*. Then
\[
V_{H,n}-6/H\ \le V\ \le
V_{H,n}+(H+3)/(2n).
\]
Thus \(H=\sqrt{12n}\) gives a bracket of width at most
\(2\sqrt{3/n}+3/(2n)\). These are **finite path-support and
finite horizon** bounds, not a finite-turn or finite-dimensional LP
reduction; arbitrary Lipschitz path shapes remain.

Exact global \(\epsilon\)-complementarity bounds are also established
for both supports. A separate explicit pair of Monster trajectory
laws proves that **identical time-marginal spatial CDFs can have
different first-contact expectations**: capture means \(2\) versus
\(67/20\) against the same stationary Princess. Thus an optimal
Monster strategy cannot be specified by its one-time CDF alone:
the complete trajectory coupling is essential. The Princess CDF
remains sufficient via ordered-quantile dominance.

[Complete hand proof](research/12-global-closure/GLOBAL_MINIMAX_AND_CDF_DUALITY.md)
and [independently executed standard-library exact test](packages/interval_global_closure/verify_global_minimax_reduction.py).
The locally executed test passed 36,057 exact two-tail grid cases,
seven endpoint-completion cases, and the complete rational
CDF-coupling counterexample; the infinite-dimensional claims are
proved analytically, not mechanically by those fixtures.
**No full-game numerical bound changed; no explicit optimal CDF/Monster
support is constructed; no Lean compilation/CI.** The constructive
G2–G5 saddle gates remain OPEN.


## New exact all-count two-source Green/Zeno envelope (2026-11-12)

**Closed component, not the unrestricted game:** in the saved affine
prescribed-terminal wedge, \(1/20\le H=b-t\le1/16\) and
\(0\le y=n-Z(t)<kH\), the infimum over **every finite productive
no-initial-wait center-return chain ending at \(b=15/16\)** is now
explicit. For \(0\le y\le2H/5\) it equals the smaller of the actual
single-return cost \(E_1(H,y)\) and the two-source Green limit
\[
 E_\infty(y)=-9\ell\theta/4-\theta y^2/(4\ell)-y^2/(8k).
\]
For \(2H/5\le y<kH\) the single return wins for *all* counts.
The unique switching surplus \(y_*(H)\) is the smaller quadratic root
in [the complete hand proof](research/12-global-closure/TWO_SOURCE_GREEN_ZENO_ENVELOPE.md).
Explicit, genuinely productive, no-hinge *finite* duration words with
arbitrarily many returns attain the low-surplus infimum in the limit;
no unproved Zeno hitting-time continuity or finite-turn cutoff is used.

The decisive count-uniform estimate combines exact constrained Green
completion with a rational parameter inequality valid on the full
\(H\in[1/20,1/16]\), \(0\le y\le2H/5\) strip. The
[Fraction verifier](packages/interval_turn_sheet/verify_two_source_outer_envelope.py)
passed the exact inequality, two switching-sign bounds, and six
independent rational productive-sequence energy fixtures. Terminal-Zeno
policies without earlier reset cannot improve the infimum by the prior
rank-band estimate. This is an **exact local all-count solution**, not
a Princess law or Monster equilibrium against every initial start.

**OPEN:** low-surplus \(H<1/20\), initial waits/resets, earlier/later
exterior exits, arbitrary initial prefixes, and matching unrestricted
Princess/Monster CDF/path-law saddle. The game bounds stay unchanged.
No Lean or CI run.


## New closed gate: all-count one-return dominates outside the narrow front strip (2026-11-12)

**Exact mathematical theorem:** in the saved affine terminal center wedge, for every
\(0<H=b-t\le1/16\) and initial balanced surplus \(2H/5\le y<kH\),
the one-return center tent ending at \(b=15/16\) beats **every** finite
productive no-initial-wait chain with two or more returns. This includes
all initial/interior/final hinges by the previously proved short-hinge
deletion, and extends to prescribed terminal-Zeno accumulations by the
already verified shrinking-rank limit. There is **no turn-count cutoff**.

The prior high-surplus theorem covered only \(y\ge3kH/8\), equivalent to
\(y/H\ge3.93539\). The new cutoff is \(y/H=0.4\): more than **96.18%**
of the nominal productive surplus interval is covered, leaving only
\(0\le y<2H/5\) for any multi-return competition in this fixed-terminal
sector. An all-count two-source Green completion bound and an exact
four-corner convexity certificate provide a strict \(1/125000\) energy
margin on the intermediate strip for hinge-free chains.

[Full hand proof](research/12-global-closure/LOW_SURPLUS_UNIFORM_SINGLE_RETURN.md)
and [executed exact Fraction verifier](packages/interval_turn_sheet/verify_single_return_outer_strip.py).
**Not a global game bound or either player's optimal CDF:** initial waits,
earlier front resets, exterior exits, earlier prefixes, and matching
unrestricted laws remain open. Neither Lean nor CI was run.


## Finite two-source short-hinge classification CLOSED (2026-11-12)

A new exact **all-short-hinge deletion theorem** closes the remaining
initial and interior strict short-return hinges of the saved affine,
prescribed-terminal center-renewal problem. A short productive return
followed by another productive return can be merged, reducing the actual
balanced continuation cost by at least `k p q/4>0`, provided its
previously verified affine inverse and exterior monotonicity gates hold.
For any short action with two later productive returns, those gates follow
from the next productive rank inequality. The proof compares the genuine
future captured-rank bands: the merged route may make a later return
nonproductive, so naively evaluating the new duration word by the
*productive-only* energy formula would be invalid.

At the special terminal row `b=15/16`, a separate exact calculation
closes a short penultimate return with margins at least `ell p`
for a two-return chain, or `k p q/4 + 31 ell p/32` for longer chains.
Together with the previously proved strict final-hinge merger, this
eliminates **every active short-hinge class** from the finite productive
fixed-terminal optimization. It leaves the explicit one-return branch
and the convex no-hinge tridiagonal Green problem, with exact productivity,
rank, and duration constraints. No fixed turn-count cutoff is assumed.

[Hand proof, all three hinge classes, and scope](research/12-global-closure/LOW_SURPLUS_ALL_HINGES_EXCLUSION.md)
and [independent exact verifier](packages/interval_turn_sheet/verify_short_source_mergers.py).
The executed and committed standard-library script agrees byte-for-byte;
its **15,480 exact checks** include 5,760 independent two-source kernel
identities, 3,240 terminal-special merger tests, and 6,480 direct rank-moment
continuations, including newly nonproductive suffixes.

The same forward inequality also rules out every finite-index short
hinge in a countably infinite productive chain accumulating at the
prescribed terminal row. A third positive return exists before the
accumulation, and the captured-rank-band inequality is valid for
arbitrary infinite future policies with the same endpoint tour. Thus
any optimal *terminal-Zeno* chain must satisfy all nonshort
conditions `d h1>=y, d h_j>=ell h_(j-1)`. Infinite turns
remain possible; short hinges do not. This does not cover an earlier
front reset or accumulation interface.

**Still OPEN:** optimization over *all* no-hinge turn counts, intermediate
center resets, alternate terminal/exterior exits, global Princess-law
construction and the original unrestricted saddle. This exact *local*
classification alone does not tighten the unrestricted game-value bounds.

## Entire terminal short-hinge class CLOSED (2026-11-12)

**Another exact all-surplus, all-count theorem:** For any productive
prescribed-terminal affine renewal chain with `0<ell/k<1/8`,
duration `H<=2`, and an active terminal short hinge
`ell h_(m-1) > (k-ell) h_m`, replacing the final two excursions by one
strictly lowers the *exact balanced renewal energy* by at least
`(15/32) ell h_(m-1)`. The merger preserves productivity; the physical
conclusion is conditional on remaining in the same verified affine wedge.
This theorem does not require high initial rank surplus and works for
every finite turn count and all earlier hinge patterns.

Therefore **no energy-minimizing productive finite chain can have a
terminal short hinge**. A repeated finite merger removes any such
terminal-hinge branch without requiring a turn cutoff. The saved small
terminal wedge satisfies all geometry gates. The high-surplus one-return
result below also extends through terminal Zeno accumulations, by an
explicit captured-rank-band bound.

[Complete proof of four theorems/corollaries](research/12-global-closure/HIGH_SURPLUS_SINGLE_RETURN.md),
[locally executed exact verifier](packages/interval_turn_sheet/verify_high_surplus_single_return.py).
The independent verifier now passes **1,781 rational fixtures**:
980 saved-field two-through-eight-return energy/moment comparisons;
288 wait-departure comparisons; 60 combined waited-chain cases;
165 saved-field terminal-hinge merger/physical moment checks; and
288 universal-ratio/duration arithmetic checks. The committed script has
the exact SHA of the locally executed source. No Lean or CI run.
The actual full game bounds and G5-G8 status remain unchanged.

## High-surplus ALL-COUNT center-return region CLOSED (2026-11-12)

**New exact theorem, not a global game bound:** In the saved terminal affine
wedge with terminal row b=15/16, let H=b-t<=1/16 and rank surplus
`y=n-Z(t)`. Whenever `(3/8) k H <= y < k H`, every legal productive
center-return chain of **two or more turns** ending at b, with no initial
wait, costs at least `mu H` MORE than the single return at b. The exact
constant is
`mu=400295280226865161073511/67164016785510400000000000
 =0.005959966353787564...`.

This is a uniform, **all-count, all-short-hinge** comparison, not an
empirical cutoff. It eliminates the top five-eighths of the nominal
physical surplus interval from the difficult multireturn terminal-chain
problem. A separate exact theorem makes the cost of a one-return policy
after center waiting **strictly concave in its departure time**. The
combined corollary eliminates both arbitrary later turn counts and all
intermediate waiting choices until the first high-surplus boundary:
only immediate one-return and the boundary one-return need comparing.

[Hand proof and precise gates](research/12-global-closure/HIGH_SURPLUS_SINGLE_RETURN.md)
and [rational verifier](packages/interval_turn_sheet/verify_high_surplus_single_return.py).
The exact executed standard-library verifier passed **980** independent
physical-renewal/full-energy comparisons, **288** departure-time checks,
and **60** combined waited-chain checks, and was byte-matched to the
committed Git file. No Lean compilation or CI is claimed.

Still OPEN: low-surplus all-count hinge configurations, longer center waits
and front resets, competing exterior exits, attaching the local result to
a legal full Princess law, and matching unrestricted game strategies.
The rigorous full-game value interval is unchanged by this checkpoint.

## Tightened all-continuous-warp ceiling (2026-11-12, current)

**New exact theorem, restricted to the common-coordinate-warp orbit of the
archived 338-path Princess law:**

`36290299773897097/25600000000000000`
` <= sup_warp inf_monster E[T] <= `
`567055553277100451603891/400000000000000000000000`
` = 1.4176388831927511290097275`.

The gap for this **restricted warp family** is now **exactly**
`19619309958310978891/400000000000000000000000
 = 0.000049048274895777455`. Compared with the preceding all-warp
ceiling `1.425272697457848...`, this narrows that interval by about
**99.36%**, with no assumption of fixed warp knots or derivatives.

A rational mixture of 35 actual legal Monster routes (9 archived attacks,
one full sweep from -1, and 25 additional positive-start sweeps)
controls every strictly increasing continuous odd period-two common warp.
The independent exact verifier passed 11,830 two-method first-contact
comparisons, all 84 step thresholds, and 80 exact ramp-integral checks.
See [tightened hand proof](research/12-global-closure/LOWER_WARP_ALL_TIGHTENED.md),
[exact certificate](packages/interval_global_closure/common_warp_lower_all_tight.cert.json),
and [exact verifier](packages/interval_global_closure/verify_lower_warp_all_tight.cjs).
These mathematical checks passed V8; no native CLI, Lean compilation, or
CI is claimed.

**The unrestricted full-game bound remains UNCHANGED:**
`1.417589834917855... <= V <= 1.426129744306782...`.
Neither the fixed-law warp orbit nor the new 35-route Monster law is
certified as a full-game equilibrium. G5-G8 are OPEN. The older all-warp
ceiling below is retained as a historical (now superseded) restricted
certificate.

## New ALL-common-warp ceiling (2026-11-12)

A complete **all-resolution** common light-coordinate warp certificate is now
proved for the archived 338-path Princess law. Thirteen physical Monster
routes, with rational weights summing to 1, give the rigorous restriction

`sup_psi inf_m E[T(m,P_psi)] <= 570109078983139212403/400000000000000000000
 = 1.4252726974578480310075`.

Here psi ranges over **all** continuous strictly increasing odd maps with
psi(u+2)=psi(u)+2, including smooth and non-piecewise-affine warps.
The complete 75-threshold step envelope covers the continuum; 4,394 exact
first-hit evaluations and 16 independent ramp-integral checks passed V8.
The proof and executable certificate are at
[LOWER_WARP_ALL_EXACT_CEILING.md](research/12-global-closure/LOWER_WARP_ALL_EXACT_CEILING.md).

This ceiling is strictly below the existing full-game upper certificate
(1.42612974430678...), so these warped laws cannot match that current
upper target. **It is NOT a new unrestricted game upper bound**, nor a
proof that this class cannot attain a smaller unknown equilibrium value.
The earlier 16-knot ceiling (1.41758984127931...) is numerically much
tighter on its restricted grid. Both results remain valid, with different
scope. G5-G8 and the exact game value remain OPEN.

## New global lower deformation exclusion (2026-11-12)

The archived 338-path Princess law is **already globally optimal to within
6.37e-9 inside its entire family of common increasing light-coordinate
warps on the uniform 16-knot grid**. An explicit 16-route Monster mixture
has exact rational weight denominator 10^12. Its complete 5,408 first-hit
integer certificate proves the **restricted-family ceiling**

`2268143746046896063134267573/1600000000000000000000000000
 = 1.41758984127931...`

against **all** such warped Princess laws, including approaching flat
warps. The archived unrestricted lower guarantee is
`36290299773897097/25600000000000000 = 1.417589834917855...`.
This new ceiling is *not* a full-game upper bound and is *not* a new
full-game lower bound. It closes the coarse common-warp direction and
shows that changing the lower law's mass/transport shape is necessary.
The exact executable verifier and complete derivation are at
[LOWER_WARP_16_EXCLUSION.md](research/12-global-closure/LOWER_WARP_16_EXCLUSION.md).
The exact score checks passed in V8, not as a separately executed Node
CLI wrapper. Finer 32-knot discovery did not finish its unrestricted
response iteration and supplies no certificate. The full game remains
**OPEN** with unchanged rigorous interval and unmatched strategies.


**Current revision:** 2026-11-12 UTC.

**Problem.** Both players independently choose hidden 1-Lipschitz paths in the interval [-1,1], including their starting positions. Capture occurs at the first coincidence. The monster minimizes and princess maximizes expected capture time. No prescribed maximum number of turns; both can randomize privately.

**Definitive open item:** The exact minimax value has **not** been determined. There is no pair of matching unrestricted upper/lower saddle certificates and no theorem that all equilibria lie in a fixed bounded-complexity support family.

## Latest continuation: effective fixed-fan responses and global selector optimization

The fixed-fan response gap is closed: a computable integer N, obtained from
the complete CDF arrangement, bounds the pieces of some optimal unrestricted
Monster response to each fixed ordinary positive-width fan. The first
stationary-contact lemma, quantitative source width, characteristic confinement,
and chronological degenerate transfers provide the global count. Rational
or algebraic fan data admit a terminating exact response procedure in principle.
The count can be large and is not uniform over vanishing widths or all Princess laws.

A separate exact oracle now maximizes every finite causal-selector linear CDF
functional over all legal Princess paths, with actual rational approximations
and an explicit physical error. Its full 26-pair test, independent DP, contact
conventions, physical scores, and effective-bound arithmetic passed root V8 replay.

The selector formulation also has an exact finite-bank minimax theorem,
using compact payoff profiles rather than an invalid contact-continuity claim.
Its two-oracle synthesis terminates at each positive fixed-bank tolerance.

These are response theorems and construction tools. There is still no matching
unrestricted saddle or exact game value; the established bounds are unchanged.
No native replay, Lean compilation, or CI is claimed.

See [the checkpoint](research/12-global-closure/EFFECTIVE_RESPONSES_AND_GLOBAL_SELECTOR_ORACLE.md),
[the effective bound](research/12-global-closure/EFFECTIVE_FAN_RESPONSE_BOUND.md),
and [the global selector theorem](research/12-global-closure/GLOBAL_SELECTOR_PLANE_ORACLE.md).

## Previous continuation: local initial-prefix normal forms and exact fan separation

A local initial CDF source with one affine cell or two stationary density
half-cells now has an all-count finite-piece normal form. The single-cell
rank moment is concave. At a density interface the naive concavity extension
fails, with a preserved exact positive-curvature witness; arbitrary-excursion
normalization and a physical crossover deletion repair that argument.
A sufficiently short interface return block needs at most five tents,
and its final partial half-cell bridge gives at most 15 affine pieces.
The stated affine future-persistence condition is essential.
The separately labelled interface-return extension covers old captured bands.

For every fixed finite positive-width unit/wait fan, these local results
also prove existence of an optimal Monster response with finitely many affine
pieces. With ordinary rational fan data, the response value and some optimal
vertices are algebraic. This is an existence theorem; it supplies no effective
piece count and makes no algebraicity claim about the full game's value.
See [the proof](research/12-global-closure/FINITE_FAN_RESPONSE_EXISTENCE.md).

Exact supplied-route ordered fan costs, weight superplanes, and complete
continuous initial-start arrangements are implemented. The M1 and fixed-tail
separators distinguish raw mixtures from the common-quantile law and include
the extra event/rank cuts needed for the latter. Reflected endpoint fans have
their own legal physical construction and exact marginal/selector provider.

One entire reflected-fan candidate basis is now excluded: for all weights
on its 342 ordinary profiles at fixed width 1/1024,26 legal Monster reflection pairs
give a verified ceiling approximately1.415422716576155, below the already
proved unrestricted lower bound. This is a restriction-of-basis certificate,
not a full-game upper bound. All 8,892 coefficient enclosures and the final
strict comparison were replayed by exact integer arithmetic. The same
Monster mixture has an unrestricted Princess response around1.5474683,
with two separately realized legal approaching witnesses.

The unrestricted game bounds remain unchanged. These local normal forms
and exact separators do not establish a globally sufficient equilibrium
class or a matching saddle. Exact V8 checks completed while native execution
was unavailable; no native replay, Lean compilation, or CI is claimed.

See [the checkpoint](research/12-global-closure/LOCAL_PREFIX_CLOSURE_AND_FAN_ORACLES.md)
and [the whole-basis exclusion](research/12-global-closure/REFLECTED_FAN_BASIS_EXCLUSION.md).

## Previous continuation: finite center continuations and exact static tails

For an ordered common-quantile law made from finitely many fixed translation
intervals of unit/wait base paths, the center continuation now has an explicit
finite productive-return bound. A finite time partition supplies stationary
center diamonds, and a future-independent merge inequality gives at most
2J-1 productive balanced returns before the base paths become stationary.
Arbitrary center histories and growing Zeno entrances are included by a
uniform quantile-approximation argument. Initial same-side prefixes remain
a separate obligation.

The stationary tail is solved exactly for every bounded piecewise constant
density plus finitely many atoms. Productive turns reduce to density/atom
boundaries, and an exact O(K^2) dynamic program returns the optimal route.
The reduction includes arbitrary infinite histories and closed atom contacts;
stationarity alone does not justify a direct endpoint-tour shortcut.

For the older frozen field, the early constant cone now has an exact
attachment formula in terms of its actual exit data, and the entire middle
strip has a strict productive-duration gap giving at most 38 returns.
A new two-extrema envelope strengthens arbitrary first-prefix moment bounds
without claiming one path attains every pointwise maximum.

The fixed translation-interval scorer and its strict/closed marginal provider
have independent exact replays, including asymmetric/outward intervals.
No successful global lower candidate or matching saddle is inferred from
these structural theorems. The native ordered-weight optimization was
interrupted before its new controller files could be written. The exact
game bounds remain unchanged. No Lean compilation or CI was run.

See [the checkpoint](research/12-global-closure/FINITE_CENTER_AND_STATIC_TAILS.md),
[finite fan-center returns](research/10-turn-density/FAN_FINITE_CENTER_RETURNS.md),
and [the exact stationary-tail theorem and DP](research/12-global-closure/STATIC_TAIL_BOUNDARY_REDUCTION.md).

## Previous continuation: complete terminal-center gates and fixed-tail starts

The supplied field now has two complete unrestricted center regions.
For all times from 7/8 through the explicit threshold
t_L=9321277864605/10363024948016, sufficiently high captured ranks have
exact value equal to the actual exterior envelope. From t_L through
15/16, the same equality holds for EVERY admissible center rank.
The proofs include productive waits, all exterior returns, closed
endpoint contacts, arbitrary turn counts and accumulation.

The immediate exterior envelope on the entire front [7/8,15/16] is also
proved to be the single return at 15/16. The rank-removal construction
covers the interval between the earlier Zeno regime and the late
all-record regime without needing each front-count transition separately.
The entire earlier low-record FIRST-arrival region now has an exact
shared-budget prefix certificate at 7131/5000 = 1.4262. Its saved replay
checks 874 covering boxes, over three million rational envelope comparisons,
and 108 independent physical-prefix comparisons. The first-arrival slab is
therefore reduced to the known exterior continuation or excluded by this
strict cost margin. Low-record intermediate arrivals and earlier center
waves remain; these local results do not close the original game.

A new fixed-tail theorem reduces continuous Monster initial positions to
actual Princess initial atoms and legality boundaries. Its exact separator
finds a two-turn attack from 3/16-epsilon against the pinned M1-repaired
candidate, with cost approximately 1.405281110684115. That is a candidate
rejection, not a game bound.

The coupled search preserves all physical paths. Its complete initial M1
universe covers zero-weight rows too. The saved 349-pair,1465-atom state,
the earlier full matrices and exact geometry are recoverable from verified
text-safe compressed snapshots. Numerical master values and unfinished
full response searches remain explicitly separate from certificates.

The global bounds are unchanged and a matching unrestricted saddle is
still missing. No Lean compilation or CI was run.

See [the complete checkpoint](research/12-global-closure/TERMINAL_CENTER_AND_FIXED_TAILS.md),
[the late center theorem](research/10-turn-density/CENTER_LATE_EXTERIOR.md),
and [fixed-tail initial reduction](research/12-global-closure/FIXED_TAIL_INITIAL_REDUCTION.md).

## Previous continuation: exact conditional value and fixed physical strategies

The supplied affine-center continuation is now solved exactly on its stated
front interval, including an attaining continuous path with accumulating
turns. Its full algebraic lower certificate and finite-truncation attainment
calculation were independently replayed. This is a conditional state value;
the full unrestricted interval game remains open. The transformed front
branch is slack for the current global target, so work continues on the
off-front states and their actual exterior exits.

The retained 159-path finite-bank candidate is rejected. Complete all-start
M1 separation finds an attack from `15/16-epsilon` with limiting cost
`4115606858452227030094659793/3276799999999999976930082816`
(approximately 1.25598). Its fixed first-leg prefix alone caps any tail
repair at approximately 1.27910.

The coupled search now preserves actual physical paths when adding attacks.
All 172,833 entries of the initial 159-by-1,087 exact limiting payoff matrix
are complete. Reweighting that finite matrix gives approximately 1.41431,
not a game bound. Generalized infinitesimal realizations, an unrestricted
germ upper-response oracle, exact frozen-pair scoring, and complete M1
separation have independent replays. A collapsed ordinary Monster companion
has no larger unrestricted response, but remains a separately evaluated law.

The exact global bounds below are unchanged. No matching unrestricted
saddle, exact game value, or Lean kernel proof is claimed. No Lean
compilation or CI was run.

See [the current checkpoint](research/12-global-closure/EXACT_CENTER_AND_FROZEN_EXCHANGE.md),
[the algebraic center value](research/10-turn-density/AFFINE_CENTER_ZENO_ATTACHMENT.md),
and [the frozen-path contract](research/12-global-closure/FROZEN_GERM_ROWS.md).

## Previous continuation: exact center chains and avoided-center construction

The full game remains open. This checkpoint closes specified center-return
components and preserves a construction issue that matters for the missing
lower strategy: an approaching path that reverses just before zero can have
a different adaptive response value from a path that touches or lingers near
zero. The same limiting priced labels do not determine this value.

For the supplied affine slab, the front-to-front continuation with a prescribed
final return has an exact all-count quadratic solution. Increasingly ordered
excursion lengths absorb every hinge correction, and a tridiagonal KKT
certificate selects the optimal number of excursions. The count thresholds
accumulate at a geometric infinite-return limit. Independent replay passes
6,072 checks. Separate chain/reset identities and the complete last-crossing
envelope are also exact; the latter includes every exterior cell, endpoint
contact, and inverse breakpoint. These are local and supplied-law results,
not a matched lower strategy for the game.

The common-warp compiler now covers all 301 early-family cells and 3,502 late
edges, with 129,302 exact basis/quarter comparisons. Both complete coefficient
tensors were independently rebuilt and their Git blob hashes reproduced.
The five-family optimization is rejected by a missing early positive-side
attack. The initial-to-center identity isolates the exact captured-rank moment
that an arbitrary same-side prefix must contribute; a finite prefix family is
not assumed exhaustive.

One strictly increasing common-coordinate update of the 280-pair Monster
law is frozen with exact unrestricted response
`57045189772271291487410009/40000000000000000000000000 = 1.426129744306782287185250225`.
The independently replayed integer flow/cut and all 560 physical captures
certify this upper strategy. Further geometric value iterations are not
being used as a substitute for the missing saddle construction.

The two exact extremal response profiles require isolated avoided-center
bounces; they cannot be replaced by center contacts. Their entire exact face
also has a cheap common Monster attack, so it is not a lower law. A separate
two-path example proves an adaptive-value discontinuity of exactly 1/2 for
an avoided bounce. Rational-function arithmetic now retains all infinitesimal
capture orders, with 12 independently replayed standard regressions.
Objective-only limit pruning has a finite uniform lower/upper sandwich and
passes those regressions plus two unequal-germ/equal-limit tests. A completed
supplied-law search certifies only that law's limiting response; an unfinished
search gives only an explicit attack.

The full-bank 159-path dual mixture and a new avoided-bounce realization are
under investigation. No response guarantee is assigned before their adaptive
search completes. No Lean compilation or CI was run.

See [the checkpoint and scope ledger](research/12-global-closure/CHAINS_AND_AVOIDED_BOUNCES.md),
[the exact upper package](packages/interval_common_warp/README.md), and
[the reproduction commands](REPRODUCE.md).

## Previous continuation: center renewal and common geometry

The center continuation now has an exact imbalance factorization. If the
captured radial prefixes are r<=n, its remaining absolute value is
J(t,r,n)=(1/2) integral_r^n beta_t(q)dq+V(t,n). This holds for arbitrary
legal continuations, including accumulating turns and exact contacts.
A two-variable potential W(t,n)=V(t,n)+T_t(n)/2 therefore suffices at
center returns. Independent exact replay passes 19,722 physical repair,
capture, and renewal checks.

The early constant cone has an analytic quadratic potential whose internal
triangle residual is a square. A general incoming affine cell with
0<=(-R_V)/R_U<1/8 has an exact Riccati component and a geometrically
accumulating local response, with 30,864 independently replayed rational
checks. Crossing actions and the exterior attachment remain necessary;
the candidate's final slab does not admit the naive constant-front or
single-crossing attachment. No global potential at a matching value is
asserted.

A separate full-record boundary certificate handles the high-start center
and post-one continuations without resetting the rank records at U=1.
The late negative-M2 family is now minimized over ALL continuous starts
and turns by 3,502 exact quadratic edge checks. Its minimum on the
original field is the already known fixed-one exclusion, now with all
later turns included.

Common increasing odd light-coordinate warps give a bijection of legal
controls. Fixed-law lower response is concave in the warp, upper response
is convex, and flat limiting warps have a uniform approaching realization.
An attained saddle must satisfy the resulting capture-coordinate symmetry.
The first strict lower warp is rejected by a complete fixed-one M2 audit:
its finite-bank improvement misses a legal cost of about 1.42013860114.
This is an actual rejected geometry update, not a lower guarantee.

The earlier 280-pair upper certificate is preserved and has been replayed
again in the independent V8 workflow, including all integer conservation
and cut equations and a physical response. The established game bounds
are unchanged by this continuation. The exact unrestricted minimax value
and matching strategy pair remain OPEN; G5-G8 remain unchecked.

The second native executor outage left the newest gated field bytes and
the final native early-gate program unavailable. Their native hashes are
not represented as remote uploads. All newly listed standalone center,
boundary, edge, and warp computational bodies were actually executed.
No Lean compilation or CI was run. See
[the center and geometry checkpoint](research/12-global-closure/CENTER_AND_GEOMETRY_CONTINUATION.md).

## Previous continuation: constructed strategies and unrestricted responses

**G5-G8 remain open.** The upper side now has an actual normalized rational
law with 280 reflected pairs and exact unrestricted response supremum
`957063215727541539/671088640000000000 = 1.426135325025828985869...`.
Its integer flow/cut certificate has been independently replayed, and its
extremal query payoffs agree in the separate Python Fraction model.
An actual rational princess response is within `1.91e-8` of this supremum;
all 560 oriented first capture times were independently checked.

The computational bottleneck in the 909-pair bank is resolved: a small
normalized master keeps every monster column and invokes the unrestricted
princess separator after every proposed mixture. The exact law above is
one frozen checkpoint; full-bank optimality and full-game optimality are
not inferred from it. The bank now incorporates complete CDF dual routes
and physical attacks, and the frozen checkpoint contains 1,086 columns.
A common dyadic map preserves every light-coordinate equality and order;
the resulting law was independently recertified. Independent rounding of
physical turns is not a safe substitute for preserving those relations.

The lower side constructs full legal CDFs and searches arbitrary-turn
physical paths on their native characteristic graph. A previously converged
finite-bank field was defeated by a two-interior-turn route with a first
outward turn at `U=1+2^-18`. The repaired search includes every native M2
turn, all 54,145 native initial-inward routes, and center waits. Adaptive
record refinement closed the response objective on the declared H3 node
graph at approximately `1.42103472748`; it does not eliminate the remaining
spatial-grid restriction. Longer-horizon CDF optimization also continues.
No new all-Monster lower guarantee is claimed from these discovery runs.

Center waits in a symmetric Monster law can be replaced by closed unit-speed
excursions without worsening its unrestricted upper response. The proof
covers any finite number of initial or intermediate center waits. It does
not transfer old attack payoffs against Princess laws with center atoms.

See [the explicit law, response, and certificate](research/12-global-closure/EXACT_UPPER_CHECKPOINT.md).
No Lean compilation or CI was run.

## Explicit pair and individual best responses

The archived 338-path Princess law and new 280-pair Monster law have now
been played against each other exactly. Their cross payoff is
`74616624991393892648392565953/52428800000000000000000000000`,
approximately `1.4231991766241816`. The Monster's maximum unilateral
improvement is `0.005609341706326255653...`; the Princess's improvement
supremum is `0.002936148401647378654...`. This is an explicit approximate
saddle pair for the unrestricted game. It does not tighten either
established game-value bound.

Two independent first-hit implementations agreed on all 94,640
representative pair encounters. The archived optimal Monster route was
rescored exactly against all 338 Princess paths. The global response
certificates are imported; this new cross-play replay is separate.
It was completed in V8 after the general executor became unavailable.
See [the laws, exact regrets, proof, and best responses](research/12-global-closure/EXPLICIT_STRATEGY_PAIR.md).

## Latest computational endpoint

The execution environment became unavailable during the next global searches.
The exact 280-pair upper certificate above is durable and unchanged. A tested
faster exact finite-law response engine was recovered byte-for-byte against
its recorded SHA256 and is preserved with its executed verifier. The late
512-path search did not finish and gives no new lower bound.

[The interruption ledger](research/12-global-closure/CONTINUATION_INTERRUPTED.md)
distinguishes completed observations, unavailable late inputs, reconstructed
source, and unexecuted design. It preserves concrete global routes to the
remaining lower certificate: a joint free-field/moving-atom construction and
a Bellman residual potential with explicit center and endpoint obligations.
No matching saddle or new lower guarantee is claimed.

## Previous continuation: whole-strategy optimization and exact limiting tests

**G5-G8 remain open. No matching unrestricted pair or new game-value bound
is claimed.** The work now uses global candidate tests instead of extending
the sequence of local response lemmas.

A common order-polytope LP optimizes an entire supplied finite monster bank
against every princess path. A 472-pair fixture is exactly reconstructed
and independently cut-checked at `219625051/152700512`. Adding the archived
upper support gives a 531-pair numerical solve whose active support remains
the old 67 pairs. These are fixed-bank results, not equilibrium-support
sufficiency theorems.

An exact rational-function capture-order oracle checks approaching lower
laws uniformly over all monsters, including epsilon-dependent initial
positions and turns. It rejects the coarse canonical lower counterpart:
its unrestricted response limit is only `108090289/152700512`, attained by
a straight-left sweep. A corresponding attack also defeats the larger
canonical counterpart. These are rejected-law payoffs, not bounds on V.

Diffusing the coarse responses uniformly inside their entire deadline
corridors also fails. One fixed endpoint sweep gives the whole approaching
family, and every coupling of its marginals including ordered quantiles,
limsup payoff at most `34192713983279/29347816802304 < 7/6`.
Both rejected constructions are stopped; no local repair is claimed.

The fixed 909-pair reoptimization using prior active field routes did not
finish in its bounded run or its same-bank interior-point fallback. It
returned no candidate value or normalized strategy. The saved run status
distinguishes this computational limit from the exact candidate exclusions.

See [the global checkpoint](research/12-global-closure/README.md) and
[reproduction instructions](packages/interval_global_closure/README.md).
Exact Python checks were executed, including independent rational
capture calculations, global-cut equality, and the continuum exclusion.
No Lean compilation or CI was run. Concurrent commit `2a8b53d` and its
exact face/record certificates are preserved below.

## Previous continuation: exact response faces and full mixed-CDF attacks

The archived 67-pair upper law now has a replayable exact integer
maximum-flow certificate for its unrestricted response supremum. An
independent replay checks all capacities, conservation equations, source
reachability, exact agreement with the archived probability law, and the
complete residual face (10,125 strongly connected components). This is an
exact supplied-law certificate, not an optimal-law proof.

The finite-law monster oracle now searches implicit ordered quantiles
without expanding their full crossing arrangement. Its complete regression
suite and the archived 60-path optimum were independently reproduced.
A separate exact scorer integrates the full ordered marginal mixture of
the continuous field and finite paths, including capture atoms. It rejects
the interim round-41 candidate with exact off-support routes. Shrinking a
shared path perturbation does not resolve the earlier incoming-contact
defect.

The high-start pre-center delayed branch with second turn s>=1 is now
closed for the specified field, using whole-region record Bellman checks
and constraints implied by the monster's history. Delayed U<s<1 and the
complete unrestricted lower certificate and matching strategy/value remain open. The established rigorous value
interval is unchanged. See
[the exact-face checkpoint](research/10-turn-density/EXACT_FACE_CONTINUATION.md)
and the linked source certificates for executed checks and precise scope.

## Earlier continuation: global atomic response and exact response regions

The finite-law upper response now has a single global survival-cut
formulation. It includes arbitrary starts and turning histories, retains
strict-contact approach sides, and reproduces the existing certified
67-pair upper law's response. A normalized optimal law has not been
constructed.

On the lower side, exact continuous-start checks show that the frozen
endpoint_joint_i1 field fails both fixed-U=1 M2 signs and an early M3
region. Whole geometric response cells replace sampled starts/cutoffs.
General initial inward/outward routes and their center-contact boundary
now have explicit first-moment formulas, including free second turns
and endpoint atoms. The remaining record Bellman inequalities and the
matching saddle construction are open.

The original executor became unavailable. Reviewed sources and formulas
were reconstructed, and the principal exact checks were independently
run with BigInt rationals in V8. Reconstructed Python sources were not
rerun during the outage. See
[the continuation checkpoint](research/10-turn-density/CONTINUATION_2026_11_11.md)
for precise verification and recovery status. No Lean compilation or CI
was run, and the established rigorous value interval is unchanged.

## Earlier continuation: turning densities, global certificates, and endpoint matching

The current work targets exact closure rather than additional interval
refinement. The endpoint-inward comparison now excludes a positive-length
initial unit outward run at an active positive-M1 start, even when positive
M2 is inactive. Endpoint activity also forces slack in the corresponding
fixed-`U=1` route. The construction therefore keeps the full initial field,
the true post-one inverse moments, and distinct active regions.

A continuous same-half theorem reduces arbitrary post-one returns to the
free single-excursion family under explicit CDF gates. Those gates pass
exactly over the entire supplied terminal triangle. On the upper side,
paired monotone controls have an attractive cut formulation, with exact
physical finite fixtures and explicit continuum-error obligations.
An analytic incoming correction repairs the terminal negative-M1 defect
without changing any high-start monster payoff adversely. Its shared
outer capture columns still need to be matched. No matching saddle or
new game-value bound is claimed.

### New construction results

| ID | Result | Scope and remaining obligation | Evidence |
| --- | --- | --- | --- |
| B21 | Exact general one-turn CDF response, a contractive transport obstacle, and a chained-turn uncrossing identity | Retains strict incoming traces and closed capture traces. The obstacle controls the specified one-turn family; uncrossing constrains active support. Neither controls every monster by itself. | `research/10-turn-density/ORDERED_CDF_RESPONSE.md`; 90 exact response identities and 432 exact uncrossing comparisons |
| B22 | All-princess response reduction for separated early and late turning densities | Four scalar parameters plus an explicit monotone prefix inverse suffice under the stated density, separation, and suffix-envelope conditions. Integrable singular tails are included under the additional hypotheses in Section 9. No exact maximizing value for an optimal law has been certified. | `SEPARATED_SHEETS_RESPONSE.md`, `UPPER_EQUALITY_CORRIDOR.md`; exact corridor checks and independent direct-capture integration in `packages/interval_turn_density/` |
| B23 | A two-state center Bellman certificate with explicit initial-prefix inequalities | A supplied potential satisfying these inequalities certifies an ordinary ordered princess law against arbitrary monsters, without a turn cutoff. Concavity in the surviving frontier permits finitely many frontier knots. No matching potential/law has yet been supplied. | `CENTER_BELLMAN_CERTIFICATE.md`; 756 independent exact capture checks in `verify_center_bellman.py` |
| B24 | Exact endpoint integral equations, a curved-prefix correction, and a positive local analytic upper tail | The cost identities and trace obstructions are exact. The fractional/power-log expansions and numerical local fit do not establish a full nonlinear solution, global attachment, normalization, or a saddle. | `ENDPOINT_FUNCTIONAL_SYSTEM.md`; 540 initial-wave derivatives, 328 terminal identities, 60 endpoint traces, and 570 curved-prefix capture checks |
| B25 | Positive-start late-turn sheets on both sides of the primal-dual construction | An explicit upper turning density preserves the four-scalar response reduction. The lower CDF has exact first-capture identities and a solved local cap/exit system, including the endpoint capture jump. The sheet is not attached to a complete law. | `TWO_SIDED_LATE_RESPONSE.md`, `POSITIVE_TURN_SHEET.md`; 4,284 exact upper-envelope checks and 4,895 exact lower identities and transport checks |
| B26 | A global signed-CDF Bellman certificate covering every monster path, including its free initial motion | Strict/closed rank records and a time-two terminal formula include capture atoms. Concavity reduces record-cell checks to vertices. A separate two-frontier center theorem covers curved laws. No actual potential at a matching upper value has been constructed. | `GLOBAL_CDF_BELLMAN.md`, `GENERAL_CENTER_BELLMAN.md`; 1,189 and 1,056 independent exact Fraction checks |
| B27 | Exact full-CDF costs for either sign of initial position and two interior monster turns | The formulas include initial atoms, same-half initial reversals, center and endpoint equality faces, and uncaught ranks after the second turn. They give concave field constraints, not an exhaustive monster family. | `TWO_INTERIOR_TURN_CDF.md`; 4,512 exact Fraction checks in `verify_two_interior_cdf.py` |
| B28 | An attained endpoint-sweep continuation value from center memory | At a center return, the larger captured radial prefix contains every rank that previously visited the center. If it also covers every future interior-capturable rank, a direct sweep toward the less-captured sign is optimal among all continuations. The future envelope includes endpoint departures and characteristic atoms. Earlier costs and a matching upper law remain open. | `CENTER_MEMORY_SWEEP.md`; 3,987 exact independent capture checks and an exact rational boundary audit in `center_memory.py` |
| B29 | Positive early turning sheets, corrected overlapping signed prices, and a source-resolved late exit | The specified upper laws retain a four-scalar response theorem under their stated monotonicity and residual conditions. For supplied lower-rank flux, the positive late cap has one uniquely determined scalar exit. These are constructive components; no complete normalized saddle law is supplied. | `SIGNED_EARLY_RESPONSE.md`, `NEGATIVE_EXIT_PHASE.md`, `POSITIVE_TURN_SHEET.md`; 2,112 exact prefix comparisons, 4,400 exact source-cap identities, and independent capture comparisons |
| B30 | Signed early two-turn upper densities and an actual normalized attached numerical law | The explicit M3 densities supply prefix prices without a post-one beta slope. A normalized floating law is now assembled from both signed M3 sheets and the earlier late sheets. Its numerical response is about 1.42518584; this is not an exact response ceiling, and nonzero structural multipliers prevent treating its LP dual as a lower law. | `EARLY_M3_RESPONSE.md`; 15,906 exact identities, independent whole-law capture integration, and labelled structural constraints in `m3_attached_settled.json` |
| B31 | Ordered negative-prefix optimization without monotonicity of p=f+g | Adjacent-violator pooling and two exhaustive cases at the small M3 band replace the old constant-inverse restriction. The specified-law response still has four scalar parameters. The resulting density fit is numerical and unmatched. | `ORDERED_NEGATIVE_PREFIX.md`; 3,960 exact comparisons with a complete independent dynamic program and three whole-law capture checks |
| B32 | Pointwise compression of arbitrary initial prefixes for ordinary capped waves | With separated cross-initial incoming and outgoing characteristics, every first-center, first-endpoint, or fixed-interior prefix is dominated by the stated short prefix families. Initial atoms are allowed; two explicit counterexamples rule out silently allowing cross-initial coalescence. It does not prove that the current curved field has this ordinary structure. | `ORDINARY_PREFIX_COMPRESSION.md`; 9,759 exact checks including 7,800 direct pointwise capture comparisons |
| B33 | A complete normalized numerical law with a positive integrable analytic tail | The endpoint density and all induced M2/M3 sheets are integrated as one continuous component. The tested fixed outer attachment fails to select a matching ordinary branch and retains binding join conditions. This is an actual law and a failed attachment test, not a certified upper ceiling or an equilibrium. | `packages/interval_turn_density/SINGULAR_TAIL_ATTACHMENT.md`; independent moment, Stieltjes feature, and sheet-mass comparisons |
| B34 | Initial-inward upper sheets with complete negative-prefix control | Uniform and localized two-dimensional densities have exact first-contact features. Ordered finite arrangements handle independent localized sheets; nested tail maximizers handle the tied ramp. All induced M2/M3 changes are retained. The tested fixed triangles are inactive in the numerical fits and do not establish matching support. | `UNIFORM_INWARD_UPPER.md`, `UNIFORM_INWARD_PREFIX_ARRANGEMENT.md`, `LOCALIZED_INWARD_UPPER.md`; 483 and 260 exact feature checks and independent full-feature prefix comparisons |
| B35 | A strict finite inward attack excludes ordinary initial tails at active positive-M2 starts | Shifting the monster's start while keeping its outward characteristic fixed improves precisely an initial rank band. The negative integral is explicit and does not assume indifference. An exact full-CDF identity also identifies the moving boundary of possible inward support. A curved initial phase remains to be constructed. | `INWARD_INITIAL_OBSTRUCTION.md`, `INITIAL_INWARD_CDF.md`; 639 exact CDF identities, 10 atom fixtures, 47 directional identities and 47 strict finite attacks |
| B36 | Removal of an unnecessary high-start negative-M2 support restriction | The bounded-law response theorem permits negative M2 starts up to one. Removing four artificial equalities selects a small component below the early-turn floor, while physical residuals set it to zero above that floor. The independent localized inward triangle remains unused; remaining density conditions and the lower law are unmatched. | `packages/interval_turn_density/independent_full_start_discovery.json`; normalized floating law with all remaining constraints labelled; not a certified game bound |
| B37 | A conditional golden-ratio initial curvature law | If inward equality reaches a flat positive-M2 boundary with the stated uniform power and off-diagonal regularity, the initial curvature exponent is `(1+sqrt(5))/2`. Quadratic curvature is attacked. An exactly flat positive-M2 physical mixture verifies the local sign calculation. This is a fixed-start germ, not a global tail or an active-set construction. | `CURVED_INITIAL_POWER_PHASE.md`; independent 45-digit physical capture checks in `verify_curved_initial_power.py` |
| B38 | Exact curved-phase source and row/column moment equations | The initial corrections, low-field source, and full rank-order obstacle are retained. The moments also apply to a fully curved incoming phase. A constant-incoming cap has a separate conditional contraction; it is not silently imposed on the full field. Moving-ridge and general free-second-turn corrections are explicit response components, not a matched support theorem. | `CURVED_TERMINAL_SOURCES.md`; exact first-intersection checks in `verify_curved_terminal_sources.py` |
| B39 | An inverse-integral initial-inward obstacle with explicit local contraction bounds | The fixed-front map has an invariant inverse box, an audited inverse horizon, and safe transport/cap conditions. Weighted estimates identify the additional gates for a joint construction. Neither a compatible exterior nor a full free-second-turn law has yet instantiated those gates. | `INITIAL_INWARD_OBSTACLE.md`; derivative-free first-contact identity and explicit Banach estimates |
| B40 | Exact free-start conditions and finite deletion of unproductive second-turn segments | A smooth start derivative distinguishes slower initial tangents from a unit tangent. A pointwise finite comparison excludes a final outward CDF plateau, gives a quantitative inactive inward-rank strip, and removes a negative-M3 return that captures no new rank. This forces the general free-second-turn family into the construction. | `INITIAL_INWARD_START_CONDITION.md`, `INWARD_TURN_DOMINANCE.md`; 1,079 and 12,513 exact checks |
| B41 | General fixed-second-turn inward adjoint, including a necessary terminal edge | Exact physical density scores and initial/final variations retain the moving capture boundary. A positive local adjoint operator can be solved on a supplied patch. The provisional critical endpoint balance fails its incoming test under the stated old attachment; it is not a solved tail. | `packages/interval_turn_density/CURVED_INWARD_ADJOINT.md`; 693 exact physical integral and derivative checks |
| B42 | Free-second-turn first contacts and an exact surface/cap incompatibility | A second turn on a start-independent graph `s=S(v)` creates an upward outgoing-characteristic kink when it meets an ordinary incoming cap with positive column mass. Exact finite midpoint variations exclude that proposed matching junction. A start-dependent surface and a curved incoming transition remain to be constructed. | `packages/interval_turn_density/FREE_SECOND_INWARD_CONTACTS.md`; 1,576 exact checks |
| B43 | A source-free free-second-turn obstacle and necessary active-support gate | The exact comparison retains strict initial traces and closed middle traces. Smooth second-turn stationarity compresses active support to a surface; a first-inverse moment bounds how far its capture frontier can lie below the initial frontier. The rounded incoming phase supplies legal transport but is not an equilibrium. | `FREE_SECOND_INWARD_FIELD.md`; independent 1,036- and 720-check capture audits, plus 282 exact support-gate checks |
| B44 | Detached double-corner cost equations and a conditional all-I reduction | Positive-M2 equality is not assumed. Concavity and low-source conditions reduce the terminal three-parameter inward family to negative M1 or the double-corner curve. The corrected outgoing coefficient is `8-2xi`. This lower-side reduction does not supply a matching upper law. | `DETACHED_INWARD_CORNERS.md`; 1,260 exact continuous-rank checks |
| B45 | Two independent obstructions to the ordinary corner upper law | The singular double-corner law has upward outgoing- and incoming-characteristic kinks. Spreading its second turn leaves a positive first-corner kink. Finite legal princess variations therefore improve the payoff under the stated smooth-remainder conditions, even with positive M2 absent. Curved transitions and other nonsmooth components remain outside these exclusions. | `packages/interval_turn_density/DOUBLE_CORNER_INWARD_CONTACTS.md`, `FIRST_CORNER_INWARD_OBSTRUCTION.md`; 1,631 and 3,312 exact physical-integration checks |
| B46 | Exact gain/loss identity for repeated same-half returns | Three record conditions permit pointwise turn deletion. Their joint failure can matter: a legal rational example beats all three elementary deletions. A separate conditional uncrossing identity excludes two chained active inward routes under its stated record gates. No universal reduction to one inward excursion is asserted. | `REPEATED_SAME_HALF.md`; 1,322 exact checks, plus 442 exact chained-inward checks |
| B47 | Trace-sensitive final-characteristic price for a pre-one inward phase | The inward derivative has one nonnegative mass term and two oppositely signed edges. Active-support deletion removes both strict edges under the stated final-outgoing and regularity gates. Its remaining mass vanishes at the endpoint, conditionally forcing the positive-M2 density to tend to one eighth of the endpoint-M1 mass. Contact atoms and post-one phases require separate analysis. | `packages/interval_turn_density/TERMINAL_INWARD_C_VARIATION.md`; 7,104 exact physical checks |
| B48 | Endpoint-inward coalescence, a full field obstacle, and a support compatibility condition | The exact initial-band comparison retains initial atoms and the endpoint capture jump. Active positive M1 excludes an ordinary initial unit run when the lower initial endpoint is atomless. Nondegenerate active endpoint-inward columns require positive-M2 slack. | `ENDPOINT_INWARD_OBSTACLE.md`; 1,056 exact comparisons; `packages/interval_turn_density/ENDPOINT_INWARD_ADJOINT.md`, with 1,198 exact physical checks |
| B49 | Full post-one first-hit moments and a necessary initial-tail delay | The endpoint baseline uses the first `U=1` crossing, not a later outgoing characteristic. The source retains every post-one rank and the possible `V=1` contact correction. An initially monotone outward high-rank phase fails the active-M1 moment condition. Later motion after an inward excursion remains possible. | `POSTONE_FIRST_HIT_MOMENTS.md`; 1,139 exact first-capture and moment checks |
| B50 | Arbitrary-speed same-half continuation reduction after `U=1` | Explicit strict/closed CDF gates and a separate center-continuation condition reduce every continuation to a free second turn, without a turn-count bound. Exact whole-cell checks instantiate the geometry on the supplied terminal triangle. The remaining one-I costs and earlier prefixes are separate obligations. | `POSTONE_SAME_HALF_DELAY.md`, `POSTONE_SAME_HALF_GATE.md`; 672 delay and 3,620 gate fixtures; 6,936 transport triangles and 477 split-cell vertices in the field certificate |
| B51 | A paired-control upper response with global finite cuts | Universal folding and endpoint completion reduce the specified density law to two outer parameters and monotone controls. Its endpoint coupling is attractive; the finite optimizer checks a feasible flow and equal-capacity cut. Continuum approximation and outer parameter coverage remain necessary before claiming an upper ceiling. | `packages/interval_turn_density/ENDPOINT_PAIRED_RESPONSE.md`, `monotone_cut.py`, and independently integrated physical feature verifiers |
| B52 | A legal analytic terminal incoming repair and unrestricted high-start preservation | Exact quadratic inverse envelopes and an initial-front cap repair every terminal negative-M1 start without remeshing. The correction cannot lower the payoff of any monster starting at absolute position at least `255/256`. Coarser positive capture columns change, so outer matching is still open. | `JOINT_ENDPOINT_COMPONENT.md`, `INCOMING_WARP_RESPONSE_PRESERVATION.md`; exact quadratic range gates, 3,362 physical preservation checks, and a separate outer-column audit |
| B53 | An endpoint version of the conditional golden initial germ | Coalescence yields the local power balance using the true first inverse at `U=2-b`, without positive-M2 equality or exterior CDF derivatives. A unit tangent with exponent above the golden ratio is attacked. Equality approaching the diagonal is an additional hypothesis for the balanced exponent. | `ENDPOINT_CURVED_INITIAL_POWER.md`; 42 independent 45-digit physical comparisons, not rational or interval certificates |
| B54 | Removal of initial center waits at the upper-response level | Lower semicontinuity permits strictly positive princess approximations. Extending the departing leg backward replaces the saved waiting/two-triangle rows by signed early M3 without increasing the response supremum. This is not pointwise domination of center-contact lower laws. | `INITIAL_CENTER_WAIT_RESPONSE.md`; 342 exact physical comparisons and retained center-contact counterexamples |
| B55 | One global lexicographic survival cut for a supplied finite monster law | Covers every princess start, speed, turn history, and completion time. Full residual equality face is retained. Weight optimization and a matching lower law remain separate. | `packages/interval_turn_density/ATOMIC_SURVIVAL_RESPONSE.md`; 1,335 pre-outage nonlex checks, independent V8 lex checks, and reproduction of the existing 67-pair upper law |
| B56 | Exact failures of the frozen field over all fixed-U=1 M2 starts and an early M3 cell | The field's endpoint reference is not a lower guarantee. The whole response regions, including interior stationary minima, are checked exactly. | `M1_START_AUDIT.md`, `exact_response_audit.mjs`; 119 quadratic regions, 238 physical comparisons, and the attacked tetrahedron |
| B57 | Fixed geometric response cells and exact small copositive constraints | Full M1/M2 and second-V=1 M3 cells have affine-in-field quadratic forms. Order-four copositivity is exactly PSD plus entrywise nonnegative; higher-order lifts require separate treatment. | `QUADRATIC_RESPONSE_CELLS.md`, `response_cells.py`, `verify_response_cells.mjs`; exact full-cell containment, knot, and volume checks |
| B58 | Pre-center record Bellman envelope and corrected moving-rank flux | Incoming legs merge automatically; outward inequalities, initial values, and continuation boundaries remain obligations. The flux formula retains incoming plateaus and one-sided rank limits. | `PREONE_RECORD_BELLMAN.md`, `verify_record_bellman_flux.py`; 13,092 historical moment fixtures and an independent exact flux witness |
| B59 | Arbitrary-response preservation under an outward CDF delay | Low starts improve by quantile order; sufficiently high starts are unchanged by characteristic causality. This is a comparison with the old law, not an absolute lower guarantee. | `OUTWARD_BAND_RESPONSE_PRESERVATION.md`; complete analytic reconstruction, 3,396 historical physical fixtures |
| B60 | Free-second-turn initial-inward response and its center-contact face | Two rank cutoffs give the general interior formula. The center face captures both reflected center masses and has a distinct lower-dimensional formula. No global field feasibility is asserted. | `GENERAL_INWARD_RESPONSE_LIFT.md`, `CENTER_INWARD_RESPONSE_CELL.md`; 120 interior and 35 center physical checks, plus 31 cutoff minimizations |
| B61 | Exact integer unrestricted response and complete residual face of the archived 67-pair monster law | Every physical mass matches the archived law; flow/cut equality and the residual condensation are replayable exactly. This does not prove optimality of the law. | `packages/interval_turn_density/ATOMIC_SURVIVAL_V8.md`, `verify_atomic_seed_integer.cjs`; 80,892 nodes, 176,922 arcs, and 10,125 exact residual SCCs |
| B62 | Exact implicit-quantile capture-order oracle for finite rational polygonal princess laws | The ordered coupling is scored without expanding the full crossing arrangement. A sampled continuous law is not covered as a lower certificate. | `FINITE_QUANTILE_CAPTURE_SEARCH.md`; independent replay of 40 archived raw/ordered cases, 24 subunit cases, 1,920 ray comparisons, and the 60-path optimum |
| B63 | Exact full ordered mixed-CDF scoring and attained attacks on interim dual realizations | Strict/closed records include capture atoms. The finite common-epsilon law and round-41 continuous/finite mixture fail actual off-support routes; finite-master objectives are not global lower guarantees. | `MIXED_CDF_RESPONSE_SCORING.md`; 64 finite and 28 continuous crosschecks, independent M1 moment, and saved early/late M2 and waiting attacks |
| B64 | Complete high-start pre-center Bellman gate for genuinely delayed second turns s>=1 | For the specified field, initial start at least 255/256 and current U<1. Exact comparator regions close this delayed branch; U<s<1, boundary continuations, initial costs and a matching law remain separate. | `RECORD_BELLMAN_POST_GATE.md`; independent full replay of 45,092 active cases, 17,740 quadratic Bernstein pairs and 1,156 post-one triangles |
| B65 | Exact center imbalance factorization and two-state renewal | Covers arbitrary legal histories and preserves both captured frontiers through an explicit imbalance moment. A matching global potential and initial attachment remain open. | `CENTER_IMBALANCE_RENEWAL.md`; 19,722 independently replayed rational physical and kernel checks |
| B66 | Analytic constant-cone and affine-cell renewal potentials | Internal inequalities are exact squares or rational quadratic comparisons. The affine Riccati component permits accumulating turns. Exterior inverse branches, crossing actions and front attachment remain explicit conditions. | `verify_center_affine_renewal.cjs`; 30,864 independently replayed exact checks |
| B67 | Full-record high-start center and post-one boundaries | Retains the complete earlier records. A center endpoint-block comparison and whole-cell slope/flux conditions supply the stated continuation boundaries; initial costs and the full lower strategy remain separate. | `RECORD_BELLMAN_BOUNDARY.md`; 1,156 negative post-one triangles and 6,834 floor-split flux vertices |
| B68 | Complete continuous late negative-M2 minimization | Turn concavity reduces the supplied-field family to mesh edges, including closed endpoint jumps. No restriction to existing turns or starts. | `CONTINUOUS_LATE_M2_EDGES.md`; 3,502 edges, 7,004 quadratic identities, and an independent exact physical minimum |
| B69 | Exact projection of unpriced response thresholds | Preserves every finite-law payoff and the entire monotone-completion fiber. It reduces the solver without changing physical controls. | `PRICED_ORDER_PROJECTION.md`; 62,087 exact order comparisons and four independently replayed global-cut comparisons |
| B70 | Actual initial center waits in the global upper-response compiler | Strictly positive princess approximations give the correct unconditional waiting contribution and continuation record. This does not transfer waiting costs to a lower law with center mass. | `CENTER_WAIT_RESPONSE.md`; 896 rational reward identities, 147 physical checks, and an exact mixed integer fixture |
| B71 | Common light-coordinate geometry optimization and saddle conservation | Strict warps biject legal paths; boundary warps have uniform approaching realizations. A necessary attained-saddle symmetry is proved. A finite-bank strict lower warp is defeated by a complete continuous-family audit. | `COMMON_LIGHT_COORDINATE_WARP.md`; 484 exact feature rows, 6,936 warped triangles, and 301 continuous-start cells |

These notes are in `research/10-turn-density/`. The endpoint work
permits distinct initial and incoming distributions and keeps moving
negative outgoing fronts. A literal time-one central atom and a
nondegenerate incoming `U=1` atom create exact first-contact dips; they
cannot replace nearby continuous layers in a matching law. The analytic
tail has integrable singular densities with a necessary logarithmic
modulation, but its local numerical compatibility is not proof closure.

The latest attachment checks expose substantive incompatibilities in the
saved numerical seed. Its extra-return ranks cannot supply the negative-row
flux required by the positive-turn sheet. Holding the saved low-branch
parameters fixed also forces `A(beta)<A(b)`, contrary to monotonicity.
Reconstructing the outer upper densities from two stationarity equations
leaves the incoming equation and the suffix-switch equality unsatisfied.
These are fixed-candidate diagnostics, not exclusions of the entire
two-sided geometry. The next construction must solve the field, free
boundaries, and density law jointly. See
`packages/interval_turn_density/TWO_SIDED_CHECKPOINT.md` and Section 8 of
`POSITIVE_TURN_SHEET.md`.

The new exact checks and the hand arguments have received internal review.
No Lean compilation or CI was run. The existing exact game bounds are
unchanged, and G5-G8 remain open.

The current joint construction moves the entire triangular CDF field,
including its initial law and incoming and outgoing regions. It uses one
fixed mesh to identify missing attack geometry. The numerical objective
is explicitly only a finite-route objective. Independent capture-order
searches extract routes from quantile contours, then evaluate and polish
those routes against the entire field. Early one-turn, two-turn, and
four-turn attacks have successively exposed missing constraints; none of
the intermediate objectives is a lower bound for the unrestricted game.
The probe's capture engine is separately checked against exact continuous
rank integration and direct atomic intersections, including time-two
endpoint arrival and a turn very close to an endpoint.

The complete frozen CDF and its reproducible 17,131-route pool are in
`packages/interval_cdf_discovery/`. The frozen field is explicitly defeated:
an initial inward turn from `13/16`, then an outward turn, costs about
`1.42146653905`, strictly below its finite-pool objective. The cost is
checked exactly by two independent CDF action formulas. An exact rational
mixture repairs both optional late-turn inequalities while preserving the
early cone and center-memory barrier, but does not remove this attack.
The package also audits all continuous M1 starting positions exactly by
quadratic cells, including their interior stationary points. These are
specified-field constructions and exclusions, not narrower game bounds.

The later `initial_inward_*` checkpoint includes 71,289 existing-coordinate
routes and genuinely active short initial-inward loops. Its complete field
is also explicitly excluded by the exact continuous-start M1 audit, which
finds a terminal start with cost about `1.42324491624` below the pooled
objective. A separate rational repair establishes both late inequalities
exactly and still has the same type of attack. The active support and full
source terms are being used to construct an analytic terminal attachment;
the fixed mesh has not been refined.

The source-corrected ordinary terminal equations now have an explicit
conditional incoming-front contraction, recorded in
`TERMINAL_SOURCE_FIXED_POINT.md`. B35 rules out using that ordinary initial
attachment as a matching strategy. The next endpoint construction must
retain a curved initial phase and the free inward-turn support boundary.
The fixed field's final affine cell is not used as an endpoint asymptotic.

The subsequent curved-phase continuation does not claim closure. The
free-start derivative and finite second-turn deletion have both been
checked independently. They show why solving only the fixed-`U=1`
inward equation and then imposing an ordinary incoming cap is insufficient.
The general initial-inward route `I(a,v,s)` has three free parameters;
the next construction must locate its active second-turn surface and
verify all of its inequalities. A simple turn graph depending only on
`v` also requires the separate upper-response junction audit, rather than
being inferred from a lower local minimum.

The detached ordinary-corner proposal now has a full conditional lower
response reduction, but its proposed upper law is excluded by exact finite
princess variations. Distributing only the second turn does not remove
the first-corner obstruction. The source-free comparison also supplies a
necessary support gate for earlier second turns, including turns outside
the previously separated outgoing region. Repeated same-half returns have
their own exact gain/loss formula; an explicit example shows why simple
turn deletion is not a general theorem for curved fields.

Pre-one incoming motion remains a candidate-branch assumption. Endpoint
absorption by time two does not imply that every incoming phase lies at
`U<1`. A further incoming wave after the first `U=1` crossing must retain
its actual first inverses and post-one source. No assertion here excludes
all such waves, proves attainment of an optimal lower law, or supplies a
complete unrestricted saddle.

### Earlier proof audit and exclusions

**G4 is now closed at the hand-proof and source-review level.** The original
continuous-to-finite response arguments have been expanded into standalone
proofs and cross-checked in this continuation. This is internal mathematical
review, not external peer review or a Lean kernel check.

| ID | Result | Scope and consequence | Evidence |
| --- | --- | --- | --- |
| B1 | Exact deadline characterization for arbitrary Borel monster laws | Extends the fixed-support theorem to continuum mixtures, including starting-position atoms, endpoints, tangencies, and truncated payoffs. It is an equality of suprema, not an attainment claim. | `research/07-structural-audit/DEADLINES.md` |
| B2 | Coordinatewise capture-order domination | For any n specified 1-Lipschitz princess paths, a canonical monster captures each no later than any given monster; at most n-1 positive capture legs suffice. This justifies the existing response searches independently of the weights. | `research/07-structural-audit/CAPTURE_ORDER.md` Sections 1-2 |
| B3 | No universal turn or horizon cutoff follows from symmetry and ordering | A symmetric stationary family with 2k+1 paths forces k-1 interior turns and last capture at time k+2. Therefore a simple equilibrium family needs an additional, equilibrium-specific theorem. | Same note, Sections 3-4; `packages/interval_structural_obstructions/verify.py` |
| B4 | Exact characteristic response for arbitrary M1/M2 start measures | Capture formulas retain initial atoms, first-inverse conventions and the **last** point of a possible `t+p(t)=1` plateau. | `research/08-continuum/CHARACTERISTIC_RESPONSE.md`; 14,008 exact direct-intersection checks |
| B5 | The complete three-parameter wait/inward/outward response family is insufficient for arbitrary M1/M2 mixtures | Its supremum against an explicit twelve-path mixture is `2641/1600`; a two-inward-leg path obtains `100559/60000`, a strict gap `3043/120000`. These are response-example values, not game bounds. | `research/08-continuum/WAIT_IN_OUT_COUNTEREXAMPLE.md`; 7,392 exact arrangement cases |
| B6 | Exact fixed-monster-start continuation value 2 and uniform quantile approximation | Improves the tail inequality to `V <= (1+2/H)V_H`; n midpoint quantile paths approximate every truncated monster payoff within `H/n`. This is approximation, not exact closure. | `research/08-continuum/QUANTILE_AND_TAIL.md` Sections 1-4 |
| B7 | Explicit sufficient upper and lower continuum certificate tests | A two-dimensional characteristic potential proves a proposed M1/M2 upper guarantee; a Bellman potential with exact endpoint-tail cost proves a proposed princess lower guarantee against all monsters. **No matching candidate instantiates both tests yet.** | `research/08-continuum/M1_M2_CONTROL.md`; `QUANTILE_AND_TAIL.md` Sections 5-6 |
| B8 | A missing inward leg strictly improves the proposed three-parameter response family | After crossing `U=1` at `V=c>=0`, an added inward leg gives exact gain `(1-epsilon-c) mu_1((a,1-epsilon))/4`. The original continuum indifference equations omit this response. | `research/08-continuum/POST_SWEEPER_DETOUR.md`; 4,440 exact direct-intersection comparisons |
| B9 | Improved exact unrestricted upper guarantee | A rational 134-path monster mixture gives `V <= 36563170811/25600000000 = 1.4282488598046875`. All 27 full-interval starting chambers have integer flow and matching deadline checks. | `research/08-continuum/REFINED_UPPER_BOUND.md`; `packages/interval_refined_upper/verify.py` |
| B10 | A complete four-parameter princess-response reduction for a specified monotone-density class | Requires bounded M1/M2 densities, monotone positive M1 and negative M2 densities, and an explicit density-gap condition. Boundary responses are covered by an interior perturbation and lower semicontinuity. **No optimal law satisfying these hypotheses has been constructed.** | `research/08-continuum/CONDITIONAL_RESPONSE_REDUCTION.md`; corrected functional and conditional equations in `CANDIDATE_DENSITIES.md` |
| B11 | The corrected sampled princess candidate fails the unrestricted lower requirement | An explicit legal monster gives payoff at most `1554318825101/1279999999616`, approximately 1.21431158, against a rational 124-path candidate. The same obstruction survives ordered quantile rearrangement. This is an exclusion, not a new game bound. | `research/08-continuum/CENTRAL_CONCENTRATION.md`; `packages/interval_central_concentration/verify.py` |
| B12 | A finite unrestricted monster-response theorem for specified ordered multi-leg princess laws | Requires strict quantile parameter order, endpoint completion by time two, and a finite partition satisfying the incoming-density kernel inequality. It includes central waits and bounds useful zero-return triangles by `sum_j J_j+3k`. It does not establish optimal-law membership. | `research/09-equilibrium-structure/ORDERED_MULTI_LEG_CDF.md`, `CENTER_RETURN_REDUCTION.md`, `MULTI_LEG_FINITE_RESPONSE.md` |
| B13 | A finite exact quadratic certificate for a rational law satisfying B12 | Fixed direction words, capture regimes, and all equality strata produce rational quadratics on rational polytopes. The exact unrestricted response value is rational and attained by a rational route. This is a finiteness theorem, not a completed arrangement enumeration for an equilibrium. | `research/09-equilibrium-structure/FINITE_QUADRATIC_CERTIFICATE.md` |
| B14 | The positive-M1-tail/M2 continuum candidate class is globally suboptimal | Allows arbitrary M2 measures and positive M1 measures, including atoms, provided there is M1 mass strictly below one in every top interval and no interior negative M1 component. A quantitative arbitrary-path exchange and finite-row minimax prove a strict improvement; reweighting selected princess responses cannot repair this class. | `research/09-equilibrium-structure/SUFFIX_GAP_EXCLUSION.md` |
| B15 | Exact continuous-rank payoff evaluation for ordered three-/five-/multi-leg laws | Integrates rational CDF records, including center and endpoint atoms, without sampling princess ranks. Analytic, independent collision, and equality-face fixtures pass. It evaluates fixed routes, not the full optimization in B13. | `packages/interval_continuous_rank/` |
| B16 | Four-parameter princess-response reduction with signed M1 support | For bounded densities, it suffices that `f`, `f+g`, and `h+ell` are nondecreasing. Opposite Chebyshev monotonicity handles the suffix without requiring the signed-M1 density itself to be monotone. Boundary parameters denote controlled payoff limits. This is a specified-law upper reduction, not an equilibrium theorem. | `research/09-equilibrium-structure/SIGNED_M1_SUFFIX_REDUCTION.md`; exact functional checks in `packages/interval_signed_densities/` |
| B17 | Shifted-turn formulas and an obstruction to the proposed canonical lower branch | General M2 turning characteristic `U=b` has exact first-capture formulas retaining plateau endpoints and equality cases. Shifting the common M2 component strictly improves against a globally maximizing canonical response with a positive extra inward leg. Extending that conclusion to every near-best response still requires equality-case control. | `SHIFTED_CHARACTERISTIC_RESPONSE.md`; `SIGNED_M1_SUFFIX_REDUCTION.md` Section 7; `FREE_TURN_STATIONARITY.md`, all in `research/09-equilibrium-structure/` |
| B18 | Exact first- and last-wave two-turn attack formulas | Direct capture classes give finite integral formulas against ordered five-leg laws, including missed fronts and endpoint mass. They defeat the saved fixed-second-wave fits. These examples do not exclude all five-leg laws or establish optimal support. | `research/09-equilibrium-structure/FIRST_WAVE_TWO_TURN_RESPONSE.md`, `LAST_WAVE_TWO_TURN_RESPONSE.md`; rational fixtures in the continuous-rank package |
| B19 | Arbitrary-path negative-M2 shift identity and conditional whole-law exclusions | A global cap controls the late inverse traces, including center and endpoint coincidences. Strict-localization and local mixed-active-set theorems extend the attack to arbitrary near-best princess laws. Each requires its stated scalar gap or strictness assumptions; the whole signed-support class is not declared excluded. | `research/09-equilibrium-structure/NEGATIVE_M2_SHIFT.md`; 28 exact cap and 28 exact shift fixtures in `packages/interval_signed_densities/verify_trace_cap.py` |
| B20 | The rationalized signed-density candidate is strictly suboptimal against all princess paths | A 946-cell exact local scalar certificate instantiates B19, including mixed no-extra/extra active responses. An explicit rational mixture of four monster laws improves the original response ceiling by a strictly positive certified amount. This excludes the fixed rational law, not every signed-M1/M2 law and not a proposed value of the game. | `research/09-equilibrium-structure/LOCAL_SCALAR_GAP.md`; `packages/interval_signed_densities/verify_local_gap.py`, `local_gap_certificate.json` |

B12-B14 have been independently cross-reviewed internally at the hand-proof
level. The early separated three-leg case needs at most two useful interior
capture turns; center waiting requires the additional density argument.
The synchronized incoming-wave shortcut is separately excluded in
`SYNCHRONIZED_INCOMING_OBSTRUCTION.md`. No Lean compilation or CI was run.
The unrestricted game value and gates G5-G8 remain open.

The signed primal-dual equations are preserved in
`SIGNED_PRIMAL_DUAL_SYSTEM.md` in the same research directory. Their branch
ordering, free boundaries, and matching lower law have not been solved.
The rationalized fixed-bin candidate that motivated them is now excluded
by B20; its exact local gap has passed independent mathematical review.
The fixed-bin density search was used to expose those conditions, not to
claim a new value bound. Its monotonicity-constrained LP dual is not a
princess lower strategy against arbitrary pure monsters. A separate fixed
support probe assigns positive weight to negative M2 paths with turns off
`U=1`, supporting the need to examine that geometry.

New exact checks passed: 81 signed-functional derivative cases, 21 boundary
tangent cases, and the first-/last-wave capture fixtures. An independent
optional numerical integration check agrees with the rational functional
on 27 constant-density cases. No Lean compilation or CI was run.

The B20 certificate checks all 946 closed quadratic cells, exact density
normalization and monotonicity, and the explicit improving mixture's
nonnegative rational coefficients. An independent direct-capture checker
integrates 20 legal epsilon paths and verifies five exact payoff limits
against the actual rational density law, including the comparison response
and both bad-region maximizers. The dual derivative checker also passes
16 exact fixtures with distinct outgoing fronts. These checks support
the fixed-law exclusion; they do not give a matching game certificate.

The independent first-/last-wave audit passes 20 and 22 exact direct
intersection comparisons, including five nonempty first-return intervals.
Joint turn/start derivatives pass in four different front chambers. A
separate exact construction proves that a finite last incoming wave can
have a strict interior optimal turn at a fixed start; it is not a saddle
for the full game. The general shifted-characteristic checker now includes
earlier turns and passes 9,440 captures plus 440 fixed-time-turn cases.

The exact no-extra-family test in `packages/interval_no_extra_family/`
checks 176 rational chambers and 675 vertex limits. Its scoped ceiling
exceeds the known unrestricted lower guarantee, so **exclusion was not
achieved**. It neither proves nor disproves that family's optimality.

The nine-point instance in B3 has exact optimum `381/2633`. Restricting the
monster to at most two interior turns gives `763/5266`, a strict loss of
`1/5266`. All 256 interval-expansion orders and a separate Bellman recurrence
agree. **These are values of an obstruction example, not bounds on V.**

The exact unrestricted game remains open. In particular, B1 is a continuum
functional reduction; B2 has a bound depending on the supplied support size;
and B3 rules out a proposed general shortcut. None supplies the missing
matching saddle pair.

B10 is a useful conditional structure theorem, but it does not show that
an unrestricted optimal monster law belongs to that density class. B11
explains why the sampled dual cannot close the lower inequality: too much
of its mass concentrates near the center at time one, and a shifted sweep
exploits its time marginals. Solving the corrected density equations alone
would not repair that failure.

The new exact checks all passed in this continuation: 256 stationary capture
orders plus an independent Bellman recurrence; 14,008 characteristic
intersections; 7,392 wait-in-out parameter cases; 4,440 post-transition
detour comparisons; and 27 networks for the new upper certificate. The
archived upper certificate and full 48,228-state lower response calculation
also passed again. The conditional density formulas passed 81 exact
derivative cases and 594 ODE/factor identities; the central-concentration
verifier checked all 124 rational paths and both marginal bounds. No Lean
compilation or CI was run.

The bounded numerical experiments and their explicit stopping conditions
are preserved in `packages/interval_continuum_discovery/`. The interrupted
large LP, nonconverged cut-generation runs, and restricted floating duals
are not certificates.

## Historical certificates and their precise scope

| ID | Claim | Scope | Evidence | Caveat |
| --- | --- | --- | --- | --- |
| A1 | Upper guarantee V <= 229233/160000 | Against all continuous princess paths, for a fixed 32-path monster mixture | `interval_pm_proof/PROOF.md`; `interval_pm_proof/verify.py`; saved integer flows | Early, superseded upper bound |
| A2 | Exact best princess response to a specified finite piecewise-linear monster mixture via event deadlines | Arbitrary 1-Lipschitz princess paths; fixed finite monster support | `interval_exact_reduction/REDUCTION.md`, `verify_exact.py` | The converse envelope theorem is a written handproof; the verifier checks finite certificates |
| A3 | Exact best monster response to a specified 60-path princess mixture = 56305800187/40000000000 | Arbitrary 1-Lipschitz monster paths; fixed princess mixture | `interval_exact_response_result/PROOF.md`, `verify.py`/`tests.py` | Requires validity of capture-order structural lemma; not game value |
| A4 | The prior exact-response target is strictly suboptimal | Perturbation and all-minimizer enumeration for same fixed princess support | `interval_target_exclusion/PROOF.md`, `verify_target.py` | Exhaustive search is expensive; no global value |
| A5 | Original 32-monster-path support cannot be globally optimal | Exact fixed-support LP and a better 68-path upper strategy | `interval_equilibrium_check/PROOF.md`, `verify.py`, flows | Excludes only that support, not all M1/M2 trajectories |
| A6 | Historical upper guarantee V <= 5717477/4000000 = 1.42936925 | Against unrestricted princess paths, supplied 68-path mixture | `interval_equilibrium_check/PROOF.md` Section 4, `exclusion_*` certificates | Superseded by B9; continuous response reduction internally audited in this continuation |
| A7 | Exact response of a 338-path princess distribution = 36290299773897097/25600000000000000 = 1.417589834917855... | Unrestricted monster best response to specified mixture | `interval_uniform_reduction/PROOF.md`, `verify.py` | Better current lower candidate, conditional on capture-order reduction |
| A8 | A small, finite grid game has a fully enumerated rational saddle certificate | Only 259 princess and 720 monster paths on the specified grid | `interval_uniform_reduction/grid_case.json`, `verify.py`, `tests.py` | **Not** the unrestricted game |
| A9 | Uniform finite approximation theorem for full unrestricted game | Asymptotic bound between grid values and V | `interval_uniform_reduction/PROOF.md` | Written proof not formalized, and grids are very large; does not determine exact V |

**Best two-sided bounds established by these packages and the audited hand arguments:**

`36290299773897097/25600000000000000 <= V <= 57045189772271291487410009/40000000000000000000000000`

That is `1.417589834917855... <= V <= 1.426129744306782287185250225`
(gap approximately `0.008539909388927`). These are not an exact solution.
The hand arguments have received internal cross-review, not external peer
review or Lean verification. The current upper law is documented in
[the exact common-coordinate upper package](packages/interval_common_warp/README.md).
The earlier unwarped law and its separate pair-regret calculation are retained.
B9 is the superseded 67-pair upper certificate; it uses only necessary
capture constraints and feasible integer flows.
Previously discussed values 11/8 and approximately 1.373 are incompatible
with the lower certificate for this version of the game.

## Verification audit of this handoff

Ran successfully in extracted directory (Python standard library, no Lean compilation):

- `interval_pm_proof/verify.py`: PASS
- `interval_exact_reduction/verify_exact.py`: PASS
- `interval_equilibrium_check/verify.py`: PASS
- `interval_exact_response_result/tests.py`: PASS
- `interval_uniform_reduction/tests.py`: PASS
- `interval_exact_response_result/verify.py`: PASS (full)
- `interval_target_exclusion/verify_target.py`: PASS (full, 751,782 states)
- `interval_uniform_reduction/verify.py`: PASS (full, 48,228 states)

The initially time-capped `interval_target_exclusion/verify_target.py` was rerun without the short cap and **PASSED** (751,782 response-search states). Both `interval_exact_response_result/verify.py` and `interval_uniform_reduction/verify.py` also **PASSED** on full runs. PASS means the arithmetic and finite-response assertions passed, **not** that all continuous theorems were kernel-checked.

## Firm separation of statuses

- **Closed:** finitely specified response examples and fixed-support optimization, each with their own conditions.
- **Open:** identifying an unrestricted equilibrium or proving a globally exhaustive finite strategy family.
- **Open:** exact value of the full game.
- **Not a proof:** numerical LP search logs, shape speculation, truncated response searches, and guessed rational values.

