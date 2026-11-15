# Two directional runs suffice when the continuation is included

Independently reviewed proof, 2026-11-13.

This strengthens the fixed-field response reduction, but uses a different
local invariant from FOUR_LEG_AFFINE_RECORD_RESPONSE.md. It does **not**
preserve the two exit records. Instead it includes the cost of the fixed
future physical continuation, which is concave in those records.

## 1. Scalar statement and the continuation cost

Let a scalar path satisfy

\[
 -\beta\le Y'\le\alpha,\qquad
 Y(0)=0,\quad Y(T)=f,\qquad \alpha,\beta>0.
\]

Its entry record interval is \([-a,b]\), with \(a,b\ge0\).
Write its exit record interval as \([-B,H]\), and its running range as
\(\mathcal R(t)\). Let \(g(B,H)\) be any finite concave function that is
nonincreasing in each variable on the relevant record domain.

Consider the total cost

\[
 J(Y)=T-\int_0^T\mathcal R(t)\,dt+g(B,H).
\]

Put

\[
 p=\frac1\alpha,\qquad q=\frac1\beta,\qquad
 \kappa=p+q,\qquad
 A=\frac{T+qf}{\kappa},\qquad
 C=\frac{T-pf}{\kappa}.
\]

Then \(A,C\ge0\), \(A-C=f\), and \(pA+qC=T\).
The two pure-order paths are:

* \(Y_U\): travel upward by \(A\), then downward by \(C\);
* \(Y_D\): travel downward by \(C\), then upward by \(A\).

Both use maximal directional speeds, have duration \(T\), and end at
\(f\).

**Theorem.**

\[
 \boxed{\min\{J(Y_U),J(Y_D)\}\le J(Y).}
\]

In the Princess game, \(g\) has the required form. Fix the future
physical continuation after the cell, including its endpoint contacts.
In absolute rank coordinates, let \(L(s),U(s)\) denote the minimum
strict CDF and maximum inclusive CDF seen in that continuation by
relative time \(s\). If the current scalar origin is the rank \(y_0\),
its remaining capture cost is

\[
 g(B,H)=
 \int_0^{T_{\rm rem}}
 \left[
   \min(y_0-B,L(s))+1-\max(y_0+H,U(s))
 \right]\,ds.
\]

Each integrand is concave and nonincreasing in \(B,H\). The finite
normalized completion horizon makes this function finite and continuous.
Actual endpoint jumps are included in \(L,U\); they do not affect this
concavity.

It is enough to prove the theorem for \(f\ge0\). Reflection exchanges
\(a,b\), \(\alpha,\beta\), and the two pure-order paths when \(f<0\).

## 2. The fixed-record four-leg reduction

Apply the four-leg theorem while keeping the exit records fixed.
It weakly decreases the local cost and leaves \(g\) unchanged.
When only one record is new, the pure-order path directed first toward
that new record already dominates: it visits every such level at its
earliest possible time and can only enlarge the other record.

When both records are new, it remains to consider:

* a tour of the two global records, followed by \(f\) and a final hold;
* one initial partial record excursion, the two global records,
  and \(f\).

By the four-candidate envelope, a genuinely useful partial excursion
uses all available time. An unused-time partial excursion can be moved
to an endpoint of its concave one-variable cost interval; that endpoint
either removes the partial excursion or uses all time.

## 3. A partial excursion is unnecessary for the full cost

Consider first a partial right excursion

\[
 r,\ -B,\ H,\ f.
\]

Here \(b\le r\le H\), \(B\ge a\), \(H\ge f\), and the active duration
constraint is

\[
 r+B+H=S,\qquad S=\frac{T+qf}{\kappa}.
\]

Ignoring constants independent of the turns, the exact local capture
cost is

\[
 -T(B+H)+\frac{pH^2+qB^2}{2}
 +\kappa\bigl[BH+r(H-a)-r^2\bigr].
\]

Eliminate \(H=S-r-B\). Its Hessian in \((r,B)\) is

