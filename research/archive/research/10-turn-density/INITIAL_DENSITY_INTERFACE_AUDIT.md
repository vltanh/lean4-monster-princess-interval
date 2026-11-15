# Initial two-density interface: exact audit and deletion

## Scope

This note concerns an interior initial point of an ordered symmetric fan law, before any actual center or endpoint contact. It audits local capture formulas, records a counterexample to an overbroad concavity argument, and proves a conditional deletion. It does not by itself prove a uniform global bound on pre-first-center turns.

After shifting the source to time zero and spatial position zero, the local signed CDF has the form
\[
F(t,x)-q_0=\alpha t+
\begin{cases}
\beta_-x,&x\le0,\\
\beta_+x,&x\ge0,
\end{cases}
\qquad \beta_\pm\ge|\alpha|.
\tag{1}
\]
The proof may assume \(\alpha\ge0\) by reflection. The strict case below uses \(\beta_\pm>\alpha\).

For bang-bang fixed-width translation fans, (1) is the only possible nontrivial initial split. A moving edge of slope \(+1\) or \(-1\) through the source lies on the corresponding boundary of its forward light cone. A stationary edge through the source can split its interior into two half-cells. All such stationary edges give one common interface; continuity forces a common time coefficient \(\alpha\).

The same statement holds for reflected outward fans: their marginal interval-density edges still have slopes \(0,\pm1\). The ordered realization is essential.

## 1. The exact first-capture correction

Let alternating physical turning amplitudes be \(x_i\ge0\), starting to the right. Write
\[
\sigma_i=(-1)^{i+1},\quad
S_i=2\sum_{j<i}x_j,\quad
t_i=S_i+x_i,\quad
c_i=\beta_{\sigma_i}+\sigma_i\alpha.
\]
Here \(S_i\) is the interface-crossing time preceding the outward portion of turn \(i\). Its signed record magnitude is
\[
r_i=c_i x_i+\sigma_i\alpha S_i.
\tag{2}
\]
Assume these are productive extrema, so \(r_i\ge r_{i-2}\ge0\), with the initial records explicitly supplied.

If the newly caught band lies wholly on the half containing its extremum, its capture moment is
\[
\mathcal M_i=
\frac{r_i^2-r_{i-2}^2}{2c_i}
+\frac{\beta_{\sigma_i}S_i}{c_i}(r_i-r_{i-2}).
\tag{3}
\]
For \(\alpha>0\), all new lower records lie in \(x<0\). A positive-going leg may begin catching new upper ranks while it is still in \(x<0\). Its exact correction to (3) is
\[
\boxed{\quad
H_i=\frac12\left(
\frac1{\beta_++\alpha}-\frac1{\beta_-+\alpha}
\right)
(\alpha S_i-r_{i-2})_+^2.
\quad}
\tag{4}
\]
Indeed both inverse formulas meet at rank \(\alpha S_i\); integrating their affine difference over the missed triangular band gives (4).

The correction is positive when \(\beta_->\beta_+\). It cannot be discarded from a minimization. If a block ends after a left turn, its final return to the interface may itself create an upper band; append that interface endpoint as a zero-amplitude positive extremum when this band is productive. Otherwise retain the final return as a nonproductive connector.

## 2. Conditional parity concavity when (4) vanishes

Set
\[
c_+=\beta_++\alpha,\qquad c_-=\beta_--\alpha,
\]
\[
\kappa_+=\frac{\beta_+-\alpha}{c_+},\qquad
\kappa_-=\frac{\beta_-+\alpha}{c_-},\qquad K=\kappa_+\kappa_-.
\]
When the opposite-parity records are fixed, successive positive-side interface times satisfy
\[
S_{j+1}=K S_j+\frac{2\kappa_-}{c_+}r_j
+\frac2{c_-}r^-_j.
\tag{5}
\]
Up to a positive factor, the quadratic variation in the intermediate positive records \(v_j\) is
\[
Q(v)=-\sum_jv_j^2+
(1-K)\sum_{h<j}K^{j-1-h}v_hv_j.
\tag{6}
\]
The fixed final-time constraint is
\[
\sum_{j=1}^mK^{m-j}v_j=0.
\]
Put \(z_0=z_m=0\), \(z_j=Kz_{j-1}+v_j\). Then
\[
\boxed{\quad
Q(v)=-\frac{K+1}{2}
\sum_{j=1}^m(z_j-z_{j-1})^2<0
\quad(v\ne0).
\quad}
\tag{7}
\]
The negative parity has the same identity with its corresponding positive factor. Thus fixing the time budget restores strict parity concavity even when the unconstrained Hessian is indefinite.

