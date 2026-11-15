# A completed affine-center attachment on the saved field

## Scope

This packet proves a center-continuation lower potential on the
reachable cone from the single balanced state
\[
 t_0=57/64,\qquad n_0=Z(t_0)=10184278599/62500000000
\]
of the saved field
`packages/interval_cdf_discovery/snapshots/endpoint_joint_i1_field.json`
(blob `5c45d042ee9948faebc03354c3e1e2ee3cbec1a5`).
It covers arbitrary subsequent center histories, including accumulating
returns, under the center-renewal reduction. It is not a global game
bound, a matching strategy, or a statement about arbitrary prefixes
before the first center visit.

The curvature is the exact rational number \(B=3000\).
An extension to the algebraic large Riccati root is a separate task;
closeness of numerical curvatures is not used as a proof.

## 1. Field, potential, and internal domain

On \(7/8\le V\le U\le b=15/16\),
\[
 R(U,V)=kU-\ell V+c,\quad Z(t)=dt+c,\quad d=k-\ell,
\]
where
\[
 k=655898601421/62500000000,\quad
 \ell=820954217/12500000000,\quad
 c=-71289950193/7812500000.
\]
Write \(q_b=Z(b)=10184278599/15625000000\) and \(r=\ell/k\).

For \(y=n-Z(t)\), put
\[
 V_0(t,n)=-dt^2/2-ty-(B+1/8)y^2/k.
\tag{1}
\]
The exact curvature gate is
\[
 16r^2B^2-(2-8r)B+1\le0.
\tag{2}
\]
It places \(B\) between the two Riccati roots. The productive-triangle
residual outside the short-return range is the positive quadratic
\[
 k[(1/4-r-2Br^2)h^2-(y/k)h+2B(y/k)^2].
\]
In the remaining productive range it is concave in \(h\), so its two
endpoints suffice. The nonproductive and wait residuals are those in
`CENTER_IMBALANCE_RENEWAL.md`; their coefficients are positive here.
Thus (1) verifies internal triangles and waits.

The reachable internal domain is
\[
 t_0\le s\le b,\quad
 Z(s)\le m\le
 \min\{R(s,t_0),R(b,s)\}.
\tag{3}
\]
The first upper bound is a genuine history bound from the initial
center state. The second is the affine inverse-cell gate.
Every internal successor that remains in (3) has both relevant
outgoing inverses inside the affine wedge. A productive return \(p<b\)
leaves the inverse domain exactly when
\[
 N=R(p,s)\ge R(b,p),
 \quad\text{or}\quad
 (k+\ell)p-\ell s-kb\ge0.
\tag{4}
\]

Define
\[
 A=k/8-\ell/2,\quad
 C_{\rm front}=(b+2)(1-q_b)+db^2/2,
\]
\[
 C_B=C_{\rm front}
 -\frac{9\ell^2}{16(A-k/(16B))}
 =\frac{10748868539258338056002451551}
        {1918110601942289500000000000}.
\tag{5}
\]
The attached potential is \(V_0+C_B\) until the first exit from (3).

## 2. Direct exits

