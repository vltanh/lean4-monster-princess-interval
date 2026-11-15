# Boundary projection and a finite exact response for a fixed P1 CDF

Analytic proof independently reviewed, 2026-11-13. Exact rational
regressions accompany the formulas; no Lean compilation is claimed.

This note completes the physical-cell step in
FOUR_LEG_AFFINE_RECORD_RESPONSE.md. The result concerns a supplied
continuous piecewise-affine Princess CDF. It does not assert that an
unrestricted optimal Princess CDF has a finite mesh.

## 1. A characteristic boundary half-cell

Use \(U=t+x\), \(V=t-x\). A physical boundary half-cell is the
intersection of an axis-aligned \((U,V)\) rectangle with the physical
strip \(-1\le x\le1\). In the usual characteristic mesh, its diagonal
boundary is \(x=1\) or \(x=-1\).

Suppose the interior CDF on this cell is

\[
 F_{\mathrm{int}}(t,x)=A+bU-cV,\qquad b,c\ge0.
\]

Extend this affine expression to the whole coordinate rectangle.
Apply the four-leg scalar theorem with the actual segment's
entry and exit scalar states and record interval.

The reconstructed path \(m_*(t)\) has speed at most one, the original
entry and exit positions and times, and nondecreasing \(U_*,V_*\).
It stays in their coordinatewise box, and hence in the coordinate
rectangle. It may leave the physical strip.

Every value of its affine scalar field \(Y_*(t)\) is inside the
prescribed exit record interval, which is contained in \([0,1]\).
That restriction is essential to the next step.

## 2. Clipping uses both endpoint record traces

Clip the reconstructed physical path:

\[
 \widehat m(t)=\min(1,\max(-1,m_*(t))).
\]

Clipping preserves the speed bound and the entry and exit states.
Its light coordinates are again nondecreasing. Consequently they
remain in the same entry/exit coordinate box. Since the path is now
inside the strip, it stays in the original boundary half-cell.

When \(m_*(t)>1\), spatial monotonicity of the affine extension gives

\[
 F_{\mathrm{int}}(t,1)\le Y_*(t)\le1.
\]

The actual endpoint CDF traces are

\[
 F^-(t,1)=F_{\mathrm{int}}(t,1),\qquad F^+(t,1)=1.
\]

They therefore bracket the hypothetical scalar value \(Y_*(t)\).
When \(m_*(t)<-1\), the corresponding relations are

\[
 0\le Y_*(t)\le F_{\mathrm{int}}(t,-1),
\]

and

\[
 F^-(t,-1)=0,\qquad
 F^+(t,-1)=F_{\mathrm{int}}(t,-1).
\]

Again the actual endpoint traces bracket the scalar value.
When no clipping occurs, both interior traces equal \(Y_*(t)\).

Thus, at every time, the actual cumulative lower record of the clipped
path is no larger than the scalar lower record, and its actual upper
record is no smaller than the scalar upper record. Its captured rank
interval contains the scalar interval pointwise.

The four-leg theorem improves the integrated scalar record range and
preserves its exit interval. Clipping can only improve these
comparisons. Therefore the clipped physical path does not increase
capture payoff on the cell, and its exit record state is at least
as favorable for every common continuation.

At the first actual endpoint contact, replace the remaining trajectory
by the direct unit-speed sweep to the opposite endpoint. This
universally dominates the clipped continuation. There is consequently
no need to count extra stationary boundary pieces introduced by
clipping.

The argument would be wrong if it used only the continuous interior
trace at an endpoint. The strict lower trace and inclusive upper
trace are both needed.

## 3. Constant cells and center cells

If \(b+c=0\), the field is constant throughout the cell and its
coordinate rectangle. Any two-bang physical route that uses the
fixed nonnegative \(U,V\) increments has the correct duration and
endpoints and preserves the scalar record state. Boundary clipping
and first-endpoint sweep dominance apply as above. No division by
\(b+c\) is used.

If only one of \(b,c\) is zero, the scalar monotone version of the
four-leg theorem applies. Its constant-\(F\) leg is still a legal
physical motion.

Some reflection-symmetric characteristic meshes split the square
crossing \(x=0\) along its center diagonal \(U=V\), rather than its
time diagonal \(U+V=\text{constant}\). The two halves have the same
affine field. Both center vertices have CDF value \(1/2\), so the
affine time derivative is zero; reflection symmetry gives the same
spatial derivative on the two halves. Merge them into one rectangle.

Every remaining interior triangle is bounded by coordinate lines and
a time diagonal. It contains the coordinatewise box between any
comparable entry and exit points. Rectangles have the same property.

## 4. No cell can be reentered

Along every physical path, \(U,V\) are nondecreasing.

For an interior time-diagonal triangle or a rectangle, any points of
the trajectory between two visits lie in their coordinatewise box,
which is contained in the cell. The path cannot leave and later reenter.

For a physical boundary half-cell, its only boundaries inside the
physical strip are coordinate lines. Leaving its coordinate rectangle
cannot be reversed by a monotone \(U,V\) path, and leaving through the
physical diagonal would leave the legal strip. It cannot be reentered
before first endpoint contact either.

Motion along a shared coordinate edge is already a unit-speed physical
leg. A time-diagonal edge is at one fixed physical time. Such edge
ties can be assigned to either incident cell and do not create an
infinite sequence of genuine cell visits.

