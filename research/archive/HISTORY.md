# History of the research repository

> The research repository was retired on 2026-11-15 and its git history was not kept. These are its
> commit messages, verbatim and newest first, so that the order of the work stays readable. The files
> of the last commit are the rest of this folder. All commits are by the maintainer.

## The research branch

Branch `research/interval-progress-2026-11-10`, the head of pull request 1 (72 commits).

### 2026-11-15 13:42 · `dfc7fbc` · Solve exact center-wait Princess versus principal one-turn Monster subgame

### 2026-11-15 12:18 · `02d10e7` · Strategy page: keep no record of the visitor's tries [skip ci]

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

### 2026-11-15 11:52 · `3abf02e` · Strategy page: one side only, clearer hunt, plans and squeeze; a site build [skip ci]

The playground now shows every path on one side of the interval, so mirror
images no longer crowd the boards. The hunt, the Princess's plan and the
squeeze were redrawn to be read at a glance: the hunt shows which of her
paths are caught when, her plan groups the routes by how close they come to
the centre, and the squeeze puts each tried strategy on one number line
between the bounds.

build_strategy_page.py --site DIR writes the page as the folder for
vltanh.me/princess-monster-interval/, with the Princess's field in
field.bin (differences along the radius, gzip-compressed, 67 KB), so every
file is under the site's 500 KB limit.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

### 2026-11-15 08:57 · `3119a6e` · Redesign the strategy page as a playground; correct an overstated indifference claim [skip ci]

The page now follows the vltanh.me playgrounds (paper, ink, Newsreader,
numbered parts, board and readout panel, shared theme toggle):
1. Hide from the monster: steer the princess in a live round against a
   monster drawn from his plan, then see the exact average of your path
   against the whole plan; a demo follows a traced best path.
2. Catch the princess: drag the start and turn of a monster path and watch
   which of her curves it catches; lattice cost against her nodal field.
3. and 4. Explore each plan. 5. Indifference charts and the bounds.

Correctness of the page's numbers:
- Averages are exact for the monster's law placed on the grid 1/512, whose
  proved bound 1.4242096 (from atomic_upper.cpp, recorded in the data) the
  page quotes; a coarse four-point version could exceed its own claim.
- The meeting search also checks the monster's turning points, which a
  sample-only search missed. An apparent average of 1.424278 above the
  1/512 bound came from that; with the fix it is 1.423944, and a per-atom
  comparison found no capture time above the proof's table.
- Demo paths are the program's staircases stored exactly and followed just
  inside the far corners of their cells (average 1.42381 vs bound 1.42421).

Also corrects the summary, HANDOFF and STATUS: 96 % of the monster law's
probability (not all of it) is on paths within 2e-4 of the cheapest path
against the princess field, and 99 % within 1e-3.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

### 2026-11-15 08:29 · `a36cc15` · Consolidate the light-cone results and add an interactive strategy page [skip ci]

- research/14-light-cone-lattice/README.md: one summary of the 2026-11-14/15
  work: bounds with their level of checking, the Monster's law and the
  Princess's field, how nearly each equalizes the other's options, the
  structural findings, the next steps, and a file map.
- STATUS, HANDOFF, NEXT_WORK and the root README: the stacked dated update
  paragraphs are replaced by one current summary each, pointing to it. The
  independently replayed enclosure is still stated separately from the newer
  bounds. The stale 'BigInt replay pending' wording now says the replay was
  started, stopped after about 15 minutes and not completed.
- research/14-light-cone-lattice/strategies.html: self-contained page with
  spacetime pictures of both strategies, a Monster path against the
  Princess's field computed on the certificate's lattice, the Princess's
  best payoff and best responses against the Monster law, and the cost map
  of one- and two-turn Monster paths against the field. Built by
  packages/interval_lightcone/build_strategy_page.py from the committed law,
  field and programs (strategy_page_data.py, strategy_page_template.html).
- atomic_upper.cpp: the staircase output takes an explicit list of start
  cells (@k1,k2,...). The bound computation is unchanged: every integer in
  atomic_upper_replay.json was reproduced with the new build, and
  check_atomic_upper.py passes; the record's program hash is updated.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

### 2026-11-15 07:39 · `0f3052f` · n = 1024 certificate package; both programs agree on V <= 1.4240199 [skip ci]

- packages/interval_discovery_certificates/princess_front_n1024: field.json,
  center.replay.json and manifest.json as written by the unchanged
  refine.py (center engine, policy 4), plus the records of price_center
  policy 3 and of price_normalized on the identical binary input. All three
  return 18652368301398, i.e. V >= 9322984150699/6553600000000. The BigInt
  replay is running and is not claimed.
- The NumPy program returns the same integer as the C++ program for the law
  optimized for the grid 1/2048 (6413215524569876), so the upper bound
  1603303881142469/1125899906842624 has been computed by both.

Co-Authored-By: Claude Fable 5.2 <noreply@anthropic.com>

### 2026-11-15 07:09 · `4775295` · Lower-bound note: exact bank minima of grid-16, 32, 64 profiles under refinement [skip ci]

The repository's optimizer, seeded from the next coarser solution, gives the
best grid-k profiles in minutes. Refined and priced exactly, their bank
minima exceed their limits by about 0.18/n, and the limits rise by 2.5e-3 and
1.2e-3 per doubling of k (about 0.078/k below the estimated value). This
predicts about 1.4231 for a grid-128 profile priced at n = 1024.

Co-Authored-By: Claude Fable 5.2 <noreply@anthropic.com>

### 2026-11-15 07:08 · `13f9844` · n = 1024 lower bound: the second native engine returns the same minimum [skip ci]

price_center.cpp (policies 3 and 4) on the same binary table returns
18652368301398, as price_normalized.cpp did, in 25 minutes each. The note,
the replay record and the status files now say that both native engines
agree and that there is no independent BigInt replay.

Co-Authored-By: Claude Fable 5.2 <noreply@anthropic.com>

### 2026-11-15 06:24 · `ec5dd50` · NEXT_WORK: two routes to a better Princess field, with measured engine costs [skip ci]

Co-Authored-By: Claude Fable 5.2 <noreply@anthropic.com>

### 2026-11-15 06:20 · `5f90182` · Upper bound V <= 1.4240199 from a law optimized for the grid 1/2048 [skip ci]

650 rounds of optimize_atomic_law.py on 32 bins and the grid 1/2048 give
atomic_law_32bins_grid2048.txt with the exact bound
1603303881142469/1125899906842624 = 1.4240199075 (maximum 6413215524569876;
C++ program, the NumPy replay of this law is still running). The LP floor for
this class on this grid is 1.4240143. With the n = 1024 lower bound the
bracket is 1.4225745 <= V <= 1.4240199, width 0.0014454.

Co-Authored-By: Claude Fable 5.2 <noreply@anthropic.com>

### 2026-11-15 06:10 · `37d20a5` · Lower bound V >= 1.4225745 from the retained field refined to n = 1024 [skip ci]

The retained n512 Princess field is refined by a factor 2 with the
repository's common-threshold rule (exact over twice the denominator; the
order closure changes no node) and priced by the unchanged
price_normalized.cpp: complete normalized-bank minimum
18652368301398/13107200000000 = 1.4230627671, hence
V >= 9322984150699/6553600000000 = 1.4225744858854674 by the 1/(2n)
transfer (previously 1.4222581340234375).

One run (4.96 h, 16 GB, 3.6e10 retained states); no second engine and no
independent replay. The binary was byte-identical to a fresh build of the
repository source and reproduces the certified n512 minimum; the priced
table was compared byte for byte with the one refine_retained_field.py
rebuilds. Adds the note, the replay record and the status entries. With the
atomic upper bound: 1.4225745 <= V <= 1.4240687, width 0.0014941.

Co-Authored-By: Claude Fable 5.2 <noreply@anthropic.com>

### 2026-11-15 02:49 · `f65a5f2` · Atomic upper bound: Python replay agrees at N = 2048 for both 16-bin laws [skip ci]

Co-Authored-By: Claude Fable 5.2 <noreply@anthropic.com>

### 2026-11-15 02:42 · `0b8751c` · Capture-order pricing from samples; exact prices of the retained field on shifted lattices [skip ci]

capture_order_pricing_samples.cpp prices ordered laws given by integer
samples (it returns the same integers as capture_order_pricing.cpp on three
test laws). The retained n512 field on M shifted copies of the lattice is
worth exactly 1.4045756 (1000 levels, M = 2) and 1.4137093 (1000 levels,
M = 4): valid lower bounds, weaker than the lattice certificate, with an
error of about 0.04/M.

Co-Authored-By: Claude Fable 5.2 <noreply@anthropic.com>

