# A quantitative obstruction to replacing only the endpoint component

**Status: proved obstruction for a specified modification family.**
Keeping the current interior Monster law fixed and replacing its
endpoint atom by **any** law of canonical one-turn paths cannot
reach the frozen target \(U_*\). The result permits arbitrary
continuous replacement measures, arbitrary starting positions and
turn locations, and both possible first endpoints. It is not a
lower bound on \(W_1\).

## 1. General theorem

Let a reflection-symmetric Monster law have mass \(q\) on the immediate
endpoint-sweep pair. Suppose every other supported start satisfies
\[
 |m(0)|\le1-\delta,\qquad 0<\delta<1.
\tag{1}
\]
Assume each path visits both endpoints, and let its endpoint-time
baseline be
\[
 M=\frac12\mathbb E(\tau_-+\tau_+).
\tag{2}
\]
Keep the non-endpoint part of this law fixed. Replace any or all of
the endpoint mass by an arbitrary reflection-symmetric measure of
the same total mass \(q\), supported anywhere in the canonical
class \(\mathcal B_1\). Thus
\[
 \widetilde\nu=\nu_{\mathrm{bulk}}+\mu,\qquad
 \mu(\mathcal B_1)=q,
\tag{3}
\]
where \(\nu_{\mathrm{bulk}}\) is the unchanged old interior part.
Leaving some endpoint mass untouched is allowed. The new paths
may start and turn anywhere in the arena; their first center need
not occur by time two. The definition of \(\mathcal B_1\) requires
at most one interior unit-speed reversal before the first endpoint,
followed by a direct opposite sweep.

**Theorem.** Every such repaired law \(\widetilde\nu\) satisfies
\[
 \boxed{
 \sup_{p\ {\rm legal}}\mathbb E_{\widetilde\nu}T(m,p)
 \ \ge\
 M+\frac{q\delta(2-\delta)}{8-\delta}
 =
 M+\frac{q\delta}{4}
   -\frac{3q\delta^2}{4(8-\delta)}.}
\tag{4}
\]

Here \(M\) is the **old** law's baseline. The modified law's
baseline generally changes. Thus this theorem gives a quantitative
limit on an endpoint-only modification, not a claim that its new
clocks or endpoint times remain unchanged.

## 2. Two complete endpoint-layer kernels

Use the immediate-outward Princess
\[
 p_\varepsilon(t)=\min\{1,1-\varepsilon+t\},
 \qquad 0<\varepsilon<\delta,
\tag{5}
\]
and its reflection with equal probabilities. Against the endpoint
sweep pair \(E\), its expected capture time is
\[
 K_E(\varepsilon)=1+\varepsilon/4.
\tag{6}
\]
The actual Princess starting exactly at the endpoint is different:
at \(\varepsilon=0\) she is captured immediately by one of the
sweeps. All limits below are taken through strictly positive
\(\varepsilon\), not by substituting that boundary path.

Represent a new interior start by \(1-a\), where \(0<a\le1\),
using fair reflection. Center starts correspond to \(a=1\).
There are exactly two possibilities for its first endpoint.
The kernels below use \(0<\varepsilon<\delta<1\), so an initial
tie \(\varepsilon=a\) can occur only when \(a<1\).

### Opposite endpoint first

The path initially moves outward for duration \(h\), possibly zero,
then moves left to \(-1\), then right to \(1\), where
\[
 0\le h<a,\qquad d=a-2h\in(-a,a].
\tag{7}
\]
Its vertices are
\[
 (0,1-a),\quad(h,1-a+h),\quad(2-d,-1),\quad(4-d,1).
\tag{8}
\]
The negative Princess reaches her endpoint before time one and is
captured at \(2-d\). If \(\varepsilon<a\), the positive Princess
starts to the right of the Monster, remains ahead during its initial
outward leg, and is not caught until its positive endpoint at
\(4-d\). If \(\varepsilon>a\), the Monster meets her on its leftward
leg at time \((\varepsilon-d)/2\). Initial equality is captured
at time zero. Consequently the exact kernel is
\[
 K_A(a,d;\varepsilon)=
 \begin{cases}
 3-d,&\varepsilon<a,\\
 1-d/2,&\varepsilon=a,\\
 1+\varepsilon/4-3d/4,&\varepsilon>a.
 \end{cases}
\tag{9}
\]
This includes the direct inward route \(h=0,d=a\), a turn on either
side of the principal front, and all initial-contact ties.

