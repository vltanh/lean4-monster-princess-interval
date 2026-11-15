# Constructive Princess extraction from the finite clock-grid dual

Research proof, 2026-11-13.

Let \(V\) be the unrestricted interval Princess--Monster value, and let
\(U_n\) be the rational finite-clock-grid optimum defined in
EFFECTIVE_FINITE_UPPER_REDUCTION.md and POLYNOMIAL_CLOCK_GRID_LP.md.
Write \(h=1/n\) and \(\Delta=h/2\). The already proved enclosure is

\[
 U_n-\frac h2\le V\le U_n.
\]

The finite LP also yields an explicit Princess strategy. For every
rational \(0<\varepsilon\le1/2\), one can construct a legal symmetric
ordered Princess law with a finite rational piecewise affine CDF,
sticky endpoints, and maximal outward motion after time \(2\), whose
security is at least

\[
 \boxed{U_n-\frac h2-\frac{h\varepsilon}{2}.}                 \tag{1}
\]

For example, \(\varepsilon=1/2\) gives \(U_n-3/(4n)\), while
\(\varepsilon=1/(2n)\) gives
\(U_n-1/(2n)-1/(4n^2)\).
The parameter must remain positive. No claim is made that the
zero-width interpolation is a legal regular CDF or that a finite
program terminates exactly at \(V\).

The construction does not require random rounding to be unbiased.
The field is defined as the expected nodal field under the same
rounding used in the physical clock transfer. This identity, not
unbiasedness of the rounded coordinate, is the relevant property.

## 1. Exact lattice, clock polytope, and nodal minimax

Use light coordinates \(U=t+x\), \(W=t-x\). The full lattice domain is

\[
 {\cal L}_n=\{(ih,jh):i,j\in\mathbb Z,\quad
 0\le i+j\le16n,\quad |i-j|\le2n\}.
\]

It is the set of lattice nodes in \(0\le t\le8\), \(|x|\le1\).
In the physical indexing \(t=a\Delta,x=b\Delta\), the parity
condition is \(a\equiv b\pmod2\). All grid paths in the finite
program start at time zero with \(x\in h\mathbb Z\), visit the
center by time \(2\), and complete both endpoints by time \(8\).

Let \(P_n\) be the compact rational polytope of symmetric laws on
these paths and their atomic active clocks, before introducing
pressure-matching variables. It can be represented either by the
finite path bank or by the polynomial occupancy graph. Its linear
image consists of the aggregate active selected-event measures
\(\alpha\). For an oriented path the negative-endpoint active clock
has mass \(\tau_-\); for a fair reflected pair the equivalent
two-clock representation has mass
\((\tau_-+\tau_+)/2\). Denote this aggregate mass by \(M\).

For a positive event \(z=(t,r)\), \(r>0\), associate the interval
\(I_z=[t-r,t+r]\). A negative event \((s,-a)\) has the radial
interval \(I_y=[s-a,s+a]\). Matching is allowed precisely when
\(I_z\subseteq I_y\). Center events are omitted from both pressure
sides.

For fixed positive and negative masses \(p_z,q_y\), the unmatched
positive mass is

\[
 d=\max_{\substack{0\le u_z,v_y\le1\\u_z\le v_y\ (I_z\subseteq I_y)}}
       \left(\sum_zp_zu_z-\sum_yq_yv_y\right).                 \tag{2}
\]

This is the finite bipartite max-flow/min-cut dual. Its apparently
different source and target values can be replaced by one radial
isotone profile. Given feasible \(u,v\), put, on every radial
lattice node \(y\),

\[
 g_y=\sup\{u_z:I_z\subseteq I_y,\ r_z>0\},                    \tag{3}
\]

with empty supremum zero, and put \(g(t,0)=0\).
Then \(0\le g\le1\), \(g\) is nondecreasing under interval
containment, \(g_z\ge u_z\) at source nodes, and \(g_y\le v_y\)
at target nodes. Thus replacing \(u,v\) by \(g,g\) weakly increases
the expression in (2). Conversely every such \(g\) is feasible
in (2). Including zero-mass and otherwise unreachable lattice
nodes in (3) does not change the optimum.

Let \(Q_n\) be the rational polytope of these radial profiles.
Define the signed *interior-trace* nodal field by

