# A finite initial-interface return block

## 1. The local theorem and its scope

Let an ordered signed law have a continuous interior CDF which, in the forward cone of an interior source \((0,a)\), is
\[
F(t,a+x)=q_0+\alpha t+
\begin{cases}
B x,&x\le0,\\
b x,&x\ge0,
\end{cases}
\qquad B,b\ge|\alpha|.
\tag{1}
\]
Assume the monster initially has zero captured-record width at \(q_0\). This is the ordinary nonatomic initial-start state, and also the only possible source of an initial accumulation of alternating productive record turns.

Reverse the local spatial and rank orientations if necessary, so \(\alpha\ge0\). In the nondegenerate case \(B>\alpha\), put
\[
C=B-\alpha,\quad D=B+\alpha,\quad P=b+\alpha,\quad
\gamma=\frac BC+\frac12.
\tag{2}
\]
Fix a return time \(T>0\). Require that (1) hold throughout the unchanged forward cone up to time \(\gamma T\), including the unit rays used for earliest-capture comparisons. The cone is assumed to stay inside the physical interval; when this is a pre-first-center application, choose it inside the same physical half as well.

**Interface-return block theorem.** Every legal monster prefix from \((0,a)\) back to \((T,a)\), followed by any fixed continuation, has a replacement of no greater expected capture cost which is either:

- one pure interface wait; or
- at most **five real maximal interface tents**, with the same return time and location.

There are no additional waits in the second alternative. A tent consists of two unit legs on one side of the interface. Degenerate zero-duration tents are omitted.

The theorem is local. It does not state a uniform global prefix count over unrelated fan laws or over vanishing source-cone margins. A prefix ending away from the interface needs a separate affine half-cell bridge. The proof below gives a finite-sequence bound uniform in the number of original returns, which is the ingredient needed for an initial-Zeno replacement.

The initial two-half-cell form is automatic at a sufficiently small forward neighborhood of a source in a fixed-width bang-bang translation fan: moving edges through the source lie on the light-cone boundary, and only stationary edges split its interior. Both clipped and reflected-outward fans have this marginal geometry. The law is the ordered realization, not the raw crossing-path mixture.

## 2. The normalization and its persistence gate

On the right side, \(F(t,a+x)\ge q_0+\alpha t\). A right excursion creates no new lower record. Its maximal tent is pointwise farther right, so it catches every new upper rank no later. An unproductive right excursion can be replaced by an interface wait.

For a left excursion, use the independently proved arbitrary-left normalization in `AFFINE_INTERFACE_EXCURSION.md`. For an excursion of duration \(d\), let \(L\) be its newly reached lower magnitude relative to the interface rank at entry, and let
\[
L_{\max}=Cd/2.
\]
If it creates a new lower record, replacing the whole excursion by the maximal left tent can delay some upper-flow captures, but the earlier extra lower band pays for that delay against every future continuation. Its quantitative surplus is at least
\[
\frac{BCd(L_{\max}-L)}{D^2}\ge0.
\tag{3}
\]
An old lower band cancels, and deleting an already captured upper band only reduces the worst upper loss. If no new lower record is caught, waiting at the interface catches every new upper rank at least as early.

The earliest possible future hit of an extra lower rank \(r\), after returning to the interface at elapsed time \(d\), is
\[
\frac{Bd+r}{C}.
\tag{4}
\]
The latest relevant value is at most \(\gamma d\). If a subexcursion starts at \(\tau\) and \(\tau+d\le T\), then
\[
\tau+\gamma d\le\gamma T.
\]
Consequently the single cone hypothesis in Section 1 covers every normalization, merge, and boundary push in the proof. No exterior field is frozen or silently extrapolated.

These normalizations also absorb interface waits. On the right, the larger tent dominates a wait-plus-right-excursion pointwise. On the left, the whole wait-plus-productive-excursion path stays in the left half, so the same normalization applies. Consecutive same-side pieces combine the same way. Therefore every finite prefix reduces to alternating real tents, or to a pure wait if none is productive.

## 3. Deleting the positive crossover when \(B\ge b\)