### Same endpoint first

The path initially moves inward, possibly for zero time, then
outward to \(1\) at time \(z\), and then sweeps to \(-1\):
\[
 a\le z<4-a,
\]
\[
 (0,1-a),\quad
 ((z-a)/2,1-(a+z)/2),\quad
 (z,1),\quad(z+2,-1).
\tag{10}
\]
The negative Princess is captured at \(z+2\). Direct intersection
with the positive Princess gives
\[
 K_B(a,z;\varepsilon)=
 \begin{cases}
 1+z,&\varepsilon<a,\\
 1+z/2,&\varepsilon=a,\\
 1+z/2+(\varepsilon-a)/4,&a<\varepsilon\le z,\\
 1+3z/4+\varepsilon/4,&\varepsilon>z.
 \end{cases}
\tag{11}
\]
The turn equality \(\varepsilon=z\) belongs to the third branch;
replacing it by the fourth branch's limit would miss a tangency.
Every branch satisfies
\[
 K_B(a,z;\varepsilon)\ge1+\varepsilon/4.
\tag{12}
\]
Thus these same-side-first repairs never improve the
immediate-outward test over an endpoint sweep. This assertion
holds even for a deep initial inward excursion.

An actual endpoint start has first endpoint time zero, so its
canonical \(\mathcal B_1\) continuation is just \(E\). It is retained
separately, not obtained by assigning \(a=0\) to an interior
route whose first endpoint has been misidentified.

## 3. The two limiting tests

For \(\varepsilon<\delta\), every path in the unchanged interior
part starts strictly between the two Princess targets. During
their immediate outward motion a speed-one Monster cannot close
the initial gap. Each target reaches its endpoint first and is
therefore captured exactly at the corresponding Monster endpoint
time. The unchanged part contributes \(M-q\).

Any replacement row with \(a>\delta\) is also initially strictly
between the two tests. It therefore captures them at its endpoint
times, independently of its intervening turns. If its first
endpoint time is \(\sigma\), its direct tour gives pair payoff
\[
 1+\sigma\ge1+a>1+\delta>1+\varepsilon/4.
\tag{12a}
\]
Consequently moving all such replacement mass back to the
endpoint-sweep row can only lower these Princess test payoffs.
This comparison holds for every \(0<\varepsilon<\delta\), not
merely at the two limiting tests. It also includes center starts.

Let \(r\) be the total replacement mass on opposite-first rows
(8) with \(a\le\delta\), and set
\[
 D=\int_{\{A,\ a\le\delta\}} d\,d\mu.
\tag{13}
\]
The integral is signed; in particular
\[
 D\le\delta r.
\tag{14}
\]
All other replacement mass consists of near same-side-first rows,
farther-in rows covered by (12a), and any untouched endpoint sweeps.
Each of these has test payoff at least that of an endpoint sweep.

Let \(\varepsilon\downarrow0\). Every fixed near opposite-first
row has positive \(a\), so (9) tends to \(3-d\). Every other
replacement row has limiting payoff at least one by (12),
(12a), or the endpoint-sweep formula.
The kernels are uniformly bounded, so dominated convergence gives
\[
 \sup_p J_{\widetilde\nu}(p)\ge M+2r-D.
\tag{15}
\]

