# Endpoint rank and incoming-front contact

This is an exact conditional interface theorem for an ordered Princess
field. It does not assume that the principal Monster family exhausts an
optimal law, or assert that an unrestricted equilibrium has this contact
interval. Its conclusion applies to arbitrary ordered Princess geometry
before the incoming front, including the curved initial phase measured by
`Delta` in `BULK_CONTACT_AND_CUSP_EQUATIONS.md`.

## 1. The contact hypothesis

Use the conventions of the bulk note: a symmetric ordered Princess law,
continuous signed CDF in the open arena and continuous endpoint interior
traces, endpoint-sticky, and maximally outward after time two. Set

\[
 A(t)=F(t,1-t),\qquad H(s)=\int_0^2\min\{s,A(t)\}\,dt,
 \qquad f(a)=F(0,a).
\]

The function `A` is nonincreasing. Write its time-zero value as its
interior endpoint trace `A(0)=F(0,1-)`. The actual endpoint sweep has
cost `C_E=H(1)`.

For `0<epsilon<1`, put

\[
 a=1-\epsilon,\qquad h=\epsilon/2,\qquad
 k=A(h),\qquad
 I=\int_0^h F(t,1-\epsilon+t)\,dt.
\]

The principal Monster row `P(1-epsilon,1)` starts at `1-epsilon`, moves
right until `(h,1-h)`, then sweeps to `-1` at time two and `+1` at time
four. The exact moment identity from the bulk note is

\[
 C_P(1-\epsilon,1)=4-I-(4-h)k+H(f(1-\epsilon)).             \tag{1}
\]

Assume that the sweep and these principal rows are in contact:

\[
 C_E=V_*,\qquad C_P(1-\epsilon,1)=V_*
                   \quad(0<\epsilon<\epsilon_0).          \tag{2}
\]

Here `V_*` is their common cost. It is not declared to be the unrestricted
game value without the remaining saddle inequalities.

## 2. Contact excludes an initial endpoint atom

Let `c=F(0,1-)`. As `epsilon` decreases to zero, both `f(1-epsilon)`
and `k` tend to `c`, while `I` tends to zero. Since `A(t)<=c` for
`t>=0`, one has `H(c)=H(1)`. Taking limits in (1) gives

\[
 \lim_{\epsilon\downarrow0} C_P(1-\epsilon,1)
                  =C_E+4(1-c).                            \tag{3}
\]

Therefore (2) forces `c=1`: the initial law has no endpoint atom. This
argument uses actual endpoint capture for `E` and an interior turn for
`P`; replacing one by the other before taking the limit would lose the
term in (3).

The same conclusion holds if the contact error
`C_P(1-epsilon,1)-C_E` merely tends to zero.

## 3. An exact scalar identity

Write

\[
 r(\epsilon)=1-f(1-\epsilon),\qquad
 D(r)=H(1)-H(1-r).
\]

Along the first rightward leg the signed field is nondecreasing, so

\[
 f(1-\epsilon)\le F(t,1-\epsilon+t)\le k.
\]

Consequently

\[
 0\le h k-I\le h\bigl(k-f(1-\epsilon)\bigr)\le h r(\epsilon).
                                                               \tag{4}
\]

Subtracting the equal costs in (2) yields

\[
 \boxed{D(r(\epsilon))=4\,[1-A(\epsilon/2)]
                          +\frac\epsilon2 A(\epsilon/2)-I.}     \tag{5}
\]

Thus all dependence on the initial path geometry is confined to a
nonnegative error bounded by `epsilon*r(epsilon)/2`. Neither an initial
unit-speed phase nor a pointwise bound on the Princess density is used.

## 4. Square-root initial tail

Assume only the following first-order incoming-front behavior:

\[
             A(t)=1-\lambda t+o(t)\quad(t\downarrow0),
                         \qquad 0<\lambda<\infty.          \tag{6}
\]

No derivative of `A` or `f` is required. Then

\[
 \boxed{1-f(1-\epsilon)
                  =2\lambda\sqrt\epsilon+o(\sqrt\epsilon).}    \tag{7}
\]