\[
 f(t,r)=\frac{1+g(t,r)}2,\qquad
 f(t,-r)=\frac{1-g(t,r)}2\quad(r>0),\qquad f(t,0)=\frac12.
                                                               \tag{4}
\]

The nodal field is nondecreasing in \(U\) and nonincreasing in
\(W\). Within either spatial sign this is exactly interval
containment; across the center it follows from the two half-ranges
in (4). It satisfies \(f(t,-x)=1-f(t,x)\).

The corresponding nodal clock plane is

\[
 R(\alpha,g)=\int 2f(t,x)\,d\alpha(t,x)
 =M+\sum_zp_zg_z-\sum_yq_yg_y.                              \tag{5}
\]

Consequently the finite upper program is exactly

\[
 U_n=\min_{\alpha\in P_n}\max_{g\in Q_n}R(\alpha,g)
     =\max_{g\in Q_n}\min_{\alpha\in P_n}R(\alpha,g).          \tag{6}
\]

The second equality is finite compact convex bilinear minimax.
All data are rational; an optimal nodal profile \(g^*\) can be
chosen rational, for example from the finite LP dual. Fix one.
Then

\[
 R(\alpha,g^*)\ge U_n\qquad\text{for every }\alpha\in P_n.    \tag{7}
\]

If an implementation outputs the covering dual
\(d_z\ge0,\ d_p+d_q\ge1\) instead, truncate those values to
\([0,1]\), take source lower values \(1-d_p\), target upper
values \(d_q\), and apply (3). Raw covering discounts themselves
are not the radial CDF.

The negative endpoint value in (4) is its interior trace. The
actual strict CDF at \(-1\) will be zero. No valid negative-active
clock selects its own first negative endpoint, so this distinction
does not change (5) on feasible grid clocks.

## 2. A one-parameter family of common odd rounding maps

The integer cell indices modulo \(2n\) are paired by the fixed-point
free involution

\[
 k\longmapsto -k-1\pmod{2n}.
\]

Choose one representative in each pair. Representatives have
orientation \(+\); their partners have orientation \(-\).
Repeat these orientations with period \(2n\).

Let \(Z\) be uniform on the interval

\[
 A=\frac12-\varepsilon<Z<\frac12+\varepsilon=B.
\]

In cell \([kh,(k+1)h]\), use the threshold

\[
 \theta_k(Z)=
 \begin{cases}
 Z,&k\text{ has orientation }+,\\
 1-Z,&k\text{ has orientation }-.
 \end{cases}
\]

For a point strictly inside this cell, round to its lower endpoint
below the threshold and to its upper endpoint above the threshold.
At a threshold tie, choose the lower endpoint in a \(+\) cell
and the upper endpoint in a \(-\) cell. Fix every grid point.
This defines \(T_Z:\mathbb R\to h\mathbb Z\).

For every \(Z\in(A,B)\), including \(Z=1/2\), the map satisfies

\[
 \begin{split}
 &T_Z\text{ is nondecreasing},\qquad T_Z(-z)=-T_Z(z),\\
 &T_Z(z+2)=T_Z(z)+2,\qquad T_Z(kh)=kh,\\
 &|T_Z(z)-z|\le b(Z):=h\max(Z,1-Z).
 \end{split}                                               \tag{8}
\]

The reflected tie conventions make oddness exact, rather than an
almost-everywhere assertion. The interval endpoints \(A,B\) have
zero probability and may be omitted. If
\(\varepsilon=1/2\), this also omits thresholds zero and one.

Since \(Z\) is uniform around \(1/2\),

\[
 \mathbb E b(Z)=h\left(\frac12+\frac{\varepsilon}{2}\right).
                                                               \tag{9}
\]

Unbiasedness \(\mathbb ET_Z(z)=z\) is true in the special full-width
case \(\varepsilon=1/2\), but is not needed below.

## 3. A continuous legal rational piecewise affine CDF

On the closed physical strip \(0\le t\le8\), \(|x|\le1\), define

\[
 F_{\mathrm{int}}(t,x)=
 \mathbb E_Z f\bigl(T_Z(t+x),T_Z(t-x)\bigr),                 \tag{10}
\]

where the arguments of \(f\) on the right are light coordinates.

