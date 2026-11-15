# Finite-gate roadmap toward an exact unrestricted game solution

**New fixed domain (2026-11-13):** the
[exact horizon reduction](research/12-global-closure/GLOBAL_EXACT_HORIZON_REDUCTION.md)
closes unbounded time: use Princess cutoff 3 and Monster completion 7.
The [seven-state physical-clock flow](research/12-global-closure/FINITE_STATE_PHYSICAL_CLOCK_LIFT.md)
closes physical lifting, with a fixed compact state polytope and seven
controls. [Finite certificate synthesis](research/12-global-closure/FINITE_GLOBAL_CERTIFICATE_SYNTHESIS.md)
reduces every declared polynomial template to an exact finite check.
The remaining gate is a matching finite certificate pair or a proved
finite bound on optimal template complexity. The flow still has
continuous measure unknowns; no finite-case closure is claimed.

> **Roadmap update, 2026-11-13:** This file records historical finite-gate attempts and negative-result directions. The **current actionable roadmap** is [HANDOFF_2026-11-13.md, §6](HANDOFF_2026-11-13.md#6-focused-next-work-gates--no-indefinite-case-queue): construct a legal global Monster/clock occupation, solve its unrestricted strict radial oracle, build the matching transport CDF and full Monster Bellman certificate, and meet both inequalities at one value. No general finite-turn reduction or equilibrium-specific finite phase classification has been established. Do not treat the older conditional G5-G8 or fixed-bank checklists as closed.

## G2 closed exclusion gate: TWO complete Monster weight rays, exact four-cut screen

A full unrestricted response search followed by physical
BigInt first-contact replay produced four legal Princess paths
and their **2,248 exact contacts** against the 281-row Monster bank.
Their exact cuts prove **continuum** rather than sampled exclusions:

* **All** weights on the ray mixing the unwarped 280-pair law
  with the archived old Princess-best-response Monster route
  have Princess response at least \(1.426135310893618...>
  U_{\rm best}=1.426129722845311...\).
* **All** legal mass transfers from original Monster atom 0
  to atom 120 have Princess response at least
  \(1.4261332895524503...>U_{\rm best}\).
  The exact two-Princess intersection is at transfer
  \(0.000004620208384168817...\).

Thus **both directions are closed as routes to a better global
upper certificate**, even for infinitesimal weight changes.
Their proofs are finite, exact and auditable:
[G2 global germ/ray theorem](research/12-global-closure/G2_NEAR_ACTIVE_GERM_SEPARATION.md),
[ray verifier](packages/interval_global_closure/verify_g2_ray_exclusions.cjs),
[exact four-cut data](packages/interval_global_closure/g2_near_active_princess_cuts.json),
[replay](packages/interval_global_closure/verify_g2_princess_cuts.cjs)
and [fast cut screen](packages/interval_global_closure/g2_princess_cut_screen.cjs).

**NEXT G2 (OPEN):** do not retry these two weight rays.
Construct a **genuinely new Monster path-geometry/continuous-support
law and Princess CDF simultaneously**. Every dual proposal must pass
the exact four-column cut screen, then the full unrestricted
Princess max-flow oracle; a successful Princess construction must
separately pass unrestricted Monster response (including center
waiting/return Zeno). G3–G5 remain OPEN. No globally matched CDF
or exact game value was found.


## G2 gate: near-active Princess germ separation REQUIRED

The first attempted constructive update is now **rigorously rejected**.
Add the archived pure Monster best-response route to the certified
280-pair upper law with any mass
\(\lambda>8.97930481037766\times10^{-9}\):
a saved **162-vertex physical Princess path** gives expected capture
strictly *above* the original law's exact upper certificate.
This covers the whole practically meaningful segment of the
one-parameter direction, with 562 exact physical hits and a fully
replayable rational witness.
[Proof and failure anatomy](research/12-global-closure/G2_NEAR_ACTIVE_GERM_SEPARATION.md),
[JSON](packages/interval_global_closure/g2_m1_injection_witness.json),
[verifier](packages/interval_global_closure/verify_g2_m1_injection.cjs).

The **new universal G2 optimality formula** is a near-active
Monster-dual Danskin condition, not just exact primary-face
complementarity:
\[
U'_+(0)=\lim_{\eta\downarrow0}
\sup_{\{p:J_{\nu_0}(p)\ge U_0-\eta\}}
[J_{\nu_1}(p)-J_{\nu_0}(p)].
\]
A zero-slack min/max label response to \(\nu_0\) scores
\(1.421874...\) against the added route, suggesting improvement;
a slightly below-optimal physical response instead scores
\(2.99999998...\) and invalidates every macroscopic injection.
Other tested start-diffusion and reweighting fixes also fail
the unrestricted Princess oracle.

**Next constructive step:** a joint route/weight master with
explicit **near-active contact-germ columns**; solve it against the
*whole* unrestricted Princess response oracle and separately verify
the candidate Princess CDF against all Monsters. Every new
Monster update must clear the fixed 162-vertex regression
witness before being promoted. This does **not** solve G2.


**First G2 diagnostic closed:** the archived 338-path / 280-pair
candidate has an *explicit global CDF ascent direction*, with
derivative at least 0.0029361293227555, and an independent
Monster best-response gain of 0.0056093417063263.
Both violations are strict. The next candidate must solve the
two-sided complementarity, not merely adjust the old support weights.
[Exact witness](research/12-global-closure/GLOBAL_CDF_VARIATIONAL_STATIONARITY.md#7-exact-nonstationarity-witness-for-the-archived-338-path280-pair-candidate).


### G1b CLOSED: global strict/closed CDF first variation

For a supplied completed Monster *trajectory law* \(\nu\),
the ordered Princess payoff is concave in its CDF. Its exact
one-sided directional derivative is the integral of near-active
strict-min and closed-max record perturbations, with no smoothness,
unique-record, or turn-count assumption. **Global Princess
optimality against \(\nu\) is equivalent** to nonpositivity of this
derivative for *every* legal CDF direction. Combined with an
unrestricted Monster lower response it is an exact saddle test,
and uniform derivative errors give an honest two-sided value
certificate. [Full proof](research/12-global-closure/GLOBAL_CDF_VARIATIONAL_STATIONARITY.md)
and [3,375-case exact fixture](packages/interval_global_closure/verify_cdf_record_variation.py).

**G2 remaining constructive decision:** Solve the coupled
record-occupation / transport variational inequality by finding
a CDF \(F\), physical Monster law \(\nu\), and matching constant \(c\).
The previous finite-bank selector-plane global oracle is a
sufficient upper separator; the Monster Bellman/renewal response
is the lower separator. Do not confuse either finite local
certificate with complete global stationarity.


## GLOBAL G1 CLOSED: unrestricted minimax and coupled support equations

The unrestricted game has been reduced at a **global mathematical
level**, not just a finite bank:
\[
\sup_{\mu}\inf_m\mathbb E_\mu T(m,P)
=\min_\nu\sup_p\mathbb E_\nu T(M,p),
\]
and the Monster minimum is **attained by a symmetric law on entire
trajectories**, possibly with infinitely many turns and continuous
support. The Princess supremum may be nonattained.

For every \(H,n\), the bounded-horizon and \(2n\)-path Princess
game \(V_{H,n}\) certifies the full value within explicit error
\[
V_{H,n}-6/H\le V\le V_{H,n}+(H+3)/(2n).
\]
This has no target absorption/turn-count assumption; with
\(H=\sqrt{12n}\), the bracket width is
\(2\sqrt{3/n}+3/(2n)\).
The game still has continuous path variables and this is not a
practical finite-LP solution at high precision.

The exact optimal-support conditions are now:
Monster-supported routes must attain the Princess CDF's minimum,
and Princess-supported quantile paths must attain the Monster
path-law's maximum, with quantitative \(\epsilon\)-versions when the
Princess supremum is not attained. A Monster's **time-marginal CDF
does not encode its first-contact value**; the complete trajectory
coupling must be carried in any proposed dual strategy.

[Proof and counterexample](research/12-global-closure/GLOBAL_MINIMAX_AND_CDF_DUALITY.md)
and [exact fixtures](packages/interval_global_closure/verify_global_minimax_reduction.py).

**Next: G2 is now the decisive open gate.** Construct an explicit
symmetric Monster path law and ordered Princess CDF making the
two global support equations tight. On the Monster side retain
trajectory coupling, and on the Princess side use the complete
selector-plane path oracle; verify **both unrestricted** response
inequalities. Do not divert to tiny extensions of local
center-return strips. G3–G5 remain open until a constructed
candidate passes its corresponding global certificate.


## Closed: exact full turn-count envelope for long-horizon terminal wedge

For the physically certified saved affine center wedge, the entire
*no-initial-wait, fixed-terminal* all-count optimization for
\(1/20\le H\le1/16,\ 0\le y<kH\) has now been solved exactly:
\[
\inf E_y=
\begin{cases}
\min(E_1,E_\infty),&0\le y\le2H/5,\\
E_1,&2H/5\le y<kH.
\end{cases}
\]
The low-surplus branch is approached by explicit productive finite
chains with two geometric Green sources, a spread-out middle, and
arbitrarily many turns. The unique transition \(y_*(H)\) is algebraic.
There is **no unbounded M4/M5/... case queue in this entire strip**.

[Complete theorem and hand proof](research/12-global-closure/TWO_SOURCE_GREEN_ZENO_ENVELOPE.md)
and [executed exact rational verifier](packages/interval_turn_sheet/verify_two_source_outer_envelope.py).

**Remaining decisive local gates:** extend the count-uniform Green
classification to \(H<1/20\) at low y; settle initial center waits and
front reset accumulation; compare the *physical* exterior exits and
all initial starts. The separate full-game G5-G8 gates still need matching
unrestricted CDF/Monster-law saddle certificates.


## Closed all-count gate: outer 96.18% of terminal-rank surplus

The saved-field prescribed-\(b=15/16\), no-initial-wait productive
center problem now admits **exact one-return optimality** for every
\(0<H\le1/16,\ 2H/5\le y<kH\), across *all finite counts* and
terminal-Zeno limits. This strictly improves the previous high-surplus
threshold \(3kH/8\), leaving **only \(0\le y<2H/5\)**
for nontrivial multi-return competition in this component.

New proof:
[uniform single-return theorem](research/12-global-closure/LOW_SURPLUS_UNIFORM_SINGLE_RETURN.md).
Exact four-corner arithmetic:
[standalone verifier](packages/interval_turn_sheet/verify_single_return_outer_strip.py).
The crucial count-uniform bound completes the square against both Green
boundary sources; it does not search M2/M3/... separately.

**Remaining:** classify this narrow front strip with arbitrary waits and
Zeno interfaces; attach the true exterior/earlier start transitions;
construct matching unrestricted Monster and Princess path-law/CDF
certificates. The full game value and optimal strategies remain OPEN.


## Closed gate: ALL strict short hinges in finite two-source renewal

The saved-field, fixed-`b` productive center-return problem is now reduced
at **every finite count** to the strictly convex *no-hinge tridiagonal*
two-source energy plus the explicit one-return branch.

- **Initial hinge active**, followed by at least two more returns:
  forward two-tent merger, actual full continuation gain `>= k p q/4`.
- **Interior hinge active**, followed by at least two more returns:
  same full-continuation merger, including any formerly productive
  suffix which becomes nonproductive.
- **Short penultimate return**: exact terminal-row formula gives a
  strict decrease under last-two merging, without assuming an affine
  terminal inverse.
- **Short final return**: previous strict merger with universal margin
  `15 ell h_(m-1)/32`.

Every original finite productive chain with a strict hinge is beaten
by a legal shorter or normalized center policy.
The same exclusion applies at each finite index of a **countably infinite
terminal-Zeno chain**: a third positive return remains before `b`, so
its short pair can be merged using the full-tail captured-rank inequality.
Accordingly the no-hinge inequalities are necessary in the infinite
terminal renewal layer too. This does not remove the known front Zeno
optimizer; it removes only short-hinge Zeno candidates. No separate M4/M5/...
short-hinge case analysis remains. The no-hinge inequalities
`d h1 >= y, d h_j >= ell h_(j-1)` retain the zero interfaces.
See [the full hand proof](research/12-global-closure/LOW_SURPLUS_ALL_HINGES_EXCLUSION.md)
and the [15,480-case independent rational verifier](packages/interval_turn_sheet/verify_short_source_mergers.py).

**Next decisive finite gates:**
(1) optimize the no-hinge Green family uniformly over all finite and
infinite counts, including active duration/positivity interfaces;
(2) include productive center waits and first-front resets;
(3) compare with actual exterior exits before/after the specified
terminal row and attach the result to initial starts.
Only then does the full-game G5--G8 matching problem become approachable.
This local theorem makes **no** claim of a better unrestricted value bound.

## Additional closed gate: delete ALL final short-return hinges

For **every** initial rank surplus, every productive fixed-terminal affine
return chain with `ell/k<1/8`, `H<=2`, and a final short hinge
`ell h_(m-1)>(k-ell)h_m`, merging its last two returns decreases cost
by at least `15 ell h_(m-1)/32` (provided the merged return stays in
the same affine field). This is independent of any earlier turns or
hinges and does not assume an equilibrium turn cutoff. Iterate merging
to eliminate the entire final-hinge branch at all finite counts.

The companion saved-field high-surplus result below now extends to
terminal Zeno accumulation at `b`. The two-source terminal problem is
therefore reduced to: the **low-surplus region with only first/interior
hinges and nonshort final return**, plus explicit center-reset/wait
boundaries and earlier/later exterior exits. Avoid duplicating a separate
terminal-short proof for each turn count.

Full theorem and arithmetic: [HIGH_SURPLUS_SINGLE_RETURN.md](research/12-global-closure/HIGH_SURPLUS_SINGLE_RETURN.md)
and [the exact standard-library verifier](packages/interval_turn_sheet/verify_high_surplus_single_return.py).
1,781 exact rational fixtures passed, including generic ratio and
duration-two tests. Full unrestricted game-value gates G5-G8 are OPEN.

## Closed finite gate: high-surplus off-front renewal (all turn counts)

The all-count two-source **high-surplus** terminal-return gate is closed.
For the saved terminal affine wedge, `0<H=b-t<=1/16` and
`3 k H/8<=y=n-Z(t)<k H`, the single productive return at `b=15/16`
beats every productive two-or-more-return chain ending at `b` without
a preceding wait by at least `mu H`, where
`mu=400295280226865161073511/67164016785510400000000000>0`.
All interior and final short-return hinges are included, so no fixed
turn cutoff is assumed.

The independent one-tent wait theorem gives strict concavity in the
departure time. The combined corollary eliminates **both arbitrarily
many later returns and all intermediate departure times** in the entire
admissible high-surplus waiting strip: compare immediate departure
with one explicit transition boundary.

- [Complete exact proof and scope](research/12-global-closure/HIGH_SURPLUS_SINGLE_RETURN.md)
- [Locally executed 1,328-check rational verifier](packages/interval_turn_sheet/verify_high_surplus_single_return.py)

The *next finite gate* is the remaining low-surplus terminal hinge/Green
comparison and any later waits that reach a front reset. Once that local
envelope is complete, compare it with actual earlier/later exterior
returns. This is a step toward G5 but neither constructs an equilibrium
Princess law nor improves the unrestricted game bound. G5-G8 remain OPEN.

## Completed: full all-warp orbit interval tightened to 0.00004905

The archived 338-path Princess law has certified unrestricted response
`1.417589834917855...`. A new rational 35-route Monster mixture
bounds **every** strictly increasing continuous odd period-two common
light-coordinate warp of that law by the exact
`567055553277100451603891/400000000000000000000000
 = 1.417638883192751...`. This narrows the *restricted orbit* interval
by about 99.36% versus the previous all-warp certificate, with 11,830
independent first contacts and 84 exact step thresholds. Read
[LOWER_WARP_ALL_TIGHTENED.md](research/12-global-closure/LOWER_WARP_ALL_TIGHTENED.md).

This is **not** an improvement to the unrestricted full-game value bound,
nor a proof that common warps can never improve the archived guarantee.
It establishes that changing only its shared light-coordinate clock can
change its response by at most `0.0000490482749...`. To close the
full-game gap to the current upper target, the Princess law must change
its mass/transport shape or the Monster upper target must be improved,
with all unrestricted inequalities independently verified. G5-G8 remain OPEN.

## Completed unrestricted-warp-family ceiling (not game closure)

The fixed archived 338-path Princess law can now be attacked uniformly
through **every continuous strictly increasing odd 2-increment common
light-coordinate warp**, not just the old 16-knot piecewise-affine family.
A 13-route exact rational Monster mixture yields the all-warp ceiling
`570109078983139212403/400000000000000000000`
(about 1.42527269746), strictly below the already certified unrestricted
upper strategy's value 1.42612974431. The 75-threshold integer step
certificate closes this candidate deformation *at that upper target*.
See [the complete all-warp proof](research/12-global-closure/LOWER_WARP_ALL_EXACT_CEILING.md).

This does NOT eliminate all warped laws as potential lower equilibria
at a smaller unknown true value, nor control mixtures of different warps,
nor prove an upper bound against arbitrary Princess laws. It does establish
that changing only the common clock of the archived law cannot close the
current full-game upper/lower certificates. G5-G8 remain open. The old
16-knot ceiling remains significantly tighter inside its smaller class.

## Excluded global deformation: coarse common warps of the old lower law

An exact 16-Monster-mixture certificate bounds **every** increasing
piecewise-linear light-coordinate warp of the archived 338-path Princess
law on 1/16 knots by 1.41758984127931..., only 6.37e-9 above that
law's existing exact unrestricted response. The entire family is stopped
as a route to matching the upper bound. This does NOT exclude finer or
curved warps, nor justify extrapolation from numerical masters. See
`research/12-global-closure/LOWER_WARP_16_EXCLUSION.md`.

The next viable lower construction must change the actual rank marginals
or their transport geometry, and every candidate must pass a full Monster
response. The global G5–G8 saddle obligations remain OPEN.


Latest checkpoint: [effective fixed-fan responses and global selector optimization](research/12-global-closure/EFFECTIVE_RESPONSES_AND_GLOBAL_SELECTOR_ORACLE.md). The fixed ordinary-fan class now has a computable globally sufficient Monster response count. The global path oracle removes a supplied Princess-basis restriction for causal-selector planes. A globally sufficient equilibrium family and matching unrestricted strategies remain open.

The exact value is unknown. Do not claim completion by improving decimal bounds or growing strategy supports indefinitely. A final proof needs one explicit constant c and an unrestricted saddle pair (or epsilon-approaching lower family):

    E_{M ~ nu}(T(M,p)) <= c       for every princess p,
    E_{P ~ mu_eps}(T(m,P)) >= c - o(1)   for every monster m.

**Current user direction:** work toward closing the proof, not increasingly
small numerical intervals. Computer assistance may be used to find the
attacking direction. Preserve useful structural results, but do not treat
a conditional class reduction as completion of the original problem.

The latest local 15-piece theorem includes arbitrary initial turn counts but
requires its stated future-persistence region. It must not be promoted to
a global field-only turn cap by compactness alone. The new whole-basis
exclusion stops weight optimization of the fixed 342-profile, width 1/1024
folded family. The construction now targets a global legal-path oracle for
linear history-selector functionals, so missing marginal geometry can be
introduced with complete separation.

## Auditable gates

- [x] **G0 — Preserve research state.** Archive all proof packages and source verifiers, isolate speculative work, mark unproved lemmas. (This PR.)
- [x] **G1 — A finite-support princess-response oracle.** Event deadlines and min-cut certificates against arbitrary princess trajectories; closed for finite piecewise-linear monster mixtures, subject to proof audit.
- [x] **G2 — A finite-support monster-response oracle.** Capture-order enumeration against a fixed finite mixture of piecewise-linear princess paths; implemented and validated on individual instances, subject to structural-lemma audit.
- [x] **G3 — Exact optimization of an initial finite monster support.** 32-path support LP solved with matching rational primal/dual certificates, then excluded globally. This gate is a *negative result*, not a step toward proving its candidate value.
- [x] **G4 — Audit both continuous reduction lemmas.** Completed at the hand-proof and source-review level in `research/07-structural-audit/`. The envelope theorem now covers arbitrary Borel monster laws; the capture-order proof supplies coordinatewise domination and justifies the existing pruning rules. Internal cross-review found no remaining mathematical gap in these arguments. This does not mean Lean verification or external peer review.
- [ ] **G5 — Obtain a globally sufficient finite equilibrium-support theorem OR a closed-form continuum equilibrium.** This is the key currently missing structural theorem. A uniform approximation theorem alone does not satisfy G5.
- [ ] **G6 — Identify exact candidate c and a pair of strategies/approximating families.** Derive from analytic optimal-control or exact finite LP duality; avoid inferring c from a numerical decimal.
- [ ] **G7 — Verify the G6 candidate upper inequality for every princess path.** Use finite deadlines if finite monster support, or a continuum proof otherwise; include boundary conditions and capture-time discontinuities. Several nonmatching upper guarantees, including the improved B9 certificate, are already proved.
- [ ] **G8 — Verify the matching G6 lower inequality for every monster path.** Use capture-order reduction if finite princess mixtures, or an epsilon/continuum limit with uniform global control. The existing lower certificate does not match B9.
- [ ] **G9 — Produce a standalone hand proof and mechanically check critical finite arithmetic.** Reduce computational steps to exact certificates. Optionally formalize in Lean; no formalization currently included.

## Current closure obligations

Use the whole-strategy pipeline in `research/12-global-closure/`.
A supplied finite monster bank can now be optimized in one LP against every
princess path, with exact rational reconstruction and a separate global cut.
A finite rational-function princess family can be checked against every
monster uniformly in its limiting parameter. Neither tool proves that an
optimal strategy has the supplied finite description.

The canonical query realization is rejected globally, including starts
that depend on epsilon. Uniformly spreading its initial position through
the full deadline corridors is also rejected, even after the strongest
ordered quantile recoupling of those marginals. Stop those constructions;
do not try to repair their deficits by an expanding list of local lemmas.

The remaining construction must choose a globally compatible distribution
inside the physical response corridors (or a different continuum law) and
match it to a genuine normalized upper law. The finite query face alone
leaves this geometry undetermined. The prior full-field candidates also
retain their documented off-support attacks; they are not accepted lower
laws merely because some continuation branches have been proved.

A closure claim requires the same exact c in both unrestricted inequalities
at the top of this roadmap. For an approaching lower family, the error must
be uniform over monsters whose whole paths may depend on the parameter.
G5-G8 remain unchecked. Another conditional certificate format, a larger
fixed bank, or a smaller numerical gap does not discharge them.

The center continuation now reduces exactly to a potential W(t,n), with
the smaller captured frontier recovered by an explicit first-hit moment.
The early-cone and incoming affine-cell components are analytic; the
middle-region crossing conditions and the initial-prefix potential still
have to be matched to an actual complete law. Common light-coordinate
warps optimize physical geometry without changing legal controls or
discarding exact contacts. Their uniform limiting construction and
capture-coordinate conservation law give additional global matching
conditions. These tools serve the same joint construction; they do not
mark G5-G8 complete. See
[the center/geometry continuation](research/12-global-closure/CENTER_AND_GEOMETRY_CONTINUATION.md).

See the new checkpoint for completed exact tests and rejected candidates.
The concurrent exact-face work in
`research/10-turn-density/EXACT_FACE_CONTINUATION.md` is preserved as prior
research. Its original outage statements describe that earlier execution;
the new Python checks were executed in this continuation.

## Earlier construction directions and stopping rules

**Current coupled endpoint branch.** Endpoint-inward routes have a full
initial-band obstacle and an exact upper adjoint. Their activity forces
slack in the fixed-positive-M2 family; imposing both equalities on the
same nondegenerate column is inconsistent. Full post-one first-hit
moments replace the old final-outgoing substitution.

The supplied terminal field now has a continuous, arbitrary-speed
post-one continuation reduction, with exact gates on every cell. An
analytic incoming correction repairs its entire negative-M1 tail and
preserves every high-start monster payoff, including arbitrary earlier
turns. It still changes coarser positive capture columns. On a band where
f and g are both active, their difference fixes the initial front from
the post field, so this common column defect requires a genuine coupled
source correction. It cannot be hidden by changing only that front.

The enlarged upper class has an attractive paired-control formulation,
including its early-turn missed-capture terms. Initial center-wait rows
can be replaced by early M3 at the response-supremum level. The next
construction therefore solves an actual normalized upper law with these
global response controls while matching the lower row/column sources.
Earlier lower prefixes, all outer start/cutoff parameters, and continuous
upper-control certificates remain explicit gates. The exact value and
the two unrestricted inequalities must still match; these structural
advances do not themselves close G5-G8.

**Current constructive branch.** Separated early and late negative-M2 turn
densities now admit an all-princess four-scalar response theorem, with the
remaining prefix obtained from an explicit monotone inverse. The matching
lower problem has exact CDF response equations and an uncrossing constraint
on active turn support. Positive-start late turns now have both an explicit
upper density and exact lower-CDF cap/exit equations. A global signed-CDF
Bellman potential covers every monster path, including the free initial
motion and capture atoms, without imposing a turn cutoff. Its record-cell
concavity gives finite vertex families for a polyhedral potential. These
are certificate formats, not instantiated matching inequalities.

The endpoint analysis has moved from initial atoms to an integrable
singular tail. Exact cost residuals give a derivative-free functional
system; a convergent power/logarithm basis gives a positive local numerical
upper tail. Its outer incoming/outgoing attachment, support boundaries,
normalization, and global matching remain open. Initial endpoint atoms,
literal central time-one atoms, and unresolved history-splice errors cannot
be hidden in limiting conventions. See `research/10-turn-density/`.

The saved seed fails the new positive-sheet flux and fixed-parameter mass
ordering checks. The exact local positive-sheet solution therefore cannot
simply be appended to that seed. The upper tail's two-equation Volterra
reconstruction also leaves a nonzero incoming residual and suffix-switch
gap. These checks direct the next work toward a joint field and adjoint
density solve, with moving free boundaries and full terminal history.

The next decisive result must be an attached legal law and a matching global
certificate. Another local fit, a smaller numerical gap, or additional
conditional equations will not close G5-G8.

**New exhaustive verification route.** For an ordered alternating-leg
princess law with the stated finite incoming-density partitions, every
monster response reduces to a finite parameter family. For rational
piecewise-affine quantile parameters, the exact response is the minimum
of finitely many rational quadratics on rational polytopes, including
all capture equality faces. This removes an unbounded response search
for a *specified* law; it does not prove optimal-law membership. See
`research/09-equilibrium-structure/`.

**The previous continuum monster class is now excluded.** A law consisting
of the endpoint sweep, positive M1 start mass in every interval immediately
below one, and arbitrary M2 mass cannot be globally optimal. The free-strip
stability proof applies to every near-best princess response, not just
selected extreme representatives. Additional near-endpoint sweep families
give a strict improvement via finite-row minimax. Solving the old density
equations more accurately cannot close the proof. The next candidate must
change its support geometry, with negative M1 starts and varying monster
turn characteristics as concrete directions.

**The signed-M1 repair also needs a global support check.** Bounded signed
M1/M2 laws now have a four-parameter upper-response theorem under the three
conditions `f`, `f+g`, and `h+ell` nondecreasing. The exact functional and
conditional primal-dual equations are written out. A shifted M2 turn
defeats their canonical positive-extra-leg branch; no matching unrestricted
lower strategy has been found. The fixed free-turn probe adds a small
positive component off `U=1`. The next task is to derive a consistent
support geometry and its unrestricted inequalities, rather than solve the
old boundary equations more accurately.

**A concrete signed candidate is now excluded exactly.** The rationalized
fixed-bin law has a proved local scalar gap on
`a in [31/32,63/64]`. Exact affine/convex reductions and 946 rational
quadratic cells verify every bad parameter, including boundary limits.
The arbitrary-path stability theorem then yields an explicit four-law
mixture with a strictly smaller ceiling. See `LOCAL_SCALAR_GAP.md`.
This closes that candidate's exclusion, not G5-G8. A matching equilibrium
still requires different support geometry or a law outside the excluded
local configuration.

**Do not synchronize the second inward wave by assumption.** The two
bounded five-leg fits with `A2` confined just above one fail explicit
first- or last-wave two-turn attacks. The last-wave formula shows why a
monster can traverse that narrow characteristic range cheaply. The older
certified lower paths also contain inward waves before `U=1`; the failed
fixed-wave experiments do not cover that geometry.

**Excluded shortcut.** Symmetric ordered princess laws can require arbitrarily
many optimal monster turns and arbitrarily late last captures. The stationary
shell construction in `research/07-structural-audit/CAPTURE_ORDER.md` proves
this for every support size. Do not claim a fixed turn count or horizon from
symmetry, noncrossing, or half-interval support alone. A successful G5 must
exploit additional equilibrium structure or directly verify a candidate.

**Second excluded shortcut.** For arbitrary M1/M2 monster laws, the whole
three-parameter wait-at-start / inward / outward princess family can miss a
strictly better response. `research/08-continuum/WAIT_IN_OUT_COUNTEREXAMPLE.md`
certifies this over every parameter, including limiting boundaries. Do not
use numerical optimality within that family as an unrestricted upper bound.

**Candidate-specific missing phase.** Even the enlarged initial-outward /
inward / central-wait / outward family omits a strictly improving inward
leg immediately after `U=1`. The exact gain is proved in
`research/08-continuum/POST_SWEEPER_DETOUR.md`. Density equations derived
before adding that phase are insufficient for the proposed upper law.

**Conditional shape theorem now proved.** For a specified M1/M2 law with
bounded densities, monotone positive-M1 and negative-M2 densities, and the
stated density-gap condition, all princess responses reduce to four scalar
parameters. `CONDITIONAL_RESPONSE_REDUCTION.md` includes negative transition
parameters and all boundary cases. This does not establish that an optimal
monster law satisfies the hypotheses, and the density functions remain
unknown. G5 is therefore still open.

**The sampled lower candidate is excluded.** The corrected numerical dual
has an explicit rational reconstruction defeated by a shifted sweep with
payoff at most approximately 1.21432. The marginal theorem in
`CENTRAL_CONCENTRATION.md` also defeats its ordered quantile rearrangement.
Do not reuse its restricted objective near 1.42804 as a lower bound. Any
replacement lower family must pass this marginal obstruction before more
expensive capture-order or Bellman work.

**Concrete continuum certificate route.** The notes in `research/08-continuum/`
now give explicit sufficient inequalities for each side of a proposed
saddle: a characteristic potential for an M1/M2 upper law, and a Bellman
potential with an exact endpoint-tail cost for a princess lower law. The
remaining work is to derive an actual candidate and verify both at the same
constant. The necessary density stationarity equations are a discovery aid,
not a substitute for those global inequalities.

The bounded numerical runs in this continuation were stopped after the
specified iteration limits or a decisive exclusion. Their source, seeds,
outputs, and stopping conditions appear in
`packages/interval_continuum_discovery/README.md`. The new exact upper bound
is recorded separately in `REFINED_UPPER_BOUND.md`; it does not close G6-G8.

Use the two exact best-response oracles in a double-oracle primal/dual search. For each support expansion, retain a rational monster upper certificate and princess lower certificate; only declare a case closed if both are unrestricted and match exactly (or via a rigorous limiting argument). If new counterexamples continue to appear, stop growing the support and prioritize G5, a genuine global structure theorem. Maintain distinct ledgers for finite supports versus a fully exhaustive reduction.

## Notes on finite approximation

`interval_uniform_reduction/PROOF.md` proposes an error-controlled limit of finite games. This supplies a potential computable characterization of V, but neither a simple exact constant nor a finite terminating certificate. Its CDF quantile-coupling and regularization proof should be independently audited before relying on it for any theorem beyond this research draft.