### 2026-11-15 02:34 · `7537028` · Compiled capture-order pricing; first exact prices of finite Princess laws [skip ci]

capture_order_pricing.cpp is the integer version of the continuous-time
best-response program; it equals the Python program on 60 random families
and prices a 1000-path law in 22 s. Equal-mass family paths sampled from the
n = 24 family solution are worth exactly 1.381741 (300 paths) and 1.398481
(1000 paths). NEXT_WORK records what is missing: a finite law close enough
to the optimum.

Co-Authored-By: Claude Fable 5.2 <noreply@anthropic.com>

### 2026-11-15 02:23 · `3a449ab` · Prototype: exact continuous-time pricing of a finite ordered Princess law [skip ci]

capture_order_pricing.py computes the Monster's best response against a
finite set of ordered piecewise-linear Princess paths as a shortest-path
problem over (captured interval, side) with Pareto labels, in exact
fractions. On 40 random families of lattice paths it equals an exhaustive
search over lattice Monster paths.

First application, recorded in NEXT_WORK: paths taken from a lattice optimum
come in bundles and price poorly (1.10 to 1.25 at n = 8 against L_8 = 1.40);
the method needs laws without bundles.

Co-Authored-By: Claude Fable 5.2 <noreply@anthropic.com>

### 2026-11-15 02:14 · `f7064dd` · NEXT_WORK: proposal for exact continuous-time pricing of finite ordered Princess laws [skip ci]

Co-Authored-By: Claude Fable 5.2 <noreply@anthropic.com>

### 2026-11-15 02:10 · `2903e86` · Upper bound V <= 1.4240687 from a law optimized for the grid 1/1024 [skip ci]

optimize_atomic_law.py treats the bin masses as LP variables and uses
atomic_upper.cpp as the exact response oracle (each staircase is a cutting
plane). On 32 bins and the grid 1/1024 it gives a law with the exact bound
6263120207237/4398046511104 = 1.4240686613, computed by both the C++ and the
NumPy program (maximum 801679386526336). The LP value 1.4240491 is a floor
for this class of laws on this grid.

- atomic_upper.cpp can now write maximising staircases; the earlier integers
  are reproduced and the check suite passes.
- A law is tied to its grid: the bound of a grid-optimized law gets worse on
  finer grids. Section 7 of the note records this and the extrapolation of
  the optimal bounds (about 1.4240 for the two-family game).
- refine_retained_field.py: exact factor-2 refinement of the retained n512
  field for pricing at n = 1024 (self-test against a literal port).
- STATUS, HANDOFF, README, NEXT_WORK updated; width with this upper 0.0018106.

Co-Authored-By: Claude Fable 5.2 <noreply@anthropic.com>

### 2026-11-15 01:55 · `2e2f999` · Lattice note: the Monster's loitering paths constrain the Princess; binning costs her more [skip ci]

With the family Princess and the exact Monster at n = 16, 0.2 % of the
Monster's weight is on paths that loiter near the center before sweeping. A
family law optimized against one-turn and two-turn Monsters only (1.412883527
against them) is held to 1.405654829 by a Monster that waits at the center;
the exact engine and the Python frontier program agree on that number.
Grouping her paths in bins of two cells by two steps costs 2.8e-3 at n = 16.

Co-Authored-By: Claude Fable 5.2 <noreply@anthropic.com>

### 2026-11-15 01:39 · `118bfad` · Princess three-parameter family: within 4e-5 of the lattice optimum [skip ci]

On the half-offset lattice, with the Monster unrestricted, the ordered law of
a mixture of paths 'out for a short time, in, (wait at the center), out,
stay' reaches 1.401183987 / 1.412892780 / 1.416567551 at n = 8 / 16 / 24,
against L_n = 1.401192172 / 1.412922839 / 1.416604366. Without the outward
run the loss is 2.8e-3. The run has the same physical length (about 0.02) at
n = 8 and 16.

Adds princess_family_lattice.py, a subsection of the lattice note, and the
corresponding STATUS / NEXT_WORK entries. Floating-point LP values.

Co-Authored-By: Claude Fable 5.2 <noreply@anthropic.com>

### 2026-11-15 01:23 · `7085725` · Prove the clock-grid identity U_n = L_n + 1/(4n) for the lattice game [skip ci]

The far-corner argument of the atomic upper bound applies to any symmetric
law on lattice paths: a Princess curve that avoids the lattice points crosses
the same lattice edges as the odd-lattice path through its cells, at most
delta/2 later and arbitrarily close to that. The note now gives this proof
instead of recording the identity as a numerical observation.

Co-Authored-By: Claude Fable 5.2 <noreply@anthropic.com>

### 2026-11-15 00:50 · `262e127` · Exact upper bound from an atomic one-turn and two-turn law: V <= 1.42413, W_1 <= 1.42452 [skip ci]

An explicit atomic Monster law of one-turn paths P_b(a) and two-turn paths
T_2(c, U_1) on the grid 1/4096 has the all-Princess upper bound
51309688667845787/36028797018963968 = 1.4241299436..., below the previous
142472349375511/100000000000003. With one-turn paths only the bound is
W_1 <= 25661865897887875/18014398509481984 = 1.4245197187....

- research/14-light-cone-lattice/ATOMIC_TWO_TURN_UPPER.md: the law, the proof
  (reflection to radial paths, capture times at grid-line crossings in light
  coordinates, far-corner bound on cell staircases) and the computation.
- packages/interval_lightcone/atomic_upper.cpp: integer dynamic program over
  cell staircases with an a-priori overflow guard.
- atomic_response.py: independent NumPy version. check_atomic_upper.py: table
  against physical trajectories in exact fractions, dynamic program against
  exhaustive enumeration on N = 1, 2, C++ against Python up to N = 256.
- atomic_upper_replay.json: both laws at N = 256 ... 4096.

Status: written proof plus exact computation; no independent review and no
Lean. STATUS, HANDOFF, README and NEXT_WORK list it separately from the
independently replayed enclosure. Also records L_32 = 1.418473089 from the
lattice solver.

Co-Authored-By: Claude Fable 5.2 <noreply@anthropic.com>

### 2026-11-15 00:02 · `306be2e` · Finish the continuum update: README, results, STATUS and HANDOFF [skip ci]

The previous commit (da77959) went out incomplete: an editing script
stopped half way, so it contains the solver and the two notes but not the
entry-point updates its message mentions. This commit adds them:

- README and results.json of packages/interval_lightcone list
  continuum_turn_levels.py and its numbers;
- the light-cone note's sections on the value estimate and next steps;
- STATUS and HANDOFF rows for the uncertified continuum laws (response
  1.42449 with one turn, 1.42410 with two-turn paths, at 16 bins) and for
  the one-turn indifference equations.

No CI run; the certified bracket is unchanged.

Co-Authored-By: Claude Fable 5.2 <noreply@anthropic.com>

### 2026-11-15 00:02 · `da77959` · Continuum LP with turn levels and two-turn paths; one-turn indifference equations [skip ci]

continuum_turn_levels.py solves the continuum game with piecewise-constant
Monster densities and exact integration: one-turn paths with turn levels
uniform on bins next to b = 1, and the two-turn family T2(c, U1) that runs
from c to meet the mirror image of P_1(-U1) and then follows it.

Numerical results at 16 bins (floating point, Princess response on a mesh):
- one turn: LP value 1.4244766, response 1.4244888 on finer meshes;
- with two-turn paths: 1.4240833, response 1.4240990.
Both are below the certified upper bound 1.424723 but are not certificates:
no exact arithmetic and no bound yet for Princess corners off the mesh.

ONE_TURN_INDIFFERENCE_EQUATIONS.md derives, for the support seen in the
numerical optima, the linear relations between the densities of the two
players (for example rho(c) = e/(7 - c) and (7 + a) p + (1 - a) s = e) and
checks them against the lattice and continuum optima. The layer before
time 1 and the thresholds are not solved.

STATUS and HANDOFF updated. No CI run; the certified bracket is unchanged.

Co-Authored-By: Claude Fable 5.2 <noreply@anthropic.com>

### 2026-11-14 23:44 · `1fbeedc` · Correct the note on the retained field; price lattice optima with the exact engine [skip ci]

The first version of the light-cone note inferred that the retained n512
Princess field has the structure of an n = 16 optimum. That inference was
wrong: by its own provenance the field is a full-width profile on grid 64,
optimized for the price of its interpolant and then refined. The two
solutions share a phase structure (median nodal difference 5.4e-4 at the
shared nodes) and nothing more is claimed now.