Every image lies in \({\cal L}_n\). Indeed oddness and monotonicity
preserve \(U+W\ge0\); period \(2\) and oddness preserve the plane
\(U+W=16\), hence its lower half-space; and period \(2\) preserves
\(|U-W|\le2\). In particular no nonexistent parity or boundary node
is being evaluated. Formula (10) agrees with \(f\) at every lattice
node because all \(T_Z\) fix grid points.

Each integrand is monotone in the light coordinates in the required
directions, and reflection swaps its two coordinates. Thus

\[
 F_{\mathrm{int}}(t,-x)=1-F_{\mathrm{int}}(t,x),\qquad
 F_{\mathrm{int}}(t,0)=\frac12,
\]

and \(F_{\mathrm{int}}\) obeys both speed-one CDF transport
inequalities.

The field is continuous, including at the center and the interior
traces of the physical endpoints. To see this directly, inside a
light-coordinate cell the probability that changing a coordinate
by \(a\) changes its rounded value is at most
\(|a|/(2\varepsilon h)\). The same bound follows across cell
boundaries by subdivision. Since \(0\le f\le1\), a telescoping
argument gives a finite Lipschitz constant for (10). In particular
the radial interior CDF has no center atom.

It is also rational piecewise affine. For fixed light-coordinate
cells, each of their two rounded values changes when \(Z\) crosses
one affine threshold: either a normalized coordinate or one minus
that coordinate. The probabilities of the at most four joint
rounding outcomes are interval lengths cut out by these two
thresholds and \(A,B\). They are affine on a finite subdivision
by rational lines. Multiplying by rational nodal values and adding
preserves rational piecewise affinity. Only one shared random
parameter is used; independent thresholds would generally produce
bilinear patches.

For \(0\le r<1\), put

\[
 G(t,r)=2F_{\mathrm{int}}(t,r)-1,
\]

and complete the radial CDF by setting \(G(t,1)=1\).
The possible jump at \(r=1\) is the endpoint atom. The common upper
quantiles of this radial distribution are legal speed-one paths,
by the transport inequalities. Give each radial rank an independent
fair spatial sign. This defines a symmetric ordered Princess law,
denoted by \(\mu\). Its strict signed CDF agrees with
\(F_{\mathrm{int}}\) on \(-1<x\le1\); at \(x=-1\) its strict
CDF is zero. Its interior negative-endpoint trace remains
\(F_{\mathrm{int}}(t,-1)\).

The quantiles may be written using the convention
\(r(t,u)=\inf\{a:G(t,a)>u\}\), \(0\le u<1\).
The endpoint value \(G(t,1)=1\) makes this well defined. The two
transport inequalities give
\(|r(t,u)-r(s,u)|\le|t-s|\).
There are finitely many affine CDF regions, so this is an explicit
finite description of a continuum of legal paths.

## 4. Exact continuous-clock identity on the bounded physical class

Fix an arbitrary Monster path \(m\) that visits zero by time \(2\)
and both endpoints by time \(8\), and consider its fair reflected
pair. For the law \(\mu\), choose minimizing causal active clocks on
this pair *before* sampling \(Z\).

This choice has an exact record interpretation. Along an oriented
path, prior to its first negative endpoint, the left-surviving rank
mass is the running minimum of the strict CDF
\(F_{\mathrm{int}}(s,m(s))\). This function is continuous on every
compact interval before that endpoint. Select a history time
attaining each running minimum and integrate the scoring-time
Lebesgue measure. The resulting selected-time measure \(\eta_m\)
satisfies

\[
 \eta_m([0,\tau_-))=\tau_-,\qquad
 \eta_m([0,s])\ge s\quad(s<\tau_-).
\]

Averaging the two orientations makes the two surviving sides equal
in expectation. Therefore, writing \(J_\mu(m)\) for capture against
the fair reflected Monster pair,

\[
 J_\mu(m)=
 \mathbb E_{\{m,-m\}}\int 2F_{\mathrm{int}}(s,m(s))\,d\eta_m(s).
                                                               \tag{11}
\]

The clocks never select the negative endpoint. Positive endpoint
contacts use the continuous interior trace, which is exactly the
actual strict CDF there. Thus no endpoint germ or center atom is
being dropped from (11). A measurable minimizing selector, or its
equivalent causal selected-time measure, suffices.

