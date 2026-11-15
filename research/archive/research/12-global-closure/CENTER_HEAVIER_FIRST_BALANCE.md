# A heavier-first and rank-balance normal form after the center

This strengthens the fixed-field theorem in
**FINITE_POSTCENTER_RESPONSE.md**. It does not classify the Monster's
precenter path or assert that an equilibrium Princess field has a finite
mesh. The separate **COMMON_THRESHOLD_FIXED_CDF_RESPONSE.md** now
provides the complete response theorem for each supplied rational
common-threshold field; the present result simplifies its center
continuation structure.

Fix a symmetric ordered Princess field satisfying that theorem's
assumptions, in particular outward motion after time two. For the
rational common-threshold fields, attainment follows from
**PARAMETRIC_CENTER_VALUE_QUADRATICS.md**. A center state has two
surviving rank masses `L,R <= 1/2`. The continuous interior trace
`F(t,0)=1/2` is part of the hypotheses; general center-atomic laws
are not covered.

**Theorem.** There is a minimum-cost finite center continuation with
all three properties:

1. Each returning triangle and the final endpoint tour initially move
   toward a side with the larger surviving rank mass.
2. These successive outward directions alternate, including the first
   direction of the final tour.
3. After every returning triangle, its affected record is no larger
   than the opposite record.

The original bounds `8n+4` full-width legs and `24n+4` narrow-width
legs remain valid. In particular, if a center state is imbalanced,
with lighter record `l` and heavier record `r>l`, a returned excursion
must reach a peak satisfying

\[
                  1-F(t+h,h)\le l.                         \tag{1}
\]

Reflection supplies the same formula for a negative excursion. Thus
an exact center-response search may remove the lighter-first branch
and every peak strictly before this rank-balance boundary.

## 1. A fixed future path is monotone in its incoming records

For a fixed future physical path, its cost is

\[
 H(L,R)=\int\bigl(\min(L,A(s))+\min(R,B(s))\bigr)\,ds,
                                                               \tag{2}
\]

with endpoint resets included in `A,B`. It is nondecreasing in both
coordinates. Reflection of the physical path interchanges its two
arguments because the Princess law is symmetric.

Consequently, if the sorted pair of new records is coordinatewise
no larger than the sorted pair of old records, either the old
continuation or its reflection has no greater cost from the new
records. This comparison uses exactly the same number of returning
triangles and endpoint-tour legs. It does not replace a finite path
by an unspecified optimal continuation.

## 2. The larger record is always an admissible first choice

Write `0 <= l <= r <= 1/2` and set

\[
 S(t,u)=1-F(t+u,u),\qquad
 I(t,h,z)=\int_0^h\min(z,S(t,u))\,du.
\]

For a triangle of height `0<h<1`, put

\[
                  p=\min(l,S(t,h)),\qquad
                  q=\min(r,S(t,h)).
\]

The outgoing ray has nonincreasing `S`, by the legal transport
inequality. During the returning leg the affected record stays at
its peak value. The other record stays constant. Hence the local
costs of attacking the heavier and lighter sides are respectively

\[
 C_r=2hl+I(t,h,r)+hq,\qquad
 C_l=2hr+I(t,h,l)+hp.                                    \tag{3}
\]

The elementary cap inequalities give

\[
 0\le I(t,h,r)-I(t,h,l)\le h(r-l),\qquad
 0\le q-p\le r-l.
\]

Substitution into (3) proves `C_r <= C_l`.

The lighter-first exit records sort to `(p,r)`. The heavier-first
exit records satisfy the stronger identity and comparison

\[
 \operatorname{sort}(l,q)
   =\bigl(p,\max(l,q)\bigr)\le(p,r).                       \tag{4}
\]

Apply Section 1 to the complete original future path. Attacking the
heavier side at the same height, followed by the appropriate original
or reflected continuation, therefore has no greater complete cost
and uses the same number of triangles. This remains true when the
triangle makes no new record or the records tie.

For a direct endpoint tour, the two costs are

\[
                D_r=3l+I(t,1,r),\qquad
                D_l=3r+I(t,1,l).
\]

The same cap inequality now yields

\[
                       D_r-D_l\le-2(r-l).                  \tag{5}
\]

Thus a strictly heavier side is the unique preferred initial side
among the two direct tours. The formula uses the existing
outward-after-two endpoint-tour reduction; it is not asserted for
an arbitrary Princess law without that hypothesis.

## 3. Greedy orientation and minimum triangle count can coexist

Among the attained optimal finite center continuations, choose one
with the fewest returning triangles. At its first triangle, apply
Section 2 if its direction is lighter-first. The reflected or
unreflected future is an actual path with the same triangle count.
The resulting complete cost cannot fall below the optimum, so the
replacement remains optimal and still has the minimum count.

Proceed chronologically through its finitely many triangles. A
replacement changes only the current triangle and its later
continuation; earlier choices remain fixed. Finally orient the
endpoint tour using (5). The result is both optimal with minimum
triangle count and heavier-first at every center departure.

This argument does not assume that an arbitrary optimal continuation
selected from a value function happens to preserve the minimum
triangle count.

## 4. Minimum-count excursions alternate

