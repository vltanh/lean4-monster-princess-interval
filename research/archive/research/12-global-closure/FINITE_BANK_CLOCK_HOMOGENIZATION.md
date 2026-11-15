# Exact finite clock-and-matching LP for a finite unit-speed Monster bank

Date: 2026-11-13. Exact finite-bank reduction and verified continuous certificate.

**Theorem:** the construction is exact for a finite reflection-closed
bank of polygonal Monster paths whose nonconstant scored legs all have
speed exactly one, with no positive-duration waits. It gives an exact
finite LP for the best mixture and causal clocks on that bank. It does
not prove that an unrestricted optimum belongs to a finite bank.

## 1. Finite path geometry

For each oriented path \(m_i\), truncate its scored portion at
\(\tau_i=\inf\{t:m_i(t)=-1\}\). Use both reflected orientations, with
probabilities \(w_i\ge0\), \(\sum_iw_i=1\), and
\(w_{\bar i}=w_i\).

Write \(U=t+x\), \(V=t-x\). A unit-speed physical leg is a horizontal
or vertical light-coordinate segment. Let \(K=\{k_0<\cdots<k_R\}\)
contain both light coordinates of every vertex of every truncated path.
Additional knots may be inserted without harming the argument.

Split each leg wherever its free light coordinate crosses a knot of
\(K\). The resulting physical cells are:

* knot points, with both \(U,V\in K\);
* open sublegs, with one coordinate equal to a knot and the other
  ranging over one entire consecutive open band \((k_j,k_{j+1})\).

The sign of \(x=(U-V)/2\) is constant on each open cell. Center events
are knot points. Arena endpoint events are vertices, hence knot points.
There are no scored open endpoint cells under the unit-speed hypothesis.

## 2. A common random monotone collapse

Independently for each open band \(I_j=(k_j,k_{j+1})\), choose
\(Z_j\) uniformly in \(I_j\). Define \(T\) to fix every knot and to
send every point of \(I_j\) to \(Z_j\).
It is nondecreasing, and it preserves all strict comparisons between
a knot and an interior point of a band.

Apply the same \(T\) to both light coordinates of every event in:

1. the joint path/scoring-time/selected-history measure;
2. the positive/negative pressure matching.

Each transformed event remains on its original physical path, because
one coordinate of its leg is fixed at a knot and its free coordinate
remains in the same subleg band.

Both \(U_i(t)\) and \(V_i(t)\) are nondecreasing along a legal path.
Thus selected-time causality

\[
 U_i(s)\le U_i(t),\qquad V_i(s)\le V_i(t)
\]

is preserved. After transformation the selected event is still no later
than the transformed scoring event on that same path.

On a unit-speed subleg the free coordinate changes at rate two.
The scoring measure \(dt\) is therefore one half of Lebesgue measure
in that free coordinate. Collapsing it to \(Z_j\) and averaging over
\(Z_j\) returns precisely the same scoring measure \(dt\).
Consequently the averaged transformed joint measure is a legal causal
clock kernel for the unchanged physical path law.

Every selected mass in an open cell becomes uniform in that cell.
Knot atoms stay fixed. This conclusion concerns the selected marginal;
the joint selected/scoring distribution need not be uniform or
independent. The existing conditional quantile compression can restore
a deterministic nondecreasing backward clock without changing that
selected marginal.

## 3. Matching is preserved, including contact equalities

For a positive physical point \(p\), write \(U_p>V_p\).
For a negative physical point \(n\), write \(U_n<V_n\).
The radial causal matching condition is exactly

\[
 U_n\le V_p,\qquad U_p\le V_n,
\]

equivalently, the negative interval \([U_n,V_n]\) contains the
positive interval \([V_p,U_p]\).

The common nondecreasing map \(T\) preserves these two inequalities.
It also preserves the signs of the events because every point has at
least one light coordinate at a fixed knot. No positive or negative
pressure is converted to center pressure, and no interior selected
event becomes an endpoint event.

