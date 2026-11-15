# Continuous record hypographs for admitted physical routes

This note gives an exact convex formulation of the actual capture payoff
of each **specified unit-speed Monster route** against a variable legal
P1 Princess CDF. A conservative piecewise-linear version uses an ordinary
LP and has an explicit error bound. Neither formulation supplies an
all-Monster certificate merely by checking a finite route list. The search
design is implemented in `packages/interval_continuous_lower/hybrid_lp.py`.
Its exact differential regressions pass; no improved bound is claimed.

## 1. Fixed geometry, variable field values

Fix a finite rational triangulation and a legal symmetric ordered CDF
`F`, continuous in the open arena with continuous endpoint interior
traces. Endpoint atoms are allowed and Princess paths stop at their first
endpoint. The nodal field values may be optimization variables, subject
to the complete legal transport and trace constraints.

Fix a piecewise unit-speed Monster route that visits both endpoints.
Split its legs at every field-cell crossing. This partition depends on
the route and triangulation, **not on the unknown nodal field values**.
The relevant clock price on one segment is therefore an affine function
with endpoint values `q0,q1`, each linear in those field variables.

The two clock prices are probability-normalized:

\[
             q_-(t)=F(t,m(t)),\qquad q_+(t)=1-F(t,m(t)).
\]

They lie in `[0,1]`; their two running records add to survival probability.
There is no extra reflection factor. Transport makes `F` nondecreasing
along a unit rightward leg and nonincreasing along a unit leftward leg.
Thus the monotonicity of each clock on each leg is fixed independently of
the unknown field values. Exactly one of the two prices can decrease on
a given leg; a clock already deactivated at its endpoint is omitted.

These premises do not automatically extend this construction to waiting
legs: the sign of `F_t` there can depend on the variable field. A different
partition or formulation would be needed. No classification of arbitrary
Monster responses is inferred from the unit-speed route list.

## 2. One affine segment and its cone

Let the duration be `Delta>0`, and let the entering record satisfy
`0<=r<=q0`. If `q1>=q0`, its exact integral is `Delta*r`.

For a decreasing price put `d=q0-q1>=0`. Direct integration of
`min(r,q0-d*t/Delta)` gives

\[
 A(r;q_0,q_1)
   =\Delta\left[r-\frac{(r-q_1)_+^2}{2d}\right],\qquad d>0.
 \tag{1}
\]

Its hypograph is represented by auxiliaries

\[
 0\le u\le d,\quad u\ge r-q_1,\quad v\ge0,\quad dv\ge u^2,
 \qquad z\le\Delta(r-v/2).
 \tag{2}
\]

The quadratic constraint is a rotated second-order cone; equivalently
`||(2u,d-v)||_2 <= d+v`. For the maximal charge choose
`u=(r-q1)_+` and `v=u^2/d`. The bound `u<=d` loses nothing because
`r<=q0`.

At `d=0`, (2) forces `u=0`. Since `r<=q0=q1`, choosing `v=0` yields
`z=Delta*r`, the exact constant-price integral. Thus the closed cone
handles zero slopes without division or an unproved limiting convention.
Increasing segments use only `z<=Delta*r`.

## 3. Causal coupling and exact projection

Couple the entering and outgoing records of every active segment by

\[
                  0\le r_{i+1}\le r_i,\qquad r_{i+1}\le q_{i,1},
 \tag{3}
\]

and impose `r_i<=q_{i,0}`. On an increasing segment, (3) is equivalent
to permitting an outgoing record no larger than the entering one.
At the initial point, each active record is at most its initial clock
price. An initial endpoint hit deactivates that endpoint's clock at once.

Endpoint values in (1)-(2) are the **interior limits before capture**.
After the segment first reaches its active endpoint, set that clock to
zero and stop charging it. Replacing the segment's final interior trace
by zero before integration would charge the endpoint atom incorrectly.
The other clock continues with its unchanged running history. Later
visits do not reactivate a stopped clock.

For any fixed legal field, every feasible auxiliary record is at most
the true running record, by induction using (3). The exact integral in
(1) is nondecreasing in `r`: it is the integral of a pointwise
nondecreasing cap. Therefore each feasible `z_i` is at most the true
segment contribution. Conversely, the true running records and the
maximal choices in (2) simultaneously attain all actual segment costs.
Consequently,

\[
 \boxed{\text{there exist feasible auxiliaries with }
                  \sum_i z_i\ge c
       \quad\Longleftrightarrow\quad C_m(F)\ge c.}
 \tag{4}
\]