The exact first-capture correction at a positive-going interface crossing time \(S\), with previous upper record \(r\), is
\[
\frac12\left(\frac1P-\frac1D\right)(\alpha S-r)_+^2.
\tag{5}
\]
Its coefficient is positive precisely in the difficult contrast \(B>b\). The full hinged capture moment is not conditionally concave in general: the exact counterexample in `INITIAL_DENSITY_INTERFACE_AUDIT.md` has normalized curvature \(1504/441>0\).

Instead use the physical deletion. Take a productive right tent \(p\), followed by a productive left tent \(q\), and write \(d=p+q\). If
\[
\alpha d\ge Pp/2,
\tag{6}
\]
the interface flow at the return has overtaken the right peak. Merging both into one left tent preserves the final upper record and adds lower mass \(Dp/2\). The upper loss is at most \(BdPp/(2D)\), while (4) credits the extra lower band by \(Bd/C\) per rank. Hence
\[
\Delta{\rm cost}\le
\frac{Bdp}{2}\left(\frac PD-\frac DC\right)<0.
\tag{7}
\]
The estimate includes arbitrary old records at the beginning of the pair.

Equality in (6) is already deletable. Thus the weak boundary of the no-crossover region is not an unclassified exceptional face.

If the chain begins with a left tent, normalize and fix that first tent. Its return has upper record exactly the interface rank, since the source record width was zero. Reset time and rank origins there. The old lower-band contribution to every subsequent moment is only linear in the new record variables. The fixed initial tent accounts for at most one of the final five.

After repeated deletions and same-side normalizations, every remaining right-left pair satisfies the strict reverse of (6). Thus all the subsequent crossover corrections (5) vanish. A final left return has the same no-crossover condition; if it fails, its preceding right-left pair is deletable as well. The sole unpaired initial left tent is the already-fixed exception.

## 4. The exact quadratic and its time kernel

For a tent whose outgoing half begins at interface time \(S\), its physical peak amplitude and its signed record magnitude satisfy
\[
x_+=\frac{r^+-\alpha S}{P},\qquad
x_-=\frac{r^-+\alpha S}{C}.
\tag{8}
\]
Set
\[
\kappa_+=\frac{b-\alpha}{P},\qquad
\kappa_-=\frac DC,\qquad K=\kappa_+\kappa_-.
\]
The interface-return time after the peak is exactly
\[
T_+=\kappa_+S+\frac{2r^+}{P},\qquad
T_-=\kappa_-S+\frac{2r^-}{C}.
\tag{9}
\]
In particular, fixing the final peak rank and exit time fixes its incoming interface time for either terminal sign. The same fixed-time hyperplane is therefore used for both signs; an exit connector is not discarded from the clock.

When the opposite-parity records are fixed, successive interface times have a linear recurrence with multiplier \(K\). For the positive parity the new-record coefficient is \(2\kappa_-/P\); for the negative parity it is \(2\kappa_+/C\).

For intermediate variations \(v_1,\ldots,v_m\) in one parity, the quadratic capture-moment variation is a positive factor times
\[
Q(v)=-\sum_{j=1}^m v_j^2
+(1-K)\sum_{h<j}K^{j-1-h}v_hv_j.
\tag{10}
\]
The fixed-time condition is, up to a positive terminal factor,
\[
\sum_{j=1}^mK^{m-j}v_j=0.
\]
Writing \(z_0=z_m=0\) and \(z_j=Kz_{j-1}+v_j\) gives the exact identity
\[
\boxed{\quad
Q(v)=-\frac{K+1}{2}\sum_{j=1}^m(z_j-z_{j-1})^2<0
\quad(v\ne0).
\quad}
\tag{11}
\]
The positive factors are
\[
\frac{2b\kappa_-}{P^2},\qquad
\frac{2B\kappa_+}{C^2},
\]
respectively. Fixed nonzero old record bands change constants and linear terms, not (11).

If \(B\ge b\), Section 3 has removed all remaining positive crossover terms. If \(B<b\), the coefficient in (5) is negative: each crossover term is a negative multiple of the square of the positive part of an affine function. It preserves concavity on every fixed-time parity direction, even when a direction crosses a hinge. Thus (11) supplies strict conditional concavity in either contrast, by different arguments.

## 5. Every limiting face is accounted for

Fix a finite alternating tent sequence, its final two captured records, and its total interface-return time. Fix a possible initial left tent as described above. Optimize only the remaining intermediate record values.