Therefore matching mass, total active mass, and total positive pressure
mass are unchanged. The objective \(M+\mu_+(X)-|\pi|\) is unchanged.
This proves that an optimal fixed-bank certificate has a representative
in the finite atom/uniform-cell templates.

The common map is essential. Independent coordinate perturbations would
not preserve matching. A deterministic midpoint collapse alone would
not preserve the physical scoring measure \(dt\).

### Canonical clock for an endpoint sweep

The implementation fixes the descending fast sweep's clock to current
time. This is without loss even before homogenization. For every legal
radius \(r\), the two functions
\(1-s-r(s)\) and \(1-s+r(s)\) are nonincreasing. Their strict-positive
indicators are therefore nonincreasing, including at contacts.
At every scoring time \(t\), current time minimizes

\[
 \Phi(r(s),1-s)
 =\mathbf1_{\{1-s>r(s)\}}+\mathbf1_{\{1-s>-r(s)\}}
 \quad\text{over }0\le s\le t.
\]

Replacing any sweep clock by current time cannot increase its plane
against any legal Princess radius. Its reflection starts at \(-1\)
and has zero active lifetime. The current sweep occupation is already
uniform in every open light-coordinate cell.

## 4. Exact clock constraints in finitely many variables

For path \(i\), write its ordered knot times as

\[
 0=t_{i0}<t_{i1}<\cdots<t_{iL_i}=\tau_i.
\]

Use variables \(A_{ij}\ge0\) for weighted selected mass at \(t_{ij}\),
and \(B_{ij}\ge0\) for weighted selected mass uniformly distributed
over \((t_{ij},t_{i,j+1})\).
These are unconditional masses, already including \(w_i\).

The total-mass constraint is

\[
 \sum_{j=0}^{L_i}A_{ij}+
 \sum_{j=0}^{L_i-1}B_{ij}=w_i\tau_i.
\]

Causality is equivalent to
\(\eta_i([0,t])\ge w_it\) for every \(0\le t\le\tau_i\).
For this template, it is exactly equivalent to the finite inequalities

\[
 \boxed{
 \sum_{r<j}A_{ir}+\sum_{r<j}B_{ir}\ge w_i t_{ij},
 \qquad 1\le j\le L_i.}
\]

These are the left limits at the knots. Between knots the difference
between the selected prefix mass and \(w_it\) is affine, so its minimum
is at an endpoint. Atoms only increase that difference.
The final inequality and total-mass equality force
\(A_{iL_i}=0\), correctly excluding selected mass at the first
\(-1\) visit. A path with \(\tau_i=0\) has no selected mass.

Conversely, these inequalities give a causal selected-history measure.
For \(w_i>0\), normalize it by \(w_i\), take its increasing quantile
clock on \([0,\tau_i]\), and obtain \(s_i(t)\le t\) with precisely
the prescribed occupation measure. Paths of weight zero are harmless.

## 5. Finite matching variables

Aggregate coincident physical cells separately by sign.
The common knot subdivision makes distinct open geometric cells
disjoint; intersections are knot points and carry their own variables.

Represent a uniform open cell by the event whose free coordinate is
the midpoint of its band. Represent a knot atom by its actual event.

**Exact cell criterion:** a positive cell and a negative cell admit a
homogenized matching if and only if their representatives satisfy
interval containment.

For necessity, apply the deterministic common midpoint collapse to
any feasible pair of events. For sufficiency:

* If both cells' free coordinates lie in the same band, use a single
  common uniform coordinate \(Z\). This gives a diagonal uniform
  coupling in the free coordinates.
* If the two free coordinates lie in different bands, use independent
  uniforms. Their relative order is fixed throughout those bands.
* If either cell is an atom, use the corresponding atom/uniform or
  atom/atom coupling.

Each such coupling has exactly the desired cell marginals and is
supported on the causal order. The midpoint is only a finite index
for this exact coupling; it is not a replacement of continuous pressure
by a physical point atom.

