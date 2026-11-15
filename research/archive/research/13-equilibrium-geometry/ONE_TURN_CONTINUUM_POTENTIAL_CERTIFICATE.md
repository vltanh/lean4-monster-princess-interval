# A finite exact certificate for continuum one-turn Monster densities

This note gives a sufficient all-Princess upper certificate for a physical
one-turn Monster law with piecewise constant start densities. The finite
certificate consists of rational quadratic potentials and rational
inequalities. It includes finitely many turn levels on either side of one,
initially crossed characteristic boundaries, endpoint atoms, and arbitrary
Princess paths.

The method is a new certificate class, not a proof that these Monster
families contain an optimum. A discovery objective is not an exact upper
until the physical inequalities have been replayed and repaired. The frozen
comparison target remains

\[
 U_* = \frac{291849329389899}{204800000000000}.
\]

The retained continuum certificate now proves

\[
 W_1\le C_{\mathrm{cont}}
 =\frac{142472349375511}{100000000000003}
 \approx1.4247234937550672
 <\frac{57}{40}<U_*.
\]

Thus the frozen strict-separation target \(W_1>U_*\) is disproved by a
physical one-turn law. The complete law and potential are frozen as exact
integer data; independent replay checks 730,146 rational inequalities with
zero residual repair. This does not identify the exact one-turn value or
prove that the displayed density families or mesh contain an optimum.
The complete comparison status is recorded in
[the subgame bracket](ONE_TURN_SUBGAME_BRACKET.md).

## 1. The physical Monster law

Let \(E\) be the fair pair of immediate endpoint-to-endpoint sweeps. Define
an oriented endpoint-first route \(S(a)\), for \(-1<a<1\), by

\[
 (0,a),\qquad (1-a,1),\qquad (3-a,-1).
\]

For \(0<b<2\), define

\[
\begin{split}
 P_b(a):\quad &(0,a),\\
 &\left(\frac{b-a}{2},\frac{a+b}{2}\right),\\
 &(b+1,-1),\qquad (b+3,1),
\end{split}                                                    \tag{1}
\]

with the start restricted to

\[
 I_b=[-\min(b,1),\ \min(b,2-b,1)].                              \tag{2}
\]

Thus \(I_b=[-b,b]\) when \(b\le1\), and \(I_b=[-1,2-b]\) when
\(b\ge1\). Almost every start in this interval gives a genuine legal
one-turn route with nonnegative turning position. Each route is paired
with its reflection. Endpoint and zero-duration degeneracies occur only
on finitely many density boundaries and have zero probability. They may
be assigned their canonical endpoint representatives without changing the
law.

Choose a finite set \(\mathcal B\subset(0,2)\), a number \(q\ge0\), and
nonnegative piecewise constant densities \(\sigma\) and \(\pi_b\).
The support of \(\sigma\) is \([-1,1]\); the support of \(\pi_b\) is
\(I_b\). Normalize by

\[
 q+\int_{-1}^{1}\sigma(a)\,da+
       \sum_{b\in\mathcal B}\int_{I_b}\pi_b(a)\,da=1.           \tag{3}
\]

The law chooses \(E\) with probability \(q\), a reflected \(S(a)\)
pair with density \(\sigma(a)\,da\), and a reflected \(P_b(a)\) pair
with density \(\pi_b(a)\,da\). All pair weights include the fair choice
of orientation. Write

\[
 \Sigma(z)=\int_{-1}^{z}\sigma(a)\,da,
 \qquad \Pi_b(z)=\int_{-1}^{z}\pi_b(a)\,da,
 \qquad M_b=\Pi_b(1),                                        \tag{4}
\]

extending these cumulative functions constantly outside their supports.

Every route visits the center by time two. For \(S(a)\), the first visit
is at \(-a\) when \(a\le0\), and at \(2-a\) when \(a>0\). For
\(P_b(a)\), it is at \(-a\) when \(a\le0\), and at \(b\) when
\(a>0\). The support restriction (2) makes these times at most two.
All routes complete their endpoint sweep before time five.

