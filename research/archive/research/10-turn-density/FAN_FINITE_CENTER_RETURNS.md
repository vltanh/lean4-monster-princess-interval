# Finite center returns for ordered translation fans

## 1. Scope and conclusion

Take finitely many continuous base paths \(p_i:[0,\infty)\to[-1,1]\), with finitely many affine pieces of slopes in \(\{-1,0,1\}\), constant after a common time \(h\). Fix nondegenerate translation intervals \([\ell_i,r_i]\), positive widths \(r_i-\ell_i\), and nonnegative weights \(w_i\) summing to one. Translate uniformly on each interval, clip to \([-1,1]\), and apply fair reflection.

**The law in this note is the ordered common-quantile realization of the resulting symmetric marginal CDF.** It is not the raw mixture of translated base paths. Raw paths can cross the center at different times even though every fixed-time marginal has no center atom; the ordered positive quantiles used here never visit the center. Pathwise costs of the raw mixture are therefore not substituted for ordered costs.

There is an explicit finite time partition
\[
0=t_0<t_1<\cdots<t_J=h
\]
such that every center diamond contained in one partition cell has stationary radial density. A balanced center continuation needs at most \(2J-1\) productive renewal returns completed by \(h\). A conservative physical realization allows one additional balancing action; it is an outward sweep if the balanced tail is empty, and need not itself return to the center.

The remaining static tail has a separate finite breakpoint reduction. For a fixed fan law, its finite breakpoint bound and the partition above give a finite center-continuation optimization, with all turn coordinates remaining continuous. This does **not** bound arbitrary same-side reversals before the first center visit. No game value, equilibrium, or successful global lower candidate is asserted.

The result includes outward fans \([0,\delta_i]\), asymmetric intervals, and symmetric intervals. It does not require endpoint absorption before \(h\).

## 2. Ordered field, traces, and inverse convention

For \(0\le x<1\), the radial CDF is
\[
R_{\rm rad}(t,x)=
\sum_i\frac{w_i}{r_i-\ell_i}
\big|[p_i(t)+\ell_i,p_i(t)+r_i]\cap[-x,x]\big|.
\tag{1}
\]
Clipping makes no change to (1) in the open spatial interval. It can create endpoint atoms; these retain their closed first-contact convention. All interior marginals are continuous and \(R_{\rm rad}(t,0)=0\).

Use light coordinates \(U=t+x,\ V=t-x\), and write \(R(U,V)=R_{\rm rad}((U+V)/2,(U-V)/2)\). The marginal transport inequalities imply that the ordered radial quantiles are nonnegative 1-Lipschitz paths. Each fixed positive quantile is strictly positive at every time, because the radial center CDF is identically zero. Thus a center wait captures no positive quantile mass.

Let \(\beta_t(q)\) be the first capture time of radial rank \(q\) by the unit outward ray from the center at time \(t\), with the endpoint included. Then
\[
t\le\beta_t(q)\le t+1,\qquad
q\longmapsto\beta_t(q)\ \hbox{is nondecreasing}.
\tag{2}
\]
Set \(T_t(q)=\int_0^q\beta_t(r)\,dr\). For a balanced state with ranks through \(n\) already caught on both signs, let \(V(t,n)\) be the remaining absolute-time expected capture contribution, and
\[
W(t,n)=V(t,n)+\tfrac12T_t(n).
\tag{3}
\]

A productive center tent from \(t\) to \(e\), with peak inside the interval, has \(\rho=R(e,t)>n\). Its exact transformed renewal action is
\[
\mathcal A_{t,e}W(n)
=W(e,\rho)+\tfrac12[T_t(\rho)-T_e(n)].
\tag{4}
\]
This is the center imbalance factorization: orient the next productive action toward the lagging sign so that the unmatched band is captured at its earliest outward times. The final all-captured balanced state can instead be completed by one outward balancing sweep. For any fixed future continuation, as well as the optimized continuation,
\[
W(e,N)-W(e,n)\le-\tfrac12\int_n^N\beta_e(r)\,dr
\quad(N\ge n).
\tag{5}
\]
Indeed every omitted reflected pair has mean capture time at least \(\beta_e(r)\). Formula (5), not any guessed future geometry, is the only continuation property used below.

