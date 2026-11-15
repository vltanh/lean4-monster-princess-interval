# Curved initial terminal phases: sources, moments, and attachment

The ordinary initial unit-speed run is excluded by
[INWARD_INITIAL_OBSTRUCTION.md](INWARD_INITIAL_OBSTRUCTION.md) wherever
the corresponding positive-M2 response is active. This note replaces
that run by a general initial arc. It gives exact cost identities, a
conditional incoming-front contraction, and attachment conditions.
It does not supply a matched law or an unrestricted game value.

The low-field sources are defined in
[TERMINAL_SOURCE_FIXED_POINT.md](TERMINAL_SOURCE_FIXED_POINT.md).
The active initial-inward equation and its free boundary are in
[INITIAL_INWARD_CDF.md](INITIAL_INWARD_CDF.md).

## 1. Geometry and conventions

Retain a low ordered sublaw of mass \(q_0=1-r_T\), with CDF \(L\).
Its initial positions are at most \(1-x_T\), and its outgoing rows
\(V\ge1-x_T\) are empty. Use the same full physical-domain extensions
in both source integrals:

\[
 Q(x)=\int_{-1}^1[L(1+x,V)-L(1,V)]\,dV,\qquad
 \Omega(\eta)=\int_{-1}^1[L(1,V)-L(1-\eta,V)]\,dV.       \tag{1}
\]

For a high path indexed by initial deficit \(\xi\), write
\(a=1-\xi,\ u=1-h(\xi),\ c=-1+d(\xi)\). Its mass element is
\(dr(\xi)\), where \(r(0)=0,\ r(x_T)=r_T\). It follows an initial
arc, then the incoming characteristic \(U=u\), then the outgoing
characteristic \(V=c\) to the endpoint. All of this path's incoming
motion finishes before \(U=1\). The low sublaw may still have post-one
flux, retained by \(Q\).

Write \(\eta=1-U,\ y=1+V\). The initial graph is

\[
 \eta=\chi_\xi(y),\qquad
 \chi_\xi(\xi)=\xi,\quad
 \chi_\xi(b(\xi))=h(\xi).
\]

Here \(b(\xi)\) is the first-turn outgoing deficit. Assume
\(0<h(\xi)<\xi\le b(\xi)<d(\xi)<1\), and extend
\(\chi_\xi(y)=h(\xi)\) for \(y\ge b(\xi)\). An initial unit tangent
is allowed. A positive-length unit run remains subject to the obstruction
above. Write the inverse as

\[
 Y_\xi(\eta)=\chi_\xi^{-1}(\eta),\qquad Y_\xi(\xi)=\xi.
\]

Monotonicity of the characteristic graph gives the speed bound.
For example, \(-1\le\partial_\eta Y\le0\) corresponds to initial
velocities in \([0,1]\). Ordered initial arcs additionally require
\(Y_\xi(\eta)\) to be nondecreasing in \(\xi\) on their common domain.
This order condition is separate from the speed condition.

The formulas below use continuous rank distributions and first-contact
traces. With atoms, horizontal first-inverse moments use the strict radial
CDF; spatial turn and column terms use the closed CDF. The verifier
avoids ambiguous atomic initial and incoming rows in the source identities
and retains the strict corner trace in the separate corner checks.

## 2. The two initial-arc corrections

Define

\[
 J_{\rm init}(y)=\int_0^y[\chi_\xi(y)-h(\xi)]\,dr(\xi),       \tag{2}
\]

\[
 K_{\rm init}(\eta)=
 \int_{\substack{\eta\le\xi\le x_T\\h(\xi)\le\eta}}
 [Y_\xi(\eta)-\xi]\,dr(\xi).                                \tag{3}
\]

Both are nonnegative. The extension of \(\chi\) makes (2) vanish after
the initial arc; no endpoint contribution is continued through it.
On the initial arc,
\(2\beta_\xi(-1+y)=y-\chi_\xi(y)\).
Relative to the ordinary initial run with the same \(r,d,h\), the
four-cost correction is therefore \(-J_{\rm init}(y)\) for both positive
M1 and positive M2. Their difference is unchanged.