## 5. A fixed-field finite response bound

Let the supplied rational P1 CDF be endpoint absorbed by time \(H\).
Extend its constant absorbed field to time \(H+2\), and let \(K\)
be the number of characteristic affine cells in the strip
\([0,H+2]\times[-1,1]\), after merging center halves.

For a fixed Princess law, the Monster may first normalize its suffix
after time \(H\) to the fastest endpoint tour in the chosen future
endpoint order. Its first endpoint is then reached by \(H+2\),
and the opposite endpoint by \(H+4\). After its first endpoint,
universal direct-sweep dominance permits one unit-speed tail.

Before that first endpoint, apply the local four-leg theorem successively
to the at most \(K\) visited cells. Each replacement preserves the
physical entry and exit states and the exit record interval. If
boundary clipping first reaches an endpoint earlier, terminate the
cell procedure and use the dominating opposite sweep.

In every nonconstant cell the possible physical velocities are

\[
 +1,\quad-1,\quad\frac{c-b}{b+c}.
\]

At most four unit-speed legs and one constant-\(F\) leg are needed.
A constant cell needs at most two unit-speed legs. Therefore

\[
 \boxed{\text{Some exact best response uses at most }5K+1
        \text{ physical affine pieces}.}
\]

The final \(1\) is the opposite-endpoint sweep. Here \(K\) includes
the constant extension through \(H+2\); if only pre-\(H\) cells are
counted, the direct analogous bound has two final endpoint-tour legs.

Existence of a best response is not assumed from a smooth payoff.
Legal Monster paths completed by \(H+4\) form a compact class, and
capture time is bounded and lower semicontinuous. Hence a fixed
Princess law has a minimizing path in this class. The preceding
replacements give another minimizing path of the stated form.

## 6. Finite rational quadratic programs

For a fixed rational field, the finite velocity set above is rational.
Choose a cell sequence, the order and directions of its at most five
pieces per cell, and a branch for all record comparisons. There are
finitely many such choices.

All piece durations are nonnegative variables. Physical time, position,
light coordinates, and affine CDF values at their endpoints are affine
functions of these durations and the initial Monster position.
Cell-membership conditions are linear. Record winners are selected
by linear comparisons.

On a constant-speed segment, the field value is affine in elapsed
time with a fixed rational slope. Its crossing time with a previous
record is therefore affine in the parameters, after choosing whether
the crossing occurs within the segment. If that slope is zero, use the
constant comparison or identity branch; no division by a zero slope is
made. Integrating the resulting
piecewise-affine survival function gives a rational quadratic
polynomial in the parameters.

The opposite-endpoint tail has the same description after subdividing
it by the fixed CDF mesh and its record crossings. Its nominal start
time and all resulting crossing times are affine in the parameters.
Thus each fully specified branch gives a rational quadratic objective
on a bounded rational polytope.

### Contact faces

Before the nominated first endpoint, a branch may use the interior
record formula. On its closure a limiting prefix can touch an endpoint
earlier. Ignoring that earlier endpoint jump can only *overestimate*
the physical capture payoff: the actual strict/inclusive traces enlarge
the captured rank interval, as proved above.

Therefore every closed-branch quadratic objective is at least the
payoff of its represented physical path, and hence at least the true
best-response value. Proper first-contact branches are also included
and contain the normal-form best response, where the formula is exact.
The minimum over all closed branches is consequently the true value.

This avoids replacing an open-face infimum by an unjustified physical
minimum. Earlier-contact paths have their own first-contact branches,
including endpoint starts at time zero. Zero-length pieces and empty
pre-endpoint prefixes are permitted.

### Rational attainment

A quadratic polynomial with rational coefficients has a rational
minimum on any nonempty compact rational polytope. To see this, take
a global minimizer and its minimal face. It is relatively interior
in that face, so its tangential gradient vanishes. This is a rational
linear system on the affine hull of the face.

The system has a rational solution arbitrarily close to the given
minimizer within the relative interior. All its stationary solutions
on that face have the same quadratic value: their differences lie
in the face tangent space and annihilate the tangential Hessian.
Thus some rational point attains the same minimum. Zero-dimensional
faces are rational vertices and require no separate argument.

It follows that a supplied rational P1 CDF has a rational exact
best-response value, computable by a finite enumeration of rational
quadratic programs and active-face linear systems.

This conclusion is fixed-field only. It neither bounds the mesh
needed by an optimal Princess CDF nor turns the globally complete
potential hierarchy into an asserted finite exact equilibrium.

## Interior-cell improvement

[TWO_RUN_AFFINE_CELL_WITH_CONTINUATION.md](TWO_RUN_AFFINE_CELL_WITH_CONTINUATION.md)
includes the entire future cost when replacing an interior affine-cell
segment. That cost is concave and nonincreasing in both exit record extents,
so one of the two unit-speed corner orders suffices. With K_int interior
cells and K_bd physical boundary half-cells, the piece bound improves to
`2 K_int + 5 K_bd + 1`. The earlier boundary argument and all finite-QP
contact-face reasoning remain unchanged. The two-run scalar comparison
alone does not justify replacing a boundary half-cell by its corner paths,
since an affine extension outside the strip can leave the rank interval.