There is an especially simple common-quantile realization useful for a
standalone replay. Let \(0<z<1\), map coordinate index \(2j\) to \(k_j\),
and map index \(2j+1\) to \((1-z)k_j+zk_{j+1}\).
This is nondecreasing in the coordinate index for every \(z\).
Thus every indexed interval-containment pair remains a containment pair
pointwise after this map. Averaging uniform \(z\) gives the correct
uniform marginal on every open cell. It works for same-band and
different-band pairs alike. Applied after finite flow decomposition,
it lifts the entire indexed matching network to a continuous measure
coupling without introducing point-mass capture approximations.

One may therefore use variables \(z_{ab}\ge0\) for feasible positive
and negative cell pairs, with

\[
 \sum_bz_{ab}\le\mu_{+,a},\qquad
 \sum_az_{ab}\le\mu_{-,b}.
\]

The aggregate cell masses \(\mu_{\pm,\cdot}\) are linear expressions
in \(A,B\). Center masses contribute to \(M\), but have no matching
source or capacity.

## 6. Complete finite LP and its exact meaning

Minimize

\[
 \boxed{
 \sum_iw_i\tau_i+\sum_a\mu_{+,a}-\sum_{a,b}z_{ab}}
\]

subject to weight normalization and reflection symmetry, the clock
mass and prefix constraints, and the matching constraints above.

Every feasible LP point produces an actual physical Monster mixture,
actual causal clocks, and an actual continuous matching certificate.
Conversely, the common random homogenization maps every feasible
fixed-bank clock-and-matching certificate to a feasible LP point of
the same objective.

The fixed-law strong one-record duality and exact causal matching
theorem then imply that this LP value is exactly

\[
 \min_{\substack{\nu\ {\rm symmetric}\\
                  \operatorname{supp}\nu\subset\{m_i\}}}
 \sup_{p\ {\rm legal}}\mathbb E_\nu T(M,p).
\]

Weights may instead be fixed to compute the exact unrestricted
Princess-response supremum of one supplied finite Monster law.
Princess attainment is unnecessary.

## 7. Sparse interval-containment network

Explicitly listing all positive/negative cell pairs can be quadratic
in the number of cells. A finite order network avoids that.

Let \(S\) be the sorted union of knots and their band midpoints,
of size \(2|K|-1\). Represent an interval by the pair of indices
\((\ell,r)\), \(\ell\le r\).
Make a directed expansion grid with edges

\[
 (\ell,r)\longrightarrow(\ell-1,r),\qquad
 (\ell,r)\longrightarrow(\ell,r+1)
\]

whenever defined. It has \(O(|K|^2)\) nodes and edges.
Connect each positive cell's mass supply to its representative interval
node, and connect each negative cell's representative interval node
to a sink with its mass as capacity.
Internal edges have no effective upper bound.

A source interval reaches a negative interval exactly when the latter
contains it. Thus the network's maximum flow is precisely the finite
matching mass. In the joint LP, source and sink capacities are the
linear pressure-mass expressions in \(A,B\). Flow decomposition
recovers a matching of cell pairs; Section 5 realizes it physically.

The grid may contain abstract intermediate intervals that are not
physical cells. This does not matter: it represents order reachability,
not extra Monster trajectories or pressure.

For a very sparse set of cells, a two-dimensional dominance range tree
is an alternative. A positive interval queries negative targets with
left endpoint no larger and right endpoint no smaller. Canonical
range-tree blocks yield \(O(N\log^2N)\) source attachments, with shared
negative target capacity nodes preventing capacity duplication.

## 8. Limitations that matter

* Positive-duration waits and subunit-speed legs are not covered.
  Applying the same \(T\) to their two varying coordinates need not
  keep the event on its physical path. Such a bank requires a separate
  argument or a different exact template.
* Every knot crossing must be retained, including center contacts and
  intersections with knots contributed by other paths.
