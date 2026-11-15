# Completeness of finite analytic-exit potential certificates

Analytic proof independently reviewed, 2026-11-13. Exact rational
regressions accompany the formulas; no Lean compilation is claimed.

The [one-potential certificate](ANALYTIC_EXIT_POTENTIAL.md) is not merely
a sufficient finite ansatz. After allowing its rational characteristic
mesh and queue mesh to refine, its certified lower values approach the
security of every legal continuous interior Princess CDF. With absorption
time \(H=3\), these finite rational certificates have supremum equal to
the unrestricted game value \(V\).

The result is approximation completeness. It does not assert that an
optimal certificate has a particular finite mesh, or that the hierarchy
terminates exactly after finitely many refinements.

The essential analytic point is proved below: the exact stopped-clock
value is Lipschitz even at the queue state constraints and endpoint exit
faces. The smoothing argument then uses integral dynamic programming
inequalities directly and does not assume a differentiable value function.

## 1. The certificate domain and exact future value

Fix \(H>0\), and a legal symmetric signed Princess CDF with a continuous
interior-trace extension \(F_{\mathrm{int}}\) to the closed physical
strip. Suppose the Princess is endpoint absorbed by \(H\):

\[
 F_{\mathrm{int}}(t,x)=\frac12
 \qquad(t\ge H,\ -1\le x\le1).
\]

The actual strict endpoint values are

\[
 F^-(t,-1)=0,\qquad
 F^-(t,1)=F_{\mathrm{int}}(t,1).
\]

For the Lipschitz statement, assume \(F^-\) is uniformly \(L\)-Lipschitz
in physical time, including its endpoint traces:

\[
 |F^-(t',x)-F^-(t,x)|\le L|t'-t|
 \quad(-1\le x\le1).
\]

The positive-endpoint-free clock has cost \(F^-(t,-x)\), and the
negative-endpoint-free clock has cost \(F^-(t,x)\).
Put \(D=H+4\).

It is helpful first to define the future control problem without
artificial queue caps. At a state \((t,x,q_+,q_-)\), the queues are
credits already paid for. A future clock with cumulative newly charged
mass \(C_j(u)\) must satisfy

\[
 q_j+C_j(u)\ge u
\]

until the corresponding endpoint is first reached. At that endpoint
the remaining clock can be completed for zero cost. Future physical
paths have speed at most one, and all newly charged costs are
nonnegative. There is no need to retain surplus priced charges after
the relevant endpoint.

Let \(\mathcal W(t,x,q_+,q_-)\) be the infimum of this future charge
cost. All quantities here are additional future costs; previously
charged costs have already been paid.

The analytic continuation formulas show that this unrestricted future
problem is identical, on

\[
 \Omega_H=[0,H]\times[-1,1]\times[0,4]^2,
\]

to the stopped problem with the first exit at an endpoint, at time \(H\),
or at either queue cap \(4\). Its exact exit costs are

\[
 \begin{aligned}
 L(t,x,q)&=\int_q^{1+x}F_{\mathrm{int}}(t+u,x-u)\,du,
       &&\text{zero when }q\ge1+x,\\
 g_{x=1}&=L(t,1,q_-),&
 g_{x=-1}&=L(t,1,q_+),\\
 g_{q_+=4}&=L(t,x,q_-),&
 g_{q_-=4}&=L(t,-x,q_+),\\
 g_{t=H}&=\frac12\min\{
      (1-x-q_+)_++(3-x-q_-)_+,\\
 &\hspace{42mm}(3+x-q_+)_++(1+x-q_-)_+\}.
 \end{aligned}
\]

These exit values agree on all intersecting exit faces.
Write \(W=\mathcal W|_{\Omega_H}\).

The equivalence is statewise, including arbitrary initial credits.
After the first endpoint, discard the cost of the clock that has
become free and apply the exact one-clock continuation. At time \(H\),
all remaining uncredited active clock units cost one half, so the
shortest tour in a chosen endpoint order minimizes both first endpoint
times. A queue credit \(4\) covers that clock through an entire shortest
endpoint tour; the other clock attains \(L\).

These statements also prove that every future policy can be improved
to one whose endpoints are completed after at most

\[
 \max(H-t,0)+4\le D
\]

additional physical time. This normalization is valid for the future
credit problem, not only for a capture payoff starting with zero credits.

## 2. A uniform bound on charged mass

For a given future physical route, let \(\tau_j\) be the elapsed time
until its endpoint \(j\) is first reached. Cap a feasible cumulative
future clock at

\[
 B_j=(\tau_j-q_j)_+.
\]

The capped clock remains feasible, because for \(0\le u<\tau_j\),

\[
 q_j+\min(C_j(u),B_j)
  =\min(q_j+C_j(u),q_j+B_j)\ge u.
\]

Nonnegative charge costs cannot increase when mass is removed.
Hence an arbitrarily near-optimal normalized policy can be chosen
with charged mass at most \(\tau_j\le D\) on each clock. The total
priced charge mass is therefore at most \(2D\).

This mass bound is used in the time comparison below. Free endpoint
completion charges need not be counted.

## 3. Lipschitz continuity, including state-constraint faces

### Queue coordinates

More initial credit cannot increase the infimum: every policy feasible
from \(q_j\) is feasible from \(q_j+\delta\). Conversely, from the
smaller credit one may charge \(\delta\) immediately, at cost at most
\(\delta\), and then follow a policy for the larger credit. Thus

\[
 0\le \mathcal W(\ldots,q_j,\ldots)
       -\mathcal W(\ldots,q_j+\delta,\ldots)\le\delta.
\]

In particular \(W\) is \(1\)-Lipschitz in each queue, including at
zero and at the cap.

### Physical time

Take a near-optimal normalized route and clocks at time \(t\), and
use exactly the same relative route and clock charges at time \(t'\).
Prefix feasibility depends only on elapsed time and the initial
credits. Every unit charge changes its cost by at most \(L|t'-t|\).
The total charged mass is at most \(2D\). Therefore

\[
 \mathcal W(t',x,q)\le
 \mathcal W(t,x,q)+2DL|t'-t|.
\]

The shifted route need not itself obey the artificial absolute time
cutoff \(D\); it is a legitimate policy in the unrestricted future
problem and can subsequently be normalized without increasing cost.
Reverse \(t,t'\) to obtain

\[
 |\mathcal W(t',x,q)-\mathcal W(t,x,q)|
       \le2DL|t'-t|.
\]

This also holds when one of the times exceeds \(H\), since the field
is stationary there and the future value is the same endpoint-tour
formula.

### Physical position

Let \(\delta=|x-y|\). Move directly from \(x\) to \(y\) in time
\(\delta\), charging each clock only enough to keep its queue
nonnegative. The cost of these new charges is at most \(2\delta\).
The queues at the end are

\[
 q'_j=(q_j-\delta)_+,
 \qquad |q'_j-q_j|\le\delta.
\]

Append a policy for \((t+\delta,y,q')\). If the preliminary segment
has already visited an endpoint, ignoring that free completion can
only overestimate the remaining cost. Thus

\[
 \mathcal W(t,x,q)\le
    2\delta+\mathcal W(t+\delta,y,q')
 \le4\delta+\mathcal W(t+\delta,y,q).
\]

The time estimate, followed by the same argument with \(x,y\)
reversed, gives

\[
 |\mathcal W(t,x,q)-\mathcal W(t,y,q)|
      \le(4+2DL)|x-y|.
\]

These comparisons take place in the equivalent unrestricted future
problem. They do not assume that a steering comparison stays inside
the stopped box or avoids its exit faces.

Combining the three estimates proves

\[
 \boxed{
 |W(z)-W(z')|
 \le 2DL|t-t'|+(4+2DL)|x-x'|
       +|q_+-q'_+|+|q_--q'_-|.}
\]

For the global choice \(H=3,D=7\), the coefficients are \(14L\),
\(4+14L\), \(1\), and \(1\). The sharper completed-by-six normalization
of the original physical game does not automatically replace this
statewise future-credit bound.

## 4. Smooth strict subsolutions approximate the exact value

The four constant controls in the interior of \(\Omega_H\) are

\[
 v_1=(1,-1,-1,-1),\quad
 v_2=(1,1,-1,-1),\quad
 v_3=(0,0,1,0),\quad
 v_4=(0,0,0,1),
\]

with costs \(c_1=c_2=0\),
\(c_3=F_{\mathrm{int}}(t,-x)\), and
\(c_4=F_{\mathrm{int}}(t,x)\).
For each short interior constant-control segment, dynamic programming
gives

\[
 W(z)\le\int_0^h c_i(z+s v_i)\,ds+W(z+h v_i).
\]

No differentiability of \(W\) is needed for this inequality.

Contract the closed box slightly toward its center,

\[
 A_\epsilon z=(1-\epsilon)z+\epsilon z_*,
\]

then convolve \(W(A_\epsilon z+\cdot)\) with a smooth compactly supported
probability kernel whose radius is smaller than half the contraction
margin. This defines a smooth function \(W_\epsilon\) on a neighborhood
of the closed box.

Let \(a_\epsilon\to0\) be a uniform bound on
\(|W_\epsilon-W|\), and let \(b_\epsilon\to0\) bound the oscillation of
each cost \(c_i\) between any point and its contracted smoothing
neighborhood. For Lipschitz fields both bounds are \(O(\epsilon)\).

Average the preceding integral dynamic programming inequality over
the smoothing kernel, and divide by \(h\). The affine contraction
scales each control by \(1-\epsilon\). It follows directly that

\[
 \nabla W_\epsilon(z)\cdot v_i+c_i(z)\ge-b_\epsilon.
\]

This argument establishes the derivative inequality for the smoothed
function without an assumed differentiable or viscosity value function.
Nonnegativity of the costs makes the contraction factor harmless.

Define

\[
 \ell=3t+q_++q_-,\qquad B_H=3H+8.
\]

For every control, \(\nabla\ell\cdot v_i=1\), and
\(0\le\ell\le B_H\) on the box. Set

\[
 \widehat W_\epsilon
  =W_\epsilon+(b_\epsilon+\epsilon)(\ell-B_H)
       -a_\epsilon-\epsilon.
\]

Then every control inequality has strict slack:

\[
 \nabla\widehat W_\epsilon\cdot v_i+c_i\ge\epsilon.
\]

On every exit face, \(W=g\), so

\[
 \widehat W_\epsilon\le g-\epsilon.
\]

Finally \(\widehat W_\epsilon\to W\) uniformly. In particular its
initial values uniformly approach \(W(0,x,0,0)\).

This construction handles the state-constraint faces \(q_j=0\) and
\(t=0\) by contracting them into the interior before smoothing.
It never extends the value function through an inadmissible queue
state.

## 5. Finite tensor potentials and polar exit checks are dense

Fix a legal rational piecewise-affine field \(F_{\mathrm{int}}\) on
a rational characteristic triangulation. Refine that triangulation
by a nested, shape-regular mesh, and refine each queue interval.
Interpolate the smooth \(\widehat W_\epsilon\) with a continuous
physical P1 function tensored with bilinear queue interpolation.

Standard interpolation estimates, or iterated one-dimensional
interpolation and the affine triangle formula, give uniform convergence
of the function and of its first derivatives on each cell closure.
Thus a sufficiently fine interpolant \(W_h\) retains, for example,
half of the strict control and exit margins.

The four control expressions are affine in physical barycentric
coordinates and separately affine in each queue coordinate.
The finite vertex tests used by the LP are therefore exact for these
expressions.

On an endpoint exit, fix the irrelevant queue at each of its mesh
nodes; linearity in that queue covers all its intermediate values.
The remaining potential has degree at most two. On a queue-cap exit,
the potential also has total degree at most two. The exact one-clock
continuation has rational piecewise-quadratic charts, linear in the
nodal CDF values. Hence the quadratic polar conditions apply on each
chart/cell intersection.

On the time exit, split both endpoint-order tour costs along their
positive-part kink planes. The cost is affine on each resulting
polytope and \(W_h\) has total degree at most three. The cubic polar
conditions apply.

The sufficient polar conditions do not leave an approximation gap.
For a degree-\(d\) polynomial \(P\), its polar form at vertices of a
polytope of diameter \(h\) differs from \(P\) at any one of those
vertices by at most a fixed multiple of
\(\operatorname{Lip}(P)h\). This follows immediately from the explicit
quadratic and cubic polarization formulas: every evaluation point
is a convex combination of vertices, and the coefficients sum to one.
The constants \(3\) and \(9\), respectively, are sufficient.

For fixed \(F\) and fixed smooth \(\widehat W_\epsilon\), the
Lipschitz constants of the chart differences \(g-W_h\) are uniformly
bounded as the mesh refines. Every chart/cell intersection has
diameter tending to zero. Since the differences already have a
strict positive uniform margin, all their polar coefficients are
eventually positive.

The initial trace is piecewise affine in \(x\), so its lower bound
is exactly tested at initial mesh nodes.

Consequently, for every

\[
 c<\min_{-1\le x\le1}W(0,x,0,0),
\]

some finite tensor-potential certificate satisfies all control, exit,
and initial conditions. The strict margins permit the potential
nodal values and \(c\) to be rounded to rational numbers while
preserving all finitely many rational inequalities.

The minimum on the right is exactly the security of the common-quantile
Princess law with field \(F\), by the full-clock representation and
the analytic exits. Thus the finite potential hierarchy is complete
for each fixed legal rational piecewise-affine CDF.

## 6. Legal rational characteristic CDFs are dense

Use light coordinates

\[
 U=t+x,\qquad V=t-x.
\]

The transport condition becomes
\(F_U\ge0\) and \(F_V\le0\).
Triangulate an axis-aligned rational \((U,V)\) grid so every triangle
has one \(U\)-parallel edge and one \(V\)-parallel edge. Use reflection
symmetric diagonals and align the boundary and absorption lines.
The clipped boundary half-squares have the same property.

Sample a continuous legal field at the vertices, using the continuous
interior traces at \(x=\pm1\). Its nodal values are nondecreasing on
\(U\)-edges and nonincreasing on \(V\)-edges. For a P1 function these
edge differences are exactly its two partial derivatives, so the
interpolant is legal. Reflection symmetry and the value \(1/2\)
after the absorption time are preserved by the aligned mesh.
Uniform continuity gives uniform convergence as the mesh refines.

The nodal values can be made rational without losing any condition.
For an integer \(N\), use the nondecreasing symmetric quantizer

\[
 Q_N(y)=\frac{\lfloor Ny\rfloor+\lceil Ny\rceil}{2N}.
\]

It obeys

\[
 Q_N(1-y)=1-Q_N(y),\qquad
 Q_N(1/2)=1/2,\qquad
 |Q_N(y)-y|\le\frac1{2N}.
\]

Applying it only to sampled nodal values preserves both coordinate
orders, exact symmetry, endpoint absorption, and the range \([0,1]\).
Piecewise-affine interpolation restores continuity between nodes.

For two fields \(F,G\) absorbed by \(H\), the full-clock identity
immediately gives

\[
 |J_F(m)-J_G(m)|
    \le2D\|F^--G^-\|_\infty
    \le2D\|F_{\mathrm{int}}-G_{\mathrm{int}}\|_\infty
\]

on the Monster class completed by \(D\): each of the two clocks has
total mass \(D\). Minimize first over clocks and then over Monster
paths. Their security values differ by at most the same bound.
Thus the legal rational characteristic approximation also preserves
security in the limit.

## 7. Continuous interior fields are value dense at absorption time three

SHARP_OUTWARD_HORIZON_REDUCTION.md proves the parameterized inequality

\[
 S(\mu^T)\ge\min\{S(\mu),(T+1)/2\}.
\]

For a Monster that has visited the center by \(T\), outward forcing
weakly delays every surviving Princess capture. Otherwise its opposite
fair half cannot be caught until the opposite endpoint, no earlier than
\(T+1+|m(T)|\). Since \(V<3/2\), the choice \(T=2\) preserves security.
Thus Princess laws maximally outward after time \(2\), hence absorbed
by time \(3\), can have security arbitrarily close to \(V\).
They may have interior atoms.

Represent such a symmetric ordered law as a fair fixed sign times
a random nonnegative radius path \(R(t)\). Let \(Z\) be independent
uniform on \((0,1)\), and replace the radius by

\[
 R_\delta(t)=\min(1,R(t)+\delta Z).
\]

Every new path is legal, remains sign confined, and is still absorbed
by time \(3\). The coupling has uniform path distance at most \(\delta\),
so these path laws converge weakly to the original law.

For \(0\le x\le1\), the resulting interior CDF and its endpoint trace are

\[
 F_{\delta,\mathrm{int}}(t,x)
  =\frac12+\frac12\,\mathbb E
       \left[\min\left(1,\max\left(0,\frac{x-R(t)}{\delta}\right)\right)\right],
\]

and the negative side is determined by symmetry. This field is
continuous, has continuous endpoint traces, and is Lipschitz in
both \(t\) and \(x\), with constants at most \(1/(2\delta)\).
The actual strict value at \(-1\) remains zero.

Reordering these marginals by common quantiles gives a legal ordered
Princess law and weakly improves its security, by the existing
quantile-domination theorem.

To justify convergence of security despite strict capture, use the
compact Monster class of legal paths that complete both endpoints by
time \(7\). For any Princess law absorbed by \(3\), replacing the
Monster suffix after \(3\) by the fastest tour in its future endpoint
order proves that this class gives the unrestricted best response.

On the compact path product, first capture time is bounded by \(7\)
and lower semicontinuous. Indeed, capture by a fixed time is a closed
condition under uniform path convergence. If Princess laws
\(\mu_n\Rightarrow\mu\), choose nearly minimizing Monster paths \(m_n\),
first take a subsequence realizing the lower limit of their costs,
and then pass to a convergent subsequence \(m_n\to m\). The joint laws
\(\delta_{m_n}\otimes\mu_n\) converge weakly, so the lower
semicontinuity inequality gives

\[
 \liminf_n\inf_{m'}J(m',\mu_n)
    \ge J(m,\mu)\ge\inf_{m'}J(m',\mu).
\]

Thus the radial smoothing cannot lose a fixed amount of security
in the limit. Quantile reordering only improves this conclusion.
Continuous Lipschitz interior fields with endpoint atoms, absorbed
by \(3\), are therefore value dense for the unrestricted game.

## 8. The complete finite linear hierarchy

Use \(H=3\), \(D=7\), queue cap \(4\), and

\[
 \ell=3t+q_++q_-\le17.
\]

For any rational \(c<V\), first choose an outward-after-\(2\) Princess
law of larger security. Smooth its radii as in Section 7, then choose
a sufficiently accurate legal rational characteristic CDF as in
Section 6. Its security is still larger than \(c\). Sections 3--5
then supply a finite rational tensor-potential certificate with
initial bound at least \(c\).

Every such certificate is valid against every physical Monster path
by the one-potential theorem. Hence

\[
 \boxed{
 \sup\{c:\ c\text{ has a finite rational analytic-exit potential
 certificate with }H=3\}=V.}
\]

The unknown CDF nodal values, potential nodal values, and initial bound
enter all constraints linearly. Tail chart geometry, polar checks,
symmetry, transport, and initial conditions are finite on each mesh.
Their coefficients are rational when the meshes are rational.

The prototype's absorption horizon \(H=3\) is therefore globally
sufficient. The sharper physical horizon theorem supplies the
value-density step; the future-credit comparison and certificate
itself retain their safe statewise completion horizon \(D=7\).

The proof supplies a convergent hierarchy and finite certificates for
every strict lower target \(c<V\). It does not supply a uniform
finite mesh at which the exact value must be attained.

## 9. Sticky endpoints may also be imposed

[STICKY_CDF_DENSITY.md](STICKY_CDF_DENSITY.md) proves that stopping each
Princess at her first endpoint weakly increases capture against every
Monster. Stopped outward radial dithering then produces regular ordered
sticky CDFs with security tending from below to the original security.
The positive endpoint trace is nonincreasing. The nodal constraints
`F(t_next,1) <= F(t,1)` are preserved by characteristic interpolation
and the symmetric monotone rational quantizer. The same completeness
statement therefore holds with these additional finite linear constraints.
The regularization can preserve outward time 2, hence absorption time 3.
This still asserts approximation completeness, not finite exact attainment.