To prove this, observe that

\[
 D(r)=\int_0^2\bigl(r-[1-A(t)]\bigr)_+\,dt
                         \sim\frac{r^2}{2\lambda}.         \tag{8}
\]

For completeness, fix `eta` with `0<eta<lambda`. On a sufficiently small
initial interval, `(lambda-eta)t<=1-A(t)<=(lambda+eta)t`.
For sufficiently small `r`, monotonicity of `A` confines the positive
integrand in (8) to this interval. Integrating the two comparison
triangles bounds `D(r)` between `r^2/[2(lambda+eta)]` and
`r^2/[2(lambda-eta)]`; then let `eta` tend to zero.

Section 2 gives `r(epsilon)->0`. Equations (4)–(6) therefore give

\[
 D(r(\epsilon))=2\lambda\epsilon+o(\epsilon),
\]

because the geometric error is at most `epsilon*r(epsilon)/2=o(epsilon)`.
Combining this with (8) proves (7).

The same conclusion holds under the weaker near-contact condition

\[
 C_P(1-\epsilon,1)-C_E=o(\epsilon).                         \tag{9}
\]

Indeed the exact right side of (5) then acquires the negative of that
cost difference, which is another `o(epsilon)` error. A mere numerical
smallness of the cost difference without this scale is insufficient.

If instead `C_P(1-epsilon,1)>=C_E`, the law has no initial endpoint atom,
and (6) holds, the same calculation gives the one-sided necessary bound

\[
 \limsup_{\epsilon\downarrow0}
       \frac{1-f(1-\epsilon)}{\sqrt\epsilon}\le2\lambda.     \tag{10}
\]

Contact saturates this bound.

In particular, a finite P1 field with bounded initial slope at the
positive endpoint cannot satisfy the contact hypothesis and (6): it
would instead have `1-f(1-epsilon)=O(epsilon)`. This is a conditional
exclusion of that contact pattern for such a field, not a general
nonattainment theorem.

## 5. Rank-to-front time is universal

Let `T` be the radial Princess's first hit of `t+r(t)=1`, and let
`b=2T`. Because the Princess paths are ordered, their initial deficits
and front-hit times are ordered by the same rank. The early departure
distribution is determined by the sweep trace:

\[
                  \Pr(b\le s)=2[1-A(s/2)]\sim\lambda s.    \tag{11}
\]

Strict versus inclusive representatives agree at continuity ranks;
generalized inverses give the same asymptotic even if there are flat
trace intervals. In particular, the rank threshold whose initial radius
is `1-epsilon` has initial outer-tail mass `2r(epsilon)`. Let
`b(epsilon)` be its corresponding front-time quantile. Equations (7)
and (11) give

\[
 \boxed{b(\epsilon)=4\sqrt\epsilon+o(\sqrt\epsilon).}       \tag{12}
\]

Equivalently, its first front hit is at
`T(epsilon)=2sqrt(epsilon)+o(sqrt(epsilon))`. The coefficient in (12)
does not depend on the front density `lambda`.

This is a statement about ranks and first front contacts, not an
assumption that the intervening Princess paths have only one turn. A
curved initial path, a shadow segment, or an initial outward phase can
change the column correction `Delta` while preserving this asymptotic
rank-to-front correspondence. It is therefore compatible with, and
provides boundary data for, an initial-inward Monster sheet.

### The exact initial velocity budget

For the positive radial path `p_epsilon` of this rank, absolute continuity and the
two endpoint coordinates give the exact identity

