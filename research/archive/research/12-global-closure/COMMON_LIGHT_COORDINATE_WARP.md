# Common light-coordinate warps

This construction moves the existing geometric knots without introducing new
knots. It applies to arbitrary legal paths, not only affine CDFs. A finite
route-bank optimization remains a discovery problem; its minimum is not an
unrestricted lower guarantee.

## 1. A bijection of legal controls

Let psi be a strictly increasing continuous map of the real line satisfying

    psi(-x)=-psi(x),        psi(x+2)=psi(x)+2.

Then psi(0)=0 and psi(1)=1. Map each spacetime point by

    U=t+x, V=t-x,
    new_t=[psi(U)+psi(V)]/2,
    new_x=[psi(U)-psi(V)]/2.

For a speed-one path, U and V are nondecreasing. Their transformed versions
are also nondecreasing, so the image path has speed at most one. New time
is strictly increasing along the path and tends to infinity, because
psi-id is bounded and 2-periodic. The image is therefore a legal graph
over all nonnegative times.

The initial face U=-V remains time zero by oddness. The center U=V remains
the center. The endpoint faces U=V+2 and V=U+2 remain the two endpoints by
periodicity. Reflection commutes with the map. Applying psi^{-1} proves
that this is a bijection on each player's legal control space.

Two image paths meet exactly when their original paths meet: injectivity
in both characteristic coordinates prevents a new intersection between
distinct original spacetime points. The time order along either path is
preserved. Thus every first capture at original coordinates(Uc,Vc) occurs
at new time[psi(Uc)+psi(Vc)]/2.

For an ordered radial field,

    R_new(U,V)=R_old(psi^{-1}(U),psi^{-1}(V)).

A common knot warp maps each old right triangle affinely to another
axis-aligned right triangle. Nodal values and all nodal order constraints
are unchanged. Rational knot images and rational nodal values therefore
specify an exact legal field with the same number of nodes and triangles.

## 2. Convex geometry optimization

Fix a princess law mu and a reference monster m. Transform both by psi.
Their expected capture time is the linear functional

    C_m(psi)=1/2 E_mu[psi(Uc)+psi(Vc)].

Since every physical monster is the transform of a reference monster,

    inf_m J(T_psi mu,m)=inf_m C_m(psi).

The unrestricted response value for the warped princess law is therefore
concave in psi. Dually, for a fixed monster law nu, its unrestricted
princess response is a supremum of linear warp functionals and is convex.

Use knots 0=k0<...<kn=1 and increments d_i=psi(k_i)-psi(k_(i-1)).
The feasible closed knot set is the simplex d_i>=0,sum_i d_i=1.
For strict positive increments the piecewise-affine warp is an actual
bijection. The basis psi_i ramps from 0 to 1 on[k_(i-1),k_i], is constant
elsewhere on[0,1], and extends oddly and 2-periodically. Hence

    C_m(d)=sum_i d_i C_m(psi_i).

Each interval coefficient psi_i(y)-psi_i(x) is nonnegative for y>=x.
This also preserves positive survival-reward graph representations.
Dropping a tiny identity reward is not automatically safe uniformly in
d: an interval may expand. Any discarded-error bound must use its maximum
basis coefficient or the support function over the allowed warp set.

For finitely many reference monsters, maximizing their minimum is a small
linear program. Its value is only a finite-bank objective. New physical
attacks are pulled back through psi^{-1} before their capture-coordinate
row is added. No quantile discretization is required for the row itself.

## 3. Zero increments have a controlled approaching realization

Let psi0 be nondecreasing, possibly with flat intervals, and put

    psi_eps=(1-eps)psi0+eps id,        eps>0.

This is strictly increasing and

    ||psi_eps-psi0||_infinity
      <=eps ||id-psi0||_infinity.

For every reference monster, the two capture-coordinate functionals
differ by at most this same number, independently of its turn count,
capture time or history. Taking the infimum over ALL reference monsters
preserves the bound. The legal warped lower laws therefore approach the
formal boundary-warp response uniformly. One need not assert that the
degenerate physical limit law attains this response; it can acquire extra
contacts.

