# Exact initial-inward contact block and the column correction

This note gives an exact response constraint for the initial-inward
Monster family present in the current physical certificates. It couples
that family to the `f,B,k,H,Delta` objects of
`BULK_CONTACT_AND_CUSP_EQUATIONS.md`. The contact equation is locally
invertible and its full feasibility problem is convex. Neither fact
asserts that this family exhausts an unrestricted optimal Monster law:
earlier-center alternating excursions and the endpoint-first families
remain separate constraints.

## 1. Deficit coordinates for the same initial field

Use a symmetric ordered Princess CDF `F`, continuous in the open arena
and with continuous endpoint interior traces, endpoint-sticky and
maximally outward after time two. Put

\[
 \mathcal F(U,W)=F((U+W)/2,(U-W)/2),\qquad
 A(t)=F(t,1-t),\qquad H(s)=\int_0^2\min\{s,A(t)\}\,dt.
\]

For `0<=a<=z<1` introduce

\[
 L(a,z)=\mathcal F(1-a,z-1),\qquad
 \phi(a)=F(0,1-a),\qquad K(z)=A(z/2).
\tag{1}
\]

Thus `phi(a)` is the bulk note's `f(1-a)`, and `K(z)` is its
`k(1-z)`. Both arguments here are endpoint deficits. The transport
inequalities imply

\[
 L_a\le0,\quad L_z\le0,\qquad
 L(a,a)=\phi(a),\quad L(0,z)=K(z),
\tag{2}
\]

\[
 \phi(z)\le L(a,z)\le\min\{\phi(a),K(z)\}.
\tag{3}
\]

The patch (1) is in the positive arena and before the principal front.
It records a genuine two-dimensional initial field, not an independent
choice of unrelated one-dimensional traces.

## 2. Exact cost of every initial-inward row

The row `I_(a,z)` has vertices

\[
 (0,1-a),\quad
 \left(d,1-\frac{a+z}{2}\right),\quad
 \left(h,1-\frac z2\right),\quad(2,-1),\quad(4,1),
 \qquad d=\frac{z-a}{2},\ h=\frac z2.
\tag{4}
\]

It moves left, then right to the principal front, then left and right
through both endpoints. The first turn is strictly positive for
`0<a<z<1`. At `a=z>0` the first leg vanishes and (4) is the principal row
`P(1-z,1)`. The actual path at `a=0` is the fast sweep, with the endpoint
contact convention treated separately below.

Let `0<a<=z<1`, `l=L(a,z)` and `f=phi(a)`. Direct record accounting gives

\[
\begin{aligned}
 C_I(a,z)={}&4+H(l)
       +\frac12\int_a^z L(a,s)\,ds
       -\frac12\int_0^a\max\{f,L(b,z)\}\,db\\
 &-\frac{z-a}{2}(f+l)
       -\left(4-\frac z2\right)\max\{f,K(z)\}.
\end{aligned}
\tag{5}
\]

The two maxima must be retained. In particular, the later peak need not
exceed the initial upper record.

The actual `a=0` sweep has cost `H(1)`. The trace formula (5) at `a=0`
instead has value `H(1)+4[1-phi(0)]`. These agree when there is no initial
endpoint atom, as in the square-root contact theorem; otherwise the
initial endpoint capture is a genuine discontinuity. The sweep is always
kept as its own physical row.

To verify (5), the first left leg has lower record equal to the current
field and upper-survivor record `1-f`. Its lower-record integral is
the first integral in (5). On the middle right leg the lower record is
`l`, while the upper-survivor record is
`1-max(f,current field)`; its latter field integral is the second
integral in (5). At the principal turn the upper record is
`max(f,K(z))`. The front values before time `h` are at least `K(z)>=l`,
so the lower-record integral on the descending leg is `H(l)-h*l`.
After the negative endpoint, the next center time is three; outward
motion after two ensures that the remaining positive ranks are caught
only at the positive endpoint at time four. Summing these contributions
and collecting constants gives (5).

The formula concerns actual ordered capture. A crossing mixture of
Princess paths can have different first-capture labels despite the same
one-time marginal field. Its common-quantile reordering is the law to
which (5) applies.

