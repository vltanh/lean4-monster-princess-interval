# Exact general inward–outward response with free second turn

## Scope

This is an exact response formula for a supplied ordered, fairly reflected
princess law. It is not an equilibrium or an unrestricted lower certificate.
The radial law is at its endpoint by time two. Its interior CDF is continuous
and affine on the supplied triangular regions, with no initial endpoint or
center atom and no outgoing V=1 atom. Endpoint capture uses the closed CDF.

The formula covers an arbitrary interior first inward turn, an arbitrary
second outward turn, second turns before or after U=1, and a second turn at
the endpoint. A first turn at the center is a separate boundary case and
is deliberately excluded: it can capture both reflected center copies.

The identities below were checked against independent physical
first-capture integration in exact V8 BigInt arithmetic after the executor
outage. This is substantive response algebra, not a value-interval update.

## 1. Route and first moments

Use U=t+x and V=t-x on the positive half. The monster starts at z>0,
moves inward to (z,v), outward to (s,v), then visits -1 and +1. Thus

\[
0<z\le1,\qquad -z\le v<z,\qquad z\le s\le v+2.
\]

Its physical vertices are

\[
(0,z),\quad ((z+v)/2,(z-v)/2),\quad
((s+v)/2,(s-v)/2),\quad(s+1,-1),\quad(s+3,1).
\]

Zero-duration repeated vertices are harmless. Put

\[
A=R(z,-z),\quad l=R(z,v),\quad
B=\begin{cases}1,&s=v+2,\\R(s,v),&s<v+2,\end{cases}
\qquad m=\max(A,B),
\]
\[
N=\int_{-z}^{z}R(z,V)\,dV.
\]

The endpoint value B=1 is essential. Replacing it by the interior endpoint
trace misses the captured endpoint atom and gives the wrong response.

Let alpha_q(U) and beta_q(V) be the *first* inverses of t+p_q(t) and
t-p_q(t), with inverse zero if the initial threshold has already been
passed. Define P_U(q)=integral_0^q alpha_r(U)dr and
T_V(q)=integral_0^q beta_r(V)dr. Exact capture records give

\[
2C_I=P_z(A)-P_z(l)+P_s(l)
     +T_v(m)-T_v(A)+(s+3)(1-m)+T_s(1).       \tag{1}
\]

The first two capture bands concern lower positive ranks; the next band
contains new upper positive ranks. The complete negative reflected copy
uses T_s(1). In particular T_s(1) cannot be replaced by s+1 when s<1.

## 2. Two independent rank cutoffs

For the supplied continuous field,

\[
2P_z(A)=N,\qquad
2P_z(l)=(z+v)l+\int_v^zR(z,V)\,dV.          \tag{2}
\]

The later lower-rank moment is

\[
2P_s(l)=\min_c\left((s+c)l+\int_c^sR(s,V)\,dV\right).  \tag{3}
\]

The physical lower bound for c is max(-s,s-2). It can be tightened to
v<=c<=min(s,1): R(s,v)>=R(z,v)=l, and for c<v the derivative of the
displayed expression is l-R(s,c)<=0. Raising c to v cannot increase it.
The bound s-2 is already no larger than v by legality of the route.
Flat cutoff rows are allowed; the minimum need not have a unique root.

Equivalently, an implementation can avoid a rank inversion and use

\[
2P_s(l)=2sl-
 \int_{\max(-s,s-2)}^s(l-R(s,V))_+\,dV.       \tag{4}
\]

For the new upper positive captures, integration by parts gives

\[
2[T_v(m)-T_v(A)+(s+3)(1-m)]
=2(s+3)(1-A)-(s+6-v)(B-A)_+
 -\int_z^s(R(U,v)-A)_+\,dU.                 \tag{5}
\]

There is no omitted contribution before U=z: R(U,v)<=l<=A there.
Monotonicity in U yields the exact hinge lift

\[
\int_z^s(R(U,v)-A)_+dU
=\max_{z\le b\le s}
 \left(\int_b^sR(U,v)dU-(s-b)A\right).        \tag{6}
\]