This holds jointly for any finite list of admitted routes, with the same
field variables and separate causal histories. Identical causal prefixes
can share auxiliaries: the true records satisfy every path constraint
simultaneously, so sharing changes no projected field set.

The global legal-field constraints remain essential. Independent linear
endpoint-price variables without a consistent CDF do not describe a
Princess strategy. Fixed physical paths and a fixed triangulation make
(2)-(4) a finite convex model; they do not turn the finite path list into
a complete response oracle.

## 4. A conservative ordinary LP

For a positive integer `K`, define on `0<=u<=d`

\[
 \overline\psi_K(u,d)=
 \max_{0\le j<K}
 \left\{\frac{2j+1}{K}u-\frac{j(j+1)}{K^2}d\right\}.
 \tag{5}
\]

For `d>0`, this is `d` times the secant interpolation of `s^2` at
`s=j/K`, evaluated at `s=u/d`. Adjacent lines meet at those knots.
On the containing interval its excess is
`d*(s-j/K)*((j+1)/K-s)`, so

\[
 0\le\overline\psi_K(u,d)-u^2/d\le d/(4K^2).
 \tag{6}
\]

At `d=0,u=0`, all lines equal zero. Replace the cone in (2) by the
`K` linear lower bounds on `v` in (5). Since these secants lie above
the perspective, every resulting charge is a **lower bound on the
actual continuous payoff**. These are inner feasibility constraints;
they are not frozen upper supporting clock planes.

For a fixed field, choose the true records, `u=(r-q1)_+`, and
`v=overline psi_K(u,d)`. The record propagation remains exact; only
the integrated charges lose value. Therefore the maximal inner-LP
route score `C_m^(K)` satisfies

\[
 C_m(F)-\frac1{8K^2}\sum_{\text{decreasing segments}}\Delta_i d_i
       \le C_m^{(K)}(F)\le C_m(F).
 \tag{7}
\]

Here `Delta_i` is physical time and `d_i` is a drop in a probability
price. No field-denominator or fair-reflection factor is implicit.

For the uniform full-width common-threshold profile grid `p`, retain
the characteristic crossing partition, including any further triangle
crossings. A unit-speed segment has `Delta_i<=1/(2p)`. The decreasing
clock's total variation on any one complete physical leg is at most
one. Thus a `J`-leg route obeys the field-independent estimate

\[
 \boxed{0\le C_m(F)-C_m^{(K)}(F)
                      \le\frac{J}{16pK^2}.}
 \tag{8}
\]

For example, `p=64`, `J<=4`, and `K=16` give loss at most
`1/65536`. For a nonuniform mesh use (7), or its bound using the actual
maximum segment duration. Merging intervals requires reassessing that
duration bound. Equation (8) is not a uniform error estimate for
arbitrary Monster paths with no given leg count.

## 5. Exact regression and the next acceptance gate

```bash
python -B packages/interval_quantile_certificate/test_continuous_record_hypographs.py \
  --report /tmp/continuous_record_hypographs_replay.json
```

The standard-library regression checks the capped-affine identity,
zero slopes, all tested secant error bounds, deliberately smaller causal
record histories, initial endpoint atoms, endpoint resets, and complete
specified routes. It compares each route with both existing exact
chronological integrations. Physical segment monotonicity is selected
from direction and clock orientation, and every crossing interval is
checked to be affine. It runs no conic optimizer or complete response
oracle.

The implemented hybrid search combines a legal CDF profile with
these continuous constraints for a modest physical route list. The
existing large cache should first be covered by batch separation of
its exact active calendar planes. Only repeatedly violating histories
should acquire the larger nodal-record hypographs. Once the whole cache
passes, rationalize and exactly rescore the continuous routes, then use
the complete native response oracle to test the candidate. Ordinary cached
calendar rows cover the broad bank; repeatedly violating paths are promoted
to exact discrete records. Every admitted continuous route has the secant
hypograph, with exact chronological rescoring as a separate gate. See the
[driver commands and tests](../../packages/interval_continuous_lower/README.md#hybrid-continuous-records).
This implementation supplies no response-completeness theorem or new game
bound. The secant model's optimum is an inner model value, not an upper on
the exact known-route optimum.

The current record-LP campaign failed its cached-path floor before
continuous rescoring; replacing the continuous model alone does not
address that path-coverage and memory bottleneck. Conversely, merely
passing a continuous route bank gives no unrestricted Princess security.
A sharp global lower still requires an all-Monster certificate, such as
the control and exit inequalities in
[`FINITE_RECORD_BELLMAN_LIFT.md`](FINITE_RECORD_BELLMAN_LIFT.md), or a
complete fixed-field response computation. No sufficiency of the
`P/I/J` families is assumed here.