Any same-side excursion between successive center visits is dominated by the maximal tent with the same two center times. The tent is pointwise farther from the center on that sign, so a path hit by the original excursion is met no later by continuity. The reflected paths have no new center capture in the interior of the excursion. An empty sequence of waits and excursions can similarly be absorbed into the next productive tent. A capped tent reaching a spatial endpoint is retained as an endpoint action; sufficiently long delays are replaced by endpoint completion.

## 3. Stationary-cone merge without future stationarity

Suppose the entire center diamond from \(t\) to \(e\) satisfies
\[
R(U,V)=k(U-V),\qquad k>0.
\tag{6}
\]
Consider consecutive productive returns \(t\to u\to e\), and write
\[
p=u-t,\quad q=e-u,\quad
N_1=kp,\quad N_2=kq,\quad N=k(p+q).
\]
Their productivity gives
\[
0\le n\le N_1\le N_2,\qquad N\le1;
\tag{7}
\]
strict productivity uses strict inequalities where appropriate. In particular \(q\ge p>0\).

Replace both returns by the single tent \(t\to e\). By (4) and (5), twice the merged-minus-unmerged cost is at most
\[
\begin{aligned}
&\int_n^{kp}(\beta_e-\beta_u)\,dr\\
&\quad+\int_{kp}^{kq}(\beta_t-\beta_u)\,dr
+\int_{kq}^{k(p+q)}(\beta_t-\beta_e)\,dr.
\end{aligned}
\tag{8}
\]
All needed \(\beta_t,\beta_u\) captures occur inside the stationary diamond, so
\[
\beta_t(r)=t+\frac r{2k},\qquad
\beta_u(r)=t+p+\frac r{2k}.
\tag{9}
\]
No formula is imposed on \(\beta_e\).

The positive \(\beta_e\) band in (8) has length \(kp-n\). Pair it, in increasing rank order, with the first \(kp-n\) ranks of the negative band \([kq,k(p+q)]\). Monotonicity in (2) makes this paired contribution nonpositive. The remaining negative band has length \(n\), so its contribution is at most \(-ne\). Substituting (9) into the remaining terms gives
\[
\boxed{\quad
2\Delta_{\rm merge}
\le-\frac{kpq}{2}-nq+\frac{n^2}{4k}<0.
\quad}
\tag{10}
\]
The strict sign follows from \(n\le kp\) and \(q\ge p>0\). The case \(n=0\) still has the strict term \(-kpq/2\).

This is a future-independent merge. It remains valid if the field changes immediately after \(e\), has later moving density, or has endpoint atoms. Applying it to a fixed future continuation first, then taking its infimum, avoids an attainment assumption.

After merging, some later actions may become empty because the balanced record increased. They can be removed or absorbed into the next productive tent. The imbalance factorization reuses that next action and does not require a new productive center return. If the balanced record is already one, the sole remaining unmatched band is caught by a terminal outward sweep. A conservative physical-action count may retain this as an extra action.

## 4. Constructing the finite stationary-diamond partition

For each base piece, consider both translated edges
\[
a_i(t)=p_i(t)+\ell_i,\qquad b_i(t)=p_i(t)+r_i.
\]
First partition \([0,h]\) at every base vertex and every zero crossing of either translated edge. On an open resulting interval \((L,R)\), each edge has constant slope in \(\{-1,0,1\}\) and no zero crossing.