A fixed nonzero initial captured band changes only the constant and linear terms. In a single affine cell with initial band \([-b,a]\) and first positive leg, the correction to the zero-band moment is
\[
-\frac{a^2}{2c_+}-\frac{b^2}{2c_-}
-b\left(\frac1{c_+}+\frac1{c_-}\right)x_1.
\]
The Hessian is unchanged.

Equation (7) applies to the no-crossover quadratic. If \(\beta_-<\beta_+\), (4) has a negative coefficient, so each additional term is a negative multiple of the square of a positive part of an affine function and preserves conditional concavity. If \(\beta_->\beta_+\), that conclusion is false.

## 3. Exact counterexample to full hinged parity concavity

Choose
\[
\alpha=\frac14,\qquad \beta_+=\frac12,\qquad \beta_-=2.
\]
Take 49 alternating physical extrema
\[
x_j=\frac{2^{j-1}}{2^{53}},\qquad j=1,\ldots,49.
\]
All are productive and all 24 positive crossover hinges are active. Fix every negative record and the final positive record. For the 24 intermediate positive records use
\[
\varepsilon=2^{-126},\quad
z_j=\min(j,24-j)\varepsilon,\quad
v_j=z_j-\frac37z_{j-1}.
\]
The two perturbations \(r_j^\pm=r_j\pm v_j\) retain exactly the same exit time, exit position, and two final records. Independent continuous first-capture integration gives
\[
\boxed{\quad
\frac{\mathcal M(+)+\mathcal M(-)-2\mathcal M(0)}
{2\varepsilon^2}=\frac{1504}{441}>0.
\quad}
\tag{8}
\]
The shared relative exit data are
\[
t=\frac{422212465065983}{4503599627370496},\qquad x=\frac1{32},
\]
\[
L=-\frac{351843720888321}{18014398509481984},\qquad
M=\frac{703687441776639}{18014398509481984}.
\]

This field is realized by a legitimate clipped translation fan near the actual initial point \(a=1/2\). Its four raw positive components, each followed by fair reflection, are:

| Weight | Base during the audit | Translation interval |
|---|---|---|
| \(1/4\) | \(p(t)=1/2-t\) | \([-1/4,1/4]\) |
| \(1/4\) | \(p(t)=1/2\) | \([-1/4,1/4]\) |
| \(3/8\) | \(p(t)=1/2\) | \([-1/8,0]\) |
| \(1/8\) | \(p(t)=1\) | \([0,1/8]\) |

On \(0\le t\le1/8\), \(|x-a|\le1/32\), the signed CDF is exactly (1) with \(q_0=13/16\). The moving interval's two edges remain outside this rectangle, the third row supplies only the stationary left-density increment, and the last row is an endpoint atom. Thus the affine formula holds on the entire rectangle, not only at test points.

Appending the same endpoint tour to all three prefixes preserves (8): the exact full ordered-fan capture scorer again returns \(1504/441\). This is a counterexample to a proposed proof step, not evidence that an infinite-turn optimum is necessary.

## 4. Deleting an overtaken right-left pair

Let
\[
\alpha>0,\quad B=\beta_-\ge b=\beta_+\ge\alpha,\quad
C=B-\alpha>0,\quad D=B+\alpha,\quad P=b+\alpha.
\]
At an interface state allow arbitrary previously captured records \([-b_0,a_0]\), containing the current rank zero.

