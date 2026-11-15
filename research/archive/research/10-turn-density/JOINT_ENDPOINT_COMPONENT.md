# A solved endpoint/front component and its incoming-source coupling

This checkpoint contains complete legal ordered CDFs and an analytic
incoming correction. It does **not** give an unrestricted game value or a
matching upper strategy. The fixed-coordinate construction is a
feasibility experiment; its target is the endpoint-sweep cost of the
supplied field, not an asserted value of the game.

The exact formulas used below are in
[ENDPOINT_INWARD_OBSTACLE.md](ENDPOINT_INWARD_OBSTACLE.md),
[INITIAL_INWARD_CDF.md](INITIAL_INWARD_CDF.md), and
[POSTONE_FIRST_HIT_MOMENTS.md](POSTONE_FIRST_HIT_MOMENTS.md).

## 1. Solve the initial front with the endpoint obstacle

Use deficits `x=1-a`, `y=1+v`, and

    D(x,y)=1-R(1-x,-1+y),       r(y)=D(y,y).

The complete post-one field is supplied, including its endpoint-interior
traces. Define

    P_y(d)=2 integral_(0)^d alpha_(1-q)(1+y)dq
          =2yd+integral_(-1+y)^1 [R(1+y,V)-(1-d)]_+dV,

    Jpost(y)=integral_0^y Dpost(delta,y)d delta,
    Qall(y)=P_y(1)-P_0(1)-y,
    G(y)=3y+Qall(y)+H1+Jpost(y).

For the present input `H1=0`. Positive-M1 equality with the endpoint sweep
is the scalar equation

    P_y(r(y))=G(y)+integral_0^y D(t,y)dt.                       (1)

Thus each iteration first recomputes r by a one-dimensional increasing
inverse; it does not freeze the old initial distribution or impose
positive-M2 equality.

This front step preserves monotonicity. For `y2>y1` and fixed rank d,
the speed inequality for alpha gives

    P_y2(d)-P_y1(d)<=Qall(y2)-Qall(y1)+d(y2-y1).

Meanwhile G increases by at least `3(y2-y1)+Delta Qall`, and the
column integral of a transport-monotone input D is nondecreasing. Hence
the new r is increasing. No projection of r is needed to obtain this
property.

After substituting (1), the local endpoint inverse has left side

    Phi_xy(d)=P_y(d)-(y-x)d

and right side

    G(y)+integral_0^y min(D(t,y),r(x))dt
        -integral_x^y D(x,t)dt
        -integral_0^y [Dpost(delta,y)-r(x)]_+d delta.            (2)

The update clips the scalar root to its physical rank interval and then
takes a coordinate-monotone minorant. The latter preserves the diagonal
when its input lies between r(x) and r(y). The delayed-f comparison in the
endpoint note proves that the lower rank clamp is inactive at a physical
fixed point satisfying (1). This observation is about the fixed point;
it does not declare an arbitrary lower-clamped iterate a feasible law.

On a prescribed initial box with inverse slopes at least
`m_r sqrt(y)` for (1) and `m_D sqrt(y)` for (2), the front has sup-norm
Lipschitz factor `k_r=sqrt(Y)/m_r`. When `k_r<=1`, the substituted endpoint
root has factor at most `(2+k_r)sqrt(Y)/m_D`. Fixed incoming/exterior data
and invariant boxes are still hypotheses for a continuum Banach theorem.
The numerical experiment below does not replace those hypotheses by a
claim of continuum convergence.

## 2. What the fixed-coordinate experiment actually achieves

The input is `snapshots/initial_inward_candidate.json`. The experiment
uses exactly its 13 existing tail coordinates and 91 nodes in
`0<=x<=y<=1/128`; it adds no mesh coordinates. All post-one data stay fixed.
The old pre-one field is initially an explicit incoming upper obstacle.

* The endpoint/f update converges in five numerical iterations. At the
  local nodes, f equality and all endpoint inequalities hold to floating
  roundoff. Exporting the updated values into the complete field passes
  all **6,936 exact rational transport-cone checks**.
* That law has a genuine fixed-U1 inward attack at
  `x=2^-18,y=1/128`, below the target by
  `1.2865004401e-6`. Direct signed first-capture integration confirms it.
* Adding the exact fixed-U1 inward root to the same minimum of obstacles
  converges in six iterations. It removes the local nodal I1 deficits,
  retains the f/endpoint node checks, and again passes all 6,936 exact
  transport cones.

The second field is `snapshots/endpoint_joint_i1_field.json`. Independent
continuous-start M1 checking finds no positive-f dip on
`a>=127/128` beyond the approximately `2.2e-18` floating-export residual.
It still has the inherited negative-M1 dip inside the final affine cell,
about `-0.00021701618` relative to the endpoint target. Nodal checks do
not see this defect.

An ell row-area cap was also tested. The continuous export changes the
adjacent exterior strip, so its row moment includes the exact wing
`(Y_next-Y) Delta D(x,Y)/2`, not just the local integral. Holding r(Y)
fixed and solving those row caps restores ell at the nodes, but leaves
the outer f residual `-6.3095966e-8`. The recorded cap-shape experiments
do not remove this compatibility condition. They are retained as
diagnostics, not successful alternative fields.

## 3. An actual continuous incoming correction

For a rank band `[q0,q1]`, write

    h(z)=min(max(z-q0,0),q1-q0).

Replace its pre-one CDF contribution by

    h(min(A_base(U),R_base(psi(U),V))),                         (3)

