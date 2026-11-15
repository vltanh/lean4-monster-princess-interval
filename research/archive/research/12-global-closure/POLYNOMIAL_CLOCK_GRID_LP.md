# Polynomial-size occupancy form of the effective finite reduction

Research proof for independent review, 2026-11-13.

The exponential physical-path bank in
EFFECTIVE_FINITE_UPPER_REDUCTION.md can be compressed exactly.
Its value \(U_n\) is the value of a rational linear program with
\(O(n^4)\) states, arcs and matching variables. Therefore

\[
 U_n-\frac1{2n}\le V\le U_n
\]

can be obtained from a finite LP of polynomial size in \(n\).
This is an additive approximation theorem, not a claim that a
fixed finite LP already has the exact unrestricted value.

## 1. Atomic causal clocks are mixtures of integer credit calendars

Put

\[
 \Delta=\frac1{2n},\qquad N=16n,
\]

so the physical completion horizon is \(N\Delta=8\).
Fix one physical lattice path whose first visit to a particular
endpoint occurs at step \(k\). Normalize its clock mass by its
physical-path probability and by \(\Delta\). The resulting charges
\(b_0,\ldots,b_{k-1}\) satisfy

\[
 b_j\ge0,\qquad
 \sum_{j=0}^{k-1}b_j=k,\qquad
 S_j:=\sum_{i=0}^{j}b_i\ge j+1.
\]

Let \(Z\) be uniform on \([0,1)\), and set

\[
 S'_j=\lfloor S_j+Z\rfloor,\qquad S'_{-1}=0,\qquad
 b'_j=S'_j-S'_{j-1}.
\]

The cumulative values are nondecreasing integers. Since \(j+1\)
and \(k\) are integers,

\[
 S'_j\ge j+1,\qquad S'_{k-1}=k.
\]

