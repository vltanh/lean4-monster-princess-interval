# The complete continuous late negative-M2 response family

## Scope

For a supplied ordered endpoint-by-two CDF on the saved Cartesian triangular
mesh, the minimum over every continuous negative start and every continuous
late first turn reduces exactly to 3,502 univariate quadratic edge problems.
This closes a response family, not the unrestricted game.

The self-contained exact verifier is
[verify_late_negative_m2_edges.cjs](../../packages/interval_cdf_discovery/verify_late_negative_m2_edges.cjs).
Its rational field reader is the previously checked source with Git blob
5714f57ada458f38ef8b46adb32be2472a009622. The geometry is pinned to
endpoint_joint_i1_field.json, blob 5c45d042ee9948faebc03354c3e1e2ee3cbec1a5.
Different nodal CDF values are allowed only on that same geometry.

## 1. Physical routes and the affine field functional

For \(0\le a\le1\), the negative-start monster uses the vertices
\[
 (0,-a),\quad ((s+a)/2,(s-a)/2),\quad(s+1,-1),\quad(s+3,1),
 \qquad 1\le s\le2+a.
\]
The first coordinate is time. Write
\[
 A(a)=R(a,-a),\quad N(a)=\int_{-a}^{a}R(a,v)\,dv,\quad
 I(a,s)=\int_a^sR(u,a)\,du.
\]
The continuous initial trace has no center or endpoint atom, and the
interior trace on \(V=1\) is zero. These conditions and transport are checked
by the reader. Exact first-capture integration gives
\[
 \boxed{4C_-(a,s)=N(a)+4s+8-2(s+1)A(a)
 -(6+s-a)B(a,s)-I(a,s).}                              \tag{1}
\]
For an interior turn, \(B(a,s)=R(s,a)\). At the actual positive endpoint
\(s=2+a\), use the closed \(B=1\). The integral uses the interior trace:
the point jump changes the turn-capture term but has zero integral.

Equation (1) partitions the initially captured negative ranks, the positive
ranks caught before the turn, and the remaining endpoint captures. It is
also the endpoint collapse of equation (2) in
[TWO_INTERIOR_TURN_CDF.md](TWO_INTERIOR_TURN_CDF.md). Each term is affine in
the nodal CDF values for fixed \((a,s)\); this family has no clipped
moving-rank moment.

## 2. Concavity reduces the turn parameter to edges

Inside one affine triangle at fixed \(a\),
\[
 4\partial_s C_-=4-2A(a)-2R(s,a)-(6+s-a)R_U(s,a),
 \qquad
 \boxed{4\partial_s^2 C_-=-3R_U(s,a)\le0.}              \tag{2}
\]
Thus each fixed-\(a\) fiber has its minimum at a fiber endpoint on an edge.
The cost need not be concave across several triangles. Horizontal edges
have fixed \(a\), so their endpoints suffice by the same argument. Those
vertices also occur on the retained nonhorizontal edges.

An actual endpoint turn can have a lower cost than its interior limit.
The closed endpoint branch is checked separately. Every limiting cost on
that boundary is no smaller than an included actual endpoint cost. No
continuity through the contact jump is assumed.

## 3. Every retained edge carries an exact quadratic

The saved geometry is a conforming Cartesian triangulation. A retained
edge varies \(a\) within one initial-knot interval. There \(A(a)\) is affine.
The row defining \(N(a)\) meets a fixed sequence of triangles whose crossing
coordinates are affine in \(a\). Integrating affine pieces between these
limits gives a quadratic.

The same argument applies to the column integral \(I(a,s)\). No mesh vertex
is crossed between successive \(a\)-knots. Its intersection coordinates
are affine in \(a\), and the edge's upper limit \(s\) is affine as well.
Their order cannot change in the open strip of a conforming mesh. The
integral is therefore quadratic. \(R(s,a)\) is affine along the edge.
The closed endpoint branch, where \(B=1\), also remains quadratic.

The verifier pins the complete reference geometry, checks the axis-aligned
triangle cells, and checks that no retained edge straddles an initial
knot. Its additional exact evaluations at one third and two thirds are
algebra checks; the polynomial-degree proof is the arrangement argument,
not interpolation tests alone.

For an edge polynomial \(q(t)=q_0+q_1t+q_2t^2\), \(0\le t\le1\), check both
endpoints and, when \(q_2>0\), the stationary point
\(t=-q_1/(2q_2)\) if it lies inside the interval. These checks cover the
whole edge, hence the complete continuous parameter domain.

## 4. Executed exact certificate

The fresh standalone V8 run on the original saved field checks:

| Whole-domain item | Count |
| --- | ---: |
| Post-one positive-V triangles | 3,468 |
| Retained vertical and diagonal edges | 3,502 |
| Actual endpoint edges | 34 |
| Exact additional quadratic identities | 7,004 |
| Interior stationary candidates | 407 |

The entire late negative-M2 minimum is
\[
 \frac{3049055886151563289642052958230357}
 {2142660280000789348352000000000000}
 \approx1.423023479088547,
\]
at
\[
 s=1,\qquad a=\frac{9808320373751385}{16347200622564616}.
\]
The generic unit-route first-capture engine reproduces this exact fraction
independently. It agrees with the earlier fixed-one exclusion, now with
every later continuous turn also covered. The saved report is
snapshots/late_negative_m2_full_exact.json.

A separate native Python run had previously checked a corrected diagnostic
field over the same complete domain. Its minimum occurred at \(s=129/128\),
and genuine diagonal-edge stationary attacks also occurred. That field's
latest bytes were not remotely preserved before the second executor outage;
the present standalone certificate deliberately uses the fully available
original field. No inaccessible native candidate is required for replay.

From the repository root:

~~~sh
node packages/interval_cdf_discovery/verify_late_negative_m2_edges.cjs \
  --expected packages/interval_cdf_discovery/snapshots/late_negative_m2_full_exact.json
~~~

The exact computational body was executed in the tool V8 runtime. The new
file-I/O wrapper was not executed after the native environment went offline.

## 5. Use in the joint construction

Each edge polynomial has coefficients affine in the CDF nodal values.
These forms can be compiled once; each changed field then needs only 3,502
scalar quadratic minimizations for this complete family. A violated
minimizer supplies an affine field constraint directly.

Early turns, other path geometries, the unrestricted pre-center potential,
and a matching upper strategy remain separate. This result does not change
the established rigorous bounds on the game.