Next let \(\varepsilon\uparrow\delta\) from below. For an
opposite-first row with \(a<\delta\), (9) tends to
\(1+\delta/4-3d/4\). A row with \(a=\delta\) remains in the first
branch and has the larger limit \(3-d\), because
\[
 (3-d)-(1+\delta/4-3d/4)
 =2-(\delta+d)/4>0.
\]
Same-side-first rows satisfy (12), and the endpoint sweeps satisfy
(6). Dominated convergence therefore gives
\[
 \sup_p J_{\widetilde\nu}(p)
 \ge M+q\delta/4-3D/4.
\tag{16}
\]

Initial atoms do not invalidate either limit. For every fixed
interior start, its initial-equality parameter is eventually
avoided as \(\varepsilon\) approaches either endpoint; atoms at
\(a=\delta\) remain on the explicitly handled strict side.
The true equality values (9) and (11) are retained throughout.

By (14), the right side of (15) is at least
\[
 M+(2/\delta-1)D.
\]
Combine this and (16) with weights
\[
 \lambda=\frac{3\delta}{8-\delta},
 \qquad 1-\lambda=\frac{8-4\delta}{8-\delta}.
\]
The coefficient of \(D\) cancels. Since a supremum dominates
the weighted average of any two of its lower bounds, the result is
\[
 \sup_pJ_{\widetilde\nu}(p)
 \ge M+(1-\lambda)q\delta/4
 =M+\frac{q\delta(2-\delta)}{8-\delta},
\]
proving (4).

This is a response lower bound for each fixed repaired Monster law.
It does not assert a uniform approximation by one finite Princess
mixture as the repair measure varies, nor does it interchange a
limit with an infimum over those measures.

## 4. Exact consequence for the current one-turn law

The independently certified law in
[ONE_TURN_PHYSICAL_UPPER.md](ONE_TURN_PHYSICAL_UPPER.md) has
\[
 q=\frac{158373491249}{250000000000},\qquad
 \delta=\frac1{128},\qquad
 M=\frac{182280512903797}{128000000000000}.
\tag{17}
\]
Its original endpoint-loop floor is
\[
 M+q\delta/4
 =\frac{91219443197523}{64000000000000}
 =1.425303799961296875.
\tag{18}
\]
The saved all-Princess upper exceeds (18) by only
\[
 \frac{9803}{1024000000000000}.
\]
Thus changing clocks alone can gain at most this tiny exact
difference for the fixed physical law.

More strongly, any endpoint-only replacement satisfying (3) has worst
Princess response at least
\[
 \boxed{
 \frac{62211501887219437}{43648000000000000}
 \approx1.4253001715363691.}
\tag{19}
\]
This remains above the target
\(U_*=291849329389899/204800000000000\) by
\[
 \frac{88908487977701}{349184000000000000}
 \approx0.0002546178747528552.
\tag{20}
\]
The largest improvement that theorem (4) even permits over the
old endpoint-loop floor is
\[
 \frac{158373491249}{43648000000000000}
 \approx0.0000036284249278088345.
\tag{21}
\]

Therefore neither a finer calendar nor an arbitrary canonical
one-turn replacement of the endpoint component can establish the
desired upper \(W_1\le U_*\) while the old interior law is held
fixed. Moving replacement starts farther inward does not escape
the obstruction: those rows are covered by (12a). A successful
one-turn modification must change the old interior probabilities,
the old interior paths, or both. This does not rule out such
changes and does not prove \(W_1>U_*\).

## 5. Exact replay

Run:

~~~sh
python3 packages/interval_one_turn/verify_endpoint_repair.py
~~~

The standard-library checker independently intersects the physical
affine paths to check (9), (11), all initial/turn ties, (12), and
the outside-gap comparison (12a), including center starts.
It reads the compact saved one-turn law, checks its physical
geometry and weights, reconstructs \(M,q,\delta\), tests actual
immediate-outward Princesses against that law, and recomputes
every fraction (18)–(21). These finite checks audit the formulas;
the arbitrary-measure statement is proved above by the two limits
and their exact weighted inequality. No CI or Lean result is
claimed.