For a moving edge of slope \(+1\) or \(-1\), its zero lies outside \((L,R)\). Hence
\[
|a_i(s)|,\ |b_i(s)|\ge
\min(s-L,R-s)
\tag{11}
\]
for each such nonzero edge separately. A center diamond with endpoints inside \([L,R]\) has radius at time \(s\) no greater than this minimum.

For stationary edges, take the smallest **nonzero** absolute edge value \(\eta\); ignore an edge identically zero but retain the other edge of that interval. Subdivide so that each final cell has length
\[
\Delta\le \min(1,2\eta),
\tag{12}
\]
omitting the \(2\eta\) restriction only if there is no nonzero stationary edge. Positive interval width guarantees that an interval with one zero edge still has another nonzero edge.

The length-one restriction keeps every within-cell diamond strictly away from the spatial endpoint except at irrelevant zero-radius time boundaries. It prevents endpoint clipping jumps from being confused with the interior linear density.

Inside any such diamond, each translated interval contributes one of:
\[
0,\qquad \frac{w_i x}{r_i-\ell_i},\qquad
\frac{2w_i x}{r_i-\ell_i}.
\tag{13}
\]
The middle case is an interval with one stationary edge at the center. Thus (6) holds with a constant \(k_j\ge0\) throughout the entire cell diamond.

**Critical-tip convention.** If a stationary symmetric fan has \(|p_i|=\delta_i\), the zero edge does not remove the restriction from its other edge at distance \(2\delta_i\): require \(\Delta\le4\delta_i\). For an outward fan based at zero with interval \([0,\delta_i]\), require \(\Delta\le2\delta_i\). Simply deleting all restrictions when one edge is zero would be incorrect.

Everything is rational when the base vertices, intervals, and weights are rational. Long collections of equal subcells can be represented by a compact arithmetic-progression block; materializing a very large finite bound is unnecessary.


### Reflected outward fans

The same partition argument applies to
\[
p_z(t)=1-|1-p(t)-z|,\qquad z\in[0,\delta],
\quad0\le p\le1,\quad0<\delta\le1,
\]
followed by fair reflection. For \(0\le x<1\), the contribution to the radial CDF is
\[
\frac w\delta\left(
|[p,p+\delta]\cap[0,x]|
+|[2-p-\delta,2-p]\cap[0,x]|
\right).
\tag{16}
\]
These are two positive interval-density components, not a probability mixture of two clipped rows. Their total mass in \([0,1]\) is one. All four moving edges retain slopes \(0,\pm1\), and the center-critical edges are \(p=0\) and \(2-p-\delta=0\). The folding map is 1-Lipschitz, so the full marginal has a legal ordered realization. Positive translation width makes its center and endpoint marginals nonatomic.

Equations (11)--(13) use only positive interval-density components and edge geometry, so they apply to (16) without change. The static tail is again piecewise constant in spatial density. The verifier includes the two-component representation explicitly and checks its normalization, endpoint traces, center diamonds, and independent static capture integrals.

**Fixed-law scope.** The integer \(J\) is finite for each fixed positive-width fan law. It need not be uniform along an unrelated sequence of base paths whose stationary nonzero edge margin tends to zero. In particular, a vanishing-width avoided-center germ is not assigned a uniform count merely because every individual member has a finite partition.


## 5. Finite number of returns, including critical times and accumulation

Start with a finite canonical balanced renewal chain. An excursion completed by \(h\) is either contained in a single closed partition cell or strictly crosses a partition boundary.

There are at most \(J-1\) boundary-crossing excursions: their time interiors are disjoint, and each contains at least one distinct partition boundary. After repeated use of (10), there is at most one productive excursion wholly contained in each cell. Two such excursions in one cell are consecutive after empty pieces have been removed, and could otherwise be merged. Cells with \(k_j=0\) contain no productive interior excursion.

Therefore
\[
\#\{\hbox{productive balanced returns completed by }h\}
\le J+(J-1)=2J-1.
\tag{14}
\]
A center excursion straddling \(h\) is handled by the static continuation from its actual state at time \(h\); it is not counted twice. Partition-boundary contacts are covered by the closed diamonds and continuity of the interior fan CDF. No uniform positive distance of the support from the center is assumed.

