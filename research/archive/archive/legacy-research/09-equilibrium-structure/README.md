# Structural work toward a matching interval equilibrium

The target of this continuation is a closed unrestricted saddle proof.
Numerical computation is used to identify or reject strategy geometry, not
to produce successively narrower intervals as the deliverable. No matching
equilibrium has yet been constructed.

## An exhaustive response mechanism for a specified princess law

The following chain removes unbounded monster complexity for an explicitly
stated class of ordered laws. It is conditional on the proposed law's
parameters and density pieces, not a theorem that an optimal law belongs
to the class.

1. [Ordered multi-leg CDF](ORDERED_MULTI_LEG_CDF.md) gives an exact lattice
   formula for the radial distribution of alternating inward/outward paths,
   including endpoint absorption, and bounds radial rank reversals.
2. [Separated three-leg responses](FINITE_MONSTER_RESPONSE.md) proves a
   two-turn reduction when the paths stay separated from the center.
3. [Center return reduction](CENTER_RETURN_REDUCTION.md) handles genuine
   central waiting mass. An explicit density-kernel condition replaces
   sufficiently local zero-return triangles by waiting at zero.
4. [Multi-leg finite response](MULTI_LEG_FINITE_RESPONSE.md) extends that
   argument to k inward waves. The safe class uses at most
   `sum_j J_j + 3k` zero-return triangles, finitely many initial capture
   turns, zero waits, and an endpoint completion by time six.
5. [Finite quadratic certificates](FINITE_QUADRATIC_CERTIFICATE.md) proves
   that a rational piecewise-affine law in this class has a finite exact
   unrestricted response certificate. All capture regimes, including
   equality faces, reduce to rational quadratic minimizations on rational
   polytopes. The minimizing value and an attaining route are rational.

The [continuous-rank evaluator](../../packages/interval_continuous_rank/)
integrates a specified monster payoff using exact rational CDF records.
It supports three, five, and finitely many alternating princess legs.
It evaluates routes; it does not yet enumerate the entire quadratic
arrangement or certify an equilibrium.

## Candidate exclusions and the next support geometry

[The free suffix strip exclusion](SUFFIX_GAP_EXCLUSION.md) rules out the
previous positive-M1-tail/M2 candidate class, including arbitrary M2
measures and arbitrary princess responses. A quantitative path exchange
forces a restriction on every near-best response. Nearby reflected
monster sweeps then exploit that restriction, and finite-row minimax
converts the obstruction into a strict improvement of the candidate law.
The order of the concentration and monster-shift limits is explicit.

[Synchronized incoming obstruction](SYNCHRONIZED_INCOMING_OBSTRUCTION.md)
also rules out the tempting repair in which all incoming characteristics
concentrate just above one. It is a direct analytic response bound for
that family, not an inference from an unsuccessful optimization.

The next candidate must include a different support geometry. Negative
M1 starts near an endpoint and monster turns off the common `U=1` line
are concrete directions. The bounded computations in
`packages/interval_turn_curve_discovery/` and the continuous-rank package
are discovery aids. Floating LP values, local fits, and incomplete response
searches are not unrestricted certificates.

## Signed support and the remaining turning-point obstruction

[The signed-M1 response theorem](SIGNED_M1_SUFFIX_REDUCTION.md) includes
negative M1 starts. Three monotonicity conditions reduce every princess
response to four scalar parameters; the suffix argument uses opposite
Chebyshev monotonicity and does not require a convex threshold tail.
[Exact functional derivatives](SIGNED_M1_FUNCTIONAL.md) and a
[conditional primal-dual system](SIGNED_PRIMAL_DUAL_SYSTEM.md) record the
equations and the active-boundary inequalities separately.

That system is not a matching candidate. A
[shifted turning characteristic](SHIFTED_CHARACTERISTIC_RESPONSE.md)
attacks the canonical positive-extra-leg responses. The
[free-turn stationarity equations](FREE_TURN_STATIONARITY.md) describe
what an additional monster support would have to satisfy. Flat score
regions and singular lower-path limits still require their own treatment.

[The arbitrary-path negative-M2 shift](NEGATIVE_M2_SHIFT.md) supplies an
exact identity and a global cap lemma for the late first-inverse traces.
It gives whole-law exclusions under stated strict-localization hypotheses,
including a local mixed-active-set version using four monster laws. These
arguments control arbitrary near-best paths rather than substituting
selected canonical representatives.

[The exact local scalar certificate](LOCAL_SCALAR_GAP.md) completes that
obligation for the rationalized signed-density discovery law. It maximizes
946 closed rational quadratic cells, proves the required local gap, and
instantiates an explicit four-law monster mixture with a strictly smaller
response ceiling against every princess path. The result excludes this
fixed signed candidate; it does not exclude the whole signed-support class
or determine the game value. Independent direct-capture integration checks
the actual rational law's scalar payoff limits.

Two bounded five-leg fits also failed explicit
[first-wave](FIRST_WAVE_TWO_TURN_RESPONSE.md) and
[last-wave](LAST_WAVE_TWO_TURN_RESPONSE.md) two-turn attacks. Their second
incoming characteristics were confined just above one. These are
diagnoses of those fits, not an exclusion of every finite-wave law.

The [independent wave audit](TWO_TURN_WAVE_AUDIT.md) checks both formulas by
integrating direct segment intersections. A
[finite-last-wave counterexample](FINITE_LAST_WAVE_COUNTEREXAMPLE.md)
shows that a final wave can support a strict interior optimal turn at a
fixed start. The [joint start/turn equations](LAST_WAVE_STATIONARITY.md)
retain both moving prefix fronts; in the stated high-rank regime, a smooth
minimizing turn curve must increase with the distance of the start from
the center. These are necessary support conditions, not a constructed
equilibrium.

An [exact no-extra-family test](../../packages/interval_no_extra_family/)
also preserves an unsuccessful exclusion attempt. Its rational ceiling
remains above the known unrestricted lower guarantee, so it does not
decide the viability of that two-parameter princess family. It identifies
useful earlier monster turns without turning its restricted result into a
claim about the full value.

## Review status

The finite response chain and suffix exclusion have received internal
independent mathematical review. Exact Python fixtures check characteristic
capture formulas, CDF integration, and boundary discontinuities. No Lean
compilation, CI, or external peer review is claimed. Gates G5-G8 remain
open until an actual matching pair or uniformly approaching lower family
has been identified and proved against both unrestricted strategy spaces.