Suppose two adjacent returning triangles have the same sign, with
heights `h1,h2` and total height `H=h1+h2`.

If `H<1`, replace them by the one triangle of height `H` with the
same entry and exit times. On that whole interval the replacement
is pointwise at least as far outward on their common side. Spatial
CDF monotonicity makes its affected running survival record no
larger at every time. The opposite record is unchanged. Its local
cost and every common future cost therefore do not increase, but
it uses one fewer triangle.

If `H>=1`, an out-of-arena triangle is not used. The original combined
segment remains on one side for at least two units of time. The
one-sided long-excursion argument of
**FINITE_POSTCENTER_RESPONSE.md**, Section 3, replaces this entire
segment and its future by the direct endpoint tour toward its sign.
The same-side survivors are caught no later by immediate outward
travel. Opposite-side survivors cannot be caught before a subsequent
departure toward the opposite side at or after time `t+2>=2`;
outward forcing then
prevents their interior capture, and their endpoint cannot be
reached before `t+3`. The direct tour reaches it at `t+3`.
Again the returning triangle count decreases without increasing
cost.

Finally, a last returning triangle followed by a tour initially
going toward the same side is a one-sided center-to-first-endpoint
prefix followed by the opposite sweep. The direct tour toward that
side dominates it by the same Section 3 argument and deletes that
last triangle.

Each case contradicts minimum triangle count. Thus the outward
directions alternate, including the final tour's first direction.
At the next center departure, the opposite side must therefore be
at least as heavy as the just-attacked side. This proves property 3
and, when `l<r`, inequality (1).

### Center holding intervals

The finite-response theorem used here already supplies a no-hold
normal form, even when the original center zero set has positive
measure. No holding intervals are silently omitted from that
starting theorem.

If a recurrence separately includes a center hold, it need not
create an additional case. Such a hold keeps both surviving records
constant because `F(t,0)=1/2` and both records are at most `1/2`.
Absorb a hold of length `w` immediately
before a triangle into the single outward tent over their combined
duration `w+2h`. This tent pointwise dominates the hold and triangle
on their common side and has height `h+w/2`. Use it when that height
is less than one. At height at least one, use the preceding legal
direct-tour argument instead. A hold before the final tour is a
one-sided prefix to its first endpoint and is removed by the same
direct-tour dominance. These operations do not increase the number
of returning triangles. They also handle two same-sign triangles
separated by a hold. If both records are zero, choose a direct tour
with zero cost and no returning triangle. If a positive record
remains, an infinite center hold has infinite remaining cost.

## 5. A reduced exact center recurrence

Let `Qhat(t,l,r)` denote the center value on the ordered wedge
`0<=l<=r<=1/2`. With `q_h=min(r,S(t,h))`, the complete recurrence is

\[
\begin{split}
 \widehat Q(t,l,r)=\min\bigg\{&3l+I(t,1,r),\\
 &\inf_{\substack{h\in\mathcal H(t)\\q_h\le l}}
 \left[2hl+I(t,h,r)+h q_h
       +\widehat Q(t+2h,q_h,l)\right]\bigg\},               \tag{6}
\end{split}
\]

where a proper returning height satisfies
`0<h<1` and may be restricted to `h<=2-t` for `t<2`, by the
established peak-shortening argument. After time two,

\[
                         \widehat Q(t,l,r)=3l+r.
\]

For the operational finite-depth construction, start with the direct
tour and iterate the right side of (6). The same proof works with
any fixed triangle budget: reuse the complete old continuation in
Section 2 and choose a minimizing route with the fewest triangles
within that budget. Thus the constrained recurrence equals the
unconstrained two-sign recurrence at each depth, and depth `2m+1`
is still complete.

When `l<r`, its height constraint is exactly `S(t,h)<=l`. Since `S`
is nonincreasing along the outward ray, this deletes an initial
interval of heights, not a disconnected guessed test bank. On the
balanced diagonal retain `q_h<=l` as written; replacing it by
`S(t,h)<=l` would incorrectly delete a possible no-new-record
excursion when the two records already tie.

All records after a returned triangle interlace:

\[
            (l,r)\longmapsto(q_h,l),\qquad q_h\le l.
\]

This is a structural restriction on the record dynamics of an exact
fixed-field response. It supplies neither a finite precenter bound
nor a family containing an optimal unrestricted Princess field.

## 6. Verification and remaining scope

`packages/interval_global_closure/verify_center_heavier_first.py`
uses only Python `Fraction` arithmetic. It independently checks the
cap inequalities, sorted-record identity, and reflected continuation
comparison for finite monotone cost envelopes. It also checks the
pointwise merging of same-sign triangles, including intervening
center holds. These are
regressions of the algebra; the universal statement follows from
the proof above and the cited finite-response and endpoint lemmas.

The equilibrium step remains: construct a Princess field and a
causal physical Monster law satisfying both unrestricted saddle
inequalities, or prove an equilibrium-sufficient field class and
solve it. The complete finite response theorem for each supplied
field in **COMMON_THRESHOLD_FIXED_CDF_RESPONSE.md** does
not bound the complexity of the Princess fields that must be
considered. The rank-balance restriction alone does neither.