To pass from finite chains to arbitrary center histories, first use a fixed finite completion horizon \(H\). Sample ordered quantiles with discrepancy at most \(\varepsilon\). The strict and closed signed CDFs differ uniformly by at most \(\varepsilon\), so their running-record survival costs differ by at most \(2H\varepsilon\), uniformly over monster paths, including endpoint contacts.

For the finite sampled law, retain the finitely many first-capture points of any candidate monster route and connect them by unit/wait segments; no sampled first-capture time increases. Maximal-tent replacement gives a finite canonical center route. Evaluate this route against the original continuous field, then apply the merge (10) to that field. The two comparisons with the sampled law cost at most \(4H\varepsilon\) in total. Thus the infimum over arbitrary histories is approximated by routes with the uniform count (14), not by a sequence whose count tends to infinity.

With endpoint completion and the separate static bound, the remaining finite list of action times is compact. First-capture time is lower semicontinuous under uniform convergence of monster paths; Fatou's lemma then gives an attaining finite-action limit if desired. The quantile-discrepancy step is essential: lower semicontinuity alone would not justify replacing an arbitrary path by nearby finite paths.

This removes initial growing center-Zeno sequences as well as forward accumulation after a positive record. It does not assert that all center chains are finite before replacement.

## 6. Static attachment and remaining initial-prefix gap

After \(h\), the ordered fan law is static. Each original interval and its reflection give finitely many constant-density spatial pieces, with clipping atoms at the endpoints. The surviving signed law is the static law restricted to the two running-record tails, adding at most two spatial breakpoints.

The separately proved static-turn concavity reduction pushes each productive turn to a fixed surviving-density breakpoint or a colliding turn that can be deleted. If \(K\) counts all relevant breakpoints, this yields a completion of at most \(2(K+1)\) additional time. For \(N\) input intervals, \(4N+4\) bounds the density/support and surviving-tail breakpoints; retaining the current starting position as an extra candidate gives the conservative \(K=4N+5\). One may therefore use
\[
H=h+2(4N+6)
\tag{15}
\]
as a deliberately nonsharp common horizon.

Only the availability of a finite static horizon is needed in Section 5. The detailed static breakpoint proof and its tighter counts belong to the separate static-tail certificate.

The result concerns continuation after a center visit. For an arbitrary initial monster position, all same-side motion before its first center remains an additional optimization. Neither the absence of center atoms nor (14) supplies a finite count for that prefix.

## 7. Exact replay

The standalone source is `packages/interval_turn_sheet/verify_fan_center_partition.cjs`; its function-body API is `Function(source)().verify()`, and it also runs as a native CommonJS CLI.

The saved report contains:

- 140 exact merge polynomial identities;
- 700 exact future-inverse monotonicity pairings, including nonlinear and jump traces;
- 216 independent continuous ordered-CDF capture comparisons for two tents versus one, with 4,080 affine capture pieces and strict/closed endpoint traces;
- 682 exhaustive finite time-partition chain count checks;
- four symmetric/asymmetric/outward fan fixtures with 64 exact edge-margin checks and 1,008 cone-CDF identities;
- two reflected-outward partitions with 29 edge checks and 180 further cone identities, plus 36 normalization/endpoint checks and 12 independent static ordered capture integrals.

The physical scorer directly integrates signed running records along unit monster legs. It does not use (4), (8), or (10) to compute its route payoffs. Several fixtures change the base motion immediately after the merged return, so future stationarity is not silently built into the capture check.

The theorem's whole-diamond and all-count arguments are the proofs above; finite fixtures are regressions, not substitutes for those proofs. These checks were executed in the exact BigInt rational V8 runtime after the native environment became unavailable. No native Python or Node rerun is claimed for this packet.
