# A finite lower-certificate LP with all endpoint continuations eliminated

This note is a sufficient certificate for the unrestricted interval game. It
uses one continuous potential, not a finite Monster bank. The finite mesh and
polynomial degree are restrictions on the *certificate*, so a feasible answer
is a global lower bound. No bound on the degree or mesh needed at equilibrium
is asserted.

The underlying full-clock representation is proved in the repository's
`research/12-global-closure/FINITE_STATE_PHYSICAL_CLOCK_LIFT.md`. The construction
below only uses its pathwise direction; it does not require an Eulerian
superposition theorem.

## 1. Princess field and the four clock controls

Let `F_int(t,x)` be a symmetric signed Princess CDF on the open interval. We
require continuity, `0 <= F_int <= 1`,

\[
 F_{\rm int}(t,-x)=1-F_{\rm int}(t,x),\qquad
 (F_{\rm int})_x\ge |(F_{\rm int})_t|,
 \qquad F_{\rm int}(t,x)=\tfrac12\quad(t\ge3).
\]

For a continuous piecewise-affine field the derivative inequalities are imposed
on each triangle. They imply the usual transport-cone inequalities and hence
realization by a common-quantile law of 1-Lipschitz Princess paths. The last
condition says that every Princess is at an endpoint by time 3. The
[sharp outward-time theorem](SHARP_OUTWARD_HORIZON_REDUCTION.md) now proves
that this class is value dense for the unrestricted game: forcing ordered
Princesses outward after time 2 preserves security. The finite certificate
remains sufficient for any supplied field in this class.

The actual strict CDF is

\[
 F^-(t,-1)=0,\qquad F^-(t,x)=F_{\rm int}(t,x)\ (-1<x<1),
 \qquad F^-(t,+1)=F_{\rm int}(t,+1).
\]

In particular the left endpoint's interior trace is generally positive.
Symmetry gives equal endpoint atom masses, but it does not make either endpoint
trace interchangeable with its strict point value.

The two full clocks have total mass 7 and satisfy the causal prefix condition.
At physical time `t`, write their credits as

\[
 q_+=\eta_+([0,t])-t,\qquad q_-=\eta_-([0,t])-t.
\]

The plus clock is the one that becomes free at Monster position `+1`. Its
charge cost is `F^-(t,-x)`. The minus clock becomes free at `-1` and has charge
cost `F^-(t,x)`. There is **no extra factor of one half**: the signed CDF already
includes the two fair Princess sides.

On the state `z=(t,x,q_+,q_-)`, the controls and costs are

| Control | Velocity | Cost per unit control |
|---|---|---|
| Move left | `(1,-1,-1,-1)` | `0` |
| Move right | `(1,+1,-1,-1)` | `0` |
| Charge plus | `(0,0,1,0)` | `F^-(t,-x)` |
| Charge minus | `(0,0,0,1)` | `F^-(t,x)` |

Convex combinations also cover velocities strictly between -1 and +1. Graph
completion turns clock atoms into charge-only segments. The coordinate
`ell=3t+q_++q_-` increases at unit speed under each of the four controls.

## 2. Why no visited-set or first-center mode is needed

Because the Princess is absorbed at the endpoints by time 3, take any Monster
path and retain its prefix through time 3. Among Princesses not yet caught,
only the stationary endpoints remain. Replace the Monster suffix by the
fastest tour visiting the endpoints in the same order as the original path.
This weakly advances both relevant endpoint hitting times. If one or both
endpoints are never visited by the original path, choose any completion
consistent with the visited order; all previously infinite remaining capture
times weakly decrease. From any position in `[-1,1]` the tour takes at most 4,
so the replacement completes by time 7.

There is also pointwise dominance after the first endpoint: from `+1`, the
fastest sweep to `-1` catches every remaining Princess no later than any other
Monster continuation. The reflected assertion holds from `-1`. This follows
by the intermediate value theorem, since the sweep stays weakly to the left
of every competing Monster until it reaches `-1`.

Thus, when certifying this particular absorbed Princess law against every
Monster, it suffices to study a path until the first of:

* its first endpoint visit;
* physical time 3;
* either clock credit reaching 4.

The third stopping rule is an analytic simplification, not a restriction on
Monster paths. At such a stop the continuation has an exact explicit lower
cost. Every clock trajectory starts with zero credits; initial clock atoms are
handled by the same charge controls before the stop. All relevant unknown
states therefore lie in the compact domain

\[
 \Omega=\{0\le t\le3,\ -1\le x\le1,\ 0\le q_+,q_-\le4\}.
\]

There is no first-center deadline and no discrete mode in this certificate.

## 3. The exact one-clock continuation

Define

\[
 L(t,x,q)=
 \begin{cases}
 \displaystyle\int_q^{1+x}F_{\rm int}(t+u,x-u)\,du,&q<1+x,\\
 0,&q\ge1+x.
 \end{cases}                                                    \tag{1}
\]

This is the minimum future cost of the minus clock if the plus-clock cost is
ignored. Move straight left from `x`. Existing credit pays for its first `q`
units of physical time; after that, charge at the current time until reaching
`-1`. All remaining clock mass can then be charged at `-1` for zero cost. This
attains (1).

For the converse, any legal Monster position at elapsed time `u` is at least
`x-u`. Spatial monotonicity gives a charge cost at least
`g(u)=F_int(t+u,x-u)` before the fastest possible hit of `-1`. The transport
inequality makes `g` nonincreasing. With current credit `q`, every future clock
must have charged at least `(u-q)_+` additional mass by elapsed time `u`.
First-order stochastic dominance for this decreasing nonnegative cost then
bounds its remaining cost below by `integral_q^(1+x) g(u) du`. This proves the
claim even for clocks with atoms.

A useful equivalent proof uses the light coordinates

\[
 a=t+x,\qquad b=t+q,\qquad
 C(a,b)=\left[\int_b^{a+1}F_{\rm int}(v,a-v)\,dv\right]_{{\rm empty}=0}.
                                                               \tag{2}
\]

Then `L(t,x,q)=C(t+x,t+q)`. Moving left leaves both arguments fixed. Moving
right increases `a` and leaves `b` fixed, which cannot decrease `C`. Charging
increases `b`, and its derivative is `-F_int(b,a-b)`; the transport cone makes
this at most the current charge cost in absolute value. If a derivative proof
expands `C_a`, the upper-limit term is the **interior trace**
`F_int(a+1,-1)`, which is nonnegative. It must not be replaced by the strict
point value zero.

### First-endpoint exits

At `x=+1`, the plus clock can be completed free. The exact continuation cost is

\[
 T_+(t,q_+,q_-)=L(t,1,q_-)
               =\int_{q_-}^{2}F_{\rm int}(t+u,1-u)\,du,          \tag{3}
\]

with the empty-integral convention. It does not depend on `q_+`. At `x=-1`,
the reflected exact cost is

\[
 T_-(t,q_+,q_-)=L(t,1,q_+).                                      \tag{4}
\]

These formulas explicitly account for the actual zero charge cost at the
endpoint already visited. The unknown interior potential is never propagated
through endpoint charge controls.

### Queue-credit exits

If `q_+=4`, move first left to `-1`, then right to `+1`. This tour takes at most
4, so the plus credit covers it until the plus clock becomes free. The minus
clock attains (1). Nonnegativity of the discarded plus cost gives the matching
lower bound. The exact continuation is therefore

\[
 Q_+(t,x,q_-)=L(t,x,q_-).                                        \tag{5}
\]

Similarly, at `q_-=4`,

\[
 Q_-(t,x,q_+)=L(t,-x,q_+).                                       \tag{6}
\]

The completion remains within time 7. Simultaneous exit faces have compatible
values; either can be used.

### The time-3 exit

At time 3 both Princess endpoints have mass one half. Before the corresponding
endpoint is first visited, each unit of uncredited clock costs one half. For
any fixed endpoint order, the shortest tour minimizes both first-visit times.
Consequently the exact remaining cost is