The physical membership statement is a special case of
[the complete one-turn domain theorem](ONE_TURN_COMPLETE_DOMAIN.md).
The fair stationary-endpoint Princess supplies the exact test value

\[
 B_{\mathrm{end}}
 =q+\int_{-1}^{1}(2-a)\sigma(a)\,da
       +\sum_{b\in\mathcal B}(b+2)M_b.                       \tag{5}
\]

Every claimed all-Princess upper for this law must be at least (5).

## 2. Why the response reduction covers every Princess

Reflection symmetry first permits symmetrizing a Princess law. The ordered
quantile normalization then replaces it by a mixture of fair reflected
radial paths without decreasing its payoff against any fixed Monster.
This is the same reflection and ordering reduction used in
[the physical upper proof](ONE_TURN_PHYSICAL_UPPER.md). It imposes no
Princess turn bound.

For the present law, radial motion may additionally be made maximally
outward after time two. To see this, fix a surviving positive radial target
at time two. The Monster has already visited zero. If it had subsequently
passed from the target's inner side to its outer side, it would have met
the target. Thus it is still on the inner side. Replacing the target's
future by

\[
 p(t)=\min\{1,p(2)+t-2\},\qquad t\ge2,                       \tag{6}
\]

cannot advance its first capture. Continuity gives an old contact no later
than any new contact. The negative target is identical after reflection.
Initial coincidences have already been counted at time zero.

It therefore suffices to bound legal radial paths on \([0,2]\), followed
by (6). For deriving the formula, take a strict radial path satisfying
\(0<p(t)<1\) and having Lipschitz constant strictly smaller than one on
\([0,2]\). Arbitrary radial paths follow by applying

\[
 p_\epsilon(t)=(1-2\epsilon)p(t)+\epsilon,
 \qquad 0\le t\le2,
\]

and then using (6). These legal paths converge uniformly on the relevant
bounded horizon. First capture is jointly lower semicontinuous under
uniform convergence of continuous paths. Fatou's lemma therefore passes
a common upper for the approximating Princesses to the original one.
The argument retains center and endpoint atoms and actual time-zero
capture. It does not replace closed contact by an avoided trace.

The center deadline is used specifically for (6). The more general
inverse-curve upper oracle does not require that deadline; this note's
short-horizon potential formula does.

## 3. An exact payoff formula, including initial crossings

For a strict radial path let

\[
 r=p(0),\qquad s=p(2),\qquad U(t)=t+p(t),\quad W(t)=t-p(t).
\]

Both light coordinates are strictly increasing on \([0,2]\), and
\(U\ge W\). Let \(A(r)\) be the already-crossed-boundary contribution

\[
 A(r)=\sum_{\substack{b\in\mathcal B\\b\le r}}(b+3)M_b.      \tag{7}
\]

Only levels \(b<1\) can contribute for a strict initial radius. The
right trace at \(r=b\) is understood in (7).

The contribution of the endpoint-sweep component to the running cost of
**twice** the expected capture time is

\[
 G_E(U,W)=q\bigl(\mathbf 1_{U<1}+\mathbf 1_{W<1}\bigr).       \tag{8}
\]

The endpoint-first component contributes

\[
\begin{split}
 G_S(r;U,W)={}&\Sigma(-U)+\Sigma(-W)\\
 &+[\Sigma(2-U)-\Sigma(r)]_+
       +\Sigma(2-W)-\Sigma(-r).                             \tag{9}
\end{split}
\]

For a turn level \(b\), put

\[
 G_b(r;U,W)=
 \begin{cases}
  2M_b-\Pi_b(r)-\Pi_b(-r)+\Pi_b(-U)+\Pi_b(-W),&U<b,\\
  M_b-\Pi_b(-r),&U\ge b>W,\\
  0,&W\ge b.
 \end{cases}                                                \tag{10}
\]

If \(r<b\), let \(\tau_b\) be the first time \(U=b\). It occurs
before time two and contributes the jump reward

\[
 J_b(W)=\left(b+3-\frac{b+W}{2}\right)\Pi_b(-W).              \tag{11}
\]

There is no reward at \(W=b\). The terminal contribution at time two is