where `U<=psi(U)<=1` and psi is increasing. The initial-front cap in (3)
is essential on bridge intervals: without it, a warp can change A and
decrease the negative-M1 cost despite increasing its row integral.
The cap preserves A exactly and is inactive on each repair interval
below. Every argument in (3) is increasing in U and decreasing in V;
disjoint band contributions therefore give a complete legal ordered CDF.
The physical point `(psi(U),V)` remains inside the light cone because
`|V|<=U<=psi(U)<=1<=V+2` whenever the warp is used.

On a repair interval suppose `A(U)>q1` and `R(1,V)<q0` for `V>=U`.
Then the negative-M1 vertical suffix term H is unchanged and its exact
four-cost gain is

    B(psi(U))-B(U),
    B(U)=(q1-q0)(1+U)
          +integral_(-U)^U [(q0-R(U,V))_+-(q1-R(U,V))_+]dV.    (4)

Let V0 denote the base field's endpoint-sweep cost and set

    T(U)=B(U)+4[V0-C_ell,base(U)].

The construction checks `T(U)<=B(1)` on the entire interval, then uses

    psi(U)=max(U,B^(-1)(max(B(U),sup_(t<=U) T(t)))).             (5)

The running maximum gives monotonicity even if the unprojected source
is not monotone. Equations (4)-(5) prove the ell inequality, rather than
merely matching it at sample starts. Equality need not hold where the
envelope is raised. Across a flat interval of B, the band CDF is
pointwise constant: it is monotone in U and has equal integrals.
Consequently a generalized-inverse jump across that interval does not
create a jump of the band CDF in this continuous base field.

The selected bands are:

| Band | Repair interval | Exact quadratic pieces | Initial saturation margin |
|---|---|---:|---:|
| `[.5,.85]` | `[127/128,255/256]` | 47 | `.0175170259` |
| `[.85,.904]` | `[255/256,1]` | 52 | `.00072883199` |

The coefficient pieces, inverse-range checks, and exact rational margins
are stored in `endpoint_low_band_warp.json` and
`endpoint_high_band_warp.json`. Their disjoint-band sum is specified by
`endpoint_two_band_field.json`; `WarpedField.radial(U,V)` evaluates the
actual unmeshed law. This is not a piecewise-linear interpolation of
sampled warp values.

The two repair intervals cover all terminal ell starts. The other band's
change has nonnegative row gain there, with initial A and H fixed, so the
combined field satisfies every negative-M1 inequality on
`[127/128,1]` relative to V0. It also preserves the continuous return gate
audited for the base field: on the terminal negative-V cone the lower
band is saturated, and the higher band gives

    D_new>=min(D_base,.096),       r_new=r_base.

Since `.096>1.9 e(1/128)`, the base inequality
`D>=1.9 min(r,e)` survives. All post-one gates are unchanged. See
[POSTONE_SAME_HALF_GATE.md](POSTONE_SAME_HALF_GATE.md) for the scope of
that response reduction.

## 4. The remaining coupling is measured, not suppressed

The incoming correction is visible to coarser positive-start routes.
For every positive start `a<1`, the initial and alpha terms are fixed,
and direct capture records give

    4 Delta Cf(a)=4 Delta Cg(a)
       =-integral_a^1 Delta R(U,-a)dU.                         (6)

Independent integration of the capped selected field finds a cost drop
of about `7.4449631e-8` at `a=5/8`. The new f/g slacks there are about
`-7.5312e-8`; at `a=15/16` the new g slack is about
`-1.26853e-7`. These changes are much larger than the reported numerical
integration errors. Thus the new complete field is **not** an all-route
lower certificate. Its common outer column source must be included in
the next front/post-field solve. The f-minus-g relation alone cannot
detect the loss in (6).

The loss is also certified without numerical inversion or quadrature.
`verify_warp_outer_column.py` uses the exact B/T coefficient pieces to
prove `psi(1048575/1048576)>2097151/2097152`. Monotonicity then gives a
uniform positive capped-band change on
`[1048575/1048576,16777201/16777216]` in the column for `a=5/8`.
Consequently

    integral_a^1 Delta R(U,-a)dU
      >=20483216873/214748364800000000000 > 0.

Together with the exact base costs, (6) proves that both corrected
positive costs at this start are strictly below V0. This rational
certificate proves the incompatibility; the larger numerical losses
above describe its size. Neither is a bound on the unrestricted game.

## 5. Reproduction

From the repository root:

```sh
python -B packages/interval_cdf_discovery/extract_endpoint_postdata.py packages/interval_cdf_discovery/snapshots/initial_inward_candidate.json --output packages/interval_cdf_discovery/snapshots/endpoint_postdata.json
python -B packages/interval_cdf_discovery/endpoint_joint_component.py
python -B packages/interval_cdf_discovery/endpoint_joint_component.py --include-fixed-one --output-prefix packages/interval_cdf_discovery/snapshots/endpoint_joint_i1
python -B packages/interval_cdf_discovery/terminal_band_warp.py --repair-end 255/256 --output packages/interval_cdf_discovery/snapshots/endpoint_low_band_warp.json
python -B packages/interval_cdf_discovery/terminal_band_warp.py --qlo 17/20 --qhi 113/125 --repair-start 255/256 --bridge-start 127/128 --output packages/interval_cdf_discovery/snapshots/endpoint_high_band_warp.json
```

No Lean compilation or CI is involved. Exact transport and source
identities, numerical fixed-point residuals, analytic warp gates, and
remaining route failures are deliberately reported separately.