New check: price_normalized.cpp, run on the optimal fields of the lattice
solver, returns the solver's value plus 1/(4n) to rounding, with exact bank
minima 45838149486/32000000000 (n = 8) and 91427061649/64000000000
(n = 16). The common-threshold interpolant of the n = 16 optimum prices
only 1.4170340, 1.4141311, 1.4122022 on n = 32, 64, 128, so lattice optima
are not seeds for a better certified lower bound.

Adds price_lattice_optimum.py and corrects STATUS, HANDOFF and NEXT_WORK.
No CI run; the certified bracket is unchanged.

Co-Authored-By: Claude Fable 5.2 <noreply@anthropic.com>

### 2026-11-14 23:02 · `fc3060a` · Add validated light-cone lattice solver and its numerical findings [skip ci]

New package packages/interval_lightcone: a Princess nodal-field LP with an
exact frontier dynamic program for the Monster, written in the light
coordinates U = t + x, W = t - x, plus turn-limited and one-turn variants
and a continuum one-turn LP with piecewise-constant start densities.

The unrestricted solver reproduces the exact clock-grid optima U_n for
n = 1, 2, 3, 4, 6 to 2e-15 through U_n = L_n + 1/(4n) and gives L_8, L_16
and L_24. These are floating-point LP values, not certificates; the
certified bracket is unchanged.

Findings recorded in research/14-light-cone-lattice:
- one interior Monster turn is within 1.7e-4, 7.9e-5, 5.2e-5, 2.2e-4 of
  unrestricted play at n = 4, 8, 16, 24 (small, not decreasing);
- turn levels just off b = 1 matter: levels b = 1 and b = 2 - a alone cost
  7.7e-4 at n = 16 and stay near 1.4254 in the continuum;
- the retained n512 Princess field agrees with the n = 16 optimum at
  shared nodes (median difference 5.4e-4);
- extrapolated grid values put V near 1.424 (estimate, not a bound).

STATUS, HANDOFF, NEXT_WORK, the package map and the working note point to
the new note. No CI run and no Lean result.

Co-Authored-By: Claude Fable 5.2 <noreply@anthropic.com>

### 2026-11-14 16:11 · `3996407` · Close frozen one-turn separation with exact continuum certificate [skip ci]

Retain a legal canonical one-turn Monster law with all-Princess upper
142472349375511/100000000000003, strictly below the frozen benchmark.
The integer/P2 certificate replays 730146 exact rational inequalities
with zero residual repair and improves the unrestricted upper as well.

Include the physical payoff and continuum coverage proofs, exact verifier,
independent capture checks, prior projected checkpoint, and finite-bank
obstruction. Update the handoff and status to distinguish the resolved
comparison from the still-open exact restricted and unrestricted values.

Validation: local frozen replay, verifier self-tests, two chronological
physical audits, finite-bank replay, subgame regression, and independent
projected-upper reconstruction. No new CI run or Lean result is claimed.

### 2026-11-14 14:43 · `fca015c` · research: certify improved physical one-turn upper independently [skip ci]

### 2026-11-14 14:18 · `1b47f50` · Prove one-turn minimax and exact finite lower hierarchy with full-domain capture checker [skip ci]

### 2026-11-14 13:48 · `d557835` · Prove endpoint-only one-turn repair obstruction with exact capture replay [skip ci]

### 2026-11-14 13:27 · `47b6e61` · Certify reweighted one-turn physical upper with independent integer replay [skip ci]

### 2026-11-14 13:12 · `ecccd6b` · Close complete one-turn response domain and exact boundary formulas [skip ci]

### 2026-11-14 13:00 · `5d7004f` · Direct one-turn necessity research through complete continuous response and two-sided certificates

### 2026-11-14 10:37 · `f14ace8` · Certify an all-Princess upper for the one-interior-turn Monster subgame

### 2026-11-13 22:41 · `d7612c6` · Audit Monster switch distributions and certify the role of rare path families

Merge duplicate calendars and bind the exact 752-pair physical law. Two independent Fraction collision routines verify a center-wait Princess counterexample to three fixed-proportion ablations. Derive a discontinuous switch-time contact formula and a low-dimensional duration hierarchy.

Retain the exact report and a cheap CI replay. A two-interior-turn sublaw inherits a slightly weaker upper; no new best bound, continuum-family exclusion, or equilibrium sufficiency is asserted. Preserve all concurrent geometry and finite-support matching results.

### 2026-11-13 22:31 · `878d526` · Reduce physical matching to antipodal events; disprove universal front-one projection

Prove causal first-antipodal pressure retiming and an N+2-knot normal form for each finite fully matched Monster support. Keep finite optimal support explicitly open. Include simultaneous rate-limited Princess domination and the endpoint-start gap.

Add an exact six-target security-loss counterexample to direct front-one completion, its complete capture-order replay, and a bounded-density extension. Strengthen the local curvature exchange to resolve the atom-free cusp's finite global response, while excluding its whole-inner extension through U=21/16.

Preserve all numerical certificates and manual-only discovery policy; add focused geometry regressions. No exact game value or completed Lean proof is claimed.

### 2026-11-13 21:58 · `abf3171` · Separate the atom-free cusp's centered and free-start optima

Prove that every front-one radial power cusp has a finite off-center response strictly better than its centered Zeno optimum. Use one early maximal excursion and the attained finite positive-gap continuation, then advance the remaining path and bound all chronological captures.

Keep the static majority-center global-Zeno theorem unchanged. The comparison does not assert a finite global optimizer or solve the unrestricted equilibrium.

### 2026-11-13 21:51 · `102b396` · Prove inner curvature exclusion and global free-start Zeno obstruction

Extend the curved exchange to first positive-region exit and replace the center density hypothesis with a continuity modulus. Prove that an endpoint sweep excludes the same inner monotonicity already through U=41/40, and give an attained static-law counterexample to a universal finite-turn free-start response theorem.

Add independent exact physical boundary regressions and integrate the reviewed scopes into the condensed geometry program. Preserve all numerical certificates, archived handoffs, and manual-only discovery policy. The unrestricted game remains open.

### 2026-11-13 21:41 · `96a9b82` · Freeze numerical discovery to manual dispatch; add exact geometry regression CI

### 2026-11-13 21:40 · `210477f` · Reframe interval game PR around global equilibrium geometry; archive numerical handoffs

### 2026-11-13 21:25 · `1dec0f8` · Merge remote-tracking branch 'origin/research/interval-progress-2026-11-10' into research/interval-progress-2026-11-10

### 2026-11-13 21:25 · `3eb98b7` · Merge remote-tracking branch 'origin/research/interval-progress-2026-11-10' into research/interval-progress-2026-11-10

### 2026-11-13 21:25 · `abb80a0` · Prove curved initial response and finite postcenter gates; audit retained n512 certificate

Give an explicit three-parameter LRL guard, a one-parameter incoming-front continuation, and finite return bounds from density and center slack. Endpoint mixing yields a value-dense regular class with finite postcenter complexity per member. Prove the fixed-center Zeno obstruction and conditional front-one nonalgebraicity without claiming a finite equilibrium class or exact game solution.

Retain independent physical regressions and stronger source/proof/artifact bindings for the completed n512 lower. Reconcile the authoritative 1.4222581340234375–1.4250455536616162109375 bracket with all concurrent discovery outcomes.

### 2026-11-13 21:25 · `91cf786` · feat(discovery): run and resume selective hybrid CDF searches

### 2026-11-13 21:20 · `6b0c501` · feat(discovery): implement hybrid continuous record hypographs

### 2026-11-13 21:17 · `1b0cf3c` · Close the joint CI campaign with exact outcomes and revised proof priorities

Bind all three completed discovery artifacts and all 19 complete native pricing results. Record no improvement beyond the retained n512/752-pair bracket, distinguish calendar failures from physical counterexamples, and retain exact fixed-field diagnostics. Update the single handoff with completed verification, the unmet 1e-4 target, and the next structural gate.

### 2026-11-13 21:07 · `378fbeb` · Bind the stronger certified bracket and preserve every discovery candidate

Retain rejected Princess trials and every complete-priced field with immutable hashes, exact best selection and safe resumption. Record failed geometry families and the earlier-front obstruction. Add exact continuous-record hypographs with conservative secant error and independent regressions. Keep expensive campaigns explicitly selected, preserve portable replay inputs, and update the authoritative bound and proof handoff.

### 2026-11-13 20:50 · `855d87a` · Retain independently certified n512 Princess and discover joint physical Monster laws

Archive the completed exact front512 lower and explicit Princess extraction with original CI bytes and hashes. Add native max-flow optimization with exact endpoint-loop separation, preserve the n512 fixed-law clock obstruction, and run three joint path/probability discovery families. Keep complete response verification separate from inexpensive retention checks.

