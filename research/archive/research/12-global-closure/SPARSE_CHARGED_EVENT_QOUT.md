# Exact projection of Qout onto charged clock events

For a supplied centered physical Monster law and fixed causal clocks, its
normalized Princess upper plane depends on only finitely many radial events.
The full uniform spacetime grid is unnecessary for this upper optimization.
This is a projection of the existing Qout order, not a new restriction on
Princess strategies or a finite-bank lower certificate.

## Projected order

Write an event as `(t,r)` with `0<=t<=2` and `0<r<=1`. The full Qout graph
has the ordinary transport implications

\[
 g(t,r)\le g(s,a)\quad\hbox{if } a-r\ge |s-t|,
\]

and endpoint stopping, `g(v,1)<=g(u,1)` for `u<=v`.
Among any selected set of events, the complete reachable relation is

\[
 (t,r)\preceq(s,a)
 \quad\Longleftrightarrow\quad
 a-r\ge|s-t|\quad\text{or}\quad
 \bigl[a=1\text{ and }s\le\min\{2,t+1-r\}\bigr].
 \tag{1}
\]

Ordinary cone moves increase the radius. Once they reach radius one,
endpoint stopping can decrease time but cannot return to an interior
radius. Thus interior-to-interior reachability is exactly containment.
From `(t,r)`, the accessible endpoint times form
`[t-(1-r),t+(1-r)] intersect [0,2]`. Its largest element is
`min(2,t+1-r)`; stopping then gives precisely the second relation in (1).
In the parity lattice all these relevant endpoint times have legal parity,
so the same argument is exact for the discrete graph.

Outward substitution after time two creates no hidden pre-two relation.
A later node `(v,b)` has footpoint `(2,b-v+2)`. For `t<=2<=v`, the cone
inequality `b-r>=v-t` is equivalent to
`(b-v+2)-r>=2-t`, exactly the pre-two cone relation to that footpoint.
Post-two endpoint stopping is already implied by pre-two stopping and
radial monotonicity at time two.

## Exact extension

Given values in `[0,1]` on the selected nodes satisfying (1), define the
value at any omitted node as the supremum of selected predecessor values,
with empty supremum zero. This is an isotone extension and agrees with
every selected value. The selected-node feasible polytope is therefore
exactly the projection of Qout. All integer-valued nodal assignments have
an integer-valued extension on the same denominator.

The implementation fills ordinary cone predecessors, then applies
backward endpoint maxima. No cone edge can leave the endpoint, so this
single endpoint pass is sufficient. Exact integer closure repairs any
floating tolerance before a field is used in discovery. Such a field
still needs complete response pricing before it supplies a Princess lower.

## Sparse construction

In light coordinates `u=t+r`, `v=r-t`, containment means coordinatewise
order. For each source, scan successive increasing `u` groups. In each
group select the smallest eligible `v`; retain it only if it is a new
strict record low. These are precisely its minimal containment successors.
Add the chain of decreasing endpoint times and, for each source, its
latest eligible selected endpoint under (1). The resulting graph has
exactly the required reachability. Its worst-case size need not be linear;
the present computation makes no general sparsity complexity claim.

The floating master retains an IPM crossover basis and appends newly
charged variables, order inequalities and physical calendar rows. Old
order edges remain valid as nodes are added. All mixture weights are
rationalized and independently certified before any upper is retained.

## Certificate acceptance does not trust graph completeness

For integer signed event coefficients `c`, baseline `M`, and positive
total `P`, a feasible source-to-sink flow `F` through valid Qout edges
gives the upper `M+P-F`, with the usual physical scale. The sparse replay
checks physical unit-speed paths, both causal clocks, every supplied edge
against (1), capacities, conservation, and an equal-value cut.

Even if a graph-construction bug omitted a valid implication, it could
only enlarge the maximizing field class and weaken the resulting upper.
An invalid added implication could strengthen an upper unsafely; this is
why the independent integer replay checks every edge's geometry directly.
No floating LP optimality assertion is part of acceptance.

On the retained n128 law, the projected graph has 21,139 nodes and 83,882
arcs and reproduces exactly the existing upper
`145925593551091/102400000000000`, with flow and cut both
`93007371780317`. The original full graph has 65,666 nodes and 151,953
arcs. This is a verified computational reduction, not a new game bound.

The relation and extension have an independent mathematical review and
559,500 finite pair comparisons, 96 integer extension checks, five
independent full/projected LP comparisons, and three persistent-model
node/calendar update checks. These are manuscript and computational
results, not a Lean formalization.