The analogous supremum bound holds for the warped upper law. Its
degenerate path images remain legal after erasing intervals of zero new
time; a zero new-time interval has zero spatial motion as well. First-hit
lower semicontinuity transfers a finite limiting upper ceiling to that
degenerate law.

## 4. A saddle-point capture-coordinate conservation law

Suppose(mu,nu) is an attained finite-value saddle with value C. For every
odd 2-periodic Lipschitz function f,

    E_mu,nu[f(Uc)+f(Vc)]=0.                         (1)

This does not require smooth first-capture dependence or endpoint
absorption.

Choose psi_eps=id+eps f for both signs of sufficiently small eps.
Let T_eps be capture for(mu,T_(psi_eps^-1)nu), and let

    M_eps=E[(f(U_eps)+f(V_eps))/2].

The two saddle inequalities, together with the exact common-warp capture
identity, give

    0 <= E[T_eps]-C <= -eps M_eps,
    |M_eps| <= ||f||_infinity.

Consequently E[T_eps]->C. The inverse-warped monster converges uniformly
to the original monster, with position error at most
2|eps| ||f||_infinity. First-contact lower semicontinuity gives
liminf T_eps>=T0 almost surely. Since T0 is integrable,

    E[(T0-T_eps)_+]->0,

and the preceding expectation convergence implies E|T_eps-T0|->0.
The princess is held fixed and is 1-Lipschitz, so the capture coordinates
converge in L1. Thus M_eps->M0. The positive and negative eps inequalities
force M0=0, proving(1).

Equivalently, the average of the two capture-coordinate distributions
modulo2 is invariant under reflection x->-x. Continuous odd test functions
follow by uniform approximation from Lipschitz ones. This is a necessary
condition for an attained saddle, not a sufficient equilibrium condition.

## 5. What survives the warp

Every dominance statement proved separately for each princess path survives:
if one monster captures each original path no later, its image captures each
transformed path no later as well. Rank-order statements and center-memory
barriers also survive after their time coordinates are mapped by psi. In
particular, a barrier whose old characteristic threshold is s0 has new
threshold psi(s0).

A comparison proved only after averaging capture times need not survive.
The time map depends on both capture coordinates. Therefore expected-cost
derivative signs, moment equalities and Bellman inequalities must be
rechecked in the warped field. One cannot import their old numerical
margins merely from physical legality or unchanged nodal ranks.

## 6. Exact portable coefficient builder

The function-body source in blob
1746e6ee8047e097d7af68a3401af190cfc2f7fa exports createWarpTools(E).
E is the repository's exact rational field API, preserved in blob
5714f57ada458f38ef8b46adb32be2472a009622. In V8:

    const E=Function(exactSource)();
    const W=Function(warpSource)().createWarpTools(E);

W exposes WarpCoordinates, captureFeatures, remapExactField, and dot.
The builder splits unit legs and center waits at every CDF triangle and
warp-knot crossing. It integrates the transformed time against the exact
new-capture measure, including strict/closed center and endpoint jumps.
It retains full rational coefficients. remapExactField bypasses any
coordinate-denominator approximation; warped knots can have large exact
denominators and must not be rounded back to the original dyadic grid.

The exact 484-by-34 matrix is preserved in blob
f4aa1a9ebc6cac9e4bb58a52b468a143e21ef139. Its original complete field is
blob5c45d042ee9948faebc03354c3e1e2ee3cbec1a5. All 483 unit-route rows match
the independent exact first-record scorer; the center-wait row matches its
previous physical certificate. Seven nonidentity warped-field and
warped-route captures also agree exactly, and all 6,936 warped transport
triangles pass. The matrix's finite-bank identity minimum is
approximately 1.423023479088547. These checks validate the feature
construction and explicitly do not prove unrestricted lower feasibility.

The native gated field iter008/iter011 was not used here. Its bytes became
inaccessible when the executor disconnected; its reported native hashes
are not evidence of a remote upload.