Take a productive right tent of duration \(p\), then a productive left tent of duration \(q\), with \(T=p+q\). Suppose
\[
\alpha T\ge\frac{Pp}{2}.
\tag{9}
\]
The final interface flow has overtaken the right peak. Replace the pair by one maximal left tent of duration \(T\).

The right peak is \(m=Pp/2\). The old and new lower magnitudes are
\[
r_{\rm old}=\frac{Cq}{2}-\alpha p,\qquad
r_{\rm new}=\frac{CT}{2},
\]
so the extra lower band has mass \(Dp/2\). Productivity requires \(r_{\rm old}\ge b_0\), while \(m\ge a_0\). The final upper record is the same \(\alpha T\).

All previously captured lower ranks remain captured, and old new-lower ranks are caught no later. Upper ranks above \(m\) have the same return-line capture time. The possible delay on the old right band is at most its full-band value
\[
\frac{BTm}{D}
+\frac{m^2}{2}\left(\frac1D-\frac1P\right)
\le\frac{BTPp}{2D}.
\tag{10}
\]
Removing already captured upper ranks from this integral only reduces the worst loss.

The merged route catches an extra lower rank \(-r\) at time \(r/C\). If it had survived to the old exit at time \(T\), no continuation could catch it before the direct unit-left ray, whose first-hit time is
\[
\frac{BT+r}{C}.
\tag{11}
\]
Hence each extra rank gains at least \(BT/C\). Combining (10) and (11) gives
\[
\boxed{\quad
\Delta{\rm cost}\le
\frac{BTp}{2}\left(\frac PD-\frac DC\right)<0.
\quad}
\tag{12}
\]
This comparison is valid against any fixed future continuation, not only an optimized one.

**Local persistence gate.** Formula (11) must stay inside the negative affine region. A sufficient time condition is that the local field extends through
\[
t_{\rm entry}+\left(\frac BC+\frac12\right)T.
\tag{13}
\]
All relevant rays remain in the forward light cone of the interface source. This condition holds for sufficiently small pairs at a nondegenerate initial interface, but is not silently assumed for an arbitrary large excursion.

The proof above assumes two actual tents. A separate strengthened normalization for arbitrary productive left-side excursions was derived by the upper worker and independently audited: with \(L_{\max}=CT/2\), its extra-lower first-hit credit dominates every possible upper-flow advantage. That result is needed before (12) can be applied to general same-side oscillations.

## 5. What remains for a finite prefix theorem

There is a credible local reduction, but its final theorem is being audited separately:

1. normalize positive-side excursions pointwise;
2. normalize arbitrary productive negative-side excursions using the first-hit credit and (13);
3. replace nonproductive pieces by interface waits and absorb waits where legal;
4. for \(B\ge b\), delete every overtaken right-left pair;
5. use (7) on the remaining hinge-free finite chain, with fixed final records and time.

At a vertex argument, every tight constraint must be identified: duplicate records, zero-amplitude turns, flow equality, and the possible terminal zero-amplitude interface endpoint. Conditional concavity alone is insufficient if additional corridor faces are left unclassified. A uniform finite-sequence bound is also required before passing to an initial accumulation limit.

The exact counterexample in Section 3 and the persistence gate in Section 4 must remain visible in any later proof; neither can be bypassed by assuming the old ordinary-prefix family.

## 6. Exact replay

`packages/interval_turn_sheet/verify_initial_density_interface.cjs` is standalone. Use `Function(source)().verify()` in V8, or execute the CommonJS file directly.

The saved report includes:

- 363 direct local capture-moment identities, 71 with active crossover hinges;
- 486 fixed-time parity sum-of-squares identities;
- the 49-leg positive-curvature witness, checked by local moments and by the complete ordered-fan endpoint continuation;
- 108 complete ordered-fan capture comparisons for the deletion, including nonzero old record bands;
- 12 exact band-mass/deletion-bound identities.

The full fan scorer integrates strict/closed signed running records on affine time intervals. It does not evaluate route payoffs using (3), (4), or (12). All checks were run in exact BigInt rational V8. No native rerun is claimed after the environment outage.