\[
\begin{split}
 K(r,s)={}&\int_{-r}^{s}(1-a)\sigma(a)\,da\\
 &+\sum_{\substack{b\in\mathcal B\\ b>1,\ 2-s<b}}
           (b-1)\bigl[M_b-\Pi_b(-r)\bigr].                  \tag{12}
\end{split}
\]

With \(G=G_E+G_S+\sum_bG_b\), the exact expected payoff is

\[
 \boxed{
  2J(p)=A(r)+\int_0^2G(r;U(t),W(t))\,dt
       +\sum_{\substack{b\in\mathcal B\\r<b}}
            J_b(W(\tau_b))+K(r,s).
 }                                                           \tag{13}
\]

### Where the terms come from

Here is a direct capture-time derivation. Write \(\tau_U(c)\) and
\(\tau_W(c)\) for the first times the corresponding increasing light
coordinate reaches \(c\), using the actual outward continuation after
time two. For the strict pre-two paths under consideration, all relevant
pre-two crossings are unique.

For \(S(a)\), the positive and negative Princess captures are

\[
\begin{array}{c|cc}
 &\text{first case}&\text{second case}\\ \hline
T(S(a),p)&\tau_W(-a),\ a<r&\tau_U(2-a),\ a>r\\
T(S(a),-p)&\tau_U(-a),\ a<-r&\tau_W(2-a),\ a>-r.
\end{array}                                                   \tag{13a}
\]

These are actual first contacts: a unit-speed outgoing Monster cannot
catch a target initially behind it, and after the endpoint its opposite
unit-speed leg meets the target at the displayed light-coordinate level.
The equality cases \(a=\pm r\) are initial captures; each is a null slice
of the start density. For example, integrating the first case in the first
row at time \(t\) gives \(\Sigma(-W(t))\); integrating the second gives
\([\Sigma(2-U(t))-\Sigma(r)]_+\). The other row gives the remaining
two terms of (9). If \(a\in(-r,s)\), the last crossing in (13a) occurs
at endpoint time \(3-a\), so its post-two remainder is \(1-a\).
All other \(S\) captures occur by time two. This proves the first term
of (12) as well.

For \(P_b(a)\) with \(r<b\), put
\(\tau=\tau_U(b)\) and \(c=-W(\tau)=b-2\tau\). Then
\(-b<c<r\), and, away from the null start slices \(a=c,r,-r\),

\[
T(P_b(a),p)=
\begin{cases}
 b+3,&a<c,\\
 \tau_W(-a),&c<a<r,\\
 \tau,&a>r,
\end{cases}
\qquad
T(P_b(a),-p)=
\begin{cases}
 \tau_U(-a),&a<-r,\\
 \tau_W(b),&a>-r.
\end{cases}                                                   \tag{13b}
\]

To check the nontrivial first split, the Monster turns at
\(h=(b-a)/2\). A positive target initially above the Monster is met
on its first leg precisely when \(U(h)<b\), equivalently \(h<\tau\)
or \(a>c\). If \(a<c\), the target is still above the Monster at the
turn; the leftward leg moves away from it. On the final rightward leg the
Monster has \(W=b+2>2\), whereas the target has \(W\le2\) until
its own endpoint stop under (6). Its capture is therefore exactly at
\(b+3\). The negative-target cases follow from the first rightward
crossing of \(U=-a\) or the subsequent leftward crossing of \(W=b\).

Before \(\tau\), (13b) gives positive survival mass
\(M_b-\Pi_b(r)+\Pi_b(-W(t))\) and negative survival mass
\(M_b-\Pi_b(-r)+\Pi_b(-U(t))\). After \(\tau\), the still-uncaught
positive mass is \(\Pi_b(c)\), all caught at \(b+3\); its remaining
integral is exactly \((b+3-\tau)\Pi_b(c)\). The remaining negative
mass is \(M_b-\Pi_b(-r)\) until \(W=b\). This proves both branches
of (10), the jump (11), and the absence of a \(W=b\) jump. If
\(W(2)<b\), that negative mass is caught at endpoint time \(b+1\),
which gives the second term of (12).

