# Exact clock atomization by a common left-floor map

Date: 2026-11-13.

For every finite reflection-closed bank of polygonal unit-speed Monster
paths, subdivide by the common union of all light-coordinate vertex
knots. Then **vertex-supported causal clocks suffice exactly** for the
bank's unrestricted Princess-response minimax.

In particular, on the common light grid, the vertex-clock value \(U_n\)
and the vertex-plus-uniform-leg value \(\widehat U_n\) are equal:

\[
 \boxed{\widehat U_n=U_n
 =\min_{\nu\text{ on the physical grid bank}}
       \sup_{p\text{ legal}}\mathbb E_\nu T(M,p).}
\]

The physical paths do not change in this argument. Only their selected
history events and the matching are moved earlier. There is no physical
time error and no clock buffer. This is distinct from the effective
quantization theorem, which changes arbitrary physical paths into grid
paths and therefore still needs its \(1/(2n)\) buffer estimate.

## 1. Common subdivision of a finite unit-speed bank

Use light coordinates \(U=t+x\), \(W=t-x\). Truncate each oriented
active clock at the path's first visit to its negative endpoint.
Include both reflected orientations. Let

\[
 K=\{k_0<k_1<\cdots<k_R\}
\]

contain both light coordinates of every physical vertex of every
scored path. Subdivide every unit-speed leg wherever its free light
coordinate crosses any knot of \(K\).

Every resulting open physical subleg has one light coordinate fixed
at a knot and the other increasing through one consecutive band
\((k_j,k_{j+1})\). Its chronological left endpoint is the physical
point obtained by replacing that free coordinate by \(k_j\).

This subdivision includes every center crossing: the free coordinate
meets the leg's fixed coordinate, which itself belongs to \(K\).
Initial and arena endpoint events are also retained as vertices.

## 2. Floor selected histories while keeping physical scoring fixed

Define the common nondecreasing map \(T\) on the relevant coordinate
range by

\[
 T(k_j)=k_j,\qquad T(z)=k_j\quad(k_j<z<k_{j+1}).
\]

Apply \(T\) to both light coordinates of every selected event and to
both ends of every pressure-matching pair. Do **not** transform the
physical path, the scoring event, or the scoring measure \(dt\).

On each open scored subleg, the selected event moves to that
subleg's chronological left vertex on the same physical path.
Vertices stay fixed. If the old selected history time is \(s\),
write its new time as \(\ell_m(s)\). Then

\[
 0\le\ell_m(s)\le s.
\]

Thus a selected-time measure \(\eta_m\) of total active mass \(\tau_m\)
is sent to \(\ell_{m\#}\eta_m\) with the same mass, and

\[
 (\ell_{m\#}\eta_m)([0,t])
 \ge \eta_m([0,t])\ge t\qquad(0\le t<\tau_m).
\]

Causality improves. Every selected event remains strictly before the
clock's own endpoint: a scored subleg cannot depart that endpoint,
since its clock would already be inactive. Flooring a selected time
can therefore never introduce a selected atom at the active endpoint.

Reflection causes no difficulty. It swaps \(U\) and \(W\), and the
same \(T\) acts on both. Oddness of \(T\) is unnecessary. The physical
Monster law and its reflection symmetry remain unchanged, as does
the active endpoint baseline \(M=\mathbb E\tau_-\).

## 3. Matching and the exact center-collapse accounting

For a positive selected event \(p\), write its radial interval as
\(I_p=[W_p,U_p]\). For a negative event \(q\), write
\(I_q=[U_q,W_q]\). A match is allowed exactly when

\[
 I_p\subseteq I_q.
\]

The common nondecreasing map preserves this containment:

\[
 [T(W_p),T(U_p)]\subseteq[T(U_q),T(W_q)].
\]

Spatial signs cannot reverse. A positive or negative event may
collapse to the center. If a matched negative target collapses,
its transformed containing interval is a singleton, so its
transformed positive source must collapse too.

Push the matching through \(T\), then discard exactly those pairs
whose positive source has collapsed. All remaining pairs have a
strictly positive source and strictly negative target, with the
required cone containment.

Let \(P\) be the original positive mass and \(|\pi|\) its matched
mass. Let \(r\) be the positive mass that collapses and \(\lambda\)
the discarded matched mass. Then

\[
 0\le\lambda\le r,\qquad
 P'=P-r,\qquad |\pi'|=|\pi|-\lambda.
\]

The new deficiency satisfies

\[
 d'=P'-|\pi'|
    =d-r+\lambda\le d.
\]

Since \(M\) did not change,

\[
 \boxed{M+d'\le M+d.}
\]

This argument includes atoms, equality contacts, and center
collapse. It does not assume a density or a positive separation
from the center.

## 4. Exact finite-bank consequence

Start with any physical clock-and-matching certificate on the
finite bank. Sections 1--3 produce an atomic certificate on the
subdivision vertices with no larger objective. Conversely, atomic
clocks are allowed among arbitrary causal clocks. Hence the two
infima are equal.

The fixed-bank strong one-record duality and causal matching theorem
identify that common infimum with the bank's unrestricted Princess
response value. No Princess best-response attainment is required.
If one starts with a minimizing sequence of arbitrary clocks, the
same construction gives an atomic minimizing sequence; the finite
atomic LP is compact and attains its infimum.

Mixture weights can be fixed or optimized. In either case the
atomic masses obey the exact left-limit prefix inequalities. On
an equally spaced physical grid of step \(\Delta\), they are

\[
 \sum_{i=0}^{j}a_{m,i}\ge w_m(j+1)\Delta,\qquad
 \sum_i a_{m,i}=w_m\tau_m.
\]

For a nonuniform common subdivision, replace
\((j+1)\Delta\) by the next physical vertex time.

In particular the polynomial vertex-clock grid LP already computes
the exact true value of its finite physical bank. The uniform-leg
planning graph is an equivalent refinement and an independent
realization of the same value; it is not a strictly stronger
optimization.

## 5. Scope and an important distinction

The conclusion applies to finite unit-speed polygonal banks after
the full common light-knot subdivision. Positive-duration waits and
general subunit-speed legs are excluded: both light coordinates may
vary, and flooring them can leave the physical leg. No such case
is silently converted to a unit-speed path here.

The theorem also does not say that left-flooring a clock decreases
its plane against each fixed Princess field. It need not do so.
What decreases is the matching objective \(M+d\), which is the
all-Princess upper certificate.

For example, the previously extracted regular CDFs for the \(n=1\)
and \(n=2\) finite duals have a smaller continuous fast-sweep capture
cost than their left-vertex clock plane. That is a failure of those
particular interpolations to preserve a tight clock plane. It is
not evidence of a difference between the atomic and continuous
clock minimax values on the same physical bank.

Finally, this exact atomization does not remove the unrestricted
physical-path problem. The effective finite reduction still gives

\[
 U_n-\frac1{2n}\le V\le U_n,
\]

rather than asserting \(U_n=V\) for a finite \(n\).

## 6. Dependencies and independent regression

The active one-clock dual and the matching identity are proved in
GLOBAL_INFINITE_HORIZON_ACTIVE_DUAL.md and
GLOBAL_CAUSAL_PRESSURE_MATCHING.md. The fixed-bank geometry is also
described in FINITE_BANK_CLOCK_HOMOGENIZATION.md.

An independent exact regression checks selected events on unit-grid
paths, causality, matching type pairs, center collapse, and weighted
deficiency accounting. Its scope is the floor transformation, not
the numerical solution of a finite LP or the exact full-game value.