\[
 \int_0^{T(\epsilon)}[1+p_\epsilon'(t)]\,dt=\epsilon.       \tag{13}
\]

Indeed `p_epsilon(0)=1-epsilon` and `p_epsilon(T)=1-T`. Therefore its average velocity
before the incoming-front hit is

\[
 \frac{1}{T(\epsilon)}\int_0^{T(\epsilon)}p_\epsilon'(t)\,dt
 =-1+\frac{\epsilon}{T(\epsilon)}
 =-1+\frac12\sqrt\epsilon+o(\sqrt\epsilon).                \tag{14}
\]

For every fixed `c>0`, the unit-speed constraint and (13) imply

\[
 \bigl|\{t<T(\epsilon):p_\epsilon'(t)\ge-1+c\}\bigr|
                         \le\frac{\epsilon}{c}.           \tag{15}
\]

In particular, the total time at outward unit speed is at most
`epsilon/2`. Thus the whole incoming interval has length of order
`sqrt(epsilon)`, whereas time at velocities bounded away from inward
unit speed is only of order `epsilon`. This permits short outward or
curved transients; it does not force them to be absent or to be a single
interval.

## 6. The initial-inward valley has an outward leading profile

There is a further compatibility consequence for the inward sheet. Use
the deficit coordinates of `INITIAL_INWARD_SHEET_CONTACT.md`, so

\[
 \phi(z)=f(1-z),\quad K(z)=A(z/2),\quad
 L(a,z)=\mathcal F(1-a,z-1),\quad0<a\le z<1.
\]

Suppose an inward row `I_(a,z)` and its associated principal row
`P(1-z,1)` have the same cost, and `K(z)>phi(a)`. Put
`d=(z-a)/2`, `h=z/2`, `l=L(a,z)` and `s=phi(z)`.
Let `J_left` be the field integral on the inward row's initial left
leg, and `J_right` its integral on the principal row's first right
leg up to the same first-turn point. Both legs last `d`. Finally put

\[
 E_{\rm clip}=\int_d^h
       [\phi(a)-F(t,1-z+t)]_+\,dt,
\]

\[
 B=d[\phi(a)+l]-J_{\rm left}-J_{\rm right}+E_{\rm clip}.
\]

Subtracting the two exact cost formulas gives

\[
 H(l)-H(s)=B,
 \qquad
 \boxed{0\le B\le\frac z2[\phi(a)-\phi(z)]
                         \le\frac z2[1-\phi(z)].}         \tag{16}
\]

Here the lower bound also follows directly from the geometry:
`J_left<=d*phi(a)` and `J_right<=d*l`. For the upper bound use
`J_left>=d*l`, `J_right>=d*s`, and
`E_clip<=(a/2)[phi(a)-l]`. These yield
`B<=d[phi(a)-s]+(a/2)[phi(a)-l]<=(z/2)[phi(a)-s]`.

Assume the flat E/P contact and front hypotheses of Sections 1–4.
Uniformly over any such active inward points with `z` tending to zero,

\[
 \boxed{1-L(a,z)\sim2\lambda\sqrt z,\qquad
 0\le L(a,z)-\phi(z)\le
                         \left(\frac\lambda2+o(1)\right)z.}     \tag{17}
\]

Indeed put `r_z=1-phi(z)` and `r_l=1-l<=r_z`.
Equation (16) says
`D(r_z)-D(r_l)=B=O(z^(3/2))`. Since
`D(r_z)~2lambda z`, the triangle comparison in (8) gives
`r_l~r_z~2lambda sqrt(z)`, uniformly. Its strengthened chord form is

\[
 D(r_z)-D(r_l)\ge
    \frac{r_z+r_l}{2(\lambda+\eta)}(r_z-r_l)
\]

for any fixed positive `eta` and sufficiently small `z`. Combining
this with `B<=z*r_z/2` and then letting `eta` tend to zero proves the
second bound in (17).

The initial deficit of the valley's rank is consequently asymptotic to
`z`. Its position is, to leading rank order, that of the rank initially
at `1-z` moving outward to the inward Monster's first turn. The actual
curved attachment is in the smaller CDF correction in (17); it is not
excluded by the long, mostly inward front-approach interval of Section 5.

This conclusion is about **individual active inward contacts**. It does
not say that every point of the parameter triangle is active. Inactive
incoming strips still contribute to the full column correction `Delta`
and cannot be filled using (17) without a separate argument.

The theorem supplies checkable asymptotic interface conditions for a
candidate continuum construction. It does not show that an optimal law
has positive sweep mass, a principal contact interval extending to the
endpoint, or the regular front behavior (6).