All integrals use the declared absolutely continuous start densities, so
the omitted equality slices carry no probability. The separate endpoint
atom is retained exactly in (8). The strictification argument of Section 2
then restores arbitrary Princess path contacts; it is not an assumption
that an arbitrary Princess avoids characteristic contact.

If \(r\ge b\), the initial \(U=b\) boundary has already been passed.
The support condition \(a\le b\le r\) means that one reflected member
is caught at its final endpoint time \(b+3\). That contributes
\((b+3)M_b\) at time zero. Its other member retains the running term
\(M_b-\Pi_b(-r)=M_b\) until \(W=b\). This proves (7), including the
initially crossed case that would be lost by simply omitting an unavailable
\(U\)-crossing time.

At \(r=b<1\), the pre-crossing limit of (11) is
\((b+3)\Pi_b(r)=(b+3)M_b\). Thus the two initial traces fit together
with the same explicit jump reward. Both neighboring traces are retained
in the finite certificate.

If \(W(2)<b\), then necessarily \(b>1\). Under (6), the still-uncaught
record reaches its relevant endpoint at time \(b+1\). The post-two
remainder is exactly the second line of (12). At \(W(2)=b\), actual
contact occurs at time two, whereas the pre-crossing limiting trace may
have the positive remainder in (12). The phase on the \(W<b\) side
retains that limiting terminal value, including its boundary endpoint;
the post-crossing phase retains the actual zero remainder. This gives a
valid upper at both traces.

An independent exact check integrates actual chronological captures over
the complete one-dimensional start arrangement. It agrees with (13) on
77 rational full-support fixtures and 308 separate density-subinterval
fixtures. These include eleven starts already beyond \(U=b\), four starts
exactly on that boundary, and six late-\(W\) terminal cases among the
full-support fixtures. Interior waits and several varying subunit Princess
paths are included.

## 4. A short-horizon potential certificate

Use the physical light-coordinate domain

\[
 \mathcal P=\{(U,W):0\le U-W\le2,\ 0\le U+W\le4\}.           \tag{14}
\]

Let the ordered levels be \(\{1\}\cup\mathcal B\). A phase is indexed
by the number of those levels already crossed by \(U\) and by \(W\).
Only nonempty phase regions are used. The state has the initial radius
\(r\), the two current light coordinates, and this phase. No history of
individual crossings beyond their current order is needed.

For each phase \(k\), let \(V_k(r;U,W)\) be a continuous, piecewise
continuously differentiable potential inside that phase. Distinct phase
traces may differ at a boundary. It is sufficient to verify the following
inequalities:

\[
 2(V_k)_U+G_k\le0,
 \qquad 2(V_k)_W+G_k\le0.                                  \tag{15}
\]

Across \(U=b\), require

\[
 V_{\rm pre}\ge J_b+V_{\rm post}.                           \tag{16}
\]

If the boundary is \(U=1\) and no \(P_1\) component is present, its
jump reward is zero. Across every \(W\)-level require

\[
 V_{\rm pre}\ge V_{\rm post}.                              \tag{17}
\]

On the time-two terminal edge of each phase require

\[
 V_k(r;2+s,2-s)\ge K_k(r,s),                                \tag{18}
\]

where the subscript retains the appropriate strict or pre-crossing trace
from (12). Finally, on each initial phase interval require

\[
 A(r)+V_{k(r)}(r;r,-r)\le2C.                               \tag{19}
\]

**Certificate theorem.** Conditions (15)--(19) imply
\(J(p)\le C\) for every legal Princess path and hence for every Princess
law.

Indeed, \(U'=1+p'\), \(W'=1-p'\), and these nonnegative derivatives
sum to two. Equation (15) gives \(dV/dt+G\le0\) almost everywhere.
Continuity inside each phase handles all mesh crossings, including paths
that cross an internal triangle edge infinitely often. Each phase crossing
releases at least its specified reward by (16) or (17). Adding the
terminal and initial inequalities telescopes to (13). Strictification
and lower semicontinuity then give the complete physical scope established
in Section 2.

## 5. Why finitely many rational inequalities suffice