The feasible set is compact. Actual tent amplitudes are nonnegative and their durations sum to the fixed time, so all paths stay in
\[
|x-a|\le\min(t,T-t)
\]
inside the unchanged source cone. The recurrence (8)--(9) makes the constraints affine in record variables. They are:

1. same-parity record order, with fixed old and final bounds;
2. nonnegative physical amplitudes;
3. the one total-time equality;
4. in the \(B\ge b\) branch, the no-crossover inequalities.

There is no hidden distant cell face: the entire cone was assumed unchanged.

The final records and return time/location are fixed during this minimization. The cost of the fixed subsequent continuation is therefore constant, so only the prefix capture moment is being minimized.

Every active boundary has a concrete reduction:

- **Duplicate record.** A right tent with no new upper record is unproductive. A left tent with no new lower record is replaced by an interface wait. Absorb the wait into an adjacent same-side piece as in Section 2.
- **Zero right amplitude.** The two adjoining left pieces form one left-confined path and can be normalized together. Any interface flow capture at the zero-amplitude point is retained by that normalization.
- **Zero left amplitude.** It is nonproductive and disappears.
- **Tight no-crossover face.** It is exactly equality in (6) for the preceding right-left pair, so (7) deletes it.
- **Terminal flow capture.** If a final left return adds a new upper band in the \(B<b\) branch, represent the interface endpoint as one fixed zero-amplitude upper extremum of rank \(\alpha T\). It accounts for the final return capture through (5), but is not a real tent. If the final return is nonproductive, the last two genuine peak records remain the fixed pair. In the \(B\ge b\) branch a terminal crossover is removed by (7), except for the fixed unpaired initial left tent.

The first/last fixed bounds are not additional free intermediate levels. An initial no-crossover equality at time zero is also fixed and creates no free face.

Suppose at a minimum two intermediate record levels of the same parity were free. Their nonzero fixed-time direction preserves the opposite parity and final records. If all relevant faces are strict, a sufficiently small displacement in both signs is feasible, and (11) makes one sign strictly improve the cost. Therefore the minimum must meet one of the reducing faces just listed. Apply that reduction and repeat; the number of real tents decreases.

Once no reduction remains, there is at most one intermediate record level in each parity. With the two final records, this gives at most four real tents after the fixed initial left tent: at most **five real tents in total**. A retained terminal zero-amplitude interface endpoint does not increase this count.

The argument is a finite-sequence reduction with a uniform bound, not the weaker assertion that one particular infinite optimizer is absent.

## 6. Degenerate slopes

If \(B=\alpha>0\), the whole forward cone has \(F\ge q_0\), so no new lower record can occur. The maximal right tent pointwise dominates every return prefix. If \(b=\alpha>0<B\), every right peak equals the interface flow at its own return; any following left tent therefore satisfies (6), so deletions leave at most an initial left and a final right tent.

For \(\alpha=0\), the crossover correction vanishes. Positive densities give \(K=1\) in (11). If one side has zero density, only the other side can create new records, and its maximal tent dominates. The all-zero case is a pure wait.

Thus degeneracies do not require dividing by a zero rank speed or taking an unsupported limit of (11).


### Explicit extension to an arbitrary old record band

The same five-tent conclusion holds if the interface source has any fixed already captured band \([q_0-b_0,q_0+a_0]\), with \(a_0,b_0\ge0\). This is an extension of the zero-width theorem, not an assumption imported into its proof.

If both signs create new records and the productive chain begins to the right, let its first upper magnitude be \(r_1\). The first left-half crossing time is \(S_-=2r_1/P\). Relative to the zero-band moment, the moments of ranks that were already caught are exactly
\[
\frac{a_0^2}{2P}+\frac{b_0^2}{2C}
+\frac{B b_0S_-}{C}
=
\frac{a_0^2}{2P}+\frac{b_0^2}{2C}
+\frac{2B b_0r_1}{CP}.
\tag{12}
\]
The first upper band is met on the first outward right leg; the old lower band is first met on the first outward left leg. Later crossover hinges do not alter either first moment. Subtracting (12) changes only constants and a linear first-record term, so both conditional parity identities and the negative-hinge concavity remain unchanged.