### 2026-11-13 20:40 · `f79b812` · Search Princess geometry with exact path-record hypographs and certify fixed-field refinement ceilings

### 2026-11-13 20:31 · `4503f3e` · Independently replay stronger incoming-front refinement and regenerate explicit Princess laws

### 2026-11-13 20:27 · `3265d48` · Couple initial contact obstacles, prove conditional return compression, and record verified n256 upper

Add exact moving-front upper and inward-endpoint lower equations with independent chronological replays, active-valley endpoint scaling, and a strict central-return compression theorem under an explicit shape hypothesis. Preserve the failed prefix shortcut as an exact countercheck.

Update the authoritative bracket to the independently retained 752-pair Monster certificate and recognize the concurrent exact center engine. The unrestricted equilibrium and finite sufficient Princess class remain open.

### 2026-11-13 20:26 · `0882acb` · Independently replay fine lower targets with compact BigInt pricing and prove affine-cell reduction

### 2026-11-13 20:23 · `23deb66` · Search finer causal clocks with independently checked native integer flow

### 2026-11-13 20:13 · `43ecfa2` · Search continuous Princess geometry with exact floors and incoming-front constraints

Separate continuous physical-attack supporting planes from the sampled-bank lower objective. Run three independent full and front-constrained discovery families, preserve exact rejected attacks and resumable state, and require complete bank pricing for accepted geometry.

Add exact quantile extraction and continuous rational attack scoring, front-aware center termination, and integer-only fine refinement. Gate independent BigInt certification on a genuinely stronger native lower. Existing exact verification and all concurrent global front results remain intact.

### 2026-11-13 20:04 · `a276a73` · Certify a new physical upper and compress exact center response searches

Retain the CI-discovered n256 physical law with upper 291849329389899/204800000000000, independent Python/Node flow-cut replay, exact hashes and source artifact provenance.

Prove phase-specific Pareto monotonicity for heavier-first balanced center excursions. Add exact deterministic-return jumps, unrestricted reference regressions and a separate CI replay. Preserve the original verifier and all concurrent incoming-front work.

### 2026-11-13 19:52 · `6417c7a` · Prove a global incoming-front reduction and preserve the certified Princess lower

Force each Princess rank outward at a security-preserving characteristic front. A law-independent physical Monster normalization then yields an optimal law completed by2V+2, with arbitrary Princess atoms handled by regularization.

Project the exact n256 field to the front-two subpolytope, retaining its proven bank lower and explicit Princess guarantee. Bind both source and projected artifacts in independent Node and Python replays; no new minimum-attainment claim.

Record exact bulk, endpoint-shadow and conditional square-root contact equations, with independent chronological capture checks. Add a lightweight front/contact CI workflow. Preserve concurrent adaptive-field and physical-mixture discovery; the unrestricted value bracket remains unchanged.

### 2026-11-13 19:50 · `cc94527` · Discover adaptive CDF fields and physical mixtures through exact closure cuts

Avoid freezing coarse transport geometry by optimizing charged CDF coordinates and extending them with exact lower/upper order envelopes closest to the incumbent. Seed only useful calendar planes while keeping every known physical response in separation.

Add a small probability master with an exact sparse max-flow oracle, multiple active cuts, and full-grid replay of improved physical laws. Preserve floating estimates separately from certified unrestricted uppers. Run independent CI families plus a complete n512 refinement and gated independent BigInt replay. No change to the authoritative bracket is asserted before new certificates finish.

### 2026-11-13 19:36 · `317d1d8` · Search finer Princess fields and new endpoint-layer Monster laws in CI

Add a separate four-family target-width discovery campaign. Princess searches optimize a finer transport field using complete integer separation, bounded updates and a component-level proximal model. Monster searches vary starts, inward loops, independent contact fronts and probabilities, with exact all-Princess physical replay.

Project Qout onto charged clock events and retain a growing sparse LP basis. An independent geometric edge checker reproduces the retained n128 upper with 21,139 nodes instead of 65,666; exact graph completeness is not trusted for upper acceptance. Add response-bank checkpoints, hashes, solver logs and resumable artifacts. The certified unrestricted bracket is unchanged by this implementation commit; a width below 1e-4 remains the research target.

### 2026-11-13 19:12 · `f54fb6a` · Close the continuous n1 response and certify fixed-family obstructions

Compute the exact response for every initial position against the supplied full-width n1 Princess field, with free-start security 39/32, complete precenter candidate regeneration, physical boundary constraints, and independent chronological replay. Extend exact-center CI through the full response.

Add the reviewed strict-transport and conditional initial-contact obstructions, the endpoint-loop kernel, and fixed-opponent outward completion. Independently realize 41 polynomial-germ Princess profiles and recapture all 57,646 oriented contacts to certify a 1.4250400082376236269997635 lower on the retained n64 law's entire strict common-warp family with fixed probabilities. This is not a lower on the unrestricted game.

Preserve the concurrent n128 physical upper, CI discovery artifacts, CDF shape results and heavier-first center theorem. The unrestricted interval remains 582291421641/409600000000 <= V <= 145925593551091/102400000000000. No matching saddle, finite equilibrium-sufficient Princess class or completed Lean formalization is claimed.

### 2026-11-13 18:45 · `1b00ea6` · Update the authoritative handoff with observed CI discoveries and the remaining equilibrium gate [skip ci]

Record the certified interval 582291421641/409600000000 <= V <= 145925593551091/102400000000000, the distinct explicit Princess security, actual artifact/run links, budget-stopped searches, and the absence of a further accepted shape in all three structural CI families. Preserve the concurrent complete fixed-field response theorem and the new heavier-first recurrence without claiming global equilibrium sufficiency or Lean verification.

Make campaign comparisons read the stronger retained upper and recompute historical improvement flags; local exact-baseline regression passed. Documentation and comparison metadata only: retain the already observed exact CI results without repeating unchanged exhaustive searches.

### 2026-11-13 18:40 · `973d730` · Prove heavier-first alternating center responses and the rank-balance boundary

Reuse an actual continuation or its reflection to compare sorted record states without changing triangle count. Minimum-count optimal continuations alternate signs; legal tent merging and direct endpoint tours cover center holds and large excursions. This yields an exact one-direction recurrence on ordered records, with returned record q no larger than the opposite record. Preserve the constant center trace and outward-after-two hypotheses. Independent manuscript audit and Fraction exchange regressions passed; no equilibrium-sufficient Princess class or new game value is claimed.

### 2026-11-13 18:37 · `999d60d` · Retain the CI-discovered unrestricted upper and launch structural CDF discovery

Archive the actual mutation-search artifact with U=145925593551091/102400000000000, independently checked physical clocks and integer flow/cut. Preserve its exact hashes, seed, logs provenance and budget qualification. Add parallel variation/curvature searches with fixed-security separation, including the current stronger Princess geometry, and a concrete physical counterexample to cached-bank-only smoothing. Add hash-bound extraction of explicit Princess laws from completed native certificates, with independent small BigInt regressions.

### 2026-11-13 18:35 · `70caa3a` · Complete exact finite Monster response for supplied common-threshold CDFs [skip ci]

Prove the two legal affine half-cell bounds and assemble the moving-kink reduction over monotone light rectangles. Include free starts, true endpoint contacts, arbitrary original turns, explicit 248n+94 / 744n+218 piece bounds, and finite rational quadratic computation with rational attainment. Update the canonical summaries to identify the remaining global Princess-equilibrium gap. Two independent manuscript reviews passed. No global saddle or Lean compilation is claimed. All four exact replay jobs at 6655765 passed; this commit changes manuscripts only and preserves concurrent discovery changes.

### 2026-11-13 18:32 · `8dfa025` · Preserve completed exact fields when a restarted LP reaches its budget [skip ci]

The restored plain master exceeded a genuine single-solve allowance after the cumulative-timer fix. Mark that outcome BUDGET_STOPPED without using an unfinished LP objective, while retaining unexpected errors as failures. Independent small discovery, BigInt, restart and budget regressions passed locally. Do not rerun the unchanged expensive campaign solely for this status correction; structural discovery and retained-certificate workflows follow separately.

### 2026-11-13 18:28 · `d1307d1` · Resume selected discovery searches and compare against the new certified lower

Preserve the concurrent fixed-field and lower-bound results. Reuse the corrected native HiGHS clock, restore the interrupted plain-search checkpoint, and retain exact native replay plus independent field and Fraction checks as the explicit promotion gate. Make a second full BigInt replay optional rather than silently conflating it with mathematical validity.

### 2026-11-13 18:21 · `6655765` · Prove finite post-center response and certify a stronger unrestricted lower