Choose rational density knots, rational initial-radius knots, and a rational
triangulation of (14). All density break lines in the arguments
\(-U,-W,2-U,2-W\), and every phase level, must be included in the
spatial mesh. The initial-radius partition contains the positive and
negative density knots and every initial crossing level \(b<1\).

A practical mesh starts with positive knots from zero to one and extends
them by an odd map of period two. Applying that same map to both light
coordinates keeps the physical boundary diagonals aligned. The triangular
connectivity is fixed, but gradients are computed in the resulting physical
coordinates. Quadratic edge nodes are physical arithmetic midpoints; they
are not images of old midpoints under the grading map.

For each initial-radius knot, use continuous quadratic Lagrange potentials
(P2) on every phase triangle, with separate copies across phase boundaries.
For fixed \(r\), every cumulative term in \(G\) is affine on a triangle.
The only remaining hinge is the positive part in (9), which is convex.
Since a P2 first derivative is affine, each left side of (15) is convex
on the triangle. Its three vertex inequalities therefore imply the whole
triangle inequality. Aligning the hinge itself is optional.

The branch of the hinge at a given vertex is determined by whether
\(2-U\ge r\), because the density is nonnegative. Hence its coefficients
are linear in the unknown density masses. All other constraints are also
linear in the masses and potential values. This is a finite linear program
for discovery, followed by exact rational replay.

On an edge, (16)--(18) are quadratic inequalities. Given their values
\((f_0,f_{1/2},f_1)\), the three quadratic Bernstein coefficients are

\[
 f_0,\qquad 2f_{1/2}-\frac{f_0+f_1}{2},\qquad f_1.            \tag{20}
\]

Nonpositivity of these coefficients certifies a nonpositive residual on
the entire edge. This is a sufficient test; it does not assert that every
nonpositive quadratic has nonpositive coefficients in this representation.

### Interpolating the initial radius

Between two radius knots, interpolate the endpoint potentials linearly in
\(r\). On such an interval all \(\Pi_b(\pm r)\) and
\(\Sigma(\pm r)\) terms are affine. The positive part in (9) is convex
in \(r\). Consequently the running cost is bounded above by the linear
interpolation of its endpoint values. The two endpoint versions of (15)
therefore prove the interior versions.

The jump (11) is independent of \(r\). The terminal integral has second
derivative \(\sigma(-r)\ge0\) on each aligned interval, while the
additional \(P_b\) terminal terms are affine in \(r\). Thus interpolation
also preserves (16)--(18).

Along \((U,W)=(r,-r)\), each endpoint potential has a quadratic trace.
Multiplying by the linear interpolation weights gives a cubic. The initial
bonus (7) is constant on each initial phase interval. Four cubic Bernstein
coefficient inequalities certify (19), with each physical edge restricted
as necessary to the chosen radius subinterval. Both sides of an initial
phase boundary are checked. The method therefore does not merely sample
Princess initial positions.

Cumulative-CDF auxiliary columns may be used to keep the numerical matrix
sparse. Their constraints are exactly
\(C_j-C_{j-1}=m_j\). Eliminating them recovers the density-mass program
coefficient-for-coefficient. Exact replay reconstructs all cumulative
functions directly from the actual masses and ignores the auxiliary
columns.

## 6. Exact repair of a rounded numerical potential

A floating optimizer need not return an exactly feasible vector. Round its
mass and potential values to rational numbers, make all density masses
nonnegative with the required supports, and normalize their total exactly.
Rebuild every physical coefficient from these data. No floating residual,
saved geometry table, or optimizer success flag is a certificate.

Let \(\delta_H\ge0\) be the largest positive HJB vertex residual. For
each phase edge \(k\to l\), let \(\delta_{kl}\ge0\) be the largest
positive Bernstein residual of its boundary inequality. Let
\(\delta_{T,k}\ge0\) bound the terminal residuals of phase \(k\), and
let \(\delta_I\ge0\) bound all initial cubic residuals. All maxima are
taken over every radius knot or initial-radius interval as appropriate.

The phase graph is acyclic: a crossing increases the number of crossed
\(U\)- or \(W\)-levels. Define, backward on this graph,