\[
 K(x,q_+,q_-)=\frac12\min\left\{
 (1-x-q_+)_++(3-x-q_-)_+,\quad
 (3+x-q_+)_++(1+x-q_-)_+
 \right\}.                                                     \tag{7}
\]

This agrees with (3)--(6) on their time-3 intersections.

## 4. The pathwise potential theorem

Let `W` be continuous and piecewise continuously differentiable on `Omega`,
with a finite Lipschitz constant. Require, throughout the interior of every
piece,

\[
 \begin{split}
 W_t-W_x-W_{q_+}-W_{q_-}&\ge0,\\
 W_t+W_x-W_{q_+}-W_{q_-}&\ge0,\\
 W_{q_+}+F_{\rm int}(t,-x)&\ge0,\\
 W_{q_-}+F_{\rm int}(t,x)&\ge0.                    \tag{8}
 \end{split}
\]

On the stopping faces require

\[
 \begin{split}
 W(t,1,q_+,q_-)&\le T_+(t,q_+,q_-),\\
 W(t,-1,q_+,q_-)&\le T_-(t,q_+,q_-),\\
 W(t,x,4,q_-)&\le Q_+(t,x,q_-),\\
 W(t,x,q_+,4)&\le Q_-(t,x,q_+),\\
 W(3,x,q_+,q_-)&\le K(x,q_+,q_-).                   \tag{9}
 \end{split}
\]

Finally require

\[
 W(0,x,0,0)\ge c\qquad(-1\le x\le1).                            \tag{10}
\]

Then the realized Princess law guarantees expected capture time at least `c`
against every legal Monster path.

Indeed, integrate (8) along any graph-completed physical path and clocks up to
the first stopping face. This gives

`cost_before_stop >= W(initial)-W(exit)`.

The exact continuation formulas give
`cost_after_stop >= boundary_value(exit) >= W(exit)`.
Thus every clock costs at least `W(initial) >= c`. Minimize over the clocks,
then use the full-clock identity and the time-7 domination from Section 2.
The piecewise chain rule is valid because `W` is continuous and locally
Lipschitz; on a common face the tangential derivatives agree. The inequalities
can be checked from both adjacent pieces.

## 5. A concrete finite linear program

Fix a reflection-symmetric triangulation of the physical `(t,x)` strip. The
field `F_int` is continuous P1 on it. It is only needed through time 5 in the
tail formulas, and its nodal values at times at least 3 are fixed to one half.
Its transport inequalities, symmetry, and `[0,1]` bounds are finite linear
constraints.

For `W`, use a continuous P1 function on each physical triangle, tensored with
a bilinear function on every rectangular `(q_+,q_-)` cell. Nodal values are the
unknowns. Every expression in (8) is affine in physical barycentric
coordinates and separately affine in the queue coordinates. The movement
inequalities are therefore **equivalent** to their values at the 3 physical
vertices times 4 queue corners. The charge inequalities need only the 3
physical vertices times the 2 endpoints of the other queue coordinate. Initial
conditions are checked at physical-space nodes.

### Exact tail charts

Transform the physical F mesh by `(t,x) -> (a=t+x,v=t)`. Between successive `a`
coordinates of transformed vertices, its triangles have affine lower and
upper `v` boundaries. In each such trapezoid, integrating the P1 field from
`v=b` up to `v=a+1` makes `C(a,b)` a quadratic polynomial in `(a,b)`, linear in
the nodal F values. This gives finitely many charts with rational linear
boundaries. The identically-zero chart covers `b >= a+1`.

Pull those chart boundaries back to each endpoint or queue-cap face. The
intersection with a tensor cell is a rational convex polytope. At an endpoint,
fixing the irrelevant queue at each of its grid nodes is sufficient because
`W` is affine in that queue while the right side does not depend on it. On
each remaining chart, `boundary_value-W` has total degree at most two.

For any quadratic polynomial `P`, define its symmetric polar form

\[
 B_2(u,v)=2P\left(\frac{u+v}{2}\right)-\frac{P(u)+P(v)}2.         \tag{11}
\]

