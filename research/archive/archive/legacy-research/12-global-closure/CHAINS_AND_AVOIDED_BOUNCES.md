# Exact center chains and avoided-center construction

## Status and purpose

The unrestricted interval game is still open. This continuation preserves exact
components needed by a global certificate and tests a different lower-strategy
construction. A smaller numerical interval is not treated as closure.

The current exact guarantees are
\[
 \frac{36290299773897097}{25600000000000000}
 \le V\le
 \frac{57045189772271291487410009}{40000000000000000000000000}.
\]
The upper fraction is one frozen strictly increasing coordinate update of the
previous 280-pair law. Its exact integer flow/cut certificate and physical
response were independently replayed. The lower fraction is unchanged. The
earlier explicit-pair regret calculation concerns the unwarped upper law and
has not been relabeled as a regret calculation for this update.

No Lean compilation or CI was run. The computational bodies described below
were executed in the portable V8 runtime; their Node filesystem wrappers were
not invoked during the native executor outage.

## 1. The center-return component now has an all-count solution

The center imbalance theorem reduces a symmetric ordered radial law to
\[
 J(t,r,n)=\frac12\int_r^n\beta_t(q)\,dq+V(t,n),\qquad
 W(t,n)=V(t,n)+T_t(n)/2.
\]
Thus a completed return need not retain the entire preceding monster path.
The earlier theorem already includes arbitrary legal continuations and
accumulating turns.

For an affine incoming cell \(R(U,V)=kU-\ell V+c\), put
\(d=k-\ell\), \(z(t)=dt+c\), and \(r=\ell/k<1/8\).
The associated Riccati parameter is
\[
 \theta=\frac{1-\sqrt{1-8r}}{1+\sqrt{1-8r}}.
\]
A productive chain with excursion lengths \(h_1,\ldots,h_m\), beginning on
the center front and with its final return prescribed at the slab boundary,
has a quadratic energy plus explicit negative hinge corrections. These
corrections cannot simply be omitted. The new sorting proof absorbs them
into the decrease of the quadratic when the excursion lengths are arranged
in increasing order.

The resulting convex problem has a tridiagonal Hessian. Its exact KKT
solution selects a finite number of productive excursions until the
available duration reaches
\[
 H_*=\frac{3\theta}{1-\theta}.
\]
The count thresholds increase to \(H_*\). Beyond that threshold a geometric
infinite chain gives the exact infimum of this component. This closes the
prescribed-final-return optimization for every turn count; it does not
justify moving an arbitrary last return to the slab boundary.

The chain identities also retain the terminal linear hinge, productive waits,
and non-front resets. An explicit rational counterexample defeats the
earlier one-crossing potential. The independently replayed front solution
has 6,072 exact checks, including direct affine rank-primitive moments,
sorting and hinge comparisons, KKT conditions, support thresholds, and
geometric limits.

Sources:

- [Exact chain and reset identities](../10-turn-density/AFFINE_CENTER_CHAIN_IDENTITIES.md).
- [All-count convex solution](../10-turn-density/FRONT_CHAIN_QUADRATIC_SOLUTION.md).
- [Front-chain verifier](../../packages/interval_turn_sheet/verify_front_chain_quadratic.cjs).

## 2. Last crossing is an actual exterior envelope

For the saved piecewise affine field, every last crossing from the final
incoming slab has a finite exact envelope. The analysis retains the outgoing
cells after the nominal boundary, the inverse-integral breakpoints, the
closed endpoint jump, and waits. A last return after the constant-row cap
is dominated by the cap, while the endpoint route remains a separate branch.

The full inverse-model comparison proves that an affine Riccati polynomial
can remain an internal subsolution even when a later inverse leaves its
local affine cell. The transformed potential must use the actual inverse
moment \(T_{\rm actual}\). This comparison alone does not attach the
potential to all exits.

The independent replay checks six states over 368 exact quadratic intervals,
736 quarter-point comparisons and 368 independent moment identities. The
source also audits the full future cone, outgoing model comparison, and
closed endpoint gate. The separate global attachment problem remains open.

See [the complete last-crossing envelope](../10-turn-density/CENTER_LAST_CROSSING_ENVELOPE.md).

An unconditional reachable-defect construction now attaches any verified
internal subsolution to a complete exit envelope. It takes the infimum of
the exit defect over a nested reachable-state relaxation. The construction
is a lower potential, and does not assert that the relaxation is attained.
Independent replay of the complete saved-field example checks 3,135
quadratic crossing polygons and 7,479 primitive identities. The earliest-hit
base and single-pair base give weak values at the tested state; neither
closes the center value or repairs the field's known attacks.

See [the attachment theorem and exact diagnostic](../10-turn-density/CENTER_REACHABLE_DEFECT.md).

## 3. Complete declared warp families expose a missing early attack

A common strictly increasing map of both light coordinates preserves all
capture orders and bijects legal paths. It gives a useful exact geometry
variation, but a finite set of active attacks is not enough to certify a
lower law.

The coefficient compiler now covers 301 early-family cells and 3,502 late
edges. Both complete tensors were independently regenerated, including
129,302 rational basis/quarter comparisons and 907 separate identity
feature comparisons. Their serialized Git blob hashes agree with the
saved tensors. All five reported family minima were also evaluated by
independent physical capture formulas.

