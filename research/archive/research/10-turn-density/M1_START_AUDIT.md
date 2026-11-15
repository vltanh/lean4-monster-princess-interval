# Every sweep starting position for an affine CDF field

This is an exact verification procedure for a **specified** triangular
CDF field. It removes sampling of the monster's initial position in the
M1 family. It does not prove that a sweep is an unrestricted best response,
and does not close the game value.

## 1. Assumptions and cost identities

Use the ordered radial law, fair reflection, and endpoint absorption by
time two. The field is continuous and affine on its triangles, with the
correct transport signs. Assume no initial center or endpoint atom and no
outgoing atom on `V=1`, as in the frozen discovery fields. Write

\[
A(z)=R(z,-z),\quad
N(z)=\int_{-z}^{z}R(z,V)\,dV,\quad
H(z)=\int_z^{z+2}R(U,z)\,dU.
\]

An M1 monster starts at `x`, runs to `+1`, and then to `-1`. Its cost at
a negative start is

\[
\boxed{4C_1(-z)=N(z)+4z+8-2(z+3)A(z)-H(z).}             \tag{1}
\]

The negative-copy ranks through `A(z)` are caught on the initial leg;
their doubled first-inverse contribution is `N(z)`. The remaining negative
ranks are caught at time `z+3`. The positive copies are caught on the
outward characteristic `V=z`; their doubled integral is `2(z+1)-H(z)`.
This gives (1), including the endpoint and center starting faces.

For a positive start put

\[
I(z)=\int_z^{2-z}R(U,-z)\,dU,\qquad
K(z)=\int_{-z}^{1}(A(z)-R(2-z,V))_+\,dV.
\]

Then

\[
\boxed{4C_1(z)=8-4z+(3-z)A(z)-I(z)-K(z).}              \tag{2}
\]

This also follows by taking the endpoint face in the positive one-turn
identity. The portion of its incoming integral above `V=1` is
`(1-z)A(z)`; removing that part gives exactly (2). There are no incoming
or outgoing characteristic atoms in the open field, so the integral
traces coincide. Actual endpoint contact still uses its closed spatial
CDF, as required by the original capture identity.

## 2. The finite quadratic arrangement

For (1), use every initial-CDF knot and every mesh coordinate in `[0,1]`.
Between consecutive breakpoints, each row-cut endpoint is affine in `z`,
and the integrated CDF is affine in both its arguments. Thus the cost is
a quadratic polynomial in `z`. Its minimum is at an interval endpoint
or at the interior stationary point of that quadratic.

For (2), first include the reflected mesh breakpoints `2-U`. On the strip
`1<=U<=2`, divide triangles also at the reflected initial-CDF knots if
necessary. The current discovery mesh already contains those cuts. On
each resulting triangle,

\[
A(2-U)-R(U,V)
\]

is affine. Its zero line cuts triangle edges at exact rational points.
Add `z=2-U` for each such intersection. These are all vertices at which
the vertical slice of the positive-part region can change. Between
successive breakpoints, its slice endpoints are affine in `z`; integrating
the affine function over that slice is again quadratic. The same exact
endpoint/stationary-point check therefore covers **every** positive start.

`packages/interval_cdf_discovery/audit_m1.py` implements this arrangement
with Fractions. It additionally checks each recovered quadratic at a
fourth rational point, and recomputes every interior minimizer. This is
not an optimizer tolerance or a finer starting grid.

On the frozen `constant_half_wait_candidate.json`, there are 34 negative
and 148 positive quadratic cells. The respective exact minimum costs
are approximately `1.42325291845` and `1.42328251252`. The complete rational
values and attaining starting points are in the saved audit. These values
are **specified-field M1 minima**, not bounds on the game and not the
unrestricted minimum for this field.

## 3. A stronger exact same-half attack

The route

\[
(0,13/16),\quad(1/32,25/32),\quad(1/8,7/8),\quad
(2,-1),\quad(4,1)
\]

is legal and first moves inward, turns outward, and then makes its final
endpoint tour. Against the frozen field it costs approximately
`1.42146653905`; against the separately repaired rational field it costs
approximately `1.42146698736`. In both cases the exact cost is strictly
less than `142147/100000`.

`verify_frozen_attack.py` obtains the same rational value in two ways:
the initial-inward identity and signed-CDF first-moment actions on the
actual unit-speed legs. It also cross-checks 24 signed M1 costs exactly.
The repair enforces the late derivative inequalities, but it does not
remove this early attack. Neither frozen field supports its larger
finite-pool objective as an unrestricted guarantee.


## 4. The complete fixed-U=1 M2 start audit