If an initial left tent of duration \(t_0\) is fixed, its normalized records are
\[
\max(b_0,Ct_0/2),\qquad \max(a_0,\alpha t_0).
\]
After resetting the rank origin to the current interface value \(\alpha t_0\), the old relative bounds become
\[
b_0'=\max(b_0,Ct_0/2)+\alpha t_0,\qquad
a_0'=\max(a_0,\alpha t_0)-\alpha t_0.
\tag{13}
\]
They are fixed nonnegative constants. In particular \(a_0'\) need not vanish; (12) covers it explicitly.

Initial record-bound equalities are nonproductive tents, so the face classification is unchanged. Every later free no-crossover gate is associated with a genuine preceding productive right peak. If only one sign ever creates a new record, the corresponding pointwise or arbitrary-left normalization gives the required simpler form directly. The degenerate-speed arguments also remain one-sided.

The extension therefore changes neither the common cone/persistence hypothesis nor the five-real-tent count. Its finite-sequence and compactness arguments are the same. For the limiting argument, retain the final extrema after including the fixed old band; no originally captured rank is lost.


## 7. Arbitrary and accumulating interface returns

Let a legal prefix return to the interface at the fixed time \(T\), possibly with infinitely many turns or interface contacts. Approximate it uniformly by finite piecewise-linear legal paths, retaining as interpolation nodes times at which its final lower and upper CDF extrema are attained. The local CDF is continuous and Lipschitz, so its running records and finite-prefix capture moments converge. Retaining the extremum nodes ensures that the approximants lose no already captured rank; any extra capture only improves the identical subsequent continuation.

Each finite approximant can be normalized and compressed to the uniform bound of five tents. Their duration vectors lie in a compact simplex, with finitely many orientation patterns. Pass to a subsequence. Its limiting prefix is again a legal at-most-five-tent return block, allowing zero durations, and it has the same return time/location.

First-capture time is lower semicontinuous under this uniform prefix convergence with the identical future path appended. Fatou's lemma gives no greater expected total cost in the limit. This use of lower semicontinuity is preceded by the record-preserving finite approximation; it does not assume an unproved global payoff continuity on an infinite horizon.

In particular, if interface returns accumulate at an initial zero-width source, choose any sufficiently small positive return time satisfying the cone/persistence gate, compress that entire block, and leave the rest of the path unchanged. Positive captured width then separates later alternating productive record episodes on a bounded time interval. No claim of a global uniform count follows from this local statement alone.

## 8. Remaining bridge and global-cover obligations

A prefix that ends away from the interface is not covered by this return-block theorem. The separate affine half-cell bridge uses the last interface contact and a one-cell rank-time optimization. Its endpoint and confinement faces must be checked explicitly.

Likewise, turning the local theorem into a global all-monster oracle requires a finite cover of the fixed fan's moving and stationary density regions, the finite center-return theorem, and the static-tail reduction. The finite local source theorem must not be substituted for those remaining global obligations.

## 9. Exact replay and dependencies

The standalone source is `packages/interval_turn_sheet/verify_interface_return_block.cjs`; `Function(source)().verify()` and its CommonJS CLI produce the saved report.

Its exact checks include:

- 1,944 strict parity sum-of-squares identities, for both terminal signs and both varying parities;
- 648 terminal clock identities;
- 180 arbitrary-left credit-margin factorizations;
- 81 complete ordered-fan capture comparisons for nontrivial left-confined excursions and nonzero old records;
- 30 active terminal flow-capture endpoints and 69 inactive exit connectors;
- 1,134 independent old-band first-hit corrections, including 270 cases with later crossover hinges, and 252 fixed-initial-left reset identities.

The all-finite-sequence face proof in Sections 3--5 supplies the count; it is not inferred from these finite fixtures.

Dependencies:

- `INITIAL_DENSITY_INTERFACE_AUDIT.md`: exact crossover, failed-parity-concavity witness, and right-left physical deletion; blob `b2d70f275029f312ca8de45790ab02920bea84e6`.
- `AFFINE_INTERFACE_EXCURSION.md`: arbitrary-left normalization; independently audited blob `2ad880d9ab22b8b96217f29410c02c82bfbcb628`.
- The frozen affine-corridor proof is used only in the separate partial-prefix bridge, not to hide a corridor restriction in the return-block proof.

All report checks were executed in exact BigInt rational V8 after the native environment became unavailable. No native rerun is claimed.