If `u_1,...,u_N` are all vertices of a convex polytope and
`B_2(u_i,u_j)>=0` for every pair, then `P>=0` everywhere on the polytope,
because

\[
 P\left(\sum_i\lambda_i u_i\right)
 =\sum_{i,j}\lambda_i\lambda_j B_2(u_i,u_j).
\]

These are sufficient linear inequalities in the unknown F and W values. They
are not asserted necessary.

### Exact time-3 tour charts

For each of the two endpoint orders in (7), split each terminal tensor box
along its two positive-part kink planes. The endpoint-order cost is affine on
each resulting polytope. Terminal `W` is trilinear in `(x,q_+,q_-)`, so
`P=cost-W` has total degree at most three. Its symmetric degree-three polar
form is

\[
 B_3(u,v,w)=\frac92P\left(\frac{u+v+w}{3}\right)
 -\frac43\left[P\left(\frac{u+v}{2}\right)
              +P\left(\frac{u+w}{2}\right)
              +P\left(\frac{v+w}{2}\right)\right]
 +\frac{P(u)+P(v)+P(w)}6.                                      \tag{12}
\]

Impose `B_3>=0` on all triples of the polytope's vertices, for both endpoint
orders. Expanding the cubic at any convex combination proves positivity just
as in the quadratic case. This is a finite sufficient **linear** guard for
(7), without replacing any positive part by a negative affine expression.

All polytope vertices can be enumerated by exact rational active-plane
intersections in dimensions two and three. There is no four-dimensional
triangulation and no unknown event order in this certificate construction.

## 6. Prototype and remaining limits

The prototype discovery implementation uses a floating LP builder and exact-geometry tail
charts. The committed standalone verifier below reconstructs the analytic
conditions directly and does not require that discovery implementation. The half-unit physical mesh, queue knots
`0,1,2,4`, and exact time-3 tour charts give 616 variables, 22,967 inequalities and
33 equalities (the direct cubic-product polarization removes redundant floating
representations of identical rows). The floating solve returns
`c = 1.257403157971858`. Its repaired rational-matrix candidate is
`3772209269/3000000000 = 1.2574030896666666`; all 22,967 reconstructed
inequalities and 33 equalities are replayed with arbitrary-size integers by
the prototype matrix checker. That checker alone does not prove that its rounded
matrix equals the analytic inequalities. The characteristic example below has
a separate independent analytic bridge. Neither weak value improves the
repository's known lower bound.

The static fair-endpoint fixture `F_int=1/2`,

\[
 W(t,x,q_+,q_-)=2-|x|-\tfrac12(q_++q_-),\qquad c=1,
\]

satisfies all generated inequalities and checks signs, endpoint assignment,
and the boundary polar forms. Tail-chart regressions also reproduce the
closed-form integrals for constant and spatially uniform CDF fields.

Rationalization can use the following simple repair. On the domain,
`ell=3t+q_++q_-<=17`. Replacing

\[
 W\ \mapsto\ W+\gamma(\ell-17)-\varepsilon
\]

increases every control derivative by `gamma`, weakly decreases every exit
boundary value (and every associated boundary polar coefficient), and loses
only `17 gamma+epsilon` at the initial face. This repairs uniformly bounded
coefficient-rounding residuals after the Princess CDF has itself been
projected to an exactly legal rational field. It is not a replacement for
checking every rational row.

The finite program is now an implementable global lower-certificate search.
A fixed mesh does not imply exact equilibrium, and the attained coarse value
shows that certificate approximation remains substantial. Proving an optimum
lies in any prescribed finite ansatz is a separate missing theorem.


## 7. Characteristic geometry and separation diagnostics

The improved physical mesh is an axis-aligned grid in `U=t+x,V=t-x`, split
into triangles. Either diagonal retains one U-edge and one V-edge in each
triangle, so its P1 transport conditions are exactly the corresponding nodal
orders `F_U>=0,F_V<=0`. Samples of a legal continuous CDF therefore remain
legal after interpolation. Choose grid spacing dividing 1 and the time
horizon, so the interval and time-strip boundaries cut cells only along
diagonals through grid vertices. The implementation `LightMesh` also uses the
`U-V=0` diagonal in center-crossing cells to align symmetry and the `|x|`
fixture. The diagonal choice is recorded in every exported field.