\[
 \begin{pmatrix}
 -3p-4q&-p-2q\\
 -p-2q&-p-q
 \end{pmatrix}.
\]

The upper left entry is negative and the determinant is
\(p(2p+3q)>0\), so this quadratic is strictly concave.
Adding the concave continuation term \(g(B,S-r-B)\) preserves concavity.

A minimum therefore occurs at a vertex of the two-dimensional
polytope cut out by

\[
 r\ge b,\quad r\le H,\quad B\ge a,\quad H\ge f,\quad
 r+B+H=S.
\]

Every vertex has at least one of

\[
 r=b,\qquad r=H,\qquad B=a.
\]

Indeed, otherwise only the face \(H=f\) could be active in addition to
the affine sum, leaving a nontrivial two-sided perturbation.

If \(r=b\), the initial excursion reaches only an old upper record and
can be removed. If \(r=H\), the first visit already reaches the global
upper record, and the later return to that same record is unnecessary.
Both cases reduce to a tour of the two global records with a final hold.
If \(B=a\), no lower record is new, and \(Y_U\) dominates directly.

For a partial left excursion

\[
 -l,\ H,\ -B,\ f,
\]

the same computation with the reflected rates gives strict concavity on
the active sum plane \(l+H+B=(T-pf)/\kappa\).
Because \(f\ge0\), the remaining constraints are

\[
 a\le l\le B,\qquad H\ge\max(b,f).
\]

Every vertex has \(l=a\) or \(l=B\), and either equality removes the
partial excursion. Thus a two-global-record tour always suffices for
the full cost.

## 4. Reduce a two-global-record tour to an old or terminal record

For the low-first tour \(-B,H,f\), the local capture cost is

\[
 T-T(B+H)
 +\frac{p(H^2-b^2)+q(B^2-a^2)}2
 +\kappa B(H-b).
\]

For the high-first tour \(H,-B,f\), replace the last term by
\(\kappa H(B-a)\).

Fix the sum \(s=B+H\). Each local cost has quadratic coefficient
\(-\kappa/2\) in \(B\), after substituting \(H=s-B\).
Adding \(g(B,s-B)\) gives a concave function on the interval

\[
 B\ge a,\qquad H\ge\max(b,f).
\]

Both the fixed duration and the final holding time depend only on this
sum for the chosen order. Hence at least one endpoint of the interval
has no larger full cost.

At \(B=a\), no lower record is new, so \(Y_U\) dominates.
If \(H=b\ge f\), no upper record is new, so \(Y_D\) dominates.
The only remaining case is

\[
 H=f>b.
\]

## 5. The terminal upper record

### 5.1 Low-first order

The path is \(-B,f\), followed by a hold. Fill this hold by continuing
the upward leg beyond \(f\), then returning to \(f\). Existing first
visits are unchanged; only additional upper levels are captured.
The new upper record is

\[
 H'=A-B,\qquad B+H'=A,
\]

and the new tour uses all time. Apply the fixed-sum concavity argument
again, now at sum \(A\). At one endpoint \(B=a\), the pure path \(Y_U\)
dominates. At the other \(H=f\), one has \(B=A-f=C\), and the resulting
path is exactly \(Y_D\).

### 5.2 High-first order

The path is \(f,-B,f\), followed by a hold. Use any holding time to
extend its negative excursion. This retains all old first visits and
only captures additional negative levels. It yields the full-time tour

\[
 Y_V:\quad f,\ -(C-f),\ f,
\]

where necessarily \(C\ge a+f\). Put
\(\theta=f/C\in(0,1]\).

The exit records of the three paths are

\[
 \begin{array}{c|cc}
  &B&H\\ \hline
 Y_U&a&C+f\\
 Y_D&C&f\\
 Y_V&C-f&f.
 \end{array}
\]

The \(\theta,1-\theta\) mixture of the pure-order records has

\[
 \overline B=C-f+\frac{af}{C}\ge C-f,\qquad
 \overline H=2f\ge f.
\]

Consequently, concavity and monotonicity give

