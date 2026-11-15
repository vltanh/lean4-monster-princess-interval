# Off-front affine center returns and exterior transfer

## Scope

This continues the exact conditional result in
**AFFINE_CENTER_ZENO_ATTACHMENT.md**. It proves an off-front chain
identity and short-return comparisons with explicit inverse and exterior
hypotheses. It does not solve the entire off-front continuation or give
a global equilibrium.

The saved field is
**packages/interval_cdf_discovery/snapshots/endpoint_joint_i1_field.json**,
blob **5c45d042ee9948faebc03354c3e1e2ee3cbec1a5**.
All new physical fixtures use complete CDF moments. The initial-prefix
examples also use the independent unit-route first-capture engine.

The closed long-front branch is globally slack for this field at every
common payoff at most \(3/2\): its transformed continuation trace exceeds
\(3/2\). The relevant arrivals have \(n>Z(t)\).

## 1. Arbitrary first-center attachment

Let a monster remain positive until its first center visit \(\sigma\).
Allow arbitrary speed, turns, endpoint visits, and accumulating turns.
Its running strict lower and closed upper radial records are \(L_t,M_t\).
Before \(\sigma\), only the positive-copy rank band of mass \(M_t-L_t\)
has been captured. Put \(M=M_\sigma\); at the center \(L_\sigma=0\).

The layer-cake identity, including initial and characteristic atoms, is
\[
 \int_0^M\tau_q^+\,dq
 =\sigma M-\int_0^\sigma(M_t-L_t)\,dt.
\tag{1}
\]
The negative ranks through \(Z(\sigma)\) are caught at \(\sigma\).
Their moment cancels the center-factorization term
\(T_\sigma(Z(\sigma))/2=\sigma Z(\sigma)/2\). Thus the exact optimized
total after this prescribed prefix is
\[
 \boxed{
 W(\sigma,M)+\frac12\left[
 \sigma M-\int_0^\sigma(M_t-L_t)\,dt
 \right].}
\tag{2}
\]
No record is reset before the first center.

For an affine phase
\[
 R(U,V)=kU-\ell V+c,\quad d=k-\ell,\quad Z(t)=dt+c,\quad 0<8\ell<k,
\]
with terminal boundary \(b\), write \(q_b=Z(b)\). If the full exterior
attachment passes, the exact long-front trace is
\[
 W(t,Z(t))=C_*+ct/2,
\]
\[
 C_*=(b+2)(1-q_b)+db^2/2
 -\frac9{16}\left[k-4\ell-\sqrt{k(k-8\ell)}\right].
\tag{3}
\]
An active first-center front family therefore requires
\[
 \frac12\int_0^{Z(\sigma)}\tau_q^+dq
   =V_{\rm game}-C_*-c\sigma/2,
\tag{4}
\]
or, equivalently,
\[
 \int_0^\sigma(M_t-L_t)dt
 =d\sigma^2+2c\sigma+2(C_*-V_{\rm game}).
\tag{5}
\]
For the saved field,
\[
 \min_{57/64\le t\le\tau}W(t,Z(t))
 =W(\tau,Z(\tau))\simeq1.504521793992329>3/2
\]
exactly. Since the moment in (4) is nonnegative, this front is not an
active first-center attachment at a target at most \(3/2\).

For fixed \(b\), the hypograph of \(C_*\) is the second-order cone
\[
 w\ge0,\quad \|(w,4\ell)\|_2\le k-4\ell,
\]
\[
 C\le(b+2)(1-c)-(\tfrac12b^2+2b)(k-\ell)
 -\tfrac9{16}(k-4\ell-w).
\tag{6}
\]
Maximizing over \(w\) recovers (3). A smaller \(w\) is only a lower
scalar certificate and cannot silently replace the Riccati curvature.
With \(H=b-t_0\), the long-front-duration gate is
\[
 \ell/k\le H(H+3)/[2(2H+3)^2].
\tag{7}
\]
These parameter gates do not replace the exterior response audit.

## 2. Complete off-front chain energy

Start from \((t,n)=(t,Z(t)+y)\), \(y\ge0\). Let productive lengths
\(h_1,\ldots,h_m>0\) sum to \(H=b-t\), with
\[
 kh_1\ge y,\qquad kh_j\ge\ell h_{j-1}\quad(j\ge2).
\tag{8}
\]
Put \(g_0=y,\ g_j=\ell h_j,\ A=k/8-\ell/2\). The chain followed by
the appropriate endpoint tour has cost
\[
 C_{\rm front}-dt^2/2-ty-y^2/(8k)+\mathcal E_m,
\tag{9}
\]
where
\[
 \begin{aligned}
 \mathcal E_m={}&A\sum h_j^2
 -\frac\ell2\sum_{j<m}h_jh_{j+1}
 -\frac y2h_1-\frac{3\ell}2h_m\\
 &-\frac1{8k}\sum_{j<m}(g_{j-1}-dh_j)_+^2
 -\frac12(g_{m-1}-dh_m)_+ .
 \end{aligned}
\tag{10}
\]
The initial hinge is retained. The final hinge is **linear**, because
\(T_b(q)=bq+(q-q_b)_+\); an affine inverse beyond \(q_b\) would be wrong.