Finally, the complete reflected first moment is

\[
2T_s(1)=2s+2-\int_s^{s+2}R(U,s)\,dU,         \tag{7}
\]

where the discovery representation extends R(U,V)=0 for V>1.
This keeps the full early outgoing moment and reduces correctly to
2s+2 for s>=1 under the stated V=1 convention.

## 3. Exact lifted formula

For z<=b<=s, v<=c<=min(s,1), and j in {0,1}, set

\[
\begin{aligned}
F_j(z,v,s,b,c)={}&N+4s+8+(s+c-z-v)l-(s+b+6)A\\
&-j(s+6-v)(B-A)\\
&-\int_v^zR(z,V)dV+\int_c^sR(s,V)dV\\
&-\int_b^sR(U,v)dU-\int_s^{s+2}R(U,s)dU.
\end{aligned}                                                   \tag{8}
\]

Equations (1)–(7) prove

\[
\boxed{4C_I(z,v,s)=\min_{b,c,j}F_j(z,v,s,b,c).}          \tag{9}
\]

Thus a lower target h on this entire response family is equivalent to
F_j>=4h for every legal lifted tuple and both branches. No cutoff is
frozen from a numerical field.

Every F_j is affine in the CDF nodal values. On a fixed geometric region
it is a quadratic in the five variables (z,v,s,b,c). The endpoint branch
s=v+2 uses the constant B=1 and must be represented separately from the
interior trace.

### Removing the extra hinge branch

If all negative-M1 inequalities already hold, only j=1 is necessary.
When B>A, F_1<=F_0. When B<=A, the outward excursion captures no new upper
positive rank. Deleting that excursion gives the direct initial inward
sweep and its endpoint tour. The lower positive first inverses,
the complete reflected first inverses, and the final upper tail all
become no later. This direct route is the reflection of negative M1
starting at -z. Hence the actual I cost is already above target in this
case, and both lifted branches are above it. This deletion argument uses
the actual captured records, not a reset at U=1.

## 4. Consequences for exact geometric verification

For a fixed rational field, an interior minimizer satisfies

\[
R(b,v)=A(z),\qquad R(s,c)=R(z,v).
\]

On specified nonflat triangles, these equations solve b and c as affine
functions of the three physical parameters (z,v,s). Substitution gives
a quadratic response on a rational three-dimensional polytope. Zero
slopes, boundary cutoffs, and equality faces need their own branches.
One can therefore verify a supplied field by exact quadratic minimization
on those regions without sampling starts or turns.

For joint field construction, retain b and c as variables to keep
coefficients affine in the nodal values. This is a five-dimensional
lift. A simplex has six vertices, so nonnegativity is a 6-by-6
copositivity constraint. The identity copositive = PSD + entrywise
nonnegative is exact only up to order four. Using that decomposition here
is a sufficient restriction, not an exact representation.

The cutoff directions do have useful structure:

\[
\partial_{bb}F_j=R_U(b,v)\ge0,\qquad
\partial_{cc}F_j=-R_V(s,c)\ge0,\qquad
\partial_{bc}F_j=0.
\]

These facts permit exact separate cutoff minimization; they do not by
themselves establish an exact order-six semidefinite representation.

## 5. Executed checks and remaining work

The independent exact verifier in
packages/interval_cdf_discovery/exact_response_audit.mjs checked 120
physical routes: six starts, four interior first-turn choices, and five
second-turn choices. These include 28 endpoint second turns and 73
second turns with s>1. For 24 nondegenerate cases it independently
enumerated both rank-cutoff roots/boundaries and both hinge branches,
and the minimum of (8) equaled the physical first-capture value.

The sparse implementation is GeometryForms.positive_i_four in
quadratic_response_forms.py. That Python method is a reconstruction
written during the outage; its formula was verified independently, but
the new Python method itself was not rerun.

The global field solve, all geometric response inequalities, the
pre-center Bellman gate, and a matching unrestricted upper law remain
open. This formula supplies the missing free-second-turn I family to
that construction. It does not assert that the supplied field passes it.
