# Finite center continuations and exact stationary tails

Date: 2026-11-12 UTC.

The unrestricted interval game remains open. This checkpoint proves complete
structural reductions for specified classes of continuations. It also gives
an exact evaluator for a stationary tail. It does not supply a matching
global lower/upper strategy or a new interval-game bound.

## 1. An exact stationary-tail theorem and evaluator

Suppose all remaining targets are stationary after time \(h\), with a bounded
piecewise constant signed spatial density and finitely many atoms. Let \(D\)
contain the arena endpoints, all density-cell endpoints and all atom
positions, and let \(K=|D|\). An optimal continuation from any current Monster
position has productive turns only in \(D\), with no boundary productive twice.
It can be completed by time \(h+2(K+1)\).

The key local calculation varies one productive right turn \(y\), keeping
the neighboring and later spatial turns fixed. Within a density cell of
signed density \(\beta\), the latency contribution satisfies
\[
 C''(y)=-4\beta\le0.
\]
An interior turn can therefore be moved to a density boundary, an atom, or
a collision with an existing record. Closed atom contacts lower the cost;
a collision removes an empty excursion. Iterating gives the finite route
class. Arbitrary infinite histories are covered by explicit truncation,
endpoint completion and bounded-density interpolation that retains all
atom first hits.

This corrects a tempting but false shortcut: stationarity alone does not
make a direct tour of the remaining extremes optimal. Interior high-mass
points can be visited before tiny endpoint tails. The finite-boundary
theorem retains exactly those alternatives.

The implementation is an acyclic dynamic program. Its state records the
visited interval of boundary indices and the current side. If the remaining
mass is \(M\), the next boundary is \(y\), and the new searched cell has width
\(\Delta\) and density \(\beta\), the transition cost is
\[
 M\,|y-x|-\frac{\beta\Delta^2}{2}.
\]
An atom at \(y\) is removed in the next state, so its travel cost is counted.
There are \(O(K^2)\) states. All computations use exact rational or
rational-function arithmetic, and the output includes an actual route.

The turn verifier checks 77 exact second derivatives, 27 closed atom jumps,
48 collision deletions and 564 independent physical capture integrals.
The DP replay checks 24 states against 164 exhaustive boundary routes,
plus 36 fan-marginal and 156 captured-rank survivor identities.

See [STATIC_TAIL_BOUNDARY_REDUCTION.md](STATIC_TAIL_BOUNDARY_REDUCTION.md).

## 2. Continuous translation laws with fixed geometry

For each fixed base path \(p_i\), choose a translation uniformly from a fixed
nondegenerate interval \([\ell_i,r_i]\), clip the resulting path to the arena,
and apply fair reflection. A path and its interval are immutable strategy
data. The interval may be symmetric or outward, such as \([0,\delta]\).
All base paths used in the preserved experiment have slopes in
\(\{-1,0,1\}\).

There are two different laws to retain:

- The raw mixture chooses one translated physical path. Its pairwise payoffs
  are linear in the component weights.
- The common-quantile coupling uses the same time marginals to produce an
  ordered law. It is legal and has no smaller Princess payoff against any
  Monster, but its payoffs are generally not the raw matrix averages.

For the ordered law the radial CDF is
\[
 R_{\rm rad}(t,x)=
 \sum_i\frac{w_i}{r_i-\ell_i}
 \big|[p_i(t)+\ell_i,p_i(t)+r_i]\cap[-x,x]\big|,
 \qquad 0\le x<1.
\]
It has no center atom. Every fixed positive radial quantile therefore stays
strictly positive. This conclusion is about the ordered coupling: raw
translated paths can cross zero at different times.

The exact interval scorer integrates first-inverse moments over translation
bands. Its independent verifier integrates physical translated and clipped
paths instead. The replay covers 2,088 exact scores on 7,666 affine
translation pieces, 1,181 clipping crossings and 3,915 strict/closed
marginal checks.

A floating discovery companion retains the Monster's actual endpoint-hit
flags when collapsing ordinary coordinates. Dropping those flags changes
one verified payoff by exactly one. Its 6,282 exact comparisons agree within
\(1.14\cdot10^{-13}\). Floating optimization outputs remain discovery data.

The preserved symmetric-fan trial is a selected-response experiment.
The interval/outward scorer is verified separately; that fact does not
supply an unrestricted response certificate for an outward mixture.
The native ordered-weight optimization was interrupted before its new
controller files could be written, so no optimization outcome is claimed.