* Clock prefix constraints must use left limits at knot times.
* Same-band matching requires the diagonal coupling; replacing it by
  independent uniforms can break the order.
* The conclusion is exact for the supplied finite bank, with arbitrary
  Princess paths. It supplies no finite-bank sufficiency theorem for
  the unrestricted Monster strategy space.

## 9. Executed 241-pair application and an independent exact replay

This reduction was implemented for the reweighted 241-pair Monster law
contained in the self-contained certificate
[reweighted_physical_clock_certificate.json.gz](../../packages/interval_global_closure/reweighted_physical_clock_certificate.json.gz).
Its geometry has 482 oriented paths and 203 common light-coordinate knots.
The finite model has 85,268 scored path sublegs, 17,099 positive pressure
cells, 15,401 negative cells, and a pruned order grid with 35,727 nodes.

The numerical LP was used only for discovery. A separate ordinary
integer circulation supplied exact rational values satisfying 153,495
equalities. The construction uses the fact that local backlog balances
replace dense clock-prefix rows, leaving at most two nonzero entries
in each column, each equal to \(+1\) or \(-1\).

For completeness, a column with entries \(s\) at row \(u\) and \(t\)
at row \(v\) is represented on two sheets by arcs
\(u^s\to v^{-t}\) and \(v^t\to u^{-s}\).
Give row \(u\)'s two sheets supplies \(b_u,-b_u\).
Single-entry columns use one common ground node with zero supply.
Averaging paired arc flows recovers the original variable.
Exact rational supplies and bounds become integral after scaling.

All unmatched-positive columns have sole coefficient \(+1\).
Their arcs pass through two mirrored bottlenecks, each bounded by the
exact desired deficiency. This imposes the unmatched-mass budget in
an ordinary feasibility circulation; no numerical objective value is
used as the final upper certificate.

The resulting rational certificate has mass denominator
\(8\,000\,000\,000\,000\,000\,000\,000\,000\,000\).
More importantly, the standalone replay does not trust that construction.
It independently:

* rebuilds the legal reflected physical paths and their common cells;
* checks 85,268 exact clock-prefix inequalities and every pathwise mass;
* verifies source and target capacities, plus 12,214 nonzero expanding
  interval-flow edges and exact flow conservation;
* verifies that all unmatched pressure is a submeasure of the continuous
  current-time endpoint-sweep front.

There are 5,135 matched positive cells and 6,962 matched negative cells.
Only three front cells retain positive mass.
The exact certificate gives

\[
 M=\frac{356499183697229725947074931}
          {250000000000000000000000000},
 \qquad
 d=\frac{9570689369683068933669}
          {4000000000000000000000000000},
\]

\[
 \boxed{
 U=M+d=
 \frac{1140799301969009059644426513}
      {800000000000000000000000000}
 \approx1.4259991274612613.}
\]

Run from the repository root:

    python packages/interval_global_closure/replay_continuum_clock_certificate.py packages/interval_global_closure/reweighted_physical_clock_certificate.json.gz

This replay uses only Python's standard library and the inline path law
in the compressed certificate. It needs no optimizer, saved LP model,
compiled helper, or sampled Princess strategy list. It was executed
successfully and independently replayed by a second agent.

The active one-clock dual and the causal matching identity used here are
proved in [GLOBAL_INFINITE_HORIZON_ACTIVE_DUAL.md](GLOBAL_INFINITE_HORIZON_ACTIVE_DUAL.md)
and [GLOBAL_CAUSAL_PRESSURE_MATCHING.md](GLOBAL_CAUSAL_PRESSURE_MATCHING.md).
The verified front localization enables the further physical continuum
construction in
[ENDPOINT_FRONT_DEFICIENCY_COMPLETION.md](ENDPOINT_FRONT_DEFICIENCY_COMPLETION.md).

No unrestricted Monster finite-support theorem, matching global Princess
lower strategy, exact full-game value, Lean compilation, or Lean kernel
certificate is claimed.