This continuation also removes start sampling from the M2 family whose
first turn is U=1. For a>=0, define A=A(a), N=N(a),

\[
B_\pm=R(1,\pm a),\quad I_\pm=\int_a^1R(U,\pm a)dU,\quad
K=\int_{-a}^1(A-R(1,V))_+dV.
\]

The exact signed costs are

\[
4C_2(a)=12+2A-(7+a)B_- -I_- -K,
\]
\[
4C_2(-a)=N+12-4A-(7-a)B_+-I_+.
\]

Negative starts use the common initial/grid breakpoints. Positive starts
also split whenever A(a) crosses a fixed row value R(1,V_i). Within every
resulting interval the cost is quadratic. Its endpoint values and any
interior stationary point therefore give the exact global minimum.

For endpoint_joint_i1_field.json the endpoint reference is

\[
V_0=2985216065253480021/2097152000000000000.
\]

The positive M2 minimum is

\[
\frac{61994785573126022897501035790501376708583323}
{43563909270327237018364602744832000000000000}
=1.4230767305208911\ldots,
\]

at a=238813713375000299959477253/332366251146905800005833456.
The negative M2 minimum is

\[
\frac{3049055886151563289642052958230357}
{2142660280000789348352000000000000}
=1.423023479088547\ldots,
\]

at a=9808320373751385/16347200622564616. These lie below V_0 by
approximately 0.0003852147 and 0.0004384661 respectively.

The 85 positive and 34 negative quadratic regions were checked exactly,
with two independent physical first-capture comparisons per region
(238 comparisons). The later V8 reconstruction reproduced every exact
minimum independently after the original executor became unavailable.

These are failures of the supplied field. They are not new game bounds.
In particular, preserving old M1/M2 columns in a terminal correction
does not establish that those old columns already met the target.

## 5. An earlier two-turn defect and its whole-cell certificate

A negative-start M3 route starts at -a, turns at U=s, then V=1,
and completes the endpoint tour. Put

\[
B=R(s,a),\quad D=R(1,s),\quad I=\int_a^sR(U,a)dU,\quad
G=\int_s^1(R(U,s)-A(a))_+dU.
\]

Its exact cost is

\[
4C_3(-a;s,1)
=N(a)+12-8A(a)+(s+a-4)B-(7-s)(D-A(a))_+-I-G.
\]

The positive part in G is essential; the center trace can lie below A.
At a=1/32, s=273/320 the cost equals

\[
15434184049555077911630832656723/
10843618135685201920000000000000,
\]

which is below V_0 by the exact amount

\[
1293714632475068364089328937/
10843618135685201920000000000000.
\]

This point was extended to the entire geometric tetrahedron

\[
0\le a\le s-13/16,\qquad 13/16\le s\le b\le7/8,
\]

where b is the free rank cutoff. Its exact minimum occurs in the
interior at a=0.0302357859461..., s=0.857134032303...,
b=0.858288261371.... The physical cost is
1.4233421829970763..., again below V_0.

See QUADRATIC_RESPONSE_CELLS.md for the exact lifted matrices and the
singular-face minimization proof. The fixed geometry, including every
start/cutoff in each cell, supplies constraints for a joint field solve.
It does not certify this failing field.

Implementation: packages/interval_cdf_discovery/audit_fixed_one.py.
Independent executed reconstruction:
packages/interval_cdf_discovery/exact_response_audit.mjs and
snapshots/continuation_exact_recovery_report.json.


## 6. A genuine early positive-M2 attack in the final affine corner

For the same endpoint_joint_i1 field, let
\(a=262143/262144\) and \(s=524287/524288<1\).
The monster starts at \(a\), runs right to first characteristic \(U=s\),
then visits the negative and positive endpoints. Its route, after
removing the repeated time-zero vertex, is
\[
 (0,262143/262144),\
 (1/1048576,1048573/1048576),\
 (1048575/524288,-1),\
 (2097151/524288,1).
\]
The general initial-inward formula (with zero first inward leg) and the
independent physical record integral give the same exact cost
\[
 \frac{3037502927420596050426366332305024657}
 {2134207024934514851840000000000000000}
 =1.4232466166274556\ldots<V_0.
\]
The full ordered round-41 continuous/finite mixture costs approximately
1.4232167207728863 on this same route. The exact mixed fraction and
complete input identifiers are saved in
snapshots/early_positive_m2_tail_attack.json. These are specified-law
attacks, not new game bounds. They also lie outside the delayed \(s\ge1\)
Bellman branch certified in RECORD_BELLMAN_POST_GATE.md.