\[
 \beta_k=\max\left\{0,\delta_{T,k},
                 \max_{k\to l}(\delta_{kl}+\beta_l)\right\}.
                                                                    \tag{21}
\]

Set \(t=(U+W)/2\), and correct the potentials by

\[
 \widetilde V_k=V_k+\delta_H(2-t)+\beta_k.                    \tag{22}
\]

The added time term has \(2\partial_U=2\partial_W=-\delta_H\),
so it repairs (15). It cancels at each phase interface and is zero at time
two. Equation (21) repairs every boundary and terminal residual.

Let \(\beta_{\rm init}\) be the largest \(\beta_k\) among phases that
meet the initial edge. Then

\[
 \boxed{\widetilde C
       =C+\delta_H+\frac{\beta_{\rm init}+\delta_I}{2}}       \tag{23}
\]

repairs the initial inequalities as well. For levels all at least one,
only the initial phase \((0,0)\) is needed. Levels below one may produce
several initial phases, which is why (23) uses their maximum.

This proves an exact rational upper without an exact rational LP solve.
The correction may be small or large; either way its full value is included
in the reported bound. An explicit comparison gate accepts a counterexample
to the strict-separation target only when
\(\widetilde C\le U_*\).

## 7. The retained countercertificate and historical controls

An analytic endpoint-only potential is

\[
 V=
 \begin{cases}
  3-U-W,&U<1,\\
  2-(U+W)/2,&U\ge1>W,\\
  0,&W\ge1.
 \end{cases}
\]

Together with \(q=1\) and \(C=3/2\), it satisfies the entire certificate
with zero rational repair. Extra \(P_b\) phases carry identical copies
of the appropriate endpoint potential and zero density. This checks the
HJB sign, the interface direction, the terminal convention, and the factor
two in the initial bound.

### The retained exact law

The common positive mesh has 24 intervals: a uniform \(1/16\) bulk,
endpoint dyadics through \(1-1/4096\), and the endpoint one. The six turn
levels are

\[
 \mathcal B=\left\{\frac{15}{16},\frac{31}{32},1,
                 \frac{65}{64},\frac{33}{32},\frac{17}{16}\right\}.
\]

Write \(N=100000000000003\). The exact probabilities of the families are

| Physical family | Probability numerator over \(N\) |
|---|---:|
| Endpoint sweep \(E\) | 58,529,458,302,223 |
| Endpoint-first density \(S\) | 23,338,621,584,333 |
| \(P_{15/16}\) density | 2,557,066,763 |
| \(P_{31/32}\) density | 210,093,876,391 |
| \(P_1\) density | 16,091,292,591,464 |
| \(P_{65/64}\) density | 1,643,036,417,352 |
| \(P_{33/32}\) density | 83,345,115,201 |
| \(P_{17/16}\) density | 101,595,046,276 |

These numerators sum exactly to \(N\). The individual density-bin
masses and all P2 nodal numerators are stored in
[`one_turn_continuum_upper.json.gz`](../../packages/interval_one_turn/one_turn_continuum_upper.json.gz).
Its frozen-input SHA-256 is

```text
c87c7b902382396bce06e4265b6140077b50e336af48de5ff6d2f301af9dc482
```

The canonical input uses integer masses and integer potential numerators
with one exact normalization denominator. It has no CDF auxiliary values
and no floating optimizer values. The positive mesh, density supports,
phase labels, physical P2 node ordering, and every physical coefficient
are reconstructed by the verifier.

The [retained replay](../../packages/interval_one_turn/one_turn_continuum_upper_replay.json)
checks:

| Inequality family | Exact checks |
|---|---:|
| HJB derivatives at triangle vertices | 691,200 |
| \(U\)-boundary quadratic Bernstein coefficients | 19,050 |
| \(W\)-boundary quadratic Bernstein coefficients | 18,000 |
| Terminal quadratic Bernstein coefficients | 1,800 |
| Initial cubic Bernstein coefficients | 96 |
| **Total** | **730,146** |

Every positive residual is exactly zero. Therefore every phase offset in
(21), the HJB correction, the initial correction, and the total repair
in (23) are exactly zero. The rounded potential itself is feasible over
the full continuum of initial radii and legal radial paths.