See [UNIFORM_TRANSLATION_FANS.md](UNIFORM_TRANSLATION_FANS.md).

## 3. A finite all-count center reduction for the ordered family

For the class above, with base paths stationary after \(h\), construct a
finite partition \(0=t_0<\cdots<t_J=h\). Partition at base vertices and zero
crossings of translated edges. Subdivide stationary-edge intervals so that
a whole center diamond stays inside the same density regime, and keep each
cell's duration at most one to exclude endpoint jumps from the interior
formula.

Every center diamond inside a cell then has
\[
 R(U,V)=k(U-V)
\]
for a constant \(k\ge0\). Consider two consecutive productive center returns,
of durations \(p\) and \(q\), starting at balanced captured rank \(n\).
Productivity implies \(n\le kp\le kq\). Merging the returns gives
\[
 2\Delta_{\rm merge}
 \le-\frac{kpq}{2}-nq+\frac{n^2}{4k}<0.
\]
The proof uses only monotonicity and the earliest possible capture time in
the future. It does not assume that the future remains stationary.

After merging, there is at most one productive return inside each partition
cell, and at most \(J-1\) returns that cross cell boundaries. Hence
\[
 \boxed{\text{at most }2J-1\text{ productive balanced returns by }h.}
\]
A conservative physical realization retains one additional balancing
action, followed by the separately solved static tail. Uniform quantile
approximation transfers the reduction to arbitrary center histories,
including growing Zeno entrances. It is not merely a statement that each
particular finite route can be shortened.

The packet passes 140 polynomial merge identities, 700 arbitrary-future
inverse pairings, 216 independent ordered physical captures, 682 exhaustive
partition-count cases and 1,008 whole-cone field identities. The root replay
reproduced those results independently.

This proves a finite center-continuation problem for a fixed ordered fan law.
It does not bound the same-side prefix before the first center.
See [FAN_FINITE_CENTER_RETURNS.md](../10-turn-density/FAN_FINITE_CENTER_RETURNS.md).

## 4. Earlier-center attachment for the previous frozen field

The earlier field has a different, center-atom structure. On its cone
\(0\le V\le U\le1/2\), its exact radial CDF is \(R(U,V)=\lambda U\), where
\[
 \lambda=\frac{3521265547}{12500000000}.
\]
Its front value is a future running minimum of its actual first-exit
envelope. An off-front state needs at most one internal productive return
before that front waiting phase. No constant front value is assumed.

In the middle strip \(1/2\le t\le7/8\), the past center frontier is at least
\(H=\lambda/2\). The full continuous field satisfies
\[
 R(e,t)>H\Longrightarrow
 e-t>\frac{3521265547}{358964317046}.
\]
The exact clipped-triangle audit therefore bounds the number of productive
middle returns by 38. This removes a turn-count question for that field;
it does not determine the low-record outside continuation.

See [CENTER_EARLY_MIDDLE_ATTACHMENT.md](../10-turn-density/CENTER_EARLY_MIDDLE_ATTACHMENT.md).

## 5. Arbitrary initial prefixes: what is and is not closed

The previous complete first-arrival exclusion remains valid on its specified
late interval. A stronger pointwise envelope now covers arbitrary same-side
prefixes by compressing only two extreme target contacts at a time. It
retains capture order, the time needed to reach center, and the strict
center trace. Exact polygon-edge arrangements evaluate its moment bound.

This envelope is a sufficient lower bound. Its pointwise maximizers can
depend on time, so it does not prove that one reversal is enough for a
whole optimal prefix. The verifier checks 27 multiple-turn prefixes,
3,141 record and moment comparisons and 289,040 envelope inequalities.

The general initial-prefix reduction remains a separate obligation.
Local affine-cell concavity is under investigation with its cell-containment
conditions retained. At a stationary density interface, a crossover
correction can change curvature; a blanket concavity extension cannot be
assumed. These local issues must be settled before declaring a complete
all-Monster response algorithm for the new family.

See [TWO_EXTREMA_PREFIX_ENVELOPE.md](../10-turn-density/TWO_EXTREMA_PREFIX_ENVELOPE.md).

## 6. Global scope

The proven reductions make several unbounded-history components finite or
exactly evaluable. A strategy attaining the current global ceiling, a
matching unrestricted opponent guarantee, and a closed minimax value are
still missing. The existing exact game bounds are unchanged.

The late native-runtime outage did not affect the already uploaded
certificates. The interval-fan extension, finite fan-center packet and
static DP were executed in the independent exact V8 runtime. No Lean
compilation or CI was run.