A light-grid spacing of one half has 95 CDF nodes and yields a one-potential
LP with 1,040 variables, 31,255 inequalities, and 53 equalities. Its numerical
optimum is `1.3387313212347847`; the fully replayed rational certificate is

\[
 \boxed{\frac{2677462523}{2000000000}=1.3387312615.}
\]

The independent checker
`packages/interval_global_closure/analytic_exit/replay_certificate.py` verifies this
characteristic certificate directly with Fraction geometry and exact function
evaluation. It checks 105,733 raw analytic inequalities, exact mesh coverage
and reflection, and 804 direct tail line integrals, including every
endpoint/queue/time polar guard. It does not import the floating LP builder or
assume a coefficient lattice. Its report is
`packages/interval_global_closure/analytic_exit/coarse_characteristic_replay.json`. The
minimum endpoint-guard slack is `63/2000000000` and minimum charge slack is
`1/400000000`. This supplies the analytic bridge for the displayed rational
characteristic bound.

Every exit in the numerical dual is at a first endpoint; the time-3 and
queue-credit cap guards have zero dual mass. This is a diagnosis of the coarse
finite certificate, not a theorem eliminating those guards.

A separate small CDF-only master optimizes the same field class against a
finite bank of physical Monster routes. Each separator is an actual pair of
causal running-record clocks, so the master bounds that finite-bank problem.
It has no unrestricted lower-certificate interpretation. These diagnostic
values distinguish field approximation from potential approximation:

| Physical field mesh | CDF nodes | Finite-bank optimum, numerical |
|---|---:|---:|
| Rectangular step 1/4 | 189 | 1.3522426362 |
| Characteristic light step 1/2 | 95 | 1.3886828734 |
| Characteristic light step 1/4 | 349 | 1.4076323248 |
| Characteristic light step 1/8 | 1,337 | 1.4171614336 |

The quarter-unit rectangular field returned by the joint potential LP has
actual fastest-sweep payoff `1.29921842918125`, matching its certified
numerical lower `1.299218429139409` up to projection error. Thus that particular
field was weak; there was no hidden high-security field behind its potential
value. The CDF-only optimization shows that the potential ansatz also imposed
additional loss within the same field space.

The common-quantile exporter constructs exact affine common-quantile paths
inside the field triangles, preserving endpoint plateaus. For N radial
midpoint ranks with fair reflection, the signed strict CDF error is at most
`1/(4N)` uniformly. Since both laws are absorbed by 3, their payoffs against
every Monster differ by at most `7/(2N)` after the exact time-7 reduction. The
128-rank rectangular-field realization was independently replayed against the
fastest sweep at approximately `1.299375021472078`, consistently with the
continuous field. No unrestricted improvement is inferred from a bank value.


## 8. Reproduction and global completeness

From the repository root, run:

```sh
python packages/interval_global_closure/analytic_exit/replay_certificate.py packages/interval_global_closure/analytic_exit/coarse_characteristic_certificate.json
```

The input SHA256 is
`39da8088fbe2aa7e19051aa34f96083b25bf683cbea8ddcaf579b27eb5eba781`.
The verifier uses only the Python standard library and rebuilds all exact
geometry, direct tail integrals, and polynomial polar inequalities from the
certificate coefficients. Three independent native replays passed.

[The completeness theorem](FINITE_POTENTIAL_HIERARCHY_COMPLETENESS.md) proves
that with absorption horizon **3**, the supremum of these finite rational
certificate bounds is the unrestricted value V. Every rational c<V has a
finite certificate in this hierarchy. It does not prove that V itself has
a finite certificate, bound the mesh required to attain a chosen accuracy,
or identify a matching optimal Monster law. The sharp outward-time reduction makes the existing horizon-3 prototype
globally complete in this supremum sense. Its statewise future-credit
argument still safely uses completion horizon 7, even though the normalized
zero-credit physical game has completion horizon 6.