This follows from the exact renewal kernel
\[
 K(t,e;n)=\frac12[T_t(N)-T_t(n)+T_e(N)-T_e(n)],
 \qquad N=R(e,t).
\]
Productivity puts every earlier inverse used by the original chain
before its following return. The verifier checks (9) against full
saved-field CDF moments, with all three hinge types.

## 3. Short-return merge with full continuation records

Consider two consecutive productive returns \(p,q\) from gap \(y\),
where the first is short:
\[
 dp\le y\le kp.
\tag{11}
\]
At \(e=t+p+q\), the original and merged captured ranks are
\[
 n=Z(t)+y,\quad N_1=Z(t)+kp,\quad
 N_2=Z(t+p)+kq,\quad
 \widehat N=Z(t)+k(p+q)=N_2+\ell p.
\]
Any genuine balanced-tail value satisfies
\[
 V(e,\widehat N)-V(e,N_2)
 \le-\int_{N_2}^{\widehat N}\beta_e(u)\,du.
\tag{12}
\]
Indeed each omitted reflected pair has mean future capture time at least
\(\beta_e(u)\), for every fixed continuation.

Assume the old lower band \(n\le u\le N_1\) has its affine inverse at
\(e\), and the added upper band satisfies
\(\beta_e\ge\beta_e^{\rm aff}\). The first gate holds if the original
plan has a following productive return before \(b\), or a suitable front
reset there. The extra ranks may have inverses beyond \(b\).

Put \(P=\ell p,\ g=y-dp\in[0,P]\). Twice the merged-minus-original
cost is at most
\[
 -kpq/2-gq-\ell^2pq/(2k)
 +\frac{g^2-P^2+(P-dq)_+^2-(g-dq)_+^2}{4k}.
\tag{13}
\]
To derive (13), expand the two renewal kernels and use (12). The
time-\(e\) remainder is
\(\int_n^{N_1}\beta_e-\int_{N_2}^{\widehat N}\beta_e\);
the exterior comparison therefore has the favorable direction.
The bracket is nonpositive because
\((z-dq)_+^2-z^2\) is nonincreasing on \(z\ge0\). The other terms
are strictly negative for \(p,q>0\).

The merge may leave the affine inverse domain. Its replacement must
then use the actual exterior envelope. This is not a deletion theorem
that keeps every path in a fixed-\(b\)-only subclass.

For the saved field the needed inverse lower bound is exact:
\(R(U,V)\le kU-\ell V+c\) on all relevant interior points, and
\(Z(7/8)+2k\ge1\) includes the closed endpoint jump. The verifier
checks 408 vertices, no domain-crossing triangles, and zero minimum
CDF gap. All 36 merge fixtures put the old inverse endpoint at \(b\)
while the added ranks genuinely use the post-\(b\) field.

## 4. Final short return versus the earlier endpoint tour

At state \((s,n)\), suppose
\[
 n\ge q_b,\quad H=b-s,\quad N=R(b,s)=q_b+\ell H\ge n.
\]
Compare the tent returning at \(b\), followed by its endpoint tour,
with a direct endpoint tour from \(s\). The exact rank comparison is
\[
 2\Delta=(H-2)(1-n)+\int_N^1(b+3-\beta_s(q))dq.
\]
Since \(\beta_s(q)\le s+1\),
\[
 2\Delta\ge2H(1-N)-(2-H)(N-n)
 \ge H[2(1-N)-(2-H)\ell].
\tag{14}
\]
All opposite survivors are endpoint-only after the first tour, using
the future rank barrier. Thus
\(q_b+\ell(1+H/2)\le1\) suffices for domination. For all \(H\le2\),
the stronger convenient gate is \(q_b+2\ell\le1\). Its exact saved-field
margin is \(6776671717/31250000000>0\).

This is an exterior alternative. It does not remove the final linear
hinge from the identity (10).

## 5. Quadratic transfer and count selection