Put \(\tau=d^{-1}(x)\) and \(E(x)=r(\tau)\). If the positive costs
match the endpoint sweep, the exact equations are

\[
 (8-2x)E(x)=x[3-r(x)]+Q(x),                              \tag{4}
\]

\[
 \int_0^x[d(t)+h(t)]\,dr(t)+J_{\rm init}(x)
 =3x+Q(x)+xE(x)+\int_0^\tau h(t)\,dr(t).                 \tag{5}
\]

For negative M1, the first \(U=1-\eta\) hitting time on the initial arc
changes by \([Y_\xi(\eta)-\xi]/2\). Define

\[
 H_r(\eta)=(8-2\eta)r(\eta)+\int_0^\eta r(t)\,dt-3\eta,
 \qquad J(x)=\int_0^x[d(t)-t]\,dr(t).
\]

Its exact residual is

\[
 4[C_\ell(1-\eta)-C_{\rm end}]
 =H_r(\eta)-\Omega(\eta)
 -J(\min\{h^{-1}(\eta),x_T\})+K_{\rm init}(\eta).          \tag{6}
\]

At \(\eta=h(x)\), incoming-front indifference becomes

\[
 J(x)=H_r(h(x))-\Omega(h(x))
       +\int_{h(x)}^x[Y_\xi(h(x))-\xi]\,dr(\xi).          \tag{7}
\]

The endpoint four-cost is unchanged by the initial arc:

\[
 4C_{\rm end}=4+\int_{-1}^1L(1,V)\,dV
                         +\int_0^{x_T}d(t)\,dr(t).      \tag{8}
\]

## 3. A field formulation that eliminates the incoming front

The identities in this section are more general than the initial-arc
plus constant-\(U\) class in Section 1. They apply to an arbitrary ordered
high prefix that has reached its final outgoing characteristic by
\(U=1\), with the stated first-contact traces and no incoming plateau
on \(U=1\). In particular, the incoming motion can itself be curved
all the way to that row. The conditional cap construction in Section 4
is not an assumption of the row and column identities.

Let \(R_{\rm high}\) be the high sublaw's CDF, of total mass \(r_T\):

\[
 D(x,y)=r_T-R_{\rm high}(1-x,-1+y),\qquad
 e(y)=D(0,y)=r(d^{-1}(y)).                               \tag{9}
\]

This is a **high-submeasure deficit**. It equals \(1-R\) only where
\(L=q_0\). Where \(L<q_0\), rank ordering requires \(D=r_T\); using
\(1-R\) instead would count retained low mass twice.

Let \(d_T=d(x_T)\) and extend \(D(x,y)=r_T\) for \(y\ge d_T\).
The terminal field has the traces

\[
 D(x,x)=r(x),\quad D(0,y)=e(y),\quad
 D(x_T,y)=r_T\ (y\ge x_T),\quad D_x,D_y\ge0.              \tag{10}
\]

The initial positive correction is a column moment:

\[
 J_{\rm init}(y)=yr(y)-\int_0^yD(x,y)\,dx
 +\int_0^{d^{-1}(y)}h\,dr-\int_0^yh\,dr.                 \tag{11}
\]

Substituting it into the positive identities gives

\[
 4[C_g(1-y)-C_{\rm end}]
 =(8-y)e(y)+\int_0^yD(x,y)\,dx-\int_0^yd(t)\,dr(t).       \tag{12}
\]

For negative M1, the high part of the strict first-inverse row is
\(N_{\rm high}(1-\eta)=\int_\eta^{d_T}[r_T-D(\eta,y)]\,dy\).
Consequently,

\[
 4[C_\ell(1-\eta)-C_{\rm end}]
 =(8-2\eta)r(\eta)-3\eta-\Omega(\eta)
 -\int_\eta^{d_T}D(\eta,y)\,dy+\int_0^{d_T}e(y)\,dy.       \tag{13}
\]