## 3. The inactive upper-peak branch is dominated

Let `D_a` start at `1-a`, move directly to `-1` at time `2-a`, then to
`+1` at time `4-a`. If

\[
                         K(z)\le\phi(a),
\]

the whole row (4) never improves its original upper record before the
positive endpoint. The direct row's position is no farther right than
the old one until its earlier negative endpoint. Its lower record is
therefore no larger at every time. Its remaining upper-survivor mass
`1-phi(a)` is caught `a` units earlier. Hence

\[
 \boxed{C_I(a,z)-C_D(a)\ge a[1-\phi(a)]
                 \quad\text{when }K(z)\le\phi(a).}
\tag{6}
\]

Consequently, once the direct-inward rows satisfy a proposed lower bound,
this whole branch needs no additional inequality. A nontrivial active
interior sheet, with `a>0` and `phi(a)<1`, must lie in

\[
                          K(z)>\phi(a).
\tag{7}
\]

When the front trace is strictly decreasing, (7) is equivalently
`z<2 H'(phi(a))`. The trace inequality (7), rather than a particular
inverse representative, is the atom-safe way to state the branch.

Under the hypotheses of `ENDPOINT_SQUARE_ROOT_CONTACT.md`, the boundary
`K(z)=phi(a)` satisfies

\[
                       a=\frac{z^2}{16}+o(z^2).
\tag{8}
\]

Thus a near-endpoint active inward sheet lies above this parabolic
rank/front boundary. This does not determine its support inside that
region or prove that the boundary itself is a contact curve.

## 4. A strongly monotone scalar contact equation

On (7), the second maximum in (5) is `K(z)`. If this row is active at
cost `V_*`, then its local unknown `l=L(a,z)` solves

\[
\begin{aligned}
 H(l)-\frac{z-a}{2}l={}&V_*-4
       -\frac12\int_a^z L(a,s)\,ds
       +\frac12\int_0^a\max\{\phi(a),L(b,z)\}\,db\\
 &+\frac{z-a}{2}\phi(a)
       +\left(4-\frac z2\right)K(z).
\end{aligned}
\tag{9}
\]

The right side uses earlier values on the same row and smaller values
of the first coordinate on the same column. Values at the single
integration endpoint have zero measure.

For fixed previous data, this equation has at most one solution in the
legal interval (3). More precisely, if `l_1<l_2<=K(z)`, monotonicity of
the front gives `A(t)>=K(z)` for `0<=t<=z/2`. Therefore

\[
 H(l_2)-H(l_1)\ge\frac z2(l_2-l_1),
\]

and hence

\[
 \boxed{\left[H(l_2)-\frac{z-a}{2}l_2\right]
       -\left[H(l_1)-\frac{z-a}{2}l_1\right]
                      \ge\frac a2(l_2-l_1).}
\tag{10}
\]

This proof remains valid on front plateaus and does not assume
`H'(K(z))=z/2`. For `a>0` it is a genuine lower bound on the inversion
slope. A constraint `C_I>=V_*` is consequently a lower obstacle on
the local value `L(a,z)`, once the previous data are fixed.

There is an important scope limit. Equation (9) is a mixed Volterra
relation: increasing earlier same-row values lowers its right side,
whereas increasing earlier same-column values raises it. Thus a greedy
pointwise-minimum construction is not justified by (10) alone. No claim
of a globally least legal field, existence of a solution for arbitrary
boundary data, or an endogenous contact region follows merely from
local invertibility.

## 5. Differential form on a smooth active phase

Suppose the field and front are differentiable on an open active phase,
with no positive-length level ties in the following clipped integral.
Write

\[
 R(a,z)=-L_z(a,z)\ge0,\qquad
 \beta(a,z)=\sup\{b\in[0,a]:L(b,z)>\phi(a)\}.
\]

Transport makes the strict set in this definition an initial interval.
Differentiating (5) with respect to `z`, while keeping `a` fixed, gives

