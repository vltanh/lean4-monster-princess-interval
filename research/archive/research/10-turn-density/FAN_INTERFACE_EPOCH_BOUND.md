# A scale-free bound inside one stationary-interface epoch

## Status

The fixed-interface inequalities in this note are proved and exactly checked. The final global charging step is **open**. No uniform global turn cap or finite-family game claim follows yet.

Inputs are a continuous ordered CDF arising from a fixed positive-width fan of piecewise unit/wait paths, and a finite time horizon \(H\). Its interior CDF is piecewise affine, with a finite spatial Lipschitz constant \(M\). Characteristic edges have slopes \(+1,-1\); stationary edges have slope \(0\).

The arbitrary-old-record local bridge is `AFFINE_HALF_CELL_BRIDGE.md`, using the explicit old-band extension of `INITIAL_INTERFACE_RETURN_BLOCK.md`.

## 1. Exact time slabs and the initial cone

Partition time at profile vertices and every edge-intersection time. No new approximation grid is introduced. In an open slab ending at \(b\), fix a stationary interface \(x=c\). Continuity gives the same temporal coefficient on both sides:
\[
F(t,x)=F(s,c)+\alpha(t-s)+\beta_\pm(x-c).
\]

Let \(\Delta>0\) be a lower bound for the distance to every different stationary interface and relevant physical boundary. Consider a first visit \((s,c)\) in this slab, and set \(R=b-s\).

A characteristic edge moving away from \(c\) cannot enter the forward unit cone from \((s,c)\). An edge approaching \(c\) would meet \(c\) no earlier than the next slab boundary, so its initial distance is at least \(R\). It cannot meet the expanding forward cone before time \(R/2\).

Thus the same two-half-cell formula holds in the forward cone through
\[
h=\min(\Delta,R/2).
\]
Coincident characteristic edges at the source lie on the cone boundary; continuity gives the same CDF values there.

For \(\alpha>0\), put \(C=\beta_--\alpha>0\) and
\[
\gamma=\beta_-/C+1/2,\qquad d=h/\gamma.
\]
The local normal form can be applied over \([s,s+d]\), because its required future trace remains in the common cone through \(s+\gamma d=s+h\). For \(\alpha<0\), exchange sides and rank signs.

The exact scale cancellation is
\[
\frac Rd=\gamma\max(R/\Delta,2)
\le\gamma\max(H/\Delta,2).
\]
It is essential to retain \(R\), rather than replace it prematurely by \(H\) in the numerator \(R/d\). This is what makes the bound uniform as \(s\) approaches \(b\).

## 2. Productive opposing excursions

At the first interface visit, the running lower rank record is at most \(F(s,c)\). It can only decrease afterward.

Take a later left excursion, beginning at interface time \(u\), returning after duration \(q\), with no intervening boundary event changing this affine half cell. Its lowest possible CDF is attained by the maximal left tent and equals
\[
F(s,c)+\alpha(u-s)-Cq/2.
\]
Therefore a productive new lower record requires
\[
q>\frac{2\alpha(u-s)}C.
\]
In particular, if \(u\ge s+d\), it requires \(q>2\alpha d/C\). Disjoint productive opposing excursions before \(b\) are consequently bounded by
\[
\frac{RC}{2\alpha d}
=\frac{C\gamma}{2\alpha}\max(R/\Delta,2).
\]
One excursion straddling \(s+d\) can be counted separately.

A nonproductive opposing excursion is dominated by interface waiting. This comparison needs no future-persistence assumption. Do not normalize a long productive left excursion with the earlier tent lemma unless its separate persistence hypothesis is satisfied.

## 3. The stronger rank-width gate

If the path returns to the interface at any time \(r\ge s+d\), then
\[
H_r-L_r\ge F(r,c)-F(s,c)\ge\alpha d.
\]
This positive captured width persists.

Inside the physical interval, the CDF trace along any legal Monster is \(2M\)-Lipschitz. Switching between productive upper and lower capture fronts therefore takes at least \(\alpha d/(2M)\) units of time. The number of later productive front alternations within the slab is bounded by
\[
\frac{2MR}{\alpha d}
\le\frac{2M\gamma}{\alpha}\max(H/\Delta,2).
\]
Endpoint capture jumps are handled separately: once an extreme rank is captured, that record cannot expand again.

For a phase with no new lower captures, the pointwise maximal legal bridge between its fixed time/position endpoints captures every new upper rank no later. The corresponding minimal bridge works for a lower-only phase. Nonproductive gaps may be included in an adjacent phase. Each such bridge has at most three affine pieces, including a possible boundary wait.

The first crossing piece after \(s+d\), before a first later interface return, is not covered by this positive-width estimate. It requires an affine-cell face reduction or a separately charged boundary event.

## 4. What the finite event census supplies

On a fixed characteristic line segment, \(m(t)-t\) or \(m(t)+t\) is monotone. Its contact set is one interval. A newly introduced contact on the same characteristic after a frozen old contact forces the entire intervening path to follow that characteristic. This is useful for a monotone face-charging construction.

A transfer between different stationary positions costs at least \(\Delta\) in spatial variation. There are at most \(H/\Delta\) such transfers. The number of characteristic edge pieces and exact time slabs is finite.

When \(\alpha=0\), the two half cells are static. Each side can create only its corresponding record, so maximal same-side tents are pointwise dominant without future-rank credit. The zero-flux case must be treated by this static reduction; the formulas dividing by \(\alpha\) do not apply to it.

## 5. The exact remaining global gate

The local and epoch results do not yet establish a global finite atlas count.

A complete proof must normalize the first crossing piece and strict affine-cell traversals while charging every newly active face to the *same evolving path*. It must show that:

1. creating a characteristic contact cannot repeatedly consume an already counted contact in unrelated deformations;
2. transfers to different stationary positions are charged against the actual path's finite spatial variation;
3. same-interface contacts created by an affine vertex reduction either trigger the positive-width gate, lie in the controlled initial fraction, or are nonproductive and removable; and
4. endpoint, center, and exact time-slab boundaries preserve the strict/closed record conventions.

The connected characteristic-contact interval is a promising mechanism for item1. It is not a substitute for the full causal construction. In particular, adding counts taken from separate modified paths would not prove a bound on a single normal form.

Existence of some finite-piece optimal response, or compactness by itself, does not provide this explicit global count.

## 6. Exact checks

`verify_interface_epoch.cjs` verifies the scale cancellation, forward-cone margins, and opposing-record inequality using exact rational arithmetic and arbitrary left piece fixtures. The report is `interface_epoch_checks.json`.

These checks concern only the proved epoch lemma. They do not certify the open charging construction.
