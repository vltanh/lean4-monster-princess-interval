# The free start condition for an initial-inward sheet

The turn equation in [INITIAL_INWARD_CDF.md](INITIAL_INWARD_CDF.md)
does not by itself characterize an active two-dimensional monster sheet:
its initial position is free too. This note derives that second derivative
and its initial-boundary trace. It also distinguishes an immediately slower
initial tangent from the unit tangent in
[CURVED_INITIAL_POWER_PHASE.md](CURVED_INITIAL_POWER_PHASE.md).
These are necessary conditions, not a constructed equilibrium.

## 1. Hypotheses and notation

Use the ordered reflected law and endpoint hypotheses of the exact inward
response identity. Work at a smooth interior point `-a<v<a`, without an
initial atom, a first-contact atom on the row, or a positive-length column
level set at the initial rank. Put

\[
 A=A(a),\quad \rho=A'(a),\quad r=R(a,v),\quad B=R(1,v),
 \quad J(r)=\int_0^r c_1(q)\,dq.
\]

Here `c_1(q)=2 alpha_q(1)-1` is defined by the **first** `U=1`
inverse. It is identified with the final outgoing characteristic only when
that identification is valid for the particular law. Assume that `J` is
differentiable at `r` and that differentiation under the row and column
integrals is justified. At atoms or coincidence intervals, use the strict
and closed traces of the exact integral formula instead.

Suppose `B>A`. Define

\[
 U_A(v)=\sup\{U\in[a,1]:R(U,v)\le A\}.
\]

Monotonicity gives `R(a,v)<=A` and
`measure{U in [a,1]:R(U,v)>A}=1-U_A(v)`.
On a continuous strictly ordered inverse branch,
`U_A(v)+v=2 beta_{A(a)}(v)`. Using the threshold definition avoids
selecting an arbitrary quantile representative at a spatial gap.

## 2. Exact derivative with respect to the free start

The start derivative is

\[
\begin{aligned}
4\,\partial_a C_I(a,v)
={}&A-r+\int_{-a}^v R_U(a,w)\,dw\\
 &+[1+c_1(r)-a-v]R_U(a,v)
   -[U_A(v)+v]\rho .                         \tag{1}
\end{aligned}
\]

To check it, differentiate the exact four-cost

\[
12-8A+\int_{-a}^v R(a,w)\,dw
 +(1-a-v)r+J(r)
 -(7-v)(B-A)-\int_a^1(R(U,v)-A)_+\,dU.
\]

The moving lower row endpoint contributes `A`; the explicit factor in
the turn term contributes `-r`. The moving lower column endpoint
contributes zero because `r<=A`. The three coefficients of `rho` sum to

\[
-8+(7-v)+(1-U_A)=-v-U_A.
\]

This proves (1). If a column level set at `A` has positive length,
differentiate the positive part one-sidedly; a smooth version of (1)
cannot be assigned across that face without its trace correction.

An open active inward sheet must satisfy both (1) with zero left side
and the turn equation from `INITIAL_INWARD_CDF.md`. A start/turn curve
instead has only its tangent stationarity condition; it is not a
two-dimensional positive density by assumption.

## 3. Deficit coordinates and the initial inverse

Use `x=1-a`, `y=1+v` and the full-field deficits

\[
 D(x,y)=1-R(1-x,-1+y),\quad r_0(x)=1-A(1-x),
 \quad w=e^{-1}.
\]

Assume on this branch that `1+c_1(1-D)=w(D)`. Let
`chi_x(y)=1-U_{A(1-x)}(-1+y)`. This is the initial-rank inverse
when that rank is on its initial arc; the threshold definition still
specifies it on any other regular first-inverse branch.
Since `R_U=D_x`, (1) becomes

\[
\begin{aligned}
4\,\partial_a C_I
={}&D(x,y)-r_0(x)+\int_x^y D_x(x,z)\,dz\\
 &+[w(D(x,y))+x-y]D_x(x,y)
   -[y-\chi_x(y)]r_0'(x).                    \tag{2}
\end{aligned}
\]

Thus an active varying patch satisfies

\[
[w(D)+x-y]D_x
 =[y-\chi_x(y)]r_0'
  -[D-r_0]-\int_x^y D_x(x,z)\,dz.             \tag{3}
\]

Transport makes the two subtracted quantities on the right nonnegative.
Equation (3) therefore tests whether a proposed initial inverse can
support a positive `D_x`, or whether a transport plateau/obstacle must
intervene. It is not an independent way to choose `chi`: the inverse must
belong to the same field `D`.

## 4. The no-inward-turn boundary

Let `Cg(a)=CI(a,-a)`. Suppose the characteristic field has a one-sided
initial tangent, and the initial rank first reaches outgoing thresholds
just above `-a` at times tending to zero. In particular, exclude a
positive-length initial unit outward run. Let

\[
 d(a)=1+c_1(A(a))>0.
\]

At the boundary, `r=A`, the row integral vanishes, and
`U_A(-a+)+(-a)=0`. Formula (1) gives

\[
4\,[\partial_v^+C_I(a,-a)+C_g'(a)]
 =4\,\partial_a C_I(a,-a+)
 =d(a)R_U(a,-a+).                            \tag{4}
\]

The first equality uses the chain rule along `v=-a`; it does not
differentiate at a first-contact jump. If the initial spatial density is
`rho` and the initial princess velocity at this rank is `s`, the
transport identity is

\[
R_U(a,-a+)={\rho(1-s)\over2}.
\]

Consequently

\[
4\,[\partial_v^+ C_I+C_g']
 ={d\rho(1-s)\over2}.                         \tag{5}
\]

There are two distinct consequences at an active flat positive-M2 band.

* If `s<1` and `rho>0`, an infinitesimal inward turn has **positive**
  first-order slack. It is permissible for the inward equality set to
  begin away from the no-turn boundary. A unit tangent is not forced by
  positive-M2 equality alone.
* If an inward equality set reaches the boundary with the stated regular
  traces, (5) forces `s=1`. The next term then matters. Under the additional
  uniform power and off-diagonal regularity assumptions of
  `CURVED_INITIAL_POWER_PHASE.md`, that term gives the golden-ratio
  curvature exponent.

For an ordinary positive-length initial unit run, the first inverse does
not tend to zero. The missing term in (1) instead survives as
`-(u(a)-a)rho` and gives the strict attack already proved in
`INWARD_INITIAL_OBSTRUCTION.md`. The two boundary calculations apply to
different first-contact geometries.

## 5. Independent exact checks

Run

```sh
python -B packages/interval_turn_sheet/verify_initial_inward_start.py
```

The verifier uses continuous ordered polygonal laws with initial speeds
`1/4`, `1/2`, `3/4`, and `1`. Complete signed capture-record integrals
give the reference costs. The formula side separately integrates the
selected local `R_U` branches and computes the initial rank's first
outgoing inverse from its polygon. Rational finite differences on stable
quadratic cells compare the derivatives exactly.

It passes 468 interior start identities, 324 turn identities on `B<A`,
188 strict descending-turn checks within those cells, and 99 initial
boundary identities with immediately slower tangents: **1,079 exact
checks** in all. Initial and incoming atoms remain covered by the
separate integral-formula verifier, rather than by assigning a smooth
derivative to them. No new game bound or matched strategy follows from
these identity checks.