## 5. Transfer the fixed clocks, not a post-rounded best response

For each \(Z\), apply \(T_Z\) to both light coordinates of the
physical paths and of all selected events in (11).
Fill simultaneous coordinate jumps by legal positive coordinate-axis
steps, including every exact image tiepoint. At the physical
boundary use an inward-first order when required. Use a
reflection-invariant finite filling kernel, as in the common
quantization theorem.

The result is a fair reflected law on unit-speed lattice paths.
An old event at time \(s\) has new time

\[
 \rho_{m,Z}(s)=
 \frac{T_Z(s+m(s))+T_Z(s-m(s))}{2},\qquad
 |\rho_{m,Z}(s)-s|\le b(Z).                                 \tag{12}
\]

Its new first negative endpoint time \(\tau'_-\) obeys
\(\tau'_-\le\tau_-+b(Z)\). Center-by-\(2\) and completion-by-\(8\)
are preserved exactly: a center visit at \(s\le2\) maps to
\(T_Z(s)\le2\), and an endpoint visit at \(s\le8\) maps to
\(1+T_Z(s-1)\le8\). Oddness preserves the initial time zero and
puts the initial position in \(h\mathbb Z\).

Push each old selected-time measure through \(\rho_{m,Z}\), add
\(b(Z)\) units at time zero, and retain the earliest
\(\tau'_-\) units. The prefix argument is exact: for \(t<\tau'_-\),
the buffer alone suffices if \(t<b(Z)\); otherwise

\[
 b(Z)+(\rho_{m,Z\#}\eta_m)([0,t])
 \ge b(Z)+\eta_m([0,t-b(Z)])\ge t.
\]

The old time \(t-b(Z)\) is strictly before \(\tau_-\), by the
endpoint-time bound. Taking \(t\uparrow\tau'_-\) shows that
at least \(\tau'_-\) units lie strictly before the new negative
endpoint, so the truncation never needs to retain an atom there.
If \(\tau'_-=0\), the repaired clock is empty.

The retained clock is supported on grid vertices and satisfies the
left-limit atomic prefix constraints. After conditioning on each
new grid path and averaging the fill choices, it is a feasible
point of \(P_n\). Therefore (7) gives, for every \(Z\),

\[
 R_{\rm new}(Z)\ge U_n.                                    \tag{13}
\]

Now evaluate its cost. Before buffer and truncation, Fubini and the
fact that the old clocks were fixed before \(Z\) give

\[
 \mathbb E_Z R_{\rm pushed}(Z)=J_\mu(m).                    \tag{14}
\]

This is precisely the defining identity (10). It does not require
rounding to be unbiased, and would not follow from choosing new
old clocks separately after observing \(Z\).

For this bookkeeping, use the nodal *interior trace* even for raw
image events that have landed at the negative endpoint. Such raw
events have nonnegative cost. They are removed whenever necessary
by the active-clock truncation, and are never retained in (13).

The time-zero buffer is symmetric for each \(Z\): both orientations
receive the same \(b(Z)\), \(T_Z\) is odd, and the fill kernel respects
reflection. Since \(f(0,x)+f(0,-x)=1\), its total nodal plane cost is
exactly \(b(Z)\), including the center case. Truncation removes only
nonnegative nodal costs. Combining (13)--(14),

\[
 U_n\le\mathbb E_ZR_{\rm new}(Z)
     \le J_\mu(m)+\mathbb E b(Z).
\]

Using (9), every center-by-\(2\), completed-by-\(8\) Monster path
therefore satisfies

\[
 J_\mu(m)\ge
 U_n-h\left(\frac12+\frac{\varepsilon}{2}\right).             \tag{15}
\]

No comparison between vertex-detected capture and actual grid capture
is needed. The finite dual bounds every admissible atomic clock
plane directly; (11) supplies an exact old continuous clock plane.

## 6. An explicit sticky outward-after-two law and all Monsters

First stop every radial quantile of \(\mu\) at its first endpoint
contact. This weakly increases its capture time against every
Monster path and preserves the rank ordering. Because \(\mu\) has
no interior atoms, its stopped radial CDF, for \(r<1\), is

\[
 G_{\rm st}(t,r)=
 \min\left(G(t,r),\inf_{0\le s\le t}G(s,1-)\right).           \tag{16}
\]

The endpoint trace is continuous and piecewise affine, so its running
minimum is rational piecewise affine. Formula (16) is again a finite
rational piecewise affine field. The absence of a center atom is
relevant: for an arbitrary nonsmoothed law the analogous strict
signed-CDF formula should not be asserted at \(x=0\).

Next, after time \(2\), move every radial path maximally outward:

\[
 \widetilde r(t,u)=
 \begin{cases}
 r_{\rm st}(t,u),&t\le2,\\
 \min(1,r_{\rm st}(2,u)+t-2),&t\ge2.
 \end{cases}
\]

Call the fair reflected law \(\widetilde\mu\).
It is sticky, legal, ordered, and absorbed at the endpoints by
time \(3\). For \(t\ge2,r<1\), its radial CDF is

\[
 \widetilde G(t,r)=
 \begin{cases}
 0,&r<t-2,\\
 G_{\rm st}(2,r-t+2),&r\ge t-2.
 \end{cases}                                               \tag{17}
\]

Thus it retains a finite rational piecewise affine description.

Consider any Monster path \(m\).

If it visits the center by time \(2\), every surviving positive
Princess is to its right and every surviving negative Princess to
its left. Maximal outward forcing after \(2\) therefore cannot
make either survivor be caught earlier. Moreover, after time \(2\)
these survivors can only be caught at their respective endpoints.
Their endpoint arrival times are no later than the Monster's direct
earliest arrival there, by the strict survivor order at time \(2\).

Consequently one may replace the Monster suffix after time \(2\)
by a direct tour of the two endpoints in its original endpoint
order, obtaining a path \(\widehat m\) with no larger payoff against
\(\widetilde\mu\). This new path preserves the center visit and
completes by time \(6\). If one side has no survivors, choose an
endpoint order that serves the remaining side first. It lies in
the completed-by-\(8\) class used in (15). The stopping and outward
operations imply

\[
 J_{\widetilde\mu}(m)
 \ge J_{\widetilde\mu}(\widehat m)
 \ge J_\mu(\widehat m)
 \ge U_n-h\left(\frac12+\frac{\varepsilon}{2}\right).         \tag{18}
\]

If the Monster has not visited zero by time \(2\), its sign has
been constant. The opposite fair half of the Princess law is still
uncaptured. After time \(2\), that half moves away at full speed and
can only be caught at the opposite endpoint, at time at least
\(3+|m(2)|>3\). Hence the expected payoff is greater than \(3/2\).
The target in (18) is at most \(V\), by the already established
finite reduction, and \(V<3/2\) by the available explicit upper
certificate. Thus (18) holds in this case as well.

Reflection of the Monster does not alter its payoff against the
symmetric Princess law, so the fair-pair formulation imposes no
restriction on arbitrary deterministic or mixed Monster responses.
This proves (1).

## 7. Finite constructive output and scope

A complete implementation can perform the following exact operations:

1. Solve the rational clock-grid LP and its dual; obtain \(U_n\)
   and a rational optimal nodal profile through (2)--(6).
2. Choose rational \(0<\varepsilon\le1/2\), orient the finitely many
   reflection-paired grid cells, and use the common threshold law.
3. Integrate the two-switch nodal field exactly by interval lengths
   in \(Z\), producing its rational piecewise affine subdivision.
4. Apply (16) and (17), and return the common quantile description.

Every step is finite. The Monster primal certificate gives an upper
bound \(U_n\); the Princess law gives the lower guarantee (1).
For any requested positive tolerance, choosing \(n\) and
\(\varepsilon\) explicitly yields finite descriptions of both
strategies with a certified gap.

This is stronger than an abstract lower bound inferred only from
the upper approximation theorem: it supplies a concrete legal
Princess law. It still does not identify a closed form for \(V\),
prove finite exact termination, or assert that the limiting Princess
law has finitely many affine regions.

The limiting choice \(\varepsilon=0\) is deliberately excluded.
A deterministic discontinuous rounding can destroy continuity at
the center or along a characteristic. The finite LP's center cost
then need not coincide with the actual strict-CDF capture plane.
Positive interpolation width removes that issue and costs only
the explicitly displayed additional \(h\varepsilon/2\).