\[
 \theta g(Y_U)+(1-\theta)g(Y_D)
 \le g(\overline B,\overline H)
 \le g(Y_V).
\]

The same mixture has at least as much integrated captured range.
Write \(\mathcal A_U,\mathcal A_D,\mathcal A_V\) for those three
integrals. Direct first-visit accounting gives

\[
 \begin{aligned}
 C\bigl[\theta\mathcal A_U+(1-\theta)\mathcal A_D-\mathcal A_V\bigr]
 ={}&
 \kappa bC(C-f)
 +\frac{pfC^2}{2}
 +\frac{qf(C^2-a^2)}{2}\\
 &+\frac{qf^2C}{2}+paf^2.
 \end{aligned}
\]

Every term is nonnegative, since \(C\ge a+f\), \(a,b,f\ge0\),
and \(p,q>0\). Hence the mixture's full cost is no greater than
that of \(Y_V\); one of its two pure paths has no greater cost.

This completes the scalar proof.

## 6. Degenerate slopes

If \(\beta=0<\alpha\), the scalar value is nondecreasing.
Putting all upward movement first visits every new scalar level as
early as possible, so the corresponding pure physical order dominates.
If \(\alpha=0<\beta\), use the reflected order.
If both slopes are zero, the scalar records remain constant and either
physical pure order has the same local and continuation cost.

No division by a zero slope is needed in these branches.

## 7. Consequences for a fixed characteristic CDF mesh

In an affine cell

\[
 F(t,x)=F_0+bU-cV,\qquad U=t+x,\quad V=t-x,
\]

the scalar rates are \(\alpha=2b,\beta=2c\).
For fixed physical entry and exit points, the two pure orders are
particularly simple:

* first increase \(U\), then \(V\);
* first increase \(V\), then \(U\).

Their turn points are respectively
\((U_{\rm exit},V_{\rm entry})\) and
\((U_{\rm entry},V_{\rm exit})\).
Their physical velocities are only \(+1,-1\); there is no
field-dependent constant-level velocity.

For ordinary interior characteristic triangles or merged center
rectangles, both paths remain in the coordinatewise entry-exit box
inside the cell.

**Boundary restriction.** This implication cannot automatically be
extended to a physical boundary half-cell. Its coordinate box can leave
the strip, and the two pure orders can then make the affine extension
exceed the rank interval \([0,1]\). The earlier boundary projection proof
requires the hypothetical scalar values to remain in that interval.
Use the established four-directional-leg plus constant-level
replacement for such a boundary cell.

Apply the theorem successively to the cells of a fixed response path,
each time using that path's entire current future continuation to
define \(g\). The full capture cost never increases. The physical cell
entry and exit points are preserved until a first endpoint permits
normalization of the whole remainder.

Thus, with \(K_{\rm int}\) interior affine cells and \(K_{\rm bd}\)
physical boundary half-cells in the characteristic strip through time
\(H+2\), a best response to an absorbed-by-\(H\) fixed field can be
chosen with at most

\[
 \boxed{2K_{\rm int}+5K_{\rm bd}+1}
\]

physical pieces, including its final opposite-endpoint sweep.
All interior-cell pieces have unit speed. Center halves are merged as
before, and endpoint/zero-time branches remain included.

This is a fixed-field response theorem. It does not establish that the
globally optimal Princess field belongs to any fixed finite mesh.

## 8. Computational interpretation

For fixed entry and exit points in an interior cell, there are exactly
two local physical candidate paths. No continuous partial-turn
parameter or exit-record optimization remains inside that cell.

The transition updates are maxima and minima of the old records and
the affine CDF values at the two endpoints and the selected corner.
On a fixed ordering branch these updates are affine; the cell capture
cost is rational quadratic for a rational field. One can therefore use
record-state Bellman functions on mesh edges, with two corner
transitions per entry-exit pair, in place of future-clock queues.

The exit point along an edge remains a continuous decision. This
theorem alone does not turn the response into a finite graph shortest
path or the joint Princess optimization into a finite linear program.