\[
\begin{aligned}
 2\,\partial_z C_I={}&
 -[2H'(L(a,z))-z+a]R(a,z)
       +\int_0^{\beta(a,z)}R(b,z)\,db\\
 &+K(z)-\phi(a)+(8-z)[-K'(z)].
\end{aligned}
\tag{11}
\]

An interior active row has zero `z` derivative. Thus the active phase
satisfies the integral differential equation

\[
 \boxed{[2H'(L(a,z))-z+a]R(a,z)
     =\int_0^{\beta(a,z)}R(b,z)\,db
           +K(z)-\phi(a)+(8-z)[-K'(z)].}
\tag{12}
\]

The denominator is at least `a` wherever the derivative exists, by
(10). All terms on the right are nonnegative on (7). The primitive
identity (9), rather than an arbitrary branch of (12), is used at
plateaus and other nondifferentiable contacts.

Equations (9) and (12) supply a response-side determination of the
initial field on its active region. They are complementary to the
Monster-density shadow contact equations in
`BOUNDARY_LAYER_KERNEL_AND_GAP.md`; those determine which variations
of the Princess field can be active. Neither side alone determines the
global support.

## 6. The former column defect is now an explicit field integral

For a principal row of initial deficit `z`, (5) at `a=z` reduces to

\[
 C_P(1-z,1)=4+H(\phi(z))
       -\frac12\int_0^z L(b,z)\,db
       -\left(4-\frac z2\right)K(z).
\tag{13}
\]

Thus its lower inequality `C_P>=V_*` is exactly the column upper bound

\[
 \int_0^z L(b,z)\,db
          \le8-2V_*+2H(\phi(z))-(8-z)K(z).
\tag{14}
\]

Use the canonical incoming comparison `B` from the bulk note. Then
its nonnegative correction is precisely

\[
 \boxed{\Delta(1-z)=\int_0^z
       [L(b,z)-\max\{\phi(z),B(1-b)\}]\,db.}
\tag{15}
\]

The artificial terminal value of `B` changes no integral. The original
transport proof supplies nonnegativity of the integrand. Hence a legal
solution of the inward contact block fixes this `Delta` and the
corresponding first-visit inverses; it is no longer an independently
chosen scalar correction. If only part of the triangle is active, the
remaining part is still governed by its transport inequalities, the
nonactive response inequalities, and other support families.

## 7. An exact convex feasibility block

For fixed `phi,K,H`, (5) is concave as a functional of `L`: `H(L(a,z))`
is concave; the negative clipped-column integral is concave; the other
terms are linear. Therefore all inequalities `C_I(a,z)>=V_*`, together
with the transport/trace constraints and principal column upper bounds,
form a convex feasibility problem. The active region need not be
prescribed in order to pose or certify that problem.

In fact the convexity is joint in the entire initial field and the
sweep trace. Write the moment explicitly as

\[
                 H(L(a,z))=\int_0^2\min\{L(a,z),A(t)\}\,dt.
\]

This is jointly concave in `(L,A)`. Both negative maxima in (5) are
jointly concave in their arguments, and `phi(a)=L(a,a)` and
`K(z)=A(z/2)` are linear consistency conditions. All remaining terms
are linear. Thus the full E/P/I lower block may be synthesized jointly
in `(L,A,V_*)`, instead of alternating unrelated trace optimizations.
An exact finite representation must still check the continuous
parameter inequalities; sampling a finite row bank alone does not do so.

This synthesis is over partial traces that extend to the **same legal
symmetric sticky CDF**. Conditions (2) alone do not list every cross-cone
compatibility with the remaining sweep trace, particularly its negative
half. Extendibility is a genuine additional requirement. Its feasible
set is convex: it is the projection of the convex cone of legal global
CDF fields, including their linear symmetry, transport, endpoint-trace
and outward-after-two conditions. Thus requiring this compatibility does
not change the joint convexity assertion, but arbitrary unrelated
`L,A` data are not declared realizable.

If a candidate field satisfies these inequalities for every `(a,z)`,
the sweep inequality and the separately checked direct-inward rows,
it is a sufficient lower certificate against the physical family
E/P/I. It is not yet an unrestricted lower certificate. Endpoint-first
paths outside this patch and the earlier-center renewal problem must
also be covered. The current physical laws contain genuine repeated
center excursions, so those constraints cannot be deleted merely because
their total mass is small.

## 8. The backward adjoint determines the initial-inward pressure

There is a complementary equation on the Monster side. Suppose the
initial-inward family has density `zeta(a,z) da dz`. Keep the principal
and endpoint-family densities `g,h` in the bulk note's **physical start
coordinate**, and set `G=g+h`. Consider a field variation supported
strictly inside the patch (1), leaving its initial and front traces
unchanged. Assume `H` is differentiable at the selected valley values;
level ties otherwise require the corresponding subgradient formulation.

Differentiating (5) and applying Fubini gives the following exact local
pressure from the I family:

\[
\begin{aligned}
 \rho_I(a,z)={}&
 \left[H'(L(a,z))-\frac{z-a}{2}\right]\zeta(a,z)
       +\frac12\int_z^1\zeta(a,q)\,dq\\
 &-\frac12\int_a^z
       1_{\{L(a,z)>\phi(p)\}}\zeta(p,z)\,dp.
\end{aligned}
\tag{16}
\]

The three terms are, respectively, the selected first-turn value; the
initial-left occupations of rows which turn later on the same line;
and the record-active outgoing occupations of rows starting later on
the same column. The fixed front and initial traces contribute no
additional term to this compactly supported variation.

If `phi` is strictly decreasing, let `rho=phi^{-1}(L(a,z))`, which lies
in `[a,z]` by (3). The last integral then runs from `rho` to `z`.
The main P/S pressure from the bulk note, under the coordinate change
`U=1-a,W=z-1`, is

\[
              \rho_{P/S}(a,z)
                     =\frac{G(a-1)-G(1-z)}2.
\]

Thus on an open phase where both transport constraints permit free
signed variations, Princess optimality gives

\[
\begin{aligned}
 &[2H'(L(a,z))-z+a]\zeta(a,z)
       +\int_z^1\zeta(a,q)\,dq
       -\int_{\phi^{-1}(L(a,z))}^z\zeta(p,z)\,dp\\
 &\hspace{30mm}=G(1-z)-G(a-1)-2\rho_{\rm rest}(a,z).
\end{aligned}
\tag{17}
\]

Here `rho_rest` is the actual pressure of every remaining physical
family, including earlier-center multiple excursions. It is set to zero
only in a model that actually omits those families, not because their
measured mass is small.

For a known field `L`, (17) is linear in the inward density. Its
integrals use later values of the two parameters, whereas the forward
contact equation (12) uses the earlier column. The same strictly positive
coefficient `2H'(L)-z+a>=a` occurs in both equations. Together with
`zeta>=0`, the response inequalities and the complementarity
`zeta(a,z)>0 => C_I(a,z)=V_*`, this supplies a forward/backward candidate
contact system for the initial phase.

One must not impose (17) unchanged on a saturated transport phase: there
the allowed variations are restricted and the relevant transport
multiplier or boundary-flux conditions replace free cancellation. These
active-set and global support conditions remain part of the construction
problem, not consequences of the displayed integral equations alone.

## 9. Independent exact regression

`verify_initial_inward_contact.py` imports only the standard-library
chronological physical oracle and CDF integrator from
`verify_bulk_contact_equations.py`. The oracle intersects actual affine
Princess and Monster paths and integrates first capture times; it does
not use (5) to obtain them.

For a uniform initial radius, stationary until `T` in `{0,1,2}`, then
maximally outward and endpoint-sticky, the replay passes:

* 405 physical I costs, including 203 nontrivial peaks below the initial
  upper record and 128 above it;
* 232 direct-inward dominance comparisons from (6);
* 1,215 chord inequalities from (10), including flat front portions;
* 49 exact physical central-difference checks of (11) on a smooth branch;
* 45 fast-sweep and 45 principal-row boundary reductions.

The direct physical oracle uses 4,396 affine contact branches. Run

```sh
python -B packages/interval_global_closure/verify_initial_inward_contact.py \
  packages/interval_global_closure/initial_inward_contact_replay.json
```

These are exact regressions of the analytic identities, not an assertion
that any test field has a positive active inward sheet.