Normalize
\[
 \mathcal F(t,y)=V(t,Z(t)+y)+dt^2/2+ty+y^2/(8k).
\]
One productive return gives
\[
 \mathcal F(t,y)=Ah^2-yh/2-(y-dh)_+^2/(8k)
                  +\mathcal F(t+h,\ell h).
\tag{15}
\]
A nonshort internal return has \(h\ge y/d\), so its hinge vanishes.
A last short action followed by an exterior return remains in the
exit envelope unless its own comparison has been proved. Empty waits
before productivity can be absorbed into the next tent; a first front
hit or an accumulation at the front remains a reset boundary.

For a quadratic next piece
\(F=\alpha t^2+\beta ty+\gamma y^2+\delta t+\epsilon y+\zeta\),
the return variable has coefficients
\[
 a_h=A+\alpha+\beta\ell+\gamma\ell^2,\quad
 b_h=(2\alpha+\beta\ell)t+\delta+\epsilon\ell-y/2.
\]
If \(a_h>0\), the stationary \(h=-b_h/(2a_h)\) is affine in \((t,y)\)
and gives a quadratic value. Affine feasibility endpoints also give
quadratic values; if \(a_h\le0\), endpoints suffice. A finite quadratic
exterior envelope therefore permits exact piecewise-quadratic transfer
without refining the CDF.

For a fixed-\(b\), no-hinge stationary chain, set
\[
 \theta=\frac{1-\sqrt{1-8\ell/k}}{1+\sqrt{1-8\ell/k}},\
 C_0=\ell/(4\theta),\
 a_0=\theta y/\ell,\ b_0=3\theta.
\]
Its energy is
\(C_0[h^TK_mh-2a_0h_1-2b_0h_m]\), with diagonal \(1+\theta^2\)
and neighboring entries \(-\theta\). It is strictly convex.

Define
\[
 c_m=\frac{1-\theta^m}{(1-\theta)(1+\theta^{m+1})},\
 P_m=\frac{m-2\theta c_m}{(1-\theta)^2},
\]
\[
 u_m=\frac{1-\theta^{2m}}{1-\theta^{2m+2}},\
 v_m=\frac{\theta^{m-1}(1-\theta^2)}{1-\theta^{2m+2}}.
\]
When only \(\sum h_j=H\) is active, the energy is
\[
 C_0\left[-u_m(a_0^2+b_0^2)-2v_ma_0b_0
 +\frac{((a_0+b_0)c_m-H)^2}{P_m}\right].
\tag{16}
\]
The lengths solve
\(K_mh=a_0e_1+b_0e_m-\lambda{\bf1}\), with
\(\lambda=((a_0+b_0)c_m-H)/P_m\), and must pass all trace gates.

The negative interaction \(-2v_ma_0b_0\) explains why a finite chain
can beat separately optimized decay, front wait, and growth. Those
one-source solutions cannot just be added. A candidate beating the
separated energy \(-C_0(a_0^2+b_0^2)\) by \(\varepsilon>0\) permits
the geometric count cutoff
\[
 E_m+C_0(a_0^2+b_0^2)\ge-2C_0a_0b_0\theta^{m-1}.
\]
Boundary counts, front resets, and exterior attachment remain explicit
obligations. This note does not assert an all-count optimum.

## 6. A relevant actual arrival

Start at \(+1/16\), turn outward at characteristic \(U=7/8\), and first
reach center at \(t=7/8\). Then
\[
 n=258532002831/500000000000\simeq0.517064005662,\quad Z(t)=0,
\]
while \(R(b,t)=655898601421/10^{12}\).
The exact immediate exterior optimum returns at \(262143/262144\);
its total cost, including the real initial prefix, is
\[
 1929434720496067479221702069181/
 1355452266960650240000000000000
 \simeq1.4234619451575867.
\tag{17}
\]
The independent unit-route score agrees. A forced return at \(b\)
instead costs about \(1.44483738\). Thus the next relevant two-source
problem has a substantial initial gap and the genuine exterior
boundary, not only the endpoint source at \(b\).

For first-center times \(57/64,29/32,59/64\) with the same initial
start, the immediate exterior totals are respectively about
\(1.42805242,1.43323101,1.43346815\). These are response evaluations,
not new lower guarantees or an exclusion of preceding internal returns.

## 7. Reproduction and coverage

The verifier contains 96 full-CDF energy identities, 36 genuine
post-\(b\) merge comparisons, 12 terminal-short endpoint comparisons,
12 normalized transfer identities, and the 408-vertex inverse gate.
Its four actual initial-prefix examples use exact continuous quadratic
exterior minimization and independent unit-route scores.

The pure V8 entry point is Function(source)().verify(fieldData).
The report distinguishes identities, whole-cell gates, and diagnostic
arrival evaluations. The separate algebraic front packet was fully
replayed by the parent. No global game-value claim is made here.