The certified bound is

\[
 C_{\mathrm{cont}}
 =\frac{142472349375511}{100000000000003}.
\]

Its exact gap below the frozen benchmark is

\[
 U_*-C_{\mathrm{cont}}
 =\frac{6595786886122747988169697}
        {20480000000000614400000000000}
 \approx0.00032205990654895263>0.
\]

The simpler rational comparison \(C_{\mathrm{cont}}<57/40<U_*\)
also follows directly. The stationary-endpoint test (5), independently
computed from the stored masses, is

\[
 B_{\mathrm{end}}
 =\frac{4706174332466029}{3303225806451712}
 \approx1.4247207451801027,
\]

which is below the certified upper. This test is a consistency check for
the law; the 730,146 exact inequalities establish the all-Princess bound.

The certificate ranges over all Princesses by Sections 2--5. Its finite
mesh is a sufficient upper-potential construction, and its Monster law
is an actual continuum mixture of canonical one-turn paths. Neither a
finite sampled Princess bank nor a finite sampled Monster bank is used
to extend its scope. No optimality assertion over all one-turn laws is
needed for the strict benchmark comparison.

### Earlier control with levels at least one

Before adding the nearby turn levels used above, the same 24-interval
mesh with levels \(1,17/16,9/8,3/2\) gave the independently repaired
upper

\[
 \frac{129732862765992169}{91022222222221312}
 \approx1.4252877989427992.
\]

Its repair was approximately \(2.03\cdot10^{-9}\). That earlier
control had 691,200 HJB inequalities, 14,400 \(U\)-interface
inequalities, 9,150 \(W\)-interface inequalities, 1,800 terminal
inequalities, and 96 initial inequalities. It remained above \(U_*\).
The retained six-level law and its zero-repair integer certificate
supersede that comparison result.

## 8. Verification commands

Replay the retained countercertificate directly from the repository root:

```sh
python3 packages/interval_one_turn/verify_continuum_upper.py \
  packages/interval_one_turn/one_turn_continuum_upper.json.gz \
  --require-counterexample --output /tmp/one_turn_continuum_replay.json
```

This command requires only the Python standard library. It performs no
optimization and does not load the floating discovery program.

From the repository root, the standard-library controls are

```sh
python3 packages/interval_one_turn/verify_continuum_upper.py --self-test
python3 packages/interval_one_turn/verify_continuum_functional.py
```

The second command integrates actual segment-by-segment first captures;
it does not use the potential inequalities as its physical payoff oracle.
For a complete numerical P2 candidate containing the rational mesh, phase
node ordering, and nodal values, replay with

```sh
python3 packages/interval_one_turn/verify_continuum_upper.py candidate.json \
  --output exact_continuum_replay.json
```

Gzip-compressed candidate input is accepted. The default rounding scale is
\(10^{14}\); `--digits` changes that explicit rationalization. The report
includes the input SHA-256 hash, the normalized rational law, every class
of residual, the phase offsets, the complete repair, the exact upper,
and its signed difference from the frozen benchmark. The independently
reconstructed node ordering must agree with the candidate's declared
ordering. Auxiliary CDF values and saved optimizer residuals are ignored.

Add `--require-counterexample` to reject every candidate whose repaired
upper is greater than \(U_*\). The ordinary exact upper check and this
additional comparison gate are separate assertions.

For delivery, freeze the rounded discovery vector into the canonical integer
format and replay that exact input separately:

```sh
python3 packages/interval_one_turn/verify_continuum_upper.py discovery.json \
  --freeze-output continuum_certificate.json.gz
python3 packages/interval_one_turn/verify_continuum_upper.py \
  continuum_certificate.json.gz --output continuum_replay.json \
  --require-counterexample
```

The frozen format `one-turn-continuum-potential-v1` contains nonnegative
integer probability numerators, integer P2 nodal numerators, one positive
normalization denominator, and rational mesh data. It omits auxiliary CDF
columns. Its replay checks the exact probability sum and support restrictions
and performs no floating rationalization. The frozen input, rather than the
optimizer's success flag or log, is the physical proof artifact.