The saved five-family optimum is rejected by a positive-start early-turn
route. Its exact cost is
\[
 \frac{181988419226356214104426769}
      {128000000000000000000000000}
 =1.421784525205908\ldots .
\]
This is an attack on that supplied candidate, not a new game guarantee.

For a general same-side prefix ending at its first center time \(s\), with
captured radial rank \(M\), the exact total cost is
\[
 G_\sigma=W(s,M)+\frac12\int_0^M\tau_q^\sigma\,dq.
\]
The negative-side center moment cancels with the imbalance correction.
Consequently the unresolved prefix problem is the captured-rank first-hit
moment coupled to the center potential. No fixed turn family is declared
exhaustive.

See [the full warp quadratics](WARP_RESPONSE_QUADRATICS.md) and
[the early-prefix coupling](WARP_EARLY_CENTER_COUPLING.md).

## 4. A frozen upper law and the obstruction on its exact response face

The new [upper package](../../packages/interval_common_warp/README.md)
retains the 280 probabilities and changes only the common light-coordinate
map. All 68 stored increments are positive and sum to one. The projected
integer graph has 59,593 nodes, 177,126 arcs and 104,598 positive flow entries.
Independent replay verifies every capacity, every conservation equation,
the matching cut, both exact extremal payoff rows, and all 560 oriented
physical captures.

The two extremal response profiles require isolated avoided-center bounces.
Replacing such a bounce by a literal contact changes capture order.
Furthermore, the complete exact response face has a common inexpensive
monster attack, justified by its priced query gates. Therefore that exact
face is not an unrestricted lower strategy.

Rounding a finite optimizer can make its exact optimal face much smaller
than the collection of nearly optimal responses. The face obstruction does
not exclude every approaching lower construction.

See [the face geometry and its qualifications](../../packages/interval_common_warp/CENTER_AVOIDANCE_FACE.md).

## 5. Infinitesimal avoidance changes the adaptive response

For \(0<\tau<1\), consider the equally weighted reflected pair generated by
\[
 p_\epsilon(t)=\min\{1,\epsilon+(1-\epsilon)|t-\tau|\}.
\]
Its unrestricted adaptive-monster response is exactly
\[
 \frac{1+\epsilon+(1-\epsilon)\tau}{2}.
\]
A literal zero-touching limiting path instead has response \(\tau/2\).
The discrepancy tends to \(1/2\). The proof controls all first hits and the
earliest possible opposite-sign hit; a straight sweep attains the bound.
An atomless time-jitter version has the same limiting phenomenon.

This example has value at most one and is not a proposed equilibrium.
Its role is to show why a lower law cannot be reconstructed by taking the
pointwise limit of its response labels. An infinitesimal center plateau
and an actual reversal before zero can have different adaptive values even
when the same limiting priced queries are met.

See [the exact avoided-bounce example](AVOIDED_CENTER_BOUNCES.md).

## 6. Exact rational-function search and limit-only pruning

The existing complete finite-law capture-order oracle has been lifted to
the ordered field \(\mathbb Q(\epsilon)\). Its 6,318-character search core
is unchanged. Polynomial signs are decided by the first nonzero coefficient,
and every comparison contributes an explicit positive radius on which its
decision is valid. Division and equality checks also register their
denominator/sign guards.

The independent adapter replay covers six fixtures in raw and sorted modes:
twelve pruned/unpruned exact searches, rational specialization below the
common radius, and independent segment or running-record capture checks.
The saved report agrees in full. It reaches degree 24 and records a common
radius \(1/96\) for those fixtures.

A separate adapter changes exactly one objective-bound pruning gate.
It may prune a node when the limit of its admissible lower bound is at
least the current witness limit. It retains the complete rational bound.
All arrival times, contacts, geometry and Pareto comparisons remain exact.

When the finite search completes, the minimum of the retained lower
bounds and the final witness is a uniform lower function; the witness is
an upper function. Their limits agree. This certifies the limiting response
of the supplied law even if their linear terms differ. The adapter passes
the twelve standard regressions and two deliberate tests with
\[
 L_*=\tfrac12-\tfrac13\epsilon,\qquad
 B_*=\tfrac12+\tfrac13\epsilon.
\]
It correctly reports a limiting optimum of \(1/2\) and does not claim the
full germ optimum. An interrupted search remains only an attack witness.

See [the limiting-search proof and interface](../../packages/interval_global_closure/ASYMPTOTIC_CAPTURE_SEARCH.md).

## 7. Remaining closure work

The candidate now being investigated comes from the actual 159-row
probability-master dual of the full 1,086-column bank. The unrelated
36-control coordinate-warp dual has an exact adaptive attack near 1.070313
and is rejected as a lower law.

The full-bank candidate needs a legal approaching realization, complete
adaptive monster response, and a matching upper certificate. In particular,
the connector between limiting query labels must preserve isolated
center avoidance without introducing a slower near-center plateau that a
monster can exploit. The new connector and full candidate search are
separate from the completed results above.

The center exterior attachment and arbitrary same-side prefix problem
also remain available analytic routes to a lower certificate. None of
these outstanding obligations is replaced by a numerical finite-bank
score, an incomplete search, or a further interval refinement.