Prove 8n+4 post-center unit-speed legs for full-width common-threshold CDFs, or 24n+4 for positive narrow width, including arbitrary infinite excursions and closed center sets. Derive an exact finite rational quadratic envelope with polyhedral eligibility domains and a bounded scalar-elimination recurrence.

Implement and completely regenerate the n=1 five-layer center envelope: 48 exact pieces and center value 79/64. Independently integrate 297 reconstructed physical routes and replay 120 raw/pruned comparisons. Add exact quadratic polytope minima, endpoint/partial-excursion charts, scalar elimination, and dedicated CI.

Raise the unrestricted value lower to 582291421641/409600000000 through a full n=256 feasible Qout dual, independently verified by native integers and BigInt. Regenerate the explicit Princess law with security 582289859141/409600000000. Preserve the concurrent B=1536 lattice construction, its Princess extraction, discovery updates, and unchanged 703-pair upper 364842628535291/256000000000000.

Prove four-leg compression between moving-interface contacts and the stationary-kink bound. Correct the persistent HiGHS cumulative timer with a real regression. Pre-center off-interface reduction and a finite equilibrium-sufficient class remain open; no complete Lean proof is claimed.

### 2026-11-13 18:16 · `daad861` · Extract an explicit all-Monster Princess law from the full lattice certificate

Prove physical-to-clock domination and apply constructive common-threshold interpolation to obtain a NEW law securing 27450199627/19327352832 = 1.4202772550181382..., improving the retained fixed strategy by 0.0007940029. The game-value bound is unchanged and no security is assigned to the original frozen H3 CDF.

Save the portable law, source hashes and exact extraction. Check 4.7 million transport inequalities and independent Fraction regression on 4090 paths and 41544 clocks. Add a separate extraction CI job without rerunning discovery or pretending to reprice the unchanged 1.84-billion-transition certificate.

### 2026-11-13 18:12 · `840d255` · Use CI to discover new Princess CDFs and physical Monster laws

Add a separate five-experiment discovery workflow while preserving exact verification. Optimize new transport profiles and physical path mixtures, save resumable strategies and solver metadata, gate fine-grid pricing, and independently replay prospective unrestricted improvements. Keep finite-bank estimates, game-value transfer bounds, and same-strategy security distinct.

Validate 816 generated Princess-response seeds, 750 Monster mutation proposals, exact small-grid certificates, refinement and resumable best-candidate retention.

### 2026-11-13 17:44 · `17b8c5d` · Certify a meaningful unrestricted Princess–Monster lower bound

Prove V >= 3050023091/2147483648 by a complete B=1536 integer response search and the exact 1/B quantization transfer. The frozen CDF and all 1536 decision layers give K=18308527154 at scale 12884901888.

Prove the exact centered and uncentered time-one exits for supplied fields outward after one. Add safe persistent-endpoint pruning, independent cost precision, a compact frozen input, and a standalone replay with source/input hashes.

Validate the full 28,323,841-entry CDF and final fraction independently; pass 41 exhaustive Fraction regressions and the retained native sampler compatibility checks. Add CI coverage for the full lattice replay.

Preserve the concurrent normalized-bank reductions, explicit Princess law, and independently replayed 703-pair Monster upper. The combined interval is 1.420277678873389959... <= V <= 1.42516651771598046875, 41.86% narrower than the original task. Keep one current handoff and the exact saddle objective OPEN.

### 2026-11-13 17:26 · `eaa5755` · Certify stronger unrestricted bounds and exact normalized finite-bank reductions

Prove common left-floor clock atomization, first-endpoint/time-two physical normalization, feasible-Qout Princess extraction and fixed-law Qout closure uppers. Add exact n=4/n=6 certificates and equivalent uniform-clock checks.

Certify 363388689093/256000000000 <= V <= 364842628535291/256000000000000. The compact n=256 lower passes independent native and BigInt complete pricing; a legal Princess quantile law secures 726775425061/512000000000. The 703-pair Monster law has an exact flow/cut replay.

Add exact pursuit pruning, bounded witness storage and cached separation for discovery, plus rational interpolation/counterexample tests. Preserve concurrent finite-initial-support nonattainment results. Record the full-width quarter-mesh counterexample and the fixed-response triangulation caveat. The exact game and complete Lean proof remain open.

### 2026-11-13 16:47 · `34aa12a` · Prove finite-initial-support nonattainment and certify Princess contact obstructions

Show every finite-start Princess law is strictly improvable by a short-prefix mixture, ruling out attained finite-path equilibria. Give both compactness and saddle-complementarity proofs, with independent rational prefix/contact checks.

Certify an exact ceiling for every reweighting of the 338-path seed and its discontinuous loss under legal mesh snapping. Record the global two-sweep outgoing-cone constraint and a deterministic 588-path prefix regression with exact all-Monster verification.

Replay the existing unrestricted bounds, physical clocks, n=3 grid and extraction, and analytic-exit fixture. Update the sole current handoff and concise status. The exact value, sharp continuous lower, and matching unrestricted saddle remain OPEN.

### 2026-11-13 16:26 · `7d718af` · Research handoff: consolidate global proofs, archive legacy experiments, and preserve exact certificates

One reviewable commit replacing the 216-commit exploration timeline.
- Canonical HANDOFF.md, NEXT_WORK.md, ROADMAP.md, STATUS.md and REPRODUCE.md.
- Archive 64 historical research notes, 38 exploratory logs and eight long narratives verbatim.
- Retain all current proof manuscripts, executable verifiers, source inputs and CI workflow at stable paths.
- Archive full predecessor history on branch archive/pr1-pre-squash-2026-11-13.

The unrestricted interval game remains OPEN. Exact value bounds and theorem scopes unchanged.

### 2026-11-10 21:36 · `cdeba40` · Initialize research repository with problem statement

## Before the squash of 2026-11-13

Branch `archive/pr1-pre-squash-2026-11-13`: the commits of the first days before they were squashed into the branch above (216 commits).

### 2026-11-13 16:00 · `7253c33` · Extract explicit Princess strategies and certify the first three complete clock grids

### 2026-11-13 15:42 · `0b68d7d` · Prove an effective global finite reduction with polynomial clock LPs

### 2026-11-13 15:07 · `6603b41` · Reduce interior response cells to two runs and prove sticky endpoint value density

### 2026-11-13 14:29 · `7d01b1f` · Prove sharp outward horizons and finite quadratic response to every characteristic P1 field

### 2026-11-13 14:08 · `acd5c48` · Prove completeness of finite analytic-exit lower certificates and add exact replay

### 2026-11-13 13:34 · `ac53f68` · Prove attained full-pressure matching with protected tails and horizon nine

### 2026-11-13 13:21 · `9e0439d` · Reduce the full game to physically matched pressure on horizon nine

### 2026-11-13 12:59 · `744cd95` · Prove finite clock homogenization and certify continuum pressure completion

### 2026-11-13 12:30 · `d0e4d45` · Certify stronger unrestricted upper bound from full ordered-CDF optimization

### 2026-11-13 11:34 · `0eb5a1f` · Repair two escaped LaTeX labels in the horizon theorem

### 2026-11-13 11:32 · `7c3de4f` · Prove exact global horizon and sufficient finite-state clock lifting

### 2026-11-13 11:03 · `391f0c0` · Repair quantile symmetry and prove the aggregate clock relaxation is insufficient

### 2026-11-13 11:01 · `6908c3f` · Replay tight unrestricted upper certificate in native Node

### 2026-11-13 10:32 · `aba66a5` · Repair Markdown math and formatting in global effort-discrepancy summary [skip ci]

### 2026-11-13 10:32 · `d6b0b59` · Repair Markdown math and formatting in global effort-discrepancy summary [skip ci]

### 2026-11-13 10:32 · `e61c2e8` · Repair Markdown math and formatting in global effort-discrepancy summary [skip ci]

### 2026-11-13 10:32 · `24f8384` · Link corrected global matching theorem and effort–deficiency obstruction in research/12-global-closure/README.md [skip ci]

### 2026-11-13 10:32 · `ed59b90` · Link corrected global matching theorem and effort–deficiency obstruction in STATUS.md [skip ci]

### 2026-11-13 10:32 · `bf43cdc` · Link corrected global matching theorem and effort–deficiency obstruction in HANDOFF_2026-11-13.md [skip ci]

### 2026-11-13 10:31 · `eceb5fe` · Add global effort-versus-causal-matching uncertainty inequality [skip ci]

### 2026-11-13 10:29 · `a165bc9` · Index global causal-pressure Strassen matching proof and exact verifier in REPRODUCE.md [skip ci]

### 2026-11-13 10:29 · `8b3495a` · Index global causal-pressure Strassen matching proof and exact verifier in research/12-global-closure/README.md [skip ci]

