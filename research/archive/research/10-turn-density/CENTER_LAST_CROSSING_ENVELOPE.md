# The last center crossing and its exact exterior envelope

## 1. Scope and assumptions

This note closes the *last crossing* of a center renewal phase. It does
not solve the earlier renewal within that phase, the initial search
prefix, or the interval game.

Use the ordered, fairly reflected radial law and exact center
factorization in [CENTER_IMBALANCE_RENEWAL.md](CENTER_IMBALANCE_RENEWAL.md).
Let \(0\le a\le b\le c\le a+2\). Assume:

- The law is legal and endpoint-absorbed by time two.
- With \(q_b=R(b,b)\), every future interior radial CDF at
  \(U\ge V\ge b\) is at most \(q_b\).
- For each departure \(t\in[a,b]\), the interior row \(U\mapsto R(U,t)\)
  is constant on \(c\le U<t+2\).

Closed outward traces are used for captured ranks. The spatial endpoint
has its own closed capture jump to rank one; it is never replaced by
the interior limit. Define
\[
 T_t(q)=\int_0^q\beta_t(v)\,dv,\qquad
 H(e)=\int_e^{e+2}R(U,e)\,dU.
\]
These moments retain center and outgoing-characteristic atoms. The
standalone saved-field implementation additionally checks the absence
of a \(V=1\) atom, as required by its exact-field reader.

## 2. One crossing ends the center renewal

Consider a balanced center state \((t,n)\), \(t\in[a,b]\).
For a triangle returning at \(e\ge b\), put
\[
 N=\max(n,R(e,t)).
\]
Transport gives \(N\ge R(b,b)=q_b\). All surviving ranks above \(N\)
are therefore endpoint-only after this return. Their exact balanced
continuation is
\[
 V(e,N)=(e+2)(1-N).
\]
Thus the total value of this crossing action is
\[
 {\cal K}_e(t,n)=
 \frac12\int_n^N[\beta_t(q)+\beta_e(q)]\,dq
          +(e+2)(1-N).                              \tag{1}
\]
The imbalance factorization supplies the actual continuation from the
two unequal frontiers at the return. No captured record is discarded.

When \(e\ge c\) remains strictly before the endpoint return \(t+2\),
\(N\) is constant. Every \(\beta_e(q)\) is nondecreasing in its departure
parameter \(e\), and the last term in (1) is nondecreasing. Hence every
such later interior return is dominated by \(c\).

The closed endpoint action \(e=t+2\) is separate: it has \(N=1\) even
when the preceding interior row is flat. Its transformed cost is
\[
 {\cal B}_{\rm end}(t,n)
   =\frac{T_t(1)+(t+3)(1-n)}2.                       \tag{2}
\]

A center wait crossing \(b\) captures no further rank after \(b\):
the future center trace is at most \(q_b\). It is enough to wait to
\(b\) and then take the endpoint continuation. An unproductive crossing
with \(N=n\) is also dominated by this earlier wait boundary.

Consequently, the continuation from a center time in \([a,b]\) consists
of renewal actions before \(b\), followed by exactly one of:

1. a useful crossing \(e\in[b,c]\);
2. the closed endpoint action (2);
3. a wait reaching \(b\), or a limiting chain accumulating at its front.

The preceding renewal may have arbitrarily many returns. The statement
uses the finite-quantile/bounded-horizon limit from the center
factorization theorem; it does not assume that an arbitrary continuous
path has a first positive-measure productive excursion. Maximal tents
dominate arbitrary same-half excursions with fixed center endpoints.
An excursion reaching an endpoint first is covered by the endpoint
alternative. After the first return at or beyond \(b\), no further
center renewal is needed.

## 3. The crossing kernel

For a useful crossing \(N=R(e,t)\ge n\), let
\[
 I(t,e)=\int_t^eR(U,t)\,dU.
\]
First-inverse integration gives
\[
 T_t(N)=\frac{(t+e)N-I(t,e)}2.
\]
Since all ranks above \(q_b\) are endpoint-only on departure from \(e\),
\[
 T_e(N)=(e+1)N-H(e)/2.
\]
For the transformed value \(\mathcal W=V+T/2\), define
\(\mathcal B_e={\cal K}_e+T_t(n)/2\). Substitution yields
\[
 \boxed{
 4\mathcal B_e(t,n)=4e+8-(e+6-t)R(e,t)
                    -I(t,e)-H(e)-2T_e(n).
 }                                                     \tag{3}
\]
Where differentiable in rank,
\(\partial_n\mathcal B_e=-\beta_e(n)/2\).
Formula (3) retains the complete outgoing inverse moment. In
particular, non-flat incoming pieces after \(U=b\) must not be replaced
by a cap at \(b\).

If the pre-\(b\) wedge is affine,
\(R(U,V)=kU-\ell V+c_0\), \(d=k-\ell>0\), the wait boundary is explicit.
Put \(q_b=db+c_0\). For \(n\le q_b\),
\[
 V_{\rm wait}(t,n)=
 \frac{(q_b-n)((q_b+n)/2-c_0)}d
        +(b+2)(1-q_b).
\]
For \(n\ge q_b\), it is \((b+2)(1-n)\).
Add \(T_t(n)/2\) to obtain its transformed cost.

There is also an exact rank boundary before \(b\).
If \(n\ge R(b,t)\), no return before \(b\) is productive, and no
pre-\(b\) center wait captures a new rank. Removing empty waits shows
that the complete continuation at that state is the finite crossing,
wait, and endpoint envelope above. The unresolved inner renewal lies
below \(R(b,t)\).