The exact exterior normal form and cutoff are those in
`CENTER_LAST_CROSSING_ENVELOPE.md\). A useful crossing return lies in
\([b,17/16]\); longer non-endpoint returns are dominated by \(17/16\).
The closed endpoint action is separate. Center waiting to \(b\)
retains its complete capture moment.

The exact minimum of the direct crossing defect \(E-V_0\) over (3)
and the entire continuous crossing family is \(C_B\). It is attained
on the \(e=b\) face. The minimizer is the stationary point of
\[
 C_{\rm front}+A H^2-\frac32\ell H-\frac12Hy+
 \frac Bk y^2,\qquad H=b-s,
\]
in its no-hinge branch. Eliminating \(y\) gives (5).

The verifier checks 140 three-dimensional rational polytopes, with
all vertex, edge-stationary, face-stationary, and interior-stationary
candidates. It also independently checks every composed cost against
the full CDF moments. Endpoint and wait exits have strictly larger
minimum defects, retained exactly in the report.

Passing these direct exits alone would be insufficient: (4) can occur
before \(b\).

## 3. Rank-boundary exits

Suppose a first triangle returns at \(p<b\) and reaches
\(N=R(p,s)\ge R(b,p)\). Then no productive return before \(b\) remains.
Also \(N\ge q_b\), so all later ranks on a center row \(V\ge b\) are
endpoint-only. The exact exterior envelope at \((p,N)\) therefore
consists of a crossing return \(v\in[b,17/16]\), or an endpoint tour.

Waiting to \(b\) from this state is dominated by the endpoint tour
from \(p\): no surviving rank visits center before \(b\), every first
outward capture occurs no later when the tour starts at \(p\), and
the opposite endpoint is reached earlier. A nonproductive crossing
is likewise dominated by the included options.

For a useful second crossing, put \(M=R(v,p)\ge N\). The complete
two-action cost is
\[
 \frac12[
 T_s(N)-T_s(m)+T_p(M)-T_p(m)
 +(v+1)(M-N)]
 +(v+2)(1-M).
\tag{6}
\]
The intermediate \(T_p(N)\) cancels exactly. For endpoint continuation
from \(p\), the corresponding cost is
\[
 \frac12[
 T_s(N)-T_s(m)-T_p(m)+T_p(1)
 +(p+3)(1-N)].
\tag{7}
\]
These formulas retain the actual outgoing moments beyond \(b\).

For a fixed affine inverse cell of \(T_p(m)\), the rank-dependent
part of (6) or (7), after subtracting \(V_0(s,m)\), is quadratic in
\(m\), with coefficient
\[
 B/k-\frac1{8R_U}.
\]
Its exact fiber minimum is therefore among affine fiber endpoints
and, when this coefficient is positive, an affine stationary point.
A lower rank endpoint can minimize only when its right derivative
is nonnegative; an upper endpoint only when its left derivative is
nonpositive. These one-sided KKT gates are necessary even across
inverse-rank jumps.

After this rank elimination, all remaining constraints are affine
in \((s,p,v)\), and the costs are quadratic. Center and endpoint
inverse cells are included. Zero-area inverse images and boundary
faces use the continuous moment limits of the adjacent cells; no
pointwise inverse value at a plateau is substituted for a moment.

The complete retained arrangement has:

- 231 rank candidates and 126 feasible rank regions;
- 126 endpoint regions and 5,760 crossing regions;
- 28,514 polytope vertices;
- 103,840 exact Bernstein pairs.

For a quadratic \(q\) on a polytope with vertices \(x_i\), the vertex
values and pair coefficients
\[
 2q((x_i+x_j)/2)-[q(x_i)+q(x_j)]/2
\]
being nonnegative prove \(q\ge0\) throughout the polytope. This
certifies 5,885 regions directly after subtracting \(C_B\).
One remaining region is checked by the complete quadratic
stationary-face method. Its minimum is exactly \(C_B\).

There are 66 independent full-CDF composition checks, one endpoint
and one crossing check for every feasible inverse type. The affine
moment pieces themselves are also checked before the inequality
audit. These composition checks supplement the algebraic cancellation
in (6) and (7); they do not replace the all-region inequality proof.

## 4. Waits, accumulation, and full records

An empty wait that exits (3) before \(b\) can be deleted by extending
the next useful tent backward to the earlier center time. It captures
the chosen-side ranks no later; the removed wait had captured no
surviving opposite-side rank. Endpoint continuation is handled in the
same way. A wait that first reaches \(b\) is already a direct exit.

Every internal action has nonnegative \(V_0\)-residual. At the first
exit, Sections 2 and 3 give the certified continuation value.
The polynomial is continuous on the closed reachable domain.
An accumulating sequence of productive center returns reaches a
center-front state, and the finite costs telescope to that state
without a residual jump. The bounded-horizon approximation and
imbalance factorization in `CENTER_IMBALANCE_RENEWAL.md` then give
the assertion for unrestricted center continuations, not merely a
fixed number of turns.

The exact lower value delivered at the specified initial center
state is
\[
 C_B-\frac d2(57/64)^2
 =\frac{45046242873448026508184381387}
        {30689769631076632000000000000}
 \simeq1.46779345087797.
\]
This is a future-capture contribution at one balanced center state.
It is not an interval-game lower bound.

## 5. What this constrains in a matched construction

At the algebraic large Riccati root, the fixed-\(b\) stationary exit
would have
\[
 H_*=3\theta,\qquad y_*=3\ell\theta^2,
 \quad
 \theta=\frac{1-\sqrt{1-8r}}{1+\sqrt{1-8r}}.
\]
Its growing equality chain has successive return lengths
\(\ldots,3\theta^3,3\theta^2,3\theta\) and accumulation time
\(b-3\theta/(1-\theta)\). These are potential free-boundary and
active-support equations for a joint law. The rational packet does
not certify equality at that algebraic curvature; its actual inverse
and exterior gates must be replayed there.

A global matching construction still needs the initial-prefix
attachment, the other center regions, and the upper law. Existing
pure-monster deficits of the saved field remain.