### 2026-11-13 10:29 · `c255f35` · Index global causal-pressure Strassen matching proof and exact verifier in STATUS.md [skip ci]

### 2026-11-13 10:29 · `9aecbdb` · Index global causal-pressure Strassen matching proof and exact verifier in HANDOFF_2026-11-13.md [skip ci]

### 2026-11-13 10:29 · `59aa0f1` · Record exact matching/backlog regression counts and compact-set Hall formulation [skip ci]

### 2026-11-13 10:28 · `3a61961` · Byte-match executed exact Fraction pressure-matching verifier [skip ci]

### 2026-11-13 10:26 · `e7573c9` · Verify causal pressure max-flow matching and backlog flux identities with exact Fraction arithmetic [skip ci]

### 2026-11-13 10:25 · `c81e57f` · Correct domain notation for global active-occupation mass [skip ci]

### 2026-11-13 10:22 · `90ead30` · Derive unrestricted causal-pressure Strassen matching and search-effort discrepancy dual [skip ci]

### 2026-11-13 09:41 · `f1423f0` · Correct handoff: halving is arbitrary Bellman bookkeeping, not optimal strategic recurrence [skip ci]

### 2026-11-13 09:40 · `9d71989` · Add exact optimal straight-route counterexample to treating halving as a turn [skip ci]

### 2026-11-13 09:40 · `92d8d02` · Clarify that halving is arbitrary accounting, prove every-threshold DPP and reject strategic-switch interpretation [skip ci]

### 2026-11-13 09:25 · `fa129be` · Record executed recurrence tests and pin the byte-matched Python source [skip ci]

### 2026-11-13 09:25 · `15fa61d` · Test half-survival response recurrence with exact moving-target DP and physical captures [skip ci]

### 2026-11-13 09:24 · `3f2f9f7` · Derive a globally contractive survivor-mass recurrence for unrestricted Monster responses [skip ci]

### 2026-11-13 09:09 · `2da8deb` · Pin authoritative unrestricted-game handoff and current certificate scope in research/12-global-closure/README.md [skip ci]

### 2026-11-13 09:09 · `86666cd` · Pin authoritative unrestricted-game handoff and current certificate scope in REPRODUCE.md [skip ci]

### 2026-11-13 09:09 · `0675b9f` · Pin authoritative unrestricted-game handoff and current certificate scope in STATUS.md [skip ci]

### 2026-11-13 09:09 · `15c8307` · Pin authoritative unrestricted-game handoff and current certificate scope in ROADMAP.md [skip ci]

### 2026-11-13 09:09 · `e9591c4` · Pin authoritative unrestricted-game handoff and current certificate scope in README.md [skip ci]

### 2026-11-13 09:08 · `fcb08de` · Fix Markdown paragraph boundary in upper-certificate audit note [skip ci]

### 2026-11-13 09:08 · `9990364` · Audit tight-upper provenance: distinguish historical warp verifier from tight certificate [skip ci]

### 2026-11-13 09:06 · `b1a95bd` · Normalize Markdown code fencing and inline literals in consolidated handoff [skip ci]

### 2026-11-13 09:05 · `47c9187` · Consolidate 172-commit unrestricted Princess–Monster research into audited global proof handoff [skip ci]

### 2026-11-13 08:55 · `325345f` · Emphasize unrestricted global coercivity and still-open matching Bellman/HJB gate [skip ci]

### 2026-11-13 08:52 · `60890f3` · Record global continuum-offset stability and nonzero near-sweep energy barrier [skip ci]

### 2026-11-13 08:51 · `1033751` · Verify continuous Princess-offset integration and rational global coercivity threshold [skip ci]

### 2026-11-13 08:51 · `533ffba` · Strengthen global endpoint stability via continuum Princess offsets, convexity and Jensen [skip ci]

### 2026-11-13 08:43 · `bc514d5` · Add 1050-path exact first-contact regression for global sweep-stability theorem [skip ci]

### 2026-11-13 08:43 · `28bb72f` · Prove global sweep stability modulus and nonzero optimal Monster excursion energy [skip ci]

### 2026-11-13 08:09 · `cedef2b` · Track exact fixed-start Monster response and global initial-position/reversal moment bound [skip ci]

### 2026-11-13 08:09 · `a4d722c` · Verify exact fixed-start Monster runner response with 37 rational physical fixtures [skip ci]

### 2026-11-13 08:08 · `32659bb` · Solve exact fixed-start Monster response to runner law and derive global initial-position/reversal moment inequality [skip ci]

### 2026-11-13 08:08 · `c85609f` · Record exact all-monotone game and canonical interior-start reversing support theorem [skip ci]

### 2026-11-13 08:07 · `0d6e9b5` · Eliminate every endpoint-start reversing Monster trajectory from a canonical unrestricted optimum [skip ci]

### 2026-11-13 08:07 · `2ce00b2` · Add exact rational weighted sweep envelope verifier [skip ci]

### 2026-11-13 08:07 · `88bf458` · Clarify boundary-weight attainment and nonuniqueness of monotone minimizers [skip ci]

### 2026-11-13 08:07 · `223d20d` · Solve all-monotone Monster subgame and weighted sweep envelope exactly [skip ci]

### 2026-11-12 23:55 · `6b16660` · Ledger global order-one contact germ theorem and free-flow singular-pressure exclusion [skip ci]

### 2026-11-12 23:54 · `1bf2232` · Index global attained infinite-horizon dual, monotone clock, and singular contact-germ proof [skip ci]

### 2026-11-12 23:54 · `6873faa` · Cross-reference attained unrestricted dual and exact contact-germ closure [skip ci]

### 2026-11-12 23:53 · `933a230` · Prove exact order-one global contact-germ jumps and singular free-flow pressure exclusion [skip ci]

### 2026-11-12 23:51 · `d964bf7` · Ledger: exact attained unrestricted one-clock minimax and productive reversal structural bound [skip ci]

### 2026-11-12 23:49 · `bdca413` · Clarify canonical global dual reversal sector is precompletion nonmonotone [skip ci]

### 2026-11-12 23:49 · `3351a4e` · Strengthen universal reversal-mass theorem to productive precompletion turns [skip ci]

### 2026-11-12 23:47 · `ecd96aa` · Verify causal time quantile clock and exact continuous two-sweep radial score [skip ci]

### 2026-11-12 23:46 · `c174515` · Split global active occupation into explicit sweep characteristic and unknown reversing pressure [skip ci]

### 2026-11-12 23:45 · `78b1e46` · Prove attained exact unrestricted one-clock dual with finite active occupation mass [skip ci]

### 2026-11-12 23:40 · `6f4a243` · Compress global dual to one monotone causal clock and uniformly bounded active occupation [skip ci]

### 2026-11-12 23:36 · `389fab8` · Canonicalize attaining strong record dual to endpoint sweeps plus reversing histories [skip ci]

### 2026-11-12 23:34 · `5db4736` · Add exact rational finite causal-selector duality and radial-contact verifier [skip ci]

### 2026-11-12 23:32 · `ec496b3` · Prove attained global causal selector strong duality and symmetric radial oracle [skip ci]

### 2026-11-12 23:17 · `18c2ec8` · Handoff canonical optimal Monster sweep/reversal decomposition and broader exact tests [skip ci]

### 2026-11-12 23:16 · `6073b8a` · Canonicalize an optimal Monster law into exact endpoint sweeps plus reversing histories [skip ci]

### 2026-11-12 23:15 · `270fa16` · Document full dual/reversal test fixtures and precise execution provenance [skip ci]

### 2026-11-12 23:15 · `043135e` · Reproduce exact 338-path Princess vs monotone sweep cross in Fraction [skip ci]

### 2026-11-12 23:14 · `98a6aba` · Physically verify 7.39% reversal theorem ingredient against 259 unrestricted Monster prefixes [skip ci]

### 2026-11-12 23:14 · `579cca0` · Record sharpened 7.39% universal optimal reversal support theorem and exact sweep cross-score [skip ci]

### 2026-11-12 23:13 · `fad16b5` · Sharpen universal optimal Monster reversing mass to 7.39% via exact unrestricted two-runner response [skip ci]

### 2026-11-12 23:10 · `fd713a7` · Track global record dual and theorem forcing reversals in all optimal Monster laws [skip ci]

### 2026-11-12 23:10 · `c2b53c2` · Prove every unrestricted optimal Monster law has >=4.9% reversing mass [skip ci]

### 2026-11-12 23:06 · `5d72b5f` · Link exact 429-path dual and physical first-contact verifier [skip ci]

### 2026-11-12 23:06 · `031d7a2` · Add Fraction physical/causal-selector regression for solved two-sweep subgame [skip ci]

