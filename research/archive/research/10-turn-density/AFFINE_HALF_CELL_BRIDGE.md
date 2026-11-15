# The final half-cell bridge in an initial fan neighborhood

## Status and dependencies

This note closes the final partial-excursion case of the **local initial** normal form. It does not give a global turn count for a fan law.

The return-block input is `INITIAL_INTERFACE_RETURN_BLOCK.md`. The original zero-width statement was preserved as blob `cf37c35b720e3a52e99d04a71cf4033cc9e2e774`; the explicit arbitrary-old-record extension is blob `d10fa2df15cb767f11fb5cb4b92cf990e3a046ce`. The other inputs are `AFFINE_RECORD_PREFIX.md` and `AFFINE_INTERFACE_EXCURSION.md`.

Suppose the initial forward cone, through the required persistence horizon, has only
\[
F(t,x)=q_0+\alpha t+\beta_\pm(x-a),\qquad x\gtrless a.
\]
The source is \((0,a)\), away from a physical endpoint, and \(F\) is continuous. The game center is allowed; this argument uses the full signed CDF. A change of local spatial and rank signs reduces to \(\alpha\ge0\).

For \(\alpha>0\), write \(B=\beta_-\), \(C=B-\alpha>0\), and
\[
\gamma=B/C+1/2.
\]
For the nondegenerate proof take \(\beta_\pm>\alpha\). The zero inverse-speed cases are treated separately in the return-block note. Assume the entire initial cone through time \(\gamma T\) remains in these same two half cells. Every replacement below stays in the initial cone through time \(T\), and every future-rank credit uses only the stipulated persistence through \(\gamma T\).

## 1. Local theorem

For any legal initial Monster path on \([0,T]\), with arbitrary speeds and arbitrary turn accumulation, and any fixed continuation after its exit point at time \(T\), there is a path with no larger capture payoff, the same exit point and time, and the same continuation, comprising:

- either at most five complete interface tents, or an all-wait interface block;
- at most three further productive unit-speed legs in its final left half cell;
- one possible constant-rank hold; and
- one nonproductive affine connector to the prescribed exit.

If the final partial excursion lies on the right, a maximal two-leg bridge replaces the last three items.

Thus at most **15 affine pieces** suffice in this fixed initial neighborhood. This is a local zero-width-source statement. It does not assert that compactness supplies a uniform global number of such neighborhoods, nor that the same constant is valid across an arbitrary CDF arrangement.


### Explicit extension to an old captured interval

The same local 15-piece bound holds with an arbitrary previously captured interval containing the source rank, using the **explicit old-record extension** of the return theorem. This is an added dependency, not an inference from its earlier zero-width version.

For a right-first productive chain with old relative band \([-b_0,a_0]\), the discarded old-rank moment is
\[
\frac{a_0^2}{2c_+}+\frac{b_0^2}{2c_-}
+\frac{2\beta_-b_0}{c_-c_+}\,r_1.
\]
Only a constant and a linear term change. After a fixed initial left tent of duration \(t_0\), the old upper offset is
\[
a_0'=\max(a_0,\alpha t_0)-\alpha t_0,
\]
which need not be zero; the same correction applies. The separately verified return theorem retains this offset exactly.

For the partial bridge, right pointwise dominance only uses that the current interface rank lies in the captured interval. Left earliest travel applies to each new target independently of the old interval. The single-cell suffix objective again changes only by constant and linear old-band terms, leaving its strict Hessian unchanged. The last-active-face proof therefore goes through verbatim, and the prefix through that face uses the now extended return theorem.

The common-cone and future-persistence hypotheses remain unchanged. This extension supplies a local result at a later stationary-interface visit; it still does not supply a global atlas count.

## 2. A right partial excursion is immediate

After an interface visit at time \(s_0\), a path confined to \(x\ge a\) has
\[
F(t,x)\ge F(s_0,a).
\]
That rank is already in its captured interval. Hence this partial excursion can create only upper records.

For a prescribed endpoint \(x_e\ge a\) at time \(T\), the pointwise maximal legal bridge is
\[
m_*(s)=a+\min\{s-s_0,\ x_e-a+T-s\}.
\]
It stays on the right and dominates every other bridge pointwise. It captures every new upper rank no later and loses no new lower rank. It has at most one turn.

## 3. Constrained earliest travel on the left

Translate the most recent interface point to \((0,0)\). In the left half,
\[
y=F-q_0=\alpha t+B x,\qquad x\le0.
\]

From a state \((t,x)\) with rank \(q_0=\alpha t+Bx\):

- For a lower target \(q<q_0\), travel unit left. Its earliest capture is
  \[
  t+\frac{q_0-q}{B-\alpha}.
  \]
- For an upper target \(q>q_0\), travel unit right. The unrestricted affine hit time is
  \[
  t_u=t+\frac{q-q_0}{B+\alpha},
  \]
  and the interface is reached at \(t_b=t-x\).
  If \(t_u\le t_b\), capture the target there. Otherwise reach the interface first and wait there until \(q/\alpha\).