## 4. Finite quadratic exterior data

For a piecewise-affine characteristic field, (3) is a rational quadratic
on a finite arrangement in \((t,e,n)\). The cuts are:

- the incoming triangle containing \((e,t)\);
- intersections of the line \(V=t\) with mesh edges;
- outgoing \(V=e\) cell boundaries;
- the outgoing rank-\(n\) inverse crossing an edge;
- the useful-capture boundary \(R(e,t)=n\).

Every edge rank is affine in its edge parameter. Thus all these domain
conditions are affine. The row integrals and first-inverse primitive
are quadratic on each piece. In particular, a fixed \((t,n)\) has an
exact one-dimensional quadratic partition in \(e\).

A quadratic reaches its minimum on a closed interval at an endpoint,
or at its stationary point if that point is interior and the curvature
is positive. This gives an exact continuum minimizer without a
return-time grid. More generally, eliminating \(e\) gives finitely
many quadratic candidate functions of \((t,n)\), each on a polyhedral
domain. Their lower envelope need not itself have a polyhedral
partition: comparisons between quadratic candidates can have curved
boundaries.

The saved-state oracle constructs every listed cut exactly, evaluates
the quadratic from three rational values on each interval, and checks
two additional rational values. The mathematical arrangement gives
the degree-two assertion; the extra evaluations audit the construction
and arithmetic. It retains the endpoint jump as a separate candidate.

## 5. An internal inverse-model comparison

This additional gate can be useful for attaching a lower potential.
Suppose the affine wedge is as above and, on every full outgoing row
with \(V\in[a,b]\),
\[
 R_{\rm actual}(U,V)\le kU-\ell V+c_0.
\]
Also require
\[
 z(t)+2k\ge1\qquad(t\in[a,b]),
\]
so the inequality includes the *closed endpoint* rather than merely
its interior trace. Then
\[
 \beta_t^{\rm actual}(q)\ge
 \beta_t^{\rm aff}(q)
 :=t+\frac{(q-z(t))_+}{2k},\qquad 0\le q\le1.          \tag{4}
\]
Thus an internal triangle's actual balanced renewal kernel is at least
the affine-model kernel, even if an outgoing inverse has left the
affine wedge.

The polynomial \(V_C\) from the affine Riccati construction remains an
internal subsolution under this comparison. Its transformed version
must be defined using the **actual** moment,
\[
 \mathcal W_C^{\rm actual}=V_C+T_{\rm actual}/2.
\]
It is generally not the simple polynomial \(\mathcal W_C\) outside the
local inverse range. Exit inequalities must use the actual kernel (3),
wait boundary, and endpoint boundary. No attached value of \(C\) is
certified in this note.

The equality curvature is not the only possible subsolution curvature.
Any \(B\) between the two roots of
\[
 16r^2B^2-(2-8r)B+1\le0
\]
makes the productive affine quadratic nonnegative; the other internal
triangle and wait signs remain nonnegative as well. A finite supremum
of separately attached lower subsolutions is again a lower
subsolution, by monotonicity of the balanced Bellman operator. This
is a verification option, not an exact-value assertion.

## 6. Exact saved-field audit

The verifier uses
`packages/interval_cdf_discovery/snapshots/endpoint_joint_i1_field.json`,
Git blob `5c45d042ee9948faebc03354c3e1e2ee3cbec1a5`, with
\[
 a=7/8,\quad b=15/16,\quad c=17/16,\quad
 q_b=10184278599/15625000000.
\]

- All 6,324 future positive-cone vertex checks are at most \(q_b\).
- All 408 vertices on the row \(V=b\) equal \(q_b\).
- All 75 triangles with \(U\ge17/16\) and
  \(V\in[7/8,15/16]\) have exactly zero \(R_U\).
- No triangle crosses the three defining grid lines.
- All 408 outgoing affine-model vertex checks pass. The minimum
  closed-endpoint model value is
  \(655898601421/31250000000>1\).
- All 69 outgoing \(V=1\) nodes vanish.

The field nevertheless has **30 non-flat incoming triangles** between
\(U=b\) and \(U=17/16\) over departures \(V<b\). Their exact coefficients
are retained in the report. For example,
\[
 R(15/16,7/8)=655898601421/10^{12},
\]
whereas
\[
 R(1,7/8)=730280888043/10^{12},
 \qquad
 R(17/16,7/8)=148453227923/(2\cdot10^{11}).
\]
Therefore the prescribed-\(b\) front-chain QP is a valid component, not
the whole continuation.

## 7. Reproducible state-wise minima

`verify_center_last_crossing.cjs` exposes
`makeOracle(fieldData).minimize(t,n)` and `verify(fieldData)`.
The pure-V8 replay checked six rational states, comprising 368 exact
quadratic intervals, 736 additional quarter-point identities, and 368
independent comparisons of (3) with the complete renewal moments.
The minimizing return can differ materially by rank. For instance,
at \(t=57/64,n=z(t)\) it is \(15/16\), while at
\(t=57/64,n=3/5\) it is \(63/64\). At \(n=7/10\), the direct endpoint
alternative beats the best interior crossing.

These are conditional continuation values for specified center states.
They are not values of the original game. The remaining task is to
attach the finite quadratic exterior envelope to the inner affine
renewal or to a verified lower subsolution, and then to the global
initial-prefix problem.
