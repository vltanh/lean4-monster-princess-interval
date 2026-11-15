# Exact elimination of unpriced event thresholds

The finite atomic response engine introduces a threshold variable
`x(i,k)` for the event-control predicate `P(V_i) >= label_k`. The full event
grid contains many variables that do not occur in any payoff reward. They can
be eliminated exactly before either maximum flow or the joint probability-law
LP is solved. No monster coordinate, princess control, or payoff coefficient
is rounded in this reduction.

## The induced order

The common label set is ordered globally. Its threshold implications are

\[
x(i,k)\le x(j,l)\quad\text{whenever}\quad i\le j,\ k\ge l.
\]

The formula holds for Boolean threshold selections and for inclusion
probabilities in the associated order polytope. Physical bounds force the
variables with `k<=lo(i)` to one and those with `k>hi(i)` to zero. Both `lo`
and `hi` are nondecreasing in the event index.

Let `S` be precisely the variable thresholds appearing in at least one
nonzero reward of the supplied library. Every assignment to `S` that obeys
the displayed dominance implications extends to the full event grid. Its
least extension is

\[
x_{\min}(i,k)=\max\left(\mathbf1_{k\le lo(i)},
 \sup\{x(j,l):(j,l)\in S,\ j\le i,\ l\ge k\}\right),
\]

where the supremum of the empty set is zero and the prescribed zero values
above `hi(i)` are retained. No priced predecessor can violate that upper
bound: `j<=i` implies `hi(j)<=hi(i)`.

At a priced node, the expression equals its specified value by the induced
order. It is nondecreasing in the event index and nonincreasing in the label
index, so it is a legal extension. The greatest extension is obtained from
the corresponding infimum over priced successors, with empty infimum one
and the same forced bounds. Thus the projection of the full order polytope
onto `S` is exactly the induced dominance-order polytope.

Since every reward depends only on nodes in `S`, this preserves every atom's
payoff simultaneously. It therefore preserves the response supremum for
every probability law and the optimum of the joint law/flow LP.

## Sparse predecessor construction

`project_order.py` processes event rows from left to right, and used thresholds
within a row from high labels to low labels. For each label it stores the most
recent used node at that label. When adding `(i,k)`, it scans labels `l>=k`
and adds a predecessor edge only when the stored event index is a new record
high. The scan stops when a previously processed node in row `i` is reached.

Every added edge is a valid dominance implication. Conversely, take any old
node with event index at most `i` and threshold at least `k`. Replace it by the
latest node at its threshold. If that latest node is not a record during the
scan, an earlier scanned threshold has a later event index and is a successor
of it. That record node has an edge to `(i,k)`. Induction gives the desired
path. A same-row record covers all remaining larger labels, which justifies
stopping there. Hence the graph has exactly the required reachability.

The scans for consecutive used thresholds in a row cover disjoint label
intervals apart from their common endpoints. The procedure therefore avoids
building all pairwise dominance edges.

## Retaining the full response face

The minimum extension is a convenient representative, not the complete
optimal response face. Unpriced variables may occupy the entire order-polytope
fiber between the least and greatest extensions. These degrees of freedom
must be restored when constructing a lower law or distributing contact layers.

`projected_cut.cjs` returns the least full-grid extension of the least optimal
priced cut and the greatest full-grid extension of the greatest optimal priced
cut. Both are checked by the original rational first-capture evaluator. The
remaining fiber still carries all monotone completions; it is not replaced by
a finite mixture of those two extremal paths.

As in the underlying event theorem, these are limiting response controls.
Passing from that face to an attained or uniformly near-optimal lower law
against every monster remains a separate obligation.

## Checks and measured reduction

The deterministic verifier in `project_order.py` performs 62,087 exact
reachability comparisons on 120 small generated dominance posets. It compares
the projected graph to the defining pairwise order, not to the implementation's
scan rule.

`verify_projected_cut.cjs` is a portable independent comparison using the
repository's certified 67-atom law, mixtures with explicitly supplied genuine
initial-inward and late-turn atoms, and a single center-M3 atom. All four
projected cuts agree with the original event oracle in the displayed numeric
values, and both extremal policies are rescored by rational physical
first-capture formulas. Run it from its installed package with Node; a
`--strategy` argument can specify the certified strategy JSON elsewhere.

A separate native-state replay compared the certified law, the solved 179-atom
law, their equal mixture, and a center-M3 atom on the entire 468-atom event
arrangement. Its largest difference was `9.71e-14`. These numerical flow
comparisons are not exact capacity certificates. The 62,087 poset comparisons
can be rerun independently with `python project_order.py --verify-only`.

On the current 468-atom library, priced threshold nodes decrease from 80,274
to 23,080. The projected order has 45,541 edges. Reward definitions and all
their coefficients are unchanged. On the separately named intended-grid
library the corresponding counts are 78,669 to 22,814, with 45,013 edges.