For the upper case, the greatest feasible rank before the target is
\[
\min\{q,\ \alpha s,\ q_0+(B+\alpha)(s-t)\}.
\]
It pointwise dominates the rank of any other left-confined path to that target. The lower unit ray is the analogous pointwise minimum.

Build the sequential earliest itinerary directly. Inductively, reaching a fixed rank earlier cannot make its next target later: one could follow that rank's quantile to its former time before using the old route. The quantile moves at speed \(-\alpha/B\), remains on the left after it is first available, and is legal.

Consequently any finite sequence of productive record targets can be reached by unit legs and interface waits, with every requested capture no later. At the last target, any remaining slack can be taken as a constant-rank hold. The held rank's physical position moves left, so it remains in the half cell.

The case \(\alpha=0\) is simpler: a left partial excursion creates only lower records and is dominated by its pointwise minimal Lipschitz bridge.

At the center of a symmetric atom-free fan law, \(F(t,0)=1/2\) forces \(\alpha=0\), and reflection gives \(\beta_+=\beta_-\). Its local cone is therefore a single static affine density, or a flat cell when that density is zero. The same zero-flux argument applies. A genuine center atom is outside the continuous-CDF hypothesis and is not covered by this observation.

## 4. The last active face

After the last generated interface contact or wait, the capture portion of the accelerated itinerary has only unit rank travel. Fix the final two record levels, the prescribed final record time as an upper budget, and the original nonproductive exit connector.

In a single affine cell the exact capture moment is the quadratic in `AFFINE_RECORD_PREFIX.md`. Its Hessian is strictly negative definite. Its rank-order constraints and total-time budget are linear.

Left confinement adds only the linear face inequalities
\[
r_i\le\alpha\tau_i
\]
at the record vertices. Because physical segments are affine and the half-plane is convex, checking these endpoints is sufficient for each unit leg. The final constant-rank hold stays on the left.

Minimize the quadratic on this compact polytope. At a minimizing vertex, take the **last** active confinement face. It is a physical interface contact. Freeze its point, time, and the preceding variables. All earlier face constraints are causal and do not constrain variations of later records.

After this last contact, all confinement inequalities are strict. Deleting repeated, nonproductive record levels leaves only the two rank-order chains and one time budget. More than three productive levels would leave a nonzero feasible local direction on which the strict affine Hessian is negative, contradicting minimality. Equivalently, the remaining chain polytope can have at most one partial level in addition to its two final levels.

Everything through the last contact is now an interface-return block and is replaced by the at-most-five-tent theorem. For the original statement that theorem is applied at the zero-width source. For the explicit extension above, use its verified old-record version. Any extra records captured by the replacement only help the unchanged suffix.

If the final connector itself has the last interface contact, there is no productive suffix after it. Otherwise the connector can be the straight segment from its original final-record point to the prescribed exit: the physical speed is legal, and its affine rank remains between already captured records, so it is nonproductive.

## 5. Arbitrary paths and the limiting step

For an arbitrary legal initial path, use uniform piecewise linear interpolation retaining the first attainment times of both final CDF extrema and the exit time. The interpolants lose no rank captured by the original prefix. Extra captures between interpolation nodes can only help the fixed continuation.

The running CDF extrema converge uniformly because the local CDF is Lipschitz. Thus the first-capture moments on the original captured rank band converge. Apply the finite-itinerary reductions to each interpolant.

The family with the stated finite number of affine pieces is compact after zero-duration pieces are allowed. Pass to a convergent subsequence. First capture is lower semicontinuous under uniform Monster convergence with the Princess path fixed, so the limiting replacement has no greater expected capture cost. Nonnegative-time Fatou applies to the unchanged continuation. A common finite continuation horizon is sufficient but is not needed for this last inequality.

This passage removes genuine initial turn accumulation; it does not assume that all excursions have a positive minimum duration.

## 6. Why the global count remains separate

Characteristic fan edges have slopes \(+1\) or \(-1\), and a legal Monster can cross each such edge at most once on its affine time segment. Stationary interfaces can be revisited.

The local persistence radius can tend to zero as a source approaches an intersection of a moving edge and a stationary interface. The 15-piece local statement therefore cannot simply be multiplied by a claimed compact-cover size. An explicit global cell-boundary count, or a different all-path certificate for a fixed fan law, remains a separate obligation.

## 7. Exact implementation checks

Files:

- `packages/interval_turn_sheet/affine_half_cell_bridge.cjs`
- `packages/interval_turn_sheet/verify_affine_half_cell_bridge.cjs`
- `packages/interval_turn_sheet/affine_half_cell_bridge_checks.json`

The exact rational replay passes:

- 258 constrained earliest-target cases;
- 364 physical legality checks;
- 114 comparisons with prescribed old arrival times;
- 220 chronological first-contact comparisons; and
- 175 pointwise maximal-right-bridge comparisons.

The code checks the explicit travel rules and bridge inequalities. The finite-piece count additionally uses the symbolic last-active-face argument and the separately verified return-block theorem.