Equations (4), (12), and (13), with zero residuals, are a coupled
column/row moment system. Unknowns can be \(r\), the outgoing trace
\(e\), and the two-dimensional field \(D\); then \(d=e^{-1}\circ r\).
No initial-speed fit or incoming map has to be frozen in this formulation.
It must still be combined with initial-inward inequalities and their
equality set, transport, the low-field obstacle, and outer traces.
The moments alone do not ensure those conditions.

At \(\eta=x_T\), (13) recovers the same outer scalar as before:

\[
 \int_0^{x_T}d\,dr=(8-x_T)r_T-3x_T-\Omega(x_T).           \tag{14}
\]

Curving the initial paths does not remove that matching obligation.

## 4. Conditional contraction for the incoming front

Alternatively supply the initial inverse family \(Y_\xi(\eta)\).
Assume \(0<x_T\le10^{-5}\),

\[
 \frac4{5\sqrt x}\le r'(x)\le\frac1{\sqrt x},\qquad
 3\sqrt x\le w(x)\le5\sqrt x,\qquad w=d+h,
\]

and \(\Omega(0)=0,\ 0\le\Omega'\le8000\) on
\(0\le\eta\le(4/25)x_T^2\). Suppose also
\(Y_\xi(\xi)=\xi,\ -1\le\partial_\eta Y_\xi\le0\).
For each \(x\), set

\[
 K_x(\eta)=\int_\eta^x[Y_\xi(\eta)-\xi]\,dr(\xi),\qquad
 A_x(\eta)=H_r(\eta)-\Omega(\eta)+K_x(\eta),\qquad
 W(x)=\int_0^x[w(t)-t]\,dr(t).
\]

The initial-inverse bounds imply

\[
 0\le K_x(\eta)\le\frac23x^{3/2},\qquad
 \partial_\eta K_x(\eta)\ge-2\sqrt x.
\]

Together with the other assumptions they give

\[
 A_x'(\eta)\ge\frac6{\sqrt\eta}
 \quad\text{for}\quad 0<\eta\le\frac4{25}x^2.             \tag{15}
\]

On the closed box \(x^2/50\le h(x)\le4x^2/25\), define

\[
 T[h](x)=A_x^{-1}\left(W(x)-\int_0^xh(t)\,dr(t)\right).   \tag{16}
\]

At the lower trial value, \(A_x\le2.266x\), while the argument in (16)
exceeds \(2.398x\). At the upper trial value, \(A_x>5.107x\), while the
argument is at most \(5x\). Thus the box is invariant. The inverse
derivative bound gives

\[
 \|T[h_1]-T[h_2]\|_*
 \le\frac2{75}x_T^{3/2}\|h_1-h_2\|_*,
 \qquad \|h\|_*=\sup_{0<x\le x_T}\frac{|h(x)|}{x^2}.      \tag{17}
\]

This proves a unique fixed point for the supplied \(r,w,\Omega,Y\).
Differentiating its implicit equation gives

\[
 h'(x)=\frac{[d(x)-Y_x(h(x))]r'(x)}{A_x'(h(x))}.          \tag{18}
\]

Here \(Y_x\) means the path indexed by \(\xi=x\), not a partial
derivative. Since \(Y_x(h)\le2x\) and \(d=w-h\), the numerator is
positive on this box, and \(h'\le x/3\). If also \(w'\ge1/\sqrt x\),
then \(d'>0\).

This is an exact conditional component. It does not solve the positive
equations or produce an active initial-inward field. An arbitrary
supplied inverse family need not have the unit tangent or curvature
required by active inward responses.

### The same incoming component as a row-cap projection

For a supplied uncapped initial field \(Z\), define

\[
 D_i(x,y)=\max\{e(y),\min\{i(x),Z(x,y)\}\}.
\]

Here \(Z\ge e\), and \(r(x)\le i(x)\le r_T\). The negative-M1 moment
is the scalar equation

\[
 M_x(i):=\int_x^{d_T}D_i(x,y)\,dy
 =(8-2x)r(x)-3x-\Omega(x)+\int_0^{d_T}e(y)\,dy.          \tag{18a}
\]

Let \(b_x(i)\) be the initial field's rank-\(i\) crossing, and
\(w(i)=e^{-1}(i)\). If \(b_x(i)<w(i)\), differentiation gives
\(M_x'(i)=w(i)-b_x(i)>0\). Equivalently,

\[
 \int_0^iw(q)\,dq
 -\int_{r(x)}^iY_{r^{-1}(q)}(x)\,dq
 =(8-x)r(x)-3x-\Omega(x).                              \tag{18b}
\]

Thus negative M1 fixes the incoming cap while this equation has an
unsaturated root. It does not fix the outgoing trace \(e\) by itself.
Once \(i=r_T\), a failed row equality is an outer-source obligation;
one must not continue the cap beyond the total high mass.

For fixed \(r,e,\Omega\), this projection is nonexpansive under a
useful separation condition. Consider a straight interpolation between
two supplied fields \(Z\), and suppose every interpolating row-cap
solution has

\[
 \frac{b_x(i)-x}{w(i)-b_x(i)}\le\kappa\le1.             \tag{18c}
\]

A sup-norm perturbation \(\epsilon\) changes the moment before adjusting
the cap by at most \((b_x(i)-x)\epsilon\). The cap derivative therefore
has magnitude at most \(\kappa\epsilon\). Clipping the field is
nonexpansive in both its field and cap arguments, so the resulting
\(D_i\) changes by at most \(\epsilon\).

The outward-speed box above gives (18c) with room to spare. If
\(i=r(\xi)\), then \(b_x(i)\le2\xi-x\), whereas
\(w(i)=d(\xi)\ge3\sqrt\xi-(4/25)\xi^2\). For
\(\xi\le10^{-5}\), the ratio in (18c) is less than \(0.00212\).
This is a conditional estimate for feasible unsaturated rows, not an
assertion that arbitrary outer sources have such roots.

Transport also requires the selected \(i(x)\) to be nondecreasing.
For a differentiable initial inverse its derivative obeys

\[
 [w(i)-b_x(i)]i'(x)
 =(8-2x)r'(x)-r(x)-3-\Omega'(x)
   +\int_{r(x)}^i\partial_xY_{r^{-1}(q)}(x)\,dq.
 \tag{18d}
\]

In the small incoming region covered by Section 4, the stated derivative
bounds make the right side positive. Beyond that region a saturated cap
is kept fixed and the low source is adjusted as below. Variations of
\(r,e,\Omega\) belong to the joint outer block and are not covered by the
fixed-front nonexpansiveness assertion.

## 5. Low-field warp and the full order obstacle

For \(h_T\le\eta\le x_T\), negative-M1 equality now requires

\[
 \Omega_*(\eta)=H_r(\eta)-J(x_T)+K_{x_T}(\eta).           \tag{19}
\]

If this is increasing, lies in the old source's range, and matches its
values at both slab edges, the coordinate change is

\[
 \phi(1-\eta)=1-\Omega_{\rm old}^{-1}(\Omega_*(\eta)),
 \qquad L_{\rm new}(U,V)=L_{\rm old}(\phi(U),V).          \tag{20}
\]

The correction \(K\) must be retained. At \(\eta=x_T\) it vanishes,
so (14) is still the outer endpoint condition.

The old single-valley domination argument used initial speed \(+1\).
It does not cover the curved arc. The complete field must instead obey

\[
 L_{\rm new}(U,V)<q_0\quad\Longrightarrow\quad
 D(1-U,1+V)=r_T.                                       \tag{21}
\]

On the boundary high initial arc, the explicit condition is

\[
 L_{\rm old}\left(
 1-\Omega_{\rm old}^{-1}(\Omega_*(\eta)),
 -1+Y_{x_T}(\eta)\right)=q_0,
 \qquad h_T\le\eta\le x_T.                              \tag{22}
\]

The incoming and outgoing legs still admit the speed-bound comparison
from a correctly ordered valley. The arc obstacle, valley, and initial
support must all hold; row moments cannot replace them.

## 6. Active-corridor scope of the first-turn gate

On a varying active initial-inward patch, the exact derivative requires
\(e(y)<r(x)\). On the initial arc of rank \(\xi\),
\(x=\chi_\xi(y)\). If equality is assumed along the *entire* initial
arc to its first turn, this yields

\[
 b(\xi)\le d(h(\xi)).                                  \tag{23}
\]

This is a condition on that proposed active corridor. It does not follow
from all inward inequalities alone, because outside the equality set
responses may have positive slack.

The distinction has an exact check. Put \(x=h(\xi)\), \(b=b(\xi)\),
and \(i=r(\xi)\). At this first-turn corner,

\[
\begin{aligned}
 4[C_I(1-x,-1+b)-C_\ell(1-x)]
 ={}&x[3+2r(x)-i]+\Omega(x)\\
 &-(8-b)[r(x)-e(b)]_+
   -\int_0^x[r(x)-D(t,b)]_+\,dt .
\end{aligned}                                         \tag{24}
\]

For its derivation, the outgoing tail of the row is \(D=i\) from \(b\)
to \(d(\xi)\), followed by \(D=e\). Substitute that row decomposition
into (13) and the exact initial-inward cost formula.
If \(e(b)\ge r(x)\), both positive-part terms vanish. The remaining
quantity is strictly positive. Even when negative M1 is matched, this
corner has positive inward slack; it is not itself an attack.

For an actually active corner, (24) gives a quantitative separation.
Set \(S=x[3+2r(x)-i]+\Omega(x)\) and
\(\Delta=[r(x)-e(b)]_+\). Transport gives

\[
 0\le\int_0^x[r(x)-D(t,b)]_+\,dt\le x\Delta.
\]

If both costs at that corner match, then

\[
 \frac{S}{8-b+x}\le\Delta\le\frac{S}{8-b}.               \tag{25}
\]

In particular, \(\Omega\ge0\) and \(i\le1\) imply
\(\Delta\ge2x/(8-b+x)>0\). Thus an active cap entry must have a
positive rank gap of order \(x\); placing it exactly at \(B=A\)
cannot meet the two equalities.

The locally audited unit-tangent germ has golden-ratio exponent when
inward equality touches the diagonal. It does not justify extending one
power arc uniformly to the incoming turn. That extension and resulting
power estimates for (2)-(3) are additional hypotheses; they are not used
in the contraction above.

## 7. An exact source for a free second monster turn

Keep the terminal outgoing gap, and suppose the strict radial CDF at the
initial inward turn is \(L\ge q_0\). The retained low ranks lie below
that turn and enter its later \(\alpha(s)\) first-inverse contribution.
Write the start and first turn as
\(a=1-x,\ v=-1+y\), and its second turn as \(s=1-k\), where
\(0\le k\le x\le y\). Put

\[
 D_0=D(x,y),\qquad
 m(z)=\min\{r(x),D(z,y)\},\qquad
 F(z)=\int_y^{d_T}[D(z,t)-D_0]_+\,dt .
\]

The exact change from second turn \(U=1\) is

\[
\begin{aligned}
 T_I(k;x,y)
 &:=
 4[C_I(1-x,-1+y,1)-C_I(1-x,-1+y,1-k)]\\
 &=k(3-D_0)+\Omega(k)+F(k)-F(0)
   +\int_0^k m(z)\,dz\\
 &\quad -(8-y-k)m(k)+(8-y)m(0).
\end{aligned}                                         \tag{26}
\]

This formula does not assume a constant incoming block. To derive it,
the general second-turn derivative has its low-rank inverse contribution
\(\Omega'(z)\), high-rank contribution \(F'(z)\), and column record
\(m(z)\). With the center and outgoing-row terms zero in this gap,

\[
 4\partial_s C_I
 =3-D_0+2m(z)+\Omega'(z)+F'(z)-(8-y-z)m'(z),
 \qquad z=1-s.
\]

Integration by parts gives (26). The same identity follows directly
from the first-contact CDF formula; the verifier checks it across
piecewise-linear branches rather than assuming differentiability.
At \(k=x\), the middle outward leg has zero length, and the route is
exactly the negative-M1 sweep by reflection.

For a selected positive-M2 second turn \(s_g(x)=1-k(x)\), set
\(T_g(x)=T_I(k(x);x,x)\). Since its first inward leg has zero length,
the corrected positive equalities are

\[
 (8-2x)e(x)=x[3-r(x)]+Q(x)+T_g(x),                     \tag{27}
\]

\[
 \int_0^x d\,dr
 =(8-x)e(x)+\int_0^xD(t,x)\,dt-T_g(x).                 \tag{28}
\]

These retain every high-prefix and low-source contribution. Selecting
the second turn, proving its optimality, and finding the active initial
start/turn surface remain part of the coupled problem.

### Conditional incoming-ridge simplification

For the constant-\(U\) incoming class only, let
\(k(y)=h(d^{-1}(y))=i^{-1}(e(y))\). Assume that every high rank below the
initial turn rank has finished its incoming motion by this second turn.
Between \(1-k(y)\) and \(1\), the column is at its outgoing cap,
\(m(z)=e(y)\) when \(B>A\), and \(F(z)\) is constant. Then (26) reduces to

\[
 T_I=k(y)[3-D(x,y)+2e(y)]+\Omega(k(y)).                 \tag{29}
\]

At \(y=x\), this is the explicit correction to the two positive
equations. In the Section 4 box,
\[
 \frac{dk}{de}=\frac{h'(\xi)}{r'(\xi)}
 \le\frac5{12}\xi^{3/2},\qquad \xi=r^{-1}(e),
\]
so the implicit outgoing-trace update in (27) has a small derivative.
This is a conditional response component, not a matching-law claim.
In particular, putting all second turns on one surface \(s=S(v)\)
must still pass the upper variation in the outgoing cutoff: positive
column mass on a ridge can create an upward cutoff kink. The general
formula (26) allows the second-turn support to move instead of freezing
that ridge.

## 8. Verification and remaining construction

Run:

~~~sh
python -B packages/interval_turn_density/verify_curved_terminal_sources.py
~~~

It passes 25,610 exact checks. Direct first-contact integration is compared
with corrected positive and negative costs, the unchanged positive
difference, both field moments, and the corner identity. Fixtures have
several initial speeds, nonzero low post/prefix sources, and cases on both
sides of the incoming cutoff. They include 96 corner reductions and
88 strict positive-slack corner cases. These checks establish identities,
not their simultaneous solvability.

The additional 2,464 checks use paths with strictly changing \(U\)
throughout the incoming phase, ending their inward motion at \(U=1\).
They independently verify (4), (8), (12), and (13) without a constant-\(U\)
incoming block. The corresponding inverse graphs do not satisfy the
outward-speed hypothesis of Section 4, and no cap-contraction claim is
made for them.

There are also 114 exact ridge checks and 420 general free-second-turn
checks. The latter include all row/column terms, fully curved incoming
paths, moving positive-M2 turns, and 60 collapsed-leg comparisons with
the independent negative-M1 capture route.

The remaining joint problem is to find \(r,e,D\) and outer data satisfying
the moments, the full initial-inward obstacle with its moving active set,
transport, and the retained-field order obstacle. The contraction supplies
\(h\) when the other initial data are given; the row/column formulation
lets those data move. Neither formulation yet supplies a complete
matching law.
