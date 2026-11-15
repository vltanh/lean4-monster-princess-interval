# Exact long-front center continuation with an accumulating optimal path

**Scope.** This closes a center-continuation component of the saved
ordered princess field. It does not give the value of the unrestricted
interval game, certify that the saved field is optimal, or close its
initial-prefix and other phase inequalities.

The saved field is
`packages/interval_cdf_discovery/snapshots/endpoint_joint_i1_field.json`,
blob `5c45d042ee9948faebc03354c3e1e2ee3cbec1a5`.
The source-domain and exterior assumptions are exactly those in
`AFFINE_CENTER_ATTACHED_SUBSOLUTION.md`; the complete exit audit is
replayed here at the algebraic curvature, rather than inferred by
continuity from \(B=3000\).

## 1. Exact constants and value

On the wedge \(7/8\le V\le U\le b=15/16\), write
\[
 R(U,V)=kU-\ell V+c,\qquad Z(t)=dt+c,\quad d=k-\ell,
\]
with the exact constants given in the rational attachment note.
Set
\[
 D=1-8\ell/k=\frac{623060432741}{655898601421},\qquad
 \theta=\frac{1-\sqrt D}{1+\sqrt D},
\]
\[
 B_+=\frac{2}{(1-\sqrt D)^2}=\frac1{4(\ell/k)\theta},
 \qquad
 \tau=b-\frac{3\theta}{1-\theta}.
\tag{1}
\]
Here
\[
 \tau=\frac{39}{16}
       -\frac{1967695804263}{1246120865482}\sqrt D
       \simeq0.8984790728300504,
\]
which is strictly after \(t_0=57/64\).

Let
\[
 C_{\rm front}=(b+2)(1-Z(b))+db^2/2.
\]
The exact attached constant is
\[
 C_*=C_{\rm front}-\frac94\ell\theta
 =-\frac{149534660791}{10^{12}}
   +\frac{5903087412789}{10^{12}}\sqrt D.
\tag{2}
\]
For every center-front state with
\[
 57/64\le t\le\tau,\qquad n=Z(t),
\]
the unrestricted future balanced-tail value is
\[
 \boxed{V(t,Z(t))=C_*-\frac d2t^2.}
\tag{3}
\]
In particular,
\[
 V(57/64,Z(57/64))
 =-\frac{34284998454479}{8\cdot10^{12}}
   +\frac{5903087412789}{10^{12}}\sqrt D
 \simeq1.467793462469908.
\]
This is an absolute future-capture contribution at the stated center
state, not an interval-game payoff from time zero.

## 2. Lower bound: the full exit gate

Use
\[
 V_0(t,n)=-dt^2/2-t[n-Z(t)]
          -(B_++1/8)[n-Z(t)]^2/k.
\]
Its internal Riccati residuals are nonnegative. The exact replay
checks every exit from the reachable inverse domain
\[
 t_0\le s\le b,\qquad
 Z(s)\le m\le\min(R(s,t_0),R(b,s)).
\tag{4}
\]
The direct crossing minimum is exactly \(C_*\); endpoint and wait
minima are larger. The rank-boundary exits are the two-action
families (6) and (7) of the rational attachment note. Their full
rank-fiber, KKT, inverse-cell, and geometric arrangement is regenerated
over the quadratic field.

All signs are exact. A scalar is represented as
\(a+b\sqrt D\), \(a,b\in\mathbb Q\). Addition, multiplication, and
division use the quadratic relation. For opposite-signed coefficients,
the sign comparison reduces to the rational comparison of
\(a^2\) and \(b^2D\); equal-sign cases are immediate. The numerator
and denominator of \(D\) are nonsquares in lowest terms, so the
representation is a field. Floating conversion is used only for
descriptive decimal output.

The same complete quadratic-polytope argument therefore gives
\(V\ge V_0+C_*\) on (4). Every later front state lies in the reachable
cone from \((t_0,Z(t_0))\), so this lower bound applies throughout
the interval in (3). The proof retains actual outgoing inverses
after \(b\), the closed endpoint jump, and the first rank-boundary
exit. It does not extrapolate the affine CDF into the exterior.

## 3. An attaining continuous path

Start at center time \(t\le\tau\) with rank \(Z(t)\) captured on both
sides. Wait at center until \(\tau\). Define
\[
 e_j=\tau+\frac{3\theta^j}{1-\theta},
 \qquad j=1,2,\ldots .
\]
Then \(e_j\downarrow\tau\), \(e_1=b\), and
\[
 e_j-e_{j+1}=3\theta^j.
\]
On each interval \([e_{j+1},e_j]\), use a maximal unit-speed tent,
with alternating signs. At \(b\), sweep first toward the lagging
endpoint and then toward the other endpoint.

The tent heights tend to zero at \(\tau\), so this defines a
continuous 1-Lipschitz path. It has infinitely many returns
accumulating at the departure time, followed by a finite endpoint
tour. No finite turn bound is assumed.

Each return rank is
\[
 R(e_j,e_{j+1})=Z(e_j)+3\ell\theta^j.
\]
Every inverse needed before the final return lies before the next
larger return: the next length is \(1/\theta\) times the previous
one, whereas the affine inverse extension requires only
\((\ell/k)\) times that length. Thus the actual-field renewal moments
are exactly the affine moments. After the return at \(b\), all
remaining interior-capturable ranks are already below the captured
fronts, by the audited exterior barrier. The final endpoint formulas
therefore apply exactly.

## 4. Exact limiting cost, without a hitting-time continuity assumption

For the finite growing chain with lengths
\[
 3\theta^m,\ 3\theta^{m-1},\ldots,3\theta,
\]
first wait until its departure time. The exact productive-chain
identity gives the improvement over pure front waiting:
\[
 -\frac94\ell\theta\,(1-\theta^{2m}).
\tag{5}
\]
All short-return hinges vanish because the lengths increase.
The remaining initial square is positive for every finite \(m\).
Taking the limit in (5) gives (2).

This limit is also the cost of the continuous path in Section 3.
The finite and infinite paths agree after the finite chain's
departure. Before that time, the only ranks whose capture status
or capture time can differ lie in an interval of width at most
\[
 d\,\frac{3\theta}{1-\theta}\,\theta^m
   +3\ell\theta^{m+1}.
\]
Capture times are bounded by \(b+3<4\). The expected-cost difference
therefore tends to zero directly. No favorable continuity of first
hitting times is assumed.

The upper construction and lower exit certificate meet, proving (3).
Finite growing truncations are strictly above the value; the
accumulating path is an actual admissible optimizer for this
conditional continuation problem.

## 5. Structural consequence for a joint law

The exact front trace of the transformed potential is
\[
 W(t,Z(t))=C_*+\frac c2t.
\tag{6}
\]
This is a concrete boundary condition for the earlier center and
same-half prefix problems. It replaces a freely chosen continuation
constant on this branch.

If this branch is active in a globally matched law, its final
stationary exit must satisfy
\[
 b-s_*=3\theta,\qquad
 n_*-Z(s_*)=3\ell\theta^2,
\]
and the incoming prefix must meet the common payoff after adding
its actual captured-rank first moments. The all-initial sweep
constraints remain essential. A field may pass this entire local
center certificate and still fail an initial inward sweep or another
global response.

The saved field has such unresolved global deficits. Equation (3)
should be used as an exact continuation boundary in the joint
construction, not as evidence that those deficits disappeared.