### 2026-11-12 23:05 · `f610694` · Derive global record-occupation HJB dual, free-flow balance, exact two-sweep nonattainment [skip ci]

### 2026-11-12 22:47 · `5e73ad3` · Track global CDF transport LP and discontinue frozen-bank G2 direction [skip ci]

### 2026-11-12 22:46 · `6f724a6` · Introduce unrestricted CDF transport LP and strict reordering witness [skip ci]

### 2026-11-12 22:22 · `e521eca` · Add executable G2 four-cut, all-ray exclusion handoff to global closure README

### 2026-11-12 22:21 · `68bf531` · Record two exact all-mass G2 exclusions and verified four-column physical cut bank

### 2026-11-12 22:21 · `911ad03` · Record two exact all-mass G2 exclusions and verified four-column physical cut bank

### 2026-11-12 22:21 · `44a6c3e` · Record two exact all-mass G2 exclusions and verified four-column physical cut bank

### 2026-11-12 22:20 · `8018397` · Prove exact continuum exclusion of entire injection and sweep-transfer Monster weight rays

### 2026-11-12 22:20 · `394bf3e` · Strengthen exact certificate: all nonnegative injection weights also fail best upper bound

### 2026-11-12 22:19 · `3345374` · Certify full sweep-reweighting ray cannot beat best exact game upper bound

### 2026-11-12 22:17 · `2a6002f` · Extend G2 analysis with four exact Princess columns and correct face-certification scope

### 2026-11-12 22:17 · `b3061bf` · Add independent exact replay for all 2,248 G2 Princess cut captures

### 2026-11-12 22:16 · `bcde01f` · Add exact four-column physical Princess rejection screen for Monster weight proposals

### 2026-11-12 22:15 · `aa015b4` · Add fourth near-active Princess column to exact G2 master bank

### 2026-11-12 22:15 · `6b679eb` · Certify exact Princess germ defeating three-cut balanced Monster shift

### 2026-11-12 22:11 · `7a8ff80` · Grow G2 exact Princess cut bank to three columns and 1,686 physical hits

### 2026-11-12 22:11 · `fc4b9d5` · Add exact global Princess counterexample to 0.1% Monster sweep reweight

### 2026-11-12 22:09 · `d3f843d` · Add two globally valid exact Princess separation columns for coupled Monster master

### 2026-11-12 22:08 · `449b5b1` · Record G2 exact germ witness, failed global Monster updates and revised exchange gate

### 2026-11-12 22:08 · `cf3c339` · Record G2 exact germ witness, failed global Monster updates and revised exchange gate

### 2026-11-12 22:08 · `3f28cfa` · Record G2 exact germ witness, failed global Monster updates and revised exchange gate

### 2026-11-12 22:06 · `653bca3` · Prove exact near-active Monster dual test and exclude naive best-response injection

### 2026-11-12 22:05 · `258df5d` · Add exact 562-contact replay and mixture-ray exclusion check

### 2026-11-12 21:54 · `d6bccba` · Certify exact physical Princess attack against 1% best-response Monster injection

### 2026-11-12 21:30 · `c837705` · Record exact positive CDF first-variation witness and Monster deviation

### 2026-11-12 21:30 · `9162b5d` · Record exact positive CDF first-variation witness and Monster deviation

### 2026-11-12 21:29 · `1d52b4f` · Check exact archived strategy CDF directional ascent obstruction

### 2026-11-12 21:28 · `cd84e99` · Exhibit exact global CDF ascent direction rejecting archived 338x280 pair

### 2026-11-12 21:25 · `b7f8ecb` · Strengthen universal horizon and finite-rank guarantees multiplicatively

### 2026-11-12 21:25 · `fb18e3d` · Cross-link global minimax result to exact CDF variational KKT theorem

### 2026-11-12 21:24 · `0b49e3b` · Record G1b exact near-record CDF variational saddle theorem

### 2026-11-12 21:24 · `75dc092` · Record G1b exact near-record CDF variational saddle theorem

### 2026-11-12 21:24 · `62a1992` · Record G1b exact near-record CDF variational saddle theorem

### 2026-11-12 21:24 · `56f7ba7` · Record G1b exact near-record CDF variational saddle theorem

### 2026-11-12 21:23 · `dd3fd5a` · Close zero-weight extended-payoff detail in global minimax separation

### 2026-11-12 21:22 · `c6c7966` · Add exact tie and nonattainment regression checks for CDF first variation

### 2026-11-12 21:21 · `c10c6e3` · Derive exact global strict/closed-record CDF first variation and saddle test

### 2026-11-12 21:18 · `5f4d23c` · Record G1 global minimax, compact Monster optimizer and rank-horizon brackets

### 2026-11-12 21:18 · `00f935e` · Record G1 global minimax, compact Monster optimizer and rank-horizon brackets

### 2026-11-12 21:17 · `14ed7b2` · Record G1 global minimax, compact Monster optimizer and rank-horizon brackets

### 2026-11-12 21:17 · `eb9a4d0` · Record G1 global minimax, compact Monster optimizer and rank-horizon brackets

### 2026-11-12 21:15 · `059038b` · Add exact Monster coupling and global horizon/rank reduction fixtures

### 2026-11-12 21:15 · `f7a4d37` · Prove global minimax and attained Monster law; give uniform rank-horizon game reduction

### 2026-11-12 20:51 · `5a6a017` · Record exact long-horizon two-source all-count envelope and remaining saddle gates

### 2026-11-12 20:51 · `4698d08` · Record exact long-horizon two-source all-count envelope and remaining saddle gates

### 2026-11-12 20:51 · `b67d834` · Record exact long-horizon two-source all-count envelope and remaining saddle gates

### 2026-11-12 20:50 · `15c5e35` · Add exact productive Green approach fixtures for six finite turn counts

### 2026-11-12 20:49 · `803a0ee` · Add exact rational envelope certificate and phase-switch signs

### 2026-11-12 20:48 · `c66b9db` · Solve all-count fixed-terminal center-return envelope in long-horizon strip

### 2026-11-12 20:36 · `69f935d` · Record uniform all-count single-return closure and narrow remaining strip

### 2026-11-12 20:36 · `52481b9` · Record uniform all-count single-return closure and narrow remaining strip

### 2026-11-12 20:35 · `66f441c` · Add exact Fraction verifier for uniform single-return theorem

### 2026-11-12 20:35 · `3163cbc` · Prove all-count single-return optimality outside narrow front strip

### 2026-11-12 20:01 · `71a47f1` · Record infinite-turn short-hinge exclusion in all-count roadmap [skip ci]

### 2026-11-12 20:01 · `5b13574` · Record no-short-hinge necessity for terminal Zeno Monster controls [skip ci]

### 2026-11-12 20:01 · `d375463` · Extend all-short-hinge exclusion to terminal Zeno policies at every finite index [skip ci]

### 2026-11-12 19:58 · `0cebcd7` · Surface uniform finite-chain all-short-hinge deletion and Green reduction [skip ci]

### 2026-11-12 19:55 · `f7e9396` · Replace turn-by-turn hinge roadmap by all-count no-hinge Green and exterior gates [skip ci]

### 2026-11-12 19:55 · `f990f49` · Close all strict short-hinge branches of finite two-source terminal renewal [skip ci]

### 2026-11-12 19:54 · `0e45282` · Add 15,480 exact two-source, penultimate, and full-suffix merge checks [skip ci]

### 2026-11-12 19:53 · `8fa4027` · Eliminate first, interior, and terminal short hinges for finite center-renewal chains [skip ci]

### 2026-11-12 18:59 · `d30bafb` · Surface universal terminal-hinge deletion and high-surplus all-count closure [skip ci]

### 2026-11-12 18:59 · `b49e805` · Refine finite closure roadmap after eliminating terminal short hinges for all surplus levels [skip ci]

### 2026-11-12 18:58 · `5b83671` · Mark full terminal short-hinge class closed, with exact all-surplus merger theorem [skip ci]

### 2026-11-12 18:58 · `ffb8a87` · Check universal final-hinge strict merger across ratios and duration-two boundary [skip ci]

### 2026-11-12 18:57 · `7951610` · Add 165 exact terminal-short hinge merger fixtures and full moment comparisons [skip ci]

### 2026-11-12 18:57 · `55a517f` · Prove global final-short-hinge merger at all surplus levels and turn counts [skip ci]

### 2026-11-12 18:53 · `7773089` · Surface completed all-turn high-surplus and waited-continuation theorems [skip ci]

### 2026-11-12 18:52 · `52470e6` · Extend high-surplus one-return theorem through terminal Zeno accumulation [skip ci]

### 2026-11-12 18:52 · `0b30221` · Handoff closed all-count high-rank renewal region and state next finite gate [skip ci]