Thus each realization \(b'\) is an integer causal calendar.
The identity \(\mathbb E\lfloor x+Z\rfloor=x\) gives
\(\mathbb E b'_j=b_j\) at every selected vertex.
Only the finitely many fractional parts of the \(S_j\) change the
calendar, so this is a finite mixture.
For \(k=0\), the unique calendar is empty; its queue starts inactive
with zero credit at the initial endpoint.

For the two active endpoint clocks, make these decompositions
independently conditional on the same physical path. Their joint
mixture retains both selected-event marginals exactly. In particular
it preserves every aggregate pressure and every matching capacity.

The future credit after charging at physical step \(j\) is
\(q=S'_j-j\). It is at least one before an active physical move,
decreases by one during that move, and is zero on arrival at its
endpoint. Moreover

\[
 0\le q\le k-j\le N-j.
\]

This gives a bounded finite-state realization of every feasible
atomic-clock path law.

## 2. The finite state graph

A state records

\[
 (j,k,q_-,q_+,e_-,e_+,c).
\]

Here:

* physical time is \(t=j\Delta\), \(0\le j\le N\);
* physical position is \(x=k\Delta\), \(-2n\le k\le2n\);
* \(e_-\) and \(e_+\) indicate that the corresponding endpoint
  has already been visited;
* \(c\) indicates a center visit;
* an active endpoint clock has an integer credit
  \(0\le q_\pm\le N-j\); an inactive clock has credit zero.

Exclude states with \(j\ge4n\) and \(c=0\), enforcing the proven
center deadline \(2\). Start states have \(j=0\), even \(k\),
zero queues, and the correct instantaneous endpoint/center flags.
Thus the allowed initial positions are exactly the spacing-\(1/n\)
lattice positions.

There are four kinds of control arcs.

**Negative-clock charge.** If \(e_-=0\), increase \(q_-\) by one,
provided its bound remains satisfied. Its selected physical event is
\((j\Delta,k\Delta)\).

**Positive-clock charge.** If \(e_+=0\), increase \(q_+\) by one.
Its selected event, in the reflected one-clock representation, is
\((j\Delta,-k\Delta)\).

**Left or right physical move.** Increase \(j\) by one and change
\(k\) by \(-1\) or \(+1\), staying in the physical strip. Every
still-active queue must be at least one before the move and is
decremented by one.

Update the center flag on reaching \(k=0\). On a first endpoint
arrival, require the corresponding decremented queue to be exactly
zero, then mark that clock inactive. This zero-credit requirement is
essential: arbitrary disposal of prepaid credit would change the
active clock mass.

States with both endpoint flags set may terminate. They can also be
extended to time \(8\) by arbitrary legal unit-speed grid moves;
all Princess paths have already been captured, so this does not
affect any active clock or cost.

The integer

\[
 \ell=3j+q_-+q_+
\]

strictly increases on every arc. A charge increases it by one;
a move increases it by \(3-a\ge1\), where \(a\in\{0,1,2\}\)
is the number of active clocks. Hence the graph is acyclic.

## 3. Unit flow gives an actual physical law

Add a source connected to the allowed initial states and a sink
connected to terminal states. Impose nonnegative arc flows, unit
source outflow, and ordinary conservation at all other states.

Every such finite acyclic flow decomposes into source-to-sink paths.
Each graph path carries:

1. a genuine unit-speed physical Monster path;
2. one integer causal clock ending at its negative endpoint;
3. one integer causal clock ending at its positive endpoint.

The two clocks remain attached to the same physical path. This
joint state is the information missing from the invalid raw
Eulerian occupation relaxation.

For each decomposed physical path, use a fair reflection. Attach the
negative clock to the original path and the positive clock, with
selected positions reflected, to its reflected path.
This constructs a symmetric physical Monster law with one active
clock on each orientation.

Accordingly a charge arc of flow \(f\) contributes event mass
\(\Delta f/2\): at \((t,x)\) for a negative-clock charge and at
\((t,-x)\) for a positive-clock charge.

The total selected mass is

\[
 M=\frac\Delta2\sum_{\text{charge arcs }a}f_a
   =\frac12\,\mathbb E(\tau_-+\tau_+),
\]

which is precisely the symmetric active-clock baseline.

## 4. Pressure matching and the objective

Aggregate charge counts at each reflected one-clock event node
\(z=(j,k)\). Call them \(c_z\), before multiplying by \(\Delta/2\).
For a positive node \(k>0\) and a negative node \(k'<0\), introduce
a matching variable \(\gamma_{zz'}\ge0\) exactly when

\[
 -k'\ge k+|j'-j|.
\]

This is the physical interval-containment condition in integer
coordinates. Bound each source sum by \(c_z\) and each target sum
by \(c_{z'}\). Minimize

\[
 \frac\Delta2\left[
    \sum_{\text{charge arcs }a}f_a
    +\sum_{z:\,k>0}c_z
    -\sum_{z,z'}\gamma_{zz'}
 \right].
\]

The expression is \(M+\) unmatched positive pressure.
Every feasible flow and matching therefore gives an actual
unrestricted all-Princess upper bound.

All matrix coefficients can be chosen integral; only the displayed
overall objective scale is fractional.

## 5. Exact equivalence with the physical-path-bank LP

Starting from a feasible physical-path-bank solution, pair the two
reflected active clocks for each physical path. Section 1 decomposes
each conditional clock into integer calendars. Taking their product
conditional on that physical path produces graph paths with exactly
the same physical probabilities and aggregate selected-event masses.
The same pressure matching remains feasible. Thus the occupancy LP
has value no larger than the bank LP.

Conversely, decompose any occupancy flow as in Section 3. Its fair
reflected physical law, clock calendars, and matching form a feasible
solution of the bank LP, with exactly the same objective.
Paths terminating early can be extended within the bank through
time \(8\). Hence the occupancy LP has value no smaller than the
bank LP.

The two optimal values are therefore identical.

## 6. Size and effective approximation

The indices \(j,k,q_-,q_+\) each have \(O(n)\) possibilities;
the endpoint and center flags have only finitely many possibilities.
There are therefore \(O(n^4)\) states and at most four control arcs
per state, apart from the source and sink arcs.

There are \(O(n^2)\) physical event nodes. Introducing every permitted
positive-negative matching pair uses at most \(O(n^4)\) variables.
Flow conservation, event aggregation, and matching capacities have
the same polynomial size. Their integer coordinates have
\(O(\log n)\) bit length.

The common-quantization theorem now gives

\[
 \boxed{U_n-\frac1{2n}\le V\le U_n}
\]

for this polynomial-size rational LP. In particular, taking
\(n\ge1/(2\varepsilon)\) gives an additive enclosure of width
at most \(\varepsilon\).

A rational optimal flow can be decomposed into at most as many
positive-weight graph paths as there are arcs. Thus the resulting
finite rational upper law also has a polynomial support bound,
although the coarse constants and the size of exact LP arithmetic
may still be substantial.

No claim of exact finite termination or practical high-precision
running time is made.