### 2026-11-12 18:51 · `1a12c2c` · Record proved all-turn high-surplus wedge and completed waiting-strip gate [skip ci]

### 2026-11-12 18:50 · `80620bc` · Match exact locally executed rational verifier source [skip ci]

### 2026-11-12 18:49 · `ec8bb1b` · Extend all-count theorem to the initial-wait continuum and exact two-endpoint policies [skip ci]

### 2026-11-12 18:49 · `fdb29ed` · Verify high-surplus waited all-count suffix elimination and endpoint departure reduction [skip ci]

### 2026-11-12 18:48 · `2da985d` · Polish high-surplus proof notation and executable references [skip ci]

### 2026-11-12 18:47 · `10d29e3` · Add independent exact physical-moment checks for high-surplus and waiting-time theorems [skip ci]

### 2026-11-12 18:47 · `f70e9ac` · Prove all-count high-surplus one-return dominance and strict waited-tent concavity [skip ci]

### 2026-11-12 18:27 · `3351b7a` · Record failed global bound tests and isolate the substantive M3 certification target [skip ci]

### 2026-11-12 18:02 · `11fe3ff` · Improve unrestricted game upper via exact integer max-flow and warp [skip ci]

### 2026-11-12 17:44 · `bb2c4af` · Reject numerically infeasible all-warp discovery simplex outputs [skip ci]

### 2026-11-12 17:42 · `e28e38a` · Handoff the tightened all-warp interval and preserve full-game open gates [skip ci]

### 2026-11-12 17:42 · `95bd1fa` · Handoff the tightened all-warp interval and preserve full-game open gates [skip ci]

### 2026-11-12 17:42 · `9a52b03` · Record 99.36% tightening of archived-law all-warp interval, preserve global status [skip ci]

### 2026-11-12 17:41 · `35acbde` · Restore code markup while retaining exact mathematical LaTex [skip ci]

### 2026-11-12 17:41 · `fcce530` · Repair mathematical markup in tightened all-warp hand proof [skip ci]

### 2026-11-12 17:40 · `c9f012f` · Prove all-warp orbit ceiling within 4.905e-5 of certified lower response [skip ci]

### 2026-11-12 17:39 · `f1fc78b` · Independently verify 11,830 capture times and exact all-warp ceiling [skip ci]

### 2026-11-12 17:37 · `f21b95d` · Freeze tighter 35-route exact all-common-warp ceiling at 1.417638883192751 [skip ci]

### 2026-11-12 17:32 · `673cb19` · Add finite all-warp bank LP and global canonical Monster separation for discovery [skip ci]

### 2026-11-12 17:22 · `4986404` · Handoff all-warp certificate and keep full-game closure gates open [skip ci]

### 2026-11-12 17:22 · `28b9a7c` · Handoff all-warp certificate and keep full-game closure gates open [skip ci]

### 2026-11-12 17:22 · `1f9952d` · Record complete all-warp family ceiling without marking saddle closed [skip ci]

### 2026-11-12 17:21 · `9671e82` · Prove all-continuous-warp ceiling with 13 physical Monster routes [skip ci]

### 2026-11-12 17:20 · `83f5b63` · Verify all-warp ceiling by exact BigInt step envelope and 16-bin cross-check [skip ci]

### 2026-11-12 17:18 · `31d3d59` · Certify a 13-route mixture for all monotone common-coordinate warps [skip ci]

### 2026-11-12 13:37 · `a42e2ff` · Certify 16-knot lower warp no-go by 5408 exact captures [skip ci]

### 2026-11-12 09:55 · `0548158` · Identify the infinite-turn renewal hierarchy [skip ci]

### 2026-11-11 23:11 · `b87cdea` · Prove effective fan responses and global selector synthesis [skip ci]

### 2026-11-11 22:31 · `2c0636c` · Close local fan prefixes and certify a full basis exclusion [skip ci]

### 2026-11-11 21:41 · `0bdaa1c` · Prove finite fan center continuations and exact static tails [skip ci]

Add a future-independent center merge, a finite whole-diamond partition, and a complete stationary-tail breakpoint theorem with an exact dynamic program. Preserve early/middle field attachment, stronger arbitrary-prefix moment envelopes, and verified fixed-interval fan scoring. Initial-prefix closure and a matching global saddle remain open.

### 2026-11-11 21:02 · `e4453d1` · Certify terminal center and arbitrary first-prefix regions [skip ci]

Prove all-record late exterior equality, high-record rank removal, and the complete low-record first-center exclusion. Preserve fixed-tail initial reduction, exact rejection matrices, verified native workers, and the immutable 349-path exchange checkpoint. Full unrestricted saddle remains open.

### 2026-11-11 20:06 · `d223c44` · Close affine center continuation and preserve exact frozen strategy exchange [skip ci]

### 2026-11-11 18:52 · `45ed8e5` · Solve affine center chains and preserve exact avoided-center construction tools [skip ci]

### 2026-11-11 17:41 · `917c8cd` · Prove center imbalance renewal and preserve exact geometry audits [skip ci]

### 2026-11-11 17:23 · `8404810` · Render certified strategy values by exact rational long division [skip ci]

### 2026-11-11 17:20 · `2080d8c` · Certify explicit strategy-pair regrets and preserve global response recovery [skip ci]

### 2026-11-11 16:49 · `cc81521` · Construct both strategy searches and certify the improved upper law [skip ci]

### 2026-11-11 16:09 · `cfb51d0` · Construct a rational monster law and certify its unrestricted best response [skip ci]

### 2026-11-11 15:41 · `4537fe6` · Exclude the full diffuse corridor family and refocus global proof closure [skip ci]

### 2026-11-11 15:37 · `632e1cf` · Optimize full finite monster banks and certify unrestricted epsilon responses [skip ci]

### 2026-11-11 15:30 · `2a8b53d` · Certify exact response faces and the high-start post-turn Bellman gate [skip ci]

### 2026-11-11 15:14 · `0e951c0` · Audit finite-reduction gate: absorbed turn obstruction and exact Bellman checks [skip ci]

### 2026-11-11 14:25 · `2e2fe3b` · Add global survival cuts and exact continuum response cells with independent recovery checks [skip ci]

### 2026-11-11 13:02 · `7fc6bf6` · Construct endpoint obstacles and certify continuous return and incoming-repair gates [skip ci]

### 2026-11-11 11:35 · `53d2114` · Audit free inward turns, corner obstructions, and repeated returns [skip ci]

### 2026-11-11 10:55 · `144c556` · Add curved phase identities and require productive free second turns [skip ci]

### 2026-11-11 09:51 · `fef619f` · Exclude ordinary initial tails and add complete inward-response constructions [skip ci]

### 2026-11-11 09:13 · `95bd8b4` · Prove ordered prefix reductions and test analytic tail attachment [skip ci]

### 2026-11-11 08:42 · `3d3b0da` · Add full CDF attacks, exact repairs, and signed M3 density law [skip ci]

### 2026-11-11 06:58 · `6125e80` · Add two-sided turn identities and global signed Bellman certificate [skip ci]

### 2026-11-11 06:34 · `525333b` · Add turning-density response certificates and endpoint integral system [skip ci]

### 2026-11-11 00:33 · `719dca4` · Exclude signed-density candidate with an exact all-path certificate [skip ci]

### 2026-11-10 23:45 · `05aa56d` · Prove finite ordered-law response reductions and exclude one-sided M1 candidates [skip ci]

### 2026-11-10 22:48 · `adb5084` · Prove conditional response reduction and sharpen exact interval bounds [skip ci]

### 2026-11-10 22:26 · `fb81943` · Derive continuum certificate tests and disprove the wait-in-out reduction [skip ci]

### 2026-11-10 22:11 · `713460a` · Audit continuous response reductions and exclude universal turn cutoffs [skip ci]

### 2026-11-10 21:52 · `c3dd561` · Record complete passing verifier runs in status ledger

### 2026-11-10 21:50 · `03efea1` · Add binary flow certificates and full research snapshot archive

### 2026-11-10 21:49 · `1be127b` · Import uniform finite reduction code, exact grid test, and search logs

### 2026-11-10 21:49 · `2a9d134` · Import five proof packages, verifiers, and roadmap as readable sources

### 2026-11-10 21:48 · `317ca0e` · Add precise research status and verification ledger

### 2026-11-10 21:42 · `e251fb6` · Fix exact monster-response proof import

### 2026-11-10 21:38 · `d446ad5` · Archive six research proofs and exact-response reductions

## A local commit never pushed

Applied to `packages/interval_continuous_lower` in this folder.

### 2026-11-13 21:30 · `9ff1706` · perf(discovery): promote continuous routes by exact activity

[skip ci]
